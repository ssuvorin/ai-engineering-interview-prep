> Source: https://outcomeschool.com/blog/how-does-hybrid-search-work

# How does Hybrid Search work?
URL: https://outcomeschool.com/blog/how-does-hybrid-search-work
Published: 2026-07-07
Author: Amit Shekhar

How does Hybrid Search work?

# How does Hybrid Search work?

Authors
: - Name
: Amit Shekhar
Published on
: July 7, 2026

Hybrid Search is a technique that combines keyword search and semantic search, and merges their results into one final ranked list. This way, we get exact word matches and meaning-based matches together.

In this blog, we will learn about how Hybrid Search works. We will also see why we need it, the two kinds of search it combines, how their results are merged together, and where it is used in real systems like RAG.

We will cover the following:

- What is keyword search?
- Why keyword search alone is not enough
- What is semantic search?
- Why semantic search alone is not enough
- What is Hybrid Search?
- How Hybrid Search runs both searches
- How the two result lists are combined
- Reciprocal Rank Fusion (RRF)
- Weighted score combination and normalization
- Hybrid Search in the real world

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is keyword search?

Before we talk about Hybrid Search, we must first understand what keyword search is.

The first way is keyword search.

Keyword search finds documents that contain the same words as the query.

In simple words, it looks for an exact word match. If the user types the word "refund", keyword search looks for documents that literally contain the word "refund".

Let's say our query is "refund policy". Keyword search scans every document and asks a simple question: does this document contain the words "refund" and "policy"? The documents that contain these words, especially many times, get pushed to the top.

The most popular method for keyword search is called BM25. Here, we just need to understand what it does in plain words.

BM25 gives each document a score, which is a number that tells us how well the document matches the query words. A higher score means a better match. BM25 looks at two simple things:

- How often the query words appear in the document. More appearances usually mean a better match.
- How rare the query word is across all documents. A rare word like "refund" matters more than a common word like "the".

So, BM25 reads the query words, counts how they appear in each document, and gives every document a score. Then it sorts the documents from the highest score to the lowest. This sorted list is called a ranked list.

Keyword search is also called lexical search. The word "lexical" simply means "relating to words". So lexical search is word-based search. Keep this word in mind, because we will use it later.

This is how keyword search works. It is fast, simple, and great at finding exact words.

### Why keyword search alone is not enough

Now, here is the catch with keyword search.

Keyword search only understands words, not meaning. It cannot tell that two different words mean the same thing.

Let's see the problem with an example. Suppose our document says "how to return your shoes", but the user types "how to send shoes back". A human knows these mean the same thing. But keyword search sees different words. The word "return" is not the same as "send back". So keyword search may rank the correct document very low, or miss it completely.

This problem is called the synonym problem. A synonym is a different word with the same meaning, like "car" and "automobile", or "doctor" and "physician". Keyword search treats them as totally unrelated, because the letters are different.

So, the issue with keyword search is that it is blind to meaning. Let's see how the next approach solves this issue.

### What is semantic search?

The second way is semantic search.

Semantic search finds documents that have the same meaning as the query, even if they use different words.

The word "semantic" simply means "relating to meaning". So semantic search is meaning-based search.

In simple words, semantic search understands that "send shoes back" and "return your shoes" mean the same thing, and it brings up the right document even though the words are different.

Now, the question is, how does a computer understand meaning? The answer is something called an embedding.

An embedding is a list of numbers that represents the meaning of a piece of text.

Let's understand this slowly, because it is the heart of semantic search. A special model called an embedding model reads a piece of text and turns it into a long list of numbers. This list of numbers is called a vector. The amazing part is this: texts that mean similar things get similar lists of numbers, and texts that mean different things get very different lists of numbers.

So, the sentence "return your shoes" and the sentence "send shoes back" will produce two lists of numbers that are very close to each other, because they mean almost the same thing.

We can picture it as below:

```
TEXT  ->  EMBEDDING MODEL  ->  VECTOR (a list of numbers)

"return your shoes"   ->   [ 0.91, 0.12, 0.77, ... ]
"send shoes back"     ->   [ 0.89, 0.15, 0.74, ... ]   <- very close to the one above
"order a pizza"       ->   [ 0.04, 0.88, 0.21, ... ]   <- far away, different meaning

```

Here, we can see that the first two texts mean almost the same thing, so their lists of numbers are very close. The third text means something completely different, so its list of numbers is far away.

So, to do semantic search, we first turn every document into a vector ahead of time. When the user types a query, we turn the query into a vector too. Then we look for the document vectors that are closest to the query vector. The closest vectors mean the most similar meaning. This is called vector search, because we are searching using vectors. Finding these closest vectors quickly across a huge number of documents is a whole technique in itself - we have a detailed blog on Approximate Nearest Neighbor (ANN) search that explains how this works.

We can picture this closeness as points sitting in a space, like below:

```
            far away (different meaning)
                                          *  "order a pizza"

       *  "send shoes back"   (the query)
        \
         \  close by
          \
           *  "return your shoes"

                 *  "track my order"
                    (a bit farther)

```

Here, we can see that "return your shoes" sits very close to our query "send shoes back", because they mean almost the same thing. "Track my order" sits a bit farther, and "order a pizza" sits far away, because it means something completely different. Vector search simply picks the points that sit closest to the query.

Just like keyword search, vector search also gives each document a score and returns a ranked list. Here, the score is a measure of how close the document vector is to the query vector. A higher closeness score means a better match in meaning.

This is how semantic search works. It understands meaning, so it handles synonyms and rephrasing beautifully.

To learn how embeddings and Vector Databases power meaning-based search, we cover them in depth in our AI and Machine Learning Program at Outcome School.

### Why semantic search alone is not enough

Now, semantic search sounds perfect. But it has its own catch.

Semantic search is great at meaning, but it can be weak at exact, precise terms.

Let's see why with an example. Suppose a user searches for a specific product code like "SKU-48217", or an exact error code like "ERR_500", or a specific person's name, or a rare technical term. These are exact strings that must match exactly, not soft ideas about meaning.

A product code does not really have a "meaning". So semantic search may pull up documents that feel related but do not contain the exact code we asked for. It can quietly miss the one document that has the exact term.

So, here is the situation we are in:

- Keyword search is great at exact words and codes, but blind to meaning.
- Semantic search is great at meaning, but weak at exact codes and rare terms.

Each one is strong exactly where the other one is weak. So, here comes Hybrid Search to the rescue.

### What is Hybrid Search?

Hybrid Search is a technique that combines keyword search and semantic search, and merges their results into one final ranked list.

Let's decompose the term to make it clear.

> Hybrid Search = Keyword Search + Semantic Search

The word "hybrid" simply means a mix of two different things. So Hybrid Search is a mix of word-based search and meaning-based search.

In simple words, Hybrid Search runs both searches at the same time, and then combines what they found. This way, we get the exact-match power of keyword search and the meaning power of semantic search, together in one result.

Let's say we ask two helpers to find a document for us. One helper is very good at spotting exact words and codes. The other helper is very good at understanding what we actually mean. If we listen to only one of them, we lose what the other one is good at. So we ask both, and then we combine their answers. This is exactly what Hybrid Search does.

Let's connect it to what we learned. If the user searches for an exact code, keyword search catches it. If the user searches with different words for the same idea, semantic search catches it. Hybrid Search makes sure we do not lose either one.

So, Hybrid Search gives us the best of both worlds. Now, let's understand exactly how it works step by step.

### How Hybrid Search runs both searches

Hybrid Search starts by running two separate searches on the same query.

Step 1: The user types a query, for example "how to send shoes back".

Step 2: We run a lexical search using BM25. This is the keyword search. It returns a ranked list of documents, each with a BM25 score.

