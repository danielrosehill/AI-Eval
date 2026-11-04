---
name: rag-eval
description: Evaluate a retrieval or RAG pipeline - separating retrieval from generation, building a question set from real documents, and comparing generators with retrieval held fixed. Use when the user says "evaluate my RAG", "test retrieval", "is the chatbot finding the right documents", "which embedding model", or "why is my RAG hallucinating".
---

# Evaluate a RAG pipeline

**Measure retrieval and generation apart.** A wrong answer has two possible causes, and one
overall score can't say which. Fix retrieval first: no generator recovers a passage it never saw.

## Steps

1. **Build the question set from the real corpus.** 30–50 questions, each with the answer and the
   passages that hold it. Real user questions come first. Include questions that need several
   passages, and some the corpus can't answer, where the right response is to say so.
   An LLM can draft these, but a person checks them. Synthetic questions echo the
   wording of their source passage, which flatters retrieval.

2. **Score retrieval alone.** No LLM needed: recall@k (is the right passage in the top k?) and
   MRR or nDCG for ranking. Compare chunking, embedding models and rerankers here, changing
   one at a time.

3. **Score generation with retrieval held fixed.** Freeze the retrieved context so that
   every generator sees the same thing, and go wide across generators as in `run-eval`:

   | Metric | Question |
   |---|---|
   | Faithfulness | Is every claim supported by the context? |
   | Answer correctness | Does it match the reference answer? |
   | Abstention | Does it decline when the context lacks the answer? |
   | Citation accuracy | Do the citations point to passages that say that? |

4. **Then test end to end** on the winning combination, with a live retriever.

5. **Choose tooling.** Small and agent-run: `setup-agent-eval-space`, using LLM-judged
   faithfulness. Otherwise Ragas (`ragas`) or DeepEval (`install-eval-cli`). Their judged metrics
   are LLM calls, so they carry a cost and need spot-checking by hand.

6. **Report** retrieval and generation separately, plus failures sorted by cause: not retrieved,
   retrieved but ignored, or invented.

## Don't

- Don't change the retriever and generator in one run.
- Don't rely on a long-context model to skip this. Stuffing the corpus in the prompt is a
  candidate pipeline, and it gets evaluated like the others.
- Don't send a private corpus to a judge or provider the user hasn't approved.
