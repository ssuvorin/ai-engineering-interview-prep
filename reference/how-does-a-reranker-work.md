> Source: https://outcomeschool.com/blog/how-does-a-reranker-work

# How does a Reranker work?
URL: https://outcomeschool.com/blog/how-does-a-reranker-work
Published: 2026-06-08
Author: Amit Shekhar

How does a Reranker work?

# How does a Reranker work?

Authors
: - Name
: Amit Shekhar
Published on
: June 8, 2026

A Reranker is a model that takes a list of documents and reorders them, putting the most relevant ones at the top for a given question. In simple words, it is a smart sorter that sits after the first fast search.

In this blog, we will learn about how a Reranker works. We will also see where it sits in a search and RAG pipeline, why we need it, and how it makes our answers more accurate.

We will cover the following:

- What is a Reranker?
- Where a Reranker sits in a search / RAG pipeline
- The two-stage retrieval idea
- Why first-stage retrieval is fast but not precise
- Bi-encoder vs Cross-encoder
- How a Reranker scores documents step by step
- The accuracy vs latency and cost trade-off
- Late-interaction models like ColBERT
- Real examples of Rerankers
- Why Rerankers matter for RAG

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a Reranker?

A Reranker is a model that takes a list of documents and reorders them, putting the most relevant ones at the top for a given question.

In simple words, a Reranker is a smart sorter. We give it a question and a small pile of documents. It reads each document carefully against the question and decides which one answers the question best. Then it arranges them from most relevant to least relevant.

Let's say we go to a library and ask the librarian for books on "healthy cooking". A junior helper quickly runs around and brings us 50 books that have the words "healthy" or "cooking" somewhere on the cover. That is a fast but rough first pass.

Now, a senior librarian sits down, opens each of those 50 books, and actually reads a few pages. She knows that one book is about cooking for athletes, another is a diet plan, and another only mentions cooking once in passing. She reorders the pile so the best matches are on top.

That senior librarian is the Reranker.

So, the Reranker does not search the whole world. It only re-arranges a shortlist that someone else already gathered. It does not invent new documents and it does not go and find more. It simply reorders what it is given. This single idea is the heart of everything we will learn today.

### Where a Reranker sits in a search / RAG pipeline

Before we go deeper, we must understand where the Reranker lives in a real system.

Most modern search systems and AI question-answering systems follow a pipeline. A pipeline is just a series of steps where the output of one step becomes the input of the next step.

Let's talk about RAG for a moment, because Rerankers are very popular there. RAG stands for Retrieval-Augmented Generation. In simple words, it is a technique where, before an AI model answers our question, we first fetch some relevant documents and hand them to the model so it can answer using real facts instead of guessing.

So in RAG, the flow looks like below:

```
Question
   |
   v
[ Retriever ]   --> fetches many candidate documents (fast, rough)
   |
   v
[ Reranker ]    --> reorders the candidates by true relevance (slow, precise)
   |
   v
[ LLM ]         --> reads the best documents and writes the final answer
   |
   v
Answer

```

Here, the LLM is the AI model that writes the final answer in plain language. LLM stands for Large Language Model. We can see that the Reranker sits right in the middle. It comes after the first fetch and before the AI writes the answer. Its only job is to clean up and reorder what the first step found, so that the AI reads the best material.

We have a detailed blog on Agentic RAG that covers how modern RAG systems retrieve and reason over multiple sources.

Now, the question is, why do we need two separate steps at all? Why not let one model do everything? To answer that, we need to understand the two-stage retrieval idea.

### The two-stage retrieval idea

Imagine we have a huge collection of documents. It can be millions of web pages, or thousands of company documents, or the chapters of many books. We call this big collection the corpus.

When a user asks a question, in theory the perfect approach would be to carefully read every single document in the corpus and pick the best ones. But reading millions of documents carefully for every question would take forever. It would be too slow and too expensive.

So, here comes the two-stage approach to the rescue.

Stage 1 - Retrieval: A fast retriever quickly scans the entire corpus and pulls out a list of maybe 100 or 200 candidate documents that look roughly related to the question. This stage is built for speed. It is allowed to be a little sloppy.

