> Source: https://outcomeschool.com/blog/how-do-query-rewriting-and-multi-query-retrieval-work

# How do Query Rewriting and Multi-Query Retrieval work?
URL: https://outcomeschool.com/blog/how-do-query-rewriting-and-multi-query-retrieval-work
Published: 2026-10-08
Author: Amit Shekhar

How do Query Rewriting and Multi-Query Retrieval work?

# How do Query Rewriting and Multi-Query Retrieval work?

Authors
: - Name
: Amit Shekhar
Published on
: October 8, 2026

Query Rewriting and Multi-Query Retrieval are two ways of improving the search step of an AI system. Query Rewriting uses an LLM to turn the user's messy question into one clear search query, and Multi-Query Retrieval uses an LLM to turn the question into several different search queries, searches with all of them, and merges the results.

In this blog, we will learn about how Query Rewriting and Multi-Query Retrieval work. We will also see why the user's raw question is often a bad search query, how Query Rewriting fixes vague, follow-up, and badly worded questions, how Multi-Query Retrieval searches from many angles, how the results from many searches are merged using Reciprocal Rank Fusion, how they differ from each other, and when to use which one.

We will cover the following:

- The problem: the user's question is not a good search query
- What is Query Rewriting?
- How does Query Rewriting work?
- Types of Query Rewriting
- Query Rewriting in code
- The problem that Query Rewriting does not solve
- What is Multi-Query Retrieval?
- How does Multi-Query Retrieval work?
- How do we merge the results? Reciprocal Rank Fusion
- Multi-Query Retrieval in code
- Query Rewriting vs Multi-Query Retrieval
- Where they work well and where they fail

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The problem: the user's question is not a good search query

Query Rewriting and Multi-Query Retrieval are used in the retrieval step of RAG (Retrieval-Augmented Generation), where we search our documents, pick the pieces of text called chunks that are most related to the question, and give them to an LLM before it answers.

The flow looks like below:

```text
User question -> Retriever -> Top chunks -> LLM -> Answer

```

If retrieval brings the wrong chunks, the LLM often gives a wrong answer.

And retrieval depends completely on the text we search with. That text is called the search query.

In a simple RAG system, we search with the user's question exactly as they typed it. But real users do not type perfect search queries.

Let's see a few real situations:

- Follow-up questions: The user first asks, "What is the refund policy of the Pro plan?". Then they ask, "And what about the Basic one?". If we search with "And what about the Basic one?", the retriever has no idea that we are talking about refunds.
- Vague questions: "My thing is not working after the update." Which thing? Which update?
- Different words: The user asks, "How do I get my money back?", but our documents say "refund process". A keyword search does not match them.
- Extra noise: "Hi, hope you are well, quick question, my manager asked me, how many leaves do we get in a year?". Most of these words are not useful for search.
- Many questions in one: "Compare the battery life and price of phone A and phone B." This needs information from several different places.

In all these cases, the retriever brings poor chunks, and the LLM gives a poor answer.

So, here comes Query Rewriting to the rescue.

## What is Query Rewriting?

Query Rewriting is a step where an LLM rewrites the user's question into a clear, complete, and search-friendly query before we search.

It is like going to a big library and asking the librarian, "I want that book about the boy wizard". The librarian does not search for "boy wizard". The librarian searches for "Harry Potter". The librarian rewrote our query.

The flow now looks like below:

```text
User question -> LLM rewrites -> Clear query -> Retriever -> Top chunks -> LLM -> Answer

```

The answer is still written using the user's original question. Only the search uses the rewritten query.

## How does Query Rewriting work?

The best way to learn this is by taking an example.

Step 1: The user is chatting with a support bot.

```text
User: What is the refund policy of the Pro plan?
Bot:  You can get a full refund within 30 days.
User: And what about the Basic one?

```

Step 2: Before searching, we send the chat history and the latest question to an LLM with an instruction like below:

```text
Given the conversation and the latest question, rewrite the latest
question as a standalone search query that contains all the needed
details. Return only the query.

```

Step 3: The LLM returns:

```text
Refund policy of the Basic plan

```

Step 4: We search with "Refund policy of the Basic plan". Now, the retriever finds the right chunk about Basic plan refunds.

Step 5: We give that chunk and the user's question to the LLM, and it answers correctly.

## Types of Query Rewriting

Query Rewriting is one idea, but it is used in a few different ways, depending upon our use case:

- Standalone rewriting: Turns a follow-up question into a complete question, using the chat history. Like the refund example above. This is the most common type in chat applications.
- Clarifying and cleaning: Removes noise, fixes spelling, and keeps only the important words. "Hi, quick question, how many leaves do we get in a year?" becomes "Annual leave policy number of days".
- Expanding: Adds words that the documents are likely to use. "How do I get my money back?" becomes "refund process, return money, get refund".
- Step-back rewriting: Turns a very specific question into a more general one, so that we find the background information. "Why did my order #4521 get delayed in Mumbai?" becomes "Reasons for order delivery delays".

All of them follow the same pattern: an LLM changes the query, and then we search. A close cousin of these is HyDE, where the LLM writes a hypothetical answer instead of a query, and we search with that answer.

## Query Rewriting in code

Now, let's see the code for a simple Query Rewriting step. Here, `call_llm` sends a prompt to an LLM and returns its text, and `retriever.search` searches our chunks. We are hiding their details for the sake of understanding.

```python
def rewrite_query(chat_history, question):
    prompt = f"""Given the conversation and the latest question, rewrite the
latest question as a standalone search query. Return only the query.

Conversation:
{chat_history}

Latest question: {question}"""
    return call_llm(prompt).strip()

def answer(chat_history, question):
    search_query = rewrite_query(chat_history, question)
    chunks = retriever.search(search_query, top_k=5)
    return call_llm(f"Context:\n{chunks}\n\nQuestion: {question}\nAnswer:")

```

Here, we have:

- `rewrite_query` builds a prompt with the chat history and the latest question, and asks the LLM for one clean search query.
- In `answer`, we first rewrite the question, then search with the rewritten query.
- Finally, we give the found chunks and the original question to the LLM to write the answer.

Here, we can notice that the user never sees the rewritten query. It is used only for searching.

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

## The problem that Query Rewriting does not solve

Query Rewriting gives us one better query. But one query, however good, looks at the question from only one angle.

Let's say the user asks, "Is the new phone good for gaming?". The useful information can be in many places:

- A chunk about the processor.
- A chunk about the screen refresh rate.
- A chunk about heating and battery during long use.

A single query like "new phone gaming performance" can find the first chunk but miss the others, because they use very different words.

Also, if the LLM rewrites the query in a slightly wrong way, we have no backup. One bad rewrite means bad retrieval.

So, the question is: what if we search from many angles at the same time?

Here comes Multi-Query Retrieval into the picture.

## What is Multi-Query Retrieval?

Multi-Query Retrieval is a method where an LLM creates several different versions of the user's question, we search with each version separately, and then we merge all the results into one list.

It is like looking for a lost key at home. If we only look in the bedroom, we can miss it. If three family members look in the bedroom, the kitchen, and the car at the same time, the chance of finding the key is much higher.

## How does Multi-Query Retrieval work?

Let's take the same gaming example.

Step 1: The user asks, "Is the new phone good for gaming?".

Step 2: We ask the LLM to create, let say, 3 different search queries for the same question:

```text
Query 1: new phone processor and graphics performance
Query 2: new phone display refresh rate and touch response
Query 3: new phone heating and battery life during heavy use

```

Step 3: We search with each query separately. Each search returns its own top chunks.

```text
Query 1 -> [processor chunk, benchmark chunk, ...]
Query 2 -> [display chunk, touch chunk, ...]
Query 3 -> [battery chunk, heating chunk, ...]

```

Step 4: We merge all the results into one list and remove the duplicates, because the same chunk can come from more than one query.

Step 5: We give the merged chunks and the original question to the LLM, and it writes a complete answer covering speed, display, and battery.

The flow looks like below:

```text
                     /--> Query 1 -> Retriever -> results 1 \
User question -> LLM ---> Query 2 -> Retriever -> results 2 --> Merge -> LLM -> Answer
                     \--> Query 3 -> Retriever -> results 3 /

```

Note: Many systems also keep the user's original question as one of the queries, so that we never lose what a plain search would have found.

Similarly, Multi-Query Retrieval solves the "many questions in one" problem that we saw earlier. For "Compare the battery life and price of phone A and phone B", the LLM can split it into smaller questions like "phone A battery life", "phone A price", "phone B battery life", and "phone B price". Splitting a big question into smaller questions like this is called query decomposition.

## How do we merge the results? Reciprocal Rank Fusion

Now, the next big question is: how do we merge the lists?

The simplest way is to take all the chunks from all the lists, remove the duplicates, and keep them. This is called taking the union. It works, but it does not tell us which chunks are the most important.

A better way is Reciprocal Rank Fusion, or RRF. When Multi-Query Retrieval is combined with RRF, it is often called RAG-Fusion.

RRF gives each chunk a score based on its position in each list, and adds these scores across all the lists.

The formula is as below:

RRF score of a chunk = sum over all lists of 1 / (k + rank)

Here, `rank` is the position of the chunk in that list (1 for the top), and `k` is a constant, commonly 60.

Here, "reciprocal" just means "1 divided by". A chunk at the top of a list gets a bigger score than a chunk at the bottom. A chunk that appears in many lists collects score from each of them.

Let's see an example with 3 queries and their top 3 chunks:

```text
Query 1 -> [D2, D5, D1]
Query 2 -> [D5, D3, D2]
Query 3 -> [D5, D2, D4]

```

Now, we calculate with `k = 60`:

```text
D5: 1/(60+2) + 1/(60+1) + 1/(60+1) = 0.0161 + 0.0164 + 0.0164 = 0.0489
D2: 1/(60+1) + 1/(60+3) + 1/(60+2) = 0.0164 + 0.0159 + 0.0161 = 0.0484
D3: 1/(60+2)                        = 0.0161
D1: 1/(60+3)                        = 0.0159
D4: 1/(60+3)                        = 0.0159

```

The final order is D5, D2, D3, and then D1 and D4 with the same score.

Here, we can see that D5 wins because it was near the top of all three lists. D2 is a close second. D3, D1, and D4 appeared in only one list each, so they come later.

RRF only needs the positions, not the raw scores. So, it works even when the lists come from different kinds of search. This is also why RRF is the most common way to merge keyword search and semantic search results in Hybrid Search.

## Multi-Query Retrieval in code

Now, let's see the code for Multi-Query Retrieval with RRF. We can write the code as below:

```python
def generate_queries(question, n=3):
    prompt = f"""Write {n} different search queries for the question below.
Each query must look at the question from a different angle.
Return one query per line.

Question: {question}"""
    lines = call_llm(prompt).strip().split("\n")
    return [question] + [line.strip() for line in lines if line.strip()]

def rrf_merge(result_lists, k=60):
    scores = {}
    for results in result_lists:
        for rank, chunk_id in enumerate(results, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)

def multi_query_search(question, top_k=5):
    queries = generate_queries(question)
    result_lists = [retriever.search(q, top_k=top_k) for q in queries]
    return rrf_merge(result_lists)[:top_k]

```

Here, we have:

- `generate_queries` asks the LLM for `n` different queries, one per line, and also keeps the original question in the list.
- `retriever.search` returns a list of chunk ids for each query, best first.
- `rrf_merge` goes through every list, gives each chunk `1 / (k + rank)`, and adds the scores. Then, it sorts the chunks by the total score. Duplicates are handled automatically, because the same chunk id simply collects more score.
- `multi_query_search` connects everything and returns the best `top_k` chunks.

## Query Rewriting vs Multi-Query Retrieval

Let me tabulate the differences between Query Rewriting and Multi-Query Retrieval for your better understanding.

