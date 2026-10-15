# probe via eval

# Evaluation and Testing — Answer Key (1-36)

### 1. AI Agent Evaluation
- Идеал: measuring how well an agent (LLM that plans, calls tools, acts in multi steps) completes tasks — evaluates outcome AND trajectory, not only final text.
- Обязательные пункты:
  - Why different from LLM eval: agent behavior spans planning, tool use, recovery, loops; cost/latency/step counts matter.
  - Types: outcome eval, trajectory eval, tool use eval, planning eval.
  - Key metrics: task success rate (most important), tool call accuracy, steps per task, cost per task, latency per task, recovery rate, safety score, loop detection.
  - Benchmarks: BFCL (tool calling), tau-bench (customer service), SWE-bench Verified (coding), Terminal-Bench, MLE-bench, GAIA, WebArena / VisualWebArena / BrowseComp (web), OSWorld / AppWorld (computer use).
  - Best practice: strong test set (easy/hard/edge/adversarial), evaluate both outcome and trajectory, run each test 3–5× (avg + worst), sandbox with fake tools/data, track cost and latency from day one, validate judge vs humans, regression-run full test set after every change, set max steps/timeout, weekly human review of trajectories.
- Частые ошибки: judge only the final answer; single run; no trajectory review; no timeout → infinite loops.
- Красные флаги: «агент сам себя оценит», «максимум шагов не нужен» (loops are a known failure mode).

### 2. LLM Evaluation
- Идеал: process of measuring how well an LLM performs expected tasks — outputs checked for correctness, helpfulness, safety, usefulness.
- Обязательные пункты:
  - Types: automatic metrics, benchmarks, human evaluation, LLM-as-a-judge, task-specific and safety/red-team eval.
  - Automatic metrics: perplexity (intrinsic), BLEU/ROUGE/BERTScore (extrinsic) — fixed formulas best for exact-match tasks.
  - Why: no single metric is enough; open-ended tasks need humans/judges.
  - Challenges: open-ended outputs, data contamination, cost, judge bias, drift over time, edge cases.
- Частые ошибки: apply text-similarity metrics to free-form answers; trust one metric alone.
- Красные флаги: «метрика — истина в последней инстанции», не упоминать человеческую проверку.

### 3. AI Agent Observability
- Идеал: record everything an agent does internally, step by step, so you can explain behavior and debug.
- Обязательные пункты:
  - Three pillars: logs, metrics, traces — traces most important for agents (full journey of one task, step by step).
  - Span = record of one step/operation; trace = complete run made of nested spans forming a tree.
  - Design the agent as a graph of small steps → each node gives a clean span for free.
  - Track: prompt/response per LLM call, tool calls + args/results, token count, cost per task, latency per task, errors, retries.
- Частые ошибки: only metrics, no traces; no token/cost tracking; cannot answer "why did the agent do X?".
- Красные флаги: «observability = просто логи бэкенда», не отличать span от trace.

### 4. What is evaluation-driven development for AI applications?
- Идеал: build the eval first (like tests in TDD), then iterate model/prompt/tool changes against it — eval suite gates every improvement.
- Обязательные пункты:
  - Write an eval set aligned with product goals before shipping; treat it like regression tests in CI.
  - Every prompt/model/tool change triggers the full (or sampled) eval run; deploy on passed threshold.
  - Loop: define goal + way to check → implement → run eval → feedback into development.
  - Combines automatic metrics, LLM judge, human validation of judge, and continuous monitoring.
- Частые ошибки: eval after the fact; happy-path only tests; no baseline.
- Красные флаги: «сначала фича, потом метрика», «один ручной прогон = гарантия».

### 5. Why is AI only as good as our definition of done?
- Идеал: definition of done = goal + checkable way to verify it; AI is only as strong as the checker we give it.
- Обязательные пункты:
  - With an exact checker (unit test, compiler, exact I/O) the AI loops and iterates until green — many tries, self-correcting.
  - Without a checker (vague "build login", "clean architecture", "readable") nothing turns red/green, so AI gets only one try → unreliable.
  - The loop needs a check signal: `am I done or not?` Every round gives honest feedback.
  - Fix: test-first, exact I/O, commands that must run clean, write edge cases as an explicit list, turn vague quality into a number (<200 ms for 1000 rows), be honest about uncheckable parts.
