> Source: https://outcomeschool.com/blog/grouped-query-attention

# What is Grouped Query Attention (GQA) and Why Do LLMs Use It?
URL: https://outcomeschool.com/blog/grouped-query-attention
Published: 2026-04-22
Author: Amit Shekhar

What is Grouped Query Attention (GQA) and Why Do LLMs Use It?

# What is Grouped Query Attention (GQA) and Why Do LLMs Use It?

Authors
: - Name
: Amit Shekhar
Published on
: April 22, 2026

Grouped-Query Attention (GQA) is a strategy where the attention heads are divided into groups, and all the heads within a group share the same Key and Value, while each head still has its own Query.

In this blog, we will learn about Grouped-Query Attention (GQA) and how it differs from Multi-Head Attention (MHA).

We will also learn about Multi-Query Attention (MQA) along the way and see when to use which one.

Grouped-Query Attention is one of the most important optimizations in modern Large Language Models. It allows models to generate text much faster while using less memory, and that too without losing much quality.

Before jumping into Grouped-Query Attention, we must know how Multi-Head Attention works. We have a detailed blog on Transformer Architecture where we have explained Multi-Head Attention as well. I will highly recommend reading it first.

Today, we will cover the following topics:

- The Big Picture
- Quick Recap: Multi-Head Attention (MHA)
- The Problem with Multi-Head Attention
- What is Multi-Query Attention (MQA)?
- What is Grouped-Query Attention (GQA)?
- How Grouped-Query Attention Works
- GQA is a Generalization of MHA and MQA
- GQA vs MHA vs MQA
- Real-World Use Cases
- A Note on Terminology
- Uptraining: Converting MHA to GQA
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

In Multi-Head Attention, every head keeps its own Key and Value. This is great for quality, but it makes the KV Cache very large during inference. Grouped-Query Attention keeps the same set of Queries, but it makes groups of heads share one Key and one Value. This shrinks the KV Cache by a lot while keeping the quality very close to Multi-Head Attention. It is one of the main KV Cache Compression techniques, the one that is built into the model design itself.

In simple words:

Grouped-Query Attention = Near Multi-Head Attention quality + Much smaller KV Cache through head grouping.

## Quick Recap: Multi-Head Attention (MHA)

In our blog on Transformer Architecture, we have explained Multi-Head Attention in detail. Here is a quick recap.

In Multi-Head Attention, we run the attention mechanism multiple times in parallel. Each parallel run is called a head. Each head has its own separate set of weight matrices for Query (Q), Key (K), and Value (V).

If we want to understand the math behind how Q, K, and V actually work in attention, we have a detailed blog on Math Behind Attention: Q, K, V.

Let's say we have a model with 8 heads. This means:

- Head 1 has its own Q₁, K₁, V₁
- Head 2 has its own Q₂, K₂, V₂
- Head 3 has its own Q₃, K₃, V₃
- ... and so on for all 8 heads

Each head looks at the input from a different perspective. The outputs from all heads are concatenated and passed through a final projection to produce the result.

Think of it like a team of 8 detectives investigating a crime scene. Each detective has their own set of clues (K and V) and their own set of questions (Q). Each one investigates independently and finds different insights. When they share their findings, the team gets a complete picture.

This works great during training. But, here is the catch. There is a big problem during inference (i.e. when the model is actually generating text for the user). Let's understand this problem.

## The Problem with Multi-Head Attention

When a language model generates text, it produces one word at a time. For each new word, the model needs to look back at all the previous words using the attention mechanism.

Note: Technically, language models work with tokens (small pieces of text) instead of whole words. But just for the sake of understanding, we will use the word "word" throughout this blog.

Now, here is the important part. To compute attention, the model needs the Key (K) and Value (V) for every previous word. If the model recomputes K and V for all previous words every time it generates a new word, it would be very slow.

So, the model stores the Key and Value of all previous words in memory. This stored memory is called the KV Cache.

The best way to learn this is by taking an example.

Let's say we are generating a sentence and we have already produced 1,000 words. The model has 8 heads. Each head stores its own Key and Value for all 1,000 words.

So, the KV Cache stores:

- 8 sets of Keys (one per head) x 1,000 words = 8,000 Key vectors
- 8 sets of Values (one per head) x 1,000 words = 8,000 Value vectors
- Total: 16,000 vectors in memory

Note: This is per transformer layer. The full KV Cache multiplies this by the number of layers in the model. This is why long-context inference gets memory-hungry so fast.

