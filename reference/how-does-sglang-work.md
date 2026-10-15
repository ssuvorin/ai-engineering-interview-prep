> Source: https://outcomeschool.com/blog/how-does-sglang-work

# How does SGLang work?
URL: https://outcomeschool.com/blog/how-does-sglang-work
Published: 2026-06-30
Author: Amit Shekhar

How does SGLang work?

# How does SGLang work?

Authors
: - Name
: Amit Shekhar
Published on
: June 30, 2026

SGLang is a high-performance serving framework for large language models. It serves a model's answers to many users at the same time, as fast as possible, using clever ideas like RadixAttention to reuse past work.

In this blog, we will learn about how SGLang works. We will also see what problem it solves, how it makes serving large language models faster, and the clever ideas that make it special.

We will cover the following:

- What is SGLang?
- A quick recap of how an LLM generates text
- The problem SGLang solves
- RadixAttention: the heart of SGLang
- How RadixAttention reuses past work
- The frontend language of SGLang
- How the runtime and the frontend work together
- Continuous batching in SGLang
- Structured output and faster decoding
- A simple end-to-end picture
- More powerful features of SGLang
- How SGLang compares to vLLM

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is SGLang?

SGLang is a high-performance serving framework for large language models and multimodal models.

In simple words, it is a tool that takes a large language model and serves its answers to many users at the same time, as fast as possible.

The name SGLang comes from two parts.

SGLang = `SG` (Structured Generation) + `Lang` (Language).

So, the name itself tells us two things. It helps us generate structured output in a controlled way, and it gives us a small language to write our instructions.

Do not worry, we will learn about each of these parts in detail.

For now, just remember this. `SGLang` has two main pieces that deliver these two things. One piece is a runtime, which is the engine that actually runs the model fast and takes care of the structured output. The other piece is a frontend language, which is the small language we just mentioned, the friendly way for us to tell the model what to do.

Now, before we understand why `SGLang` is fast, we must first understand how an `LLM` generates text. Once we know that, the magic of `SGLang` will be very clear.

### A quick recap of how an LLM generates text

An `LLM` writes text one word at a time. To be precise, it writes one token at a time.

A token is a small piece of text. It can be a whole word, a part of a word, or even a single character. For the sake of understanding, we can think of a token as roughly one word.

So, the model reads our input, then it produces one token. Then it reads our input plus that new token, and it produces the next token. It keeps doing this until the answer is complete.

Let's say we ask the model, "The sky is".

First, the model reads "The sky is" and produces "blue".

Then it reads "The sky is blue" and produces "today".

Here, we can notice something important. To produce each new token, the model looks back at everything that came before.

Now, looking back at all the previous tokens again and again would be very slow. So, the model stores some helpful numbers from the previous tokens and reuses them. These stored numbers are called the KV cache.

The KV cache is the model's memory of the tokens it has already processed. It stands for the key and value cache. We do not need the deep math here. We just need this simple idea.

> The KV cache is the model's saved work for the tokens it has already seen, so it does not have to redo that work for every new token.

This KV cache is very important. It is the key to understanding why `SGLang` is so fast. Keep this idea in mind.

### The problem SGLang solves

Now, let's understand the real problem.

In the real world, an `LLM` does not answer just one person. It answers thousands of people at the same time. And the same model is asked many similar things again and again.

Let's say we build a chatbot. Every single conversation begins with the same instruction, which is called a system prompt.

A system prompt is a fixed set of instructions we give the model before the user speaks. For example, "You are a helpful assistant.".

So, every user's request starts with this same instruction. The model has to process this same text again and again, for every user. This is wasted work.

Here is another example. Suppose we are building an agent that answers questions about a document. The document is the same for every question. But the model reads the whole document from scratch for each question.

This is like reading an entire book from page one, every single time someone asks you a small question about it. It is slow, and it wastes effort.

So, the problem is clear. The model repeats the same expensive work many times. We need a way to do that shared work only once and reuse it.

So, here comes `SGLang` to the rescue.

