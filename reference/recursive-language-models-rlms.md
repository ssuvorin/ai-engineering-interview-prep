> Source: https://outcomeschool.com/blog/recursive-language-models

# What are Recursive Language Models (RLMs) and How Do They Work?
URL: https://outcomeschool.com/blog/recursive-language-models
Published: 2026-05-19

What are Recursive Language Models (RLMs) and How Do They Work?

# What are Recursive Language Models (RLMs) and How Do They Work?

Authors
: - Name
: Amit Shekhar
Published on
: May 19, 2026

In this blog, we will learn about Recursive Language Models (RLMs), a new way of using language models to handle very large inputs that do not fit in the model's context window.

We will cover the following:

- What is a Recursive Language Model (RLM)?
- Why do we need RLMs?
- How an RLM works
- How the model writes and runs code
- Why RLMs work better
- Recursion inside RLMs
- How RLMs differ from simple chunking
- Advantages of RLMs
- Limitations of RLMs
- When to use RLMs
- RLM vs RAG
- A real use case

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a Recursive Language Model (RLM)?

A Recursive Language Model (RLM) is a way of using a language model where the model can call another language model (or itself) on smaller parts of the input to solve a bigger problem.

In simple words, instead of putting the entire input into the model at once, the model breaks the input into smaller pieces and calls another language model (or itself) on those smaller pieces.

RLM = Recursive + Language Model

Here, Recursive means the model can call itself (or another model) again and again on smaller parts of the problem. Language Model is the LLM that understands and generates text.

## Why do we need RLMs?

The best way to learn this is by taking an example.

Let's say we have a very long document with 1 million tokens, and we want to ask a question about it.

When we put a lot of text into a language model, the following issues arise:

- The model has a context window limit. It cannot accept too many tokens at once.
- The quality of the answer goes down as the context gets longer. The model gets confused with too much information and misses important details in the middle. This is called context rot.
- The cost of running the model goes up.
- The speed of the model goes down.

This means, just making the context window bigger does not solve the problem. We need a better approach.

We have a detailed blog on The Lost in the Middle Problem in LLMs that covers this problem end to end.

So, here comes the Recursive Language Model to the rescue.

## How an RLM works

In an RLM, the main model does not directly read the full input. Instead, the full input stays inside a Python environment as a variable. The model gets a small prompt that only names this variable and explains how to use it. The model then writes code to read parts of the input and call other language models on those parts. The smaller calls return short answers, which the main model combines into the final answer.

The next section walks through this with a concrete example.

Now, the question is: why is this called recursive? The answer is, the model can call another model, which can again call another model, and so on. Each call works on a smaller piece. This is just like recursion in programming.

## How the model writes and runs code

Let's understand this with a real example. Suppose we have a long meeting transcript and we want to ask: "What were the action items?"

The model only generates text. It cannot run code by itself. So, we wrap the model with a Python environment. This environment has a variable `context` that stores the full transcript, and a function `call_llm(prompt)` that calls another language model.

Now, we send a short prompt to the main model:

```
Question: What were the action items?
Write Python code to answer this. The Python environment has:
- A variable named `context` that stores the full transcript.
- A function `call_llm(prompt)` that calls another language model.

```

Very important: The full transcript is never sent to the main model. Only the variable name `context` is sent in the prompt, not its actual content. The transcript stays inside the Python environment. The model can read parts of it through code, but the model never reads the whole thing. This is what keeps the main model's context small even when the input is huge.

Now, the loop runs as below:

Step 1: The model writes Python code as its response:

```python
turns = context.split("\n")
results = [call_llm(f"Find action items in: {turn}") for turn in turns]
print(results)

```

Here, the model decides to split `context` by turn and call `call_llm` on each one.

Step 2: The code runs in the Python environment. Each `call_llm` call sends one turn to another language model and gets back a short answer. All answers are collected into a list.

Step 3: The list is sent back to the model. The model now sees only the short answers, not the full transcript.

Step 4: The model reads the list and returns the final list of action items as the answer. If the answer was not clear yet, the model would write more code and the loop would continue.

This back-and-forth between the model and the Python environment is called an agentic loop.

So, the model is only generating text. The text just happens to be Python code. The Python environment runs the code. And `call_llm` is just an API call to another language model.

## Why RLMs work better

Here, we can notice that each smaller call gets a small input. In our transcript example, each `call_llm` call works on just one turn, not the full meeting. A small input is easy for the model to handle. The model can focus on the small piece and give a good answer.

Also, the main model only sees the small answers, not the full input. So, the main model has a clean and small context.

This way, we avoid context rot. The problem is solved.

## Recursion inside RLMs

Now, let's understand the recursive part more clearly.

