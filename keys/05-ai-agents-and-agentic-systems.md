# AI Agents and Agentic Systems — Answer Key (1-27)

### 1. What is an AI agent, and how does it differ from a simple LLM call?
- Идеал: An AI agent is an LLM wrapped in a loop with tools and memory that keeps working until a goal is achieved; a plain LLM is a one-request/one-response call.
- Обязательные пункты:
  - The goal comes in at the top; the LLM decides each step: call a tool or return a final answer; the loop runs until the goal is achieved.
  - LLM (brain) + Instructions (system prompt) + Tools (name/description/input_schema) + Memory (short- and long-term) + Loop (the runtime).
  - The LLM does not run tools — it recommends them; the loop executes and feeds observations back.
  - Agent: an LLM + a loop + tools + memory (code that takes input, executes actions, repeats until complete = agent).
- Частые ошибки: сводить различие к «chat vs plain LLM», не упоминать tool use и loop.
- Красные флаги: «пален LLM сам вызывает функции», «агент — это просто модель с длинным контекстом».

### 2. AI Agent Memory
- Идеал: Memory is the system around a stateless LLM that lets it "remember" across turns, sessions, and users; the LLM never remembers anything itself.
- Обязательные пункты:
  - LLM is stateless — every call starts fresh; agent remembers on its behalf.
  - Memory stack (4 layers): Context Window, Short-Term (session scratchpad), Long-Term (persistent), External Knowledge (tools/RAG — queried, not maintained).
  - Four core operations: Write, Read, Update (on contradiction), Forget.
  - Runtime memory flow per turn: retrieve relevant long-term memory → read short-term scratchpad → build prompt (system + memory + user message) → LLM loop → write new memory → respond.
  - Store what matters next week; skip low-signal messages. Don't store every message (bloat ruins retrieval).
  - Fixes: semantic search, update-on-contradiction, forget policy, scope by user ID.
- Частые ошибки: путать short-term и long-term (долго хранить временное / терять стабильное); не делать update/forget.
- Красные флаги: «модель сама запоминает предыдущие диалоги», «важно хранить всё» (нужен отбор).

### 3. Harness Engineering in AI
- Идеал: Harness engineering is building the control layer around an AI model that makes it usable in production — managing inputs, outputs, tools, memory, errors, and evaluation.
- Обязательные пункты:
  - The model alone is just an engine; the harness is the car body/steering/brakes/dashboard around it.
  - Components: prompt management (Context Engineering), tool orchestration, memory management, error handling, I/O processing, guardrails.
  - Agent harness: prepare prompt → model → if tool call, harness executes tool, feeds result back → repeat until model says task complete.
  - The model does not execute tools; the harness does.
  - Eval: LLM-as-a-Judge for open-ended outputs; agent eval covers trajectory/tool calls/plan.
  - Best practices: modular, log everything, guardrails day one, test harness code itself (harness has bugs), monitor latency/errors/cost.
- Частые ошибки: сводить всё к промпту/модели; не тестировать код harness; не логировать tool calls.
- Красные флаги: «достаточно хорошей модели, обвязка неважна», «harness == Context Engineering» (он часть harness).

### 4. What matters more for an agentic coding tool like Claude Code: the model or the harness?
- Идеал: The harness matters as much as — often more than — the model: a great model with a poor harness gives a poor experience; a good model with a great harness gives an excellent experience.
- Обязательные пункты:
  - A chatbot can't see the project, can't do anything, can't verify — Claude Code gives the model "eyes and hands" (Read/Grep/Glob/Edit/Write/Bash).
  - Agent loop: gather context → take action → verify results → repeat; Bash verification runs tests/compiler and errors feed back (reflection).
  - Grep/Glob funnel: thousands of files → few matches → read only relevant code so the context window never overflows.
  - Verification is the most important part — looking correct ≠ being correct; run the code/tests.
  - Harness anche: CLAUDE.md project memory, permissions, plan mode, subagents, hooks, Context Engineering.
- Частые ошибки: приписывать весь результат модели; не упоминать verify-цикл и контекст-фаннел.
- Красные флаги: «любая хорошая модель даст тот же результат», «harness — это просто UI-обвязка».

