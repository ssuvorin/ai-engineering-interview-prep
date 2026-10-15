> Source: https://outcomeschool.com/blog/decoding-eagle

# What is EAGLE? Feature-Level Speculative Decoding Explained
URL: https://outcomeschool.com/blog/decoding-eagle
Published: 2026-09-01
Author: Amit Shekhar

What is EAGLE? Feature-Level Speculative Decoding Explained

# What is EAGLE? Feature-Level Speculative Decoding Explained

Authors
: - Name
: Amit Shekhar
Published on
: September 1, 2026

EAGLE is a speculative decoding method that makes a language model generate text faster without changing its output at all. It guesses the future tokens at the level of the model's internal features, not at the level of words.

In this blog, we will learn about EAGLE, a state-of-the-art way to speed up language model generation by drafting tokens at the feature level instead of the token level.

We will cover the following:

- What is EAGLE?
- A quick recap of speculative decoding
- The problem with token-level drafting
- The big idea: draft at the feature level
- Resolving the uncertainty by feeding back the token
- The math behind the speedup with small numbers
- EAGLE-2 and dynamic draft trees
- How EAGLE lives on today
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

EAGLE was introduced in 2024 in the research papers "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty" and its follow-up "EAGLE-2", by Yuhui Li and collaborators at Peking University, Microsoft Research, and the University of Waterloo.

EAGLE is among the fastest lossless ways to speed up text generation, and it is built into many serving systems. It improves on earlier methods with one key insight about where to do the drafting. So, let's decode it piece by piece.

## What is EAGLE?

EAGLE is a speculative decoding method, a way to make a language model generate text faster without changing its output at all.

It works by having a small, cheap draft step guess several future tokens, which the big model then checks all at once. EAGLE's twist is that it does the guessing at the level of the model's internal features, not at the level of words. This makes the guesses much more accurate, which leads to a bigger speedup.

## A quick recap of speculative decoding

We covered speculative decoding and Medusa before. The short version: generating text one token at a time is slow because each token needs a full pass through the big model. That slow, one-token-at-a-time stage is the decode phase of inference. We have a detailed blog on Prefill vs Decode that explains why it is the bottleneck.

Speculative decoding fixes this by cheaply guessing several tokens ahead, then letting the big model verify them all in a single pass. If the guesses are right, we get several tokens for the cost of one verification. The better the guesses, the more tokens are accepted, and the bigger the speedup.

So the whole game is making accurate guesses cheaply. EAGLE found a better place to make them.

## The problem with token-level drafting

Earlier methods, like Medusa, guess the next tokens directly. But predicting the exact next token is hard and uncertain.

Why? Because of sampling. Even the big model does not output one token, it outputs a probability distribution, and the actual token is sampled from it with some randomness. Predicting which token will be sampled is inherently noisy. So token-level guesses are often wrong, and wrong guesses get rejected, which limits the speedup.

We wanted a more predictable thing to guess. EAGLE found one.

## The big idea: draft at the feature level

EAGLE's insight is to guess the next feature instead of the next token.

A feature here means the model's internal hidden state, the rich vector it computes in its second-to-last layer, just before it turns that vector into a token. EAGLE observed that this feature sequence is much more regular and predictable than the token sequence. The randomness of sampling happens at the very last step, token selection, but the features flowing underneath are smooth.

So EAGLE trains a small, lightweight draft network that autoregresses at the feature level: it predicts the next feature from the previous features, and only at the end maps features to tokens. Because features are more predictable than tokens, these drafts are far more accurate, so more of them get accepted by the big model.

```
Medusa style:   guess the next TOKEN directly        (noisy, often rejected)
EAGLE style:    guess the next FEATURE, then the token (smooth, often accepted)

```

## Resolving the uncertainty by feeding back the token

There is a subtlety EAGLE had to fix, which gives the first paper its name: feature uncertainty.

The next feature actually depends on which token was sampled at the previous step. If we do not know the sampled token, the next feature is uncertain. EAGLE solves this by feeding the previously sampled token back into the draft network, along with the features.

