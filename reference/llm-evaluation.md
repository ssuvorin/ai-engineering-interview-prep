> Source: https://outcomeschool.com/blog/llm-evaluation

# What is LLM Evaluation? Metrics, Benchmarks, and Methods Explained
URL: https://outcomeschool.com/blog/llm-evaluation
Published: 2026-05-24
Author: Amit Shekhar

What is LLM Evaluation? Metrics, Benchmarks, and Methods Explained

# What is LLM Evaluation? Metrics, Benchmarks, and Methods Explained

Authors
: - Name
: Amit Shekhar
Published on
: May 24, 2026

LLM Evaluation is the process of measuring how well a Large Language Model performs on the tasks we expect it to do. We check if its outputs are correct, helpful, safe, and useful for our use case.

In this blog, we will learn about LLM Evaluation. We will understand what it is, why we need it, the main types of evaluation, the automatic metrics and benchmarks we can use, human evaluation, LLM as a Judge, task-specific and safety evaluation, the common challenges, and the best practices to follow.

We will cover the following:

- What is LLM Evaluation?
- Why do we need LLM Evaluation?
- Types of LLM Evaluation
- Automatic Metrics
- Benchmarks
- Human Evaluation
- LLM as a Judge
- Task-Specific Evaluation
- Safety and Red-Teaming Evaluation
- Challenges in LLM Evaluation
- Best Practices
- When to use which method

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is LLM Evaluation?

LLM Evaluation is the process of measuring how well a Large Language Model performs on the tasks we expect it to do.

In simple words, we give the model some inputs, look at the outputs, and check if the outputs are correct, helpful, safe, and useful. This is how we decide whether a model is good enough for our use case.

Let's say we have built a chatbot using an LLM. Now, the question is: how do we know if our chatbot is actually good? Is it giving correct answers? Is it polite? Is it safe? Is it better than the older version we had last week? To answer all these questions, we need LLM Evaluation.

## Why do we need LLM Evaluation?

LLMs are very powerful, but they are not perfect. They can make mistakes. They can give wrong information. They can sound very confident even when they are wrong. This is called hallucination, where the model makes up facts that are not true. They can also produce harmful or biased content.

So, before we ship an LLM to our users, we must know how it behaves. And after we ship it, we must keep checking it to make sure it does not get worse over time.

Here are the main reasons we need LLM Evaluation:

- To compare different models and pick the best one for our use case.
- To compare different versions of the same model after fine-tuning or prompt changes.
- To find weak spots where the model fails so that we can fix them.
- To make sure the model is safe and does not produce harmful content.
- To track quality over time, so that we know if the model is getting better or worse.
- To build trust with our users, our team, and our stakeholders.

Without evaluation, we are just guessing. And guessing is not a good idea when real users depend on our product.

## Types of LLM Evaluation

There are four main types of LLM Evaluation. We will learn about each of them in detail.

- Automatic Metrics - We use formulas to score the model output against a reference answer.
- Benchmarks - We test the model on standard datasets that everyone uses.
- Human Evaluation - We ask humans to read the outputs and rate them.
- LLM as a Judge - We use another LLM to score the outputs.

Each of these has its own strengths and weaknesses. In real projects, we usually combine more than one of them.

Beyond these four core methods, there are two cross-cutting areas we will also cover later in this blog: Task-Specific Evaluation and Safety Evaluation. These are not separate methods. They reuse the four above.

Now, let's discuss each one.

## Automatic Metrics

Automatic Metrics are simple formulas that compare the model output with a reference answer and give us a score.

The best way to learn this is by taking an example. Suppose we ask the model to translate a sentence from English to French. We already have the correct French translation written by a human. The model gives its own French translation. Now, we want to know how close the model's translation is to the human translation. This is where automatic metrics come into the picture.

Here are the common ones:

BLEU

BLEU is used mostly for translation tasks. It is a precision-based metric. It asks: what fraction of small word groups (called n-grams) in the model output also appear in the reference answer? A higher BLEU score means the model output is closer to the reference. For example, if the reference is "The cat sat on the mat" and the model says "The cat sat on the mat", BLEU is very high. If the model says "A feline rested on the rug", BLEU is low even though the meaning is the same.

