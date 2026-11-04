---
name: go-public
description: Pre-publication review for an eval. Use it to take an eval that was explicitly created private public (in whole or in part), or to review a public eval before its results are promoted or cited. Checks method, model selection, git history for credentials, dead links and logged-out access, flips any private artifacts to public, and registers the eval. Use when the user says "make this eval public", "open-source the prompts", "review before I cite this", "is this ready to share", or before draft-article cites a run.
---

# Pre-publication review

Evals are public from creation (see "Lifecycle" in `conventions.md`). This skill has
two uses:

- **An eval created private** on the user's request: review it, then flip the
  artifacts the user chooses to public. All three, or one or two, are equally valid.
- **A public eval before its results are promoted** (cited in an article, a topic
  section of an index, a post): run the same review. Skip the flip.

| Artifact | Typical reason it was kept private |
|---|---|
| Code repo (method, rubric, harness, reports) | Method still changing |
| Prompts dataset | To avoid training-data contamination, or prompts not yet piloted |
| Runs dataset | Results not yet checked, or a run with a known flaw |

**References.** Read `conventions.md` ("Lifecycle") and `pitfalls.md` at
`../../references/`. If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.

## Steps

1. **Ask which artifacts to make public**, if any are private and the request didn't
   say. Use one multi-select question listing the artifacts that exist, with their
   current visibility. If all are already public, this is a review only.
2. **Pre-publication review.** Read the repo and run the checks below. Report them as
   a short list of pass, fix and judgement items. Fix the mechanical ones yourself
   and ask about the judgement ones.
   - **Banner and README** are current: the status matches what exists, there's no
     "TODO" or placeholder text in a section that is meant to be filled, and the
     dates are absolute.
   - **Method holds up**: controls exist, a judge isn't grading its own model, the
     smoke run isn't presented as a result, n is shown next to rates, and open
     questions are listed rather than hidden.
   - **Model selection**: the panel is stated with exact slugs and the run date, and
     the README says why these models. A missing obvious comparator is a judgement
     item, not a blocker.
   - **Judge validated** against a hand-labelled sample or a second judge, if results
     are being shared. If not, the README must say so plainly.
   - **History**: the whole git history is public, not just the latest tree. Run
     `git log -p` through a quick scan for credentials, private notes and raw data
     that was committed and later removed. If anything turns up, stop and tell the
     user. Rewriting history is their decision.
   - **Disclaimer** is present if prompts state false claims on purpose.
   - **Links**: every link in the README resolves. Anything it links to that will
     still be private after this step is named, so the user knows those links will
     404 for readers.
3. **Flip visibility** only for the chosen private artifacts, after the review is clean or
   the user accepts the open items:
   ```bash
   gh repo edit <owner>/<Name>-Eval --visibility public --accept-visibility-change-consequences
   python3 -c "from huggingface_hub import HfApi; HfApi().update_repo_settings('<owner>/<Name>-Eval', private=False, repo_type='dataset')"
   python3 -c "from huggingface_hub import HfApi; HfApi().update_repo_settings('<owner>/<Name>-Eval-Runs', private=False, repo_type='dataset')"
   ```
   Never make the `-Ratings` dataset or the `-Arena` Space public.
4. **Verify from outside.** Make a logged-out request to each public URL:
   `curl -s -o /dev/null -w '%{http_code}'` on `https://github.com/<owner>/<Name>-Eval`
   and on `https://huggingface.co/api/datasets/<owner>/<Name>-Eval` with no token.
   A 200 there is the check that matters. The API call's own success is not proof.
5. **Update the README.** Set the Visibility line to the new state, and add the
   GitHub topics (`gh repo edit --add-topic llm-evaluation,...`) and a description if
   they're missing. Commit and push.
6. **Register** (if anything was flipped): run `register-eval`.
7. **Offer the write-up**, in one line: if a finished run exists, `analyse-findings`
   and `draft-article` can turn it into a post.

## Going back

Making something private again is possible (`--visibility private`,
`private=True`), but forks, clones and HF downloads made in the meantime stay out
there. Say this in one sentence if the user asks to reverse it.
