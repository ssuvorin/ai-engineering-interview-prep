> Source: https://outcomeschool.com/blog/context-engineering

# What is Context Engineering?
URL: https://outcomeschool.com/blog/context-engineering
Published: 2026-05-08
Author: Amit Shekhar

What is Context Engineering?

# What is Context Engineering?

Authors
: - Name
: Amit Shekhar
Published on
: May 8, 2026

Context Engineering is the practice of designing, organizing, and managing everything that goes into an LLM's context window, so that the model can do its task reliably.

In this blog, we will learn about Context Engineering - what it is, why it has become the most important skill for building reliable AI applications, how it differs from Prompt Engineering, the components that make up the context, common patterns like RAG, few-shot examples, tools, and memory, and the best practices and common mistakes to keep in mind.

We will cover the following:

- What is Context Engineering?
- The Big Picture
- Why Context Engineering matters
- Prompt Engineering vs Context Engineering
- The components of the context
- Common patterns in Context Engineering
- Common mistakes to avoid
- Best practices
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Context Engineering?

Context Engineering is the practice of designing, organizing, and managing everything that goes into an LLM's context window so that the model can do its task reliably.

In simple words, Context Engineering is the work of deciding what information to give the model, how to organize it, and when to include it, so that the model produces the right output.

The LLM itself is just a function. It takes whatever is in the context window and predicts the next tokens. Whatever the model says or does is decided entirely by what we have put into the context.

If the context is good, the output is good. If the context is bad, the output is bad. That is the whole story.

## The Big Picture

Before we go into the details, let's understand the big picture.

Imagine we are about to brief a brilliant new colleague who has just joined our team. This colleague is extremely smart and a fast worker. But there is one catch - they have no memory of anything we have discussed before. Every time we ask them to do a task, we have to brief them from scratch.

To get good work out of them, we need to give them, in one short briefing:

- Who they are and what role they are playing.
- What the task is.
- Any background documents they need to read.
- Examples of past work that look like what we want.
- The tools they can use.
- The format we want the answer in.

If we miss something, they cannot guess. They will do their best with whatever we hand them.

This is exactly what we are doing with an LLM. The LLM is the brilliant colleague. The context window is the briefing. Context Engineering is the discipline of writing that briefing well.

In simple words: Context Engineering = Briefing the LLM with the right information, in the right shape, at the right time.

## Why Context Engineering Matters

LLMs are stateless. They do not remember anything between calls. Every time we send a request, the model starts fresh. The only thing the model knows about our task is whatever we have included in the context window.

This means three things:

- The output of the LLM is decided entirely by the input context.
- A weak model with a great context can outperform a strong model with a poor context.
- As we move from simple chat to RAG, agents, and multi-step workflows, the context becomes more and more crucial. The complexity of the application is now mostly about context, not about the model.

Earlier, we used to spend most of our time picking the right model and tweaking the wording of the prompt. That is Prompt Engineering. Prompt Engineering is still useful, but it is now just one small part of a much bigger discipline.

Today, the real bottleneck for building reliable AI applications is Context Engineering. We have powerful models. What we need is the ability to feed them the right information at the right time.

This was all about why Context Engineering matters. Now, let's compare it with Prompt Engineering.

## Prompt Engineering vs Context Engineering

These two terms get mixed up a lot. Let's draw a clean line between them.

Prompt Engineering is the art of writing the wording of a single instruction well. For example, the difference between "summarize this article" and "summarize this article in three bullet points, written for a non-technical reader". The task is the same, but the wording produces different results.

Context Engineering is the bigger discipline of designing the entire information environment the model sees. It includes the prompt, but also the system instructions, the retrieved documents, the examples, the tool outputs, the memory, the conversation history, and the output format.

Let me tabulate the differences between Prompt Engineering and Context Engineering for your better understanding.

