> Source: https://outcomeschool.com/blog/graphrag

# GraphRAG
URL: https://outcomeschool.com/blog/graphrag
Published: 2026-05-05

GraphRAG

# GraphRAG

Authors
: - Name
: Amit Shekhar
Published on
: May 5, 2026

In this blog, we will learn about GraphRAG and how it improves retrieval by using a knowledge graph along with vector search.

We will cover the following:

- What is GraphRAG?
- Why normal RAG is not enough
- The big picture of GraphRAG
- How GraphRAG builds the knowledge graph
- How GraphRAG answers a question
- Local search vs Global search
- When to use GraphRAG
- Trade-offs of GraphRAG
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is GraphRAG?

Imagine asking our company knowledge base, "How is our CEO connected to our biggest customer through past projects?" and getting a clean, connected answer instead of a pile of unrelated chunks. That is what GraphRAG enables.

Let's start with the name itself.

GraphRAG = Graph + RAG.

The "Graph" part is a knowledge graph, where each important thing in our documents becomes a node, and each relation between those things becomes a connection.

The "RAG" part is Retrieval-Augmented Generation, where we fetch relevant information from our data and pass it to the LLM along with the question, so the LLM can answer correctly.

In simple words:

GraphRAG = RAG that uses a knowledge graph to find better, more connected information before answering.

For the sake of understanding, we can think of a knowledge graph like a small Wikipedia of our own data, where every important thing is a page, and every link between two pages tells us how they are related.

GraphRAG is one of several advanced flavors of RAG. Another one is Agentic RAG, where the agent decides what to retrieve and when. A related trick is HyDE, where we search with a hypothetical answer instead of the raw question to retrieve better chunks.

### Why normal RAG is not enough

Before we go into GraphRAG, we must first understand where normal RAG struggles.

Normal RAG works like this:

- We split our documents into small chunks.
- We convert each chunk into an embedding (a vector of numbers).
- When the user asks a question, we convert the question into an embedding too.
- We find the chunks whose embeddings are closest to the question.
- We pass those chunks to the LLM as context.

This works well for simple questions where the answer sits inside one or two chunks.

But here is the catch.

Suppose our documents talk about many people, companies, products, and events. The user asks:

> "How is Person A connected to Company X through their work history?"

To answer this, we need to:

- Find Person A.
- Find their previous companies.
- Find which of those companies are linked to Company X.
- Combine all of this into one answer.

Normal RAG cannot do this well. It picks chunks that look similar to the question, but it does not actually follow the connections between people, companies, and events. The information is scattered across many chunks, and similarity search alone cannot stitch them together.

This kind of question is called a multi-hop question, because answering it needs more than one hop across pieces of information.

Do you see the problem? The information is connected like a web, but normal RAG treats every chunk as an island.

This is where GraphRAG comes into the picture.

### The big picture of GraphRAG

Before we go into the details, let's understand the big picture.

GraphRAG works in two phases:

- Indexing phase: We read all our documents once and build a knowledge graph out of them. This graph stores every important thing (entity) and how it is connected to other things (relation).
- Query phase: When the user asks a question, we look up the relevant part of the graph, follow the connections, collect the right information, and pass it to the LLM as context.

So the heavy work is done once during indexing, and every user question then runs through the lighter query phase.

We can picture the full flow like below:

```
   INDEXING PHASE (run once)
   ----------------------------------------------------
   Documents
       |
       v
   Split into Chunks
       |
       v
   Extract Entities + Relations  (using LLM)
       |
       v
   Build Knowledge Graph
       |
       v
   Group nodes into Communities
       |
       v
   Write Community Summaries  (using LLM)
       |
       v
   Stored: Graph + Embeddings + Summaries

   ----------------------------------------------------

   QUERY PHASE (run for every question)
   ----------------------------------------------------
   User Question
       |
       v
   Find starting entities (embedding similarity + extraction)
       |
       v
   Walk connections + collect chunks + summaries
       |
       v
   Pass everything to the LLM as context
       |
       v
   Final Answer

```