So the draft network looks at both the smooth feature stream and the actual token that was just chosen, which removes the uncertainty and lets it predict the next feature accurately. This combination is what makes EAGLE's drafts so good.

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

## The math behind the speedup with small numbers

The speedup of any speculative method is simply how many tokens get accepted per verification pass, on average. We saw this with Medusa.

Suppose token-level drafting gets, on average, `2.5` tokens accepted per pass:

```
token-level speedup = about 2.5 times

```

Because EAGLE's feature-level drafts are more accurate, more of them survive verification. Suppose it gets `3.5` tokens accepted per pass:

```
feature-level speedup = about 3.5 times

```

The whole gain comes from a higher acceptance rate: more guessed tokens are correct, so more are kept per pass. And because every kept token is still verified against the big model, the final output is exactly what the big model would have produced. The speedup is free in quality.

Note: Acceptance counts of `2.5` and `3.5` are just for the sake of understanding, so we can see the relationship. Real numbers depend on the model and task. The rule, more accurate drafts mean more accepted tokens mean more speedup, stays exactly the same.

## EAGLE-2 and dynamic draft trees

EAGLE-2 added another improvement. Instead of a fixed shape of guesses, it builds a dynamic draft tree.

The draft network does not just guess one chain of tokens. It guesses a tree of likely continuations. EAGLE-2 makes this tree context-aware: it spends more guesses where the draft network is confident and fewer where it is unsure, and it shapes the tree on the fly for each input. This squeezes out even more accepted tokens per pass, pushing the speedup higher, while still being lossless.

To learn Speculative Decoding, KV Cache, LLM Internals, vLLM, and to build a Large Language Model (LLM) from scratch, check out our AI and Machine Learning Program at Outcome School.

## How EAGLE lives on today

EAGLE is one of the leading speculative decoding methods in practice.

- It gives some of the highest lossless speedups available, often around `3` to `4` times faster generation, and is widely adopted.
- It is supported in major serving systems like vLLM, SGLang, and TensorRT-LLM, so many production deployments use it.
- Its core lesson, that drafting at the smoother feature level beats drafting at the noisy token level, influenced later fast-inference research, and it was extended further in EAGLE-3.

Speculative decoding is one piece of a much bigger toolkit for fast serving. We have a detailed blog on LLM Inference Optimization that covers these techniques end to end.

So EAGLE took the powerful idea of speculative decoding and made it sharper by guessing the model's smooth internal features instead of its noisy output tokens, getting more accepted tokens and a bigger speedup for free.

## Quick Summary

- EAGLE is a state-of-the-art speculative decoding method that speeds up generation losslessly.
- Speculative decoding guesses several tokens cheaply and verifies them in one pass, so better guesses mean more speedup.
- Guessing the exact next token is noisy because of sampling randomness, which limits earlier methods like Medusa.
- EAGLE's big idea is to draft at the feature level, the smooth internal hidden state, which is far more predictable than tokens.
- It resolves feature uncertainty by feeding the previously sampled token back into the draft network.
- The speedup equals the average accepted tokens per pass, and more accurate feature-level drafts raise it, for example from `2.5` to `3.5` times.
- EAGLE-2 adds context-aware dynamic draft trees for even more speedup, and EAGLE is used in vLLM, SGLang, and TensorRT-LLM.

Now, we have decoded EAGLE piece by piece and understood how drafting smooth internal features instead of noisy tokens makes speculative decoding faster while keeping the output identical.

### Does EAGLE change the output of the language model?

No. EAGLE makes generation faster without changing the output at all. Every drafted token is still verified against the big model, so the final output is exactly what the big model would have produced. The speedup is free in quality.

### Is EAGLE better than Medusa?

Yes. EAGLE usually gets a bigger speedup than Medusa. Medusa guesses the next tokens directly, and token-level guesses are noisy because of sampling randomness, so many get rejected. EAGLE guesses the next feature, which is smoother and more predictable, so more drafts are accepted per pass.

### How much faster does EAGLE make text generation?

