> Source: https://outcomeschool.com/blog/decoding-deepseek-v4

# What is DeepSeek-V4 and How Does It Work? Architecture Explained
URL: https://outcomeschool.com/blog/decoding-deepseek-v4
Published: 2026-04-24
Author: Amit Shekhar

What is DeepSeek-V4 and How Does It Work? Architecture Explained

# What is DeepSeek-V4 and How Does It Work? Architecture Explained

Authors
: - Name
: Amit Shekhar
Published on
: April 24, 2026

DeepSeek-V4 is a family of open Mixture-of-Experts language models that supports a one-million-token context, at roughly a tenth of the cost of DeepSeek-V3.2.

In this blog, we will learn about DeepSeek-V4, the new family of open Mixture-of-Experts language models that natively supports a one-million-token context with dramatically lower inference cost.

DeepSeek-V4 makes one-million-token context roughly a tenth as expensive as it was in DeepSeek-V3.2. It introduces a new attention design, a new way of doing residual connections, a new optimizer, and a new post-training pipeline. We will decode each of these one by one.

We will cover the following:

- The Big Picture
- Two Models: DeepSeek-V4-Pro and DeepSeek-V4-Flash
- Hybrid Attention with CSA and HCA
- Manifold-Constrained Hyper-Connections (mHC)
- Muon Optimizer
- FP4 Quantization-Aware Training
- Pre-Training
- Post-Training: Specialist Training and On-Policy Distillation
- Reasoning Modes
- Putting It All Together
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

DeepSeek-V4 is built to solve one core problem: make ultra-long context cheap. Modern reasoning models and AI Agents need to handle very long inputs - long documents, long tool histories, long agent trajectories. The standard attention mechanism in a Transformer becomes very expensive as the input gets longer. DeepSeek-V4 redesigns attention so that even a one-million-token input remains practical.

In simple words:

DeepSeek-V4 = DeepSeek-V3 + Hybrid Compressed Attention + Better Residual Connections + Muon Optimizer + On-Policy Distillation.

Let's put this into perspective with real numbers. At a one-million-token context:

- DeepSeek-V4-Pro uses only 27% of the per-token compute of DeepSeek-V3.2.
- DeepSeek-V4-Pro uses only 10% of the KV cache size of DeepSeek-V3.2.
- DeepSeek-V4-Flash uses only 10% of the per-token compute and 7% of the KV cache size of DeepSeek-V3.2.

This is a massive efficiency gain. Now, let's decode each piece.

## Two Models: DeepSeek-V4-Pro and DeepSeek-V4-Flash

DeepSeek-V4 ships as two models. Both are Mixture-of-Experts (MoE) models. In an MoE model, the feed-forward layer is split into many small expert networks, and a router picks only a few experts per token. This is how the total parameter count can be huge while the per-token compute stays small.

Let me tabulate the differences between the two models for your better understanding so that you can decide which one to use based on your use case.

| Model | Total Parameters | Activated Parameters | Transformer Layers | Context Length | Pre-training Tokens |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-V4-Flash | 284B | 13B | 43 | 1M | 32T |
| DeepSeek-V4-Pro | 1.6T | 49B | 61 | 1M | 33T |

Here, "activated" means the parameters that actually run for each input token. In an MoE model, only a small fraction of the experts are active per token, so activated parameters are much smaller than total parameters.

Both models support a context of one million tokens natively. Both are trained on more than 32 trillion tokens.

DeepSeek-V4-Pro is the larger, more capable model. DeepSeek-V4-Flash is the smaller, faster, more cost-efficient model.

## Hybrid Attention with CSA and HCA

This is the most important change in DeepSeek-V4. Let's understand the problem first.

The Problem. Standard attention compares every query token with every other token. Suppose we have N tokens in the input. The cost grows like N x N. At one million tokens, this becomes one trillion comparisons across the full sequence. The KV cache, which is the memory of past keys and values, also grows linearly with N. Both of these become a serious bottleneck for long context.

We have a detailed blog on KV Cache in LLMs that explains what KV cache is and why it matters, and another on KV Cache Compression that covers the standard ways to shrink it.

The Solution. Here comes the hybrid attention design to the rescue. DeepSeek-V4 introduces two new attention types and uses both of them in an interleaved manner across layers:

- CSA (Compressed Sparse Attention) - lighter compression, but uses sparse selection.
- HCA (Heavily Compressed Attention) - heavier compression, but keeps attention dense.

Let's decode the names first.