| Aspect | Prompt Engineering | Context Engineering |
| --- | --- | --- |
| Scope | One instruction at a time | The full context window |
| Concerns | Wording, phrasing, structure of one prompt | Everything the model sees: system prompt, RAG, tools, examples, memory, history |
| When it matters most | Simple one-shot tasks | RAG, agents, multi-step workflows, production systems |
| Failure mode | Bad wording leads to a bad answer | Missing or wrong context leads to wrong answers, hallucinations, or wrong tool use |
| Example fix | Rewriting a sentence in the prompt | Adding a retrieved document, adjusting memory, reordering the system prompt |

In short - Prompt Engineering is a subset of Context Engineering. Every prompt we write is part of the context, but the context is much more than just the prompt.

Let's see this as a diagram:

```
   +-------------------------------------------------+
   |  CONTEXT WINDOW (Context Engineering scope)     |
   |                                                 |
   |   System prompt                                 |
   |   Examples (few-shot)                           |
   |   Retrieved documents (RAG)                     |
   |   Tools and tool descriptions                   |
   |   Memory                                        |
   |   Conversation history                          |
   |   Tool results                                  |
   |                                                 |
   |   +-----------------------------------------+   |
   |   |  PROMPT (Prompt Engineering scope)      |   |
   |   |                                         |   |
   |   |  "Summarize this article in three       |   |
   |   |   bullet points for a non-technical     |   |
   |   |   reader."                              |   |
   |   +-----------------------------------------+   |
   |                                                 |
   +-------------------------------------------------+

```

Prompt Engineering tunes the small inner box - the wording of one instruction. Context Engineering designs the whole outer box - everything the model sees at this moment. Both matter, but Context Engineering is the bigger discipline.

This was all about Prompt Engineering vs Context Engineering. Now, let's see what actually goes into the context.

## The Components of the Context

When we look at the context window of a real LLM application, it is not just one prompt. It is a structured stack of pieces, each playing a different role.

Let's see this as a diagram:

```
       +------------------------------------------+
       |  CONTEXT WINDOW (what the LLM sees)      |
       +------------------------------------------+
       |                                          |
       |  1. System prompt                        |
       |     (role, rules, persona, format)       |
       |                                          |
       |  2. Examples (few-shot)                  |
       |     (input -> output samples)            |
       |                                          |
       |  3. Retrieved documents (RAG)            |
       |     (relevant external knowledge)        |
       |                                          |
       |  4. Tools and tool descriptions          |
       |     (what the agent can do)              |
       |                                          |
       |  5. Memory                               |
       |     (long-term facts, user preferences)  |
       |                                          |
       |  6. Conversation history                 |
       |     (previous turns)                     |
       |                                          |
       |  7. Tool results                         |
       |     (outputs from tool calls)            |
       |                                          |
       |  8. Current user message                 |
       |     (the latest question or instruction) |
       |                                          |
       +------------------------------------------+
                          |
                          ↓
                  LLM produces output

```

Let's decode each one.

1. System prompt. The system prompt sets the role, the rules, and the format. It is the "you are an X, you must do Y, you must not do Z, you must respond in Z format" piece. It defines the personality and the boundaries.

2. Examples (few-shot). A few input-output samples that show the model the pattern we want. Even one good example can dramatically improve the output. This is sometimes called in-context learning.

3. Retrieved documents (RAG). When the answer depends on external knowledge (a knowledge base, a docs site, a database), we retrieve the most relevant chunks and put them in the context. We have a detailed blog on Agentic RAG that goes deeper into this.

4. Tools and tool descriptions. When the LLM is acting as an agent, the context includes a list of tools available to it (function names, descriptions, parameter schemas). This is what tells the LLM what it can do.

5. Memory. Long-term facts about the user, past conversations, learned preferences. We have a detailed blog on AI Agent Memory that explains how memory is structured for agents.

6. Conversation history. The previous turns in the current session. This is what gives the model continuity in a chat.