EAGLE often gives around 3 to 4 times faster generation. This is among the highest lossless speedups available. The exact number depends on the model and task, since the speedup equals the average number of tokens accepted per verification pass.

### Is EAGLE used in production serving systems?

Yes. EAGLE is supported in major serving systems like vLLM, SGLang, and TensorRT-LLM, so many production deployments use it. It is one of the leading speculative decoding methods in practice, and it was extended further in EAGLE-3.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# What is N-gram Speculation in LLMs and How Does It Speed Up Generation?
URL: https://outcomeschool.com/blog/n-gram-speculation-in-llms
Published: 2026-09-13
Author: Amit Shekhar

What is N-gram Speculation in LLMs and How Does It Speed Up Generation?

# What is N-gram Speculation in LLMs and How Does It Speed Up Generation?

Authors
: - Name
: Amit Shekhar
Published on
: September 13, 2026

N-gram Speculation is a simple trick that makes an LLM write its answer faster. It guesses the next few tokens by finding the same words earlier in the text, and then the model verifies all those guesses in one single run.

In this blog, we will learn about N-gram Speculation in LLMs, a simple trick that makes a language model write its answer faster by guessing the next few words from the text it has already seen. We will also see how an LLM writes one token at a time, why that is slow, what Speculative Decoding is, what an n-gram is, how N-gram Speculation guesses the next tokens by looking up the prompt, how the model verifies those guesses without changing the final answer, and where it works well and where it fails.

We will cover the following:

- How an LLM generates text
- Why generating text is slow
- What is Speculative Decoding?
- The cost of a draft model
- What is an N-gram?
- What is N-gram Speculation?
- N-gram Speculation step by step
- Why the output stays exactly the same
- Where it works well and where it fails
- N-gram Speculation vs Draft Model Speculative Decoding

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## How an LLM generates text

An LLM is a Large Language Model. It is an AI model that reads text and writes text. When we ask a chatbot a question, an LLM is writing the answer.

Before jumping into N-gram Speculation, we must know one thing about how an LLM writes.

An LLM writes its answer one token at a time.

A token is a small piece of text. For the sake of understanding, we can think of a token as a word. So, the sentence "The cat sat on the mat" has six tokens. Punctuation marks like "." are also tokens.

The text we give to the model is called the prompt. It can be a question, a document, a piece of code, or anything else.

Let's say our prompt asks the model to write a sentence about a cat. The model works like below:

- It reads everything written so far, which is the prompt, and predicts one token: "The"
- It adds "The" to the text, reads everything again, and predicts the next token: "cat"
- It adds "cat", reads everything again, and predicts: "sat"
- And so on, till the answer is complete.

So, to write 100 tokens, the model runs 100 times. Each run is called a decoding step.

And, every new token depends on all the tokens before it. So, the model cannot write the 10th token before it has written the 9th token. It has to go one by one.

We have a detailed blog on Autoregressive Models that explains this one-token-at-a-time generation in depth.

## Why generating text is slow

Now, the question is, why is this slow?

An LLM has billions of numbers inside it, called weights. The model runs on a special chip called the GPU. To predict even one token, the GPU has to load all these billions of weights from memory and do the math.

But, here is the catch. Loading the weights from memory takes much more time than doing the math. The GPU is very fast at math. But, it has to wait for the weights to arrive from memory. Most of the time, the GPU is just waiting.

Let's take an analogy. Assume that we have a chef who can cook ten dishes at once. But, the helper brings the ingredients from the store room for only one dish at a time. The chef cooks that one dish in a second and then waits for the helper again. The chef is fast, but the kitchen is slow because of the trips to the store room.

The GPU is the chef. The memory is the store room. Loading weights is the trip. Predicting one token is one dish.

The number of trips decides the speed, not the cooking. This is called being memory-bound. The speed is limited by memory, not by the math.

We have a detailed blog on Prefill vs Decode that explains why this decode phase of an LLM is memory-bound.