| Point | Query Rewriting | Multi-Query Retrieval |
| --- | --- | --- |
| Output of the LLM step | One better query | Several different queries |
| Number of searches | One | One per query |
| Main strength | Fixes follow-ups, vague, and noisy questions | Finds information spread across different places |
| Safety against a bad rewrite | No backup | Other queries act as backup |
| Merging step needed | No | Yes, union or RRF |
| Speed and cost | Fast, one extra LLM call | Slower, one extra LLM call plus many searches |
| Best for | Chat applications with follow-up questions | Broad or multi-part questions |

Note: We can use both together. First, rewrite the follow-up question into a standalone question. Then, create multiple queries from that clean question.

In Agentic RAG, an agent goes one step further and decides on its own when to rewrite the query and when to search again.

## Where they work well and where they fail

Advantages:

- Both improve retrieval without changing our documents or our retriever.
- Query Rewriting makes follow-up questions in a chat work correctly.
- Multi-Query Retrieval finds more of the useful chunks, which is called better recall.
- Both work with any retriever: keyword search, vector search, or both.

- Both add an extra LLM call before search, which adds time and cost.
- The LLM can change the meaning while rewriting. For example, it can drop an important detail like a version number. We must test our rewriting prompt carefully.
- Multi-Query Retrieval can bring in chunks that are only loosely related, which adds noise to the prompt. A reranker after the merge step can reorder the chunks by true relevance, so that only the best ones reach the LLM.
- For simple, clear questions, they add cost without much benefit.

Query Rewriting and Multi-Query Retrieval improve the question side of the search. We can also improve the chunk side by adding a short note to every chunk about where it comes from in the document. We have a detailed blog on how Contextual Retrieval works that explains this end to end.

Now, we must have understood how Query Rewriting and Multi-Query Retrieval work, how they differ, and when to use which one.

### Does the user see the rewritten query?

No. The user never sees the rewritten query. It is used only for searching. The final answer is still written using the user's original question, together with the chunks that the rewritten query found.

### Can we use Query Rewriting and Multi-Query Retrieval together?

Yes. We can use both together. First, we rewrite the follow-up question into a standalone question using the chat history. Then, we create multiple queries from that clean question, search with each of them, and merge the results.

### Why keep the original question as one of the queries in Multi-Query Retrieval?

Many systems keep the user's original question as one of the queries so that we never lose what a plain search would have found. The other queries also act as a backup against one bad rewrite.

### What value of k is used in Reciprocal Rank Fusion?

The constant k is commonly set to 60. Each chunk gets 1 / (k + rank) from every list it appears in, and these scores are added. A chunk near the top of many lists collects the highest total score.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# How does Approximate Nearest Neighbor (ANN) search work?
URL: https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work
Published: 2026-06-29

How does Approximate Nearest Neighbor (ANN) search work?

# How does Approximate Nearest Neighbor (ANN) search work?

Authors
: - Name
: Amit Shekhar
Published on
: June 29, 2026

In this blog, we will learn about Approximate Nearest Neighbor (ANN) Search, the idea that lets apps find "similar" things in a huge collection in the blink of an eye. It powers search engines, recommendation systems, face matching, and the memory behind modern AI chatbots. We will also see why the naive approach fails, how trees, hashing, clustering, and graphs make the search fast, and where ANN search is used in the real world.

We will cover the following:

- What is Nearest Neighbor Search?
- How do we turn things into numbers (vectors)?
- How do we measure "closeness"?
- The naive approach and why it fails
- What is Approximate Nearest Neighbor (ANN) Search?
- The trade-off: speed vs accuracy
- Approach 1: Trees (KD-Tree)
- Approach 2: Hashing (LSH)
- Approach 3: Clustering (IVF)
- Approach 4: Graphs (HNSW)
- A simple code example
- Where ANN Search is used
- Picking the right method

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Nearest Neighbor Search?

Nearest Neighbor Search means finding the item in a collection that is the most similar to a given item.

A neighbor is something that lives close to us. The nearest neighbor is the one that lives closest of all.

Let's say we walk into a music app and play one song. The app then says, "Here are songs similar to this one." To do that, the app looked at its whole library and found the songs that are closest in style to the one we played. That is nearest neighbor search.

