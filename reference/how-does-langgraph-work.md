> Source: https://outcomeschool.com/blog/how-does-langgraph-work

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

LangGraph is a framework that helps us build applications powered by an LLM, where the work is organized as a graph of steps, and a shared state travels from one step to the next.

In this blog, we will learn about how LangGraph works. We will also see why we need it, what graphs, state, nodes, and edges are, how tools work and who actually calls them, how memory and human-in-the-loop fit in through a complete example, and when to use it in the real world.

We will cover the following:

- What is LangGraph?
- Why do we need LangGraph?
- What is a Graph in LangGraph?
- What is State in LangGraph?
- Nodes and Edges
- Conditional Edges
- A complete example
- Tools and who calls them
- Memory and persistence
- Human-in-the-loop
- When to use LangGraph

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is LangGraph?

LangGraph is a framework that helps us build applications powered by an LLM, where the work is organized as a graph of steps.

Before we go ahead, let's understand one term first. An LLM is a Large Language Model. It is the kind of AI model that powers tools like ChatGPT. We give it some text, and it gives us back some text.

Now, let's decompose the name to make it simple.

LangGraph = Lang + Graph

`Lang` comes from language, because we are working with language models. `Graph` is a way of connecting steps together. So, LangGraph is a way to connect language model steps together in a structured manner.

In simple words, LangGraph lets us describe an AI application as a set of steps, and it controls which step runs, in what order, and what happens next.

LangGraph comes from the same team behind LangChain and builds on its ideas, adding graphs, loops, and branching on top. We have a detailed blog on how LangChain works that explains this in depth.

## Why do we need LangGraph?

The best way to learn this is by taking an example.

Suppose we want to build a simple AI app. We send a question to the LLM, and it gives us an answer. This is easy. We do not need any framework for this.

But real applications are not that simple. Let's say we are building a customer support assistant. The assistant must do many things.

First, it must read the user's message. Then, it must decide whether the question is about billing or about a technical issue. After that, it must search the right document. Then, it must ask the LLM to write a reply. And sometimes, it must ask a human to approve the reply before sending it.

Now, here is the catch. These steps are not a straight line. The app must make decisions. It must loop back and try again. It must remember what happened before. It must pause and wait for a human.

If we write all of this with plain `if` and `else` conditions, the code becomes messy very fast. It becomes hard to read and hard to change.

So, here comes LangGraph to the rescue.

LangGraph lets us describe these steps and decisions clearly as a graph. It then runs the graph for us. It makes our life easy.

## What is a Graph in LangGraph?

Before jumping into LangGraph, we must know what a graph is.

A graph is a collection of points connected by lines.

In simple words, a graph has two things.

- Nodes: these are the points. Each point is a piece of work.
- Edges: these are the lines. Each line connects one point to the next point.

Let's say we draw a small map. We have three circles named A, B, and C. We draw an arrow from A to B, and another arrow from B to C. This is a graph. The circles are nodes. The arrows are edges.

Let's visualize this as below:

```text
   +-----+        +-----+        +-----+
   |  A  | -----> |  B  | -----> |  C  |
   +-----+        +-----+        +-----+
    node           node           node
            edge           edge

```

Here, we can see that `A`, `B`, and `C` are the nodes, which are the boxes that do work. The arrows between them are the edges, which tell the graph where to go next. The graph starts at `A`, moves to `B`, and then moves to `C`.

Consider a simple real-world map. We start at home, then we go to the office, then we go back home. Home and office are nodes. The roads between them are edges.

In LangGraph, each node does some work, and each edge tells the app where to go next. This is the core idea, and everything else is built on top of it.

Designing a system this way, as nodes and edges, is called Graph Engineering, and we have a detailed blog on it that explains this from the ground up.

## What is State in LangGraph?

Before we build a graph, we must understand one more important concept called state.

State is the shared memory that travels through the graph.

In simple words, the state is a box of information that every node can read from and write to. As the app moves from one node to the next, the state carries the data along.

Let's say we are processing an order. The state can hold the user's message, the items in the cart, and the final reply. Node 1 puts the user's message into the state. Node 2 reads that message and puts the cart items into the state. Node 3 reads everything and writes the final reply.

