> Source: https://outcomeschool.com/blog/reflection-agent

# What is a Reflection Agent? How It Generates, Critiques, and Revises
URL: https://outcomeschool.com/blog/reflection-agent
Published: 2026-05-07
Author: Amit Shekhar

What is a Reflection Agent? How It Generates, Critiques, and Revises

# What is a Reflection Agent? How It Generates, Critiques, and Revises

Authors
: - Name
: Amit Shekhar
Published on
: May 7, 2026

A Reflection Agent is an AI Agent that first writes a draft, then reads and critiques its own draft, and then writes a better version using that critique. It repeats this until the work is good enough.

In this blog, we will learn about the Reflection Agent - what it is, how it is built, its anatomy, how it generates, critiques, and revises its own work, and how to handle its common failure modes.

We will cover the following:

- What is a Reflection Agent?
- Reflection Agent vs AI Agent
- Anatomy of a Reflection Agent
- How a Reflection Agent Works
- A Full Trace Example
- Reflection Agent vs ReAct Agent
- Common Failure Modes and How to Fix Them
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a Reflection Agent?

A Reflection Agent is an AI Agent built using the Reflection pattern. In this pattern, the agent first writes a draft, then reads its own draft and critiques it, then writes a better version using that critique. It repeats this loop until the work is good enough.

Let's decompose the term:

Reflection Agent = Reflection + Agent

Reflection is the self-review part - the agent reads its own output, judges what is wrong with it, and writes feedback for the next round. Agent is the wrapper around the LLM that runs this loop, keeps track of the drafts and critiques, and decides when to stop.

In simple words:

Reflection Agent = A Generator that writes a draft + A Critic that reviews the draft + A loop that revises until the work is good.

Think of a Reflection Agent like a writer working with an editor on the same essay. The writer puts down a first draft. The editor reads it and points out what is weak, what is missing, and what is unclear. The writer reads the feedback and writes a better second draft. The editor reads the new draft and points out what still needs work. The loop continues until the editor has nothing more to say. A Reflection Agent works the exact same way - one part writes, the other part reviews, and they keep improving the work together.

A plain LLM call gives us one draft and stops. A Reflection Agent gives us a draft, reviews it, revises it, and keeps going until the work passes its own quality bar. So, the Reflection Agent is useful whenever the first attempt is rarely good enough and we want the agent to improve its own work before handing it back.

Reflection is what we reach for when no exact checker exists for the task. We have a detailed blog on AI Is Only as Good as Our Definition of Done that explains this step by step.

## Reflection Agent vs AI Agent

Now, a natural question arises - if a Reflection Agent is an LLM in a loop, isn't that just an AI Agent? Let's clear this up.

Reflection is a pattern to build AI Agents. It is not a different category.

AI Agent is the broad category - any system where an LLM is wrapped in a loop with tools and memory. Reflection is one specific way to shape that loop, where the agent generates an output, critiques it, and uses the critique to produce a better one. Other patterns like ReAct, Plan-and-Execute, and Agentic RAG shape the loop differently.

In simple words:

Reflection is a way to build an AI Agent. It is one of the common patterns, especially for tasks where quality matters more than speed.

## Anatomy of a Reflection Agent

A Reflection Agent has five parts. Let's decode each one.

```
+--------------------------------------------------------+
|                    The Agent Loop                      |
|                                                        |
|   User Task                                            |
|       |                                                |
|       v                                                |
|   +-----------+         +--------+                     |
|   | Generator |  ---->  | Critic |                     |
|   +-----------+         +--------+                     |
|       ^                     |                          |
|       |                     v                          |
|       |               +------------+                   |
|       +-- (revise) -- | Stop Check | -> Final Output   |
|                       +------------+                   |
+--------------------------------------------------------+

```

1. The Generator. This is the LLM that writes the draft. It reads the user's task and produces the first version of the output. On later rounds, it reads the previous draft and the critique, and writes a revised version that addresses the feedback.

