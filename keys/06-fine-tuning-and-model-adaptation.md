
# Fine-Tuning and Model Adaptation — Answer Key (all 32)

### 1. What is fine-tuning, and when should you fine-tune an LLM?
- Идеал: taking an already-trained (pre-trained/foundation) model and training it a bit more on your own task data so it becomes good at your specific task, instead of training from scratch.
- Обязательные пункты:
  - Weights = the model's "knowledge"; fine-tuning slightly adjusts these numbers on your examples via prediction, loss, backprop + gradient descent, repeated over epochs.
  - Use when you must change behavior/style/skill that a prompt can't give: brand voice, strict medical/legal format, proprietary terminology, task mastery (e.g. InstructGPT made GPT-3 follow instructions).
  - Do NOT fine-tune just to add facts; give facts in the prompt / RAG instead. Fine-tuning changes behavior, not a way to feed data.
- Частые ошибки: думать что fine-tuning = RAG/промпт; тратить ресурсы на FT ради фактов, которые проще добавить в контекст.
- Красные флаги: fine-tuning заменяет pre-training/data; без FT модель не знает ничего.

### 2. Explain the difference between full fine-tuning and parameter-efficient fine-tuning (PEFT).
- Идеал: full FT updates every weight in the model (deep changes, high memory/compute, one huge copy per task); PEFT freezes the base and trains only a tiny set of extra parameters (memory- and cost-light, one shared base + small adapters per task).
- Обязательные пункты:
  - Full: high memory, slow, expensive; can learn deeply; 10 tasks = 10 giant model copies.
  - PEFT (LoRA, prefix/prompt tuning, adapters): <1% trainable params, low memory/cost, shared base.
  - Choose based on use case/resources: limited machines, LoRA/PEFT; deep changes + heavy resources, full.
- Частые ошибки: думать что PEFT всегда хуже по качеству или меняет архитектуру; считать full FT обязательным.
- Красные флаги: PEFT = обучение одного вектора эмбеддинга; full FT не требует памяти на градиенты.

### 3. What is LoRA (Low-Rank Adaptation), and how does it work?
- Идеал: LoRA freezes original weights and learns a small low-rank update dW = B*A on the side; A (random init) and B (zero init) are trained, base stays untouched.
- Обязательные пункты:
  - Rank r (8-64 typical) controls trainable params/capacity; trainable params drop ~100-1000x.
  - B zero-init so training starts exactly from the pre-trained model; only A/B train.
  - Can be merged into original weights after training, zero extra inference latency; unmerged adapters allow swapping many tasks on one base (adapter is few MB vs multi-GB).
  - Used for LLMs, image models (Stable Diffusion), domain/style adaptation; foundation of QLoRA.
- Частые ошибки: считать что обучается вся матрица; не знать про merge и что B инициализируется нулями.
- Красные флаги: LoRA обучает низкоразрядную копию весов; rank = количество слоёв.

### 4. What is QLoRA, and how does it enable fine-tuning on consumer hardware?
- Идеал: QLoRA = LoRA + 4-bit quantization of the frozen base model, so large models can be fine-tuned on a single consumer GPU.
- Обязательные пункты:
  - Base weights stored/trained in 4-bit (quantized); LoRA adapter learns the adjustments.
  - Dramatically cuts memory vs full FT / plain LoRA (7B weights ~4.5GB in NF4, fits a single consumer GPU like a 24GB card).
  - LoRA is the building block: LoRA + 4-bit quant = QLoRA.
- Частые ошибки: путать QLoRA с инференс-квантизацией; думать что квантится обучаемая LoRA-часть.
- Красные флаги: QLoRA обучает 4-битные веса; QLoRA не требует LoRA.

