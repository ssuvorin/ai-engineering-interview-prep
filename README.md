# AI Engineering Interview — Study Workspace

> Personal interview-prep workspace built on top of [amitshekhariitbhu/ai-engineering-interview-questions](https://github.com/amitshekhariitbhu/ai-engineering-interview-questions): **571 theory questions** across 15 sections + a **30-question resume deep-dive** (предметное интервью) generated from my own resume.

The upstream question list lives in [QUESTIONS.md](QUESTIONS.md). This repo adds a complete self-study loop: question worksheets, grading answer keys, and a fetched reference corpus for every question.

## Repository structure

| Path | What it is |
|---|---|
| `qa/` | **Working zone.** 16 files, one per section. Every question has an empty `## Your answer` slot — fill it in bullet form. |
| `keys/` | **Grading keys.** Compact answer keys per section: `Идеал` (ideal answer) → `Обязательные пункты` (must-cover points) → `Частые ошибки` (common mistakes) → `Красные флаги` (red flags). Large sections split into `.part2`/`.part3`. Don't peek before answering. |
| `reference/` | **Source corpus.** 144 fetched articles behind the upstream question list — Outcome School blogs, Substack posts, YouTube transcripts, LinkedIn/X posts. `_manifest.json` maps URL → file, `_qmap.json` maps section → question → source files. |
| `resume/` | My resume (`resume.md`) — the basis for the resume deep-dive section. |
| `QUESTIONS.md` | Original upstream question list (unmodified). |
| `HOW-TO-STUDY.md` | The study loop, in Russian. |

## Sections

| # | Section | Questions |
|---|---|---|
| 01 | [Must Know](qa/01-must-know.md) | 6 |
| 02 | [LLM Fundamentals](qa/02-llm-fundamentals.md) | 80 |
| 03 | [Prompt Engineering](qa/03-prompt-engineering.md) | 30 |
| 04 | [Retrieval-Augmented Generation (RAG)](qa/04-retrieval-augmented-generation-rag.md) | 42 |
| 05 | [AI Agents and Agentic Systems](qa/05-ai-agents-and-agentic-systems.md) | 53 |
| 06 | [Fine-Tuning and Model Adaptation](qa/06-fine-tuning-and-model-adaptation.md) | 32 |
| 07 | [Vector Databases and Embeddings](qa/07-vector-databases-and-embeddings.md) | 26 |
| 08 | [AI System Design](qa/08-ai-system-design.md) | 49 |
| 09 | [LLMOps and Production AI](qa/09-llmops-and-production-ai.md) | 53 |
| 10 | [Evaluation and Testing](qa/10-evaluation-and-testing.md) | 36 |
| 11 | [AI Safety, Ethics, and Responsible AI](qa/11-ai-safety-ethics-and-responsible-ai.md) | 45 |
| 12 | [Multimodal AI](qa/12-multimodal-ai.md) | 30 |
| 13 | [AI Infrastructure and Scalability](qa/13-ai-infrastructure-and-scalability.md) | 35 |
| 14 | [Coding and Practical Implementation](qa/14-coding-and-practical-implementation.md) | 32 |
| 15 | [Behavioral and Scenario-Based Questions](qa/15-behavioral-and-scenario-based-questions.md) | 22 |
| 16 | [Resume Deep-Dive — предметное интервью](qa/16-resume-deep-dive.md) | 30 |

## The study loop

1. Open a section file in `qa/`, answer under each `## Your answer` — your own words, bullets are fine.
2. Grade against the matching `keys/<file>.md`:
   - **✓** — must-cover points present
   - **±** — partial; key lists what's missing
   - **✗** — wrong/empty; key gives the correct core + a link to `reference/<slug>.md` for the deep read
3. Recommended order (core → periphery):

```
01 → 02 → 04 → 05 → 03 → 07 → 09 → 10 → 13 → 06 → 08 → 12 → 11 → 14 → 15 → 16
```

Section 16 works anytime — it's about your own experience, not theory.

## Resume deep-dive (section 16)

30 questions generated from [resume/resume.md](resume/resume.md) — the предметное интервью: not theory, but *"can you defend every bullet on your resume"*. Six groups: self-presentation → flagship project deep-dive → architecture decisions → engineering process → data/metrics background → honesty & pressure questions. Keys check fact consistency with the resume and flag spots that need pre-prepared stable answers (`[нужна заготовка]`).

## Credits

- Questions and source links: [Amit Shekhar / Outcome School](https://github.com/amitshekhariitbhu/ai-engineering-interview-questions) — see [QUESTIONS.md](QUESTIONS.md) and the original license in [LICENSE](LICENSE).
- Study structure, answer keys, fetched reference corpus: this repo.
