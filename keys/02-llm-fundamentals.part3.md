# LLM Fundamentals — Answer Key (61-80)

### 61. Your chatbot loses context after 10 turns in a conversation. How do you maintain a long conversation context?
- Идеал: Manage AI agent memory around the stateless LLM: extract, store and retrieve the right context each turn.
- Обязательные пункты:
  - The LLM remembers nothing between calls — memory is a system you build around it (summaries/entities, not raw history).
  - Use the four core operations: write, read, update, forget.
  - Keep context small and relevant: compact or retrieve instead of re-sending the whole transcript.
- Частые ошибки: sending the full raw history every turn — blows context, costs tokens, degrades quality (context rot).
- Красные флаги: «просто растяни контекст — и всё решится»; «LLM сам помнит прошлое».

### 62. Your chatbot fails when users switch topics mid-conversation. How do you handle topic switches?
- Идеал: Detect the switch and rebuild the prompt for the new topic, keeping only durable context and dropping stale turns from the generation focus.
- Обязательные пункты:
  - Update memory: swap working context to the new topic; keep long-term facts that apply across topics.
  - Retrieve the new topic's relevant context instead of pushing old history.
  - The model sees the minimal current slice, not the whole prior conversation.
- Частые ошибки: lazy concatenation of all history into one prompt.
- Красные флаги: «переключение темы — это баг модели»; «просто увеличь лимит контекста и всё само решится».

### 63. Your QA system always generates an answer even when no answer exists in the context. How do you detect unanswerable questions?
- Идеал: Make abstention a designed, tested behavior: the model may refuse when context lacks support, and the pipeline verifies grounding before showing an answer.
- Обязательные пункты:
  - Instruct the model: if the context contains no answer, say so — evaluate the refusal path too.
  - Grounding check: verify the generated claim is supported by the given context (a judge pass) and abstain otherwise.
  - In RAG, pre-check retrieval: if top chunks lack the asked entity, flag before generation.
- Частые ошибки: no abstention instruction; measuring only answer correctness; letting the model guess from missing evidence.
- Красные флаги: «модель обязана всегда дать ответ»; «нет ответа — это баг кода, а не дизайн».

### 64. Your summarization system hallucinated facts not in the original article. How do you fix it?
- Идеал: Fix faithfulness at the system level — ground the summary in the source and verify it before shipping.
- Обязательные пункты:
  - Faithfulness check: every summary claim must be traceable to the source (verifier/judge pass on output).
  - Add a grounding constraint at generation: «summarize only what the article says».
  - Evaluate with entailment/faithfulness metrics, not just ROUGE.
- Частые ошибки: only regenerating and hoping; judging by fluency alone.
- Красные флаги: «просто подними температуру — станет точнее»; «галлюцинация — это баг API, а не процесс работы модели».

### 65. Your text generation repeats phrases in long outputs. How do you fix repetition?
- Идеал: Fix repetition at decoding time — repetition-aware penalties and better sampling, a cheap decode-side fix rather than a retrain.
- Обязательные пункты:
  - Apply presence/frequency penalties to logits: already-emitted tokens get scaled down so loops don't reinforce themselves.
  - Tune sampling (temperature/top-p) and no-repeat n-grams so long outputs stay diverse.
  - Check decode parameters and output budget before fine-tuning.
- Частые ошибки: raising temperature blindly or dropping penalties; blaming the model for a decode-strategy issue.
- Красные флаги: «переобучь модель, чтобы не повторялась»; «это баг serving-фреймворка, а не мой decode».

### 66. Transformers work on text, so can they also understand images?
- Идеал: Yes — a Vision Transformer (ViT) treats an image like text: split into patches, embed each as a token, run through a transformer encoder to classify.
- Обязательные пункты:
  - Image → patches (e.g. 16×16×3) → flatten → linear projection into patch embeddings (visual tokens).
  - A learnable CLS token attends to all patches and yields the final image representation.
  - Position embeddings preserve spatial layout; then a standard transformer encoder.
- Частые ошибки: думать, что трансформер обрабатывает пиксели напрямую; забыть CLS-token.
- Красные флаги: «ViT читает картинку как OCR-текст, токенизируя в слова»; «ViT — это просто CNN в другом виде».

### 67. Small Language Models (SLMs)
- Идеал: An SLM is a language model typically under 10B parameters — a deliberate trade of broad knowledge and deep reasoning for speed, low cost, privacy, on-device deployment.
- Обязательные пункты:
  - «Small» = design choice: fewer parameters, less capacity; quality per parameter via distillation from larger teachers, better optimizers, longer training.
  - Why: lower cost (100×–200× cheaper per token), lower latency, on-device/offline (GGUF), privacy/control.
  - Best for narrow, latency- or privacy-sensitive tasks (routing, classification, extraction); keep an LLM for broad knowledge and hard reasoning.
