# LLMOps and Production AI — Answer Key (41-53)

### 41. How do you manage secrets and API keys securely in LLM applications?
- Идеал: keep every credential out of code and config, and enforce least privilege per key with rotation, so a leak never equals full access.
- Обязательные пункты:
  - Store secrets in a managed vault (AWS Secrets Manager, Vault, GCP Secret Manager) or Kubernetes Secrets / env; never in code repo, config file, or logs. Inject at runtime.
  - Per-environment, per-service keys with strictest scope: read-only API keys, separate keys for prod/dev/CI; rotate keys regularly via API/vault, and revoke immediately on suspected leak.
  - Restrict network egress if possible; monitor spend to detect leaked keys being used; avoid keys in browser-frontend code (call backend which holds keys).
- Частые ошибки: keys in `.gitignore`-ed dotenv still committed; one key shared across env; no rotation plan.
- Красные флаги: "it's fine because the repo is private"; keys committed with rotation deferred to "later."

### 42. Your LLM API has latency spikes during peak hours. How do you stabilize it?
- Идеал: smooth the load instead of letting requests pile up, keeping response time within SLO during bursts.
- Обязательные пункты:
  - Caching (prompt + semantic) to cut the number of real model calls — biggest lever for repeat traffic.
  - Queue with bounded concurrency and backpressure: a pool of workers over a queue, cap in-flight requests to the provider per its rate limits, and expose a queue-depth metric so we can scale out.
  - Autoscale (provision more instances during peak) and spread across regions; add retries with exponential backoff + jitter so a spike doesn't cause a retry-storm.
  - Observe split latencies (TTFT vs inter-token): if TTFT rises, it's batching/concurrency waiting; if inter-token rises, it's compute/network contention. Target measure; then fix root cause, e.g. deploy more replicas, warm request, tune batch size.
- Частые ошибки: adding retries without backoff/jitter — makes spikes worse.
- Красные флаги: "we send every request straight to the model, that's fine"; claiming fixed without measuring split latency.

### 43. Your LLM endpoint's p99 latency doubled after a deploy with no model change. How do you diagnose it?
- Идеал: bisect the change and isolate which hop adds the tail: preflight/guard code, prompt/template, router, batching, or infra — not a model change.
- Обязательные пункты:
  - Build a latency profile: p50 vs p99 split by route/model, TTFT vs inter-token (total latency), load vs no-load comparison.
  - Search for new bottlenecks across the trace: added validation/serialization code in the path, larger prompts from changed template, new router overhead, batching changes, concurrent worker pool shrinking, cache misses/hit-ratio drop.
  - Compare p99 to p50: if p99 rose while p50 flat → it's queueing/conviction under concurrency, backpressure, or GC/cold cache; if both rose → every request path got slower.
- Частые ошибки: blame the provider without checking your own new code first.
- Красные флаги: "we didn't touch the model so it must be the provider" without evidence; quoting overall latency instead of p99-by-step.

### 44. Your LLM costs are too high in production. How do you reduce costs without degrading quality?
- Идеал: pay for intelligence only on hard queries and skip the model for repeat ones — mix caching, routing, and cheaper models, then measure quality.
- Обязательные пункты:
  - Semantic caching: embed query → cosine similarity vs stored embeddings → hit above threshold (~0.85-0.95) returns stored answer, model never called; miss → call and store in a vector DB.
  - LLM routing: send simple queries to small cheap fast models, hard ones to frontier (cost gap ~30x: $0.50 vs $15 per 1M output tokens); cascade routing is the most cost-saving (cheap first, escalate on low confidence) but adds latency to hard queries.
  - Compression/context: keep prompt stable to maximize prefix (prompt) caching, trim tokens, shorten conversation retention; streaming alone doesn't cut cost.
- Частые ошибки: routing on length alone; adding a frontier-LLM router that costs more than it saves — router latency must stay <10% of target LLM's.
- Красные флаги: "use the cheapest model for everything reduces cost" (quality drop); "lower the semantic-cache threshold to 0.5 to get more hits" (returns wrong answers).