Now, imagine a large model with 64 heads and a sequence length of 100,000 tokens. The KV Cache becomes extremely large. It takes up a huge amount of GPU memory.

Going back to our detective analogy, each detective (head) maintains their own personal notebook (KV Cache) where they write down clues about every word they have seen. With 64 detectives and 100,000 words, that is 64 separate notebooks, each with 100,000 pages. That is a lot of paper.

This is the problem. The KV Cache in Multi-Head Attention grows very fast and takes up a lot of memory. This makes inference slow and expensive, especially for long sequences and large models.

So, we need a smarter approach that reduces the size of this KV Cache without losing the quality of the model's output. First, let's understand Multi-Query Attention (MQA), which was the first attempt to solve this problem. Then we will learn about Grouped-Query Attention (GQA), which is a better solution.

If we want to go deep into Multi-Head Attention, KV Cache, and Transformer internals, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

## What is Multi-Query Attention (MQA)?

Multi-Query Attention (MQA) is a strategy where all heads share the same Key and Value, but each head still has its own Query.

Let's decompose the term:

Multi-Query Attention = Multiple Queries + Single shared Key and Value

In Multi-Head Attention, each head has its own Q, K, and V. In Multi-Query Attention, each head has its own Q, but all heads share one single K and one single V.

Let's say we have 8 heads:

Multi-Head Attention (MHA):

- Head 1: Q₁, K₁, V₁
- Head 2: Q₂, K₂, V₂
- Head 3: Q₃, K₃, V₃
- ... (8 separate K and V sets)

Multi-Query Attention (MQA):

- Head 1: Q₁, K_shared, V_shared
- Head 2: Q₂, K_shared, V_shared
- Head 3: Q₃, K_shared, V_shared
- ... (only 1 K and 1 V set for all heads)

Now, the KV Cache only needs to store 1 set of Keys and 1 set of Values instead of 8. The KV Cache becomes 8 times smaller.

Going back to our detective analogy, in MQA, all 8 detectives share a single notebook of clues. They still ask their own different questions (Q), but they are all looking at the same evidence. This saves a lot of paper (memory), but it limits their ability to find different insights.

The problem with MQA:

MQA reduces memory by a lot, but there is a trade-off. Since all heads share the same Key and Value, the model loses some of its ability to look at the input from different perspectives. The quality of the output can drop, and training can also become unstable.

We need something in between. Something that reduces memory like MQA but maintains quality like MHA.

So, here comes Grouped-Query Attention to the rescue.

## What is Grouped-Query Attention (GQA)?

Grouped-Query Attention (GQA) is a strategy where heads are divided into groups, and all heads within a group share the same Key and Value, while each head still has its own Query.

Let's decompose the term:

Grouped-Query Attention = Grouped Queries + Shared Key and Value per group

In simple words, instead of giving every head its own K and V (like MHA) or giving all heads a single shared K and V (like MQA), GQA divides the heads into groups and lets each group share one K and V.

The best way to learn this is by taking an example.

Let's say we have 8 heads and we divide them into 2 groups (4 heads per group):

Group 1: Head 1, Head 2, Head 3, Head 4 - share K_group1, V_group1

Group 2: Head 5, Head 6, Head 7, Head 8 - share K_group2, V_group2

So:

- Head 1: Q₁, K_group1, V_group1
- Head 2: Q₂, K_group1, V_group1
- Head 3: Q₃, K_group1, V_group1
- Head 4: Q₄, K_group1, V_group1
- Head 5: Q₅, K_group2, V_group2
- Head 6: Q₆, K_group2, V_group2
- Head 7: Q₇, K_group2, V_group2
- Head 8: Q₈, K_group2, V_group2

Now, instead of storing 8 sets of K and V (like MHA), we only store 2 sets. The KV Cache becomes 4 times smaller.

And instead of using just 1 shared K and V (like MQA), we use 2 sets. So, the model still has some ability to look at the input from different perspectives.

Going back to our detective analogy, in GQA, we divide the 8 detectives into 2 teams. Each team of 4 detectives shares one notebook of clues. This way, we need only 2 notebooks instead of 8 (much less paper), but we still have 2 different sets of clues (better than 1). Each team can discover different things.

GQA is the sweet spot between MHA and MQA. It gives us the memory savings close to MQA while keeping the quality close to MHA.

