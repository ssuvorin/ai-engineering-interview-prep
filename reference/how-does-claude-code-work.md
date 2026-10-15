> Source: https://outcomeschool.com/blog/how-does-claude-code-work

# How does Claude Code work?
URL: https://outcomeschool.com/blog/how-does-claude-code-work
Published: 2026-07-20
Author: Amit Shekhar

How does Claude Code work?

# How does Claude Code work?

Authors
: - Name
: Amit Shekhar
Published on
: July 20, 2026

Claude Code is a coding agent from Anthropic that runs in the terminal. We give it a task in plain English, and it completes the task by reading our code, editing files, running commands, and checking its own work.

In this blog, we will learn about how Claude Code works. We will also see what Claude Code is, why a normal AI chatbot is not enough, how the agent loop drives it, what tools give it its eyes and hands, how it searches a big project and verifies its own work, and how CLAUDE.md, permissions, plan mode, subagents, and hooks fit together.

We will cover the following:

- What is Claude Code?
- The problem with a normal AI chatbot
- The agent loop
- The tools of Claude Code
- Example: Claude Code fixing a bug
- How does Claude Code search a big project?
- How does Claude Code verify its own work?
- CLAUDE.md: The project memory
- Permissions: How we stay in control
- Plan mode, subagents, and hooks
- Putting it all together

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Claude Code?

Claude Code is a coding agent from Anthropic that runs in the terminal. We give it a task in plain English, and it completes the task by reading our code, editing files, running commands, and checking its own work.

Before we go further, we must understand two words used above: terminal and agent.

The terminal is the text window on our computer where we type commands. There are no buttons and no icons. We type a command, press enter, and the computer does the work and shows the result as text.

An agent is a program that does not just answer our question, it takes actions on its own to complete a goal.

In simple words, Claude Code is like a developer sitting inside our computer. We tell it what we want in normal English, and it does the actual work: it opens files, reads code, makes changes, runs the code, and confirms that everything works.

Let's say we hire a new developer for our team. On day one, we tell the developer: "There is a bug in the login page, please fix it." The developer does not ask us to copy and paste every file for them. They open the project, search for the login code, read it, fix it, run the tests, and tell us it is done. Claude Code works exactly like this developer.

At the center of Claude Code is Claude, an AI model created by Anthropic, trained on a huge amount of text and code, so it can read and write both. But a model alone can only talk. To understand why that is a problem, let's look at how we use a normal AI chatbot.

## The problem with a normal AI chatbot

Suppose we have a bug in our project and we ask a normal AI chatbot for help.

First, we copy the code from our project and paste it into the chat. Then, the chatbot replies with the fixed code. After that, we copy the fixed code back into our project. Finally, we run the tests ourselves to see if the fix works.

If the fix does not work, we copy the error, paste it into the chat, and repeat the whole cycle again.

Here, the chatbot has three big limitations:

- It cannot see our project. A real project has hundreds or thousands of files, and the chatbot only sees the small piece we paste.
- It cannot do anything. It can only produce text. We have to make every change with our own hands.
- It cannot verify its answer. It never knows if the code it suggested actually works.

We are working as a messenger between the chatbot and our computer. This is slow and painful.

The whole situation looks like below:

```
+--------------+   copy and paste   +--------+   copy and paste   +--------------+
|  AI chatbot  | <----------------> |   We   | <----------------> | Our computer |
|  only talks  |                    |        |                    |  runs code   |
+--------------+                    +--------+                    +--------------+

```

Here, we can see that we are sitting in the middle. The chatbot cannot reach our computer, and our computer cannot reach the chatbot. Everything passes through our hands, one copy and paste at a time.

So, here comes Claude Code to the rescue.

Claude Code gives the AI model the two things it never had: eyes and hands. The eyes and hands are called tools. The model is the brain that decides what to do, and the tools are what actually do it. Do not worry, we will learn about each tool in detail.

## The agent loop

