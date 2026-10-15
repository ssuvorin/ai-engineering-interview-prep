> Source: https://outcomeschool.com/blog/how-ai-agents-communicate

# How AI Agents Communicate
URL: https://outcomeschool.com/blog/how-ai-agents-communicate
Published: 2026-05-26
Author: Amit Shekhar

How AI Agents Communicate

# How AI Agents Communicate

Authors
: - Name
: Amit Shekhar
Published on
: May 26, 2026

AI agents communicate by sending messages to each other to share information, ask for help, and work together to finish a task. They can talk directly, through a central coordinator, by broadcasting, or through shared memory.

In this blog, we will learn about how AI agents communicate. We will understand why agents need to communicate, the main ways they talk to each other, the message format, and the protocols that make agents work together to finish complex tasks.

We will cover the following:

- What is agent communication?
- Why do agents need to communicate?
- What agents need in order to communicate
- How a message flows between agents
- The ways AI agents communicate
- Direct Communication
- Centralized Communication
- Broadcast Communication
- Shared Memory Communication
- What a message looks like
- The rules agents follow to talk
- Challenges when agents communicate
- Best Practices

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is agent communication?

Agent communication is the way two or more AI agents send messages to each other to share information, ask for help, and work together to finish a task.

Before we go further, let's quickly recall what an AI agent is. An AI agent is a system that uses an LLM to think, plan, and take actions to complete a task on our behalf. Now, when we have many such agents, they must talk to each other, and that talking is what we call agent communication.

In simple words, one agent alone can do only so much. A real task often needs many agents, where each agent is good at one thing. One agent searches for information. Another agent writes the answer. Another agent checks the answer. For all of them to work together, they must share their progress and pass results to each other.

Let's say we are building a travel planner. One agent finds the flights. One agent finds the hotels. One agent finds the local activities. A main agent collects all of this and builds the final trip plan. None of this works if the agents cannot pass information to each other. So, here comes agent communication to the rescue.

Think of it like a team in an office. One person handles design, one handles code, one handles testing. They talk to each other through messages, emails, and meetings. Without this communication, the team cannot ship a product. In the same way, AI agents need a clean way to communicate to finish a task together.

## Why do agents need to communicate?

A single agent can handle a simple task. But, real tasks are big and have many parts. We break a big task into smaller parts and give each part to a specialized agent. Now, these agents must share their work. This is why agents need to communicate.

Here are the main reasons agents need to communicate:

- To let each agent focus on one job and become good at it.
- To pass the output of one agent as the input of another agent.
- To let agents ask each other for help when they get stuck.
- To split a big task into smaller tasks that run across many agents.
- To let agents work in parallel and finish faster.
- To let agents check and correct each other's work.
- To build large systems where many agents act like a team.

Without communication, every agent works alone in its own box. With communication, agents become a team that can solve much bigger problems together.

We have a detailed blog on Multi-Agent Systems that explains how these agents are organized into a working team.

## What agents need in order to communicate

Before we learn how agents communicate, we must know the main parts that make it possible.

- Sender - The agent that creates and sends the message.
- Receiver - The agent that gets the message and acts on it.
- Message - The actual information that is being shared, like a question, a result, or an instruction.
- Protocol - The agreed set of rules that decides the format of the message and how it is sent. Both agents must follow the same protocol.
- Channel - The path through which the message travels, like a network call, a queue, or a shared memory.
- Shared Context - The common memory or state that agents can read from and write to.

These are the building blocks. Agents put these pieces together so that messages flow cleanly from one agent to another.

## How a message flows between agents

Now, let's see how a message actually flows from one agent to another, step by step. The steps are:

- Step 1: Agent A finishes its part of the task and prepares a message.
- Step 2: Agent A formats the message based on the agreed protocol.
- Step 3: Agent A sends the message to Agent B through the channel.
- Step 4: Agent B receives the message and reads it.
- Step 5: Agent B does its work using the information in the message.
- Step 6: Agent B sends a reply or passes a new message to the next agent.
- Step 7: This continues until the full task is finished.

We can picture this flow like below:

```text
   request:   Agent A  ──▶  Channel  ──▶  Agent B
   reply:     Agent A  ◀──  Channel  ◀──  Agent B

```

Here, we can see that Agent A formats the message and sends it through the channel to Agent B, and Agent B's reply travels back through the same channel. At every step, an agent can also store the message in shared memory, log it, and check it for safety. This back-and-forth flow of messages is the heart of how agents communicate.

Now, it's time to learn the main ways agents communicate.

