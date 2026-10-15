> Source: https://outcomeschool.com/blog/feed-forward-networks-in-llms

# What is the Feed-Forward Network in LLMs and What Does It Do?
URL: https://outcomeschool.com/blog/feed-forward-networks-in-llms
Published: 2026-04-13
Author: Amit Shekhar

What is the Feed-Forward Network in LLMs and What Does It Do?

# What is the Feed-Forward Network in LLMs and What Does It Do?

Authors
: - Name
: Amit Shekhar
Published on
: April 13, 2026

The Feed-Forward Network in LLMs is a simple neural network inside every Transformer layer. After attention lets the words gather information from each other, the Feed-Forward Network processes each word on its own.

In this blog, we will learn about Feed-Forward Networks in LLMs - understanding what they are, how they work inside the Transformer architecture, why every Transformer layer needs one, and what role they play in making Large Language Models so powerful.

When we read about Transformers, we always hear about the attention mechanism. But there is another equally important component that does a huge amount of work inside every Transformer layer - the Feed-Forward Network (FFN).

In fact, in most modern LLMs, the feed-forward network holds the majority of the model's parameters. If we think of attention as the component that figures out relationships between words, the feed-forward network is what stores and applies the actual knowledge.

When we hear "Feed-Forward Network", it sounds complex. But do not worry. If we break it down into its individual parts, every single piece is simple. Our goal is to explain feed-forward networks so clearly that by the end, we will be able to explain how they work to anyone.

We will cover the following:

- What is a Feed-Forward Network?
- Understanding Feed-Forward Networks with a Real-World Analogy
- Where Does the Feed-Forward Network Sit in a Transformer?
- How Does a Feed-Forward Network Work - Step by Step
- The Expand-then-Contract Pattern
- Why Does the FFN Expand and Then Contract?
- ReLU and Activation Functions
- What Does the Feed-Forward Network Actually Learn?
- How Much of the Model is the Feed-Forward Network?
- Feed-Forward Networks in Mixture of Experts
- Why Feed-Forward Networks Are So Important

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

A Feed-Forward Network (FFN) is a small neural network that sits inside every layer of a Transformer. After the attention mechanism figures out how words relate to each other, the feed-forward network takes each word's representation and processes it individually - refining it, enriching it, and adding knowledge to it.

In simple words: Feed-Forward Network = The knowledge store and refiner inside each Transformer layer.

Think of it like this. Imagine a team meeting where everyone discusses a project. This is attention - words talking to each other. After the meeting, each team member goes back to their own desk and uses their own expertise to refine their notes and add deeper insights. This is the feed-forward network - each word being processed individually using stored knowledge.

So, attention is about how words talk to each other. The feed-forward network is about how each word processes what it heard.

## What is a Feed-Forward Network?

A Feed-Forward Network is the simplest type of neural network. The word "feed-forward" means data flows in only one direction - forward. It goes from input to output, passing through one or more layers in between, without ever looping back.

Let's break the name down:

Feed-Forward = Feed (pass data) + Forward (in one direction)

There are no loops, no cycles, and no going back. Data enters from one side and exits from the other. This is what makes it different from other types of neural networks like Recurrent Neural Networks (RNNs) where data can loop back on itself.

In its simplest form, a feed-forward network has an input layer where data comes in, a hidden layer where the actual processing happens, and an output layer where the result comes out.

```
Input Layer       Hidden Layer       Output Layer
   [x1] ----\       [h1] ----\
              \-->            ---->   [y1]
   [x2] ------>    [h2] ------>      [y2]
              /--->           ---->   [y3]
   [x3] ----/       [h3] ----/

```

Here, each connection between the layers has a weight (a number). The network multiplies the input values by these weights, adds them up, and passes the result through an activation function to produce the output. We will learn about activation functions in a later section.

Note: In the Transformer's FFN, the structure is just two linear transformations with an activation function in between. The first linear transformation is the input-to-hidden step (W1), and the second one is the hidden-to-output step (W2), rather than distinct input, hidden, and output layers like traditional neural networks.

