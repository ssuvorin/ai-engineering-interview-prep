> Source: https://outcomeschool.com/blog/what-is-graph-engineering

# What is Graph Engineering?
URL: https://outcomeschool.com/blog/what-is-graph-engineering
Published: 2026-08-21
Author: Amit Shekhar

What is Graph Engineering?

# What is Graph Engineering?

Authors
: - Name
: Amit Shekhar
Published on
: August 21, 2026

Graph Engineering is the practice of designing an AI system as a graph, where every step of the work is a node, and every path from one step to another is an edge. We break the work into small steps and clearly decide which step runs after which.

In this blog, we will learn about Graph Engineering, the practice of building an AI system as a graph of small steps connected by clear paths instead of one giant prompt or one endless loop. We will also see why we need it, what nodes and edges actually mean, how the state travels through the graph, how conditional edges take decisions, how cycles let the system do the work again, how parallel branches save time, how checkpoints let us pause and resume, and where it works well and where it fails.

We will cover the following:

- What is Graph Engineering?
- Graph = Nodes + Edges
- Why do we need Graph Engineering?
- The three building blocks: Node, Edge, and State
- Let's build our first graph
- Conditional edges: taking decisions inside the graph
- Cycles: doing the work again when needed
- One full run, step by step
- Parallel branches: doing many things at the same time
- Checkpoints: pause and resume the graph
- Human in the loop
- Handling errors inside a graph
- Graph Engineering vs Loop Engineering
- Where Graph Engineering works well
- Where Graph Engineering fails
- Best practices in Graph Engineering
- Conclusion

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Graph Engineering?

Graph Engineering is the practice of designing an AI system as a graph, where every step of the work is a node and every path from one step to another step is an edge.

Graph Engineering = Graph + Engineering.

In simple words, instead of writing one huge instruction and hoping that the model does everything correctly in one go, we break the work into small steps, and then we clearly decide which step runs after which step.

Here, whenever we say the model, we mean the AI model that reads text and writes text, and whenever we say a tool, we mean anything outside the model that our system can call, like a search, a database, or an email service.

We hear this word mostly around AI agents today, and there is a good reason for that. Real work is never one step. Real work is many steps, with going back, waiting, checking, and approving in between. Graph Engineering is how we give that shape to our system.

## Graph = Nodes + Edges

Before jumping into Graph Engineering, we must know what a graph is.

A graph is just two things.

- Nodes: the places where something happens.
- Edges: the paths that connect one place to another place.

The best way to learn this is by taking an example.

Let's say we are looking at the metro map of a city. Every station on that map is a node. Every track between two stations is an edge. A train starts from one station, travels on a track, reaches the next station, and continues like this until it reaches the last station.

Now, replace the stations with the steps of our work, and replace the tracks with the order of our work. That is exactly the graph we build in Graph Engineering.

| Metro map | Our AI system |
| --- | --- |
| Station | Node, which means one small step of work |
| Track between two stations | Edge, which means the path to the next step |
| Bag that the passenger carries | State, which means the information that travels along |
| First station | The step where our system starts |
| Last station | The step where our system stops |

Here, we can see that an edge is simply the answer to one small question. After this step is over, which step runs next?

Now, we have understood the graph. Now, let's understand why we need Graph Engineering at all.

## Why do we need Graph Engineering?

Let's say we are building a system that answers questions about a company's internal documents. A user asks a question, and our system must give a correct answer with proper sources.

We will build this system step by step. At every step we will see the problem, and then we will move to a better approach.

### Approach 1: One big prompt

We write one long instruction and send it to the model.

```text
You are a helpful assistant. Read the user question. Search the company
documents. Read the results. Write an answer. Check that the answer is
correct. Add the sources. If something is missing, search again.

```

The model reads all of this and tries to do everything at once.

Problem: The model does some parts and quietly forgets the other parts. Sometimes it writes the answer without searching. Sometimes it searches but never checks the answer. And when the output is wrong, we have no idea which part went wrong, because everything happened inside one single call. We cannot fix what we cannot see.