Stage 2 - Reranking: The Reranker takes only that shortlist of 100 or 200 candidates and reads each one carefully against the question. It then reorders them and we keep only the top few, for example the top 5 or top 10.

Let's see this with a simple picture:

```
Corpus (1,000,000 documents)
        |
        |  Stage 1: fast retriever
        v
   100 candidates  (rough shortlist)
        |
        |  Stage 2: reranker
        v
   Top 5 documents  (carefully reordered, most relevant)

```

Here, we can notice the trick. We never run the slow, careful model on all one million documents. We only run it on the 100 that survived the first stage. This way we get both speed and accuracy.

This is the central idea. The first stage trades precision for speed. The second stage trades speed for precision. Together, they give us the best of both.

### Why first-stage retrieval is fast but not precise

Now, let's understand the first stage better, because understanding its weakness is exactly why the Reranker exists.

There are two common ways to do first-stage retrieval, and many real systems combine both into what is called Hybrid Search. Let's understand both in simple words.

BM25 (keyword search): This is the classic way. It matches the words in the question with the words in the documents. If the question says "healthy cooking", it looks for documents that contain those exact words and rewards documents where the rarer, more meaningful words appear more often. It is fast and it works well, but it only understands exact words. It does not understand meaning. If a document says "nutritious recipes" instead of "healthy cooking", BM25 will struggle, because the words are different even though the meaning is the same.

Vector search (semantic search): This is the modern way. Here, every document is converted into a list of numbers called an embedding. An embedding is a way to represent the meaning of a piece of text as a point in space. Texts with similar meaning end up close to each other, and texts with different meaning end up far apart. When a question comes, we turn the question into an embedding too, and then we look for the documents whose embeddings are closest to the question's embedding.

We have a detailed blog on how a Vector Database works that explains embeddings and vector search in depth.

Vector search is wonderful because it understands meaning, not just words. But it is still not perfect.

Here is the catch. In vector search, the question and the documents are turned into embeddings completely separately, ahead of time. The model never gets to look at the question and a document together. It compresses an entire document into one fixed list of numbers before it ever sees our question. A lot of fine detail is lost in that compression.

Let's say we ask, "Which medicine should I avoid if I have high blood pressure?" A document that talks a lot about blood pressure and medicines in general will look very close in vector space, even if it never actually says which medicine to avoid. The embedding captures the broad topic, but it can miss the precise answer.

So, first-stage retrieval is fast and gives us a good rough shortlist. But it often puts a "kind of related" document above the "exactly right" document. It gets us into the right neighborhood, but not to the right house.

One way to improve the first stage itself is HyDE, where we search with a hypothetical answer instead of the raw question, so the query is shaped more like the documents we want. Another is Multi-Query Retrieval, where an LLM writes several versions of the question, we search with each of them, and we merge the results.

This is exactly the gap the Reranker fills. To understand how it does a better job, we must learn about two types of models.

### Bi-encoder vs Cross-encoder

This is the most important part of the blog, so let's go slowly.

A first-stage retriever using vector search is built on a bi-encoder. The Reranker is built on a cross-encoder. The names sound similar, but the difference between them is the whole secret.

Bi-encoder: The word "bi" means two. A bi-encoder uses two separate passes. It encodes the question on its own, and it encodes each document on its own, into separate embeddings. The question never meets the document inside the model. Only at the very end do we compare the two embeddings to see how close they are.

Let's picture it like below:

```
BI-ENCODER (used for fast retrieval)

  Question  -->  [encoder]  -->  [ vector A ]
                                       \
                                        compare distance --> score
                                       /
  Document  -->  [encoder]  -->  [ vector B ]

```

Here, the big advantage is speed. Because each document is encoded by itself, we can encode all our documents once, in advance, and store their embeddings. When a question arrives, we only encode the question and compare. That is why vector search over millions of documents can be very fast. The structure that makes this fast over so many vectors is Approximate Nearest Neighbor (ANN) search, which skips most of the comparisons.

But the disadvantage is precision. The model decided what each document "means" without ever knowing what we would ask. It had to guess in advance which details matter.

Cross-encoder: The word "cross" means crossing or combining. A cross-encoder takes the question and one document and feeds them in together, joined as a single input. The model reads them side by side and can directly relate each word of the question to each word of the document. At the end, it outputs a single number, a relevance score, that says how well this document answers this question.

