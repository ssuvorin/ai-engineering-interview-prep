> Source: https://outcomeschool.com/blog/llm-inference-optimization

# LLM Inference Optimization
URL: https://outcomeschool.com/blog/llm-inference-optimization
Published: 2026-06-14

LLM Inference Optimization

# LLM Inference Optimization

Authors
: - Name
: Amit Shekhar
Published on
: June 13, 2026

LLM Inference Optimization is the set of techniques that make a Large Language Model generate its answers faster and serve more users at a lower cost.

Techniques like KV Cache, Paged Attention, Flash Attention, Speculative Decoding, and Continuous Batching are what make LLMs fast and scalable in production. Let’s learn all of these techniques one by one.

## KV Cache in LLMs

In this blog, we will learn about KV Cache - where K stands for Key and V stands for Value - and why it is used in Large Language Models (LLMs) to speed up text generation.

We will start with how LLMs generate text one token at a time, understand the role of Key, Value, and Query inside the model, see the problem of repeated computation through an example, and then walk through how KV Cache solves this problem by storing and reusing past results.

## KV Cache Compression

In this blog, we will learn about KV Cache Compression, the set of techniques that shrink the memory an AI model uses to remember the conversation while it is writing its reply.

We will cover the following:

- What is an LLM and how it writes text
- What is Attention
- What is the KV Cache
- Why the KV Cache becomes huge
- What is KV Cache Compression
- Approach 1: Quantization
- Approach 2: Token Eviction
- Approach 3: Sharing Keys and Values across Heads
- Approach 4: Low-Rank Compression
- Comparison of the approaches
- When to use which one

Read here: KV Cache Compression

## Paged Attention in LLMs

In this blog, we will learn about Paged Attention, a technique that solves the memory waste problem of KV Cache, allowing LLMs to serve many more users at the same time.

We will start with a quick recap of KV Cache, understand the memory problem it creates, see how traditional memory allocation wastes space through an example, and then walk through how Paged Attention solves this problem by borrowing an idea from how computers manage memory.

## Decoding Flash Attention in LLMs

In this blog, we will learn about Flash Attention by decoding it piece by piece - understanding why standard attention is slow, what makes Flash Attention fast, how it uses GPU memory cleverly, and why it is used in almost every modern Large Language Model (LLM).

We will cover the following:

- A quick recap of standard attention
- Why standard attention is slow
- How GPU memory actually works (HBM vs SRAM)
- The core idea behind Flash Attention
- Tiling: breaking the work into small blocks
- Online softmax: computing softmax without the full matrix
- Recomputation in the backward pass
- Flash Attention 2
- Flash Attention 3
- Advantages and impact of Flash Attention

## Grouped Query Attention

In this blog, we will learn about Grouped-Query Attention (GQA) and how it differs from Multi-Head Attention (MHA).

Today, we will cover the following topics:

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

Read here: Grouped Query Attention

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

## Speculative Decoding

In this blog, we will learn about Speculative Decoding - what it is, why LLM generation is slow without it, how a small draft model and a big target model work together to produce tokens faster, the rejection sampling math that guarantees no quality loss, real numbers showing the 2× to 3× speedup, where it is used in production, and the trade-offs to watch out for.

We will cover the following:

- What problem does Speculative Decoding solve?
- The Big Picture
- Why is LLM generation slow?
- The core idea behind Speculative Decoding
- Step-by-step walkthrough
- The verification step
- Real numbers and speedup
- Where it is used
- Trade-offs
- Quick Summary

## Decoding Medusa

In this blog, we will learn about Medusa, a simple way to make a language model generate text 2 to 3 times faster by giving it several extra heads that guess multiple future tokens at once.

We will cover the following:

- What is Medusa
- Why text generation is slow
- A quick recap of speculative decoding
- The problem with needing a draft model
- The big idea: many heads on one model
- How tree attention checks many guesses at once
- The math behind the speedup with small numbers
- The results
- How Medusa lives on today
- Quick Summary