### 5. Explain the ReAct (Reasoning + Acting) agent architecture.
- Идеал: ReAct is an agent pattern where the LLM in a loop writes explicit reasoning (Thought), picks a tool (Action), reads the result (Observation), and repeats until it produces a Final Answer.
- Обязательные пункты:
  - ReAct = Reasoning + Acting; the most common agent pattern; visible step-by-step reasoning (CoT surfaced in the loop).
  - Loop: Thought → Action → Observation → repeat → Final Answer; classic form one tool per thought, modern APIs allow multiple parallel tool calls.
  - Five parts: LLM, System Prompt (explains pattern + lists tools + rules), Tools, Memory (running history), Loop Controller (executes tools, enforces stop conditions).
  - Prompt template: either `Thought:` + `Action: tool(input)`, or `Thought:` + `Final Answer:` when done; rules: always start with Thought, wait for Observation, stop as soon as final answer.
  - Trace: search Tokyo population → Observation → calculator(14000000*0.15) → Observation → Final Answer 2.1M.
  - Implement as while-loop: call LLM → if is_done return final answer → else for each tool_call run `call_tool` and append result as tool message; safety stop via max_steps.
  - Use API function-calling schema, not the literal string format from the paper.
- Частые ошибки: называть любой агент с тулами «ReAct» без цикла Thought/Action/Observation.
- Красные флаги: «ReAct — это категория, а не паттерн», «в ReAct модель сама исполняет инструменты».

### 6. What is the Plan-and-Execute agent pattern?
- Идеал: The agent first writes a full step-by-step plan up front, then executes it step by step, re-planning only when reality does not match the plan.
- Обязательные пункты:
  - Parts: Planner (strong LLM writes the plan), Executor (usually smaller/cheaper LLM runs each step), Tools, Memory, optional Re-Planner (checks state: continue / update plan / stop).
  - Flow: Plan once → Execute step by step → Re-Plan when a step fails or surprises.
  - Vs ReAct: ReAct thinks one step at a time (adaptable, costlier); Plan-and-Execute plans up front (cheaper for many predictable steps, less adaptive). Use ReAct for open-ended tasks, Plan-and-Execute for multi-step tasks with a clear path.
  - Failure modes: bad plan, step drift, no re-planning, over-planning, outdated plan, infinite re-planning (fixes: clear prompt with small concrete steps, specific steps tool+input, always re-plan on errors, smallest plan, rewrite from latest state, hard limits).
- Частые ошибки: не упоминать re-planning на ошибке/сюрпризе; смешивать отличия от ReAct.
- Красные флаги: «план один раз и никогда не корректируется», думать, что Planner и Executor всегда одна модель.

### 7. What is tool use (function calling) in LLMs, and how does it enable agents?
- Идеал: Function calling lets the LLM request external tools via a structured JSON call (name + arguments), which our app executes — closing the live-data and action gaps.
- Обязательные пункты:
  - LLM only generates text; it can't fetch live data or take actions; function calling solves both gaps.
  - We describe functions by name, description, parameters (JSON schema); model returns `{"name": ..., "arguments": {...}}`.
  - Key insight: the model does NOT run the function — the app does. Model = brain, app = hands; keeps everything safe (app stays in control).
  - Round trip: define functions → user asks → model returns JSON call → app runs real function → result sent back to model → model writes final plain answer.
  - Message loop: user → function call → tool result → final answer.
  - Enables agents: agent = talk + act via function calling; the backbone of agents.
- Частые ошибки: думать, что LLM сам исполняет функцию; не описывать JSON schema параметров.
- Красные флаги: «function calling — это просто форматирование JSON», «модель может исполнять функцию без нашего кода».