Now, one more important thing. Suppose the helper carries the ingredients for ten dishes in a single trip. The trip takes the same time as before. And, the chef cooks all ten dishes at once. So, we get ten dishes in the time we earlier got one.

Similarly, once the weights are loaded, the GPU can process many tokens at once for almost the same cost as one token.

But, there is a problem. The model cannot produce ten new tokens at once, because the second token depends on the first, the third depends on the second, and so on. It has to go one by one.

What it can do is check ten tokens at once, if someone gives it those ten tokens already. Checking means, for each position, the model tells us what it would have predicted there, and we see whether it agrees with the token we gave.

So, here comes the idea: if we can somehow guess the next few tokens cheaply, and then give all of them to the model to check in one run, we can save a lot of trips.

Here comes the Speculative Decoding into the picture.

## What is Speculative Decoding?

Speculative Decoding is a technique where we first guess the next few tokens quickly, and then ask the big model to verify all those guesses in one single run.

Here, the big model means our actual LLM, the one whose answer we want.

Speculate means to guess. So, Speculative Decoding = Guess first + Verify later.

It has two parts:

- Draft: Something cheap and fast guesses the next few tokens. Let's say it guesses 5 tokens.
- Verify: The big model takes all 5 guessed tokens together and checks them in one run. It accepts the guesses it agrees with and throws away the rest.

If the big model agrees with all 5 guesses, we get 5 tokens in the time of 1 run. If it agrees with only 2, we get 2 tokens plus one more correct token from the big model itself. Either way, we never get less than 1 token per run. So, we never lose.

Now, the next big question is: who does the guessing?

In the original Speculative Decoding, the guessing is done by a small LLM called the draft model. It is a smaller version of the big model, so it is fast, and it guesses reasonably well.

## The cost of a draft model

The draft model works, but it has its own problems.

- We need a second model. It has to be trained or found, and it must use the same vocabulary as the big model. Vocabulary means the list of tokens that the model knows. If the two models break text into different tokens, the guesses cannot be compared.
- It takes extra memory on the GPU. Memory is what we are short of.
- It takes time to run. Even if it is small, it still runs once for every guessed token.
- When the big model is updated, the draft model also needs to be updated to match it.

So, the question is, can we guess the next tokens without any extra model at all?

The answer is yes. We just look at the text we already have.

So, here comes the N-gram Speculation to the rescue.

## What is an N-gram?

Before jumping into N-gram Speculation, we must know what an n-gram is.

N-gram = N + gram

- gram means a piece or a unit. Here, one unit is one token.
- N is a number. It tells how many units are together.

In simple words, an n-gram is just N tokens standing next to each other in the text.

Let's take the sentence: "the cat sat on the mat"

- 1-grams: "the", "cat", "sat", "on", "the", "mat"
- 2-grams: "the cat", "cat sat", "sat on", "on the", "the mat"
- 3-grams: "the cat sat", "cat sat on", "sat on the", "on the mat"

That's it. An n-gram is just a small window of N tokens sliding over the text.

Now, one interesting observation. Text repeats a lot. If we see "sat on the" once, and later we see "sat on" again, there is a good chance the next token is "the" again. N-gram Speculation uses exactly this observation.

Now that we have learned about n-grams, it's time to learn about N-gram Speculation.

## What is N-gram Speculation?

N-gram Speculation is a form of Speculative Decoding where the guesses come from matching n-grams in the text we already have, instead of from a draft model.

The text we already have means the prompt plus the tokens generated so far.

In simple words, we take the last few tokens we have written. We search for the same few tokens earlier in the text. If found, we copy the tokens that came after that earlier match and use them as the guess.

There is no draft model here. The draft comes from the text itself.

This is also called Prompt Lookup Decoding, because we look up the prompt to make the guess.

Let's understand with an analogy.

Suppose we are copying a long paragraph from a book by hand. We have written "the quick brown". We do not need to think hard about what comes next. We just look at the book, find "the quick brown", and see that "fox jumps over" comes after it. We copy those words quickly. Then we double check that we copied correctly.

The book is our prompt. Looking at the book is the lookup. Copying "fox jumps over" is the draft. Double checking is the verification by the big model.

