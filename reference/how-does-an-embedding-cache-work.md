> Source: https://outcomeschool.com/blog/how-does-an-embedding-cache-work

# How does an Embedding Cache work?
URL: https://outcomeschool.com/blog/how-does-an-embedding-cache-work
Published: 2026-06-21
Author: Amit Shekhar

How does an Embedding Cache work?

# How does an Embedding Cache work?

Authors
: - Name
: Amit Shekhar
Published on
: June 21, 2026

An Embedding Cache is a place where we store the embeddings that we have already computed, so that the next time we need the embedding for the same text, we reuse the stored one instead of computing it again.

In this blog, we will learn about how an Embedding Cache works. We will also see what an embedding is, why an Embedding Cache saves us a lot of money and time, how the cache key is built, and where it is used in real systems like RAG and semantic search.

We will cover the following:

- What is an embedding?
- A quick recap of how we get an embedding
- What is an Embedding Cache?
- Why we need an Embedding Cache
- The core idea behind an Embedding Cache
- The cache key, a hash of the text plus the model
- The request flow, a hit and a miss
- Eviction, LRU and TTL
- Where the cache lives, memory or disk
- The benefits of an Embedding Cache
- An Embedding Cache in the real world

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is an embedding?

Before we talk about an Embedding Cache, we must first understand what an embedding is.

An embedding is a list of numbers that represents the meaning of a piece of text.

In simple words, an embedding is the way a computer turns words into numbers, so that it can understand and compare them.

Let's say we have the sentence "I love dogs." A computer does not understand words the way we do. So, we pass this sentence through a special model, and it gives us back a long list of numbers, for example `[0.12, -0.85, 0.33, ...]`. This list of numbers is the embedding.

The magic is in what these numbers capture. Two pieces of text that mean similar things get embeddings that are close to each other. Two pieces of text that mean very different things get embeddings that are far apart. So, "I love dogs" and "I adore puppies" will have embeddings that sit close together, while "I love dogs" and "The stock market crashed" will have embeddings that sit far apart.

We can picture this closeness like below:

```
   meaning space (close means similar, far means different)

      "I love dogs"  *
                      \
                       * "I adore puppies"   (close together, similar meaning)

                                        * "The stock market crashed"
                                          (far away, different meaning)

```

Here, we can see that "I love dogs" and "I adore puppies" sit close together because they mean similar things, while "The stock market crashed" sits far away because it means something very different. The closer two embeddings sit, the more similar their meaning.

This is incredibly useful. Once text becomes numbers, the computer can measure how similar two pieces of text are just by checking how close their numbers are. This is the foundation of search systems that understand meaning, not just exact words.

Why similar meanings land close together and different ones land far apart comes down to how the model is trained - we have a detailed blog on Contrastive Learning that explains this approach step by step.

Now, here is something important to notice. To get this list of numbers, we have to send the text to a model and ask it to compute the embedding. This step is not free. We will come back to this point soon, because it is the heart of the Embedding Cache.

### A quick recap of how we get an embedding

To understand the Embedding Cache, we must understand one thing about how we get an embedding.

We do not compute embeddings by hand. We use an embedding model. An embedding model is a special model whose only job is to take text and return its embedding, that list of numbers we just talked about.

So, the flow is simple. We send some text to the embedding model, and it sends back the embedding.

We can picture it as below:

```
   "I love dogs"   -->   [ Embedding Model ]   -->   [0.12, -0.85, 0.33, ...]
       (text)                (does work)                  (the embedding)

```

Here, we can see that the text goes in on the left, the embedding model does some work in the middle, and the list of numbers comes out on the right.

Now, here is the key point to remember.

Asking the embedding model to compute an embedding costs real money and real time.

Most embedding models run on a server, and we usually pay based on how much text we send. Even if we run the model on our own machine, computing an embedding uses real computing power and takes real time. So, every single embedding we compute has a cost, both in money and in delay.

So, if we ask the model to compute the embedding for the same text many times, we pay for the same work again and again. That is wasteful.

This is the foundation we needed. Now we are ready to understand the problem.

To learn how embeddings work and how they power modern AI systems, we cover Embeddings from the ground up in our AI and Machine Learning Program at Outcome School.

### What is an Embedding Cache?

Now that we know how we get an embedding, let's understand the Embedding Cache.

An Embedding Cache is a place where we store embeddings we have already computed, so that the next time we need the embedding for the same text, we grab the stored one instead of computing it again.

