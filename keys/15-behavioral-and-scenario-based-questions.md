# Behavioral and Scenario-Based Questions — Answer Key (1-22)

### 1. What is AI Engineering, and how does it differ from Machine Learning Engineering?
- Идеал: AI Engineering is the discipline of building and operating production systems that use AI (LLMs, agents, RAG) end-to-end, whereas MLE focuses on training and optimizing models. A deal-breaker answer names only "training models".
- Обязательные пункты:
  - AI Eng: orchestration (prompts, agents, tools, evals), LLMOps (deployment, monitoring, latency, cost), integration into product.
  - MLE: data pipelines, model training/validation, metrics (precision/recall), feature engineering.
  - Overlap: both need evals, both own quality; AI Eng leans system-level, MLE leans model-level.
  - Пример: AI Eng builds a RAG chatbot in production; MLE fine-tunes the model it uses.
- Частые ошибки: свести AI Engineering к "использованию библиотек" или к MLE; не упомянуть production/prompting/evals.
- Красные флаги: «AI Engineer просто пишет промпты»; не различает роли.

### 2. How do you decide whether a problem needs AI or a traditional software solution?
- Идеал: start from the problem, not the hype — pick AI only when it adds measurable value no deterministic logic can.
- Обязательные пункты:
  - Prefer traditional (rules, heuristics, lookup) when input/output patterns are fixed and behavior must be guaranteed.
  - Choose AI when: unstructured input (text/image/audio), no explicit rules, fuzzy semantics, generation needed.
  - Estimate cost of error: if wrong answer is catastrophic, add hard guardrails or don't use free-form AI.
  - Verify with a cheap prototype + eval before committing.
- Частые ошибки: «AI first» для всего; ignore deterministic fallbacks; skip cost-of-error analysis.
- Красные флаги: «мы добавили AI, потому что модно»; не упоминать fallback to rules.

### 3. How do you measure the ROI of an AI feature?
- Идеал: tie AI to a business metric, monetize or save costs, then compare against cost — with clear baseline counterfactual.
- Обязательные пункты:
  - Pick the metric the feature moves (conversion, ticket deflection, time saved, revenue, CSAT) — define baseline "without AI".
  - Costs: engineering time, inference/compute, data, maintenance, MLOps — total cost of ownership.
  - ROI = (incremental business value − total cost) / total cost; present with A/B or quasi-experiment evidence.
  - Attribute carefully: control groups; do not credit all improvement to the model; check statistical significance.
- Частые ошибки: metric without baseline; only technical metrics (accuracy) — need business value.
- Красные флаги: «ROI = accuracy»; no counterfactual.

### 4. How do you handle hallucinations when they occur in a production AI system?
- Идеал: prevent at design, detect at runtime, respond with clear escalation path — not just "tell the model to be honest".
- Обязательные пункты:
  - Prevention: RAG grounding, constrained outputs (schema, allowlists), better prompting, tool use over free-form generation.
  - Detection: retrieval-groundedness checks, self-consistency, classifier/evaluator, uncertainty thresholds.
  - Runtime: refuse to guess, "I don't know" fallback, log and alert, degrade gracefully.
  - Response plan: documented, tested, human review for critical paths.
- Частые ошибки: только add "don't lie" to prompt; no detection or fallback; treat all hallucinations as user error.
- Красные флаги: «LLM сам знает, когда галлюцинирует»; нет fallback.

### 5. How do you decide between using an LLM API vs self-hosting an open-source model?
- Идеал: trade-off analysis on cost, privacy, quality, and infra; decision made per use-case.
- Обязательные пункты:
  - API: fast to ship, no GPU, no MLOps burden — but per-token cost, latency, data leaves your control.
  - Self-host: data stays in-house, cost scales with GPU capacity; requires infra + ops skills.
  - Deciders: data sensitivity, volume (break-even point), required quality, team expertise, scale.
  - Hybrid: sensitive path self-hosted, bulk non-sensitive via API; benchmark quality difference first.
- Частые ошибки: думать self-hosting всегда дешевле; забыть про cost of ops/GPUs; ignore API latency variance.
- Красные флаги: «self-hosting бесплатно»; забыть privacy breach with API.