The heart of Claude Code is the agent loop.

When we give Claude Code a task, it works through three phases: gather context, take action, and verify results. And, it repeats these phases again and again until the task is complete.

The agent loop looks like below:

```
              +------------------+
              |   Your request   |
              +------------------+
                       |
                       v
              +------------------+
    +-------->|  Gather context  |
    |         +------------------+
    |                  |
    |                  v
    |         +------------------+
    |         |   Take action    |
    |         +------------------+
    |                  |
    |                  v
    |         +------------------+
    |         |  Verify results  |
    |         +------------------+
    |                  |
    +---- not done ----+
                       | done
                       v
              +------------------+
              |  Task complete   |
              +------------------+

```

Here, we can see the three phases of the loop:

- Gather context: Claude Code searches and reads the files of our project to understand the code before touching it.
- Take action: It edits files, creates new files, and runs commands to make the change.
- Verify results: It runs the tests or the program to check if the change actually works.

If the verification fails, it does not stop. It goes back, reads the error, and tries again. The loop continues until the work is done. Shaping that loop deliberately - the step budget, the error message fed back, and the exit conditions - is Loop Engineering.

One more thing to notice: we are part of this loop too. We can interrupt Claude Code at any point, correct it, or give it more information. It works on its own, but it always listens to us.

If we want to go deep into how agents like this work under the hood - the agent loop, Agent Architecture, and the ReAct Pattern - we build an AI Coding Agent from scratch in our AI and Machine Learning Program at Outcome School.

Now that we have understood the loop, it's time to learn about the tools that power each phase.

## The tools of Claude Code

A tool is one small ability that Claude Code gives to the model. The model cannot touch our computer directly. It can only request a tool, the tool does the work, and the result goes back to the model. Then, the model decides the next step based on that result. This request-and-respond mechanism, where the model asks for a tool and the result comes back, is called function calling. We have a detailed blog on how Function Calling works in LLMs that explains it in depth.

Claude Code has many tools, but six of them do most of the work. Let me tabulate them with a real-world comparison for your better understanding:

| Tool | What it does | Like a developer... |
| --- | --- | --- |
| `Read` | Reads a file and returns its content | Opening a file to read the code |
| `Grep` | Searches for a word or pattern inside all files | Using "Find in all files" in an editor |
| `Glob` | Finds files whose names match a pattern | Looking for a file by its name |
| `Edit` | Changes a specific part of a file | Editing a few lines of code |
| `Write` | Creates a new file or replaces a file | Creating a new file in the project |
| `Bash` | Runs any terminal command | Running the tests, building the app |

Here, `Grep` and `Glob` can look strange, so let me explain them in simple words.

`Grep` is a text search. If we ask it to search for the word `loginUser`, it looks inside every file of the project and tells us which files contain that word and on which lines. It is like pressing Ctrl+F, but for the entire project at once.

`Glob` is a filename search. A pattern like `*.js` means "all files whose names end with .js". So, `Glob` answers questions like "which test files exist in this project?" without opening a single file.

And, `Bash` is the most powerful tool. It can run any command we could type in the terminal ourselves: running tests, installing packages, using git, starting a server, and etc. This one tool is what lets Claude Code verify its own work.

The best way to learn how these tools work together is by taking an example.

## Example: Claude Code fixing a bug

Let's say one test in our project is failing. We open the terminal in our project folder and type as below:

```
claude
> Fix the failing login test

```

Here, the first line starts Claude Code, and the second line is our request in plain English. Notice that we did not tell it which file has the bug. We do not even know that ourselves.

Now, let's watch what Claude Code does, step by step.

Step 1: It uses `Bash` to run the test command of the project, for example `npm test`. The output says one test failed: "loginUser should return a token".

Step 2: It uses `Grep` to search for `loginUser` across the project. The search finds the function inside a file called `auth.js`.

Step 3: It uses `Read` to open `auth.js`. Now, the model can see the actual code and understand the bug. Let say the code forgets to return a value in one case.