### 5. How does fine-tuning work?
- Идеал: pick pre-trained base, prepare task dataset (input + correct output), feed examples (model predicts), measure loss (how wrong), adjust weights via backprop/gradient descent by lr-scaled steps, repeat over epochs until loss small.
- Обязательные пункты:
  - Worked example: weight w=2.0, input 4, answer 10, pred 8, error 2, adjustment = lr*error*input, converges 8,9.6,9.92,10; real models do this for billions of weights.
  - Data quality matters most: small clean set beats large messy set; consistent style.
  - Full FT updates all weights; LoRA trains small extra weights; always test on unseen examples (did it learn or memorize).
- Частые ошибки: пропускать этап предсказание->loss; не упоминать learning rate и эпохи.
- Красные флаги: fine-tuning не меняет веса; достаточно один раз показать данные.

### 6. Explain Prefix Tuning and Prompt Tuning. How are they different from LoRA?
- Идеал: both are PEFT, the LLM stays frozen and only a tiny set of soft parameters trains; they differ from LoRA which learns weight update matrices.
- Обязательные пункты:
  - Prefix Tuning: learn a block of virtual tokens (pure numbers, NOT words, not input) injected at EVERY layer as extra keys/values in attention; only prefix trains, model frozen.
  - Prompt Tuning: learn only a trainable soft prefix appended to input embeddings (no per-layer K/V injection).
  - Prefix Tuning uses a reparameterization trick (small MLP producing K/V) for stability (prefix_projection in peft, off by default); trains well under 1% of params; one shared model + one tiny prefix per task.
- Частые ошибки: думать префикс - слова в промпте; считать Prompt Tuning тем же, что Prefix; игнорировать что LoRA меняет веса.
- Красные флаги: prefix = текст перед предложением; Prompt Tuning требует отдельную копию модели.

### 7. What is adapter-based fine-tuning?
- Идеал: insert small trainable adapter modules (extra layers) into the frozen transformer and train only those; base stays frozen, adapters carry task knowledge (parameter-isolation family).
- Обязательные пункты:
  - Part of PEFT: cheap, low memory, shared base + per-task adapters; related to continual learning (frozen base + new params); LoRA is a low-rank adapter variant.
  - Adapter swapping: serve many tasks from one base by loading the right adapter; keep unmerged for easy swapping.
- Частые ошибки: путать адаптеры и LoRA как взаимоисключающие; считать что база тоже обучается.
- Красные флаги: adapter training fully retrains the model; адаптеры всегда добавляют latency.

### 8. Explain the difference between pre-training, supervised fine-tuning (SFT), and preference optimization (RLHF/DPO).
- Идеал: three stages with different goals/data: pre-training = learn language on huge internet text; SFT = imitate good human-written answers on a small high-quality set; preference optimization = learn human preferences (RLHF reward model + PPO, or DPO directly on pairs).
- Обязательные пункты:
  - Pre-training (GPT-3): next-word prediction on internet text, raw language skill, but can't follow instructions (misalignment: continues the "explain" pattern instead of answering).
  - SFT (~13k examples in InstructGPT): imitate good answers/style, teaches instruction-following baseline, not enough alone.
  - RLHF/DPO: SFT then Reward Model on human-ranked pairs (Bradley-Terry) then PPO with KL; DPO does it in one supervised step without reward model.
- Частые ошибки: пропускать SFT как основу; смешивать pre-training objective с alignment.
- Красные флаги: alignment заменяет pre-training; SFT достаточно без preference optimization.

### 9. What is RLHF (Reinforcement Learning from Human Feedback), and how is it used to align LLMs?
- Идеал: RLHF is a 3-stage pipeline converting human preferences (which answer is better) into a reward signal guiding RL, making the LLM helpful, honest, harmless.
- Обязательные пункты:
  - Stage 1 SFT: fine-tune base on high-quality human prompt-response pairs (10k-100k) to imitate good answers.
  - Stage 2 Reward Model: humans rank responses (4-9 per prompt, C(4,2)=6 .. C(9,2)=36 pairs), train an RM scoring (prompt,answer) to a single number; objective pushes winner's score above loser (loss = -log sigmoid(r_w - r_l); Bradley-Terry).
  - Stage 3 PPO RL: policy (LLM) generates, RM scores, PPO nudges weights; adds KL penalty vs reference/SFT model to prevent drift/reward hacking; final reward = RM score - beta*KL.