Let's picture it like below:

```
CROSS-ENCODER (used for reranking)

  Question + Document  -->  [ model reads them together ]  -->  relevance score (for example, 0.92)

```

Here, the advantage is accuracy. Because the model sees the question and the document at the same time, it can catch fine details. It can notice that the document really does name the exact medicine to avoid, and not just talk about medicines in general.

But the disadvantage is speed. The cross-encoder must run fresh for every single question-document pair. Nothing can be prepared in advance, because the question is new every time. If we had a million documents, we would have to run the cross-encoder a million times for one question. That is far too slow.

Let me tabulate the differences between a bi-encoder and a cross-encoder for your better understanding so that you can decide which one to use based on your use case.

| Point | Bi-encoder | Cross-encoder |
| --- | --- | --- |
| How it reads | Question and document separately | Question and document together |
| Output | One embedding per text | One relevance score per pair |
| Speed | Very fast | Slow |
| Precision | Good, but loses fine detail | High, catches fine detail |
| Can precompute? | Yes, embed documents in advance | No, must run per question |
| Best used for | First-stage retrieval over the full corpus | Reranking a small shortlist |

So now we can clearly see the plan. We use the fast bi-encoder to shortlist many candidates, and then we use the accurate cross-encoder to reorder only that shortlist. The Reranker is the cross-encoder.

To go deep into Embeddings and Vector Databases, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

### How a Reranker scores documents step by step

Now, let's walk through exactly what a Reranker does when a question comes in. We will use small numbers for the sake of understanding.

Suppose the user asks: "What is the capital of France?"

The first-stage retriever returns 4 candidate documents:

- Document 1: "France is a country in Europe known for its food and culture."
- Document 2: "Paris is the capital and largest city of France."
- Document 3: "The Eiffel Tower is located in Paris and is very famous."
- Document 4: "Berlin is the capital of Germany."

Step 1: The Reranker pairs the question with each document, one at a time. So we form 4 pairs.

Step 2: It feeds each pair into the cross-encoder, which reads the question and that document together and produces a relevance score. A higher score means more relevant.

Let's say the scores come out like below:

```
Question: "What is the capital of France?"

(Question + Document 1)  -->  cross-encoder  -->  0.34
(Question + Document 2)  -->  cross-encoder  -->  0.97
(Question + Document 3)  -->  cross-encoder  -->  0.55
(Question + Document 4)  -->  cross-encoder  -->  0.21

```

Here, we can see that Document 2 scored the highest, because it directly says Paris is the capital of France. Document 3 scored in the middle because it mentions Paris but does not actually answer the question. Document 4 scored low because it is about Germany, even though it shares the word "capital". The exact numbers do not matter on their own. What matters is the order they give us.

Step 3: The Reranker sorts the documents by score, from highest to lowest.

After sorting, the order becomes: Document 2, Document 3, Document 1, Document 4.

We can picture this reordering as below:

```
   BEFORE (first-stage order)            AFTER (reranked order)

   +-----------------------+             +-----------------------+
   | 1. Document 1  (0.34) |             | 1. Document 2  (0.97) |
   | 2. Document 4  (0.21) |   rerank    | 2. Document 3  (0.55) |
   | 3. Document 2  (0.97) |   ------->  | 3. Document 1  (0.34) |
   | 4. Document 3  (0.55) |             | 4. Document 4  (0.21) |
   +-----------------------+             +-----------------------+

```

Here, we can notice that the first-stage order on the left is messy, because Document 4 about Germany was placed high just for sharing the word "capital", while the truly correct Document 2 was buried lower. After reranking on the right, the documents are sorted purely by their relevance score, so Document 2 rises to the very top and Document 4 sinks to the bottom.

Step 4: We keep only the top-k documents. If we choose top-2, we keep Document 2 and Document 3.

Notice something important. The first-stage retriever often places a document like Document 4 high, because it shares the strong word "capital" with the question. The Reranker fixed this mistake by actually understanding the meaning. It pushed the truly correct document, Document 2, to the very top.

This is how a Reranker works in practice. It scores, it sorts, and we take the top few. Problem Solved.