- Частые ошибки: judge by "looks complete"; assume a passing happy-path test proves correctness.
- Красные флаги: «AI слабый» (no — our clarity is the limit), «компилируется = done».### 6. How do you evaluate LLM outputs? What metrics do you use?
- Идеал: choose evaluation type by task, not one universal metric — combine automatic metrics, benchmarks, human eval, and LLM-as-judge.
- Обязательные пункты:
  - Automatic metrics: perplexity (intrinsic); BLEU, ROUGE, BERTScore (extrinsic). Fixed formulas suit exact-match tasks.
  - Human evaluation: gold standard (helpfulness, tone, creativity); Likert rating, pairwise comparison, error annotation.
  - LLM-as-judge: scalable but must be validated against human ratings (position/verbosity/style/self-preference bias).
  - Benchmarks: MMLU, HumanEval, GSM8K — only for relative model comparison.
  - Task-specific: RAG (context precision/recall, faithfulness, answer relevance), summarization (conciseness, relevance).
- Частые ошибки: BLEU for open-ended answers; trust judge without human calibration.
- Красные флаги: «одна метрика для всех задач», не упоминать человеческую проверку.

### 6. How do you evaluate LLM outputs? What metrics do you use?
- Идеал: combine automatic metrics, human eval, benchmarks, and LLM-as-judge; pick method by task.
- Обязательные пункты:
  - Automatic: perplexity (intrinsic); BLEU / ROUGE / BERTScore (extrinsic). Fixed formulas for exact-match outputs.
  - Human evaluation: gold standard - captures tone, helpfulness, creativity formulas don't; Likert, pairwise, error annotation.
  - LLM-as-judge: scalable but must be validated against humans (style/position/verbosity/self-preference bias).
  - Benchmarks (MMLU, HumanEval, GSM8K) for relative comparison, not product quality.
  - Task-specific: RAG (context precision/recall, faithfulness, answer relevance), summarization (conciseness, relevance).
- Частые ошибки: trust one metric alone; BLEU on creative answers.
- Красные флаги: «метрики всегда объективны», не упоминать человеческую валидацию.

### 7. Explain BLEU, ROUGE, and BERTScore. When would you use each?
- Идеал: two n-gram overlap metrics + one embedding-based semantic metric; pick by task kind.
- Обязательные пункты:
  - BLEU: precision-based n-gram overlap with brevity penalty — for machine translation.
  - ROUGE: recall-based n-gram overlap (ROUGE-L longest common subsequence) — for summarization.
  - BERTScore: semantic similarity via embeddings, tolerates paraphrase/near-synonyms better.
  - Use when exact/reference scoring matters and cost is a concern; BERTScore for semantic closeness.
- Частые ошибки: penalize synonyms; BLEU for summarization; ignore brevity penalty.
- Красные флаги: «BERTScore = BLEU с другим именем», «ROUGE — это precision».

### 8. What is G-Eval, and how does it use LLMs for evaluation?
- Идеал: LLM-as-judge with chain-of-thought: the judge generates evaluation steps, applies them, then scores.
- Обязательные пункты:
  - G-Eval = Generate evaluation steps + Score; also called chain-of-thought judging.
  - Flow: (1) judge writes down the evaluation steps/checklist, (2) applies each step to the answer one by one with reasoning, (3) gives a final score (e.g. 1–5).
  - Much better agreement with human ratings than a direct scoring prompt — slows the judge down, reads the answer more carefully.
  - Prompt includes criterion (e.g. helpfulness), user question, assistant response, plus explicit Step 1/2/3 instructions.
- Частые ошибки: confuse G-Eval with plain one-shot scoring; judge scores without reasoning.
- Красные флаги: «G-Eval — это фреймворк автоматической проверки фактов», не упомянуть CoT-шаги.

