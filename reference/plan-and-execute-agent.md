> Source: https://outcomeschool.com/blog/plan-and-execute-agent

# What is a Plan-and-Execute Agent and How Does It Work?
URL: https://outcomeschool.com/blog/plan-and-execute-agent
Published: 2026-05-04

What is a Plan-and-Execute Agent and How Does It Work?

# What is a Plan-and-Execute Agent and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: May 3, 2026

A Plan-and-Execute Agent is an AI Agent that first writes the full plan up front, and then runs that plan step by step, instead of figuring out the next step after every action.

In this blog, we will learn about the Plan-and-Execute Agent - what it is, its anatomy, how it plans and runs the steps, how it differs from a ReAct Agent, and how to handle its common failure modes.

We will cover the following:

- What is a Plan-and-Execute Agent?
- Plan-and-Execute Agent vs AI Agent
- Anatomy of a Plan-and-Execute Agent
- How a Plan-and-Execute Agent Works
- A Full Trace Example
- Plan-and-Execute Agent vs ReAct Agent
- Common Failure Modes and How to Fix Them
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a Plan-and-Execute Agent?

A Plan-and-Execute Agent is an AI Agent built using the Plan-and-Execute pattern. In this pattern, the agent first writes the full plan up front, and then runs the plan step by step. It does not figure out the next step on the fly at every turn. It thinks once at the start, walks through the plan, and re-plans only when reality does not match the plan.

Let's decompose the term:

Plan-and-Execute Agent = Plan + Execute + Agent

Plan is the thinking part - a strong LLM reads the user's task and writes a full step-by-step plan to solve it. Execute is the doing part - typically a smaller, cheaper LLM picks a tool for each step, and the runtime calls the tool. Agent is the wrapper around both that connects the Planner and the Executor, tracks progress, and decides when the task is done.

In simple words:

Plan-and-Execute Agent = A Planner that writes the steps + An Executor that runs the steps + A loop that connects them.

Think of a Plan-and-Execute Agent like a project manager and a worker on a team. The project manager reads the requirement, writes a clear list of tasks, and hands it over. The worker picks up each task, finishes it, and reports back. If things go off track, the project manager updates the plan. A Plan-and-Execute Agent works the exact same way - one part plans, the other part executes.

A plain LLM call gives us one response and stops. A Plan-and-Execute Agent gives us a full plan, runs each step, and keeps going until every step is complete. So, the Plan-and-Execute Agent pattern is used whenever a task has many steps and we want the agent to think through the whole journey before starting.

Before an agent plans and executes on its own, the simplest way to run a task as a series of steps is Prompt Chaining, where we pass the output of one prompt into the next by hand.

## Plan-and-Execute Agent vs AI Agent

Now, a natural question arises - if a Plan-and-Execute Agent is an LLM in a loop with tools, isn't that just an AI Agent? Let's clear this up.

Plan-and-Execute is a pattern to build AI Agents. It is not a different category.

AI Agent is the category - any system where an LLM is wrapped in a loop with tools and memory. It does not say how the loop is structured, whether the agent plans ahead, or whether the planning and execution are split across different LLM calls.

Plan-and-Execute is a pattern for building that loop, where the agent first generates the full plan in one LLM call, and then runs each step of the plan with another LLM call (or a series of them). The planning is done once at the start. The execution happens step by step after that.

So when we say "Plan-and-Execute Agent," we mean an AI Agent built with the Plan-and-Execute pattern. Other patterns like ReAct, Reflection, and Agentic RAG also build AI Agents - they just shape the loop differently.

In simple words:

Plan-and-Execute is a way to build an AI Agent. It is one of the common patterns, especially for tasks with many steps.

## Anatomy of a Plan-and-Execute Agent

A Plan-and-Execute Agent has five parts. Let's decode each one.

