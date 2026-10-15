# AI System Design — Answer Key (26-49)

### 26. Design an AI-powered legal document review system.
- Идеал: ingest contracts/pleadings, extract and classify key clauses, flag anomalies and risks, summarize, and produce tracked redlines a lawyer reviews and approves — human-in-the-loop, never autonomous decisions.
- Обязательные пункты:
  - Ingestion: PDF/docx parsing, OCR for scanned docs, normalize to text; chunk at contract-section granularity, not sentences.
  - Extraction: hybrid retrieval (BM25 + vector) over clause libraries; LLM with structured JSON output (clause type, text span, parties, dates, obligations) — never free text.
  - Risk rules: deterministic rule-based checks over extracted fields (missing termination, out-of-range dates) so findings are reproducible and auditable.
  - Review workflow: provenance doc-to-chunk-to-fact-to-suggestion; lawyer previews and commits; per-client ACLs, encryption, full audit trail.
- Частые ошибки: whole long PDF into context; no structured output; no human approval gate.
- Красные флаги: "model decides/rejects contract"; no audit trail.

### 27. Conversational AI with memory across sessions.
- Идеал: LLM is stateless; memory is built around it. A four-layer stack: context window (in-prompt, lost on overflow), short-term (session scratchpad, plan/step state), long-term (persistent user facts/preferences/summaries), external knowledge (RAG/tools). Four core ops: Write, Read, Update, Forget.
- Обязательные пункты:
  - Runtime flow per turn: read relevant long-term + short-term -> build prompt (system + retrieved memories + user msg) -> LLM loop with tools -> write new memories -> respond.
  - Store what matters next week; skip chit-chat; handle retrieval misses (semantic/embedding + ANN), outdated facts (update on contradiction), memory bloat (forget policy).
  - Long-term writes often async after response; scope memory to user_id, encrypt, consent.
- Частые ошибки: storing everything; confusing short/long-term layers; no forget policy.
- Красные флаги: "LLM сам помнит" (it is stateless); no isolation between users.

### 28. Latency vs quality trade-offs in AI systems.
- Идеал: balance response speed against correctness per request, not globally; query routing decides.
- Обязательные пункты:
  - Tiering: small/fast model for simple requests, large/slow for hard ones; router with evals.
  - Techniques: prompt/semantic caching, streaming, speculative decoding, small-model-first + verify, parallel vs sequential search.
  - Define SLO (p95 latency) and minimum quality; measure both; tune on real data.
  - Quality-critical (medical/legal) favors quality; interactive UX favors latency; caching gets both.
- Частые ошибки: one model for all; measuring latency but not correctness.
- Красные флаги: "small model всегда хуже"; claims quality without evaluation.

### 29. Caching strategies for LLM applications.
- Идеал: two complementary caches. Prompt caching reuses the model's internal KV cache for a repeated prompt prefix; semantic caching returns a saved final answer when a new question matches by meaning.
- Обязательные пункты:
  - Prompt caching: stable part first (system instructions, big docs, tool defs, few-shot), changing part last; exact-prefix match char-for-char; TTL ~5 min; write ~1.25x, read ~0.1x cost; best in RAG/agents. A changing token (date/ID) at top breaks the cache.
  - Semantic caching: embed question -> cosine similarity vs cached embeddings -> score >= threshold returns saved answer without calling model; miss -> call, store Q+embedding+answer in vector DB (ANN).
  - Threshold: too high = no hits, too low = wrong answers; ~0.85-0.95; test with real queries; suits stable answers (not weather).
- Частые ошибки: confusing the two (semantic reuses answer, prompt reuses internal computation); "cache changes quality" (no).
- Красные флаги: exact-match caching only; no threshold tuning.

### 30. Rate limiting and cost management for AI APIs.
- Идеал: control usage per tenant/user and bound spend while keeping good UX. Token-aware, layered.
- Обязательные пункты:
  - Rate limiting: token bucket / sliding window per user, key, IP; token-based (prompt+completion), not just call count; queue + retry/backoff on 429.
  - Cost: per-tenant budgets/caps, alerts; model tiering and routing; caching, batching; log per-request cost.
  - Prioritize premium/critical quota; degrade non-critical gracefully.