### 9. What is LLM-as-a-judge evaluation, and what are its limitations?
- Идеал: an LLM grades outputs using a prompt; four common forms: single-answer scoring, pairwise comparison, reference-based, rubric-based.
- Обязательные пункты:
  - Steps: define criteria → choose judge ≥ capability of the model being judged (GPT-5/Claude Opus/Gemini Pro or open judge models) → write prompt with task/input/output/scale/rules/format → run on a sample → compare with human ratings → iterate → use at scale.
  - Rubric-based is the most common in production; pairwise for model/prompt comparison.
  - Biases: style (most dominant), position (first answer wins → swap order and average), verbosity (prefers long), self-preference, preference leakage/bandwagon.
  - Best practice: validate judge against humans, handle position bias, use a Panel/Jury of multiple judge models from different families, keep criteria simple.
- Частые ошибки: judge weaker than the evaluated model; prompt without style guidance; single judge family.
- Красные флаги: «жюри не требует валидации на людях», «всегда объективен».

### 10. How do you conduct human evaluation for AI systems?
- Идеал: have real people rate outputs — still the gold standard for meaning, tone, creativity, and safety.
- Обязательные пункты:
  - Methods: Likert scale (1–5) rating, pairwise comparison (like Chatbot Arena, Elo used for ranking), error annotation (mark the exact mistakes).
  - Why: formulas can't judge open-ended tasks; humans catch subtleties a judge/metric misses.
  - Costs: slow, expensive, annotator disagreement — so it is used on samples to validate the automated judge, then scale with the judge.
  - Very useful for collecting preference data for RLHF reward models.
- Частые ошибки: run human eval on thousands of examples; single annotator.
- Красные флаги: «человек не нужен — метрики всё решат», «оценки людей всегда согласованы».

### 11. What is red teaming, and how do you red team an LLM application?
- Идеал: adversarial eval — try to break the model before real users do, then fix and re-test.
- Обязательные пункты:
  - Goal: find safety/robustness failures (harmful content, jailbreaks, prompt injection, over-refusal).
  - Process: define scope + success criteria → recruit diverse adversarial testers → craft attacks (jailbreak, injection, social-engineering) → log attempts/responses → classify and fix → re-run to confirm.
  - Include a defined attack taxonomy; test the actual deployment surface, not just the model.
- Частые ошибки: red team once and stop; test only obvious harmful prompts; never re-run after fixes.
- Красные флаги: «red team — это просто бета-тестирование», «промпт-инъекция не относится к безопасности».

### 12. How do you detect and measure hallucinations in LLM outputs?
- Идеал: use grounding/factual-consistency checks against a trusted source, plus automated and human measures.
- Обязательные пункты:
  - Signal: claim not supported by provided context → likely hallucination; check entity/topic overlap and contradiction with a knowledge source.
  - Automated: faithfulness/groundedness metric (e.g. RAGAS), NLI-style entailment models (is output entailed by context?), token/n-gram overlap with retrieved text, LLM-as-judge for factual consistency.
  - Human: annotate fabricated statements (error annotation) on a sample; build a labeled hallucination test set.
  - Mitigate: require citations/grounding via RAG, add refusal for unknown, post-hoc validation.
- Частые ошибки: полагаться на один сигнал (один метр не ловит всё); проверять правдоподобность текста вместо соответствия контексту.
- Красные флаги: «галлюцинации видны невооружённым глазом», «достаточно LLM-as-judge без ground truth».

### 13. What is adversarial testing for AI systems?
- Идеал: intentionally craft inputs to break the system (underperform, unsafe, ungrounded) before real users hit them.
- Обязательные пункты:
  - Types: perturbations (typos, paraphrases), prompt injection, jailbreaks, adversarial datasets, fuzzing, red teaming.
  - Run in sandbox; measure robustness = performance across adversarially varied inputs.
  - Use results to harden (guardrails, filtering, better prompts) and add caught failures to the regression suite.