- Частые ошибки: считать SLM «маленькой LLM без минусов»; пропускать distillation.
- Красные флаги: «SLM ничем не хуже большой на любой задаче»; «SLM — только для телефона».

### 68. Large Reasoning Models (LRMs)
- Идеал: An LRM first produces a long internal reasoning trace, then a final answer — trading latency and cost for higher accuracy on hard multi-step problems.
- Обязательные пункты:
  - Pipeline: [question] → [long trace] → [short answer]; trace often hidden.
  - Test-time compute: more thinking → higher accuracy (o1 AIME improves with attempts), at 10×–30× cost and 10–120 s latency.
  - Training: RL with verifiable rewards via GRPO (RLVR) on reasoning traces.
  - Use for math/code/logic/planning; plain LLM for cheap fast chat.
- Частые ошибки: думать, что reasoning — магия, а не токены; не упоминать trade-off.
- Красные флаги: «LRM лучше всегда и везде»; «trace скрыт — значит модель не думает».

### 69. Jev and System One Models
- Идеал: Jev is a System One Model: it generates no text, takes a state plus questions with allowed answers, and returns typed decisions with calibrated probabilities in one pass.
- Обязательные пункты:
  - Typed answers: choice (≤255), number (range), yes/no — each with a probability; shape fixed before the model runs, so output can't be malformed.
  - Answers many questions in a single pass: ~70–500 ms, up to ~200× faster, free output.
  - «Cannot hallucinate» means no invented options and honest uncertainty.
- Частые ошибки: чатиться с ним как с LLM; ждать связный текст.
- Красные флаги: «Jev — это LLM, который пишет быстрее токеном за токеном»; «System One — просто маркетинговый термин».

### 70. What are Autoregressive Models?
- Идеал: A model that generates one token at a time by predicting the next token from all previous ones — the way GPT-style models write.
- Обязательные пункты:
  - Chain rule: P(x1..xn) = P(x1)·P(x2|x1)·…·P(xn|x1..x(n-1)).
  - Generation loop: past → model → next-token probabilities → sample → append → repeat until <end>.
  - Needs causal masking so the model never sees future tokens during training.
  - KV cache reuses past keys/values each step.
  - Pros: quality, streaming. Cons: slow sequential generation.
- Частые ошибки: confusing it with non-autoregressive parallel generation; omitting masking.
- Красные флаги: «LLM пишет весь ответ за один проход»; «модель может подсмотреть следующий токен — это нормально».

### 71. Explain the difference between autoregressive and masked language modeling.
- Идеал: Autoregressive (causal) models predict token-by-token left-to-right with causal masking and generate text; masked LM (BERT-style) fills masked tokens using bidirectional context and is used for understanding, not generation.
- Обязательные пункты:
  - Autoregressive: predict next token given past, one direction, causal mask, decoder-only — good for generation.
  - Masked LM: mask tokens, predict from both directions, encoder-only — good for representations/understanding.
  - Choice depends on the task: generation vs embeddings/classification.
- Частые ошибки: говорить, что BERT тоже генерирует текст; путать random mask и causal mask.
- Красные флаги: «masked LM — то же, что autoregressive, просто с маской»; «BERT генерирует, как GPT».

### 72. Proximal Policy Optimization (PPO)
- Идеал: PPO improves a policy (the LLM) in small, safe steps — the key is clipping, keeping the new policy close to the old one and stabilizing RLHF.
- Обязательные пункты:
  - Objective: L = min(ratio·advantage, clipped_ratio·advantage); epsilon ≈ 0.2.
  - Advantage comes from a value model (critic) — better/worse than expected.
  - In RLHF: policy=LLM, reward model scores responses, frozen reference adds KL penalty, critic predicts reward.
  - Clipping prevents large jumps; data is reused for multiple updates.
- Частые ошибки: не упоминать critic; утверждать, что PPO «убирает» reward model.
- Красные флаги: «PPO делает гигантские шаги, чтобы быстрее сойтись»; «у PPO нет reward model».

### 73. Direct Preference Optimization (DPO)
- Идеал: DPO trains an LLM directly on human preference data (chosen vs rejected) without a separate reward model and without RL — the model is its own reward model.
- Обязательные пункты:
  - Preference data: prompt + chosen + rejected response.
  - Loss: L = -log sigmoid(beta·(log_ratio_chosen − log_ratio_rejected)); a frozen reference model anchors the update; beta controls how far the new model may move.
  - vs RLHF/PPO: no reward model, no value model, no RL loop — it's supervised; simpler, stable, cheaper. Still needs preference pairs and a decent starting model.
- Частые ошибки: думать, что DPO обходится вообще без человеческих данных.
- Красные флаги: «DPO не нужен reference model»; «DPO — это PPO с другим именем».