### 6. How do you manage stakeholder expectations for AI projects?
- Идеал: set realistic expectations early and continuously with concrete numbers, not promises of perfection.
- Обязательные пункты:
  - Frame AI as probabilistic: show expected accuracy, error modes, and guardrails — contrast with deterministic software.
  - Agree on success metrics and release criteria together (evals, thresholds, rollback).
  - Deliver incrementally with demos; communicate progress/blocks as they happen.
  - Manage scope: define what is NOT in scope; correct misconceptions (AI ≠ magic).
- Частые ошибки: overpromise at kickoff; hide failures until demo day; skip evals so no numbers exist to discuss.
- Красные флаги: «модель будет почти всегда точной» without measurements; deadline without baselines.

### 7. Describe your approach to debugging a poor-performing RAG system.
- Идеал: instrument and isolate the failure along the pipeline, then fix at the right layer.
- Обязательные пункты:
  1. Define the failure precisely with an eval set; categorize error (ranking, retrieval, generation, prompt, chunk).
  2. Check retrieval in isolation: are top-k chunks relevant? (embedding/query mismatch, chunk too big/small, filters).
  3. Then generation: does the model use good retrieved context when present?
  - Fix layers: chunking, embedding/reranker, query rewriting, prompt grounding, hybrid search (BM25+vector), citations to trace.
- Частые ошибки: blame the model first; change промпт randomly without measuring; not separating retrieval vs generation.
- Красные флаги: «проблема точно в модели» без проверки retrieval; tweak без eval.

### 8. How do you stay current with the rapidly evolving AI landscape?
- Идеал: structured, active learning that feeds work — not passive headline scanning.
- Обязательные пункты:
  - Primary sources: arXiv abstracts, model cards, official docs/blogs (OpenAI/Anthropic/Google/DeepMind).
  - Community: conference talks (NeurIPS/ICML), X/Twitter, newsletters, benchmark pages (lmsys, papers-with-code).
  - Hands-on: build small experiments/POCs with new APIs/models; read OSS code (transformers, vLLM).
  - Filter: prioritize what affects your product/stack; selective attention, not everything.
- Частые ошибки: только новости/YouTube; не практиковаться; пытаться следить за всем.
- Красные флаги: «читаю всё подряд каждый день», не способен назвать ни одного рабочего источника.

### 9. How do you balance innovation with reliability in AI systems?
- Идеал: separate risk — pilot innovations on non-critical paths, shield critical paths with guards and rollback.
- Обязательные пункты:
  - Use staged rollout: canary, shadow mode, A/B with automatic rollback gates.
  - Isolate blast radius: new models behind feature flags; keep deterministic fallback.
  - Evaluate before and after: evals + canary metrics (accuracy, latency, cost); halt on regression.
  - Process: review + sign-off for risky changes; "fast to try, fast to rollback".
- Частые ошибки: innovation kills production (no rollback); или reliability freezes innovation.
- Красные флаги: «меняем модель и наблюдаем за падением метрик через месяц» без canary.

### 10. Tell me about a challenging AI project you worked on...
- Идеал: STAR (Situation-Task-Action-Result) with the AI-specific trade-off honestly stated and a measurable outcome.
- Обязательные пункты:
  - Situation/Task: define the AI goal and the unique difficulty (data scarcity, latency, cost, quality ceiling).
  - Actions: concrete techniques used (prompting→RAG→fine-tune ladder, evals, guardrails).
  - Trade-offs: e.g. RAG over fine-tune for freshness; accuracy within latency budget; per-token cost vs self-host.
  - Results: quantifiable (accuracy %, latency, cost, user adoption, revenue) + one lesson learned.
- Частые ошибки: no numbers for outcome; no honest trade-off; story without AI specificity.
- Красные флаги: хвастается "сделал без ошибок"; не упоминает, что пошло не так.

### 11. How would you handle biased or harmful outputs in production?
- Идеал: treat as incident: contain, diagnose, fix at source, and add guardrails — not a one-off patch.
- Обязательные пункты:
  - Triage: reproduce, confirm harm, scope impact, pause/restrict affected service or add filter.
  - Root cause: is it data/system prompt/guardrail gap/model? Check bias test cases.
  - Fix: better system prompt + policy, output filtering/guardrails, red-teaming, targeted fine-tune; add regression evals for that case.
  - Monitor: bias/toxicity metrics, feedback loop, incident review.