[…308ln elided…]

So, our goal is clear. We want to take this giant pile of weights and run it on a normal laptop. Now let's see why this was hard before GGUF.

### The problem before GGUF

To run a model on our laptop, the program needs more than just the weights. It needs a few things together:

- The weights, which are the model's learned numbers, stored as tensors.
- The tokenizer, which is the tool that breaks our text into small pieces the model can read, and joins the pieces back into text. We will understand this better soon.
- The config and metadata, which is the information that describes the model, for example what kind of model it is, how it is built, and how much text it can handle at once.

In the early days, these pieces were often scattered across many separate files in different formats. One file for the weights, other files for the tokenizer, another file for the settings. To load the model, the program had to find all of them, read each one correctly, and stitch them together.

This caused real problems:

- It was fragile. If one file was missing or in a slightly different format, loading failed.
- It was not portable. Sharing a model meant sharing a folder of many files, and another person's tool may read them differently.
- It was slow to load. Reading and combining many files takes time before the model is even ready.

There was an earlier format called GGML that tried to pack things together for running models on normal computers. GGML was a good start and made local inference possible. But as models grew and changed, GGML had limits. It was not flexible enough, and adding new information to the file was painful. Every time the model design changed, the format struggled to keep up.

Let's picture the old scattered way against the single-file goal as below:

```
THE OLD WAY (scattered files):

  +----------------+   +------------------+   +-----------------+
  |  weights file  |   |  tokenizer file  |   |  settings file  |
  +----------------+   +------------------+   +-----------------+
          |                    |                      |
          +--------------------+----------------------+
                               |
                       program must find,
                       read, and stitch all
                       of them together

  fragile, not portable, slow to load

THE GOAL (one organized file):

  +----------------------------------------+
  |  weights + tokenizer + settings        |
  |  all packed together in one file       |
  +----------------------------------------+

  open it and run, nothing to stitch

```

Here, we can see that the old way kept the weights, the tokenizer, and the settings in separate files, so the program had to find each one, read it correctly, and stitch them together. The goal is one organized file that holds everything, so the program can open it and run right away.

We needed a single, well-organized file that holds everything, loads fast, and is easy to extend.

So, here comes GGUF to the rescue.

### What is GGUF?

GGUF is a single file format that stores everything needed to run a large language model for local inference, all in one self-contained file.

GGUF stands for GPT-Generated Unified Format. The key idea for us is in the words Unified Format, where "Unified" means everything the model needs is brought together into one single, organized file, instead of being scattered across many separate files.

In simple words, GGUF is one file that contains the model's weights, the tokenizer, and all the settings, packed neatly together so a program can open it and start running the model right away.

It is the successor to the older GGML format. GGUF was created to fix GGML's limits, and today it is the standard format for running models locally.

Let's use a simple analogy. Suppose we want to move into a new house and we need a bed, a table, and a chair. The old way was like getting these as loose parts in three different boxes, with instructions in three different languages, and we had to assemble everything ourselves. GGUF is like getting one neatly packed box that has everything inside, clearly labeled, ready to use the moment we open it.

So, GGUF is the one box that holds the whole model, ready for our laptop to run.

Now, let's open the box and see what is inside.

### What is stored inside a GGUF file?

A GGUF file is built to hold three kinds of things together. Let's look at each one.

First, the tensors. These are the model's weights, the learned numbers we talked about earlier. This is the biggest part of the file, because a model can have billions of numbers.

Second, the key-value metadata. Metadata is data that describes other data. It is stored as simple pairs of a key and a value, like a label and its answer. For example, a key could be the architecture, which means the type of model and how it is built, and its value tells the program which kind of model this is. Another key could be the context length, which means how many tokens the model can read at once, and its value is a number like 4096. There are many such pairs that fully describe the model.

Third, the tokenizer. A model cannot read raw text. It first breaks the text into small pieces called tokens. A token is a small chunk of text, roughly a word or part of a word. The tokenizer is the tool that does this splitting and also joins tokens back into text. GGUF stores the tokenizer's vocabulary and rules right inside the file, so the program does not need any extra file to understand our text.