```
+--------------------------------------------------------+
|                     The Agent Loop                     |
|                                                        |
|   User Task                                            |
|       |                                                |
|       v                                                |
|   +---------+                                          |
|   | Planner |  --->  Plan: [Step 1, Step 2, Step 3]    |
|   +---------+                                          |
|       |                                                |
|       v                                                |
|   +----------+         +-------+                       |
|   | Executor |  <--->  | Tools |                       |
|   +----------+         +-------+                       |
|       |     ^                                          |
|       v     | (updated plan, if needed)                |
|   +------------+                                       |
|   | Re-Planner |                                       |
|   +------------+                                       |
|       |                                                |
|       v                                                |
|   Final Answer (when the task is done)                 |
+--------------------------------------------------------+

```

1. The Planner. This is the LLM that writes the plan. It reads the user's task and produces a list of steps to solve it. The plan is usually a numbered list, where each step is a small, clear instruction. A good Planner breaks the task into steps that the Executor can run one at a time.

2. The Executor. This is the part that runs each step of the plan. The LLM inside the Executor is usually smaller and cheaper than the Planner, since each step is much narrower than the full task. The LLM picks a tool for the current step, the runtime calls the tool, and the result is saved into memory. In some setups, the Executor is itself a small sub-agent like a ReAct loop. The Executor does not plan ahead - it only handles the current step and moves on.

3. The Tools. These are the actions the Executor can take - search the web, query a database, run a calculator, send an email, read a file, and etc. Each tool has a name, a description, and an input schema.

4. The Memory. This is the running history of the agent - the original task, the plan, every step that has been executed, and every result. The Planner reads it when revising the plan. The Executor reads it to know what has already been done.

5. The Re-Planner. This is the LLM that decides what to do after each step is executed. It checks the result, compares it to the plan, and decides one of three things - keep going with the next step, update the plan if something has changed, or stop because the task is done. In some setups, the Re-Planner is the same LLM as the Planner, just called again with the latest state.

All five parts work together. The first four - Planner, Executor, Tools, and Memory - are the must-have parts. The Re-Planner is optional in the simplest setups, but most production agents include it to handle the cases where reality does not match the plan.

## How a Plan-and-Execute Agent Works

The flow is simple. The agent runs through three phases - Plan, Execute, and Re-Plan.

Phase 1: Plan. The user gives the agent a task. The Planner reads the task and writes a step-by-step plan. The plan is saved into memory.

Phase 2: Execute. The Executor picks the first step of the plan. The LLM recommends the right tool, the runtime calls it, reads the result, and saves the result into memory. Then it moves to the next step.

Phase 3: Re-Plan. After every step (or after a few steps), the Re-Planner reads the current state. If everything is on track, the Executor continues. If a step failed, returned an unexpected result, or made the rest of the plan invalid, the Re-Planner updates the plan. If the task is done, the agent stops and returns the final answer.

The loop continues until the plan is fully executed or the Re-Planner decides we have the final answer. Shaping that repeat - the step budget, the re-plan trigger, and the exit - is Loop Engineering.

In simple words:

Plan once. Execute step by step. Re-plan when reality does not match the plan.

## A Full Trace Example

Let's see this in action. Just for the sake of understanding, suppose the user gives the agent this task:

> "Find the current population of India and Japan, and tell me which country has more people and by how much."

Phase 1: Plan.

The Planner writes the plan:

```
1. Search for the current population of India.
2. Search for the current population of Japan.
3. Compare the two numbers.
4. Return the country with the larger population and the difference.

```

Phase 2: Execute.

Step 1. The Executor calls the search tool with the query `"current population of India"`. Suppose the tool returns `1.43 billion`. The result is saved into memory.

Step 2. The Executor calls the search tool with the query `"current population of Japan"`. Suppose the tool returns `124 million`. The result is saved into memory.

Step 3. The Executor calls the calculator tool with `1,430,000,000 - 124,000,000`. The tool returns `1,306,000,000`. The result is saved into memory.

Step 4. The Executor reads the memory and produces the final answer.

Phase 3: Re-Plan.

After each step, the Re-Planner checks the state. Everything is on track, so it does not change the plan. After Step 4, the Re-Planner sees that the task is done. The agent stops.

> "India has more people than Japan by about 1.31 billion. India has 1.43 billion people, and Japan has 124 million people."

