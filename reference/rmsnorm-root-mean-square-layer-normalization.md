> Source: https://outcomeschool.com/blog/rmsnorm-root-mean-square-layer-normalization

# What is RMSNorm? Root Mean Square Layer Normalization Explained
URL: https://outcomeschool.com/blog/rmsnorm-root-mean-square-layer-normalization
Published: 2026-04-25

What is RMSNorm? Root Mean Square Layer Normalization Explained

# What is RMSNorm? Root Mean Square Layer Normalization Explained

Authors
: - Name
: Amit Shekhar
Published on
: April 24, 2026

RMSNorm (Root Mean Square Normalization) is a simpler and faster version of Layer Normalization that keeps only the re-scaling step and drops the re-centering step. It powers most modern Large Language Models.

In this blog, we will learn about RMSNorm, a faster and simpler alternative to Layer Normalization that powers most modern Large Language Models like Llama, Mistral, Gemma, Qwen, PaLM, and DeepSeek.

Our goal is to decode RMSNorm so clearly that by the end, we will be able to explain how it works to anyone.

We will cover the following:

- Why normalization is needed in deep networks
- A quick recap of Layer Normalization (LayerNorm)
- What RMSNorm is and how it works
- The math behind RMSNorm with a concrete numeric example
- LayerNorm vs RMSNorm - the key differences
- Why modern LLMs prefer RMSNorm
- A code example
- Where RMSNorm fits in a Transformer
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

Neural networks like LLMs stack many layers on top of each other. As numbers flow through these layers, they can become very big or very small. This makes training slow and unstable.

To fix this, we scale the numbers at each layer to keep them in a healthy range. This scaling step is called normalization.

In simple words:

RMSNorm = A simpler and faster way to normalize numbers inside a neural network.

Instead of centering and scaling the numbers (like LayerNorm does), RMSNorm just scales them using their root mean square value. Same stabilizing effect, less work.

## Why Do We Need Normalization?

Let's say we have a deep neural network with 100 layers. At each layer, numbers get multiplied by weights, added together, and passed through activation functions.

Here is the problem. After many layers, these numbers can:

- Become very large - during training, this causes the exploding gradient problem
- Become very small - during training, this causes the vanishing gradient problem

When this happens, the network becomes unstable. Training slows down. Sometimes it does not learn at all.

So, here comes normalization to the rescue. Normalization keeps the numbers at each layer in a stable, healthy range - not too big, not too small. This makes training faster and more stable.

## A Quick Recap of Layer Normalization

Before jumping into RMSNorm, we must quickly recall how Layer Normalization (LayerNorm) works, because RMSNorm is a simplification of it.

LayerNorm takes a vector of numbers and does two things:

Step 1: Re-center. Subtract the mean so the numbers are centered around zero.

Step 2: Re-scale. Divide by the standard deviation so the numbers have a consistent spread.

Then it applies two learned parameters - `gamma` and `beta` - to allow the network to adjust the output if needed.

The formula is:

```
LayerNorm(x) = gamma * (x - mean) / sqrt(variance + eps) + beta

```

Here:

- `mean` is the average of the values in the vector
- `variance` is how spread out the values are
- `eps` is a tiny number to avoid division by zero
- `gamma` and `beta` are learned parameters

LayerNorm works very well. It was used in the original Transformer paper. But there is one question researchers asked:

> Do we really need both steps, re-centering and re-scaling? Or is one of them enough?

This question led to RMSNorm.

## What Is RMSNorm?

RMSNorm (Root Mean Square Normalization) is a simpler version of LayerNorm that keeps only the re-scaling step and drops the re-centering step.

In simple words:

RMSNorm = LayerNorm with only the re-scaling step.

It was introduced in 2019 by Biao Zhang and Rico Sennrich in their paper "Root Mean Square Layer Normalization".

The key insight was this:

> Most of the benefit of LayerNorm comes from the re-scaling step, not from the re-centering step.

So, if we skip the mean subtraction, we save computation without losing accuracy.

Here is a mental model that sticks:

LayerNorm controls both shift and scale. RMSNorm controls only scale - and that turns out to be enough.

Now, a natural question arises - if we do not re-center the values, how does the network handle mean shifts? The answer is that Transformers have residual connections and learned projections all over the place. These can absorb mean shifts on their own. So the network does not need normalization to do that job for it. The scale is the part that really needs a dedicated fix, which is why RMSNorm is enough in practice.

