# AI Agents and Agentic Systems — Answer Key (28-53)

### 28. What is the difference between reactive and proactive agents?
- Идеал: Reactive agents answer the current input with no prior state or goal (stimulus → response); proactive agents pursue a persistent goal across steps and act on their own initiative.
- Обязательные пункты:
  - Reactive: stateless, single-turn, react to a trigger; e.g. chatbot, simple QA.
  - Proactive: holds goal + memory, plans multi-step work, initiates actions without a prompt (e.g. monitor-and-alert agent).
  - Proactive needs memory+loop+goal persistence; reactive is cheaper/more predictable.
- Частые ошибки: сводить к «с тулами / без тулов» — суть в инициативе и цели, а не в наличии tool-use.
- Красные флаги: «reactive = ReAct», «проактивный — это просто планирование».

### 29. How do you manage token consumption and cost in long-running agent workflows?
- Идеал: control the loop so context doesn't grow unbounded and calls aren't repeated: compact history, set stop conditions, route models, cache tool results, trim prompts.
- Обязательные пункты:
  - Context compaction: when the window crosses a threshold (~80%), summarize older turns into a short note (same LLM does it) and keep recent messages in full — never just drop old ones (sliding window loses facts and attention-sink tokens).
  - Stop conditions: max iterations + clear "done" criteria so the loop stops.
  - Model routing: big model for reasoning, small/cheap for extraction; cache tool results; concise/dynamic system prompt.
- Частые ошибки: передавать полную историю в каждый вызов; не ставить стоп-условие (50k+ токенов за простой запрос).
- Красные флаги: «решение — урезать промпт», «слайдинг-виндоу без потерь».

### 30. Human-in-the-loop: when is it needed?
- Идеал: pause agent at a decision point, human approves/guides, then resume — valve for risky autonomy.
- Обязательные пункты:
  - Pause-and-resume; checkpoints (e.g. LangGraph); approval for critical actions.
  - Needed: irreversible/financial/legal actions, low confidence, policy, external-facing output.
  - Stay scoped: automate routine steps, escalate only risky ones; timeouts.
- Частые ошибки: over-approval kills autonomy; under-approval on irreversible actions.
- Красные флаги: «HITL = финальное подтверждение ответа», «человек не нужен».

### 31. Guardrails — how to prevent harmful agent actions?
- Идеал: external checks wrapping the LLM: input guardrail before model, output guardrail before delivery/action.
- Обязательные пункты:
  - Types: topic, safety, privacy, format, factual.
  - Implementation: deterministic (banned words, regex) + guard LLM/judge returning safe/unsafe.
  - Apply to tool calls too; polite refusal on block.
- Частые ошибки: only one side; trusting the model's own judgment.
- Красные флаги: «списка слов достаточно», «модель сама себе гардрейл».

### 32. Agent reflection: what it is, how it improves quality?
- Идеал: generate → critique → revise loop until a quality bar is met (Stop Check decides when to stop).
- Обязательные пункты:
  - Components: Generator, Critic, optional Tools, Memory, Stop Check.
  - Vs ReAct: ReAct explores world via tools; Reflection polishes output — use when quality > speed.
- Частые ошибки: путать Reflection с ReAct; бесконечный цикл критики без stop-условия.
- Красные флаги: «критика без повторной генерации улучшит ответ».
### 33. Code-generating vs tool-calling agents?
- Идеал: code-generating agents write and execute arbitrary programs; tool-calling agents choose from a fixed set of tools.
- Обязательные пункты:
  - Tool-calling: bounded action space, reuses well-defined ops, easy to validate/sandbox per tool.
  - Code-generating: unbounded action space — new logic (e.g. pandas code); needs sandbox, error feedback, strict limits.
  - They blend: code-exec agent has a run_code tool; both share think-act-observe loop.
- Частые ошибки: думать, что код-агент не требует песочницы.
- Красные флаги: «код-агент = tool-calling» без разбора действий.

### 34. Multi-modal inputs/outputs in agentic systems?
- Идеал: let the agent ingest and emit images/audio/video via a vision/multimodal model and typed tool outputs, with modality-aware context management.
- Обязательные пункты:
  - Input: convert media to model-readable forms (OCR, transcription) or feed raw to multimodal model; downsample.
  - Output: return media through tools (save image, generate audio), not just text claims.
  - Cost/context: media is token-heavy — compress, cache, use paths.
- Частые ошибки: assume every LLM sees images.
- Красные флаги: «добавил картинку в промпт = агент готов» без vision-модели.

### 35. State management in complex agent workflows (LangGraph)?
- Идеал: shared state travels through the graph — define State (TypedDict); each node returns an update; edges route by state.
- Обязательные пункты:
  - Nodes: `(state) -> dict`; don't call each other directly.
  - Conditional edges branch (e.g. bills → billing node vs technical).
  - Checkpoint/persist state for resume + human-in-the-loop.
- Частые ошибки: direct function-to-function coupling; no persistence.
- Красные флаги: «state — одна переменная в функции»; no checkpoints.

### 36. Customer support agent with escalation logic?
- Идеал: classify → route → answer from KB → escalate to human on low confidence/high stakes with full context.
- Обязательные пункты:
  - Pipeline: intent classifier → conditional route → RAG → draft reply → confidence gate.
  - Escalation triggers: low confidence, repeated failure, angry user, complex/legal issue.
  - Handoff context: conversation + attempted steps + summary; log outcome.
- Частые ошибки: escalate without context; no confidence gate.
- Красные флаги: «эскалация = пересылка сообщения», нет триггеров.

### 37. Agent orchestration: what is it, how implemented?
- Идеал: coordination layer for LLMs/tools/data/steps; developer controls flow (vs agent where LLM decides).
- Обязательные пункты:
  - Patterns: sequential, parallel, conditional, loop, orchestrator-worker.
  - Orchestrator-worker: split task → workers (parallel) → combine.
  - Tools: LangChain, LangGraph, CrewAI, etc.
- Частые ошибки: путать с agents (flow control); не упоминать patterns.
- Красные флаги: «оркестрация = один LLM», «агент = оркестрация всегда».

### 38. Sakana Fugu — how does it orchestrate a team of AI models?
- Идеал: Fugu is a family of "conductor" orchestrator models: read a question, pick which frontier models work on it, let them work, combine answers.
- Обязательные пункты:
  - Fugu (one worker, fast) vs Fugu-Ultra (multi-model plan, slower, max quality).
  - Lightweight selection head on hidden state → logits score each worker → pick highest, no text generation = low latency.
  - Training: SFT (softmax soft targets, KL loss) then evolutionary strategies (sep-CMA-ES); Ultra's Conductor via GRPO; swappable model pool.
- Частые ошибки: think Fugu answers itself; reduce to a simple router.
- Красные флаги: «Fugu generates the answer», «one model is best at everything».

### 39. Sandboxed code execution for agents?
- Идеал: run model-generated code in an isolated sandbox with resource limits, timeouts, no host access.
- Обязательные пункты:
  - Isolation: containers, ephemeral FS, read-only host mounts, no secrets in sandbox.
  - Limits: CPU/memory/time, max turns, kill on timeout; network deny-by-default.
- Частые ошибки: run as host user; expose prod data.
- Красные флаги: «sandbox = virtualenv», «свой код не проверяем».

### 40. Infinite loop in agent — detect and break?
- Идеал: cause — LLM stateless, can't see the tool already returned; loop re-executes same tool/input. Tool errors/format also play a role.
- Обязательные пункты:
  - Diagnosis: check whether full history is fed back; inspect tool result format.
  - Fix: max_steps safety net; detect repeated tool calls and inject a clear note («tool X already returned Y»); fix tool result handling; clear stop instruction.
- Частые ошибки: blame only the model; rely on the LLM to self-realize.
- Красные флаги: «просто больше контекста», «модель сама помнит».

### 41. Conflicting answers from different tools — reconcile?
- Идеал: weigh sources by trust/freshness, cross-verify, synthesize; escalate on unresolved high-stakes conflict.
- Обязательные пункты:
  - Source hierarchy: DB/verified API > search > model guess; consider recency.
  - Reconcile: cross-check vs a third source, majority/consensus, or most authoritative.
  - Unresolved + high stakes → ask user / escalate, don't guess.