The issue with this approach is that there is no structure at all. Let's see how the next approach solve this issue.

### Approach 2: A chain of steps

Now, we break the work into separate calls, and we run them one after another.

```text
Step 1: understand the question
Step 2: search the documents
Step 3: write the answer
Step 4: send the answer

```

This is prompt chaining, and it is much better. Every step has only one job. When something goes wrong, we know exactly which step failed.

Problem: A chain always moves forward in a straight line. It never comes back. But real work needs coming back. What if the search returns nothing useful? What if the answer is wrong and needs to be written again? A straight chain cannot do this. It simply walks forward and delivers a bad answer.

The issue with this approach is that it cannot go back. Let's see how the next approach solve this issue.

### Approach 3: One loop

Now, we put the whole thing inside an agent loop. The model thinks, calls a tool, looks at the result, and thinks again, again and again, until it decides that the work is done.

This solves the coming back problem. The model can search again, write again, and correct itself.

Problem: Now we have gone to the other extreme. Every decision is taken by the model inside one loop, so we have very less control. The model repeats the same failing search ten times. It skips the checking step because it feels confident. It calls a dangerous tool that we never wanted it to call at that moment. The path is different on every run, so testing becomes very hard.

The issue with this approach is that the flow is completely in the model's hands. Let's see how the next approach solve this issue.

### Approach 4: A graph

So, here comes Graph Engineering to the rescue.

We keep the small steps of Approach 2, we keep the coming back ability of Approach 3, and we write down the paths ourselves.

```text
understand  ->  search  ->  write  ->  check
check       ->  send        (when the answer is good)
check       ->  search      (when the sources are missing)
check       ->  write       (when the answer is weak)

```

Here, we can see that every step is small and visible, the system can go back when it needs to, and the model takes decisions only at the places where we allow it to take decisions.

The problem is solved. This is Graph Engineering.

The example we took here, where the system searches, writes, checks, and searches again, is what we call Agentic RAG, and we have a detailed blog on it that explains this in depth.

## The three building blocks: Node, Edge, and State

Every graph we build has only three parts.

Node: A node is one step of the work. It is just a function. It takes the current information, does one small job, and gives the updated information back. A node can call a model, call a tool, hit a database, or run plain code with no model at all.

Edge: An edge is a path from one node to another node. It answers only one question. Which node runs next?

State: The state is the shared notebook of the graph. Every node reads from this notebook and writes into this notebook. This is how the second node knows what the first node did.

Let's see the state for our document question system as below:

```python
state = {
    "question": "What is our refund policy?",
    "intent": None,
    "documents": [],
    "answer": None,
    "score": None,
    "attempts": 0,
}

```

Here, we have created a simple notebook with empty values. As the graph runs, the nodes will keep filling these values. The `understand` node fills `intent`. The `search` node fills `documents`. The `write` node fills `answer`. The `check` node fills `score` and `attempts`.

This state is the most important design decision in Graph Engineering. If the state is clean, the graph stays simple. If the state becomes a dumping ground of random keys, the graph becomes impossible to understand. Whatever a node puts in front of the model also comes out of this state, so keeping it clean is good Context Engineering as well.

Now that we have learned about the building blocks, it is time to build a real graph.

## Let's build our first graph

First, we will write the nodes. Every node is a plain function.

```python
def understand(state):
    state["intent"] = model.find_intent(state["question"])
    return state

def search(state):
    state["documents"] = db.search(state["intent"])
    return state

def write(state):
    state["answer"] = model.write_answer(state["question"], state["documents"])
    return state

```

Here, we can notice that each function does exactly one job and returns the updated state. There is no big instruction anywhere. The `understand` node only finds the intent. The `search` node only searches. The `write` node only writes the answer from the documents that the `search` node found.

Then, we will connect these nodes with edges.

```python
graph = Graph(state)

graph.add_node("understand", understand)
graph.add_node("search", search)
graph.add_node("write", write)

graph.add_edge("understand", "search")
graph.add_edge("search", "write")

graph.set_entry("understand")
graph.set_finish("write")

```

