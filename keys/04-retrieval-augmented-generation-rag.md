# Retrieval-Augmented Generation (RAG) — Answer Key (1-42)

### 1. What is Retrieval-Augmented Generation (RAG), and why is it important?
- Идеал: RAG = Retrieval + Augmented + Generation — it fetches relevant text from private/current documents at inference time and adds it to the LLM prompt, letting the model answer from data it never trained on.
- Обязательные пункты:
  - Keeps LLM answers grounded in real documents — reduces hallucination.
  - Knowledge stays current without retraining; update docs = update answers.
  - Complements parametric knowledge; best for factual, dynamic, or private data.
  - Foundation of enterprise AI: combines retrieval with generation.
- Частые ошибки: описывать как «поиск + генерация» без embeddings/векторного поиска; путать с fine-tuning.
- Красные флаги: «RAG заменяет память модели», «RAG — просто поиск по документам».

### 2. Explain the architecture of a basic RAG system.
- Идеал: Two phases — offline indexing (chunk → embed → store) and online query (embed question → ANN search → top-k → augment prompt → LLM generate).
- Обязательные пункты:
  - Indexing: parse document → chunk → embed → store in vector DB with metadata.
  - Query: embed query → ANN search → retrieve top-k → build prompt [chunks + question] → LLM → answer.
  - Straight-line flow: retrieve once, generate once (no loop).
  - Optional reranker between retrieval and generation.
- Частые ошибки: забывать различие indexing/query фаз; не учитывать статичность embeddings после индексации.
- Красные флаги: «архитектура = vector DB + LLM» (пропускают chunking/retrieval/reranking).

### 3. What are the key components of a RAG pipeline?
- Идеал: Five components: (1) document processing + chunking, (2) embedding model, (3) vector database (ANN index), (4) retrieval + optional reranking, (5) LLM generation with augmented prompt.
- Обязательные пункты:
  - Chunking: strategy (fixed/semantic/recursive) + size + overlap.
  - Embedding model: encodes text into vectors; choice affects quality/cost/speed.
  - Vector DB: stores vectors + metadata; supports ANN indexes (HNSW/IVF/PQ).
  - Retrieval: ANN top-k → optional reranker (cross-encoder/ColBERT/LLM) reorders.
  - Generation: LLM gets chunks + question + system prompt → grounded answer.
- Частые ошибки: считать vector DB и embedding одной вещью; пропускать reranker в production.
- Красные флаги: «достаточно Pinecone», «chunking не нужен».

### 4. What are chunking strategies, and how do you choose the right chunk size?
- Идеал: Cutting a document into small pieces so the right chunk is retrieved at query time. Balance concept completeness, embedding-model token limit, and retrieval precision.
- Обязательные пункты:
  - Too small → loses context; too large → blurs detail and precision.
  - Must fit embedding model's max tokens (e.g. 512/8192).
  - Narrative → larger; Q&A/legal clauses → smaller.
  - Overlap preserves boundary context but adds redundancy; ~10-20% typical.
  - Evaluate on recall + answer quality; try 512 tokens to start.
- Частые ошибки: брать size без тестов; большой overlap (стоимость).
- Красные флаги: «512 всегда достаточно», «chunking не влияет на retrieval».

### 5. Compare fixed-size chunking, semantic chunking, and recursive chunking.
- Идеал: Fixed-size splits at token/char boundaries ignoring meaning. Recursive splits at strongest separators first (blank lines → newlines → full stops → spaces), falling back only when needed, preserving paragraphs. Semantic splits at embedding-similarity boundaries, keeping complete ideas together.
- Обязательные пункты:
  - Fixed-size: simple, fast; cuts mid-sentence — breaks meaning; hard to size.
  - Recursive: never exceeds size limit (falls back to spaces); most chunks match paragraphs; safest default.
  - Semantic: whole idea units; most expensive; best for thematic documents.
  - Contextual (separate): LLM writes a context note per chunk (Q6).
  - Choose: recursive default; semantic when clear thematic shifts; fixed only for prototyping.
- Частые ошибки: fixed-size в production; не мержить крошечные соседние куски в recursive.
- Красные флаги: «recursive = semantic», «fixed-size достаточно».

