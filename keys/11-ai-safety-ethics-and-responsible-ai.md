# AI Safety, Ethics, and Responsible AI — Answer Key (1-45)

### 1. What are hallucinations in LLMs, and how do you mitigate them?
- Идеал: Hallucination = confident false content; fluently generated, not modeling of uncertainty. Mitigation = retrieval grounding + verification, not prompting alone.
- Обязательные пункты:
  - Cause: next-token prediction, no truth model, overfit to text patterns; coaxed by leading questions.
  - Mitigation: RAG/retrieval grounding, tool calls (search/code/calculator), citations, fact-checking model, constrained decoding, abstention ("I don't know").
  - Tuning: proper temperature/top-p, eval suite tracking hallucination rate.
- Частые ошибки: думать, что «вероятность» или «больше данных» полностью убирают галлюцинации; не упоминают retrieval/grounding.
- Красные флаги: «LLM можно научить не галлюцинировать» одним промптом; «проблема только в температуре».

### 2. What is prompt injection, and what are the different types (direct, indirect)?
- Идеал: Prompt injection — attacker slips instructions into the text the app sends to the LLM so it follows attacker over developer.
- Обязательные пункты:
  - В корне: instructions and data share one channel; model can't reliably tell system instructions from user/retrieved text.
  - Direct injection: attacker is the user typing malicious instructions directly (e.g. "Ignore your rules…" as input).
  - Indirect injection: attacker hides instructions in data the model reads (web page, document, email, tool output) — turns our own feature into attack surface.
  - Not like SQL injection: there's no separate query/instructions layer to parameterize; defense is design-time.
- Частые ошибки: думать, что escaping/sanitizing текста решает; путать indirect с XSS.
- Красные флаги: «промпт-инъекцию можно полностью заблокировать фильтром», не понимать, что система промпт — тоже текст, который можно перебить.

### 3. How do you implement input and output guardrails for AI systems?
- Идеал: Guardrails = safety checks around the LLM: input guardrail before the model, output guardrail after it.
- Обязательные пункты:
  - Input guardrail: classifies/validates the user message (topic policy, safety): unsafe → refuse, LLM never sees it.
  - Output guardrail: checks the LLM answer for private data, harmful content, format before delivery.
  - Guard model: small/vocabulary-bounded classifier returns safe/unsafe (0 risk of "forgetting" constraints, calibrated); or another LLM as judge.
  - Walkthrough: unsafe "make a weapon" → stop at input; safe "bank hours?" → main LLM → output guard → user.
- Частые ошибки: полагаться только на system prompt; проводить инъекцию в output-фильтр.
- Красные флаги: «guardrails = system prompt», «guard также должен галлюцинировать», не упоминать выходную проверку.

### 4. What is AI alignment, and why is it important?
- Идеал: Alignment = making the model follow intent, be genuinely helpful, honest, harmless — best taught via RLHF (InstructGPT) / standard formulation.
- Обязательные пункты:
  - Original GPT-3 was not enough: next-token prediction learned text, not intent; model was smart but unaligned.
  - InstructGPT alignment prompt: HHH (helpful, honest, harmless).
  - 3-step: SFT → Reward Model (learn preferences, reward signal) → RL with PPO maximize reward; KL penalty against drifting too far.
  - Alignment tax: cost/loss in quality; size lost to alignment (1.3B InstructGPT preferred over 175B GPT-3; 175B InstructGPT beaten in 85% comparisons).
- Частые ошибки: путать alignment с просто «следовать инструкциям»; не упоминать RLHF/PPO.
- Красные флаги: «alignment = заставить модель говорить правду», не знать HHH, «RLHF без KL».

### 5. How do you detect and mitigate bias in AI systems?
- Идеал: Bias = systematic unfair error against a group; detect at data/model/output, mitigate at each stage. (Synthesize.)
- Обязательные пункты:
  - Detect: data audits (representation — gender/race/source skew), metrics by subgroup (accuracy/FN/FP gaps, statistical parity, equalized odds), calibration checks.
  - Mitigate data: rebalance sampling, synthetic data, remove non-causal proxies carefully; model: fairness constraints, post-processing thresholds.
  - Process: diverse eval sets, red-teaming, ongoing monitoring over distribution drift; document limits.
- Частые ошибки: смотреть только на общую метку качества; атрибутировать всё модели, забывая данные; «добавил ресемплинг — bias ушёл».
- Красные флаги: «bias можно устранить навсегда» (пере-возникает), «просто удалить атрибуты» (прокси остаются).

### 6. What are the key data privacy considerations (GDPR, CCPA) when building AI applications?
- Идеал: Сбор/использование персональных данных регламентированы; нужны законное основание, прозрачность и контроль пользователя.
- Обязательные пункты:
  - GDPR: lawful basis, purpose limitation, data minimization, DPIA for high-risk; rights: access, erasure ("right to be forgotten"), portability, objection, automated-decision explanation.
  - CCPA/CPRA: California — disclosure, right to know, delete, opt-out of sale/sharing, no retaliation.
  - Engineering: consent management, PII inventory/DLP, encryption in transit+at rest, retention limits (data minimization), vendor DPAs, DPIA; never send sensitive data to external APIs without basis — only what's needed (целевой сбор).