## Decoding EAGLE

In this blog, we will learn about EAGLE, a state-of-the-art way to speed up language model generation by drafting tokens at the feature level instead of the token level.

We will cover the following:

- What is EAGLE
- A quick recap of speculative decoding
- The problem with token-level drafting
- The big idea: draft at the feature level
- Resolving the uncertainty by feeding back the token
- The math behind the speedup with small numbers
- EAGLE-2 and dynamic draft trees
- How EAGLE lives on today
- Quick Summary

## N-gram Speculation in LLMs

In this blog, we will learn about N-gram Speculation in LLMs, a simple trick that makes a language model write its answer faster by guessing the next few words from the text it has already seen.

We will cover the following:

- How an LLM generates text
- Why generating text is slow
- What is Speculative Decoding
- The cost of a draft model
- What is an N-gram
- What is N-gram Speculation
- N-gram Speculation step by step
- Why the output stays exactly the same
- Where it works well and where it fails
- N-gram Speculation vs Draft Model Speculative Decoding

## Continuous Batching in LLMs

In this blog, we will learn about Continuous Batching, a technique that lets LLM servers handle many more users at the same time by keeping the GPU busy at every single step of generation.

We will cover the following:

- Quick Recap: How an LLM Generates Tokens
- Why Batching Matters for LLMs
- The Old Way: Static Batching
- The Problem with Static Batching
- What is Continuous Batching?
- The Ride-Share Analogy
- How Continuous Batching Works Step by Step
- A Numeric Example
- Real Numbers and Speedup
- Benefits of Continuous Batching
- A Few Important Notes
- Quick Summary

## Prompt Caching

In this blog, we will learn about how Prompt Caching works. We will also see why we need it, how it actually works inside a large language model, and where it is used in real systems like AI assistants and agents.

We will cover the following:

- What is a prompt
- A quick recap of how an LLM reads a prompt
- What is Prompt Caching
- Why we need Prompt Caching
- The core idea behind Prompt Caching
- The exact-prefix rule
- Cache write vs cache read and TTL
- What we should put in the cache
- The benefits of Prompt Caching
- Prompt Caching in the real world

## Prefill vs Decode: LLM Inference Optimization

In this blog, we will learn about Prefill vs Decode, the two phases of LLM inference, and how understanding them helps us optimize the speed of an LLM. We will also see how the prefill and decode phases work, how the KV cache connects them, how they differ and when to use which one based on our use case, and how we optimize each phase to make an LLM faster.

We will cover the following:

- The two phases: Prefill and Decode
- Prefill explained in simple words
- Decode explained in simple words
- A diagram of the two phases and the KV cache flow
- The KV cache as the bridge between the two phases
- A step-by-step walkthrough of a few decode steps
- Prefill vs Decode comparison table
- Why this split matters: compute-bound vs memory-bound
- The key metrics: TTFT, TPOT, throughput, and end-to-end latency
- Optimization techniques mapped to each phase

## Prefill-Decode Disaggregation

In this blog, we will learn about Prefill-Decode Disaggregation, a way of running a large language model where the reading of the prompt and the writing of the answer happen on separate machines.

We will cover the following:

- How an LLM answers a request
- What is the KV Cache?
- Prefill is compute-heavy, Decode is memory-heavy
- The problem when both run on the same GPU
- TTFT vs TPOT
- The naive approaches and their issues
- What is Prefill-Decode Disaggregation?
- How Prefill-Decode Disaggregation works
- Walkthrough of one request
- Advantages of Prefill-Decode Disaggregation
- Disadvantages of Prefill-Decode Disaggregation
- Where it works well and where it is overkill
- Co-located vs Disaggregated serving

## How does vLLM work?

In this blog, we will learn about how vLLM works. We will also see why we need it, how it manages memory so cleverly, and where it is used in the real world to serve large language models to many users at once.

We will cover the following:

- What is serving an LLM
- A quick recap of prefill, decode, and the KV cache
- The problem: the KV cache eats GPU memory
- Why naive serving wastes memory
- What is vLLM
- PagedAttention, the core idea
- How PagedAttention shares memory
- Continuous batching
- The OpenAI-compatible API server
- The benefits of vLLM
- vLLM in the real world

## How does SGLang work?

In this blog, we will learn about how SGLang works. We will also see what problem it solves, how it makes serving large language models faster, and the clever ideas that make it special.

We will cover the following:

- What is SGLang
- RadixAttention: the heart of SGLang
- How RadixAttention reuses past work
- The frontend language of SGLang
- Continuous batching in SGLang
- Structured output and faster decoding
- More powerful features of SGLang
- How SGLang compares to vLLM

## How does TensorRT-LLM work?

In this blog, we will learn about how TensorRT-LLM works, NVIDIA's own engine that squeezes the highest possible speed out of an NVIDIA GPU when it runs a large language model.

We will cover the following:

- What is inference
- What is a GPU and what is a kernel
- The problem: the GPU spends its time on the wrong things
- What is TensorRT-LLM
- The big idea: prepare the model ahead of time
- The build step: from a model to an engine
- Kernel fusion
- Quantization
- Custom attention kernels
- The paged KV cache
- In-flight batching
- CUDA graphs
- Speculative decoding
- Running one model across many GPUs
- How we actually serve the model
- The PyTorch backend, the newer and easier path
- The full journey of one request
- TensorRT-LLM vs vLLM
- Where it works well and where it fails

## How does Ollama work?

In this blog, we will learn about how Ollama works, the free tool that lets us download and run LLMs on our own computer with one simple command. We will also see why model files must be shrunk before they fit on a laptop, how Ollama's client and server talk to each other, and how models are loaded onto the CPU and GPU.

We will cover the following:

- What does running an LLM locally mean?
- What is Ollama?
- The big problem: models are huge
- Quantization and the GGUF file format
- The architecture: client and server
- What happens when we run a model?
- How models are downloaded and stored
- How the model runs on CPU and GPU
- What is a Modelfile?
- Using Ollama from code through its API
- Where it works well and where it fails

## How do CUDA Kernels work?

In this blog, we will learn about how CUDA Kernels work, the small programs that run on a GPU and do the heavy lifting behind almost every modern AI model.

We will cover the following:

- Why do we need a GPU?
- What is CUDA?
- What is a CUDA Kernel?
- Threads, Blocks, and Grids
- Host and Device
- Writing our first CUDA Kernel
- How a thread finds its own work
- What happens inside the GPU when a kernel runs
- Memory in CUDA
- Why CUDA Kernels matter for AI
- Where CUDA Kernels work well and where they fail

## How does an LPU work?

In this blog, we will learn about how an LPU works, the chip that was built for one single job, running a large language model that is already trained and producing text as fast as possible.

We will cover the following:

- What is an LPU
- How an LLM writes text, one token at a time
- The real bottleneck is memory, not math
- Why a GPU struggles here
- Keeping the model on the chip
- Removing all the guesswork with a compiler
- A network that never waits
- What happens when we send a prompt
- Where an LPU works well and where it does not
- LPU vs GPU

### Does Speculative Decoding reduce the quality of the output?

No. In Speculative Decoding, a small draft model and a big target model work together to produce tokens faster. The rejection sampling math guarantees no quality loss. It gives a speedup of around 2 to 3 times.

### Can we speed up generation without a separate draft model?

Yes. Medusa gives the model several extra heads that guess multiple future tokens at once, so it does not need a draft model. N-gram Speculation guesses the next few words from the text the model has already seen.

### What is the difference between the prefill and decode phases?

Prefill and decode are the two phases of LLM inference. Prefill reads the prompt and is compute-heavy, while decode writes the answer and is memory-heavy. The KV cache acts as the bridge between the two phases. Prefill-Decode Disaggregation goes one step further and runs these two phases on separate machines.

### Which techniques help an LLM server handle more users at the same time?