## The ways AI agents communicate

There are four main ways AI agents communicate. We use these patterns again and again, and we will learn about each one in detail.

- Direct Communication - One agent talks straight to another agent.
- Centralized Communication - A main agent sits in the middle and routes all messages.
- Broadcast Communication - One agent sends a message to many agents at once.
- Shared Memory Communication - Agents talk through a common memory instead of direct messages.

In real projects, we mix many of these patterns inside the same system. Now, let's discuss each one.

## Direct Communication

Direct Communication means one agent sends a message straight to another agent, without anyone in the middle.

The best way to learn this is by taking an example. Let's say we have a research agent and a writing agent. The research agent finds the facts and sends them straight to the writing agent. The writing agent uses these facts to write the article, and if it needs more facts, it sends a request straight back to the research agent.

We can picture it like below:

```text
Research Agent  ◀───────▶  Writing Agent

```

Here, the two agents talk to each other directly, in both directions. There is no manager in the middle. This is the simplest way agents can communicate.

Advantage:

- Simple to set up and understand.
- Fast, because there is no extra layer in the middle.

Disadvantage:

- Hard to manage when there are many agents, because every agent must know how to reach every other agent.
- If we add a new agent, we must connect it to all the others by hand.

This was all about Direct Communication. Now, let's learn about Centralized Communication.

## Centralized Communication

Centralized Communication means a main agent sits in the middle, and all other agents talk to this main agent instead of talking to each other directly.

The main agent is often called the orchestrator or the manager. It receives messages, decides which agent must act next, and routes the message to the right agent.

Let's say we are building a customer support system. The main agent reads the user's question. If it is a billing question, the main agent sends it to the billing agent. If it is a technical question, the main agent sends it to the technical agent. The billing agent and the technical agent never talk to each other. They only talk to the main agent.

We can picture it like below:

```text
              ┌──────────────┐
   User ◀──▶  │  Main Agent  │
              └──────────────┘
              ▲          ▲
              │          │
              ▼          ▼
          Billing    Technical
           Agent       Agent

```

Here, the main agent is the brain that controls the flow of all messages. Notice that every arrow points both ways, because each agent receives work from the main agent and sends its result back to it.

- Easy to manage, because all messages go through one place.
- Easy to add a new agent, because we only connect it to the main agent.
- Easy to log and monitor, because all messages pass through one point.

Disadvantage:

- The main agent can become a bottleneck if there is too much traffic.
- If the main agent fails, the whole system fails.

This is how Centralized Communication works. Now, let's move to Broadcast Communication.

## Broadcast Communication

Broadcast Communication means one agent sends the same message to many agents at once, and any agent that is interested can act on it.

This is also called the publish-subscribe pattern. One agent publishes a message. Many agents subscribe to that type of message. When the message is published, all subscribed agents receive it.

Let's say we are building a news system. One agent publishes a new article. A summary agent, a translation agent, and a fact-check agent all subscribe to new articles. The moment the article is published, all three agents receive it and start their own work in parallel.

We can picture it like below:

```text
                                  ┌──▶ Summary Agent
   News Agent ──▶ [Broker] ───────┼──▶ Translation Agent
   (Publisher)                    └──▶ Fact-check Agent

```

Here, the sender does not send to the agents directly. It just publishes the message to the broker, and the broker delivers it to every agent that has subscribed. This is why the sender does not need to know who is listening.

- Very flexible, because the sender does not need to know the receivers.
- Easy to add new agents, because they just subscribe to the messages they care about.
- Good for running many agents in parallel.

- Harder to track which agent did what.
- Can create a lot of traffic if too many agents listen to too many messages.

This was all about Broadcast Communication. Now, it's time to learn about Shared Memory Communication.

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

## Shared Memory Communication

Shared Memory Communication means agents do not send messages to each other directly. Instead, they read from and write to a common memory that all of them can access.

This common memory is often called a blackboard. One agent writes its result on the blackboard. Another agent reads that result, does its work, and writes its own result back. This continues until the task is done.

Let's say we are solving a complex math problem with many agents. The first agent writes the known values on the blackboard. The second agent reads them, solves one part, and writes the partial answer. The third agent reads the partial answer and finishes the solution. No agent sends a direct message. They all talk through the shared blackboard.

We can picture it like below:

```text
   Agent 1 ◀──▶ ┌───────────────────┐ ◀──▶ Agent 2
                │   Shared Memory   │
                │   (Blackboard)    │
   Agent 3 ◀──▶ └───────────────────┘ ◀──▶ Agent 4

```