Let's say one piece is still too long for the smaller call. The smaller call can also act as an RLM. It can again split its piece into even smaller parts and call another language model on each part.

So, the structure looks like below:

- The main RLM works on the full input.
- The main RLM calls sub-RLMs on each big piece.
- Each sub-RLM can again call sub-RLMs on each smaller piece.
- The smallest calls work on tiny pieces of text.

This is just like a tree. The top of the tree handles the big problem. The leaves of the tree handle the small pieces. Each level passes its answer up to the next level.

Note: The depth of recursion depends on the size of the input and the type of question. The model itself decides how deep to go.

That's the beauty of Recursive Language Models.

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

## How RLMs differ from simple chunking

Now, the next big question is: how is this different from just splitting the input into chunks and processing each chunk?

In simple chunking, we fix the chunk size beforehand. We send each chunk to the model, get an answer, and combine the answers. The split is fixed, and we always do the same steps.

In an RLM, the model itself decides how to split the input. The model also decides what to ask for each piece. The model can change its strategy based on the question.

So, how can we say RLM is smarter? The answer is, the RLM is more like a human reader. A human reader does not chunk a book into fixed pages. A human reader skims, jumps, reads carefully, and decides on the fly. An RLM works in a similar way.

This makes RLMs more flexible than simple chunking.

## Advantages of RLMs

- Handles very long inputs. RLMs can work with inputs much larger than the model's context window.
- Better accuracy on long context. Since each call works on a small piece, the model can focus and give better answers.
- Lower cost in some cases. We do not need to send the full input every time. We only send small pieces when needed.
- Modular thinking. The model can break a big problem into small problems, just like a human would.
- Flexible. The model decides how to split the input based on the question.

## Limitations of RLMs

- More complex to build. We need to set up a code environment and tool calls.
- Many model calls. One question can lead to many small calls. This can be slow.
- Errors can stack up. If a smaller call gives a wrong answer, the final answer can also become wrong.
- Hard to debug. Since the model writes its own code, it can be hard to know what went wrong.

So, RLMs are powerful, but we must use them carefully.

## When to use RLMs

I will highly recommend using RLMs for the following cases:

- We have a very long document and need to ask questions about it.
- We need to analyze a large codebase.
- We need to summarize a long meeting or transcript.
- We need to compare many files at once.
- The task can be broken into smaller, independent sub-tasks.

For short inputs, we do not need RLMs. A simple language model call is enough. We must choose the approach based on our use case.

## RLM vs RAG

Now that we have learned about RLMs, it's time to compare RLMs with another popular approach called RAG (Retrieval-Augmented Generation).

In RAG, we first search for the most relevant parts of a document and then send only those parts to the language model.

In RLM, the model itself decides how to explore the input. The model can write code, split the input, and call smaller models.

Let me tabulate the differences between RAG and RLM for your better understanding so that you can decide which one to use based on your use case.

| Feature | RAG | RLM |
| --- | --- | --- |
| How it picks data | A search step picks relevant parts first | The model itself explores the data |
| Flexibility | Less flexible, depends on the search step | More flexible, model decides what to do |
| Code execution | No code execution by the model | The model can write and run code |
| Best for | Question answering on a fixed knowledge base | Complex tasks on long inputs |
| Complexity | Easier to build | Harder to build |

For simple question answering, RAG is enough. For complex analysis on long inputs, RLM is a better fit.

To master RAG, Context Engineering, and Orchestration and Routing, check out our AI and Machine Learning Program at Outcome School.

## A real use case

A real use case in software development:

Let's say we want to find all the security issues in a large codebase. The codebase has hundreds of files. The total size is much bigger than what a normal model can read in one go.

With an RLM, we can do the following:

- Store the codebase as a variable.
- Ask the RLM: "Find all security issues."
- The RLM writes code to loop through each file.
- For each file, the RLM calls a smaller language model to find security issues in that file.
- The smaller calls return short lists of issues.
- The RLM combines all the issues into a final report.

Here, we can see that the main RLM does not read the full codebase. The main RLM only sees small summaries from each file. This keeps the main context clean and small.

This way we can use RLMs to solve the interesting problem of large codebase analysis.

## Summary

We have learned the following:

- A Recursive Language Model (RLM) is a way of using a language model that can recursively call other language models on smaller parts of the input.
- RLMs solve the problem of long context and context rot.
- The main model writes code to split the input and call smaller models.
- RLMs are powerful for long documents, codebases, and complex tasks.
- We must use RLMs carefully because they have more complexity and more model calls.

Now, we have understood Recursive Language Models (RLMs).

This way we can use RLMs to solve any problem on long inputs in a very simple way.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