- Частые ошибки: count-only limits; no spend alerting.
- Красные флаги: "безлимит" for all; ignoring token variance.

### 31. Failover and fallback strategies for AI systems.
- Идеал: keep features running when a model/provider fails by degrading along a planned chain, with circuit breakers isolating the outage.
- Обязательные пункты:
  - Fallback ladder: primary large -> alternate provider -> small/local fast model -> cached/heuristic -> explicit decline. Never silently wrong; say "degraded mode".
  - Circuit breaker (open/half-open/cooldown), timeouts + retries with jitter, bulkhead per provider.
  - Health checks, automatic failover, idempotency; log which tier served each request.
- Частые ошибки: infinite retries on a dead provider; silent degradation; no breaker -> cascading load.
- Красные флаги: "fallback = always same answer"; retry without backoff.

### 32. High availability and fault tolerance.
- Идеал: system stays within SLO (>99.9%) despite node/model/provider failures via redundancy, isolation, rerouting.
- Обязательные пункты:
  - Redundancy: stateless serving behind LB, multi-AZ replicas; model replicas over multiple GPUs/engines.
  - Fault isolation: circuit breakers, bulkheads per provider/model/tenant; queue with retries so bursts don't cascade.
  - State: replicated DB (WAL/RDB), durable queue for async jobs; avoid single orchestrator/cache SPOFs.
  - Ops: health checks, autoscaling, runbooks, chaos testing; graceful degradation under partial capacity.
- Частые ошибки: single model dependency without breaker; stateless web but single shared memory state.
- Красные флаги: "HA = just add replicas" without isolation; ignoring stateful components.

### 33. Graceful degradation when the model is unavailable.
- Идеал: keep the product usable and honest as capability drops stepwise instead of hard-failing.
- Обязательные пункты:
  - Tier plan: full LLM -> smaller/fast model -> cached/semantic answers -> retrieval-only summaries -> rule-based/canned -> clear error/fallback UI.
  - Communicate limits: "I can't reason right now, here's a canned answer" rather than a plausible wrong one; surface degraded mode in UI/telemetry.
  - Preserve critical value (e.g. search works even if chatbot is down).
- Частые ошибки: confident wrong answer from stale tier; no signal quality degraded.
- Красные флаги: "always return an answer" at any cost; hiding degradation.

### 34. Multi-region deployment of AI systems.
- Идеал: serve users close to their region for latency and comply with data-residency rules, with active/active or active/passive topology.
- Обязательные пункты:
  - Latency: place model/inference replicas and edge gateways per region; global load balancing for region failover.
  - Data residency/privacy (GDPR, localization): user data and model inputs stay in-region; per-region storage isolation.
  - State: geo-replicated DBs with a chosen consistency model (or region-local state); idempotent APIs for cross-region retries; event streaming.
  - Failover: traffic management, per-region config/model version control, staggered rollouts; GPU fleet cost per region.
- Частые ошибки: one model serving all regions (latency, legal); ignoring per-region version divergence.
- Красные флаги: "one region, migrate later" as the plan; sharing user PII across borders.

### 35. AI-powered e-commerce search engine.
- Идеал: understand intent + semantics, not just keyword match, and rank products personalized to the shopper.
- Обязательные пункты:
  - Query understanding: spell-correct, synonym/rewrite, embedding retrieval (query<->product embeddings), hybrid with BM25 for tail keywords; combine via learning-to-rank.
  - Ranking: candidates (vector + keyword) -> rerank with cross-encoder/GBDT/LLM using clicks, price, availability, cohort; facets and filters.
  - Personalization: user context/embedding, history, A/B test; freshness/stock signals matter.
  - Infra: offline indexing + embedding pipeline; online low-latency ANN; rerank on small pool; monitor CTR/search quality.
- Частые ошибки: vectors alone (miss exact SKUs); no personalization; ignoring price/stock in ranking.
- Красные флаги: "просто векторный поиск"; no ranking feedback loop.

### 36. AI gateway/proxy for managing LLM access across an org.
- Идеал: a single control plane in front of all LLM providers/models so teams share one safe, observable, governed access point.
- Обязательные пункты:
  - Unified API + routing: OpenAI-compatible surface; route per model/provider/policy (cost tier); load balance and failover.
  - Governance: authN/authZ per team/app, rate limits, spend budgets, PII/redaction inspection, content/topic policy, prompt auditing.
  - Observability: logs, traces, token/cost metering, latency dashboards, evaluation per route.
  - Central caching + retries/backoff; share cached prompts/answers.
- Частые ошибки: teams calling providers directly (no governance); per-team keys with no budget.
- Красные флаги: gateway without rate limits (cost blowups); no logging (audit/compliance).

### 37. RAG handling conflicting information across sources.
- Идеал: surface and resolve contradictions explicitly rather than silently blending, so users trust and understand the answer.
- Обязательные пункты:
  - Detect conflicts: retrieve passages with metadata (source, timestamp, authority); compare claims/entailment (LLM or embedding) and flag contradictions.
  - Resolve priority: provenance rules (official > unofficial, newer > older); cite sources; if unresolvable, say "sources disagree".
  - Present: list both sides with citations; honestly note uncertainty; don't average.
- Частые ошибки: silently merging either answer; no citations.
- Красные флаги: "RAG always resolves"; hiding source disagreement to look confident.