Here, the shared memory is the single place where all the work comes together. Every arrow points both ways, because each agent reads from the blackboard and writes back to it.

- Agents do not need to know about each other, only about the shared memory.
- Easy to add new agents that read and write the same memory.
- Good for tasks where many agents build on the same growing result.

- We must handle the case where two agents write at the same time.
- The shared memory can become messy if too many agents write to it without rules.

This way we can use Shared Memory Communication to let many agents work on the same problem together.

Now that we have learned about all four patterns, let me put them in a table for your better understanding so that you can decide which one to use based on your use case.

| Pattern | How agents talk | Real-world analogy | Best for |
| --- | --- | --- | --- |
| Direct | One agent to another, no middleman | Two people talking face to face | A few agents in a fixed flow |
| Centralized | All agents talk to one main agent | A manager routing tasks | Clear control and easy logging |
| Broadcast | One agent sends to many at once | A teacher announcing to a class | Many agents reacting in parallel |
| Shared Memory | Agents read and write a common memory | A whiteboard everyone writes on | Many agents building one result |

In real projects, we often mix these patterns. For example, a main agent can use Centralized Communication to control the overall flow and decide which agent runs next. Then, inside one of those steps, a group of agents can use Shared Memory Communication to read and write the same data while they work together. The right mix depends on our use case.

To learn how to design these communication patterns into real systems - Multi-Agent Systems, Orchestration and Routing, and Agent Architecture - check out our AI and Machine Learning Program at Outcome School.

## What a message looks like

Now, the next big question is: what does a message between two agents actually look like? The answer is, a message is usually a small structured block of data that both agents can understand.

A good message often has the following parts:

- Sender - Which agent sent the message.
- Receiver - Which agent the message is for.
- Type - The kind of message, like a request, a result, or an error.
- Content - The actual information, like the question, the answer, or the data.
- Context - Extra information that helps the receiver, like the task id or past history.

A simple message can look like below. It is written in JSON, which is just a simple text format used to store data in a clear and readable way.

```json
{
  "sender": "research_agent",
  "receiver": "writing_agent",
  "type": "result",
  "content": "Here are the five key facts about the topic...",
  "context": {
    "task_id": "trip-123",
    "step": "research"
  }
}

```

Here, we can see that the message clearly says who sent it, who it is for, what type it is, and what it contains. Because the format is fixed, both agents can read it without confusion. This is why a clear message format is so important when agents communicate.

## The rules agents follow to talk

A protocol is the agreed set of rules that all agents follow to talk to each other. Both agents must follow the same protocol, just like two people must speak the same language to understand each other.

Here are some popular protocols and standards:

- MCP (Model Context Protocol) - An open standard that connects agents and models to tools and data sources in a common way. It helps an agent use external tools without custom code for each one.
- A2A (Agent2Agent Protocol) - A standard made for agents to talk to other agents, even when they are built by different teams or companies.
- HTTP and REST APIs - The classic way, where one agent calls another agent's API over the network.
- Message Queues - Tools like Kafka or RabbitMQ that let agents send messages through a queue, so the sender and receiver do not have to be online at the same time.

One good thing to know is that this space is coming together, not breaking apart. Both MCP and A2A now sit under the Linux Foundation, and they work together. We use MCP to connect an agent to its tools, and we use A2A to connect one agent to another agent. So, instead of every team building its own rules, we now have common standards that everyone can share. There is one more open standard worth knowing here, called OKF, which writes down what our data and systems actually mean, so an agent knows what it is looking at once a protocol connects it. We have a detailed blog on What is OKF (Open Knowledge Format)? that covers this end to end.

We do not have to pick just one. We can use a simple API call for two agents in the same system, and a standard protocol like A2A when agents from different companies must talk. The right choice depends on our use case.

If we want to go deep into protocols like the Model Context Protocol (MCP) and the full multi-agent architecture, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Challenges when agents communicate

Here are the main challenges:

- Different formats - If two agents use different message formats, they cannot understand each other. We need a common protocol.
- Message loss - A message can get lost on the network. We must plan for retries and confirmations.
- Latency - Every message adds delay. The more agents talk, the slower the system becomes.
- Loops - Two agents can keep sending messages back and forth forever. We must add limits to stop endless loops.
- Wrong information - One agent can send wrong or made-up information, and the next agent will trust it. One mistake can spread across all agents.
- Security - A bad message can trick an agent into doing something harmful. We must check every message.
- Order of messages - Messages can arrive in the wrong order. We must handle this so that agents do not act on old information.
- Observability - With many messages flowing in many directions, it becomes hard to know what is happening inside the system.