In simple words, an Embedding Cache means: compute the embedding once, then reuse it.

The word "cache" simply means a place where we store something so we can grab it quickly later, instead of making it again from scratch.

Let's connect this to what we just learned. Computing an embedding costs money and time. So, the first time we compute the embedding for a piece of text, we save it in the cache. The next time we need the embedding for that exact same text, we do not call the embedding model at all. We simply look it up in the cache and return the saved list of numbers.

So, an Embedding Cache is about never paying to compute the embedding for the same text twice.

Now, the question is, why do we even need this? Let's see.

### Why we need an Embedding Cache

The same text comes up again and again, far more often than we would expect. Let's understand this with two common situations.

The first situation is re-ingestion. Ingestion means the process of taking our documents, breaking them into small pieces, and computing an embedding for each piece so we can search them later. Now, suppose we update one paragraph in a large document and run the ingestion again. Most of the document did not change at all. But if we are not careful, we recompute the embedding for every single piece, even the ones that are exactly the same as before. We pay all over again for work we already did.

We can picture this re-ingestion like below:

```
   document broken into pieces, then re-ingested after editing one piece

   piece 1   unchanged   -->  reuse from cache   (free)
   piece 2   unchanged   -->  reuse from cache   (free)
   piece 3   EDITED      -->  compute again      (pay once)
   piece 4   unchanged   -->  reuse from cache   (free)
   piece 5   unchanged   -->  reuse from cache   (free)

```

Here, we can see that only piece 3 changed, so only piece 3 needs a new embedding. With a cache, the four unchanged pieces are reused for free. Without a cache, we would recompute all five, paying for work we already did.

The second situation is repeated queries. Imagine we have a search system used by thousands of people. Many people search for the same popular things. Hundreds of users type the same query, such as "return policy" or "reset my password." Each time, we need the embedding of that query to search. Without a cache, we compute the embedding for "return policy" hundreds of times, even though it is the exact same text every time.

Let's put some numbers to it for the sake of understanding. Suppose:

- A popular query is searched 1,000 times in a day.
- Without a cache, we compute its embedding 1,000 times.
- With a cache, we compute it once and reuse it 999 times.

That is 999 calls saved for just one popular query.

This causes two real problems when we have no cache:

- It is costly. We pay for every embedding we compute. Recomputing the same embedding again and again means we pay for the same work over and over.
- It is slow. Calling the embedding model adds delay. If the model runs on a server, we also wait for the network. Doing this for text we have already processed adds delay for no reason.

So, here comes the Embedding Cache to the rescue.

### The core idea behind an Embedding Cache

Let's understand the core idea step by step.

We learned that computing an embedding is the costly part. The Embedding Cache takes a simple but powerful step.

The idea is to store every embedding we compute, paired with the text it came from. Before computing a new embedding, we first check the cache. If the embedding for that text is already there, we reuse it and skip the costly computation.

Let's walk through it with our example.

Step 1: A user searches for "return policy." We check the cache. The embedding is not there yet, because this is the first time. So, we call the embedding model, get the embedding, and save it in the cache. Then we use it for the search.

Step 2: Another user searches for "return policy" later in the day. We check the cache. This time, the embedding is already there, because we saved it in Step 1. So, we skip the embedding model completely and use the saved embedding directly.

So, the second search did not pay any cost to compute the embedding. It simply read the saved one.

Let's see a simple diagram to make this clear as below:

```
WITHOUT an embedding cache (every time):

   "return policy"  -->  call the model  -->  compute embedding   (slow, costly, repeated)

WITH an embedding cache (after the first time):

   "return policy"  -->  found in cache  -->  return saved embedding   (fast, cheap)
                         skip the model

```

The problem is solved. We now compute the embedding for a piece of text only once. So, for our popular query searched 1,000 times, we pay for one computation and reuse it the other 999 times.

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

### The cache key, a hash of the text plus the model

Now, there is one very important detail we must understand, because this is what makes the cache reliable.

To store and find something in a cache, we need a key. A key is a label we attach to a stored item, so we can find it again later. Think of it like the name on a folder in a filing cabinet. We need the right name to pull out the right folder.

So, the question is, what should we use as the key for an embedding?

The simplest answer is to use the text itself. But there are two problems with using the raw text directly. First, the text can be very long, like an entire paragraph, which makes for a clumsy key. Second, and much more important, the same text can be sent to different embedding models, and each model produces a different embedding for the same text.

