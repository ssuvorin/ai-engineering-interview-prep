# Vector Databases and Embeddings — Answer Key (1-26)

### 1. What are embeddings in the context of AI engineering?
- Идеал: Embeddings are learned vector representations of data (text, images, audio) placed in an N-dimensional space so that similar items cluster together and dissimilar items are far apart.
- Обязательные пункты:
  - Created by feeding data through a trained embedding model; the model learns from patterns — words appearing in similar contexts tend to mean similar things (Firth, 1957).
  - Real embeddings have hundreds to thousands of dimensions (not 1D–3D as in simplified examples); a typical sentence embedding uses 384–3072 numbers.
  - Enable ML models to find similar objects without understanding meaning directly — just measure distance between vector points.
  - Use cases: document similarity, content-based recommendations, collaborative filtering (user+item embeddings), image retrieval, face recognition, LLMs, vector databases.
- Частые ошибки: Assuming embeddings are hand-crafted; confusing a vector with a model; ignoring that embeddings live in a learned space where only relative distance matters.
- Красные флаги: «embeddings are just one number per word», «embedding model gives meaning, not position».

### 2. How do embedding models convert text to vectors?
- Идеал: A trained neural model reads text and outputs a list of numbers (a vector) that encodes the text's meaning in a learned space — similar texts get similar vectors.
- Обязательные пункты:
  - Model learns from large corpora the distributional hypothesis: words in similar contexts have similar meaning; from this, it builds position vectors.
  - Text is tokenized, passed through an encoder (e.g., transformer), and the output CLS token or mean-pooled token embeddings form the sentence vector.
  - The resulting vector is a point in N-dimensional space; no individual dimension is interpretable — meaning is distributed across all dims.
  - Model name and version are part of the cache key; different models (or versions) produce different numbers for the same text — never interchangeable.
- Частые ошибки: Thinking the same text produces the same vector across models; ignoring that model upgrade changes all vectors.
- Красные флаги: «the model chooses what each number means», «I can use old embeddings with a new model».

### 3. What is Contrastive Learning, and how is it used to train embedding models?
- Идеал: A self-supervised technique that trains a model by pulling similar pairs (positives) close together and pushing dissimilar pairs (negatives) far apart in the embedding space, without any human labels.
- Обязательные пункты:
  - Positive pairs: two augmented views of the same image; two sentences with the same meaning; an image and its correct caption (for image-text models).
  - Negative pairs: any other image/sentence in the batch; all negatives are sampled implicitly.
  - Augmentation is critical — changes must preserve meaning (crop/rotate for images; paraphrases for text).
  - Loss functions: Contrastive Loss (pair, fixed margin), Triplet Loss (anchor/positive/negative, safety gap), InfoNCE (1 anchor + many negatives → classification-like; temperature controls sharpness).
  - Popular methods: SimCLR (large-batch negatives), MoCo (queue + momentum encoder for memory efficiency), CLIP (image-text contrastive, zero-shot via text-label embeddings), SigLIP (sigmoid pairwise loss, larger batches), DINO/BYOL/SimSiam (positive-only, stop-gradient/momentum/predictor to avoid collapse).
  - Use cases: image search, face recognition, recommendations, text similarity, multimodal models, medical imaging.