### 45. Your application is hitting LLM provider rate limits during peak hours. How do you handle it?
- Идеал: spread demand so you stay under the provider's rate limits without failing requests — prioritize, queue, amortize, and have a plan for when limits still trip.
- Обязательные пункты:
  - Client-side: a per-provider token/rate limiter (mirror the provider's RPM/TPM), a bounded queue, and retries with exponential backoff + jitter on 429s — never hammer retries.
  - Burden-shift: semantic + prompt caching to reduce model calls; routing to different providers or different quota buckets; streaming/scheduling non-urgent batch traffic outside peak.
  - Fail ordering: serve a cached fallback or graceful message rather than a hard error when quota is exhausted; queue timeout request or return best-effort degraded response.
- Частые ошибки: unlimited immediate retries on 429 → retry-storm eats the quota (exception quota) and amplifies outage.
- Красные флаги: "we just retry aggressively"; ignoring the rate-limit response's `Retry-After` header.

### 46. Your application depends on one LLM provider. How do you switch providers without downtime?
- Идеал: abstract the provider behind an interface so swap is a config change, not a rewrite — and you never cut over cold.
- Обязательные пункты:
  - Provider abstraction: call models through an OpenAI-compatible client or your own adapter/interface (model alias → provider endpoint), not vendor-specific SDK calls scattered through code.
  - Configuration-driven models: map task → model alias in env/config; point aliases at the new provider and roll out with canary (new provider serves small % first).
  - Dual-run + validation: run both providers in parallel (i.e. shadow traffic), compare quality/cost/latency, then shift traffic; fallback to the old provider on errors — keep old token in place until verified.
- Частые ошибки: hardcoded provider calls everywhere; cutting over all traffic at once without a shadow compare.
- Красные флаги: "we'll rewrite the integration on the day of migration"; provider-specific prompts baked into app code.

### 47. Your AI system handles 100 requests/sec but crashes at 5000. How do you scale for concurrent requests?
- Идеал: decouple the burst from the backend so all 5000 can be accepted without overloading — queue + autoscaling, not more threads per pod.
- Обязательные пункты:
  - Key insight: 100→5000 RPS is a burst/concurrency problem, not a capacity constant — you need asynchronous processing: ingress accepts immediately, pushes to a bounded queue (Kafka/SQS/Redis), workers consume at provider-safe concurrency.
  - Scale out horizontally: stateless request handlers + external queue = N replicas autoscale by queue depth/CPU; goal is matching consumer concurrency to provider rate limits and own saturation point.
  - Bounded concurrency + backpressure: cap in-flight requests per worker, retry with exp backoff+jitter, circuit-break on provider saturation; never unbounded goroutines/threads per request (they exhaust memory/connections).
  - Right-sizing under load test: measure where saturation begins (CPU, memory, connections, provider limits), set autoscale thresholds before that cliff; add load testing to find the crash point, then scale + tune.
- Частые ошибки: assuming the fix is "more threads" — that deepens memory/connection exhaustion; ignoring provider side limits.
- Красные флаги: "raise max concurrency to fix it"; scaling pods wired by requests count alone without a queue.

### 48. A traffic spike brings down your AI system. How do you handle peak traffic?
- Идеал: absorb the spike gracefully instead of crashing — absorb, shed, and let the backend work within its limits.
- Обязательные пункты:
  - Add a queue + worker pool: sustained throughput flat-lines at a safe level; ingress is decoupled so a 100x spike becomes queued work, not 100x load. Monitor queue depth.
  - Autoscaling + capacity headroom: provision replicas by expected peak (autoscale on queue depth/CPU), and pre-warm for known peaks (sales, launches).
  - Load shedding: rate limiting, throttling, per-client quotas; under extreme load, deliberately return degraded/cached responses (graceful degradation) before the system dies; overload breaker.
  - Cache bursts: protect expensive model calls behind semantic/prompt caching so repeat spike traffic is served without new model calls.
- Частые ошибки: no queue so the spike hits the backend directly; scale-up too slow (late autoscale) → saturate before replicas ready.
- Красные флаги: "just buy more servers" without a queue/rate-limiter; serving every spike request with full-cost model calls.

### 49. One LLM provider outage took down your entire system. How do you eliminate single points of failure?
- Идеал: replicate across providers so no single vendor outage is fatal, plus a fast, verified fallback path.
- Обязательные пункты:
  - Multi-provider strategy: run ≥2 providers (or same provider in different region/quota) behind a unified gateway/router; architecture abstracts the provider — the app works with whichever provider is chosen; keep task-specific aliases so models can swap.
  - Router with health-based failover: route to secondary provider on timeouts/5xx/rate-limit exhaustion; pre-verify fallback (pricing, quota, quality parity) so it actually works at cutover; cache-intensive requests so the outage window is survivable.
  - Lower blast radius: per-provider quota and concurrency budgets so one throttled provider doesn't spill load and take down the fallback; regional diversity.
- Частые ошибки: "provider B is backup" but it has no quota provisioned — same 429 under load; failover tested only in calm conditions.
- Красные флаги: "two providers so we're immune" with no automatic health-based routing; no cache/drain to survive a multi-minute wall.

### 50. Your multi-LLM pipeline fails when one model in the chain breaks. How do you handle orchestration failure?
- Идеал: make each step of the chain independently safe — timeout, retry, and fallback so one broken model degrades one step instead of failing the whole workflow.
- Обязательные пункты:
  - Per-step reliability: every step gets a timeout + retry policy (exp backoff + jitter) and a fallback (e.g. substitute model/provider or a cached/heuristic answer) — a single failure shouldn't break the whole workflow per orchestration best practice.
  - Isolate steps and bound loops: design the flow so steps are independent (parallel/branch pattern) and loops have a max-iteration budget/stop-condition so a bad model output can't loop forever and burn money.
  - Graceful error handling: on failure return a partial/best-effort result and signal it, or route to a human/fallback path — never a hard 500 on a mid-chain step; log the failing step (input/output/error) for diagnosis.
  - Test each step in isolation before the whole chain; add guardrails at boundaries (validate step output before feeding next).
- Частые ошибки: a sequential chain with no retries → one model hiccup kills the request; unbounded loops (no max tries) burning tokens.
- Красные флаги: "the pipeline is fine, it's just one provider" — a chain without per-step timeouts/retries is the SPOF; infinite retry loops.

### 51. Your AI pipeline has zero visibility into which step is failing. How do you add observability?
- Идеал: a full step-by-step record (logs + metrics + traces) so any failure can be pinpointed to the exact span, its input, output, and duration — no guessing.
- Обязательные пункты:
  - Add tracing: one trace per request made of spans (one span per step: LLM call, tool call, retrieval); spans are nested (planning span → inner LLM-call span) and each records input, output, duration, error — the "black box flight recorder" for the agent.
  - Three pillars: structured logs, metrics (per-step latency, errors, token cost), and traces; attach them to run_id/request_id so a failing step is identifiable; log at every step.
  - Instrument step boundaries & failures: explicit traces/spans in the orchestration graph (each node = one clean span), capture errors + token/cost per call, add guardrails + eval to catch silent failures (answers that look right but are wrong).
- Частые ошибки: only trailing HTTP status codes; no correlation id across steps so you can't tie a failure back to one span.
- Красные флаги: "logs alone are enough" for a multi-step agent; hiding intermediate steps / errors so silent failures go undetected.

### 52. You quantized your LLM, but accuracy dropped significantly. How do you minimize quantization loss?
- Идеал: preserve accuracy by quantizing smarter: local, per-channel scales; protecting outlier/salient weights; keeping activations high precision; prefer QAT over PTQ for low bits.
- Обязательные пункты:
  - Per-channel quantization — separate scale per row, not one per tensor; asymmetric quantization hugs the true range and uses every integer value; weight-only quant keeps activations in FP16 — the common, safer choice for LLMs.
  - Keep critical weights at higher precision: AWQ protects "salient" weights tied to large activations; bitsandbytes keeps outliers high-precision; GPTQ compensates rounding error layer-by-layer; consider retaining embedding/LM-head or output layers un-quantized.
- Частые ошибки: naive per-tensor symmetric INT4/2-bit on all weights, losing outlier detail.
- Красные флаги: claiming "INT8 is accurate but INT4 damages quality" as a rule — smart methods like GPTQ/AWQ keep 4-bit low-loss; "post-training quantization is better than QAT anytime" — QAT wins at low bits.

### 53. One failing AI component can take down your entire platform. How do you design graceful degradation?
- Идеал: degrade gracefully — when something fails, return a useful partial result, not a whole-platform failure; every component has a survival mode.
- Обязательные пункты:
  - Boundaries and isolation: per-component circuit breakers, timeouts, and quotas so one component's failure doesn't cascade; a failing model returns a cached fallback / lower-quality answer instead of propagating an error.
  - Progressive quality tiers: best answer → cached/summarized answer → static answer → graceful message; define these before the failure, not during; mark the result as degraded (quality/diagnostics flag).
  - Redundancy: run ≥2 replicas/providers in active-active with health routing; test degradation paths; priority-based shedding: protect core functions, shed or defer non-essential work first.
- Частые ошибки: infrastructure down = everything hard-fails with no fallback.
- Красные флаги: "we have no degraded mode because everything is critical" — everything critical means nothing has a known failure path; returning hard errors instead of degraded responses.