2. The Critic. This is the LLM that reviews the draft. It reads the draft and writes a critique - what is wrong, what is missing, what could be better. The critique is the signal the Generator uses to improve the next draft. In most setups, the Critic is the same LLM as the Generator, just called with a different prompt that asks it to review the draft. Using two separate models is also possible. The Critic is essentially LLM as a Judge used inside the loop - one LLM reading and scoring another LLM's output against a set of criteria.

3. The Tools. These are optional helpers the Critic can use to back up its review - search the web to check a claim, run a unit test to check the code, query a database to verify a fact, etc. Reflection Agents with no tools will rely only on the Critic's own judgement. A Critic that can actually run the code, check a citation, or verify a fact is much stronger than one critiquing from its own knowledge alone.

4. The Memory. This is the running history of the agent - the original task, every draft, every critique, and the revision count. The Generator reads it to know what to fix. The Critic reads it to track what has already been pointed out so it does not repeat the same feedback. In practice, keeping the full history blows up the context window after a few rounds, so most setups keep only the latest draft and critique, or summarize the older rounds.

5. The Stop Check. This is the part that decides when to stop the loop. It can stop when the Critic says the draft is good enough, when the maximum number of rounds is hit, or when two rounds in a row produce the same critique. Without a Stop Check, the loop can run forever. Deciding when a loop stops is one of the core problems of Loop Engineering.

All five parts work together.

## How a Reflection Agent Works

The flow is simple. The agent runs through three phases - Generate, Critique, and Revise - with a Stop Check after each Critique that decides whether to revise again or to stop.

Phase 1: Generate. The user gives the agent a task. The Generator writes the first draft. The draft is saved into memory.

Phase 2: Critique. The Critic reads the draft and writes a critique - what is wrong, what is missing, what can be better. The critique is saved into memory. The Stop Check then reads the critique and decides one of three things - the draft is good enough (stop and return it), the maximum number of rounds has been hit (stop and return the latest draft), or the loop continues to Revise.

Phase 3: Revise. The Generator reads the latest draft and the latest critique, and writes a new draft that addresses the feedback. The new draft is saved into memory. The loop returns to Phase 2 (Critique).

The loop continues until the Stop Check fires.

```
+----------+      +----------+      +-------+
| Generate | ---> | Critique | ---> | Stop? | ---> [yes] ---> Final Output
+----------+      +----------+      +-------+
                       ^                |
                       |                v [no]
                       |           +--------+
                       +---<-------| Revise |
                                   +--------+

```

Here, we can see that the Stop Check sits right after Critique - so the agent never wastes a Revise round when the first draft is already good enough.

This shape, where every step is a node and every arrow is an edge, is exactly what we design in Graph Engineering, and we have a detailed blog on it that covers this end to end.

Generate a draft. Critique the draft. Stop if good enough, otherwise revise.

## A Full Trace Example

Let's see this in action. Just for the sake of understanding, suppose the user gives the agent this task:

> "Write a one-paragraph product description for a wireless mouse aimed at office workers."

Phase 1: Generate.

The Generator writes the first draft:

```
This wireless mouse is good for office work. It connects to your computer
and lets you click and scroll. The battery lasts a long time. It is
comfortable to hold.

```

The draft is saved into memory.

Phase 2: Critique.

The Critic reads the draft and writes the critique:

```
- The draft is too generic. It does not mention any specific features
  that office workers care about, like silent clicks or a comfortable grip.
- The draft does not mention battery life in concrete numbers.
- The phrase "good for office work" is weak. The reader does not learn
  why it is good.
- The draft does not have a clear opening hook.

```

The critique is saved into memory.

Phase 3: Revise.

The Generator reads the previous draft and the critique, and writes a second draft:

```
Stay focused through long meetings and quiet workdays with our silent-click
wireless mouse, designed for office workers who care about a clean,
distraction-free desk. The contoured grip keeps your hand relaxed for
hours, and the precision scroll wheel makes long documents easy to skim.
A single AA battery powers the mouse for up to 18 months, so you can
forget about charging cables for good.

```

The new draft is saved into memory.

Note: The agent invented "18 months" of battery life to satisfy the critic's ask for "concrete numbers." The first draft did not have this number, and the Generator made one up. This is a real risk - when the Critic asks for specifics the model does not actually have, the Generator may fabricate them. We will cover this in the failure modes.

Stop Check. The Critic reads the new draft and finds nothing important to fix. The Stop Check fires. The agent stops.

Final Output:

> The second draft above is returned to the user.

Here, we can notice that the agent did not get the answer right on the first try. It wrote a weak first draft, read it, found the problems, and rewrote a much stronger second draft - all on its own.

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

## Reflection Agent vs ReAct Agent

A ReAct Agent and a Reflection Agent are two different patterns to build an AI Agent. Both are common. The difference is about what the loop is for.

A ReAct Agent uses the loop to explore - it thinks, picks a tool, reads the result, and thinks again to figure out what to do next. The loop is about gathering information and taking actions.

A Reflection Agent uses the loop to improve - it writes a draft, reviews the draft, and writes a better draft. The loop is about polishing the output until it is good enough.

Let's see this difference visually.

```
ReAct Agent - the loop is about exploring:

  +---------+   +--------+   +-------------+
  | Thought |-->| Action |-->| Observation |--+
  +---------+   +--------+   +-------------+  |
       ^                                      |
       +-- (loop until final answer) ---------+

Reflection Agent - the loop is about improving:

  +-----------+   +--------+   +--------+
  | Generator |-->| Critic |-->| Revise |--+
  +-----------+   +--------+   +--------+  |
       ^                                   |
       +-- (loop until good enough) -------+

```

Here, we can see that the ReAct Agent loops to learn what to do, while the Reflection Agent loops to make the output better. The ReAct Agent stops when it has enough information to answer. The Reflection Agent stops when the output passes its own quality bar.

Let me tabulate the differences between a ReAct Agent and a Reflection Agent for your better understanding so that you can decide which one to use based on your use case.

| Property | ReAct Agent | Reflection Agent |
| --- | --- | --- |
| Purpose of the loop | Explore - gather information and act | Improve - critique and revise the output |
| What changes per turn | The action picked and the observation | The draft itself |
| Tools | Central - the agent acts through tools | Optional - mostly used to back up the critique |
| Stop condition | The agent has enough to answer | The Critic is satisfied, or max rounds hit |
| Best for | Tasks that need external information | Tasks where quality matters more than speed |
| Cost | Grows with the number of tool calls | Grows with the number of revision rounds |
| Visibility | Reasoning is visible at every turn | Each draft and critique is visible at every round |

In simple words:

Use ReAct when the task needs information from the world. Use Reflection when the task needs the output to be polished.

We must skip Reflection altogether when:

- The first draft is usually correct - simple Q&A, classification, or lookups.
- Latency matters more than polish - real-time chat, voice agents.

If we want to go deep into the ReAct pattern, agent architecture, evaluation of LLMs and agents, and LLM as a Judge, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Common Failure Modes and How to Fix Them

A Reflection Agent is powerful, but it has its own set of mistakes that we must handle.

1. Soft Critic. The Critic praises the draft no matter what and never points out real problems. The agent stops on the first round and returns a weak output. To fix this, we must give the Critic a clear system prompt that asks for at least three specific issues per critique, and tell it that "no issues" is only allowed if the draft is genuinely strong against a list of named criteria.

2. Useless Critic. The Critic finds problems but writes vague feedback like "make it better" or "improve the wording." The Generator cannot act on this. To fix this, we must tell the Critic to write concrete, actionable feedback - "the second sentence is too long, split it" instead of "improve the flow."

3. Worse Revisions. The Generator reads the critique and writes a draft that is worse than the previous one. To fix this, we must keep the previous draft in memory and make the Stop Check compare the new draft against the previous one - if the new draft does not address the critique or is clearly worse, we revert to the previous draft.