In a RAG system, those top-2 documents are then handed to the AI model, which reads them and writes a clean answer like "The capital of France is Paris." The better the documents we hand over, the better the final answer. The Reranker makes sure we hand over the best documents.

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

### The accuracy vs latency and cost trade-off

Now, we must talk about the cost, because this is exactly why we do not just rerank everything. Two things matter here. One is latency, which simply means how long the user waits for an answer. The other is the money cost of running the model.

A cross-encoder is powerful but slow and expensive to run. Every question-document pair needs a full pass through the model. So the more documents we rerank, the more time and money it takes.

Let's say running the cross-encoder on one pair takes a tiny moment. Running it on 100 pairs is fine, it stays fast enough for a user to wait. But running it on one million pairs for every question would be painfully slow and would cost a fortune.

This is the whole reason for the two-stage design. We let the cheap, fast bi-encoder handle the millions, and we save the expensive, accurate cross-encoder for the small shortlist.

```
Run cross-encoder on ALL 1,000,000 docs  -->  extremely slow and costly  (we avoid this)

Run cross-encoder on TOP 100 only         -->  fast enough and very accurate  (we do this)

```

So, the Reranker gives us a careful, high-quality reordering, but we apply it only where it pays off. We balance accuracy against latency and cost by choosing how many candidates to rerank. A common choice is to retrieve 100 to 200 candidates and rerank them down to the top 5 or top 10, which also keeps the final prompt short, so a genuinely relevant document does not get lost in the middle of a long prompt.

Note: The number of candidates we rerank is a knob we can tune. More candidates means higher accuracy but more cost and a slower response. Fewer candidates means faster and cheaper but we risk missing a good document that the first stage ranked low. We pick the balance based on our use case.

### Late-interaction models like ColBERT

We have seen two extremes. The bi-encoder is fast but rough. The cross-encoder is precise but slow. Now, the next question is, can we have something in the middle? The answer is yes.

There is a family of models called late-interaction models, and the most well-known one is called ColBERT, which is short for Contextualized Late Interaction over BERT.

In simple words, a late-interaction model is a clever middle ground between a bi-encoder and a cross-encoder.

Let's understand the idea gently. A normal bi-encoder squeezes a whole document into one single embedding. ColBERT does not do that. Instead, it keeps a separate small embedding for each word in the document, and it can compute these document embeddings in advance, just like a bi-encoder. That keeps it fast.

Then, at question time, it compares the words of the question against the words of the document in a fine-grained way and adds up the best matches. This word-by-word comparison happens late, which is why it is called "late interaction". It recovers a lot of the fine detail that a normal bi-encoder loses.

So, ColBERT sits between the two worlds. It is more precise than a plain bi-encoder because it compares at the word level, and it is faster than a cross-encoder because it precomputes the document side. We can think of it as a faster, lighter way to get some of the Reranker's accuracy.

Now, an important question is, where exactly does ColBERT fit in our pipeline? This matters, because ColBERT can sit in two different places. We can picture both placements as below:

```
Option A - ColBERT as the Reranker (Stage 2 only):

   Question --> [ Retriever ] --> [ ColBERT ] --> [ LLM ] --> Answer

Option B - ColBERT as Retriever and Reranker together (Stage 1 + Stage 2):

   Question --> [ ColBERT ] --> [ LLM ] --> Answer

```

[…432ln elided…]
| --- | --- | --- |
| BERT reranker | 34.7 | ~10,700 ms |
| ColBERT (rerank) | 34.9 | ~61 ms |

ColBERT was about 170 times faster with roughly the same quality, and used vastly fewer computations. And run end-to-end over the full 8.8 million passages, it retrieved in well under a second with very high recall, far better quality than the cheap keyword and single-vector methods.

## Where ColBERT led

ColBERT created a whole retrieval paradigm. Let's decode its legacy, piece by piece.