Paged Attention and Continuous Batching both help here. Paged Attention solves the memory waste problem of the KV Cache, allowing LLMs to serve many more users at the same time. Continuous Batching keeps the GPU busy at every single step of generation, so the server can handle many more users.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# How does Cursor work?
URL: https://outcomeschool.com/blog/how-does-cursor-work
Published: 2026-07-22

How does Cursor work?

# How does Cursor work?

Authors
: - Name
: Amit Shekhar
Published on
: July 22, 2026

In this blog, we will learn about how Cursor works. We will also see what Cursor is, why it is a code editor with an AI brain on top, how it indexes our codebase into embeddings and searches it by meaning, how Tab autocomplete, Chat, and Agent mode work, how Cursor applies changes through a diff, why it uses different models for different jobs, and how it tries to keep our code private.

We will cover the following:

- What is Cursor?
- Cursor = Code Editor + AI
- The big idea behind Cursor
- How does Cursor understand our code?
- How does Cursor index our codebase?
- How does Tab autocomplete work?
- How does the Chat work?
- How does the Agent mode work?
- How does Cursor apply the changes?
- Why does Cursor use different models?
- How does Cursor keep our code private?
- The complete flow of Cursor

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Cursor?

Cursor is an AI code editor. It is a place where we write our code, but with an AI helper sitting right next to us.

Let's say we are writing code. Normally, we type every single line by ourselves. We think, we type, we fix the mistakes, and we repeat. It takes time.

Now, imagine a smart friend sitting next to us. This friend has read a lot of code. When we start typing, the friend already guesses what we want to write next. When we get stuck, we simply ask the friend, and the friend writes the code for us. When we want to build a whole feature, we just describe it in plain English, and the friend does the work across many files.

That smart friend is Cursor.

So, Cursor is a code editor where an AI is always ready to help us read, write, and change our code.

## Cursor = Code Editor + AI

Let's understand both parts.

Code Editor: A code editor is a simple app where we open our files and write our code. Cursor is built on top of a very popular code editor called VS Code. So, if we have ever used VS Code, then Cursor will feel the same. All the buttons, the file explorer on the left, the tabs on the top, everything feels familiar.

AI: This is the special part. Cursor connects our editor to powerful AI models. These AI models are the same kind of models that power tools like ChatGPT. They can read text, understand it, and write text. And code is also just text. So, these AI models can read our code and write new code for us.

So, Cursor takes a normal code editor and adds a powerful AI brain on top of it. That is the whole idea.

## The big idea behind Cursor

Before jumping into the details, we must understand the big idea. It will make everything else easy.

The AI model does not live inside Cursor. The AI model lives on a big computer far away, called a server. This server belongs to companies that build these models.

So, Cursor is like a bridge. On one side, there is us and our code. On the other side, there is the powerful AI model on the server.

We can picture it like below:

```
                        sends our code + question
   +----------------+  ----------------------------->  +-------------------+
   |     Cursor     |                                   |     AI model      |
   |  (our editor   |                                   |  (on the server)  |
   |   + our code)  |  <-----------------------------   |                   |
   +----------------+       returns the answer          +-------------------+

```

Here, we can see that our code never runs the AI by itself. Cursor sends the needed pieces to the AI model and brings the answer back.

When we ask for help, Cursor does three things:

- First, it collects the right pieces of our code. This is called context.
- Then, it sends our question along with that context to the AI model.
- Finally, it takes the answer from the AI model and puts it back into our code.

Here, the most important word is context. The AI model has never seen our project before. It does not know our files. So, Cursor must send the right pieces of our code to the AI model, so that the AI can give a useful answer.

Let's say we ask a doctor for advice over the phone. The doctor is very smart, but the doctor cannot see us. So, we must describe our problem clearly. The better we describe it, the better the advice.

In the same way, the AI model is very smart, but it cannot see our project. So, Cursor must describe our code clearly to the AI model. This is the real magic of Cursor. It is very good at picking the right pieces of our code and sending them to the AI.

Now, let's understand how Cursor does this.