4. Endless Loop. The Critic always finds something to fix, so the loop never ends. To fix this, we must set a maximum number of rounds (often 2 or 3 is enough) and a stop condition that triggers when two rounds in a row produce a critique with the same complaints.

5. Cost Explosion. Each Critique-and-Revise round costs one Critic call and one Generator call. A 5-round Reflection Agent costs roughly 1 initial generate + 5 critiques + 5 revises = 11 LLM calls for one task. To fix this, we must cap the number of rounds, use a smaller model for the Critic where the critique is structured against named criteria, and skip reflection entirely for tasks where the first draft is usually good enough.

6. Drift From the Task. The Critic keeps suggesting changes that make the draft longer, fancier, or more detailed - but drift away from what the user originally asked for. To fix this, we must give the Critic the original task in every prompt and ask it to first check whether the draft answers the user's task before suggesting any other improvements.

7. Hallucination via Critique. When the Critic asks for specifics the Generator does not actually have - like a concrete battery life, a real benchmark number, or a verified citation - the Generator may invent the value to satisfy the critique. The new draft looks better but is now wrong. To fix this, we must either give the Critic real tools to verify facts (web search, database lookup, code execution), or add a rule in the Critic's prompt that says "do not ask for specifics that are not in the original task or in the previous drafts."

Now, we have understood what a Reflection Agent is and how to handle the common failure modes.

## Quick Summary

Let's recap what we have learned:

- Reflection Agent is an AI Agent built using the Reflection pattern - generate a draft, critique it, revise it, and repeat until the work is good enough.
- Reflection Agent = Reflection + Agent - the Generator writes the draft, the Critic reviews it, and the Agent loop revises until the Stop Check fires.
- Anatomy has five parts - the Generator, the Critic, the Tools, the Memory, and the Stop Check.
- The flow has three phases - Generate, Critique, and Revise - looping until the output is good enough.
- Reflection vs ReAct - ReAct loops to explore the world, Reflection loops to improve the output. Use ReAct when the task needs external information. Use Reflection when the task needs the output to be polished.
- Common failure modes are Soft Critic, Useless Critic, Worse Revisions, Endless Loop, Cost Explosion, Drift From the Task, and Hallucination via Critique - all of them can be handled with a strict Critic prompt, a hard cap on rounds, real verification tools where possible, and a Stop Check that protects against bad revisions.
- Reflection is one of the most common patterns to build AI Agents that need to produce high-quality, polished output.

### Does the Critic have to be a separate model from the Generator?

No. In most setups, the Critic is the same LLM as the Generator, just called with a different prompt that asks it to review the draft. Using two separate models is also possible. Either way, the Critic works like an LLM as a Judge inside the loop.

### Does the Critic need tools to work?

No, tools are optional. Without tools, the Critic relies only on its own judgement. But a Critic that can actually run the code, check a citation, or verify a fact with a search or a database query is much stronger than one critiquing from its own knowledge alone.

### How many reflection rounds are usually enough?

Often 2 or 3 rounds are enough. We must set a maximum number of rounds because the Critic can always find something to fix. Every extra round costs one Critic call and one Generator call, so a hard cap also keeps the cost under control.

### Can a Reflection Agent make the output less accurate?

Yes. When the Critic asks for specifics the Generator does not actually have, like a concrete number or a verified citation, the Generator may invent the value. The new draft looks better but is now wrong. We fix this by giving the Critic real tools to verify facts, or by telling it not to ask for specifics that are not in the task or previous drafts.

### When should we skip the Reflection pattern?

We should skip Reflection when the first draft is usually correct, like simple Q&A, classification, or lookups. We should also skip it when latency matters more than polish, like in real-time chat or voice agents.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# How does LangGraph work?
URL: https://outcomeschool.com/blog/how-does-langgraph-work
Published: 2026-07-02
Author: Amit Shekhar

How does LangGraph work?

# How does LangGraph work?

Authors
: - Name
: Amit Shekhar
Published on
: July 2, 2026

[…450ln elided…]