7. Tool results. When the LLM has recommended a tool (search, calculator, database query) and the runtime has executed it, the result of that tool comes back into the context for the next turn.

8. Current user message. The fresh question or instruction the user just sent.

All eight of these compete for the same finite context window. Context Engineering is the discipline of deciding what goes in, in what order, and at what size.

A quick note for you

No matter which tech domain you work in, get familiar with these topics:

- LLM
- RAG
- MCP
- Agent
- Fine-tuning
- Quantization

We put it all together in one video:

AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, and Quantization

No need to stop reading - bookmark it and watch later when you get time. Future you will thank you.

Now, let's get back to the topic.

Coming back to our briefing analogy - the system prompt is the job role we hand the colleague, the examples are the past work we point them at, the retrieved documents are the binder of background reading, the tools are the equipment they can use, the memory is what we have learned about them and the user across past meetings, the conversation history is the meeting we are currently in, the tool results are the answers they got back from running their equipment, and the current user message is the latest thing the user just said. Every briefing has to fit on one page. That one page is the context window.

This was all about the components of the context. Now, let's see the common patterns we use to fill them.

If we want to go deep into RAG, Vector Databases, Memory in Agents, and Tool use in Agents, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Common Patterns in Context Engineering

Before we go through the patterns, let's see what actually happens at every turn.

The context is not stored anywhere. It is rebuilt from scratch every single turn. We pull pieces from different sources and assemble them into one fresh context for that one call.

Let's see this as a diagram:

```
   For each new turn, we pull from these sources:

      +----------+   +----------+   +----------+   +----------+
      |  System  |   |  Memory  |   |   RAG    |   |Few-shot  |
      |  prompt  |   |  store   |   |retrieval |   |examples  |
      +----------+   +----------+   +----------+   +----------+

      +----------+   +----------+   +----------+   +----------+
      |  Tool    |   |   Tool   |   |  Conv.   |   | Latest   |
      |  list    |   |  results |   | history  |   |  user    |
      |          |   |(if any)  |   |          |   | message  |
      +----------+   +----------+   +----------+   +----------+

              All combined into one single input:
                                  ↓
                  +-------------------------------+
                  |     Assembled context         |
                  |     (sent to the LLM)         |
                  +-------------------------------+
                                  |
                                  ↓
                         LLM produces output
                                  |
                                  ↓
                  Next turn rebuilds the context
                  from scratch (with any new tool
                  results from this turn included)

```

Here, we can see that Context Engineering is not a one-time setup. It is a fresh decision on every turn. Each pattern below is a tool we use to fill one of these boxes well.

Now, let's go through the most important patterns.

1. RAG (Retrieval-Augmented Generation).

Instead of stuffing the entire knowledge base into the context, we retrieve only the most relevant pieces and inject them. This keeps the context small and focused.

We pair RAG with chunking, embedding-based search, and re-ranking to make sure the right pieces land in the context.

2. Few-shot examples.

We include a handful of example pairs of input and the desired output (2-5 is a good starting range, but the optimum varies by task). The model learns the pattern from the examples and follows it. This is one of the cheapest ways to lift quality.

3. Tool calling.

Instead of asking the model to do everything itself, we give it tools and let it recommend which tool to use when needed. The runtime then executes the recommended tool. The tool definitions live in the context, and so do the tool results when they come back.

This is the foundation of building an AI Agent, and it overlaps closely with Harness Engineering, which is the broader design of the loop, tools, and context that an agent runs inside. It also overlaps with Loop Engineering, which is the design of the repeating cycle itself - how many turns the agent gets, what carries forward, and when it must stop.

4. Memory injection.

For agents and chat systems, we keep a memory of important facts and inject only the relevant slices into the context for each new turn. We do not put the entire memory in every time. We pick what is relevant to the current task.

5. Conversation history management.

In a long chat, the full history grows past the context window. We use techniques like summarization, sliding windows, or selective inclusion to keep the conversation history within budget.