CSA = Compressed + Sparse + Attention.

HCA = Heavily + Compressed + Attention.

The best way to learn this is by taking an example. Let's say we are reading a huge library of one million pages and we want to answer a question. Standard attention is like reading every single page from start to end before answering. It works, but it is painfully slow.

CSA and HCA both fix this, but in different ways. We will use this library example throughout to understand both. Let's decode each one.

### CSA: Compressed Sparse Attention

CSA does two things to make attention cheap.

Step 1: Compress. Instead of keeping the KV cache for every single token, CSA combines every `m` consecutive tokens into one compressed entry using learned softmax weights. Just for the sake of understanding, let's say `m = 4`. So every 4 tokens get combined into 1 entry in the KV cache. The KV cache shrinks by a factor of `m`.

In our library example, this is like grouping every 4 pages into one summary card. Instead of reading 1 million pages, we now have only 250K summary cards to look at.

Step 2: Select. After compression, CSA still does not look at every summary card. It uses a small Lightning Indexer to score each compressed entry against the current query, and then picks only the top-k most relevant ones. The Lightning Indexer runs in FP4 precision to keep this scoring step cheap.

In our library example, this is like a quick scanner who flips through the 250K summary cards, scores each one for relevance, and hands us only the top few cards. We then read only those few cards in detail. Most of the library is skipped completely.

For a deeper background on Q, K, V in attention, we have a detailed blog on Math Behind Attention: Q, K, V.

Here is a simple ASCII picture:

```
All tokens:    [t1][t2][t3][t4][t5][t6][t7][t8] ...
                |__________|  |__________|
                  group 1       group 2
                     |             |
Compressed:        [C1]          [C2]          [C3] ...
                     |             |             |
Lightning Indexer scores each one against current query
                     |             |             |
                  score=0.9     score=0.2     score=0.8
                     |             |             |
Top-k selection:   [ C1 ]        ( C2 )        [ C3 ]
                   picked        skipped       picked
                     |                           |
                     +-------------+-------------+
                                   |
                                   v
                  Attention runs only on [C1] and [C3]
                         (the picked compressed entries)

```

So CSA first compresses many tokens into one, and then picks only the few compressed entries that look most relevant. This is how CSA brings the cost down. Both compute and memory are saved.

### HCA: Heavily Compressed Attention

This was all about CSA. Now, let's move to HCA.

HCA makes a different trade-off. It compresses much more aggressively, and because the compressed sequence is already tiny, dense attention on it is cheap. No need for sparse selection.

HCA uses a much larger group size `m'`, much bigger than `m` in CSA. For DeepSeek-V4, `m'` is set to 128. So instead of combining 4 tokens into one entry, HCA combines 128 tokens into one entry. The KV cache shrinks even more dramatically.

In our library example, this is like grouping every 128 pages into one summary card. Now we have only about 7,800 summary cards in total. Since the number of cards is already very small, we just read all of them, every time. There is no need to pick the top few.

So CSA and HCA are two different design points with the same goal - cheap long-context attention. CSA does mild compression plus sparse top-k selection. HCA does aggressive compression plus dense attention. The result for both: very low compute and very low memory.

This was all about HCA. Now, let's see how the actual model uses both.

In DeepSeek-V4, the layers are interleaved. For DeepSeek-V4-Flash, the first two layers use pure sliding window attention, and the rest alternate between CSA and HCA. For DeepSeek-V4-Pro, the first two layers use HCA, and the rest alternate between CSA and HCA. This way, different layers handle long context in slightly different ways, and together they cover both fine-grained selection (CSA) and broad coverage (HCA).

### Sliding Window Branch

Now, a natural question arises - what if compression blurs out important details from very recent tokens?

The answer is the sliding window branch. Both CSA and HCA also keep a small extra set of recent uncompressed KV entries. For DeepSeek-V4, this window size is 128 tokens.

In our library example, this is like always keeping the last 128 pages we just read on our desk in full. Compression is used for the older pages, but the most recent pages are right there in front of us, uncompressed and ready to read. This makes sure that local fine-grained dependencies are not lost.

### Attention Sink

One more small but clever trick. In the core attention of both CSA and HCA, DeepSeek-V4 adds a small set of learnable sink logits to the denominator of the softmax. This allows each attention head to have attention scores that sum to less than 1.

Why does this help? In standard attention, the scores are forced to sum to exactly 1. This means every query token must distribute all of its attention somewhere, even when nothing in the context is actually relevant. Attention sinks let the model say "none of these are important right now" and spend less attention overall.