We have a detailed blog on Byte Pair Encoding in LLMs that explains how this tokenization step works.

Let's picture the layout of a GGUF file as below:

```
A SINGLE GGUF FILE

+--------------------------------------------------+
|  HEADER                                          |
|    marker "GGUF" + version + counts              |
+--------------------------------------------------+
|  KEY-VALUE METADATA                              |
|    architecture      = "llama"                   |
|    context length    = 4096                      |
|    tokenizer vocab   = [ ...tokens... ]          |
|    quantization info = ...                       |
+--------------------------------------------------+
|  TENSOR INFO (a small table of contents)         |
|    names, shapes, and where each tensor sits     |
+--------------------------------------------------+
|  TENSOR DATA (the weights, the big part)         |
|    [ billions of numbers, the model's brain ]    |
+--------------------------------------------------+

```

Here, we can see that the file starts with a small header. The header begins with the four letters `GGUF`, which is a marker that tells any program "this is a GGUF file". After that comes the key-value metadata, which describes the model in plain labeled pairs. Then comes a small tensor info table, which is like a table of contents that lists every tensor's name, its shape, and where it sits in the file. Finally comes the actual tensor data, the huge block of weights.

So, with one file, the program has the weights, the description, and the tokenizer, all in one place. The problem of scattered files is solved.

Now, there is still one big challenge. These models are huge. Let's see how GGUF helps them fit on a normal laptop.

### What is quantization?

A model with billions of weights is very large. If each weight is stored as a very detailed, very exact number, the file becomes too big to fit in a laptop's memory.

Let's understand the size problem with a simple idea. Each number can be stored using a certain number of bits. A bit is the smallest unit of computer memory, a single 0 or 1. The more bits we use per number, the more precise the number is, but the more space it takes.

Suppose every weight is stored using 16 bits. A model with 7 billion weights would then need about 14 gigabytes just for the weights. That is too big for many laptops to handle comfortably.

So, here comes quantization to the rescue.

Quantization is the technique of storing each weight using fewer bits, so the model becomes much smaller.

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

In simple words, quantization means we round the model's numbers to a simpler, shorter form that takes less space.

Let's use a simple analogy. Suppose a price is 19.997 rupees. If we round it to 20 rupees, it is shorter and easier to store, and for most purposes it is close enough. We lost a tiny bit of exactness, but we saved space. Quantization does the same thing to the model's weights. It stores them with fewer bits, so each number is a little less exact but takes much less room.

Let's see the effect with numbers. If we drop from 16 bits per weight down to about 4 bits per weight, our 7 billion weight model shrinks from around 14 gigabytes to roughly 4 gigabytes. Now it fits on a normal laptop and can run on its CPU or GPU.

But, here is the catch. There is a trade-off.

- Fewer bits means smaller size and faster running, but slightly lower quality. The answers can become a little less accurate, because we made the numbers less exact.
- More bits means larger size and slower running, but higher quality. The answers stay closer to the original model.

So, we choose the level of quantization based on our use case. If we have a small laptop and want speed, we pick a smaller form. If we have more memory and want the best quality, we pick a larger form.

GGUF supports many quantization levels, and it stores the quantized weights directly inside the file. This is one of the biggest reasons GGUF is so useful for local inference.

Quantization is one way to make a model smaller. Another is knowledge distillation, where a small model learns to copy a larger one. We have a detailed blog on how Knowledge Distillation works that explains this in depth.

Now, these quantization levels have names that look strange at first, like `Q4_K_M`. Let's decode them.

### Understanding quantization names like Q4_K_M

When we download a GGUF model, we will see names like `Q4_K_M`, `Q5_K_M`, and `Q8_0`. These look confusing, but they follow a simple pattern. Let's break one down.

Take `Q4_K_M` as below:

```
Q4_K_M
 | | |
 | | +---  M  =  the size variant (S = small, M = medium, L = large)
 | +-----  K  =  a smarter, modern quantization method
 +-------  4  =  about 4 bits used per weight

```