6. Output formatting.

We tell the model the exact output format we want - JSON, a specific schema, a markdown table, a structured form. Putting the format requirement in the context makes downstream parsing reliable.

For truly reliable parsing, structured output APIs and JSON schema constraints (offered by most modern model providers) are stronger than prompt-based formatting alone. The prompt asks for the format, the schema enforces it.

7. Context compression.

When the raw context is too long, we compress it. This can be summarization, key-fact extraction, or structured rewriting. The goal is to keep the meaning while shrinking the token count.

8. Per-step context rebuilding (for agents).

In an AI agent, every step in the loop is a fresh LLM call with a freshly built context. Between steps, the agent's state changes - new tool results come in, sub-tasks get completed, plans get revised. We rebuild the context for the next step using only what is relevant right now: the current sub-task, the latest tool result, the relevant facts from memory. We do not just append everything endlessly.

The agent that does this well stays focused. The agent that does not gets buried under old, useless information and fails the task.

This was all about the patterns. Now, let's see the common mistakes to avoid.

## Common Mistakes to Avoid

Most failures in LLM applications are actually Context Engineering failures. Here are the most common mistakes.

Mistake 1: Stuffing the context with everything.

A bigger context is not always a better context. When too much information is in the context, the model gets distracted, slows down, costs more, and often produces worse answers. The model has to pick the relevant signal out of a lot of noise, and the more noise we add, the harder it gets. The community is now calling this context rot or context degradation - the slow decay in answer quality as the context grows past what the task actually needs.

The fix is to be ruthless about what goes in. Only include what is needed for this turn.

Mistake 2: Not including enough.

The opposite mistake. The model cannot guess what it does not see. If we expect the model to know our company's policy on refunds, that policy must be in the context.

The fix is to ask: "If I were doing this task, what would I need to know? Is all of that in the context?"

The harder part is that this knowledge usually lives in people's heads, wikis, and code comments, so there is nothing to put in the context in the first place. OKF is an open standard for writing exactly that knowledge down as plain markdown files an agent can read. We have a detailed blog on What is OKF (Open Knowledge Format)? that explains how it works.

Mistake 3: Bad ordering.

Order matters. The model pays more attention to information at the start (the system prompt area) and the end (the most recent message). Putting critical instructions in the middle of a long context is a recipe for the model ignoring them. This is a well-studied phenomenon called "lost in the middle" - models genuinely under-attend to information buried deep inside a long context.

The fix is to put rules and instructions at the start, and the current task at the end.

Mistake 4: Stale context.

Old conversation history, old tool results, old retrieved documents that are no longer relevant - all of this clutters the context and confuses the model.

The fix is to actively prune the context. If something is not relevant to the current step, remove it.

Mistake 5: No structure.

Pasting a wall of text into the context with no headers, no separators, no labels makes it hard for the model to parse. Even though LLMs can read unstructured text, structure helps them focus.

The fix is to use clear section markers, headers, and consistent formatting.

Mistake 6: Confusing instructions.

When the system prompt says one thing and the user message says another, the model has to guess which one to follow. When two retrieved documents contradict each other, the model has to pick one.

The fix is to design the context so that there is one clear answer to "what should the model do right now".

This was all about the common mistakes. Now, let's see the best practices.

## Best Practices

Here are the best practices that experienced teams follow.

1. Treat the context as a budget.

[…470ln elided…]

Let's break the term into two parts.

Loop means something that repeats. The agent does a step, and then it does another step, and then another one, until some condition tells it to stop.

Engineering means designing that repetition on purpose, with rules, limits, and checks, instead of letting it run wild.

So, Loop Engineering is the deliberate design of the repeat.

The best way to learn this is by taking an example.

Let's say we are cooking a soup. We taste it. It needs salt. We add a pinch of salt. We taste it again. It is still not enough. We add another pinch. We taste again. Now it is good, so we stop and serve it.

Here, we can see a loop. Taste, decide, act, taste again.

Now think about what can go wrong. A cook who never tastes will never know when to stop. A cook who forgets that salt was already added will keep adding salt forever. A cook who tastes a hundred times will serve the soup cold. A cook who never decides that the soup is good enough will never serve it at all.

Loop Engineering is everything we do to prevent these problems. How many tastes are allowed, what the cook must remember, what "good enough" means, and what to do when the soup is already ruined.

An AI agent has exactly the same problems. Let me map the kitchen to the agent for your better understanding.

| In the kitchen | In the agent |
| --- | --- |
| The cook | The AI model that decides what to do next |
| Adding a pinch of salt | An action, such as running a command or reading a file |
| Tasting the soup | Looking at the result of that action |
| Remembering the salt already added | The memory that carries from one turn to the next |
| "The soup is good enough" | The definition of done |
| "Serve it before it goes cold" | The limit on how many turns are allowed |

### Why do we need Loop Engineering?

Earlier, we used a language model like a vending machine. We put in a question, we got out an answer, and the story ended there. One request, one response.

But real tasks are not like that. Consider a task like "find the bug in this file and fix it". The model cannot do this in one shot, because it does not know what is inside the file yet. It must read the file first. After reading, it must run the test. After running the test, it must see the error. After seeing the error, it must edit the code. After editing, it must run the test again to confirm.

So, the work naturally becomes a sequence of steps, and each step depends on the result of the previous one. That is a loop.

Once we put a model inside a loop, a new class of problems arrives that never existed in the single-question world. The agent can repeat itself. It can forget what it already did. It can drift away from the original goal. It can run forever and burn a lot of money. It can declare success when nothing actually worked.

None of these are problems of the prompt. They are problems of the loop.

Now, let's take a real use-case. A coding agent that fixes a failing test, a research agent that reads twenty pages before writing a summary, and a support agent that checks an order, then checks the refund policy, then raises a ticket. Every one of them is a loop running behind the scenes. The company that builds the better loop ships the better agent, even when everyone is calling the very same model.

So, here comes Loop Engineering to the rescue.

### What is a loop in an AI agent?

Before jumping into the loop, we must know one word that we will use again and again from here onwards.

The context is everything the model can see at this moment. It is the working notepad of the agent. The goal sits in it, the earlier steps sit in it, and every result sits in it. The model has no other memory. If a fact is not in the context, then for the model that fact does not exist.

Now, one turn of an agent loop has three parts.

Think: the model reads the context and decides what to do next.

Act: the system runs the thing the model asked for. The model cannot touch the outside world by itself, so it asks for a tool. A tool is simply a small program that we hand to the model, such as one that reads a file, searches the web, runs a command, or fetches data from another service.

Observe: the result of that action comes back and gets added to the context.

Then the turn ends, and the next turn begins with that updated context. Think, act, observe. Again and again.

This think, act, observe cycle is exactly the pattern behind a ReAct Agent, and we have a detailed blog on it that explains this in depth.

The important thing to notice is that the model itself does not loop. The model just produces one output when we call it. The loop is code that we write around the model. That is why we can engineer it.

> The model decides what to do next. The loop decides what actually happens.

### The simplest loop and its problems

Let's see the most basic version of an agent loop as below:

```python
while True:
    decision = model(context)
    result = run_tool(decision.tool, decision.input)
    context = context + result

```

Here, we can see that the model looks at the context, picks a tool, we run that tool, and we paste the result back into the context. Then it goes around again.

This works for a small demo, and it fails badly in the real world.

Problem 1: There is no stop. `while True` means the agent can go around a thousand times if the model never says it is finished.

Problem 2: The context only grows. Every raw tool result gets pasted in. After twenty steps, the context is huge, expensive, and full of noise.

Problem 3: There is no error handling. If the tool crashes, the whole loop crashes with it.

Problem 4: There is no definition of done. Nothing in this code knows what success looks like.

The issue with this approach is that it trusts the model to manage itself. Let's see how the next approach solve this issue.

### The parts of the loop that we must engineer

There are seven parts in a loop, and each one is a decision that we, the engineers, must make.

The goal. The loop must carry a clear statement of what finished means. "Fix the bug" is weak. "The test named `test_login` passes" is strong, because a machine can check it.

The step budget. The loop must have a maximum number of turns. When the budget runs out, the agent stops and reports honestly that it did not finish.

The tools. The list of actions the agent is allowed to take. A short, sharp list of tools produces a much better loop than a long list of overlapping ones, because the model has fewer wrong turns available to it.

The observation. What we paste back after a tool runs. A tool that returns ten thousand lines of output will drown the loop. We must trim it, or summarize it, or return it in small pages, before it enters the context.

The memory. What carries forward from turn to turn. Full history is honest but expensive. A running summary is cheap but can lose details. This choice shapes everything.

The feedback on failure. When a tool returns an error, the message we paste back is a teaching signal. "Error" teaches nothing. "File not found at path `src/mian.py`, did you mean `src/main.py`" lets the agent recover on the very next turn.

The exit. The set of conditions under which the loop stops. Success, budget exhausted, repeated failure, or a request for a human. Every one of these must be handled.

Now, we have understood the parts. Let's see them inside real code.

Our updated loop:

```python
MAX_STEPS = 12

def run_agent(goal, context):
    for step in range(MAX_STEPS):
        # the goal goes in on every single turn, so the agent cannot drift
        decision = model(goal, context)

        if decision.is_done:
            if verify(goal):          # check the claim, do not believe it
                return decision.answer
            context = add(context, "Verification failed. Keep working.")
            continue

        try:
            result = run_tool(decision.tool, decision.input)
        except ToolError as e:
            # a crash becomes a lesson instead of the end of the run
            result = f"Tool failed: {e}. Try a different approach."

        context = add(context, trim(result))

    return "Could not finish within the step budget."

```

Here, we have made six changes.

- `MAX_STEPS` gives the loop a hard ceiling, so it can never run forever.
- The `goal` is passed in on every turn, so the agent always knows where it is headed.
- `decision.is_done` gives the model a proper way to say that it has finished.
- `verify(goal)` checks that claim with real code instead of believing it. If the check fails, we tell the agent and let it continue.
- The `try` block turns a crash into a message, so a broken tool becomes a lesson instead of the end of the run.
- `trim(result)` keeps the observation small, so the context stays clean.

Note: the `verify` step is the single most valuable line here. Without it, an agent will happily tell us that the bug is fixed while the test is still failing.

This is how a loop stops being a demo and starts being a system.

A quick note for you

No matter which tech domain you work in, get familiar with these topics:

- LLM
- RAG
- MCP
- Agent
- Fine-tuning
- Quantization

We put it all together in one video:

AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, and Quantization

No need to stop reading - bookmark it and watch later when you get time. Future you will thank you.

Now, let's get back to the topic.

### Prompt Engineering vs Context Engineering vs Loop Engineering

These three names sound similar, so let's separate them clearly.

Prompt Engineering is about the wording of one instruction. What do we say to the model, and how do we say it.

Context Engineering is about the content of that notepad. What information sits in front of the model at this moment, where it came from, and what we left out.

Loop Engineering is about the shape of the repetition. How many turns, what changes between turns, what carries forward, and when it ends.

Let me tabulate the differences between the three for your better understanding.

| Point | Prompt Engineering | Context Engineering | Loop Engineering |
| --- | --- | --- | --- |
| Unit of work | One instruction | One context | One full run |
| Main question | What do we say? | What does the model see? | What happens next, and when do we stop? |
| Typical fix | Rewrite the wording | Add, trim, or reorder information | Add a budget, a check, or a better exit |
| Failure it prevents | A vague or misread answer | A confused or overloaded model | An endless, drifting, or falsely successful run |
| Who controls it | The person writing the prompt | The code that gathers the information | The code that runs the model again and again |

Prompt Engineering fixes what the model hears, Context Engineering fixes what the model knows, and Loop Engineering fixes what the model is allowed to do over time.

This was all about the comparison. Now, let's learn about the ways a loop breaks in practice.

### Common ways a loop breaks

Most of the time, we do mistakes while designing the loop, and the same failures show up again and again.

The endless loop. The agent keeps taking turns and never decides that the work is complete. It usually happens when the goal has no definition of done that a machine can check.

The repeating loop. The agent runs the same failing command four times in a row and expects a different result. It happens when the failure message carries no new information, so the model has no reason to change its plan.

The forgetting loop. The agent solves a sub-problem on turn three, and by turn fifteen that solution has been squeezed out of the context. The agent then solves the same sub-problem again. This is a memory design failure.

The drifting loop. The agent starts by fixing a login bug and ends up rewriting the whole database layer. Each single step looked reasonable, and the destination is completely wrong. It happens when the original goal is not repeated in the context on every turn.

The lying loop. The agent announces that the task is complete, and nothing was actually verified. This is the most dangerous one, because the run looks successful in the logs.

The expensive loop. The agent finishes correctly, and it took ninety turns and a very large bill, because every raw tool output was pasted in and re-sent on every single turn.

Now that we have seen the failures, it is time to learn the techniques that prevent them.

### Techniques of Loop Engineering

Give a step budget. Set a maximum number of turns and stop cleanly when it is reached. A run that reports "I could not finish in twelve steps, here is how far I got" is far more useful than a run that never returns.

Make done checkable by a machine. Do not ask the loop to decide that the code "looks correct". Ask it to run the test and read the pass or fail result that the computer itself reports. If a machine cannot check the goal, the loop cannot reliably end.

Verify before we trust. When the model says it is finished, run the check ourselves. If the check fails, put that fact into the context and continue the loop.

Repeat the goal every turn. Keep the original task at the top of the context on every single turn. This costs a few extra words on every turn, and it is the cheapest cure for drift.

Make failures informative. Turn an error into a hint. Instead of pasting the full crash report, paste the one line that matters plus a short note about what to try next.

Break the repeat. Detect when the same action is being attempted again with the same input. When that happens, block it and add a message such as "This exact command already failed twice. Try a different approach."

Trim every observation. Before a tool result enters the context, cut it down. The first few and the last few lines of a long output, the first twenty search results instead of all of them, the relevant function instead of the whole file.

Compact the history. When the context crosses a threshold, replace the old turns with a short summary that keeps the decisions and the facts learned, and drops the raw noise. The agent then continues with a light, clean context. We have a detailed blog on context compaction that explains this step by step.

Plan first, then loop. Ask for a short plan on the first turn, and keep that plan visible in the context. Each later turn then works against a written list instead of a vague memory, and the drift problem shrinks a lot. This is the idea behind the Plan-and-Execute Agent, and we have a detailed blog on it that covers the pattern end to end.

Use sub-loops. When a step is big, hand it to a separate agent with its own small loop, its own budget, and its own tools. The sub-agent returns only its final result. The parent loop stays short and clean, because all the noisy intermediate steps stayed inside the child.

Keep a human in the loop for irreversible steps. Deleting data, sending an email, moving money, deploying to production. The loop must pause and ask before crossing these lines.

Let me tabulate the failures against their fixes for your better understanding so that you know exactly which technique to reach for.

| The failure | The fix |
| --- | --- |
| The endless loop | A step budget and a finish line a machine can check |
| The repeating loop | Better failure messages, and blocking a repeated action |
| The forgetting loop | Compact the history instead of dropping the old turns |
| The drifting loop | Repeat the goal every turn, and plan first |
| The lying loop | Verify the claim with code before exiting |
| The expensive loop | Trim every observation, and use sub-loops |

If we want to go deep into Loop Engineering, Memory in Agents, Context Engineering, and Subagent, we cover all of them from the ground up in our AI and Machine Learning Program at Outcome School.

### A complete example

Let's take a real task. The goal is: "The test `test_login` must pass."

Turn 1. The agent reads the goal. It calls the tool that runs the test. The result comes back as a failure, and it points at line 42. We trim the output to the goal, the failing test name, and that one error line.

Turn 2. The agent reads line 42 and the function around it. It sees that a token is compared before it is created.

Turn 3. The agent edits the file to move the token creation above the comparison.

Turn 4. The agent runs the test again. It fails with a different error now, which tells us that the loop is making progress and not spinning.

Turn 5. The agent reads the new error, sees a missing import, and adds it.

Turn 6. The agent runs the test. It passes. The agent says it is done.

The verify step. The loop does not simply believe this. It runs the whole test suite one final time itself. Every test passes, so the loop exits and returns the answer.

Here, we can notice a few things. The loop had a budget of twelve turns and used six. The goal was checkable by a machine, so the ending was never in doubt. Each error message pointed at exactly one line, so every turn changed the plan. And the final claim was verified by code, not accepted on trust.

That is a well engineered loop.

### Where it works well and where it fails

Where it works well:

- Tasks that have a clear finish line that a machine can check, such as tests passing, a build succeeding, or a file matching a required format.
- Tasks where the environment gives honest feedback after every action, such as a compiler, a test runner, or a service that returns a real error message.
- Tasks that can be broken into small steps, where a wrong step is cheap to undo.
- Long tasks where the agent must gather information before it can even plan.

Where it fails:

- Tasks with no objective finish line, such as "make this essay better". The loop has nothing to check, so it either stops too early or never stops.
- Environments that give slow or silent feedback. If a mistake shows up only thirty minutes later, the loop cannot learn from it in time.
- Actions that cannot be undone. A loop that experiments freely is a very bad fit for production systems and real money.
- Very long tasks where the context must hold hundreds of facts. The summarizing starts dropping things, and the forgetting loop appears.

Now we must have understood what Loop Engineering is. Prompt Engineering shapes one sentence, Context Engineering shapes what the model sees, Graph Engineering shapes the path from one step to the next, and Loop Engineering shapes the whole run from the first turn to the last. As agents take on longer and longer work, the quality of the loop, and not the cleverness of the prompt, decides whether the work actually gets finished.

### Can a stronger model make up for a badly designed loop?

No. A strong model inside a badly designed loop will still fail, while a modest model inside a well designed loop will often finish the job. The loop decides how many times the model tries, what it sees on each try, what it is allowed to do, and when it must stop.

### Should we trust an agent when it says the task is done?

No. We must verify the claim with real code before the loop exits, such as running the tests ourselves. If the check fails, we put that fact into the context and let the agent continue. Without this step, an agent can report that a bug is fixed while the test is still failing.

### What should an agent do when it runs out of its step budget?

It should stop cleanly and report honestly that it did not finish. A run that says it could not finish within the budget and shows how far it got is far more useful than a run that never returns. The step budget is what keeps the loop from running forever.

### Is it good to paste the full tool output back into the context?

No. If every raw tool result is pasted in, the context keeps growing and becomes huge, expensive, and full of noise. We must trim each observation first, such as keeping only the relevant lines, the first few search results, or the one function we need instead of the whole file.

### What is the difference between Loop Engineering and Graph Engineering?

Graph Engineering shapes the path from one step to the next, while Loop Engineering shapes the whole run from the first turn to the last. Loop Engineering focuses on the repeating think, act, observe cycle of an agent, including its step budget, memory, feedback on failure, and exit conditions.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-356 and 827-1144 of 1144; 470 middle lines (25.9KB) elided. Read artifact://81 for full output]