Note: In GQA, only the Key and Value are shared within a group. The Query is still separate for every head. This is important because the Query is what allows each head to look at the input from a different perspective. By keeping the Queries separate, GQA preserves the diversity of attention patterns. The KV Cache shrinks because we only store the Key and Value during inference, not the Query.

Now, let's understand how GQA actually works step by step.

## How Grouped-Query Attention Works

Let's walk through the process step by step.

Step 1: Divide the heads into groups. The number of groups is a setting that we choose before training. Let's say we have 8 heads and 2 groups.

Step 2: Each head computes its own Query (Q) using its own weight matrix. So, all 8 heads have their own separate Queries. This is the same as MHA.

Step 3: Each group computes one shared Key (K) and one shared Value (V) using the group's weight matrices. Group 1 computes K_group1 and V_group1. Group 2 computes K_group2 and V_group2.

Step 4: Each head runs the attention mechanism using its own Query but with the shared Key and Value of its group. Heads 1 to 4 use K_group1 and V_group1. Heads 5 to 8 use K_group2 and V_group2.

Step 5: The outputs from all heads are concatenated and passed through the final projection, just like in MHA.

The result is the same type of output as MHA. But the KV Cache is much smaller because we only store K and V for each group, not for each head.

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

This is how Grouped-Query Attention works.

Now, let's see something very interesting about GQA.

To master GQA, MQA, Multi-Head Attention, and the math behind Q/K/V from the ground up, check out our AI and Machine Learning Program at Outcome School.

## GQA is a Generalization of MHA and MQA

Here is something beautiful about GQA. It is actually a generalization of both MHA and MQA. Let's understand how.

- When the number of groups = number of heads: Each group has exactly 1 head. Each head gets its own K and V. This is exactly Multi-Head Attention (MHA).
- When the number of groups = 1: All heads are in one group. All heads share the same K and V. This is exactly Multi-Query Attention (MQA).
- When the number of groups is between 1 and number of heads: This is Grouped-Query Attention (GQA).

So, MHA and MQA are just special cases of GQA. By changing the number of groups, we can control the trade-off between quality and memory. That's the beauty of Grouped-Query Attention.

Now that we have learned about all three, let's compare them.

## GQA vs MHA vs MQA

Before we compare the numbers, let's first see the three architectures visually side by side.

```
MHA (8 query heads, 8 KV sets - one per head):

  [Q1]  [Q2]  [Q3]  [Q4]  [Q5]  [Q6]  [Q7]  [Q8]
   |     |     |     |     |     |     |     |
   v     v     v     v     v     v     v     v
  [K1]  [K2]  [K3]  [K4]  [K5]  [K6]  [K7]  [K8]
  [V1]  [V2]  [V3]  [V4]  [V5]  [V6]  [V7]  [V8]

MQA (8 query heads, 1 KV set - shared by all heads):

  [Q1]  [Q2]  [Q3]  [Q4]  [Q5]  [Q6]  [Q7]  [Q8]
    \     \    \    |     |    /    /     /
     +-----+----+---+-----+---+----+-----+
                       |
                       v
                  [K_shared]
                  [V_shared]

GQA (8 query heads, 2 groups - 1 KV set per group):

  [Q1] [Q2] [Q3] [Q4]       [Q5] [Q6] [Q7] [Q8]
    \   |    |   /             \   |    |   /
     +--+----+--+                +-+----+-+
            |                          |
            v                          v
       [K_group1]                 [K_group2]
       [V_group1]                 [V_group2]

```

Here, we can see the difference clearly:

- In MHA, each Query has its own private Key and Value. 8 Queries, 8 KV sets. Maximum quality, maximum memory.
- In MQA, all Queries point to a single shared Key and Value. 8 Queries, 1 KV set. Minimum memory, but reduced diversity.
- In GQA, Queries are divided into groups, and each group shares one Key and Value. 8 Queries, 2 KV sets. A balance of both worlds.

Now, let me tabulate the differences between GQA, MHA, and MQA for your better understanding so that you can decide which one to use based on your use case.

| Feature | MHA | MQA | GQA |
| --- | --- | --- | --- |
| Key-Value sets | One per head | One for all heads | One per group |
| KV Cache size | Largest | Smallest | In between |
| Output quality | Best | Can degrade | Close to MHA |
| Memory usage during inference | Highest | Lowest | In between |
| Inference speed | Slowest | Fastest | Fast |
| Example (8 heads, 2 groups) | 8 KV sets | 1 KV set | 2 KV sets |