### 6. What is Contextual Retrieval, and how does it improve RAG?
- Идеал: Add a short LLM-written note (50-100 tokens) before each chunk at index time explaining where it sits in the document, so retrieval finds it even when the chunk alone is ambiguous («the company», «it», «above table»).
- Обязательные пункты:
  - Problem: chunks lose document context (entities/section names at doc top).
  - Process: split doc → for each chunk send (doc + chunk) to LLM → 2-4 sentence note → note+chunk → embed + BM25 index.
  - Contextual Embeddings + Contextual BM25 give two signals; reranking improves further.
  - Cost: prompt caching reuses the shared document across chunks; one-time per doc.
  - Use when chunks cross-reference outside text; skip when chunks self-contained.
- Частые ошибки: применять везде (дорого без пользы); не использовать prompt caching.
- Красные флаги: «замедляет inference» (затраты только при индексации).

### 7. What are embedding models, and how do they convert text to vectors?
- Идеал: An embedding model encodes text into a dense vector where similar meanings map to nearby points. The model works on vectors, not text.
- Обязательные пункты:
  - Embedding = list of floats (vector); similarity measured by cosine/dot/Euclidean.
  - Similar meaning → close vectors; trained via contrastive learning.
  - Vectors from different models are incompatible languages — never mix.
  - Traps: negation («safe» vs «not safe») sits close; embeddings carry bias; new words badly placed.
  - Long text → one vector loses detail; hence chunking.
- Частые ошибки: сравнивать embeddings разных моделей; думать, что embedding проверяет факты.
- Красные флаги: «embeddings понимают текст».

### 8. How do you choose an embedding model for your RAG system?
- Идеал: Match language/domain, then benchmark on your own retrieval task — no universal best.
- Обязательные пункты:
  - Language: multilingual model for mixed languages (e.g. multilingual-e5).
  - Domain: general models fail on jargon; use domain fine-tuned.
  - Max sequence length covers your chunk size.
  - Vector dims: higher = expressive but costly.
  - Benchmark on your question-chunk pairs (recall@n); model change forces full re-embed.
  - Trade cost/latency vs accuracy (small all-MiniLM vs large text-embedding-3).
- Частые ошибки: выбор по общим бенчмаркам без своих данных; игнор token limit.
- Красные флаги: «самая большая = лучшее».

### 9. Explain Agentic RAG.
- Идеал: RAG + AI Agent that drives the retrieval loop — decides which tool, which query, whether to re-retrieve, when to stop.
- Обязательные пункты:
  - Three building blocks: Agent (LLM), Tools (vector/SQL/web/graph/keyword), Loop (runtime + scratchpad).
  - ReAct loop: think → act → observe → repeat.
  - Fixes multi-hop, ambiguous queries, multiple sources, bad retrieval.
  - Patterns: Self-RAG (grades own retrieval), CRAG (fallback), query decomposition.
  - vs Standard: fixed one-shot → dynamic loop; higher latency + cost.
- Частые ошибки: без лимита итераций (бесконечный цикл); путать с plain tool-calling.
- Красные флаги: «агент сам вызывает tools», «всегда лучше standard RAG».

### 10. What is hybrid search, and why is it better than pure vector search?
- Идеал: Runs keyword (BM25) and semantic (embedding) search independently, then fuses the ranked lists — catches both exact matches and meaning.
- Обязательные пункты:
  - Keyword: exact terms, proper nouns, IDs, numbers, negation.
  - Semantic: meaning-neighbor chunks despite different words.
  - Fusion 1 — RRF: score = sum of 1/rank per list; ignores raw scores, avoids scale mismatch; simple default.
  - Fusion 2 — Weighted combination: normalize both scores to [0,1], blend with weights (e.g. 0.7 kw + 0.3 sem); tunable but needs tuning.
  - No normalization ⇒ can't add raw scores directly.
- Частые ошибки: сравнивать raw scores разных поисков без нормализации.
- Красные флаги: «hybrid = параллельный запуск без fusion».

### 11. What is re-ranking, and how does it improve RAG retrieval quality?
- Идеал: Two-stage: fast bi-encoder first-stage returns top-k candidates; a more precise cross-encoder reranker reorders them for true relevance.
- Обязательные пункты:
  - Bi-encoder: query & doc encoded separately → fast (precomputed) but coarse.
  - Cross-encoder: query+doc together → single relevance score, precise but O(n)/query.
  - Rerank a shortlist (top 50-200), not the whole corpus.
  - Accuracy vs latency/cost; cross-encoder most accurate, ColBERT middle, LLM strongest/slowest.