DeepSeek-V4 also applies RMSNorm on the queries and compressed KV entries just before the core attention step. This is what keeps attention logits stable and prevents them from exploding.

Note: Put together, CSA, HCA, Sliding Window, and Attention Sink make one trade-off possible: less memory, less compute, with no major loss in quality. That is what makes one-million-token context practical.

## Manifold-Constrained Hyper-Connections (mHC)

This was all about attention. Now, let's move to the residual connections inside the Transformer.

Let's decode the name first.

mHC = Manifold + Constrained + Hyper + Connections.

In a normal Transformer, every layer adds its output to a "residual stream" - a single shared signal that flows from the bottom of the model to the top. Hyper-Connections (HC) widen this residual stream by a factor of `n_hc` (set to 4 in DeepSeek-V4), turning the single stream into multiple parallel streams. Three learned matrices (A, B, C) mix these streams at every layer, giving the model more flexibility in how information flows.

The issue with plain HC is that it becomes numerically unstable when we stack many layers. The signal can blow up or collapse. Training breaks down.

So, here comes mHC to the rescue. mHC fixes the problem by constraining the residual mapping matrix to lie on a special manifold called the Birkhoff polytope - the set of doubly stochastic matrices. A doubly stochastic matrix is a matrix whose every row sums to 1 and every column sums to 1. This simple constraint bounds the largest stretch factor (the spectral norm) of the matrix at 1, so the signal cannot blow up as it passes through dozens of layers.

The result is that deeper stacks train stably, and the model expressivity is preserved. It works perfectly.

## Muon Optimizer

This was all about mHC. Now, let's move to the optimizer.

DeepSeek-V4 swaps the optimizer for most of its parameters from AdamW to Muon.

Muon = An optimizer that uses the full gradient matrix and orthogonalizes the update direction.

Why does this matter? Most optimizers like AdamW treat each weight independently. Muon, on the other hand, looks at the full gradient matrix and applies an orthogonalization step before doing the weight update. This orthogonalization is done using Newton-Schulz iterations. It normalizes all the singular values of the update matrix to be close to 1, so no single direction in the update dominates. The result is faster convergence and more stable training.

A few important points:

- AdamW is still used for the embedding module, the prediction head, all RMSNorm modules, and the static parts of mHC.
- Muon is used for everything else.
- The DeepSeek team uses a hybrid Newton-Schulz iteration with carefully chosen coefficients for stable orthogonalization.

This gives us the best of both worlds. Muon brings faster convergence where it matters, and AdamW stays where it is already proven to work well.

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

## FP4 Quantization-Aware Training

Now, let's move to how DeepSeek-V4 makes inference faster and cheaper. The answer is FP4 Quantization-Aware Training.

Let's decode this.

- FP4 stands for floating point with only 4 bits per number. Compared to FP8 or BF16, FP4 uses much less memory and bandwidth. It makes our life easier on the hardware side.
- Quantization-Aware Training (QAT) means the model is trained while simulating the lower-precision number format, so the weights adapt to the precision loss during training itself. Without QAT, we would squeeze the weights down only at deployment time, and the model would lose quality. With QAT, the model learns to live with low precision.

DeepSeek-V4 applies FP4 to two key places:

- MoE expert weights, which take up most of the GPU memory.
- The Query-Key (QK) path of the CSA indexer, where the lightning indexer computes scores in FP4.

There is one more clever detail here. FP8 (E4M3) has 2 more exponent bits than FP4 (E2M1), which gives it a much wider dynamic range. Because of this, the FP4 block scale factors can be fully absorbed into the FP8 format during dequantization. This means the FP4-to-FP8 dequantization is lossless, and the entire existing FP8 training pipeline can be reused without any modification.

The end result is a 2x speedup on the top-k selector while preserving a 99.7% recall of KV entries. There is no major quality loss.

## Pre-Training

Now that we have learned about the architecture and optimizer, it's time to learn about pre-training.

Data. The pre-training corpus has more than 32 trillion tokens. It includes mathematical content, code, web pages, long documents, scientific papers, and multilingual data. The team puts a special emphasis on long-document curation since the model is built for long context.

Sequence length scheduling. Training does not start at one-million tokens directly. First, the model trains at a sequence length of 4K. Then, the length is extended to 16K. After that, to 64K. Finally, to 1M. Sparse attention is also turned on gradually. The model first warms up with dense attention for the first 1T tokens, and sparse attention is introduced at 64K and kept on for the rest of the training.