Here, we can see that the name has three parts. The `Q` simply means quantized. The number after it, the `4`, tells us roughly how many bits are used per weight. So `Q4` means about 4 bits per weight, and `Q8` means about 8 bits per weight. The `K` means it uses a smarter, modern method that spends bits more wisely to keep quality high. The last letter, `M`, is a size variant, where `S` is small, `M` is medium, and `L` is large.

So, the simple rule to remember is this:

The number is the bits per weight. A bigger number means more bits, which means bigger file and better quality. A smaller number means fewer bits, which means smaller file and slightly lower quality.

Let me tabulate the common quantization levels for your better understanding so that you can decide which one to use based on your use case.

| Name | Bits per weight | File size | Quality | Good for |
| --- | --- | --- | --- | --- |
| `Q4_K_M` | about 4 | smallest of these | good | laptops with limited memory, a great balance |
| `Q5_K_M` | about 5 | medium | better | a bit more memory, slightly better answers |
| `Q8_0` | about 8 | largest of these | best | plenty of memory, quality matters most |

Here, we can notice that `Q4_K_M` gives the smallest size with good quality, which is why it is one of the most popular choices. As we move to `Q5_K_M` and then `Q8_0`, the file gets bigger and the quality improves, but we need more memory to run it.

Note: If we are not sure which one to pick, `Q4_K_M` is a safe starting point for most laptops, because it balances size and quality very well. If our answers feel a little off and we have spare memory, we can move up to `Q5_K_M` or `Q8_0`.

So, now we know how to read these names and pick the right one based on our use case.

To master Quantization and Model Compression, check out our AI and Machine Learning Program at Outcome School.

### How GGUF loads fast with memory mapping

We learned that a GGUF model can still be a few gigabytes. Now the question is, how does it start so fast without filling up our memory?

The answer is a technique called memory mapping, often written as mmap.

Let's first understand the slow way. The simple way to load a file is to read the whole thing from the disk into memory before we use it. For a 4 gigabyte model, that means waiting until all 4 gigabytes are copied into memory. That is slow, and it uses a lot of memory right away.

So, here comes memory mapping to the rescue.

Memory mapping lets the program treat the file on disk as if it were already in memory, without copying the whole thing first.

In simple words, instead of loading everything up front, the program only reads the parts of the file it actually needs, exactly when it needs them.

Let's use a simple analogy. Suppose we have a thick book. The slow way is to photocopy the entire book before reading a single page. Memory mapping is like keeping the book on the table and simply opening the exact page we need, only when we need it. We do not copy the whole book first. We just read pages on demand.

Let's see the difference as below:

```
WITHOUT memory mapping:

  disk file (4 GB)  ===> copy all 4 GB into memory ===> then start
       slow start, uses a lot of memory immediately

WITH memory mapping (GGUF):

  disk file (4 GB)  --- start immediately --->
       the program reads only the needed parts, when needed
       fast start, memory used efficiently

```

Here, we can see that without memory mapping the program must copy all 4 gigabytes before it even starts, which is slow and heavy on memory. With memory mapping, the program starts right away and pulls in only the parts of the model it needs, when it needs them. This is why a GGUF model can start so quickly.

GGUF is designed to work perfectly with memory mapping. Because the tensors are laid out in a clean, ordered way inside the file, the program can jump straight to any tensor it needs and read it directly. The model starts fast and uses memory efficiently.

This is how GGUF gives us a fast startup on a normal machine.

If we want to go deep into LLM Inference Engineering and Cloud vs On-device Deployment, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

### Why GGUF is cross-platform and extensible

There are two more qualities of GGUF that make it so widely used. Let's understand both.

First, GGUF is cross-platform. Cross-platform means it works the same way across different operating systems and devices. The same GGUF file runs on Windows, macOS, and Linux, and on different kinds of processors. We do not need a different file for each system. We download one GGUF file and it just works wherever we run it.