This way, the nodes do not need to call each other directly. They just read and write to the shared state. The state is the glue that holds the whole graph together.

Let's see the code for a simple state as below:

```python
from typing import TypedDict

class State(TypedDict):
    message: str
    reply: str

```

Here, we have defined a `State` using `TypedDict`. A `TypedDict` is just a dictionary where we declare the names and the types of the values it will hold. Our state holds two things. The `message` is the user's input. The `reply` is the answer we will produce. This is the box that will travel through our graph.

## Nodes and Edges

Now that we have understood the state, it's time to learn about nodes and edges in LangGraph.

A node is a Python function that takes the current state and returns an update to the state.

In simple words, a node is one step of work. It reads the state, does something, and gives back the part of the state it wants to change.

Let's see the code for a node as below:

```python
def write_reply(state: State):
    user_message = state["message"]
    answer = "Thanks for your message: " + user_message
    return {"reply": answer}

```

Here, we have created a node named `write_reply`. It reads the `message` from the state. It builds a small answer. Then it returns a dictionary with the new `reply`. LangGraph takes this returned value and updates the shared state with it. The node does not change anything else. It only updates what it returns.

Now, let's understand edges.

An edge connects one node to the next node, and tells the graph where to go after a node finishes.

In simple words, an edge is the arrow between the steps. After one node finishes, the edge decides which node runs next.

There are two special points in every graph. The `START` point is where the graph begins. The `END` point is where the graph stops. We connect our first node to `START` and our last node to `END`.

## Conditional Edges

Till now, we have learned about normal edges that always go to the same next node. But real apps must make decisions.

So, here comes the conditional edge into the picture.

A conditional edge is an edge that picks the next node based on the current state.

In simple words, a conditional edge is like a fork on a road. Based on what is in the state, the graph chooses one path or another.

Let's say a user sends a message. We must check whether it is a billing question or a technical question. If it is billing, we go to the billing node. If it is technical, we go to the technical node. This decision is made by a conditional edge.

We can picture the fork as below:

```text
                              +------------+
                       bill   |  billing   |
                     -------> |    node    |
   +---------+      /         +------------+
   |  route  | ----+
   | message |      \         +------------+
   +---------+       -------> | technical  |
                    not bill  |    node    |
                              +------------+

```

Here, we can see that the `route message` step looks at the state and then picks one path. If the message contains the word `bill`, the graph goes to the `billing` node. Otherwise, the graph goes to the `technical` node. This is how a conditional edge branches the graph based on the state.

Let's see the code for a conditional edge function as below:

```python
def route_message(state: State):
    if "bill" in state["message"]:
        return "billing"
    return "technical"

```

Here, we have created a function named `route_message`. It reads the `message` from the state. If the message contains the word `bill`, it returns the text `billing`. Otherwise, it returns the text `technical`. LangGraph reads this returned text and sends the graph to the matching node. This way, the graph can branch in different directions.

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

## A complete example

Now, the best way to bring everything together is by building the same billing example from start to end.

Let's recall our customer support assistant. It reads a user message, decides whether the message is about billing or about a technical issue, and then replies with the right team. We have already seen the state and the routing function. Now, let's assemble the full graph step by step.

First, we define the state and the two nodes as below:

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message: str
    reply: str

def billing(state: State):
    return {"reply": "This is the billing team. We will help you with your payment."}

def technical(state: State):
    return {"reply": "This is the technical team. We will help you fix the issue."}

```

Here, we have defined our `State` with `message` and `reply`. We have created two nodes. The `billing` node writes a reply from the billing team. The `technical` node writes a reply from the technical team. We have also imported `StateGraph`, which is the builder we use to create our graph, along with `START` and `END`, which are the start and stop points.

Then, we bring back our routing function as below:

```python
def route_message(state: State):
    if "bill" in state["message"]:
        return "billing"
    return "technical"

```

Here, we have the same `route_message` function we saw earlier. It reads the `message` from the state. If the message contains the word `bill`, it returns `billing`. Otherwise, it returns `technical`. This is the function that decides which node runs next.

After that, we build the graph and connect the parts as below:

```python
builder = StateGraph(State)
builder.add_node("billing", billing)
builder.add_node("technical", technical)

builder.add_conditional_edges(START, route_message)
builder.add_edge("billing", END)
builder.add_edge("technical", END)

