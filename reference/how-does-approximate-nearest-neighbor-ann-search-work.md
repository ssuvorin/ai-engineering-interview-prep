> Source: https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work

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

### How do we turn things into numbers (vectors)?

A computer does not understand a song, a photo, or a sentence directly. It only understands numbers. So, the first step is to turn every item into a list of numbers.

This list of numbers is called a vector.

> Vector = a list of numbers that describes an item

In simple words, a vector is like a fingerprint made of numbers. Each item gets its own fingerprint.

Let's say we describe a person using just two numbers: their age and their height. Then a person becomes a vector of two numbers, like below:

```
   Person A  ->  [ 25, 170 ]
   Person B  ->  [ 27, 172 ]
   Person C  ->  [ 60, 165 ]

```

Here, we can see that each person is now a list of two numbers. Person A and Person B have similar numbers, so they are similar. Person C has a very different age, so Person C is far from the other two.

Real items like photos and sentences are not described by just two numbers. They are described by hundreds or even thousands of numbers. A special kind of model, called an embedding model, reads an item and produces this vector for us. We do not need to know how it works right now. We just need to know that it turns any item into a vector, and similar items get similar vectors. We have a detailed blog on Contrastive Learning that explains how models learn to give similar items similar vectors.

So, every song, photo, and sentence becomes a point in space described by numbers. Now, let's learn how to measure the distance between two such points.

### How do we measure "closeness"?

Once everything is a vector, "similar" becomes "close", and "different" becomes "far". So, we need a way to measure the distance between two vectors.

The most common way is Euclidean distance. This is just the straight-line distance between two points, the same distance we measure with a ruler.

Let's take two simple vectors with two numbers each:

```
   A = [ 1, 2 ]
   B = [ 4, 6 ]

```

We find the difference in each number, square it, add them, and take the square root:

- difference in first number: 4 - 1 = 3
- difference in second number: 6 - 2 = 4
- distance = square root of (3 squared + 4 squared) = square root of (9 + 16) = square root of 25 = 5

So, the distance between A and B is 5. A smaller distance means the two items are more similar.

We can picture these two points on a simple grid like below:

```
   6 -|                 B (4,6)
   5 -|                /
   4 -|               /
   3 -|              /  distance = 5
   2 -|   A (1,2)---/
   1 -|
   0 -+----------------------
       0  1  2  3  4  5  6

```

Here, we can see two points A and B on a grid. The straight line connecting them is the Euclidean distance, and its length is 5. The closer two points sit, the shorter this line, and the more similar the items are.

Note: There is another popular measure called cosine similarity, which looks at the angle between two vectors instead of the gap between them. It is widely used for text. For now, we just need the core idea: there is a number that tells us how close two vectors are.

So, now finding the nearest neighbor means finding the vector with the smallest distance to our query. Let's see the simplest way to do that.

### The naive approach and why it fails

The most obvious way to find the nearest neighbor is to check every single item.

We take our query vector, measure its distance to every vector in the collection, and keep the one with the smallest distance. This is called the brute-force approach, and it is also called exact search because it always gives the perfect answer.

Let's see this approach like below:

```
   query  ----compare---->  item 1   (distance = 12)
   query  ----compare---->  item 2   (distance = 3)   <- closest so far
   query  ----compare---->  item 3   (distance = 9)
   query  ----compare---->  item 4   (distance = 7)
   ...
   query  ----compare---->  item N   (distance = 5)

```

Here, we can see that we compare the query against every single item, one by one, and pick the smallest distance. For a small collection, this works perfectly.

But, here is the catch. Real collections are huge.

Let's say we have one billion vectors, and each vector has 1000 numbers. To answer one query, we must do one billion distance calculations, and each calculation touches 1000 numbers. That is a thousand billion operations for a single search. And large apps handle thousands of searches every second.

So, the brute-force approach is too slow. It does not scale. We need something much faster.

So, here comes Approximate Nearest Neighbor Search to the rescue.

### What is Approximate Nearest Neighbor (ANN) Search?

Approximate Nearest Neighbor Search means finding a neighbor that is very close to the true nearest one, but much faster, by allowing a tiny chance of not being perfectly exact.

In simple words, instead of checking every item, we use clever shortcuts that look at only a small part of the collection and still find an answer that is almost always correct.

Let's decompose the term:

> Approximate Nearest Neighbor = Approximate + Nearest Neighbor

Approximate means "very close to correct, but not guaranteed to be perfect". Nearest Neighbor is the most similar item, which we already learned.

The best way to understand this is by taking an example. Suppose we are in a giant library and we want a book on cooking. The brute-force way is to read the title of every single book in the building. That is perfect but extremely slow.

The smart way is to walk straight to the "Food and Cooking" section and look only there. We may not find the single best cookbook in the entire building, but we will almost certainly find an excellent one, and we will find it in seconds.

That is exactly what ANN does. It organizes the data in advance so that, at search time, it can jump to the right neighborhood and ignore everything else.