Here, we can notice that the agent did not figure out the steps one at a time. It planned the whole journey first, then walked through it.

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

## Plan-and-Execute Agent vs ReAct Agent

A ReAct Agent and a Plan-and-Execute Agent are two different patterns to build an AI Agent. Both are common. The difference is about when the thinking happens.

A ReAct Agent thinks one step at a time. At every turn, it writes a Thought, picks an Action, reads the Observation, and thinks again. It does not plan ahead. It decides the next step only after seeing the latest result.

A Plan-and-Execute Agent thinks once at the start. It writes the whole plan up front, then runs each step. It re-plans only if something goes wrong.

Let's see this difference visually.

```
ReAct Agent - the LLM thinks at every step:

  +---------+   +--------+   +-------------+
  | Thought |-->| Action |-->| Observation |--+
  +---------+   +--------+   +-------------+  |
       ^                                      |
       +-- (loop until final answer) ---------+

Plan-and-Execute Agent - the LLM thinks once, then runs:

  +------+   +--------+   +--------+   +--------+
  | Plan |-->| Step 1 |-->| Step 2 |-->| Step 3 |--> Final Answer
  +------+   +--------+   +--------+   +--------+
                              ^
                              +-- (re-plan only if a step fails)

```

Here, we can see that the ReAct Agent loops back to the LLM on every step, while the Plan-and-Execute Agent calls the LLM once for planning and then runs each step in sequence. The ReAct Agent pays for thinking at every turn. The Plan-and-Execute Agent pays for thinking once up front.

Let me tabulate the differences between a ReAct Agent and a Plan-and-Execute Agent for your better understanding so that you can decide which one to use based on your use case.

| Property | ReAct Agent | Plan-and-Execute Agent |
| --- | --- | --- |
| When the LLM plans | One step at a time | Full plan up front, then re-plan only if needed |
| LLM calls per task | One LLM call per step | One big planning call + smaller calls per step |
| Cost | Higher when many steps are needed | Lower for tasks with many predictable steps |
| Latency | Slower for long tasks (many big calls) | Faster for long tasks (Executor calls can be smaller) |
| Adaptability | Very high - adapts at every turn | Lower - adapts only when re-planning |
| Best for | Open-ended tasks where the next step is unclear | Multi-step tasks with a clear path to the answer |
| Visibility | Reasoning is visible at every turn | The whole plan is visible up front |

In simple words:

Use ReAct when the next step depends on the last result. Use Plan-and-Execute when the steps can be planned ahead.

If we want to go deep into the ReAct pattern, agent architecture, orchestration and routing, and multi-agent systems, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Common Failure Modes and How to Fix Them

A Plan-and-Execute Agent is powerful, but it has its own set of mistakes that we must handle.

1. Bad Plan. The Planner writes a plan that is incomplete, in the wrong order, or skips important steps. The whole run goes off track from the start. To fix this, we must give the Planner a clear system prompt with examples of good plans, list the available tools, and ask it to write small, concrete steps instead of vague ones.

2. Step Drift. The Executor reads a step like "search the docs for the retry policy" and runs a public web search instead. The result is technically a search, but it does not fit what the Planner had in mind. To fix this, we must make each step in the plan specific - include the exact tool name, the exact input, and the expected output. The smaller and clearer the step, the less the Executor can drift.

3. No Re-Planning. A step fails or returns a surprise, but the agent keeps running the rest of the plan blindly. The final answer is wrong. To fix this, we must always run the Re-Planner after each step, or at least after any step that returns an error or an unexpected result. The Re-Planner reads the new state and decides whether the rest of the plan is still valid.

4. Over-Planning. The Planner writes a giant plan with 30 steps for a task that needs 3. Each extra step costs an LLM call and a tool call. To fix this, we must tell the Planner to write the smallest plan that solves the task and to merge steps that can be done together.

5. Plan Becomes Outdated. The plan was correct at the start, but after a few steps, the situation has changed - a search returned new information, a tool returned data in a different format, or a step revealed that an assumption was wrong. The rest of the plan no longer fits. To fix this, the Re-Planner must rewrite the remaining steps based on the latest state, not just continue with the original plan.

6. Infinite Re-Planning. The Re-Planner keeps rewriting the plan without making progress. The agent loops forever. To fix this, we must set a maximum number of re-plans, a maximum number of total steps, and a stop condition that triggers when the plan has not changed for two re-plans in a row.

Now, we have understood what a Plan-and-Execute Agent is and how to handle the common failure modes.

## Quick Summary

Let's recap what we have learned:

- Plan-and-Execute Agent is an AI Agent built using the Plan-and-Execute pattern - plan the whole task up front, then run the plan step by step.
- Plan-and-Execute Agent = Plan + Execute + Agent - the Planner writes the plan, the Executor runs each step, and the Agent loop connects them.
- Anatomy has five parts - the Planner, the Executor, the Tools, the Memory, and the Re-Planner.
- The flow has three phases - Plan once, Execute step by step, Re-Plan when reality does not match the plan.
- Plan-and-Execute vs ReAct - ReAct thinks one step at a time, Plan-and-Execute thinks once up front. Use ReAct for open-ended tasks. Use Plan-and-Execute for multi-step tasks with a clear path.
- Common failure modes are Bad Plan, Step Drift, No Re-Planning, Over-Planning, Plan Becomes Outdated, and Infinite Re-Planning - all of them can be handled with a clear system prompt, small steps, and a strict Re-Planner.
- Plan-and-Execute is one of the most common patterns to build AI Agents that need to handle long, multi-step tasks reliably.

### Do the Planner and the Executor use the same LLM?

Usually not. The Planner is a strong LLM that writes the full plan, while the LLM inside the Executor is usually smaller and cheaper, since each step is much narrower than the full task. In some setups, the Re-Planner is the same LLM as the Planner, just called again with the latest state.

### Is the Re-Planner required in a Plan-and-Execute Agent?

No. The Re-Planner is optional in the simplest setups. The Planner, Executor, Tools, and Memory are the must-have parts. Still, most production agents include a Re-Planner to handle the cases where reality does not match the plan.

### Can the Executor itself be an agent?

Yes. In some setups, the Executor is itself a small sub-agent, like a ReAct loop. Either way, the Executor does not plan ahead. It only handles the current step, saves the result into memory, and moves on to the next step.

### How do we stop a Plan-and-Execute Agent from re-planning forever?

We put hard limits on the loop. We set a maximum number of re-plans, a maximum number of total steps, and a stop condition that triggers when the plan has not changed for two re-plans in a row. This way, the agent cannot keep rewriting the plan without making progress.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# How does Function Calling work in LLMs?
URL: https://outcomeschool.com/blog/how-does-function-calling-work-in-llms
Published: 2026-06-13
Author: Amit Shekhar

How does Function Calling work in LLMs?

# How does Function Calling work in LLMs?

Authors
: - Name
: Amit Shekhar
Published on
: June 13, 2026

Function Calling is a way to let an LLM use external tools, APIs, and functions to get things done. The model does not run the function itself. It only tells our code which function to call and with which inputs.

In this blog, we will learn about how Function Calling works in LLMs. We will see what it is, why we need it, the key insight behind it, and how it powers AI agents and assistants step by step.

We will cover the following:

- What is Function Calling?
- Why We Need Function Calling
- The Key Insight: The Model Does Not Run the Function
- How Function Calling Works Step by Step
- A Concrete Example: get_weather(city)
- The Conversation Loop
- Multi-Step and Parallel Function Calling
- Relation to Structured Outputs and JSON Mode
- Real-World Use: The Backbone of AI Agents
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Function Calling?

Function Calling is a way to let an LLM use external tools, APIs, and functions to get things done. It is also called tool calling, and both names mean the same thing.

Before we go further, let's make sure we understand a few words.

An LLM (Large Language Model) is the model behind tools like ChatGPT. It reads text and generates text. That is the only thing it does on its own.

A function is a small block of code that does one job. For example, a function can fetch today's weather, send an email, or look up a price in a database.

[…451ln elided…]

All three pillars must be strong.

## Common Agent Roles

