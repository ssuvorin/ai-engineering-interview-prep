> Source: https://outcomeschool.com/blog/decoding-colbert

# What is ColBERT? Late Interaction Retrieval Explained
URL: https://outcomeschool.com/blog/decoding-colbert
Published: 2026-08-12
Author: Amit Shekhar

What is ColBERT? Late Interaction Retrieval Explained

# What is ColBERT? Late Interaction Retrieval Explained

Authors
: - Name
: Amit Shekhar
Published on
: August 12, 2026

ColBERT is a retrieval method that keeps the word-by-word matching of a slow BERT reranker, but makes it fast enough to search millions of passages, using a trick called late interaction.

In this blog, we are going to learn about ColBERT, a retrieval method that keeps the fine-grained, word-by-word matching of a slow BERT reranker but makes it fast enough to search millions of passages, using a clever trick called late interaction.

We will cover the following:

- What is the ColBERT paper?
- The building blocks we must know first
- The big picture: what ColBERT does
- The two old extremes
- Late interaction: the key idea
- Encoding the query and document
- The MaxSim operation
- Why max, not average
- Ranking documents
- Training: positives and negatives
- The loss with small numbers
- Fast retrieval at scale
- The cost of a bigger index
- The Results
- Where ColBERT led
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is the ColBERT paper?

ColBERT encodes the query and each document into a bag of per-token vectors, separately, so documents can be encoded ahead of time. At search time it scores relevance with a cheap operation called MaxSim. This keeps the word-level detail of a slow BERT reranker while being fast enough to search millions of passages.

ColBERT was introduced in 2020 in the paper "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT" by Omar Khattab and Matei Zaharia at Stanford. The name means Contextualized Late Interaction over BERT.

BERT itself is an encoder-only transformer, the half that reads a text in both directions and builds a deep understanding of every token in it. We have a detailed blog on Encoder vs Decoder in Transformers that explains how each half works.

## The building blocks we must know first

Before jumping into the paper, we must know a few simple words. Do not worry, each one is just a plain idea.

- Token - a word or word-piece, the unit the model reads.
- Embedding - a vector capturing the meaning of a token.
- Cosine similarity - a score from -1 to 1 for how aligned two vectors are. For unit-length vectors, it equals their dot product.
- Reranker - a model that re-scores a small set of candidate documents for relevance.
- Offline / online - work done ahead of time (offline) versus at query time (online).

That is everything we need. Now, let's move to the big picture.

## The big picture: what ColBERT does

Before going into the details, let's see the simple input-to-output view.

```
   Document  ->  BERT  ->  a bag of per-token vectors   (done OFFLINE, once)

   Query     ->  BERT  ->  a bag of per-token vectors   (done at query time)
                                  |
                                  v
              cheap MaxSim score between the two bags  ->  relevance

```

The whole trick: encode the query and the document separately into per-token vectors, so all documents can be pre-computed offline. At query time, only a cheap scoring step runs. Let's decode why this is such a good middle ground.

## The two old extremes

Before ColBERT, BERT-based retrieval came in two flavors, each with a flaw.

- Cross-encoder (accurate but slow): feed the query and document together into BERT, so every query word attends to every document word. Very accurate, but BERT must run from scratch for every query-document pair. Nothing can be precomputed. On millions of passages, this is impossibly slow (the paper measured one BERT reranker at over 10 seconds per query).
- Single-vector dual encoder (fast but blunt): encode the whole query into one vector and the whole document into one vector, then take a single dot product. This is the DPR style: fast and precomputable, but squashing a whole passage into one vector loses word-level detail, so quality drops.

Let's put the two of them side by side, along with the one ColBERT proposes:

```
  1. Cross-encoder  (accurate, slow)

     query + document together  ->  BERT  ->  score
     BERT runs once per pair, nothing can be stored ahead of time

  2. Single-vector dual encoder  (fast, blunt)

     query     ->  BERT  ->  [ one vector ]
                                          >--  one dot product  ->  score
     document  ->  BERT  ->  [ one vector ]

  3. Late interaction, ColBERT  (accurate and fast)

     query     ->  BERT  ->  [ v1  v2  v3 ]
                                          >--  MaxSim  ->  score
     document  ->  BERT  ->  [ v1  v2  v3  v4  v5 ]

```

Here, we can see the difference clearly. In the first one, the query and the document go into BERT together, so nothing can be stored ahead of time. In the second one, they go in separately, but each side is squeezed into a single vector, so the word-level detail is lost. In the third one, they go in separately and each side keeps one vector per token, so we get both.

The second one is the style behind most vector search running today. We have a detailed blog on how Semantic Search works that explains that single-vector flow step by step.

So the question was: can we keep the word-level detail of the cross-encoder, but still precompute documents like the dual encoder? The third row is the answer, and we will decode it next.

## Late interaction: the key idea

ColBERT's answer is late interaction. Encode the query and document into bags of per-token vectors, separately. Because the document encoder never sees the query, every document's vectors can be computed once, offline, and stored.

