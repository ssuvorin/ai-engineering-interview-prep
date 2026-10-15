> Source: https://outcomeschool.com/blog/mixture-of-experts

# What is Mixture of Experts (MoE) and How Does It Work?
URL: https://outcomeschool.com/blog/mixture-of-experts
Published: 2026-04-09
Author: Amit Shekhar

What is Mixture of Experts (MoE) and How Does It Work?

# What is Mixture of Experts (MoE) and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: April 9, 2026

Mixture of Experts (MoE) is a neural network architecture that has many smaller networks called experts, and a router that activates only a few of them for each input. This makes large models faster and cheaper to run.

In this blog, we will learn about the Mixture of Experts (MoE) architecture - understanding what experts are, how the router picks them, why MoE makes large models faster and cheaper, and why it powers many of today's most powerful Large Language Models (LLMs).

When we hear "Mixture of Experts", it sounds complex. But do not worry. If we break it down into its individual parts, every single piece is simple. Our goal is to explain this architecture so clearly that by the end, we will be able to explain how Mixture of Experts works to anyone.

We will cover the following:

- Why Mixture of Experts was needed
- What an "expert" really means
- The router and how it picks experts
- Where MoE sits inside a Transformer
- Sparse activation and why it saves compute
- Load balancing across experts
- Advantages and challenges of MoE
- Why MoE powers many modern LLMs

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

A Mixture of Experts model is a special kind of neural network where, instead of using one big network for every input, the model has many smaller networks called experts and only activates a few of them for each input. A small component called the router decides which experts to use for each input.

In simple words: Mixture of Experts = Many small expert networks + A router that picks which ones to use.

Think of it like a hospital. A hospital does not have one single doctor who treats every patient. It has many specialists - a heart specialist, a skin specialist, a brain specialist, and so on. When a patient walks in, a receptionist (the router) sends them to the right specialist (the expert). The patient does not need to meet every doctor in the hospital. They only meet the ones who are relevant to their problem.

This is exactly how Mixture of Experts works inside an LLM.

## Why Was Mixture of Experts Needed?

Before MoE, large language models were dense. Dense means every token uses every single parameter of the model. If a model has 100 billion parameters, every token uses all 100 billion parameters during inference.

This had two big problems:

Problem 1: Compute cost. As models grew bigger to become smarter, the compute cost grew with them. A bigger model meant slower inference and higher GPU bills for every single token.

Problem 2: Wasted capacity. Not every input needs every part of the model. Different inputs benefit from different sub-networks, but in a dense model, every input is forced to pass through every parameter, whether it needs them or not.

So, here comes the Mixture of Experts to the rescue. It lets us build a model with a huge total number of parameters while only using a small fraction of them for each input. We get the benefits of a massive model without paying the full compute cost.

## What Is an Expert?

An expert is simply a small neural network. In most modern LLMs, each expert is a small feed-forward network - the same kind of feed-forward network we already know from the Transformer architecture.

A Transformer layer in an MoE model can have 8 experts, or 64 experts, or even 128 experts sitting side by side. Each expert is a complete feed-forward network on its own.

Note: The word "expert" can be misleading. An expert is not specially trained on math or physics. The model learns on its own which experts should handle which kinds of inputs during training. In practice, experts often specialize by low-level patterns like punctuation, word types, or token shapes, not by high-level topics. There is no manual labeling.

## The Router

Now that we have many experts sitting side by side, the next question is: how does the model decide which expert to use for each input?

This is where the router comes in. The router is a tiny neural network that looks at each input token and decides which experts should process it. In practice, the router is usually just a linear layer followed by a softmax, not a deep network.

The router works in three simple steps.

First, the router looks at the input token and produces a score for every expert. If there are 8 experts, the router produces 8 scores. The math behind it is simple: Router(x) = Softmax(x * W_router), where `x` is the input token and `W_router` is the router's learned weight matrix. The softmax is just a function that turns raw scores into probabilities that add up to 1.

Then, the router picks the `top-k` experts with the highest scores. In most MoE models, `k` = 2, meaning only the `top-2` experts are picked for each token. Some models like Switch Transformer use `k = 1`.

Finally, the token is sent only to those `top-k` experts. The other experts are completely skipped for this token.

Here is a simple visual of the router picking experts. Suppose in this example, the router picks E3 and E5:

```
                          Token
                            |
                         Router
                            |
         +------+------+----+----+------+------+
         |      |      |         |      |      |
         v      v      v         v      v      v
        E1     E2   [ E3 ]      E4   [ E5 ]   ... E8
                      |                |
                      v                v
                    Out_3            Out_5
                       \             /
                        \           /
                         \         /
                       Weighted Sum
                         (Combined)
                             |
                             v
                          Output

```

Only the picked experts run. The rest stay idle for this token. This is how MoE works at its core.

## Where Does MoE Sit Inside a Transformer?

Before we go further, let's quickly recall the structure of a Transformer layer. Each Transformer layer has two main sub-layers:

- A multi-head attention sub-layer
- A feed-forward sub-layer

In a normal (dense) Transformer, the feed-forward sub-layer is one single big network that every token passes through.

