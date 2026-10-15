> Source: https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms

# What is LoRA (Low-Rank Adaptation) and How Does It Fine-Tune LLMs?
URL: https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms
Published: 2026-04-24

What is LoRA (Low-Rank Adaptation) and How Does It Fine-Tune LLMs?

# What is LoRA (Low-Rank Adaptation) and How Does It Fine-Tune LLMs?

Authors
: - Name
: Amit Shekhar
Published on
: April 23, 2026

LoRA (Low-Rank Adaptation) is a way to fine-tune a large model without updating all of its weights. It keeps the original weights frozen and learns a tiny pair of extra matrices on the side.

In this blog, we will learn about LoRA - Low-Rank Adaptation of Large Language Models.

Today, we will cover the following topics:

- The Big Picture
- Why Full Fine-Tuning Is Expensive
- The Core Idea Behind LoRA
- How LoRA Works Step by Step
- A Small Numeric Example
- Where LoRA Is Applied in a Transformer
- Merging LoRA Back Into the Model
- Real-World Use Cases
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

LoRA is a way to fine-tune a large model without updating all of its weights. Instead of changing the original weight matrix, we keep it frozen and learn a tiny pair of extra matrices on the side. These tiny matrices capture the "adjustment" we want.

In simple words:

LoRA = Frozen original weights + A small low-rank update learned on the side.

This makes fine-tuning much cheaper, faster, and lighter on storage. And, we still get strong task-specific performance.

## Why Full Fine-Tuning Is Expensive

Before jumping into LoRA, we must first understand why full fine-tuning is hard.

We can learn everything about fine-tuning in this video.

A modern Large Language Model can have billions of parameters. For example, a 7 billion parameter model has 7 billion numbers inside it. When we do full fine-tuning, we update every single one of these numbers.

This causes the following issues:

- GPU memory explodes. We need to keep the weights, the gradients, and the optimizer states in memory. For Adam, this can be 3 to 4 times the size of the model itself.
- Training is slow. Updating billions of parameters takes a lot of compute.
- Storage is heavy. Each fine-tuned copy of the model is the same size as the original. If we have 10 different tasks, we need 10 full copies of a multi-gigabyte model.
- Sharing is hard. A multi-gigabyte checkpoint per task is not easy to ship to users.

We need a smarter way. We need a way to adapt the model to a new task without touching most of its weights.

So, here comes LoRA to the rescue.

## The Core Idea Behind LoRA

The full form of LoRA is Low-Rank Adaptation.

Let's decompose the name:

LoRA = Low-Rank + Adaptation.

- Adaptation means we are adapting the model to a new task or a new style.
- Low-Rank means the change we apply to the weights is represented in a very compact form using two small matrices.

The idea is based on a powerful observation from the original LoRA paper from Microsoft:

> When we fine-tune a large model, the actual update that we apply to the weights is very low-rank. We do not need a full giant update matrix - a much smaller one is enough.

In simple words, the "adjustment" needed to teach the model a new task is much smaller than the model itself. So, we do not need a giant matrix to represent it.

Why does this work? The pre-trained model already knows a lot. It has learned grammar, facts, reasoning, and general patterns. Fine-tuning it for a new task is not a rewrite. It is just a small nudge along a few important directions. That is exactly what "low-rank" means.

Let's take a real-world analogy. Think of the pre-trained model as a giant textbook. Full fine-tuning is like rewriting every page of the textbook for a new topic. LoRA is like keeping the textbook unchanged and adding a small set of sticky notes on top that carry the new knowledge. The textbook stays the same, and the small notes do the actual adjustment.

Now, let's see how this works in math.

A weight matrix `W` inside the model has shape `d x d`. In full fine-tuning, we learn a new matrix `W_new` of the same shape:

```
W_new = W + ΔW

```

Here, `ΔW` is the change we want to apply. Both `W` and `ΔW` are huge.

LoRA replaces this huge `ΔW` with a product of two small matrices:

```
ΔW = BA

```

Where:

- `A` has shape `r x d`
- `B` has shape `d x r`
- `r` is the rank, a small number like 4, 8, 16, 32, or 64
- `d` is the original dimension, often 4096 or larger