- Частые ошибки: ad-hoc manual testing; ignore injected instructions in user data.
- Красные флаги: «adversarial тесты нужны только для безопасности», считать, что тесты не могут ломаться намеренно.

### 14. How do you build a regression test suite for AI applications?
- Идеал: an automated eval set run on every change to catch regressions before deploy — the AI equivalent of unit tests.
- Обязательные пункты:
  - Core cases: golden/labeled set, past bugs, edge + adversarial cases, prompt/tool/model-change checks.
  - Include thresholds (metric must not drop below baseline); run in CI on every change; canary regressions too surfaced.
  - Re-add every fixed failure into the suite; human spot-check of samples weekly.
- Частые ошибки: happy-path-only; no fixed baseline threshold; never rerun on prompt changes.
- Красные флаги: «регрессии не случаются у LLM», «достаточно числовой метрики без примеров».

### 15. What are benchmark suites (MMLU, HumanEval, GSM8K), and how do you interpret them?
- Идеал: standardized community datasets to compare models fairly on specific skills — interpret as relative signal, not product quality.
- Обязательные пункты:
  - MMLU: general knowledge, multiple choice, 57 subjects (hard version MMLU-Pro); HumanEval: coding function-writing; GSM8K: grade-school math word problems.
  - Others: HellaSwag (commonsense), SWE-bench Verified (real code), MATH/AIME (hard math), TruthfulQA, IFEval (instruction following), RULER (effective context length), Chatbot Arena (Elo from real user votes).
  - Interpret carefully: saturation (top models hit ceiling → harder benchmarks replace them), contamination (model saw test questions in training → inflated scores), qualification bar (easy = basic gate).
  - Use for comparing models/versions on benchmarks, but always build product-specific eval for real workload.
- Частые ошибки: take benchmark score as absolute truth; ignore saturation/contamination.
- Красные флаги: «высокий MMLU = идеальный продукт», не знаю, что такое лидерборд.

### 16. What is benchmark contamination, and how do you guard against it?
- Идеал: understand and control data leakage so scores are not inflated.
- Обязательные пункты:
  - Cause: model saw the test questions during training → memorized → falsely high score; common in general pretraining.
  - Detection: hold out a private/untrained eval set; check n-gram overlap between training data and benchmark questions; use contamination-resistant benchmarks (LiveCodeBench uses problems released after cutoff).
  - Guarding: separate training from eval data, monitor overlap, prefer fresh/private eval sets, do not fine-tune on benchmark questions.
- Частые ошибки: massaging eval data to improve the score; ignoring overlap; reusing the same test set forever.
- Красные флаги: «переучил на тестовых вопросах не страшно», «LiveCodeBench contamination-resistant, потому что вопросы статические».

### 17. Your new model version scores higher on every benchmark, but users say it got worse. Why, and how do you find the problem?
- Идеал: recognize that benchmark scores measure different things than the product's real task (bad eval alignment) — your product eval must mirror actual user workload, not benchmarks.
- Обязательные пункты:
  - Causes: eval criteria drift (metric measures wrong thing), contamination, overfitting to benchmark, input/data drift, judge bias, or the change fixed benchmark-specific behavior while breaking real flows (e.g. style/tone hardening).
  - Diagnose: collect failing user reports → reproduce → build a product-focused eval set from real user cases → run human eval on the diff → compare distributions (old vs new inputs/outputs) → check what changed (prompt, model, guardrail).
  - Fix: iterate on the product eval, not the benchmark; roll back or tune the change; add reported regressions to the regression suite.
- Частые ошибки: tune to benchmarks blindly; ignore user telemetry.
- Красные флаги: «раз benchmark вырос, продукт обязательно стал лучше», «регрессии пользователей бывают только из-за багов».

### 18. How do you evaluate a RAG system end-to-end?
- Идеал: evaluate both retrieval and generation, end-to-end, with component metrics plus a final correctness check.
- Обязательные пункты:
  - Retrieval: context precision (are top-k relevant docs), context recall (did we retrieve all needed docs).
  - Generation: faithfulness/groundedness (answer supported by retrieved context), answer relevance (addresses the question).
  - End-to-end: final answer correctness + no hallucination beyond context; measure on real user-like queries.
  - Frameworks: RAGAS, DeepEval.