ROUGE

ROUGE is used mostly for summarization tasks. It asks: what fraction of n-grams in the reference summary are covered by the model summary? Just like BLEU, a higher score is better.

BERTScore

BERTScore uses contextual embeddings to compare the meaning of the model output with the reference. So, even if the words are different, if the meaning is close, the score is high. Going back to our earlier example, "A feline rested on the rug" would score high against "The cat sat on the mat" because the meaning is almost the same. This makes BERTScore much better than BLEU for tasks where the wording can vary a lot.

METEOR

METEOR is another metric that improves on BLEU by handling synonyms, stemming, and word order. It sits between pure surface matching and full semantic matching.

Perplexity

Perplexity measures how well the model predicts the next token. A lower perplexity means the model assigns a higher probability to the actual next token in the test data. This metric is mostly used during model training to track if the model is learning.

Exact Match

Exact Match is the simplest one. The score is 1 if the model output is exactly the same as the reference answer, and 0 otherwise. This is useful for tasks like math problems or short factual questions.

Note: In modern LLM evaluation, reference-based metrics like BLEU and ROUGE are mostly used in research papers and translation pipelines. For production LLM applications, we usually rely on LLM as a Judge or task-specific evaluation, which we will learn about soon.

- Fast and cheap to run.
- We can run them at scale on millions of examples.
- The scores are repeatable. Same input gives same score every time.

Disadvantage:

- They only check surface similarity. They do not understand meaning.
- A model can give a perfect answer in different words and still get a low score.
- They do not work well for open-ended tasks like creative writing or chat.

This was all about Automatic Metrics. Now, let's learn about Benchmarks.

## Benchmarks

Benchmarks are standard datasets that the whole research community uses to test LLMs.

When a new LLM is released, the team behind it usually publishes scores on popular benchmarks. This helps us compare it with other models in a fair way.

Different benchmarks test different skills. Let's group them by category, so that we know what each one is for.

General Knowledge

- MMLU - Tests general knowledge across 57 subjects like history, law, math, and medicine, using multiple-choice questions.
- MMLU-Pro - A harder version of MMLU with 10 answer choices and mandatory chain-of-thought reasoning.

Common Sense Reasoning

- HellaSwag - The model has to pick the most likely ending to a short story.

Coding

- HumanEval - Tests coding ability with simple function-writing problems.
- SWE-bench Verified - Real GitHub issues from open-source projects. Tests whether a model can solve real-world software problems.
- LiveCodeBench - A coding benchmark that uses problems released after the model's training cutoff, so it is contamination-resistant.

Math

- GSM8K - Math word problems at the grade-school level.
- MATH - Harder competition-style math problems.
- AIME - Math olympiad problems used for advanced reasoning.

Frontier Reasoning

- GPQA-Diamond - PhD-level science questions used to separate strong reasoning models from average ones.
- Humanity's Last Exam (HLE) - Over 3,000 expert-level questions across many fields, used as a hard frontier challenge.

Instruction Following

- IFEval - Tests instruction-following with verifiable constraints, like "answer in exactly 3 bullet points".

- BFCL (Berkeley Function-Calling Leaderboard) - Tests how well a model can use tools and call functions, very relevant for agents.

- RULER - Tests the effective context window, which is more honest than the nominal context length the model claims.

Truthfulness

- TruthfulQA - Tests if the model gives truthful answers instead of repeating common false beliefs.

Conversation Quality

- Chatbot Arena (LMArena) - Real users chat with two anonymous models side by side and pick the better one. The models are then ranked using an Elo score, just like in chess.

Now that we have seen the categories, we must understand three important ideas that decide how useful a benchmark really is.

- Saturation - Over time, top models start scoring near the ceiling on a benchmark. When every model scores very high, the benchmark stops separating good from great. So, the research community keeps building harder benchmarks to take their place.
- Data contamination - The model may have seen the test questions during training, which makes the scores look higher than they really are. Contamination-resistant benchmarks try to fix this by using problems released after the model's training cutoff.
- Qualification bar - Older or easier benchmarks are not useless. They become a basic check that any serious model must pass before we even look at the harder ones.

- Easy to compare different models, because everyone uses the same dataset.
- Covers a wide range of skills.
- Backed by the research community.

- A high score on a benchmark does not always mean the model works well on our specific use case.
- A benchmark can be saturated, contaminated, or both, which makes the scores misleading.
- Public benchmarks rarely match the exact task we care about in our product.

This is how Benchmarks work. Now, let's move to Human Evaluation.

## Human Evaluation

Human Evaluation is when real people read the model outputs and rate them.

This is still the gold standard. Humans can judge things that formulas cannot, like tone, helpfulness, creativity, and safety.

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

Let's say we ask the model to write a short poem. There is no single correct answer here. A formula cannot tell us if the poem is good. But a human reader can.

Here are the common ways to do human evaluation:

- Likert Scale Rating - The human gives a score from 1 to 5 on quality, helpfulness, or safety.
- Pairwise Comparison - The human sees two outputs and picks the better one. This is used in tools like Chatbot Arena.
- Error Annotation - The human marks the exact mistakes in the output, so we know where the model failed.

- Humans can judge meaning, tone, and quality.
- Works for open-ended tasks where there is no single correct answer.
- Gives us deep insights into where the model fails.

- Very slow and expensive.
- Different humans may give different scores for the same output.
- Hard to scale to thousands or millions of examples.

One more thing to note. These same pairwise comparisons are also used to train models, not just to score them. We have a detailed blog on Decoding InstructGPT that shows how human rankings turn into a reward model.

This was all about Human Evaluation. Now, let's learn about LLM as a Judge.

## LLM as a Judge

LLM as a Judge means we use a strong LLM to score the outputs of another LLM.

Human evaluation is great but very expensive. So, here comes the LLM as a Judge to the rescue. We give a powerful model, like a top-tier LLM, the input prompt and the output, and we ask it to rate the output.

For the sake of understanding, let's see an example. Suppose we want to check if a chatbot's reply is helpful and polite. We can write a prompt like this:

```
You are an expert evaluator. Read the user question and the assistant reply.
Rate the reply on a scale of 1 to 5 for helpfulness and politeness.
Give a short reason for your rating.

User question: {question}
Assistant reply: {reply}

```

The judge LLM reads the prompt and gives us a score and a reason. We can then use this score just like a human score.

- Much cheaper and faster than human evaluation.
- Can scale to millions of examples.
- Works well for open-ended tasks where formulas fail.

- The judge LLM can have its own biases. The well-known ones are:

- Position bias - The judge can favor the first option, or sometimes the second, when comparing two answers side by side.
- Verbosity bias - The judge can favor longer answers, even when a shorter one is better.
- Self-preference bias - The judge can favor outputs from its own model family.
- The judge is not perfect. It can also make mistakes.
- We must validate the judge by comparing its scores with human scores on a small sample.

If you want to learn more about this, I have a separate blog on LLM as a Judge that goes deeper into this topic.

This is how LLM as a Judge works. Now, it's time to learn about Task-Specific Evaluation.

## Task-Specific Evaluation

Task-Specific Evaluation is a layer on top of the four types we just learned. It means we design our own evaluation based on the exact task our LLM is doing.

Under the hood, task-specific evaluation usually uses automatic metrics or LLM as a Judge. But the questions we ask, the inputs we test on, and the things we score are all chosen based on our specific use case.

General benchmarks tell us how a model does on average. But, in our real product, we have a specific task. The evaluation must match that task.

Let's see a few common cases.

RAG (Retrieval Augmented Generation)

In RAG, the model uses a retrieved document to answer a question. So, we need to check two things: did the system retrieve the right document, and did the model use the document correctly to answer the question?

The standard here is the RAGAS four-metric pattern:

- Context Precision - Of the chunks we retrieved, how many are actually relevant?
- Context Recall - Of all the relevant chunks in our corpus, how many did we manage to retrieve?
- Faithfulness (Groundedness) - Is the final answer supported by the retrieved context, or did the model make something up?
- Answer Relevance - Does the answer actually address the user's question?

Context Precision and Context Recall are the classic Precision and Recall metrics applied to retrieval. We have a detailed blog on Precision vs Recall that explains both in depth.

There are popular frameworks that implement these metrics, like RAGAS, DeepEval. We do not need to learn all of them, but we must know that they exist so that we know what to search for when we build a real RAG system.

Agents

In agent systems, the model uses tools and takes many steps. So, we need to check:

- Did the agent pick the right tool?
- Did it pass the correct arguments?
- Did it finish the task?
- How many steps did it take?

Two popular agent benchmarks worth knowing:

- τ-bench (tau-bench) - Evaluates agents in realistic customer-service environments.
- SWE-bench Verified - For coding agents specifically, based on real GitHub issues.

Other names we will see are GAIA for general-assistant tasks, WebArena for browser agents, and BFCL for function-calling accuracy.

Code Generation

For code generation, we run the generated code against test cases. If the tests pass, the code is correct. This is much better than just comparing the code text.

Customer Support Chatbots

For chatbots, we check things like: did the bot answer the question, was the answer polite, did it follow our brand guidelines, and did it escalate to a human when needed.

This way we can use Task-Specific Evaluation to solve any problem in a very simple way.

If we want to go deep into RAG, Vector Databases, Tool use in Agents, and Multi-Agent Systems, check out our AI and Machine Learning Program at Outcome School.

## Safety and Red-Teaming Evaluation

Safety Evaluation is its own category, where we test the model against adversarial and harmful inputs.

So far, we have focused on whether the model gives correct and useful answers. But, there is one more important question: is the model safe?

In safety evaluation, we red-team the model with adversarial prompts. We try jailbreaks, prompt injections, and harmful requests. We check if the model refuses correctly, if it leaks sensitive data, and if it shows bias on sensitive topics. We have a detailed blog on How do LLM guardrails work? that explains how these checks are enforced on the input and the output.

Here are some well-known safety benchmarks:

- HarmBench - Tests model behavior on harmful and adversarial requests.
- AdvBench - A standard set of adversarial prompts used to attack models.
- TrustLLM - A broad evaluation suite covering truthfulness, safety, fairness, robustness, privacy, and ethics.

In production, we also run continuous safety monitoring on real traffic, because new attack patterns appear all the time.

## Challenges in LLM Evaluation

LLM Evaluation is hard. Here are the main challenges:

- Open-ended outputs - There is no single correct answer for many tasks, so formulas do not work well. For example, there are a thousand ways to write a good email reply, and no formula can score all of them correctly.
- Data contamination - The model may have seen the test data during training, which makes the scores misleading.
- Cost - Human evaluation is expensive, and running large evaluation sets through powerful LLMs is also expensive.
- Bias in the judge - When we use LLM as a Judge, the judge can have its own preferences that do not match real users.
- Drift over time - The model behavior can change after fine-tuning, prompt updates, or even just because the provider updated the model on the backend. So, we must keep evaluating in production, not just before launch.
- Edge cases - The model may work well on average, but fail badly on rare but important cases. We must check for these and add them to our evaluation set.

Now, the next big question is: how do we deal with all these challenges? The answer is, we follow some best practices.

## Best Practices

Here are the best practices that I personally believe in for LLM Evaluation:

- Build a custom evaluation set - Do not rely only on public benchmarks. Build a small but high-quality dataset that matches our real use case.
- Combine many methods - Use automatic metrics for speed, LLM as a Judge for scale, and human evaluation for the final check.
- Validate the judge - When using LLM as a Judge, compare its scores with human scores on a small sample to make sure the judge is reliable.
- Track over time - Run evaluations every time we change the prompt, the model, or the system. Save the results so we can see trends.
- Cover edge cases - Add hard examples, adversarial examples, and safety examples to our evaluation set.
- Keep humans in the loop - Even with automated evaluation, review a small sample by hand every week to catch problems that the metrics miss.
- Measure cost and latency too - Quality is not the only thing that matters. We must also track how fast the model responds and how much each call costs. A perfect answer that takes 30 seconds is not useful in a real product.