- Частые ошибки: пропускать reranker; запускать cross-encoder на всём корпусе.
- Красные флаги: «reranker = отдельный поиск», «reranker заменяет ANN».

### 12. What is ColBERT, and how does late interaction retrieval work?
- Идеал: Contextualized Late Interaction over BERT. Encodes query and document into per-token vectors; docs precomputed; a cheap MaxSim computes word-by-word similarity at query time.
- Обязательные пункты:
  - Each token → 128-dim unit vector (cosine = dot).
  - Docs encoded once, stored; query encoded at runtime.
  - MaxSim: sum over query tokens of max over doc tokens of dot(Eq_i,Ed_j).
  - Max (not avg) rewards one strong match (0.96 vs 0.52 diluted).
  - Pairwise softmax cross-entropy loss (positive > negative).
  - ~170x faster than BERT reranker, same MRR (34.9 vs 34.7); index ~100x bigger (154GB MS MARCO).
  - ColBERTv2 residual compression (→16-25GB); PLAID centroid pruning.
  - Usable as first-stage retriever OR reranker; ColPali extends to image patches.
- Частые ошибки: путать с cross-encoder; игнор storage cost.
- Красные флаги: «ColBERT — только reranker», «late interaction медленная».

### 13. Compare reranker architectures: cross-encoder, ColBERT, and LLM-based rerankers.
- Идеал: Triangle of accuracy/speed/cost. Cross-encoder most accurate per pair but slowest (no precompute). ColBERT word-level with precomputed docs, middle. LLM-based strongest judgment but slowest/most expensive.
- Обязательные пункты:
  - Cross-encoder: doc+query together → score; no precompute; best quality, poor scale.
  - ColBERT: per-token bag, precomputed docs, MaxSim; ~same quality as cross-encoder, ~170x faster, 100x bigger index.
  - LLM-based: LLM judges/ranks; strongest but slowest + costly.
  - Production: bi-encoder top-100 → reranker → top 5-10 chunks to LLM.
- Частые ошибки: сравнивать только скорость, не учитывая storage/стоимость; пропускать reranker на малом корпусе.
- Красные флаги: «LLM-based reranker всегда лучший» (дорого при большом top-k), «cross-encoder можно гонять по всему корпусу».

### 14. How do you handle multi-document and multi-hop questions in RAG?
- Идеал: Standard RAG can't answer questions whose evidence is spread across multiple chunks. Fix with Agentic RAG (agent decomposes and routes each sub-question) and GraphRAG (walk relations across chunks).
- Обязательные пункты:
  - Multi-hop: find entity X first, then use X to query Y.
  - Agentic decomposition: split into sub-questions, each search, combine results; multi-tool routing.
  - GraphRAG: embeddings find starting entity, walk the graph to connected entities, collect nodes/edges/chunks/summaries — no single chunk holds the full chain.
  - Multi-query retrieval: generate multiple query variants, search each, merge with RRF.
  - Query decomposition: split «compare A and B» into per-fact subqueries.
- Частые ошибки: надеяться, что одна стопка chunks покроет multi-hop.
- Красные флаги: «обычный RAG справляется с multi-hop», «одна большая chunk = решение».

### 15. What is the "lost in the middle" problem in RAG systems?
- Идеал: LLMs attend to the start and end of a long prompt but underuse the middle (U-shaped attention curve). Middle chunks get ignored → wrong answers even when the correct chunk is present.
- Обязательные пункты:
  - The U-shaped curve: beginning strong, end strong, middle weak.
  - Evidence: insert the answer chunk at different positions → accuracy drops in middle.
  - Send fewer, better chunks (reranker) + order strongest first / second-strongest last, fold inward.
  - Put the question at the very end of the prompt (strongest position).
  - Repeat critical instructions at start AND end.
  - Bigger context window ≁ fix (capacity ≠ quality).
- Частые ошибки: «контекст 200K решает всё»; dump everything in prompt.
- Красные флаги: «большой контекст устраняет lost-in-middle», «порядок chunk незначим».