Mitigating Training Instability. Training trillion-parameter MoE models is hard. Loss spikes happen. But here is the catch - simple rollbacks do not prevent the next spike from happening. The DeepSeek team found two practical tricks that fix this:

- Anticipatory Routing. The MoE routing network at step `t` is computed using slightly older parameters `θ_{t-Δt}`, while the rest of the backbone uses the current parameters `θ_t`. This asymmetry breaks the feedback loop where bad routing causes outliers, which then cause worse routing.
- SwiGLU Clamping. The output of the SwiGLU activation is clamped to a fixed range. This prevents extreme values from appearing and destabilizing training.

With these two tricks in place, training stays stable all the way through.

## Post-Training: Specialist Training and On-Policy Distillation

Till now, we have learned about pre-training. Now, it's time to learn about post-training.

Post-training is where DeepSeek-V4 takes a different path from many other models. The pipeline has two stages. Let's decode each one.

### Stage 1: Specialist Training

For each target domain like mathematics, coding, agent use, instruction following, and etc., the DeepSeek team trains a separate expert model. Each expert model is built in two steps.

First, the base model goes through Supervised Fine-Tuning (SFT) on high-quality, domain-specific data. This establishes the foundational capability for that domain. Then, Reinforcement Learning is applied using GRPO (Group Relative Policy Optimization), guided by domain-specific reward signals. This sharpens the model for the specific success criteria of that domain.

After this stage, the team has multiple specialist expert models - one per domain, each trained for varying reasoning efforts - each excelling in its own field.

This was all about Stage 1. Now, let's move to Stage 2.

### Stage 2: On-Policy Distillation (OPD)

Now, a natural question arises - how do we combine all these expert models into one final unified model?

The answer is On-Policy Distillation (OPD).

In simple words:

On-Policy Distillation = The student model generates its own outputs, and learns to match the probability distribution of the right teacher expert for each task.

Let's understand what makes OPD different from regular distillation.

In regular distillation, the student learns from data that the teacher produced. But there is one catch - the student never sees the kind of outputs it actually produces at inference time. This creates a gap between training and real behavior.

In OPD, the student samples its own trajectories. This is the "on-policy" part. The student writes its own drafts, and the teacher corrects each token by providing the full vocabulary distribution it would have used. The student is pulled towards the teacher's distribution using reverse KL loss. Reverse KL is mode-seeking - it pushes the student to concentrate probability mass where the teacher's mass is concentrated, rather than smearing out across all teacher modes. This gives sharper, more decisive outputs.

Also, different teachers are weighted based on the task. For a math task, the math expert teaches more. For a coding task, the coding expert teaches more. This way, all the specialist knowledge gets merged into one single unified student.

This step replaces the traditional mixed RL stage that DeepSeek-V3.2 used. The team found that OPD gives more stable and faithful knowledge transfer than weight merging or mixed RL, which is why it became the core consolidation step in the DeepSeek-V4 post-training pipeline.

## Reasoning Modes

This was all about post-training. Now, let's move to how DeepSeek-V4 actually serves users at inference time.

DeepSeek-V4 supports three reasoning modes that the user can pick depending on how hard the task is. Let me tabulate the differences between them for your better understanding so that you can decide which one to use based on your use case.

| Reasoning Mode | When to Use | How it Works |
| --- | --- | --- |
| Non-think | Routine daily tasks, quick answers | No ` ` block, direct response |
[…414ln elided…]
Published: 2026-04-20
Author: Amit Shekhar

What is Cross-Entropy Loss?

# What is Cross-Entropy Loss?

Authors
: - Name
: Amit Shekhar
Published on
: April 20, 2026

Cross-Entropy Loss is a number that tells us how wrong our predicted probabilities are. It measures how different the model's predicted probabilities are from the true answer. The closer the prediction is to the truth, the smaller the loss.

In this blog, we will learn about the math behind Cross-Entropy Loss with a step-by-step numeric example.

When we train a classification model in machine learning, the model predicts probabilities for each class. For example, given an image, the model outputs something like: "I am 70% sure this is a cat, 20% sure it is a dog, and 10% sure it is a rabbit." To train the model, we need a way to measure how wrong these predictions are compared to the true answer. This is exactly what Cross-Entropy Loss does. It is the most widely used loss function in classification tasks, and it powers the training of almost every modern AI model, including GPT, BERT, and image classifiers.