Now, `BA` still has shape `d x d`, but we never store the full `d x d` update. We only store `A` and `B`, which are tiny compared to `W`.

Note: For simplicity, we are assuming `W` is a square `d x d` matrix. In real Large Language Models, attention projection matrices are square, but feed-forward layers are not. They are usually `d x 4d` or `4d x d`. LoRA works for any rectangular matrix - if `W` has shape `d x k`, then `B` becomes `d x r` and `A` becomes `r x k`. The idea stays exactly the same.

Here is a simple ASCII diagram comparing the sizes.

```
       ΔW (full update)                 B            x            A
        (d x d matrix)              (d x r)                   (r x d)

     +-------------------+             +--+              +-------------------+
     |                   |             |  |              +-------------------+
     |                   |             |  |
     |                   |             |  |
     |                   |     =       |  |      x
     |                   |             |  |
     |                   |             |  |
     |                   |             |  |
     |                   |             |  |
     +-------------------+             +--+

```

Here, the big square is the full update we would have to store. The thin column `B` and the short row `A` together carry all the information we actually train. The visual size difference is exactly why LoRA is so memory-efficient.

The forward pass for an input vector `x` becomes:

```
h = Wx + (BA)x

```

Here, `W` is frozen. Only `A` and `B` are trained.

## How LoRA Works Step by Step

Let's walk through LoRA step by step.

Step 1: Take the pre-trained model and freeze all of its original weights. Nothing inside the original model will be updated during training.

Step 2: For each weight matrix we want to adapt, add two small matrices `A` and `B` next to it.

- `A` is initialized with small random values (Gaussian).
- `B` is initialized with all zeros.

This zero initialization is important. At the start of training, `BA = 0`, so the model behaves exactly like the original pre-trained model. Training then gradually nudges `BA` away from zero.

Step 3: During training, only `A` and `B` receive gradient updates. The original `W` stays untouched.

Step 4: During the forward pass, compute the output as:

```
h = Wx + (alpha / r) * (BA)x

```

Here, `alpha` is a scaling factor. The ratio `alpha / r` controls how strongly the LoRA update influences the output. A common choice is `alpha = 2 * r`.

Step 5: After training, we have a tiny set of new weights `A` and `B` that capture the task-specific knowledge. The original model is still untouched.

That's the entire idea.

Going back to our textbook analogy, the original textbook is the frozen `W`. The sticky notes are `A` and `B`. The notes start blank because `B` is zero. As training goes on, the notes fill up with corrections that nudge the textbook's behavior toward the new task.

Note: The choice of rank `r` is the most important LoRA hyperparameter. A smaller `r` means fewer trainable parameters and faster training, but the adapter has less capacity to learn complex changes. A larger `r` gives more capacity but loses some of the efficiency benefits. In practice, ranks of 8 to 64 work well for most tasks.

## A Small Numeric Example

Let's put this into perspective with real numbers.

Suppose we have a weight matrix `W` of shape `4096 x 4096`. The number of parameters in `W` is:

```
4096 x 4096 = 16,777,216

```

That's around 16.8 million parameters in just one matrix. A full fine-tune would update all of them.

Now, let's apply LoRA with rank `r = 8`.

- `A` has shape `8 x 4096` = 32,768 parameters
- `B` has shape `4096 x 8` = 32,768 parameters
- Total LoRA parameters = 65,536

Let's compare:

- Full fine-tune: 16,777,216 parameters per matrix
- LoRA with r=8: 65,536 parameters per matrix

That is roughly 256x fewer parameters for the same matrix. And, this is just for one matrix - the savings multiply across every layer of the model.

For a full 7B parameter model, full fine-tuning updates 7 billion parameters. LoRA with rank 8 typically updates only a few million. The trainable parameter count drops by a factor of around 1000x or more, depending on the rank and where LoRA is applied.

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

## Where LoRA Is Applied in a Transformer

LoRA can be applied to any linear layer in the model. But, in practice, LoRA is most commonly applied to the attention projection matrices.

We have a detailed blog on Transformer Architecture that explains how attention layers work inside a transformer.

Inside each attention block, we have four projection matrices:

- `W_Q` - the Query projection
- `W_K` - the Key projection
- `W_V` - the Value projection
- `W_O` - the Output projection

