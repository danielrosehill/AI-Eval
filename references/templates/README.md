# <Name>-Eval

> **Status: placeholder (<YYYY-MM-DD>).** Scope and design only. No prompts, harness or results yet.<If a component: " This is component N of [Dan-Eval](https://github.com/danielrosehill/Dan-Eval).">
>
> **Visibility:** repo public · prompts public · runs none

<The question, in one or two sentences. Example: "Does a model assume the user is in the US when nothing says so?">

## Test prompts

<Added by draft-test-prompts. Until then: "Not yet written.">

<!-- Once published:
[![Hugging Face](https://img.shields.io/badge/HuggingFace-Dataset-yellow?logo=huggingface)](https://huggingface.co/datasets/<owner>/<Name>-Eval)

N prompts (<breakdown>): [huggingface.co/datasets/<owner>/<Name>-Eval](https://huggingface.co/datasets/<owner>/<Name>-Eval). The source of truth is [`data/prompts.jsonl`](data/prompts.jsonl) in this repo, and [`data/README.md`](data/README.md) is the dataset card. The Hugging Face dataset is uploaded from `data/`:

```bash
hf upload <owner>/<Name>-Eval data . --repo-type dataset
```
-->

## Mechanism

<How the eval works: what kind of prompts, which dimensions, and the controls.>

- **<Dimension>.** <What it probes, with two or three example prompts.>

Controls:

- <Prompts that remove the ambiguity, to show the model moves off its default when told.>
- <A sanity comparison, e.g. models from labs in different countries.>

## Grading

Score each response from 0 to 3:

| Score | Meaning |
|---|---|
| 0 | <clean> |
| 1 | <mild> |
| 2 | <clear> |
| 3 | <severe> |

<How scores aggregate: an index per model, broken down by dimension.>

## Results

<Added by publish-run. Until then: "Not yet run.">

## Open questions

- <Unresolved design choices. Write them down rather than guessing.>

## Origin

<Where the idea came from: a plan file it graduated from, earlier notes, the session date.>

## Related

<Sibling evals and how this one differs.>

## Disclaimer

<Only if prompts state false or one-sided claims on purpose: they do not represent the author's views; reference notes record mainstream evidence as of <date>; contest a note by opening an issue.>

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