- Частые ошибки: only checking retrieval or only answer; no ground-truth eval; conflate relevance with faithfulness.
- Красные флаги: «RAG оценивается одним скором», не различать context precision/recall.

### 19. How do you evaluate the quality of AI agents?
- Идеал: measure task completion and trajectory quality with outcome + process metrics; run repeatedly in a sandbox.
- Обязательные пункты:
  - Outcome metrics: task success rate, goal completion, cost per task, latency per task, safety score.
  - Trajectory metrics: tool call accuracy, steps per task, recovery rate (can it recover from tool failure), planning correctness, loop detection.
  - Evaluate per subtask milestones, not just final result; run each scenario multiple times (avg + worst); sandbox with fake tools.
- Частые ошибки: single success/fail per task; ignore trajectory; no recovery/loop checks.
- Красные флаги: «агент хороший — у него все задачи завершились» без проверки пути; нет лимита шагов.

### 20. How would you evaluate an autonomous coding agent? Why can SWE-bench pass rates be misleading?
- Идеал: evaluate on your repo's real issues with acceptance tests, not just public SWE-bench.
- Обязательные пункты:
  - SWE-bench Verified: real GitHub issues, but pitfalls — saturation, contamination, benchmark doesn't match your codebase/tooling/style, resolution != correctness, only pass/fail on hidden tests - a merge is considered correct only if hidden tests pass.
  - Evaluation design: private held-out issues from your repo, acceptance criteria (diff + new tests pass), trajectory log (how many edits, test runs, steps), human review of the PR quality (clean diff, no hacks).
  - Also measure: revert/no-op rate, time per issue, cost per resolved issue, success on reformulated/ambiguous tasks and multi-file changes, failure on regressions.
- Частые ошибки: equate SWE-bench score with agent quality for your stack; ignore diff quality and hidden test drift.
- Красные флаги: «SWE-bench — единственный способ оценить кодинг-агента», считать pass = «хорошее решение».

### 21. What is the difference between offline and online evaluation for AI systems?
- Идеал: offline = evaluate on collected/static data before shipping; online = evaluate with live traffic after deploying.
- Обязательные пункты:
  - Offline: on a fixed labeled dataset/benchmark, no real users — cheap, fast, repeatable (regression suites, benchmarks, LLM judge on recorded cases).
  - Online: A/B tests, canary, user feedback, production telemetry (errors, latency, cost, churn), drift detection.
  - Use offline first, then confirm with online; catch offline-blind issues (context drift, real-user phrasing, performance under load).
- Частые ошибки: only offline (miss drift) or only online (slow, expensive, risky).
- Красные флаги: «A/B достаточно, офлайн-тесты не нужны», «офлайн-скор гарантирует продакшн-качество» (пропасть между ними).

### 22. How do you measure factual consistency in LLM outputs?
- Идеал: check that every claim is supported by a trusted source (retrieved context), rather than invented.
- Обязательные пункты:
  - Groundedness/faithfulness: output should be entailed by retrieved docs — use NLI-style models, entailment scores, or RAGAS faithfulness.
  - Detect contradictions: reuse docs and compare claims (verification), entity/topic overlap.
  - Manual: annotate errors in a sample (error annotation); build a factual-consistency test set.
  - Practical: require citations, post-hoc verify with the same/other model + retrieved sources.
- Частые ошибки: factual consistency = string similarity; no grounding to source.
- Красные флаги: «если ответ красиво написан — он прав», «consistency — это стилистическая проверка».

### 23. How do you evaluate multi-turn conversation quality?
- Идеал: assess whole dialogue, not just per-turn output — flow, coherence, context usage.
- Обязательные пункты:
  - Per turn metrics: correctness, relevance, tone; across turns: coherence, consistency (does it contradict itself or forget state), follow-up handling.
  - Methods: human eval on dialogue samples, LLM judge with dialogue-level rubric, behavioral metrics (number of re-asks, downstream success, user satisfaction, task completion rate).
  - Data: scripted multi-turn sessions + real logged dialogues; track memory usage and state retention.
