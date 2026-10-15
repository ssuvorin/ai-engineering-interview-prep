# AI System Design — Answer Key (1-25)

### 1. Design a Real-Time Voice AI Agent
- Идеал: streaming cascaded pipeline (STT → LLM+tools → TTS) per call, run by an orchestrator; the key metric is voice-to-voice latency — reply must start within ~800 ms after the user stops (cap ~1.5 s). Voice is harder than chat: no "Enter", noisy audio, interrupts.
- Обязательные пункты:
  - Transport: phone via SIP/RTP (telephony); app/browser via WebRTC (UDP, jitter buffer, packet-loss concealment, AEC, noise suppression); audio as 20 ms chunks; codecs Opus ~32 kbps / G.711.
  - Components: media gateway (codecs, echo cancellation) → orchestrator (one session per call) → streaming STT → LLM with tools → streaming TTS.
  - No Enter: VAD + turn detection decide the end of speech; interruption (barge-in) via playback_progress + clear_audio_buffer messages.
  - Scale ~10k concurrent calls → GPU fleet; cost dominated by GPUs (STT/LLM/TTS).
  - Approaches: cascaded (controllable, more latency) vs end-to-end speech-to-speech (lower latency, less control) vs hybrid.
- Частые ошибки: treat as a text chatbot; ignore turn detection and interruption; accept multi-second replies.
- Красные флаги: «задержка не важна», «один запрос ждёт весь звонок», «модель сама определит конец речи без VAD».

### 2. Design ChatGPT: Training to Serving (End to End)
- Идеал: two halves — training (data → pretrain → align → evaluate → frozen model) and serving (gateway → GPU inference farm → streamed replies) with the model inside an optimized serving engine.
- Обязательные пункты:
  - Training: web-scale data collection/cleaning/dedup → pretraining (next-token prediction on GPU cluster) → SFT on human demonstrations → RLHF (reward model + PPO) → eval gates per stage.
  - Serving: API gateway (auth, rate limit) → router/pool → inference engine on GPUs (KV cache, PagedAttention, continuous batching) → SSE streaming.
  - Repeated system prompt → prompt caching; shared prefixes across users.
  - Observability: TTFT/TPOT, tokens, cost; guardrails on input/output.
  - Bottlenecks: prefill compute-bound, decode memory-bound, KV cache limits concurrency.
- Частые ошибки: forget the training side; name only endpoints; ignore cost/batching.
- Красные флаги: «serve на CPU», «без батчинга потянет 10M users», «кэш не поможет».

### 3. Design a RAG System (Chat with Your Documents)
- Идеал: ground the LLM in the user's documents via retrieve → prompt → generate, citing sources; reduces hallucination without retraining.
- Обязательные пункты:
  - Components: ingest (parse → chunk → embed → vector DB); retrieval (embed query → ANN top-k → rerank); generation (chunks + question → LLM → cited answer); eval (RAGAS: context precision/recall, faithfulness, answer relevance).
  - Data flow: query → embed → vector search → rerank → build prompt → LLM → answer.
  - Bottlenecks: chunk quality, embedding/retriever mismatch, context-window limit, latency of embedding + LLM.
  - Tradeoffs: dense vs hybrid (BM25+semantic); reranker cost vs precision; ANN speed vs exactness.
- Частые ошибки: no citations; treat RAG as fine-tuning (weights unchanged); huge chunks; no eval.
- Красные флаги: «ретривер не нужен», «просто впихнули документы в промпт», «RAG дообучает модель».

### 4. Design an Enterprise RAG Assistant over 10M Documents with Per-User Permissions
- Идеал: authorization enforced at retrieval time — every chunk is filtered by the caller's identity/ACL (a metadata predicate) before it reaches the LLM; output filtering is a fallback, not the primary control.
- Обязательные пункты:
  - Ingest with ACL metadata (owner, groups, roles, classification) attached to every chunk; permission filters pushed into the vector DB query (embedding + ACL predicate).
  - Two-tier check: filter at search, re-verify at rerank/answer stage.
  - Tenant isolation, encryption, audit logging of each retrieval.
  - Scale: 10M docs → shard by tenant, partitioned ANN indexes, ACL denormalized into chunks.
  - Tradeoff: filter-before-search (secure, may miss hidden docs) vs filter-after-search (higher recall, leak risk) — prefer before with index-level ACL.
  - Caching scoped per user/permission; never a shared global answer cache.