So, ANN trades a tiny bit of accuracy for a massive gain in speed. For almost every real app, this trade is more than worth it.

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

### The trade-off: speed vs accuracy

Before we learn the methods, we must understand the one idea that connects all of them: the trade-off between speed and accuracy.

In ANN, we measure quality using a number called recall.

Recall is the percentage of times the approximate answer matches the true nearest neighbor.

A recall of 100 percent means the approximate answer is always perfect. A recall of 95 percent means it is correct 95 times out of 100, and slightly off the other 5 times. In practice, being slightly off usually means returning the second or third closest item instead of the very closest, which is perfectly fine for most apps.

We can picture the trade-off like below:

```
   brute-force        ANN (tuned for          ANN (tuned for
   (exact)            high accuracy)           high speed)

   recall: 100%       recall: ~99%             recall: ~90%
   speed:  slow       speed:  fast             speed:  very fast

```

Here, we can see the whole picture. As we push for more speed, recall drops a little. As we push for more accuracy, speed drops a little. Every ANN method gives us a knob to balance these two, and we tune it based on our use case.

Now, let's learn the main approaches that make ANN fast. We will build them up one by one.

### Approach 1: Trees (KD-Tree)

The first idea is to split the space into smaller and smaller regions, so we only search the region our query falls into.

A popular method here is the KD-Tree. The "KD" stands for "K-Dimensional", which simply means it works with vectors that have many numbers.

In simple words, a KD-Tree keeps cutting the space in half, again and again. Each cut sends us down one branch and lets us ignore the other branch.

Let's say all our points are spread on a flat board. First, we draw a vertical line that splits the points into left and right. Then, inside each side, we draw a horizontal line that splits them into top and bottom. We keep doing this, building a tree of cuts.

We can picture the tree like below:

```
                    [ all points ]
               split by a vertical line
                 /                  \
        left region              right region
        /         \              /          \
   sub-region   sub-region   sub-region   sub-region

```

Here, we can see that the whole space is cut into a tree of regions. When a query arrives, we follow the cuts down to the small region where it belongs, and we only compare against the few points in that region. We skip the rest of the tree.

The issue with this approach is that it works well only when each vector has few numbers. When vectors have hundreds of numbers, the cuts stop being helpful, and we end up checking almost everything anyway. This problem of high-dimensional data is famously called the curse of dimensionality.

So, trees are great for low-dimensional data but weak for the large, high-dimensional vectors used in modern AI. Let's see how the next approach solves this issue.

### Approach 2: Hashing (LSH)

The next idea is to use a smart shortcut called hashing.

Normally, hashing turns an item into a short code, and very different items get very different codes. But for ANN, we use a special twist called Locality Sensitive Hashing, or LSH.

Locality Sensitive Hashing is a method that gives similar items the same code on purpose, so they land in the same bucket.

In simple words, LSH groups similar vectors into the same "bucket". At search time, we look only inside the query's bucket instead of the whole collection.

Let's say we sort thousands of marbles into a few boxes, and we make sure that marbles of similar color always go into the same box. Later, to find marbles similar to a red one, we open only the red box. We ignore all the other boxes.

We can picture LSH like below:

```
   all vectors  ---LSH--->   Bucket 1: [ v3, v9, v14 ]
                             Bucket 2: [ v1, v7 ]
                             Bucket 3: [ v2, v5, v8, v11 ]   <- query lands here

   query  ---LSH--->  Bucket 3, so compare only with v2, v5, v8, v11

```

Here, we can see that LSH first drops every vector into a bucket. When a query arrives, we run the same hashing on it, find its bucket, and compare only with the few vectors in that bucket. We skip every other bucket.

The advantage is that this is very fast and uses simple, fixed rules. The disadvantage is that the accuracy can be uneven. Sometimes a true neighbor lands in a different bucket and we miss it. To fix this, we use several hash tables at once, which uses more memory.

So, LSH is fast and simple, but to get high accuracy it needs extra memory. Let's see how the next approach handles this.

### Approach 3: Clustering (IVF)

The next idea is to group nearby vectors into clusters in advance, and then search only the clusters closest to our query.

This method is called IVF, which stands for Inverted File Index. The name sounds heavy, but the idea is simple.

In simple words, we divide all the vectors into groups, where each group has a representative center point, and at search time we only open the few groups whose centers are nearest to the query.

The best way to learn this is by taking an example. Suppose we sort all the people in a country by which city they live in. Each city has a center. To find people near a given location, we first find the nearest city or two, and then look only at the people in those cities. We do not scan the whole country.

This happens in two phases.

Step 1: Build the clusters (done once, in advance). We group all the vectors into clusters. Each cluster gets a center point that represents it. This grouping step is often done using a method called k-means, which simply finds natural groups in the data.

Step 2: Search (done for every query). When a query arrives, we first compare it only with the cluster centers, which are very few. We pick the nearest few clusters. Then we compare the query only with the vectors inside those chosen clusters.

We can picture IVF like below:

```
   Cluster A (center cA): [ v1, v4, v8 ]
   Cluster B (center cB): [ v2, v6 ]
   Cluster C (center cC): [ v3, v5, v7, v9 ]

   Step 1: query vs centers ->  cA, cB, cC   (pick nearest: cC)
   Step 2: query vs members of C only -> v3, v5, v7, v9

```

Here, we can see that we first compare the query against a handful of cluster centers, not the whole collection. Then we open only the nearest cluster and compare against the vectors inside it. Everything else is skipped.

There is a knob here called `nprobe`, which decides how many clusters we open. If we open more clusters, we get higher accuracy but slower speed. If we open fewer clusters, we get more speed but lower accuracy. We tune `nprobe` based on our use case.

So, IVF gives us a clean balance and scales to billions of vectors. But we can have an even smarter approach than this too.

### Approach 4: Graphs (HNSW)

The most popular ANN method today is based on graphs. It is called HNSW, which stands for Hierarchical Navigable Small World.

The name is long, so let's decompose it.

A graph is just a set of points connected by links. Here, each vector is a point, and we connect each vector to its nearby vectors with links. To find a neighbor, we hop from point to point along the links, always moving closer to the query. This is the "Navigable" part.

The Hierarchical part means we build several layers of this graph, stacked on top of each other. The top layer is sparse and has only a few points with long links. Each lower layer is denser. We start our search at the top, take big jumps to get close fast, and then drop into the lower, denser layers to fine-tune the answer.

The best way to understand this is by taking an example. Think of how we travel between two cities. First, we take a highway to cover most of the distance quickly, which is the top layer. Then, we take main roads, which is the middle layer. Finally, we take small local streets to reach the exact house, which is the bottom layer.

We can picture the layers like below:

```
   Top layer (few points, long jumps)
      A -------------------- F
       \                    /
        \                  /
   Middle layer (more points)
      A ---- C ---- D ---- F
       \    /  \   /  \   /
   Bottom layer (all points, short hops)
      A - B - C - D - E - F - G   <- final answer found here

```

Here, we can see the journey. We enter at the top layer and take large jumps to get into the right area quickly. Then we move down layer by layer, taking smaller and smaller hops, until we reach the closest point in the dense bottom layer. We never touch the points that are far away.

This greedy hopping is extremely fast and gives very high accuracy. This is why HNSW is the default choice in most modern vector databases.

The advantage is excellent speed and accuracy together. The disadvantage is that the graph uses more memory and takes longer to build than the other methods. But for most apps, the search speed matters most, so HNSW wins.

So, now we have learned the four main families of ANN: trees, hashing, clustering, and graphs.

These four families are the engines inside modern Vector Databases. If we want to go deeper into Vector Databases, embeddings, and AI and ML System Design, we cover all of these in our AI and Machine Learning Program at Outcome School.

### A simple code example

Now, let's see ANN in action using a popular open-source library called FAISS, which is built for fast vector search. We will use the IVF method we just learned. Let's see the code as below:

```python
import faiss
import numpy as np

# Suppose we have 100000 vectors, each with 128 numbers
dimension = 128
data = np.random.random((100000, dimension)).astype("float32")

# Build an IVF index with 100 clusters
quantizer = faiss.IndexFlatL2(dimension)
index = faiss.IndexIVFFlat(quantizer, dimension, 100)

# Step 1: learn the clusters from the data
index.train(data)

# Step 2: add all the vectors into the index
index.add(data)

# Open 10 nearest clusters per query (the nprobe knob)
index.nprobe = 10

# Search: find the 5 nearest neighbors of one query vector
query = np.random.random((1, dimension)).astype("float32")
distances, neighbors = index.search(query, 5)

print(neighbors)

```

Here, we have built an ANN search system, and let me explain each part.

- `data` is our collection of 100000 vectors, each with 128 numbers.
- `IndexIVFFlat(quantizer, dimension, 100)` creates an IVF index that splits the data into 100 clusters.
- `index.train(data)` is Step 1. It learns the cluster centers from the data.
- `index.add(data)` is Step 2. It places every vector into its nearest cluster.
- `index.nprobe = 10` is the knob. It tells the search to open the 10 nearest clusters per query. A higher value gives more accuracy but less speed.
- `index.search(query, 5)` finds the 5 nearest neighbors of the query, returning their distances and positions.

So, in just a few lines, we have built a fast search over 100000 vectors without comparing against every single one. It works perfectly.

The kind of search index we just built is exactly what powers RAG systems and the long-term memory of AI assistants. We have a complete program where we learn RAG and build an AI Tutor from scratch - check out our AI and Machine Learning Program at Outcome School.

### Where ANN Search is used

[…337ln elided…]

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

[Showing lines 1-389 and 727-1102 of 1102; 337 middle lines (19.1KB) elided. Read artifact://79 for full output]