`SGLang` was built around one central idea. If two requests share the same starting text, they can share the saved work for that text. This saved work, as we learned, is the KV cache.

The technique that makes this sharing possible is called RadixAttention. This is the heart of `SGLang`.

### RadixAttention: the heart of SGLang

Let's break down this name first.

RadixAttention = `Radix` (a way to organize text by shared prefixes) + `Attention` (the core operation an LLM uses to look back at previous tokens).

To understand `Radix`, we must first understand a prefix.

A prefix is the starting part that two pieces of text have in common.

For example, look at "The sky is blue" and "The sky is clear". They share the prefix "The sky is". After that, one says "blue" and the other says "clear".

Now, `SGLang` keeps a smart structure called a radix tree to store the KV cache of many requests.

A radix tree is a tree-like structure that groups text by its shared prefix. We can think of it as a family tree of sentences. Sentences that begin the same way share the same branch. They only split apart at the point where they become different.

Let's make this very concrete with a small example.

Suppose three users send these three requests:

- "You are a helpful assistant. What is the capital of France?"
- "You are a helpful assistant. What is the capital of Japan?"
- "You are a helpful assistant. Tell me a joke."

Here, we can see that all three share the same start, which is "You are a helpful assistant.".

Without `SGLang`, the model would process "You are a helpful assistant." three separate times.

With `SGLang`, the radix tree stores that shared part once. Its KV cache is computed only one time. Then each request continues from there. And wherever some requests still share even more text, that shared text becomes another branch that is also stored only once.

Let's see the radix tree as below:

```
              "You are a helpful assistant."
              (shared prefix, KV cache stored once)
                            |
              +-------------+--------------+
              |                            |
              v                            v
     "What is the capital of"       "Tell me a joke."
      (shared by two requests,        (unique tail)
       KV cache stored once)
              |
          +---+---+
          |       |
          v       v
      "France?"  "Japan?"
      (unique)   (unique)

```

Here, we can see that the common start, "You are a helpful assistant.", sits at the top as one shared branch. Its saved work is computed only once. Below it, the two requests that ask about a capital share even more text, which is "What is the capital of". So that part becomes another shared branch, and its saved work is also stored only once. Only at the very bottom do "France?" and "Japan?" split into their own unique parts. The "Tell me a joke." request shares only the top branch and then goes its own way. None of the shared branches are ever recomputed.

This is how RadixAttention saves a huge amount of work. The shared prefix is processed once, and that saved work is reused by other requests that share it, for as long as it stays in memory.

The problem is solved.

### How RadixAttention reuses past work

Now, let's understand the steps `SGLang` follows. This will make everything clear.

Step 1: A new request arrives. For example, "You are a helpful assistant. What is the capital of Italy?".

Step 2: `SGLang` looks at its radix tree. It checks how much of the start of this request already exists in the tree.

Step 3: It finds that "You are a helpful assistant. What is the capital of" is already there, because the earlier requests about France and Japan added it. So, it reuses the saved KV cache for that whole part. It does not recompute it.

Step 4: Only the new part, which is "Italy?", is processed fresh. The new saved work is then added as a new branch in the tree.

Step 5: The model generates the answer one token at a time, just like we learned earlier.

So, the more text different requests share, the more work `SGLang` saves. This sharing is automatic. We do not have to do anything special to enable it.

There is one more thing to understand. The memory that stores the KV cache is limited. It cannot hold everything forever.

So, `SGLang` must decide what to keep and what to throw away when the memory gets full. It uses a simple and smart rule. It removes the least recently used branches first. This means the branches that nobody has used for the longest time get removed first.

This is a clever choice. The popular shared prefixes, like the system prompt, stay in memory because they are used all the time. The rare one-off parts get removed when space is needed.

This is how `SGLang` keeps the most useful saved work and reuses it as much as possible.

We have a detailed blog on how prompt caching works that explains this in depth.

### The frontend language of SGLang

Till now, we have learned about the engine. Now, it is time to learn about the friendly part, which is the frontend language.

The frontend language is a simple way for us to write our instructions to the model, right inside our `Python` code.

Why do we need this? Because real tasks are rarely a single question. A real task is often many steps.

Let's say we want the model to do this:

- Read a paragraph.
- Summarize it.
- Then translate the summary into French.

These are three steps that depend on each other. Writing all of this by hand, and keeping it fast at the same time, is hard.

So, the frontend language lets us describe these steps clearly. We can write a sequence of model calls, mix in our own text, and capture the model's output into variables.

Let's see a small example as below:

```python
import sglang as sgl

@sgl.function
def summarize_and_translate(s, paragraph):
    s += "Summarize this paragraph:\n" + paragraph + "\n"
    s += "Summary: " + sgl.gen("summary", max_tokens=64)
    s += "Now translate the summary to French.\n"
    s += "French: " + sgl.gen("french", max_tokens=64)

```

Here, we have defined a function that does two model calls in order.

- The variable `s` holds the growing conversation. We keep adding text to it.
- `sgl.gen("summary", ...)` asks the model to generate the summary and saves it under the name `summary`.
- After that, we ask the model to translate, and we save the result under the name `french`.

So, we describe the whole flow in plain steps, and `SGLang` runs it efficiently behind the scenes.

This is the beauty of the frontend language. We write our intent simply, and the runtime takes care of speed and sharing.

### How the runtime and the frontend work together

Now, let's connect the two pieces we have learned.

The frontend language is how we describe the task. The runtime is the engine that runs it fast using RadixAttention.

Here is the nice part. The frontend understands the structure of our program. It knows which parts are fixed and shared, and which parts are new.

So, when many requests run the same program, they naturally share the same prefixes. The runtime sees this and reuses the KV cache through the radix tree.

In simple words, the frontend and the runtime are designed to help each other. The frontend exposes the shared structure, and the runtime exploits it for speed.

This teamwork is the core reason `SGLang` is both easy to use and fast.

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

### Continuous batching in SGLang

Now, let's learn another idea that helps `SGLang` stay fast. This idea is not unique to `SGLang`. Many modern serving systems use it too. It is called continuous batching.

First, what is a batch? A batch is a group of requests that the model processes together at the same time. Processing many requests together is much more efficient than processing them one by one.

But there is a catch with simple batching. Different requests finish at different times. One user may want a short answer, and another may want a long one.

In old-style batching, we would wait for the whole group to finish before starting a new group. This means fast requests are stuck waiting for slow ones. That wastes time.

So, here comes continuous batching to the rescue.

Continuous batching means that as soon as one request in the group finishes, a new waiting request takes its place right away. We do not wait for the whole group to finish.

Let's say we have a batch of four requests. Request two finishes early. Instead of leaving an empty slot, `SGLang` immediately fills that slot with the next waiting request.

Let's see the difference as below:

```
Old-style batching (slot sits empty, time wasted):

  Slot 1: [ R1 running ............ ]
  Slot 2: [ R2 done ] [ empty, waiting for whole group ]
  Slot 3: [ R3 running ............ ]
  Slot 4: [ R4 running ............ ]

Continuous batching (empty slot filled right away):

  Slot 1: [ R1 running ............ ]
  Slot 2: [ R2 done ] [ R5 starts immediately ........ ]
  Slot 3: [ R3 running ............ ]
  Slot 4: [ R4 running ............ ]

```

Here, we can see that in old-style batching, the slot of the finished request stays empty until the whole group is done. In continuous batching, a new waiting request, R5, jumps into that slot right away. No slot sits idle.

So, the model is always kept busy. No slot sits empty. This keeps the hardware working at full power and serves more users in the same amount of time.

This is how continuous batching squeezes the most out of the machine.

One important point to remember. Continuous batching is a common technique, so it is not the part that makes `SGLang` special. The special part is that `SGLang` brings continuous batching and RadixAttention together. RadixAttention reuses the shared work through the radix tree, and continuous batching keeps the machine busy. This combination is what makes `SGLang` shine when many requests share a long common start.

To learn how serving engines stay fast - KV Cache, Continuous Batching, Prompt Caching, and Paged Attention - check out our AI and Machine Learning Program at Outcome School.

### Structured output and faster decoding

Let's remember the name again. `SGLang` has the word "Structured Generation" in it. Now, we will finally understand that part.

Many times, we do not want free text from the model. We want the answer in a fixed format.

For example, we may want a `JSON` answer like below:

```json
{
  "name": "Italy",
  "capital": "Rome"
}

```

A JSON is a simple, common format used to store data as a set of names and values. Many programs read and write data in this format.

The problem is, a normal model may produce slightly broken `JSON`. It may forget a bracket or add extra words. Then our program cannot read it.

So, `SGLang` lets us force the output to follow a fixed shape. We give it a rule for the format, and `SGLang` makes sure every generated token follows that rule.

This is called constrained decoding.

Constrained decoding means the model is only allowed to pick tokens that keep the output valid for our chosen format. If a token would break the format, it is simply not allowed.

So, the output is always valid. We never get broken `JSON`. The problem is solved.

There is a bonus here. Because the format already fixes some parts of the output, `SGLang` can sometimes fill those fixed parts very quickly instead of asking the model for them one token at a time. This makes structured output faster too.

This is how `SGLang` gives us reliable, well-shaped answers, and gives them quickly.

### A simple end-to-end picture

Now, let's put the whole story together in one simple flow.

Step 1: We write our task using the `SGLang` frontend language. We describe the steps and the format we want.

Step 2: Our request goes to the `SGLang` runtime, which is the engine.

Step 3: The runtime looks at the radix tree and checks for any shared prefix, like the system prompt. If it is already there, it reuses the saved KV cache through RadixAttention.

Step 4: Only the new part of our request is processed fresh, and its saved work is added to the tree.

Step 5: Our request joins a batch. Thanks to continuous batching, the engine stays fully busy and serves many users together.

Step 6: The model generates the answer one token at a time. If we asked for a fixed format, constrained decoding keeps every token valid.

Step 7: We get our answer, fast and correctly shaped.

Here is the whole flow as below:

```
   We write the task (frontend language)
                 |
                 v
        SGLang runtime (engine)
                 |
                 v
     Check the radix tree for a shared prefix
                 |
        +--------+--------+
        |                 |
   found prefix       new part
        |                 |
        v                 v
  reuse saved KV    process fresh and
  cache (Radix      add to the tree
  Attention)             |
        +--------+--------+
                 |
                 v
   Join a batch (continuous batching keeps
            the engine busy)
                 |
                 v
   Generate one token at a time
   (constrained decoding keeps the format valid)
                 |
                 v
       Fast, well-shaped answer

```

Here, we can see the request flowing from our frontend code, into the runtime, through the radix tree where shared work is reused, into a batch that keeps the engine busy, and finally out as a valid answer.

This is how `SGLang` works from start to finish.

We have a detailed blog on LLM inference optimization that covers the broader landscape of these techniques.

### More powerful features of SGLang

We have now seen the full core flow of `SGLang`. But `SGLang` is a large and modern tool, and it does much more than the core. Let's look at its other powerful features in simple words. Many of these are also found in other modern serving tools, so they are not unique to `SGLang`.

Before we list them, we need one small idea. When a model answers, there are two stages. First, it reads the whole prompt in one go. This stage is called the prefill. Then, it writes the answer one token at a time. This stage is called the decode. Many of the features below make these two stages faster.

Chunked prefill. Some prompts are very long, like a big document. Reading such a long prompt in one go can block everyone else. So, `SGLang` can break a long prompt into smaller chunks and read them bit by bit, mixed in with the answer writing. This keeps the work smooth for all users.

[…776ln elided…]

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

[Showing lines 1-407 and 1184-1618 of 1618; 776 middle lines (47.9KB) elided. Read artifact://58 for full output]