## How does Cursor understand our code?

Let's say our project has a thousand files. When we ask a question, the AI model cannot read all thousand files at once. It is too much. It would be slow and very costly.

So, Cursor must find only the few files that matter for our question. This is the real problem to solve.

For example, we ask, "Where do we check the user's password?" Cursor must find the file that handles the password. It must not send the file that handles the app color or the file that handles the images.

So, how does Cursor find the right files? Here comes the indexing to the rescue. Let's understand it.

## How does Cursor index our codebase?

Indexing means Cursor reads all our files once and prepares them in a smart way, so that later it can search through them very fast.

Let's understand this step by step.

Step 1: Cursor breaks our code into small pieces. Each piece is called a chunk. A chunk is usually a small part of a file, like one function or a few lines that belong together.

[…573ln elided…]

So, anywhere we keep sending the same large beginning of a prompt, Prompt Caching helps us a lot.

If we want to go deep into RAG, Vector Databases, and AI Agents, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

This is how Prompt Caching works. We save the model's internal work for a fixed, repeated beginning of the prompt, we keep that beginning exactly the same and place it first, and then we reuse it again and again to get faster and cheaper responses.

### What is the difference between prompt caching and semantic caching?

Prompt caching reuses the model's internal work, the KV cache, for a repeated beginning of a prompt. The model still reads the new part and writes a fresh reply. Semantic caching reuses the final answer whenever a new question means the same thing, even if the words are different.

### Does prompt caching change the quality of the answers?

No. Prompt caching makes our application faster and cheaper without changing the quality of the answers. The model still sees the full prompt. It just avoids redoing the work for the repeated part that it has already done.

### Why is our prompt cache not getting any hits?

A very common reason is something that changes near the top of the prompt, like the current date, a random ID, or a user name. The cached part must match exactly, character for character, so even one early change breaks the cache for everything after it. We should put the stable part first and the changing part last.

### Is prompt caching always cheaper?

Not for the first request. A cache write costs a little more than normal processing, around 1.25 times the normal price. The savings come from later cache reads, which cost around one-tenth of the normal price. So caching pays off when many requests share the same beginning and arrive within the TTL window.

### How do we know if prompt caching is actually working?

We can check the response from the provider. It shows how many tokens were written to the cache and how many were read from it. If later requests show tokens read from the cache, the caching is working.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# How does Semantic Caching work?
URL: https://outcomeschool.com/blog/how-does-semantic-caching-work
Published: 2026-07-08

How does Semantic Caching work?

# How does Semantic Caching work?

Authors
: - Name
: Amit Shekhar
Published on
: July 7, 2026

Semantic Caching is a cache that matches questions by their meaning instead of their exact words. So, if a new question means the same as an old one, the AI app can reuse the saved answer.

In this blog, we will learn about how Semantic Caching works. We will also see why traditional caching falls short for AI apps, how Semantic Caching uses embeddings and similarity to reuse past answers, and how setting the right threshold makes it work in the real world.

We will cover the following:

- What is a cache?
- The problem with traditional caching for AI apps
- What is Semantic Caching?
- What are embeddings?
- What is similarity between embeddings?
- How does Semantic Caching work step by step?
- A numeric walkthrough
- Setting the similarity threshold
- Advantages of Semantic Caching
- Things to keep in mind

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a cache?

A cache is a place where we store the answer to a question, so that the next time the same question comes, we can return the saved answer instantly.

In simple words, a cache is a memory of past answers.

Let's say a friend asks us, "What is the capital of France?" We answer, "Paris." If the same friend asks the same question again, we do not think again. We simply say "Paris" because we remember it.

That memory of past answers is the cache. It saves us time, and it saves us effort.

This is how a cache works in software too. The first time, we do the hard work and compute the answer. After that, we store it. The next time, we return the stored answer directly.

### The problem with traditional caching for AI apps

Now, let's understand why normal caching is not enough for AI apps.