## Understanding Feed-Forward Networks with a Real-World Analogy

The best way to learn this is by taking an example.

Let's say we have a factory that makes custom furniture.

The factory has three stages:

Stage 1 (Input): Raw wood planks arrive at the factory. These are our raw materials - the input.

Stage 2 (Hidden - Expand): The wood planks go to a large workshop where many specialists work. One specialist cuts the wood. Another one sands it. Another one carves patterns. Another one drills holes. Another one checks for quality. This workshop is much bigger than the input area because the factory needs many specialists to work on different aspects of the wood at the same time.

Stage 3 (Output - Contract): After all the specialists have done their work, the refined pieces are assembled back into a finished piece of furniture. The output is compact - a single, refined product.

This is exactly how the feed-forward network works in a Transformer.

## Where Does the Feed-Forward Network Sit in a Transformer?

Every Transformer layer has two main sub-layers:

- Multi-Head Attention - where words look at each other to understand relationships
- Feed-Forward Network - where each word is processed individually to refine its representation

The data flows through them in order. First, the input passes through the attention mechanism. Then, the output of attention passes through the feed-forward network. Each sub-layer also has a residual connection (skip connection) and layer normalization around it.

```
         Input
           |
   -----------------
   | Multi-Head    |
   | Attention     |
   -----------------
           |
   Add & Layer Norm
           |
   -----------------
   | Feed-Forward  |
   | Network       |
   -----------------
           |
   Add & Layer Norm
           |
         Output

```

This entire block is one Transformer layer. A typical LLM stacks many such layers on top of each other. For example, GPT-3 has 96 layers, and each layer has its own attention sub-layer and its own feed-forward network sub-layer. The diagram above shows the original Transformer's post-norm arrangement (layer normalization after each sub-layer). Modern LLMs like GPT and LLaMA typically use pre-layer normalization (LayerNorm before each sub-layer), which helps with training stability.

Now, there is an important difference between these two sub-layers. The attention mechanism processes all words together - it lets every word look at every other word. But the feed-forward network processes each word independently. The same feed-forward network is applied to each word's representation separately and independently. In practice, all tokens are processed in parallel (as a batched matrix multiplication), but the key point is that given the contextualized representations from attention, each token is processed independently by the FFN.

I will highly recommend reading our detailed blog on Transformer architecture that explains how all the pieces fit together.

## How Does a Feed-Forward Network Work - Step by Step

Now, let's understand how the feed-forward network works step by step.

Each word's representation is a vector of numbers. The feed-forward network takes this vector and passes it through two linear transformations with an activation function in between.

Here is what happens:

Step 1: First linear transformation (Expand)

The input vector is multiplied by a weight matrix and a bias is added. This transforms the input from a smaller dimension to a much larger dimension.

```
hidden = input * W1 + b1

```

Here, we can see that the input is multiplied by the weight matrix `W1` and a bias `b1` is added. If the input dimension is 4096, the hidden dimension is typically 16384 (4 times larger).

Step 2: Activation function

The result from Step 1 is passed through an activation function like ReLU or GELU. The activation function introduces non-linearity - meaning it allows the network to learn complex patterns that a simple linear transformation cannot capture. We will learn more about this in the activation function section.

```
activated = ReLU(hidden)

```

Step 3: Second linear transformation (Contract)

The activated output is multiplied by another weight matrix and a bias is added. This transforms the data back from the larger dimension to the original smaller dimension.

```
output = activated * W2 + b2

```

Here, `W2` is the weight matrix of the second layer and `b2` is the bias. The output has the same dimension as the input.

Putting it all together:

```
FFN(x) = ReLU(x * W1 + b1) * W2 + b2

```

Here, we can see the complete feed-forward network in one line. Two matrix multiplications, one activation function, and two bias additions. It is that simple.

## The Expand-then-Contract Pattern

Now, let's understand a very important pattern in the FFN - the expand-then-contract pattern.

The input has a certain dimension (let's call it `d_model`). The hidden layer expands this to a much larger dimension (typically `4 * d_model`). Then the output contracts it back to the original dimension `d_model`.

Let's put this into perspective with real numbers:

- In GPT-3 (175B), `d_model` = 12288. The hidden layer expands this to 4 * 12288 = 49152. Then it contracts back to 12288.
- In LLaMA 2 (7B), `d_model` = 4096. The hidden layer expands this to approximately 11008 (not exactly 4x because LLaMA 2 uses SwiGLU, which we will learn about shortly). Then it contracts back to 4096.

```
Input (d_model)            Hidden (expanded)               Output (d_model)
  [4096 dims] -------->     [11008 dims] -------->          [4096 dims]
              Expand                       Contract

```

So, the data starts small, becomes big in the middle, and becomes small again at the end.

This was all about the expand-then-contract pattern. Now, let's understand why the FFN does this.

## Why Does the FFN Expand and Then Contract?

Now, a natural question arises - why does the feed-forward network expand the dimension and then shrink it back? Why not just keep the same size throughout?

The answer is simple: the larger hidden layer gives the network more room to think.

Think of it like solving a math problem. We start with a small problem written on a sticky note (input). We need a large whiteboard (expanded hidden layer) to work through all the intermediate steps. Once we have the answer, we write it back on a small sticky note (output).

The expansion gives the network more space to extract patterns and transform the data. The contraction then compresses the result back to the size that the rest of the model expects.

This is a key design choice in Transformers. Without this expansion, the network would not have enough space to do the complex processing it needs.

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

## ReLU and Activation Functions

We mentioned that an activation function is applied between the two linear layers. But what is an activation function and why do we need it?

Without an activation function, the feed-forward network would just be two matrix multiplications stacked together. And two linear operations combined are still a linear operation. This means the network could only learn simple, straight-line patterns - which is not useful for understanding language.

So, here comes the activation function to the rescue.

The activation function adds non-linearity, which allows the network to learn complex, curved, and irregular patterns.

ReLU (Rectified Linear Unit) is one of the simplest activation functions:

```
ReLU(x) = max(0, x)

```

It does one simple thing: if the number is positive, keep it as it is. If the number is negative, replace it with zero.

For example:

- ReLU(5) = 5 (positive, keep it)
- ReLU(-3) = 0 (negative, replace with zero)
- ReLU(0) = 0

This simple operation is very powerful. By setting negative values to zero, ReLU creates sparsity - meaning many neurons in the hidden layer become inactive (output zero) for any given input. This sparsity helps the network specialize. Different neurons activate for different types of inputs, allowing different parts of the network to store different knowledge.

Note: Smoother activation functions like GELU reduce this explicit sparsity effect, but they tend to improve overall model performance.

GELU (Gaussian Error Linear Unit) is a smoother version of ReLU that is used in many modern LLMs like GPT and BERT. Instead of making a hard cutoff at zero, GELU gradually reduces small negative values. The idea is the same - it adds non-linearity - but it does so more smoothly.

SwiGLU is another activation function used in newer models like LLaMA. SwiGLU uses a gating mechanism that lets the network learn which parts of the information to keep and which to suppress. In practice, models using SwiGLU tend to perform better than those using ReLU or GELU.

Very important: SwiGLU changes the structure of the FFN. Instead of two weight matrices (W1 and W2), SwiGLU uses three weight matrices (W1, V, and W2). Do not worry if the formula below feels complex - the key takeaway is that SwiGLU adds a gating mechanism using an extra matrix, and the rest is just how the pieces connect. The formula becomes:

```
SwiGLU(x) = (Swish(x * W1) ⊙ (x * V)) * W2

```

Here, `*` represents matrix multiplication and `⊙` represents element-wise (Hadamard) multiplication. The input `x` is multiplied by two separate matrices (W1 and V), and their results are combined using element-wise multiplication (`⊙`). Because there is a third matrix, the total number of parameters would increase if we kept the same hidden dimension. So, the hidden dimension is reduced from 4x to roughly 2.7x to keep the parameter count similar. For example, LLaMA 2 7B has `d_model` = 4096 and a hidden dimension of 11008, which gives us 11008 / 4096 = approximately 2.69x instead of 4x.

Note: Larger variants like LLaMA 2 70B do not strictly follow the 2.7x rule. The 70B model has a hidden dimension of 28672 with `d_model` = 8192, giving a ratio of about 3.5x. The general principle of reducing from 4x to compensate for the third matrix holds, but the exact ratio varies across model sizes.

Note: The choice of activation function has evolved over time. The original Transformer paper used ReLU. Then GPT and BERT moved to GELU. And now many newer models use SwiGLU. The core idea remains the same - add non-linearity - but the specific function can be chosen based on our use case.

## What Does the Feed-Forward Network Actually Learn?

Now that we have understood how activation functions work and why they matter, let's move to a deeper question. If attention learns relationships between words, what does the feed-forward network actually learn?

Research has shown that a large portion of the model's stored knowledge resides in the feed-forward network weights. The FFN memorizes facts, patterns, and associations from the training data.

Let's say we have a library. The attention mechanism is like a librarian who finds which books are related to each other and puts them together on a table. The feed-forward network is like the actual books on the shelves - they contain the knowledge.

Without the books, the librarian has nothing to work with. Without the librarian, the books just sit on the shelves unused. Both are needed.

Now, think of each neuron in the hidden layer as a pattern detector. Some neurons activate when they see patterns related to geography (like "Paris is the capital of..."). Other neurons activate for patterns related to grammar (like verb tenses). Others activate for patterns related to math, science, coding, and so on.

Let's say the sentence is "The capital of France is". After attention processes this sentence, each word has context from the other words. Now, the feed-forward network takes the representation of the last token and applies its stored knowledge. Certain neurons in the hidden layer activate strongly because they recognize the pattern "capital of France". These activated neurons then contribute to producing an output that points towards "Paris".

Note: Just for the sake of understanding, we are simplifying here. In reality, the knowledge is distributed across many neurons and many layers, not stored in one single neuron. But the core idea is the same - the FFN is where the model's learned knowledge lives.

In simple words:

- Attention figures out which words are relevant to each other (relationships)
- Feed-Forward Network applies stored knowledge to each word's enriched representation (facts and patterns)

This is why feed-forward networks hold the majority of the model's parameters. They need to store a vast amount of knowledge from the training data.

## How Much of the Model is the Feed-Forward Network?

Let's put this into perspective with real numbers.

In a standard Transformer layer, the feed-forward network uses roughly two-thirds (about 66%) of all the parameters in that layer. The attention mechanism uses the remaining one-third.

Here is why. In standard multi-head attention (without parameter sharing), the main parameter matrices are for Query (Q), Key (K), Value (V), and Output (O). Each of these is of size `d_model x d_model`. So attention has approximately `4 * d_model * d_model` parameters.

In the feed-forward network, we have two weight matrices: `W1` of size `d_model x 4*d_model` and `W2` of size `4*d_model x d_model`. So the FFN has approximately `2 * d_model * 4*d_model = 8 * d_model * d_model` parameters.

```
Attention parameters:  ~4 * d_model^2
FFN parameters:        ~8 * d_model^2

FFN / Total = 8 / (8 + 4) = 8 / 12 = ~66%

```

This means that in a model like GPT-3 with 175 billion parameters, roughly 110-115 billion parameters are in the feed-forward networks across all layers (the rest goes to embeddings, layer norms, and the final projection head). That is a massive knowledge store.

Note: In modern models that use Grouped-Query Attention (GQA) or Multi-Query Attention (MQA), the K and V matrices are smaller than Q and O. This means the attention parameters are fewer, and the FFN's share becomes even larger than 66%.

## Feed-Forward Networks in Mixture of Experts

Now that we have understood how much of the model is the feed-forward network, let's understand how some modern models use multiple feed-forward networks instead of one.

In standard Transformers, every token passes through the same feed-forward network in each layer. But in Mixture of Experts (MoE) models, the single feed-forward network is replaced with multiple feed-forward networks - each one called an expert.

A small router network decides which expert(s) each token should be sent to. Only a few experts (typically 2 out of 8 or 64) are activated for each token. The rest stay idle.

```
                    Token
                      |
                   [Router]
                  /    |    \
               /       |       \
         [Expert 1] [Expert 2] ... [Expert N]
            (FFN)     (FFN)         (FFN)
              \        |
               \       |
            Selected Outputs Combined

```

Instead of one large feed-forward network trying to be good at everything, we have many smaller feed-forward networks that can specialize in different types of patterns. The router learns which expert is best for each type of input.

The result is that we can have a model with a huge total number of parameters for knowledge capacity, while only using a fraction of them for each token, keeping the compute cost low.

We have a detailed blog on Mixture of Experts that explains the complete architecture.

## Why Feed-Forward Networks Are So Important

Now that we have understood how feed-forward networks work, let's understand why they are so important inside LLMs.

Without the FFN, the model would have no knowledge. The attention mechanism figures out relationships between words. But the actual knowledge - facts, patterns, grammar rules, reasoning patterns - is stored in the parameters of the feed-forward network. The model would understand word relationships but would have no knowledge to apply.

The FFN refines what attention discovers. After attention processes the relationships between words, the feed-forward network refines each word's representation. It takes the "who is related to whom" signal from attention and adds "what do I know about this" from its stored knowledge.

Without the activation function, the model could not learn complex patterns. Without the activation function in the FFN, the entire Transformer would be a series of linear operations. Linear operations alone cannot model the complexity of language. The FFN's activation function is what gives the model the ability to learn complex, non-linear patterns.

The FFN holds the majority of the model's parameters. About two-thirds of a Transformer's parameters are in the feed-forward networks. This means the FFN is where the model's capacity primarily lives. When we say a model has 70 billion parameters, about 46 billion of those are in the feed-forward networks.

The FFN processes each token independently, making it highly efficient. While attention requires all tokens to interact with each other, the FFN processes each token on its own. This makes the FFN highly parallelizable and computationally efficient.

In simple words: Attention moves information across tokens. FFN transforms information within a token.

Now, we have understood why feed-forward networks are so important. Without them, LLMs would have no place to store their knowledge.

## Quick Summary

Let's recap what we have learned:

- Feed-Forward Network (FFN) is a simple neural network inside every Transformer layer that processes each word independently after the attention mechanism.
- Feed-Forward means data flows in only one direction - from input to output, with no loops.
- The FFN has two linear layers with an activation function in between. The first layer expands the dimension (typically to 4x), and the second layer contracts it back to the original size.
- The expand-then-contract pattern gives the network a larger "thinking space" to process information before compressing it back.
- Activation functions (ReLU, GELU, SwiGLU) add non-linearity, allowing the network to learn complex patterns.
- The FFN acts as a knowledge store, memorizing facts, patterns, and associations from training data.
- About 66% of a Transformer's parameters are in the feed-forward networks, making them the largest component.
- In Mixture of Experts models, the single FFN is replaced with multiple specialized FFNs (experts) with a router selecting which ones to activate.
- Attention is about relationships between words. FFN is about knowledge applied to each word individually.

### What is the difference between attention and the Feed-Forward Network in a Transformer?

Attention moves information across tokens, while the Feed-Forward Network transforms information within a token. Attention lets every word look at every other word to figure out relationships. The FFN then takes each word's representation on its own and applies stored knowledge to refine it.

### Does the Feed-Forward Network look at other tokens?

No. The Feed-Forward Network processes each token independently. The same FFN is applied to each word's representation separately. In practice, all tokens are processed in parallel as a batched matrix multiplication, which makes the FFN highly parallelizable and computationally efficient.

### Why can't we remove the activation function from the FFN?

Wi