Step 3: At the same time, we run a vector search using embeddings. This is the semantic search. It turns the query into a vector, finds the closest document vectors, and returns its own ranked list of documents, each with a closeness score.

So, after this, we have two ranked lists. One list comes from keyword search, and one list comes from semantic search.

Let's see it as below:

```
                       Query: "how to send shoes back"
                                     |
                 +-------------------+-------------------+
                 |                                       |
          KEYWORD SEARCH                          SEMANTIC SEARCH
            (BM25)                                  (embeddings)
                 |                                       |
        ranked list A:                          ranked list B:
        1. Doc-7   (score 9.1)                  1. Doc-3   (score 0.95)
        2. Doc-2   (score 6.4)                  2. Doc-7   (score 0.88)
        3. Doc-9   (score 4.2)                  3. Doc-5   (score 0.81)

```

Here, we can see that both searches looked at the same query but returned different lists. Keyword search put Doc-7 first because it shares exact words. Semantic search put Doc-3 first because it is closest in meaning. Notice that Doc-7 appears in both lists, which is a strong hint that it is a very good match.

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

Now we have two lists. The next big question is: how do we combine them into one final list? Let's see.

### How the two result lists are combined

The step where we merge the two ranked lists into one final list is called fusion.

The word "fusion" simply means joining two things into one. So fusion means joining the keyword list and the semantic list into a single final ranking.

But, here is the catch. We cannot just add the two scores together directly. Look again at the example above. The BM25 score for Doc-7 was 9.1, while its semantic score was 0.88. These numbers live on completely different scales.

Let's understand this scale problem. BM25 scores can be any number, like 2, 6, or even 40, with no fixed top value. Semantic closeness scores usually sit between 0 and 1. So if we simply add them, the big BM25 numbers would crush the small semantic numbers. The keyword search would always win, and the semantic search would barely count. That is unfair, and it defeats the whole purpose of combining them.

So, we need a fair way to combine the two lists. There are two popular methods. The first one cleverly avoids the score problem altogether, and the second one fixes the scales first. Let's learn both.

### Reciprocal Rank Fusion (RRF)

The first and most popular method is called Reciprocal Rank Fusion, or RRF.

RRF combines the two lists using the position of each document in each list, not its raw score.

This is the clever trick. RRF ignores the messy raw scores completely. Instead, it only looks at the rank, which means the position of the document in the list. The document at the top is rank 1, the next is rank 2, and so on.

Why does this help? Because a position is just a position. Rank 1 means the same thing in both lists, whether the raw score was 9.1 or 0.88. So the scale problem disappears.

Let's understand the word "reciprocal". The reciprocal of a number is just 1 divided by that number. So the reciprocal of 2 is 1 divided by 2, which is 0.5. The reciprocal of 4 is 1 divided by 4, which is 0.25.

Here is the idea in plain words. For each document, RRF gives it points based on its rank in each list. A better rank, which means a smaller rank number, gives more points. We give points using the reciprocal of the rank. So:

- A document at rank 1 gets 1 divided by 1, which is the most points.
- A document at rank 2 gets 1 divided by 2, which is fewer points.
- A document at rank 3 gets 1 divided by 3, which is even fewer points.

Then, for each document, we add up the points it earned from both lists. The document with the most total points goes to the top of the final list.

Let's walk through our example. We will keep it simple just for the sake of understanding, as below:

```
Doc-7:  rank 1 in keyword list  ->  1/1 = 1.00
        rank 2 in semantic list ->  1/2 = 0.50
        total = 1.00 + 0.50 = 1.50

Doc-3:  not in keyword list     ->  0
        rank 1 in semantic list ->  1/1 = 1.00
        total = 0 + 1.00 = 1.00

Doc-2:  rank 2 in keyword list  ->  1/2 = 0.50
        not in semantic list    ->  0
        total = 0.50 + 0 = 0.50

```