Suppose we are building an app that uses a Large Language Model that powers tools like ChatGPT. Every time a user asks a question, our app sends that question to the model, the model thinks, and then it returns an answer.

But, here is the catch. Sending a question to the model costs money, and it also takes time. If a thousand users ask the same thing, we pay a thousand times, and each user waits.

So, we think of caching. We store each question and its answer. The next time the exact same question comes, we return the stored answer.

This is called exact-match caching. It matches the question word by word, letter by letter.

Let's see the problem with an example. Assume that two users ask these questions:

- User 1: "What is the capital of France?"
- User 2: "Tell me the capital city of France."

For us humans, both questions mean the same thing. The answer is "Paris" in both cases.

But for exact-match caching, these two are completely different. The words are different, the order is different, so the cache thinks they are two separate questions. It will send the second question to the model again, and we pay again.

The issue with this approach is that it only understands letters, not meaning. People ask the same thing in many different ways, so the cache almost never matches.

We needed a solution for that, and Semantic Caching was introduced to solve this problem.

### What is Semantic Caching?

Semantic Caching is a cache that matches questions by their meaning instead of their exact words.

Let's break the term to understand it better.

> Semantic Caching = Semantic + Caching

The word "semantic" simply means "related to meaning." So, Semantic Caching is caching based on meaning.

In simple words, if a new question means the same thing as an old question, we return the old answer, even if the words are different.

Going back to our example, "What is the capital of France?" and "Tell me the capital city of France." mean the same thing. So, Semantic Caching treats them as a match and returns "Paris" without asking the model again.

This is the beauty of Semantic Caching. It understands intent, not just text.

Now, the next big question is: how does a computer understand the meaning of a sentence? A computer only understands numbers. So, here come embeddings into the picture.

### What are embeddings?

An embedding is a list of numbers that represents the meaning of a piece of text.

In simple words, an embedding turns a sentence into numbers, in such a way that sentences with similar meaning get similar numbers.

Let's understand this with a simple picture in our mind. Imagine a big map. On this map, every sentence becomes a single point. Sentences that mean the same thing land close to each other. Sentences that mean very different things land far apart.

For the sake of understanding, consider this map:

- "What is the capital of France?" lands at one point.
- "Tell me the capital city of France." lands very close to it, because the meaning is almost the same.
- "How do I bake a chocolate cake?" lands very far away, because the meaning is totally different.

So, the embedding is just the address of that point on the map, written as a list of numbers.

Let's visualize this map of meaning as below:

```text
   meaning
      ^
      |
      |   [France capital question]
      |   [France capital city question]   <- close, same meaning
      |
      |
      |
      |                          [bake a chocolate cake]  <- far, different
      |
      +-------------------------------------------------> meaning

```

Here, we can see that the two questions about the capital of France land close to each other, because they mean almost the same thing. The question about baking a cake lands far away, because its meaning is completely different. This closeness on the map is exactly what we measure later.

A real embedding has hundreds of numbers. But for the sake of understanding, let's pretend each embedding has only two numbers. We can write them like below:

```python
# Just for understanding, real embeddings have hundreds of numbers
"What is the capital of France?"      -> [0.91, 0.10]
"Tell me the capital city of France." -> [0.89, 0.12]
"How do I bake a chocolate cake?"     -> [0.05, 0.95]

```

Here, we can notice that the first two lists of numbers are very close to each other. The third one is far away. This matches our understanding, because the first two questions mean the same thing, and the third one means something completely different.

This is how a model converts meaning into numbers. We use a special model called an embedding model to create these numbers for any text we give it.

To learn embeddings, Vector Databases, and RAG in depth, we cover all of these in our AI and Machine Learning Program at Outcome School.

### What is similarity between embeddings?

Now that we have learned about embeddings, it's time to learn how we compare two embeddings.

Similarity is a number that tells us how close two embeddings are in meaning.

In simple words, we take two lists of numbers and we calculate a single score. A high score means the meanings are close. A low score means the meanings are far apart.

The most common score used here is called cosine similarity. We do not need to learn the math today. We just need to remember one thing.