- Частые ошибки: путать GDPR (права, автоматизированные решения) и CCPA (opt-out) требования; думать, что anonymization всегда безопасно.
- Красные флаги: «анонимизировал — GDPR не применим» (без доказательной де-идентификации часто неверно).

### 7. How do you handle PII in LLM inputs and outputs?
- Идеал: Treat PII as untrusted input data with DLP layer at input + detection at output, since LLMs echo or leak text. (Synthesize + guardrails file.)
- Обязательные пункты:
  - Input: redaction/NER, masking before prompt, no storage unless needed; allowlist of allowed categories.
  - Output: guardrail scan for PII (names, emails, SSN, phone, IP) — block/redact before user; LLM partnerships: send only на внутренних approved средах.
  - Prompt design: system instruction "не выводи PII"; не складывать ключи в промпт.
  - Logs: encrypted with access control, retention limit; data minimization.
- Частые ошибки: полагаться на system prompt, чтобы LLM не повторял PII; не проверять output. Красные флаги: «PII в промпте — ок, если не логировать»; «модель не может утечь данные».

### 8. What is explainability in AI, and why does it matter?
- Идеал: Explainability — способность объяснить, почему модель дала результат, в терминах, понятных человеку; критична для доверия и ответственности.
- Обязательные пункты:
  - Why: trust, debugging, compliance (GDPR automated decisions), audit, catching bad behavior.
  - Types: local vs global explanations; model-agnostic (SHAP/LIME) vs intrinsic (linear models/trees).
  - Tradeoff: accuracy ↔ interpretability; deep models черный ящик → post-hoc approximations.
- Частые ошибки: считать, что глубокие модели принципиально необъяснимы и это ок; путать post-hoc с причинностью.
- Красные флаги: «SHAP покажет причину решения» (это атрибуция, не причинность); «accuracy всегда важнее объяснимости».

### 9. What is the difference between interpretability and explainability?
- Идеал: Interpretability — свойство самой модели (прозрачность устройства); explainability — постфактум объяснение конкретного решения — могут давать даже «чёрные ящики».
- Обязательные пункты:
  - Interpretable model: человек может понять её внутреннюю логику (линейные, деревья, правила) — «насколько мы понимаем модель».
  - Explainable: объяснения конкретных предсказаний (SHAP/LIME/saliency) — «почему этот ответ». Интерпретируемая модель сама себе объяснение.
  - Key difference: interpretability — intrinsic property (built-in); explainability — often post-hoc, approximate, can be inconsistent.
- Частые ошибки: использовать термины как синонимы; думать, что объяснения для чёрных ящиков дают полную гарантию точности.
- Красные флаги: «объяснил значит интерпретируем», «post-hoc объяснения точны на 100%».

### 10. What is mechanistic interpretability, and why do AI labs invest in it?
- Идеал: Mechanistic interpretability — reverse-engineering the model's internal circuits/features to understand mechanisms, not just attribution. (Synthesize.)
- Обязательные пункты:
  - Goal: find features/attention heads/MLP circuits performing actual computations (e.g., induction heads, truthfulness circuits).
  - Why labs invest: safety (detect deception/backdoors/overly good at tasks), alignment/control, debugging, nudging models, tools like SAE (sparse autoencoders).
  - Hard: models too large, features polysemantic, non-linear — reverse-engineering scale is enormous.
- Частые ошибки: путать с SHAP-объяснениями единственного предсказания; думать, что это готовый инструмент продакшена.
- Красные флаги: «мы интерпретируем каждый нейрон» (полисемантия), «механистическая интерпретируемость = объяснение вывода пользователю».

### 11. How do you build trust with users in AI-powered applications?
- Идеал: Trust — через прозрачность (что делает/не делает), объяснимость решений, надёжность и контроль пользователя.
- Обязательные пункты:
  - Transparency: label AI involvement, show confidence/uncertainty, disclose limits.
  - Behavior: consistent accuracy, graceful failures/abstention, fast honest errors; human oversight for high-stakes.
  - Control: user can override, appeal, opt out; privacy respected — no creepy surveillance.
  - Process: model cards, data provenance, incident reporting.
- Частые ошибки: ожидать, что trust достигается одним «мы объясним всё»; скрывать промахи.
- Красные флаги: «надёжность не важна, главное интерфейс», «обещаем идеальную точность» (создаёт over-reliance).

### 12. What are adversarial attacks on AI systems, and how do you defend against them?
- Идеал: Adversarial attacks — crafted inputs that flip a model's behavior (perturbation, evasion, poisoning, prompt injection); defense layered. (Synthesize.)
- Обязательные пункты:
  - Types: evasion (white-box FGSM/PGD, transferable black-box), poisoning (training data), prompt injection, backdoors.
  - Defense: adversarial training (train on perturbed inputs), input sanitization/validation, robust preprocessing, ensemble, anomaly detection, monitoring; for LLM: guardrails, tool isolation, output filtering.
  - Tradeoffs: more robustness → accuracy/overhead cost; no perfect defense—treat as arms race, monitor.
- Частые ошибки: полагаться на один фильтр; считать, что «модель можно полностью защитить»; игнорировать соц. engineering/инъекции в данные.
- Красные флаги: «adversarial robustness = просто больше данных», «защита от атак на 100%».

