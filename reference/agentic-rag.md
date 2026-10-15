> Source: https://outcomeschool.com/blog/agentic-rag

# Agentic RAG
URL: https://outcomeschool.com/blog/agentic-rag
Published: 2026-05-01

Agentic RAG

# Agentic RAG

Authors
: - Name
: Amit Shekhar
Published on
: May 1, 2026

In this blog, we will learn about Agentic RAG - what it is, why standard RAG falls short, the agentic RAG loop, the three building blocks, the common patterns, when to use it, and the limitations to keep in mind.

A hard question often needs more than one search. Some of those searches need different sources. Some depend on what the previous search found. Standard RAG cannot do any of this. Agentic RAG can.

Agentic RAG = Agentic + RAG

We will cover the following in this blog:

- The Big Picture
- A Quick Recap of RAG
- A Quick Recap of AI Agent
- Why Standard RAG Falls Short
- What is Agentic RAG
- The Agentic RAG Loop
- The Three Building Blocks
- A Walkthrough with a Real Example
- Common Patterns of Agentic RAG
- Standard RAG vs Agentic RAG
- When to Use Agentic RAG
- Limitations of Agentic RAG
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

The best way to think about this is with a real-world analogy. Suppose we want to find an answer in a big library.

Standard RAG is like a librarian who fetches one book. We hand over the question. The librarian picks the book that matches the words best, gives it to us, and the LLM reads it to write the answer. One shot. Done.

Agentic RAG is like a researcher. The researcher reads the question, thinks about where to look, picks a section, reads it, and decides whether the answer is in there. If not, the researcher goes back, picks a different shelf, runs a follow-up search, and keeps going until the answer is found.

The librarian flow is fast but cannot adapt to the question. The researcher flow is slower but can handle questions that need many steps.

This is exactly the difference between Standard RAG and Agentic RAG. Agentic RAG turns the one-shot retrieval into a loop driven by an AI Agent that keeps working until it can answer well.

In simple words:

Agentic RAG = RAG + an AI Agent that controls the retrieval steps.

## A Quick Recap of RAG

Before jumping into Agentic RAG, we must quickly recall what RAG is.

RAG stands for Retrieval-Augmented Generation. The flow is simple:

- The user asks a question.
- We convert the question into an embedding.
- We search a vector database and pull the top relevant chunks.
- We pass those chunks plus the question to the LLM.
- The LLM generates the final answer.

One clever twist on the second step is HyDE, where instead of embedding the raw question, we first ask the model to write a hypothetical answer and search with that - a trick that often retrieves better chunks.

We can see this flow as below:

```
User Question
     |
     v
+------------------+
|     Embed        |
|   the question   |
+------------------+
     |
     v
+------------------+
|  Vector Search   |
|  (top-k chunks)  |
+------------------+
     |
     v
+------------------+
|       LLM        |
|  (generate)      |
+------------------+
     |
     v
  Final Answer

```

Here, we can see that the flow is a straight line. There are no decisions in the middle. Retrieve once. Generate once. Return. This is the librarian flow.

In a production RAG system, a Reranker often sits between retrieval and the LLM to reorder those top chunks by true relevance. We have a detailed blog on how a Reranker works that covers this step end to end.

## A Quick Recap of AI Agent

Now, let's recall what an AI Agent is.

An AI Agent is a system that uses an LLM as its brain and runs in a loop. The LLM plans the next step, recommends a tool, observes the result, and decides what to do next. It is not a one-shot prompt. It is a thinking loop with access to tools. This is the researcher in our analogy.

## Why Standard RAG Falls Short

Standard RAG works for simple questions. But the moment the question gets harder, it breaks down. The reason is simple. Our librarian only knows how to match words. The librarian cannot think, cannot ask follow-up questions, and cannot decide where to look.

Let's see the problems this causes.

Problem 1: Multi-hop questions.

Suppose the user asks:

> "What was the Q4 revenue of the company that acquired Acme in 2023?"

To answer this, we first need to find out which company acquired Acme in 2023. Only after that, we can retrieve the Q4 revenue of that company. One single retrieval cannot do this. The librarian sees the long question and tries to find one matching book. There is no such book.

Problem 2: Ambiguous queries.

The user asks: "What about the new policy?"

The retrieval system has no idea which policy. Standard RAG will pull random chunks and the answer will be wrong. The librarian does not stop to ask "which policy?". The librarian just matches words and hands over a book.