The word-level interaction still happens, but late: after both sides are encoded, and through a cheap operation instead of inside BERT. This is the difference from the single-vector model, which has almost no token-level interaction at all. ColBERT keeps "every query word can find its match in the document", just done cheaply.

## Encoding the query and document

A single BERT is shared for both, told which is which by a marker token:

- The query gets a `[Q]` marker. Short queries are padded with `[MASK]` tokens up to a fixed length, and BERT fills those positions with useful extra terms, a kind of learned query expansion.
- The document gets a `[D]` marker, and punctuation tokens are dropped to save space.

Each token vector is then projected down to a small size (128 numbers) and made unit-length. So a document becomes a matrix of token vectors, not a single vector. Making the vectors unit-length means cosine similarity is just a dot product:

```
q1 = [0.6, 0.8, 0.0]   (length = sqrt(0.36 + 0.64) = 1)
d1 = [0.8, 0.6, 0.0]   (length = sqrt(0.64 + 0.36) = 1)

dot = 0.6*0.8 + 0.8*0.6 + 0.0*0.0 = 0.48 + 0.48 = 0.96

```

Because both are unit length, this `0.96` is their cosine similarity.

To learn Tokenization, Embeddings, and Transformer Architecture in depth, check out our AI and Machine Learning Program at Outcome School.

## The MaxSim operation

Now the heart of ColBERT: scoring a document with MaxSim. This is the one formula of the paper:

```
S(q, d) = sum over i of ( max over j of ( Eq_i · Ed_j ) )

```

First, let's define every symbol:

- `S(q, d)` is the relevance score of document `d` for query `q`
- `Eq_i` is the vector of the i-th query token
- `Ed_j` is the vector of the j-th document token
- `·` is the dot product, which here is the cosine similarity, because we made every vector unit length in the previous section
- `max over j` means: for one query token, take its best match across all the document tokens
- `sum over i` means: add up those best matches over all the query tokens

So the rule in plain words is: for each query token, find its best-matching document token, then sum those best matches.

Let's compute it with a 2-token query and a 3-token document. We keep the same `q1` and `d1` from the previous section, so one of the numbers is already familiar. Our tiny vectors, all unit length:

```
Query tokens                Document tokens
q1 = [0.6, 0.8, 0.0]        d1 = [0.8, 0.6, 0.0]
q2 = [0.0, 0.6, 0.8]        d2 = [0.0, 0.0, 1.0]
                            d3 = [1.0, 0.0, 0.0]

```

Step 1: the dot product of every query token with every document token, term by term.

```
q1 · d1 = 0.6*0.8 + 0.8*0.6 + 0.0*0.0 = 0.48 + 0.48 + 0.00 = 0.96
q1 · d2 = 0.6*0.0 + 0.8*0.0 + 0.0*1.0 = 0.00 + 0.00 + 0.00 = 0.00
q1 · d3 = 0.6*1.0 + 0.8*0.0 + 0.0*0.0 = 0.60 + 0.00 + 0.00 = 0.60

q2 · d1 = 0.0*0.8 + 0.6*0.6 + 0.8*0.0 = 0.00 + 0.36 + 0.00 = 0.36
q2 · d2 = 0.0*0.0 + 0.6*0.0 + 0.8*1.0 = 0.00 + 0.00 + 0.80 = 0.80
q2 · d3 = 0.0*1.0 + 0.6*0.0 + 0.8*0.0 = 0.00 + 0.00 + 0.00 = 0.00

```

Putting those six numbers into a small table:

```
              d1     d2     d3
   q1  ->  [ 0.96   0.00   0.60 ]
   q2  ->  [ 0.36   0.80   0.00 ]

```

Step 2: take the max along each row, which means the best document token for each query token.

```
   q1: max(0.96, 0.00, 0.60) = 0.96   (best match is d1)
   q2: max(0.36, 0.80, 0.00) = 0.80   (best match is d2)

```

Step 3: sum those maxima.

```
   score = 0.96 + 0.80 = 1.76

```

So the document scores `1.76`. In words: each query word found its best home in the document (q1 at d1, q2 at d2), and we added up how well each query word was matched.

Here, we have used 3-number vectors, a 2-token query, and a 3-token document, just for the sake of understanding. In the real ColBERT, every vector has 128 numbers, the query is padded to 32 tokens, and a passage can run to a few hundred tokens, so the table above becomes a 32 by 300 grid of numbers. The steps stay exactly the same.

Let's look at the formula once more:

```
S(q, d) = sum over i of ( max over j of ( Eq_i · Ed_j ) )

```

Now, every part of this formula is clear. The dot product is the similarity of one query token to one document token, the max picks the best document token for that query token, and the sum adds those best matches over the whole query.

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

## Why max, not average

Why take the max over document tokens, not the average? Because a document is relevant if it contains a good match for a query word, even if most of its other words are unrelated.

Let's take the q1 row we just computed and try both.

```
q1 similarities to the document: [0.96, 0.00, 0.60]

MaxSim uses:   0.96        (rewards the single strong match)
Average gives: (0.96 + 0.00 + 0.60) / 3 = 1.56 / 3 = 0.52   (dilutes the strong match)

```