In an MoE Transformer, the feed-forward sub-layer is replaced with a Mixture of Experts. The multi-head attention sub-layer stays the same. Only the feed-forward part is replaced.

Here is a simple visual:

```
       Input to Transformer Layer
                  |
                  v
       Multi-Head Attention
                  |
                  v
                Router               (picks top-k experts)
                  |
       +----+----+----+----+----+----+----+
       |    |    |    |    |    |    |    |
       v    v    v    v    v    v    v    v
       E1   E2 [E3]   E4 [E5]   E6   E7   E8     (only top-k run)
                  |
                  v
                Output

```

So MoE does not replace the entire Transformer. It only replaces the feed-forward sub-layer inside each Transformer layer. Everything else stays the same.

Note: Not every layer has to be an MoE layer. Some MoE models alternate between dense layers and MoE layers. This is a design choice.

## Sparse Activation

This is where MoE becomes powerful. Because only a few experts run for each token, we say the model is sparsely activated.

Let's take an example. Suppose we have an MoE model with 8 experts in each layer, and the router picks the top 2 experts for each token. This means only 2 out of 8 experts run for each token. The other 6 stay idle.

Note: Each MoE layer has its own router with its own learned weights. So if a model has 32 MoE layers, it has 32 separate routers - one for each layer. Routers are not shared across layers, because each layer learns its own way of dispatching tokens to its own set of experts.

Here is a simple visual showing one router per MoE layer:

```
                          Token
                            |
                            v
              +-------------------------+
              |   Transformer Layer 1   |
              |                         |
              |   Multi-Head Attention  |
              |            |            |
              |        Router 1         |
              |            |            |
              |   E1 ..  [E3]  .. E8    |
              +------------|------------+
                           v
              +-------------------------+
              |   Transformer Layer 2   |
              |                         |
              |   Multi-Head Attention  |
              |            |            |
              |        Router 2         |
              |            |            |
              |   E1 ..  [E5]  .. E8    |
              +------------|------------+
                           v
                          ...
                           |
                           v
              +-------------------------+
              |   Transformer Layer 32  |
              |                         |
              |   Multi-Head Attention  |
              |            |            |
              |        Router 32        |
              |            |            |
              |   E1 ..  [E2]  .. E8    |
              +------------|------------+
                           v
                         Output

```

Each MoE layer has its own router and its own set of experts. The picked experts can be different at every layer.

So even though the model has the total parameters of all 8 experts, the actual compute used per token is only the compute of 2 experts. This is a huge saving.

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

## Active Parameters vs Total Parameters

MoE models are often described as having "total parameters" and "active parameters". Total parameters are the full size of the model. Active parameters are the parameters actually used per token.

Let's say each expert has 10 billion parameters. The model has a total of 80 billion parameters across all 8 experts. But for each token, only 20 billion parameters are actually used. The model behaves like a 20-billion-parameter model in terms of compute, but it carries the knowledge of an 80-billion-parameter model.

For example, Mixtral 8x7B has 8 experts and is built on top of a 7-billion-parameter base. The total size is around 47 billion parameters, but only about 13 billion are active per token. The model is fast like a 13-billion-parameter model but smart like a 47-billion-parameter model.

Note: A common confusion is "8 x 7 = 56, so why is Mixtral 47B and not 56B?". The reason is that only the feed-forward sub-layer is replicated across experts. The attention layers, embeddings, and normalization layers are shared across all experts. So the total parameters are not simply (number of experts) x (expert size).

In simple words: a big brain with a small bill.

## Load Balancing

Now, here is the catch. What if the router keeps picking the same 2 experts for every token? Then the other 6 experts never learn anything, and the model wastes its capacity.

This is a real problem in MoE training, and it is called the load imbalance problem.

To solve this, MoE models use a special technique called load balancing. During training, an extra signal called the auxiliary load balancing loss (introduced in papers like Switch Transformer and GShard) is added to the main loss. This extra loss pushes the router to spread tokens more evenly across all experts. This way, every expert gets a fair share of tokens to learn from.

Think of it like a manager in an office. If only two employees get all the work and the rest sit idle, the team is unbalanced. A good manager makes sure work is spread fairly across the team. The load balancing loss is exactly that manager for the router.

Without load balancing, MoE models collapse - only a few experts get used and the rest become dead weight. With load balancing, all experts learn useful skills and the model uses its full capacity.

There is also one more practical detail called expert capacity. Each expert can only process a fixed number of tokens per batch. If too many tokens get routed to the same expert, the extra tokens are either dropped or sent to the next-best expert. This capacity limit is what makes load balancing critical in real systems.

## How Outputs Are Combined

When the router picks the `top-k` experts for a token, each picked expert produces its own output. So how does the model combine these outputs into a single output?

The router does not just pick the `top-k` experts. It also produces weights for them - numbers that tell us how much to trust each picked expert. The final output is a weighted sum of the outputs from the picked experts.

In simple words: final output = weight_1 * Expert_1(input) + weight_2 * Expert_2(input) (for `top-2` experts).