In simple words: MHA gives the best quality but uses the most memory. MQA uses the least memory but can lose quality. GQA is the sweet spot - it uses much less memory than MHA while keeping quality very close to MHA.

Now, let's see some real-world use cases.

## Real-World Use Cases

GQA is now used in many popular large language models:

- LLaMA 2 (34B and 70B): Uses GQA with 8 KV groups. The 70B model has 64 query heads, so the KV Cache is 8 times smaller compared to standard MHA. (Meta described the 34B in the paper but never publicly released its weights.) The smaller LLaMA 2 models (7B and 13B) still use standard MHA.
- LLaMA 3: Uses GQA across all model sizes for faster inference.
- Mistral 7B: Uses GQA with 32 query heads and 8 KV groups. It also pairs GQA with Sliding Window Attention so that long inputs stay cheap.

These models use GQA because it allows them to handle longer sequences and serve more users at the same time, and that too while keeping the quality of the output very high.

Serving many users on one GPU also means managing the KV Cache memory carefully at serving time, and we have a detailed blog on vLLM that explains how a serving system handles this.

GQA is especially useful for:

- Long conversations: When the model needs to remember thousands of previous words, GQA keeps the KV Cache manageable.
- Serving many users: Smaller KV Cache means more users can be served on the same GPU.
- Edge deployment: Reduced memory makes it easier to run models on devices with limited resources.

GQA has become a standard technique in modern LLMs. It enables us to have faster inference and lower memory usage without meaningfully sacrificing quality. It makes our life easy.

To learn LLM Internals, KV Cache, and Model Deployment and Serving end to end, check out our AI and Machine Learning Program at Outcome School.

## A Note on Terminology

In the actual code of popular models (like the configurations in HuggingFace or LLaMA), the number of groups is called `num_key_value_heads`. The number of query heads is called `num_attention_heads`.

So, the number of heads per group is simply:

Heads per group = `num_attention_heads` / `num_key_value_heads`

Let's say we read about a model that has 32 query heads and 8 KV heads. This means there are 8 groups, and each group has 4 heads sharing the same Key and Value.

This terminology is good to know because when we read the configuration of a real model, we will see `num_key_value_heads` directly instead of the word "groups".

## Uptraining: Converting MHA to GQA

Now, the next big question is: do we always need to train a GQA model from scratch? The answer is no.

The original GQA paper showed that we can take an existing Multi-Head Attention model and convert it into a GQA model very cheaply. This is called uptraining.

The process is simple:

Step 1: Take an existing MHA model that has already been trained.

Step 2: For each group, take all the Key weight matrices of the heads in that group and average them. Do the same for the Value weight matrices. This gives us one shared Key and one shared Value per group.

Step 3: Fine-tune the model for a short time. The original paper showed that uptraining with just around 5% of the original pre-training compute is enough to recover quality close to full MHA.

This is one of the main reasons GQA was adopted so quickly. Labs did not have to throw away their existing MHA models or spend huge compute to train new ones. They could just uptrain them into GQA.

Now, we have understood Grouped-Query Attention and how it differs from Multi-Head Attention. We also learned about Multi-Query Attention, how GQA is a generalization of both MHA and MQA, the terminology used in real code, and how existing MHA models can be uptrained into GQA.

## Quick Summary

Let's recap what we have learned:

- Multi-Head Attention (MHA): Every head has its own Query, Key, and Value. Best quality, but the KV Cache becomes very large during inference.
- The KV Cache problem: During text generation, the model stores the Key and Value of every previous word for every head. With many heads and long sequences, this takes a huge amount of GPU memory.
- Multi-Query Attention (MQA): All heads share one single Key and one single Value, while each head still has its own Query. The KV Cache becomes very small, but the output quality can drop.
- Grouped-Query Attention (GQA): Heads are divided into groups. Each group shares one Key and one Value, while each head still has its own Query. This is the sweet spot between MHA and MQA.
- GQA is a generalization: When the number of groups equals the number of heads, GQA becomes MHA. When the number of groups is 1, GQA becomes MQA. Anything in between is GQA.
- Importance: GQA gives us memory savings close to MQA while keeping quality close to MHA. It is now used in many popular models like LLaMA 2, LLaMA 3, and Mistral 7B.
- Uptraining: We do not need to train a GQA model from scratch. We can take an existing MHA model, average the K and V weights within each group, and fine-tune for a short time to convert it into a GQA model. This is one of the main reasons GQA was adopted so quickly.

### Why does GQA share the Key and Value but not the Query?

[…662ln elided…]

### How many sink tokens should we keep in a streaming window?

Keeping just the first 4 tokens as sinks is usually enough to keep the model stable. We join these sink tokens with a sliding window of recent tokens and throw away only the middle. This way, the leftover attention always has a home.

### Does StreamingLLM use more memory as the conversation grows?

No. StreamingLLM keeps a few sink tokens plus a sliding window of recent tokens, so it uses only a small, fixed amount of memory. With this, a model can handle millions of words of conversation without crashing or turning to nonsense.

### What is the difference between the first-token sink and a learnable attention sink?

A learnable attention sink is a special, dedicated token that the model is trained to dump extra attention onto. Instead of borrowing the first real word as a drain, the model gets its own private drain that holds no meaning. This is even cleaner, because the drain is no longer mixed up with a real word.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# What is RoPE (Rotary Position Embedding)? The Math Behind It
URL: https://outcomeschool.com/blog/math-behind-rope-rotary-position-embedding
Published: 2026-04-23
Author: Amit Shekhar

What is RoPE (Rotary Position Embedding)? The Math Behind It

# What is RoPE (Rotary Position Embedding)? The Math Behind It

Authors
: - Name
: Amit Shekhar
Published on
: April 23, 2026

RoPE (Rotary Position Embedding) is a way to give position information to a Transformer. It rotates the Query (Q) and Key (K) vectors by an angle that depends on the token's position, so that attention depends on the relative distance between tokens.

In this blog, we will learn about the math behind Rotary Position Embedding (RoPE) and why it is used in modern Large Language Models.

Today, we will cover the following topics:

- The Big Picture
- Why a Transformer Needs Position Information
- Older Approaches and Their Problems
- The Core Idea Behind RoPE
- The 2D Rotation Math
- How RoPE Is Applied to Q and K
- Why the Dot Product Captures Relative Position
- A Small Numeric Example
- Real-World Use Cases
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

A Transformer reads all the tokens in a sentence at the same time. It does not know which word came first and which came last. So, we have to give it position information separately. RoPE is a clever way to do that. Instead of adding a position vector, RoPE rotates the Query and Key vectors based on their position. After the rotation, the dot product between any two tokens automatically reflects the relative distance between them.

In simple words:

RoPE = Rotate the Q and K vectors by an angle that depends on the token's position.

This makes the attention score depend only on the relative distance between two tokens, which is exactly what we want.

We have a detailed blog on Math Behind Attention: Q, K, V that explains how Q, K, and V are used inside attention.

## Why a Transformer Needs Position Information

A Transformer processes all the tokens in a sentence in parallel. It does not read them one by one like we do.

We have a detailed blog on Transformer Architecture that explains how a Transformer works end to end.

Let's see why this is a problem.

Consider these two sentences:

- "The cat chased the dog."
- "The dog chased the cat."

Both sentences contain the exact same words. The only difference is the order. To us, the meaning is completely different. But, to a raw Transformer, both look the same. It has no idea who chased whom.

We need to inject position information into the model so that it knows the order of the words.

## Older Approaches and Their Problems

There are two well-known older approaches to add position information.

Approach 1: Sinusoidal Positional Encoding. This is the original method from the "Attention Is All You Need" paper. We compute a fixed vector for each position using sine and cosine functions. We add this vector to the token embedding before feeding it into the model.

Approach 2: Learned Positional Embeddings. Instead of using a fixed formula, we let the model learn a separate embedding for each position. We add this learned vector to the token embedding.

Both approaches share two big problems.

- They use addition. The position vector is added to the token embedding. This mixes position information into the meaning of the word, and the two end up competing inside the same vector.
- They do not encode relative distance. With absolute positional embeddings, the model has to learn from scratch how every pair of positions relates. There is no built-in structure that says "positions 5 and 10" have the same relationship as "positions 105 and 110".
- They struggle with longer sequences. If the model was trained on sequences of length 2048 and we suddenly give it 8192 tokens at inference time, learned embeddings have nothing to fall back on. Sinusoidal encoding can technically extrapolate, and the original "Attention Is All You Need" paper actually proposed it partly for this reason. But, later research showed that this property does not hold up well in practice.

We need a smarter way. We need a method that handles position more cleanly and works at any sequence length.

So, here comes RoPE to the rescue.

## The Core Idea Behind RoPE