This is how LangGraph works. We describe our AI application as a graph of nodes and edges, we let a shared state carry the data, we use conditional edges to make decisions, and we use a checkpointer for memory and human approval. We must also remember the key point about tools. The LLM only recommends which tool to use, and the agent actually calls the tool. The framework runs the graph for us, and we get a clear and powerful way to build complex AI applications in a very simple manner.

### What is the difference between LangGraph and LangChain?

LangGraph comes from the same team behind LangChain and builds on its ideas. It adds graphs, loops, and branching on top. In LangGraph, we describe the app as nodes and edges, a shared state carries the data, and the framework decides which step runs next.

### Do we need LangGraph for a simple question and answer app?

No. For one question and one answer, a plain LLM call is the best fit, and we do not need any framework. LangGraph becomes useful when our app has many steps, decisions, loops, tool calls, memory, or human approval.

### Do nodes in LangGraph call each other directly?

No. Each node reads from the shared state, does its work, and returns only the part of the state it wants to change. The edges then decide which node runs next. The state is the glue that holds the whole graph together.

### Can a LangGraph graph loop back to an earlier step?

Yes, looping back is built in. For example, after the LLM node, a conditional edge checks whether the LLM recommended a tool. If yes, the graph goes to the tool node, runs the tool, and loops back to the LLM node with the result. If no, it goes to `END`.

### Why does human-in-the-loop depend on the checkpointer?

Because the checkpointer saves the state after each step. This lets the graph stop at any node and wait. A human checks the saved state, makes a decision, and the graph resumes from that exact point.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# AI Orchestration
URL: https://outcomeschool.com/blog/ai-orchestration
Published: 2026-05-22

AI Orchestration

# AI Orchestration

Authors
: - Name
: Amit Shekhar
Published on
: May 22, 2026

In this blog, we will learn about AI Orchestration. We will understand what it is, why we need it, how it is different from AI Agents, and the common patterns we use to coordinate multiple LLMs, tools, and steps together to build real AI products.

We will cover the following:

- What is AI Orchestration?
- Why do we need AI Orchestration?
- AI Orchestration vs AI Agents
- Components of AI Orchestration
- How AI Orchestration works
- Patterns of AI Orchestration
- Sequential Pattern
- Parallel Pattern
- Conditional Pattern
- Loop Pattern
- Orchestrator-Worker Pattern
- Tools for AI Orchestration
- Challenges in AI Orchestration
- Best Practices

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is AI Orchestration?

AI Orchestration is the process of coordinating multiple AI components, such as LLMs, tools, data sources, and agents, to work together to finish a complex task.

In simple words, a single LLM call is not enough for most real-world tasks. We often need many LLM calls, many tool calls, and many steps that depend on each other. AI Orchestration is the layer that decides which component runs, in what order, with what input, and what to do with the output.

Let's say we have built an app that takes a user's question, searches our company documents, summarizes the top results, generates a final answer, and then translates it into the user's language. This is not one LLM call. This is many steps, and each step depends on the previous one. The system that coordinates all these steps is the AI Orchestration layer.

Think of it like a conductor in an orchestra. There are many musicians, each playing a different instrument. The conductor decides who plays when, who plays louder, and who stops. Without the conductor, the music will be a mess. In the same way, without AI Orchestration, our AI system will be a mess. So, here comes AI Orchestration to the rescue.

## Why do we need AI Orchestration?

A single LLM call can answer simple questions. But, real products are not that simple. In a real product, we have many models, many tools, many data sources, and many steps. We need a way to connect all of these in a clean and reliable way.

Here are the main reasons we need AI Orchestration:

- To break a complex task into many small steps that are easy to manage.
- To pick the right model or tool for each step. A small model for easy steps, a big model for hard steps.
- To pass the output of one step as the input of the next step in a clean way.
- To run independent steps in parallel and save time.
- To handle errors and retries when a step fails.
- To add guardrails, logging, and monitoring at every step.
- To control cost and latency by avoiding unnecessary model calls.
- To make the whole system easy to test, debug, and improve.