Here are some everyday examples of the same idea:

- We upload a photo, and the app finds similar-looking photos.
- We type a question, and a search engine finds the most relevant answers.
- We watch one video, and the app suggests the next similar video.

So, nearest neighbor search is simply "find me the most similar thing". Now, the question is: how does a computer measure how similar two things are? For that, we first need numbers.

[…672ln elided…]

ReAct Agent. The agent alternates between Thought, Action, and Observation at every step. The most common pattern.

Plan-and-Execute Agent. The agent first creates a complete plan, then executes each step one by one. Good for long tasks.

Reflection Agent. The agent writes a draft, critiques its own work, and revises. Good when quality matters more than speed.

Agentic RAG. The agent decides when and how to retrieve documents, then uses them to answer. Good for knowledge-heavy tasks.

Multi-Agent System. Several agents with different roles work together. One researches, another writes, another reviews.

Note: These are not mutually exclusive. A real system often combines patterns - for example, a ReAct agent that uses Agentic RAG for knowledge lookups, with a Reflection step at the end for quality.

To learn ReAct, Agentic RAG, Multi-Agent Systems, and the full agent architecture, check out our AI and Machine Learning Program at Outcome School.

## What AI Agents Can Do Today

Let's look at some real things AI Agents are doing right now. This is not theory - these are in production.

Coding agents. Read a repository, understand the code, make changes, run tests, and submit a pull request. Examples: Claude Code, Cursor, GitHub Copilot agent mode.

Research agents. Search the web, read papers, synthesize findings, and produce a structured report. Examples: OpenAI Deep Research, Perplexity, Gemini Deep Research.

Customer support agents. Read a ticket, look up the user's account, check order status, and reply with a fix - with handoff to a human when needed.

Browser agents. Open a browser, navigate websites, fill forms, and complete tasks like booking or purchasing. Examples: Claude Code (Computer Use is now in Claude Code), ChatGPT Agent.

Data analysis agents. Query databases, run calculations, create charts, and summarize the findings. Examples: ChatGPT data analysis, Claude's code execution. These agents also need to know what our tables actually mean, otherwise they guess, and OKF is an open standard for writing that knowledge down in files an agent can read. We have a detailed blog on What is OKF (Open Knowledge Format)? that explains this in depth.

Personal assistants. Manage calendar, read and draft emails, search files, and complete multi-step tasks on the user's behalf. Examples: Apple Intelligence, Google Gemini assistant.

Every one of these is the same five-part structure. Only the tools and instructions change. Once we understand the five parts, we understand all AI Agents.

## When to Use an AI Agent

Now, a natural question arises - when should we actually build an AI Agent, and when is a simpler tool the better choice?

Use an AI Agent when:

- The task needs more than one step to complete.
- The next step depends on the result of the current step.
- The task needs external information or real-world actions (not just knowledge from the model).
- The path is not fixed - the agent has to decide what to do as it goes.

Do not use an AI Agent when:

- A single LLM call can solve the task (like summarizing a paragraph).
- The task is a fixed pipeline with no branching - a regular script is simpler.
- Latency and cost matter more than flexibility, and the task is simple.
- We cannot tolerate the non-determinism that comes with LLM decisions.

The rule of thumb is simple: if the task needs decisions and actions that depend on each other, an AI Agent is the right tool. If not, stick with a plain LLM call or a script. Using an agent when a script would do is over-engineering.

## Common Failure Modes

AI Agents are powerful, but they fail in specific ways. Knowing these failures helps us build more reliable agents. Let's decode each one.

1. Infinite loops. The agent keeps calling the same tool and never produces a final answer.

How to fix: Set a hard limit on the number of steps.

2. Wrong tool selection. The agent picks the wrong tool for the job.

How to fix: Write very clear tool descriptions. Every word in the description matters.

3. Hallucinated actions. The LLM picks a tool that does not exist or passes invalid arguments.

How to fix: Use native tool-use support from the LLM, and validate inputs in the loop before running the tool. Return a clear error as an observation if the input is invalid so the agent can self-correct.