The full form of RoPE is Rotary Position Embedding.

Let's decompose the name:

RoPE = Rotary + Position + Embedding.

- Position means we are encoding the position of a token.
- Embedding means we are doing this inside the vector space the model uses. Learn more about Embeddings: Embeddings in Machine Learning
- Rotary means we are using rotation as the encoding mechanism.

The idea is simple. Instead of adding a position vector to the token embedding, we rotate the Query and Key vectors by an angle that depends on the token's position. The further along a token is in the sequence, the more we rotate its vector.

The magic is in the dot product. When we compute the attention score `Q · K`, the rotations combine in a way that the result depends only on the difference in positions between the two tokens, not on their absolute positions.

So, RoPE gives us relative position information for free through the dot product.

Let's take a real-world analogy. Think of each pair of dimensions inside a token's vector as a clock hand. (We will see in a later section that the vector is split into many such pairs, each acting as its own clock at its own speed.) A token at position 1 rotates the hand to "1 o'clock". A token at position 5 rotates it to "5 o'clock". When we compare two tokens, we are not asking "where does each hand point?" - we are asking "how many hours apart are the two hands?". That is exactly the relative-position information attention needs.

## The 2D Rotation Math

To understand RoPE, we must first understand how rotation works in 2D.

Suppose we have a 2D vector `v = [x, y]`. We want to rotate it by an angle `θ` (theta). The new vector `v'` is:

```
x' = x * cos(θ) - y * sin(θ)
y' = x * sin(θ) + y * cos(θ)

```

This is the standard 2D rotation. We can write it as a matrix multiplication:

```
| x' |   | cos(θ)  -sin(θ) |   | x |
|    | = |                 | * |   |
| y' |   | sin(θ)   cos(θ) |   | y |

```

That is the rotation matrix. It rotates any 2D vector by angle `θ` while keeping its length unchanged.

Here is a simple ASCII diagram showing the rotation.

```
                  y
                  |
                  |     v'
                  |    /
                  |   /
                  |  /
                  | /  θ
                  |/___________ v
                  +------------- x

```

Here, the vector `v` starts along the x-axis. After rotating by angle `θ`, it becomes `v'`. The length of the vector stays the same. Only the direction changes.

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

## How RoPE Is Applied to Q and K

Now, let's see how this rotation is used inside attention.

We have a Query vector `Q` and a Key vector `K`. These are not 2D vectors. They have many dimensions, often 64 or 128.

RoPE works on these high-dimensional vectors by splitting them into pairs of 2D vectors. If `Q` has 64 dimensions, we treat it as 32 pairs of 2D vectors. Each pair gets its own rotation.

For a token at position `m`, RoPE rotates each pair by an angle `m * θ_i`, where `θ_i` is a fixed frequency that depends on which pair we are looking at.

Here is a simple ASCII diagram showing how a Q vector with `d = 8` dimensions is split and rotated.

```
Q = [ q_1, q_2 | q_3, q_4 | q_5, q_6 | q_7, q_8 ]
      \______/   \______/   \______/   \______/
       pair 1     pair 2     pair 3     pair 4
         |           |           |           |
         v           v           v           v
      rotate      rotate      rotate      rotate
      by m*θ_1    by m*θ_2    by m*θ_3    by m*θ_4
      (fastest)                           (slowest)

```

Here, the 8-dimensional vector is split into 4 pairs. Each pair is rotated by its own angle, and the rotation amount also scales with the token's position `m`.

The standard formula for the frequencies is:

```
θ_i = 10000^(-2(i-1)/d)    for i = 1, 2, ..., d/2

```

Here, `d` is the per-head dimension. For the first pair this gives `θ_1 = 1` (largest, fastest rotation). For the last pair, with `d = 128` (a common per-head size), this gives `θ_(d/2) ≈ 0.0001` (smallest, slowest rotation). So, low-index pairs rotate fast and high-index pairs rotate slowly. This is similar to how sinusoidal positional encoding uses many frequencies, but here the frequencies are applied as rotations, not as added vectors.

Note: This formula is the exact knob that long-context techniques like YaRN and NTK-aware scaling tune. They modify these frequencies so a model trained on shorter sequences can handle much longer ones at inference.

After applying RoPE, the rotated `Q` for a token at position `m` is `R_m * Q`, where `R_m` is the rotation matrix for position `m`. Similarly, the `K` vector at position `n` gets its own rotation `R_n * K`.