When we hear Cross-Entropy Loss, it sounds complex. But do not worry. If we break it down into its individual parts, every single piece is simple. Our goal is to decode this so clearly that by the end, we will be able to explain how Cross-Entropy Loss works to anyone.

We will cover the following:

- The Big Picture
- What is Cross-Entropy?
- The Cross-Entropy Loss Formula
- Why We Take the Negative Log
- Binary Cross-Entropy Loss
- Categorical Cross-Entropy Loss
- Step-by-Step Numeric Example
- Cross-Entropy Loss for Language Models
- The Gradient of Cross-Entropy Loss
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture. Cross-Entropy Loss measures how different the predicted probability distribution is from the true probability distribution. If our prediction is close to the truth, the loss is small. If our prediction is far from the truth, the loss is large.

In simple words:

Cross-Entropy Loss = A number that tells us how wrong our predicted probabilities are.

The lower the cross-entropy, the better the model. During training, we keep updating the model weights to make this loss as small as possible. The algorithm that actually performs these weight updates is called gradient descent. We have a detailed blog on Math Behind Gradient Descent that explains how this works step by step.

## What is Cross-Entropy?

The word Cross-Entropy comes from information theory. Let's decompose it:

Cross-Entropy = Cross + Entropy

- Entropy measures the uncertainty of a probability distribution. If a coin is perfectly fair (50% heads, 50% tails), the entropy is high because we are very unsure about the outcome. If a coin always lands heads (100% heads, 0% tails), the entropy is zero because there is no uncertainty.
- Cross means we are comparing two distributions: the true distribution (what should happen) and the predicted distribution (what our model thinks will happen).

So, Cross-Entropy measures the uncertainty we have when we use the predicted distribution to describe events that actually follow the true distribution. If the two distributions are identical, the cross-entropy is at its minimum. If they are very different, the cross-entropy is large.

The Weather Forecaster Analogy

The best way to learn this is by taking an example. Suppose we have a weather forecaster who every morning announces the chance of rain, sunshine, and snow as probabilities (e.g. "60% rain, 30% sunshine, 10% snow"). At the end of the day, exactly one of these actually happens.

Now, how do we score this forecaster fairly?

- If she says "90% rain" and it rains, she gets a very small penalty. Great forecast.
- If she says "90% sunshine" and it rains, she gets a huge penalty. She was confidently wrong.
- If she says "34% rain, 33% sunshine, 33% snow" (completely unsure) and it rains, she gets a moderate penalty. Hedging is neither punished heavily nor rewarded.

Cross-Entropy Loss is exactly this scoring system. The model is the forecaster, the softmax output is the probability announcement, and the true label is what actually happened. We will keep coming back to this analogy throughout the blog.

## The Cross-Entropy Loss Formula

Before we write the formula, let's see the full pipeline of how cross-entropy loss is computed during training:

```
  [raw scores]        [probabilities]         [loss]
   (logits)     -->    (after softmax)  -->  (-log of correct class)
  z = [2, 3, 1]        p = [0.24, 0.66, 0.09]     0.4076
       |                     |                       |
       +-----> softmax ------+----> -log(p_dog) -----+

```

The raw scores (logits) come out of the final layer of the model. Softmax turns them into probabilities that sum to 1. Cross-Entropy Loss then looks at the probability of the correct class and takes its negative log.

The general formula for Cross-Entropy Loss is:

```
CE = - sum over all classes i of [ y_i * log(p_i) ]

```

Here:

- `y_i` is the true label for class `i` (usually 1 for the correct class, 0 for all others)
- `p_i` is the predicted probability for class `i`
- `log` is the natural logarithm (base `e`)
- The sum runs over all classes

Since `y_i` is 1 only for the correct class and 0 for all others, the formula simplifies to:

```
CE = - log(p_correct)

```

Where `p_correct` is the predicted probability for the correct class.

In simple words, cross-entropy loss is just the negative log of the probability that our model assigned to the correct answer.

## Why We Take the Negative Log

Now, a natural question arises - why do we take the log, and why the negative sign?

> Why should a forecaster who says "90% sunshine" on a rainy day be punished far more than one who says "60% sunshine"? Because confident mistakes are more dangerous than hedged mistakes. The log makes this punishment happen automatically.

Let's understand this step by step.

Why log?

Suppose our model predicts the correct class with probability `0.9`. This is a great prediction. Now suppose another model predicts the correct class with probability `0.1`. This is a terrible prediction. We want our loss to reflect this difference strongly.

