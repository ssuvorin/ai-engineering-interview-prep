> Source: https://outcomeschool.com/blog/causal-masking-in-attention

# What is Causal Masking in Attention and Why Do LLMs Need It?
URL: https://outcomeschool.com/blog/causal-masking-in-attention
Published: 2026-01-08
Author: Amit Shekhar

What is Causal Masking in Attention and Why Do LLMs Need It?

# What is Causal Masking in Attention and Why Do LLMs Need It?

Authors
: - Name
: Amit Shekhar
Published on
: January 8, 2026

Causal Masking in Attention is a mechanism that blocks the future tokens, so that each token can look only at itself and the tokens before it, never at the tokens after it.

In this blog, we will learn about causal masking in attention.

We will start with the introduction of causal masking, understand the problem of seeing future tokens through an example, and then walk through its implementation to see how masked attention prevents the model from accessing future tokens.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

As we all know, the attention layer is the most important component of the Transformer architecture and the key building block behind LLMs (Large Language Models).

Inside the attention layer, we use causal masking. This ensures that a token can attend only to itself and past tokens, never to future tokens.

Causal masking is a mechanism that uses a mask matrix to block future positions in the attention score matrix, ensuring each token attends only to itself and past tokens, never to future tokens.

This is exactly why the Decoder of a Transformer can look only backward, while the Encoder reads the whole input in both directions.

Let's try to understand this with an example.

Take the sentence: "I love teaching AI"

Token positions:

```bash
[ I | love | teaching | AI ]
  1     2        3        4

```

Let's see what happens without causal masking.

### Without Causal Masking

- While predicting "love", the model could attend to "teaching" and "AI".
- While predicting "teaching", it could already see "AI".

This is not something we want.

We should not allow the model to see the future, because doing so would introduce information leakage.

If future tokens are visible, the model can learn shortcuts by using words that it is supposed to predict as inputs. This leads to unrealistically good training performance but breaks the fundamental assumption of language modeling: predicting the next token using only past context.

During inference, future tokens do not exist.

If the model relied on future information during training, it would fail when asked to generate text step by step.

Causal masking ensures that training conditions match inference conditions, forcing the model to learn genuine language patterns instead of memorizing answers.

So, if we allow the model to see the future, training becomes easier, but generation becomes incorrect.

Let's see what happens with causal masking.

### With Causal Masking

- While predicting "love", the model attends to "I".
- While predicting "teaching", it attends to "I" and "love".
- While predicting "AI", it attends to "I", "love", and "teaching".

Here, we do not allow the model to see the future, so it is forced to behave exactly as it would during inference.

Blocking future tokens is one way to limit what a token can attend to. Limiting how far back a token can look is another, and we have a detailed blog on Sliding Window Attention that covers this end to end.

Now, let's understand how this is implemented using a mask matrix.

### Implementation of Causal Masking

In the attention layer, we compute an attention score matrix.

An attention score is a number that indicates how relevant one token is to another token.

- Each token compares itself with all other tokens.
- The attention score measures how much focus to give to each token.
- A higher score means more attention.
- A lower score means less attention.

As a result, each token computes a score with every other token, forming a 2D matrix where rows represent query tokens and columns represent key tokens. We have a detailed blog on Math behind Attention: Q, K, V that explains how query and key vectors are computed.

Since the sentence "I love teaching AI" contains 4 tokens, the attention scores form a 4 × 4 matrix.

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

Each row corresponds to a query token, and each column corresponds to a key token.

Each value in this matrix indicates how much one token should attend to another before normalization.

Example attention score matrix (before masking):

```bash
            I     love   teaching    AI
          --------------------------------
I         | 2.0 | 1.0 |   3.0   | 0.5 |
love      | 1.5 | 2.5 |   0.5   | 1.0 |
teaching  | 0.2 | 1.0 |   2.0   | 1.5 |
AI        | 0.1 | 0.3 |   0.7   | 2.5 |

```

Ideally, masking is applied before softmax. Let's see what happens if we skip masking and directly apply softmax.

After Softmax: Attention Weights