Problem 3: Multiple data sources.

Some questions need a SQL database. Some need a vector store. Some need a live web search. Standard RAG hits one source. It cannot pick the right one. Our librarian only knows one library. If the answer lives in a database, on the web, or in a graph of relationships, the librarian cannot reach it.

Problem 4: Bad retrieval quality.

Sometimes the top retrieved chunks are not relevant. Standard RAG does not know this. It just passes whatever it found to the LLM. The LLM then makes up the answer. The librarian hands over whatever matched the words best, without checking if the book actually has the answer.

Do you see the problem? Standard RAG is rigid. It cannot adapt.

So, here comes Agentic RAG to the rescue. We replace the librarian with a researcher.

## What is Agentic RAG

Agentic RAG is a system where an AI Agent drives the retrieval process. Instead of one fixed retrieve-then-generate step, the agent decides every step in a loop.

The agent decides:

- Does this question even need retrieval?
- Which tool or data source should we use?
- What should the search query look like?
- Are the retrieved chunks good enough to answer?
- Should we retrieve again with a better query?
- Should we combine results from multiple sources?
- When can we stop and write the final answer?

This is a big shift. The retrieval is no longer a fixed pipeline. It is a decision made by the agent at every step. The librarian has been replaced by the researcher.

## The Agentic RAG Loop

Let's see the loop.

```
User Question
     |
     v
+------------------+
|    AI Agent      |
|   (the LLM)      |
+------------------+
     |
     | thinks: "Do I need to retrieve?
     |          Which tool? What query?"
     v
+------------------+
|  Retrieval Tool  |
|  (vector / SQL / |
|   web / graph)   |
+------------------+
     |
     | returns chunks
     v
+------------------+
|    AI Agent      |
|   evaluates:     |
|  "Good enough?"  |
+------------------+
     |
     +--- No  --> retrieve again with a new query
     |
     +--- Yes --> generate the final answer

```

Here, we can see that the agent is in control. It loops until it has enough information.

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

## The Three Building Blocks

Agentic RAG has three building blocks. Let's decode each one.

1. The Agent (The Brain)

This is the researcher's mind. It is an LLM that does the thinking. It reads the question, plans the next step, recommends the tool, and evaluates the result.

2. The Tools (The Hands)

These are the resources our researcher can reach for. A real researcher uses different sources for different questions. The agent has the same options:

- Vector search: for finding text by meaning over documents
- Keyword search: for exact term matches
- SQL query: for structured data in a database
- Web search: for fresh information on the internet
- Knowledge graph query: for relationships between entities

The agent recommends the right tool based on the question, just like a researcher walks to the right shelf.

3. The Loop (The Workflow)

This is the back-and-forth between the researcher's mind and the resources. The runtime that ties the agent and the tools together. It calls the agent, runs the tool the agent recommended, feeds the result back to the agent, and repeats.

Across the loop, the runtime keeps track of every past step - the actions the agent took and the results it saw. This running record is called the scratchpad or agent memory. The agent reads this record on every step so it knows what it has already tried and what it has already learned.

Note: The LLM inside the agent does not call the tool itself. The LLM only outputs text - the name of the tool to use and the arguments. The runtime around the LLM is what actually calls the tool and feeds the result back. This distinction is important.

To build an AI Tutor from scratch - learning RAG, Agentic RAG, agent memory, and vector databases - check out our AI and Machine Learning Program at Outcome School.

## A Walkthrough with a Real Example

The best way to learn this is by taking an example.

Let's say the user asks:

> "What was the Q4 revenue of the company that acquired Acme in 2023?"

Here is how Agentic RAG handles it. Watch the agent act like a researcher.

Step 1: The agent reads the question. It thinks: "This is a multi-hop question. I first need to find who acquired Acme in 2023."

Step 2: The agent recommends the web search tool with the query: `company that acquired Acme in 2023`.

Step 3: The web search returns: "Globex acquired Acme in 2023."

Step 4: The agent updates its plan. Now it needs Globex's Q4 2023 revenue.

Step 5: The agent recommends the vector search tool over the internal financial reports with the query: `Globex Q4 2023 revenue`.

Step 6: The vector search returns chunks from Globex's Q4 financial report.

Step 7: The agent evaluates the chunks: "Yes, these chunks contain the revenue number. I have enough."

Step 8: The agent generates the final answer using the gathered information.