If we just used `1 - p`, the difference between `0.9` and `0.1` would be only `0.8`. That does not feel strong enough. But if we use `log(p)`:

- `log(0.9) = -0.105`
- `log(0.1) = -2.303`

The log stretches out the small probabilities and punishes them much more harshly. Let's put this into perspective with real numbers:

- `-log(0.1) = 2.303`
- `-log(0.01) = 4.605`
- `-log(0.001) = 6.908`

A prediction of `0.01` gets almost double the penalty of a prediction of `0.1`, and a prediction of `0.001` gets three times the penalty. Every time the predicted probability shrinks by a factor of 10, the penalty goes up by a fixed amount (about `2.303`).

Here is the deeper reason why `log` is the right tool:

- `1 - p` is linear and capped at 1. Even a confidently wrong prediction of `p = 0.01` gets a penalty of only `0.99`.
- `-log(p)` is unbounded as p approaches 0. A confidently wrong prediction of `p = 0.001` gets a penalty of `6.908`, and the penalty keeps growing without limit as `p` gets smaller.

This is exactly what we want - the model should be strongly discouraged from being confidently wrong.

Why negative?

The log of any number between 0 and 1 is always negative. Since loss should be a positive number (lower is better), we put a negative sign in front to flip it. So:

- `p = 0.9` -> `-log(0.9) = 0.105` (small loss, good prediction)
- `p = 0.1` -> `-log(0.1) = 2.303` (large loss, bad prediction)
- `p = 1.0` -> `-log(1.0) = 0` (zero loss, perfect prediction)
- `p` close to `0` -> `-log(p)` close to `infinity` (huge loss, the forecaster said "0% chance of rain" and it rained)

This is how cross-entropy gives a clean, well-behaved loss value that is small when we are right and large when we are wrong.

## Binary Cross-Entropy Loss

Now, let's look at the simplest case - when we have only two classes (e.g. spam or not spam, cat or dog, rain or no rain). This is the exact setting of our forecaster analogy when she only predicts "rain" or "no rain".

In this case, the true label `y` is either `0` or `1`, and the predicted probability `p` is a single number between `0` and `1` (usually the output of a sigmoid function).

The formula is:

```
BCE = - [ y * log(p) + (1 - y) * log(1 - p) ]

```

Here, only one of the two terms is active at a time:

- If `y = 1`: only `-log(p)` is active. We want `p` to be close to 1.
- If `y = 0`: only `-log(1 - p)` is active. We want `p` to be close to 0.

Let's see with an example. Suppose the true label is `y = 1` and the model predicts `p = 0.8`:

```
BCE = - [ 1 * log(0.8) + 0 * log(0.2) ]
    = - log(0.8)
    = 0.223

```

Now suppose the true label is `y = 1` but the model predicts `p = 0.2`:

```
BCE = - [ 1 * log(0.2) + 0 * log(0.8) ]
    = - log(0.2)
    = 1.609

```

The second prediction is punished with a much larger loss. It works perfectly.

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

## Categorical Cross-Entropy Loss

Now, let's move to the case with multiple classes (e.g. classifying an image as cat, dog, rabbit, or bird).

In this case, the true label is a one-hot vector. A one-hot vector is just a list of zeros with a single `1` at the position of the correct class. If we want to understand one-hot encoding in detail, we can watch this video on one-hot encoding. For example, if the true class is "dog" out of [cat, dog, rabbit, bird], the true label is:

```
y = [0, 1, 0, 0]

```

The model outputs a probability distribution over all classes, usually by applying a softmax function on top of the raw scores (also called logits). Let's say the model predicts:

```
p = [0.2, 0.7, 0.05, 0.05]

```

The categorical cross-entropy is:

```
CE = - sum [ y_i * log(p_i) ]
   = - [ 0 * log(0.2) + 1 * log(0.7) + 0 * log(0.05) + 0 * log(0.05) ]
   = - log(0.7)
   = 0.357

```

Since the true label is one-hot, only the term for the correct class survives. So the formula reduces to `- log(p_correct)`.

To master cross-entropy, loss functions, and logits in depth, check out our AI and Machine Learning Program at Outcome School.

## Step-by-Step Numeric Example

Let's put this into perspective with real numbers. Suppose we have a classification problem with 3 classes: cat, dog, rabbit. The true label is dog, so the one-hot true vector is:

```
y = [0, 1, 0]

```