Let's see exactly how it works.

## The Math Behind RMSNorm

RMSNorm uses the Root Mean Square (RMS) of the input vector to scale the values.

We do three things, in order:

Step 1: Square each value in the vector.

Step 2: Take the mean (average) of those squared values.

Step 3: Take the square root of that mean.

That is it. The result is the RMS value.

Intuitively, the RMS value tells us the typical magnitude of the numbers in the vector. A vector like `[100, 200, 300]` has a large RMS. A vector like `[0.01, 0.02, 0.03]` has a tiny RMS. By dividing each value by the RMS, we strip away the overall size and keep only the relative shape. That is exactly what we want from normalization.

The formula is:

```
RMS(x) = sqrt( (x1^2 + x2^2 + ... + xn^2) / n )

```

Where `n` is the number of values in the vector.

Once we have the RMS, the RMSNorm formula is:

```
RMSNorm(x) = gamma * x / RMS(x)

```

Here:

- `x` is the input vector
- `RMS(x)` is the root mean square of the vector
- `gamma` is a learned parameter (one per dimension)

Why do we need `gamma` at all? Because dividing by the RMS forces every vector to a fixed magnitude, which is too restrictive. `gamma` gives the network a knob to stretch or shrink each dimension back to whatever scale is actually useful for the task. So normalization stabilizes training, and `gamma` makes sure we do not lose expressiveness along the way.

In practice, we add a tiny number `eps` inside the square root to avoid division by zero:

```
RMSNorm(x) = gamma * x / sqrt( mean(x^2) + eps )

```

Notice there is no `beta` in RMSNorm. We do not need to shift the output because we never subtracted the mean in the first place.

## Let's Put This Into Perspective With Real Numbers

Learning by example is the best way to learn.

Let's say we have an input vector with 4 values:

```
x = [2, 4, 4, 8]

```

Step 1: Square each value.

```
[2^2, 4^2, 4^2, 8^2] = [4, 16, 16, 64]

```

Step 2: Take the mean of the squares.

```
mean = (4 + 16 + 16 + 64) / 4 = 100 / 4 = 25

```

Step 3: Take the square root.

```
RMS(x) = sqrt(25) = 5

```

Step 4: Divide each input value by the RMS.

```
x / RMS(x) = [2/5, 4/5, 4/5, 8/5] = [0.4, 0.8, 0.8, 1.6]

```

Step 5: Multiply by gamma. For the sake of understanding, let's assume gamma is `[1, 1, 1, 1]`.

```
RMSNorm(x) = [0.4, 0.8, 0.8, 1.6]

```

The numbers are now scaled to a healthy range. That is all RMSNorm does.

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

## LayerNorm vs RMSNorm - The Key Differences

Let me tabulate the differences between LayerNorm and RMSNorm for your better understanding.

| LayerNorm | RMSNorm |
| --- | --- |
| Re-centers (subtracts mean) and re-scales (divides by std) | Only re-scales (divides by RMS) |
| Has two learned parameters: `gamma` and `beta` | Has one learned parameter: `gamma` |
| Slower - computes both mean and variance | Faster - only computes the RMS |
| Used in the original Transformer, BERT, GPT-2 | Used in Llama, Mistral, Gemma, Qwen, PaLM, DeepSeek |

To see the difference visually, here are the two pipelines side by side:

```
LayerNorm:

  x  -->  [ subtract mean ]  -->  [ divide by std ]  -->  [ * gamma + beta ]  -->  output

RMSNorm:

  x  -->  [    skipped     ]  -->  [ divide by RMS ]  -->  [    * gamma     ]  -->  output
              ^^^^^^^                                            ^^^^^^^
        re-centering step                                     no beta,
            removed                                        one parameter

```

Here, we can see that RMSNorm drops the mean subtraction step completely and also drops the `beta` parameter. Everything else follows the same idea as LayerNorm.

## Why Modern LLMs Prefer RMSNorm

Now, a natural question arises - why do most modern LLMs use RMSNorm instead of LayerNorm?

The answer comes down to three reasons.