Now that we know the pillars, let's look at the agents themselves. Not every multi-agent system looks the same. Most reuse a small set of roles. Let's break each one down.

Orchestrator. The agent that runs the show. It receives the user request. It breaks the request into subtasks. It delegates them. It combines the results into a final answer. We also call it a manager or coordinator.

Worker. A specialist agent that does one kind of task well. Workers include researchers, writers, coders, data analysts, and anything else that maps to a real-world specialization. The more focused the role, the more reliable the agent. A focused worker like this is also called a SubAgent - a smaller, specialized agent that runs under a main agent.

Router. An agent whose only job is to look at a request and decide which worker should handle it. We use it when the system has many workers and the right one depends on the input. It keeps each worker's system prompt small and focused.

Planner. An agent that produces a step-by-step plan for a complex task. The workers then execute the plan. Separating planning from execution makes both steps more reliable - this is the idea behind the Plan-and-Execute Agent pattern.

Critic or Reviewer. An agent that checks another agent's output for quality, safety, or correctness. It sends the output back for revisions if needed. It is great for reducing hallucinations and errors. The condition is that the critic must have independent grounding (sources, tools), not just the same context as the writer. This role is a close cousin of LLM as a Judge - one LLM evaluating another LLM's output against explicit criteria, wired here as an in-loop reviewer instead of an external scorer.

Tool Specialist. An agent that owns the prompting strategy and schema knowledge for a specific tool or data source. The calling agent does not have to know these details. For example, a "database agent" that knows the schema deeply and writes good SQL. Or a "web search agent" that knows how to phrase strong queries.

Let's see how these roles work together with a concrete example. Suppose we want a system that handles customer support emails. We can split the work across four agents:

- The Orchestrator receives a customer email like "I want a refund for my last order, it arrived damaged".
- It hands off the lookup to a Researcher Worker that pulls the order details, the return policy, and the customer's account history.
- It hands the gathered notes to a Writer Worker that drafts a personalized reply.
- It hands the draft to a Critic that checks for tone, accuracy, and policy compliance, and sends it back for revisions if needed.
- Once the Critic approves, the Orchestrator sends the final reply to the customer.

Four agents, each with one job. The Researcher does not know about writing replies. The Writer does not know about looking up customer data. The Critic does not know about drafting from scratch.

Each agent has a small, focused system prompt. The tool set is tight. This is exactly what makes the system more reliable. A single agent trying to juggle all four jobs would be less reliable.

Here is what the wiring looks like end to end:

```
Customer Email
    |
    v
Orchestrator
    |
    v
Researcher --> notes
    |
    v
Writer --> draft
    |
    v
Critic --> approve or revise
    |
    v
Final Reply

```

The Orchestrator runs the workers in sequence here. Each step needs the previous one's output.

And, the actual messages flowing between the Orchestrator and each worker look like this. Let's go through each round.

Round 1: Orchestrator asks the Researcher to gather information.

The Orchestrator sends:

```json
{
  "task": "look up order details, return policy, and customer history",
  "order_id": "4521"
}

```

The Researcher does the lookup and sends back:

```json
{
  "notes": {
    "order": {
      "id": "4521",
      "item": "blue running shoes",
      "status": "delivered",
      "delivered_on": "2026-04-10"
    },
    "policy": "Damaged items can be returned within 30 days for a full refund.",
    "customer": {
      "name": "Alex",
      "tier": "regular",
      "past_returns": 1
    }
  }
}

```

Here, the Researcher returns the order details, the return policy, and the customer history. The Writer will use these notes in the next round.

Round 2: Orchestrator asks the Writer to draft a reply.

The Orchestrator forwards the notes and adds a few hints:

```json
{
  "notes": { "...": "the notes from Round 1" },
  "customer_name": "Alex",
  "tone": "warm and clear"
}

```

The Writer drafts the reply:

```json
{
  "draft": "Hi Alex, I am sorry to hear your blue running shoes arrived damaged..."
}

```

Here, the Writer turns the raw notes into a personalized reply. The "tone" hint tells the Writer how to sound. The Critic will check the draft next.