Our model produces the following raw scores (logits) for an input image:

```
z = [2.0, 3.0, 1.0]

```

Step 1: Apply softmax to convert logits into probabilities.

The softmax formula is:

```
p_i = exp(z_i) / sum of exp(z_j) over all j

```

Let's compute each exponent:

- `exp(2.0) = 7.389`
- `exp(3.0) = 20.086`
- `exp(1.0) = 2.718`

The sum is: `7.389 + 20.086 + 2.718 = 30.193`

So the probabilities are:

- `p_cat = 7.389 / 30.193 = 0.2447`
- `p_dog = 20.086 / 30.193 = 0.6652`
- `p_rabbit = 2.718 / 30.193 = 0.0900`

We are rounding intermediate values to 4 decimal places for clarity.

Step 2: Compute the cross-entropy loss.

Since the true class is dog, we only care about `p_dog`:

```
CE = - log(p_dog)
   = - log(0.6652)
   = 0.4076

```

So the cross-entropy loss for this prediction is approximately `0.4076`. The model said "66% chance it's a dog" and it was a dog - a decent but not great forecast.

Step 3: Let's see what happens if the model is more confident.

Suppose the logits become:

```
z = [1.0, 5.0, 0.5]

```

- `exp(1.0) = 2.718`
- `exp(5.0) = 148.413`
- `exp(0.5) = 1.649`

Sum: `2.718 + 148.413 + 1.649 = 152.780`

- `p_cat = 2.718 / 152.780 = 0.0178`
- `p_dog = 148.413 / 152.780 = 0.9714`
- `p_rabbit = 1.649 / 152.780 = 0.0108`

Now the loss is:

```
CE = - log(0.9714) = 0.0290

```

The loss dropped from `0.4076` to `0.0290`. The more confident and correct the model is, the smaller the loss. This is the beauty of cross-entropy. Our forecaster just got better - she said "97% chance of what actually happened" and barely got penalized.

Step 4: Let's see what happens if the model is confidently wrong.

Suppose the logits are:

```
z = [5.0, 1.0, 0.5]

```

- `exp(5.0) = 148.413`
- `exp(1.0) = 2.718`
- `exp(0.5) = 1.649`

Sum: `148.413 + 2.718 + 1.649 = 152.780`

- `p_cat = 148.413 / 152.780 = 0.9714`
- `p_dog = 2.718 / 152.780 = 0.0178`
- `p_rabbit = 1.649 / 152.780 = 0.0108`

The loss is:

```
CE = - log(0.0178) = 4.029

```

Here, the loss jumped from `0.4076` to a huge `4.029`. The model was confidently predicting "cat" when the true answer was "dog", so cross-entropy punishes it heavily. This is exactly the behavior we want. Coming back to our forecaster analogy, this is the forecaster who said "97% sunshine" on a day it rained - a big penalty.

Note: In practice, deep learning frameworks like PyTorch and TensorFlow do not compute softmax and cross-entropy as two separate steps. They fuse them into a single numerically stable function (e.g. `CrossEntropyLoss` in PyTorch, `softmax_cross_entropy_with_logits` in TensorFlow). The reason is that computing `exp(z)` for large logits can overflow, and computing `log` on very small probabilities can underflow. The fused version applies the `log-sum-exp` trick to avoid both problems. So in real code, we pass the raw logits directly, not the softmax output.

## Cross-Entropy Loss for Language Models

Now, let's take a real use-case in modern AI. In large language models like GPT, which are built on the Transformer architecture, the model predicts the next token from a vocabulary of tens of thousands of tokens (often 50,000+).

At each position in the sequence, the model outputs a probability distribution over the entire vocabulary. The true label is the actual next token (represented as a one-hot vector of size 50,000+).

For a single token prediction:

```
CE = - log(p_actual_next_token)

```

For a full sequence of `N` tokens, we compute the loss at every position and take the average:

```
Total Loss = (1 / N) * sum over all positions of [ - log(p_actual_next_token) ]

```

For example, if the sentence is "The cat sat on the mat" and the model is predicting each next token, we compute `- log(p)` for each correct token ("cat", "sat", "on", "the", "mat") and average them.

This average cross-entropy loss is also closely related to another famous metric called Perplexity, which is simply `exp(average cross-entropy)`. A lower cross-entropy means a lower perplexity, which means a better language model. If we want to go deeper into the attention math that produces those next-token probabilities in the first place, we can read our blog on Math Behind Attention - Q, K, V.