Now that we have learned about the challenges, it's time to learn the best practices that help us solve them.

## Best Practices

Here are the best practices for agent communication:

- Use a common protocol - Pick one protocol and make all agents follow it. This removes confusion and makes agents understand each other.
- Keep messages small and clear - A message must carry only what the receiver needs. Smaller messages are faster and easier to debug.
- Add a maximum number of messages - Always set a limit on how many messages can flow for one task. This stops endless loops between agents.
- Validate every message - Check every incoming message before acting on it. This keeps the system safe from bad or harmful messages.
- Log every message - Log who sent what, when, and to whom. We will need these logs to debug and improve the system.
- Handle failures gracefully - Plan for lost messages, timeouts, and retries. A reliable system expects failures and recovers from them.
- Give each agent one clear job - When each agent has a single focused job, the messages stay simple and the system stays clean.
- Keep a shared context - Store the task state in a shared place so that every agent works with the same up-to-date information.
- Keep humans in the loop for critical actions - For high-stakes actions like making a payment or sending an email, ask for human approval before the action runs.

This is how AI agents communicate.

### What is the difference between MCP and A2A?

MCP connects an agent to its tools, while A2A connects one agent to another agent. MCP is an open standard that connects agents and models to tools and data sources in a common way. A2A is made for agents to talk to other agents, even when they are built by different teams or companies. Both now sit under the Linux Foundation and work together.

### Can we mix different agent communication patterns in one system?

Yes. In real projects, we often mix these patterns. For example, a main agent can use Centralized Communication to control the overall flow and decide which agent runs next. Then, inside one of those steps, a group of agents can use Shared Memory Communication to read and write the same data. The right mix depends on our use case.

### Is Direct Communication a good choice when we have many agents?

No. Direct Communication is simple and fast, but it becomes hard to manage with many agents, because every agent must know how to reach every other agent. Adding a new agent means connecting it to all the others by hand. Centralized Communication is easier to manage here, because we only connect the new agent to the main agent.

### How do we stop two AI agents from messaging each other forever?

We set a maximum number of messages that can flow for one task. Two agents can keep sending messages back and forth forever, so this limit stops endless loops. Logging every message also helps us see who sent what, when, and to whom, which makes such problems easier to debug.

### What happens if one agent sends wrong information to another agent?

The next agent will trust it, and one mistake can spread across all agents. A bad message can even trick an agent into doing something harmful. This is why we must validate every incoming message before acting on it and keep humans in the loop for high-stakes actions like making a payment or sending an email.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# What are Agent Skills?
URL: https://outcomeschool.com/blog/what-are-agent-skills
Published: 2026-07-30
Author: Amit Shekhar

What are Agent Skills?

# What are Agent Skills?

Authors
: - Name
: Amit Shekhar
Published on
: July 30, 2026

An Agent Skill is a folder of instructions, and optionally scripts and reference files, that an AI agent loads by itself only when the task actually needs it.

In this blog, we will learn about Agent Skills. We will also see why we need them, what is inside a Skill, how the description makes an agent pick up the right Skill by itself, how progressive disclosure keeps the context window free, how Agent Skills differ from MCP, and how we can create our own Skill.

We will cover the following:

- The problem before Agent Skills
- What are Agent Skills?
- What is inside a Skill?
- The description is the trigger
- Progressive disclosure, the main idea
- A Skill can carry real code
- Where Skills live
- How do we create our own Skill?
- Agent Skills vs MCP
- A real example
- Importance of Agent Skills
- Things we must be careful about
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The problem before Agent Skills

Before jumping into Agent Skills, we must understand the problem they solve.

An AI agent is an AI that takes actions step by step to finish a job for us. It can read files, run commands, and use tools.

Now, an agent is very capable in general, but it does not know how our team does things. It does not know our company's report format. It does not know the exact steps our team follows to release software. It does not know that our brand never uses a certain word.

So, what do we do? We type all of it into the chat, every single time.

We must have faced this. We explain the same eight steps on Monday. We explain them again on Wednesday. We explain them once more the next week to a teammate. The knowledge lives in our head, and we keep paying the cost of typing it out.

```
   Monday:     we type the 8 steps again
   Wednesday:  we type the 8 steps again
   Next week:  our teammate types the 8 steps again

```

Here, we can see the waste. The knowledge is stable, but the effort repeats forever.

Now, we can think that the answer is simple. Let's write all of it into one big instruction file, and keep that file loaded at all times.

But, here is the catch. That does not work either, and we must understand why.

An agent reads everything through a limited space called the context window. Think of it as the agent's desk. Only so many pages fit on the desk at one time. Every instruction we keep loaded occupies that desk space forever, even when it has nothing to do with the current job. Load twenty procedures, and the agent is reading nineteen irrelevant ones while trying to do the twentieth.

Deciding what deserves that limited space is a discipline of its own. We have a detailed blog on Context Engineering that covers this end to end.

So, we need a way to give the agent deep knowledge without keeping all of it on the desk at all times.

We needed a solution for that. So, here come Agent Skills to the rescue.

## What are Agent Skills?

An Agent Skill is a folder of instructions, and optionally scripts and reference files, that an AI agent loads by itself only when the task actually needs it.

Agent Skills were introduced by Anthropic in October 2025, and the format is open, so anyone can write one and anyone can use one.

In simple words, a Skill is a set of written instructions that teaches an agent how to do one particular job well. We write it once, and the agent picks it up on its own whenever that job comes up.

Let's decompose the term for the sake of understanding.

> Agent Skills = Agent + Skills

The agent is the AI that does the work. A skill is one specific ability it has learned. So, Agent Skills are simply the specific abilities we hand to our agent.

Consider a new employee joining our team. They are already smart and already know their profession. But they do not know our office. So, we do not retrain them from zero. We hand them our team handbook. Inside that handbook, there are separate chapters. One chapter for filing an expense. One chapter for releasing software. One chapter for writing a report.

The new employee does not read the whole handbook every morning. They open one chapter, only when they face that particular job.

A Skill is exactly one such chapter. And the agent is smart enough to open the right chapter by itself.

## What is inside a Skill?

Now, let's open a Skill and see what is inside. A Skill is just a folder on a computer, which means we can read it, edit it, and share it like any other folder.

Inside that folder, there is one required file called `SKILL.md`. The `.md` ending means it is a markdown file, which is simply a plain text file with light formatting. Note: There is nothing special or secret about it. We can open it in any text editor.

A `SKILL.md` file has two parts.

The first part sits at the very top, between two lines of dashes. This top part is called the frontmatter, and it holds the labels that describe the Skill. The two important labels are the `name` and the `description`.

The second part is the body, which is everything below the frontmatter. The body holds the actual instructions, written in plain English.

Let's see a small one as below:

```markdown
---
name: weekly-report
description: Creates the weekly team report in our company format. Use this whenever the user asks for a weekly report or a team update.
---

# Weekly report

Follow these steps.

First, collect all the tasks finished in the last seven days.
Then, group them under three headings: Shipped, In Progress, and Blocked.
After that, write one short line for each task. Never write more than one line.
Finally, put the total count at the top.

Never include internal ticket numbers in the final report.

```

Here, we can see the whole idea in one small file. The top part tells the agent what this Skill is and when to reach for it. The body tells the agent exactly how to do the job. Both parts are plain English, and we did not write a single line of programming code.

Note: The `name` must be written in small letters, with hyphens in place of spaces, like `weekly-report`. The `description` is plain English, and we must keep it short enough to read in one breath.

A Skill folder can also hold other files next to `SKILL.md`, like a reference document, a template, or a script. We will come to those shortly.

## The description is the trigger

Now, the most important question is: how does the agent know when to use our Skill?

The answer is the `description`.

The agent reads the `name` and the `description` of every available Skill. Then, when we ask for something, it compares our request against those descriptions and decides which Skill fits.

So, the `description` is not decoration. It is the trigger. A vague description means the Skill sits unused. A clear description means the Skill fires at the right moment.

Let's compare two descriptions.

```
   Weak:    "Report helper."
            The agent cannot tell when this applies. It stays unused.

   Strong:  "Creates the weekly team report in our company format.
             Use this whenever the user asks for a weekly report
             or a team update."
            The agent knows exactly what it does and when to use it.

```

Here, we can see the difference clearly. The strong one says what the Skill does and when to use it. Those are the two things the agent needs.

Note: We must write the description for the agent to read, not for a human to admire.

## Progressive disclosure, the main idea

Now, we come to the heart of Agent Skills. This one idea is what makes them work, so let's go slowly.

Remember our problem. The agent's desk is small, and we cannot keep everything on it.

Agent Skills solve this with something called progressive disclosure. The words sound heavy, but the idea is simple. It means revealing information in stages, and only as much as is needed right now.

It works in three levels.