- Частые ошибки: «просто добавлю запрет в промпт»; не фиксировать регрессию; не информировать пользователей.
- Красные флаги: «LLM нейтрален», «модель сама решит»; отрицать bias.

### 12. How do you approach cost optimization for an AI system that's exceeding budget?
- Идеал: measure first, cut the biggest cost item, then monitor spend.
- Обязательные пункты:
  - Instrument: per-feature token/GPU cost dashboard; identify top spenders by use-case.
  - Levers: smaller/cheaper model, prompt compression (fewer tokens, caching), prompt/semantic caching, batching + async, quantization, routing (small model first), self-host only when volume justifies.
  - Business figures: what does each query earn/save — kill low-value calls; budgets with alerts.
  - Track regressions: cost metrics in CI for prompt/model changes.
- Частые ошибки: сокращать качество вслепую; не измерять до оптимизации; забыть cost of cache/storage infra.
- Красные флаги: «перевод на бесплатную модель резко всё решит»; нет дашборда cost per feature.

### 13. Describe a time when you had to choose between model accuracy and latency...
- Идеал: decision driven by product SLAs and user impact, with measured trade-off and mitigation.
- Обязательные пункты:
  - Establish constraints: what latency is acceptable for the interaction (chat vs batch analysis).
  - Measure both candidates on the same eval set (accuracy) and target (p95/p50 latency, cost).
  - Pick/compromise: larger model + caching/streaming, or smaller model + fallback for critical correctness.
  - Mitigations: distillation, quantization, speculative decoding, partial streaming, routing.
  - Verify with A/B: business metric should not regress while p95 meets target.
- Частые ошибки: «берём самую точную модель» ignoring SLA; no latency measurement.
- Красные флаги: не знает p95; «точность важнее всего» без цены задержки.

### 14. How would you handle a situation where your AI system's quality degrades over time?
- Идеал: treat as drift — monitor, detect, root-cause, then refresh with minimal disruption.
- Обязательные пункты:
  - Detect first: production monitoring of quality (labels, feedback, downstream metrics) — not just user complaints.
  - Distinguish causes: data drift (input distribution), concept drift (task meaning), model drift (provider update), prompt rot (behavior/system change), dependency versions.
  - Act: refresh with new data / update prompt / swap model / tune retrieval; add eval regression.
  - Prevent: automated periodic re-evals, alert thresholds, refresh pipeline, versioned artifacts.
- Частые ошибки: «переобучим на новых данных» не зная, drift ли причина; нет мониторинга до жалоб.
- Красные флаги: «качество упало → переобучаем» без анализа причины; верит, что модель стабильна вечно.

### 15. How do you communicate AI limitations to non-technical stakeholders?
- Идеал: translate probabilistic behavior into concrete, business-relevant terms; give decision handles.
- Обязательные пункты:
  - Analogies + concrete numbers: "95% на наших тест-кейсах; 5% ошибок такой-то природы".
  - Focus on what the system can/can't do and error classes, guardrails built; no jargon (no "logits").
  - Show real examples side-by-side: good output vs error output.
  - Agree on risk appetite and mitigations (human-in-loop, thresholds) — not just explain.
- Частые ошибки: абстрактное «мы снижаем ошибки» без цифр; тех. жаргон.
- Красные флаги: считать stakeholders «глупыми»; не давать конкретных примеров.

### 16. How would you approach building an AI feature with limited labeled data?
- Идеал: leverage unlabeled data and transfer, and validate with a small but careful set.
- Обязательные пункты:
  - Pretrained models + few-shot prompting; active learning: label most informative samples.
  - Weak supervision: heuristics/rules/noisy labels → larger training set; synthetic data (validated).
  - Prefer RAG over fine-tuning when no labels needed.
  - Ensure eval set is representative even if small; watch overfitting.
- Частые ошибки: «надо больше данных» as excuse; drop quality because dataset small; ignore active learning.
- Красные флаги: «без 100k лейблов ничего не выйдет»; обучать с нуля на маленькой выборке.

### 17. Describe your experience working with cross-functional teams on AI projects.
- Идеал: show you translate between business/product/design/engineering — AI projects are inherently cross-team.
- Обязательные пункты:
  - Specific example with roles: PM set goal, data team provided data, designers did UX, engineers built, you coordinated.
  - How you resolved disagreements (scope/metrics) — concrete resolution.
  - You spoke "business" and "model" simultaneously: shared expectations set.
  - Named outcome + your contribution — own your part.
