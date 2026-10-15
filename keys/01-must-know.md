# Must Know — Answer Key (1-6)

### 1. LLM
- Идеал: LLM — large language model trained on huge text corpora to predict next token; "large" → scale + emergent abilities (reasoning, instruction following).
- Обязательные пункты:
  - Transformer architecture, attention over tokens.
  - Trained via self-supervised next-token prediction, then instruction tuning (+ RLHF) to align.
  - Why it matters: one model handles many NLP tasks without per-task engineering.
  - Пример: GPT-4 / Claude answer questions, summarize, write code.
- Частые ошибки: думать, что LLM "знает" — model has no structured database; next-token prediction ≠ knowledge retrieval. Контекстное окно ограничено.
- Красные флаги: «LLM = поисковик по интернету», «модель хранит базу знаний».

### 2. RAG
- Идеал: Retrieval-Augmented Generation — inject retrieved external knowledge into the prompt to ground answers.
- Обязательные пункты:
  - Pipeline: embed query → vector search over document chunks → prepend top-k chunks to prompt → LLM answers from them.
  - Why: reduces hallucination, covers fresh/private data, no retraining, cite sources.
  - Tradeoffs: chunk quality, embedding mismatch, re-ranking, retrieval latency.
  - Пример: chatbot over company docs answers with citations.
- Частые ошибки: путать RAG с fine-tuning (RAG не меняет веса модели); возвращать найденное без синтеза; плохие чанки.
- Красные флаги: «RAG дообучает модель»; уверен, что ретривер не важен.

### 3. MCP
- Идеал: Model Context Protocol — open standard (Anthropic) for connecting LLMs/apps to external tools, backends, data sources.
- Обязательные пункты:
  - Client–server: MCP host/client (e.g. Claude Desktop, an app) ↔ MCP server exposing tools/resources/prompts over JSON-RPC.
  - Why: tool integration once, reuse everywhere; replaces ad-hoc plugins/auth per integration.
  - Пример: MCP server for filesystem or GitHub — model calls it as a tool.
- Частые ошибки: путать MCP с API; думать, что это способ дообучения модели.
- Красные флаги: «MCP = протокол денормализации», не упомянуть стандарт/универсальность.

### 4. Agent
- Идеал: autonomous system where LLM plans and executes multi-step tasks using tools and memory, with reflection on results.
- Обязательные пункты:
  - Loop: goal → plan → tool calls → observe → replan (ReAct pattern).
  - Components: LLM brain + tools + memory + environment.
  - Why: goes beyond single-turn chat to goal-driven multi-step execution.
  - Пример: coding agent that browses repo, edits files, runs tests iteratively.
- Частые ошибки: агент = просто промпт с инструментами; не упоминать цикл plan-act-observe.
- Красные флаги: «агент сам учится» (не обучение), «полностью автономен» без ограничений.

### 5. Fine-tuning
- Идеал: further training on an already-pretrained base model with a smaller, task-specific dataset to specialize it.
- Обязательные пункты:
  - Full fine-tuning updates all weights; LoRA updates low-rank adapter — cheaper, reversible.
  - Why: better domain accuracy/style over prompting alone; but costs GPU time.
  - When vs RAG: RAG for dynamic/factual freshness; FT for fixed style/format/behavior.
  - Пример: fine-tune on legal documents so model uses that terminology.
- Частые ошибки: думать, что fine-tuning only way to improve; fine-tune on small bad data → overfit.
- Красные флаги: «fine-tuning = RAG», не знать LoRA/qlora.

### 6. Quantization
- Идеал: reduce precision of model weights (fp16 → int8/4bit) to shrink memory and speed inference.
- Обязательные пункты:
  - Why: models too big for consumer GPUs; space/speed trade-off for slight accuracy loss.
  - Types: post-training quantization (PTQ), quantization-aware training (QAT); GGUF (llama.cpp), GPTQ, AWQ.
  - Пример: Llama-2-70B from ~140 GB fp16 → ~35 GB 4-bit, runnable on a single consumer GPU.
- Частые ошибки: думать, что цель — улучшить качество (это сжатие, качество обычно чуть падает).
- Красные флаги: «квантование ускоряет ТОЛЬКО за счёт потери качества», путать с дистилляцией (разные вещи).
