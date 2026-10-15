# LLM Fundamentals — Answer Key (1-40)

### 1. What are foundation models, and how have they changed AI engineering?
- Идеал: Foundation models are large pre-trained models (e.g. LLMs) that serve as a general base, repurposed via prompting/fine-tuning for many tasks; they shifted AI engineering from building models to integrating and orchestrating them.
- Обязательные пункты:
  - Pre-trained on massive data; one model handles many downstream tasks.
  - Changed AI engineering: engineers consume an LLM and build RAG, MCP tools, agents, fine-tuning, quantization around it.
  - Lower barrier — no training from scratch needed to build a working AI product.
- Частые ошибки: отождествлять foundation models только с ChatGPT; не упомянуть сдвиг от «своей» модели к использованию готовой + обвязке (RAG/agents).
- Красные флаги: «foundation model требует дообучения под каждую задачу обязательно»; «это просто API-обёртка над поиском».

### 2. What is a Large Language Model (LLM), and how does it work?
- Идеал: An LLM is a large model trained on massive text that predicts the next token; generating text step by step, each token informed by prior context.
- Обязательные пункты:
  - Language model: understands/generates text based on patterns; "large" = scale.
  - Trained on huge corpora; internal math over token IDs.
  - Autoregressive: emits one token at a time, feeding output back as input.
- Частые ошибки: думать, что LLM «понимает» как человек или обращается к БД знаний; не упомянуть next-token prediction.
- Красные флаги: «LLM ищет ответ в интернете». Основная механика — только предсказание следующего токена.

### 3. Inside ChatGPT: What Happens After You Hit Enter?
- Идеал: не чтение слов: токенизация → токен-ID → embedding → через слои Transformer (attention) → softmax-вероятности → автогенерация следующего токена.
- Обязательные пункты:
  - Not reading words — to tokenize prompt, each token gets numeric ID.
  - Tokens → numbers; model runs forward pass over them.
  - Predicts next token, repeats (probability game, one word at a time).
  - ChatGPT is just an interface around an LLM.
- Частые ошибки: считать, что модель «думает» или читает слова; пропустить этап token→ID→embedding.
- Красные флаги: «ChatGPT ищет готовый ответ в базе»; «модель вычисляет весь ответ за один проход».

### 4. What is the Transformer architecture and how does it work?
- Идеал: tokens-in/tokens-out machine (text-in, text-out), processes all input tokens in parallel with attention; introduced in "Attention Is All You Need" (2017).
- Обязательные пункты:
  - Replaced sequential RNN processing — solves forgetting (long-range) and slowness.
  - All tokens at once; attention lets every token look at every other.
  - Two halves (encoder+decoder) in the original; decoder-only in most LLMs.
- Частые ошибки: не упоминать attention как ядро; описывать как языковую модель с памятью.
- Красные флаги: «Transformer обрабатывает слова по одному последовательно»; «он запоминает в специальную базу».

### 5. What are the key components of the Transformer architecture?
- Идеал: tokenization → embedding + positional encoding → multi-head attention; FFN; residual connections; layer normalization; (encoder/decoder).
- Обязательные пункты:
  - Embedding + positional encoding give token and order info.
  - Multi-head self-attention (sub-layers with residual + LayerNorm).
  - Feed-forward network per token, residual + LayerNorm.
  - Original model: encoder + decoder; modern LLMs mainly decoder-only.
- Частые ошибки: забыть positional encoding и residual/LayerNorm; сводить всё к attention.
- Красные флаги: «attention без FFN достаточно»; «positional encoding не обязателен, модель сама чувствует порядок».

### 6. Walk me through what happens, step by step, in one forward pass of a decoder-only Transformer.
- Идеал: decoder-only is the same pass as a single token step of generation: tokenize + embed + positional encoding → block of (masked self-attention → FFN) with residuals and LayerNorm → final LayerNorm → linear head → logits → softmax/sampling → next token.
- Обязательные пункты:
  - Input tokens → token IDs → embeddings + positional info.
  - Causal (masked) self-attention: only past tokens; each head gives context-aware representation.
  - FFN processes each token independently; residual connections and LayerNorm stabilize each block.
  - Stack of N blocks → output LayerNorm → vocabulary projection (logits) → softmax → sample/logits → next token appended.
