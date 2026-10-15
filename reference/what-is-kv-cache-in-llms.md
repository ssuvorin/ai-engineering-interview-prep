> Source: https://outcomeschool.com/blog/kv-cache-in-llms

# KV Cache in LLMs
URL: https://outcomeschool.com/blog/kv-cache-in-llms
Published: 2026-03-27

KV Cache in LLMs

# KV Cache in LLMs

Authors
: - Name
: Amit Shekhar
Published on
: March 26, 2026

KV Cache is a memory inside a Large Language Model (LLM) that saves the work already done for the earlier words, so that the model does not repeat the same work for every new word it generates. Here, K stands for Key and V stands for Value.

In this blog, we will learn about KV Cache. We will start with how LLMs generate text one token at a time, understand the role of Key, Value, and Query inside the model, see the problem of repeated computation through an example, and then walk through how KV Cache solves this problem by storing and reusing past results.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## How LLMs Generate Text

Before we understand KV Cache, we first need to understand how LLMs generate text.

An LLM - Large Language Model - is a model that has been trained on a massive amount of text data. It can understand and generate human language. When we give it a sentence, it predicts what comes next.

LLMs generate text one token at a time. A token is a small piece of text - it can be a word, part of a word, or even a single character. For simplicity, let's treat each word as one token.

Let's say we give the model this input:

```
"I love"

```

The model looks at "I" and "love", and predicts the next token: "teaching".

Now the full sequence becomes:

```
"I love teaching"

```

The model looks at "I", "love", and "teaching", and predicts the next token: "AI".

Now the full sequence becomes:

```
"I love teaching AI"

```

This process continues, one token at a time, until the model decides to stop.

The important thing to notice here is: every time the model predicts a new token, it needs to look at all the previous tokens to decide what comes next.

This token-by-token generation happens in two phases, prefill and decode, and the KV Cache is the bridge between them. We have a detailed blog on Prefill vs Decode that explains this step by step.

## What Happens Inside the Model

Now, let's understand what happens inside the model when it generates each token.

The model has a component called the attention layer, the heart of the Transformer architecture. The job of the attention layer is to help the model figure out which previous tokens are important for predicting the next token. Not all previous tokens are equally useful. Some matter more than others.

Inside the attention layer, every token is converted into three things. Let's understand each of them with a simple analogy.

Imagine a classroom where a new student joins and wants to find out who can help with a specific topic:

- Query (Q): The new student's question - "Who here knows about this topic?" Every token being predicted gets a Query. It represents what the token is looking for.
- Key (K): The name tag each existing student wears that says what they know - "I know about math" or "I know about science." Every previous token gets a Key. It describes what information that token holds.
- Value (V): The actual notes each student has. Once the new student finds the right person using their name tag (Key), the notes (Value) are what they actually use. Every previous token gets a Value. It carries the actual information.

So, the current token uses its Query to compare against the Keys of all previous tokens. This comparison produces attention scores - numbers that tell the model how much focus to give to each previous token. A higher score means that token is more relevant. A lower score means it is less relevant. The model then uses these scores to collect the Values from the relevant tokens. If we want to go deeper into how Q, K, and V are computed, we have a detailed blog on Math behind Attention: Q, K, V.

This is how the attention layer works.

Now, let's see the problem.

To learn the attention layer, Q/K/V internals, and Transformer architecture in depth, check out our AI and Machine Learning Program at Outcome School.

## The Problem: Repeated Computation

Every time the model predicts the next token, it computes the Key, Value, and Query for all tokens in the sequence - not just the new one.

Let's see what happens step by step with our example:

Step 1: Input is "I love"

The model computes Key, Value, and Query for:

- "I"
- "love"

It uses these to predict the next token: "teaching".

Step 2: Input is "I love teaching"

The model computes Key, Value, and Query for:

- "I" (already computed in Step 1, but computed again)
- "love" (already computed in Step 1, but computed again)
- "teaching" (new)

It uses these to predict the next token: "AI".

Step 3: Input is "I love teaching AI"