Round 3: Orchestrator asks the Critic to review the draft.

The Orchestrator sends the draft and the things to check:

```json
{
  "draft": "Hi Alex, I am sorry to hear your blue running shoes arrived damaged...",
  "check_for": ["tone", "accuracy", "policy compliance"]
}

```

The Critic returns its verdict:

```json
{
  "verdict": "needs revision",
  "issues": ["The reply does not mention the 30-day return window."]
}

```

Here, the Critic flags one issue. The Orchestrator hands the draft back to the Writer with the feedback. The loop continues until the Critic approves.

Each message is a structured object with named fields. It is not unstructured chat. That is what keeps the agents on the rails.

Note: Not every system needs all of these. A simple multi-agent system can have just an orchestrator and two workers. A complex one can have a planner, a router, five workers, and a critic. We start small. We add roles only when a real gap shows up.

To master Multi-Agent Systems, subagents, agent architecture, and orchestration, check out our AI and Machine Learning Program at Outcome School.

## How Agents Communicate

With the roles clear, the next question is how they actually talk to each other. Agents need to share information to work together. There are three main ways they do it. Let's understand each one.

```
Message Passing:    A <--msg--> B    (point-to-point between any agent pair)

Shared State:        A     B     C
                      \    |    /
                       v   v   v
                    +-------------+
                    |  Blackboard |   (all agents read and write)
                    +-------------+

Handoffs:           A --(work + context)--> B --(work + context)--> C

```

1. Message passing. One agent sends a structured message to another. The message contains the task, the context, and any inputs needed. This is direct and clear. It can get noisy when many agents are involved. It works well for small systems with a few well-defined agents.

2. Shared state or blackboard. All agents read from and write to a shared memory. Each agent picks up what is relevant to it. It does its work. It writes the result back. This is flexible. It needs careful rules to avoid chaos.

3. Handoffs. A handoff is a message that also transfers control. One agent finishes its part. It passes both the work and the context to the next agent. It then steps out of the loop. This is like a relay race - clean, predictable, and easy to reason about. Only one agent is "active" at a time.

In simple words:

Handoff = Message + Control transfer.

Note: These three modes overlap. A handoff is mechanically a special case of message passing - a message that also transfers control. Real systems mix all three. We use handoffs for the main flow. We use message passing for side queries. We use shared state for context everyone needs.

Very important: If we want this to work reliably, communication between agents must be structured. If agents just chat in unstructured text, misunderstandings multiply quickly. We define clear message formats. We define expected fields. We define what each agent is responsible for.

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

One more thing to notice. Agents can share memory fully. They can share it partially via summaries. They can share nothing at all. Each choice trades context richness for token cost.

Now that we know how agents talk, the next question is who runs when.

## How Agents Coordinate

Coordination is how the system decides who runs when. There are five common patterns. Let's go through each one.

```
Sequential:    A -> B -> C -> D

Parallel:      Request
                 |
             +---+---+
             |   |   |
             A   B   C
             |   |   |
             +---+---+
                 |
              Merge -> Response

Router:        Request -> Router -> (A or B or C)

Hierarchical:       Orchestrator
                    /     |     \
                   A      B      C

Graph:          A <--> B
                ^      ^
                v      v
                C <--> D
                (any agent can call any other)

```

Sequential. Agents run one after another. Each agent builds on the previous one's output. Simple. Easy to debug. Slow if the steps could run in parallel.

Parallel. We have multiple agents working at the same time on independent subtasks. We merge their results at the end. Fast - but only when the subtasks are truly independent.

Router. A router agent picks which worker handles each request. Good when requests fall into a few distinct categories.

Hierarchical. An orchestrator delegates to workers. The workers can themselves delegate to sub-workers. Great for complex, nested tasks. Looks very much like how a real company org chart works.

Graph or Network. Any agent can call any other based on the task at hand. Useful when the task is exploratory and the right next agent depends on intermediate findings. Maximum flexibility - but harder to debug and reason about. We see this pattern in modern multi-agent frameworks, and Graph Engineering is the practice of designing such a graph well.