If we want to go deep into LLM fundamentals, the Transformer architecture, and how language models are trained end to end, we have a complete program - check out our AI and Machine Learning Program at Outcome School.

## The Gradient of Cross-Entropy Loss

Now, let's understand why cross-entropy is the go-to loss function when combined with softmax.

The gradient of cross-entropy loss with respect to the logits `z` has a remarkably simple form:

```
dCE / dz_i = p_i - y_i

```

This means the gradient is just `predicted probability - true label`. That is it.

Let's see what this means with our earlier example. With `p = [0.2447, 0.6652, 0.0900]` and `y = [0, 1, 0]`:

```
Gradient = [0.2447 - 0, 0.6652 - 1, 0.0900 - 0]
         = [0.2447, -0.3348, 0.0900]

```

Here, we can see that:

- The gradient for cat is positive (`0.2447`), so the model will reduce the score for cat.
- The gradient for dog is negative (`-0.3348`), so the model will increase the score for dog.
- The gradient for rabbit is positive (`0.0900`), so the model will reduce the score for rabbit.

This is exactly what we want. The gradient naturally pushes the model to assign higher probability to the correct class and lower probability to the wrong classes.

The fact that the gradient is this clean makes cross-entropy extremely efficient to train with. There is no messy chain rule explosion, no vanishing gradients from the loss itself. This is why softmax + cross-entropy is the default pairing for classification in almost every deep learning framework.

This `p_i - y_i` is the starting point of backpropagation - the gradient that then flows backward through every layer of the network to update all the weights. We have a detailed blog on Math Behind Backpropagation that explains this end-to-end flow step by step.

## Quick Summary

Let's recap what we have decoded:

- Cross-Entropy Loss measures how different the predicted probability distribution is from the true distribution. Think of it as the scoring system for our weather forecaster.
- Formula:`CE = - sum [ y_i * log(p_i) ]`. For one-hot labels, this simplifies to `CE = - log(p_correct)`.
- Why log: It punishes confidently wrong predictions much more than slightly wrong ones.
- Why negative: The log of a probability is always negative, so we flip it to get a positive loss value.
- Binary Cross-Entropy is used for two-class problems and uses the sigmoid output.
- Categorical Cross-Entropy is used for multi-class problems and uses the softmax output.
- In language models, cross-entropy is computed at every token position and averaged over the sequence. It is tightly connected to Perplexity.
- Gradient:`dCE / dz_i = p_i - y_i`. This clean form is one of the main reasons cross-entropy is the default loss for classification.
- In real code, frameworks fuse softmax and cross-entropy into a single numerically stable op. We pass raw logits in, not probabilities.

This is how cross-entropy loss works. Now, we have understood the math behind Cross-Entropy Loss. It is the simple idea of measuring `- log(probability of the correct answer)` that drives the training of almost every classification model we use today.

### Should we pass softmax probabilities or raw logits to the loss function in PyTorch?

We should pass the raw logits. Frameworks like PyTorch and TensorFlow fuse softmax and cross-entropy into a single numerically stable function. Computing `exp(z)` for large logits can overflow, and computing `log` on very small probabilities can underflow. The fused version uses the log-sum-exp trick to avoid both problems.

### Why not use 1 - p as the loss instead of the negative log?

Because `1 - p` is linear and capped at 1. Even a confidently wrong prediction of `p = 0.01` gets a penalty of only `0.99`. The negative log is unbounded as `p` approaches 0, so it strongly discourages the model from being confidently wrong.

### When should we use Binary Cross-Entropy instead of Categorical Cross-Entropy?

We use Binary Cross-Entropy for two-class problems, like spam or not spam, where the prediction usually comes from a sigmoid output. We use Categorical Cross-Entropy for multi-class problems, like cat, dog, rabbit, or bird, where the prediction comes from a softmax output and the true label is a one-hot vector.

### Can the cross-entropy loss be zero?

Yes. If the model assigns a probability of 1.0 to the correct class, the loss is `-log(1.0)`, which is 0. This is a perfect prediction. As the probability of the correct class moves close to 0, the loss moves close to infinity.

### How is cross-entropy related to perplexity?

Perplexity is simply the exponential of the average cross-entropy. In language models, cross-entropy is computed at every token position and averaged over the sequence. A lower cross-entropy means a lower perplexity, which means a better language model.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-304 and 719-1175 of 1175; 414 middle lines (29.4KB) elided. Read artifact://70 for full output]