Now, let's decode each phase.

### How GraphRAG builds the knowledge graph

This is the indexing phase. It happens once, before any user asks a question.

Let's say our documents contain a paragraph like this:

> "Alice worked at Acme as an engineer. Acme was acquired by Globex in 2020. Bob was the CEO of Globex at that time."

A normal RAG pipeline would just split this into chunks and store the embeddings.

GraphRAG does more. It uses an LLM to read the text and pull out two things:

- Entities: the important things mentioned, like people, companies, dates, products. Here, the entities are `Alice`, `Acme`, `Globex`, `Bob`.
- Relations: how those entities are connected, like "works at", "acquired", "CEO of". Here, the relations are `Alice -> works at -> Acme`, `Globex -> acquired -> Acme`, `Bob -> CEO of -> Globex`.

We can picture the graph like below:

```
   Alice ----(works at)----> Acme
                              ^
                              |
                          (acquired)
                              |
   Bob ------(CEO of)----> Globex

```

Here, every entity is a node and every relation is an edge that connects two nodes.

GraphRAG repeats this for every chunk in our documents. Slowly, a large knowledge graph is built. The same entity from different chunks gets merged into one node, so all information about `Globex` ends up at the same place.

There is one more step. Once the graph is built, GraphRAG groups closely connected nodes into communities. A community is a small cluster of nodes that talk about a similar theme, like "Acme acquisition story" or "Bob's career". For each community, an LLM writes a short community summary in plain English.

So after indexing, we have:

- A graph of entities and relations.
- Embeddings for each entity, relation, chunk, and community summary.
- Community summaries for groups of related entities.

Recomputing all of these embeddings on every re-index gets expensive, so we have a detailed blog on how an Embedding Cache works that explains how to skip the ones that have not changed.

Note: GraphRAG does not throw away embeddings. It keeps them and uses them along with the graph. So at query time, we can find the right starting point in the graph using embeddings, and then walk the connections from there.

Our knowledge layer is ready now.

To learn RAG, Vector Databases, embeddings, and LLM fundamentals in depth, check out our AI and Machine Learning Program at Outcome School.

### How GraphRAG answers a question

This is the query phase. It happens every time a user asks something.

Let's say the user asks:

> "How is Alice connected to Bob?"

GraphRAG handles this in a few simple steps:

- Step 1: Convert the question into an embedding and find the most relevant entities in the graph by embedding similarity. Also pick up any entities mentioned directly in the question. Here, the starting entities are `Alice` and `Bob`.
- Step 2: Walk the connections starting from these nodes. From `Alice`, we reach `Acme`. From `Acme`, we reach `Globex`. From `Globex`, we reach `Bob`. We have a path now.
- Step 3: Collect the relevant nodes, edges, original text chunks, and community summaries along this path, and pass all of this to the LLM as context with the original question.
- Step 4: The LLM generates a clean, connected answer.

The answer would look like:

> "Alice worked at Acme. Acme was later acquired by Globex, where Bob was the CEO. So Alice is connected to Bob through the Acme-Globex acquisition."

Here, we can see that the answer pulls information from three different sentences in the original document and stitches them together using the graph. Normal RAG would have struggled here because no single chunk contains the full chain.

This is the power of GraphRAG. It does not just find similar chunks. It walks the relations and brings back a connected story. It works perfectly.

The problem is solved.

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

### Local search vs Global search

GraphRAG supports two different ways of searching the graph, based on the type of question.

Local search is used when the question is about a specific entity or a small region of the graph.

For example: "What is Alice's role at Acme?"

Here, we only need to look at the area of the graph around `Alice` and `Acme`. We collect a small subgraph, the connected text chunks, and pass them to the LLM.

Global search is used when the question is about the whole dataset and needs a high-level understanding.

