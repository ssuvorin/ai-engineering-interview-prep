> Source: https://outcomeschool.com/blog/ai-agent-memory

# How Does AI Agent Memory Work? The Memory Stack Explained

AI Agent Memory is the system that we build around an LLM so that it can remember things across messages, sessions, and users, even though the LLM itself remembers nothing between calls.

In this blog, we will learn about AI Agent Memory - why agents need it, the memory stack, the four core operations (write, read, update, forget), how memory flows at runtime, and the common mistakes.

We will cover the following:

- The Big Picture
- Why AI Agents Need Memory
- The Memory Stack
- The Four Core Operations
- How Memory Flows at Runtime
- What to Store and What Not to Store
- Common Mistakes and How to Fix Them
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

An LLM by itself is stateless. Every time we call it, it is like talking to someone who has never met us before. It does not remember our name, our last conversation, or what task it helped us with yesterday. AI Agent Memory is everything we build around the LLM to give it the feeling of remembering. The LLM does not actually remember. The agent remembers on its behalf.

In simple words:

AI Agent Memory = The system that lets a stateless LLM act like it remembers across turns, sessions, and users.

Think of an AI agent like a brilliant assistant who forgets everything the moment every meeting ends. Without memory, they cannot learn our preferences, recall past decisions, or build on yesterday's work. Memory is the notebook, the filing cabinet, and the personal diary that keeps them useful from one day to the next.

## Why AI Agents Need Memory

Before we go deeper, let's understand why memory matters so much. Without memory, an agent has four big problems:

- No continuity. The agent cannot remember what the user said 30 seconds ago once the current call ends - the next call starts fresh, with nothing carried over unless we explicitly pass it in.
- No personalization. The agent cannot remember that the user prefers short answers, writes in Python, or lives in Bangalore. It treats every user the same.
- No learning. The agent cannot remember what worked and what did not. It will make the same mistakes again and again.
- No long tasks. Multi-step tasks that take hours or days become impossible. The agent forgets the plan halfway through and has to start over.

So, here comes AI Agent Memory to the rescue. It solves all four problems by giving the agent a place to store information and a way to bring it back when needed.

Now, let's understand what memory actually looks like inside an agent.

## The Memory Stack

AI Agent Memory is not a single thing. It is a stack of layers, each with a different lifespan and a different purpose. Let's decode each layer.

```
+--------------------------------------------+
|              AI Agent Memory               |
|                                            |
|  Layer 1: Context Window (in the prompt)   |
|     - In the current prompt                |
|     - Lost when context overflows          |
|                                            |
|  Layer 2: Short-Term Memory (session)      |
|     - Scratchpad, current task state       |
|     - Lost when the session ends           |
|                                            |
|  Layer 3: Long-Term Memory (persistent)    |
|     - Facts about the user                 |
|     - Past conversations                   |
|     - Learned preferences                  |
|                                            |
|  Layer 4: External Knowledge (tools/RAG)   |
|     - Documents, databases, APIs           |
|     - Queried, not maintained by agent     |
+--------------------------------------------+
```

- Layer 1 - Context Window. This is the text the LLM sees in a single call. It is the fastest memory because the LLM reads it directly. But it is also the smallest. Once it is full, older messages have to be dropped or summarized.
- Layer 2 - Short-Term Memory. This is the scratchpad the agent uses during one task or session. It holds the plan, the current step, and the intermediate results. When the session ends, this memory is usually gone.
- Layer 3 - Long-Term Memory. This is the persistent memory that survives across conversations and sessions. It stores user facts, preferences, past conversation summaries, and learned behaviors. This is what makes the agent feel like it "knows" the user.
- Layer 4 - External Knowledge. This is everything the agent can query but does not maintain - documents, databases, APIs, the web. The agent reads from these sources but does not write back to them as its own memory, even when the sources belong to the same company. Some frameworks classify this as a type of long-term memory; others keep it separate.

All four layers work together. The context window is the LLM's desk. Short-term memory is the notepad next to the desk. Long-term memory is the personal diary in the drawer. External knowledge is the library across the street. We want to keep our desk clean, our notepad organized, our diary trustworthy, and the library indexed.