The model computes Key, Value, and Query for:

- "I" (already computed in Step 1 and Step 2, but computed again)
- "love" (already computed in Step 1 and Step 2, but computed again)
- "teaching" (already computed in Step 2, but computed again)
- "AI" (new)

Do you see the problem?

The Key and Value for "I" were computed in Step 1. But the model computes them again in Step 2, and again in Step 3. The same goes for "love" and "teaching".

The model is repeating the same work for tokens it has already seen. This is wasted computation.

As the sequence grows longer, this problem gets worse. If the model has already generated 100 tokens, then at the next step, it would recompute the Key and Value for all 100 previous tokens just to predict one new token. This makes text generation very slow.

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

## What is KV Cache?

KV Cache is a memory where we save the Key and Value of every token that has already been processed, so that the model does not compute them again.

So, here comes the KV Cache to the rescue. The idea behind KV Cache is simple: compute the Key and Value for each token once, store them, and reuse them in every future step.

Think of it like taking notes. Imagine you are in a meeting. Every time someone new speaks, instead of asking all the previous speakers to repeat what they said, you simply read from your notes and only listen to the new speaker. The notes are your cache.

Let's see how the same example works with KV Cache:

Step 1: Input is "I love"

The model computes Key, Value, and Query for:

- "I"
- "love"

It saves the Key and Value of "I" and "love" in the KV Cache.

It uses these to predict the next token: "teaching".

KV Cache now contains: Key and Value for "I", "love"

Step 2: Input is only "teaching" (only the new token)

The model retrieves the Key and Value of "I" and "love" from the KV Cache. No recomputation needed.

It computes Key, Value, and Query only for the new token: "teaching".

It saves the Key and Value of "teaching" in the KV Cache.

It uses all of these together to predict the next token: "AI".

KV Cache now contains: Key and Value for "I", "love", "teaching"

Step 3: Input is only "AI" (only the new token)

The model retrieves the Key and Value of "I", "love", and "teaching" from the KV Cache. No recomputation needed.

It computes Key, Value, and Query only for the new token: "AI".

It saves the Key and Value of "AI" in the KV Cache.

KV Cache now contains: Key and Value for "I", "love", "teaching", "AI"

So, instead of recomputing the Key and Value for every token at every step, the model computes them only for the new token and reuses the cached values for all previous tokens.

This is how KV Cache avoids repeated computation.

This same idea can be taken one step further by reusing the cached Keys and Values across many requests that share the same starting text. We have a detailed blog on Prompt Caching that explains how this works.

## Why Only Key and Value Are Cached, Not Query

You would naturally ask: why do we cache only the Key and Value, and not the Query?

The Query is only needed for the current token - the one being generated right now. The current token uses its Query to compare against the Keys of all previous tokens to find which ones are relevant. Once the prediction is done, that Query is no longer needed.

But the Key and Value of every past token are needed at every future step, because every new token must look at all the previous tokens to make its prediction.

So, we only need to store the Keys and Values. This is why it is called KV Cache - it caches the K eys and V alues.

## How Much Faster Does It Get

Let's compare the two approaches side by side:

Without KV Cache:

```
Step 1: Compute K, V, Q for 2 tokens
Step 2: Compute K, V, Q for 3 tokens  (2 recomputed)
Step 3: Compute K, V, Q for 4 tokens  (3 recomputed)
Step 4: Compute K, V, Q for 5 tokens  (4 recomputed)
...
Step N: Compute K, V, Q for (N+1) tokens  (N recomputed)

```

The amount of computation keeps growing at every step.

With KV Cache:

```
Step 1: Compute K, V, Q for 2 tokens → Save K, V for 2 tokens in cache
Step 2: Compute K, V, Q for 1 token  → Reuse K, V for 2 tokens from cache
Step 3: Compute K, V, Q for 1 token  → Reuse K, V for 3 tokens from cache
Step 4: Compute K, V, Q for 1 token  → Reuse K, V for 4 tokens from cache
...
Step N: Compute K, V, Q for 1 token  → Reuse K, V for N tokens from cache

```

After the first step, the model computes only for one new token at each step instead of the entire sequence.

To put this into perspective: if the model is generating a sequence of 100 tokens, without KV Cache, the total number of Key and Value computations across all steps would be 2 + 3 + 4 + ... + 100 = 5,049 computations. With KV Cache, it would be 2 + 1 + 1 + ... + 1 = 101 computations. That is roughly 50 times fewer computations. The longer the sequence, the bigger the savings.

This is what makes KV Cache so effective at speeding up text generation.

## The Trade-Off: Speed vs Memory

KV Cache makes generation faster, but it comes with a trade-off: it uses extra memory to store all the Key and Value information for every token that has been generated so far.

As the sequence gets longer, the cache grows larger. For very long sequences with thousands of tokens, the cache can consume a significant amount of memory.

For a chat that never ends, one common fix is to keep only a recent window of tokens plus the first few attention sinks, so that the cache stays at a fixed size. This is one of several KV Cache Compression techniques that shrink this memory, and the others do it without throwing away a single token.

So, KV Cache is a trade-off: we use more memory to save computation time. For most use cases, this trade-off is well worth it, as the speed improvement is significant.

When serving an LLM to many users at once, managing this KV Cache memory efficiently becomes critical. We have a detailed blog on vLLM that explains how a serving system handles this end to end.

Now, we have understood the KV Cache in LLMs.

In the next blog, we will learn about Paged Attention that solves the memory issue of KV Cache.

### Does the model still compute anything for the new token when KV Cache is used?

Yes. With KV Cache, the model still computes the Key, Value, and Query for the new token. It only skips the work for the previous tokens, whose Keys and Values it reads from the cache. Then it saves the Key and Value of the new token in the cache for future steps.

### Can the KV Cache be reused across different requests?

Yes. The same idea can be taken one step further by reusing the cached Keys and Values across many requests that share the same starting text. This is called Prompt Caching. It builds on the KV Cache idea of computing something once and reusing it.

### How do we stop the KV Cache from growing forever in a long chat?

One common fix is to keep only a recent window of tokens plus the first few attention sinks. This way, the cache stays at a fixed size. This is one of several KV Cache Compression techniques, and the others shrink the memory without throwing away a single token.

### Does KV Cache solve the memory problem of LLMs?

No. KV Cache saves computation time, but it uses extra memory, and the cache grows larger as the sequence gets longer. When serving an LLM to many users, managing this memory becomes critical. Paged Attention is the technique that solves the memory issue of KV Cache.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# What is KV Cache Compression?
URL: https://outcomeschool.com/blog/kv-cache-compression
Published: 2026-09-12
Author: Amit Shekhar

What is KV Cache Compression?

# What is KV Cache Compression?

Authors
: - Name
: Amit Shekhar
Published on
: September 12, 2026

KV Cache Compression is a set of techniques that shrink the memory an AI model uses to remember the conversation while it is writing its reply, so that the model can handle longer text with less memory.

In this blog, we will learn about KV Cache Compression, the set of techniques that shrink the memory an AI model uses to remember the conversation while it is writing its reply. We will also see how an LLM writes one token at a time, what the KV Cache is and why we need it, why this cache becomes so huge, how quantization stores the same memory in fewer bits, how we can throw away the tokens that do not matter, how sharing across attention heads reduces the cache, how the cache can be squeezed into a small hidden vector, and when to use which one.

We will cover the following:

- What is an LLM and how it writes text?
- What is Attention?
- What is the KV Cache?
- Why the KV Cache becomes huge
- What is KV Cache Compression?
- Approach 1: Quantization
- Approach 2: Token Eviction
- Approach 3: Sharing Keys and Values across Heads
- Approach 4: Low-Rank Compression
- Comparison of the approaches
- When to use which one

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is an LLM and how it writes text?

An LLM (Large Language Model) is an AI model that reads text and writes text. ChatGPT, Claude, Gemini, all of them are based on LLMs.

An LLM learns by reading a huge amount of text from the internet. This learning process is called training. Once the training is done, we can ask the model questions, and it writes the answers.

The most important thing to know about an LLM is that it does not write the full reply in one shot. It writes one small piece at a time. This small piece is called a token. For the sake of understanding, we can think of a token as a word.

Let's say we ask the model, "What is the capital of France?"

The model writes "The". Then it looks at everything so far and writes "capital". Then it looks at everything so far again and writes "of". Then "France". Then "is". Then "Paris".

So, to write every new token, the model has to look back at all the previous tokens. This looking back is done by something called Attention.

Now, let's understand Attention.

## What is Attention?

Attention is the way a model decides which previous tokens are important for writing the next token.

In simple words, Attention is looking back and picking what matters.

Let's say the model is writing the sentence, "The dog was tired, so it went to sleep." When the model reaches the word "it", it needs to know that "it" refers to "the dog". So, the model pays more attention to "dog" and less attention to the other words.

Now, the question is, how does the model do this?

Every token is converted into three things:

- Query (Q): What the current token is looking for.
- Key (K): What each previous token offers, like a label.
- Value (V): The actual information that each previous token carries.

Each of these is just a list of numbers. In AI, a list of numbers is called a vector. So, every token has a Query vector, a Key vector, and a Value vector.

Let's take an analogy. Suppose we are in a library. We have a question in our mind. This is the Query. Every book has a title on its spine. This is the Key. The content inside the book is the Value.

We compare our question with the title of every book. The books whose titles match our question well get more attention. Then we read the content of those books and combine what we learned.

This is exactly what Attention does. The Query of the new token is compared with the Key of every previous token. Based on how well they match, the Values are combined and passed forward to help write the next token.

We have a detailed blog on Math behind Attention - Q, K, and V that explains this step by step.

One more thing to notice: A model does this Attention not just once. It has many layers stacked one after another, and every layer has many attention heads. Each head is like a separate reader looking for a different thing. One head looks for grammar, one looks for names, one looks for what "it" refers to, and etc.

Now that we have learned about Attention, it's time to learn about the KV Cache.

To master Q, K, V Matrices, Self-Attention and Multi-Head Attention, and build a Large Language Model (LLM) from scratch, check out our AI and Machine Learning Program at Outcome School.

## What is the KV Cache?

Now, let's see the problem. For every new token, the model needs the Key and the Value of every previous token.

Let's say the model has already written 100 tokens and is now writing the 101st token. It needs the Keys and Values of all 100 previous tokens. Without any memory, the model would calculate the Keys and Values of all the 100 tokens again. Then for the 102nd token, it would calculate for all 101 tokens again. And so on.

This is a huge waste. The Key and Value of a token never change once they are computed. So, why calculate them again and again?

So, here comes the KV Cache to the rescue.

KV Cache = Key + Value + Cache

A cache is just a memory where we store something so that we do not have to compute it again.

The KV Cache is the memory where the model stores the Keys and Values of every previous token so that it can reuse them while writing the next token.

Now, when the model writes the 101st token, it only calculates the Key and Value of the newest token, adds them to the cache, and reads everything else from the cache.

This makes text generation very fast. Problem Solved!

But, here is the catch. This cache grows with every single token. And it grows very fast.

## Why the KV Cache becomes huge

The best way to learn this is by taking an example.

Before jumping into the example, we must know two small things. A bit is the smallest unit of memory in a computer, it is either 0 or 1. And 8 bits make 1 byte.

Let's take a model with the following. These numbers are close to the real numbers of Llama 2, a popular open-source model:

- 32 layers
- 32 attention heads in each layer
- Each head has a Key vector of 128 numbers and a Value vector of 128 numbers
- Each number is stored in 16 bits, which means 2 bytes

Now, let's calculate how much memory one token needs in the cache.

For one head in one layer, we store 128 numbers for the Key and 128 numbers for the Value. That is 256 numbers.

For 32 heads, that is 256 x 32 = 8,192 numbers.

For 32 layers, that is 8,192 x 32 = 262,144 numbers.

Each number takes 2 bytes. So, one token needs 262,144 x 2 = 524,288 bytes. That is 0.5 MB. Here, 1 MB is about a million bytes, and 1 GB is about a thousand MB.

Let's see the code for this calculation as below:

```python
layers = 32
heads = 32
[…321ln elided…]
A large model needs a lot of memory. It needs powerful and costly hardware. It takes more time to give an answer. This delay between asking and getting the answer is called latency. High latency means the user waits longer.

Now, think about where we want to use AI.

We want AI on our phones. We want AI on small devices like a smartwatch, a camera, or a car. These small devices are called edge devices, because they sit at the "edge", close to the user, far from big data centers. Edge devices have little memory and little battery. A huge model simply cannot fit there.

We also want AI to respond instantly. A chat reply that takes ten seconds feels broken. We want low latency.

And, we want AI to be cheap to run. Running a giant model for millions of users costs a lot of money.

So, the situation is this:

- The big model is accurate but slow and expensive.
- The small model is fast and cheap but less accurate on its own.

We want the best of both. We want a small, fast, cheap model that still keeps most of the accuracy of the big model.

So, here comes Knowledge Distillation to the rescue. It lets us shrink the brain into a smaller body while keeping most of the intelligence.

To go deep into Model Compression, Quantization and Optimizations, and Cloud vs On-device Deployment, check out our AI and Machine Learning Program at Outcome School.

Now, to understand how the teacher passes its knowledge, we must first understand the difference between hard labels and soft labels.

### Hard labels vs soft labels

Let's take a simple example. Suppose we are building a model that looks at a photo and decides what is in it. The possible answers are `cat`, `dog`, `car`, and `horse`. Each possible answer is called a class.

Now, suppose we show the model a photo of a cat.

A hard label is the single correct answer, and nothing more. For this photo, the hard label says: this is a `cat`. We can write it like this.

```
cat   = 1
dog   = 0
car   = 0
horse = 0

```

Here, we can see that the hard label gives full marks to `cat` and zero to everything else. It is just the plain truth, with no extra information.

Now, let's look at what the teacher model actually produces. When the teacher sees the cat photo, it does not output just one word. It outputs a probability for every class. A probability is a number between 0 and 1 that tells us how confident the model is. All the probabilities add up to 1.

This full set of probabilities is called a soft label or a probability distribution. It can look like this.

```
cat   = 0.90
dog   = 0.08
car   = 0.01
horse = 0.01

```

Here, we can see that the teacher is 90% sure it is a `cat`. But it also gives a small 8% to `dog`, and almost nothing to `car` and `horse`.

So, the difference is simple.

- A hard label says only "it is a cat".
- A soft label says "it is mostly a cat, a little bit like a dog, and not at all like a car".

This small extra information turns out to be very powerful. Let's understand why.

### Dark knowledge

The soft label carries hidden information that the hard label throws away. This hidden information is called dark knowledge.

In simple words, dark knowledge is what the teacher knows about how the classes relate to each other.

Let's go back to our cat photo. The teacher gave `dog` an 8% chance and `car` almost 0%. Think about what this is telling us. The teacher is saying: a cat looks somewhat like a dog, but a cat looks nothing like a car.

This is true knowledge about the world. Cats and dogs are both furry, four-legged animals, so they can be confused. A cat and a car have nothing in common, so they are never confused.

A hard label can never teach this. A hard label only says "cat", and treats "dog" and "car" as equally wrong. But they are not equally wrong. Being a little bit "dog" is a reasonable mistake. Being "car" is a silly mistake.

So, when the student learns from the soft labels, it learns these relationships. It learns that cats and dogs are close. It learns that cats and cars are far apart. This is much richer than just memorizing the single right answer.

This is the heart of Knowledge Distillation. The soft labels of the teacher teach the student far more than a plain hard label ever could.

Let's make this concrete with a comparison.

```
   HARD LABEL                 SOFT LABEL (from teacher)
   -----------                -------------------------
   cat   = 1                  cat   = 0.90   <- the answer
   dog   = 0                  dog   = 0.08   <- "a bit like a dog"
   car   = 0                  car   = 0.01   <- "nothing like a car"
   horse = 0                  horse = 0.01   <- "nothing like a horse"

   Tells: only the answer     Tells: the answer + how classes relate

```

Here, we can see that the soft label on the right is doing extra teaching that the hard label on the left simply cannot do.

Now, there is one more problem. Sometimes the teacher is too confident. It can say `cat = 0.99` and give almost nothing to the others. When that happens, the useful dark knowledge becomes very tiny and hard to see. We need a way to bring out these small numbers. So, here comes temperature into the picture.

### Temperature in the softmax

Before we explain temperature, we must understand one small step that happens inside the model.

When a model makes a prediction, it first produces raw scores for each class. These raw, unprocessed scores are called logits. A logit can be any number, like `8.2` or `-1.4`. These raw scores are hard to read directly.

To turn these raw scores into clean probabilities that add up to 1, the model uses a function called the softmax. The softmax takes the logits and squashes them into nice probabilities between 0 and 1.

We have a detailed blog on Cross-Entropy Loss that explains logits and the softmax in depth.

Now comes the clever part. The softmax has a knob we can turn, called the temperature, often written as `T`.

In simple words, temperature controls how soft or how sharp the probabilities come out.

- A low temperature (like `T = 1`) gives sharp probabilities. One class gets a very high value, and the rest get tiny values.
- A high temperature (like `T = 4`) gives softer, more spread-out probabilities. The smaller values grow bigger and become easier to see.

Let's see this with our cat example. At a normal temperature, the teacher is very confident.

```
T = 1  (sharp):    cat = 0.95   dog = 0.04   car = 0.005   horse = 0.005

```

Now, if we raise the temperature, the same prediction spreads out.

```
T = 4  (soft):     cat = 0.70   dog = 0.22   car = 0.05    horse = 0.03

```

Here, we can see that at the higher temperature, the `dog` value jumped from 0.04 to 0.22. The dark knowledge, which means the relationship between cat and dog, is now clear and loud. The student can learn from it much more easily.

So, during distillation, we raise the temperature so the teacher's soft labels reveal these subtle relationships. The student gets a clearer, richer lesson.

Note: We use the higher temperature only during training. When the finished student is actually used in the real world, we go back to the normal temperature.

Now, we have soft labels, dark knowledge, and temperature. The next question is: how exactly do we train the student using all this? The answer is the distillation loss.

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

### The distillation loss

To train any model, we need a way to measure how wrong it is. This measure of wrongness is called the loss. Training means slowly changing the model's numbers to make the loss as small as possible. A smaller loss means the model is making better predictions.

In Knowledge Distillation, the student must do two things at the same time.

First, it must match the teacher's soft labels. The student looks at a photo, produces its own soft probabilities, and we compare them to the teacher's soft probabilities. We want them to be as close as possible. The measure of how different two probability distributions are is called KL divergence. We do not need the math. We only need to know that a smaller KL divergence means the two distributions are more similar. This part is called the distillation loss.

Second, the student must also get the true answer right. We compare the student's prediction to the real hard label, the actual truth. This part is the normal loss, the same loss we would use to train any model from scratch.

Now, why do we keep both? Because each one helps.

- The distillation loss teaches the rich dark knowledge from the teacher.
- The normal loss keeps the student grounded in the real, correct answers, so it does not blindly copy the teacher's mistakes.

So, the total loss is a blend of the two.

```
Total loss  =  part 1  +  part 2

part 1  =  weight       x  distillation loss   (student vs teacher soft labels)
part 2  =  (1 - weight) x  normal loss         (student vs true hard labels)

```

Here, we can see that the total loss is just a weighted mix. The `weight` is a number we choose that decides how much the student must listen to the teacher versus the true answer. For example, we often give more weight to the teacher's soft labels, because that is where the extra knowledge lives.

The flow looks like below:

```
                    +----------------+        +----------------+
   same photo --->  |  TEACHER       |        |  STUDENT       |  <--- same photo
                    |  (big model)   |        |  (small model) |
                    +----------------+        +----------------+
                            |                         |
                teacher     |                         |  student
                soft labels v                         v  soft labels
                    +------------------------------------------+
                    |  distillation loss  (student vs teacher) |
                    +------------------------------------------+
                                        |
                                        v
                              +--------------------+
                              |     TOTAL LOSS     |
                              |   (weighted mix)   |
                              +--------------------+
                                        ^
                                        |
                    +------------------------------------------+
                    |  normal loss  (student vs true label)    |
                    +------------------------------------------+
                            ^                         ^
                            |                         |
                    true hard label           student prediction

```

Here, we can see that the same photo goes into both the teacher and the student. The distillation loss measures how far the student's soft labels are from the teacher's soft labels. The normal loss measures how far the student's prediction is from the true hard label. Both losses are then blended into one total loss, which is the single number we make smaller during training.

This combined loss is the engine of Knowledge Distillation. By making this total loss small, the student learns the correct answers and the teacher's wisdom together.

Now, let's put all the pieces into one clear walkthrough.

### A step-by-step training walkthrough

Let's walk through exactly what happens when we distill knowledge from the teacher into the student. We will use our animal photo example.

Step 1: We start with a trained teacher model. The teacher is big and already accurate. We do not change the teacher at all during distillation. It only gives lessons.

Step 2: We take a fresh, small student model. The student starts with random numbers and knows nothing yet.

Step 3: We take a photo from our training data, for example, our cat photo.

Step 4: We pass the photo through the teacher. We use a high temperature so the teacher produces soft labels full of dark knowledge, like `cat = 0.70, dog = 0.22, car = 0.05, horse = 0.03`.

Step 5: We pass the same photo through the student. The student produces its own soft labels at the same high temperature, for example, `cat = 0.50, dog = 0.30, car = 0.15, horse = 0.05`.

Step 6: We calculate the distillation loss by comparing the student's soft labels to the teacher's soft labels using KL divergence. Right now they are different, so this loss is high.

Step 7: We also calculate the normal loss by comparing the student's normal prediction to the true hard label, `cat = 1`. For this part, we use the normal temperature.

Step 8: We blend the two losses into the total loss using our chosen weight.

Step 9: We slightly adjust the student's numbers to make this total loss smaller. This single adjustment is called one training step.

Step 10: We repeat Steps 3 to 9 for thousands of photos, again and again.

Slowly, the student's soft labels start to match the teacher's. The student learns not just the answers, but also the rich relationships between classes. After enough training, the student becomes a small, fast model that behaves almost like the big teacher.

We have a detailed blog on Gradient Descent that explains how this adjustment to the model's numbers works step by step.

This is how Knowledge Distillation actually trains the student. Now, let's see the different types of it.

### Types of Knowledge Distillation

Everything we have learned so far is the most common form, but there are three main types. The difference is simply about which part of the teacher the student copies. Let's keep it simple.

Response-based distillation. This is what we have been doing the whole time. The student copies the teacher's final output, which means the soft labels at the end. The student watches what the teacher answers and learns to answer the same way. This is the simplest and most popular type.

Feature-based distillation. A model does not jump straight from input to answer. It processes the input step by step through inner stages called layers. The output of these inner stages is called a feature, which is the model's internal understanding before the final answer. In feature-based distillation, the student copies these inner features of the teacher, not just the final output. It is like a student copying not only the senior's final answer but also the rough working and notes the senior wrote on the way.

Relation-based distillation. Here, the student learns the relationships between different things the teacher saw. For example, the teacher can treat two photos as very similar to each other. The student learns to keep those same two photos similar in its own understanding. So, the student copies the connections the teacher draws between examples, not just single answers.

So, to summarize the three types simply.

```
Response-based  ->  copy the teacher's FINAL answer (soft labels)
Feature-based   ->  copy the teacher's INNER understanding (features in layers)
Relation-based  ->  copy the RELATIONSHIPS the teacher sees between examples

```

Here, we can see that all three share the same goal. The student tries to behave like the teacher. They only differ in which part of the teacher's behavior the student copies. We can pick one based on our use case.

To master Knowledge Distillation, SLMs and Model Distillation, and Model Compression in depth, check out our AI and Machine Learning Program at Outcome School.

Now, let's look at where Knowledge Distillation is used in the real world.

### Real examples of Knowledge Distillation

DistilBERT. BERT is a famous language model used to understand text. It is powerful but big. DistilBERT is a distilled version of BERT. It is much smaller and faster, around 40% smaller and about 60% faster, while keeping roughly 97% of BERT's language understanding. This is a perfect example of the trade we want: a much lighter model that keeps almost all the accuracy.

Smaller chat models. Many small chat models are distilled from much larger chat models. The large model acts as the teacher and produces high-quality answers. The small model is trained to copy those answers. The result is a compact chat model that can run cheaply and reply fast, while still sounding close to the big one. We have a detailed blog on Small Language Models (SLMs) that covers these compact models end to end.

On-device AI. This is where distillation truly shines. When we want AI to run directly on a phone, a smartwatch, or a camera, the model must be tiny and quick. We distill a big, accurate model into a small student that fits on the device. So, features like offline translation, voice typing, and smart photo sorting can run right on the device, without sending data to a server. This means faster results, lower cost, and better privacy, because our data stays on the device. On-device models like these are usually shipped in the GGUF format. We have a detailed blog on how GGUF works that explains how these models are packed into one file.

So, now we know where we can use Knowledge Distillation, and why it matters so much for real products.

Distillation is one way to get a smaller model. Another is quantization, where we keep the same model but store its numbers using fewer bits. We have a detailed blog on how Model Quantization works that explains this from the ground up.

### Wrapping up Knowledge Distillation

Let's quickly recap everything in simple words.

A big model, the teacher, is accurate but slow and expensive. A small model, the student, is fast and cheap but less smart on its own. Knowledge Distillation trains the student to copy the teacher, so we get a small model that keeps most of the big model's accuracy.

The key idea is that the teacher does not just give the right answer. It gives soft labels, a full set of probabilities over all classes. These soft labels carry dark knowledge, which means they reveal how the classes relate to each other, like a cat being a little bit "dog" and nothing like a "car". We use a higher temperature in the softmax to make this dark knowledge clear and easy to learn.

We train the student with a combined loss. The distillation loss pulls the student toward the teacher's soft labels using KL divergence, and the normal loss keeps the student correct on the true hard labels. We repeat this over many examples until the student behaves like the teacher.

This is how Knowledge Distillation works.

### Does the teacher model change during Knowledge Distillation?

No. The teacher is a big model that is already trained and accurate. We do not change the teacher at all during distillation. It only gives lessons in the form of soft labels, and only the student's numbers are adjusted to make the total loss smaller.

### Why not train the small model only on the true labels?

Because hard labels throw away useful information. A hard label only says "it is a cat" and treats every other class as equally wrong. The teacher's soft labels also show how classes relate, like a cat being a little bit like a dog and nothing like a car. This dark knowledge teaches the student far more.

### Is the high temperature also used when the student model is deployed?

No. We use the higher temperature only during training, so the teacher's soft labels reveal the subtle relationships between classes. When the finished student is actually used in the real world, we go back to the normal temperature.

### Does the student simply copy the teacher's mistakes?

Not blindly. The total loss blends two parts. The distillation loss pulls the student toward the teacher's soft labels, and the normal loss compares the student to the true hard labels. This normal loss keeps the student grounded in the real, correct answers, so it does not blindly copy the teacher's mistakes.

### What is the difference between Knowledge Distillation and quantization?

Both make a model smaller, but in different ways. Knowledge Distillation trains a separate small student model to copy a big teacher model. Quantization keeps the same model but stores its numbers using fewer bits.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-420 and 742-1062 of 1062; 321 middle lines (19.1KB) elided. Read artifact://69 for full output]