This way we can use LLM Evaluation to solve the interesting problem of knowing if our LLM is actually good.

## When to use which method

[…957ln elided…]
                                     |
                                     v
Layer 1 (middle):  A --- C --- D --- F        more points, medium steps
                           |
                           v
Layer 0 (bottom):  A-B-C-D-E-F-G-H            all points, fine steps  ->  reach E

```

Here, we can see that we begin with big jumps at the top, then take medium steps in the middle, and finally take fine steps at the bottom to land on the closest point `E`. We never had to check every single point.

Let's walk through it once more in simple words:

- Step 1: Enter at the top layer, where only a few points exist. Move to the point closest to our query. This covers a lot of ground in one big jump.
- Step 2: Drop down to the middle layer. From the point we reached, move to an even closer neighbour.
- Step 3: Drop down to the bottom layer. Take small, careful steps among the closely packed points until we reach the nearest one.

This is how HNSW gives us very fast and very accurate searches. It is the most widely used index in modern vector databases.

### IVF explained simply

IVF stands for Inverted File Index. This is another clever way to speed up the search.

The idea is to group similar vectors into clusters before any search happens. This grouping is done once, in advance.

Let's say we group all our vectors into a few clusters. Each cluster has a center point, which represents the average of that group. We can picture the clusters like below:

```
   Cluster 1          Cluster 2          Cluster 3
  +----------+       +----------+       +----------+
  |  x    x  |       |  x   x   |       |  x  x  x |
  |    C1    |       |    C2    |       |    C3    |
  |  x    x  |       |   x   x  |       |   x   x  |
  +----------+       +----------+       +----------+

  C1, C2, C3 are the center points (the average of each group)
  each x marks one stored vector inside the cluster

```

Here, we can see that the vectors are divided into groups, and each group has one center point that sits in the middle of it.

Now, when a user searches, we do the following.

First, we compare the query vector with only the cluster centers, not the millions of vectors. Then, we pick the few clusters whose centers are closest to the query. After that, we search only inside those few clusters and ignore the rest.

Let's see the search journey like below:

```
Query
  |
  v
Compare with cluster centers only      (cheap, just a few comparisons)
  |
  v
Pick the closest clusters              (say, the 3 nearest clusters)
  |
  v
Search only inside those clusters      (ignore all the other clusters)