Reason 1: Speed. RMSNorm does less math than LayerNorm. It skips the mean subtraction and the variance calculation. On a small vector, this may not look like much. But LLMs have billions of parameters, trillions of tokens, and dozens to hundreds of normalization calls per forward pass (two per Transformer block, stacked across many blocks). A small saving per call adds up to a big saving overall. The original paper reported training time reductions of 7% to 64% depending on the model and task. Training becomes faster. Inference becomes faster.

Reason 2: Broadly the same accuracy. The original RMSNorm paper showed that models trained with RMSNorm reach the same accuracy as models trained with LayerNorm - sometimes slightly better, sometimes slightly worse, but broadly the same. We get the speed benefit without losing quality.

Reason 3: Simpler implementation. RMSNorm has fewer moving parts than LayerNorm. It is easier to implement and easier to reason about. With one less parameter (`beta`) and one less statistic to compute (the mean), the kernel is cleaner and easier to fuse efficiently on GPUs. This simplicity matters when we are training at the scale of trillions of tokens across thousands of GPUs.

This is why the modern LLM stack has almost completely switched to RMSNorm.

## A Code Example

Let's see the code for RMSNorm as below:

```python
import torch
import torch.nn as nn

class RMSNorm(nn.Module):
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.gamma = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        # Square each value and take the mean along the last dimension
        mean_square = x.pow(2).mean(dim=-1, keepdim=True)
        # Take the square root to get RMS (eps added for stability)
        rms = torch.sqrt(mean_square + self.eps)
        # Scale the input: divide by RMS and multiply by gamma
        return self.gamma * x / rms

```

Here, we can see that:

- We only have one learned parameter - `gamma`. There is no `beta`.
- We compute the mean of the squared values along the last dimension.
- We take the square root of that mean to get the RMS.
- We divide the input by the RMS and multiply by `gamma`.

That is the entire implementation. It is very simple.

## Where RMSNorm Fits in a Transformer

In a modern LLM like Llama, RMSNorm is applied at two places inside each Transformer block:

- Before the attention block
- Before the feed-forward block

This style is called pre-norm, which means we normalize the input first, then pass it through the attention or feed-forward layer. Pre-norm helps training stability in very deep networks, which is why almost all modern LLMs use it.

Here is how one Transformer block looks with pre-norm RMSNorm:

```
              input x
                 |
      +----------+              <- residual path
      |          v
      |      [ RMSNorm ]
      |          |
      |          v
      |      [ Attention ]
      |          |
      +--------> (+)
                 |
      +----------+              <- residual path
      |          v
      |      [ RMSNorm ]
      |          |
      |          v
      |       [ FFN ]
      |          |
      +--------> (+)
                 |
                 v
              output

```

Here, we can see that each RMSNorm sits before the heavy layer (Attention or FFN), not after. The residual path skips around the whole block so the original input can flow through untouched.

One additional RMSNorm is also applied at the very end of the model, right before the final output projection. This last normalization keeps the hidden state in a stable range before it gets projected into logits.

We have a detailed blog on Transformer Architecture that explains where normalization fits in the overall flow.

## Quick Summary

Let's recap what we have learned:

- Normalization keeps the numbers flowing through a deep network in a healthy range, which makes training faster and more stable.
- LayerNorm does two things - it re-centers the values (subtracts the mean) and re-scales them (divides by standard deviation).
- RMSNorm keeps only the re-scaling step. It divides the input by its Root Mean Square value.
- Root Mean Square is exactly what the name says - the square root of the mean of the squares.
- RMSNorm is faster than LayerNorm because it skips the mean subtraction and the variance calculation.
- Accuracy is broadly the same. The original paper showed RMSNorm matches LayerNorm on quality - sometimes slightly better, sometimes slightly worse. We get the speed benefit essentially for free.
- Modern LLMs like Llama, Mistral, Gemma, Qwen, PaLM, and DeepSeek all use RMSNorm.
- Only one learned parameter - `gamma`. It has one value per dimension of the vector. There is no `beta` in RMSNorm.

We have learnt how RMSNorm works, why it is faster than LayerNorm, and why most modern LLMs have adopted it.

### Is RMSNorm less accurate than LayerNorm?

No. The original RMSNorm paper showed that models trained with RMSNorm reach broadly the same accuracy as models trained with LayerNorm, sometimes slightly better and sometimes slightly worse. So we get the speed benefit without losing quality.

### How does a Transformer handle mean shifts if RMSNorm does not re-center?

