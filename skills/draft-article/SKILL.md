---
name: draft-article
description: Draft a blog post, journalistic article or press-style summary from an eval's findings memo, for a general or specialist audience. Writes findings/<run_id>/article-<audience>.md and hands publishing to the blog skills. Use when the user says "write a blog post about the eval", "turn the findings into an article", "draft a piece for journalists", or "pitch this to a publication".
---

# Draft an article

Evals often turn into blog posts or journalism. This skill writes the draft. It works
**only** from the verified findings memo, so nothing reaches prose that wasn't checked
against the data.

**References.** Read `../../references/pitfalls.md` item 19. If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.

## Inputs

- `findings/<run_id>/findings.md` and `numbers.json`, which must have passed
  `analyse-findings`' mechanical verification. If they haven't, run that first.
- `exports/<run_id>/` for charts and excerpts.
- The format, if the user named one. Otherwise default to a blog post.

| Format | Reader | Shape |
|---|---|---|
| `blog` | Technical readers of the user's blog | First person, 800–1500 words: why I built this, how it works, what I found, caveats, links to repo and datasets |
| `feature` | General-interest readers | Leads with the most concrete finding and one vivid verbatim excerpt. Method is explained without jargon. Limitations are in the body, not a footnote |
| `brief` | Journalists and editors | One page: headline finding, three supporting numbers, two excerpts, method in three sentences, limitations, links, contact |
| `thread` | Social | 5–8 short posts, each one claim with its number, ending with links |

## Steps

1. **Check visibility.** An article links to the repo and datasets. If any artifact it
   would cite is private (an eval created private on request), say which ones and ask
   whether to run `go-public` first, or to draft anyway for later (the links are
   marked `[private]` in the draft). If the cited run hasn't had the `go-public`
   review, offer it in one line.
2. **Choose the angle** from the memo's headline findings, the ones most concrete and
   best supported. Propose the angle and a title in one line, then write. Don't wait
   for approval of an outline.
3. **Write** `findings/<run_id>/article-<format>.md`:
   - Every number and excerpt is copied from `numbers.json` and `findings.md`. Never
     round in a way that changes the claim, and give n where a rate appears.
   - Keep the evidence tiers in the substance even without the labels. Measured
     results are stated as facts, and readings as readings ("one explanation is…").
   - Name the limitations in the body. "Twelve prompts per topic, one judge model" is
     a sentence, not a footnote.
   - Use the user's email and writing style guide where one exists
     (`references/email-style.md` in the Google-Workspace plugin): short sentences,
     not promotional, no emojis.
   - Embed charts from `exports/<run_id>/charts/` by relative path.
4. **Verify** with the same script as `analyse-findings` step 5, pointed at the article:
   every number in `numbers.json`, every excerpt verbatim in `responses.jsonl`.
5. **Commit** the draft. Don't publish it.
6. **Hand-off, on request only.** For the user's blog, use
   the blog tooling named in the overlay, if any, with the draft. Publishing
   a post is an outward action, so confirm first. For a journalist brief, the user
   sends it. If asked to email it, use whatever mail tool the user has.