Here, we can see that Doc-7 wins. It earned points from both lists, because it was near the top in both. Doc-3 was only strong in the semantic list, and Doc-2 was only strong in the keyword list. So Doc-7, which both searches agreed was good, rises to the top of the final list.

This is the beauty of RRF. A document that both searches like will naturally float to the top, because it collects points from both sides.

Note: In the real RRF formula, we add a small fixed number to the rank before dividing, to keep the top ranks from being too far ahead of the rest. We do not need that detail to understand the idea. The main point is that RRF uses ranks, not raw scores, so it avoids the scale problem completely.

So, RRF is simple, fair, and works very well in practice. This is why it is the most common fusion method in Hybrid Search.

### Weighted score combination and normalization

The second method is called weighted score combination.

In weighted score combination, we use the actual scores from both searches, but we first fix their scales, and then we blend them using weights.

We learned that the raw scores live on different scales, so we cannot add them directly. To solve this, we first do something called normalization.

Normalization means rescaling all the scores so that they fall into the same range, usually between 0 and 1.

In simple words, normalization is like converting two different units into one common unit, so we can compare them fairly.

After normalization, we apply a weight to each search. A weight is simply how much importance we give to each search. The weights let us tune the balance based on our use case.

Let's see the simple formula in plain words, as below:

```
final score = (weight_keyword  x  normalized keyword score)
            + (weight_semantic x  normalized semantic score)

```

Here, we can see that the final score for a document is a blend of its normalized keyword score and its normalized semantic score, each multiplied by how much we trust that search.

Let's say we set the keyword weight to 0.5 and the semantic weight to 0.5. That means we trust both searches equally. If our documents are full of exact codes and product names, we can raise the keyword weight, for example to 0.7, and lower the semantic weight to 0.3. If meaning matters more for our use case, we do the opposite.

So, the two steps for this method are simple. First, normalize the scores so they are on the same scale. Then, blend them using weights that match our use case.

Now, let me tabulate the differences between RRF and weighted score combination for your better understanding so that you can decide which one to use based on your use case.

| Point | Reciprocal Rank Fusion (RRF) | Weighted score combination |
| --- | --- | --- |
| What it uses | The rank (position) of each document | The actual normalized scores |
| Needs normalization | No, because ranks already share a scale | Yes, we must normalize first |
| Tuning control | Less control over balance | More control through weights |
| Ease of use | Very simple, works well by default | Needs more tuning to get right |

Here, we can see that RRF is the easy, reliable default, while weighted score combination gives us finer control when we are ready to tune.

### Hybrid Search in the real world

Now, let's see where Hybrid Search is used in real systems.

The biggest place where Hybrid Search shines is RAG. RAG stands for Retrieval-Augmented Generation. In simple words, it is a system where we first fetch some relevant documents and then send them to a large language model along with the user's question, so the model can answer using real, up-to-date information.

The quality of a RAG system depends heavily on the fetching step, which is called retrieval. If we fetch the wrong documents, the model gives a wrong answer, no matter how smart the model is.

There are also techniques that sharpen this retrieval step further, like HyDE, which searches with a hypothetical answer instead of the raw question, and Contextual Retrieval, which adds a short note about the source document to every chunk before indexing. We have a detailed blog on how HyDE works in RAG that explains this step by step.

We can picture where Hybrid Search fits inside RAG, like below:

```
   User question
        |
        v
  +--------------+     fetched documents       +-----+
  | HYBRID       | ------------------------>   | LLM | --> Answer
  | SEARCH       |                             +-----+
  | (retrieval)  |                                ^
  +--------------+                                |
                                            User question

```

Here, we can see that the user question first goes into Hybrid Search, which fetches the most relevant documents. Those documents and the user question are then handed to the LLM together. The LLM reads both and produces the final answer. So if Hybrid Search fetches the right documents, the LLM has the right information to answer well.

[…783ln elided…]
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

[Showing lines 1-343 and 1127-1513 of 1513; 783 middle lines (43.6KB) elided. Read artifact://45 for full output]
