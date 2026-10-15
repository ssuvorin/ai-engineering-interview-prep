> Source: https://outcomeschool.com/blog/decoding-medusa

# What is Medusa? Multi-Head Speculative Decoding Explained
URL: https://outcomeschool.com/blog/decoding-medusa
Published: 2026-08-31
Author: Amit Shekhar

What is Medusa? Multi-Head Speculative Decoding Explained

# What is Medusa? Multi-Head Speculative Decoding Explained

Authors
: - Name
: Amit Shekhar
Published on
: August 31, 2026

Medusa is a method that makes a language model generate text 2 to 3 times faster by adding a few extra heads to it. Each extra head guesses a token further ahead, so the model can produce several tokens in one step.

In this blog, we will learn about Medusa, a simple way to make a language model generate text 2 to 3 times faster by giving it several extra heads that guess multiple future tokens at once.

We will cover the following:

- What is Medusa?
- Why text generation is slow
- A quick recap of speculative decoding
- The problem with needing a draft model
- The big idea: many heads on one model
- How tree attention checks many guesses at once
- The math behind the speedup with small numbers
- The results
- How Medusa lives on today
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

Medusa was introduced in 2024 in the famous research paper "Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads" by Tianle Cai, Yuhong Li, Tri Dao, and their collaborators.

Medusa makes a model generate text much faster, without changing the model's answers, and without needing a second helper model. The name comes from the mythical Medusa with many heads, because this method adds several prediction heads to one model. So, let's decode it piece by piece.

## What is Medusa?

Medusa is a method to speed up text generation by adding extra prediction heads to a language model.

A normal model has one head that predicts the next token. Medusa adds a few more heads, where each one tries to predict a token further ahead. So instead of guessing just the next token, the model guesses the next few tokens all at once, and then quickly checks them.

In simple words, Medusa lets the model say "here is the next word, and here is my guess for the few words after it too", and if those guesses are right, we get several words for the price of one.

## Why text generation is slow

A language model generates text one token at a time. To produce a token, it runs a full forward pass through the whole network. Then it feeds that token back in and runs another full pass for the next token, and so on.

```
pass 1 -> token 1
pass 2 -> token 2
pass 3 -> token 3
...

```

So writing 100 tokens means 100 full passes, one after another. This is slow, and it is the main reason chatbots feel like they are typing.

The frustrating part is that a forward pass is not actually busy. Generating one token barely uses the GPU, because the GPU is built to do huge amounts of math in parallel, but we are asking it for just one token at a time. The hardware is mostly idle. We needed a way to make each pass produce more tokens. We needed a solution for that, and Medusa is one answer.

We have a detailed blog on Prefill vs Decode: LLM Inference Optimization that explains why this decode phase leaves the GPU waiting.

## A quick recap of speculative decoding

One earlier answer was speculative decoding. The idea is to use a small, fast model to guess several tokens ahead, then let the big model check all those guesses in a single pass. If the guesses are right, the big model accepts them, and we get several tokens from one pass of the big model.

This works well, but it has a cost.

## The problem with needing a draft model

Speculative decoding needs a second model, the small draft model, to make the guesses. That brings problems.

- We have to find or train a small model that matches the big one well.
- We have to load and run two models, using more memory and adding complexity.

It would be much simpler if the big model could make its own guesses, with no separate draft model at all. That is exactly what Medusa does.

## The big idea: many heads on one model

Medusa adds a few small extra heads on top of the existing model. Each head is tiny, just a small layer. They all read the same internal state the model already computed.

- The original head predicts the next token, as usual. Call it the position 1 token.
- Medusa head 1 predicts the token at position 2.
- Medusa head 2 predicts the token at position 3.
- Medusa head 3 predicts the token at position 4.

```
                model's internal state
                  /     |     |     \
                 v      v     v      v
            [orig]  [head1][head2][head3]
              |        |      |      |
              v        v      v      v
           token1   token2 token3 token4   <- all guessed in ONE pass

```

So in a single forward pass, the model produces not just the next token, but a guess for the next several tokens too. The base model is frozen, and only these small heads are trained, which is cheap and fast.

Think of how you sometimes finish a friend's sentence before they do. If your guess is right, the conversation moves faster. If it is wrong, no harm done, they just say the real word. Medusa's heads are like that: they guess the next few words, and we keep the guesses only when they turn out to be correct.

But guesses can be wrong. So we need a way to check them and only keep the correct ones.

## How tree attention checks many guesses at once

Each head does not give just one guess. It gives its top few candidates. For example, head 1 might suggest two likely words, and head 2 might suggest two likely words. Combining them gives several possible continuations.

Medusa arranges all these candidate continuations into a tree, and then checks the entire tree in a single forward pass using a special attention mask called tree attention. This mask lets every candidate path be verified at the same time, without them interfering with each other.