Let's understand this clearly. Suppose we have two embedding models, an older one and a newer one. We send "return policy" to both. They return different lists of numbers, because they are different models. The same thing happens if we simply upgrade one model to a new version, because a new version also produces different numbers. If our key was just the text "return policy," then both models would try to use the same cache spot. The newer model would read the older model's embedding and get the wrong numbers. This is called a collision, which means two different things accidentally landing on the same key.

So, here is the rule we must follow.

The cache key is built from the text plus the model name and version. This way, different models never collide.

To turn this into a short, neat key, we use a hash. A hash is a function that takes any input, no matter how long, and turns it into a short fixed-length string of characters. The same input always produces the same hash, and even a tiny change in the input produces a completely different hash. So, a hash is a perfect way to make a compact, unique key from a long piece of text.

We can picture the key like below:

```
   text:  "return policy"
   model: "text-embedding-v3"
                  |
                  v
        combine them together
                  |
                  v
            apply a hash
                  |
                  v
   key:  "a3f9c1...b27"   (short, unique, model-specific)

```

Here, we can see that we take the text and the model name together, then run them through a hash to get a short unique key. Because the model name is part of the key, the older model and the newer model get different keys for the same text, so they never read each other's embeddings.

This is how the cache stays correct even when we use more than one embedding model.

### The request flow, a hit and a miss

Now, let's put the whole thing together and walk through exactly what happens on a single request.

Before that, we must learn two simple words.

A cache hit means the embedding we are looking for is already in the cache. We found it, so we reuse it.

A cache miss means the embedding is not in the cache yet. We did not find it, so we have to compute it.

Let's see the full flow as below:

```
   request: need embedding for some text
                  |
                  v
        hash the text + model name  -->  get the key
                  |
                  v
        is the key in the cache?
            |                 |
           YES               NO
        (cache HIT)       (cache MISS)
            |                 |
            v                 v
     return the saved    call the embedding model
        embedding         and compute it
                              |
                              v
                        store it in the cache
                        under the key
                              |
                              v
                        return the embedding

```

Here, we can see the complete journey. First, we take the text and the model name and hash them to get the key. Then, we check whether that key is already in the cache. If it is a hit, we return the saved embedding right away and we are done, no model call needed. If it is a miss, we call the embedding model, compute the embedding, store it in the cache under that key, and then return it.

Notice the beautiful part. After a miss, we store the result. So, the very next time the same text comes in, it becomes a hit. The first request pays the cost, and every request after that for the same text is fast and free.

The problem is solved. Every piece of text is computed at most once.

### Eviction, LRU and TTL

Now, the next question is, does the cache keep growing forever? The answer is no. A cache has limited space, and we cannot store everything forever. So, at some point, we must remove old items to make room for new ones. This removing of items is called eviction.

In simple words, eviction is the cache throwing out some old stored items so it does not run out of space.

There are two common ways to decide what to evict. Let's understand both.

The first way is LRU, which stands for Least Recently Used. The idea is simple. When the cache is full and we need room, we throw out the item that has not been used for the longest time. The thinking is that if we have not needed an embedding in a long while, we probably will not need it soon, so it is the safest one to remove.

Let's understand LRU with a small example as below:

```
   Cache is full. We need to add a new item.

   item A  -->  last used 1 minute ago
   item B  -->  last used 2 minutes ago
   item C  -->  last used 30 minutes ago   <-- least recently used, evict this one

```

Here, we can see that item C has not been used for the longest time, so LRU picks it for eviction. We remove item C and use that freed space for the new item.

The second way is TTL, which stands for time to live. TTL is how long an item is allowed to stay in the cache before it expires and gets removed, no matter what. For example, if we set a TTL of one hour, then every stored embedding is removed one hour after it was saved.

TTL is useful when our text or our model can change over time and we do not want to keep old embeddings forever. The word "stale" simply means old and no longer fresh. LRU is useful when we simply have limited space and want to keep the items we use most often.

Note: We can even use both together. We keep popular items with LRU, and we still let everything expire after the TTL, so nothing stays stale forever. We choose the eviction strategy based on our use case.

So, eviction keeps our cache from growing out of control while keeping the useful items around.

### Where the cache lives, memory or disk

Now, let's understand where this cache actually lives. There are two common choices, and each one fits a different need.

The first choice is in-memory, often using a tool called Redis. In-memory means the cache lives in the computer's memory, which is the fast working space of a computer. Redis is a popular tool that stores data in memory and gives it back extremely quickly. Looking up an embedding from an in-memory cache is very fast, often a tiny fraction of a second. This is great for repeated queries in a live system, where speed matters the most.

