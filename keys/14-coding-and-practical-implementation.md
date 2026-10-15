# Coding and Practical Implementation — Answer Key (1-32)

### 1. Implement a basic RAG pipeline using an embedding model and a vector database
- Идеал: index once (chunk → embed → store), then per query (embed → search → prompt → generate) end-to-end. All stages named.
- Обязательные пункты:
  - Index step (done once): chunk documents → embed each chunk → store vector along with original text (+ metadata) in vector DB.
  - Query step: embed the question with the SAME embedding model → vector DB returns top-k chunks (cosine/ANN).
  - Generation step: build prompt with "answer only from the given context" + the k chunks, LLM synthesizes a grounded answer (optionally with citations).
  - Edge cases: empty corpus / low-similarity query → say "not found" instead of hallucinating; metadata filters (pre vs post); must re-embed everything if the embedding model changes.
  - Complexity: O(key) per query is cheap; dominant latencies are embedding + LLM generation.
  - Sketch: `def answer(q): v=embed(q); ctx=kb.search(v, k=5); return llm(f"Context:\n{ctx}\nQuestion:{q}\nAnswer:" )`.
- Частые ошибки: embed документов на каждый запрос; ответ без grounding; игнор retrieval quality.
- Красные флаги: «RAG переобучает модель», «вектор БД = обычная SQL with O(n) scan».

### 2. Build a simple AI agent with tool use (e.g., calculator, web search)
- Идеал: ReAct-style loop where LLM reasons, recommends a tool, code executes it, observation feeds back — until Final Answer.
- Обязательные пункты:
  - Five parts: LLM (brain), system prompt (tools + rules), tools (name/description/input schema), memory (history of thoughts/actions/observations), loop controller (runs the loop, checks stop).
  - Cycle: Thought → Action → Observation → repeat; exit on Final Answer or max_steps (safety stop).
  - The LLM proposes, code executes — the model never runs tools itself; modern APIs return multiple tool_calls per turn, run in parallel.
  - Trigger: multi-step tasks a single call can't finish (e.g. search → calculator → final answer).
  - Sketch: `while step<max_steps: r=llm(msgs,tools); if r.final: return r; [msgs.append(tool_result(call_tool(t))) for t in r.tool_calls]`.
- Частые ошибки: один вызов без цикла; нет memory; нет лимита шагов; модель "сама" исполняет инструменты.
- Красные флаги: «агент = просто API call», «бесконечный цикл без stop conditions».

### 3. Implement semantic search using embeddings and cosine similarity
- Идеал: query and documents become vectors; rank by cosine similarity; match meaning, not exact words.
- Обязательные пункты:
  - Keyword search fails on synonyms ("repair car" vs "fixing automobile") — exact spelling only.
  - Embedding = vector of numbers that captures meaning; similar texts land close together.
  - Cosine similarity ∈ [-1, 1]: ≈1 same direction, ≈0 unrelated, ≈-1 opposite; higher = more similar → `cos(A,B) = (A·B)/(|A||B|)`.
  - Vector DB stores vector + original data + metadata; pre-filtering = filter first, post-filtering = drop after search (pre is better).
  - Embed docs once, embed query per search; ANN (HNSW/IVF/PQ) for millions, recall as quality metric.
  - Code: compute similarity each candidate, keep top-k.
- Частые ошибки: keyword matching, no normalization, comparing embeddings from different models.
- Красные флаги: «cosine score > 1», «semantic search = keyword == rank».

### 4. Write code for different text chunking strategies (fixed-size, recursive, semantic)
- Идеал: chunking because each piece needs one clear meaning, fits context window, cuts cost/latency, and retrieves well; can implement and contrast the big three.
- Обязательные пункты:
  - Fixed-size: cut after every N chars/tokens — simplest, predictable; cuts mid-word/idea → broken fragments. `for i in range(0,len(text),size): slice`.
  - Recursive: try strongest separator first (`["\n\n","\n",". "," "]`), recurse with next weaker separator on oversized parts, then merge tiny neighbors back to size. Most-used default; worst case falls back to spaces.
  - Semantic: split to sentences → embed each → cut where neighbor similarity drops below a tuned threshold. Real topic boundaries; slow/costly, threshold-sensitive, weak on one-flowing-topic docs.
  - Overlap (10-20%) preserves boundary context; structure-based chunking uses headings and carries heading path (`Leave Policy > Sick Leave`).
  - Choosing size: too big → blurry meaning; too small → lost context; validate on retrieval quality.
- Частые ошибки: фиксированный чанк без учета смысла; нет overlap; рекурсивный без merge-back; "семантика бесплатная".
- Красные флаги: «большой чанк = больше контекста = лучше», «chunk 100000 — ок».

### 5. Implement a prompt template system with variable substitution
- Идеал: safe, typed interpolation of variables into a reusable prompt with explicit placeholder set.
- Обязательные пункты:
  - Template with `{var}` placeholders; render via `str.format`/`format_map` (or regex for `{{` literal braces).
  - On render: detect missing keys (raise or fill defaults) — never silently produce broken prompt; coerce/serialize non-str values.
  - Separate sections (system, retrieved context, few-shot, user) and compose them; keep templates data-driven, not hardcoded.
  - Edge cases: literal braces, missing var, multimap conflicts, escaping user content to prevent template breakage/injection.
  - Sketch: `vars = regex findall(r"{(\w+)}", t); require vars ⊆ keys; return t.format_map({k: escape(v) for k,v in kwargs.items()})`.
- Частые ошибки: `.format()` на недоверенном вводе; молчаливая подстановка пустых значений; шаблоны, разбросанные по коду.
- Красные флаги: «бесплатно подставляю всё, что пришло», «prompt = конкатенация в 4 местах».

### 6. Build an evaluation pipeline for LLM outputs using LLM-as-a-judge
- Идеал: judge LLM scores another model's outputs against explicit criteria — human-level quality at machine cost/scale.
- Обязательные пункты:
  - Why: human eval doesn't scale; BLEU/ROUGE only check word overlap, miss meaning. A judge understands meaning; strong judges agree with humans >70-80% (≈ human-human agreement), so it's the default eval method.
  - Build steps: define criteria → pick judge model (≥ as capable as the evaluated model) → write prompt (task, input, output, scale, format) → validate on sample vs human ratings → iterate → run at scale.
  - Types: single-answer scoring (1-5/1-10), pairwise comparison (A/B), reference-based (vs ground truth), rubric-based (multi-criteria + overall — most common in prod).
  - G-Eval / chain-of-thought judging: judge writes its evaluation steps, applies them, then scores — better agreement than direct scoring.
  - Biases: style bias (prefers bullets/format over content), position bias (fix by swapping order + averaging), verbosity bias (longer = higher).
- Частые ошибки: судья слабее оцениваемой модели; нет критериев; не сверяли с людьми; не учитывают biases.
- Красные флаги: «judge всегда беспристрастен», «BLEU == качество ответа».

### 7. Implement streaming responses for an LLM API
- Идеал: get tokens as the model produces them via SSE instead of waiting for the full reply — live typing effect, tiny time-to-first-token.
- Обязательные пункты:
  - LLMs are autoregressive: one token at a time, each step looks back at all previous tokens.
  - SSE (Server-Sent Events): one HTTP connection kept open; `Content-Type: text/event-stream` tells the client to stream.
  - Event format: each token on a `data:` line, events separated by blank lines; often JSON payload; final event is `data: [DONE]` to end the stream.
  - Client: read chunks, buffer partial lines (arbitrary chunk boundaries), emit completed events, stop on [DONE].
  - Tradeoff vs WebSockets: SSE unidirectional (server→client), simpler, auto-reconnect; WS for bidirectional.
- Частые ошибки: думать, что модель генерирует ответ сразу; не обрабатывать частичные строки; не уметь ловить [DONE].
- Красные флаги: «streaming = поллинг», «SSE двунаправленный», игнор prefill → time-to-first-token.

### 8. Build a simple vector similarity search from scratch
- Идеал: brute-force nearest-neighbor from scratch, then motivate ANN/indexes for scale.
- Обязательные пункты:
  - Brute force: compare query vector with every stored vector, keep top-k by metric (cosine/dot/L2). O(n·d) time per query, O(n·d) memory.
  - Sketch: dot products across all vectors, then heapq.nlargest/partition to get top-k; store vectors + original data together.
  - Brute force too slow at scale (100M × 1000 dims = 100B ops/search) → ANN trades small accuracy loss for huge speed, measured by recall (e.g. 9/10 true nearest = 90% recall).
  - Indexes: HNSW (hierarchical layered graph, top-down jumps), IVF (cluster centers first, then search few nearest clusters), PQ (compresses each vector to save memory).
- Частые ошибки: only brute force / no ANN knowledge; «миллион векторов сравню в цикле на каждый запрос».
- Красные флаги: «ANN точнее brute force», «HNSW = exact search».