- Частые ошибки: пропускать SFT и RM; не упоминать reward hacking и KL.
- Красные флаги: RLHF = просто ранжирование ответов без RL; reward model не нужен.

### 10. What is Deep RL from Human Preferences, the paper that started RLHF?
- Идеал: 2017 paper by Christiano, Leike (OpenAI + DeepMind) that learns a reward from human pairwise comparisons instead of hand-writing it; the origin of RLHF.
- Обязательные пункты:
  - Problem: many goals (backflip, good summary) cannot be written as formulas, and bad formulas get hacked (reward hacking).
  - Human compares short trajectory clips (1-2s) side by side (pick better / equal / cannot tell); no numbers.
  - Reward model predicts per-step reward, clip total = sum; Bradley-Terry formula turns two totals into preference probability; trained with cross-entropy to match human picks.
  - Agent then trained with ordinary RL (A2C for Atari, TRPO for robots, PPO today); backflip from ~900 comparisons, <1% feedback on complex tasks; sometimes beats true reward.
- Частые ошибки: не знать что идея (не текст-речард, а сравнение); думать что это придумано для LLM.
- Красные флаги: human gives scores not comparisons; reward gets hand-coded.

### 11. Why did DPO displace PPO-based RLHF at many labs? When is online RL still better?
- Идеал: DPO removes the reward model and RL loop - the LLM is its own reward model, trained directly on preference pairs with a single supervised loss - so it is simpler, stable, cheaper, and competitive.
- Обязательные пункты:
  - PPO-based RLHF needs reward model + value model (critic, ~policy size) + reference model + PPO tuning; expensive, unstable, easy to fail.
  - DPO = one loss (log sigmoid(beta*(log-ratio chosen - log-ratio rejected)) vs reference model), supervised; no RM, no RL, lower memory/compute, stable.
  - When online RL still wins: exploration and when you need maximum performance on complex tasks; PPO lets model explore responses it was not shown, DPO only learns from given pairs and can overfit; DPO needs good instruction-tuned start + paired data quality + beta tuning.
- Частые ошибки: думать DPO убирает human preference data; не знать что DPO нужен reference model как safety anchor.
- Красные флаги: DPO умеет explore; DPO не требует качественных пар.

### 12. What is instruction tuning, and why is it important for chat models?
- Идеал: fine-tuning the model on instruction-response examples so it follows requests instead of continuing the pattern (SFT stage of InstructGPT); this is what turned GPT-3 into an assistant.
- Обязательные пункты:
  - GPT-3 predicted next word on internet text; asked "explain X to a 6yo" it continued with more "explain..." lines; perfect next-word, useless answer = misalignment.
  - SFT: ~40 labelers wrote ~13k good prompt-answer examples; model imitates them (plain supervised learning) - learns to follow instructions and answer style.
  - Foundation for later stages (reward model + PPO); InstructGPT (even 1.3B) preferred over 175B GPT-3; 175B InstructGPT preferred ~85% of the time over 175B GPT-3, hallucination 21% vs 41%.
- Частые ошибки: не связывать instruction tuning с SFT; думать что pre-training уже учит инструкциям.
- Красные флаги: достаточно одного промпта вместо SFT; instruction tuning не влияет на hallucinations.

### 13. How do you prepare a dataset for fine-tuning an LLM?
- Идеал: curate a task-matched, high-quality, deduplicated set of (instruction/prompt, correct response) examples; quality beats quantity, consistency beats variety.
- Обязательные пункты:
  - Format: instruction + input + expected output (chat format with system/user/assistant turns if chat model); one style per dataset.
  - Cleaning: dedup near-identical samples, remove wrong/hallucinated answers, filter profanity/PII, check diversity/coverage of intents and edge cases, stratify train/valid/test (no leakage).
  - Scale: small clean sets (hundreds to tens of thousands) often enough for behavior/style; more for task mastery; augmentation or synthetic data to expand; human review of a sample to verify quality.