- Частые ошибки: позволять «видеть» будущие токены (нет causal mask); пропускать позиции и residual+norm; забывать финальный проход на vocab.
- Красные флаги: «декодер смотрит в обе стороны, как encoder»; «ответ генерируется одним вычислением целиком».

### 7. What is tokenization in LLMs?
- Идеал: process of breaking text into small pieces (tokens) and mapping each to a number the model can process; every LLM has its own tokenizer.
- Обязательные пункты:
  - Token = word, subword, character, punctuation, space-attached.
  - Character-level: tiny vocab but long sequences, little meaning per token. Word-level: short sequences but huge vocab + unknown-token problem.
  - Subword-level: common words stay whole, rare words split; manageable vocab (~50k-200k), no unknown problem — used by modern LLMs.
  - Rule of thumb: ~4 chars per token (English).
- Частые ошибки: считать токен = слово; не упоминать числовое ID и отдельный токенайзер у каждой модели.
- Красные флаги: «модель читает слова/буквы напрямую»; «один токен = одна буква».

### 8. Explain BPE (Byte Pair Encoding).
- Идеал: subword tokenization algorithm; starts with single chars/bytes and iteratively merges the most frequent adjacent pair, building a vocabulary of common subwords.
- Обязательные пункты:
  - Why: word-level has unknown words; character-level is too long. BPE = middle ground (pieces between chars and words).
  - Steps: split corpus into characters → count adjacent pairs → merge most frequent → repeat until target vocab size; merges saved as ordered rules.
  - Encoding new text: apply saved merge rules in order.
  - Byte-level BPE (GPT-style): starts from 256 byte values, so nothing is ever unknown (any Unicode, emoji).
  - Tokenizer trained separately before the LLM and frozen during model training.
- Частые ошибки: «BPE делит на морфемы по словарям»; забыть, что токенайзер замораживается.
- Красные флаги: «BPE без статистики частот пар»; «инкрементально обучается вместе с моделью (переобучается на лету)».

### 9. Explain WordPiece and SentencePiece.
- Идеал: subword tokenizers like BPE; WordPiece = greedy frequency-based merges scored by likelihood gain (used by BERT); SentencePiece = trainable subword tokenizer treating text as raw chars with prefix marker ▁, language-agnostic (used by T5, LLaMA).
- Обязательные пункты:
  - WordPiece: similar to BPE but selects pairs that maximize language-model likelihood, not raw frequency; ## prefix marks continuation (BERT).
  - SentencePiece: operates on raw Unicode (no pre-tokenized words), adds ▁ (whitespace) marker; supports BPE, unigram, word/char models; reversible between text and tokens.
  - Both solve the unknown-word problem via subword decomposition.
- Частые ошибки: путать WordPiece с BPE (разное правило отбора пар); думать, что SentencePiece токенизирует только по пробелам.
- Красные флаги: «WordPiece = BPE 1-в-1»; «SentencePiece хранит целые слова и не выдерживает OOV».

<sub>Синтез — референсы в qmap отсутствуют.</sub>

### 10. What is positional encoding, and why is it needed in Transformers?
- Идеал: LLMs have no notion of word order (they process tokens in parallel, unlike RNNs). Positional encoding/embeddings inject each token's position so the model can distinguish "Outcome School" from "School Outcome".
- Обязательные пункты:
  - Transformers are order-invariant without it; attention alone doesn't carry position.
  - Positional info is added to token embeddings before feeding into the network.
  - Lets the model know relative/absolute positions of words.
- Частые ошибки: думать, что position избыточен или что attention самодостаточен.
- Красные флаги: «positional encoding превращает transformer в RNN»; «это то же самое, что attention bias».

