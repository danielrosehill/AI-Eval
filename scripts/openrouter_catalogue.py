#!/usr/bin/env python3
"""OpenRouter catalogue helper for the ai-eval plugin. Standard library only.

  fetch     --out FILE                        snapshot /api/v1/models (no key needed)
  new       --catalogue FILE --days N         models released in the last N days
  filter    --catalogue FILE --requirements FILE [--out FILE]
  estimate  --catalogue FILE --requirements FILE --candidates FILE
            [--outputs N] [--judge SLUG] [--cap USD]
  endpoints SLUG                              providers serving one model
  key                                         key limit and usage (OPENROUTER_API_KEY)
  ping      --candidates FILE | SLUG [SLUG…]  one tiny paid call per model (needs key)

Output is JSON on stdout.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone

API = "https://openrouter.ai/api/v1"


def call(path, body=None, key=None, timeout=60):
    headers = {"Content-Type": "application/json", "User-Agent": "ai-eval-plugin"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"error": {"message": raw[:300]}}
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, {"error": {"message": str(e)}}


def need_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set")
    return key


def per_million(value):
    return round(float(value or 0) * 1_000_000, 4)


def normalise(m):
    arch = m.get("architecture") or {}
    price = m.get("pricing") or {}
    top = m.get("top_provider") or {}
    reasoning = m.get("reasoning") or {}
    return {
        "id": m["id"],
        "name": m.get("name"),
        "lab": m["id"].split("/")[0],
        "released": datetime.fromtimestamp(m.get("created", 0), timezone.utc).date().isoformat(),
        "context": m.get("context_length") or 0,
        "max_output": top.get("max_completion_tokens"),
        "input_modalities": arch.get("input_modalities") or [],
        "output_modalities": arch.get("output_modalities") or [],
        "usd_per_m_in": per_million(price.get("prompt")),
        "usd_per_m_out": per_million(price.get("completion")),
        "parameters": m.get("supported_parameters") or [],
        "reasoning_default": reasoning.get("default_enabled"),
        "reasoning_mandatory": reasoning.get("mandatory"),
        "reasoning_efforts": reasoning.get("supported_efforts"),
        "knowledge_cutoff": m.get("knowledge_cutoff"),
        "expires": m.get("expiration_date"),
    }


def load(path):
    with open(path) as f:
        return json.load(f)


def cost_per_output(model, tokens):
    out = tokens.get("output", 0) * tokens.get("reasoning_overhead", 1)
    return (tokens.get("input", 0) * model["usd_per_m_in"] + out * model["usd_per_m_out"]) / 1_000_000


def cmd_fetch(a):
    status, body = call("/models")
    if status != 200:
        sys.exit(f"GET /models returned {status}: {body}")
    models = sorted((normalise(m) for m in body["data"]), key=lambda m: m["released"], reverse=True)
    snapshot = {"fetched": date.today().isoformat(), "count": len(models), "models": models}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(snapshot, f, indent=1)
    print(json.dumps({"out": a.out, "count": len(models), "newest": [m["id"] for m in models[:5]]}, indent=1))


def cmd_new(a):
    cutoff = (date.today() - timedelta(days=a.days)).isoformat()
    hits = [m for m in load(a.catalogue)["models"] if m["released"] >= cutoff]
    print(json.dumps([{k: m[k] for k in ("id", "released", "context", "usd_per_m_in", "usd_per_m_out")} for m in hits], indent=1))


def reject_reason(m, hard, tokens, today):
    if m["usd_per_m_in"] < 0 or m["usd_per_m_out"] < 0:
        return "router_or_dynamic_price"
    if hard.get("exclude_free", True) and m["usd_per_m_in"] == 0 and m["usd_per_m_out"] == 0:
        return "free_tier"
    if m["expires"] and str(m["expires"])[:10] <= today:
        return "expired"
    if m["id"] in hard.get("exclude_ids", []):
        return "excluded_id"
    if m["lab"] in hard.get("exclude_labs", []):
        return "excluded_lab"
    if not set(hard.get("input_modalities", ["text"])) <= set(m["input_modalities"]):
        return "input_modality"
    if not set(hard.get("output_modalities", ["text"])) <= set(m["output_modalities"]):
        return "output_modality"
    if m["context"] < hard.get("min_context", 0):
        return "context_too_small"
    if m["max_output"] is not None and m["max_output"] < hard.get("min_max_output", 0):
        return "max_output_too_small"
    if not set(hard.get("required_parameters", [])) <= set(m["parameters"]):
        return "missing_parameter"
    if hard.get("released_after") and m["released"] < hard["released_after"]:
        return "too_old"
    cap = hard.get("max_cost_per_output_usd")
    if cap is not None and cost_per_output(m, tokens) > cap:
        return "over_cost_cap"
    return None


def cmd_filter(a):
    req = load(a.requirements)
    hard, tokens = req.get("hard", {}), req.get("tokens", {})
    today = date.today().isoformat()
    kept, dropped = [], {}
    catalogue = load(a.catalogue)
    for m in catalogue["models"]:
        reason = reject_reason(m, hard, tokens, today)
        if reason:
            dropped[reason] = dropped.get(reason, 0) + 1
        else:
            kept.append({**m, "usd_per_output": round(cost_per_output(m, tokens), 5),
                         "max_output_unknown": m["max_output"] is None})
    kept.sort(key=lambda m: m["usd_per_output"])
    result = {"catalogue_date": catalogue["fetched"], "total": catalogue["count"],
              "kept_count": len(kept), "dropped": dropped, "kept": kept}
    if a.out:
        with open(a.out, "w") as f:
            json.dump(result, f, indent=1)
        result = {k: v for k, v in result.items() if k != "kept"}
        result["out"] = a.out
    print(json.dumps(result, indent=1))


def cmd_estimate(a):
    models = {m["id"]: m for m in load(a.catalogue)["models"]}
    req = load(a.requirements)
    tokens = req.get("tokens", {})
    outputs = a.outputs or req.get("sampling", {}).get("outputs_per_model", 2)
    rows, missing, total = [], [], 0.0
    for c in load(a.candidates)["candidates"]:
        m = models.get(c["id"])
        if not m:
            missing.append(c["id"])
            continue
        each = cost_per_output(m, tokens)
        rows.append({"id": c["id"], "usd_per_output": round(each, 5), "usd_total": round(each * outputs, 4)})
        total += each * outputs
    judge_total = 0.0
    if a.judge:
        j = models.get(a.judge)
        if not j:
            sys.exit(f"judge {a.judge} is not in the catalogue")
        judged = {"input": tokens.get("output", 0) + 1500, "output": 500}
        judge_total = cost_per_output(j, judged) * outputs * len(rows)
    grand = total + judge_total
    rows.sort(key=lambda r: r["usd_total"], reverse=True)
    result = {"models": len(rows), "outputs_per_model": outputs, "generation_usd": round(total, 4),
              "judge_usd": round(judge_total, 4), "total_usd": round(grand, 4),
              "not_in_catalogue": missing, "per_model": rows}
    if a.cap is not None:
        result["cap_usd"] = a.cap
        result["within_80pct_of_cap"] = grand <= a.cap * 0.8
    print(json.dumps(result, indent=1))


def cmd_endpoints(a):
    status, body = call(f"/models/{a.slug}/endpoints")
    if status != 200:
        sys.exit(f"endpoints for {a.slug} returned {status}: {body}")
    rows = [{k: e.get(k) for k in ("provider_name", "quantization", "context_length", "max_completion_tokens",
                                   "status", "uptime_last_30m")}
            for e in body["data"].get("endpoints", [])]
    print(json.dumps({"id": a.slug, "endpoints": rows}, indent=1))


def cmd_key(_):
    status, body = call("/key", key=need_key())
    if status != 200:
        sys.exit(f"GET /key returned {status}: {body}")
    d = body["data"]
    print(json.dumps({k: d.get(k) for k in ("limit", "limit_remaining", "usage", "is_free_tier")}, indent=1))


def cmd_ping(a):
    key = need_key()
    slugs = list(a.slugs)
    if a.candidates:
        slugs += [c["id"] for c in load(a.candidates)["candidates"]]
    rows, spent = [], 0.0
    for slug in slugs:
        started = time.time()
        status, body = call("/chat/completions", key=key, timeout=120, body={
            "model": slug, "max_tokens": 64,
            "messages": [{"role": "user", "content": "Reply with the single word: ready"}]})
        usage = body.get("usage") or {}
        cost = usage.get("cost") or 0
        spent += cost
        ok = status == 200 and bool(body.get("choices"))
        rows.append({"id": slug, "ok": ok, "status": status, "provider": body.get("provider"),
                     "seconds": round(time.time() - started, 1), "usd": cost,
                     "error": None if ok else (body.get("error") or {}).get("message")})
    print(json.dumps({"pinged": len(rows), "ok": sum(r["ok"] for r in rows), "spent_usd": round(spent, 7), "rows": rows}, indent=1))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("fetch"); s.add_argument("--out", required=True); s.set_defaults(fn=cmd_fetch)
    s = sub.add_parser("new"); s.add_argument("--catalogue", required=True); s.add_argument("--days", type=int, default=14); s.set_defaults(fn=cmd_new)
    s = sub.add_parser("filter"); s.add_argument("--catalogue", required=True); s.add_argument("--requirements", required=True); s.add_argument("--out"); s.set_defaults(fn=cmd_filter)
    s = sub.add_parser("estimate"); s.add_argument("--catalogue", required=True); s.add_argument("--requirements", required=True); s.add_argument("--candidates", required=True)
    s.add_argument("--outputs", type=int); s.add_argument("--judge"); s.add_argument("--cap", type=float); s.set_defaults(fn=cmd_estimate)
    s = sub.add_parser("endpoints"); s.add_argument("slug"); s.set_defaults(fn=cmd_endpoints)
    s = sub.add_parser("key"); s.set_defaults(fn=cmd_key)
    s = sub.add_parser("ping"); s.add_argument("slugs", nargs="*"); s.add_argument("--candidates"); s.set_defaults(fn=cmd_ping)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