> Higher similarity score means closer meaning.

For the sake of understanding, the score usually goes from 0 to 1.

- A score near 1 means the two sentences mean almost the same thing.
- A score near 0 means the two sentences mean very different things.

So, when a new question comes, we find its embedding, and we compare it with the embeddings of all our saved questions. If any saved question has a high enough similarity score, we treat it as a match.

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

### How does Semantic Caching work step by step?

Before we see the full flow, let me map each piece to a simple real-world role for your better understanding.

| Piece in Semantic Caching | Real-world role |
| --- | --- |
| Embedding model | A translator that turns a sentence into numbers |
| Embedding | The address of a sentence on the map of meaning |
| Similarity score | A judge that tells how close two meanings are |
| Threshold | A rule that decides "close enough or not" |
| Cache | A notebook of past questions and their answers |

Now, let's put everything together and see the full flow.

Step 1: A user sends a question to our app.

Step 2: We convert the question into an embedding using the embedding model. Now the question is a list of numbers.

Step 3: We compare this embedding with the embeddings of all the questions already stored in our cache. We calculate a similarity score for each.

Step 4: We find the saved question with the highest similarity score.

Step 5: Now, the decision. If the highest score is above a chosen limit, we call it a cache hit. We return the saved answer directly, without calling the model. This is fast and free.

Step 6: If no saved question crosses that limit, we call it a cache miss. We send the question to the model, get a fresh answer, and then store the new question, its embedding, and its answer in the cache for the future.

This is how Semantic Caching serves answers by meaning.

We can picture the full flow as below:

```text
        User question
              |
              v
   +----------------------+
   |   Embedding model    |   (turn text into numbers)
   +----------------------+
              |
              v
   +----------------------+
   |  Search the cache    |   (compare with saved embeddings)
   |  for the best score  |
   +----------------------+
              |
              v
       score >= threshold ?
        /              \
      yes               no
       |                 |
       v                 v
  +-----------+   +--------------------+
  | Cache hit |   |    Cache miss      |
  | return    |   | ask the model,     |
  | saved     |   | then store the new |
  | answer    |   | question + answer  |
  +-----------+   +--------------------+

```

Here, we can see that every question first becomes numbers through the embedding model. We then search the cache for the closest saved question and its score. If the score crosses the threshold, we take the left path and return the saved answer, which is a cache hit. If it does not, we take the right path, ask the model for a fresh answer, and store it, which is a cache miss.

In a real system, these saved embeddings live in a vector database that is built to store embeddings and find the closest ones fast using Approximate Nearest Neighbor (ANN) search.

Let's see this flow in simple code as below:

```python
def get_answer(question):
    new_embedding = embed(question)            # Step 2: text to numbers

    best_match, score = search_cache(new_embedding)  # Step 3 and 4

    if score >= 0.85:                          # Step 5: cache hit
        return best_match.answer

    answer = ask_model(question)               # Step 6: cache miss
    store_in_cache(question, new_embedding, answer)
    return answer

```

Here, we can see the whole idea in one place. The `embed` function turns the question into numbers. The `search_cache` function finds the closest saved question and its similarity `score`. If the `score` is high enough, which is `0.85` in our example, we return the saved answer. If not, we ask the model, and then we save the new result so that the next similar question becomes a cache hit.

Here, the number `0.85` is the limit we talked about. It is called the similarity threshold, and we will understand it in detail next.

### A numeric walkthrough

The best way to learn this is by taking an example. Let's walk through it step by step with numbers.

Assume that our cache already has one saved question.

- Saved question: "What is the capital of France?"
- Saved answer: "Paris"

Now, a new user sends a question, and we compare it with our saved question.

Step 1: New question is "Tell me the capital city of France." We compute its embedding and compare it with the saved one. The similarity score comes out to be `0.93`. Our threshold is `0.85`. Since `0.93` is greater than `0.85`, this is a cache hit. We return "Paris" instantly, and we do not call the model.