### 11. What are embeddings?
- Идеал: embeddings are vector representations of objects (text, images, audio) that capture their properties and relationships; similar items land close in vector space.
- Обязательные пункты:
  - Produced by embedding models (e.g. text/audio embedding models on text/document data).
  - Numbers are what the model actually computes with; dot-product similarity reflects relatedness.
  - In Transformers the input starts as token embeddings (contextualized by attention layers).
- Частые ошибки: путать embeddings с one-hot (нет геометрического смысла подобия); думать embeddings — это словарь пар «слово→ID».
- Красные флаги: «embeddings = случайные вектора», «embeddings — это и есть ответ модели».

### 12. Explain the Query (Q), Key (K), and Value (V) in attention.
- Идеал: Q is what a token is looking for; K is what each token offers/labels; V is the actual information carried. Attention matches Q against K, then mixes V by the resulting weights.
- Обязательные пункты:
  - Q = X·W_Q, K = X·W_K, V = X·W_V (learned matrices).
  - Scores = Q·K^T — relevance comparison; higher score = stronger match.
  - Output = weighted sum of V; formula softmax(Q·K^T/√d_k)·V.
- Частые ошибки: путать роли Q/K/V; думать V участвует в сравнении.
- Красные флаги: «V — то, что мы ищем», «K хранит выходной результат».

### 13. What is self-attention, and how does it work in Transformers?
- Идеал: every token looks at every other token in the same sequence (including itself) to understand context; Q, K, V all come from the same input sequence.
- Обязательные пункты:
  - Solves RNN problems: parallelization (GPU-friendly) and long-range dependencies (no distance decay).
  - Contextual understanding: same word gets different representation depending on sentence (e.g. "it" → "animal" vs "street").
  - Steps: Q·K^T → scale by √d_k → softmax → weights×V.
  - One head can learn only one type of relationship → motivates multi-head.
- Частые ошибки: не упомянуть «все из одной последовательности»; сказать, что она рекуррентна.
- Красные флаги: «self-attention не видит себя», «она обрабатывает слова по порядку».

### 14. What is Cross Attention in Transformers?
- Идеал: attention where Query comes from one sequence (decoder) and Key/Value come from a different sequence (encoder) — one sequence asks, another answers; the bridge in encoder–decoder (translation, multimodal) models.
- Обязательные пункты:
  - Q from the decoder side; K, V from the encoder output, computed once and reused for every decoder step.
  - Not masked: the whole input sequence is known, so every output token may attend to every input token.
  - Attention matrix rectangular (output length × input length).
  - Same math as self-attention; difference is source of Q/K/V.
- Частые ошибки: применять causal mask; не упоминать, что K/V пересчитываются на каждом шаге.
- Красные флаги: «в cross attention Q,K,V с одной стороны»; «это то же самое, что self-attention внутри decoder».

### 15. Why do we scale the dot product attention by √dₖ?
- Идеал: dot products grow with d_k; large scores push softmax to extremes (near 0/1), causing vanishing gradients and over-confident attention; dividing by √d_k keeps scores in a healthy range.
- Обязательные пункты:
  - Variance of the dot product = d_k (each element mean 0, variance 1 → variance of sum = d_k). Mathematically exact proof.
  - Without scaling → e.g. scores [50,10,5] → softmax near [1,0,0] — collapse to a single token.
  - Large values → vanishing gradients; √d_k restores unit variance (≈1).
- Частые ошибки: называть константу вместо √d_k; думать масштаб не влияет на градиенты.
- Красные флаги: «делим на d_k»; «√d_k произвольно выбранная константа».