Level 1. At the start, the agent loads only the `name` and the `description` of each Skill. That is a couple of lines each. So even fifty Skills cost almost nothing on the desk. At this point the agent knows only that the Skill exists, and nothing more about it.

Level 2. We ask for something. The agent matches our request to a description and decides this Skill is needed. Only now does it read the full body of `SKILL.md`. The detailed instructions arrive exactly when they become useful.

Level 3. If the body points to another file in the folder, like a long reference document, the agent opens that file only if it actually needs it.

```
   Level 1  ->  name + description only          (always loaded, tiny)
   Level 2  ->  the full SKILL.md instructions   (loaded when it matches)
   Level 3  ->  extra files in the folder        (loaded only if needed)

```

Let's put some real numbers on this, because they show why it works so well.

The unit we measure desk space in is called a token, which is roughly a piece of a word. Level 1 costs only about a hundred tokens for each Skill. Level 2, the full body, is normally kept under five thousand tokens, and we pay that cost only for the one Skill we are actually using.

Now, let's compare the two numbers, because the comparison is striking. Fifty Skills at Level 1 cost around five thousand tokens in total. That is the same as the body of one single Skill. So knowing that fifty procedures exist costs us no more than reading one of them in full.

Here, we can see why this is clever. The agent behaves as if it knows fifty procedures in depth, while its desk stays almost empty. Nothing is loaded until it earns its place.

This is exactly what a good handbook does. The table of contents is short and always in front of us. The chapter is long, and we open it only when we need it.

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

## A Skill can carry real code

Now, let's learn one more thing that makes Skills powerful.

A Skill folder can hold a script, which is a small program that can be run. When the job involves an exact, repeatable operation, we put a script in the folder and the instructions tell the agent to run it.

Now, why does this matter so much? Let's understand the difference.

Without a script, the agent has to write the code itself, every single time. It thinks, it writes, it sometimes writes it slightly differently, and it fills up the desk with all of that writing.

With a script, the agent runs one ready-made, tested file. The result is the same every time, and it costs almost nothing on the desk.

```
   Without a script:  the agent writes the code again each time
                      (slower, and the result can vary)

   With a script:     the agent runs one tested file
                      (fast, and the result is the same every time)

```

Here, we can see a simple rule. If the task needs judgment, we write instructions in plain English and let the agent think. If the task needs exactness, we write a script and let the agent run it.

## Where Skills live

Now, let's see where we keep these folders. There are two common places, and the difference matters.

Personal Skills. These live in our own home folder, in a place like `~/.claude/skills/`. Note: That `~` symbol is just a short way of writing our home folder. These Skills are ours alone, and they are available in every project we work on. Good for our personal working habits.

Project Skills. These live inside the project itself, in a place like `.claude/skills/`. Because they sit inside the project, they travel along with it. When a teammate copies the project onto their own computer, they get all the Skills automatically, without anybody telling them.

```
   ~/.claude/skills/   ->  our personal Skills, in every project
   .claude/skills/     ->  the project's Skills, shared with the whole team

```

Here, we can notice the real benefit of Project Skills. Our team's knowledge stops living inside one person's head and starts living inside the project, where everybody gets it for free.

The `.claude` name in these paths belongs to a coding agent that reads such folders at the start of a session. We have a detailed blog on How does Claude Code work? that explains how it picks up our project files.

## How do we create our own Skill?

Now, let's create one ourselves. The best part is that there is nothing to install and no code to write.

Step 1: Inside our project, create a folder path `.claude/skills/`.

Step 2: Inside that, create one folder named after our Skill, like `weekly-report`.

Step 3: Inside that folder, create a file named `SKILL.md`.

Step 4: At the top of that file, write the frontmatter with the `name` and the `description`.

Step 5: Below the frontmatter, write the steps in plain English, exactly as we would explain them to a new teammate.

The whole thing will look like below:

```
   our-project/
     .claude/
       skills/
         weekly-report/
           SKILL.md

```

Here, we can see how small this really is. One folder and one text file, and our Skill is ready.

Now, here is the best way to write the body. We must imagine we are writing for a capable new teammate, somebody who already knows the profession but does not know our office. So, we skip everything they already know, and we write down only what is specific to us. That single habit produces good Skills.

## Agent Skills vs MCP

Now, the following question arises. There is another thing called MCP that also gives an agent new abilities, so how are the two different?

First, let's recall what MCP is. MCP, which stands for Model Context Protocol, is one common standard that lets an AI application connect to outside tools and data, like our database or our GitHub.