### 9. Implement a conversation memory system for a chatbot (sliding window, summary, buffer)
- Идеал: LLM stateless across calls; memory is everything built around it to fake remembering; layers + strategies.
- Обязательные пункты:
  - Layers: context window (what LLM sees now) → short-term (session scratchpad, lost at session end) → long-term (persistent user facts/preferences/summaries) → external knowledge (RAG, queried not maintained).
  - Four core ops: Write, Read, Update, Forget — all must work.
  - Runtime loop: read relevant memory → build prompt → LLM (+tools) → write back; long-term write often async so user doesn't pay latency.
  - Sliding window: keep last N messages (drop oldest) — simple, loses early context. Buffer: hold messages up to a token limit, then flush. Summary memory: periodically summarize old turns into a compact summary placed in the prompt.
  - Long-term sub-types: episodic / semantic / procedural; scope memories per user, consent for sensitive data.
- Частые ошибки: store everything (bloat kills retrieval); confuse short/long-term; no forget policy; mixing users' memories.
- Красные флаги: «LLM сам помнит диалог», «пишу каждый message в long-term».

### 10. Write code to detect and handle hallucinations in LLM outputs
- Идеал: no silver bullet; concrete detection mechanisms + mitigate, not just "run stronger model".
- Обязательные пункты:
  - Grounded-check: require citations; verify each claim/answer sentence against retrieved chunks (NLI: entail/contradict/neutral).
  - Self-consistency: sample N answers, aggregate; divergence ⇒ likely hallucination; use as an answer-conflict signal.
  - Confidence: logits/uncertainty; model verbalized confidence is unreliable.
  - Handle: on contradiction → return "insufficient evidence", regenerate grounded only, or route to retrieval again.
  - Sketch: `labels=[nli(s, ctx) for s in split_claims(ans)]; if any(l=="contradict"): return "no evidence found" else ans`.
- Частые ошибки: trust verbal "I'm sure"; regex on full answer without per-claim grounding; no sources at all.
- Красные флаги: «гарантирую 100%», «есть один universal detector».