- Частые ошибки: silently average numbers with different semantics; trust last call.
- Красные флаги: «всегда беру последний ответ» без ранжирования.

### 42. Reduce token consumption?
- Идеал: same levers as Q29 — stop early, summarize history, route models, cache tool results, compact prompts.
- Обязательные пункты (ref):
  - Max iterations + clear stopping condition — stop once it has enough information.
  - Summarize history after every few steps instead of passing full history.
  - Model routing: powerful only for complex reasoning; small model for extraction.
  - Cache tool results; dynamic concise system prompts (long system prompt × many calls is huge).
- Частые ошибки: забыть, что system prompt платится на КАЖДОМ шаге.
- Красные флаги: «урезать output max_tokens» — это не снижает входные токены.

### 43. Agent keeps exceeding budget per task — enforce limits?
- Идеал: build budget into the loop as a hard safety stop: turn cost, time, step limits — the code stops it, not the model.
- Обязательные пункты (ref):
  - Stop conditions: natural (LLM says done) + safety (step/cost/time budget) — both required.
  - Step limit (max_steps) protects against infinite loops; add cost and time budgets.
  - Track cumulative spend per task; abort and report when exceeded.
- Частые ошибки: rely on the LLM to stop; no explicit counters.
- Красные флаги: «проблема в модели, не в коде» — loop owns the budget.

### 44. Agent hallucinates tool capabilities and passes wrong inputs — fix?
- Идеал: ground the model in true tool signatures — strict schemas, validation, error feedback; not just better prompts.
- Обязательные пункты:
  - Practical diagnosis: tool descriptions and schemas are the model's only knowledge of the tool — keep them precise.
  - Fix: use API-defined tools with strict JSON schema (required types/enums); validate args server-side before execution; return clear errors and let the model retry; few-shot examples; list fewer, smaller tools; structured output to guarantee shape.
- Красные флаги: «промпт «не выдумывай» решает», нет валидации аргументов.
- Частые ошибки: обвинять модель без проверки своих tool definitions.

### 45. Agent deleted a production DB — prevent irreversible actions?
- Идеал: make destructive actions impossible without explicit multi-layer approval and reversibility guarantees.
- Обязательные пункты:
  - Permissions: agent can read prod, needs human approval to write/delete; dry-run flag.
  - Destructive tools require confirmation + explicit confirmation inputs («type DELETE»).
  - Backups & safe rollback, restore drill, staging first, audit logs.
- Частые ошибки: give agent write access freely; no approval gate.
- Красные флаги: «просто спроси один раз» без гейта на необратимые операции.

### 46. Many tools, keeps picking the wrong one — improve tool selection?
- Идеал: reduce the tool surface and make each tool's purpose unmistakable, so the model picks correctly.
- Обязательные пункты:
  - Fewer, well-named tools; clear descriptions with when-to-use and examples; group/namespace.
  - Router layer: a classifier selects a subset of tools per request rather than exposing all.
  - Few-shot examples; evaluate selection accuracy; fallback: verification after tool output.
- Частые ошибки: throw more tools with vague names; expect model to discover.
- Красные флаги: «больше инструментов = умнее», «не нужна маршрутизация» (все сразу).

### 47. Agent takes too long to complete a task — speed it up?
- Идеал: cut latency by parallelizing, caching, and cutting redundant calls/steps — not by rushing the model.
- Обязательные пункты:
  - Parallelize independent tool calls in one turn (LLMs can emit multiple tool calls → run them in parallel); cache repeated tool results.
  - Reduce steps: better tools, fewer round-trips, router to skip unnecessary work.
  - Cheaper/faster model for easy steps; concise prompts; keep context short (compaction).
  - Fire-and-forget where async is OK; measure per-step latency budget.
- Частые ошибки: sequential single-call loops when calls are independent.
- Красные флаги: «ускорить = понизить качество модели» без диагностики узких мест.

### 48. Long-running agent drifts and works on the wrong thing after hours — diagnose and fix?
- Идеал: diagnose drift as goal/context loss, then add re-anchoring: keep the original goal visible at every turn and re-verify outputs against it.
- Обязательные пункты:
  - Diagnosis: compaction may drop the goal from the summary; check logs — where goal faded; state corruption.
  - Fix: keep immutable goal in system prompt every turn; re-anchor after compaction; periodic re-planning / checkpoint compare vs original task.
  - Add a drift check node with stop on deviation; human re-orientation; store goal + definition-of-done explicitly; test recovery/regression.
- Красные флаги: «просто перезапуск решит», «агент сам поймёт цель из хвоста лога».
- Частые ошибки: обвинять модель в лени, не проверив, что цель видна модели.

### 49. LLM selects right tool but wrong parameters — fix parameter extraction?
- Идеал: structured arg generation + validation loop: model emits args against a strict schema, code validates, errors return to model for correction.
- Обязательные пункты:
  - Use function-calling vs free-text: function calling generates a JSON object keyed to tool args by construction.
  - Tight schemas: required fields, types, enums, ranges; few-shot examples; default-field hints.
  - Runtime: validate args before execution; on mismatch return a clear error, ask model to fix; retry bounded.
  - Structured output / constrained decoding (grammar) to guarantee parseable JSON; test param paths.
- Красные флаги: «спека параметров не важна, модель разберётся».
- Частые ошибки: сваливать на модель без валидации и ошибки-обратной связи.

### 50. How do Computer-Use Agents work?
- Идеал: perceive → think → act loop over a real screen, like a human: screenshot, decide next action, execute it, repeat.
- Обязательные пункты:
  - Perceive: screenshot (pixels) + optionally accessibility tree; vision model reads it.
  - Think: vision+LLM takes goal + screenshot + history, outputs next single action as structured JSON.
  - Act: `click(x,y)`, `type(...)`, `scroll`, `key(...)`, `screenshot()`.
  - Why: no API needed for apps; more robust than hardcoded scripts; but slower, error-prone, high tokens. MCP preferred when API exists — more reliable.
- Частые ошибки: думать, что agent планирует все шаги заранее — решает по одному шагу.
- Красные флаги: «computer-use = скрипт» (это агент с vision-LLM в цикле).

### 51. How does LangChain work?
- Идеал: framework of composable building blocks chained together with the `|` pipe; output of one block feeds the next.
- Обязательные пункты:
  - Blocks: PromptTemplate (fill placeholders), LLM, OutputParser, Memory (stores conversation), Retrieval/RAG (vector store), tools/agents (decision loop).
  - Chain = template | llm | parser; invoke() runs the pipeline; memory injects past context on each call.
  - RAG flow: chunk docs → embed → vector store → retrieve → LLM answers with context.
- Красные флаги: «LangChain = модель», «chain — это одна функция».
- Частые ошибки: не упоминать pipe-композицию и memory; путать с LangGraph.

### 52. How does LangGraph work?
- Идеал: graph orchestration framework on top of LangChain for loops/branches; model = nodes, edges, shared State.
- Обязательные пункты:
  - StateGraph(State): add_node, add_edge, add_conditional_edges(start→route); compile → runnable dag; invoke(state).
  - Nodes: `(state) -> dict` updates; edges; conditional edges route by state (e.g. billing vs technical).
  - Shared state, checkpoints/persistence for resume, human-in-the-loop interrupts, memory.
  - Use: when workflow needs loops/branching/persistence beyond simple chain.
- Красные флаги: «LangGraph = LangChain другого имени», нет понятий nodes/edges/state.
- Частые ошибки: путать с LangChain (LangGraph — для циклов/ветвлений/персистентного state, не линейных цепочек); забывать про checkpoints для resume.

### 53. What is OKF (Open Knowledge Format)?
- Идеал: open standard for documenting what an organization knows about its data/systems in plain markdown files so any agent/tool reads it.
- Обязательные пункты:
  - Bundle = folder; one file per concept (tables/orders.md); index.md optional; plain markdown + YAML frontmatter; `type` is the only required field.
  - Cross-links between files turn the bundle into a graph the agent follows; it's not the data itself — it's the meaning/knowledge around it.
  - Published by Google Cloud Data Cloud team; complements MCP (access) and Agent Skills (actions).
- Частые ошибки: думать, что OKF хранит данные rows, а не семантику.
- Красные флаги: «OKF = инструмент/сервер», «OKF заменяет MCP» (они разные слои).