Both are useful, and they are not competing at all. They answer two different questions.

MCP connects the agent to the outside world. It answers the question "what can the agent reach?" It gives the agent hands.

Agent Skills teach the agent our way of working. They answer the question "how should the agent do this?" They give the agent know-how, so it follows our exact steps and our exact format.

So, one gives reach and the other gives know-how.

Let me tabulate the differences between Agent Skills and MCP for your better understanding.

| Point | Agent Skills | MCP |
| --- | --- | --- |
| What it gives | Know-how, our steps and our format | Reach, a connection to outside systems |
| What it is made of | A folder of instructions, and sometimes scripts | A running program that offers tools and data |
| Question it answers | How should this be done? | What can the agent reach? |
| Needs a server running | No | Yes |
| Best for | Procedures, formats, style, checklists | Databases, apps, live data, actions |

In real work we often use both together. MCP connects the agent to our issue tracker, and a Skill tells it how our team writes an issue.

There is also a third piece in this space, built almost exactly like a Skill. OKF (Open Knowledge Format) writes down the knowledge about our data as a folder of plain markdown files, so the agent knows what our tables actually mean. We have a detailed blog on What is OKF (Open Knowledge Format)? that explains where it sits along with these two.

## A real example

The best way to learn this is by taking an example. Let's follow one request from start to finish, using the `weekly-report` Skill from earlier.

Step 1: The session begins. The agent loads only the names and descriptions of the available Skills. Our `weekly-report` description is now known to it, but the instructions are not loaded yet.

Step 2: We type, "prepare this week's team update."

Step 3: The agent compares our sentence with the descriptions it holds. Our description mentions "a weekly report or a team update", so it matches.

Step 4: The agent now reads the full body of `SKILL.md`. At this moment, it learns the three headings, the one-line rule, the total count at the top, and the rule about never including ticket numbers.

Step 5: It follows those steps and produces the report in our exact format.

Here, we can notice the best part. We never mentioned the format. We never mentioned the headings. We never reminded it about ticket numbers. We wrote all of that down once, weeks ago, and the agent applied it by itself at the right moment.

This way we can use Agent Skills to solve the interesting problem of teaching an agent our way of working, permanently, without repeating ourselves.

We have a complete program on AI Agents, Context Engineering, and Model Context Protocol (MCP) - check out our AI and Machine Learning Program at Outcome School to learn all of these in depth.

## Importance of Agent Skills

Now, we have understood how Agent Skills work. Let's see why they are important.

- Write once, use forever. We stop repeating the same instructions in every chat.
- The desk stays clean. Because of progressive disclosure, deep knowledge costs almost nothing until the moment it is used.
- Team knowledge becomes shared. A Project Skill turns one person's experience into something the whole team gets automatically.
- No programming needed. A Skill is plain English in a plain text file. Anyone who can write clear steps can write one.
- They are portable. Because the format is open and it is just a folder, the same Skill works across different tools that support it.
- They compose. The agent can combine more than one Skill in a single job, using one for the format and another for the checks.

## Things we must be careful about

Skills change how an agent behaves, so we must use them with care.

A Skill can run code. If a Skill folder contains a script, the agent can run it. That is exactly like installing any program on our computer. So, we must use Skills only from sources we trust, and we must read a Skill before using it.

A vague description is a wasted Skill. This is the most common mistake. We write good instructions, but the description does not say when to use them, so the Skill never fires. If a Skill seems to be ignored, the description is almost always the reason.

Too long is as bad as too vague. The body must hold only what the agent cannot guess by itself, which means our steps, our format, and our rules. It must not explain general knowledge that the agent already has. A tight Skill beats a long one.

One Skill, one job. It feels tempting to put everything into one giant Skill. We must not do that. Many small and focused Skills match better and load less.

Here, we can see that the rule is simple. Keep each Skill small and specific, write the description for the agent, and trust only the Skills we have read.

## Summary

Let's quickly recap what we have learned.

- An agent does not know our team's procedures, formats, and rules, so we end up typing them again and again.
- We cannot simply keep everything loaded, because the agent's context window is limited.
- An Agent Skill is a folder of instructions, and optionally scripts and files, that the agent loads by itself only when the task needs it.
- The folder needs one file called `SKILL.md`, which has a frontmatter with a `name` and a `description`, plus a body with the instructions.
- The `description` is the trigger. The agent uses it to decide when the Skill applies.
- Progressive disclosure works in three levels. Names and descriptions always, the full instructions when matched, and extra files only if needed.
- A Skill can carry a script, so exact and repeatable work runs the same way every time.
- Personal Skills live in our home folder, and Project Skills live in the project and travel to the whole team.
- Creating one needs no installation and no code. One folder and one `SKILL.md` file is a complete Skill.
- The best way to write a Skill is to write for a capable new teammate, skipping what they already know and recording only what is specific to us.
- MCP gives the agent reach, while Skills give the agent know-how. We often use both together.