Step 2: New question is "What is the population of France?" We compute its embedding and compare it. The similarity score comes out to be `0.40`. This is below `0.85`, so this is a cache miss. We send it to the model, get the fresh answer, and store it in the cache.

Step 3: New question is "How do I bake a chocolate cake?" We compute its embedding and compare it. The similarity score comes out to be `0.05`. This is far below `0.85`, so this is again a cache miss. We send it to the model and store the new answer.

Here, we can notice the pattern. Same meaning gives a high score and becomes a cache hit. Different meaning gives a low score and becomes a cache miss. This is exactly what we wanted.

### Setting the similarity threshold

The similarity threshold is the limit we choose to decide whether a new question is close enough to a saved one.

This single number is very important, so let's understand it carefully.

If we set the threshold too high, like `0.99`, then almost nothing matches. Only an exact copy would pass. We lose most of the benefit of Semantic Caching.

If we set the threshold too low, like `0.50`, then very different questions start matching. We may return a wrong answer. For example, "capital of France" could wrongly match "capital of Germany" and return the wrong city.

So, the threshold is a balance. A value around `0.85` to `0.95` works well for many apps, but the right value depends on our use case. We must test it with real questions from our users and adjust it.

> A high threshold means fewer matches but safer answers. A low threshold means more matches but a higher chance of a wrong answer.

To learn embeddings, Vector Databases, and RAG in depth, we cover all of these in our AI and Machine Learning Program at Outcome School.

### Advantages of Semantic Caching

Now, let's quickly look at why Semantic Caching is so useful.

- It saves money, because we call the expensive model far less often.
- It is much faster, because returning a saved answer takes very less time compared to asking the model.
- It reduces load on the model, so our app can handle many more users.
- It matches questions by meaning, so it works even when users phrase the same thing in different ways.

This is how Semantic Caching makes our AI apps cheaper and faster at the same time.

Semantic Caching is one way to cut the cost of LLM calls. Another is prompt caching, which reuses the model's internal work on a repeated prompt prefix. We have a detailed blog on how Prompt Caching works that explains this step by step.

### Things to keep in mind

Semantic Caching is powerful, but we must use it carefully. Let me share a few important points.

First, it is best for questions whose answers do not change quickly. A question like "What is the capital of France?" is perfect, because the answer stays the same. But a question like "What is the weather right now?" is not a good fit, because the correct answer changes every hour.

Second, we must pick a good threshold. As we learned, a wrong threshold can either kill the benefit or return wrong answers.

Third, we may want to clear or refresh the cache from time to time, so that old answers do not stay forever when the real answer has changed.

Now, we have understood how Semantic Caching works. We started with a simple cache, we saw why exact-match caching fails for AI apps, we learned about embeddings and similarity, and finally we put it all together into a clear step-by-step flow with a numeric walkthrough.

### What is the difference between semantic caching and prompt caching?

Semantic caching reuses the saved final answer when a new question means the same as an old one, so the model is not called at all. Prompt caching reuses the model's internal work on a repeated prompt prefix. Both help cut the cost of LLM calls.

### Can semantic caching return a wrong answer?

Yes, if the similarity threshold is set too low. With a low threshold like 0.50, very different questions start matching. For example, a question about the capital of France could wrongly match a question about the capital of Germany and return the wrong city. We must test the threshold with real user questions.

### Is semantic caching a good fit for questions like the current weather?

No. Semantic caching is best for questions whose answers do not change quickly, like the capital of France. A question about the weather right now is not a good fit, because the correct answer changes every hour. We may also refresh the cache from time to time so old answers do not stay forever.

### Where are the embeddings stored in a semantic cache?

In a real system, the saved embeddings live in a vector database. A vector database is built to store embeddings and find the closest ones fast using Approximate Nearest Neighbor search. Each entry keeps the question, its embedding, and its answer.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

[Showing lines 1-495 and 1069-1451 of 1451; 573 middle lines (31.6KB) elided. Read artifact://57 for full output]