Note: The original RoPE paper presents the splitting as consecutive pairs `(q_1, q_2), (q_3, q_4), ...` as shown above. In real-world implementations like LLaMA and Mistral, the splitting is done as `(q_i, q_(i + d/2))` - the first half of the vector paired with the second half. Both schemes are mathematically equivalent. They are just a permutation of dimensions, so the explanation here applies to either.

Note: RoPE is applied only to the Query and Key vectors. The Value vector `V` is left untouched. This is because the relative-position property we want comes from the `Q · K` dot product. The `V` vector is just the content being weighted by attention scores, so it does not need any position information.

To learn positional encodings, Q/K/V matrices, and the Transformer architecture in depth, check out our AI and Machine Learning Program at Outcome School.

## Why the Dot Product Captures Relative Position

This is where the magic happens.

When we compute the attention score between a query at position `m` and a key at position `n`, we calculate:

```
score = (R_m * Q) · (R_n * K)

```

Because of how rotation matrices work, this expression simplifies to:

```
score = Q · (R_(n-m) * K)

```

This works because rotation matrices are orthogonal, which means `R_m^T = R_(-m)`. The intuition is simple: rotating by `-m` undoes a rotation by `m`. So, rotating by `-m` and then by `n` combines into a single rotation by `n - m`. The full derivation is just one line of matrix algebra:

```
(R_m * Q) · (R_n * K) = Q^T * R_m^T * R_n * K
                      = Q^T * R_(-m) * R_n * K
                      = Q^T * R_(n-m) * K
                      = Q · (R_(n-m) * K)

```

The `m` rotation on `Q` effectively cancels, leaving a single net rotation by `n - m` on `K`.

The score depends only on `n - m`, which is the relative distance between the two tokens. The absolute positions `m` and `n` disappear from the formula.

This is the beauty of RoPE. The model does not see "token at position 5" and "token at position 12". Instead, it sees "these two tokens are 7 positions apart". This relative view of position is exactly what attention needs.

Let's see why this matters with a concrete example. Consider these two sentences:

- "The cat sat on the mat."
- "Yesterday, the cat sat on the mat."

In sentence 1, "cat" is at position 2 and "mat" is at position 6. The distance between them is 4.

In sentence 2, "cat" is at position 3 and "mat" is at position 7. The distance is again 4.

The relationship between "cat" and "mat" is identical in both sentences. They are 4 words apart, and the meaning of how they relate is the same. The fact that the whole sentence shifted by one word does not change anything about how "cat" relates to "mat".

Now, what if we used absolute positions instead? The model would have to separately learn:

- How (cat at pos 2) relates to (mat at pos 6)
- How (cat at pos 3) relates to (mat at pos 7)
- How (cat at pos 100) relates to (mat at pos 104)
- And so on, for every possible pair

That is wasteful. All of these are the same relationship - "two specific words, 4 positions apart". RoPE lets the model learn this once, and reuse it everywhere.

Going back to our clock analogy, when we look at two clock hands, we do not need to know what time each one shows individually. We only care about the angle between them. RoPE gives the model the same view of position.

Note: This relative-position property comes out of the math automatically. We did not design the model to learn relative positions. The rotation operation gives it to us for free.

## A Small Numeric Example

Let's put this into perspective with a small example.

Suppose we have a 2D Query vector `Q = [1, 0]` for the token at position `m = 1`. Let `θ = π / 4` (45 degrees).

The rotation matrix at position 1 is:

```
R_1 = | cos(π/4)  -sin(π/4) |   | 0.707  -0.707 |
      |                     | = |               |
      | sin(π/4)   cos(π/4) |   | 0.707   0.707 |

```

The rotated Query is:

```
R_1 * Q = | 0.707  -0.707 |   | 1 |   | 0.707 |
          |               | * |   | = |       |
          | 0.707   0.707 |   | 0 |   | 0.707 |

```

Now, suppose we have a Key vector `K = [1, 0]` at position `n = 2`. The rotation angle is `2 * π/4 = π/2`.

```
R_2 = | cos(π/2)  -sin(π/2) |   | 0  -1 |
      |                     | = |       |
      | sin(π/2)   cos(π/2) |   | 1   0 |

```

The rotated Key is:

```
R_2 * K = | 0  -1 |   | 1 |   | 0 |
          |       | * |   | = |   |
          | 1   0 |   | 0 |   | 1 |

```

The attention score is the dot product:

```
score = (R_1 * Q) · (R_2 * K)
      = 0.707 * 0 + 0.707 * 1
      = 0.707

```

So, the score for two tokens at a relative distance of `1` is `0.707`.

Now, let's verify the relative-position property. Let's pick a different pair with the same relative distance: `m = 2, n = 3`.

The rotated Query at position 2 uses the same `R_2` matrix from before:

```
R_2 * Q = | 0  -1 |   | 1 |   | 0 |
          |       | * |   | = |   |
          | 1   0 |   | 0 |   | 1 |

```

The rotated Key at position 3 uses angle `3 * π/4`:

```
R_3 * K = | cos(3π/4)  -sin(3π/4) |   | 1 |   | -0.707 |
          |                       | * |   | = |        |
          | sin(3π/4)   cos(3π/4) |   | 0 |   |  0.707 |

```

The attention score:

```
score = (R_2 * Q) · (R_3 * K)
      = 0 * (-0.707) + 1 * 0.707
      = 0.707

```

The score is `0.707` again. The absolute positions changed from `(1, 2)` to `(2, 3)`, but the relative distance stayed at `1`, so the score stayed at `0.707`. This is exactly the property RoPE was designed to give us.

## Real-World Use Cases

RoPE has become the standard for positional encoding in modern Large Language Models. Let's see where RoPE is used in practice.

- LLaMA family. All LLaMA models from Meta use RoPE.
- Mistral and Mixtral. Both use RoPE for positional encoding.
- Qwen. Alibaba's Qwen models use RoPE.
- DeepSeek. DeepSeek models use RoPE as well.
- Gemma. Google's open-weight Gemma models use RoPE.

Note: RoPE is also the foundation for many long-context techniques. Methods like YaRN, Position Interpolation, and NTK-aware scaling all extend RoPE so that a model trained on, say, 4K tokens can be used on 32K or 128K tokens at inference time. None of this would be possible if we were still using learned positional embeddings.

## Quick Summary

Let's recap what we have decoded:

- A Transformer reads all tokens in parallel. It does not naturally know the order of words, so we must inject position information.
- Older methods add a position vector to the token embedding. Sinusoidal encoding and learned embeddings lack built-in relative-distance structure and struggle with longer sequences.
- RoPE rotates the Q and K vectors instead of adding to them. The rotation angle depends on the token's position.
- The high-dimensional vector is split into pairs. Each pair is rotated by its own frequency.
- The dot product of two rotated vectors depends only on relative position. This gives us relative position information for free.
- No learned parameters. RoPE itself introduces no additional learned parameters, unlike learned positional embeddings.
- RoPE is the standard in modern LLMs. LLaMA, Mistral, Qwen, DeepSeek, and Gemma all use it.
- RoPE makes long-context extension possible. Techniques like YaRN and Position Interpolation rely on RoPE's structure.

This is how RoPE gives modern Large Language Models a clean, scalable, and elegant way to understand position.

### Is RoPE applied to the Value vector too?

No. RoPE is applied only to the Query and Key vectors, and the Value vector is left untouched. The relative-position property comes from the `Q · K` dot product. The Value vector is just the content being weighted by the attention scores, so it does not need any position information.

### Does RoPE add any learned parameters to the model?

No. RoPE itself introduces no additional learned parameters. The rotation angles come from a fixed frequency formula and the token's position. This is different from learned positional embeddings, where the model learns a separate embedding for each position.

### Can a model with RoPE handle longer text than it was trained on?

Yes, with the help of long-context techniques built on top of RoPE. Methods like YaRN, Position Interpolation, and NTK-aware scaling extend RoPE so that a model trained on, say, 4K tokens can be used on 32K or 128K tokens at inference time.

### Does rotating the Query and Key vectors change their length?

No. A rotation keeps the length of the vector unchanged, and only its direction changes. RoPE uses this rotation as the encoding mechanism, instead of adding a position vector that mixes position into the meaning of the word.

### Does it matter how the vector is split into pairs?

No. The original RoPE paper splits the vector into consecutive pairs, while implementations like LLaMA and Mistral pair the first half of the vector with the second half. Both schemes are mathematically equivalent, since they are just a permutation of dimensions.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

Our vision is to make tech education outcome-focused. Our mission is to help students master the internals and become great at system design to achieve the outcome they aspire to.

[Showing lines 1-363 and 1026-1453 of 1453; 662 middle lines (32.4KB) elided. Read artifact://42 for full output]
