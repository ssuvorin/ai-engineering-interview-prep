# AI Infrastructure and Scalability — Answer Key (1-35)

### 1. How do you improve inference speed in production LLM deployments?
- Идеал: apply a stack of GPU- and serving-level optimizations so users get responses fast and hardware is well-utilized.
- Обязательные пункты:
  - KV cache: store past keys/values once, reuse instead of recomputing (default).
  - Paged attention: manage KV cache memory efficiently → serve more concurrent users.
  - Flash attention: chunked matrix math via tiling + online softmax, keeps math units busy.
  - Grouped query attention (GQA): share K/V across query heads — balance of accuracy and memory.
  - Speculative decoding: small draft model verifies in parallel.
  - Continuous batching: add requests the moment one finishes — GPU never idle.
  - Prompt caching: reuse cached KV for repeated prompt prefixes.
  - Also: quantization, prefill/decode disaggregation.
- Частые ошибки: фокусироваться только на одной технике; игнорировать decode (memory-bound) как главный bottleneck.
- Красные флаги: «ускорение = только переписать модель», «KV cache главный, а остальное неважно».

### 2. LLM optimization techniques
- Идеал: list the standard efficiency techniques used to deploy LLMs without much quality loss.
- Обязательные пункты:
  - Quantization: reduce weight precision (32→8/4-bit) → smaller + faster, little quality impact.
  - Pruning: remove weights/neurons that contribute little → lighter, faster.
  - Knowledge distillation: train a smaller student to mimic a larger teacher.
  - KV cache: store key/value pairs so earlier tokens aren't recomputed → lower latency; plus Paged Attention.
  - Speculative decoding: small model drafts tokens, big model verifies in parallel.
- Частые ошибки: не упомянуть trade-off (каждая техника что-то жертвует); путать distillation с quantization.
- Красные флаги: «оптимизации бесплатны», «pruning = quantization».

### 3. How do you select GPUs for LLM inference?
- Идеал: choose GPUs by four core specs that determine whether a model runs and how fast.
- Обязательные пункты:
  - VRAM: model fits — weights at given precision (e.g. 70B fp16 ≈ 140 GB) + KV cache + activations + runtime overhead.
  - Memory bandwidth: main driver of decode token/s (decode is memory-bound — stream all weights per token).
  - Compute (FLOPS) via Tensor Cores: matters mostly for prefill (compute-bound).
  - Lower-precision GEMM support (FP16/BF16/INT8) and NVLink for multi-GPU.
  - Prefer single-GPU fit if possible; else multiple GPUs + parallelism.
- Частые ошибки: смотреть только на VRAM и игнорировать bandwidth (key for decode); забыть, что KV cache растёт.
- Красные флаги: «нужно только больше VRAM», «FP32 обязателен для inference».

### 4. How does a GPU work for Deep Learning?
- Идеал: GPU does thousands of small simple multiply-add operations in parallel, which is exactly what matrix multiplication (core of DL) needs.
- Обязательные пункты:
  - CPU = few powerful serial cores; GPU = thousands of simple parallel cores.
  - DL is mostly matrix multiplication = millions of independent multiply-adds.
  - VRAM holds weights+data (must fit); memory bandwidth feeds cores so they don't idle.
  - Tensor Cores do matrix math faster at lower precision (FP16/BF16/INT8).
  - CUDA + cuDNN let high-level code use this; NVLink joins multiple GPUs.
  - Training = forward + backward (heavy); inference = forward only (lighter).
- Частые ошибки: думать, что GPU cores «умные» как CPU; игнорировать bandwidth/VRAM.
- Красные флаги: «GPU подходит для любых задач», «модель можно запустить без VRAM».

### 5. How do CUDA Kernels work?
- Идеал: a CUDA kernel is one function written for a single thread that the GPU executes across thousands of threads in parallel, each handling its own data.
- Обязательные пункты:
  - CUDA = NVIDIA platform for writing GPU code (C/C++/Python) for general compute.
  - Kernel = `__global__` function on GPU; launched `kernel<<<blocks,threadsPerBlock>>>(args)`.
  - Organization: thread (single worker) → block (group, share memory, «256 threads») → grid (all blocks). No loop — each thread handles its own index: `i = blockIdx.x * blockDim.x + threadIdx.x`.
  - Host (CPU/RAM) vs Device (GPU/VRAM): copy data H2D, launch kernel, copy result D2H, free memory (cudaMalloc/cudaMemcpy/cudaFree).
  - GPU runs blocks across Streaming Multiprocessors; threads grouped into warps of 32 (same instruction per warp). Indexed by .x/.y/.z dims.
- Частые ошибки: писать цикл внутри ядра; забыть про host/devide copy; путать threadIdx/blockIdx.
- Красные флаги: «kernel — функция только для одной нити, без параллелизма», «CUDA только для графики».

### 6. How does a Google TPU work?
- Идеал: TPU is a Google ASIC built for matrix multiplication (the core of ML) using a Systolic Array, trading flexibility for speed/power efficiency.
- Обязательные пункты:
  - Hardware: Matrix Multiply Unit (MXU) containing a systolic array — a grid of tiny multiply-accumulate (MAC) calculators (e.g. 128×128).
  - Data flow: weights stay in place in the grid; inputs flow right, running totals flow down, results fall out the bottom — calculators pass results to neighbors, avoiding repeated memory trips.
  - Built for ML only: less flexible than CPU/GPU → faster and more power-efficient; lower-precision math.
  - Driven by a host computer; used by Google Search, Translate, Photos, voice; trains large LLMs; Edge TPU for on-device.
- Частые ошибки: думать, что TPU — универсальный чип; не упомянуть systolic array/отказ от гибкости.
- Красные флаги: «TPU гибче GPU», «TPU = просто большой GPU».

### 7. How does an LPU work?
- Идеал: LPU (Groq) is a specialist chip for inference of already-trained LLMs, built around the fact that generation is memory-bound, not math-bound.
- Обязательные пункты:
  - LLM generates one token at a time (a serial chain); to produce one token it must read all weights → memory-bound.
  - Idea 1: keep weights on-chip in SRAM (small, fast, ~230 MB) instead of HBM → far higher bandwidth (~80 TB/s vs ~3 TB/s), per-token latency drops (~26×). One chip can't hold a big model → split layers across many chips, moving only small activations between chips.
  - Idea 2: deterministic execution — the compiler plans every cycle in advance, no caches/schedulers → predictable timing, more compute+SRAM.
  - Idea 3: synchronized network with no handshake/wait — compiler-scheduled data movement between chips → no latency jitter.
  - Trade-off: fastest single-user token/s (no batching needed), high throughput; but many chips needed, less suited to small/training workloads.
- Частые ошибки: думать, что LPU ускоряет за счёт большего числа ядер; не сказать про memory-bound и SRAM.
- Красные флаги: «LPU быстрее всех» без пояснения цены (мало памяти на чип, много чипов), «LPU для обучения моделей».

### 8. Estimate the GPU memory needed to serve a 70B model (weights, KV cache, activations). Does it fit on a single 80 GB GPU? But it fits on 2x80GB.
- Идеал: total memory ≈ weights + KV cache + activations + overhead; compute it and conclude it does not fit on one 80 GB GPU.
- Обязательные пункты:
  - Weights: 70B params × 2 bytes (bf16/fp16) = 140 GB. (INT8 → 70 GB; INT4 → ~35 GB.)
  - KV cache: grows with batch, layers, heads, seq len. Rough, real (e.g. Llama-70B) estimate: ~8–16 GB per concurrent request at 4096 tokens. So 1 req ≈ 8–16 GB → with weights 140 GB total needs >150 GB for a single request alone.
  - Activations: small sample in practice but add a few GB; plus framework CUDA context (~1-2 GB).
  - An 80 GB GPU cannot hold 140 GB of weights + KV cache + activations → need 2×80 GB (tensor parallel) or quantization or sharding.
- Частые ошибки: считать только веса в fp16 (140 GB) и называть 80 GB достаточным; забывать KV cache и контекст CUDA.
- Красные флаги: «70B помещается в 80 GB», не знать, что параметр ≠ байт (зависит от precision).

### 9. Do the roofline math: how many tokens/sec can one H100 produce for a 70B model at batch size 1?
- Идеал: decode is memory-bound; tokens/s ≈ memory bandwidth ÷ weights per token.
- Обязательные пункты:
  - 70B params × 2 bytes (bf16) = 140 GB of weights to stream per token.
  - H100 HBM bandwidth ≈ 3 TB/s.
  - tokens/s = 3 TB/s ÷ 140 GB = 3000/140 ≈ 21 tok/s (batch=1, perfect conditions); that is the roofline ceiling, lower in practice.
  - Batch increases throughput: more tokens with the one weight load → e.g. ~21 × batch tokens/s aggregate (compute may then cap it).