Second, GGUF is extensible. Extensible means it is easy to add new information to the format without breaking older files. Remember, the metadata inside GGUF is stored as simple key-value pairs. So, when a new kind of model needs a new setting, the format simply adds a new key-value pair. Old programs can still read the file, and new programs can read the new key. This is exactly the weakness that the older GGML format had, and GGUF fixed it.

So, GGUF is portable across machines and flexible enough to grow with new models. This is why it became the standard.

Now, let's see where GGUF is actually used.

### GGUF in the real world

GGUF is the format used by llama.cpp and the popular tools built on top of it.

Let's understand `llama.cpp` first. It is an open-source program written to run large language models efficiently on normal computers, including laptops, using the CPU or the GPU. It is fast, lightweight, and it reads models in the GGUF format. GGUF was created as part of this `llama.cpp` world to be the clean, single-file format these models use.

Many friendly tools are built on top of `llama.cpp`, and they all use GGUF:

- Ollama. This is a tool that lets us download and run models locally with a simple command. Under the hood, it uses GGUF files and `llama.cpp`.
- LM Studio. This is a desktop app with a nice screen where we can search for models, download GGUF files, and chat with them, all on our own machine.

Let's picture how these pieces stack together as below:

```
  +-----------------+        +-----------------+
  |     Ollama      |        |    LM Studio    |   the friendly tools we use
  +-----------------+        +-----------------+
            |                         |
            +------------+------------+
                         |
                +------------------+
                |    llama.cpp     |   runs the model efficiently
                +------------------+
                         |
                +------------------+
                |  .gguf file      |   weights + tokenizer + metadata
                +------------------+

```

Here, we can see that the GGUF file sits at the bottom holding everything the model needs. The `llama.cpp` program reads that file and runs the model. The friendly tools like Ollama and LM Studio sit on top of `llama.cpp`, giving us a simple way to use it. So they all rely on the same single GGUF file underneath.

In all of these, the flow is the same. We download a single file that ends with `.gguf` for the model and the quantization level we want, the tool opens it using memory mapping, reads the weights, the tokenizer, and the metadata from that one file, and we start chatting. There is nothing to assemble and no scattered files to manage.

So, anywhere we want to run a large language model on our own machine, GGUF is very likely the format we will use.

The models we run locally like this are often Small Language Models, compact enough to fit on a laptop or phone. We have a detailed blog on Small Language Models (SLMs) that explains why smaller models matter.

This is how GGUF works. It packs the model's weights, its tokenizer, and its metadata into one self-contained file, it uses quantization to shrink the weights so big models fit on a normal laptop, and it loads quickly with memory mapping, which is why it became the standard format for running large language models locally.

### What is the difference between GGUF and GGML?

GGUF is the successor to the older GGML format. GGML made local inference possible, but it was not flexible enough, and adding new information to the file was painful. GGUF fixed this by storing metadata as simple key-value pairs, so new settings can be added without breaking older files.

### Which GGUF quantization level should we pick?

`Q4_K_M` is a safe starting point for most laptops, because it balances size and quality very well. If the answers feel a little off and we have spare memory, we can move up to `Q5_K_M` or `Q8_0`. A bigger number means a bigger file and better quality.

### Does a quantized GGUF model give worse answers?

Slightly. Fewer bits per weight make the numbers a little less exact, so the answers can become a little less accurate. In return, the model becomes much smaller and faster. With more bits, the file is larger but the answers stay closer to the original model.

### Do we need separate tokenizer files to run a GGUF model?

No. GGUF stores the tokenizer's vocabulary and rules right inside the file, along with the weights and the metadata. So the program does not need any extra file to understand our text. We download a single `.gguf` file and start running the model.

### Do Ollama and LM Studio use GGUF?

Yes. Both Ollama and LM Studio are built on top of `llama.cpp`, and they use GGUF files. The GGUF file holds everything the model needs, `llama.cpp` reads it and runs the model, and these tools give us a simple way to use it.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-348 and 657-973 of 973; 308 middle lines (16.0KB) elided. Read artifact://92 for full output]