Transformers have residual connections and learned projections all over the place, and these can absorb mean shifts on their own. So the network does not need normalization to do that job. The scale is the part that really needs a dedicated fix, which is why RMSNorm is enough in practice.

### Why does RMSNorm not have a beta parameter?

RMSNorm does not need `beta` because it never subtracts the mean in the first place, so there is nothing to shift back. It keeps only one learned parameter, `gamma`, with one value per dimension. This lets the network stretch or shrink each dimension to a useful scale.

### What is eps used for in RMSNorm?

The `eps` value is a tiny number added inside the square root to avoid division by zero. So the formula in practice becomes `gamma * x / sqrt(mean(x^2) + eps)`. In the code example, `eps` defaults to `1e-6`.

### Who introduced RMSNorm?

RMSNorm was introduced in 2019 by Biao Zhang and Rico Sennrich in their paper "Root Mean Square Layer Normalization". Their key insight was that most of the benefit of LayerNorm comes from the re-scaling step, not from the re-centering step.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# What is Paged Attention in LLMs and How Does It Work?
URL: https://outcomeschool.com/blog/paged-attention-in-llms
Published: 2026-03-29
Author: Amit Shekhar

What is Paged Attention in LLMs and How Does It Work?

# What is Paged Attention in LLMs and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: March 29, 2026

Paged Attention is a technique that manages the KV Cache memory more efficiently by breaking it into small, fixed-size blocks called pages. This removes the memory waste and lets LLMs serve many more users at the same time.

In this blog, we will learn about Paged Attention, a technique that solves the memory waste problem of KV Cache, allowing LLMs to serve many more users at the same time.

We will start with a quick recap of KV Cache, understand the memory problem it creates, see how traditional memory allocation wastes space through an example, and then walk through how Paged Attention solves this problem by borrowing an idea from how computers manage memory.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## Quick Recap: KV Cache

When an LLM generates text, it predicts one token at a time. A token is a small piece of text. It can be a word, part of a word, or even a single character.

At each step, the model computes a Key and a Value for the new token and needs the Keys and Values of all previous tokens.

Without KV Cache, the model would recompute the Key and Value for every previous token at every step, wasting computation. KV Cache solves this by storing the Key and Value of each token after it is computed, so they can be reused in future steps.

KV Cache makes text generation much faster. But it comes with a trade-off: it uses memory to store all those Keys and Values.

Now, let's understand the memory problem this creates.

## The Problem: Memory Waste in KV Cache

When a user sends a request to an LLM, the system needs to set aside memory for the KV Cache of that request. But here is the challenge: the system does not know in advance how long the response will be.

A user can ask a simple question that results in a 20-token response, or a complex question that results in a 2,000-token response. The system has no way of knowing upfront.

In the traditional approach, the system reserves one large block of memory for each request - where all the slots are right next to each other - enough to handle the maximum possible response length. This means reserving memory for, say, 2,048 tokens, even if the actual response turns out to be only 50 tokens.

Let's understand this with an analogy.

### The Hotel Analogy

Imagine a hotel where guests check in but do not know how many nights they will stay. Some will stay 1 night, some will stay 30 nights.

Traditional approach: When a guest checks in, the hotel reserves 30 rooms in a row on the same floor, just in case the guest stays for 30 nights. Even if the guest stays for only 2 nights, all 30 rooms remain reserved and cannot be given to anyone else.

Now imagine 10 guests check in. The hotel reserves 30 × 10 = 300 rooms in a row. But if most guests stay only a few nights, hundreds of rooms sit empty and wasted.

This is exactly what happens with KV Cache memory in the traditional approach.

The waste shows up in two ways:

1. Internal waste: Memory is reserved but never used. If a request only generates 50 tokens but memory was reserved for 2,048 tokens, the remaining space for 1,998 tokens is wasted.
2. External waste: Because memory must be allocated in one large block with all slots next to each other, small gaps of free memory scattered around cannot be used, even if together they would be enough to serve a new request.

This memory waste is a serious problem. A large portion of the reserved memory is never actually used.

Because memory is limited, this waste means the system can serve fewer users at the same time. If the system could use memory more efficiently, it could handle many more requests simultaneously.

This is the problem that Paged Attention solves.

## What is Paged Attention?

[…628ln elided…]

## Quick Summary

Let's recap what we have learned.

- RLHF stands for Reinforcement Learning from Human Feedback. It is the technique that aligns a pre-trained LLM with what humans actually want.
- RLHF = SFT + Reward Model + RL Fine-Tuning.
- Stage 1: SFT teaches the base model to follow instructions using human-written prompt-response pairs.
- Stage 2: Reward Model is trained on pairs of responses where humans picked the better one. It learns to score any response the way a human would.
- Stage 3: RL Fine-Tuning uses PPO to update the LLM so its responses earn higher scores from the Reward Model.
- The KL penalty keeps the LLM close to the SFT model and prevents it from drifting into nonsense.
- Reward hacking is the model finding tricks that fool the Reward Model. Good labeling, KL penalty, and iteration are the main defenses.
- Common mistakes include skipping SFT, using a weak Reward Model, ignoring the KL penalty, and treating the Reward Model as ground truth.
- Best practices are strong SFT, high-quality preference data, careful KL tuning, iterative rounds, real human evaluation beyond the reward score, and balanced safety plus helpfulness data.

This is how RLHF turns a raw pre-trained LLM into a helpful, honest, and safe assistant.

### Why does RLHF ask humans to compare answers instead of writing perfect ones?

Humans are much better at comparing two answers than at writing the perfect answer from scratch. We also cannot write enough examples to cover every possible question and nuance. So, RLHF turns simple judgments like "Answer A is better than Answer B" into a training signal for the model.

### How many models are involved in RLHF with PPO?

Four models work together. The Policy Model is the LLM being trained. The Value Model, or Critic, predicts expected rewards to compute the advantage. The Reward Model scores responses based on human preferences, and the Reference Model is a frozen copy of the SFT model, used for the KL penalty.

### Is PPO the only way to do the RL stage of RLHF?

No. PPO is the most commonly used algorithm, but newer algorithms like GRPO remove the Value Model entirely by computing the baseline from a group of sampled responses, bringing

# What is a Vision Transformer (ViT) and How Does It Work?
URL: https://outcomeschool.com/blog/decoding-vision-transformer-vit
Published: 2026-04-15
Author: Amit Shekhar

What is a Vision Transformer (ViT) and How Does It Work?

# What is a Vision Transformer (ViT) and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: April 15, 2026

A Vision Transformer (ViT) treats an image the same way a transformer treats a sentence. It splits the image into small patches, treats each patch as a token, and processes them with a transformer to classify the image.

In this blog, we will learn about the Vision Transformer (ViT) by decoding how it splits an image into patches, turns those patches into tokens, and processes them with a transformer to classify the image.

Before Vision Transformers, image classification was dominated by Convolutional Neural Networks (CNNs) like ResNet, VGG, and etc. The transformer architecture was only used for text. Then, in 2020, Google researchers asked a simple question - "Can we apply the transformer architecture directly to images?" The answer was yes, and the Vision Transformer (ViT) was born in the paper titled "An Image is Worth 16x16 Words".

When we hear "applying transformers to images", it sounds complex. But do not worry. If we break it down into its individual parts, every single piece is simple.

Our goal is to decode ViT so clearly that by the end, we will be able to explain how ViT works to anyone.

We will cover the following:

- The Big Picture
- Decoding Step 1: Splitting the Image into Patches
- Decoding Step 2: Patch Embedding
- Decoding Step 3: The CLS Token
- Decoding Step 4: Position Embeddings
- Decoding Step 5: The Transformer Encoder
- Decoding Step 6: The Classification Head
- Putting It All Together
- ViT vs CNN
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

ViT treats an image the same way a transformer treats a sentence. A sentence is a sequence of words (tokens). ViT splits an image into a sequence of small patches and treats each patch as a token. These patch tokens are then processed by a standard transformer encoder, just like text tokens.

In simple words:

Vision Transformer = Split image into patches (like words) + Process patches with a transformer (like processing a sentence).

Think of a jigsaw puzzle. We take a complete image, cut it into small square pieces, line up the pieces in a row, and hand them to the transformer. The transformer then looks at all the pieces together, understands how they relate to each other, and tells us what the image is.

The idea behind ViT is simple - if transformers work well for sequences of text tokens, they should also work for sequences of image patches.

A sentence like "the cat sat on the mat" is a sequence of 6 tokens. In the same way, an image becomes a sequence of patches. For example, a 224x224 image cut into 16x16 patches gives us 196 patches. Each patch is treated as a "visual word". The transformer does not care whether the tokens are words or image patches. It just processes the sequence and learns the relationships.

Now, let's decode ViT step by step.

## Decoding Step 1: Splitting the Image into Patches

The first thing ViT does is split the input image into small non-overlapping square patches.

First, we take the input image. A standard ViT uses 224x224 pixel images. Then, we divide the image into non-overlapping square patches, each of size 16x16 pixels. Since 224 / 16 = 14, we get 14 patches along each side of the image. So the image becomes a 14 x 14 grid of patches, which gives us 14 x 14 = 196 patches in total.

Think of it like a chessboard, but with 14 rows and 14 columns instead of 8. Each square of this 14 x 14 board is one patch.

Now, a natural question arises - why 16x16? It is a sweet spot. Smaller patches (say 8x8) give us more tokens and finer detail, but the sequence length grows quickly and self-attention becomes very expensive. Bigger patches (say 32x32) give us fewer tokens and faster training, but the model loses fine-grained detail. 16x16 balances both, and that is why it became the default.

```
Original Image (224 x 224 pixels)
+----+----+----+----+----+ ... +----+
|P1  |P2  |P3  |P4  |P5  |     |P14 |
+----+----+----+----+----+ ... +----+
|P15 |P16 |P17 |P18 |P19 |     |P28 |
+----+----+----+----+----+ ... +----+
|    |    |    |    |    |     |    |
  ...  ...  ...  ...  ...       ...
+----+----+----+----+----+ ... +----+
|P183|P184|P185|P186|P187|     |P196|
+----+----+----+----+----+ ... +----+

Each patch is 16 x 16 pixels
Total: 14 x 14 = 196 patches

```

Each patch captures a small region of the image. Some patches contain parts of the main object, some contain background, and some contain edges or textures.

This is how the image is broken down into a sequence. Now, let's move to the next step.

## Decoding Step 2: Patch Embedding

Now, we have 196 patches. But the transformer does not understand raw pixels. It expects each token to be a fixed-size vector of numbers, called an embedding.

Each patch is a 16x16 pixel region with 3 color channels (RGB). So each patch is a small 3D block of 16 x 16 x 3 = 768 numbers, which is then flattened into a single vector of 768 numbers.

To turn each patch into a token that the transformer can process, we use a linear projection - a simple matrix multiplication that converts these 768 numbers into a vector of a fixed dimension (768 for ViT-Base). Even though the input and output dimensions are the same here, this is not an identity mapping. The projection matrix is learned during training so that the output embedding captures the useful visual features of the patch, not just raw pixel values.

```
Patch (16 x 16 x 3, a 3D block of pixels)
        |
        v
[Flatten into a 768-dimensional vector]
        |
        v
[Linear Projection (768 -> 768)]
        |
        v
Patch Embedding (768-dimensional vector)

```

In practice, this linear projection is implemented as a convolution with kernel size 16x16 and stride 16. Do not worry if this sounds heavy. It is just an implementation detail, not a new concept - it is mathematically the same as cutting the image into 16x16 patches and projecting each one.

After this step, we have 196 patch embeddings, each of dimension 768. This is our sequence of "visual tokens", ready for the transformer.

This was all about converting patches to embeddings. Now, let's decode the next piece.

## Decoding Step 3: The CLS Token

Now, a natural question arises - once the transformer has processed all 196 patch tokens, which token do we use to make the final prediction? Each patch only sees a small part of the image, so no single patch token fully represents the whole image.

The answer is simple: we add a special learnable token called the CLS token (short for "classification token") to the beginning of the sequence.

```
Sequence: [CLS, Patch1, Patch2, Patch3, ..., Patch196]
Total tokens: 197 (1 CLS + 196 patches)

```

The CLS token does not correspond to any image patch. It starts as a learnable vector of 768 numbers. As the transformer processes the sequence, the CLS token attends to every patch and gathers information from all of them. By the end of the transformer, the CLS token contains a global summary of the entire image.

Think of the CLS token as a class representative. Every patch is like a student in a classroom. The CLS token listens to all the students, collects their information, and speaks on behalf of the whole class when the final answer is needed.

Now, let's decode the next piece.

## Decoding Step 4: Position Embeddings

Here is the catch. When we split the image into patches and line them up as a sequence, the patches lose their spatial position. The transformer only sees a list of tokens. It does not know which patch was on the top-left and which was on the bottom-right.

But the position of a patch matters. A patch containing an eye on the top of the image and a patch containing a tail on the bottom together tell us it is a cat. If we shuffle the patches randomly, the image no longer makes sense.

So, here comes the position embedding to the rescue. For each position in the sequence (0 to 196), we add a learnable vector of 768 numbers. This vector acts like a tag that tells the transformer, "This patch came from position 5 in the original image."

```
Final input = Patch Embedding + Position Embedding

Token 0:   CLS_embedding      + Position_0
Token 1:   Patch1_embedding   + Position_1
Token 2:   Patch2_embedding   + Position_2
...
Token 196: Patch196_embedding + Position_196

```

The position embedding is simply added (element-wise) to the patch embedding. Now every token carries both "what" the patch looks like and "where" it was in the image.

Now, our sequence of 197 tokens is ready for the transformer. Let's move to the next step.

## Decoding Step 5: The Transformer Encoder

The sequence of 197 tokens (CLS + 196 patches) is passed through a standard transformer encoder. We must be knowing how a transformer encoder works from text models - the same one comes into the picture here.

We have a detailed blog on Decoding Transformer Architecture that explains the transformer encoder in depth.

The encoder consists of multiple layers, and each layer contains three main components.

1. Multi-Head Self-Attention: Each token attends to every other token. This allows the model to learn relationships between different parts of the image. For example, a patch containing a cat's ear can attend to a patch containing a cat's eye, helping the model understand that they belong to the same object. This is the heart of ViT.

2. Feed-Forward Network: A two-layer neural network applied to each token independently. This adds non-linearity and increases the model's capacity. We have a detailed blog on Feed-Forward Networks in LLMs that explains this in depth.

3. Layer Normalization and Residual Connections: Standard transformer components that help with training stability.

```
Input: 197 tokens (each 768-dimensional)
        |
        v
[Layer 1: Multi-Head Self-Attention -> Feed-Forward Network]
        |
        v
[Layer 2: Multi-Head Self-Attention -> Feed-Forward Network]
        |
        v
... (12 layers in total)
        |
        v
Output: 197 tokens (each 768-dimensional)

```

After all the layers, each token has been enriched with information from all other tokens. The CLS token, in particular, has gathered information from all 196 patches and now contains a global representation of the entire image.

This is how the transformer encoder processes our sequence of visual tokens. Now, let's move to the final step.

To learn Transformer Architecture, Multi-Head Attention, and Self-Attention in depth, check out our AI and Machine Learning Program at Outcome School.

## Decoding Step 6: The Classification Head

The final CLS token representation is passed through a classification head, which is a simple linear layer that maps the 768-dimensional vector to the number of classes.

```
CLS token output (768-dimensional)
        |
        v
[Linear Layer (768 -> 1000)]
        |
        v
Class probabilities (1000 classes)
        |
        v
Prediction: "Golden Retriever" (class with highest probability)

```

The class with the highest probability is the model's prediction. It works perfectly.

Now, we have decoded every piece of ViT. Let's put them all together to see how ViT runs end to end.

## Putting It All Together

Let's trace through the entire ViT pipeline end to end with concrete numbers for ViT-Base:

```
Input image (224 x 224 x 3 RGB)
        |
        v
[Step 1: Split into 14 x 14 = 196 patches of 16 x 16]
        |
        v
[Step 2: Patch embedding -> 196 vectors, each 768-dim]
        |
        v
[Step 3: Prepend CLS token -> 197 vectors, each 768-dim]
        |
        v
[Step 4: Add position embeddings -> 197 vectors, each 768-dim]
        |
        v
[Step 5: Transformer encoder (12 layers, 12 heads each)]
        |
        v
[Step 6: Take CLS token -> Linear (768 -> 1000)]
        |
        v
Prediction: "Golden Retriever"

```

Total parameters for ViT-Base: ~86 million.

ViT comes in three standard sizes - ViT-Base (~86M parameters, 12 layers), ViT-Large (~307M parameters, 24 layers), and ViT-Huge (~632M parameters, 32 layers). The bigger the model, the more data it needs to train well, but the better it performs once trained.

This is the complete flow of ViT from an input image to a final prediction.

A quick note for you

No matter which tech domain you work in, get familiar with these topics:

- LLM
- RAG
- MCP
- Agent
- Fine-tuning
- Quantization

We put it all together in one video:

No need to stop reading - bookmark it and watch later when you get time. Future you will thank you.

Now, let's get back to the topic.

## ViT vs CNN

Now, a natural question arises - how does ViT compare to CNNs, which have been the standard for image classification for years?

Let me tabulate the differences between ViT and CNN for your better understanding so that you can decide which one to use based on your use case.

| Property | ViT | CNN (e.g. ResNet) |
| --- | --- | --- |
| Core operation | Self-attention | Convolution |
| What each layer sees | The whole image from the very first layer | Only nearby pixels at first, more with depth |
| Built-in assumptions | Almost none, learns everything from data | Strong, assumes nearby pixels are related |
| Data requirement | Needs large datasets | Works with smaller datasets |
| Scalability | Scales well with data and compute | Scales, but less steeply at very large scale |
| Architecture | Uniform (same attention blocks) | Varied (different block types) |
| Image understanding | Understands global relationships | Understands local patterns first |

CNNs come with a built-in assumption that nearby pixels are more related than distant pixels. This assumption acts like a head start - the CNN does not have to learn this from scratch. ViT does not have this head start. It learns all spatial relationships from the data itself. This is why ViT needs more data to train well, but once trained on enough data, it can outperform CNNs because it is not limited by any built-in assumption.

Let's put this into perspective with real numbers:

- When trained only on ImageNet (~1.3 million images), ViT performs worse than a well-tuned ResNet of similar size.
- When pre-trained on JFT-300M (~300 million images) and then fine-tuned on ImageNet, ViT beats the best CNNs of the time.
- The lesson is simple - more data, more ViT wins. With small data, CNNs win because of their built-in head start.

## Quick Summary

In one line:

ViT = image patches + transformer encoder.

Let's recap what we have decoded:

- Vision Transformer (ViT) applies the transformer architecture to images by treating image patches as tokens, just like words in a sentence.
- The process is - split the image into 16x16 patches, project each patch into an embedding, add a CLS token and position embeddings, process through a transformer encoder, and use the CLS token for classification.
- Patch embedding converts each 16x16x3 patch into a 768-dimensional vector using a linear projection.
- The CLS token aggregates information from all patches and is used for the final classification.
- Position embeddings tell the transformer where each patch came from in the original image.
- The transformer encoder uses multi-head self-attention so every patch can attend to every other patch, learning global relationships from the very first layer.
- ViT vs CNN: ViT looks at the whole image from the very first layer, while CNNs look at nearby pixels first. ViT needs more data but scales better.
- ViT has become the foundation for many modern vision models, including CLIP, DINO, self-supervised methods like I-JEPA, and the vision encoders used in multimodal models.

So we have learned about the Vision Transformer (ViT), how it splits an image into patches, processes them with a transformer encoder, and uses the CLS token to make the final prediction. We have also seen how ViT compares to CNNs and why it scales so well with more data.

### Does ViT work well on small datasets?

No. ViT needs large datasets to train well. When trained only on ImageNet, which has about 1.3 million images, ViT performs worse than a well-tuned ResNet of similar size. CNNs win with small data because they assume nearby pixels are related, which gives them a head start.

### Why does ViT use 16x16 patches?

16x16 is a sweet spot between detail and cost. Smaller patches give more tokens and finer detail, but the sequence grows quickly and self-attention becomes very expensive. Bigger patches give fewer tokens and faster training, but the model loses fine-grained detail. That is why 16x16 became the default.

### Does ViT use a transformer decoder?

No. ViT uses a standard transformer encoder, the same one used for text tokens. The encoder lets every patch attend to every other patch. The final CLS token is then passed through a simple linear classification head to make the prediction.

### Does ViT know where each patch came from in the image?

Only because of position embeddings. When the patches are lined up as a sequence, they lose their spatial position, so a learnable position vector is added to each patch embedding. Without it, the transformer would not know which patch was on the top-left and which was on the bottom-right.

### Which modern models are built on ViT?

ViT has become the foundation for many modern vision models. These include CLIP, DINO, self-supervised methods like I-JEPA, and the vision encoders used in multimodal models.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-471 and 1100-1471 of 1471; 628 middle lines (31.3KB) elided. Read artifact://46 for full output]
