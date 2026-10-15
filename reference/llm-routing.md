> Source: https://outcomeschool.com/blog/llm-routing

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