Note: Within Long-Term Memory, there are further sub-types - episodic (past experiences), semantic (facts and concepts), and procedural (how to do things).

## The Four Core Operations

Now that we have seen the layers, let's look at what we actually do with them. No matter how many layers we have, every memory system does only four things.

1. Write. Save new information. When something important happens - a user preference, a task result, a key fact - we write it to memory. Example: after the user says "I prefer code in Go", we write "preferred language: Go" to long-term memory.

2. Read. Pull relevant information back when needed. This is usually the hardest part. We do not want everything, only what matters right now. Example: if the user asks "Write me a function to reverse a string", we pull up "preferred language: Go" before calling the LLM - but we do not pull up their shipping address.

3. Update. Modify existing memories when new information contradicts them. If the user's favorite language was Python last month and is now Go, the memory must be updated.

4. Forget. Remove memories that are stale, wrong, or no longer relevant. Without forgetting, the memory store grows forever and retrieval gets worse.

Memory System = Write + Read + Update + Forget.

If any one of these is broken, the whole memory system breaks. An agent that writes but never reads is a waste of disk space. An agent that reads but never updates will keep acting on outdated facts. An agent that never forgets will eventually drown in its own history. All four operations must work together.

## How Memory Flows at Runtime

Here is the flow as a picture:

```
                   User Message
                        |
                        v
          +----------------------------+
          |        READ Memory         |
          |  - Long-Term (user facts,  |
          |    preferences, summaries) |
          |  - Short-Term (plan,       |
          |    recent steps)           |
          +-------------+--------------+
                        |
                        v
          +----------------------------+
          |       Build Prompt         |
          |  (system prompt +          |
          |   retrieved memories +     |
          |   user message)            |
          +-------------+--------------+
                        |
                        v
          +----------------------------+    +---------------------+
          |            LLM             |<-->| External Knowledge  |
          |    (reasons, replies)      |    | (tools, RAG, APIs)  |
          +-------------+--------------+    +---------------------+
                        |
                        v
          +----------------------------+
          |        WRITE Memory        |
          |  - Short-Term (new step)   |
          |  - Long-Term (if worth     |
          |    keeping)                |
          +-------------+--------------+
                        |
                        v
                     Response
```

Steps on every user turn:

1. The user sends a message.
2. The agent searches long-term memory for anything relevant to this message.
3. The agent also reads its short-term memory for the current session - the plan so far, recent actions, and intermediate results.
4. The agent builds the prompt for the LLM by combining: the system prompt, the retrieved long-term memories, the short-term scratchpad, and the current user message.
5. The LLM reasons and responds. The agent may call tools (external knowledge) multiple times in a loop before producing its final response.
6. The agent writes new information to memory - short-term gets the new step; if something important was learned, it gets written to long-term too.
7. The response is sent to the user.

The same flow in pseudocode:

```
while user_active:
    user_message = receive_message()

    # READ
    long_term_context = search_long_term_memory(user_id, user_message)
    short_term_context = read_short_term_memory(session_id)

    # BUILD PROMPT
    messages = [system_prompt_with(long_term_context, short_term_context), user_message]

    # LLM LOOP (may call tools multiple times before the final answer)
    while True:
        response = call_llm(messages, tools)
        if response.is_tool_call:
            tool_result = call_tool(response.tool_name, response.tool_args)
            messages.append(response)
            messages.append(tool_result)
        else:
            break

    # WRITE
    write_short_term_memory(session_id, user_message, response)
    if is_worth_keeping(user_message, response):
        write_long_term_memory(user_id, user_message, response)

    send_to_user(response)
```

Note: In production, the long-term memory write is often done asynchronously after the response is sent, so the user does not pay the latency cost.

Example: User turn 1 - "My name is Priya and I code in Go." The agent writes to long-term memory: "User's name is Priya. Preferred language: Go." User turn 2 (a week later) - "Help me write a function that reverses a string." The agent retrieves "Priya, prefers Go", and the LLM responds with a Go function addressed to Priya.