The second choice is on disk. On disk means the cache lives in files on the hard drive. Disk is slower than memory, but it can hold far more data, and the data stays even if the program restarts. This is great for ingestion, where we may compute embeddings for millions of document pieces and want to keep them around for a long time, even across restarts.

We can compare the two as below:

```
   IN-MEMORY (like Redis)        ON DISK
   ----------------------        ----------------------------
   very fast lookups             slower lookups
   limited space                 large space
   lost on restart               kept across restarts
   good for live queries         good for big ingestion jobs

```

Here, we can see that in-memory is fast but limited and temporary, while on disk is slower but roomy and lasting. Many real systems use both together, a fast in-memory cache in front and a larger disk cache behind it.

So, we pick where the cache lives based on our use case.

Keeping an AI system fast and cheap at scale - decisions like where a cache lives and how we serve it - is exactly what LLM Inference Engineering is about, and we cover it end to end in our AI and Machine Learning Program at Outcome School.

### The benefits of an Embedding Cache

Let's quickly bring together the benefits, because they are the reason we use this technique.

- Lower cost. We pay to compute an embedding only the first time for any given text. Every repeat is served from the cache for free. For popular queries and for re-ingestion of mostly unchanged documents, this saves a huge amount of money.
- Lower latency. Latency means the delay before we get a result. Reading from the cache is far faster than calling the embedding model. This matters even more when the model runs on a server, because then we also skip the wait for the network. So, our system feels faster.

In simple words, an Embedding Cache makes our application cheaper and faster at the same time, without changing the quality of the results. The embeddings are exactly the same numbers we would have computed. We just avoid computing them more than once.

That's the beauty of an Embedding Cache.

### An Embedding Cache in the real world

Now, let's see where an Embedding Cache is used in real systems.

The first place is RAG. RAG stands for Retrieval-Augmented Generation. In simple words, it is a system where we first fetch some relevant documents and then send them to a large language model along with the user's question. RAG depends on embeddings in two places. During ingestion, we compute an embedding for every piece of every document. During a query, we compute an embedding for the user's question to find the matching pieces. An Embedding Cache helps in both places. It saves the embeddings of document pieces so re-ingestion does not recompute the unchanged ones, and it saves the embeddings of popular queries so we do not recompute them for every user.

The second place is semantic search. Semantic search means searching by meaning instead of by exact words. The word "semantic" simply means related to meaning. In semantic search, we turn both the documents and the user's query into embeddings, then we find the documents whose embeddings are closest to the query's embedding. Finding those nearest embeddings fast across millions of documents is exactly what Approximate Nearest Neighbor (ANN) search does. Just like in RAG, the same documents and the same popular queries come up again and again. So, an Embedding Cache cuts down the cost and the delay here too.

So, anywhere we keep computing embeddings for the same text, whether during document ingestion or for repeated and popular queries, an Embedding Cache helps us a lot.

The same embeddings also power semantic caching, where we reuse a past answer whenever a new question means the same thing as an old one, so we can skip calling the model again.

This is how an Embedding Cache works. We compute the embedding for a piece of text once, we store it under a key built from a hash of the text plus the model name and version, and then we reuse it on every later request for the same text, while eviction with LRU or TTL keeps the cache from growing forever, so we get cheaper and faster results.

### Does an Embedding Cache change the quality of search results?

No. An Embedding Cache does not change the quality of the results. The cached embeddings are exactly the same numbers we would have computed by calling the model again. We just avoid computing them more than once, which makes the application cheaper and faster at the same time.

### What is the difference between an Embedding Cache and a Semantic Cache?

An Embedding Cache reuses the embedding for the exact same text, so we skip calling the embedding model. Semantic caching reuses a past answer whenever a new question means the same thing as an old one, so we skip calling the model that writes the answer. Both rely on embeddings, but they save different work.

### Will a similar but not identical text hit the Embedding Cache?

No. The cache key is a hash of the text plus the model name and version. The same input always produces the same hash, but even a tiny change in the input produces a completely different hash. So, only the exact same text sent to the same model becomes a cache hit.

### What happens to cached embeddings when we upgrade the embedding model?

The new model version gets its own keys, so it never reads the old model's embeddings. This is why the model name and version are part of the cache key. Without them, the new model could read the old embeddings and get the wrong numbers. A TTL also helps here, because old embeddings expire instead of staying stale forever.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:
