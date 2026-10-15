> Source: https://outcomeschool.com/blog/how-does-tensorrt-llm-work

# How does TensorRT-LLM work?
URL: https://outcomeschool.com/blog/how-does-tensorrt-llm-work
Published: 2026-09-04
Author: Amit Shekhar

How does TensorRT-LLM work?

# How does TensorRT-LLM work?

Authors
: - Name
: Amit Shekhar
Published on
: September 4, 2026

TensorRT-LLM is an open-source library from NVIDIA that makes large language models run as fast as possible on NVIDIA GPUs. We give it a finished model, and it gives us back a highly tuned, ready-to-run version for our GPU.

In this blog, we will learn about how TensorRT-LLM works, NVIDIA's own engine that squeezes the highest possible speed out of an NVIDIA GPU when it runs a large language model. We will also see what inference means, what a GPU kernel is, why a normal model run wastes a lot of the GPU's time, how TensorRT-LLM prepares the model ahead of time instead of figuring things out on the fly, how kernel fusion, quantization, the paged KV cache, in-flight batching, CUDA graphs, and speculative decoding each add speed, how one model is spread across many GPUs, and where it works well and where it fails.

We will cover the following:

- What is inference?
- What is a GPU and what is a kernel?
- The problem: the GPU spends its time on the wrong things
- What is TensorRT-LLM?
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

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is inference?

Let's start from the very beginning.

A large language model, or LLM, is the AI model behind tools like ChatGPT. We give it some text, and it gives us back some text.

An LLM has two very different parts of its life.

The first part is training. This is when the model learns. It reads a huge amount of text and slowly adjusts billions of internal numbers until it becomes good at predicting words. Training happens once, it takes a long time, and it is very expensive.

The second part is inference. This is when the model works. Training is finished, the numbers are frozen, and now we simply ask the model a question and it gives us an answer.

Inference means using an already-trained model to produce an answer.

In simple words, training is the student studying for years, and inference is the student answering our question today.

Now, here is why inference matters so much in the real world. Training happens once. Inference happens every single time any user types anything. Millions of times a day. So, even a small saving in inference time gets multiplied by millions.

This is the exact thing TensorRT-LLM is built for. It does not help us train a model. It makes inference as fast as it can possibly be.

### What is a GPU and what is a kernel?

Before we can understand what makes inference slow, we need two more simple ideas.

A GPU is a special chip that is extremely good at doing a huge amount of simple math at the same time. An LLM is basically a mountain of multiplications and additions, so a GPU is the perfect chip for it.

Let's understand the GPU with a comparison. A normal processor, called a CPU, is like one very clever person who solves problems one after another, very quickly. A GPU is like ten thousand ordinary people who all work at the same moment. If the job is one hard puzzle, the clever person wins. If the job is ten thousand small sums, the crowd wins by a mile. An LLM is ten thousand small sums, so the GPU wins.

Now, the second idea. The GPU does not do anything on its own. The CPU has to tell it what to do. It does that by sending small programs to the GPU.

A kernel is a small program that runs on the GPU and does one specific piece of math.

For example, there is a kernel that multiplies two big grids of numbers. There is another kernel that adds two lists of numbers. There is another kernel that applies a simple formula to every number in a list.

So, running an LLM means the CPU launches thousands of these kernels one after another, and the GPU runs each one. Launching a kernel is called a kernel launch.

We can picture it as below:

```
HOW A MODEL RUNS ON A GPU

   CPU (the manager)                    GPU (the ten thousand workers)
   ------------------                   -----------------------------
   "run kernel 1"        ------->       kernel 1 runs, result saved
   "run kernel 2"        ------->       kernel 2 runs, result saved
   "run kernel 3"        ------->       kernel 3 runs, result saved
        ...                                   ...
   (thousands of launches for a single token)

```

Here, we can see that the CPU is the manager sending instructions, and the GPU is the crowd of workers doing the actual math. For every single token the model writes, this whole conversation between the manager and the workers happens thousands of times.

Keep this picture in your mind. Almost everything TensorRT-LLM does is about making this picture cleaner and faster.

### The problem: the GPU spends its time on the wrong things

Now, let's see the real problem.

When we run a model in the normal way, using a standard deep learning framework, the framework figures out what to do while it is running. It reads the model layer by layer, and for each layer it picks a ready-made kernel and launches it.

This is very flexible and very convenient. We can change the model, print things in the middle, and experiment freely. That freedom is wonderful when we are building a model.

But that same freedom is expensive when we are only running a finished model millions of times. Let's see exactly where the time leaks away.

The first leak is too many small kernels. Each layer of the model is broken into many tiny steps, and each tiny step is its own kernel. A big multiplication is one kernel. Adding a small correction is another kernel. Applying a formula to every number is another kernel. Each of these kernels is small and finishes fast, but there are thousands of them.

The second leak is memory traffic. This one is the biggest, so let's understand it properly. The GPU has a large memory where all the numbers live, and a much smaller, much faster memory right next to the workers. Every kernel has to pull its numbers from the large memory, do its math, and push the answer back to the large memory. Pulling and pushing is slow. The math itself is fast.

So, when we run ten small kernels in a row, the same numbers get pulled out and pushed back ten times. The workers finish their sums almost instantly and then sit idle, waiting for the next delivery of numbers. The GPU looks busy, but it is mostly waiting.

The third leak is launch overhead. Every kernel launch costs a little bit of time on the CPU side. One launch is nothing. Thousands of launches for every single token, for every user, adds up into a real delay. Sometimes the CPU cannot even prepare the launches fast enough, and the powerful GPU sits idle waiting for its manager to speak.

The fourth leak is generic kernels. A ready-made kernel is written to work for every model, every size, and every GPU. Being general means it cannot be perfect for our exact model on our exact GPU. There is always a faster version possible.

Let's see the leak in a simple picture as below:

```
NORMAL RUN: many small kernels, numbers travel back and forth

big GPU memory:  [ numbers ]
                    |  ^        |  ^        |  ^
                    v  |        v  |        v  |
                 kernel 1     kernel 2    kernel 3
                 (multiply)   (add)       (apply formula)

   pull, compute, push  ->  pull, compute, push  ->  pull, compute, push

   the math is fast, the travelling is slow, the workers keep waiting

```

Here, we can notice that the numbers make the slow trip to and from the big memory three separate times, once for each kernel, even though the three kernels are doing one connected piece of work.

So, the problem is clear. The GPU has enormous power, and a normal run wastes a large part of it on travelling, launching, and general-purpose kernels instead of on math.

So, here comes TensorRT-LLM to the rescue.

### What is TensorRT-LLM?

Now that we understand the problem, let's understand the solution.

TensorRT-LLM is an open-source library from NVIDIA that makes large language models run as fast as possible on NVIDIA GPUs.

In simple words, we hand it a finished model, and it hands us back a highly tuned, ready-to-run version of that model that squeezes the most speed out of our specific GPU.

Let's break the name down.

TensorRT-LLM = Tensor + RT + LLM.

- Tensor is simply the name for a grid of numbers. A single number, a list of numbers, a table of numbers, and bigger versions of these are all tensors. Everything inside a model is tensors.
- RT stands for Runtime, which means the part that actually runs the model.
- LLM tells us this library is built specially for large language models.

TensorRT-LLM is built on top of an older NVIDIA tool called TensorRT, which does the same kind of speed work for all sorts of AI models. TensorRT-LLM adds everything that is special about large language models on top of it, like the KV cache, batching many users together, and splitting a giant model across several GPUs.

TensorRT-LLM does its thinking ahead of time, so that at answer time the GPU does nothing but math.

That single sentence is the heart of this blog.

To reach that speed, TensorRT-LLM uses a set of tricks that all work together:

- Kernel fusion, which merges many small pieces of math into one, so the numbers travel less.
- Quantization, which stores the model's numbers in a smaller form, so they take less space and move faster.
- Custom attention kernels, which are custom-written programs for the heaviest part of the model.
- The paged KV cache, which hands out memory in small blocks so nothing is reserved and wasted.
- In-flight batching, which keeps every slot on the GPU filled with live work at all times.
- CUDA graphs, which replay a whole recorded sequence of steps with a single instruction.
- Speculative decoding, which produces several tokens in the time normally taken by one.
- Multi-GPU execution, which splits a model too big for one GPU across many of them.

Most of these ideas are not NVIDIA-only. We have a detailed blog on LLM Inference Optimization that covers this whole family of techniques end to end.

Do not worry, we will learn about each of them in detail. Let's start with the idea that ties them all together.

### The big idea: prepare the model ahead of time

Let's understand the core idea with a simple comparison.

Suppose we open a restaurant. There are two ways to cook.

The first way is cooking to order from scratch. A customer orders, and only then do we open the recipe book, walk to the store, buy the vegetables, chop them, and start the stove. Every single order repeats all of this. It is very flexible, because we can cook literally anything a customer asks for. But every customer waits a long time.

The second way is preparing everything in advance. Before the restaurant opens, we decide the menu, chop all the vegetables, pre-mix the sauces, and arrange every tool exactly where the cook's hand will reach for it. Now when the order arrives, the cook only has to do the actual cooking. The food comes out very fast. The price we pay is that the menu is fixed. We prepared for these dishes, and cooking something completely different means preparing all over again.

A normal deep learning framework is the first restaurant. TensorRT-LLM is the second restaurant.

Ahead of time, TensorRT-LLM studies the whole model, decides the fastest possible way to run every part of it on our exact GPU, and saves that plan. At answer time, it simply follows the saved plan.

This preparation step is called the build, and what it produces is called an engine.

An engine is a single prepared file that holds the model's numbers along with the exact plan for running them fast on one specific kind of GPU. It is not a recipe book any more. It is a fully prepped kitchen.

Now, why does preparing ahead of time help so much? Because during the build, TensorRT-LLM has all the time in the world. It can try many different kernels for the same operation, actually time each one on the real GPU, and keep the winner. It can look at ten small operations sitting next to each other and decide to merge them into one. None of this is possible while a user is waiting for an answer.

So, we can now state the trade very simply. We spend a few minutes once, in exchange for speed on every request forever after.

### The build step: from a model to an engine

Now, let's walk through the build step by step, so that it feels real.

Step 1: We start with the trained model. This is the finished model as it comes from wherever we got it, with all its learned numbers, called weights. Weights are simply the numbers the model learned during training.

Step 2: We describe the model to TensorRT-LLM. TensorRT-LLM already has ready-made definitions for the popular model families, so most of the time we do not write anything. It reads the model and builds an internal map of every operation and how they connect.

Step 3: TensorRT-LLM optimizes that map. This is where the real work happens. It merges operations together, removes work that is not needed, and rearranges things into a faster shape. We will learn about these tricks in the next sections.

Step 4: It picks the best kernel for every operation. For each piece of math, it tries several kernel versions on our actual GPU, measures how long each one really takes, and keeps the fastest. This is called kernel auto-tuning. Notice that the answer can be different on different GPUs, which is exactly why the engine is tied to one GPU type.

Step 5: It writes out the engine file. The prepared plan and the weights are saved together into one file that we can load and run.

We can picture the whole build as below:

```
THE BUILD STEP

  trained model  --->  TensorRT-LLM build  --->  engine file
  (weights)            - merge operations         (weights + the exact
                       - remove extra work         plan to run them fast)
                       - try many kernels
                       - time them on the
                         real GPU, keep
                         the fastest

  happens ONCE, takes minutes        used for EVERY request after that

```

Here, we can see that all the thinking is pushed into the one-time build on the left, so that the right side, which happens millions of times, is left with pure math and nothing else.

Note: Because the plan was tuned for one specific GPU, one precision, and one set of size limits, an engine is not freely portable. If we move to a different GPU or want to allow much longer prompts, we build a new engine. This rigidity is the honest price of the speed, and we will come back to it at the end of the blog.

Now, let's learn the individual tricks that happen inside the build and inside the runtime.

### Kernel fusion

This is the most important trick, so let's understand it well.

Kernel fusion means combining several small kernels into one bigger kernel, so that the numbers are pulled from memory once instead of many times.

Remember the problem we saw earlier. The slow part is not the math. The slow part is the numbers travelling between the big GPU memory and the workers.

Let's take a concrete little example. Suppose the model needs to do three things in a row on the same numbers.

- Multiply the numbers by a big grid of weights.
- Add a small correction value to the result.
- Apply a simple formula to every number, the kind that turns negative values into zero.

Without fusion, these are three kernels. The numbers come out of the big memory, get multiplied, and go back. They come out again, get the addition, and go back. They come out a third time, get the formula, and go back. Three round trips.

With fusion, TensorRT-LLM writes one single kernel that does all three things while the numbers are still in the fast memory next to the workers. The numbers come out once, all three things happen, and they go back once. One round trip instead of three.

Let's see the difference as below:

```
WITHOUT FUSION (3 round trips)

 big memory -> multiply -> big memory -> add -> big memory -> formula -> big memory

WITH FUSION (1 round trip)

 big memory -> [ multiply + add + formula, all in fast memory ] -> big memory

```

Here, we can see that the actual math is exactly the same in both cases, and the answer is exactly the same too. The only thing that changed is how many slow trips the numbers had to make. We cut it from three to one.

Fusion also removes two kernel launches, so the CPU has less to do as well.

Now, multiply this saving by every layer of the model, and by every token of every answer, for every user. This is why fusion alone gives a large speed-up.

TensorRT-LLM fuses aggressively, and this is much easier for it than for a normal framework, because during the build it can see the whole model at once and it knows nothing is going to change later.

This is how kernel fusion turns many slow trips into one. Now, let's move to the next trick.

### Quantization

Now, let's learn the second big trick.

To understand it, we need to know how a model stores its numbers.

Every weight inside a model is a number with a decimal point, like `0.372`. The computer stores such a number using a fixed amount of space, measured in bits. A bit is the smallest unit of computer memory.

Models are usually trained using 16 bits or 32 bits for every single number. More bits means the number is stored more precisely.

Quantization means storing the model's numbers using fewer bits.

In simple words, we shrink every number into a smaller, rougher form.

Let's understand it with a comparison. Suppose we are writing down a price. We could write `19.9999999` or we could write `20`. The short version takes far less space to write, far less time to read, and for most purposes it is just as useful. Quantization is exactly this, applied to every number in the model.

So, we may take a model stored in 16 bits per number and store it in 8 bits per number, or even 4 bits per number. TensorRT-LLM supports several of these smaller forms, and NVIDIA's newer GPUs have special hardware that runs the small forms extremely fast.

Now, why does this help so much? There are three reasons, and all three matter.

The first reason is less memory used. A model in 8 bits takes about half the space of the same model in 16 bits. So, a model that did not fit on our GPU may now fit, and the space we saved becomes room for serving more users at once.

The second reason is less travelling. We already know that moving numbers is the slow part. If every number is half the size, then moving them takes about half the time. This is a direct speed-up on the exact thing that was the bottleneck.

The third reason is faster math. Modern NVIDIA GPUs have dedicated hardware for doing math on these smaller numbers, and it runs several times faster than the same math on bigger numbers.

But, here is the catch. Rounding numbers loses a little information. If we are careless, the model's answers get worse.

So, quantization is done carefully. Some sensitive parts of the model are kept at higher precision while the rest is shrunk. The rounding is calibrated by running a small amount of sample text through the model and observing the real range of the numbers, so that the rounding is tuned to what actually happens rather than guessed. TensorRT-LLM ships several well-tested quantization methods that do this properly.

[…432ln elided…]

### Does Ollama need an internet connection?

Only for downloading models. Once a model is pulled from the Ollama model library, it runs fully on our own computer, so we can keep using it offline. Our prompts and replies never leave our machine.

### Can Ollama run without a GPU?

Yes. If there is no usable GPU, Ollama runs the whole model on the CPU. It works, but replies come out more slowly. When a GPU is present, Ollama puts as many model layers on it as fit and runs the rest on the CPU.

### Can apps built for the OpenAI API use Ollama?

Yes. Ollama offers an address that follows the same request format as OpenAI's API, at `http://localhost:11434/v1`. So many apps and libraries that were built for OpenAI can use a local Ollama model just by changing the address they send requests to.

### Why is the first reply from Ollama slower than the next ones?

The first request has to load the model from disk into memory, which can take a few seconds. After that, Ollama keeps the model loaded for 5 minutes by default, so the next questions skip the loading step and the reply starts instantly. We can change this time with the `keep_alive` setting.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# What is LLM Routing? How to Send Each Query to the Right LLM
URL: https://outcomeschool.com/blog/llm-routing
Published: 2026-05-09
Author: Amit Shekhar

What is LLM Routing? How to Send Each Query to the Right LLM

# What is LLM Routing? How to Send Each Query to the Right LLM

Authors
: - Name
: Amit Shekhar
Published on
: May 9, 2026

LLM Routing is the practice of choosing the right LLM for each user query, based on cost, latency, and quality, instead of sending every query to the same LLM.

In this blog, we will learn about LLM Routing, why it matters, and how to send each user query to the right LLM based on cost, latency, and quality.

We will cover the following:

- The Big Picture
- What is LLM Routing?
- Why we need LLM Routing
- Anatomy of an LLM Router
- Routing Strategies
- A Full Trace Example
- LLM Routing vs Mixture of Experts
- When LLM Routing is Worth It
- Common Mistakes and How to Fix Them
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

LLM Routing is the layer that sits in front of many LLMs. It looks at each user query and decides which LLM should answer it. The goal is simple - send the easy queries to small, cheap, fast LLMs, and send the hard queries to big, smart, expensive LLMs. This way, we save cost without losing quality.

In simple words:

LLM Routing = Pick the right LLM for each query.

## What is LLM Routing?

LLM Routing is the practice of choosing the right LLM for each user query, instead of sending every query to the same LLM.

Let's decompose the term:

LLM Routing = LLM + Routing.

- LLM stands for Large Language Model, the model that generates the answer. We have a detailed blog on Transformer Architecture that explains the architecture behind every modern LLM, including how Multi-Head Attention works inside it.
- Routing means deciding which path a request should take.

Means, LLM Routing decides the path of a query - which LLM will handle it.

Let's say we walk into a hospital with a problem. A receptionist looks at our problem, then sends us to the right doctor. A common cold goes to a general physician. A heart problem goes to a cardiologist. A brain problem goes to a neurologist.

The receptionist is the router. The doctors are the LLMs. The patient is our user query.

This is the same idea behind LLM Routing.

## Why we need LLM Routing

Today we have many LLMs available - frontier LLMs (the biggest, smartest LLMs at the top of the market, like the latest from OpenAI, Anthropic, and Google), mid-size LLMs, small LLMs, and even task-specific LLMs for code, math, or vision. They differ on three things:

- Cost. Frontier LLMs are expensive. Small LLMs are very cheap.
- Latency. Bigger LLMs are slower. Smaller LLMs are faster.
- Quality. Some queries need the smartest LLM. Many do not.

Let's put this into perspective with real numbers:

- Frontier LLM: around `$15` per 1M output tokens.
- Small LLM: around `$0.50` per 1M output tokens.

That is a `30x` cost gap.

Now, here is the catch. Most user queries are simple - "What is 2 + 2?", "Summarize this email", "What is the capital of France?". Sending every such query to a frontier LLM is a waste of cost and time.

So, here comes LLM Routing to the rescue. It sends each query to the LLM that fits best, based on our use case.

## Anatomy of an LLM Router

Let's see the high-level picture as below:

```
                  ┌────────────────┐
   user query  →  │                │
                  │   LLM Router   │
                  │                │
                  └───────┬────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  Small   │ │   Mid    │ │ Frontier │
        │   LLM    │ │   LLM    │ │   LLM    │
        └──────────┘ └──────────┘ └──────────┘

```

Here, we can see four parts. Let's decode each one.

1. The Query. The raw input from the user. This is the only thing the router sees.

2. The Router. A small, fast component that decides which LLM should handle this query. The router can be a set of rules, a small classifier, an embedding lookup, or even a small LLM itself.

3. The LLM Pool. A set of LLMs with different strengths, costs, and speeds. We can have a small LLM, a mid-size LLM, a frontier LLM, and a code-specialist LLM all in the pool.

4. The Selected LLM. The one LLM the router has picked for this query. The query is then forwarded to it, and the response is returned to the user.

This is how an LLM Router is structured.

Note: The router itself must be very fast. A good rule of thumb is to keep the router's own latency under 10 percent of the chosen LLM's latency. If the chosen LLM takes 1 second, the router should add at most 100 ms.

## Routing Strategies

Now, let's understand the most common ways to build the router. We will go through five strategies.

### 1. Rule-based Routing

The simplest strategy. Look at keywords, length, or patterns in the query and pick an LLM.

Example code:

```python
def route(query: str) -> str:
    q = query.lower()
    if "code" in q or "function" in q or "bug" in q:
        return "code-llm"
    if len(q) < 50:
        return "small-llm"
    if len(q) < 200:
        return "mid-llm"
    return "frontier-llm"

```

Here, we have a small function that picks an LLM based on simple rules. A query about code goes to the code LLM. A very short query goes to the small LLM. A medium-length query goes to the mid LLM. Everything longer goes to the frontier LLM.

Advantage: Very fast and very cheap. No model call needed for routing.

Disadvantage: Brittle. A query like "Why is my Python script broken?" may slip past the keyword check, since none of `code`, `function`, or `bug` appear in it. New patterns break the rules.

### 2. Classifier-based Routing

Here, we train a small classifier on past data of `(query, best-LLM)` pairs. At runtime, the classifier takes the query and predicts the right LLM.

The classifier can be a simple logistic regression on top of query embeddings, a small neural network, or a System One Model like Jev that returns the chosen LLM along with a calibrated probability.

Advantage: Learns from real data. Picks up patterns that simple rules miss.

Disadvantage: Needs labeled training data and a retraining loop.

Sakana's Fugu is a real model built on this idea - a lightweight selection head reads the query and scores each model to pick the best one. We have a detailed blog on Sakana Fugu that covers how it learns which model is best.

### 3. Embedding-based Routing

Here, we convert each query into an embedding - a vector of numbers that captures its meaning. We also keep a small set of reference embeddings, one per LLM, that represent the kind of queries each LLM is best at. Because the same queries get embedded again and again here, we have a detailed blog on how an Embedding Cache works that explains how caching them removes the repeated cost.

For each new query, we find the closest reference embedding. The LLM that owns that reference handles the query.

Advantage: No training. Easy to add a new LLM - just add one more reference.

Disadvantage: Quality depends on how good the reference embeddings are.

### 4. LLM-as-Router

Here, we use a small, cheap LLM as the router. The router LLM is a separate LLM whose only job is to read the query and pick which target LLM should answer it. The idea is simple: the router speaks the same language as the query, so it can understand intent and difficulty far better than fixed rules.

Example code:

```python
def route_with_llm(query: str) -> str:
    prompt = f"""Pick the best LLM for this query.
Options: small-llm, mid-llm, frontier-llm, code-llm.
Query: {query}
Answer with one word from the options:"""
    return router_llm(prompt).strip()

```

Here, `router_llm` is the small, cheap LLM acting as the router. It reads the query and outputs the name of the target LLM to use - one of `small-llm`, `mid-llm`, `frontier-llm`, or `code-llm`. The router itself is separate from these target LLMs.

Advantage: Very flexible. No training needed. We can change the routing rules just by changing the prompt.

Disadvantage: Adds one extra LLM call before the main one. We must keep this router LLM small and fast.

### 5. Cascade Routing

This is the most cost-saving strategy. Send the query to the cheapest LLM first. If the answer looks low-confidence or wrong, escalate to a bigger LLM.

```
query  →  small LLM  →  confident? ── yes ──▶ return answer
                          │
                          no
                          ▼
                       mid LLM  →  confident? ── yes ──▶ return answer
                                     │
                                     no
                                     ▼
                                  frontier LLM ───────▶ return answer

```

Here, we can see a chain. Each LLM either answers the query, or hands it up to a bigger one.

The "confident?" check can be a self-rating from the LLM, a verifier model, or a simple heuristic like answer length and presence of "I do not know".

A small example in code:

```python
def cascade(query: str) -> str:
    answer = small_llm(query)
    if is_confident(answer):
        return answer
    answer = mid_llm(query)
    if is_confident(answer):
        return answer
    return frontier_llm(query)

```

Here, we have used a simple cascade. Each step either returns the answer or escalates to the next LLM.

Advantage: Great cost savings. Most queries get solved by the cheapest LLM.

Disadvantage: Slow for hard queries, since they pay for two or three LLM calls.

### Comparing the Strategies

Let me tabulate the differences between the routing strategies for your better understanding so that you can decide which one to use based on your use case.

| Strategy | Speed | Cost | Flexibility | Needs Training |
| --- | --- | --- | --- | --- |
| Rule-based | Very Fast | Very Low | Low | No |
| Classifier-based | Fast | Low | Medium | Yes |
| Embedding-based | Fast | Low | Medium | No |
| LLM-as-Router | Medium | Medium | High | No |
| Cascade | Slow on hard queries | Lowest on average | High | No |

There is no clear winner here. We pick the strategy based on our use case. For a small system with a few clear query types, rule-based is enough. For a large product with mixed queries, cascade or LLM-as-router works better.

## A Full Trace Example

Let's say we run a chatbot with four LLMs behind a router - `small-llm`, `mid-llm`, `frontier-llm`, and `code-llm`.

We will use a simple rule-based router for the sake of understanding.

Query 1: "What is 2 + 2?"

- Router decision: `small-llm` (length is small, no code keyword).
- Cost: very low. Latency: about 100 ms.
- Response: "4".

Query 2: "Summarize this 3-line email for me: Hi John, can you please review my Q3 sales report draft by Friday? Thanks, Sarah."

- Router decision: `mid-llm` (length is medium, no code keyword).
- Cost: low. Latency: about 500 ms.
- Response: a clean one-line summary.

Query 3: "Fix the bug in this Python function that calculates Fibonacci."

- Router decision: `code-llm` (the words "bug" and "function" both match code keywords).
- Cost: low. Latency: about 700 ms.
- Response: a corrected Python function.

Query 4: "Design a comprehensive multi-agent system for medical diagnosis that covers symptom analysis, differential diagnoses, treatment recommendations, edge cases like rare diseases, ethical considerations, and the trade-offs between accuracy and latency."

- Router decision: `frontier-llm` (length is large, no code keyword).
- Cost: high. Latency: about 3 s.
- Response: a detailed multi-step design.

Let's put all four together as below:

```
"What is 2 + 2?"           ──▶ router ──▶ small-llm     ──▶ fast & cheap
"Summarize this email..."  ──▶ router ──▶ mid-llm       ──▶ balanced
"Fix the bug in..."        ──▶ router ──▶ code-llm      ──▶ specialist
"Design a multi-agent..."  ──▶ router ──▶ frontier-llm  ──▶ smart & slow

```

Here, we can see that each query went to the right LLM based on its nature. Simple math went to the small one. Summary went to the mid one. Code went to the code one. Hard reasoning went to the frontier one. The receptionist did the right job.

Now, let's think about cost. Without routing, all four queries would have gone to the frontier LLM. With routing, only one of them did. That is a big cost saving across millions of queries.

It works perfectly.

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

## LLM Routing vs Mixture of Experts

A natural question arises - is LLM Routing the same as Mixture of Experts?

The answer is: no, but the idea is similar.

- LLM Routing picks one full LLM out of many full LLMs, at the query level.
- Mixture of Experts picks a few small expert sub-networks inside one LLM, at the token level.

Let me tabulate the differences between LLM Routing and Mixture of Experts for your better understanding.

| Aspect | LLM Routing | Mixture of Experts |
| --- | --- | --- |
| Where it lives | Outside the LLMs, in the application layer | Inside one LLM, in the model layer |
| What it routes | A full user query | A single token at a time |
| What it picks | One full LLM | A few expert sub-networks |
| Who controls it | The application developer | The model architecture |

Both use a router. Both pick a subset of compute. But LLM Routing works at the system level, and Mixture of Experts works inside a single model. We have a detailed blog on Mixture of Experts that explains the inside-the-model routing.

## When LLM Routing is Worth It

LLM Routing has real engineering cost. So, we must add it only when it pays off. Here are the signals that say it is worth it:

- High query volume. A few thousand queries per day rarely justify routing. Millions per day almost always do.
- Mixed query difficulty. If most queries are simple but some are hard, routing wins big. If every query is the same level, one LLM is enough.
- Cost pressure. If our LLM bill is high, routing brings it down fast.
- Multiple LLMs already in use. If we are already using two or more LLMs for different reasons, a router cleans up that ad-hoc logic.

If none of these apply, a single mid-size LLM may be a better choice for our use case.

## Common Mistakes and How to Fix Them

Let's go through the common mistakes and how to fix them.

1. The router itself is too heavy.

If we use a frontier LLM as the router, the router cost can be higher than the saving. Use a tiny LLM, a classifier, or simple rules for the router.

2. No fallback path.

The chosen LLM may fail, time out, or return a bad answer. Always keep a fallback LLM. If the small LLM fails, fall back to the mid LLM, and so on.

3. The router adds too much latency.

A router that adds 500 ms before the real call kills the user experience. Keep the router fast - rules in microseconds, classifiers in a few milliseconds, small LLMs under 200 ms.

4. Mixing routing with orchestration.

Routing picks one LLM for one query. Orchestration coordinates many LLMs across many steps. Do not confuse the two. Build the router as one focused component.

5. No observability.

We must log which LLM handled which query, the cost, the latency, and the quality. Without these logs, we cannot tune the router or catch bad routing decisions.

6. Routing on the wrong signal.

Routing only on query length is not enough. A short query like "Prove the Riemann hypothesis" is hard. A long query like "Please summarize this email for me, thanks" is easy. Use intent and difficulty signals, not just length.

## Quick Summary

Let's recap what we have decoded:

- LLM Routing is the practice of picking the right LLM for each user query.
- Why it matters: cost, latency, and quality. Frontier LLMs can be `30x` more costly than small ones.
- Anatomy: Query → Router → LLM Pool → Selected LLM → Response.
- Routing Strategies: rule-based, classifier-based, embedding-based, LLM-as-router, and cascade.
- Cascade Routing saves the most cost by escalating only when the cheap LLM is not confident.
- LLM Routing vs Mixture of Experts: routing picks a full LLM at the query level, while MoE picks expert sub-networks inside one LLM at the token level.
- When it is worth it: high query volume, mixed query difficulty, real cost pressure, or already using multiple LLMs.
- Common Mistakes: heavy router, no fallback, slow router, mixing routing with orchestration, no logs, and routing on the wrong signal.

Now, we have understood LLM Routing.

### Is LLM Routing the same as AI orchestration?

No. Routing picks one LLM for one query. Orchestration coordinates many LLMs across many steps. We should not confuse the two, and we should build the router as one focused component.

### How fast should an LLM router be?

The router must be very fast. A good rule of thumb is to keep the router's own latency under 10 percent of the chosen LLM's latency. If the chosen LLM takes 1 second, the router should add at most 100 ms. Rules run in microseconds, classifiers in a few milliseconds, and small LLMs should stay under 200 ms.

### Can we use a frontier LLM as the router?

It is a bad idea. If we use a frontier LLM as the router, the router cost can be higher than the saving. We should use a tiny LLM, a classifier, or simple rules for the router instead.

### Is query length a good signal for routing?

Not on its own. A short query like "Prove the Riemann hypothesis" is hard, while a long query like "Please summarize this email for me, thanks" is easy. We should use intent and difficulty signals, not just length.

### Which routing strategy saves the most cost?

Cascade Routing saves the most cost. It sends the query to the cheapest LLM first and escalates to a bigger LLM only when the answer looks low-confidence. The trade-off is that hard queries become slow, since they pay for two or three LLM calls.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-312 and 745-1179 of 1179; 432 middle lines (23.3KB) elided. Read artifact://88 for full output]