- Частые ошибки: вместо bandwidth использовать FLOPS; забыть ×2 байта на вес (bf16).
- Красные флаги: «H100 даёт 210 tok/s для 70B batch-1» (ошибка в 2 байта), «70B — чисто вычислительная задача».
### 10. What is model parallelism vs data parallelism in distributed training?
- Идеал: distinguish the two by what is split — data vs model.
- Обязательные пункты:
  - Data parallelism: full copy of the model on every GPU; split the training data; GPUs train on their own pieces, then sync gradients/weights. Scales throughput on small models.
  - Model parallelism: model too big to fit one GPU → cut the model into parts across GPUs; each GPU holds and runs its part, passing results between GPUs (enables models bigger than any single GPU's VRAM).
  - Both need fast interconnect (NVLink) to sync/share efficiently.
  - TP/PP are specific forms of model parallelism.
- Частые ошибки: путать what is sharded (data vs weights); думать, что data parallelism экономит память.
- Красные флаги: «data parallelism нужен для больших моделей», «model parallelism синхронизирует градиенты».

### 11. What is tensor parallelism, and how does it help serve large models?
- Идеал: tensor parallelism splits each layer's weight matrices across GPUs; all GPUs compute one layer's output collaboratively.
- Обязательные пункты:
  - Split weight tensor (e.g. columns) across GPU ranks; each rank computes a partial result, then all-reduce/sync to reconstruct the layer output.
  - Reduces per-GPU memory (fits large models) and per-layer compute; increase batch size on the split; but adds communication (all-reduce) between GPUs per layer → needs high-speed interconnect (NVLink/NVSwitch).
  - Training + inference use it; e.g. 2×80 GB for a 140 GB bf16 model.
- Частые ошибки: думать, что TP не нуждается в связи; не отличать TP от DP.
- Красные флаги: «TP — это просто несколько экземпляров модели» (это DP), не упоминать all-reduce.

### 12. What is pipeline parallelism?
- Идеал: split the model by layers; GPU1 runs first layers, GPU2 next, ... data flows like an assembly line.
- Обязательные пункты:
  - Model divided along depth (stage per GPU) — each stage holds a whole contiguous group of layers.
  - Activations (only a few KB/token) travel between stages, weights stay local → fits huge models.
  - Bubble problem: pipeline has to be filled/drained (flush) — idle bubbles unless micro-batching overlap; less communication than TP but higher per-request latency is possible.
  - Micro-batching/overlapping reduces the bubble/idle time.
- Частые ошибки: путать PP с TP (режет по слоям, а не внутри слоя); не упомянуть bubble/idle.
- Красные флаги: «pipeline parallelism = ускорение одного запроса», «нет никакого idle».

### 13. How does continuous batching improve LLM inference throughput?
- Идеал: instead of waiting for the whole static batch, the server re-slots finished requests immediately with new ones — GPU never idles.
- Обязательные пункты:
  - Static batching: batch of N requests runs until the slowest finishes; short requests' slots idle wasted, new users wait for full batch.
  - Continuous batching: at the token level, after each decode step swap finished requests for queued ones; run prefill for the new request, then continue decode.
  - Result: higher GPU utilization and throughput, lower per-user wait, better latency for stragglers.
  - Real needs Paged Attention for KV cache memory of many interleaved requests.
- Частые ошибки: думать, что static batching — норма; путать между «batch per token» vs «per request».
- Красные флаги: «continuous batching = только более длинные батчи», «не описывает replace-as-finish».

### 14. What is speculative decoding, and how does it speed up inference?
- Идеал: a small draft model guesses the next N tokens cheaply; the big target model verifies all of them in one parallel forward pass — more tokens per big-model run, same output distribution.
- Обязательные пункты:
  - Draft model generates K draft tokens autoregressively (fast, small); target model checks them all in a single run (generation sequential, verification parallel).
  - Accept tokens until first rejection — output is exactly what target would produce (lossless); bonus token if all accepted.
  - Rejection sampling: accept if p(x) >= q(x) else with probability p/q — guarantees distribution matches target.
  - Typically 2-3× speedup (up to 3-4× with better drafts).
  - Trade-offs: need a matched draft model (same vocabulary), extra memory/compute for it, must update draft with target.
- Частые ошибки: думать, что качество падает; не знать rejection sampling; draft-модель = «замена» цели.
- Красные флаги: «draft-модель ускоряет, но меняет ответы», «verify нельзя делать параллельно».

### 15. How does Medusa (multi-head speculative decoding) work?
- Идеал: add a few small extra heads to the model itself to guess several future tokens in one pass — no separate draft model.
- Обязательные пункты:
  - Original head predicts token 1; Medusa heads 1..k predict tokens 2..k+1 from the same internal state in ONE forward pass.
  - Base model frozen; only tiny heads trained (cheap/fast) → no separate draft model, less memory/complexity.
  - Each head proposes top candidates → candidate continuations form a tree; tree attention mask verifies all paths in one pass; keep the longest path the model agrees with → output identical to normal generation.
  - Speedup = average accepted tokens per pass, ~2-3×.
  - Inspired EAGLE and multi-token prediction (DeepSeek-V3); tree verification used in TensorRT-LLM.
- Частые ошибки: думать, что меняет ответы модели; путать с классическим draft-model speculate.
- Красные флаги: «Medusa требует вторую модель», «heads обучают всю модель заново».

### 16. How does EAGLE (feature-level speculative decoding) work?
- Идеал: draft at the level of the model's internal features (hidden states) instead of tokens — features are smoother and more predictable than sampled tokens.
- Обязательные пункты:
  - Token-level drafting is noisy: next token is sampled from a distribution → many rejected.
  - EAGLE trains a small draft network that autoregresses over the second-to-last-layer feature (hidden state); then maps features to tokens.
  - Resolves feature uncertainty by feeding back the previously sampled token along with features → accurate drafts.
  - Speedup = average accepted tokens per pass; higher acceptance → ~3-4× (lossless).
  - EAGLE-2: dynamic, context-aware draft trees; used in vLLM, SGLang, TensorRT-LLM; inspired by Medusa, extended in EAGLE-3.
- Частые ошибки: путать с Medusa (heads predict tokens); думать, что EAGLE требует вторую полную модель.
- Красные флаги: «EAGLE предсказывает токены, а не фичи», «EAGLE меняет выдачу модели».

### 17. What is N-gram Speculation in LLMs, and how does it speed up generation?
- Идеал: a form of speculative decoding where the draft comes from matching n-grams in the existing text (prompt + generated tokens), not a draft model — aka Prompt Lookup Decoding.
- Обязательные пункты:
  - Take the last n tokens as key; search earlier text for the same n-gram; copy the next k tokens after the match as the draft.
  - Big model verifies the draft in one forward pass: accept until first mismatch, then take the model's own correction. Output identical — lossless.
  - No extra model → no second-model memory, no vocab-matching problem, no per-token draft cost.
  - Works where the answer copies big chunks of input (summarize, bug fix, doc Q&A); weak for creative text; a missed draft still yields >=1 token, so no loss.
  - Real implementations try multiple n (3,2,1) and search from the end (recent text repeats more).
- Частые ошибки: думать, что n-gram speculation требует draft-модель.
- Красные флаги: «это изменяет ответ», «n-gram = языковая модель».

### 18. What is KV cache, and how do you manage memory for it?
- Идеал: KV cache stores keys/values of every processed token so decode never recomputes attention for the whole sequence — speed with memory trade-off.
- Обязательные пункты:
  - During prefill compute and store K,V for all prompt tokens; during decode compute K,V,Q only for the new token, read old K,V from cache, append.
  - Reduces work from ~O(n^2) recompute to O(n); cache grows by one entry per generated token and per user.
  - Manage memory: Paged attention (block allocation), KV cache compression, sliding window + attention sinks (fixed size), quantization of the KV cache, prompt caching across users.
  - Can explode for long contexts x many concurrent users — sometimes exceeds the weight size; per-request it is in GBs.
- Частые ошибки: не знать, почему кэшируют только K и V (Q нужен только текущему токену); думать, что кэш бесплатен.
- Красные флаги: «считать KV cache бесплатным», «кэшировать Query».

### 19. What is Paged Attention?
- Идеал: manage KV cache memory like OS paging — small fixed-size blocks/pages allocated on demand, scattered anywhere, tracked by a block table.
- Обязательные пункты:
  - Solves memory waste: traditional allocation reserves one large contiguous block (max length) per request -> internal waste (reserved but unused) + external waste (unusable small gaps).
  - Blocks are fixed-size pages (e.g. 4 tokens each), allocated as needed, need not be contiguous; a block table maps logical block -> physical location (like OS page table) .
  - Nearly eliminates both waste types -> serve many more concurrent requests on the same memory.
  - Enables memory sharing: requests with the same prefix share blocks (parallel sampling, beam search).
  - Core idea behind vLLM; same paged KV cache in TensorRT-LLM. Does NOT shrink the cache itself (that's KV cache compression).
- Частые ошибки: думать, что paged attention уменьшает сам KV cache; путать с flash attention.
- Красные флаги: «paged attention — это флеш-аттеншн», «он уменьшает размер самого кэша».

### 20. How does GGUF work?
- Идеал: GGUF = single self-contained file format (GPT-Generated Unified Format) storing everything a model needs for local inference — weights (tensors), tokenizer, and metadata/config.
- Обязательные пункты:
  - Solves the scattered-files problem (separate weights/tokenizer/config files were fragile, not portable, slow); successor of GGML.
  - Layout: header (GGUF magic + version), key-value metadata (architecture, context length, vocab, quantization info), tensor info table (names/shapes/offsets), then tensor data (the weights).
  - Quantized weights stored directly in file (Q4_K_M, Q5_K_M, Q8_0; names: Q + bits + K-method + S/M/L size variant).
  - Loads fast via memory mapping (mmap) — only needed parts pulled in on demand, near-instant start, shared across processes.
  - Cross-platform and extensible; standard for local/edge models (llama.cpp, Ollama, LM Studio).
- Частые ошибки: думать, что GGUF — движок, а не формат файла; не упоминать mmap.
- Красные флаги: «GGUF = движок инференса», «не хранит токенизатор».

### 21. How do you optimize inference for edge and mobile deployment?
- Идеал: shrink the model and use CPU/GPU efficiently so it fits and runs on phones/laptops without a server.
- Обязательные пункты:
  - Quantization: 4-8 bit weights (e.g. 7B fp16 ~14 GB → ~4 GB at 4-bit) so it fits in device memory.
  - llama.cpp: C++ engine on everyday hardware — quantized GGUF, SIMD (AVX/AVX2/AVX512/NEON) for fast CPU math, gpu-layers to offload to GPU with rest on CPU.
  - Memory mapping: instant start, on-demand load, memory sharing across processes.
  - Trade-offs: privacy/offline/no per-use cost vs accuracy loss; NPU/Edge TPU for dedicated acceleration; weight+activation quantization for max speed.
  - Compare cloud vs on-device: on-device wins for privacy/latency/cost when model small enough.
- Частые ошибки: забыть quantization как ключевой приём; думать, что edge требует GPU datacenter.
- Красные флаги: «edge = только облако», «квантование не влияет на скорость».

### 22. What is model quantization (INT8, INT4, FP16, BF16), and how does it affect quality?
- Идеал: store/compute model numbers at lower precision → less memory, faster speed, small accuracy loss.
- Обязательные пункты:
  - Formats: FP32 (32-bit, training, precise) vs FP16/BF16 (16-bit, half size; BF16 keeps wide range) vs INT8 (256 values) vs INT4 (16 values).
  - Mechanic: map real range onto integers via scale + zero-point: q = round(v/scale)+zp; dequant (q-zp)*scale; symmetric (centered, zp=0, simple/fast) vs asymmetric (one-sided data).
  - Granularity: per-tensor (1 scale) vs per-channel (scale per row) — per-channel preserves detail.
  - When: PTQ (post-training, cheap) vs QAT (quantization-aware training, best at low bits); weight-only (activations fp16, common for LLMs) vs weight+activation (fastest).
  - LLM specific: outlier problem (few huge activations ruin scale); methods GPTQ/AWQ/bitsandbytes/GGUF; 4-bit is the sweet spot; 2-bit degrades noticeably.
  - The video frames quantization among 5 techniques (with pruning, distillation, KV cache, speculative decoding).
- Частые ошибки: думать, что цель — улучшить качество; забыть, что INT4 = 16 значений.
- Красные флаги: «квантование без потери», «BF16 = INT8», «квантовать нельзя вообще ничего».

### 23. How do you implement auto-scaling for AI workloads?
- Идеал: auto-scale infrastructure based on demand — more replicas when load is high, fewer when idle.
- Обязательные пункты:
  - Metrics: request rate, queue depth, GPU utilization, TTFT/TPOT SLAs. Use queue-depth-based scaling for LLM (scaling on GPU util is too slow).
  - Kubernetes HPA/VPA or cloud ASGs; KEDA for event-driven scaling on custom metrics.
  - Per-replica batching + continuous batching interacts with scaling — warm-up time for model loading.
  - Cooldown periods prevent thrashing; scale-down to min replicas to avoid cold-start latency.  
  - Pre-scaling before traffic spikes (scheduled scaling) for known load patterns.  
  - Scale to zero (serverless) possible with cold-start budget; keep at least one warm replica.  
- Частые ошибки: масштабировать только по CPU/запросам без учёта очереди; забывать про cold-start.
- Красные флаги: «автоскейл = любое изменение нагрузки», «не мониторить очереди».  

### 24. What is the role of load balancing in AI serving infrastructure?
- Идеал: distribute requests across model replicas to ensure even load, high availability, and SLO compliance.
- Обязательные пункты:
  - Layer: load balancer (LB) in front of a pool of GPU-backed inference servers; routes each request to a replica.
  - Sticky/least-loaded: route to least-utilized or least-queued replica; avoid overloading any single GPU.
  - Health checks and draining: remove unhealthy replicas, drain before scaling down.
  - Session affinity: for stateful chat keep requests on the same replica (KV cache reuse for continued conversations).
  - Weighted/policy-based routing can separate heavy vs light requests; graceful shedding.
- Частые ошибки: round-robin without queue awareness; load balancing breaks KV-cache continuation for chat.
- Красные флаги: «без LB нет», «всё одно и то же как у веба, без учёта GPU».

### 25. How do you manage GPU memory for serving multiple models?
- Идеал: share limited GPU memory across several models/servers to maximize utilization and minimize cost.
- Обязательные пункты:
  - Separate per model: dedicate a GPU per model — simple, isolation, but wasteful for small models.
  - Co-locate multiple models on one GPU (with paged attention / memory limits) when total fits; train-limit or memory budget to prevent OOM.
  - GPU sharing tiers: single proton (vLLM/KServe) supports multi-model GPU sharing with scheduling.
  - Dynamic loading: load/unload models (paging to disk/host memory) for rare/cold models.
  - Quantize smaller models to fit more per GPU; KV cache budget per request constrains concurrency.
- Частые ошибки: думать, что одна модель = одна GPU — забыть, что маленькие модели делят GPU.
- Красные флаги: «каждая модель должна иметь отдельную GPU», «не следить за KV cache».

### 26. What is model sharding, and when would you use it?
- Идеал: split a model's parameters across multiple devices so a model that doesn't fit on one GPU can run; the general name for distributing the model.
- Обязательные пункты:
  - Weight sharding: each device stores a slice of weight tensors (tensor parallelism) or layer stages (pipeline parallelism); activations/communication between shards.
  - Required when: weights + KV cache + activations exceed a single GPU VRAM (e.g. 70B fp16 140GB > 80GB); also for training huge models.
  - Trade-off: capacity gain at cost of interconnect bandwidth (less than linear speedup).
  - Training and inference both use it; TP shards weights so each GPU holds a fraction.
  - Distinct from data parallelism (model replicated, not sharded).
- Частые ошибки: путать sharding с data parallelism; не упомянуть причину «не влезает в VRAM».
- Красные флаги: «sharding = несколько копий модели», «sharding не требует связи между GPU».

### 27. How do you implement request queuing and priority scheduling for AI services?
- Идеал: manage concurrent requests fairly: buffer in a queue when GPUs busy, schedule with priorities so SLAs are met.
- Обязательные пункты:
  - Queue with bounded depth + admission control/backpressure; reject or shed when overloaded.
  - Priority: separate queues by tier/SLA (real-time, batch, high-priority), weighted fair scheduling; per-request priority.
  - Multitenancy: fair share across tenants; request rate limiting.
  - Integrated with continuous batching (arrivals join current batch); mitigate head-of-line blocking with preemption or a scheduler that estimates first-token time.
  - Monitor queue depth, wait time, per-priority metrics.
- Частые ошибки: бесконечная очередь без backpressure; слепой FIFO для смешанных запросов.
- Красные флаги: «очередь и batching не связаны», «priority = просто FIFO».


### 28. What are the cost trade-offs between self-hosted and API-based AI inference?
- Идеал: compare upfront/ongoing cost, utilization, and variable spend between owning GPUs vs renting per-token APIs.
- Обязательные пункты:
  - Self-hosted: high upfront and fixed cost (GPU hardware, power, ops, capacity planning); low/variable per-request marginal cost; best at high sustained utilization; full control/privacy/latency.
  - API-based: zero CapEx, pay per token (usage-based), scales to arbitrary peaks, no ops; but high marginal cost and vendor lock-in at high volume.
  - Break-even: APIs win for low/variable/spiky traffic; self-host wins for steady high volume (adequate utilization, 24/7).
  - Also: spot/preemptible GPUs, caching, quantization, region pricing.
- Частые ошибки: только про цену GPU, не учитывать utilization и операционные расходы.
- Красные флаги: «API всегда дешевле», «GPU свои бесплатно».

### 29. How do you handle cold start latency for serverless AI deployments?
- Идеал: minimize the delay when a fresh inference replica must be spun up — model loading is the dominant cost.
- Обязательные пункты:
  - Model load time: loading weights (GBs) to VRAM is the big chunk; warm pool of pre-loaded replicas (min replicas) instead of scale-to-zero.
  - Snapshot/freeze: container image snapshot with preloaded weights (or model loaded on host memory) to cut startup; process-fork/restore.
  - GGUF/llama.cpp mmap gives near-instant load for local/edge.
  - Serverless with request-triggered cold start: either budget for it (queue the request until warm) or keep 1+ warm replica; predict warm-up ahead of spikes.
  - Split routing: warm replicas take interactive traffic; cold spares absorb batch.
- Частые ошибки: думать, что cold start = обычный контейнерный старт (лаги в загрузке весов).
- Красные флаги: «serverless LLM без cold start», «загружается мгновенно, как обычный лямбда».

### 30. How do you implement model caching to reduce redundant computations?
- Идеал: reuse earlier computed/prompt work so repeated input doesn't recompute prefill — prompt (KV) caching plus optional semantic caching.
- Обязательные пункты:
  - Prompt caching: save KV cache of stable prompt prefixes (system prompt, tools, docs) — cache write (~1.25x) then cheap reads (~0.1x), matching exact prefix; fixed parts first, changing parts last; TTL (e.g. 5 min).
  - Keep stable front: system instructions, big documents, tool definitions, few-shot; user message last — one changing char at the start breaks the cache.
  - Semantic caching: reuse final answers for semantically equal questions (differs from exact-prefix KV cache).
  - Also KV cache reuse across user requests sharing the same prefix, embedding caches for routing/retrieval.
- Частые ошибки: класть дату/user-name в начало промпта — убивает кэш; путать с семантическим кэшем.
- Красные флаги: «промпт-кэш работает при любом изменении», «промпт caching = это TTL на ответ».

### 31. What is the difference between synchronous and asynchronous inference, and when do you use each?
- Идеал: sync — client waits for full response; async — request queued, client notified/polled when ready.
- Обязательные пункты:
  - Sync: request-response over HTTP; client blocks on socket; for low-latency interactive chat. Simple but underutilizes GPU if requests queue behind a slow one.
  - Async: submit request, get a job ID; GPU picks from queue, computes; client polls or receives webhook. Enables continuous batching, better throughput, background processing.
  - Use sync for: interactive chat (user waits), streaming responses where partial output is shown.
  - Use async for: batch processing (large documents), webhooks for long completions, high-throughput pipelines, scheduled jobs.
  - Streaming (SSE/WebSocket) is a variant of sync where bytes arrive progressively — still synchronous per token.
- Частые ошибки: путать async с batch processing; думать, что async = не нужен GPU.
- Красные флаги: «async = без GPU» (просто очередь), «sync нельзя использовать для батчей».

### 32. What is FSDP (Fully Sharded Data Parallel), and how does it differ from DeepSpeed ZeRO?
- Идеал: FSDP = PyTorch's implementation of ZeRO-style sharded data parallelism; shards model across GPUs instead of replicating.
- Обязательные пункты:
  - FSDP shards: each GPU holds only its shard of model params; gathers full param shard for forward/backward, then frees — reduces memory from full-copy to ~1/ngpu.
  - Three ZeRO stages: ZeRO-1 sharded optimizer + gradients + params; ZeRO-2 adds gradient sharding; ZeRO-3 adds param sharding (full FSDP); ZeRO-Offload offloads to CPU.
  - FSDP is the PyTorch native version; DeepSpeed ZeRO is the same concept implemented in DeepSpeed library (which integrates with PyTorch); both follow the same design.
  - Use FSDP/ZeRO-3 for models too big for a single GPU memory; trade-off: extra communication vs VRAM reduction.
  - FSDP + activation checkpointing further reduce memory; not for inference (only training).
- Частые ошибки: путать FSDP/ZeRO с tensor parallelism; думать, что FSDP ускоряет inference.
- Красные флаги: «FSDP = tensor parallelism», «использовать ZeRO для inference».

### 33. What are TTFT, TPOT, and throughput, and how do they trade against each other?
- Идеал: define the latency/throughput metrics of the two inference phases and show the trade-off between them.
- Обязательные пункты:
  - TTFT = Time To First Token — covers prefill (processing the whole prompt) + queueing; grows with prompt length; driven by compute.
  - TPOT = Time Per Output Token — average decode time per token; driven by memory bandwidth and batching.
  - Throughput = tokens generated per unit time across the system (tokens/s); boosted by batching.
  - Trade-off: raising batch size raises throughput but can increase TTFT/TPOT (shared compute/memory); optimizing one (e.g. more concurrency) may hurt another.
  - Also total latency = TTFT + TPOT × N-output-tokens (plus queue).
  - Prefill vs decode have different bottleneck (compute-bound vs memory-bound) — motivating disaggregation.
- Частые ошибки: путать TTFT и TPOT; считать, что throughput растёт без последствий.
- Красные флаги: «TTFT = время всего ответа», «TPOT не связан с bandwidth».

### 34. How do you monitor and profile LLM inference in production (TTFT, inter-token latency, GPU utilization)?
- Идеал: instrument the serving stack end-to-end to catch latency SLO violations, memory pressure, and under-utilization.
- Обязательные пункты:
  - Metrics: TTFT, TPOT/inter-token latency (token-to-token time), end-to-end latency, queue/wait time, tokens/s (throughput), batch size, request rate, error rate.
  - Infra metrics: GPU utilization (compute), memory utilization (VRAM), memory bandwidth, KV-cache usage per request, OOM count, P99 of each latency.
  - Distributed tracing: trace through queue → prefill → decode to see where time goes; logs for request ids; sample for profiling.
  - Alerting: SLOs on TTFT/TPOT; dashboards for utilization vs latency; watch for degrading P99 with batching.
  - Profiling: nvidia-smi/DCGM, nsight-prof/profile CUDA kernels, attention hotspots, memory allocator stats; compare prefill vs decode phases.
  - Golden signals: traffic, latency, errors, saturation.
- Частые ошибки: смотреть только на GPU util и не измерять latency; измерять p50 вместо p99/p95.
- Красные флаги: «GPU util 100% = хорошо» без учёта очередей и latency; «не нужен трейсинг».

### 35. What is model routing at the infrastructure level, and how do you route requests based on complexity and cost?
- Идеал: route each query to the right LLM in a pool based on cost, latency, and quality — easy → small/cheap, hard → frontier.
- Обязательные пункты:
  - Router sits in front of a pool of LLMs (small/mid/frontier/specialist); goal: cost savings without losing quality (~30× gap between frontier and small).
  - Strategies:
    - Rule-based (keywords/length) — fast, cheap, brittle.
    - Classifier-based — trained on labeled (query, best-LLM) pairs; learns hidden patterns; needs retraining.
    - Embedding-based — nearest reference embedding per LLM; no training; add LLM = add embedding.
    - LLM-as-router — small LLM reads query and picks; flexible via prompt, adds an extra LLM call.
    - Cascade — try cheapest first, escalate only when low-confidence → highest average savings but slow for hard queries.
  - Router overhead must be small (~<10% of target latency); apply also for GPU provisioning (how to host the pool efficiently).
- Частые ошибки: не включать малый/дешёвый путь; роутинг применяют к фиче — не думать о cost-optimization.
- Красные флаги: «routing — это только CDN/nginx», «один роутер для всего» без пула моделей.