### 74. Group Relative Policy Optimization (GRPO)
- Идеал: GRPO is a cheaper alternative to PPO for LLM RL: it drops the value model and uses the average reward of a group of answers to the same question as baseline.
- Обязательные пункты:
  - The critic (value model) is nearly as big as the policy — GRPO keeps the reward model but drops the critic.
  - Generate a group (8–64) per question → score each → group mean as baseline → advantage = (reward − mean)/std → clip + KL penalty vs reference.
  - Lower memory/compute; best for reasoning with verifiable rewards.
- Частые ошибки: думать, что GRPO без наград; путать reward model и value model.
- Красные флаги: «GRPO убирает reward model»; «GRPO — это PPO».

### 75. Recursive Language Models (RLMs)
- Идеал: An RLM processes inputs larger than the context window by recursively calling another model (or itself) on smaller pieces — the main model writes and runs code to split the input instead of reading it all.
- Обязательные пункты:
  - Full input stays in a Python environment; the model writes code calling call_llm on parts, gets short answers, combines them.
  - Recursion: a sub-call may itself be an RLM, forming a tree of small calls.
  - Avoids context rot / lost-in-the-middle; more flexible than fixed chunking.
- Частые ошибки: называть RLM просто «RAG».
- Красные флаги: «RLM скармливает весь документ за один проход»; «RLM — это жёсткое chunking с другим именем».

### 76. Continual Learning in LLMs
- Идеал: Continual learning lets an LLM learn new information over time without forgetting old knowledge — the core challenge being catastrophic forgetting.
- Обязательные пункты:
  - Catastrophic forgetting: updating parameters on new data overwrites old knowledge.
  - Approaches: replay (mix old+new data — simple but costly); regularization/EWC (protect important parameters); parameter isolation (freeze originals, train small additions — LoRA, cheap).
  - RAG is an alternative: keep the model frozen and feed new knowledge from an external store — no forgetting.
  - Hard: stability vs plasticity, evaluation, data quality.
- Частые ошибки: считать, что fine-tune на новых данных не тронет старое.
- Красные флаги: «continual learning — синоним fine-tuning»; «догнать на свежих данных достаточно».

### 77. What is Recursive Self-Improvement (RSI)?
- Идеал: RSI is a loop in which an AI improves its own abilities and, being improved, gets better at improving — each round is run by a smarter worker than the last.
- Обязательные пункты:
  - Loop: evaluate self → find weakness → propose change → train/test → keep/discard → repeat with the improved version (recursive).
  - Two kinds: better at the task vs better at improving — only the second makes it truly recursive.
  - Today: partial (self-play like AlphaGo Zero); no fully human-free RSI exists.
  - Keep humans in the loop.
- Частые ошибки: считать RSI уже свершившимся; игнорировать «better at improving».
- Красные флаги: «RSI уже случилось»; «любое улучшение модели автоматически рекурсивно».

### 78. How do Diffusion Language Models (DLMs) work?
- Идеал: A DLM generates text by starting from pure noise (all words masked) and iteratively cleaning it into a meaningful sentence — it guesses all positions at once, so it can be parallel and fast.
- Обязательные пункты:
  - Forward phase (training only): add noise by masking words; reverse: the model learns to predict hidden words.
  - Generation: start fully masked → guess all words in one pass → keep confident ones, blank the rest → repeat until unmasked.
  - Contrast with autoregressive LLMs: refines the whole sequence in parallel.
  - Promising but still maturing.
- Частые ошибки: описывать DLM как autoregressive generation.
- Красные флаги: «DLM — это GPT, который пишет слова по-другому»; «диффузия — только для картинок».

### 79. How Does LLM Watermarking Work?
- Идеал: LLM watermarking hides a signal inside generated text: the secret key + context picks a preferred token list each step, probabilities are tilted toward it, and a detector with the key verifies the source.
- Обязательные пункты:
  - The LLM samples each token from probabilities — that freedom hides the signal.
  - Secret key = reproducible seed: key + context → preferred vs other tokens → small boost → sampled token.
  - Preferred set changes every step, so no pattern without the key.
  - Detection: re-derive the split with the key, measure over-representation; editing degrades it.
- Частые ошибки: путать с AI-detector — watermark требует ключ.
- Красные флаги: «watermark видно глазами и убирается синонимами».

### 80. How do RNNs and Transformers differ?
- Идеал: An RNN reads a sequence one word at a time carrying a hidden state; a Transformer reads the whole sequence at once and uses attention so every token can look directly at every other.
- Обязательные пункты:
  - RNN: sequential, step-by-step hidden state; slow (no parallel) and fades on long-range dependencies.
  - Transformer: parallel processing, attention gives direct long-range links — why modern LLMs are Transformers.
  - RNNs suit simple/streaming/short sequences; Transformers win for scale and long context.
  - Attention is O(n²) — hence optimizations (Flash Attention, sliding window, KV cache).
- Частые ошибки: не упоминать long-range issue in RNN.
- Красные флаги: «Transformer обрабатывает слова по одному, как RNN, но с вниманием»; «RNN надёжнее на длинных последовательностях».