These patterns range from fixed workflows on one end (Sequential, Parallel) to fully dynamic agent-driven control on the other (Graph). Most systems sit somewhere in the middle.

In simple words, coordination is the wiring diagram and communication is the signal that travels across the wires - both must work for the system to actually run.

If we want to go deep into orchestration, routing, and the full multi-agent architecture, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Multi-Agent vs Single Agent - The Trade-offs

Now, the natural question is - when is all this complexity worth it? Let me tabulate the differences between a Multi-Agent System and a Single Agent for your better understanding so that you can decide which one to use based on your use case.

| Property | Single Agent | Multi-Agent System |
| --- | --- | --- |
| Complexity | Low | High |
| System prompt | One, can get long | Many, each focused |
| Tool count per agent | All tools on one | Split across agents |
| Parallelism | Limited (parallel tool calls within one turn) | Natural for independent agent work |
| Debugging | Easier (one loop) | Harder (many loops, handoffs) |
| Latency | Lower for simple tasks | Higher with handoffs, lower with parallelism |
| Cost | Lower | Higher |
| Quality on complex tasks | Can degrade as tools grow | Scales better with specialization |
| Failure modes | Fails as a unit | Partial failure or cascading errors |
| Best for | Short, focused tasks | Complex, multi-skill tasks |

In simple words, multi-agent systems are more powerful for complex work. They come with a real cost in complexity, latency, and tokens. If we add agents without a real reason, we just pay more for nothing.

In most cases, we land in a hybrid spot - a single primary agent with one or two helpers like a router or a critic. Pure multi-agent setups, with many peer agents and no clear primary, are rarer than they sound. Most of the time, they are overkill until the workload genuinely needs them.

Splitting the tools across agents buys us something on the security side as well. The agent that reads untrusted text does not have to be the agent that holds the dangerous tools. We have a detailed blog on Prompt Injection in LLMs that explains this separation in depth.

## Common Mistakes

With all this power comes specific ways to fail. Let's go through each.

1. Agents talking too much. Agents keep sending messages back and forth without making progress. Token cost explodes.

How to fix: We set a cap on total turns. We make handoffs explicit. We avoid unstructured back-and-forth between agents unless it is the goal.

2. Unclear ownership. Two agents think the other is handling a task. Or both try to handle it. The result is duplicate or missing work.

How to fix: We give each agent a clearly scoped role in its system prompt. The orchestrator is the only one routing work.

3. Error propagation. A small mistake by one agent gets amplified by the next. By the final agent, the output is wrong in ways that are hard to trace.

Example: A research agent returns slightly wrong data about a topic. The writer agent builds a confident draft on top of it. The critic agent only checks grammar and style. The final output looks polished but is factually wrong - and it is hard to tell which agent introduced the error.

How to fix: We add critic or review agents at key points. We validate intermediate outputs, not just the final one.

4. Coordination overhead dominates. The agents spend more tokens coordinating than actually doing the work.

How to fix: We use the simplest coordination pattern that fits. We prefer fixed workflows and handoffs over unstructured discussion.

5. Non-determinism. The same input produces different results every run because agents make slightly different choices.

How to fix: We lower the temperature for coordination-level decisions. This reduces but does not eliminate non-determinism. Some variance comes from floating-point and provider-side effects even at temperature zero. We make the workflow structure fixed. We let only the worker outputs vary.

6. Hidden complexity. It feels like we are making the system smarter by adding agents. But really we are making it harder to reason about.

How to fix: Every new agent must have a clear reason to be there. If a single agent could do the job well, we add no agents. If not, we add the minimum number. Complexity is something we pay for. We must add it only when we need it.

7. Critic loops that never converge. A critic that is too strict or too vague keeps rejecting drafts. It sends the writer back forever. Tokens burn. Latency grows. Sometimes the original draft was already good enough.

How to fix: We cap the number of revision rounds. We make the critic's accept and reject criteria explicit and bounded. If two rounds in a row return similar feedback, we accept and ship.

The happy path is easy - the edge cases are where the real work happens. Handling these failure modes well is what makes a multi-agent system actually work.