Step 4: It uses `Edit` to fix those lines in `auth.js`.

Step 5: It uses `Bash` to run `npm test` again. All tests pass.

The whole journey looks like below:

```
Our request: "Fix the failing login test"
                          |
                          v
+---------------------------------------------------+
| Bash: run the tests      --> one test failed      |
| Grep: search "loginUser" --> found in auth.js     |
| Read: auth.js            --> understands the code |
| Edit: auth.js            --> fixes the bug        |
| Bash: run the tests      --> all tests passed     |
+---------------------------------------------------+
                          |
                          v
                    Task complete

```

Here, we can see that every tool result feeds the next decision. The failing test told it what to search. The search told it what to read. The reading told it what to edit. And, the final test run proved that the fix works.

It works perfectly.

This is the agent loop in action: gather context with `Bash`, `Grep`, and `Read`, take action with `Edit`, and verify results with `Bash` again.

To learn how a model turns plain English into real actions like these - Tool use in Agents and Agent Architecture - we cover it in our AI and Machine Learning Program at Outcome School.

## How does Claude Code search a big project?

Now, the question is: why does Claude Code search first instead of reading everything?

The answer is the context window. The context window is the working memory of the AI model. It can hold only a limited amount of text at a time. Everything the model knows about our conversation, our files, and our commands must fit inside it.

Suppose the context window is a whiteboard of a fixed size. Every file we read gets written on the whiteboard. When the whiteboard is full, old things must be erased to make room for new things.

A real project can have thousands of files. If Claude Code tried to read all of them, the whiteboard would overflow immediately. So, it does what a smart developer does: it searches first and reads only what matters.

Deciding what goes on this whiteboard and what stays off it is called context engineering. We have a detailed blog on Context Engineering that covers this end to end.

This is why `Grep` and `Glob` come into the picture. They are simple, fast text searches. They scan thousands of files in a moment and return only a small list of matching files and lines. That small list takes very less space on the whiteboard. Then, Claude Code reads only the two or three files that actually matter.

The search works like a funnel, like below:

```
+-----------------------------+
| Thousands of files          |
+-----------------------------+
               |
               |  Grep and Glob search them
               v
+-----------------------------+
| A few matching files        |
+-----------------------------+
               |
               |  Read opens only these
               v
+-----------------------------+
| Only the code that matters  |
| is on the whiteboard        |
+-----------------------------+

```

Here, we can see that the project gets narrowed down at every step. Thousands of files become a few files, and a few files become a small amount of code on the whiteboard. The whiteboard never overflows.

There is no magic database and no special index of our code. Claude Code finds its way through a project using the same simple text searches that developers have used for decades. The intelligence is not in the search tool. The intelligence is in the model deciding what to search for.

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

## How does Claude Code verify its own work?

I personally believe that this is the most important part of Claude Code.

The biggest weakness of a normal AI chatbot is that it cannot check its own answer. It writes code that looks correct, and looking correct is not the same as being correct.

Claude Code closes this gap by running the code. After making a change, it can:

- Run the tests of the project and read the results.
- Run the compiler or build and read the errors.
- Run the program itself and check the output.

If anything fails, the error message goes right back into the loop. The model reads the error, understands what went wrong, and fixes it. This can repeat many times without us doing anything.

This pattern, where an agent inspects its own output and corrects itself, is called reflection. We have a detailed blog on the Reflection Agent that explains this step by step.

The verification loop looks like below:

```
        +-------------------+
        |   Make a change   |
        +-------------------+
                  |
                  v
        +-------------------+
+------>|   Run the tests   |
|       +-------------------+
|                 |
|       +---------+---------+
|       |                   |
|     failed              passed
|       |                   |
|       v                   v
| read the error       work is done
| and fix the code
|       |
+-------+

```

Here, we can see that a failed test does not end the work. The error goes back into the loop, the code gets fixed, and the tests run again. The loop only ends when the tests pass.