- Частые ошибки: фраза без конкретного примера; «работаю один с моделью»; не назвать, как решали конфликт.
- Красные флаги: blaming other teams; no example of alignment.

### 18. Where do you see AI engineering heading in the next 3-5 years?
- Идеал: informed, structured outlook (agentic, verification, efficiency, standardization) tied to skills.
- Обязательные пункты:
  - From chatbots to agentic systems: multi-step planning, tool use, memory — reliability + verification emphasis.
  - Systems focus: evals/observability/guardrails become core — AI engineering = reliability engineering for AI.
  - Efficiency trend: smaller/specialized models, distillation, quantization, cheaper inference at scale.
  - Standardization: protocols (MCP), platformization — less bespoke integration; role grows towards owning systems.
  - Personal: keep hands-on with evals/ops to sit at intersection of product and model.
- Частые ошибки: «модели станут бесконечно умнее»; ответ без упоминания агентов/надежности.
- Красные флаги: «AGI через 3 года решит всё» — вместо grounded.

### 19. Why are you interested in this AI engineering role?
- Идеал: 3 reasons — one technical, one product/impact, one career — aligned with the company.
- Обязательные пункты:
  - Technical: deep interest in building systems around models (evals, agents, LLMOps) — "engineering", not just demos.
  - Impact: AI changes how software is built; applying it to the company's problem to deliver value.
  - Growth: role at the intersection lets me keep learning across models, infra, product.
  - Alignment: name what the company actually does (one concrete line).
- Частые ошибки: generic answer ("I like AI"); no company/role specifics; no technical depth.
- Красные флаги: туманное «я люблю AI»; не различает энтузиазм и компетенцию.

### 20. Your PM wants to ship an AI feature with a 15% hallucination rate on edge cases. How do you communicate the risk?
- Идеал: reframe — quantify what 15% means in business terms, propose concrete mitigations, don't just refuse.
- Обязательные пункты:
  - Convert 15% to real impact: of X edge-case queries, Y wrong answers of severity Z.
  - Ask what happens on a wrong answer (financial/legal/UX harm) — risk varies by domain.
  - Mitigation ladder: guardrails, confidence thresholds, human review for high-stakes, "I don't know" fallback, gradual rollout with monitoring.
  - Agree on acceptable error level with PM; escalate if risk is unacceptable.
- Частые ошибки: flat refusal without alternatives; accepting 15% blind; no user-impact analysis.
- Красные флаги: «15% — это нормально» без контекста; не предлагает guardrails.

### 21. A non-technical executive asks why your AI feature cannot be 100% accurate. How do you explain LLM limitations?
- Идеал: plain-language mechanism — model predicts the most plausible next token, not a database lookup; analogy-driven; focus on mitigations and measurement.
- Обязательные пункты:
  - Mechanism: LLM picks the most plausible continuation — no ground truth, confident mistakes are possible.
  - Analogy: an experienced assistant answering from memory, not a calculator/encyclopedia.
  - Reassure with what we control: knowledge grounding (RAG), guardrails, human review, metrics we track.
  - Frame: 100% is impossible for open-ended language, but we manage and measure error.
- Частые ошибки: technical jargon (logits/temperature); promising near-100% accuracy; defensiveness.
- Красные флаги: «LLM — это база знаний»; обещает 99.9% на открытых задачах.
### 22. You need to choose between a complex agentic system that scores 15% better on benchmarks, or a simpler RAG pipeline that is easier to maintain. How do you decide?
- Идеал: decision driven by real product impact and maintainability, not benchmark score alone.
- Обязательные пункты:
  - Question whether the benchmark measures the business outcome users actually care about.
  - Compare TCO: agentic = more components, harder to debug, more failure modes vs RAG = simpler, debuggable.
  - A 15% benchmark delta may not move the business metric — small measurable win vs complexity.
  - Decide: start with the simpler system, add complexity only when evals show real user-facing need.
- Частые ошибки: picking agentic purely on benchmark delta; ignoring ongoing maintenance cost.
- Красные флаги: benchmark-above is not enough without context; ignores maintainability.