If we want to go deeper into how Q, K, and V are computed and used, we can read Math Behind Attention: Q, K, V.

The original LoRA paper found that adapting just `W_Q` and `W_V` is often enough to get strong task performance with minimal extra parameters. In practice, we can also apply LoRA to all four projections, or even to the feed-forward layers, for better quality at the cost of more trainable parameters.

Here is a simple ASCII diagram showing the structure for a single weight matrix.

```
              Input x
                |
        +-------+-------+
        |               |
        v               v
   +---------+      +-------+
   |  W      |      |   A   |   (trainable, r x d)
   | (frozen)|      +-------+
   +---------+          |
        |               v
        |          +---------+
        |          |    B    |   (trainable, d x r)
        |          +---------+
        |               |
        v               v
        +-------+-------+
                |
                v
        h = Wx + (BA)x

```

Here, `W` stays frozen and only `A` and `B` are trained. The two paths are added together to form the final output.

If we want to go deep into the Transformer architecture, attention, and Q/K/V projections, we have a complete program - check out our AI and Machine Learning Program at Outcome School.

## Merging LoRA Back Into the Model

Here is one of the most beautiful properties of LoRA.

Once training is done, we can merge `BA` directly into `W`:

```
W_merged = W + (alpha / r) * (BA)

```

Now, the model uses a single weight matrix `W_merged` exactly like the original. There are no extra matrices and no extra computation at inference time.

This means LoRA adds zero inference latency when merged. We get the benefits of fine-tuning without any runtime overhead.

In our textbook analogy, merging is like permanently writing the sticky notes into the textbook itself. The notes are gone, but the textbook now carries the new knowledge.

We can also keep `A` and `B` separate from `W` if we want to swap between different tasks at runtime. This is the basis of adapter swapping.

Note: Merging is a one-way operation. Once we merge `A` and `B` into `W`, we cannot easily swap that adapter out for a different one. So, if we want to serve many tasks from the same base model, we should keep the adapters unmerged and load them on demand.

This ability to merge is also what sets LoRA apart from the other Parameter-Efficient Fine-Tuning methods. We have a detailed blog on How does Prefix Tuning work? that explains a method where nothing gets merged, and a small learned prefix steers every attention layer of the frozen model instead.

## Real-World Use Cases

LoRA is everywhere in modern LLM workflows. Let's see where LoRA is used in practice.

- Fine-tuning open-source LLMs on a single GPU. Models like LLaMA, Mistral, and Qwen are commonly fine-tuned using LoRA on a single consumer or workstation GPU. Without LoRA, this would need a cluster of expensive GPUs.
- Task-specific adapters. Teams train small LoRA adapters for each task - one for summarization, one for code generation, one for customer support - and load only the adapter they need. The base model stays the same.
- Style and domain adaptation. LoRA is used to teach a base model a specific writing style, a domain like medical or legal, or a specific persona.
- Image generation models. LoRA is widely used in image models like Stable Diffusion to add new characters, styles, or concepts without retraining the whole model. The community shares thousands of small LoRA files.
- Foundation for QLoRA. LoRA is the building block for QLoRA, which combines LoRA with 4-bit quantization to fine-tune very large models on a single consumer GPU.

Because LoRA freezes the base model and trains only a small adapter, it is also a popular way to do Continual Learning in LLMs - we can teach the model new tasks without overwriting the knowledge it already has.

Note: When we ship LoRA adapters to users, we only ship the small `A` and `B` matrices. These are often just a few megabytes. Compare that to a multi-gigabyte full fine-tuned model. This is why LoRA adapters are so easy to share, swap, and version.

## Quick Summary

Let's recap what we have decoded:

- LoRA = Low-Rank Adaptation. We freeze the original weights and learn a small low-rank update on the side.
- The update is `ΔW = BA` where `A` and `B` are tiny matrices controlled by a small rank `r`.
- `A` is random, `B` is zero at the start. This makes the model start exactly like the original pre-trained model.
- Only `A` and `B` are trained. The original `W` stays frozen, which saves massive amounts of memory and compute.
- Trainable parameters drop by 100x to 1000x or more depending on the rank and where LoRA is applied.
- LoRA can be merged into the original weights after training, so there is zero extra latency at inference time.
- Adapter swapping lets us serve many tasks from a single base model by loading different `A` and `B` matrices.
- LoRA is used everywhere - LLMs, image models, domain adaptation, and as the foundation for QLoRA.