This is exactly how a good developer works. We never say "the bug is fixed" without running the code. Claude Code follows the same discipline.

And, we can help it here. If we give Claude Code something to verify against, it performs much better. For example, we can say: "Write a failing test first, then fix the code, then run the tests." Now, it has a clear target, and it will keep looping until the target is hit.

## CLAUDE.md: The project memory

Every new Claude Code session starts with a fresh, empty context window. Remember the whiteboard? Each session begins with a clean whiteboard.

But, here is the catch. Our project has rules that never change: which language we use, how to run the tests, which folders must not be touched. Explaining these rules again in every session would be painful.

So, here comes CLAUDE.md into the picture.

CLAUDE.md is a simple text file that we keep in our project folder. Claude Code reads it automatically at the start of every session. Whatever we write in this file becomes standing instructions for Claude Code.

A small CLAUDE.md can look like below:

```markdown
# Project Notes

- We use Kotlin for all new code.
- Run the tests with: ./gradlew test
- Do not edit files inside the generated/ folder.

```

Here, we have written the language of the project, the exact test command, and one folder that must never be touched. Now, Claude Code knows all of this in every session without us repeating it.

Suppose a new developer joins our team and we hand them a one-page note: "Here is how our team works." CLAUDE.md is exactly that note, written for Claude Code. When one of those rules grows into a full procedure with its own steps and files, we keep it out of this always-loaded note and write it as an Agent Skill instead, which Claude Code loads only when a task actually needs it.

To master how agents remember and manage what they know - Memory in Agents and Context Engineering - we have our AI and Machine Learning Program at Outcome School that covers this from the ground up.

## Permissions: How we stay in control

Now, the next big question is: an agent that can edit files and run commands is powerful, so how do we stay safe?

The answer is permissions. By default, Claude Code asks for our approval before it edits a file or runs a command that changes something. We see a prompt like below:

```
Claude wants to run: npm test
Do you want to allow this?
> 1. Yes
  2. Yes, and do not ask again for this command
  3. No, and tell Claude what to do differently

```

Here, this is a simplified version of the prompt, just for the sake of understanding. Nothing changes on our computer until we say yes. And, if we trust a command like `npm test`, we can allow it permanently so Claude Code never asks for it again.

Claude Code also has different permission modes that we can switch between:

- Manual: Claude Code asks before every file edit and every command. This is the default.
- Accept edits: File edits are approved automatically, but other commands still need our approval. We use this when we already trust the direction of the work.
- Plan: Claude Code can only read and think. It cannot edit anything. We will learn about this mode in the next section.
- Auto: Claude Code works without asking, with safety checks running in the background. This is meant for automated setups where no human is sitting at the keyboard.

One more safety net exists: checkpoints. Before Claude Code edits any file, it saves a snapshot of that file. If we do not like the result, we can rewind everything back to how it was. Every file edit is reversible.

## Plan mode, subagents, and hooks

Till now, we have learned the core of Claude Code. Now, let's learn three features that make it even more useful.

### Plan mode

In plan mode, Claude Code is read-only. It explores the project, thinks, and then presents a plan: "Here is what I will change and why." It does not touch a single file.

We read the plan, correct it through conversation, and only then allow the implementation. It is like agreeing on the blueprint of a house before any construction starts. For big changes, this two-phase approach gives much better results than jumping straight to code.

### Subagents

Remember the whiteboard problem? Long tasks fill the context window quickly. A big exploration alone can fill the entire whiteboard.

So, here comes the subagent to the rescue.

A subagent is a helper agent with its own fresh context window, which means its own separate whiteboard. The main agent gives it one focused task, the subagent does all the messy exploration on its own whiteboard, and then it returns only a short summary.

```
               +--------------------+
               |     Main agent     |
[…848ln elided…]

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

[Showing lines 1-393 and 1242-1617 of 1617; 848 middle lines (48.6KB) elided. Read artifact://48 for full output]