This is what Agent Skills are, a simple folder that turns our own way of working into something our agent knows and applies on its own.

### Who created Agent Skills?

Agent Skills were introduced by Anthropic in October 2025. The format is open, so anyone can write a Skill and anyone can use one. Because a Skill is just a folder with a `SKILL.md` file, the same Skill works across the different tools that support the format.

### Why is my Agent Skill not being used by the agent?

The reason is almost always a vague description. The agent decides when to use a Skill by comparing our request against each Skill's description. If the description does not clearly say what the Skill does and when to use it, the Skill never fires, even when its instructions are good.

### Does adding many Skills fill up the context window?

No. At the start, the agent loads only the name and description of each Skill, which costs about a hundred tokens per Skill. So, fifty Skills cost around five thousand tokens in total. The full instructions of a Skill are loaded only when a request matches it.

### Can an agent use more than one Skill in a single task?

Yes. Skills compose, so the agent can combine more than one Skill in a single job. For example, it can use one Skill for the format and another Skill for the checks. Also, many small and focused Skills match better and load less than one giant Skill.

### Is it safe to use Agent Skills from the internet?

Only if we trust the source. A Skill folder can contain a script, and the agent can run it, which is exactly like installing a program on our computer. So, we must use Skills only from sources we trust, and we must read a Skill before using it.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# You have built an AI agent that performs multi-step tasks like researching a topic and writing a summary. The agent works well but consumes an excessive number of tokens per task - … | Pallavi .
URL: https://www.linkedin.com/posts/pallavi-shekhar_ai-aiagents-machinelearning-activity-7439550125015994368-LTmE
Published: 2026-03-17
Author: Pallavi .

# You have built an AI agent that performs multi-step tasks like researching a topic and writing a summary. The agent works well but consumes an excessive number of tokens per task - … | Pallavi . · LinkedIn · 2026-03-17

**Pallavi .**: Software Engineer at Outcome School with 8 years 1 month of experience. Previous roles include Senior Software Development Engineer at West Agile Labs, Software Engineer at NCR Corporation, and Software Engineer at Deloitte India (Offices of the US). Based in Bengaluru, Karnataka, India [IN].

---

You have built an AI agent that performs multi-step tasks like researching a topic and writing a summary. The agent works well but consumes an excessive number of tokens per task - sometimes 50,000+ tokens for a simple research query. This is making the system very expensive to run. How would you reduce the token consumption?

Answer:

Token consumption is one of the biggest cost drivers in AI agent systems. An agent that is not optimized for tokens can burn through the budget very quickly.

Many agents run in a plan-act-observe loop. If the stopping criteria is not well-defined, the agent keeps looping and consuming tokens. We must set a maximum number of iterations and add a clear stopping condition so the agent stops immediately once it has gathered enough information.

As the agent takes more steps, the conversation history grows and each new LLM call includes the entire history. We can summarize the conversation history after every few steps instead of passing the full history. This significantly reduces the input token count for each subsequent call.

Not every step needs the most powerful model. We implement a model routing strategy - the orchestrator uses a powerful model for complex reasoning and routes simpler tasks like data extraction to a smaller, cheaper model. We also add a caching layer for tool results so the agent reuses cached results instead of making duplicate calls.

Long system prompts consume tokens on every single call. If the system prompt is 2000 tokens and the agent makes 20 calls, that is 40,000 tokens just for the system prompt. We keep prompts concise and use dynamic prompts where only the relevant instructions are included based on the current step.

This is how we can solve the excessive token consumption problem in AI agents.

Follow Outcome School for knowledge-packed content.

Keep Learning, Keep Sharing, and Keep Growing.

#AI #AIAgents #MachineLearning #LLM #OutcomeSchool #TokenOptimization #CostOptimization

You have built an AI agent that performs multi-step tasks like researching a topic and writing a summary. The agent works well but consumes an excessive number of tokens per task - … | Pallavi . image

## Comments

**Outcome School** · 2026-03-17
> Follow for knowledge-packed content.

**AMIT SHEKHAR** · 2026-03-17
> #Agent #AI #LLM

## Engagement

- Reactions: 17