The average is barely half of the max, and the only thing that changed it is `d2`, a token that has nothing to do with the query. Now, imagine the same passage with 200 more unrelated tokens. The average would keep falling towards zero, while the max would stay at `0.96`.

The max captures "does the document contain a token that means the same as this query word?". An average would drown that strong `0.96` match in irrelevant tokens. So max is the right choice.

## Ranking documents

To rank, we compute MaxSim for each candidate and sort. We scored document A at `1.76` above. Now, take a document B with two tokens:

```
b1 = [1.0, 0.0, 0.0]
b2 = [0.8, 0.0, 0.6]

```

The same three steps, with the same query tokens:

```
q1 · b1 = 0.6*1.0 + 0.8*0.0 + 0.0*0.0 = 0.60
q1 · b2 = 0.6*0.8 + 0.8*0.0 + 0.0*0.6 = 0.48
q2 · b1 = 0.0*1.0 + 0.6*0.0 + 0.8*0.0 = 0.00
q2 · b2 = 0.0*0.8 + 0.6*0.0 + 0.8*0.6 = 0.48

   q1: max(0.60, 0.48) = 0.60
   q2: max(0.00, 0.48) = 0.48

   score(B) = 0.60 + 0.48 = 1.08

```

Since `1.76 > 1.08`, ColBERT ranks document A above document B. The summed maxima turn directly into a ranking. Notice why B lost: neither of its tokens is a strong home for `q2`, the best it can offer is `0.48`, while document A had `d2` sitting at `0.80`.

## Training: positives and negatives

Till now, we have learned how ColBERT scores a document. Now, the question is: where do these vectors come from? BERT does not know by itself that a query token and a document token should point the same way. It has to be taught, and it is taught with examples.

ColBERT is trained on triples, and each triple has three parts:

```
   <  q  ,  d+  ,  d-  >

   q   =  the query
   d+  =  a passage that DOES answer the query   (the positive)
   d-  =  a passage that does NOT answer it      (the negative)

```

For one triple, we run MaxSim twice, once for `d+` and once for `d-`, and we get two scores. The training goal is simple to say: make the score of the positive higher than the score of the negative.

That's the beauty of this training setup. We never tell the model what any individual vector must be. We only tell it which of the two documents should win. Over millions of triples, BERT slowly learns to place a query token and the document tokens that answer it in the same direction, which is exactly what makes `q1 · d1 = 0.96` possible.

Teaching a model by pulling a positive closer and pushing a negative away is the core idea of Contrastive Learning, and we have a detailed blog on it that covers this end to end.

## The loss with small numbers

To turn "the positive must win" into a number the model can reduce, ColBERT uses a pairwise softmax cross-entropy loss over the two scores. Let's compute it with the two scores we already have.

Let's say `d+` is document A, which scored `1.76`, and `d-` is document B, which scored `1.08`.

Step 1: take `e` to the power of each score.

```
e^1.76 = 5.812
e^1.08 = 2.945

```

Step 2: add them to get the total.

```
5.812 + 2.945 = 8.757

```

Step 3: divide the positive's value by the total. This is the softmax probability of picking the right document.

```
p = 5.812 / 8.757 = 0.664

```

Step 4: the loss is the negative natural log of that probability.

```
loss = -ln(0.664) = 0.41

```

So the loss for this triple is `0.41`. Now, let's see what happens after training pushes the two scores apart, say the positive rises to `2.5` and the negative falls to `0.5`:

```
e^2.5 = 12.182
e^0.5 = 1.649

p    = 12.182 / (12.182 + 1.649) = 12.182 / 13.831 = 0.881
loss = -ln(0.881) = 0.13

```

The loss dropped from `0.41` to `0.13`. Here, we can see that the loss only goes down when the gap between the positive and the negative grows. That single pressure, applied over millions of triples, is what teaches every token vector where to point.

## Fast retrieval at scale

MaxSim is not just cheap. It is also pruning-friendly. Each query token can independently look up its nearest document tokens in a vector index, without scoring every document. This lets ColBERT work in two modes:

- Reranking: re-score the top candidates from a cheap first stage.
- End-to-end retrieval: index all document token vectors and retrieve straight from millions of passages, in two stages (an approximate nearest-neighbor filter, then exact MaxSim on the survivors).

This is exactly what a cross-encoder cannot do, because its document representation depends on the query.

## The cost of a bigger index

Every design has a price, and we must be honest about the price ColBERT pays. Storing one vector per token instead of one vector per passage makes the index much bigger.

Let's compute it for a single passage of 100 tokens:

```
Single-vector model:  1 vector   x 128 numbers =     128 numbers
ColBERT:              100 vectors x 128 numbers =  12,800 numbers

```

That is 100 times more storage for the same passage. Multiply that by 8.8 million passages and the index for MS MARCO comes to about 154 GB, while a single-vector index for the same passages fits in a few gigabytes.

So ColBERT buys its accuracy with disk space.

## The Results

ColBERT nearly matched a full BERT reranker's quality at a tiny fraction of the cost. On the MS MARCO passage benchmark:

| Method | Quality (MRR@10) | Reranking latency |
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