### 38. Approach to capacity planning for an AI system.
- Идеал: estimate demand, convert to compute/storage needs in advance, and build slack + scaling headroom; then monitor and adjust.
- Обязательные пункты:
  - Estimate: peak RPS, tokens per request, concurrency (Little's Law), GPU-hours from model size + throughput; factor burst (3x typical).
  - Plan: baseline + autoscaling headroom (~50-100% buffer), burstable instances; reserve GPU fleet; cost projection.
  - Include: KV cache growth, quantization, batching, cold start, model replica sizing.
  - Method: measure actual usage, right-size, iterate; re-plan on new features.
- Частые ошибки: sizing for average not peak; ignoring token-length variance.
- Красные флаги: "just add autoscaling" with no estimate; no GPU model.

### 39. Multi-tenant AI chatbot platform (each business a custom bot).
- Идеал: many businesses share one platform; each tenants its own knowledge base, branding, and config, isolated and secure.
- Обязательные пункты:
  - Per-tenant: isolated vector index / DB partition, its own instructions/config, custom branding; tenant-scoped retrieval (never cross-tenant data).
  - Multi-tenancy: shared model + routing with per-tenant quota/rate-limit and spend; tenant_id in every request/embedding query.
  - Security: encryption; prompt-injection defense via tenant data isolation; audit and tenant control.
  - Ops: hot deploy of tenant config, per-tenant metrics, scaling shared services.
- Частые ошибки: cross-tenant data leakage in retrieval; one tenant starving another's quota.
- Красные флаги: "shared vector index" for all tenants; no tenant scoping.

### 40. AI meeting summarizer for thousands of meetings daily.
- Идеал: ingest audio (video/captions), transcribe, then generate structured summaries + action items at scale, reliably and privately.
- Обязательные пункты:
  - Pipeline: ingestion -> ASR/transcription -> diarization (who said what) -> LLM summarization (chunk then merge; map-reduce for long meetings) -> structured output (summary, decisions, action items, owners).
  - Scale: async job queue + workers, chunk-and-parallelize long audio; autoscale on concurrency; retries/idempotency.
  - Privacy: recordings/transcripts encrypted, access-controlled, retention policy; redact sensitive data.
  - Quality: eval against ground-truth summaries; handle crosstalk, accents, crosstalk grammar.
- Частые ошибки: one giant transcript into context; no diarization; leaking minutes.
- Красные флаги: "single full-transcript call" at scale; no retention.

### 41. AI notification system that prioritizes instead of broadcasting.
- Идеал: rank notifications by urgency and user relevance so only important ones reach the user, instead of spamming everything.
- Обязательные пункты:
  - Ranker: score each notification (urgency, channel, user preference, time-sensitivity, dedupe) — ML/LLM + rules + priority tiers; quiet-hours/categories.
  - Policy: budget per user (e.g. max/day), channel selection (push/email/SMS), dedupe/rollup, delivery batching.
  - Feedback: engagement data to tune; respect opt-outs/muting.
  - Infra: queue, prioritization, delivery service with backoff; latency for urgent (security) vs routine.
- Частые ошибки: broadcasting everything; ignoring quiet hours; no dedupe/rollup.
- Красные флаги: notification purely chronological; no user control.

### 42. AI-powered anomaly detection for cloud infrastructure.
- Идеал: continuously detect unusual patterns in time-series (and logs), alert on real anomalies (not noise), and provide actionable root-cause hints.
- Обязательные пункты:
  - Data: metrics (CPU/memory/network/error-rate) + logs/traces; feature pipeline; correlation.
  - Models: statistical forecasting + residual anomaly (or ML: isolation forest, autoencoder, LLM over summaries); thresholds per metric; ensemble to reduce false positives.
  - Platform: streaming metrics -> detection service -> alert manager; historical baseline; per-service context.
  - Feedback: label anomalies; tune; dedupe alerts; incident correlation.
- Частые ошибки: static thresholds on dynamic baseline, too many false positives, alert fatigue.
- Красные флаги: "single threshold for all"; anomaly = just threshold crossing, no model.

### 43. AI document processing pipeline for financial institutions.
- Идеал: extract structured data from financial documents (invoices, statements, KYC forms) with high accuracy and compliance.
- Обязательные пункты:
  - Stages: ingestion (PDF/TIFF/JPEG; OCR for scans) -> classification (doc type) -> field extraction (LLM + OCR + template) -> validation (business rules) -> export with confidence + human review.
  - Accuracy: low-confidence review queue; audit trail; versioning; encryption at rest/in transit; compliance (retention, consent).
  - Scale: queue + workers; parallel parsing; handle poor scans and ambiguity.
- Частые ошибки: assuming clean digital PDFs; no confidence thresholds.
- Красные флаги: "automatic 99.9%" without human review loop.

### 44. AI dynamic pricing engine.
- Идеал: set prices in real time to maximize revenue/utility given demand, competition, inventory, and constraints, while avoiding bad UX and regulatory issues.
- Обязательные пункты:
  - Inputs: demand forecasts, competitor prices, inventory/supply, elasticity, seasonality, user segment; constraints (floor/ceiling, price change limits).
  - Model: supervised/RL pricing policy (or rule + ML blend); bandit/A/B for learning; offline training + online scoring.
  - Guardrails: price bounds, customer trust (no sudden absurd jumps), anti-collusion/anti-abuse, dashboards.
  - Infra: feature serving, low-latency decision API, monitoring tradeoffs (elasticity).
- Частые ошибки: unbounded price swings; ignoring elasticity; no guardrail = user backlash.
- Красные флаги: "always raise price to max"; no fairness constraint (collusion).

### 45. AI resume screening system handling 100K applications/week.
- Идеал: rank and filter resumes at massive scale fairly and efficiently, surfacing top candidates for recruiters (human decision).
- Обязательные пункты:
  - Pipeline: ingestion (PDF/DOCX parsing, OCR) -> normalization -> embedding -> retrieval/ranking (semantic + keyword; match job req vector) -> LLM extract skills/score -> rubric score -> ranked list with explanations.
  - Scalability: batch/async jobs, queue + workers, caching resume embeddings (embed once per resume); idempotent; cost control (embedding cheap, LLM only for top-N).
  - Fairness: guard against bias on gender/race/age, blinded review, audit, transparency; compliance (GDPR/hiring laws).
  - Feedback: recruiter decisions to improve ranking.
- Частые ошибки: LLM-scoring every resume (cost); no bias mitigation.
- Красные флаги: "AI hires the candidate"; uses protected attributes.

### 46. AI voice assistant architecture.
- Идеал: real-time conversational voice loop — listen, understand, act, reply — within human-like latency; target voice-to-voice latency ~800 ms max 1.5 s, availability 99.9%.
- Обязательные пункты:
  - Pipeline: audio transport (WebRTC/WebSocket), VAD + turn detection (no "Enter" key), streaming STT, LLM brain with tools + memory, TTS back to user; stream chunks (~20 ms), not request-response.
  - Interruptions (barge-in): playback-progress + clear-audio-buffer messages; agent detects user speech and stops TTS.
  - Approaches: cascaded STT->LLM->TTS vs end-to-end speech-to-speech vs hybrid; cascaded more controllable/cheaper, end-to-end lower latency/natural.
  - Scale: one orchestrator session per call; GPU fleet for STT/LLM/TTS; back-of-envelope: ~10k concurrent calls, codec (Opus ~32 kbps); storage ~1.2 TB/day for recorded calls.
  - Edge cases: background noise, accents, misheard numbers/codes, echo, phone vs app; observability per-call tracing; privacy (voice = personal data, recordings protected).
- Частые ошибки: text-chat latency assumptions; no interruption handling; no echo cancellation.
- Красные флаги: "it's a chatbot with a mic"; ignoring streaming/latency budget.

### 47. Multi-agent workflow system where agents collaborate on complex tasks.
- Идеал: 2+ LLM agents with distinct roles (orchestrator, worker, router, planner, critic, tool specialist) collaborating on a shared task via a coordination layer.
- Обязательные пункты:
  - Three pillars: specialization (focused prompts/tools), communication (messages/shared blackboard/handoffs), coordination (who runs when).
  - Coordination patterns: sequential, parallel (independent subtasks), router, hierarchical (orchestrator->workers), graph (any-to-any); start simple, add agents only when needed.
  - Structured communication: JSON task/messages, not free chat; validate intermediate outputs; cap turns; critic/reviewer with independent grounding; lower temperature for deterministic routing.
  - Tradeoffs: complexity, latency, token cost vs quality on complex tasks; prefer hybrid (single primary + helper) unless workload needs full multi-agent.
- Частые ошибки: agents that talk without progress; unclear ownership (duplicate/missed work); error propagation; critic loop never converging.
- Красные флаги: "more agents = better"; applying multi-agent to tightly-coupled tasks (e.g. coding).

### 48. Real-time AI transcription system for concurrent audio streams.
- Идеал: transcribe many live streams simultaneously, emitting partial (interim) and final segments with low latency and speaker attribution.
- Обязательные пункты:
  - Pipeline: ingest streams -> audio preprocess (noise/VAD) -> streaming ASR (WebSocket, partial results) -> diarization -> punctuation/casing -> publish transcript events.
  - Scale: shard by stream; GPU/ASR workers with autoscaling; queue + backpressure; per-stream session state; horizontal scale on concurrent streams.
  - Latency: partial results as audio arrives; finalize on silence; map semantics per stream.
  - Reliability: reconnect/resume, out-of-order handling, idempotency; monitoring WER and latency.
- Частые ошибки: sessionless workers (lost state); no interim results; single model per stream hard-limit.
- Красные флаги: "offline batch" for a real-time system; ignoring speaker identity.

### 49. AI-powered live streaming content moderation system.
- Идеал: moderate live video/chat/audio in near real time with AI first-pass, human reviewers for borderline cases, protecting viewers and platform.
- Обязательные пункты:
  - Layers: real-time detection (chat/text, image/video frames, audio/speech) with multimodal classifiers for policy classes (hate, violence, nudity, fraud).
  - Pipeline: streaming ingest -> frame/sample + classifier (fast model) -> risky -> queue for human review; block/flag/quarantine actions with configurable thresholds.
  - Scale: async queue + workers, GPU for vision/audio, rules for deterministic cases; webhook alerts.
  - Accuracy: precision/recall tradeoff, low-latency first pass, human escalation, appeals; privacy (moderation → data retention/access).
  - Compliance: audit, fairness, less false positives for legitimate streaming.
- Частые ошибки: threshold too aggressive (over-flag) or too loose; no human layer.
- Красные флаги: "fully automated moderation" with no appeals; only text, ignoring video/audio.