After verification, Medusa keeps the longest path whose tokens the model agrees with, and throws away the rest. So we always end up with tokens the model itself would have produced. The output is the same as normal generation, just produced faster.

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

Let's see the speedup with simple numbers.

Normal generation. Each forward pass produces exactly 1 token.

```
to produce 1 token  -> 1 pass
to produce 6 tokens -> 6 passes

```

Medusa. In one pass, the original head plus 3 Medusa heads guess 4 tokens. Then one verification pass checks them. Suppose, on average, 3 of those guessed tokens are accepted each round.

```
round 1: 1 pass guesses 4 tokens, 3 are accepted  -> 3 tokens
round 2: 1 pass guesses 4 tokens, 3 are accepted  -> 3 tokens

```

So 2 passes produced 6 tokens, while normal generation would need 6 passes for the same 6 tokens. That is a 3 times speedup.

The speedup is simply the average number of tokens accepted per pass:

```
speedup = average accepted tokens per pass

```

If Medusa accepts about `2.5` tokens per pass on average, that is roughly a `2.5` times speedup. And crucially, since we only keep tokens the model agrees with, the final text is exactly what the model would have written anyway.

Note: Three extra heads and accepting 3 tokens are just for the sake of understanding, so we can calculate by hand. Real setups tune the number of heads and the tree shape. The idea stays exactly the same: more tokens per pass means faster generation.

## The results

Medusa sped up generation by about 2 to 3 times on popular models, with no change to the output quality, because every accepted token is verified against the model itself.

It is also simple to add. The base model is left frozen, and only the small heads are trained, which takes very little time and data. There is no separate draft model to manage. This simplicity is a big part of why Medusa became popular.

If we want to go deep into Speculative Decoding, KV Cache, Paged Attention, and vLLM, and build a Large Language Model (LLM) from scratch, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## How Medusa lives on today

Medusa pushed forward a whole line of fast-generation methods that need no draft model.

- It directly inspired methods like EAGLE, which predict future tokens even more accurately by working at the level of the model's internal features, and now give some of the highest speedups available.
- The idea of extra heads that predict multiple future tokens also appears in training. Multi-Token Prediction, used in models like DeepSeek-V3, trains a model with extra heads from the start, which both improves the model and gives a built-in way to speed up generation.
- Tree-based verification, where many candidate paths are checked in one pass, is now a common trick in fast inference systems like TensorRT-LLM.

So Medusa took the powerful idea of speculative decoding and made it simpler, by letting the model grow its own heads instead of leaning on a separate draft model.

Medusa is one of many tricks that make generation fast. We have a detailed blog on LLM Inference Optimization that covers these techniques end to end.

## Quick Summary

- Medusa speeds up text generation by adding several small extra heads to a model, each guessing a token further ahead.
- Normal generation is slow because it produces only one token per forward pass, leaving the GPU mostly idle.
- Speculative decoding sped things up but needed a separate draft model, which adds complexity.
- Medusa's big idea is to put many heads on one model, so a single pass guesses several future tokens, with the base model frozen and only the cheap heads trained.
- Tree attention checks many candidate continuations in one pass, and Medusa keeps the longest path the model agrees with, so the output is unchanged.
- The speedup equals the average number of tokens accepted per pass, often around 2 to 3 times.
- Medusa inspired later methods like EAGLE and the Multi-Token Prediction used in modern models.

Now, we have decoded Medusa piece by piece and understood how giving a model extra heads lets it generate several tokens at once.

### Does Medusa change the answers of the model?

No. Medusa does not change the model's answers. It keeps only the longest path of guessed tokens that the model agrees with and throws away the rest. So the final text is exactly what the model would have written with normal generation, just produced faster.

### Do we need to retrain the whole model to use Medusa?

No. The base model is left frozen, and only the small extra heads are trained. This takes very little time and data. This simplicity is a big part of why Medusa became popular.

### Is Medusa better than speculative decoding with a draft model?

Medusa is simpler than speculative decoding with a draft model. We do not need to find or train a small model that matches the big one, and we do not need to load and run two models. The big model makes its own guesses through its extra heads, which saves memory and complexity.

### What is the difference between Medusa and EAGLE?

Medusa guesses future tokens directly with extra heads, while EAGLE predicts future tokens by working at the level of the model's internal features. Medusa directly inspired EAGLE. Because EAGLE's guesses are more accurate, it now gives some of the highest speedups available.

### How much faster is Medusa than normal generation?

Medusa sped up generation by about 2 to 3 times on popular models. The speedup equals the average number of tokens accepted per pass. Since every accepted token is verified against the model itself, there is no change to the output quality.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

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
[…517ln elided…]

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

[Showing lines 1-366 and 884-1200 of 1200; 517 middle lines (28.2KB) elided. Read artifact://62 for full output]