### 11. Implement a retry mechanism with exponential backoff for LLM API calls
- Идеал: retry transient failures with capped exponential backoff + jitter; never retry client errors or non-idempotent effects.
- Обязательные пункты:
  - Retry on 429/rate-limit, 408/5xx, network/timeout; NOT on 400/401/403/422 (won't fix); honor `Retry-After` header.
  - Backoff formula `sleep = min(cap, base * 2**attempt) + jitter`; cap attempts (e.g. 5); overall deadline.
  - Generation is idempotent enough to retry; still prefer idempotency keys where available.
  - Sketch: `for a in range(max): try return call(); except transient: sleep(min(cap, base*2**a + rand())); else raise`.
- Частые ошибки: retry 400s; fixed delay без jitter; бесконечные ретраи; игнор Retry-After.
- Красные флаги: «retry при любом exception», «backoff = 1s forever».

### 12. Write a function calling (tool use) handler for an LLM API
- Идеал: model emits structured tool calls, your code executes and feeds results back; the model never runs anything itself.
- Обязательные пункты:
  - Tool schema = name + description + parameters (JSON schema: type, properties, required) — the "blank form".
  - Flow: user asks → model returns JSON call `{"name":…, "arguments":…}` → app runs real function → result appended as tool message → model writes final answer.
  - Conversation loop: user → model tool_call → tool result → model final; keep full history. Multiple tool calls per turn allowed; validate args.
  - Sketch: `if msg.tool_calls: for tc in msg.tool_calls: out = TOOLS[tc.name](**tc.args); msgs.append(tool_result(tc.id, out)); return call_llm(msgs, tools)`.
- Частые ошибки: думать, что модель исполняет функцию; не валидировать аргументы; не возвращать результат в историю.
- Красные флаги: «модель сама вызовет get_weather», «tool call без result message».

### 13. Implement a simple re-ranker for search results
- Идеал: two-stage retrieval: fast bi-encoder shortlist → cross-encoder rerank → top few; explain why both stages exist.
- Обязательные пункты:
  - Two-stage: fast retriever (BM25 or bi-encoder over the whole corpus → 100-200 candidates) → reranker reorders by true relevance → top 5-10 to LLM.
  - Bi-encoder encodes question and doc separately (independent embeddings, precomputed) — fast, loses fine detail; cross-encoder reads question+doc together → one score per pair — precise but must run per pair → only on the shortlist.
  - Rerank: score each (q, doc) pair, sort desc, keep top-k. Trade-off: more candidates = more accuracy + cost/latency; tune count (e.g. 100-200 → 5-10).
  - ColBERT = late interaction (token-level, in the middle); mechanism: correct doc "Paris is the capital" beats "mentions Paris" beats "capital of Germany".
  - Sketch: `pairs = [(ce(q, d) for d in cands)]; top = sorted(cands, key=score, rev).  top[:k]`.
- Частые ошибки: реранкер = поиск по корпусу; использовать cross-encoder на миллионы доков; не объяснить bi- vs cross-encoder.
- Красные флаги: «reranker ускоряет поиск», «reranker на весь корпус — идеален везде».

### 14. Build a basic document parser that extracts text from PDFs and splits it into chunks
- Идеал: extract text + structure (headings/order) from PDF, then recursive/structure-aware chunking.
- Обязательные пункты:
  - Extraction: PyMuPDF/pypdf/pdfplumber; handle multi-column, tables, code, scanned pages need OCR (Tesseract).
  - Preserve structure (headings, page/section path) before chunking → structure-based + recursive splitting with size cap + overlap.
  - Reuse chunking rules (recursive separators `["\n\n","\n",". "," "]`, then merge small pieces up to size); keep metadata (src, page, heading path).
  - Edge cases: tables/images/scanned PDFs, watermarks, garbage extract? OCR; empty pages; keep chunk+source link for citations.
  - Sketch: `text = extract(pdf); ch = recursive_chunks(text); store (embed(ch), ch)`.
- Частые ошибки: «PDF = plain text всегда»; игнор заголовков; теряем source mapping.
- Красные флаги: «парсить PDF = regex по тексту», «сканы без OCR».

### 15. Implement cosine similarity, dot product, and Euclidean distance from scratch
- Идеал: three metrics, formulas + semantics, O(d) each; know when each fits.
- Обязательные пункты:
  - Dot product `A·B = Σ a_i b_i` — combines direction AND magnitude; best when vectors normalized.
  - Euclidean/L2 `sqrt(Σ(a_i−b_i)²)` — straight-line distance; smaller = more similar; good for image/spatial data.
  - Cosine `cos = (A·B)/(|A||B|)` — angle only, robust to length; default for text/semantic.
  - Sketch: `dot=lambda a,b: sum(x*y for x,y in zip(a,b)); norm: sqrt(sum(x*x)); euclid = sqrt(dot(a−b,a−b))`.
- Частые ошибки: путать знак (для L2 малое = похожее), сравнивать непропормированные векторы, «длина вектора — это качество».
- Красные флаги: «cosine — кластеризация», «L2 чем больше тем лучше».

### 16. Write code to implement token counting and context window management
- Идеал: count tokens accurately with the model's tokenizer (not character counts), budget the window across sections.
- Обязательные пункты:
  - Count with tokenizer (tiktoken / model's tokenizer); ~1 token ≈ ¾ English word as rough heuristic only.
  - Budget: system + retrieved context + history + generated output must fit context window; reserve headroom for response.
  - On overflow: evict oldest turns (sliding window) BEFORE truncating retrieved context (early + late positions matter); prefer summaries; drop stale tool outputs.
  - Edge cases: very long single items, multi-turn incl. tool messages, per-model tokenizer differences, non-ASCII inflates? token count.
  - Sketch: `def make(msgs, budget): out=[]; for m in reversed(msgs): if f"size {tok(m) }"  # trim oldest`.
- Частые ошибки: считать по len(text) символами/словами; не бронировать место под ответ; обрезать середину.
- Красные флаги: «1000 символов = 1000 токенов», «всегда шлю всю историю вечно».

### 17. Build a simple prompt versioning system
- Идеал: immutable, all prompts versioned and auditable; easy rollback and comparison.
- Обязательные пункты:
  - Registry: store templates in code/DB with `id + version(+hash)`; render by `(id, version)`; immutable versions, new edit → new version (never mutate in place).
  - Content-address: hash the template → detect changes; record metadata (author, created_at, commit hash, notes, params).
  - Runtime: resolve latest by default, allow pinning; log which (id, version) was used per call for debugging/A-B.
  - Workflow: git + review; a constant/row type alongside code; ship a "default version" constant in code and keep history in DB.
- Частые ошибки: string constants в коде без версий; правим продовый промпт на ходу; не логируем версию вызова.
- Красные флаги: «версия промпта = комментарий в код», «перезаписываю промпт в прод без истории».

### 18. Implement a caching layer for LLM responses
- Идеал: exact-match cache to skip repeated identical calls; understand when caching is valid.
- Обязательные пункты:
  - Key = hash(model + messages/prompt + sampling params (temperature/top_p) + system); store value + TTL; return on hit.
  - Valid only for deterministic outputs: temperature=0 (or greedy); semantic/prompt cache is a separate feature — exact-match key breaks on tiny prompt differences.
  - Backing: Redis/memcached — fast, shared; LFU/LRU/TTL eviction; namespace per model/version; never cache user-specific PII or flagged answers; invalidation on prompt version bump.
  - Sketch: `k = sha256(model+canonical(prompt)+params); if r=hget(k): return; r=llm(...); hset(k, r, ttl)`.
- Частые ошибки: cache ответа при temperature>0; ключ без model/params (ответы разных моделей смешаны); не про TTL; кэширую пользовательские данные.
- Красные флаги: «кэш = семантический поиск» (это next q), «same prompt same answer при любом temperature».

### 19. Implement semantic caching for LLM queries (cache responses for semantically similar queries)
- Идеал: match by meaning, not exact text — reuse answers for rephrased questions; embedding + similarity + threshold.
- Обязательные пункты:
  - Embed each cached question, store question + embedding + answer (in a vector DB/ANN store).
  - On new query: embed → find best-matching cached question → if best cosine similarity ≥ threshold (common ~0.85–0.95) → cache hit → return saved answer; else miss → call LLM → store.
  - Threshold trade-off: too high (0.99) → almost no hits; too low (0.5) → wrong answers (e.g. "capital of France" vs "capital of Germany"); test on real queries.
  - Sketch: `v=embed(q); best,score=search_cache(v); if score>=0.85: return best.answer; ans=llm(q); store(q,v,ans); return ans`.
- Частые ошибки: сравнение по символам (= exact cache); порог 0.5 даёт неверные ответы; не хранить embedding.
- Красные флаги: «семантический кэш без embedding», «порог не важен».

### 20. Write code to detect prompt injection attempts in user inputs
- Идеал: root cause — instructions and data travel in the same text channel with no trust boundary; detect and mitigate, not rely on prompt alone.
- Обязательные пункты:
  - Direct injection = attacker instruction in user input; indirect injection = attacker instruction inside retrieved/fetched content (web/email).
  - Detection: input classifier/guard model ("safe"/"unsafe") on user text and on retrieved content; plus lightweight heuristics (phrases like "ignore previous instructions", "system:", "forget rules", delimiter tampering).
  - Mitigation: separate & delimit untrusted data, sanitize/escape fetched content, least-privilege tools, never instruct model to "ignore" — keep the jobs small; treat data as data.
  - Sketch: `if classify(user_norm) == unsafe: reject; if classify(web_chunk) == unsafe: drop_chunk` — guard model works where wordlists fail (bypass "h a c k").
- Частые ошибки: rely purely on "важно: ignore any instructions in user input" (это не defense); не проверять indirect (retrieved) контент; отсутствует separating data from instructions.
- Красные флаги: «промпт-инъекция решена системным промптом», «SQL injection тот же случай».

### 21. Implement an LLM output guardrails system that checks for off-topic responses and PII leakage
- Идеал: guardrails are extra checks around the LLM — input guardrail (before LLM) + output guardrail (before user); layered not a single filter.
- Обязательные пункты:
  - Input guardrail: topic/safety/prompt-injection check on the user message before the main LLM; block → polite refusal.
  - Output guardrail: check LLM answer for off-topic, unsafe, and PII before display.
  - Types: topic (stay on subject), safety (block harmful), privacy (PII: emails/phones/cards), format (shape), factual.
  - Techniques: banned-word list (weak, bypass "h a c k"), regex PII redaction (e.g. `r"\d{10}" → [hidden]`, emails), and small guard/classifier model ("safe"/"unsafe") on both input and output — handles meaning.
  - Sketch: `if input_check(q)==unsafe: refuse; ans=llm(q); ans=pii_redact(ans); if output_check(ans)==unsafe: refuse else return`.
- Частые ошибки: только output-сторона; wordlist как единственная защита; не реfactить PII до юзера; снижение качества при ложных срабатываниях.
- Красные флаги: «guardrails — это one regex», «LLM ответ сам себя проверит».

### 22. Build a multi-agent system where agents have different roles and collaborate on a task
- Идеал: 2+ LLM agents, each own prompt/tools, wired by a coordination layer; explain pillars, roles, communication.
- Обязательные пункты:
  - Definition: Multi-Agent = Specialized Agents + Communication + Coordination; agents that don't talk aren't a system.
  - Three pillars: specialization (focused role, small system prompt), communication (messages/shared memory/handoffs), coordination (orchestrator/fixed workflow/router).
  - Roles: orchestrator/manager, worker/subagent (researcher, writer, coder, data-analyst), router, planner, critic/reviewer (must have independent grounding), tool specialist (owns schema/SQL/knowledge).
  - Communication: message passing (point-to-point), shared state/blackboard, handoffs (message + control transfer); structured messages, not unstructured chat.
  - Coordination: sequential A→B→C, parallel + merge, hierarchical (orchestrator↔workers), blackboard, etc.; start small, add roles only for real gaps.
  - Tradeoffs: cost/latency high, harder to debug; critic loop until approve; example — Orchestrator→Researcher→Writer→Critic→final reply for a support email.
- Частые ошибки: субагенты без coordinator; нет structured protocol; «критик без независимых источников»; себе-довольная рекурсия (A проверяет сам себя).
- Красные флаги: «multi-agent = параллельные промпты», «стоимость/латентность игнорируются».

### 23. Implement scaled dot-product attention with a causal mask from scratch (NumPy or PyTorch)
- Идеал: exact formula `Attention(Q,K,V) = softmax(Q·K^T / √d_k) · V`, with the causal mask applied before softmax; known why.
- Обязательные пункты:
  - Q = X·W_Q, K = X·W_K, V = X·W_V (learned projections); scores = Q·K^T (query compares to every key).
  - Scale by `√d_k`: prevents scores blowing up → softmax extremes (≈0/1) that hurt learning.
  - Softmax over each row → weights sum to 1; output = weighted sum of V rows.
  - Causal mask: lower-triangular 1s (attend to self + past), zeros above; blocked positions set to −∞ BEFORE softmax (softmax(−∞)=0; using 0 instead leaves a non-zero weight → future leakage). Training must match inference (future tokens don't exist).
  - Complexity: O(n²·d) attention / O(n²) memory; causal mask halves nothing asymptotically — skip future half in flash-style impl; decoder = masked, encoder = bidirectional.
  - Sketch: `s = Q@K.T/sqrt(dk); s = s.masked_fill(triu(ones(n,n),1)==1, -inf); w = softmax(s,-1); out = w@V`.
- Частые ошибки: mask после softmax; маска нулями вместо −∞; не делить на √d_k; путают causal mask и sliding window.
- Красные флаги: «маска — zero перед softmax — ок», «causal у encoder тоже».

### 24. Implement multi-head attention, then convert it to grouped-query attention
- Идеал: MHA mechanics then why GQA shrinks KV cache; know MHA/GQA/MQA relations.
- Обязательные пункты:
  - MHA: h heads run self-attention in parallel; per head d_k = d_model/h (e.g. 512/8=64), each head own W_Q/W_K/W_V; concat all head outputs → linear W_O (mixes heads; output dim = d_model).
  - Why MHA: single head learns one relation at a time; multiple heads capture subject-verb, verb-object, long-range in parallel (paper "Attention is All You Need", 2017).
  - MHA problem: each head stores own K,V → huge KV cache at inference (per layer: heads × seq_len × head_dim × 2).
  - GQA: divide heads into groups; all heads in a group SHARE one K,V; each head keeps own Q. KV cache shrinks by (num_heads/num_groups); quality near MHA.
  - MQA = 1 group (all heads share K,V). GQA generalizes: groups=heads ⇒ MHA; groups=1 ⇒ MQA.
  - Sketch: reshape Q,K,V to (bs, heads, …, d_k); per-head mask+softmax; concat + W_O. For GQA: repeat K,V per group (`k = k.repeat_interleave(g, dim=1)` or reshape+expand) instead of independent Ws.
- Частые ошибки: think GQA меняет число Queries (нет — queries остаются на голову); скат goes O(nописыв); путают GQA с Pruning cache.
- Красные флаги: «GQA ускоряет тренировку», «GQA = меньше heads».

### 25. Implement a KV cache and single-step decode for causal multi-head attention
- Идеал: caching K,V of past tokens so each decode step computes only the new token's K,V, then attends to cached past.
- Обязательные пункты:
  - Problem: without cache the model recomputes K,V for every past token each step (2+3+…+N ≈ O(N²)); with cache compute ~1 new K,V per step (O(N)).
  - Cache only Key and Value, not Query — Query is only needed for the current (being-generated) token; past K,V are used by every future token.
  - Structure per layer: `cache_k[layer]` append new K row, `cache_v[layer]` append new V; attention = Q_new @ cached_K.T / √d_k (masked to past) → softmax → @ cached_V.
  - Phases: prefill (process full prompt once, fill cache) vs decode (one token/step, reuse cache).
  - Trade-off: speed vs memory — cache grows with sequence; sliding-window + attention sinks or paged attention bound/compact it. GQA/MQA shrink cache size.
  - Sketch (one layer, one new token): `k = proj_k(x); v = proj_v(x); K=cat([cache_k, k],1); V=cat([cache_v, v],1); out = softmax(q@K.T/√dk)@V`; return updated (K,V).
- Частые ошибки: cache только K без V; кэшировать Q; пересчитывать всю историю каждый шаг; не понимать prefill/decode.
- Красные флаги: «KV cache решает проблему памяти навсегда», «cache = промпт-кэш» (это рeuse между запросами).

### 26. Implement BPE (Byte Pair Encoding) training and encoding from scratch
- Идеал: BPE = subword tokenizer: start chars, repeatedly merge the most frequent adjacent pair until vocab reached; encoding replays merge rules in order — never greedy longest-match.
- Обязательные пункты:
  - Training: add end-of-word marker (e.g. `_`); count adjacent pairs over the corpus (weighted by word frequency); merge most frequent pair into a new token; repeat until target vocab size (32K–256K; LLaMA 3 ~128K, Gemma ~256K).
  - Result: vocab of chars + common subwords ("es","est","low") + full words; handles any word, any language/script.
  - Encoding new text: replay the ordered merge rules in the SAME order they were learned (e.g. "lowest" → l.o.w.e.s.t → es→est→lo→low → ["low","est"]); greedy longest-match can give different (wrong) results.
  - Why BPE: word-level → unknown words (one "unknown" token); char-level → too many tokens, slow, little meaning; BPE = middle ground.
  - Sketch/train: `pair = max(count(pairs)); corpus.replace(pair, token)` per iteration; encode: apply rules sequentially.
- Частые ошибки: greedy longest-match encoding вместо replay правил; не считать с весами частот; merge пары без end-of-word.
- Красные флаги: «BPE = простой split по словам», «encoding = lookup longest token in vocab».

### 27. Implement top-k, top-p, and temperature sampling over a logits vector
- Идеал: order of operations: temperature first, then top-k/top-p, then softmax + sample; code sketch.
- Обязательные пункты:
  - Temperature: `logits / T`; T<1 sharper (greedier), T>1 flatter (more random). Applied before softmax, never divide sampled probs.
  - Top-k: keep only k largest logits, zero the rest, renormalize → sample. (после temp)
  - Top-p (nucleus): sort probabilities desc, keep the smallest prefix with cumulative prob ≥ p, renormalize over kept tokens.
  - Final: sample one token (categorical distribution of the masked probs).
  - Sketch: `L = logits/T; if temp: L/=T? -- order: T → k → p → softmax on masked → np.random.choice`.
  - Complexity: O(vocab) per step (sort only for top-p).
- Частые ошибки: top-p поверх несофтмаксенных логитов без renormalization; порядок temp после p; убрать многие варианты.
- Красные флаги: «пьо обе вещи, а потом softmax?? incorrect order/no renormalization».

### 28. Implement an LRU cache with O(1) get/put, then add per-entry TTL
- Идеал: OrderedDict (dict + doubly-linked list) gives O(1); then TTL on top.
- Обязательные пункты:
  - Structure: hash map (key → node) + doubly linked list (eviction order), or `collections.OrderedDict` — move_to_end on touch; pop LRU on overflow.
  - Operations: get(key) — access returns, mark most-recently-used; put(key,value) — insert/update at MRU, evict LRU when capacity reached.
  - TTL: store `expires_at` per entry; on get check `now > expires_at` → delete (lazy); plus opportunistic sweep when adding (or a background timer) so expired entries don't linger.
  - Complexity: get/put O(1) amortized.
  - Sketch: `class LRU: ODict; get(k): if expired: del; else move_to_end; put(k,v): evict oldest if len==cap` (store expiry).
- Частые ошибки: реализация через list → O(n); не обрабатывать eviction; TTL check only on put.
- Красные флаги: «skipping TTL»; «это обязательно сингл-процессный».

### 29. Implement a token-bucket rate limiter for an LLM API where cost scales with tokens, then make it distributed
- Идеал: bucket with capacity + refill; each call consumes tokens proportional to request size; then scale across nodes.
- Обязательные пункты:
  - Token bucket: capacity C (burst), refill rate r tokens/sec; allowed if bucket has ≥ cost; debit cost; else reject/wait.
  - Cost = tokens in prompt + completion (per-model multiplier); limit by tokens, not requests.
  - Sketch: `now; bucket = min(C, bucket + (now-last)*r); if bucket >= cost: bucket -= cost; allow else: reject/wait`.
  - Distributed: shared counter → Redis; atomic Lua script (if remaining >= cost: decrement → allow, else reject) to avoid inter-node races; Redis single-threaded = linearizable; respect 429 + Retry-After clientside.
- Частые ошибки: лимит на реквесты, а не на токены; распределённый счётчик без атомарности (гонки); считают только completion.
- Красные флаги: «распределённый = локальный счётчик на каждом поде», «лимитирую по числу запросов».

### 30. Write an async batch processor that runs an LLM call over 50,000 documents with a concurrency limit, retries with jitter, and error isolation
- Идеал: controlled parallelism + resilient per-item failures, not one big loop.
- Обязательные пункты:
  - asyncio Semaphore limits concurrent in-flight calls (compliaно with API rate limit).
  - Per-item retry with exponential backoff + jitter on transient errors; cap tries and overall budget.
  - Error isolation: catch per-item exceptions → record (id, error) and continue; partial results returned; don't let one doc fail the whole batch.
  - Progress/checkpointing so a crash can resume; monitor rate-limit headers.
  - Sketch: `sem=Semaphore(N); async def go(i): async with sem: return retry(lambda: llm(docs[i]))` → `await gather(*(go(i) for i in range(50_000)))`; failures collected separately.
- Частые ошибки: все 50k в один gather одновременно (blow rate limit); один failed item роняет батч; retry без jitter/no cap; нет resume.
- Красные флаги: «concurrency = threads count», «без обработки отдельный item = всё падает».

### 31. Write a streaming SSE parser for LLM token streams that handles arbitrary chunk boundaries
- Идеал: incremental buffer-based parser that yields complete events even when `data:` lines split across network chunks.
- Обязательные пункты:
  - Buffer incoming bytes; split on `\n\n` (blank line = event boundary); partial data stays in buffer for next chunk.
  - Parse event: strip `data:` prefix; a `data:` value may arrive split across chunks (assemble); multiple `data:` lines per event → multi-line data; `data: [DONE]` = end signal.
  - Edge cases: split inside a token/word, `\r\n` line endings, several events in one chunk, keep-alive/heartbeat comment lines (`:`), last event without trailing blank line.
  - Sketch: `buf += chunk; while "\n\n" in buf: ev, buf = buf.split("\n\n", 1); yield parse(ev)`.
- Частые ошибки: парсить по сетевому пакету (assume one event per chunk); терять хвост незавершённого события; не обрабатывать [DONE]; считать каждый data: = токен.
- Красные флаги: «события приходят строго по одному», «data: только одна строка навсегда».

### 32. Implement a minimal agent loop with tool dispatch, error handling, and a step budget
- Идеал: Think → Act → Observe loop; the runtime (not the LLM) executes tools; all from the reference (whole loop fits ~20 lines).
- Обязательные пункты:
  - Natural stop: LLM returns final answer (`response.is_done`); safety stop: `max_steps` counter; production adds time/cost budgets + human interrupt.
  - Tool dispatch: loop over `response.tool_calls` (can be several, run them), append each result as a `tool` message to the history.
  - Error handling: try/except per tool call → write error string as observation so the LLM can adapt; never silently crash the loop.
  - Common failures: infinite loops (step limit), repeated identical action (detect and warn the LLM), context overflow (summarize/drop old turns). The LLM is stateless — history is resent every turn.
  - Sketch: `while step<max_steps: r=await call_llm(messages,tools); if r.is_done: return r.final_answer; for tc in r.tool_calls: try: res=await call_tool(tc.name,tc.args) except Exception as e: res=str(e); messages.append({"role":"tool","name":tc.name,"content":str(res)}); step+=1`.
- Частые ошибки: нет step budget; не обернуть tools в try/except; не вернуть observation в messages; забыть, что LLM stateless.
- Красные флаги: «агент без лимита шагов»; «tool ошибка убивает весь процесс»; «код — длинный, а суть — цикл».

---

Coverage: 32/32 questions in order; all refs are reflected (react, semantic search, vector DB, chunking, LLM-judge, streaming, agent memory, function calling, reranker, semantic caching, prompt injection, guardrails, multi-agent, attention math, causal masking, multi-head, GQA, KV cache, BPE, agent loop); the rest synthesized from industry-standard practice.