```

Here, we can see that IVF first narrows down to a few clusters, then searches only inside them.

Let's put real numbers to see the saving. Suppose we have 100 million vectors split into 100 clusters, so each cluster holds 1 million vectors. If we search only the 3 closest clusters, we check 3 million vectors instead of 100 million. That is a huge saving, and the search becomes much faster than brute force.

Note: There is a small trade-off. If the true closest vector happens to sit in a cluster we skipped, we will miss it. To reduce this risk, we can search a few more clusters, which improves accuracy but takes a little more time. We tune this based on our use case.

### PQ explained simply

PQ stands for Product Quantization. As we just saw, HNSW and IVF help us pick which vectors to check. PQ is different. It does not pick vectors. It shrinks each vector so that it takes much less memory.

Let's understand the memory problem first. Suppose each vector has 128 numbers, and each number takes 4 bytes. That is 512 bytes fo

# How does HyDE work in RAG?
URL: https://outcomeschool.com/blog/how-does-hyde-work
Published: 2026-07-06

How does HyDE work in RAG?

# How does HyDE work in RAG?

Authors
: - Name
: Amit Shekhar
Published on
: July 6, 2026

In this blog, we will learn about how HyDE works in RAG, which is the clever trick of searching with a fake answer. We will also see why searching with the plain question is weak, why a fake answer searches better, how HyDE works step by step with a worked example, and when to use it in the real world.

We will cover the following:

- What is RAG in simple words
- What is the search problem in RAG
- Why searching with the question is weak
- What is HyDE
- Why searching with a fake answer works better
- How HyDE works step by step
- A worked example of HyDE
- A simple code example of HyDE
- Advantages of HyDE
- Disadvantages of HyDE
- When to use HyDE
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is RAG in simple words

Before jumping into HyDE, we must know what RAG is.

RAG stands for Retrieval-Augmented Generation. It is a way to make an AI model answer using our own documents instead of only using what it already knows.

RAG = Retrieval + Augmented + Generation.

Let's break it down:

- Retrieval means searching and fetching the right pieces of text from our documents.
- Augmented means adding the retrieved information to the prompt (context) before sending it to the AI model.
- Generation means the AI model writing an answer using those pieces of text.

Let's say we have a big company handbook with thousands of pages. A new employee asks, "How many holidays do I get in a year?" The AI model has never read our private handbook. So, it cannot answer correctly on its own.

So, here comes RAG to the rescue. First, RAG searches the handbook and finds the few lines that talk about holidays. Then, it gives those lines to the AI model. Finally, the model reads those lines and writes a clear answer.

This is how RAG lets the model answer from our own data. If we want a deeper look at the full RAG flow, we can read the blog on Agentic RAG.

## What is the search problem in RAG

The whole power of RAG depends on one thing. The search step must find the right text.

If the search brings the wrong pages, the model gets wrong information. And then the answer will also be wrong.

So, the search step is the heart of RAG. Now, let's understand how this search actually happens.

The search in RAG does not work by matching exact words. It works by matching meaning.

To match meaning, we convert text into numbers. These numbers are called an embedding.

An embedding is a list of numbers that represents the meaning of a piece of text.

In simple words, an embedding is the meaning of text written in the language of numbers.

The important rule is simple. Two texts with similar meaning get similar numbers. Two texts with different meaning get different numbers.

We also cut our big documents into small pieces. Each small piece is called a chunk, which means a short block of text, like a single paragraph.

So, in RAG, we do the following. First, we convert every chunk of our document into an embedding and store it. Then, when a user asks a question, we convert the question into an embedding too. After that, we compare the question embedding with all the stored embeddings. Finally, we pick the chunks whose embeddings are closest to the question embedding.

This is how RAG finds the right text by comparing meaning.

The store that holds all these embeddings and finds the closest ones is called a vector database. We have a detailed blog on how a vector database works that explains this in depth.

## Why searching with the question is weak

Now, here is the catch.

A question and an answer often do not look alike. They live in different worlds.

Let's say the user asks, "Why is my laptop battery draining so fast?"

The real answer inside our documents may say something like this:

> Background applications, high screen brightness, and old battery health reduce battery life. Closing unused apps and lowering brightness improves battery duration.

Notice the problem. The question is short and uses words like "draining" and "fast". The answer is detailed and uses words like "background applications", "brightness", and "battery health".

A question and its answer are written in two different styles. So, their embeddings are not always close to each other.

Means, when we search using only the question, the meaning gap is large. The search may miss the perfect answer that is actually sitting in our documents.

This is the weakness of searching with the question. We are comparing a question to answers, but questions and answers are shaped differently.

## What is HyDE

So, here comes HyDE into the picture.

HyDE stands for Hypothetical Document Embeddings. It is a technique where we first ask the AI model to write a fake answer to the question, and then we search using that fake answer instead of the question.

In simple words, HyDE = Hypothetical + Document + Embeddings.

Let's break it down:

- Hypothetical means imaginary or made-up. It is a guess answer.
- Document means a piece of text that looks like a real answer.
- Embeddings means the meaning of that text written as numbers.

The core idea is one beautiful trick. An answer looks like an answer. So, if we want to find a real answer, we must search using something that looks like an answer.

The question does not look like an answer. But a fake answer does look like an answer.

So, we tell the AI model, "Pretend you know the answer and write it." This made-up answer is called the hypothetical document.

We do not show this fake answer to the user. We do not even trust that it is correct. We only use it as a better search key, which means the text we search with.

This is the heart of HyDE. We search with a fake answer to find the real answer.

## Why searching with a fake answer works better

Now, the question is, why does a fake answer help when it may even contain wrong facts?

The answer is about shape, not facts.

When the model writes a fake answer about battery draining, it naturally uses words like "background apps", "screen brightness", and "battery health". These are the same kinds of words that the real answer in our documents uses.

So, the fake answer and the real answer now look alike. Their embeddings become close. And close embeddings mean a strong search match.

Let's picture this meaning space as below:

```text
        Meaning space (similar meaning sits closer)

   [ Question ]                                  ----- far -----+
   "battery draining fast"                                      |
                                                                v
                                          +--------------------------+
   [ Fake answer ]  ----- close ------->  | [ Real answer chunk ]    |
   "background apps, brightness,          | "background apps, high   |
    battery health"                       |  brightness, battery     |
                                          |  health reduce life"     |
                                          +--------------------------+