This is how LoRA makes fine-tuning of Large Language Models cheap, fast, and accessible.

### Does LoRA slow down inference?

No. Once training is done, we can merge `BA` directly into the original weight matrix. The model then uses a single weight matrix exactly like the original, with no extra matrices and no extra computation. So, LoRA adds zero inference latency when merged.

### What rank should we choose for LoRA?

In practice, ranks of 8 to 64 work well for most tasks. A smaller rank means fewer trainable parameters and faster training, but less capacity to learn complex changes. A larger rank gives more capacity but loses some of the efficiency benefits. The rank is the most important LoRA hyperparameter.

### Why is the matrix B initialized with zeros?

Because at the start of training, `BA` becomes zero. This makes the model behave exactly like the original pre-trained model. Training then gradually nudges `BA` away from zero, while `A` starts with small random values.

### Can one base model serve many tasks with LoRA?

Yes. Teams train small LoRA adapters for each task and load only the adapter they need, while the base model stays the same. To do this, we should keep the adapters unmerged, because merging is a one-way operation and a merged adapter cannot easily be swapped out.

### What is the relation between LoRA and QLoRA?

LoRA is the building block for QLoRA. QLoRA combines LoRA with 4-bit quantization to fine-tune very large models on a single consumer GPU.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# What is Contrastive Learning? How It Works Step by Step
URL: https://outcomeschool.com/blog/contrastive-learning
Published: 2026-05-20
Author: Amit Shekhar

What is Contrastive Learning? How It Works Step by Step

# What is Contrastive Learning? How It Works Step by Step

Authors
: - Name
: Amit Shekhar
Published on
: May 20, 2026

Contrastive Learning is a way of teaching a model by comparing things. The model learns to pull similar things close to each other and push different things far apart.

In this blog, we will learn about Contrastive Learning. We will also see how it works step-by-step and where it is used in the real world.

We will cover the following:

- What is Contrastive Learning?
- Why do we need Contrastive Learning?
- The key idea behind Contrastive Learning.
- Positive pairs and Negative pairs.
- How does Contrastive Learning work step-by-step?
- Loss functions used in Contrastive Learning.
- Popular Contrastive Learning methods.
- Real-world use cases of Contrastive Learning.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Contrastive Learning?

Contrastive Learning is a way of teaching a model to learn good representations of data by comparing things. The model learns to pull similar things close to each other and push dissimilar things far apart in a representation space.

In simple words, Contrastive Learning = Contrast + Learning. We learn by contrasting one thing with another.

Let's say we have two photos of the same cat, taken from different angles. These two photos are similar. They should be close to each other in the representation space. Now, consider a photo of a car. This is very different from the cat photos. It should be far away from them.

This is the core idea of Contrastive Learning.

Similar things attract each other and stick together. Dissimilar things repel each other and move apart. Contrastive Learning teaches the model to behave like these magnets.

### Why do we need Contrastive Learning?

Before jumping into how it works, we must understand the problem it solves.

In traditional supervised learning, we need labeled data. For every image, we need a human to tell us "this is a cat", "this is a dog", and so on. Labeling data is expensive. It is slow. It needs a lot of human effort.

But, here is the catch. The internet has billions of images, videos, and pieces of text. Only a very small fraction of this data is labeled. We have huge amounts of unlabeled data available, but we cannot use it directly with supervised learning.

So, here comes Contrastive Learning to the rescue.

Contrastive Learning does not need any labels from humans. It is a self-supervised learning technique. The model creates its own labels from the data itself. This way, we can train the model on massive amounts of unlabeled data and still learn very useful representations.

Once these representations are learned, we can reuse them for many downstream tasks like classification, search, clustering, and etc., with very little labeled data.

This is the beauty of Contrastive Learning.

### The key idea behind Contrastive Learning

[…298ln elided…]

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

[Showing lines 1-418 and 717-1041 of 1041; 298 middle lines (17.8KB) elided. Read artifact://84 for full output]