Without AI Orchestration, we end up with messy code that nobody can maintain. With AI Orchestration, our AI system becomes clean, reliable, and ready for production.

## AI Orchestration vs AI Agents

This is an important question. Many people think AI Orchestration and AI Agents are the same. But they are not.

In AI Orchestration, the developer defines the steps and the flow. The system follows a fixed plan that the developer wrote. The LLM does the work inside the steps, but it does not decide the flow.

In AI Agents, the LLM itself decides what to do next. The agent picks the tools, picks the order, and decides when to stop. The flow is dynamic and depends on the LLM's choices at runtime.

Let me tabulate the differences between AI Orchestration and AI Agents for your better understanding.

| Aspect | AI Orchestration | AI Agents |
| --- | --- | --- |
| Who controls the flow | The developer | The LLM |
| Flow type | Fixed, defined upfront | Dynamic, decided at runtime |
| Predictability | High | Low |
| Best for | Known workflows | Open-ended tasks |
| Cost control | Easier | Harder |
| Debugging | Easier | Harder |

In real systems, we often use both together. We use AI Orchestration for the high-level flow, and AI Agents inside one of the steps when the task is open-ended. This is how AI Orchestration is different from AI Agents.

## Components of AI Orchestration

Before we learn how AI Orchestration works, we must know the main components that we orchestrate.

- LLMs - The language models that do the thinking, writing, and decision-making.
- Prompts - The instructions we give to the LLMs at each step.
- Tools - Functions that the system can call, like a search API, a database query, or a calculator.
- Memory - The place where we store past messages, results, and state across steps.
- Data Sources - Vector databases, knowledge bases, files, and APIs that give us information.
- Guardrails - Safety checks that block bad inputs and bad outputs.
- Routers - Logic that picks which step or which model to use next.
- Workflows - The graph of steps that defines how everything connects together.

These are the building blocks. AI Orchestration is the art of putting them together in the right way.

## How AI Orchestration works

Now, let's understand how AI Orchestration actually works at a high level. The steps are:

- Step 1: The user sends a request to the system.
- Step 2: The orchestrator reads the request and picks the first step in the workflow.
- Step 3: The first step runs. It can call an LLM, a tool, or a data source.
- Step 4: The orchestrator stores the output of the first step in the shared memory.
- Step 5: The orchestrator picks the next step based on the workflow definition and the current state.
- Step 6: The next step runs and produces its output.
- Step 7: The orchestrator keeps running steps until the workflow reaches its end.
- Step 8: The orchestrator sends the final output back to the user.

At every step, the orchestrator can also log the input and output, check guardrails, retry on failure, and route to a different path based on the result. This is the power of AI Orchestration. It gives us full control over a complex AI system.

Now, it's time to learn the common patterns of AI Orchestration.

## Patterns of AI Orchestration

There are five main patterns that we use again and again in AI Orchestration. Do not worry, we will learn about each of them in detail.

- Sequential Pattern - Steps run one after another.
- Parallel Pattern - Many steps run at the same time.
- Conditional Pattern - The next step depends on the output of the previous step.
- Loop Pattern - A step or a group of steps runs again and again until a condition is met.
- Orchestrator-Worker Pattern - A main orchestrator splits work and gives it to many workers.

In real projects, we combine many of these patterns inside the same workflow. Now, let's discuss each one.

## Sequential Pattern

Sequential Pattern means the steps run one after another, in a fixed order, like a chain.

The best way to learn this is by taking an example. Let's say we are building a system that turns a long meeting transcript into clean meeting notes. The steps are:

- Step 1: Take the meeting transcript from the user.
- Step 2: Use an LLM to summarize the meeting.
- Step 3: Use an LLM to extract the action items from the summary.
- Step 4: Use an LLM to format the final notes in a clean structure.
- Step 5: Return the final notes to the user.

Here, each step depends on the previous one. We cannot extract the action items before the summary is ready. We cannot format the final notes before the action items are extracted. So, the sequential pattern is the right fit.

When each of these steps is an LLM prompt whose output feeds the next, this sequential pattern is exactly Prompt Chaining.

- Simple to design and understand.
- Easy to debug, because we know exactly which step is running.

Disadvantage:

- Slow, because every step waits for the previous one.
- One failure can break the whole chain.

This was all about the Sequential Pattern. Now, let's learn about the Parallel Pattern.

## Parallel Pattern

Parallel Pattern means many steps run at the same time, and we wait for all of them to finish before moving on.

Let's say we are building a research assistant. The user asks a question, and we want to search three sources at once: our internal documents, the web, and a research database. We do not need to wait for one search to finish before starting the next one. So, we run all three searches in parallel.

The steps look like this:

- Step 1: Take the question from the user.
- Step 2: Run three searches in parallel.
- Step 3: Wait for all three results.
- Step 4: Send all the results to an LLM to write the final answer.
- Step 5: Return the final answer to the user.

Here, we have saved a lot of time by running the three searches in parallel.

- Much faster than sequential when steps are independent.
- Makes good use of compute and network.

- Works only when steps do not depend on each other.
- Harder to debug, because many things happen at once.

This is how the Parallel Pattern works. Now, let's move to the Conditional Pattern.

## Conditional Pattern

Conditional Pattern means the next step depends on the output of the previous step.

In simple words, the system reads the output of one step and then decides which path to take next. This is also called branching or routing.

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

Let's say we are building a customer support bot. The user sends a message. The first step is to classify the message into one of three categories: billing, technical, or general. Based on the category, we route the message to a different path.

- If the category is billing, go to the billing flow with billing-specific tools.
- If the category is technical, go to the technical flow with technical tools.
- If the category is general, go to a simple FAQ flow.

The conditional pattern saves us a lot of cost. We do not run heavy technical tools for a simple billing question.

- Sends each request to the right path, which saves cost and time.
- Lets us build smart systems that adapt to the input.

- The routing decision can be wrong, which sends the request to the wrong path.
- Adds complexity to the design.

This was all about the Conditional Pattern. Now, it's time to learn about the Loop Pattern.

## Loop Pattern

Loop Pattern means a step or a group of steps runs again and again until a condition is met.

This is useful when we want to keep trying until we get a good result. For example, we want an LLM to write code, run the code, and if the code has errors, fix the errors and run again. This continues until the code works or until we hit a maximum number of tries.

Let's say we are building a code-writing assistant. The steps are:

- Step 1: Take the user's request.
- Step 2: Use an LLM to write the code.
- Step 3: Run the code in a sandbox.
- Step 4: If the code works, return it to the user.
- Step 5: If the code fails, send the error back to the LLM and ask it to fix the code.
- Step 6: Go back to Step 3 and try again.
- Step 7: Stop after 5 tries even if it still fails.

This is the Loop Pattern. It is very powerful, but we must always set a maximum number of tries. Otherwise, the loop can run forever and waste a lot of money. Designing that repeat properly - the budget, the stop condition, and what carries forward - is Loop Engineering.

- Lets the system improve its own output over many tries.
- Handles tasks where the first answer is rarely perfect.

- Can run forever if the stop condition is not set carefully.
- Costs more money, because we call the LLM many times.

This is how the Loop Pattern works. Now, let's learn about the Orchestrator-Worker Pattern.

## Orchestrator-Worker Pattern

Orchestrator-Worker Pattern means a main orchestrator splits a big task into many small tasks, gives each small task to a worker, and then combines the results.

This is the most powerful pattern, and it is used in big AI systems.

Let's say we want to write a long research report on a topic. The steps are:

- Step 1: The orchestrator reads the topic from the user.
- Step 2: The orchestrator breaks the topic into five sub-topics.
- Step 3: The orchestrator sends each sub-topic to a worker. Each worker is an LLM or a small agent that researches one sub-topic.
- Step 4: All workers run in parallel and send their results back.
- Step 5: The orchestrator combines all the results into one final report.
- Step 6: The orchestrator sends the final report to the user.