- Частые ошибки: evaluate each turn in isolation; ignore forgetting/contradiction across turns.
- Красные флаги: «проверил каждый ответ отдельно — диалог хороший», не упоминать long-term memory/context.

### 24. What is the role of golden datasets in AI evaluation?
- Идеал: curated labeled inputs with known best outputs — the backbone for automatic metrics, benchmarks, and judge validation.
- Обязательные пункты:
  - Gold/test items = inputs + correct outputs (ground truth) — enables exact scoring (BLEU/ROUGE or LLM judge vs expected).
  - Serve as regression suite; used to validate judges against human-annotated ground truth.
  - Build/maintain in alignment with achievable user workload; include edge/adversarial cases and a held-out portion for new data.
- Частые ошибки: small, unrepresentative set; leaking training into eval; misaligned with real queries.
- Красные флаги: «голден-датасет — это обучающая выборка», не нужен held-out.

### 25. How do you build an eval set when there is no labelled ground truth and domain experts are expensive?
- Идеал: leverage proxies (judges, rules, propagation, bootstrapping) instead of massive human labeling.
- Обязательные пункты:
  - Distant/synthetic labels: build a small high-quality seed by hiring few experts + label transfer; use LLM to generate synthetic inputs (then manually curate a subset).
  - Rule-based checks: extractable facts, round-trip assertions, output-to-input consistency — get correctness without labels.
  - LLM-as-judge vs reference: validate judge on a small expert-annotated sample, then scale.
  - A/B / user-feedback proxies: implicit metrics (satisfaction, task completion, re-asks).
  - Choose informative, unbiased examples; re-use across evals.
- Частые ошибки: wait forever for labels; assume judge is correct without validation; unrepresentative synthetic inputs.
- Красные флаги: «без экспертов eval невозможен», «синтетика полностью заменяет человеков».

### 26. How do you implement continuous evaluation for production AI systems?
- Идеал: ongoing automated monitoring of performance/quality/safety on live and near-real-time data, pairing offline regression with online telemetry.
- Обязательные пункты:
  - Pipeline: log real traffic samples (prompts, outputs, feedback) → scheduled eval jobs (daily/weekly) run LLM judge + metrics on them → alert thresholds, dashboards.
  - Track drift: input/topic distribution drift, performance/quality drift, bias drift, novel failures/users.
  - Integration: A/B, canary, feedback loops (thumbs up/down), user-reported issues routed back into ticket/regression set.
  - Automate rollback or alerting when thresholds breach; keep humans for review of judge disagreements and edge cases.
- Частые ошибки: evaluate only at deploy time; no drift detection; ignore live feedback.
- Красные флаги: «доеплоим и забыли», «онлайн-метрики не нужны — у нас offline eval».

### 27. How do you evaluate bias in AI model outputs?
- Идеал: measure differential treatment across protected groups, not just overall accuracy.
- Обязательные пункты:
  - Metrics (group-level): demographic parity, equalized odds/equal opportunity, calibration (accuracy per group), difference in error rates across groups.
  - Probe: hold a diverse test set with protected attribute labels; evaluate same task on each group; red-team with counterfactual probes (change attribute, expect same outcome).
  - Human/LLM judge for subtle bias; measure harms to detach safety; track bias over versions (fairness regression).
- Частые ошибки: single global metric masks subgroup gaps; conflate fairness with coverage or accuracy.
- Красные флаги: «низкий bias — это высокий accuracy», не разделять группы.

### 28. How do you compare two models or prompts in a statistically rigorous way?
- Идеал: run controlled randomized comparisons and apply inferential statistics before declaring a winner.
- Обязательные пункты:
  - Use paired comparisons on the same eval set (both configurations get the same inputs); randomize order for pairwise-judge/human eval (handle position bias).
  - Report means/medians + dispersion, not just "bigger score"; compute significance (bootstrap CIs, permutation/McNemar-like, or paired t-test/wilcoxon on per-item scores).
  - Fix multiple comparisons (when testing many configs) to control false positives; pre-register the hypothesis and eval protocol.
  - Use McNemar for paired pass/fail items; bootstrap mean differences; confirm with A/B in live.