- Частые ошибки: Mixing up positive vs negative pairs; using wrong temperature (too high = soft, too low = overconfident); thinking CLIP needs labels (it doesn't — captions from the web are the labels).
- Красные флаги: «contrastive learning uses labeled data», «simCLR and CLIP are the same thing».

### 4. What is the difference between sparse and dense embeddings?
- Идеал: Sparse embeddings = high-dimensional, mostly-zero vectors where each dimension corresponds to a vocabulary term (e.g., BM25/TF-IDF), good for exact matching. Dense embeddings = fixed-low-dimensional, non-zero, learned vectors that capture meaning and generalize across synonyms.
- Обязательные пункты:
  - Sparse: interpretable (one dim = one term), zero-cost to compute, strong on exact words/codes/rare terms, weak on synonyms and rephrasing, no semantic generalization.
  - Dense: 384–1536 dims typically, every value non-zero, captures meaning and context, strong for semantic search, weak on exact codes and rare terms without fine-tuning.
  - Real-world: sparse = BM25 keyword search; dense = neural embedding models; neither is universally better.
  - Hybrid: combine both for best results — sparse catches exact terms, dense catches meaning.
- Частые ошибки: Choosing only sparse (misses meaning) or only dense (misses exact terms); thinking dense is always better because it is newer.
- Красные флаги: «sparse is just old/bad embeddings», «I only need dense».

### 5. Explain cosine similarity, dot product, and Euclidean distance for vector search.
- Идеал: Cosine similarity measures angle between vectors (ignores magnitude), value 1 = identical direction; dot product is sum of element-wise products (direction + magnitude); Euclidean distance measures straight-line gap, smaller = closer.
- Обязательные пункты:
  - Cosine similarity = (A·B) / (|A||B|); range [-1,1]; for normalized vectors it equals dot product; most popular for text — "same direction = same meaning".
  - Dot product = Σ(a_i × b_i); larger = more similar; affected by magnitude — use only when vectors are unit-normalized; then equals cosine.
  - Euclidean distance = √(Σ(a_i−b_i)²); smaller = closer; natural for image/spatial data; inverted for similarity (larger distance = less similar).
  - Practical text scores: unrelated sentences ~0.1–0.3 cosine; related ~0.7–0.9; rare to see scores near -1.
  - Table: cosine → angle → value near 1 = similar → text/semantic; dot → direction+size → larger = similar → normalized vectors; euclidean → gap → smaller = similar → image/spatial.
- Частые ошибки: Comparing raw cosine scores to thresholds meant for dot product; expecting scores near 0 to mean "no similarity" in practice.
- Красные флаги: «cosine of 0.3 means the texts are opposites».

### 6. What is a vector database, and how does it differ from a traditional database?
- Идеал: A vector database stores vectors (embeddings) alongside original data and metadata, enabling similarity search by meaning rather than exact word match. A traditional DB does exact keyword match and cannot understand semantic similarity.
- Обязательные пункты:
  - Stores (ID, vector, original data, metadata); vector carries meaning, data = what you show user, metadata = category/date/author for filtering.
  - Pre-filtering (filter first, then similarity search) is better than post-filtering (search then drop results) — avoids wasting work on items you will discard.
  - Traditional DB (SQL): "fruit that keeps the doctor away" → 0 results because no exact phrase; vector DB finds "apple a day" → correct.
  - Engines: Pinecone, Weaviate, Qdrant, Milvus, pgvector (PostgreSQL extension), Chroma.
  - Can also add vector search as an extension (pgvector) — the real question is whether the DB searches by meaning, not whether it is a special type.
- Частые ошибки: Assuming a DB with a vector index is automatically a full vector DB; ignoring pre/post-filtering implications.
- Красные флаги: «vector DB is just a key-value store».

### 7. How does Approximate Nearest Neighbor (ANN) search work?
- Идеал: ANN trades a small accuracy loss for a large speed gain by building an index in advance that lets queries skip most of the collection and only check promising regions.
- Обязательные пункты:
  - Brute force (exact) = O(N×D) comparisons per query — impossible at scale (100M × 1000 = 100B ops).
  - ANN builds a pre-computed index structure; at query time it jumps to the right neighborhood rather than scanning everything.
  - Quality measured by recall = % of true nearest neighbors found among returned results; 100% = exact, 95% = correct 95/100 times.
  - Speed vs recall tradeoff: more aggressive ANN = faster but lower recall; tune on your use case (nprobe, efSearch, m/efConstruction for HNSW).
  - Four families: KD-Tree (cuts space, suffers curse of dimensionality at high dims), LSH (hash to buckets, multiple tables for accuracy, memory-heavy), IVF (clusters with k-means, nprobe controls accuracy/speed), HNSW (layered graph, greedy hops, most popular).
  - Use cases: search engines, recommendation systems, face matching, RAG memory, AI chat long-term memory.
- Частые ошибки: Thinking ANN always returns the true nearest neighbor; confusing recall with precision.
- Красные флаги: «exact search is fine at scale», «ANN always finds the true nearest neighbor».

### 8. Compare HNSW, IVF, and flat indexes. How do you pick one, and what does recall@k cost in latency?
- Идеал: Flat = exact brute-force, 100% recall, O(N×D), only for tiny datasets. IVF = clustered, scales to billions, recall tunable via nprobe. HNSW = layered graph, best speed+accuracy by default, memory-heavy. Pick based on dataset size, recall needs, latency budget, and memory.
- Обязательные пункты:
  - Flat: exact, no approximation, slowest at scale, no build time overhead; use only when N < ~10k–100k or when exactness is required.
  - IVF (Inverted File Index): groups vectors into clusters via k-means; query compares query vector against cluster centers, then searches only inside the nearest nprobe clusters. Scales to billions; nprobe knob: more = higher recall, slower; fewer = faster, lower recall. Example from article: 100M vectors / 100 clusters = 1M/cluster; nprobe=3 → check 3M instead of 100M.
  - HNSW (Hierarchical Navigable Small World): layered graph; top layer has few points with long links (big jumps), bottom layer has all points with short hops. Greedy traversal: start top → big jumps → descend layer by layer → reach closest point at bottom. Excellent speed+accuracy but more memory than IVF and slower to build. Default in most modern vector DBs.
  - recall@k: fraction of true top-k results in returned set; higher recall requires opening more clusters (IVF nprobe), larger efSearch (HNSW), or more links per node — all increase latency linearly.
  - Practical: start with HNSW (good default); drop to IVF if memory is the bottleneck or you need billion-scale; flat only for <100k and exact requirements.
- Частые ошибки: Setting nprobe too low and accepting recall loss; thinking HNSW memory cost is fixed — it grows with M×N.
- Красные флаги: «HNSW is always best regardless of data size», «nprobe=1 is fine for high recall».

### 9. How does an Embedding Cache work?
- Идеал: Computed embeddings are stored in a cache keyed by a hash of (text + model name + version). On subsequent identical requests the cached embedding is returned instantly without calling the embedding model, saving cost and latency.
- Обязательные пункты:
  - Computing embeddings costs money and time; repeated identical texts (popular queries, re-ingestion of unchanged documents) recompute the same embedding wastefully.
  - Cache key = hash of (input text + model name + model version). This ensures different models (or versions) never collide — the new model version gets its own cache space.
  - Cache hit: key found → return saved embedding immediately, no model call.
  - Cache miss: key not found → call embedding model → store result under key → return.
  - Eviction: LRU (Least Recently Used — throw out longest-unused) when full; TTL (Time To Live — expire after fixed duration) to handle model/data changes.
  - Cache location: in-memory (Redis, fastest, limited size, lost on restart) vs on-disk (slower, large capacity, persists); often both layers.
  - Does NOT change search quality — cached embeddings are identical to freshly computed ones.
  - Semantic cache is different: it reuses a past LLM answer for a semantically similar query, skipping both embedding AND generation.
  - Use cases: RAG (re-ingestion + popular queries), semantic search.
- Частые ошибки: Using just the raw text as key (fails when same text goes to two model versions); forgetting TTL causes stale embeddings after model upgrades.
- Красные флаги: «cache changes the embedding values», «same model version always produces same cache key without the version in the key».

### 10. How do you choose the right embedding model for your use case?
- Идеал: Evaluate candidate models on a representative sample of your own data (not just leaderboards), balancing quality, dimension count, latency, cost, and language coverage.
- Обязательные пункты:
  - Match domain and language: general-purpose models (OpenAI text-embedding-3-small/large) vs domain-specific or multilingual models (BGE, E5, GTE, multilingual-E5).
  - Dimension count: lower dims = less storage and faster similarity search but potentially lower quality; higher dims = more expressive but costlier. Choose based on your retrieval quality vs. performance tradeoff.
  - Benchmark on YOUR data: run MTEB, BEIR, or a custom golden query set against candidate models and measure recall@k / nDCG@k.
  - Input length: ensure max tokens > your chunk size; handle truncation for long documents.
  - Latency and cost: API models (metered per 1K tokens) vs open-source models (self-hosted, GPU required); self-hosting for high-volume ingestion.
  - Fine-tuning: if pre-trained models perform poorly on your jargon/entities, fine-tune on domain-relevant query-passage pairs using contrastive learning.
  - Matryoshka-compatible models allow truncating dimensions without retraining — useful for cheap first-pass retrieval with full vectors for re-ranking.
- Частые ошибки: Picking based on leaderboard without validating on domain data; ignoring dimension count's effect on memory cost.
- Красные флаги: «I will use the most popular model regardless of my data», «more dimensions is always better».

### 11. What is embedding dimensionality, and how does it affect performance and cost?
- Идеал: Dimensionality is the number of floating-point values in each embedding vector; higher dims store richer meaning but linearly increase storage, indexing time, and search latency.
- Обязательные пункты:
  - Typical range: 384–3072 dims for text; lower (128–512) for images/audio; dimensions are NOT interpretable individually — meaning is distributed.
  - Memory: bytes/vector = dims × bytes_per_float (4 for FP32, 2 for FP16, 1 for int8). Example: 128-dim FP32 = 512 bytes; 128-dim int8 = 128 bytes; 4× saving via int8 quantization.
  - ANN indexing cost grows with dims (curse of dimensionality); HNSW/IVF both degrade at very high dims — balance quality vs dimensionality.
  - Encoding latency and cost: larger vectors cost more to compute (more params to run); more dims = higher API token cost if metered per token.
  - Matryoshka embeddings: trained to preserve meaning even when truncated to fewer dims — enables cheap retrieval with full vectors for re-ranking.
  - Choosing: start with the model's default (e.g., 768 or 1536); reduce only if memory/latency demands it, validating quality impact.
- Частые ошибки: Picking the highest possible dims for accuracy without measuring memory impact; ignoring that doubling dims roughly doubles storage and indexing cost.
- Красные флаги: «I'll use 4096 dims because bigger is better», «I don't need to worry about memory».

### 12. How do you handle embedding drift when the embedding model is updated?
- Идеал: A model upgrade produces a new embedding space that is incompatible with old vectors; the only reliable fix is re-embedding all stored data under the new model before switching live queries.
- Обязательные пункты:
  - Embedding vectors from different models live in different spaces — cross-space similarity is meaningless; you cannot directly compare an old vector to a new one.
  - Migration plan: keep the old index serving live queries; in parallel, re-embed all documents with the new model; build a new index; validate quality on a golden query set; cut over atomically.
  - Dual-write during transition: during the switchover window, both old and new embeddings are computed and stored; queries can be A/B tested.
  - Cache keys already include model name+version — old cached embeddings expire via TTL or are evicted; no stale collisions.
  - After cutover, old index and embeddings are decommissioned.
  - Partial re-embedding (only changed documents) works for minor model tweaks if the new model is backward-compatible; for breaking changes, full re-index is required.
- Частые ошибки: Mixing old and new embeddings in the same index (corrupts similarity scores); thinking vectors from different models can be compared.
- Красные флаги: «I'll just update the model and the old vectors will still work».

### 13. What are multi-modal embeddings, and how are they generated?
- Идеал: Multi-modal embeddings place different data types (text, image, audio) into the same shared vector space so they can be directly compared; generated by per-modality encoders trained jointly so matching pairs land close and non-matching pairs are pushed apart.
- Обязательные пункты:
  - Core recipe: encode each modality with its own encoder (text encoder, image encoder/ViT, audio encoder) → align all outputs into a shared embedding space via contrastive training → the shared space is what enables cross-modal comparison.
  - Three patterns: Multimodal Understanding (many inputs → one output, e.g. GPT-4V/Gemini describing an image); Cross-Modal Generation (input in one modality → output in another, e.g. DALL-E/Midjourney text→image, Whisper audio→text, Sora text→video); Cross-Modal Alignment (shared space itself is the product, e.g. CLIP text↔image search).
  - CLIP: Contrastive Language-Image Pre-training; trains image + text encoders on millions of web image-caption pairs; negative = mismatched caption; zero-shot classification possible — computes similarity between image and text labels like "a photo of a dog" and picks the highest.
  - Models: GPT-4V/GPT-4o, Gemini, Claude (vision), CLIP, DALL-E, Midjourney, Whisper, Sora, Veo.
  - Use cases: VQA, document understanding (PDF with tables+charts), medical imaging, self-driving cars (fusion of camera/radar/LiDAR), accessibility, content creation, customer support, education, mobile translation.
  - Caveats: multimodal ≠ just text+image (audio/video/sensor/3D count); more modalities is not always better (adds noise/latency); cost is higher than unimodal; evaluate per modality; bad pairings (wrong captions) degrade the shared space; check bias per modality.
- Частые ошибки: Claiming "just text+image" covers multimodal; assuming one model fits every modality combination; ignoring shared-space alignment quality.
- Красные флаги: «add more modalities always improves results», «CLIP is a unimodal image model».

### 14. How do you index and query multi-tenant data in a vector database?
- Идеал: Isolate each tenant either with its own index partition or via a mandatory pre-filter on a tenant_id in the metadata.
- Обязательные пункты:
  - Option A: per-tenant index/namespace — clean isolation, per-tenant tuning, but duplicate infrastructure for many small tenants.
  - Option B: shared index + tenant_id metadata filter — one index serves all, filter on tenant_id (pre-filtering) ensures each query only searches that tenant's vectors. Most common for many tenants.
  - Pre-filtering by tenant_id is critical: without it ANN merges tenants' vectors and returns other tenants' content — a privacy leak.
  - Post-filtering is a fallback only when pre-filtering is unavailable; it can return fewer candidates than needed.
  - Tenant ID also in the metadata for re-ranking and dedupe.
  - Watch scaling: a shared index must be rebalanced; per-tenant indexes give bounded recall but many small indexes cost memory.
- Частые ошибки: Skip the tenant filter entirely (cross-tenant leakage); query all tenants just to filter later.
- Красные флаги: «I can just filter tenant ID after search», «one big shared index with no filter is fine».

### 15. What is quantization of embeddings, and how does it reduce storage costs?
- Идеал: Quantization reduces numeric precision (or compresses vectors with codebooks) so each vector takes far fewer bytes, cutting storage and memory — at the cost of some accuracy.
- Обязательные пункты:
  - Memory math (from article): 128 dims × 4 bytes FP32 = 512 bytes/vector. Reduce precision: FP16 → 256 bytes, int8 → 128 bytes, binary → 16 bytes — 4–32× savings.
  - Product Quantization (PQ): split vector into sub-vectors, assign each to a nearest centroid from a codebook, store only short codes → huge compression (e.g., 64 dims→8 bytes); combine with IVF/PQ index (FAISS IndexIVFPQ).
  - Scalar quantization: map each dim to range [0,255] (int8) after computing global min/max.
  - Trade-off: aggressive PQ/int8 lowers recall; keep a residual (original vector) for re-ranking or stay with FP16 when accuracy matters (like reference's binary approach).
  - Benefit: fit more vectors in RAM → fewer shards, lower cost, faster scans.
- Частые ошибки: Using FP32 everywhere; quantizing blindly and silently losing recall; forgetting re-ranking after PQ.
- Красные флаги: «I can quantize everything to int8 with no quality loss», «PQ is only about speed, not memory».

### 16. How do you benchmark and evaluate embedding model quality?
- Идеал: Evaluate the embedding model on your own retrieval task with labeled query–relevant pairs, measuring ranking metrics against the true nearest neighbours; use public benchmarks only as a rough signal.
- Обязательные пункты:
  - Build a golden test set: queries + their ground-truth relevant items.
  - Metrics: recall@k (fraction of true top-k found), nDCG@k, MRR (reciprocal rank of first hit), precision@k; for ANN also measure latency.
  - Include hard negatives: items that look similar but are actually irrelevant.
  - Compare candidate models against the same test set (or via MTEB/BEIR); a good model must rank true positives highest.
  - Test on your actual data distribution, not just generic passages (ratio of domain terms).
  - Validate before vs after fine-tuning — you need a task that plausibly catches a regression.
  - Recall@k is the key SLA: recall@10 = % of true top-10 that ANN returns.
- Частые ошибки: Judging by cosine scores alone without labelled ground truth; comparing models on different datasets.
- Красные флаги: «the model is great because all scores are above 0.8», «I don't need ground truth, eyeballing is enough».

### 17. What is the role of metadata in vector databases?
- Идеал: Metadata (category, date, author, price, tenant_id, etc.) lets you filter and scope the similarity search so you only surface items that also satisfy business conditions.
- Обязательные пункты:
  - Vector DB stores (ID, vector, data, metadata) per item; metadata drives filtering.
  - Pre-filtering (apply metadata filter first, then run similarity search only on remaining vectors) is preferred — no wasted search.
  - Post-filtering (search first across everything, then drop non-matching) risks returning results that fail the filter or, worse, retrieving too few candidates.
  - Enables: tenant isolation, content scoping ("only health category from 2024"), exact-filter + semantic query combined.
- Частые ошибки: Filtering after ANN without understanding it is less efficient and can drop the true matches; under-specifying filters.
- Красные флаги: «metadata is irrelevant to vector search».

### 18. How do you handle large-scale vector search with billions of vectors?
- Идеал: Use ANN (IVF/HNSW) with quantization, shard the index across multiple nodes, and re-rank top candidates in a second stage to keep latency low at billion scale.
- Обязательные пункты:
  - Brute force is unsustainable: 1B vectors × 1000 dims = 1,000B operations per query (from article context 100M × 1000 dims = 100B calcs).
  - IVF: divide into clusters, each search compares query against ~nprobe clusters' centers then only members of those clusters — explicitly scales to billions (nprobe = accuracy/speed knob).
  - HNSW: hierarchical graph also supports billions, but memory-bound; use PQ to compress.
  - Distributed: shard vectors across machines (by cluster), parallel query, reduce/merge — e.g., Milvus, Weaviate, Qdrant, FAISS with distributed GPU.
  - Two-stage: ANN returns candidates → re-rank those few with full-precision vectors (PQ residual / full vector).
  - GPU acceleration: FAISS/GALAXIA etc. index on GPU; HNSW over billions on multiple nodes.
- Частые ошибки: Trying to keep everything in one node RAM; using flat search; ignoring sharding.
- Красные флаги: «I'll just add more RAM», «flat index is fine for a billion vectors».

### 19. What is hybrid search (combining keyword search with vector search)?
- Идеал: Run both a lexical (BM25/keyword) and a semantic (vector/embedding) search, then fuse the two ranked lists with RRF (or weighted normalized scores) — so exact codes and rephrased meanings both survive.
- Обязательные пункты:
  - Keyword search (lexical) = exact tokens (BM25) — best for codes, rare terms, exact phrases, single words.
  - Semantic search (vector/dense) = meaning-based: solves synonyms and rephrasing ("send shoes back" vs "return your shoes").
  - First failure mode: raw scores are on different scales (BM25 ~9.1 vs cosine 0.88); adding them directly biases.
  - Fusion: RRF — score = Σ 1/(k + rank) over the two lists; uses rank, not raw score; a doc high in both lists wins; robust and simple. Optionally weight one list.
  - Alternative: normalize each score to [0,1], then weighted sum with tunable weights.
  - RAG dependency: retrieval quality decides answer quality — hybrid gives stronger recall.
- Частые ошибки: Just dropping one method; naively adding unnormalized scores.
- Красные флаги: «BM25 and cosine scores are directly comparable», «I use only dense vectors, that's enough for exact codes».

### 20. How do you fine-tune an embedding model for a specific domain?
- Идеал: Use contrastive learning (per reference) to fine-tune an embedding model on domain-specific query–passage pairs so it matches real domain content.
- Обязательные пункты:
  - Prepare dataset of (anchor, positive, negative) triplets from your domain: positive = the relevant answer, negative = a passage that looks related but is not the answer.
  - Train with InfoNCE, Triplet, or Contrastive Loss to pull positive embeddings close and push negatives apart.
  - The reference's search-model shape: query is paired with a passage that answers it (positive) and one that does not (negative).
  - Keep augmentation meaning-preserving (paraphrases for text).
  - Evaluate on a held-out test set of domain queries before/after fine-tuning (recall@k).
  - When to fine-tune: if the base model is strong in general but weak on your jargon/custom entities.
- Частые ошибки: Fine-tuning with generic data; not including hard negatives (a model that only learns "easy" pairs overfits).
- Красные флаги: «fine-tuning means I re-train from scratch», «hard negatives are a nice-to-have».

### 21. Your vector database for RAG is consuming too much memory. How do you reduce it?
- Идеал: The fix, cause-to-solution: too much memory → too much data held full-precision → quantize, lower dims, and change the index so fewer bytes per vector resident, without dropping recall.
- Обязательные пункты:
  - Quantize: FP32 → FP16 (2×), int8 (4×), or Product Quantization (PQ: split vector into codebook codes) for the index; keep full vectors only for re-ranking.
  - Scale down vectors: reduce dimensionality (Matryoshka truncation / smaller embedding model).
  - Change index: HNSW has high memory (graph); IVF with PQ uses less; a flat index on disk doesn't keep all vectors in RAM.
  - Reduce vector count: better chunking, dedupe near-duplicate chunks.
  - Re-measure recall@k against baseline after quantization to confirm trade-off.
- Частые ошибки: Just upgrading RAM instead of fixing pressure; assuming full precision is required.
- Красные флаги: «I'll add another server», «all RAG data must be kept full-precision».

### 22. Your vector database cannot scale to millions of embeddings. How do you fix the bottleneck?
- Идеал: If it cannot scale beyond millions, replace brute-force with ANN (IVF/HNSW), and horizontally shard across nodes — exactly the approach the reference sizes for billions.
- Обязательные пункты:
  - Cause: brute-force similarity = O(N×D) per query — fine for thousands, breaks at millions and beyond.
  - Fix: IVF with cluster centers + nprobe, or HNSW hierarchical graph; recall tunable.
  - Quantize vectors (PQ/residual) to shrink per-vector footprint; improves index build and search.
  - Sharded architecture: distribute the index partition across machines, queryers fan out, aggregator merges — this is what makes billion-scale feasible.
  - Use a managed/embedded solution that can shard: Milvus, Weaviate, Qdrant, FAISS+distributed.
- Частые ошибки: Upgrading to a bigger single machine instead of sharding; skipping ANN.
- Красные флаги: «I'll buy a bigger machine», «a single node can handle billions of vectors fine».

### 23. Your new embedding model has different dimensions from the existing vectors in production. How do you handle the mismatch?
- Идеал: You cannot search across mismatched dimensions and you cannot mix model spaces — the fix is to rebuild the index with the new model's embeddings before, not after, pointing queries at it.
- Обязательные пункты:
  - Dimensions are an output of the model; different dims means the spaces are incompatible — dot/cosine across two differently-sized vectors are undefined.
  - Path: freeze the current model+index, write a batch job to re-embed the full corpus with the new model (new index), validate on a golden query set, then cut over queries.
  - Alternatively: if the mismatch is small and you must avoid re-indexing, use a trained linear projection — but it is lossy and usually worse than re-embedding.
  - Keep only one generation live at a time; never run production against a mixed index.
- Частые ошибки: Padding the shorter vector to fit dimensionality; querying the new model against the old index for some fraction of traffic.
- Красные флаги: «I'll just pad the vectors», «old and new vectors are compatible because they're both 'embeddings'».

### 24. Your vector search returns irrelevant results despite high similarity scores. How do you fix it?
- Идеал: Diagnose along three axes — embeddings, ANN parameters, retrieval setup; a high similarity score means nothing if the space is wrong.
- Обязательные пункты:
  - Likely causes: model misaligned with domain/data; vectors not normalized and wrong metric (Euclidean vs cosine); too few clusters/top-k from ANN; no metadata filtering; index stale.
  - Symptoms from reference: unrelated texts still score >0.3; so high scores alone prove nothing — compare relative rankings.
  - Tools: A/B against a golden set, inspect top-k with RECALL, hybrid (+keyword), re-rank with cross-encoder.
  - Fix: tune embedding model (fine-tune or switch), normalize embeddings, tune nprobe/efSearch, refine chunking, add metadata filters.
- Частые ошибки: Chasing high scores instead of fixing the model; rejecting results after a threshold.
- Красные флаги: «high similarity = correct answers», «0.8 is always good».

### 25. You deployed a new embedding model, and search quality crashed overnight. How do you handle embedding drift?
- Идеал: This is embedding drift — the new model produced a new space; old stored vectors are now incompatible. Roll back immediately and re-index.
- Обязательные пункты:
  - Cause: you swapped the live embedding model but kept the old vectors — or you updated the model without rebuilding the index; queries are now compared in mismatched spaces.
  - Immediate: roll back to the previous model+old index while it still exists.
  - Permanent fix: run a full re-embedding job with the new model, build a fresh index, validate on a golden set, then switch + decommission old index.
  - Prevention: version every model; pipeline computes embeddings once, stores, and versioned colocation; use pre/post-filtering and re-rank for stability.
- Частые ошибки: Only re-embedding queries, not corpus; assuming the new model's output is backward compatible.
- Красные флаги: «deploy new model first, re-index later», «it must be a problem with the data, not the model».

### 26. Your semantic search fails for short queries. How do you improve it?
- Идеал: The cause is sparse lexical signal: short queries don't give the embedding much to match. Improve with query expansion and hybrid retrieval.
- Обязательные пункты:
  - Add query expansion: rewrite the short query into longer paraphrases before embedding.
  - Use hybrid search: combine vector with BM25/keyword, so exact tokens still match; RRF fusion.
  - Retrieve candidates with ANN, then re-rank the top candidates with a cross-encoder (query-aware relevance).
  - Lucene-style token analysis on the short query: synonyms, stemming, normalization.
  - If still weak, index metadata (e.g., content type) to narrow candidates.
- Частые ошибки: Over-tuning scores for a short query instead of expanding the query and using hybrid.
- Красные флаги: «semantic search obviously fails for short queries — must abandon it», «long queries are the answer to everything».