graph = builder.compile()

```

Here, we can see the full wiring. We create a `StateGraph` and give it our `State`. We add our two nodes with `add_node`. Then we add a conditional edge from `START` using `add_conditional_edges`, which calls `route_message` to pick the next node. We add an edge from `billing` to `END` and from `technical` to `END`, so the graph stops after it replies. Finally, we call `compile`, which turns our description into a runnable graph.

After that, we run the graph with a billing message as below:

```python
result = graph.invoke({"message": "I have a question about my bill"})
print(result["reply"])

```

Here, we have called `invoke` and passed the starting state with a `message` about a bill. The graph reads the message, the conditional edge sends it to the `billing` node, the node writes the reply, and we get the final state. We print the `reply` from it.

This will print the following:

```
This is the billing team. We will help you with your payment.

```

It works perfectly. The message had the word `bill`, so the graph picked the billing path on its own.

Now, let's run the graph with a different message as below:

```python
result = graph.invoke({"message": "My app is not working"})
print(result["reply"])

```

This will print the following:

```
This is the technical team. We will help you fix the issue.

```

This time the message did not have the word `bill`, so the conditional edge sent the graph to the `technical` node. This is the same billing example we have been building, now running from start to end.

We can picture the full flow as below:

```text
                              +------------+
                       bill   |  billing   | ---> END
                     -------> |    node    |
   +-------+        /         +------------+
   | START | ----->+
   +-------+        \         +------------+
                     -------> | technical  | ---> END
                    not bill  |    node    |
                              +------------+

```

Here, we can see that the graph begins at `START`. The conditional edge reads the `message` from the state and picks one path. If the message contains `bill`, the graph goes to the `billing` node. Otherwise, it goes to the `technical` node. The chosen node writes the `reply` into the state, and the graph moves to `END`. We get the final state back with both the `message` and the `reply` filled in.

To learn how to build agent applications like this - AI Agents, Agent Architecture, and Orchestration and Routing - check out our AI and Machine Learning Program at Outcome School, where we build an AI Coding Agent from scratch.

## Tools and who calls them

Now, it's time to learn about a very important concept called tools. This is also the part where we often get confused, so we must read it carefully.

First, let's remember what an LLM really is. An LLM only takes text and gives back text. It cannot search the web on its own. It cannot read our database. It cannot send an email. It can only produce words.

But real apps need real actions. We may need to search the web, look up an order, or check the weather. So, here comes the tool into the picture.

A tool is a normal function that does a real action, like searching the web or reading a database.

Now, here is the catch, and we must be very clear about it.

The LLM does not call the tool. The LLM only recommends which tool to use.

In simple words, the LLM reads the user's request and says, "We should use the search tool, and the input should be weather in Delhi." That is all the LLM does. It returns this recommendation as text. It does not run anything.

We can picture the LLM's recommendation as below:

```text
tool:  search
input: weather in Delhi

```

Here, we can see that the LLM only produced a small piece of text. It named the tool and the input. It did not run the search. It just gave a recommendation.

So, now the question is, who actually calls the tool? The answer is the agent.

In simple words, the agent is the code that runs around the LLM. Here, LangGraph is that agent. It reads the recommendation from the LLM, calls the real tool function, gets the result, and then gives the result back to the LLM.

Let's understand this with a simple analogy. Think of the LLM as a doctor and the agent as a pharmacist. The doctor looks at the patient and writes a prescription. The doctor only recommends the medicine. The doctor does not hand over the medicine. The pharmacist reads the prescription and actually gives the medicine. In the same way, the LLM only recommends the tool, and the agent actually calls it.

Let's see this flow step by step.

- Step 1: The user asks a question.
- Step 2: The LLM reads the question and recommends a tool with some input. It does not run the tool.
- Step 3: The agent reads this recommendation and actually calls the tool.
- Step 4: The tool runs and returns a result.
- Step 5: The agent gives the result back to the LLM.
- Step 6: The LLM reads the result and writes the final answer.

We can picture this flow as below:

```text
   user question
        |
        v
   +-----------+
   | LLM node  |   recommends a tool (but does not call it)
   +-----------+
        |
        v
   +-----------+
   |   agent   |   reads the recommendation
   +-----------+
        |
        v
   +-----------+
   | tool node |   actually calls the tool, gets the result
   +-----------+
        |
        v   the result goes back to the LLM node
   +-----------+
   | LLM node  |   reads the result and writes the final answer
   +-----------+