- Частые ошибки: compare different eval sets, or use p-value on per-item judge scores without accounting for judge noise; cherry-pick configs post-hoc.
- Красные флаги: «больше среднее = статистически значимо» absent tests; «нужно 1 тест на конфиг, а не парное».

### 29. How do you evaluate the robustness of an LLM application across input variations?
- Идеал: verify quality holds across realistic and hostile perturbations, not only ideal phrasing.
- Обязательные пункты:
  - Perturbation suite: typos, slang, multilingual, rephrasing, added noise, formatting changes, different user personas, adversarial rephrasing, out-of-distribution topics.
  - Test in sandbox: same expectation across variants — check stable relevance/factuality and consistent refusals.
  - Quantify: pass rate across the perturbation set, consistency, degradation on edge cases; combine with drift monitoring + red-team cases.
- Частые ошибки: happy-path canonical input only; confuse robustness with safety.
- Красные флаги: «robustness = высокая accuracy на чистом тесте».

### 30. What are the key differences between evaluating traditional ML vs LLM applications?
- Идеал: know that LLM eval adds semantic/open-ended layers on top of classic ML eval.
- Обязательные пункты:
  - Traditional ML: structured labels, metrics (accuracy/precision/recall/AUC), fixed finite feature space, reproducible data — classic train/test/validation split.
  - LLM apps: highly open-ended outputs, data contamination risk, drift occurs, judge-driven automated eval (no one metric captures quality), test sets need to mirror real user workflow, need human/judge eval + safety + prompt-level regression suites.
  - Differences to call out: eval target (quality, safety vs accuracy), eval methods (LLM-as-a-judge, human, BLEU/ROUGE, benchmarks vs standard ML metrics), data (from real traffic + synthetic), frequency, drift-sensitivity.
- Частые ошибки: reuse ML workflow for LLM eval (only accuracy on a fixed dataset); treat LLM eval as one-shot.
- Красные флаги: «emtrics for LLM are exactly the same as classic ML», «benchmark results directly predict production quality».

### 31. How do you set up an evaluation framework from scratch for a new LLM application?
- Идеал: start with a small test set and iterate the eval loop as you build the feature.
- Обязательные пункты:
  - Steps: define evaluation criteria for each use case → seed a golden test set (easy, hard cases, edge cases, adversarial) → choose metrics / LLM judge → run a baseline eval → compare with human judgment → iterate the prompt / judge / test set → version the eval set and prompt with the app → continuous eval in CI.
  - Include: baseline, thresholds, regression runs, judge validation vs humans, drift tracking, human review.
- Частые ошибки: wait for big data, jump to benchmarks, one-off.
- Красные флаги: «нужен большой датасет сразу», «метрик много, а главной нет».

### 32. Your model passes one fairness metric but fails another. How do you handle conflicting audit results?
- Идеал: treat each metric as measuring a different slice of fairness; investigate the disagreement and reconcile against the product's actual harm, rather than picking the metric that flatters you.
- Обязательные пункты:
  - Map each metric to the harm it guards (demographic parity vs equalized odds vs calibration measure different things; disagreement is normal, not evidence of failure).
  - Drill into the subgroups and error patterns behind the conflicting numbers — find WHERE and for WHOM they diverge (which class, which decision boundary); examine base rates and label availability (disparate impact vs disparate treatment).
  - Involve domain/product/legal perspective to decide which slice matters for this deployment; document the decision and trade-offs; consider per-group thresholds or calibration as reconciliation.
  - Re-audit after changes and re-run BOTH metrics; keep audit data reproducible and time-stamped.
- Частые ошибки: average the metrics; report only the favorable one.
- Красные флаги: «одна метрика лучше другой — выбираем её» без анализа причин.