### 13. What is data poisoning, and how can it affect AI models?
- Идеал: Data poisoning — adversary injects malicious samples into training set so the model learns wrong behavior.
- Обязательные пункты:
  - Effects: degraded accuracy, targeted backdoors (trigger + intended misclassification), hidden behavioral shifts (e.g., loan model favors attacker's profile).
  - Types: label flipping, backdoor/trigger injection (patch), clean-label poisoning.
  - Defenses: data provenance/vetting, sanitization/filtering outliers, robust aggregation (e.g., in federated learning — trimmed mean, Krum), poisoning-resistance eval.
- Частые ошибки: думать, что poisoning possible только с доступом к обучению (поставщик данных тоже источник).
- Красные флаги: «дата-поизининг = переобучение», «валидационный сеть всегда поймает».

### 14. How do you implement content safety filters for AI-generated content?
- Идеал: Сочетание входного и выходного guardrail, классификатора и политик — content policy-фильтры по линиям from guardrails article (топик, вредоносность, приватность, формат, фактчность).
- Обязательные пункты:
  - Input guard: проверить вредоносность запроса до модели (модель не видит unsafe).
  - Output guard: проверить сгенерированный ответ (private data, harm, format, factuality) до пользователя.
  - Use dedicated small guard-model classifier (safe/unsafe calibrated, может только 2 ответа) или LLM-as-judge; policy-эмбеддинги.
  - Walkthrough: unsafe request → отказ; safe request → main LLM → output guard → пользователь.
- Частые ошибки: фильтровать только input; верить system prompt как фильтру (не детерминирован).
- Красные флаги: «фильтр на вывод ненужен», «guard и главная LLM одна и та же модель» (не категоричный).

### 15. What is responsible AI, and what frameworks exist for implementing it?
- Идеал: Responsible AI — developing AI that is fair, transparent, accountable, privacy-respecting and beneficial; operationalized via frameworks. (Synthesize.)
- Обязательные пункты:
  - Pillars: fairness, transparency/explainability, accountability, privacy, robustness/safety, human oversight (often defined by Google/Microsoft/shareholders as principles).
  - Frameworks: NIST AI RMF (Measure-Manage-Map-Govern), EU AI Act (tiered risk), OECD AI Principles, UNESCO Recommendation on Ethics of AI, IEEE 7000.
  - Delivery: responsible design into lifecycle (data → model → deployment → monitoring), governance roles.
- Частые ошибки: сокращать до «принципы в README»; думать, что ответственный AI создаётся одной командой без процессов.
- Красные флаги: «ответственный AI = AI Safety только про выход из-под контроля», «frameworks есть, а конкретики нет».

### 16. How do you handle copyright and IP concerns with AI-generated content?
- Идеал: Copyright — реальная угроза: модель может писать verbatim protected text; должен быть detection + policy. (Synthesize; ties to Q25.)
- Обязательные пункты:
  - During training: data provenance/licenses (curated datasets, licensing), opt-out corpora (C4-подобные), provider terms.
  - At inference: can't unlearn verbatim → detection tools (duplicate / fingerprint / watermark / query) + guard, filter output, allowlist.
  - Generated content ownership: unclear — do not claim; label AI-generated; choose public-domain aligned data.
  - Legal: IP indemnification clauses, vendor лицензии.
- Частые ошибки: думать, что генерация означает право на использование.
- Красные флаги: «у нас нет рисков, мы не храним данные», путают плагиат с copyright.

### 17. What is the EU AI Act, and how does it affect AI engineering?
- Идеал: первый comprehensive закон об AI — про obligation по уровню риска (risk-based). (Synthesize.)
- Обязательные пункты:
  - Risk tiers: prohibited (e.g., social scoring, real-time remote biometric identification в общественных местах), high-risk (critical infra, education, employment, immigration/kinds — обязательная система), limited (transparency duties), minimal.
  - High-risk obligations: risk management system, data quality/governance, technical documentation, record-keeping (audit), TRACEABILITY, human oversight, accuracy/robustness metrics.
  - Impact on engineering: compliance → DPIA-type assessments, documentation/auditability 1st-class, testing adversarial, на deploy; deadlines shifting; вне EU effect (extraterritorial, value chain).
- Частые ошибки: путать с GDPR (разные законы, но GDPR еще действует); думать AI Act = запрет ИИ.
- Красные флаги: «AI Act запрещает все генеративные модели», «просто подписал and сдал».

### 18. How do you implement audit trails and logging for AI decisions?
- Идеал: Audit trail — immutable chain of records: вход, версия модели, выход, решение, человек, контекст.
- Обязательные пункты:
  - What to log: request/features/заключая PII (minimized or encrypted), model version & weights hash, input/output, scores, confidence thresholds, human oversight decisions.
  - How: append-only или cryptographically signed logs (hash chains), time-stamps, correlation IDs; структура для compliance (GDPR Art. 22, EU AI Act Art. 12).
  - Mechanism: structured logs → data warehouse → queryable with retention policies.
- Частые ошибки: логировать только вход/выход без версии модели; незащищённые логи нарушения.
- Красные флаги: «аудиты нужны только по закону», «мы удаляем логи за 30 дней без политики» (re-identification).

### 19. What is model card documentation, and why is it important?
- Идеал: Model card — стандартный документ с характеристиками модели, подобно паспорту для людей: отчет и данные. (Synthesize.)
- Обязательные пункты:
  - Content: intended use, training data/eval metrics, performance by subgroup, limitations, bias, recommended thresholds, caveats.
  - Why: transparency to users/audits, reproducibility, trust, informing deployment decisions.
  - Example: Google Model Cards / Hugging Face model cards — performance metrics breakdown.
- Частые ошибки: модель-карточку пишут один раз навсегда (обновлять).
- Красные флаги: «модель-карточка — это README», «не нужна, когда нет закона, требующего» (но она полезна везде).

### 20. How do you handle misuse and abuse of AI systems in production?
- Идеал: Misuse handling — detect, contain, respond, prevent; multi-layer approach.
- Обязательные пункты:
  - Detect: anomaly, rate-limit, behavior scoring; monitoring abuse patterns (prompt injection attempts, attack frequency).
  - Contain: limit blast via sandboxing tools, deny access, guardrail.
  - Respond: incident playbook — alert, quarantine, deploy countermeasure; log everything.
  - Prevent: abuse detection (abuse@), rate limits, WAF-type checks, feedback loop to improve filtering.
- Частые ошибки: ждать инцидента и реагировать вручную; путать misuse с malfunction.
- Красные флаги: «один firewall всё решит», «block users навсегда без эскалации» (несправедливо).

### 21. What is differential privacy, and how can it be applied during model training?
- Идеал: Differential privacy — формальная гарантия: результат анализа почти одинаков независимо от присутствия одного пользователя в наборе данных ε-части (noise).
- Обязательные пункты:
  - Definition: алгоритм M удовлетворяет ε-DP если для соседних наборов данных вероятность выхода отличается ≤ e^ε — bound on information leakage.
  - Noise mechanism: Laplace/Gaussian noise (часто ε од).
  - Training: DP-SGD — clip gradients, add noise (это разнообразие), бюджет ε: optimize privacy-utility-ε tradeoff.
  - Budget: ε композиция ухудшается; choose ε criteria; helps re-identification protection.
- Частые ошибки: думать, что DP = просто анонимизация без шанса проследить данные, отсутствие формальной дефиниции.
- Красные флаги: «DP — это шифрование», «единственный способ — шум» без ε-бюджета; путать с k-anonymity.

### 22. How would you design an AI incident response plan? (~120 words)
- Идеал: Incident plan cover full lifecycle: detect → assess → contain → respond → recover → learn. (Scenario-like design.)
- Обязательные пункты:
  - Detection: monitoring, anomaly alerts, user-facing escalation paths.
  - Roles: on-call/incident commander, legal/comms/security; severity levels (S1-S3).
  - Response: containment (disable feature, revoke keys), runbooks, communication templates, stakeholder notification (users, regulators).
  - Post-mortem: blameless, track readiness as root causes, restore trust; ticketing automation (alerting pipeline).
  - Tests: fire-drill/chaos practising реакцию.
- Частые ошибки: план только «на бумаге» без owner'а и контактов; нет тестов.
- Красные флаги: «реагируем только после жалоб»; «no SLA/call tree» (неборьба с readiness).

### 23. What is the NIST AI Risk Management Framework (AI RMF)?
- Идеал: NIST AI RMF — voluntary framework from US NIST for managing AI risk, cross-sector, in 4 functions (Govern, Map, Measure, Manage), plus core. (Synthesize.)
- Обязательные пункты:
  - Structure: Govern (governance/oversight), Map (context/landscape of risk), Measure (metrics/assess risks with evidence), Manage (act on risks, treat/accept/transfer, document).
  - Principles: risk-based (not prescriptive compliance), socio-technical, voluntary; profiles and trustworthiness characteristics: valid & reliable, safe, secure, fair, transparent/explainable, accountable, privacy-enhanced.
  - Update: AI RMF 1.0 (Jan 2023), has Generative AI Profile.
  - Relation: complements EU AI Act; not legally binding.
- Частые ошибки: думать, что это сертификация/обязателен; путать функции с его примерами.
- Красные флаги: «NIST RMF = реестр запретов», «когда ты его обязательный, he shall» (voluntary).

### 24. Your healthcare chatbot gives medical diagnoses it should not make. How do you add safety guardrails?
- Идеал: Diagnose → restrict scope: it should refuse to diagnose, route to professional. Guard on both input/output. (Apply guardrails article to healthcare.)
- Обязательные пункты:
  - Input guard: detect request for diagnosis/self-diagnosis intent → refuse/redirect ("I can't diagnose; see a doctor").
  - Output guard: check outputs — no definitive medical claims, flag uncertainty, add disclaimer, only cite general info.
  - Scope: define allowed topics (medication reminders, appointment info, definitions) via policy; disallow diagnosis of symptoms, prescription adjustments.
  - Layer: medically trained review, high-stakes → human escalation, escalation paths (crisis → emergency).
  - Zero-shot classifier/guard-model for intent; eval: red-team medical prompts.
- Частые ошибки: полагаться на system prompt; нет выходной проверки. Красные флаги: «модель сама знает, когда не отвечать»; «disclaimer alone достаточно».

### 25. Your AI system is reproducing copyrighted material verbatim. How do you prevent this?
- Идеал: Detect verbatim duplication at inference + control training/data sources. (Synthesize.)
- Обязательные пункты:
  - Training data: curated licensed datasets, exclude copyrighted/unlicensed corpora, use opt-out requests, learn provider terms.
  - Inference: detect exact duplication of protected text: fingerprinting/matching (embedding or hash-of-ngram) against protected source, substring overlap detection, watermarking to prove origin.
  - Mechanism: run input/output -> filter, block or refuse; also monitor long exact quotes.
  - Label generated content, implement opt-out for authors (fair use option).
- Частые ошибки: полагаться только на «мысленно не выдаём» — LLM often memorizes strings; забыть про quoting in prompts.
- Красные флаги: «мы придумали новый текст, значит не нарушаем» (даже paraphrase так), «законные пути не нужны».

### 26. Your resume screening AI rejects more female candidates for engineering roles. How do you fix gender bias?
- Идеал: Diagnose root cause (data skew → model bias) → fix at data/feature/eval → monitor. (Scenario.)
- Обязательные пункты:
  - Measure: rejection rates by gender in eval/test, false-negative gap, perform stratified analysis.
  - Fix data: rebalance training labels (same resumes with different names), remove gendered features/text markers, use neutral features; post-process thresholds equalize outcomes where legal.
  - Model: adversarial debiasing, fairness-aware training, outcome monitoring; validation with blind test.
  - Process: bias committee, external audit, legal review (нельзя создавать quotas unduly), transparency report.
  - Result: reduce gender gap while keeping hit-rate.
- Частые ошибки: просто удалить поле «женский» из резюме без признания текстовых прокси; смотреть только на общий accuracy.
- Красные флаги: «давайте просто добавим больше женщин в трейнинг — решает всё»; «bias — это только данные, не модель».

### 27. Your AI model passes bias checks by gender and race separately, but fails for intersectional groups. How do you handle it?
- Идеал: Independent subgroup fairness ≠ intersectional fairness; check all intersection cells. (Scenario.)
- Обязательные пункты:
  - Cause audit: single-dimension checks mask multiplicative/compound effects (e.g., females of certain race bear both).
  - Action: add intersectional metrics (rate/error by gender×race combined), ensure each cell has enough examples; sample representation.
  - Mitigate: rebalance over intersection cells, calibration per group, fairness post-processing over composite protected groups.
  - Verify with holdout cells; document limits where data insufficient; periodic re-audit.
  - Eval: precision/recall/FN per intersection, not just overall parity.
- Частые ошибки: думать, что независимые chек'и достаточно; максимизировать only head-count parity.
- Красные флаги: «нам хватает 10 женщин в группе», игнорировать малые подгруппы как «статистический шум».

### 28. Your AI denied a loan, and the customer demands a GDPR explanation. How do you provide one?
- Идеал: GDPR Art. 22 (automated decision) — right to explanation: meaningful information about logic + right to request human review. (Scenario.)
- Обязательные пункты:
  - Verify legal basis: is it sole automated decision with significant effect? If yes — offer human intervention/contest.
  - Provide meaningful explanation: main factors (features) that led to decision, model logic at general level, provide reasons in ordinary language + contact/rights.
  - Mechanism: model-agnostic explanation (features, score, SHAP summary), appeal/rectification path.
  - Ensure transparency: letters include data used, decision reasons, channels for human review and correction; respect времени в разумный срок.
  - If compliance gap: freeze system until design allowed, add human-in-the-loop.
- Частые ошибки: говорить «модель решила», не давая права оспорить; выдавать черный ящик (нет объяснения факторов).
- Красные флаги: «GDPR не позволяет deny без трик-ап» (это про силу), «мы не обязаны объяснять, это trade secret» (это зона конфликта, но право на объяснение есть).

### 29. A user invokes the right to be forgotten, but their data is in your model weights. How do you comply?
- Идеал: Removing from weights is infeasible (no direct mapping); GDPR compliance is procedural + data-level. (Scenario.)
- Обязательные пункты:
  - Scope: erasure from training pipeline where feasible — delete raw records, logs, derived copies, not weights of millions params.
  - If impossible in weights: implement legal defensible process — document impossibility, minimize extent, retrain/expunge at full-model level only if meaningful (rare), use differential-privacy explanation.
  - Route: data erasure request workflow, right to object on profiling; maintain erasure audit.
  - Better: collect only necessary data (minimization), don't store PII in training corpora, use data deletion-as-service (no joiner).
- Частые ошибки: думать, что можно выборочно «вырезать запись» из весов; отвечать игнорированием, когда это невозможно.
- Красные флаги: «кнопка удаления удалит из весов», «модель не хранит данные, так что нечего удалять» (ложно: может запечатлеть), решение retrain for every запрос нереалистично.

### 30. The EU AI Act may classify your AI system as high-risk. How do you comply?
- Идеал: High-risk obligations: risk management, data governance, logging, human oversight, transparency, accuracy/robustness, conformity assessment. (Scenario.)
- Обязательные пункты:
  - Map classification (Annex III domains e.g., employment, credit) → high-risk; conduct conformity assessment.
  - Implement: documented risk management system, quality data, audit logs (record-keeping), human oversight design, testing (adversarial/edge cases), registrations in EU database.
  - Technical documentation (traceability), EU declaration of conformity + CE marking.
  - Post-market monitoring and reacting to incidents; designate responsible person/procurement.
  - If borderline → consult legal + mitigate to lower risk.
- Частые ошибки: думать «мы только строим инструмент», не регулируемся; пренебрегать управлением рисками.
- Красные флаги: «high-risk — только для медицинских» (неправда: employment/credit и пр.), «нас не касается, мы B2B».

### 31. Your differentially private model lost significant accuracy. How do you balance privacy and utility?
- Идеал: Privacy-utility tradeoff: tune ε/mechanism/structure. Not universal; increase ε, post-process, use dedicated algorithms. (Scenario.)
- Обязательные пункты:
  - Diagnose: is loss from noise, noisy gradient clipping, or model architecture? Profile budget.
  - Tune: increase ε (accept weaker guarantee), lower clipping C, adaptive methods, smaller noise on important parameters.
  - Restructure: sample more data, use transfer/pretrained features, limit noise to sensitive subset, change DP-SGD schedule/noise schedule.
  - Use formal guarantees documenting ε, decision of acceptable level by compliance; report.
  - Alternative: treat data as sensitive but do not falsely degrade; maybe relax requirement based on risk.
- Частые ошибки: думать, что «бит DP — бит всегда» без настройки; никогда не сравнивать альтернативные алгоритмы.
- Красные флаги: «больше шума = больше privacy = значит лучше»; снижать требования без оценки фактических рисков.

### 32. One malicious participant is poisoning your federated learning model. How do you defend against it?
- Идеал: Federated poisoning — malicious client manipulates gradients/model updates; use robust aggregation + anomaly detection. (Scenario.)
- Обязательные пункты:
  - Detect: outlier detection on updates (norm, cosine distance), contribution scoring, anomaly/sybil detection.
  - Defense aggregation: trimmed mean, Krum, coordinate-wise median — robust to outliers; FLTrust/server-based weighting.
  - Server: verify/validate updates, keep small fraction; key rotations, verifiable aggregation, secure aggregation.
  - Monitoring & quarantine: flag bad client, reduce its influence, retrain from healthy clients; adversarial tolerance and ablation.
  - Repeat: limit data from untrusted clients, require checks.
- Частые ошибки: ФедСреднее (averaging) без защиты — vulnerable; думать, что сервер видит все updates — not necessarily.
- Красные флаги: «fedavg безопасен сам по себе», «мы доверяем всем клиентам одинаково».

### 33. Your AI hiring model uses proxy features for protected attributes. How do you eliminate proxy discrimination?
- Идеал: Proxies (e.g., zip code, name, school) correlate with protected attributes → discrimination; audit + redesign. (Scenario.)
- Обязательные пункты:
  - Detect: correlation of features with protected attributes, Shapley/contribution analysis, probe subgroup metrics (ablation), residual correlation testing.
  - Mitigate: remove/limit proxy features (but rel. to legit predictors), fairness constraints (sensitive feature agnostic), adversarial debiasing, post-processing thresholds.
  - Document: explain that removing a feature is not enough if others correlate; use multi-dimensional labels.
  - Legality: prove business necessity of proxies, disparate impact analysis, multi opposition.
  - Continuously monitor for new proxies (e.g., school names change).
- Частые ошибки: удалить явный атрибут и думать, что bias исчез (name, education, location — где прокси).
- Красные флаги: «мы просто убрали поле 'пол', значит всё ок», «прокси может быть нейтральным» (неявно дискриминируют).

### 34. Your predictive model creates a feedback loop of biased outcomes. How do you break it?
- Идеал: Feedback loop = biased predictions shape future data → reinforcing bias; break by detecting and correcting data flow. (Scenario.)
- Обязательные пункты:
  - Diagnose symptom chain: model influences decisions → changes future inputs (selection bias, label feedback), self-reinforcement.
  - Break loop: collect neutral baseline data, use exploration (active learning, randomization), re-label/decouple labels, don't feed predicted outcomes back as ground truth.
  - Monitoring: drift/parity metrics over time, detect feedback effect via causal/ablation.
  - Corrective: retrain with fresh human labels, downweight stale feedback, human feedback loop, lessons learned.
  - Governance: change operational loop, add guardrails.
- Частые ошибки: думать, что переобучение само исправит; не учитывать, что корреляция растёт, потому что модель «выполняла» цель (reflection).
- Красные флаги: «мы не трогаем данные, т.к. модель стабильная», «feed-backлoops are normal» (без диагностики).

### 35. Your AI generates fake news images. How do you implement watermarking for AI-generated content?
- Идеал: (from reference) LLM watermarking — hidden statistical signal with secret key + detector; for images — similar hidden imperceptible signal baked into pixels/audio/video. (Scenario.)
- Обязательные пункты:
  - Approach: add robust imperceptible watermark during generation (e.g., SynthID-style), keyed by owner.
  - Detection: detector with the same key reads the hidden pattern back — no DB storage, measurable confidence (statistical proof in content), works on parts of content.
  - Limitations honest: needs key, works only if added, robust to small edits, weak to heavy rewriting/translation/compression; not a final proof.
  - Same idea generalizes: for images/audio/video hide an imperceptible signal in pixels/sound that a keyed detector can read back (e.g. SynthID).
  - Also embed metadata, but that's trimmable; combine with standards (C2PA) + provenance.
- Частые ошибки: думать, что watermark виден; полагаться на метаданные как единственный слой; думать, что детектор работает без ключа.
- Красные флаги: «watermarking = просто post-processing надпись», «один watermark решает всю проблему» (не защищен от атак).

### 36. Your AI denies a service, and the user has no way to challenge it. How do you design an appeals process?
- Идеал: Users need mechanism to contest automated decisions (GDPR Art. 22 / EU AI Act human oversight). (Design scenario.)
- Обязательные пункты:
  - Provide clear reason for denial (explanation of factors) with concise, non-technical language.
  - Human review path: escalate to trained reviewer, user can submit counter-evidence/correction.
  - Formal steps: appeal submission (via UI/email), SLA (e.g., 7-15 days), decision log, escalation to second reviewers.
  - Fairness: appeals must be free, easy, accessible; no retaliation; keep audit log of appeal outcomes to catch bias.
  - Continuous: track appeal rate and outcomes per segment to discover model errors/bias; close loop to model monitoring.
- Частые ошибки: создание процесса без человеков (система пересматривает сама себя); не прозрачность корректировок данных.
- Красные флаги: «человек просто читает те же результаты модели»; «апелляцию сам решает модель».

### 37. An auditor asks why your AI rejected a request 6 months ago, and you have no logs. How do you build audit trails?
- Идеал: Architected auditability from the start: record every decision + inputs, immutable. (Scenario → system design.)
- Обязательные пункты:
  - Design: every decision → structured event {timestamp, user/message hashed/anonymized, model id+version hash, input (minimized), output, score/confidence, thresholds, outcome (approve/deny), reviewer decisions, flags}.
  - Storage: append-only/immutable log (hash chains, WORM storage), encryption-at-rest, access controls.
  - Align with compliance: retention policy per GDPR/EU AI Act, allow request (audit exports), correlation/trace-id.
  - Sub-second: async write to durable store, don't sync-block serving path; data minimization (no raw PII in logs).
  - Process: periodic audit simulation, alert on gaps.
- Частые ошибки: логировать только финальный результат без причины; хранить лишние PII.
- Красные флаги: «логи чистим за 30 дней для экономии» (нарушает auditability), «мы доверяем среднему логу».

### 38. You removed PII, but users were re-identified from anonymized data. How do you prevent re-identification?
- Идеал: Anonymization alone is weak; re-identification via linking, quasic-identifiers, small cells. (Scenario.)
- Обязательные пункты:
  - Diagnose anatomy: dataset uniqueness (quasidentifiers: age, zip, date), linkage with external data.
  - Apply: k-anonymity/l-diversity/t-closeness for quasi-id cells, generalization/suppress cells <k rows, add noise.
  - Do not over-sanitize PII only; require community eval: adversarial re-identification attempt, metrics (k, uniqueness).
  - Differential privacy as stronger alternative: formal bound against any linkage, demonstrate ε.
  - Policy: data governance, no data-mining of inferred profiles, deletion/retention limits, re-ID as prohibited act, periodic re-audit.
- Частые ошибки: думать, что «удалил имя = анонимизировано»; не покрыть quasi-identifiers.
- Красные флаги: «анонимизация — это одно поле», «k-anonymity решает всё» (needs l-diversity too), «data is safe if no direct link observed».

### 39. A pre-trained model from an open-source repo may contain a hidden backdoor. How do you detect it?
- Идеал: Backdoor = hidden trigger → malicious behavior; detection by trigger-finding + behavioral tests. (Scenario.)
- Обязательные пункты:
  - Security review of repo/artifacts: hashes (compare with official releases), provenance, vendor credentials.
  - Behavioral tests: adversarial audit — trigger-injection probing (perturbations/patches, sentiment/toxicity jailbreaks), evaluate on trigger templates, robustness to weird patterns.
  - Debug: weights auditing (weight distributions, anomalous activations), outlier unit detection, SAE/interpretability probes on suspicious behavior.
  - Air-gap/staging: test in isolated env, differential eval vs known-good model, red-teaming with known attacks.
  - If suppressed trigger found → quarantine, retrain/find clean checkpoint, report.
- Частые ошибки: доверять URL репозитория без сверки хэшей; думать «красная команда — только промпты», не контролируют trigger-паттерны.
- Красные флаги: «модель прошла обычные тесты, значит чистая», «open-source = безопасно».

### 40. Your LLM's training data was deliberately poisoned by an adversary. How do you respond?
- Идеал: Incident response: detect → isolate → clean → verify → prevent. (Scenario.)
- Обязательные пункты:
  - Detect: anomalous behaviors, dedicated poisoning audits (trigger tests, outlier inputs), data provenance review.
  - Isolate: hold model, block new generation, prevent spread (don't fine-tune new models from it).
  - Response: begin severity assessment, contain exposure; investigate scope (reproducer, which data poisoned), notify affected teams.
  - Fix: remove/relabel poisoned data, retrain cleaned corpus; fingerprint monitoring; revert if needed.
  - Harden: provenance controls (sanity-filter corpus, allowlist sources, anomaly on data balance), future red-teaming.
  - Post-mortem: documented timeline, update policies.
- Частые ошибки: продолжать использование «пока не найдено влияние»; игнорировать косвенные пути poisoning (скрапинг веба, зеркала датасетов).
- Красные флаги: «почистим пару записей — и всё», «нам не нужно проверять исходники данных».

### 41. Your AI mental health chatbot gave harmful advice to a user in crisis. How do you mitigate harm?
- Идеал: Immediate safety: direct to professional resources, refuse unsafe advice, crisis escalation. (Scenario.)
- Обязательные пункты:
  - Detect crisis signs (self-harm/suicide terms): escalate to human/crisis hotline, provide emergency resources (number), avoid further harmful counsel.
  - Fix model/output: block harmful-generating advice, add guardrails (input `crisis` classifier → redirect), deny do-not-give diagnoses.
  - Root cause: safety training gap — add RLHF/crisis-specific SFT, red-team crisis/selfharm prompts, evaluate harm rate.
  - Process: incident report, monitoring false negatives, notify mental-health supervisor/clinical review.
  - Prevent over-reliance: disclaimers, human-in-loop, don't promise professional care.
- Частые ошибки: только disclaimer «обратитесь к врачу» без crisis escalation; думать «модель не должна говорить о суициде» → пугать, если поменять стиль.
- Красные флаги: «chatbot может заменить психолога», «мы не сообщаем о кризисе, чтобы не тревожить» (небезопасно).

### 42. Your AI system caused incorrect critical decisions. How do you run a blameless post-mortem?
- Идеал: Focus on system/process faults, not blame; document timeline, root causes, action items. (Scenario.)
- Обязательные пункты:
  - Prepare: status page, freeze changes, gather logs/artifacts, include highlights.
  - Structure: timeline of events, facts, root cause analysis (not individual), contributory factors, detections failures.
  - Blameless: no personal fault attribution; second-order: what process/system misdesign allowed it (data, monitoring, thresholds).
  - Actionable: prioritized fixes, owner, due dates, prevent recurrence (tests, gates, alerting).
  - Follow-up: review action completion, communicate transparently to affected/users; close open loops; review of review.
- Частые ошибки: искать виновного; постмортем без действий/сроков; игнорировать ошибки мониторинга.
- Красные флаги: «виноват разработчик», «ошибка уже исправлена, можно закрывать» без действий.

### 43. Radiologists agree with AI 98% of the time, even when it is wrong. How do you prevent human over-reliance on AI?
- Идеал: Over-reliance — humans defer to AI without independent verification; calibrate trust. (Scenario.)
- Обязательные пункты:
  - Design: AI output with calibrated confidence/uncertainty (not just binary), human decision support not autopilot; require radiologist rationale.
  - Review: force independent read-before-AI, comparison/tie-break process, second opinion button.
  - Over-reliance: measure agreement vs true errors, track when humans override, train users on failure modes, simulate scenarios.
  - Examples from aviation/medical: show AI only after human's own assessment; provide alternative findings rank.
  - Feedback: monitor override rate and accuracy of override.
- Частые ошибки: думать «если человек согласен — все ок»; not counting override when humans lazy.
- Красные флаги: «AI подтверждает мое мнение, значит это правильно», «надёжность = просто показать причину» без изменения workflow.

### 44. Your content moderation flags normal cultural expressions as offensive in other markets. How do you adapt cross-culturally?
- Идеал: Cultural context matters — same text different meaning; localize moderation, not just translate. (Scenario.)
- Обязательные пункты:
  - Diagnose: classifier trained on one language/region — no cultural lexicon, slang, gestures, dialects → false positives.
  - Adapt: per-market tuning — local eval sets, gather native speaker rule sets/taxonomy per locale, calibration by region.
  - Process: human-in-loop for flagged ambiguous; region-specific policies (criminal/illegal language vs cultural idiom). Mixed mode: default strict off vs region overrides.
  - Measure: false-positive rate per market, A/B tests, feedback from moderators.
  - Technical: multilingual capability, locality label, apologize for errors, permissions.
- Частые ошибки: одинаковый порог для всех рынков; не знать, что слово «нецензурное» различается.
- Красные флаги: «переведём правила — и готово», «стандарт один — универсальный для всех культур».

### 45. Your AI training produces massive carbon emissions. How do you reduce environmental impact?
- Идеал: Reduce compute per training run, use energy-efficient infra, offset and monitor. (Scenario.)
- Обязательные пункты:
  - Optimize: use smaller models/quantized, pruning/distillation/knowledge distillation, efficient architectures, train on fewer examples, reuse pretrained.
  - Infra: Green energy datacenters (renewable, carbon-aware scheduling — run during low-carbon hours), hardware accelerators, efficient utilization/batch.
  - Measure: track carbon/KW (emission tracking tools: CodeCarbon, ML CO2 Impact), report metrics.
  - Reduce: one-time big runs vs fine-tune smaller, reuse/multi-tenant infra, cached served models.
  - Culture: make carbon a KPI, education; grow sustainable fleet.
- Частые ошибки: думать «у меня малая модель - не важно»; считать, что причина одна (обучение) — inference/всё учёт тоже.
- Красные флаги: «перейдём на GPU с меньшим потреблением — и всё», «не оцениваем эмиссии совсем».