- A third option. Late interaction (multi-vector) now sits alongside single-vector dense (DPR), learned sparse (SPLADE), and keyword search as a main retrieval style, a middle ground more accurate than single-vector and far cheaper than a full reranker.
- Smaller indexes. ColBERTv2 attacked the storage problem directly with residual compression, storing each vector as a nearby centroid plus a tiny correction. That cut the MS MARCO index from about 154 GB down to roughly 16 to 25 GB, which is a 6 to 10 times reduction, with better quality than the original.
- Faster serving. PLAID made ColBERTv2 practical in production by pruning candidates using those centroids before touching the full vectors, bringing latency down to a few tens of milliseconds.
- Beyond text. The late-interaction idea spread to images. ColPali runs MaxSim over the patches of a document image (a page screenshot) against the query tokens, enabling visual document retrieval over charts, tables, and scanned pages, without reading the text at all.
- Inside RAG systems. Late-interaction retrievers are now a common first stage in Retrieval-Augmented Generation, where the quality of what we retrieve decides the quality of what the model answers.

Through it all, the core idea endures: keep the word-by-word matching, but defer it to a cheap MaxSim so documents can be precomputed and search stays fast.

## Quick Summary

We have decoded the ColBERT paper piece by piece. Let's recap each piece in one line.

- ColBERT encodes query and document into per-token vectors separately, then scores with a cheap MaxSim.
- The two old extremes: cross-encoders are accurate but unscalably slow, and single-vector models are fast but blunt.
- Late interaction: keep word-level matching, but run it late and cheaply so documents are precomputed offline.
- Encoding: a shared BERT with `[Q]` and `[D]` markers, projected to 128-number unit vectors (so cosine equals dot product).
- MaxSim: `S(q, d) = sum over i of ( max over j of ( Eq_i · Ed_j ) )`, which means for each query token take its best-matching document token, then sum those maxima.
- Why max: it rewards a document for containing a strong match (0.96), instead of diluting it with an average (0.52).
- Ranking: document A scored 1.76 beats document B at 1.08.
- Training: triples of query, positive passage, and negative passage, with the only goal being that the positive must score higher.
- The loss: a pairwise softmax cross-entropy, which fell from 0.41 to 0.13 as the gap between the two scores grew.
- Fast at scale: MaxSim is pruning-friendly, enabling both reranking and end-to-end retrieval from millions of passages.
- The cost: one vector per token makes the index about 100 times bigger, around 154 GB for MS MARCO.
- The results: about the same quality as a BERT reranker (34.9 vs 34.7 MRR) at roughly 170 times the speed.
- The legacy: late interaction as a main retrieval paradigm, ColBERTv2 for compressed indexes, PLAID for fast serving, and ColPali for visual document retrieval.

Now, we have decoded ColBERT piece by piece and understood how deferring the word-by-word matching to a cheap MaxSim keeps fine-grained accuracy while scaling to millions of passages.

### Why can ColBERT precompute documents when a cross-encoder cannot?

ColBERT can precompute documents because its document encoder never sees the query. So every document's token vectors are computed once, offline, and stored. A cross-encoder feeds the query and document together into BERT, so its document representation depends on the query and BERT must run again for every query-document pair.

### Is ColBERT better than a single-vector dense retriever?

ColBERT is more accurate, but it costs more storage. A single-vector model squashes a whole passage into one vector and loses word-level detail. ColBERT keeps one vector per token, which makes the index about 100 times bigger, around 154 GB for MS MARCO instead of a few gigabytes.

### Can ColBERT be used as a first-stage retriever and not just a reranker?

Yes. ColBERT can rerank the top candidates from a cheap first stage, or it can do end-to-end retrieval over millions of passages. In end-to-end mode, it uses an approximate nearest-neighbor filter first, then runs exact MaxSim on the survivors. This works because MaxSim is pruning-friendly.

### Is ColBERT used in RAG systems?

Yes. Late-interaction retrievers are now a common first stage in Retrieval-Augmented Generation. In RAG, the quality of what we retrieve decides the quality of what the model answers. ColBERT keeps word-level matching while staying fast, which makes it a good fit for this stage.

### Does late interaction work only for text?

No. The late-interaction idea spread to images through ColPali. ColPali runs MaxSim over the patches of a document image, like a page screenshot, against the query tokens. This enables visual document retrieval over charts, tables, and scanned pages without reading the text at all.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

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

[Showing lines 1-321 and 754-1140 of 1140; 432 middle lines (21.3KB) elided. Read artifact://77 for full output]