The weights come from a softmax applied only over the picked experts' scores (not all experts), so the weights for the picked experts add up to 1.

Let's walk through a concrete example. Suppose a token enters an MoE layer with 8 experts:

- Step 1: The router scores all 8 experts. Say the top-2 are Expert 3 with score `0.7` and Expert 5 with score `0.3`.
- Step 2: Only Expert 3 and Expert 5 run. Expert 3 produces an output vector `Out_3`. Expert 5 produces an output vector `Out_5`.
- Step 3: The model combines them as: final output = 0.7 * Out_3 + 0.3 * Out_5.
- Step 4: This final output is passed to the next Transformer layer.

So Expert 3's output is trusted more than Expert 5's output because its router score is higher. This way, the model gets a smooth, blended answer from the top experts instead of a rough one-expert answer.

## Advantages of Mixture of Experts

Let's understand why MoE has become so popular:

Massive scale at a fraction of the cost: We can build models with hundreds of billions or even trillions of total parameters while keeping the active parameters per token much smaller. This is the only practical way to push model size to the extreme.

Faster inference: Since only a few experts run per token, the actual compute per token is small. This means faster responses and lower GPU costs in production.

Specialization: Different experts naturally learn to handle different kinds of inputs. The router learns which expert is good at what, without anyone telling it. This gives the model rich, specialized knowledge.

Better scaling: Research has shown that MoE models often reach the same quality as dense models with much less compute during training.

## Challenges of Mixture of Experts

MoE is not free. It comes with its own set of challenges:

Memory cost: Even though only a few experts run per token, all experts must be loaded into memory. So an 80-billion-parameter MoE model still needs the GPU memory to hold 80 billion parameters, even if it only uses 20 billion per token.

Load balancing is tricky: Without careful training, the router collapses to a few experts. Engineers need to add load balancing losses and tune them carefully.

Communication cost: In large MoE models, experts often live on different GPUs. Sending tokens to the right GPU and getting the results back adds communication overhead. Serving engines like SGLang are built to spread these experts across many machines and keep this overhead low.

Harder to fine-tune: Fine-tuning MoE models is trickier than fine-tuning dense models because the router behavior can shift during fine-tuning.

## Why MoE Powers Many Modern LLMs

Many of today's most powerful LLMs use Mixture of Experts under the hood. Mixtral, DeepSeek-V2, DeepSeek-V3, and several other frontier models are all MoE-based. There are also strong rumors that many of the top closed-source models use MoE internally.

The reason is simple. As models keep getting bigger, dense models hit a wall. Training and serving a dense model with hundreds of billions of parameters is extremely expensive. MoE breaks this wall by letting us grow the total size of the model without growing the per-token compute at the same rate.

In short, MoE is the answer to the question: how do we keep making models smarter without making them slower and more expensive?

## Summary

Let's recap what we have learned:

- Mixture of Experts is an architecture where many small expert networks sit side by side, and a router picks only a few of them for each token.
- Experts are small feed-forward networks. They are not manually specialized - the model learns on its own which expert handles what.
- The router is a tiny network that scores experts and picks the `top-k` for each token.
- Sparse activation means only the picked experts run, which makes MoE fast even when total parameters are huge.
- MoE replaces the feed-forward sub-layer inside a Transformer layer. Attention stays the same.
- Load balancing is needed to make sure all experts get used during training.
- Outputs are combined as a weighted sum based on the router's scores.
- MoE gives us massive scale at a fraction of the cost, which is why it powers many of today's most powerful LLMs.

Now we have learned the Mixture of Experts architecture and understood how it works.

### Does Mixture of Experts reduce the GPU memory needed?

No. Even though only a few experts run per token, all experts must be loaded into memory. So, an 80-billion-parameter MoE model still needs the GPU memory to hold 80 billion parameters, even if it only uses 20 billion per token. MoE saves compute, not memory.

### Why is Mixtral 8x7B around 47B parameters and not 56B?

Because only the feed-forward sub-layer is replicated across experts. The attention layers, embeddings, and normalization layers are shared across all experts. So, the total parameters are not simply the number of experts multiplied by the expert size. Only about 13 billion parameters are active per token.

### Is each expert trained on a specific topic like math or physics?

No. There is no manual labeling. The model learns on its own which experts should handle which kinds of inputs during training. In practice, experts often specialize by low-level patterns like punctuation, word types, or token shapes, not by high-level topics.

### Do all MoE layers share the same router?

No. Each MoE layer has its own router with its own learned weights. If a model has 32 MoE layers, it has 32 separate routers. Each layer learns its own way of dispatching tokens to its own set of experts, so the picked experts can be different at every layer.

### What happens if too many tokens are sent to the same expert?

Each expert can only process a fixed number of tokens per batch, which is called expert capacity. If too many tokens get routed to the same expert, the extra tokens are either dropped or sent to the next-best expert. This limit is what makes load balancing critical in real systems.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

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

[…703ln elided…]
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

[Showing lines 1-352 and 1056-1512 of 1512; 703 middle lines (49.0KB) elided. Read artifact://39 for full output]