Note: In practice, the web search returns several noisy snippets. The agent reads them and pulls out the answer. We have shown a clean answer above just for the sake of understanding.

Sometimes, the agent combines results from two sources in a single step. For example, it pulls a definition from a vector store and fresh news from a web search before answering.

Standard RAG could not do this. It would have made one retrieval with the original question and failed. Agentic RAG broke the question into two steps, used two different tools, and answered correctly. The researcher did the job that the librarian could not.

Problem solved. This is the power of Agentic RAG.

## Common Patterns of Agentic RAG

Agentic RAG is a general idea. Over time, a few specific patterns have become popular. Let's quickly look at three of them.

ReAct-style RAG. The agent follows a "think, act, observe" loop. It thinks about what to do, takes an action like a retrieval, observes the result, and repeats. Our walkthrough above is a ReAct-style flow. We have a detailed blog on ReAct Agent that explains this pattern in depth.

Self-RAG. The agent grades its own retrievals on two things - relevance (are the chunks about the question?) and support (do the chunks actually back up the answer?). If not, the agent skips or trusts them less before generating. Self-RAG is about quality control on what the agent fetches.

Corrective RAG (also called CRAG). The agent recommends a fallback source when the main retrieval is bad. For example, if the vector search returns nothing useful, the agent falls back to a live web search. CRAG is about robustness when the main source fails.

All three share the same core idea. The agent decides what happens at every step. They differ in what they focus on - reasoning style, quality control, or robustness.

If we want to go deep into the ReAct pattern, and end-to-end evaluation of agents, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Standard RAG vs Agentic RAG

Let me tabulate the differences between Standard RAG and Agentic RAG for your better understanding so that you can decide which one to use based on your use case.

| Aspect | Standard RAG | Agentic RAG |
| --- | --- | --- |
| Flow | Fixed pipeline | Dynamic loop |
| Number of retrievals | One | Many, as needed |
| Tools used | One (usually vector search) | Many (vector, SQL, web, and etc.) |
| Query rewriting | No | Yes |
| Quality check on retrieved chunks | No | Yes |
| Multi-hop questions | Cannot handle | Can handle |
| Latency | Low | Higher |
| Cost | Low | Higher |
| Complexity to build | Simple | More complex |

## When to Use Agentic RAG

Use Agentic RAG when:

- The user asks multi-hop questions that need information from more than one search.
- The data lives in multiple sources (vector DB, SQL, web, files).
- The questions are ambiguous and need rewriting before retrieval.
- The quality of retrieval matters more than latency, like in research, legal, or medical use cases.
- The system needs to decide if retrieval is even needed. For greetings or small talk, no retrieval is needed.

Use Standard RAG when:

- The questions are simple and direct.
- The data lives in one place.
- Latency and cost matter more than depth.

## Limitations of Agentic RAG

A researcher takes more time and costs more than a librarian. The same is true for Agentic RAG. It is powerful, but it has trade-offs.

- Higher latency. Each loop step is one or more LLM calls. The user waits longer.
- Higher cost. Each loop step is one LLM call, and the tool results are fed back into the next prompt. More steps mean more tokens, which means a higher API bill.
- Harder to debug. The agent's decisions are not fixed. The same question can take different paths on different runs.
- Can loop too long. Without a stopping rule, the agent can keep retrying and never stop. Common stopping rules are: the LLM signals it is done, the agent's confidence in the answer is high enough, or a max step count is hit.
- More moving parts. We need to design tools, prompts, evaluation steps, and stopping rules. A simple system becomes a complex one.

We must keep these trade-offs in mind while designing the system.

## Quick Summary

Let's recap what we have learned:

- Standard RAG is a fixed pipeline: retrieve once, generate once.
- Agentic RAG is a loop where an AI Agent drives every step of retrieval.
- The agent decides when to retrieve, what to retrieve, from where, and whether to retrieve again.
- It has three parts: the agent, the tools, and the loop, with a scratchpad that tracks the past steps.
- Common patterns are ReAct-style RAG, Self-RAG, and Corrective RAG (CRAG).
- It shines on multi-hop questions, multiple data sources, and ambiguous queries.
- The trade-offs are higher latency, higher cost, and more complexity.

Standard RAG is the librarian who fetches one book. Agentic RAG is the researcher who keeps digging until the answer is found. We use Agentic RAG when Standard RAG is not enough.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:
