> Source: https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers

# Encoder vs Decoder in Transformers
URL: https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers
Published: 2026-08-06

Encoder vs Decoder in Transformers

# Encoder vs Decoder in Transformers

Authors
: - Name
: Amit Shekhar
Published on
: August 5, 2026

In Transformers, the Encoder reads the whole input at once, in both directions, to understand it. The Decoder generates the output one token at a time, and it can look only backward.

In this blog, we will learn about Encoder vs Decoder in Transformers, the two building blocks behind almost every modern AI model that works with language. We will also see how the Encoder and the Decoder differ from each other, how each one works with simple examples, why one of them reads in both directions while the other one looks only backward, what the three types of Transformers are, and when to use which one.

We will cover the following:

- What is a Transformer?
- A word about tokens
- What is an Encoder?
- What is a Decoder?
- The one big difference
- The three types of Transformers
- Let's tabulate the difference
- When to use which one?
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a Transformer?

Before jumping into Encoder and Decoder, we must know what a Transformer is.

A Transformer is the architecture behind most modern AI models that work with language. The AI tools we use today, like ChatGPT, Claude, and Gemini, are all built using the Transformer architecture.

The Transformer became famous because it is very good at understanding the relationship between words. It can look at a sentence and figure out how each word connects to the other words. This is what makes it so powerful with language.

Now, a Transformer is built from two main building blocks. One block is called the Encoder, and the other block is called the Decoder. In this blog, we will understand both of them and see how they differ.

Before that, we need to understand one small word, the token.

## A word about tokens

When a Transformer reads text, it does not read whole sentences at once. It breaks the text into small pieces. Each small piece is called a token.

A token is usually a word or a part of a word. For the sake of understanding, we can just think of a token as a word.

So, the sentence "I love AI" becomes three tokens: "I", "love", and "AI". The Transformer works on these tokens.

The exact rule for splitting the text into tokens comes from a tokenization algorithm. We have a detailed blog on Byte Pair Encoding in LLMs that explains how this works.

Now that we know about tokens, let's understand the Encoder.

## What is an Encoder?

The Encoder reads the whole input and builds a deep understanding of it.

In simple words, the job of the Encoder is to understand. It takes all the tokens of the input, looks at them together, and creates a rich meaning for each token.

Here is the most important point about the Encoder. It can look at all the tokens at the same time, both to the left and to the right of any word. It reads the whole sentence at once. This is why we say the Encoder looks in both directions.

Let's understand why both directions matter. Consider the sentence, "The bank of the river was muddy." Here, the word "bank" is confusing. It could mean a money bank or the side of a river. To understand it correctly, we must read the word "river" that comes later. The Encoder can do this, because it reads the full sentence at once and looks in both directions.

We can picture the Encoder like below:

```
   Input tokens:   [The]  [bank]  [of]  [the]  [river]  [was]  [muddy]

                     Every token looks at ALL other tokens
                      (both left and right, all at once)

                                    |
                                    v
   Output:   a deep understanding (meaning) for each token

```

Here, we can see that each token is allowed to look at every other token in the sentence. This looking at each other is done by a mechanism called Self Attention. Because of this, the Encoder understands the full meaning very well.

So, the Encoder is like a careful reader. It reads the whole thing first and understands it deeply. It does not write anything new. It only understands.

To learn the Attention Mechanism, Self-Attention, and Transformer Architecture in depth, check out our AI and Machine Learning Program at Outcome School.

## What is a Decoder?

Now that we have learned about the Encoder, it's time to learn about the Decoder.

The Decoder generates the output, one token at a time.

In simple words, the job of the Decoder is to write. It produces the answer token by token, from left to right, just like we write a sentence word by word.

Here is the most important point about the Decoder. While writing, it can only look at the tokens that came before. It cannot look at the future tokens, because those tokens are not written yet. This makes sense. When we write a sentence, we do not know the next word until we write it. Inside the model, this is enforced by a causal mask that hides the future tokens.

Let's understand this with an example. Suppose the Decoder is writing "The sky is blue". When it is about to write "blue", it can look at "The", "sky", and "is". But it cannot look at "blue" itself, because that is the word it is trying to guess right now.

We can picture the Decoder like below:

```
   Step 1:  <start>                 ->  predict next  ->  "The"
   Step 2:  <start> The             ->  predict next  ->  "sky"
   Step 3:  <start> The sky         ->  predict next  ->  "is"
   Step 4:  <start> The sky is      ->  predict next  ->  "blue"

   (each step can only look back at the words already written)

```

Here, we can see that the Decoder builds the sentence one word at a time, always looking only at the words behind it.

So, the Decoder is like a writer. It creates new text step by step, using only what it has written so far. This way of generating, where each new token depends on the tokens that came before it, is what makes it an autoregressive model.

## The one big difference

If we forget everything else, we must remember this one line.

> The Encoder reads and understands the whole input at once. The Decoder writes new output one token at a time, looking only at the past.

That is the heart of the difference. The Encoder is a reader that looks in both directions. The Decoder is a writer that looks only backward.

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

## The three types of Transformers

Now, here is something interesting. We can build a Transformer using only the Encoder, only the Decoder, or both together. This gives us three types of Transformers, and each one is good for a different job.

Let's understand all three.

1. Encoder-only: This uses only the Encoder. Its job is pure understanding. It is great for tasks like deciding if a review is positive or negative, or turning text into embeddings for search. A famous example is a model called BERT.

2. Decoder-only: This uses only the Decoder. Its job is pure generation. It writes text one token at a time. Most modern chat AI models are decoder-only, like the models behind ChatGPT, Claude, and Gemini.

3. Encoder-Decoder: This uses both blocks together. The Encoder first reads and understands the input. Then the Decoder writes the output based on that understanding. This is great for tasks where we take one full text and turn it into another, like translating a sentence from English to French. A famous example is a model called T5.

We can picture the three types like below:

```
   Encoder-only        Decoder-only        Encoder-Decoder
   ------------        ------------        ---------------
   Encoder             Decoder             Encoder + Decoder
       |                   |                   |
       v                   v                   v
   understand          generate            understand, then
   the input           the output          generate
       |                   |                   |
       v                   v                   v
   (BERT)              (ChatGPT)           (T5)

```

Here, we can see the three types at a glance. The Encoder-only type only understands. The Decoder-only type only generates. The Encoder-Decoder type first understands and then generates.

That pure understanding is what makes the Encoder-only type a great fit for search. We have a detailed blog on Decoding ColBERT that explains how a BERT encoder is turned into a fast, word-level retrieval model.

Let's understand the Encoder-Decoder flow with a translation example like below:

```
   English input: "I love AI"
          |
          v
   +---------------+
   |    Encoder    |   reads and understands the full English sentence
   +---------------+
          |
          |  passes the understanding to the Decoder
          v
   +---------------+
   |    Decoder    |   writes the French output, one token at a time
   +---------------+
          |
          v
   French output: "J'aime l'IA"

```

Here, we can see the teamwork. The Encoder understands the English sentence fully. Then the Decoder uses that understanding to write the French sentence step by step. The bridge that carries this understanding from the Encoder into the Decoder is Cross Attention.

## Let's tabulate the difference

Let me tabulate the differences between the Encoder and the Decoder for your better understanding.

| Point | Encoder | Decoder |
| --- | --- | --- |
| Main job | Understand the input | Generate the output |
| How it reads | Looks at all tokens at once | Writes one token at a time |
| Direction | Both directions (left and right) | Only backward (past tokens) |
| Good for | Understanding tasks | Writing tasks |
| Example model | BERT | The models behind ChatGPT, Claude |

## When to use which one?

This is the real question. Let's make it very simple.

The trick is to look at the task we want to solve.

- If our task is to understand text, like sorting reviews or searching, we use an Encoder-only model.
- If our task is to generate text, like chatting or writing, we use a Decoder-only model.
- If our task is to take one full text and turn it into another, like translation or summarization, we use an Encoder-Decoder model.

So, we must always ask ourselves: do we want to understand, to generate, or to convert one text into another? The answer decides which one to use.

Note: Today, most popular chat AI models are decoder-only. This is because a good writer must also understand well, and it turns out that a large Decoder learns to do both understanding and writing at the same time. This is why decoder-only models power most of the AI chat tools we use today.

## Summary

Let's quickly recap what we have learned.

- A Transformer is the architecture behind most modern language AI, and it is built from two blocks: the Encoder and the Decoder.
- The Encoder reads the whole input at once and understands it deeply, looking in both directions.
- The Decoder writes the output one token at a time, looking only at the past tokens.
- We can build three types: Encoder-only for understanding, Decoder-only for generation, and Encoder-Decoder for converting one text into another.
- Most modern chat AI models today are decoder-only.

This is how the Encoder and the Decoder work as the two building blocks of a Transformer.

Now, we must have understood Encoder vs Decoder in Transformers.

### Is ChatGPT an encoder model or a decoder model?

ChatGPT is built on a decoder-only model. Most modern chat AI models, like the models behind ChatGPT, Claude, and Gemini, are decoder-only. Their job is pure generation, writing text one token at a time while looking only at the tokens that came before.

### Why are most chat models decoder-only if they also need to understand text?

A good writer must also understand well, and a large Decoder learns to do both understanding and writing at the same time. This is why decoder-only models power most of the AI chat tools we use today.

### Can BERT be used to generate text like ChatGPT?

No. BERT is an Encoder-only model, and its job is pure understanding. It does not write anything new. It is great for tasks like deciding if a review is positive or negative, or turning text into embeddings for search.

### How does the Decoder use what the Encoder understood?

The Decoder uses Cross Attention. In an Encoder-Decoder model, the Encoder first reads and understands the full input. Cross Attention is the bridge that carries this understanding into the Decoder, which then writes the output one token at a time, like a French translation of an English sentence.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

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

[…585ln elided…]
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

[Showing lines 1-418 and 1004-1324 of 1324; 585 middle lines (32.2KB) elided. Read artifact://37 for full output]