Here, the orchestrator is the brain. The workers are the hands. Each worker can use a different model, a different prompt, and different tools, based on the sub-topic. This makes the system both fast and powerful.

Sakana's Fugu is a real model built on this very pattern - it reads each question and routes it to the strongest frontier models, then combines their answers. We have a detailed blog on Sakana Fugu that explains how it orchestrates a team of frontier models.

- Scales very well for big tasks.
- Each worker can be focused on one sub-task, so the prompts stay simple.
- Workers can run in parallel for speed.

- More complex to design.
- The orchestrator must be smart enough to split and combine the work correctly.

This way we can use the Orchestrator-Worker Pattern to solve very complex problems in a clean and scalable way. We have a detailed blog on Multi-Agent Systems that explains how orchestrator and worker agents collaborate in real systems.

## Tools for AI Orchestration

Now, the next big question is: how do we actually build AI Orchestration in code? The answer is, we have many open-source tools that make our life easier.

Here are the most popular ones:

- LangChain - A popular framework that gives us building blocks for chains, tools, and memory.
- LangGraph - A graph-based orchestration framework on top of LangChain, which is good for complex workflows with loops and branches.
- LlamaIndex - A framework that is strong in data orchestration, especially for retrieval-augmented generation.
- Haystack - An open-source framework for building search and question-answering systems.
- CrewAI - A framework for orchestrating teams of AI agents that work together.
- Microsoft Semantic Kernel - A framework from Microsoft that mixes AI and traditional code.
- DSPy - A framework that lets us define the workflow as code and learn the best prompts automatically.

We do not have to pick just one. We can also write our own orchestration in plain code if our workflow is simple. The right choice depends on our use case.

## Challenges in AI Orchestration

Here are the main challenges:

- Latency - The more steps we add, the slower our system becomes. Each step adds delay.
- Cost - Every LLM call costs money. A workflow with ten LLM calls is ten times more expensive than one.
- Error handling - When one step fails, the whole workflow can break. We must plan for retries, fallbacks, and graceful failures.
- State management - We must keep track of the state across many steps. If the state is wrong, the next step will be wrong too.
- Observability - With many steps running in many directions, it becomes hard to know what is happening inside the system.
- Prompt drift - When we change one prompt, the output of that step changes, which can break the next step.
- Testing - It is hard to test a complex workflow end-to-end, especially when LLMs give different answers for the same input.
- Vendor lock-in - Some orchestration frameworks lock us into one vendor's tools. We must pick carefully.

Now, the next big question is: how do we deal with all these challenges? The answer is, we follow some best practices.

## Best Practices

Here are the best practices for AI Orchestration:

- Start simple - Do not jump into a complex orchestration framework on day one. Start with plain code or a simple chain. Add complexity only when we really need it.
- Pick the right pattern - Match the pattern to the task. Use sequential for chains, parallel for independent steps, conditional for routing, and loops for iterative tasks.
- Use the smallest model that works - For easy steps, use a small model. For hard steps, use a big model. Do not use a big model everywhere, because it wastes money.
- Add timeouts and retries - Every step must have a timeout. Every step must have a retry policy. This makes the system reliable.
- Log everything - Log the input, the output, the time, and the cost of every step. We will need these logs to debug and improve the system.
- Keep prompts in one place - Do not scatter prompts all over the code. Keep them in one folder so that they are easy to update and version.
- Test step by step - Test each step alone before testing the whole workflow. This makes debugging much easier.
- Add guardrails at the boundaries - Check inputs at the start, and check outputs at the end. This keeps the system safe.
- Watch cost from day one - Track cost per request and cost per user. A workflow that works in testing can become very expensive in production.
- Keep humans in the loop for critical steps - For high-stakes actions like sending an email or making a payment, ask for human approval before the action runs.

This way we can use AI Orchestration to build AI systems that are reliable, fast, and ready for production.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-340 and 791-1148 of 1148; 450 middle lines (21.6KB) elided. Read artifact://82 for full output]