For example: "What are the major themes across all our company documents?"

Here, no single subgraph is enough. We need a wider view. So GraphRAG uses the community summaries that were created during indexing, and it does this in two steps:

- Map step: For each community summary, the LLM produces a small partial answer in parallel, along with a relevance score.
- Reduce step: The LLM takes the highest-scoring partial answers and combines them into one final answer.

This map-then-reduce style allows global search to scale across thousands of communities without overflowing the context window.

In simple words:

- Local search = zoom in on a specific part of the graph.
- Global search = zoom out, ask each community a small question (map), then merge the answers (reduce).

This is how GraphRAG handles both narrow and wide questions using the same underlying graph.

If we want to go deep into RAG, Context Engineering, embeddings, and Vector Databases, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

### When to use GraphRAG

GraphRAG is not always the right choice. It is most useful when:

- Our documents have many connected entities, like people, products, companies, events.
- Users ask questions that need information from multiple chunks combined together.
- Users ask high-level questions about the whole dataset, not just one fact.
- The dataset is rich in relationships, like research papers, legal documents, company knowledge bases, or news archives.

For example, a law firm has thousands of court cases, judgements, and contracts. A lawyer asks, "Which judges have ruled in our favor on intellectual property cases involving our top three clients?" To answer this, the system must connect judges, cases, rulings, and clients across many documents. Normal RAG cannot do this. GraphRAG makes our life easy here.

If our use case is simple, where one chunk is usually enough to answer a question, then normal RAG is faster, cheaper, and good enough.

Also, not every knowledge graph has to be extracted by an LLM. Teams write one by hand too, as plain markdown files that link to each other, and OKF is the open standard for exactly that. We have a detailed blog on What is OKF (Open Knowledge Format)? that explains how those links turn a folder of files into a graph an agent can walk.

### Trade-offs of GraphRAG

GraphRAG is powerful, but it comes with a trade-off:

- Indexing is expensive. Building the graph needs many LLM calls to extract entities, relations, and community summaries. This takes time and money.
- Storage is heavier. We store the graph, embeddings, and summaries together, not just chunks.
- Updates are not free. When new documents arrive, the graph and summaries must be updated, not just the embedding store.
- Engineering is more complex. We must maintain a graph database or graph structure along with the vector store.

Let me tabulate the differences between normal RAG and GraphRAG for your better understanding so that you can decide which one to use based on your use case.

| Aspect | Normal RAG | GraphRAG |
| --- | --- | --- |
| Retrieval style | Similarity search on chunks | Walk a knowledge graph + similarity search |
| Best for | Single-fact questions | Multi-hop and high-level questions |
| Indexing cost | Low | High (many LLM calls) |
| Storage | Vector store of chunks | Graph + vectors + community summaries |
| Engineering effort | Simple | More complex |
| Answer quality on connected data | Limited | Much better |

So GraphRAG makes retrieval much smarter, but it costs more to set up and maintain. I personally believe that GraphRAG is worth the cost only when our data is rich in relationships and our users genuinely ask multi-hop questions. For everything else, normal RAG is the better starting point.

### Quick Summary

Let's recap what we have learned:

- GraphRAG = Graph + RAG. It is RAG that uses a knowledge graph alongside vector search.
- Normal RAG limitation. Normal RAG cannot follow connections across multiple chunks, so multi-hop questions are hard.
- Indexing phase. GraphRAG uses an LLM to extract entities and relations from documents and build a knowledge graph. It also creates community summaries.
- Query phase. GraphRAG finds the starting entities by embedding similarity, walks the graph, collects connected nodes, edges, chunks, and summaries, and sends them to the LLM.
- Local search. Used for specific questions about a small area of the graph.
- Global search. Used for big-picture questions, powered by community summaries with a map-then-reduce step.
- When to use it. When data is connection-rich and questions span multiple entities.
- Trade-off. Better answers, but higher indexing cost, storage, and complexity.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