### 8. What is the difference between structured output and function calling?
- Идеал: Structured output (JSON mode) constrains the answer into a fixed shape; function calling is the same schema-generating ability used to request a real action — "structured output put to work".
- Обязательные пункты:
  - Structured outputs: answer forced into a fixed shape (e.g. `{name, age, city}`); JSON mode: only valid JSON, no extra words.
  - Function calling: model returns a JSON request naming a function + arguments; OUR app runs the real function.
  - Shared foundation: both rely on the model producing schema-conforming JSON.
  - Differences: structured output = just the answer shape, nobody runs code; function calling = request for action, app executes it.
  - OpenAI/Anthropic use tool schemas with strict mode for reliability.
- Частые ошибки: смешивать «формат ответа» и «запрос на действие».
- Красные флаги: «function calling — то же самое, что structured output», «JSON mode сам вызовет функцию».

### 9. How do you design and define tools for an AI agent?
- Идеал: Define each tool by a name, a precise description (what it does and WHEN to use it), and an input_schema (JSON) so the LLM picks the right tool and passes valid args.
- Обязательные пункты:
  - Tool definition: `{"name": "web_search", "description": "...", "input_schema": {"type":"object","properties":{...},"required":["query"]}}`.
  - `description` is the most important field — the LLM uses it to decide between tools; vague description → wrong tool, precise → right tool.
  - The LLM reads name to identify, description to decide when, input_schema to know argument format.
  - Keep tool list small, focused, non-overlapping; per-subagent tool sets (small focused set → fewer wrong turns).
  - MCP lets a server describe its own tools so an agent discovers them on connection.
- Частые ошибки: размытые описания; слишком длинный/пересекающийся список тулов; не задавать required поля.
- Красные флаги: «описание неважно», «чем больше тулов тем лучше» (наоборот — меньше ошибок).

### 10. How does an agent decide when to call a tool versus answering from its own knowledge?
- Идеал: The LLM decides each turn — call a tool when it needs current/private/verifiable data or a real action; answer from knowledge for stable, well-known facts.
- Обязательные пункты:
  - Call a tool when: live/current data, data outside training, private per-user data, computation, real actions (send/book/save) — otherwise hallucination risk.
  - Answer from knowledge when: stable facts the model reliably knows, no freshness needed, creative/reasoning tasks.
  - Tool descriptions ("use when…") steer this decision; the model compares request against descriptions.
  - When unsure between knowledge and tool, prefer the tool to avoid fabrication.
- Частые ошибки: отвечать по памяти на вопрос о текущих данных (устаревший/выдуманный ответ); звать тул для чисто концептуального вопроса.
- Красные флаги: «всегда сначала вызвать тул», «модель знает всё и тулы не нужны».

### 11. What is the difference between single-agent and multi-agent systems?
- Идеал: A single agent is one LLM+loop+tools+memory doing a task; a multi-agent system is 2+ specialized LLM agents collaborating on a shared task, with a coordination layer deciding who does what and in what order.
- Обязательные пункты:
  - Three pillars: Specialization, Communication, Coordination — without coordination it's just "a bunch of agents".
  - Each agent has its own prompt and tools (often its own model). Roles: Orchestrator, Worker/SubAgent, Router, Planner, Critic/Reviewer, Tool Specialist.
  - Communication: message passing (point-to-point), shared state/blackboard, handoffs (message + control transfer); structured messages keep agents on rails.
  - Coordination patterns: sequential, parallel (fan-out/fan-in), hierarchical.
  - Trade-offs: single = simple/cheap/one context; multi = specialized reliability + parallelism but coordination cost, communication errors, harder debugging.
- Частые ошибки: считать группу агентов без координации MAS; не упоминать специализацию/коммуникацию/координацию.
- Красные флаги: «MAS всегда лучше», «агенты общаются свободным текстом как угодно».

### 12. When do multi-agent systems break down, and when is a single agent the better choice?
- Идеал: Multi-agent when task splits into specialized roles, needs different models, has parallel independent subtasks, or a too-long/too-tool-heavy prompt; single agent when simple, tightly coupled, or coordination overhead outweighs gains.
- Обязательные пункты:
  - Breakdowns: agents talking too much (token explosion) → cap turns/make handoffs explicit; unclear ownership (duplicate/missing work) → scoped roles, orchestrator routes; error propagation (small mistake amplified, hard to trace) → validate intermediate outputs, add critics; coordination overhead.
  - Use multi-agent when: roles naturally split (research+write+review), parts need different prompts/models, independent subtasks give real parallelism, dedicated critic needed for quality.
  - Do NOT use when: single agent already works, task is tightly coupled (coding shares context), coordination cost > speedup, team lacks tooling/time for debugging, simplicity/predictability needed.