```bash
            I     love   teaching    AI
          --------------------------------
I         | 0.23 | 0.09 |  0.63 | 0.05 |
love      | 0.21 | 0.58 |  0.08 | 0.13 |
teaching  | 0.08 | 0.17 |  0.47 | 0.28 |
AI        | 0.07 | 0.08 |  0.12 | 0.73 |

```

At this stage, every token can attend to every other token, including future ones.

- While predicting "love", the model attends not only to past tokens but also to future tokens: it assigns an attention weight of 0.08 to "teaching" and 0.13 to "AI", which indicates information leakage.
- While predicting "teaching", the model already attends to the future token"AI" with an attention weight of 0.28, even though "AI" should not be visible at this stage.

Because of this issue, masking is required, and for that we use a causal mask matrix.

### The Causal Mask Matrix

We create a mask matrix of the same size. This matrix defines which positions are allowed (`1`) and which are blocked (`0`).

```bash
            I   love  teaching   AI
          --------------------------
I         | 1 |  0  |    0    | 0 |
love      | 1 |  1  |    0    | 0 |
teaching  | 1 |  1  |    1    | 0 |
AI        | 1 |  1  |    1    | 1 |

```

This is our mask matrix, and we will apply it to the score matrix to block future tokens.

Keep this mask matrix in mind as you read further, as we will use it to mask the attention score matrix.

- `1` → attention allowed
- `0` → attention blocked (future)

After applying the mask, the blocked positions are set to −∞.

Causal masking blocks access to future tokens by assigning −∞ to those positions.

In some time, we will understand why −∞ is used.

Example attention score matrix (before masking):

```bash
            I     love   teaching    AI
          --------------------------------
I         | 2.0 | 1.0 |   3.0   | 0.5 |
love      | 1.5 | 2.5 |   0.5   | 1.0 |
teaching  | 0.2 | 1.0 |   2.0   | 1.5 |
AI        | 0.1 | 0.3 |   0.7   | 2.5 |

```

Masked attention score matrix (after masking using our mask matrix):

```bash
            I     love   teaching    AI
          --------------------------------
I         | 2.0 | -∞  |   -∞    | -∞  |
love      | 1.5 | 2.5 |   -∞    | -∞  |
teaching  | 0.2 | 1.0 |   2.0   | -∞  |
AI        | 0.1 | 0.3 |   0.7   | 2.5 |

```

When the mask is applied, positions marked 0 in the mask matrix are blocked by setting their attention scores to −∞, while positions marked 1 retain their original values in the attention score matrix.

Why −∞? As we have to apply softmax, and because of how softmax works mathematically, −∞ becomes exactly zero after softmax. If we used zero instead, softmax would still assign a non-zero probability, allowing the model to partially attend to future tokens and defeating the purpose of causal masking.

After Softmax: Attention Weights

```bash
            I     love   teaching    AI
          --------------------------------
I         | 1.00 | 0.00 |  0.00 | 0.00 |
love      | 0.27 | 0.73 |  0.00 | 0.00 |
teaching  | 0.11 | 0.24 |  0.65 | 0.00 |
AI        | 0.07 | 0.08 |  0.12 | 0.73 |

```

Now, the future tokens receive zero attention:

- While predicting "love", the model attends to "I" with an attention weight of 0.27 and to itself ("love") with 0.73. It does not attend to the future tokens "teaching" and "AI", as both receive 0.00 attention.
- While predicting "teaching", the model attends to "I" (0.11) and "love" (0.24), and to itself ("teaching") with 0.65. It does not attend to the future token "AI", which has an attention weight of 0.00.
- While predicting "AI", the model attends to "I" (0.07), "love" (0.08), and "teaching" (0.12), and to itself ("AI") with 0.73.

Notice that every row still gives some weight to the first token "I", because it is the one token that every position can always see. This is exactly why the first tokens end up acting as attention sinks, the place where a model dumps the attention it does not need anywhere else.

This is how causal masking prevents the model from seeing future tokens.

To learn Causal Masked Attention, Q/K/V matrices, and Transformer internals end to end, check out our AI and Machine Learning Program at Outcome School.

### Why is minus infinity used for masking instead of zero?