Here, we have first added the three nodes to the graph. Then, we have added two edges. The first edge says that after `understand`, the `search` node runs. The second edge says that after `search`, the `write` node runs. Finally, we have told the graph where to start and where to stop.

After this, we can run the graph.

```python
final_state = graph.run(state)
print(final_state["answer"])

```

Here, we are giving the starting notebook to the graph. The graph walks from node to node, each node updates the notebook, and at the end we read the answer from the same notebook.

It works perfectly. But this graph is still a straight line, exactly like Approach 2. Now, let's give it the power to take decisions.

Note: The code in this blog is kept simple just for the sake of understanding. The real libraries built for this work give us the same three ideas of node, edge, and state, only with slightly different names. LangGraph is the most popular one of them, and we have a detailed blog on it that explains how it works step by step.

## Conditional edges: taking decisions inside the graph

A normal edge always goes to the same next node. A conditional edge looks at the state first and then decides which node runs next.

Let's add a `check` node that gives a score to our answer.

```python
def check(state):
    state["score"] = model.rate_answer(state["answer"], state["documents"])
    state["attempts"] = state["attempts"] + 1
    return state

```

Here, we have used the model as a reviewer, which is the LLM as a Judge pattern. It reads the answer along with the documents, and it gives a score out of ten. We are also counting the attempts, and we will see very soon why this count matters so much.

Now, we will write the routing function.

```python
def route_after_check(state):
    if state["score"] >= 8:
        return "send"
    if not state["documents"]:
        return "search"
    return "write"

```

Here, we can see that the decision is plain code, and it is fully in our hands. If the score is good, we go to `send`. If there were no documents at all, we go back to `search`. In every other case, we go back to `write` and try again.

Then, we attach this function as a conditional edge.

```python
graph.add_node("check", check)
graph.add_node("send", send)

graph.add_edge("write", "check")
graph.add_conditional_edge("check", route_after_check)

graph.set_finish("send")

```

We have followed the following steps:

- We have added the `check` node and the `send` node. The `send` node is a small node that simply delivers the final answer to the user.
- We have added a normal edge from `write` to `check`, so every answer goes for review.
- We have added a conditional edge from `check`. This edge has three possible destinations, and our routing function picks one of them by reading the state.
- We have moved the finish point from `write` to `send`, because `send` is the last station of our graph now.

Note: The model gave the score, but the model did not choose the path. The path was chosen by our own code. This is the heart of Graph Engineering. We let the model do the thinking, and we keep the control of the flow with ourselves.

To learn Graph Engineering, Orchestration and Routing, and LLM as a Judge, we cover all of them in depth in our AI and Machine Learning Program at Outcome School.

## Cycles: doing the work again when needed

In the graph above, `check` can send us back to `write`, and `write` sends us to `check` again. This going back and forth between two nodes is called a cycle.

A cycle is a very powerful thing, because this is how a system corrects itself. Write, review, write better, review again. This is exactly how a human works, and this is also the idea behind a Reflection Agent.

But, here is the catch. A cycle can run forever. If the reviewer never gives a score of eight, our graph will keep writing and checking until our money is over.

So, every cycle must have a stop condition. This is why we were counting the attempts inside the `check` node.

```python
def route_after_check(state):
    if state["score"] >= 8:
        return "send"
    if state["attempts"] >= 3:
        return "ask_human"
    if not state["documents"]:
        return "search"
    return "write"

```

Here, we have added two highlighted lines. After three attempts, the graph stops trying on its own and hands the work over to a human through a new `ask_human` node. We must also add this node to the graph, otherwise the graph will not know where this path goes.

```python
graph.add_node("ask_human", ask_human)
graph.add_edge("ask_human", "send")

```

Here, we have added the `ask_human` node and joined it to `send`, so even this sad path reaches the last station properly.

Our full graph looks like below now:

```text
understand  ->  search  ->  write  ->  check
check       ->  send        (the score is good)
check       ->  ask_human   (three attempts are over)
check       ->  search      (there are no documents)
check       ->  write       (the answer is weak)
ask_human   ->  send

```

Here, we can see the complete shape of our system on one screen. Every step is a node, every line is an edge, and there is no hidden behaviour anywhere.

Our system now fails in a safe and predictable way instead of running forever.

Very important: Every cycle in our graph must have a hard limit.

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

## One full run, step by step

Now, let's walk through one complete run and see what the notebook looks like after every node. This is the best way to feel how a graph really works.

Step 1: The user asks a question, so the starting state is:

```text
question: "What is our refund policy?"
intent: None, documents: [], answer: None, score: None, attempts: 0

```

Step 2: The `understand` node runs and fills the intent:

```text
intent: "refund policy duration and conditions"

```

Step 3: The `search` node runs and fills the documents:

```text
documents: ["policy-v3.pdf", "faq-refunds.md"]

```

Step 4: The `write` node runs and fills the answer:

```text
answer: "Refunds are allowed within 30 days."

```

Step 5: The `check` node runs. The answer has no sources in it, so the reviewer gives a low score:

```text
score: 5, attempts: 1

```

Step 6: The conditional edge reads the state. The score is below eight, the documents are present, and the attempts are below three, so the path goes back to `write`.

Step 7: The `write` node runs again, and this time it writes a better answer with sources:

```text
answer: "Refunds are allowed within 30 days of purchase, as per policy-v3.pdf."

```

Step 8: The `check` node runs again:

```text
score: 9, attempts: 2

```

Step 9: The conditional edge reads the state again. The score is eight or more, so the path goes to `send`, and the graph stops there.

Here, we can notice one beautiful thing. The system found its own mistake and corrected it, and still it never went out of our control, because we had written every path ourselves.

This was all about one single run of our graph. Now, let's see how we can make our graph faster.

## Parallel branches: doing many things at the same time

Sometimes two steps have nothing to do with each other. Searching our internal documents and searching the public web are completely independent. Running them one after another only wastes time.

In a graph, we can send one node to two nodes at the same time.

```python
graph.add_edge("understand", "search_docs")
graph.add_edge("understand", "search_web")

graph.add_edge("search_docs", "merge")
graph.add_edge("search_web", "merge")

```

Here, we can see two things. First, `understand` has two outgoing edges, so both the searches start together. This is called fan-out. Second, both the searches point to the same `merge` node, so the graph waits for both of them to finish and then continues. This is called fan-in.

The `merge` node joins the two results.

```python
def merge(state):
    state["documents"] = state["doc_results"] + state["web_results"]
    return state

```

Here, we have simply joined both the lists into the `documents` key, and the rest of our graph does not even need to know that two searches happened.

Fan-out and fan-in are two of the common patterns that we use to coordinate many steps together. We have a detailed blog on AI Orchestration that covers these patterns end to end.

Note: When two nodes run at the same time, they must write into different keys of the state. If both write into the same key, one will silently overwrite the other, and we will spend hours finding that bug.

## Checkpoints: pause and resume the graph

A long graph takes time. It calls models, it calls tools, and it waits for slow services. Now, what happens if our server restarts in the middle of a run? In a simple loop, everything is lost, and the user has to start again from zero.

Here comes checkpointing into the picture.

After every node finishes, the graph saves the state. This saved state is called a checkpoint. If something breaks, we load the last checkpoint and continue from that exact node.

```python
graph = Graph(state, checkpointer=Database())

final_state = graph.run(state, thread_id="user-123")

```

Here, we have given a storage to the graph, and we have given an id to this particular run. After every node, the state is saved against this id. If this run breaks after the `search` node, we call `run` again with the same `thread_id`, and the graph starts from `write` instead of starting from `understand`.

[…580ln elided…]

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

[Showing lines 1-473 and 1054-1397 of 1397; 580 middle lines (31.6KB) elided. Read artifact://51 for full output]