### 16. What is causal masking?
- Идеал: a mask matrix that blocks future positions so each token attends only to itself and past tokens; blocked positions set to −∞ before softmax.
- Обязательные пункты:
  - Preventing information leakage: seeing future tokens = shortcuts → unrealistically good train loss, but fails during inference (future tokens don't exist).
  - −∞ because softmax(−∞)=0 exactly — gives exact zero attention; 0 would still leak partial attention.
  - Only encoder side is bidirectional; decoder looks backward (look-only-backward) — training matches inference.
  - Different from sliding-window (limits how far back) vs causal (blocks future).
- Частые ошибки: применять маску после softmax; использовать 0 вместо −∞.
- Красные флаги: «маска нулями эквивалентна», «causal mask применяется после softmax».

### 17. What are multi-head attention mechanisms? Why use multiple attention heads?
- Идеал: many self-attention operations run in parallel, each with own Q/K/V projections, then concatenated and projected — like looking at a sentence with many pairs of eyes, each focusing on a different aspect (subject-verb, verb-object, long-range).
- Обязательные пункты:
  - d_k = d_model / h (e.g. 512/8 = 64 per head); each head has own W_Q, W_K, W_V.
  - Outputs concatenated (h×d_k = 512) then linear W_O mixes them.
  - A single head can learn only one relationship at a time; multiple heads give richer representation.
  - Introduced in "Attention Is All You Need".
- Частые ошибки: думать многоголовость добавляет автономную память; пропустить финальный линейный слой.
- Красные флаги: «heads значительно увеличивают размерность» (итог совпадает с d_model); «heads работают последовательно».

### 18. What are Feed-Forward Networks in LLMs?
- Идеал: a small neural network (two linear layers with activation) inside every Transformer layer; after attention mixes information between words, FFN processes each word individually — the model's knowledge store/refiner.
- Обязательные пункты:
  - Per-token, unlike attention (applied independently to each token representation, batched as matrix multiplication).
  - Expand-then-contract pattern (e.g. inner dim 4× the width), activation like ReLU.
  - Holds the majority of model parameters — stores and applies knowledge.
  - Sits with residual connection + LayerNorm; in MoE, the FFN is replaced by experts.
- Частые ошибки: не подчеркнуть per-token характер; думать FFN моделирует связи между словами.
- Красные флаги: «FFN — это attention для пар слов», «FFN не обучается».

### 19. What is Generative AI?
- Идеал: AI that creates new things — text, images, audio, video, code — that did not exist before (e.g. a brand-new poem, not a retrieved one).
- Обязательные пункты:
  - "Generate" = create new, not search/retrieve existing content.
  - Learns from huge numbers of examples; produces novel combinations.
  - Powers everyday tools (chat, image/audio/video generation, code assistants).
  - Limitations: plausible but can be wrong (hallucination), quality varies.
- Частые ошибки: путать с retrieval; думать у ней нет пределов и ошибок.
- Красные флаги: «генерация = поиск по базе готовых ответов», «модель хранит все свои ответы в памяти».

### 20. What is the context window in LLMs, and why does it matter?
- Идеал: the LLM's working memory — everything it sees, thinks, and replies with must fit inside it; prompt + generated output together.
- Обязательные пункты:
  - Limited token capacity per request (input + output).
  - Dictates how much document/history/context you can pass.
  - Practical impact: long docs, multi-turn chats, tool outputs, larger output length.
- Частые ошибки: путать context window с training data или памятью модели.
- Красные флаги: «контекст — это база знаний модели», «она может отвечать без ограничений».

### 21. Why is the context window limited in LLMs?
- Идеал: ограничен из-за cost: attention O(n²) compute, KV cache grows with length, and architecture/training context caps.
- Обязательные пункты:
  - Quadratic attention compute in sequence length (n² scores).
  - KV cache memory grows with tokens, constraining batch and length (GQA, quantization, eviction mitigate).
  - Model trained within a context; beyond it, attention quality degrades (attention sinks, window collapse).
  - Product: longer prompt → slower first token + more memory.
- Частые ошибки: сводить причину к одной; не упоминать KV cache и O(n²).
- Красные флаги: «можно просто выставить лимит в конфиге без потерь», «контекст ограничен только токенизатором».

### 22. What is temperature in the context of LLMs, and how does it affect output?
- Идеал: temperature is a knob that controls randomness vs predictability; it rescales logits (divide logits by T) before softmax.
- Обязательные пункты:
  - Low T → focused, predictable, higher-probability tokens; T→0 approaches greedy/argmax.
  - High T → flatter distribution, creative/surprising tokens; too high → gibberish.
  - T=1 typical default; range commonly 0–2.
  - Applied before softmax: p ∝ exp(z/T), doesn't change ranking of scores, only sharpness.
- Частые ошибки: думать temperature взвешивает слова по частоте в корпусе; что это требует переобучения.
- Красные флаги: «temperature=1 — максимальная случайность», «больше temperature = всегда лучше».

### 23. Why is the first token slower than the rest in an LLM?
- Идеал: inference has two phases — Prefill (reads the whole prompt once, computes attention for every input token, stores in KV cache) and Decode (generates one token at a time, only computing the new token against cached K/V).
- Обязательные пункты:
  - Prefill: heavy work done once → time-to-first-token (TTFT); longer prompt → slower first token (1000 tokens all processed before the first new word).
  - Decode: light work many times → time-per-output-token (TPOT); KV cache avoids recomputing attention for already-seen tokens.
  - This explains "first token slow, rest streams".
- Частые ошибки: объяснять «модель думает»; не упомянуть KV cache.
- Красные флаги: «каждый токен пересчитывает весь контекст каждый раз», «первый токен медленный из-за сети».

### 24. Explain Top-p (nucleus) sampling and Top-k sampling. How do they differ?
- Идеал: both narrow the candidate set before random sampling. Top-k keeps the k most likely tokens; Top-p keeps the smallest set whose cumulative probability reaches p (adaptive size).
- Обязательные пункты:
  - Context: always picking the best token → boring/repetitive; sampling from all tokens → silly. These strike a balance.
  - Top-k: fixed number (e.g. top 50) → can include the flat/low-prob tail or cut a peaked distribution.
  - Top-p: dynamic — builds a nucleus of most-probable tokens until cumulative ≥ p (e.g. 0.9), then samples within it.
  - Often combined with temperature; both reshape probabilities before the sample.
- Частые ошибки: называть top-p «отбрасыванием токенов с вероятностью < p по одному».
- Красные флаги: «top-k и top-p — это одно и то же», «top-p всегда оставляет ровно p токенов».

### 25. Compare greedy decoding, beam search, top-k, top-p, and temperature sampling. When does each fail?
- Идеал: greedy = always take argmax token (deterministic, fast, but locally optimal → bland/repetitive); beam search = keeps multiple partial hypotheses (better long structured output, costly/narrow); top-k/top-p = stochastic sampling from filtered sets (diverse, can be incoherent); temperature = rescales probabilities, not a separate decoding strategy.
- Обязательные пункты:
  - Greedy fails: gives up on a better continuation that follows a slightly-lower first token.
  - Beam fails: fixed width still can be repetitive/expensive; needs length normalization; strong for translation/code.
  - Top-k/p fail when the distribution is very peaked (excludes the right token) or very flat (admits junk).
  - Temperature alone can't fix a degenerate distribution — pair with top-k/p; low temp/greedy for exact/structured (code), top-p+temp for creative text.
- Частые ошибки: считать temperature самостоятельной стратегией декодирования; думать beam всегда лучше greedy.
- Красные флаги: «temperature=0 полностью эквивалентно greedy по качеству безоговорочно»; «beam нельзя ограничить шириной».

### 26. What are logits, and how are they used in text generation?
- Идеал: logits are the raw, unnormalized scores the model gives each token in the vocabulary before softmax; they express relative likelihood of the next token.
- Обязательные пункты:
  - Produced by the final projection layer over the vocabulary.
  - Softmax (after temperature scaling) converts logits into probabilities summing to 1.
  - Used to pick the next token (argmax or sampling); highest logit = most probable.
- Частые ошибки: путать logits с вероятностями; думать они уже нормированы.
- Красные флаги: «logits — это уже проценты», «logits выдаёт токенизатор».

### 27. What are stop tokens in LLMs, and how does an LLM know when to stop generating?
- Идеал: a special vocabulary token meaning "the text ends here"; the generation loop breaks when the model produces it.
- Обязательные пункты:
  - Autoregressive loop has no natural end — without a stop signal the model keeps writing (e.g. continues into history of Delhi).
  - Learned from training: stop token appended to every document/assistant reply, so the model learns what an ending looks like (not a hardcoded rule).
  - Examples: `<|endoftext|>` (GPT-2), `</s>` (Llama 2), `<|eot_id|>` (Llama 3), `<|im_end|>` (Qwen), `<end_of_turn>` (Gemma).
- Частые ошибки: думать stop token — настройка, а не выученный токен; путать с max_tokens.
- Красные флаги: «модель останавливается по длине сама», «stop token добавляется после ответа как постфикс без обучения».

### 28. What is the difference between a stop token and a stop sequence?
- Идеал: stop token = single special in-vocabulary token the model learned to emit; stop sequence = a user-supplied text fragment the inference system watches for and cuts at (model doesn't know about it).
- Обязательные пункты:
  - Stop token is built into vocabulary, learned during training, single token (e.g. `</s>`).
  - Stop sequence is set by the user/API (e.g. `stop=["\n", "Q:"]`) and checked after each generated token; generation halts on match at system level.
  - Use case: in Q&A lists the model keeps generating next questions, so a `"Q:"` stop sequence prevents runaway continuation even when the stop token scores low.
- Частые ошибки: использовать термины как синонимы.
- Красные флаги: «stop sequence — это content filter», «stop token задаёт пользователь в промпте».

### 29. What are skip connections (residual connections) in Transformers?
- Идеал: residual/skip connections add the layer's input to its output (output = input + F(input)), letting gradients flow and deeper networks train stably.
- Обязательные пункты:
  - Placed around each sub-layer (attention, FFN) along with LayerNorm.
  - Mitigate vanishing gradients in deep stacks — the identity path lets gradients pass through.
  - Preserve input info while the sub-layer adds refinement; enable training very deep LLMs.
  - Foundation for why RMSNorm de-recentering is acceptable (residuals absorb mean shifts).
- Частые ошибки: пропустить роль в стабильности training; думать skip connection заменяет attention.
- Красные флаги: «skip connection это типо слой нормлизации», «без residual transformer все равно обучается глубоко».

### 30. What is the difference between open-source and closed-source LLMs? When would you choose one over the other?
- Идеал: open-source (Llama, Mistral, Qwen) gives weights, control, fine-tuning, data privacy, self-hosting cheaply-ish but needs infra/ML skills and data management; closed (GPT-4, Claude, Gemini) is managed API — easy, secure, strong quality, but vendor lock-in, no weight access, and per-token cost.
- Обязательные пункты:
  - Open-source: full weights available, self-host, fine-tune, audit, no API dependency; cost = infra + ops.
  - Closed-source: hosted API, less setup, strong defaults, integration/scale handled; cost per token, privacy/send-data tradeoff, usage policies.
  - Choice depends on: data sensitivity (open/self-host), budget/ops, required capability, fine-tuning needs, compliance.
- Частые ошибки: не утверждать чистое преимущество одной стороны; игнорировать data privacy и латентность.- Красные флаги: «open-source всегда бесплатен в production», «closed-source всегда лучше или наоборот».

### 31. What is the difference between encoder-only, decoder-only, and encoder-decoder Transformer architectures?
- Идеал: Encoder reads the whole input at once, bidirectional; Decoder generates output one token at a time and looks only backward (causal). Combining both gives encoder-decoder; LLMs typically decoder-only; BERT is encoder-only.
- Обязательные пункты:
  - Encoder: bidirectional context, produces representations, no token generation — BERT-family (understanding/classification).
  - Decoder: causal (masked) self-attention, autoregressive generation — GPT-family (text generation).
  - Encoder-decoder: encoder representation feeds decoder via cross-attention — good for seq2seq/translation (T5).
  - Modern LLMs (ChatGPT, Claude, Gemini) are decoder-only.
- Частые ошибки: думать decoder смотрит в обе стороны; путать BERT vs GPT по направленности.
- Красные флаги: «decoder видит будущие токены», «encoder генерирует вывод».

### 32. What is KV cache, and how does it speed up inference?
- Идеал: KV cache stores the Key/Value tensors of already-processed tokens so the model doesn't recompute them when generating each new token.
- Обязательные пункты:
  - LLMs generate one token at a time; without cache each step redoes prior attention computations.
  - Two phases: prefill builds cache, decode reuses it — each new token computes attention for one new token only.
  - K = Key, V = Value per layer; bonded to prefill/decode (more in blogs).
  - Tradeoff: memory grows with sequence length/batch; affects context and batch constraints.
- Частые ошибки: думать cache хранит полный скрытый слой модели токена.
- Красные флаги: «KV cache хранит Q тоже», «без cache генерация быстрее».

### 33. Estimate the KV cache memory needed to serve a large model. How does it constrain batch size and context length?
- Идеал: размер ~ 2 × num_layers × num_kv_heads × head_dim × tokens × batch × bytes_per_element.
- Обязательные пункты:
  - KV memory per token = 2 (K and V) × layers × kv-heads × head_dim × bytes (e.g. fp16 = 2) × batch.
  - Пример: 32 layers, 8 kv-heads, head_dim 128 → 2×32×8×128 = 65536 byte/token = 64KB/token; 10k tokens → 640MB for one sequence; ×batch(32) → ~20GB.
  - Constrains: longer context or bigger batch directly multiplies cache → limited GPU/LS bandwidth; mitigations: GQA/MQA, quantization (INT8/4bit), eviction, low-rank compression, paged-attention.
  - Batch × context = the real budget (cache capacity = active tokens).
- Частые ошибки: забывать множитель 2 (K и V); считать head_dim ложно; не учитывать fp precision в байтах.
- Красные флаги: «KV cache памяти ~ параметров модели», «batch никак не связан с cache».

### 34. KV Cache Compression
- Идеал: set of techniques to shrink the memory the model uses to store the conversation while generating, enabling longer context with less memory.
- Обязательные пункты:
  - Quantization of the cache (store K/V in fewer bits — lower precision).
  - Token eviction — drop unimportant tokens from the cache (keeping attention sinks).
  - Sharing Keys/Values across heads (MQA/GQA — fewer KV sets).
  - Low-rank compression — squeeze cache into a small hidden vector.
  - Tradeoff: quality vs memory; choose by use case (long context, cost, latency).
- Частые ошибки: сводить к одному методу; игнорировать drop-quality tradeoff.
- Красные флаги: «компрессия уменьшает и кол-во токенов в контексте навсегда», «это делается переобучением модели».

### 35. What is model distillation, and how is it used with LLMs?
- Идеал: train a small "student" model to copy the behavior of a large "teacher" model, producing a fast, cheap model (runs on phone/edge) nearly as capable.
- Обязательные пункты:
  - Teacher = big/smart/slow; student = small/fast/cheap.
  - Students learn from soft labels (probability distribution, "dark knowledge") not just hard labels — softmax softened by temperature.
  - Distillation loss = student loss on hard labels + distillation loss on soft labels.
  - Applied to LLMs: distilled models deployed for inference efficiency.
- Частые ошибки: думать студент тупо повторяет ответы; не упомянуть мягкие метки.
- Красные флаги: «distillation = роение», «студент просто копирует только верные тексты teacher'а».

### 36. What is Mixture of Experts (MoE), and how does it work in models like Mixtral?
- Идеал: architecture with many small "expert" networks plus a router that activates only a few experts per input — big capacity with a fraction of compute (sparse activation).
- Обязательные пункты:
  - In Transformers, experts replace FFNs (e.g. 8/64/128 per layer); router picks top-k (e.g. 2) experts per token.
  - Before such sparse models, dense models — every token uses every parameter (100B → all 100B each token). MoE gets "massive total params, small active per token".
  - Faster/cheaper inference + allows huge models; experts specialize not by topics but patterns (learned, no manual labeling).
  - Challenge: load balancing among experts to keep router healthy.
  - Mixtral = 8 experts, top-2 routing, MoE FFN.
- Частые ошибки: думать эксперты — отдельные модели, вызываемые по очереди; что топ-к маршрутизация выбирает по смыслу «тематически».
- Красные флаги: «эксперты обучаются под отдельные темы вручную», «MoE использует все параметры на каждом токене».

### 37. What is the difference between dense and sparse models?
- Идеал: dense = every token uses every parameter (complete FFN for all tokens, full compute); sparse = uses only a subset of parameters per token (MoE — router activates a few experts).
- Обязательные пункты:
  - Dense: 100% params activated per token → deterministic cost, predictable.
  - Sparse: total params large but activated fraction small → less compute/memory during inference, can scale bigger.
  - Sparse models usually MoE. Trade-off: compute-per-token saved, but memory still holds all experts.
- Частые ошибки: думать sparse = меньше параметров всего; путать sparse attention (window) со sparse models.
- Красные флаги: «sparse модели имеют меньше параметров», «sparse = меньше качество обязательно».

### 38. How does DeepSeek-V4 work?
- Идеал: family of open MoE models (Pro and Flash) natively supporting 1M-token context at ~1/10 the cost of DeepSeek-V3.2, via compressed attention + new residuals + Muon optimizer + on-policy distillation.
- Обязательные пункты:
  - MoE FFN + router; Flash: 284B total / 13B activated, 1M ctx; Pro: 1.6T / 49B activated, 1M ctx.
  - Hybrid attention: CSA (Compressed Sparse Attention, lighter compression, sparse) + HCA (Heavily Compressed Attention), interleaved across layers.
  - Manifold-Constrained Hyper-Connections (mHC) — new residual connection design.
  - Muon optimizer + FP4 quantization-aware training; post-training = specialist training + on-policy distillation (OPD) of multiple teachers into one student.
  - At 1M ctx: Pro uses 27% per-token compute, 10% KV cache of V3.2; Flash 10% compute, 7% KV — makes ultra-long context practical.
- Частые ошибки: думать Pro/Flash — это разные архитектуры, а не масштаб; игнорировать cost angle (причина существования).
- Красные флаги: «DeepSeek-V4 — это dense model»; «поддерживает 1M контекст без новых мехнизмов attention».

### 39. What is Flash Attention?
- Идеал: an IO-aware attention that computes the same attention math but faster and more memory-efficiently on GPU by tiling and avoiding the full attention matrix in HBM — it does not change the math/result.
- Обязательные пункты:
  - Standard attention is gated by HBM (slow memory accesses) — writes giant N×N scores + N×N output, reads them back.
  - Flash Attention: tiles, processes blocks, skips materializing the giant matrix; recomputes attention scores in fast SRAM instead of reading/writing HBM.
  - Trade-off: less memory traffic, more compute — modern GPUs have plentiful compute.
  - Flash Attention 2 refines further (same core idea, less wasted work).
  - Why: standard attention memory/time grows; flash approach enables long-context LLMs.
- Частые ошибки: думать Flash Attention меняет результат/математику.
- Красные флаги: «Flash Attention — это другой тип attention с другими weights», «он тратит больше compute насильно хуже».

### 40. What is Cross-Entropy Loss?
- Идеал: number measuring how wrong the model's predicted probabilities are vs the true answer; the closer to truth, the smaller the loss. Used to train basically every classification model/LLM.
- Обязательные пункты:
  - Given logits, apply softmax → probabilities; take the log of the true class's probability: CE = -log(p_true).
  - Only the true class probability matters (others contribute via the normalizing sum).
  - Full cross-entropy H(p,q) = expected -log q over true distribution p; it's ≥ H(p) (KL non-negative).
  - The formula: p_i = exp(z_i)/Σexp(z_j); CE = −log p_true. Training minimizes CE → maximizes log-likelihood of the right answer.
  - Also: penalty — the worse the model, higher loss; used as the standard loss in next-token prediction.
- Частые ошибки: вычислять CE по всем классам а не по истинному; путать CE с softmax.
- Красные флаги: «CE = сумма вероятностей всех классов», «если модель уверена — loss большой».