We will also need tracing, retries, and token budgets. The wiring alone is not enough.

Now, let's see when all this complexity actually pays off.

To learn evaluation of agents, LLM as a Judge, and production-grade multi-agent systems, check out our AI and Machine Learning Program at Outcome School.

## When to Use a Multi-Agent System

Use a Multi-Agent System when:

- The task naturally splits into specialized roles (research + writing + review).
- Different parts of the task need very different system prompts or models (e.g., a fast small model for routing, a large model for writing).
- Parallelism can give a real speedup because subtasks are independent.
- A single agent's system prompt has grown too long or tool count too high.
- Quality matters enough that a dedicated critic or reviewer makes sense.

Do not use a Multi-Agent System when:

- A single agent already does the job well.
- The task is tightly coupled and does not split cleanly across agents (e.g., coding, where each step depends on shared context).
- The coordination overhead would cost more than the speedup.
- The team does not have the time or tooling to debug multi-agent failures.
- Simplicity and predictability matter more than raw capability.

The rule of thumb is simple. We start with a single agent. We move to multi-agent only when the single agent clearly cannot handle the task well. When we do move, we add the smallest number of agents that solves the problem. Every extra agent is extra complexity. We pay for it in tokens, latency, and debugging time.

Frameworks like LangGraph and AutoGen handle much of the wiring. We do not have to build the orchestration layer from scratch.

Now, we have understood what a Multi-Agent System is, the three pillars it rests on, and when to build one. Let's wrap up with a quick recap.

## Quick Summary

Let's recap what we have learned:

- A Multi-Agent System is a group of LLM-driven agents, each with its own role, that work together on a shared task. It is not just many agents - it is many agents plus the glue that lets them cooperate.
- The three pillars are Specialization, Communication, and Coordination. Remove any one, and the system breaks.
- Common agent roles include the Orchestrator, Worker, Router, Planner, Critic, and Tool Specialist. Most systems reuse a small mix of these.
- Agents communicate via message passing, shared state, or handoffs. The communication must be structured - unstructured chat between agents leads to chaos.
- Agents coordinate via sequential, parallel, router, hierarchical, or graph patterns. Coordination is the wiring. Communication is the signal.
- The trade-off is real - multi-agent systems are more powerful for complex tasks, but cost more in latency, tokens, and debugging effort. We must add complexity only when we need it.
- Common mistakes include too much chatter, error propagation across agents, runaway critic loops, and hidden complexity. Handling these is the real work.
- Start with a single agent. We move to multi-agent only when the single agent cannot do the job. When we do, we add the smallest number of agents that solves the problem. Every agent we add must have a clear reason to be there.

### Is a multi-agent system always better than a single agent?

No. Multi-agent systems are more powerful for complex, multi-skill tasks, but they cost more in complexity, latency, tokens, and debugging time. For short, focused tasks, a single agent is often the better choice. We start with a single agent and move to multi-agent only when it clearly cannot handle the task well.

### Is a group of agents that do not talk to each other a multi-agent system?

No. A bunch of agents that do not talk to each other is just a bunch of agents. The system part is what makes it multi-agent, which is the coordination layer and the communication that lets the agents collaborate on a shared task.

### Should we use a multi-agent system for coding tasks?

Usually not. A multi-agent system fits poorly when the task is tightly coupled and does not split cleanly across agents. Coding is a good example, since each step depends on shared context. In such cases, the coordination overhead can cost more than the benefit.

### Does setting the temperature to zero make a multi-agent system deterministic?

No. Lowering the temperature for coordination-level decisions reduces non-determinism, but it does not eliminate it. Some variance comes from floating-point and provider-side effects even at temperature zero. So, we also keep the workflow structure fixed and let only the worker outputs vary.

### Do we have to build the orchestration layer ourselves?

No. Frameworks like LangGraph and AutoGen handle much of the wiring for us. We do not have to build the orchestration layer from scratch, but we will still need tracing, retries, and token budgets.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-334 and 786-1161 of 1161; 451 middle lines (24.7KB) elided. Read artifact://80 for full output]