```

Here, we can see that the question sits far from the real answer chunk, because it is shaped differently. The fake answer sits close to the real answer chunk, because both use the same answer-like words. So, searching with the fake answer lands much nearer to the real answer.

> We are not searching with the question. We are searching with something that is shaped like the answer.

Even if the fake answer gets a fact wrong, it still points the search in the right direction. The wrong facts get thrown away later, because we only use the real documents to write the final answer.

This is how a fake answer becomes a powerful search key.

To learn how embeddings, Vector Databases, and RAG fit together, check out our AI and Machine Learning Program at Outcome School.

## How HyDE works step by step

The best way to learn this is by taking an example. Let's walk through HyDE step by step.

Step 1: The user asks a question. For example, "Why is my laptop battery draining so fast?"

Step 2: We send this question to the AI model with a simple instruction. We say, "Write a short answer to this question, even if you are not sure." The model writes a fake answer, which is our hypothetical document.

Step 3: We convert this fake answer into an embedding, which means we turn it into a list of numbers that holds its meaning.

Step 4: We compare this embedding with all the stored embeddings of our real document chunks. We pick the chunks that are closest in meaning.

Step 5: We take these real chunks and send them to the AI model along with the original question.

Step 6: The model reads the real chunks and writes the final answer. This final answer is based on our real documents, not on the fake one.

So, the fake answer is used only in the middle, only to improve the search. The final answer comes from real data.

We can picture the full flow as below:

```text
   [ User question ]
          |
          v
   +-------------------+
   | AI model writes   |   <- "even if not sure"
   | a fake answer     |
   +-------------------+
          |
          v
   +-------------------+
   | Turn fake answer  |
   | into embedding    |
   +-------------------+
          |
          v
   +-------------------+        +----------------------+
   | Search the stored | -----> | Pick closest real    |
   | document chunks   |        | document chunks      |
   +-------------------+        +----------------------+
                                          |
              [ User question ] --------> |
                                          v
                               +----------------------+
                               | AI model writes the  |
                               | final answer from    |
                               | real chunks only     |
                               +----------------------+
                                          |
                                          v
                                  [ Final answer ]

```

Here, we can see that the fake answer is used only in the middle to improve the search. The real chunks and the original question flow into the last step, and the final answer is written from the real documents only.

This is how HyDE works from start to finish.

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

## A worked example of HyDE

Let me tabulate the difference between the normal RAG search and the HyDE search for your better understanding.

| Stage | Normal RAG | HyDE |
| --- | --- | --- |
| What we search with | The user's question | A fake answer written by the model |
| Shape of the search text | Short and question-like | Detailed and answer-like |
| Closeness to real answers | Often far in meaning | Often close in meaning |
| Final answer source | Real documents | Real documents |

Here, we can see the key difference. Normal RAG searches with a question. HyDE searches with a fake answer. Both write the final answer from real documents, but HyDE usually finds better chunks to start with.

Now, let's see the meaning gap with simple numbers, just for the sake of understanding.

Suppose closeness is measured from 0 to 1, where 1 means identical meaning and 0 means completely different meaning.

- Question embedding compared to the real answer chunk: closeness is 0.55.
- Fake answer embedding compared to the real answer chunk: closeness is 0.88.

Here, we can notice that the fake answer is much closer to the real answer. So, the search picks the correct chunk more easily with HyDE.

Note: These numbers are just for the sake of understanding. The real values depend on the model and the data.

## A simple code example of HyDE

Now, let's see the code for HyDE in a simple form. We will write it in `python` as below:

```python
def hyde_search(question, model, vector_store):
    # Step 1: ask the model to write a fake answer
    prompt = "Write a short answer to this question: " + question
    fake_answer = model.generate(prompt)

    # Step 2: turn the fake answer into an embedding
    fake_answer_embedding = model.embed(fake_answer)

    # Step 3: search using the fake answer's embedding
    top_chunks = vector_store.search(fake_answer_embedding, top_k=5)

    return top_chunks

```

Here, we have done three simple things:

- First, we ask the model to write a `fake_answer` to the question.
- Then, we convert that `fake_answer` into a `fake_answer_embedding`, which is its meaning as numbers.
- After that, we call `vector_store.search` with that embedding to get the top five closest chunks.

Notice that we never search with the original `question`. We search with the `fake_answer`. That is the whole trick of HyDE.

Now, let's see how we use these chunks to write the final answer as below:

```python
def answer_with_hyde(question, model, vector_store):
    chunks = hyde_search(question, model, vector_store)

    # combine the real chunks into one block of context
    context = "\n".join(chunks)

    # ask the model to answer using only the real chunks
    final_prompt = (
        "Use the context below to answer the question.\n"
        "Context: " + context + "\n"
        "Question: " + question
    )
    return model.generate(final_prompt)

```

Here, we can see the full flow. First, we get the real `chunks` using `hyde_search`. Then, we join them into one `context`, which means one block of helpful text. After that, we send the real `context` and the original `question` to the model. Finally, the model writes the answer using only the real documents.

So, the fake answer helped us find the chunks, but it never touched the final answer. The problem is solved.

If we want to go deep into RAG and build an AI Tutor from scratch, we cover it in our AI and Machine Learning Program at Outcome School.

## Advantages of HyDE

Now, let's understand why HyDE is useful.

- It closes the gap between questions and answers, because we search with answer-shaped text.
- It often finds better chunks, which leads to better final answers.
- It works well even when the user's question is short or vague.
- It needs no extra training of the model. We only change how we search.

## Disadvantages of HyDE

But again, no technique is perfect. HyDE has some costs too.

- It is slower, because we make an extra call to the model to write the fake answer.
- It costs more, because that extra call uses extra computing power.
- The fake answer can drift off topic, and then the search may go in the wrong direction.
- For very simple questions, the question itself may already be enough, so HyDE adds cost without much gain.

So, HyDE makes our search smarter, but we pay with a little extra time and cost.

## When to use HyDE

Now, the question is, when must we use HyDE.

We should use HyDE when our questions and answers look very different from each other. This happens a lot with short questions, support tickets, and search over technical documents.

But, for very short and direct lookups, plain RAG search may be enough. So, we must choose HyDE based on our use case.

A good practice is to test both. We can run plain RAG search and HyDE search on the same set of questions, and then we keep the one that finds better chunks for our data.

## Summary

Let's quickly recap what we have learned.

RAG searches our documents by matching meaning using embeddings. But a question and its answer are shaped differently, so searching with the question alone is weak.

So, here comes HyDE. We ask the model to write a fake answer first. We search with that fake answer, because it is shaped like a real answer and lands close to the real chunks. Then, we write the final answer using only the real documents.

This way we can use HyDE to solve the search problem in RAG in a very simple way. We search with a fake answer to find the real one.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-371 and 1329-1765 of 1765; 957 middle lines (44.8KB) elided. Read artifact://50 for full output]