### 16. How do you evaluate a RAG system? Explain faithfulness, relevance, and context precision/recall.
- Идеал: Decompose RAG eval into retrieval quality (context precision/recall) + generation quality (faithfulness, answer relevance).
- Обязательные пункты:
  - Context Precision: of retrieved chunks, how many are relevant.
  - Context Recall: did retriever find ALL needed context (ground-truth coverage).
  - Faithfulness (Groundedness): is the final answer supported by the retrieved context — or did the model make it up.
  - Answer Relevance: does the answer address the user's question.
  - LLM-as-a-judge scores each; frameworks: RAGAS, DeepEval.
- Частые ошибки: оценивать только финальный ответ без retrieval; путать faithfulness с answer relevance.
- Красные флаги: «accuracy достаточно для RAG», «RAG нельзя оценить».

### 17. Explain Self-RAG. How does the model decide when to retrieve?
- Идеал: Agentic pattern where the model grades its own retrieval on relevance + support (groundedness), then decides to skip, trust, or re-retrieve before generating.
- Обязательные пункты:
  - Two reflections: relevance (chunks about question) and support (chunks back answer).
  - If irrelevant/unsupported → skip or trust less; else generate.
  - Decides when to retrieve: no retrieval for small talk, yes for open facts.
  - Quality control on what the agent fetches before generation.
  - Distinguish from CRAG (fallback on bad retrieval) and ReAct (reasoning style).
- Частые ошибки: путать с ReAct/CRAG; не понимать self-grading.
- Красные флаги: «модель ничего не проверяет в найденных chunk», «Self-RAG = один rewrite».

### 18. What is GraphRAG, and when would you use it over traditional RAG?
- Идеал: GraphRAG = knowledge graph + vector search. Index phase: LLM extracts entities and relations → graph, merges entities across chunks, groups connected nodes into communities and writes community summaries. Query phase: embed question → find start entities → walk graph → collect nodes, edges, chunks, summaries → LLM answer.
- Обязательные пункты:
  - Two phases: indexing (expensive, once) and query (cheap, per-question).
  - Entity graph with merged entities — thick node for Globex containing all info.
  - Local search: specific entity — small subgraph + chunks.
  - Global search: whole dataset — community summaries with map-reduce (map: per-community partial answers + relevance; reduce: merge top ones).
  - When to use over traditional RAG: connection-rich data, multi-hop, high-level themes, entity-centric questions.
  - Trade-offs: expensive indexing (many LLM calls), heavier storage, costly updates, complex engineering.