## What to Store and What Not to Store

Store this:
- Stable user facts (name, role, language, timezone)
- Strong preferences (prefers short answers, wants code in Python)
- Outcomes of past tasks (what worked, what failed)
- Decisions that shape future work (architecture choices, policies, constraints)

Do not store this:
- Every single message (the context window already has the live conversation)
- Low-signal chit-chat ("hi", "thanks", "ok")
- Temporary state that is already in short-term memory
- Sensitive data we do not have consent to keep

In simple words: Store what will matter next week. Skip what only matters for the next minute.

Very important: Before writing anything to long-term memory, ask one simple question: "Will this be useful in a future conversation?" If no, do not write it.

## Common Mistakes and How to Fix Them

1. Context window overflow. Prompts get too long and either fail or get truncated, losing the oldest (and sometimes most important) information. Fix: summarize old turns, drop unneeded tool outputs, put only the most relevant retrieved memories in the prompt.

2. Retrieval misses the important memory. The memory is stored but the retrieval step doesn't find it. Fix: use semantic search (embeddings) instead of keyword match, store memories with good titles and descriptions, retrieve more candidates than needed and let the LLM pick. At scale, that similarity search is powered by ANN search.

3. Outdated memories. The agent keeps acting on old facts (the user's job changed but the agent still thinks they're a student). Fix: on every write, check if an existing memory contradicts it; if yes, update or replace. Do not just append.

4. Memory bloat. The store grows forever and retrieval gets slow and noisy. Fix: add a forget policy, delete memories not used in a long time or superseded by newer ones.

5. Privacy leaks. The agent surfaces one user's sensitive data while helping another. Fix: scope every memory to a user ID, never mix across users, encrypt at rest and in transit, require explicit consent before writing.

6. Confusing short-term and long-term. Ephemeral state written to long-term, or stable facts lost on session end. Fix: be deliberate about which layer each write goes to; when in doubt, prefer short-term - we can always promote later.

Very important: Most of these mistakes are silent. The agent does not crash - it just gives subtly wrong answers. That is why we must add logging, monitoring, and regular audits of the memory store.

## Quick Summary

- AI Agent Memory is the system that lets a stateless LLM act like it remembers across turns, sessions, and users.
- The memory stack has four layers: the context window, short-term memory, long-term memory, and external knowledge.
- The four core operations are Write, Read, Update, and Forget.
- The runtime flow on every turn is: retrieve relevant memories, build the prompt, call the LLM, write new memories, respond.
- Store what will matter next week. Skip what only matters for the next minute.
- Common mistakes include context overflow, retrieval misses, outdated memories, memory bloat, privacy leaks, and confusing the memory layers.
- Memory is what turns an LLM from a clever but forgetful answerer into an agent that truly knows us and improves over time.

### Does the LLM itself remember anything in an AI agent?

No. The LLM is stateless and does not actually remember anything. Every call starts fresh. The agent remembers on its behalf.

### What is the difference between short-term and long-term memory in an AI agent?

Short-term memory is the scratchpad for one task or session, holding the plan, the current step, and intermediate results. It is usually gone when the session ends. Long-term memory survives across conversations and sessions, storing user facts, preferences, past conversation summaries, and learned behaviors.

### Is RAG the same as agent memory?

Not exactly. RAG over documents or databases is external knowledge, which the agent can query but does not maintain or write back to as its own memory. Some frameworks classify it as a type of long-term memory, while others keep it separate.

### Should we store every message in long-term memory?

No. Storing too much is one of the biggest mistakes, because retrieval works well only if the memory store is not full of junk. We store stable user facts, strong preferences, past task outcomes, and key decisions. We skip low-signal chit-chat and anything that only matters for the next minute.

### Does writing to long-term memory slow down the agent's response?

Not necessarily. In production, the long-term memory write is often done asynchronously after the response is sent, so the user does not pay the latency cost of saving new memories.

Thanks
Amit Shekhar Founder @ Outcome School