- Частые ошибки: валидировать только финальный ответ (пропустить propagation ошибок); ставить агентов на простые задачи.
- Красные флаги: «multi-agent дешевле и проще» (обычно дороже в координации), «добавить ещё агента» без реального splits на роли.

### 13. What is Model Context Protocol (MCP), and how does it standardize tool integration?
- Идеал: MCP is an open standard (Anthropic, Nov 2024) defining one common way for AI applications to connect to outside tools and data — a USB-C port for AI: build the connector once, every MCP-speaking app uses it.
- Обязательные пункты:
  - Problem: N apps × M systems = N×M hand-written connections; MCP turns this into N + M pieces of work.
  - Three parts: Host (AI app, holds the model), Client (one connection per server, inside the host), Server (small program offering tools/data — e.g. GitHub, database, files).
  - Step flow: host starts server → client and server shake hands (capability negotiation) → client asks server "what tools do you have?" → server returns self-describing list (name/description/input_schema in plain English) → host passes list to model → model requests a tool → client sends call to server → server runs it and returns result → model reads result and answers.
  - Transport: stdio (server on local machine, messages pass locally) or Streamable HTTP (server remote, shared by many users).
  - MCP does not replace APIs — the server usually calls a normal API behind the scenes.
  - Importance: live data vs frozen training, build-once-use-everywhere, no lock-in, powers AI agents — an agent is only as capable as the tools it can reach, and MCP is how it reaches them.
- Частые ошибки: путать MCP с API; думать, что сервер MCP сам управляет моделью.
- Красные флаги: «MCP заменяет APIs», «модель говорит с MCP-сервером напрямую» (модель запрашивает, host выполняет).

### 14. How does MCP differ from traditional function calling?
- Идеал: Traditional function calling is per-app: the developer writes a custom tool description for each function and wires it to the app. MCP is a shared standard: the server self-describes its tools so any MCP client discovers and uses them without per-app wiring.
- Обязательные пункты:
  - Traditional: each app reads docs and wires each tool manually; N apps × M tools = N×M integrations.
  - MCP: server announces capabilities on connection; model discovers tools by itself; one server works with every MCP-speaking app.
  - Traditional function calling is one of the things MCP standardizes (tool request/name/arguments/input_schema), but MCP also covers data sources (not just tools), self-description, and session management.
  - MCP server can provide both tools AND data (files, databases) — MCP is the broader wrapper.
  - With traditional function calling, every new app needs every new tool re-described; with MCP the server describes itself once.
- Частые ошибки: считать MCP и function calling синонимами; не видеть разницы в discovery и wiring cost.
- Красные флаги: «MCP — это просто function calling», не различать одноразовую проводку и самодесCRIBE-сервер.