- Частые ошибки: dump raw scraped data without cleaning; unbalanced data; test leakage.
- Красные флаги: больше данных всегда лучше; разметку можно не проверять.

### 14. What is catastrophic forgetting, and how do you prevent it during fine-tuning?
- Идеал: catastrophic forgetting = the model overrides old knowledge while learning new data (e.g. trained only on Sports forgets Math/History/Science); prevent by continual-learning techniques.
- Обязательные пункты:
  - Replay / data mixing: mix new data with old/sample of original data (simple, effective, but higher training cost).
  - Regularization-based (EWC): protect important parameters from changing too much when training on new data (no old data storage, but hard to pick importance balance).
  - Parameter isolation (LoRA/adapters/prefix): freeze original params, train only small new params - old knowledge fully preserved, cheap, but model grows with tasks.
  - RAG as alternative: keep model unchanged, feed new knowledge from an external store (no forgetting, but model doesn't truly learn).
- Частые ошибки: думать forgetting неизбежен без мер; игнорировать stability-vs-plasticity tradeoff.
- Красные флаги: решением является только переобучение с нуля; forgetting это про шумные данные.

### 15. When should you choose fine-tuning over RAG over prompt engineering?
- Идеал: prompt engineering for quickest change of behavior/few examples; RAG when you need up-to-date or private facts in context without retraining; fine-tuning when you must change the model's behavior/style/task mastery that prompting can't express.
- Обязательные пункты:
  - Prompt first: cheapest, no training; enough for style nudges and facts with few examples; try before FT.
  - RAG: external knowledge (updates, private docs) added at query time, no retraining, avoids forgetting; model doesn't truly learn, answers only what's in context.
  - Fine-tuning: brand voice, strict format (medical/legal), proprietary terminology, deep task mastery - behavior changes no prompt/RAG can give; costs training/hardware.
- Частые ошибки: сразу FT там, где достаточно промпта/RAG; RAG когда нужно изменить поведение.
- Красные флаги: FT нужен всегда; RAG обучениеет модель.

### 16. How do you evaluate a fine-tuned model's performance?
- Идеал: evaluate on task-specific held-out data before/after FT using a mix of automatic metrics, benchmarks, human eval, and LLM-as-a-judge.
- Обязательные пункты:
  - Automatic metrics: BLEU/ROUGE (surface similarity), BERTScore (semantic), METEOR, perplexity, Exact Match; fast, cheap, but don't capture meaning; weak for open-ended.
  - Benchmarks: MMLU, HellaSwag, HumanEval/MATH/GSM8K, TruthfulQA, IFEval; watch saturation and contamination.
  - Human eval: gold standard - Likert rating, pairwise comparison (Chatbot Arena), error annotation; slow/expensive.
  - LLM-as-a-judge: scalable proxy, but has position/verbosity/self-preference bias; validate against human labels on a sample (agreement).
  - Task-specific: e.g. RAGAS (context precision/recall, faithfulness, answer relevance) for RAG; compare FT vs base vs baseline.
- Частые ошибки: eval только на train split; полагаться на один метрик без human/judge validation.
- Красные флаги: BLEU отлично оценивает креатив; high benchmark score = good in production.

### 17. What is synthetic data generation, and how do you use it for fine-tuning?
- Идеал: use an LLM (or generator) to create or expand training examples (synthesize instruction-response pairs, paraphrases, domain text) to scale/cheapen data for fine-tuning.
- Обязательные пункты:
  - How: use a strong LLM to write new prompt-response pairs from seeds, generate rephrasings, transform human drafts, create SFT data or preference pairs; add validation to filter low-quality/failed generations.
  - Use for: expanding small golden sets, domain coverage, style transfer, synthetic preference data (can replace much human labeling - AI feedback, RLAIF); must be grounded/verified, deduplicated, and human-audited.
- Частые ошибки: использовать грязный/непроверенный синтетический шум без фильтрации; верить качеству без выборочного human review.
- Красные флаги: синтетика заменяет всю разметку без проверки; больше синтетики всегда лучше.

### 18. What are the key hyperparameters for fine-tuning (learning rate, epochs, batch size, LoRA rank)?
- Идеал: small learning rate (slow incremental nudges; LoRA typical small lr like ~1e-4-2e-4), few epochs (1-3 for SFT, avoid overfitting), moderate batch size (batch size/grad accumulation per update), LoRA rank r = 8-64.
- Обязательные пункты:
  - Learning rate: controls step size; too big over-corrects/unstable, too small slow; often lower than pre-training.
  - Epochs: 1-3 typical for SFT; watch val loss to avoid memorization.
  - Batch size + gradient accumulation; affects stability and memory (trade memory vs compute).
  - LoRA rank as most important LoRA hyperparameter; smaller r = fewer trainable params/faster but less capacity; larger r = more capacity, less efficient.
  - Also: warmup, weight decay, adapter target modules, lr for adapters.
- Частые ошибки: большой lr на все веса; много эпох на маленькой выборке; игнорировать что rank влияет на capacity/efficiency tradeoff.
- Красные флаги: чем больше rank, тем всегда лучше; обучать много эпох на шумной выборке.

### 19. Do the GPU memory math for full fine-tuning a 7B model in bf16 with Adam. Now with LoRA and QLoRA.
- Идеал: full FT memory = weights (14GB bf16) + gradients (14GB bf16) + Adam optimizer states (fp32 moments ~56GB) ≈ 84GB + activation/overhead → beyond one consumer GPU; LoRA trains ~1% params, base frozen; QLoRA NF4 fits a single consumer GPU.
- Обязательные пункты:
  - Per-param bf16 = 2 bytes; 7B params → 14GB weights, 14GB gradients; Adam keeps two fp32 moments → 8 bytes/param → 56GB; total ≈ 84GB + activations (activations scale with sequence length/batch) → ~100GB+; need multiple datacenter GPUs.
  - LoRA: ~1% of params trainable (≈70M for 7B at rank 64 ≈ 0.14GB); base 14GB frozen + small optimizer → few GB extra, fits single 24GB consumer GPU; also lower activation memory since only adapter needs grads.
  - QLoRA: base in NF4 4-bit (~4.5GB for 7B), LoRA adapter + paged optimizer → fits single consumer GPU (24GB); weight memory shrinks ~3x vs bf16 base.
  - Comparison: full FT ≈ 84GB+ vs LoRA few GB trainable vs QLoRA ~4.5GB base weights.
- Частые ошибки: забыть про optimizer states (Adam = 2 fp32 моментов); считать только weights (14GB) и думать что достаточно одной карты 16GB.
- Красные флаги: «7B = 14GB, значит хватит одной карты», не учитывать gradient/optimizer memory.

### 20. How do you fine-tune a model for a specific domain (legal, medical, finance)?
- Идеал: collect high-quality domain data, format into instruction-following pairs, start with LoRA on a strong base, validate with domain experts.
- Обязательные пункты:
  - Data: domain documents + Q&A pairs; extract from sources or synthesize, deduplicate, human-review for accuracy (errors get baked in).
  - Model: good base (already multilingual/strong), apply SFT on (task, format) pairs; use LoRA first for cost; full FT if deep restructure needed.
  - Validation: domain-specific eval (expert review, held-out domain benchmark), hallucinations/legal hallucination checks, guardrails: fine-tune for behavior, RAG for facts, and add a strict output/safety layer (domain wording for legal/medical).
- Частые ошибки: слепо обучать на сырых юридических/медицинских текстах без контроля качества; думать FT даёт гарантии фактов.
- Красные флаги: модель после FT = источник юридической истины; никакая проверка не нужна.

### 21. What is continual pre-training, and when would you use it?
- Идеал: continuing to train an already pre-trained model on new (often domain/up-to-date) raw text to update its knowledge, rather than training from scratch.
- Обязательные пункты:
  - Difference from fine-tuning: continual pre-training is still next-word prediction on large raw text, adding knowledge (domain corpus); fine-tuning is supervised on task pairs.
  - Use when: new domain/up-to-date knowledge (current events, jargon, new languages) needed and base lacks it; cheaper than full retrain.
  - Guard against catastrophic forgetting; can combine with LoRA; alternative is RAG for live facts.
- Частые ошибки: путать continual pre-training с SFT/RAG; игнорировать риск forgetting и стоимость.
- Красные флаги: continual pre-training заменяет SFT; можно бесконечно дообучать без штрафов.

### 22. How do you merge multiple LoRA adapters?
- Идеал: keep adapters separate for serving many tasks (swap them); merging is a one-way operation - add low-rank updates into base weights (W' = W + B*A), so infer with zero extra latency.
- Обязательные пункты:
  - Single adapter merge: W_merged = W + (r-scaled B*A); then can't easily unmerge/swap.
  - Multiple adapters: possible approaches - weighted sum of LoRA deltas (e.g. task arithmetic / linear combination of B*A deltas per layer), concatenation or routing adapters (MoE-style), or train one merged; each keeps separate strengths but can conflict.
  - Tradeoffs: merging reduces serving cost/latency; unmerged keeps flexibility per task.
- Частые ошибки: думать merge обратим; складывать сами адаптеры без учёта весов/масштаба некорректно - конфликты; merge всех адаптеров всегда улучшает всё.
- Красные флаги: merge адаптера обратим; merge бесплатен всегда - нужна настройка/калибровка.

### 23. What is the difference between SFT (Supervised Fine-Tuning) and alignment training?
- Идеал: SFT imitates good answers or instruction-style from labeled pairs (supervised); alignment training (RLHF/DPO) optimizes for human preferences/helpful-honest-harmless, going beyond imitation — usually runs ON TOP of an SFT model.
- Обязательные пункты:
  - SFT: learns distribution of good examples; enough for style/behavior imitation; limited by dataset size (can't write example for every prompt).
  - Alignment/RLHF: reward model + RL (PPO) or DPO with preferences; tunes for deeper goals (helpful, honest, harmless) that can't be enumerated; SFT is a prerequisite.
  - InstructGPT: SFT (13k examples) → RM (ranking) → PPO; a raw base can't be aligned well directly.
- Частые ошибки: называть SFT alignment; думать alignment заменил SFT.
- Красные флаги: SFT учит reward; alignment это просто ещё один слой SFT на предпочтениях.

### 24. What is RLAIF (RL from AI Feedback), and how does it differ from RLHF?
- Идеал: RLAIF = RLHF but the "human" feedback/reward comes from another (strong) LLM acting as judge instead of human labelers; cheaper and faster to scale.
- Обязательные пункты:
  - RLHF: human comparisons → reward model → PPO (the whole 3-stage pipeline, trusted gold standard).
  - RLAIF: an LLM judges/ranks responses (or critiques), used to build preference data/reward model; replaces much human labeling.
  - Same RL machinery, different signal source; AI feedback is "LLM-as-a-judge" for training; part of trend "AI feedback replaces much human labeling".
- Частые ошибки: думать RLAIF меняет RL-алгоритм; не связать с LLM-as-a-judge.
- Красные флаги: RLAIF эффективнее по стоимости; RLAIF = DPO (это источник сигнала, DPO — другой оптимизатор).

### 25. What is Constitutional AI, and how does it differ from RLHF?
- Идеал: Constitutional AI trains the model to align itself using a written list of principles/constitution, and can critique its own answers against those principles (self-critique), an alternative that learns alignment from explicit principles rather than (or in addition to) human preference labels.
- Обязательные пункты:
  - Core: get from Claude/Constitutional AI concept: model critiques and revises its own outputs against a explicit constitution/principles, reducing harm without heavy human feedback; can distill a critique step.
  - Diff vs RLHF: RLHF uses human preferences/reward model; Constitutional AI uses an explicit list of principles + self-critique rather than (or complementing) human labels; AI feedback (RLAIF) also fits "AI feedback" class.
- Частые ошибки: путать Constitutional AI с guardrails/простыми фильтрами; думать принципы не нужны в RM.
- Красные флаги: Constitutional AI = ещё один reward model; принципы не влияют ни на что.

### 26. What is RLVR (Reinforcement Learning with Verifiable Rewards), and when does it beat a learned reward model?
- Идеал: RLVR uses a verifiable reward - checkable ground truth (math answer correct/not, code passes tests, rule-based check) instead of a learned human-preference reward model; powers GRPO-like reasoning training.
- Обязательные пункты:
  - Verifiable reward: math/code/logic where outcome can be definitively checked (rule-based); no opinion needed.
  - GRPO: samples a group of answers, scores each (rule/reward model), uses group average as baseline for relative advantage, no value model/critic; KL penalty vs reference (SFT) model keeps drift in check.
  - Beats learned reward model when: reward is exactly checkable (math, code, logic) and objective is correctness - avoids reward hacking via fuzzy taste model; used in DeepSeek reasoning models and large reasoning model training (GRPO).
- Частые ошибки: не знать GRPO - group relative baseline; думать verifiable reward это LLM-оценка.
- Красные флаги: RLVR применим к творческим задачам; GRPO не нужен reference/KL penalty.

### 27. What is knowledge distillation for fine-tuning, and what are the legal considerations?
- Идеал: distillation trains a small student model to copy the behavior of a large teacher (using soft labels / dark knowledge), for cheaper/faster/edge deployment.
- Обязательные пункты:
  - Teacher (large, slow, accurate) → student (small, fast, cheap); student learns from teacher's soft label probability distributions (not just hard labels) = dark knowledge (relationships between classes).
  - Temperature softmax: raise T during training to reveal soft/dark knowledge, lower T at inference.
  - Loss = weighted blend of distillation loss (student vs teacher soft labels, KL) + normal loss (student vs true labels).
  - Legal considerations: copying a proprietary model's outputs/distribution may breach the API/model's Terms of Service (model distillation to replicate a competitor's product interplay with licensing/toS, IP/copyright on generated data, and license restrictions on derivatives); verify data/model license rights before distilling.
- Частые ошибки: думать distillation = обучение на hard labels; не учитывать license ToS при "перегонке" закрытой модели.
- Красные флаги: distillation всегда легальна; student обучается только на teacher soft labels и не смотрит на truth.

### 28. Your fine-tuned LLM produces factually wrong outputs due to training data quality issues. How do you fix it?
- Идеал: fix the training data pipeline (source correctness), and layer RAG/guardrails to ground facts at inference.
- Обязательные пункты:
  - Audit data: identify wrong/noisy/hallucinated examples, errors in synthetic augmentation, bad formatting; remove or correct them; fix source (or filter output) - data quality is the primary driver.
  - Improve eval: add a held-out factual benchmark to catch regressions.
  - Stop training on the bad labels: fix/correct the dataset, then do a corrective SFT pass on a small verified-clean set.
  - Use RAG to supply correct facts at inference so the model doesn't rely on its (wrongly learned) parametric memory; add output verification/guardrails to catch hallucinations.
- Частые ошибки: только увеличивать датасет, не исправляя ошибки; не отделять факты (RAG) от поведения (FT).
- Красные флаги: «переобучу на том же мусоре ещё раз», «добавлю больше данных того же качества».

### 29. You must choose between LoRA and full fine-tuning for a domain-specific assistant. How do you decide?
- Идеал: base choice on resources, required depth of change, data availability, and serving (multiple tasks vs single deep overhaul).
- Обязательные пункты:
  - LoRA: limited GPU/memory/budget, need to serve many tasks (share base + swap adapters), small domain tweak (style/tone/rules) - fast iteration, low cost; quality often comparable for moderate changes.
  - Full FT: need deep behavioral change or qualify max possible quality, and you have the GPUs/do multiple rounds; expensive, slow, one model per task (huge footprint for many tasks).
  - Decide on: task complexity (does the change need new knowledge/capability vs style), budget/hardware, number of tasks/adapters, data size.
- Частые ошибки: всегда выбирать full FT из-за «лучше качество»; использовать LoRA когда адаптер уже не хватает capacity.
- Красные флаги: «LoRA не может изменить поведение», «full FT всегда нужен для домена».

### 30. Your fine-tuned model memorized training data verbatim instead of learning patterns. How do you fix overfitting?
- Идеал: add regularization, correct/tune data, stop training earlier, use a held-out eval split and watch generalization.
- Обязательные пункты:
  - Reduce model capacity (smaller LoRA rank / fewer trainable params), weight decay, dropout.
  - Fewer epochs / early stopping on validation loss; lower lr; small clean deduplicated dataset (memorization loves noise + duplicates + long epochs); increase data diversity.
  - Evaluate on held-out test (did it learn or memorize): the fine-tuning guide says always test on unseen examples; if it only reproduces training text, cut epochs/regularize.
  - Check for verbatim leakage (train on test / duplicated samples in test set).
- Частые ошибки: продолжать train пока loss не 0; не требовать валидации на невиданных данных; полагать переобучение нельзя исправить.
- Красные флаги: «переобучение = высокий loss на train» (это недообучение); «нужно просто больше эпох».

### 31. Your fine-tuned LLM forgot its general capabilities after domain-specific fine-tuning. How do you fix catastrophic forgetting?
- Идеал: reframe as catastrophic forgetting and apply continual-learning fixes (data mixing / parameter isolation / regularization), plus keep a base eval.
- Обязательные пункты:
  - Data mixing/replay: include a sample of general/old data (or from original distribution) alongside domain data so the model keeps practicing general skills.
  - Parameter isolation: LoRA/adapters/prefix - retrain/adapt with base frozen (old knowledge preserved); this is a primary fix for domain FT forgetting.
  - Regularization (EWC-like): penalize changes to important parameters; balance stability vs plasticity.
  - Evaluate general benchmarks before/after FT to catch regressions; if the forgetting is caused by full FT, restart from a checkpoint and protect via LoRA or data mix.
- Частые ошибки: продолжать domain FT на том же наборе; «откатить к базе» без анализа причины.
- Красные флаги: полагать forgetting неизбежен — есть методы (mixing, isolation, regularization).

### 32. Your RLHF preference data has low annotator agreement. How do you ensure data quality?
- Идеал: tighten labeling protocol, measure/raise agreement, filter/flag low-confidence votes, and improve instruction clarity for annotators.
- Обязательные пункты:
  - Measure agreement (Cohen's kappa / pairwise agreement) and interpret it; low agreement = signal noise, toss or review those pairs.
  - Clear rubric and instructions (what "better" means - helpful/honest/harmless, criteria per dimension); annotator training + calibration; multiple annotators per item with majority/filtering.
  - Include tie/"cannot tell" option rather than forcing pick; review disagreements (expert arbitration); use LLM-as-a-judge only as auxiliary, validate against human labels.
  - Deduplicate, check for position bias/ordering (randomize A/B), monitor per-annotator quality/outliers.
- Частые ошибки: обучать RM на низкокачественных парах; принуждать annotator выбрать победителя без опции «не знаю».
- Красные флаги: «низкое согласие всё равно полезно», «можно игнорировать disagreements, RM вытянет».