4. Context overflow. The conversation history grows too large and no longer fits in the model's context window.

How to fix: Summarize older steps or drop stale observations, and keep the goal at the start and the newest steps at the end so that nothing important gets lost in the middle.

5. Premature stopping. The agent gives up before finishing the task.

How to fix: Make the instructions clear about when the task is truly complete.

Very important: Production-grade AI Agents are mostly about handling these failure modes well. The happy path is easy. The edge cases are where the real engineering happens. We have a detailed blog on AI Agent Evaluation that explains how to systematically measure outcome, trajectory, and tool use for AI Agents.

Now, we have understood what an AI Agent is, how it works, and when to use one. Let's wrap up with a quick recap.

## Quick Summary

Let's recap what we have decoded:

- AI Agent = LLM + Instructions + Tools + Memory + Loop. The LLM is the decision-maker. The tools are the hands. The loop keeps it going until the goal is done.
- Not just a chatbot. An AI Agent talks AND acts. It takes real actions, not just produces text.
- Five core parts. LLM, Instructions, Tools, Memory, Loop. Remove any one, and it is no longer an AI Agent.
- End-to-end flow. The loop sends the prompt to the LLM -> if the LLM picks a tool, the loop runs it and feeds the result back -> if the LLM returns a final answer, the loop stops. Repeat until done.
- Types. ReAct, Plan-and-Execute, Reflection, Agentic RAG, and Multi-Agent Systems. Real systems often combine them.
- Use cases today. Coding, research, customer support, browsing, data analysis, personal assistance. Same five-part structure everywhere.
- When to use one. The task needs multiple steps, tool use, and adaptive decisions. Otherwise, stick with a plain LLM call or a script.
- Failure modes. Infinite loops, wrong tool selection, hallucinated actions, context overflow, premature stopping. Handling these is the real work.

AI Agents bring dynamic, goal-driven control flow into mainstream software - the program decides its own next step instead of following a fixed script. That is what makes them powerful, and what makes them hard. Every serious AI application going forward is moving in this direction.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# What is Harness Engineering?
URL: https://outcomeschool.com/blog/harness-engineering-in-ai
Published: 2026-04-02

What is Harness Engineering?

# What is Harness Engineering?

Authors
: - Name
: Amit Shekhar
Published on
: April 1, 2026

Harness Engineering is everything we do to build the control layer around an AI model, which manages its inputs, outputs, tools, memory, errors, and evaluation, so that the model becomes actually usable in production.

In this blog, we will learn about Harness Engineering in AI. We will understand what a harness is, why we need it, and how it is used in AI Agents and evaluation systems.

We will cover the following:

- What is a Harness in AI?
- Why do we need Harness Engineering?
- Components of an AI Harness
- Harness Engineering for AI Agents
- Harness Engineering for Evaluation
- Best Practices in Harness Engineering
- Putting It All Together

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a Harness in AI?

Let's break the term:

Harness Engineering = Harness + Engineering

Harness means a control layer that helps you effectively use and manage a system..

Engineering means building it in a systematic and reliable way.

So, Harness Engineering is everything you do to build that control layer around the AI model to make it actually usable in production.

In simple words, the AI model alone is not enough. We need a layer of code around it that manages inputs, outputs, tools, memory, errors, and evaluation. This layer is the harness.

Just for the sake of understanding, let's say we have a very powerful engine. The engine alone cannot drive us anywhere. We need a car body, steering, brakes, fuel system, and dashboard around it. Together, they make the engine useful. The car body and all the parts around the engine - that is the harness.

Similarly, an AI model like an LLM is the engine. The harness is everything around it that makes the model useful in a real application.

## Why Do We Need Harness Engineering?

An AI model by itself can only process the input we give and return the output. But in real-world applications, we need much more than that.

We want to use the model effectively so for that we need to:

- Use tools like search engines, databases, and APIs
- Remember past conversations
- Handle errors gracefully when something goes wrong
- Follow specific instructions and formats
- Evaluate for quality and correctness
- Deploy and monitor in production

Without a harness, the model is just a raw engine with no control. The harness gives us that control.