- Частые ошибки: заявлять «GraphRAG не хранит embeddings» — он их использует как key.
- Красные флаги: «GraphRAG = всегда лучше», «GraphRAG без graph DB`.

### 19. Vectorless RAG
- Идеал: Vectorless RAG keeps documents whole and uses an LLM to choose where to look — reads titles/summaries then sections, walks a tree; no embeddings, no vector db.
- Обязательные пункты:
  - Tree of sections: chapters → subsections; LLM decides each hop.
  - Other vectorless: keyword search, SQL on structured data, whole-doc, agentic file browsing.
  - No chunking; full sections keep rules+exceptions together.
  - No vector DB / embedding model to build and maintain.
  - Easy updates (summary-only), visible reasoning, exact codes handled.
  - Works best on long structured docs.
  - Disadvantages: slower, costlier per question, needs structure, quality depends on summaries, doesn't scale alone.
- Частые ошибки: думать vectorless = без retrieval (есть keyword/SQL/whole-doc).
- Красные флаги: «масштабируется сам», «не нужен LLM».

### 20. How do you handle structured data (tables, SQL databases) in a RAG pipeline?
- Идеал: Don't embed tables as text — use text-to-SQL: LLM writes/runs a SQL query, returns rows as context. Numbers/dates handled precisely this way.
- Обязательные пункты:
  - Route: structured data → SQL path; unstructured → vector search — don't mix.
  - Convert tables to markdown/JSON for LLM context; keep structure.
  - Provide schema + few-shot; validate SQL accuracy.
  - SQL is exact for codes/IDs/amounts; qualitative text → vectors.
  - Hybrid routing: entity/quantitative → SQL; free text → vector.
- Частые ошибки: embedding таблиц как plain text.
- Красные флаги: «chunk таблицу как текст», «один пайплайн для всего».

### 21. What are the common failure modes of RAG systems, and how do you debug them?
- Идеал: Failure modes: poor retrieval (irrelevant chunks), hallucination despite context, lost-in-middle, stale/contradictory chunks, chunking damage, latency. Debug stage-by-stage: separate retrieval vs generation.
- Обязательные пункты:
  - Retrieval failure: inspect top-k, tune chunk/embedding, add hybrid reranking, query rewriting.
  - Grounding failure: prompt instruction («answer only from docs»), faithfulness eval, order chunks.
  - Checking each layer: chunking → embedding → retrieval → rerank → generation.
  - Symptom-driven: repeated errors tracked, monitored.
  - Add eval harness: regression questions, check metrics each release.
- Частые ошибки: сразу менять модель, не проверив retrieval.
- Красные флаги: «все проблемы решает prompt».

### 22. How do you handle document updates and maintain freshness in a RAG system?
- Идеал: Incremental indexing: detect changed docs, re-embed only those; store document IDs/hashes; deletions too.
- Обязательные пункты:
  - Content hash / document version → detect changes.
  - Re-index changed doc only; update metadata; delete stale chunks.
  - Embedding cache (skip unchanged embeddings).
  - Event-driven or scheduled job (cron) pipeline.
  - Cost control: re-embed only diffs, not whole corpus.
- Частые ошибки: полная переиндексация при одном изменении (дорого); забывать удалять удалённые.
- Красные флаги: «переиндексировать всё при каждом апдейте».

### 23. How do you optimize RAG for latency in production?
- Идеал: Attack each stage: ANN index, caching, fewer top-k, parallel rerank, GPU inference, precompute embeddings offline.
- Обязательные пункты:
  - Vector search: ANN (HNSW/IVF) instead of brute force.
  - Cache: semantic cache + prompt caching for repeated/shared prompts.
  - Reduce top-k and chunk sizes; rerank only shortlist.
  - Precompute embeddings at index time; no runtime embedding of docs.
  - Parallelize embedding/rerank; use small/fast embedding model.
  - Stream LLM output (first-token latency).
- Частые ошибки: преследовать только LLM latency; игнорировать retrieval p95.
- Красные флаги: «латенция = только время inference».

### 24. What is the role of metadata filtering in RAG systems?
- Идеал: Vector DB stores metadata alongside vectors; filter before/while searching by date, tenant, doc type, access level — improves precision and enforces security.
- Обязательные пункты:
  - Store metadata (source, date, tenant, tags, ACL, doc id) with each vector.
  - Filter first then search: restrict candidate set.
  - Essentials: accuracy on metadata-coded questions; ACL enforcement; dedup region.
  - Two-step: apply filter (e.g. tenant=X, date>2024) → ANN within that set.
- Частые ошибки: искать без фильтров потом фильтровать пост-фактум; игнорировать безопасность.
- Красные флаги: «метаданные не влияют на качество», «post-filtering безопасно».

### 25. Compare RAG vs fine-tuning. When would you use each?
- Идеал: RAG adds new/private knowledge at inference; fine-tuning changes model behavior/style/format on static data. Use RAG for facts and freshness, fine-tuning for behavior and domain tone; often combine.
- Обязательные пункты:
  - RAG: external retrieval + prompt; no retraining; grounded, current, transparent; cost per query.
  - Fine-tuning: teach style/format/task behavior; needs labeled data + retraining; knowledge strained and stale.
  - When to use RAG: private data, frequently updated knowledge, factual questions, citations needed.
  - When to use fine-tuning: output format, tone, domain jargon base behavior, task competence.
  - Both: fine-tune for behavior + RAG for knowledge = best.
- Частые ошибки: fine-tuning вместо RAG для свежих фактов/бюджет.
- Красные флаги: «FT заменяет RAG для знаний», «RAG учит модель стилю».

### 26. Long context windows keep getting cheaper. When should you use retrieval (RAG) vs putting everything in the context window?
- Идеал: Context window is capacity, not quality guarantee — lost-in-the-middle still degrades; cost grows per token. Use RAG to keep prompts short and relevant; only stuff full doc when it's small and the whole document matters.
- Обязательные пункты:
  - Retrieval (RAG): corpus bigger than prompt budget; need precision/grounding/citations; repeated queries across huge KB.
  - Whole-context: single short document where full understanding is required (e.g., one contract); Anthropic rule: KB < ~200K tokens (≈500 pages) can fit in prompt.
  - Cost/latency: large context = more tokens = money + time.
  - Lost-in-middle: more tokens → weaker middle recall.
- Частые ошибки: «дешевле контекста больше не нужен retrieval».
- Красные флаги: «контекст 200K избавляет от RAG», «больше токенов = лучше ответ».

### 27. What is query transformation in RAG (HyDE, query decomposition, step-back prompting)?
- Идеал: Query transformation rewrites/turns the user's question into a better search key before retrieval. Variants: HyDE (search with fake answer), rewriting, expanding, multi-query, decomposition, step-back.
- Обязательные пункты:
  - HyDE: ask LLM to write hypothetical answer (fake, even if wrong) → embed it → search. Works because answer-shaped text sits closer to real answer chunks than the question. Fake answer used only for search; final answer from real chunks. Costs one extra LLM call; may drift.
  - Query rewriting: rewrite into standalone clear query (follow-ups) or clean/expand/step-back.
  - Multi-query: LLM generates several query variants, search each, merge with RRF; duplicate removal.
  - Decomposition: split compound question into sub-questions.
  - Step-back: turn specific question into general one for background.
  - Use: question/answer word-shape differs; short/vague queries.
- Частые ошибки: показывать пользователю rewritten/hypothetical query; не merge правильно.
- Красные флаги: «мы доверяем fake answer как факту», «query rewriting = HyDE».

### 28. How do you implement citation and source attribution in RAG?
- Идеал: Track chunk provenance through the whole pipeline and have the LLM cite sources inline; verify citations against retrieved context.
- Обязательные пункты:
  - Each chunk carries metadata: source id, doc title, section, URL/PDF page.
  - Prompt: instruct model to cite chunk ids/[source] when using extracted facts; answer-only-from-docs.
  - Post-process: verify cited sources in the final context list; drop unsupported claims.
  - UI: render clickable citations linking to original docs.
  - Cite even numbers/claims from context, not parametric memory.
- Частые ошибки: генерировать ответ, потом просто прикрепить источники.
- Красные флаги: «модель сама знает источник», «цитаты не надо проверять».

### 29. How do you scale a RAG system to millions of documents?
- Идеал: Use ANN search, compress vectors, shard partitions, cache hot data, hybrid search — keep p95 latency and cost flat as corpus grows.
- Обязательные пункты:
  - ANN index (HNSW/IVF/PQ) instead of brute force.
  - Shard by tenant/metadata; distributed vector DB.
  - PQ or scalar quantization to shrink vectors in memory.
  - Parent-child and rerank shortlist to cut generation cost.
  - Cache embeddings + results; prompt caching.
  - Monitor recall vs latency; benchmark target recall.
- Частые ошибки: brute-force search; один индекс на всё.
- Красные флаги: «млн документов = просто больше RAM» (нужен ANN/shards).

### 30. What is parent-child chunking, and how does it improve retrieval?
- Идеал: Index small child chunks (for precise retrieval) and return their parent (larger context block) to the LLM — precision of small + context of large.
- Обязательные пункты:
  - Child: small chunk, embedded, used for candidate retrieval.
  - Parent: larger enclosing section, sent to LLM for answer.
  - Improves both: recall (small precise) and answer quality (full context).
  - Common in production RAG; also called small-to-big retrieval.
- Частые ошибки: путать с plain chunking sizes.
- Красные флаги: «parent-child = просто большие чанки», «оба куска embed».


### 31. Your RAG system is hallucinating despite having the right context. How do you fix it?
- Идеал: Diagnosis — cause is usually generation (not retrieval); fix with grounding prompt, faithfulness eval, better context ordering, and optional post-hoc verification (Self-RAG style).
- Обязательные пункты:
  - Cause: model may ignore context (lost-in-middle), or prompt allows extrapolation.
  - Fix 1: instruction «answer only from retrieved documents; if absent, say unknown» at start and end.
  - Fix 2: verify retrieved chunks contain the right answer (rerank + inspect); if not → retrieval fault, not generation.
  - Fix 3: place question at the very end of prompt; order chunks strongest-first.
  - Fix 4: Self-RAG style — grade support before trusting; reject unsupported answers.
  - Recurring issue → add faithfulness eval to regression suite.
- Частые ошибки: только менять temperature/prompt when correct context is missing.
- Красные флаги: «модель сама знает — промпты не влияют», «не обязательно проверять assertion».

### 32. Your RAG chunk overlap causes redundant results. How do you reduce redundancy?
- Идеал: Trim overlap margin; dedupe by document ID/content hash at index and query, use MMR to diversify results.
- Обязательные пункты:
  - Overlap creates duplicate copies of the same content in multiple chunks.
  - Reduce overlap/use large-sparse contexts or post-deduplication of retrieval results.
  - Content-hash dedup at index: 1 chunk per identical text.
  - MMR (Maximal Marginal Relevance): balance relevance against diversity when selecting final chunks.
  - Query-side: merge with RRF (multi-query) removes duplicates.
- Частые ошибки: отправить все повторы в контекст.
- Красные флаги: «повтор = усиление сигнала».

### 33. Your RAG retrieval is too slow with a large knowledge base. How do you speed it up?
- Идеал: Replace brute-force search with ANN (HNSW/IVF/PQ), cache, and reduced candidates.
- Обязательные пункты:
  - Adopt ANN index (HNSW layers > IVF clusters), PQ quantization → skip most comparisons.
  - Add prompt/semantic cache for hot queries.
  - Limit top-k; rerank shortlist only; shard partitions.
  - Faster embedding model + runtime precompute.
- Частые ошибки: решать за счёт GPU без индексации.
- Красные флаги: «brute-force для big data — ок», «единственный быстрый путь = больше RAM».

### 34. Your RAG system returns duplicate results. How do you deduplicate?
- Идеал: Normalize text then hash to find identical/near-identical chunks; keep a canonical copy per document.
- Обязательные пункты:
  - Content hash (MD5 of normalized text) at index dedups exact duplicates.
  - Semantic dedup (similarity threshold) removes near-duplicates.
  - Query-side: drop already-included chunks; use MMR; keep top-k unique by doc id.
  - RRF merge already handles multi-query duplicates: same doc from several queries collapses to one rank.
- Частые ошибки: только по URL/имени, а не по содержимому.
- Красные флаги: «дубли в KB безвредны».

### 35. Your RAG system needs per-user access control on internal documents. How do you implement it?
- Идеал: Enforce access control at retrieval time via metadata filters — once a doc is retrieved its ACL is checked / filtered; users cannot see docs they can't access.
- Обязательные пункты:
  - Store ACL/tenant in chunk metadata: doc_id + access level + tenant.
  - Add filter on user's allowed docs in the vector search query.
  - Never rely on post-generation filtering; filters restrict candidate set.
  - Consider separate index partitions per tenant; edge chat UI hides restricted content.
  - Design: ACL at ingestion → metadata → query filter.
- Частые ошибки: фильтровать после retrieval (утечки контекста), опираться на LLM запретами.
- Красные флаги: «user-level access в prompt», «post-filtering безопасно».

### 36. Your RAG system fails on domain-specific jargon. How do you fix it?
- Идеал: Teach the system the domain vocabulary: fine-tune/adapt embedding model, add lexicon + synonym/expansion in query transformation, use hybrid search.
- Обязательные пункты:
  - Embedding models trained on open text smear domain jargon.
  - Add domain glossary/synonyms in query rewriting/expansion.
  - Hybrid search keeps exact terms (keyword) alive.
  - Fine-tune a domain embedding model on in-domain data.
  - Add jargon-aware chunking/context notes; benchmark on domain queries.
- Частые ошибки: менять только LLM, не трогая embeddings/retrieval.
- Красные флаги: «jargon — знает LLM», «keywords ненужны с embeddings».

### 37. Your text-only RAG system now needs to handle images and tables. How do you extend it?
- Идеал: Add a multimodal strategy: (a) OCR/text extraction for tables, (b) generate text descriptions from images (vision LLM, ColPali), (c) embed those text descriptions, (d) route tables to structured SQL.
- Обязательные пункты:
  - Tables: parse to markdown/JSON → embed as text or put in SQL (best exact).
  - Images: vision model summarizes → embed summary; or ColPali-style late interaction over image patches.
  - Multimodal embeddings (CLIP-style) for image similarity; text-description hybrid.
  - ColPali: MaxSim over document image patches vs query tokens — visual doc retrieval over charts/scans.
  - Keep both: text chunks + image/table description chunks in the same index.
- Частые ошибки: только OCR без описание/таблиц, без мультимодального «понимания».
- Красные флаги: «embed картинку картинкой» (если нет vision), «таблицы = текст в порядке».

### 38. Your RAG knowledge base gets updated frequently and needs versioning. How do you manage it?
- Идеал: Add document versioning: unique doc/version ids, timestamps, per-version snapshots, incremental re-index on change, and audit trail.
- Обязательные пункты:
  - Store version + source_id + timestamp metadata on each chunk.
  - Incremental update: detect change (hash/version), re-embed only changed docs.
  - Keep version history for rollback; deletes propagate to index.
  - Optionally support «as-of»/recency filters for time-aware answers.
  - Separate ingestion pipeline with delta jobs and CI-like verification.
- Частые ошибки: хранить только latest версию, потерять историю/rollback.
- Красные флаги: «не нужен versioning для меняющегося KB».

### 39. Your RAG system fails on multi-hop questions that require combining multiple facts. How do you fix it?
- Идеал: Switch to Agentic RAG (decompose into sub-queries, loop) and/or GraphRAG (traverse relations across chunks); measure, then fix the specific hop.
- Обязательные пункты:
  - Diagnose: which hop fails (retrieval vs generation).
  - Agentic loop: LLM plans sub-steps, runs tool per hop, combines.
  - Query decomposition + multi-query; merge with RRF.
  - GraphRAG when facts are connected entities across docs.
  - Reranker/hybrid to improve retrieval for each hop.
  - Test with multi-hop eval set; track solved hops.
- Частые ошибки: retraining model, не добавляя сложность retrieval.
- Красные флаги: «один retrieval с длинной чанкой справится».

### 40. Your enterprise RAG system returns contradictory answers from different source documents. How do you resolve conflicts?
- Идеал: Detect conflicts, decide precedence (recency/authority), and surface both with attribution to the user.
- Обязательные пункты:
  - Metadata: source authority/source_type/recency to rank doc priority.
  - Conflict detection: retrieve multiple docs, LLM flags inconsistent claims.
  - Defuse: prompt tells to prefer higher-priority source and state disagreement between sources with citations.
  - Never silently choose one; show sources so user decides.
  - Optional: human review/moderate conflicting facts.
- Частые ошибки: тихо усреднять/выбирать один ответ без источников.
- Красные флаги: «показывать только один ответ», «конфликт — это нормально без обработки».

### 41. Your RAG system returns outdated answers from an evolving knowledge base. How do you keep it current?
- Идеал: Focus on freshness: incrementally update index on doc change, add timestamps, filter by recency, prioritize fresh docs, and evictions for deleted content.
- Обязательные пункты:
  - Event-driven/incremental re-index on change; recency-aware retrieval (filter date).
  - Metadata on last-updated; boost/mark recent.
  - Monitor for stale chunks (doc removed/deleted) and re-embed.
  - Combine with web search for very fresh facts (CRAG fallback).
  - Shedule batch jobs + backfill; test freshness KPI per doc.
- Частые ошибки: полная переиндексация дорога; игнор удалённых.
- Красные флаги: «index раз в месяц достаточно», «старые данные норм».

### 42. Your RAG system struggles with PDF documents containing tables and layouts. How do you fix PDF parsing?
- Идеал: Use layout-aware PDF extraction: proper PDF-to-text engine (pdfplumber/Camelot/PyMuPDF), detect table regions, convert tables to HTML/markdown/JSON, handle multi-column pages and preserve structure before chunking.
- Обязательные пункты:
  - Naive extraction breaks rows/columns → garbled text.
  - Table tools: pdfplumber/Camelot extract tabular data; preserve header alignment.
  - Convert to markdown/JSON for faithful embedding; with heavy tables → SQL/text-to-SQL.
  - Vision models (VLM/OCR with layout) for scanned PDFs; ColPali visual retrieval for page images.
  - Multi-column: read order matters; OCR layout analysis; map to table structures.
  - Verify: extraction sanity check, table reconstruct, eval on table questions.
- Частые ошибки: считать, что raw PDF text достаточно для таблиц/сканов.
- Красные флаги: «текст — главный путь для PDF с таблицами», «OCR не нужен».