```

Here, we can see the clear split of work. The LLM node only thinks and recommends. The tool node only does the real action. The agent connects the two. The LLM recommends, and the agent calls. This is the key idea, and we must always keep it in mind.

In LangGraph, this fits perfectly with what we have already learned. The LLM is one node. The tool is another node. After the LLM node, a conditional edge checks one simple thing: did the LLM recommend a tool? If yes, the graph goes to the tool node, runs the tool, and loops back to the LLM node with the result. If no, the graph goes to `END` with the final answer.

This is why LangGraph is so useful for building agents. It gives us a clean way to run this loop of recommend, call, and respond.

This pattern, where the LLM names a tool and its input and the agent runs it, is called function calling. We have a detailed blog on how function calling works in LLMs that covers this end to end.

## Memory and persistence

Now, let's understand a very useful feature called memory.

Memory in LangGraph means the graph can remember the state across many runs.

In simple words, without memory, the graph forgets everything once it finishes. With memory, the graph can save the state and continue later from the same place.

Let's say we are building a chat assistant. The user says "My name is Amit". Later, the user asks "What is my name?". For the second question to work, the assistant must remember the first message. This is where memory comes in.

In LangGraph, we add memory using something called a checkpointer. A checkpointer is a small helper that saves the state after each step. When the user comes back, the graph loads the saved state and continues.

This way, our app can hold long conversations and pick up exactly where it left off. The state is no longer lost. It is persisted, which means it is stored safely.

## Human-in-the-loop

Now, it's time to learn about another powerful feature called human-in-the-loop.

Human-in-the-loop means the graph can pause and wait for a human to check or approve a step before moving ahead.

In simple words, sometimes we do not want the AI to act fully on its own. We want a person to review the work first.

Let's say our assistant wrote a reply to a customer, but the reply involves a refund. We do not want to send a refund automatically. So, the graph pauses, a human reviews the reply, and only after approval does the graph continue.

Because LangGraph saves the state with a checkpointer, it can stop at any node and wait. The human checks the state, makes a decision, and the graph resumes from that exact point. This gives us control and safety in important workflows.

## When to use LangGraph

Now, we have understood how LangGraph works. Let's understand when we must use it.

Let me tabulate the differences between a simple LLM call and LangGraph for your better understanding so that you can decide which one to use based on your use case.

| Situation | Simple LLM call | LangGraph |
| --- | --- | --- |
| One question, one answer | Best fit | Not needed |
| Many steps in order | Hard to manage | Easy to manage |
| Decisions and branching | Messy with `if` and `else` | Clean with conditional edges |
| Looping back to retry | Difficult | Built-in support |
| Calling tools or actions | LLM can only recommend | Agent calls the tool |
| Remembering past runs | Manual work | Checkpointer handles it |
| Pausing for a human | Very hard | Human-in-the-loop support |

Here, we can see the pattern clearly. For a single question and a single answer, a plain LLM call is enough. But when our app has many steps, decisions, loops, tools, memory, and human checks, LangGraph makes our life easier.

So, now we know where we can use LangGraph.

Let's quickly recall the full flow with a simple analogy table. This maps each LangGraph piece to a real-world role so that it stays in our memory.

| LangGraph piece | Real-world role |
| --- | --- |
| State | The shared notebook everyone writes in |
| Node | A worker doing one task |
| Edge | The path from one worker to the next |
| Conditional edge | A fork on the road |
| Tool | A real action like searching the web |
| LLM | The advisor who only recommends the tool |
| Agent | The worker who actually calls the tool |
| Checkpointer | The save button |
| Human-in-the-loop | The manager who approves the work |

Here, we can notice how each technical piece maps to something we already know from daily life. The state is the shared notebook. The nodes are workers. The edges are the paths. The conditional edge is a fork. The tool is a real action. The LLM is the advisor who only recommends the tool, and the agent is the worker who actually calls it. The checkpointer is the save button. The human-in-the-loop is the manager who approves.

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