### 15. What are AI SubAgents?
- Идеал: A SubAgent is a smaller, specialized agent that works under a main agent, handling one specific part of a larger task — like a team member under a manager.
- Обязательные пункты:
  - Main agent = manager/coordinator, breaks task into pieces, delegates, collects and combines results. SubAgent = focused worker for one piece.
  - Why needed: context overload (one agent hits context window limit), lack of focus (too many tools = bad decisions), reusability (one SubAgent can serve multiple main agents), parallel work (SubAgents run simultaneously).
  - Flow: main agent receives task → decomposes → picks matching SubAgent per piece → sends task → SubAgent runs its own loop with its own budget/tools/memory → returns result → main agent combines.
  - SubAgent calling SubAgent gives a tree structure — powerful but dangerous (deep costly chains); use carefully.
  - Each SubAgent has its own context window — intermediate steps stay inside it; only the result comes back to main agent (keeps main agent's context clean).
  - Use SubAgents only when the task is truly complex and splits into clear independent parts; for simple tasks one agent is enough.
- Частые ошибки: ставить SubAgent-ы на простые задачи; SubAgent возвращает слишком много промежуточных данных вместо финального результата.
- Красные флаги: «SubAgent = Multi-Agent System» (SubAgent — один из способов построить MAS), «всегда нужны SubAgent-ы» (нет, для простых задач overkill).

### 16. What are the different types of agent memory (short-term, long-term, episodic)?
- Идеал: Agent memory is a stack of layers with different lifespans; short-term is session scratchpad, long-term is persistent and divides into episodic/semantic/procedural.
- Обязательные пункты:
  - Four layers: Context Window (in-prompt, fastest but smallest), Short-Term (session, plan/current step/intermediate results — gone when session ends), Long-Term (persistent — user facts, preferences, past summaries, learned behaviors), External Knowledge (tools/RAG — queried, not maintained).
  - Long-term sub-types: episodic (past experiences), semantic (facts and concepts), procedural (how to do things).
  - Four operations apply to all: Write, Read, Update, Forget.
  - External knowledge (RAG) is not the same as agent memory — some frameworks classify it as long-term, others keep separate.
- Частые ошибки: объявлять RAG и agent memory идентичными; путать episodic/semantic/procedural.
- Красные флаги: «short-term = context window» (можно, но better: layer distinction).

### 17. How do you handle agent failures and implement error recovery?
- Идеал: Treat every failure as an observation to feed back: the harness catches errors, turns them into actionable feedback, retries where useful with fallbacks, and stops safely when recovery is impossible.
- Обязательные пункты:
  - Structure: cause → diagnosis → fix. First detect the failure type (invalid output, tool call error, API error, loop stuck).
  - Error handling in harness: catch errors (try/except around tool calls), convert a crash into a lesson instead of the end of the run.
  - Retry with backoff for transient failures (API timeout), fallback tool/method when one tool fails, and feed a clear message to the model ("File not found at path X, did you mean Y?").
  - Log everything (inputs, outputs, tool calls, errors) for debugging.
  - Loop guards: max steps/repeats, detect repeated tool calls, budget (time/cost) limits.
  - If a step keeps failing after N tries, degrade gracefully — escalate to human or report failure honestly.
- Частые ошибки: логировать всё, кроме tool calls и errors; «просто перезапустить агент с начала» при долгих задачах (нужны checkpoints); не сообщать модели детализацию ошибки.
- Красные флаги: «агенты не умеют ошибатываться — пиши идеальный код», игнорировать ошибки фоново.

### 18. What is an agent loop, and how does it decide when to stop?
- Идеал: An agent loop is the runtime (Think → Act → Observe → repeat) that sends state to the LLM, runs chosen tools, feeds results back until the LLM produces a final answer; stop conditions: natural stop (LLM says done) + safety stops (step/time/cost budget, human interrupt).
- Обязательные пункты:
  - Think-Act-Observe cycle; the LLM is the brain, the loop is the hands — the loop executes tools.
  - Loop needed because one LLM call can't finish a multi-step task and the LLM is stateless — it must resend the whole history.
  - Two stop conditions and both must be present: natural stop (LLM decides goal achieved → final answer) and safety stop (step limit → "reached step limit"); production adds time/cost budget + human interrupt.
  - Loop failures: infinite loops (fix: hard step limit), stuck repeating same action (detect repeated calls → feed note back / better instructions), context overflow (summarize/drop stale observations), premature stopping (clear "when done" instructions).
  - Parallel tool calls: modern models can output multiple tool calls in a turn; loop runs them in parallel and feeds all results back.
- Частые ошибки: написать только `while True` без step budget; считать, что стоп-лимит — это цель, а не запасной вариант.
- Красные флаги: «у агента только одно стоп-условие», «loop — это то же самое, что ReAct» (ReAct — паттерн поверх цикла).

### 19. Context Engineering
- Идеал: Context engineering is designing, organizing, and managing everything that goes into the LLM's context window so the model works reliably — the real bottleneck of reliable AI apps.
- Обязательные пункты:
  - LLM is stateless; the output is decided entirely by the context; a weak model + great context can beat a strong model + poor context.
  - Context is rebuilt from scratch every turn: 8 components — system prompt, few-shot examples, retrieved documents (RAG), tools+tool descriptions, memory, conversation history, tool results, current user message.
  - Vs prompt engineering: prompt engineering tunes wording of one instruction (a subset); context engineering designs the whole information environment.
  - Patterns: RAG (retrieve only relevant), few-shot, tool calling, memory injection, conversation history management (summarization/sliding window), output formatting (structured output/schema), context compression.
  - Best practices: fit everything in the budget, use RAG to keep context small, structured over prompt-only formatting, forward to compaction when it grows.
- Частые ошибки: сводить к переписыванию промпта; класть в контекст всё подряд (retrieval + model confuse); игнорировать lost-in-the-middle при длинном контексте.
- Красные флаги: «context engineering == prompt engineering», «у модели context window огромный — можно пихать всё».

### 20. How does context compaction work?
- Идеал: Context compaction shrinks old conversation into a short summary so important facts stay and the context window gets free space — instead of deleting old messages (which loses facts), squeeze them.
- Обязательные пункты:
  - Problem: conversation grows past the fixed context window; dropping oldest (sliding window) loses hidden facts; also lost-in-the-middle and attention-sink issues.
  - Compaction = the same LLM summarizes old messages (e.g. 3000 tokens → 200-token note keeping name, goal, key decisions) and we keep recent messages in full.
  - Trigger compaction when context crosses a threshold (~80% of window), not after every message.
  - Code pattern: split history into old + recent; `summary = summarize(old)`; return `[summary] + recent`. Sliding window `messages[-max:]` is the broken version.
  - Repeat whenever the box fills; compaction is used by coding assistants to avoid forgetting the early goal after long tasks.
  - Related: lost-in-the-middle (safer to use compacted smaller context), attention sinks (never drop very first tokens).
- Частые ошибки: предлагать только sliding window без summarization; терять важные факты из старой части; компактить после каждой реплики (дорого).
- Красные флаги: «compaction — это просто удалить старые сообщения», «можно обойтись базом без сжатия, контекст и так большой».

### 21. Loop Engineering
- Идеал: Loop engineering is the deliberate design of the repeating cycle an agent runs — how many turns, what carries forward, error feedback, and when it must stop — so the agent makes progress and stops at the right moment.
- Обязательные пункты:
  - The model doesn't loop; the loop is code around it (model decides, loop decides what happens).
  - Simplest loop `while True: decision=model(context); result=run_tool(...); context+=result` fails: no stop, context grows unbounded, no error handling, no definition of done.
  - Seven engineered parts: goal (clear "what finished means"), step budget, tools (short sharp list), observation (trim/summarize/paginate results), memory (full vs running summary), feedback on failure (actionable error message), exit (success/budget/repeated failure/human).
  - Loop patterns: always re-inject the goal each turn so the agent doesn't drift; verify the "done" claim; on ToolError turn crash into a lesson.
  - A strong model in a badly designed loop fails; a modest model in a well-designed loop finishes. Handling loop edge cases is the real engineering.
  - Vs graph engineering: loop = flexible repeating cycle with one loop; graph = fixed nodes/edges with decisions as conditional edges.
- Частые ошибки: не ставить step budget / definition of done; пастить сырые огромные tool output напрямую; не подавать goal каждый ход (дрейф).
- Красные флаги: «loop engineering — это про выбор модели», «нужно дать агенту бесконечное число ходов».

### 22. Graph Engineering
- Идеал: Graph engineering designs an AI system as a graph where each step is a node and each path between steps is an edge — visible, controllable steps, with the model deciding only where we let it.
- Обязательные пункты:
  - Building blocks: Node (one step), Edge (answers "which node runs next?"), State (shared notebook all nodes read/write).
  - Why: one big prompt forgets parts + hard to find failed step; chain can't go back; one loop = too little control, untestable. Graph = small steps + going back + paths we control.
  - Conditional edges: model scores (LLM-as-Judge), routing function picks destination from state (code holds control): score≥8→send; no docs→search; else write.
  - Cycles: write→check→write for self-correction (Reflection); every cycle needs a hard limit (attempts→ask_human).
  - Parallel: fan-out + fan-in (merge node); parallel nodes must write different state keys (else overwrite each other).
  - Checkpoints: graph saves state (thread_id) after each node — resume on restart; powers HITL pause/resume.
  - Works well for fixed multi-step workflows (Agentic RAG, review loops); fails when flow is too dynamic.
- Частые ошибки: граф без явного state; параллельные ветки пишут в один ключ; циклы без лимита повторов.
- Красные флаги: «graph engineering == loop engineering» (разные: фикс. узлы/рёбра vs гибкий цикл), «пусть агент сам решает маршрут» везде (контроль должен оставаться кодом).

### 23. How AI Agents Communicate
- Идеал: Agents share information and coordinate through four main patterns — direct, centralized, broadcast, shared-memory — with structured messages and explicit control transfer.
- Обязательные пункты:
  - Direct: one agent → another, no middleman — simple/fast, but each must know how to reach each other; adding an agent rewires.
  - Centralized: orchestrator in the middle routes all messages — easy to manage/add/log, but bottleneck + single point of failure.
  - Broadcast: one sends the same message to many at once; interested agents act — scales, noisier.
  - Shared memory/blackboard: all read/write a common store, each picks what it needs.
  - Messages must be structured (task/context/inputs as named fields), not free-form chat — unstructured text multiplies misunderstandings.
  - Patterns overlap: a handoff is message + control transfer; real systems mix.
  - Watch out: agents messaging forever (cap), wrong info propagation (validate intermediate), main-agent bottleneck.
  - MCP vs A2A: different layers (tool vs inter-agent).
- Частые ошибки: свободный неструктурированный диалог агентов; direct-связь при большом числе агентов.
- Красные флаги: «коммуникация всегда через человека», «центральный агент никогда не подведёт».

### 24. What are Agent Skills?
- Идеал: An Agent Skill is a folder of instructions (and optionally scripts/reference files) the agent loads itself only when the task needs it — reusable team know-how powered by progressive disclosure (Anthropic, open format).
- Обязательные пункты:
  - Problem: typing the same steps every time (waste) vs keeping everything loaded (fills the context window) — Skills solve both.
  - Structure: `SKILL.md` — frontmatter (`name` lowercase-hyphenated, `description` = trigger) + plain-English body; folder can hold scripts/templates/docs.
  - Description is the trigger: the agent matches the request to descriptions; vague → skill never used.
  - Progressive disclosure: Level 1 name+description (~100 tokens each, always loaded — 50 Skills ≈ 5k tokens); Level 2 full SKILL.md body (<~5k tokens, loaded only when matched); Level 3 extra files opened only if needed. "Nothing loaded until it earns its place."
  - Scripts for exact repeatable operations: agent runs a tested file instead of rewriting code each time.
  - Storage: personal (`~/.claude/skills/`) every project; project (`.claude/skills/`) travels with the repo.
  - Skills vs MCP: MCP = what the agent can reach (hands); Skills = how to do the job (know-how/format/steps). Complementary.
- Частые ошибки: слабые описания (скилл не срабатывает); лить длинные процедуры в промпт; путать Skills и MCP.
- Красные флаги: «Skills заполняют контекст навсегда» (нет — progressive disclosure), «Agent Skills — это то же самое, что MCP».

### 25. How do you evaluate and test AI agents?
- Идеал: Agent evaluation measures outcome, trajectory, tool use, and planning quality — different from plain LLM eval because it must score actions, not just final text.
- Обязательные пункты:
  - 4 types: Outcome evaluation (final result: task success rate, answer accuracy, goal completion), Trajectory evaluation (steps in order: exact/in-order/any-order match, precision, recall), Tool Use evaluation (right tool picked, correct arguments, call success, result handling, no hallucinated tools), Planning evaluation (completeness/correctness/feasibility/efficiency).
  - Outcome only is not enough: a correct answer can be luck or wasteful; trajectory tells why it failed.
  - Methods: golden datasets with ground truth, LLM-as-a-Judge for open-ended outputs, self-critique, human eval for critical slices.
  - Benchmarks: agent-specific (e.g. SWE-bench, GAIA) measuring end-to-end task completion.
  - Frameworks: LangSmith, Langfuse, AgentOps, W&B, etc.
  - Challenges: no single correct trajectory, expensive, non-deterministic, hard ground truth for tool choice.
- Частые ошибки: оценивать только финальный ответ; нет ground truth для тул-выбора; игнорировать cost/waste.
- Красные флаги: «LLM eval == agent eval», «достаточно пары ручных примеров» (нужны бенчмарки).

### 26. What are the security risks of agentic systems, and how do you mitigate them?
- Идеал: The core risk is prompt injection and tool misuse — instructions and data travel through the same channel, so untrusted text can become a command an agent executes; mitigate by defense-in-depth around model, not just one filter.
- Обязательные пункты:
  - Prompt injection (direct from attacker-user; indirect hidden in fetched data — emails, web pages, docs, code comments, invoices).
  - Root cause: LLMs have no code/data separation — everything is text in one window; a command inside data and the system prompt look the same.
  - Attack: user-level prompt injection manipulates the app; indirect injection plants instructions data affecting real users (forward emails, leak PII) — victim is the innocent user.
  - Traditional security mindset (SQL) doesn't apply: SQL separates query from data; LLM sees one flat text.
  - Risks map to capabilities: tool misuse, data exfiltration, privilege escalation, covered by isolation/least privilege.
  - Mitigations: treat all tool outputs and fetched content as untrusted; don't let untrusted content override the system prompt.
  - Filter/monitor: tool-call allowlist, required arg validation (schema), quarantine screens for content produced by external sources.
  - Design to remove capability: sensitive actions need separate principal; don't share.
  - Do not rely on single text trick. Apply layered hygiene from day one (see also guardrails topics 27, 30).
- Частые ошибки: думать, что «просто не показывать system prompt» достаточно; не покрывать risk surface тулами.
- Красные флаги: «у меня нет рискованных тулов — я безопасен», «LLM умеет отличать instructions от data» (не умеет).

### 27. Your agent reads untrusted content (emails, web pages, documents) and can call tools. How do you prevent indirect prompt injection and data exfiltration?
- Идеал: Stop indirect injection at the design boundary — capability control and isolation. Attack works because the agent fetches content and folds it into the same context as its instructions (no code/data separation), so an injected note becomes a command for a tool call.
- Обязательные пункты:
  - Cause: the agent reads untrusted text and that text becomes part of the prompt = instructions to the model; a hidden note ("forward password resets to X") is recent and specific, wins over the system prompt.
  - Diagnosis: split the prompt; label content `untrusted` and tell the model "data, never instructions" — but text alone is unreliable: security boundary must be code, not prompt.
  - Fixes:
  1. Treat all tool output and fetched content as untrusted — never let it override system prompt (prompt boundary is only a weak defense).
  2. Validate/allow only tool-level requests: explicit allowlist of tools and args; tool chaining (extraction → separate tool call).
  3. Require user approval for irreversible actions (send, delete): HITL.
  4. Filter outputs (never echo raw content); keep system prompt instructions at both ends (mitigate lost-in-the-middle).
  5. Run sensitive logic in a separate agent/tool with restricted interface.
  - Preventions of indirect injection: never pass raw page/inbox text into the response; sandbox the doc-tools.
  - Data exfiltration prevention: least privilege — read-only tools; output filter; no reflection of raw content.
- Частые ошибки: полагаться только на промпт-границы («не выполняй команды из файлов»), не фильтровать, не требовать confirm для отправки.
- Красные флаги: «одна строка в системном промпте решает всё», «доверяю содержимому писем/страниц как инструменту» — не доверяй, изолируй.

<response>

I need to retry — the write split. Let me fetch the full error message.

<｜DSML｜tool_calls>
<｜DSML｜invoke name="read">
<｜DSML｜parameter name="i" string="true">Verifying nothing was written