So, We need Harness Engineering for building this control layer around AI models.

Consider any AI-powered product we use today - a coding assistant, a chatbot, or an AI search engine. All of them have a harness around the model. The quality of the harness directly affects the quality of the product. A great model with a poor harness will give a poor experience. A good model with a great harness will give an excellent experience.

## Components of an AI Harness

Now, let's understand the key components that make up an AI harness.

Prompt Management

This is the component that manages what goes into the model. It handles system prompts, user messages, templates, and context. It makes sure the model gets the right instructions every time. This is the discipline known as Context Engineering. Procedures that are too long to keep in the prompt at all times can live outside it as Agent Skills, which the harness loads only when a task matches.

Tool Orchestration

Many AI applications need the model to get assistant from external tools. For example, a coding assistant needs to read files, run commands, or search the web. The harness manages which tools are available, how they are called, and how the results are passed back to the model.

Memory Management

In a conversation, the model needs to remember what was said earlier. The harness manages this memory. It decides what to keep, what to remove, and how to compress old messages when the conversation gets too long.

Error Handling

Things can go wrong. The model can generate invalid output. A tool call can fail. The API can return an error. The harness handles all these cases so the application does not crash.

Input and Output Processing

The harness processes user input before sending it to the model. It also processes the model output before showing it to the user. This includes parsing, formatting, validation, and filtering.

Guardrails

These are safety checks built into the harness. They make sure the model does not generate harmful content, does not leak sensitive information, and stays within the boundaries of what it is supposed to do.

This was all about the key components of an AI harness. Now, let's move to the next section.

## Harness Engineering for AI Agents

Now, let's understand how Harness Engineering is used for AI Agents.

An AI Agent is a system that uses tools, makes decisions, and takes multiple actions to complete complex tasks. It can read files, write code, search the internet, send messages, and more. The agent keeps working in a loop until the task is done.

The harness for an AI Agent is more complex because it needs to manage the entire agent loop. Designing that loop deliberately - the step budget, the observations, and the exit conditions - is Loop Engineering.

Here is how the agent harness works:

Step 1: The harness takes the user task and prepares the initial prompt with system instructions, available tools, and context.

Step 2: The harness sends this to the model and gets a response.

Step 3: The harness checks if the model recommends to use a tool. If yes, the harness executes the tool and sends the result back to the model.

Step 4: The harness repeats Steps 2 and 3 until the model says the task is complete.

Step 5: The harness presents the final result to the user.

This entire loop is managed by the harness. The model does the thinking, but the harness does the managing.

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

Here, we can see that without the harness, the agent cannot function. The harness is what turns a simple model into a powerful agent.

Claude Code is a real-world example of exactly this kind of agent harness. We have a detailed blog on how Claude Code works that walks through it step by step.

Note: The model itself does not execute any tool. It only decides which tool to call. The harness is the one that actually executes the tool and feeds the result back to the model.

Let's understand with a simple example:

```
User: "Find the weather in Delhi and send it to my email"

Harness Step 1: Prepare prompt with tools [weather_api, email_api]
Harness Step 2: Send to model
Model Response: "I will first check the weather. Call weather_api(city='Delhi')"
Harness Step 3: Execute weather_api -> Result: "32°C, Sunny"
Harness Step 4: Send result back to model
Model Response: "Now I will send the email. Call email_api(to='user@email.com', body='Weather in Delhi: 32°C, Sunny')"
Harness Step 5: Execute email_api -> Result: "Email sent"
Harness Step 6: Send result back to model
Model Response: "Done. I found the weather in Delhi (32°C, Sunny) and sent it to your email."
Harness Step 7: Present final response to user

```

Here, the model decided what to do, but the harness executed every action and managed the entire flow. This is how Harness Engineering works for AI Agents.

## Harness Engineering for Evaluation

Now, let's understand how Harness Engineering is used for evaluating AI models.

An evaluation harness is a framework that runs a set of tests on an AI model and measures how well it performs.

For example, suppose we want to test if our model can answer math questions correctly. The evaluation harness will:

- Load a dataset of math questions with known correct answers
- Send each question to the model one by one
- Compare the model answer with the correct answer
- Calculate an overall score

This is similar to how we test software. We write test cases, run them, and check the results. The evaluation harness does the same thing for AI models.

The evaluation harness helps us answer important questions like:

- How accurate is the model?
- Did the model get better or worse after we made changes?
- How does one model compare to another?
- Where does the model fail?

Without an evaluation harness, we would have to test the model manually, which is slow and not reliable. The evaluation harness makes our life easy.

For open-ended outputs like chatbot replies where a single correct answer does not exist, the evaluation harness often uses LLM as a Judge to score quality where rule-based metrics fall short.

For AI Agents specifically, evaluation goes beyond the final answer - we must score the trajectory, the tool calls, and the plan as well. We have a detailed blog on AI Agent Evaluation that covers this in depth.

This was all about Harness Engineering for Evaluation. Now, let's look at some best practices.

## Best Practices in Harness Engineering

Now, let's look at some best practices we must follow when building an AI harness.

Keep the harness modular. Each component like prompt management, tool orchestration, and memory management must be separate. This makes it easy to change one part without breaking others.

Log everything. Every input, output, tool call, and error must be logged. This helps us debug issues and understand what the model is doing.

Add guardrails from day one. Do not wait until something goes wrong. Build safety checks into the harness from the beginning.

Make tools reliable. If a tool fails, the harness must handle it gracefully. It can retry, use a fallback, or inform the model about the failure.

Test the harness, not just the model. The harness itself can have bugs. We must write tests for the harness code just like we test any other software.

Monitor in production. Once deployed, the harness must be monitored for latency, errors, cost, and quality. This helps us catch issues early. We have a detailed blog on AI Agent Observability that explains this in depth.

I will highly recommend following these practices from the start. It saves a lot of time in the long run.

## Putting It All Together

Now, let's visualize how all the components of a harness work together:

```
User Input
    ↓
[Input Processing] → Clean and format the input
    ↓
[Prompt Management] → Build the prompt with context and instructions
    ↓
[AI Model (LLM)] → Generate a response
    ↓
[Output Processing] → Parse and validate the output
    ↓
[Tool Orchestration] → Execute any tool calls if needed
    ↓
[Memory Management] → Store the conversation for future reference
    ↓
[Guardrails] → Check for safety and compliance
    ↓
Final Output to User

```

Here, we can see that the AI model is just one part of the system. The harness is everything else. And in many real-world applications, the harness code is much larger than the model integration code.

This is how all the components of a harness work together to make an AI model useful in the real world.

As I keep saying: the model is the brain, but the harness is what makes the brain useful.

### Does the AI model execute tools by itself?

No. The model itself does not execute any tool. It only decides which tool to call. The harness is the one that actually executes the tool and feeds the result back to the model, and it keeps repeating this loop until the model says the task is complete.

### Is a better model more important than a better harness?

Not always. The quality of the harness directly affects the quality of the product. A great model with a poor harness will give a poor experience, while a good model with a great harness will give an excellent experience. The model is the brain, but the harness is what makes the brain useful.

### Is Harness Engineering the same as Context Engineering?

No. Context Engineering is one part of Harness Engineering. Prompt management, which handles system prompts, user messages, templates, and context, is the discipline known as Context Engineering. The harness also covers tool orchestration, memory management, error handling, input and output processing, and guardrails.

### How does an evaluation harness score open-ended outputs?

For open-ended outputs like chatbot replies, where a single correct answer does not exist, the evaluation harness often uses LLM as a Judge to score quality. This is needed where rule-based metrics fall short. For AI Agents, evaluation also goes beyond the final answer to score the trajectory, the tool calls, and the plan.

### Do we need to test the harness code separately from the model?

Yes. The harness itself can have bugs, so we must write tests for the harness code just like we test any other software. In many real-world applications, the harness code is much larger than the model integration code.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

[Showing lines 1-435 and 1108-1483 of 1483; 672 middle lines (36.5KB) elided. Read artifact://56 for full output]