Minus infinity becomes exactly zero after softmax. If we used zero instead, softmax would still assign a non-zero probability to the blocked positions. The model could then partially attend to future tokens, which defeats the purpose of causal masking.

### Is the causal mask applied before or after softmax?

The causal mask is applied before softmax. The blocked positions in the attention score matrix are set to minus infinity, and then softmax turns them into zero attention weights. If we skip masking and apply softmax directly, every token can attend to future tokens.

### Why do we need causal masking if future tokens do not exist during inference?

Causal masking makes training conditions match inference conditions. Without it, the model learns shortcuts during training by using the words it is supposed to predict. That gives unrealistically good training performance, but the model then fails when it generates text step by step.

### Does the Encoder of a Transformer use causal masking?

No. The Decoder of a Transformer can look only backward because of causal masking. The Encoder reads the whole input in both directions.

### What is the difference between causal masking and sliding window attention?

Causal masking blocks future tokens, so each token attends only to itself and the tokens before it. Sliding window attention limits how far back a token can look. Both limit what a token can attend to, but in different ways.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# What is Multi-Head Attention in Transformers and How Does It Work?
URL: https://outcomeschool.com/blog/multi-head-attention-in-transformers
Published: 2026-05-31
Author: Amit Shekhar

What is Multi-Head Attention in Transformers and How Does It Work?

# What is Multi-Head Attention in Transformers and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: May 31, 2026

Multi-Head Attention is a mechanism that runs many Self Attention operations in parallel and then combines their outputs. In simple words, the model looks at the sentence with many pairs of eyes, and each pair focuses on a different aspect.

In this blog, we will learn about Multi-Head Attention in Transformers. We will understand what it is, how it works step by step, and why it gives Transformers their power to understand language so well.

We will cover the following:

- What is Multi-Head Attention?
- A quick recap of Self Attention
- Why do we need Multi-Head Attention?
- Step-by-step working of Multi-Head Attention
- A simple example walk-through
- Where Multi-Head Attention is used
- Advantages of Multi-Head Attention

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Multi-Head Attention?

Multi-Head Attention is a mechanism that runs many Self Attention operations in parallel, each with its own set of Q, K, and V projections, and then combines their outputs into a single richer representation.

In simple words, Multi-Head Attention = Multi + Head + Attention. The word "Head" means one independent Self Attention. The word "Multi" means we run many such heads in parallel. The word "Attention" means each head decides how much to focus on every other token.

So, instead of looking at the sentence with one pair of eyes, the model looks at the sentence with many pairs of eyes at the same time, and each pair of eyes focuses on a different aspect of the sentence.

For the sake of understanding, let's take an analogy.

Suppose we are reading a sentence and we want to fully understand it. One person reads the sentence and focuses on who is doing the action. Another person reads the same sentence and focuses on where the action is happening. Another person focuses on why the action is happening. At the end, we collect the notes from every person and combine them into one final understanding of the sentence.

That is exactly what Multi-Head Attention does. Each head is one expert reader, and the final answer is the combination of all the experts.

Multi-Head Attention was introduced in the famous paper "Attention Is All You Need" in 2017, the paper that gave us the Transformer.

We have a detailed blog on the Evolution of LLM Architecture that explains what came before this paper and what came after it.

### A quick recap of Self Attention

Before jumping into Multi-Head Attention, we must know what Self Attention is.

In Self Attention, every token in a sentence looks at every other token in the same sentence to understand its meaning in context.

Self Attention uses three vectors for every token:

- Query (Q): what this token is looking for.
- Key (K): what this token offers to others.
- Value (V): the actual information this token carries.

All three, `Q`, `K`, and `V`, come from the same input sequence. That is why it is called Self Attention.

We have a detailed blog on the Math behind Attention - Q, K, and V that explains how these three vectors are created.

The Self Attention formula is:

Attention(Q, K, V) = softmax((Q . K^T) / sqrt(d_k)) . V

Here, we have done the following:

- Multiply `Q` and `K^T` to find how much each token relates to every other token.
- Divide by `sqrt(d_k)` to keep the numbers stable.
- Apply `softmax` to turn the scores into probabilities.
- Multiply by `V` to get a weighted sum of values.

This is how Self Attention works for a single set of `Q`, `K`, and `V`. We call this a single attention head.

This was all about Self Attention. Now, it's time to learn about Multi-Head Attention.

### Why do we need Multi-Head Attention?

The best way to learn this is by taking an example.

Consider the sentence:

> I love AI

This is a short sentence, but there are many different relationships hidden in it.

- `I` is the subject of the sentence.
- `love` is the action.
- `AI` is the object that the subject loves.
- `I` and `love` form a subject-verb relationship.
- `love` and `AI` form a verb-object relationship.
- `I` and `AI` are connected through the meaning of `love`.

Now, the question is: can a single attention head learn all of these relationships at the same time?

The answer is no. A single Self Attention head can only learn one type of relationship at a time. If one head is busy learning the subject-verb link, it cannot also learn the verb-object link with the same focus.

So, here comes Multi-Head Attention into the picture.

With multiple heads, each head can focus on a different type of relationship. One head can learn the subject-verb link. Another head can learn the verb-object link. Another head can learn the long-range link between the subject and the object. And so on.

This way, the model gets a much richer understanding of the same sentence.

### Step-by-step working of Multi-Head Attention

Now, it's time to learn the exact steps of Multi-Head Attention.

Assume that we have an input sequence with `d_model = 512` and we want to use `h = 8` heads.

Here, `d_model` is the size of the vector that represents each token. In simple words, every token in the sentence is converted into a list of numbers, and `d_model = 512` means each token is represented by 512 numbers. The bigger this number, the more information each token can carry.

Step 1: We start with the input embeddings. Every token in the sentence is converted into a vector of size `d_model`.

Step 2: We split the work across heads. We divide `d_model` by the number of heads. So, each head works with a smaller dimension.

- d_k = d_model / h = 512 / 8 = 64

Each head gets a dimension of 64 for its `Q`, `K`, and `V`.

Step 3: For every head, we use its own learned linear projections to create the `Q`, `K`, and `V` vectors.

- Q_i = Input x W_i_Q
- K_i = Input x W_i_K
- V_i = Input x W_i_V

Here, `W_i_Q`, `W_i_K`, and `W_i_V` are the weight matrices for head `i` that the model learns during training.

Note: Every head has its own set of weight matrices. This is what allows different heads to learn different patterns.

We can visualize how each head creates its own `Q`, `K`, and `V` as below:

```
                  Input token embedding
                     (d_model = 512)
                           |
       +-------------------+-------------------+
       |                   |                   |
   own W_Q, W_K, W_V   own W_Q, W_K, W_V   own W_Q, W_K, W_V
       |                   |        ...        |
       ↓                   ↓                   ↓
    Q1  K1  V1          Q2  K2  V2          Q8  K8  V8
    (each 64)           (each 64)           (each 64)
      Head 1              Head 2              Head 8

```

Here, we can see that the same input embedding of size 512 goes into every head, but each head uses its own weight matrices to create its own smaller `Q`, `K`, and `V` vectors of size 64.

Step 4: Each head now runs Self Attention independently using its own `Q_i`, `K_i`, and `V_i`.

- head_i = Attention(Q_i, K_i, V_i) = softmax((Q_i . K_i^T) / sqrt(d_k)) . V_i

All 8 heads do this in parallel.

Step 5: We concatenate the output of all heads side by side.

- Concat(head_1, head_2, ..., head_8)

After concatenation, we get a vector of size `h x d_k = 8 x 64 = 512`, which is the same as `d_model`. So, the output dimension matches the input dimension.

Step 6: We pass the concatenated output through one more learned linear layer to mix the information from all heads.

- MultiHead(Q, K, V) = Concat(head_1, ..., head_8) . W_O

Here, `W_O` is a learned weight matrix.

This is the final output of Multi-Head Attention.

Here, we can visualize the full flow of Multi-Head Attention as below:

```
                  Input Embeddings (512)
                              |
        +---------+-----------+-----------+----------+
        |         |                       |          |
        ↓         ↓           ...         ↓          ↓
      Head 1    Head 2                  Head N-1   Head N
   (each head creates its own Q, K, V of size 64)
        |         |                       |          |
        ↓         ↓                       ↓          ↓
     Output 1  Output 2       ...      Output N-1 Output N
       (64)      (64)                    (64)       (64)
[…537ln elided…]

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

# What is Generative AI?
URL: https://outcomeschool.com/blog/what-is-generative-ai
Published: 2026-08-05

What is Generative AI?

# What is Generative AI?

Authors
: - Name
: Amit Shekhar
Published on
: August 5, 2026

Generative AI is a type of AI that can create new things, like text, images, audio, video, and code, that did not exist before.

In this blog, we will learn about Generative AI. We will understand what the word "generate" actually means, how Generative AI is different from the older AI, how it learns from a huge amount of examples, how it creates something completely new, where we use it every day, and the limitations we must know.

We will cover the following:

- What is Generative AI?
- Generative AI = Generative + AI
- What does "generate" mean here?
- How is Generative AI different from the old AI?
- How does Generative AI learn?
- How does Generative AI actually create something new?
- What can Generative AI create?
- What is a model in Generative AI?
- The complete flow of Generative AI
- Where do we use Generative AI every day?
- The limitations we must know
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Generative AI?

Generative AI is a type of artificial intelligence that can create new things, like text, images, audio, video, and code.

Let's say we ask a computer, "Write me a short poem about the rain." A few years back, a normal computer could not do this. It could search for a poem that someone else had already written, but it could not write a fresh new poem on its own.

Now, things have changed. Today, we can ask, and the computer writes a brand new poem in seconds. Nobody wrote that exact poem before. The computer created it for us right now.

That power to create something new is what we call Generative AI.

## Generative AI = Generative + AI

The best way to understand this term is to break it into two parts.

Generative: This word comes from "generate", which means to create or to produce something new.

AI: This is short for Artificial Intelligence. It means making a computer do tasks that normally need human intelligence, like understanding language, seeing pictures, or making decisions.

So, when we join both parts:

> Generative AI = An artificial intelligence that can create new content on its own.

In simple words, it can produce fresh text, images, sound, and more, just like a human creator would.

## What does "generate" mean here?

This is the most important word, so let's be very clear about it.

To generate means to create something that did not exist before.

Let's say we have a calculator. We type `2 + 2`, and it gives `4`. This is not generating. The calculator just follows a fixed rule. The answer is always the same, and it is not new.

Now, let's say we ask Generative AI to "draw a cat riding a bicycle on the moon." No such picture existed before. The AI creates that picture, pixel by pixel, just for us. This is generating.

So, the key idea is this. Generative AI does not copy and paste an old answer. It creates a new one.

## How is Generative AI different from the old AI?

Before Generative AI became popular, we already had AI. But that older AI mostly did one job. It looked at something and gave a label or a decision.

Let's understand this with an example. The old AI was very good at answering questions like these:

- Is this email spam or not spam?
- Is there a cat in this photo or not?
- Is this review positive or negative?

Here, we can notice one thing. The old AI only chooses from options that already exist. It does not create anything new. We can call this kind of AI "the AI that decides."

Generative AI is different. It does not just decide. It creates. We can call it "the AI that creates."

Let me tabulate the difference between the two for your better understanding so that the whole picture becomes clear.

| Old AI (the AI that decides) | Generative AI (the AI that creates) |
| --- | --- |
| Looks at input and picks a label | Looks at input and produces new content |
| "Is this a cat or a dog?" | "Draw me a new cat." |
| Chooses from fixed options | Creates something that did not exist before |
| Output is a decision | Output is fresh text, image, audio, or video |

We can also picture this difference like below:

```
   Old AI (decides)                    Generative AI (creates)

   Photo of an animal                  Text: "a cat on the moon"
        |                                     |
        v                                     v
   +-----------+                        +-----------+
   |    AI     |                        |    AI     |
   +-----------+                        +-----------+
        |                                     |
        v                                     v
   "It is a cat"                        A brand new picture
   (a label)                            of a cat on the moon

```

Here, we can see the clear difference. On the left, the AI only puts a label. On the right, the AI creates a whole new picture.

Both kinds are built on Machine Learning, and we have a detailed blog on What is Machine Learning? that explains how a machine learns from data in the first place.

Now that we know what Generative AI does, the next question is: how does it learn to do this? Let's understand it.

## How does Generative AI learn?

Generative AI learns by looking at a huge amount of examples. This is the heart of everything, so let's go slowly.

Let's say we want to teach a child to write stories. We would let the child read thousands of storybooks. After reading so many stories, the child starts to understand how a story works. The child learns which words go together, how a sentence flows, and how a story begins and ends.

Generative AI learns in the same way. We show it a massive amount of examples. For a text AI, we show it a large part of the writing available on the internet, like books, articles, and websites. It reads all of this during a stage that we call training.

During training, the AI is not memorizing the text word for word. Instead, it is learning the patterns. It learns which words usually come after which words. It learns how ideas connect. It learns the style and the structure of language.

So, after training, the AI has learned the deep patterns of language. Now, it can use these patterns to create new sentences on its own.

Note: The same idea works for images. To create images, the AI is trained on a huge collection of pictures along with their descriptions. It learns what a "cat", a "bicycle", and the "moon" look like. Later, it can mix these learned patterns to draw a cat riding a bicycle on the moon, even though it never saw that exact picture before.

If we want to go deep into how this learning actually happens - Machine Learning fundamentals, Supervised and Unsupervised Learning, Neural Networks, and Backpropagation - check out our AI and Machine Learning Program at Outcome School.

## How does Generative AI actually create something new?

Now, this is the most magical part. Let's understand how a text Generative AI writes a sentence.

The secret is surprisingly simple. The AI predicts the next word, again and again. Inside the model, this writing job is done by the Decoder.

Let's say we give it the starting words, "The sky is". The AI now thinks, "What word usually comes next?" From all its training, it knows that "blue" is a very likely next word. So, it adds "blue".

Now the sentence is "The sky is blue". The AI again asks, "What comes next?" Now it adds "and". Then it asks again, and adds "clear". It keeps doing this, one word at a time, until the sentence is complete.

We can picture this step by step like below:

```
   Step 1:  "The sky is"          ->  predict next word  ->  "blue"
   Step 2:  "The sky is blue"     ->  predict next word  ->  "and"
   Step 3:  "The sky is blue and" ->  predict next word  ->  "clear"
   Step 4:  "The sky is blue and clear"  ->  and so on...

```

Here, we can see the beautiful trick. The AI never writes a whole paragraph in one shot. It writes one word, then looks at everything so far, then writes the next word. It repeats this until the full answer is ready.

So, a long and smart answer is really just the AI predicting the next word, over and over, very fast. And whether it plays safe with "blue" or takes a chance on a surprising word is controlled by a knob called Temperature, along with two more settings called Top-k and Top-p.

This way of creating, one word at a time, is called autoregressive generation, and we have a detailed blog on Autoregressive Models that explains it step by step.

This is how Generative AI creates new text. It creates images, audio, and video in a similar spirit, by using the patterns it learned during training, just with different methods for each type of content.

## What can Generative AI create?

Generative AI is not limited to text. It can create many kinds of content. Let's see a few.

- Text: It can write emails, stories, articles, answers, and summaries.
- Images: It can create paintings, photos, logos, and art from a simple description.
- Audio: It can create music, and it can create a human-like voice that reads text aloud.
- Video: It can create short video clips from a text description.
- Code: It can write computer programs and help developers build software.

So, whatever kind of content a human can create, Generative AI is learning to create it too.

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

## What is a model in Generative AI?

We keep saying "the AI", but let's give it a proper name. The trained brain of Generative AI is called a model.

A model is the final result of all that training. Think of it as a brain that has already read a huge amount of data and has learned the patterns inside it. When we chat with a Generative AI tool, we are really talking to this trained model.

When a model works mainly with text and language, we call it a Large Language Model, or LLM for short.

- Large: It has learned from a very large amount of text, and it has a very large number of internal settings that store what it learned.
- Language: Its main job is to understand and create human language.
- Model: It is the trained brain that holds all this learned knowledge.

So, when we hear names like the models behind ChatGPT, Claude, or Gemini, these are all Large Language Models. They are the trained brains that power the Generative AI tools we use.

## The complete flow of Generative AI

Now that we have learned about all the parts, let's put the whole flow together in simple steps.

- First, we collect a huge amount of examples, like text or images. This is the data.
- Then, the AI reads all this data and learns the patterns inside it. This is training.
- After that, the trained brain is ready. We call this brain the model.
- Then, we give the model a request in plain words. This request is called a prompt.
- Finally, the model uses its learned patterns to create a brand new answer for us.

We can picture the whole flow like below:

```
   Huge amount of data (text, images, code)
              |
              |  the AI reads and learns the patterns
              v
          Training
              |
              v
        Trained model  (the brain that has learned)
              |
              |  we give a prompt: "Write a poem about rain"
              v
        New content  (a fresh poem, created just now)

```

Here, we can see the full journey. First, the model learns from data. Then, we give it a prompt. Finally, it creates something new for us.

## Where do we use Generative AI every day?

Let's see a few common places.

- Chat assistants: We ask a question in plain English and get a helpful answer.
- Writing help: It helps us write emails, fix our grammar, and summarize long text.
- Image creation: We type a description, and it draws a picture for us.
- Coding help: It helps developers write and fix code faster.
- Customer support: Many company chatbots now use Generative AI to answer our questions.

It is helping millions of people every single day.

## The limitations we must know

Generative AI is powerful, but it is not perfect. We must understand its limits so that we use it wisely.

- It can be wrong. The AI predicts what sounds right, but sometimes it makes up facts that are not true. This is called a hallucination. So, we must always check important information.
- It does not truly understand. It is very good at patterns, but it does not "know" things the way a human does. It has no real feelings or life experience.
- It learns from human data. Since it learns from what humans wrote, it can also pick up the mistakes and biases present in that data.
- It needs a good prompt. The quality of the answer depends a lot on how clearly we ask. A clear prompt gives a better result.

So, Generative AI is a very helpful tool, but we must use it as a smart helper, not as a source of final truth.

## Summary

Let's quickly recap what we have learned.

- Generative AI is a type of AI that creates new content, like text, images, audio, video, and code.
- The word "generate" means to create something that did not exist before.
- The old AI mostly decided or labeled things. Generative AI creates new things.
- It learns by reading a huge amount of examples and understanding the patterns inside them.
- A text Generative AI creates a sentence by predicting the next word, again and again.
- The trained brain is called a model, and a text model is called a Large Language Model.
- It is powerful, but it can be wrong, so we must always check important facts.

This is how Generative AI works. It reads a huge amount of data, learns the patterns, and then uses those patterns to create something fresh and new for us.

Now, we must have understood what Generative AI is.

### Does Generative AI copy answers from its training data?

No. Generative AI does not copy and paste an old answer, and during training, it is not memorizing text word for word. It learns the patterns, like which words usually come after which words and how ideas connect. Then, it uses these patterns to create new content that did not exist before.

### Is an LLM the same as Generative AI?

Not exactly. Generative AI is the broad type of AI that creates new text, images, audio, video, and code. A Large Language Model, or LLM, is a trained model that works mainly with text and language. LLMs are the trained brains that power many of the Generative AI tools we use.

### Is ChatGPT an example of Generative AI?

Yes. The models behind ChatGPT, Claude, and Gemini are all Large Language Models, and they power Generative AI tools. When we ask such a tool a question in plain English, it creates a brand new answer by predicting the next word again and again, using the patterns it learned during training.

### What decides whether Generative AI picks a safe word or a surprising one?

A setting called Temperature controls this, along with two more settings called Top-k and Top-p. When the AI predicts the next word, it can play safe with the most likely word or take a chance on a more surprising one. These settings decide which way it leans.

### Is Generative AI built on Machine Learning?

Yes. Both the old AI that decides and Generative AI that creates are built on Machine Learning. Generative AI learns by looking at a huge amount of examples during a stage called training. The trained result is called a model, and it uses the learned patterns to create new content.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-450 and 988-1339 of 1339; 537 middle lines (29.6KB) elided. Read artifact://38 for full output]