### 33. Your model was fair at deployment, but became biased 6 months later. How do you monitor continuously?
- Идеал: treat fairness as a live property: continuously measure it on production traffic the way you monitor latency or error rate.
- Обязательные пункты:
  - Deploy a production fairness dashboard: sample production inputs/outputs, split by protected attributes, recompute parity/equalized odds/calibration per week.
  - Detect drift: input distribution shift, population composition change, feedback-loop skew (model's decisions change who gets seen/selected), and label/reward shift.
  - Alert on statistically meaningful metric movement (not noise); investigate root cause — new data, retraining, prompt change, EV shift.
  - Remediate: revert, retrain with fairness constraints, re-weight data, adjust thresholds, add guardrails; and add the shift case to your regression suite.
- Частые ошибки: audit once at deploy and never again; compare raw accuracy across groups without base rates.
- Красные флаги: «раз было справедливо, то и останется», нет data-дрифта в мониторинге.

### 34. An external auditor cannot reproduce your model's results. How do you ensure audit reproducibility?
- Идеал: make a full, self-contained audit trail so any reviewer can reproduce the exact outputs from inputs alone.
- Обязательные пункты:
  - Reproducibility needs: locked model versions (hash/pinned checkpoints), fixed prompts/templates, recorded hyperparameters, seed/temperature settings, and the exact eval dataset + preprocessing.
  - Store everything in a versioned artifact store (model card + data card + run manifest); log timestamped inference records (input, output, version, latency).
  - Handle nondeterminism (temperature, batching, GPU): set seeds, pin sampling, and if the task allows run deterministic/inference-time settings for audits.
  - Provide a runnable reproduction script in a documented environment (Docker/spec), and a signed trail of what changed and when.
- Частые ошибки: audit a moving target — no pinned versions; expect auditor to reverse-engineer a live API.
- Красные флаги: «у нас всё недетерминировано, но результаты воспроизводимы», версии модели «примерно такие».

### 35. How do you structure red teaming for an LLM chatbot before launch?
- Идеал: run a scoped, adversarial testing campaign before launch, guided by taxonomy and success criteria, and re-test after fixes.
- Обязательные пункты:
  - Define scope + attack surface: brand, safety, and harm policies, target behaviors (jailbreaks, injection, PII leakage, misinformation, unsafe code, prompt extraction).
  - Build an attack taxonomy and a seeded threat list; recruit diverse internal or external operators (different backgrounds, adversarial skill levels) with clear instructions and logging.
  - Test the real deployment surface (the actual chatbot with its system prompt, tools, guardrails, and RAG), not just the raw model; include multi-turn and user-data injection cases.
  - Log every attempt and response, triage by severity, patch guardrails/prompts, then re-run the campaign to confirm fixes; escalate unfixed criticals for launch decision.
- Частые ошибки: one-off attempt, no taxonomy, no re-test after fixes.
- Красные флаги: «red team — это бета-тест», «никогда не тестируем против промпт-инъекций».

### 36. How do you red team a multimodal model where text-only safety tests miss cross-modal attacks?
- Идеал: cross-modal red teaming — test each modality and the combinations — because attacks can live in the space between text, image, and audio.
- Обязательные пункты:
  - Test each mode individually (image with harmful text stamped on it, audio with hidden speech, video frames) AND cross-modal chains (harmful content hidden in an image described via text; instructions encoded in images/audio; text that triggers an unsafe image generation).
  - Watch for modality-confusion attacks: typographic attacks (text rendered in images bypassing text filters), steganographic/encoded messages, image+prompt combinations where the model misreads intent, OCR-of-and-answer reattacks.
  - Cover output modes too: the model can produce images/audio/video — test for unsafe generation and for unsafe content passed to tools downstream.
  - Use a modality-aware taxonomy, both automated scanners and human judges per modality, and evaluate the full pipeline end-to-end, not each model in isolation.
- Частые ошибки: test text prompts only; separate text and image testing without the combined/chain cases.
- Красные флаги: «текстовый фильтр ловит всё», считать, что изображения не являются входом для промпт-инъекций.