- Частые ошибки: filter after generation; shared cross-tenant index; cached answers bypass ACLs; snippet leaks.
- Красные флаги: «ставить фильтр поверх ответа LLM», «один общий индекс на всех», «права проверять в UI».

### 5. Design Memory for a Personal AI Assistant
- Идеал: a layered memory system around a stateless LLM so it appears to remember across turns, sessions, users — the agent remembers, not the model.
- Обязательные пункты:
  - Stack: context window (in-prompt), short-term (session scratchpad: plan, steps, results), long-term (persistent facts, preferences, summaries), external knowledge (tools/RAG — queried, not maintained).
  - Core ops: Write, Read, Update, Forget.
  - Runtime: read relevant memories → build prompt (system + retrieved + user) → LLM loop with tools → write (long-term async).
  - Store what matters next week (stable facts, preferences, outcomes); skip chit-chat and transient state.
- Частые ошибки: context overflow; retrieval misses; stale memories (update, don't append); bloat (forget); privacy leaks (scope to user ID); confusing layers.
- Красные флаги: «LLM сам запоминает», «храним каждое сообщение», «RAG = память агента».

### 6. Design a Deep Research Agent
- Идеал: agentic multi-step research — decompose the question, iterate search + read + extract over sources, then synthesize a grounded report with citations.
- Обязательные пункты:
  - Components: planner, search tool (web/DB APIs), page fetcher, extractor, synthesizer, verification pass.
  - Data flow: task → sub-questions → parallel searches → fetch/read → extract evidence → follow-up searches → synthesis → fact-check/citations → structured report.
  - Bottlenecks: search rate limits and cost, page fetch time, context window, runtime, source freshness.
  - Tradeoffs: breadth vs depth; grounding vs hallucination (must retrieve and cite, not rely on model memory); human-in-the-loop checkpoints.
- Частые ошибки: not citing, answering from parametric memory, endless search without stop criteria.
- Красные флаги: «исследование = один запрос к LLM», «выдумал источник и не проверил».

### 7. Design a Multi-Agent Customer Support System
- Идеал: multi-agent = specialized agents + communication + coordination; use orchestrator → researcher → writer → critic loop with small focused prompts and structured messages.
- Обязательные пункты:
  - Roles: Orchestrator (splits/delegates/merges); Researcher (order, policy, customer history); Writer (drafts reply); Critic (tone/accuracy/policy with independent grounding) → revision loop until approval (capped rounds).
  - Communication: structured JSON messages, shared state/blackboard, or handoffs (message + control transfer); never unstructured free chat.
  - Coordination: sequential, parallel, router, hierarchical, graph; support flow is sequential.
  - Data flow: email → orchestrator → researcher notes → writer draft → critic verdict → final reply.
  - Tradeoffs: multi-agent helps complex multi-skill tasks but costs tokens/latency/debugging; start single-agent, add agents only when needed.
- Частые ошибки: over-chat, unclear ownership, error propagation, non-converging critic loop, hidden complexity.
- Красные флаги: «больше агентов = всегда лучше», «агенты общаются свободным текстом», «нет проверки промежуточных результатов».

### 8. Design an On-Device AI Assistant
- Идеал: hybrid — a small quantized model runs on the device for fast/private/offline work; the big cloud model is called only for genuinely hard tasks.
- Обязательные пункты:
  - On-device wins: no network round trip (near-zero latency), privacy (data never leaves device), works offline, flat marginal cost after shipping.
  - On-device limits: small model (few B params), battery/heat, old vs new devices, slow updates (app downloads).
  - llama.cpp: quantization (Q4_K_M — 4-bit weights + K-quant super-block scale factors, ~70% smaller); GGUF single file (weights + arch + tokenizer); mmap for instant startup; SIMD kernels (AVX/NEON); gpu-layers to offload layers to GPU.
  - Cloud: bigger model, instant updates, but round-trip latency and data leaving device.
  - Routing: small local model for simple queries; cloud for hard ones.
- Частые ошибки: force everything on-device; expect huge model on phone; ignore model update strategy.
- Красные флаги: «квантование бесплатно и без потерь», «CPU так же быстр, как GPU», «приватность vs скорость не связаны».

### 9. Design a Multimodal Search System (Text, Image, Video)
- Идеал: one shared embedding space for text/image/video via a CLIP-like model, with retrieval + optional reranking behind a unified query API.
- Обязательные пункты:
  - Index: text via text encoder; images via vision encoder; videos via sampled frames + audio transcript + metadata.
  - Query: text → embed → nearest-neighbor in shared vector space; add metadata filters (date, author, format).
  - Components: ingestion workers (frame extraction, captioning/transcription), vector DB with ANN, optional cross-modal reranker (ColBERT-style late interaction).
  - Bottlenecks: video indexing cost (frame sampling), embedding compute at ingest, ANN recall, rerank latency.
  - Tradeoffs: dense-only vs hybrid retrieval; precomputed video embeddings vs on-the-fly; generic CLIP vs domain-finetuned.
- Частые ошибки: separate indexes per modality; no cross-modal calibration; ignore video audio/transcript.
- Красные флаги: «видео ищем только по тегам», «эмбеддинги строим один раз и навсегда».

### 10. Design an LLM Inference Platform (vLLM-as-a-Service)
- Идеал: multi-tenant serving platform where many requests share GPU nodes via a throughput-optimized engine; the real bottleneck is KV-cache memory, not math speed.
- Обязательные пункты:
  - Components: API gateway (auth, rate limit, billing) → scheduler → GPU nodes running vLLM → monitoring → OpenAI-compatible API.
  - Internals: prefill (compute-bound) then decode (memory-bound); KV cache grows per token and is the bottleneck.
  - vLLM: PagedAttention — KV cache in fixed-size blocks, allocated on demand, shared across requests (identical prefixes, beam search); continuous batching — swap finished requests for new ones at every step.
  - Naive serving wastes memory (over-reservation + fragmentation) → few users/GPU; vLLM fixes → more users, better GPU utilization, lower cost per request.
  - Optimization toolkit: FlashAttention, GQA/MQA, quantization, KV-cache compression, speculative decoding (Medusa/EAGLE/n-gram), prompt caching, prefill-decode disaggregation.
- Частые ошибки: think bottleneck is math speed (wrong — it's KV-cache memory); omit continuous batching; no OpenAI-compatible surface.
- Красные флаги: «vLLM меняет качество ответов», «одна непрерывная память на запрос — это нормально».

### 11. Design an LLM Evaluation Platform
- Идеал: continuously measure quality across automatic metrics, benchmarks, human eval, and LLM-as-a-judge, aligned to the actual task (not just public leaderboards).
- Обязательные пункты:
  - Automatic metrics: BLEU/ROUGE (surface n-gram match), BERTScore (semantic), METEOR, perplexity, exact match — fast/cheap but shallow, weak for open-ended tasks.
  - Benchmarks: MMLU (knowledge), HumanEval/SWE-bench (code), GSM8K/MATH (math), IFEval (instruction following), TruthfulQA; pitfalls: saturation and data contamination.
  - Human eval: Likert scale, pairwise comparison (LMArena/Elo), error annotation — gold standard, slow/costly.
  - LLM-as-a-judge: strong LLM scores output — scalable, but bias (position, verbosity, self-preference); must validate judge vs humans.
  - Task-specific: RAGAS (context precision/recall, faithfulness, answer relevance); agent evals (right tool, args, steps, τ-bench); code run against tests; safety/red-teaming (HarmBench, prompt injection).
  - Platform: eval set store → runner (offline batch + prod sampling) → judge → dashboards; track over time and on every prompt/model change.
  - Best practices: custom eval set, combine methods, validate judge, track drift, humans in the loop, measure cost/latency too.
- Частые ошибки: rely only on benchmarks; never validate the judge; no production drift monitoring.
- Красные флаги: «BLEU отлично для чата», «высокий MMLU = хороший продукт», «оценивать можно только людьми».

### 12. Design a Text-to-Image Generation Service
- Идеал: async GPU pipeline — prompt → queue → diffusion worker → decode → safety/quality checks → object store + CDN, clients poll job status.
- Обязательные пункты:
  - Components: API gateway → job queue → GPU workers running a latent-diffusion model → VAE decode → upscaling → NSFW/content filter → object store + CDN → per-user history/gallery.
  - Data flow: prompt → enqueue → worker runs denoising loop (many steps at chosen resolution) → images → CDN URL returned on completion.
  - Bottlenecks: GPU compute per image (denoising steps × resolution), queue wait, upscaling, storage growth.
  - Tradeoffs: steps/resolution vs quality; seed/CFG for consistency vs diversity; in-house model vs commercial API (cost/compliance); style consistency via same base model + LoRA.
  - Observability: generation cost, queue depth, per-user rate limits, content safety.
- Частые ошибки: ignore safety filter; sync generation (blocks users); no queue priorities.
- Красные флаги: «модель рисует по тексту без GPU», «стоимость не растёт с разрешением».

### 13. Design a Music Generation Service (Suno-like)
- Идеал: audio-generation service that composes full songs from text prompts/lyrics, working on latent audio tokens.
- Обязательные пункты:
  - Components: API → job queue → GPU workers with an audio tokenizer (e.g. VQ-VAE/EnCodec) + autoregressive/diffusion music model → audio decoder → mastering → storage/CDN → per-user library.
  - Data flow: prompt + lyrics + style tags → enqueue → model generates latent audio seq → decode to waveform → serve streaming/MP3/MP4.
  - Bottlenecks: long generations (minutes), large GPU memory (KV cache over audio tokens), licensing/copyright risk, moderation.
  - Tradeoffs: latent-token autoregressive vs diffusion over raw audio; short loops vs full-length songs; quality vs generation time and cost.
  - Observability: queue depth, GPU cost per track, misuse detection (lyrics/prompts), copyright/voice-clone guardrails.
- Частые ошибки: streaming before track done; skip moderation; ignore commercial-use licensing.
- Красные флаги: «генерируем за миллисекунды», «нет проверки копирайта».

### 14. Design a Video Generation Service (Sora-like)
- Идеал: text- or image-prompted video diffusion service (spatiotemporal generation) with heavy GPU job pipeline and strict safety (deepfakes).
- Обязательные пункты:
  - Components: API → job queue → GPU workers running video-diffusion (latent video model) → VAE decode → upscale/interpolate → cuts/loops → storage/CDN → per-user library.
  - Data flow: prompt (+ optional first/last frame) → enqueue → generate frame latents → decode frames → assemble mp4.
  - Bottlenecks: very high GPU (minutes per short clip), memory, temporal consistency, long-job orchestration, cost.
  - Tradeoffs: resolution/length/fps vs cost; single-pass vs iterative refine; text-to-video vs image-to-video heredity; watermark/authenticity vs usability.
  - Observability: job timeouts/trials, GPU utilization, safety (celebrity/voice/sexual-content), quota per user.
- Частые ошибки: sync generation; unbounded retries; ignore deepfake policy.
- Красные флаги: «видео так же дёшево, как текст», «без запрета на дипфейки».

### 15. Design an AI Coding Agent
- Идеал: agent that gathers context, acts, and verifies its own work in a loop (gather → act → verify), with tools to read/search/edit/write/run code.
- Обязательные пункты:
  - Loop: gather (search/read), act (edit/write/run), verify (run tests/build), loop on failure up to a step budget. Plan mode (read-only) for big changes.
  - Tools (Claude Code): Read, Grep, Glob, Edit, Write, Bash — model requests a tool, result feeds next decision (function calling).
  - Context engineering: search first to fit context window; CLAUDE.md as project memory loaded per session.
  - Control: ask-before-edit by default; modes manual/accept-edits/plan/auto; checkpoints to revert; subagents with fresh context.
  - Cursor taken apart: indexing (chunks → embeddings → vector DB, semantic retrieval); Tab (small fast model), Chat/Agent (big model), Apply (small model merging diffs, user accepts/rejects).
- Частые ошибки: single mega-prompt; no verification; no permissions.
- Красные флаги: «кодинг-агент = чат-бот с автодополнением», «может менять всё без контроля».

### 16. Design a Code Generation and Review System
- Идеал: generator + reviewer pipeline with multiple independent checks — static analysis, tests, LLM critique — and human approval for production code.
- Обязательные пункты:
  - Components: generator (LLM), reviewer/analyzers (static analysis, tests, critic agent), CI integration, human approval stage.
  - Data flow: task → generate → run linters/type-checks/tests → LLM critic review (style, correctness, maintainability) → fix loop → human diff review → merge.
  - Bottlenecks: test-run time, critic loop turns, codebase context size.
  - Tradeoffs: stronger review vs latency; automated vs human gates; small model for style vs big model for correctness.
- Частые ошибки: review without running code; single-shot generation unchecked.
- Красные флаги: «генерация и проверка — одно и то же», «без человеческого гейта».

### 17. Design a Content Moderation System Using AI
- Идеал: multi-stage moderation (fast classifiers → LLM semantic review → human escalation) with clear policy and low false-positive cost.
- Обязательные пункты:
  - Components: ingest (text/image/video/audio) → fast ML classifiers → rule/blocklist checks → LLM semantic reviewer → human review queue → user notification + takedown.
  - Data flow: user content → classifiers → queue → reviewer → decision (allow/blur/flag/remove) → appeal path.
  - Bottlenecks: real-time video/streaming (low latency), classifier false positives/negatives.
  - Tradeoffs: recall vs precision (block everything vs over-blocking); speed vs depth; automated triage vs human final word on borderline.
  - Extras: per-region/moderation of cultures; prompt-injection resistance; adversarial testing; monitoring of policy drifts.
- Частые ошибки: rely on single model; no appeal process; ignore adversarial bypasses.
- Красные флаги: «одна модель ловит всё», «блокируем без объяснений».

### 18. Design a Real-Time AI Recommendation System
- Идеал: low-latency mixing of retrieval and ranking, personalized per user, using streamed signals — an LLM only where it adds intent/semantic value.
- Обязательные пункты:
  - Two-stage: candidate generation (from many sources: collaborative filtering, content-based, popular, LLM-generated) → ranking model → re-rank/blend → business rules (diversity, freshness).
  - Feature store + streaming (Kafka) of clicks/views/implicit signals; near-real-time feature updates.
  - Serving with strict latency budget (<100 ms), often embed models on GPU/CPU and cache hot items.
  - Cold start handled via content signals, popularity priors, and exploration.
  - Tradeoffs: personalization vs diversity; compute vs latency (endpoint batching); CTR/ conversion as objective.
- Частые ошибки: one-pass architecture; long feature pipelines; no exploration.
- Красные флаги: «один большой LLM всё рекомендует» (LLM only as rerank, not the whole system).
### 19. Design an AI-Powered Email Assistant
- Идеал: drafts replies with context (RAG over user's inbox), handles tools (calendar/CRM), and never sends without explicit user approval — emails are untrusted input.
- Обязательные пункты:
  - Components: mailbox connector, RAG over history, draft LLM, tool-calling layer (calendar, CRM), safety layer (prompt-injection resistant), approval flow.
  - Data flow: new email → triage (priority) → RAG lookup → draft generation → inline suggestions → user approves/sends.
  - Bottlenecks: PII handling, inbox scale, injection risk (attacker-driven emails must not make the agent take tool action).
  - Tradeoffs: full auto vs human-in-the-loop (approve critical sends); RAG breadth vs token cost; structured reply vs creative drafting.
- Частые ошибки: auto-send; shallow RAG causing wrong tone/context; ignoring injection via email content.
- Красные флаги: «отправляем без подтверждения», «недостаточно проверить права каждого получателя».

### 20. Design a Medical Diagnosis Assistant Using AI
- Идеал: decision-support, not autonomous diagnosis — the assistant suggests differentials and explains, while a human clinician decides.
- Обязательные пункты:
  - Components: structured symptom intake, knowledge/RAG over vetted clinical sources, differential-generator LLM, risk triage, explanation layer, clinician review end step, audit log.
  - Data flow: symptoms → structured form → retrieval → differentials ranked with evidence → clinician confirms → follow-up plan.
  - Bottlenecks: safety (hallucinations), lack of patient-specific context, regulatory compliance (HIPAA/GDPR), bias in data.
  - Tradeoffs: breadth of recall vs precision of diagnosis; speed vs safety (always escalate in emergencies).
- Частые ошибки: считать диагноз, давать уверенные вердикты, отсутствие отказа от ответственности.
- Красные флаги: «LLM ставит диагноз сам», «нет этапа врача», «нет источника для каждого высказывания».

### 21. Design a Fraud Detection System Powered by LLMs
- Идеал: ensemble — fast ML/rule models flag anomalies; an LLM explains reasons from unstructured signals (emails, support tickets, chat) for human review and writes evidence narratives.
- Обязательные пункты:
  - Components: feature engine, fast rule/ML scorers (real-time), queue, LLM explainer (why flagged, evidence), dashboards, backoffice human review, feedback loop to retrain.
  - Data flow: transaction/activity → features → real-time scorers → threshold → LLM case summarization → decision (allow/review/block) → feedback.
  - Bottlenecks: real-time latency (block before action), false-positive rate (costly human review), non-determinism of LLM explanations.
  - Tradeoffs: allow vs block; ML speed vs LLM interpretability; generic vs per-industry models.
- Частые ошибки: put LLM in real-time decision path; non-deterministic blocking; zero feedback loop.
- Красные флаги: «LLM решает блокировку напрямую без ML/правил», «нет объяснения решений для регулятора».

### 22. Design an AI-Powered Data Extraction Pipeline from Unstructured Documents
- Идеал: document ingestion (OCR/parse) → LLM extraction into typed/structured output → validation and human-in-the-loop for low-confidence fields.
- Обязательные пункты:
  - Components: ingestion (OCR, layout parsing, chunking), embedding/retrieval or direct document pass, extraction LLM (prompted for JSON/schema), validation layer (types, ranges, cross-field checks), correction queue for human review, storage.
  - Data flow: document → OCR → LLM extract (by schema) → validate → confidence gate → auto-approve or route to human review → store structured record.
  - Bottlenecks: OCR errors on poor scans, schema drift, hallucinated field values, scale (documents/day).
  - Tradeoffs: accuracy vs cost (per-page LLM calls); full-doc vs chunked extraction; prompting vs fine-tuning.
- Частые ошибки: trust first-pass extraction; no schema validation; no human review for high-value/low-confidence fields.
- Красные флаги: «модель просто прочитала документ и всё», «нет проверки типов/диапазонов».

### 23. Design a Text-to-SQL System over a Data Warehouse with Thousands of Tables
- Идеал: NL → validated SQL with a catalog/schema grounding layer, safety guardrails, and deterministic execution.
- Обязательные пункты:
  - Components: query understanding, schema/table catalog + metadata (descriptions, columns, sample values), semantic retrieval to pick relevant tables (not all thousands), SQL generator LLM, syntax + semantic validators, read-only DB executor with row/result limits, explicit user confirm for writes.
  - Data flow: question → catalog/schema retrieval → SQL generation → validate → execute (read-only) → format result → explain.
  - Bottlenecks: schema explosion (pick correct tables), hallucinated column/table names, cost/latency of big schema prompts, SQL errors.
  - Tradeoffs: broad schema coverage vs prompt size; accuracy vs speed (few-shot + tools); direct write vs human-approved write (writes must be gated).
- Частые ошибки: send all thousands of tables into the prompt; allow unapproved writes; no validation of generated SQL.
- Красные флаги: «генерируем SQL на всю схему разом», «разрешаем UPDATE без подтверждения».

### 24. Design a Personalized Learning Assistant
- Идеал: adaptive tutor — builds a model of the learner (knowledge, pace, gaps), generates practice and explanations at the right difficulty, and tracks progress.
- Обязательные пункты:
  - Components: learner profile/store, knowledge-tracing (gap detection from answers), content generator (explanations, quizzes), difficulty adaptation, spaced-repetition scheduler, progress dashboard.
  - Data flow: answer → knowledge update → pick next topic/difficulty → generate content → feedback → schedule review.
  - Bottlenecks: personalization quality, content generation cost/latency, avoiding learner frustration/boredom.
  - Tradeoffs: mastery vs breadth of curriculum; auto-generated vs curated content (factual accuracy); strict pacing vs learner freedom.
- Частые ошибки: ignore the learner model (one-size-fits-all); no knowledge tracking; generate content without verifying correctness.
- Красные флаги: «одни и те же задания всем», «нет отслеживания прогресса», «модель придумала неверный факт».

### 25. Design an AI System for Automated Code Migration
- Идеал: plan-first migration where the agent analyzes the codebase, proposes a migration plan, applies changes (language/framework/API), and verifies via builds/tests — with human approval on plan and diffs.
- Обязательные пункты:
  - Components: codebase analysis (structure, dependencies, usage), migration planner, transformation engine (AST-based plus LLM for tricky rewrites), verification (tests/build), rollback/checkpoints.
  - Data flow: select codebase + target → analyze → plan (module-by-module) → transform (AST/LLM) → run tests → fix loop → human review → commit.
  - Bottlenecks: language/framework coverage, cross-file dependencies, long-running transforms, verifying behavioral equivalence.
  - Tradeoffs: automated vs manual (high confidence regions auto, risky ones human), one-shot vs staged rollout, correctness vs speed.
- Частые ошибки: rewrite everything in one pass; no tests as the safety net; skip human approval on behavior-changing diffs.
- Красные флаги: «мигрируем всю кодовую базу одним запросом», «без тестов и отката».
