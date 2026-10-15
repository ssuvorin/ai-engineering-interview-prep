> Source: https://outcomeschool.com/blog/math-behind-attention-qkv

# How Does Attention Work? The Math Behind Q, K, and V Step by Step
URL: https://outcomeschool.com/blog/math-behind-attention-qkv
Published: 2026-04-03
Author: Amit Shekhar

How Does Attention Work? The Math Behind Q, K, and V Step by Step

# How Does Attention Work? The Math Behind Q, K, and V Step by Step

Authors
: - Name
: Amit Shekhar
Published on
: April 3, 2026

Attention works by comparing the Query (Q) of each word with the Key (K) of every word to get scores, turning those scores into weights using softmax, and then using the weights to mix the Values (V). The formula is `softmax(Q x K^T / sqrt(d_k)) x V`.

In this blog, we will learn about the math behind Attention: Query(Q), Key(K), and Value(V) with a step-by-step numeric example.

We will cover the following:

- The Attention Formula
- Setting Up: From Words to Vectors
- Creating Q, K, and V Matrices
- Computing Attention Scores (Q x K^T)
- Scaling the Scores
- Applying Softmax
- Computing the Final Output (Attention Weights x V)
- Putting It All Together

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Attention Formula

The core formula for Scaled Dot-Product Attention is:

```
Attention(Q, K, V) = softmax(Q x K^T / sqrt(d_k)) x V

```

Here:

- `Q` is the Query matrix
- `K` is the Key matrix
- `V` is the Value matrix
- `K^T` is the transpose of the Key matrix
- `d_k` is the dimension of the Key vector
- `sqrt` means square root

Do not worry if this formula looks complex. We will break it down step by step with actual numbers. By the end of this blog, every part of this formula will be clear.

The idea is simple: we compare what each word is looking for (Query) with what every other word offers (Key), and then use those comparisons to collect the actual information (Value) from the most relevant words.

Now, let's see this with real numbers.

## Setting Up: From Words to Vectors

Let's take a simple sentence with 3 words:

"I love AI"

In a Transformer, each word is first converted into a vector (i.e. a list of numbers) called an embedding. Just for the sake of understanding, we will use very small vectors of size 4 (i.e. `d_emb = 4`).

```
"I"    → [1.0, 0.0, 1.0, 0.0]
"love" → [0.0, 1.0, 0.0, 1.0]
"AI"   → [1.0, 1.0, 0.0, 0.0]

```

We stack these into an input matrix X of shape `3 x 4` (3 words, each with 4 numbers):

```
X = | 1.0  0.0  1.0  0.0 |   ← "I"
    | 0.0  1.0  0.0  1.0 |   ← "love"
    | 1.0  1.0  0.0  0.0 |   ← "AI"

```

Here, each row is one word and each column is one number in the embedding. This is our starting point.

## Creating Q, K, and V Matrices

Now, we need to create three separate matrices: Q (Query), K (Key), and V (Value).

How do we create them? We multiply the input matrix `X` with three separate weight matrices: `W_Q`, `W_K`, and `W_V`. These weight matrices are learned during training.

```
Q = X x W_Q
K = X x W_K
V = X x W_V

```

For our example, let's say `d_k = 3` (i.e. we want Q, K, V vectors of size 3). So each weight matrix has the shape `4 x 3` (input dimension 4, output dimension 3).

Let's use the following weight matrices for the sake of understanding:

```
W_Q = | 1  0  1 |
      | 0  1  0 |
      | 1  0  0 |
      | 0  1  1 |

W_K = | 0  1  0 |
      | 1  0  1 |
      | 0  0  1 |
      | 1  1  0 |

W_V = | 1  0  0 |
      | 0  1  0 |
      | 0  0  1 |
      | 1  1  0 |

```

Now, let's compute Q, K, and V.

Computing Q = X x W_Q:

```
Q = | 1.0  0.0  1.0  0.0 |     | 1  0  1 |
    | 0.0  1.0  0.0  1.0 |  x  | 0  1  0 |
    | 1.0  1.0  0.0  0.0 |     | 1  0  0 |
                               | 0  1  1 |

```

For the first row ("I"): `[1*1 + 0*0 + 1*1 + 0*0, 1*0 + 0*1 + 1*0 + 0*1, 1*1 + 0*0 + 1*0 + 0*1]` = `[2, 0, 1]`

For the second row ("love"): `[0*1 + 1*0 + 0*1 + 1*0, 0*0 + 1*1 + 0*0 + 1*1, 0*1 + 1*0 + 0*0 + 1*1]` = `[0, 2, 1]`

For the third row ("AI"): `[1*1 + 1*0 + 0*1 + 0*0, 1*0 + 1*1 + 0*0 + 0*1, 1*1 + 1*0 + 0*0 + 0*1]` = `[1, 1, 1]`

```
Q = | 2  0  1 |   ← "I"
    | 0  2  1 |   ← "love"
    | 1  1  1 |   ← "AI"

```

Computing K = X x W_K:

For the first row ("I"): `[1*0 + 0*1 + 1*0 + 0*1, 1*1 + 0*0 + 1*0 + 0*1, 1*0 + 0*1 + 1*1 + 0*0]` = `[0, 1, 1]`

For the second row ("love"): `[0*0 + 1*1 + 0*0 + 1*1, 0*1 + 1*0 + 0*0 + 1*1, 0*0 + 1*1 + 0*1 + 1*0]` = `[2, 1, 1]`

For the third row ("AI"): `[1*0 + 1*1 + 0*0 + 0*1, 1*1 + 1*0 + 0*0 + 0*1, 1*0 + 1*1 + 0*1 + 0*0]` = `[1, 1, 1]`

```
K = | 0  1  1 |   ← "I"
    | 2  1  1 |   ← "love"
    | 1  1  1 |   ← "AI"

```

Computing V = X x W_V:

For the first row ("I"): `[1*1 + 0*0 + 1*0 + 0*1, 1*0 + 0*1 + 1*0 + 0*1, 1*0 + 0*0 + 1*1 + 0*0]` = `[1, 0, 1]`

For the second row ("love"): `[0*1 + 1*0 + 0*0 + 1*1, 0*0 + 1*1 + 0*0 + 1*1, 0*0 + 1*0 + 0*1 + 1*0]` = `[1, 2, 0]`

For the third row ("AI"): `[1*1 + 1*0 + 0*0 + 0*1, 1*0 + 1*1 + 0*0 + 0*1, 1*0 + 1*0 + 0*1 + 0*0]` = `[1, 1, 0]`

```
V = | 1  0  1 |   ← "I"
    | 1  2  0 |   ← "love"
    | 1  1  0 |   ← "AI"

```

Now, we have our Q, K, and V matrices ready.

Note: In real models, these weight matrices are not set by hand. They are learned during training. We are using simple numbers here for the sake of understanding.

Till now, we have learned how to create Q, K, and V from the input. Now, let's move to the next step.

If we want to go deep into Q/K/V matrices, embeddings, and Transformer internals from the ground up, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

## Computing Attention Scores (Q x K^T)

The first step in the attention formula is to compute `Q x K^T`.

This tells us how much each word should attend to every other word. We multiply the Query of each word with the Key of every other word.

First, we need `K^T` (transpose of K). Transposing simply means we swap the rows and columns. The first row becomes the first column, the second row becomes the second column, and so on:

```
K^T = | 0  2  1 |
      | 1  1  1 |
      | 1  1  1 |

```

Now, let's compute `Q x K^T`:

```
Q x K^T = | 2  0  1 |     | 0  2  1 |
          | 0  2  1 |  x  | 1  1  1 |
          | 1  1  1 |     | 1  1  1 |

```

For "I" attending to all words:

- "I" → "I": `2*0 + 0*1 + 1*1` = `1`
- "I" → "love": `2*2 + 0*1 + 1*1` = `5`
- "I" → "AI": `2*1 + 0*1 + 1*1` = `3`

For "love" attending to all words:

- "love" → "I": `0*0 + 2*1 + 1*1` = `3`
- "love" → "love": `0*2 + 2*1 + 1*1` = `3`
- "love" → "AI": `0*1 + 2*1 + 1*1` = `3`

For "AI" attending to all words:

- "AI" → "I": `1*0 + 1*1 + 1*1` = `2`
- "AI" → "love": `1*2 + 1*1 + 1*1` = `4`
- "AI" → "AI": `1*1 + 1*1 + 1*1` = `3`

```
            "I"   "love"   "AI"
Scores = |  1      5       3  |   ← "I"
         |  3      3       3  |   ← "love"
         |  2      4       3  |   ← "AI"

```

Here, we can see that the word "I" gives the highest attention score of `5` to "love", meaning "I" finds "love" the most relevant. The word "love" gives equal scores of `3` to all words. The word "AI" gives the highest score of `4` to "love".

This was all about computing the attention scores. Now, let's move to scaling.

## Scaling the Scores

Now, we divide every score by `sqrt(d_k)`.

In our example, `d_k = 3` (the dimension of our Key vectors), so `sqrt(3) = 1.732`.

Now, the question is: why do we scale? The answer is: if the dot product values are too large, the softmax function in the next step will produce very extreme values (close to 0 or 1). This makes it difficult for the model to learn. Scaling keeps the values in a manageable range. We have a detailed blog on the Math behind √dₖ Scaling Factor in Attention that explains this in depth.

```
Scaled Scores = Scores / sqrt(3)

```

```
                    "I"      "love"     "AI"
Scaled Scores = |  0.577    2.887     1.732  |   ← "I"
                |  1.732    1.732     1.732  |   ← "love"
                |  1.155    2.309     1.732  |   ← "AI"

```

Here, we can notice that the relative order of the scores has not changed. The word "I" still attends to "love" the most. But the values are now smaller, which is exactly what we wanted.

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

In the future, I plan to write about why we choose to divide by `sqrt(d_k)` instead of some other factor.

Now, let's apply softmax.

## Applying Softmax

Now, we apply the softmax function to each row. Softmax converts the scores into probabilities that add up to 1.

The softmax formula for a value `x_i` in a row is:

```
softmax(x_i) = e^(x_i) / sum(e^(x_j) for all j in that row)

```

Here, `e` is the mathematical constant (approximately 2.718). Do not worry about the formula too much. We will compute it step by step.

For the "I" row: [0.577, 2.887, 1.732]

- `e^0.577` = 1.781
- `e^2.887` = 17.940
- `e^1.732` = 5.651
- Sum = 1.781 + 17.940 + 5.651 = 25.372

Attention Weights:

- "I" → "I": 1.781 / 25.372 = 0.070
- "I" → "love": 17.940 / 25.372 = 0.707
- "I" → "AI": 5.651 / 25.372 = 0.223

For the "love" row: [1.732, 1.732, 1.732]

All values are equal, so each word gets equal attention:

- "love" → "I": 0.333
- "love" → "love": 0.333
- "love" → "AI": 0.333

For the "AI" row: [1.155, 2.309, 1.732]

- `e^1.155` = 3.174
- `e^2.309` = 10.063
- `e^1.732` = 5.651
- Sum = 3.174 + 10.063 + 5.651 = 18.888

Attention Weights:

- "AI" → "I": 3.174 / 18.888 = 0.168
- "AI" → "love": 10.063 / 18.888 = 0.533
- "AI" → "AI": 5.651 / 18.888 = 0.299

The final Attention Weight Matrix is:

```
                       "I"     "love"    "AI"
Attention Weights = | 0.070    0.707    0.223 |   ← "I"
                    | 0.333    0.333    0.333 |   ← "love"
                    | 0.168    0.533    0.299 |   ← "AI"

```

Here, we can see that:

- The word "I" pays 70.7% of its attention to "love", 22.3% to "AI", and only 7.0% to itself.
- The word "love" pays equal attention to all three words (33.3% each).
- The word "AI" pays 53.3% of its attention to "love", 29.9% to itself, and 16.8% to "I".

Each row adds up to 1.0 (i.e. 100%). This is what softmax ensures.

Now, we have the attention weights. It is time to compute the final output.

## Computing the Final Output (Attention Weights x V)

Now, we multiply the Attention Weight Matrix with the Value matrix `V` to get the final output.

```
Output = Attention Weights x V

```

```
Output = | 0.070  0.707  0.223 |     | 1  0  1 |
         | 0.333  0.333  0.333 |  x  | 1  2  0 |
         | 0.168  0.533  0.299 |     | 1  1  0 |

```

For "I":

- `0.070*1 + 0.707*1 + 0.223*1` = `1.000`
- `0.070*0 + 0.707*2 + 0.223*1` = `1.637`
- `0.070*1 + 0.707*0 + 0.223*0` = `0.070`

For "love":

- `0.333*1 + 0.333*1 + 0.333*1` = `0.999`
- `0.333*0 + 0.333*2 + 0.333*1` = `0.999`
- `0.333*1 + 0.333*0 + 0.333*0` = `0.333`

For "AI":

- `0.168*1 + 0.533*1 + 0.299*1` = `1.000`
- `0.168*0 + 0.533*2 + 0.299*1` = `1.365`
- `0.168*1 + 0.533*0 + 0.299*0` = `0.168`

```
Output = | 1.000  1.637  0.070 |   ← "I"
         | 1.000  1.000  0.333 |   ← "love"
         | 1.000  1.365  0.168 |   ← "AI"

```

Here, we can see that each word now has a new vector that is a weighted combination of the Value vectors of all words. The word "I" gets a new representation that is heavily influenced by the Value of "love" (because it had the highest attention weight of 0.707 for "love"). This is the power of the attention mechanism.

The output for each word is no longer just about that word alone. It now contains information from all the other words, weighted by how relevant they are. This is how the model understands context and relationships between words.

This was all about computing the final output. Now, let's put it all together.

## Putting It All Together

Let's summarize the entire computation in one place:

Step 1: Start with the input embeddings (X).

Step 2: Multiply X with weight matrices to get Q, K, and V.

Step 3: Compute attention scores by multiplying Q with the transpose of K (Q x K^T).

Step 4: Scale the scores by dividing by sqrt(d_k).

Step 5: Apply softmax to get attention weights (probabilities).

Step 6: Multiply attention weights with V to get the final output.

The entire process in one formula:

```
Attention(Q, K, V) = softmax(Q x K^T / sqrt(d_k)) x V

```

Now, every part of this formula is clear.

This is how the math behind Query, Key, and Value works in the Attention mechanism.

Every Large Language Model uses this exact computation at its core. The numbers we used were small for the sake of understanding, but in real models, the dimensions are much larger (512, 1024, or more) and the weight matrices are learned during training.

In real models, this Q, K, and V computation also runs many times in parallel, once per head. We have a detailed blog on Multi-Head Attention in Transformers that explains how these parallel heads work.

### Are the weight matrices for Q, K, and V set by hand?

No. In real models, the weight matrices `W_Q`, `W_K`, and `W_V` are learned during training. Simple hand-picked numbers are only used for the sake of understanding the math.

### Does scaling by sqrt(d_k) change which word gets the most attention?

No. Dividing by `sqrt(d_k)` does not change the relative order of the scores. It only makes the values smaller, so that softmax does not produce extreme values close to 0 or 1, which would make it difficult for the model to learn.

### Why do the attention weights in each row add up to 1?

Because softmax converts the scores into probabilities. Softmax is applied to each row, and it makes sure that every row adds up to 1.0, which is 100%. So, each weight tells us what share of its attention a word pays to every other word.

### Is the attention output of a word only about that word?

No. The output for each word is a weighted combination of the Value vectors of all words. It contains information from all the other words, weighted by how relevant they are. This is how the model understands context and relationships between words.

### Do real LLMs use the same attention computation with bigger numbers?

Yes. Every Large Language Model uses this exact computation at its core. In real models, the dimensions are much larger, like 512, 1024, or more. The Q, K, and V computation also runs many times in parallel, once per head.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# What is Self Attention in Transformers and How Does It Work?
URL: https://outcomeschool.com/blog/self-attention-in-transformers
Published: 2026-05-29
Author: Amit Shekhar

What is Self Attention in Transformers and How Does It Work?

# What is Self Attention in Transformers and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: May 29, 2026

Self Attention is the mechanism that lets every word in a sentence look at every other word in the same sentence to understand its meaning. It is the heart of modern Large Language Models like BERT and GPT.

In this blog, we will learn about Self Attention in Transformers. We will also see why we need it, what Query, Key, and Value are, how it works step by step with a simple example, and why it works so well.

We will cover the following:

- What is Self Attention?
- Why do we need Self Attention?
- Query, Key, and Value vectors
- Step-by-step working of Self Attention
- A simple example walk-through
- Why Self Attention works so well
- Multi-Head Self Attention
- Where Self Attention is used

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Self Attention?

Self Attention is a mechanism that allows every token in a sequence to look at every other token in the same sequence, including itself, to understand the context.

In simple words, Self Attention = Self + Attention. The word "Attention" means each token decides how much it should focus on the other tokens.

So, every word in a sentence looks at every other word in the same sentence and figures out which words matter the most for its meaning.

### Why do we need Self Attention?
[…727ln elided…]
- Seeing It with Real Numbers
- Putting It All Together

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Attention Formula (Quick Recap)

This scaling step lives inside the larger Transformer architecture. The formula for Scaled Dot-Product Attention is:

```
Attention(Q, K, V) = softmax(Q x K^T / sqrt(d_k)) x V

```

Here:

- `Q` is the Query matrix
- `K` is the Key matrix
- `V` is the Value matrix
- `d_k` is the dimension of the Key vector
- `sqrt(d_k)` is the square root of `d_k`

The part we are focusing on today is `/ sqrt(d_k)`. This is the scaling factor. We divide the dot product scores by the square root of the Key dimension before passing them to softmax.

Now, the question is: why do we need this scaling? The answer lies in understanding what happens without it.

## What Happens Without Scaling?

Let's say we skip the scaling step and compute attention directly as below:

```
Attention = softmax(Q x K^T) x V

```

In real Transformer models, `d_k` is 64, 128, or even larger. When `d_k` is large, the scores `Q x K^T` can become very large numbers (we will see why in the next section). And when we pass very large values into softmax, something bad happens.

The softmax function (which converts scores into probabilities) produces outputs that are extremely close to 0 and 1. One word gets almost all the attention (close to 1.0), and all other words get almost no attention (close to 0.0). The model stops spreading attention across multiple relevant words. It becomes too confident about one single word.

This is a big problem because:

- The model cannot learn from multiple words at once.
- The gradients (the signals used to update the model during training) become extremely small, almost zero. This is called the vanishing gradient problem.
- When gradients are too small, the model stops learning effectively.

So, here comes the scaling by `sqrt(d_k)` to the rescue.

Softmax has one more consequence worth knowing. Its outputs always add up to 1, so a token must give its full attention away even when nothing in the sentence deserves it. We have a detailed blog on Attention Sinks that explains where that leftover attention ends up.

But before we understand the solution, we must first understand why dot products grow when `d_k` increases.

## Why Do Dot Products Grow with dₖ?

The dot product of two vectors is computed by multiplying each pair of elements and then adding them all up.

Let's say we have two vectors `q` and `k`, each of dimension `d_k`:

```
dot_product = q_1*k_1 + q_2*k_2 + q_3*k_3 + ... + q_{d_k}*k_{d_k}

```

Here, we are adding `d_k` number of terms together.

Now, let's think about this simply. Each term `q_i * k_i` is a number. It can be positive or negative. When we add more and more of these numbers together, they do not always cancel out perfectly. Some add up, some cancel, but overall the total tends to grow in magnitude. The more dimensions we have, the more terms we add, and the larger the dot product can become.

For example, if `d_k = 4`, we are adding just 4 terms, so the dot product stays small. But if `d_k = 512`, we are adding 512 terms. Even though some positive and negative values cancel out, the sheer number of terms makes the total much larger in magnitude.

The dot product grows with `d_k`. This is the core problem. The larger the dimension, the larger the dot product, and the worse the softmax behaves.

Now, let's understand this more precisely using the concept of variance.

## Understanding Variance of the Dot Product

Do not worry, we will keep this simple.

Variance tells us how spread out a set of values can be from the average. A high variance means the values are far from the average. A low variance means the values stay close to the average.

Suppose we are measuring the height of students in a class. If all students are between 5.0 and 5.5 feet, the variance is low. If students range from 3.0 to 7.0 feet, the variance is high. Similarly, when we talk about the variance of the dot product, we are asking: how spread out can the dot product values be?

Now, let's assume that each element in the Query vector and the Key vector is a random number with:

- Mean (average) = 0
- Variance = 1

This is a standard assumption in machine learning. The input values are typically normalized to have zero mean and unit variance.

Now, what is the variance of one single product `q_i * k_i`?

When we multiply two independent random numbers, each with mean 0 and variance 1, the result has:

- Mean = 0
- Variance = 1 x 1 = 1 (we will see why in the next section)

So, each individual product `q_i * k_i` has a variance of 1.

Now, the dot product is the sum of `d_k` such products:

```
dot_product = q_1*k_1 + q_2*k_2 + ... + q_{d_k}*k_{d_k}

```

When we add `d_k` independent terms, each with variance 1, the total variance is:

```
Variance(dot_product) = d_k x 1 = d_k

```

This is the key insight. The variance of the dot product is equal to dₖ. The larger the `d_k`, the more spread out the dot product values become. And more spread out values cause problems for softmax.

## Proving It Step by Step: Variance of the Dot Product is dₖ

Now, let's prove why the variance equals `d_k`, step by step, for the sake of understanding. Do not worry, we will keep it simple.

We already know that the mean of our dot product is zero (because the average value of each `q_i` and `k_i` is zero).

Now, in general, variance is calculated as below:

```
Variance = Average of (value - mean)^2

```

But since our mean is zero, this becomes:

```
Variance = Average of (value - 0)^2
         = Average of value^2

```

So, when the mean is zero, the variance simplifies to the average of the squared values. This means we need to find the average of the squared dot product.

Now, let's see what happens when we square the dot product. Let's take a small example with `d_k = 3`:

```
dot_product = q_1*k_1 + q_2*k_2 + q_3*k_3

```

When we square this, we multiply the sum by itself. It is just like expanding `(a + b + c)^2`:

```
(a + b + c)^2 = a*a + a*b + a*c
              + b*a + b*b + b*c
              + c*a + c*b + c*c

```

Here, `a = q_1*k_1`, `b = q_2*k_2`, `c = q_3*k_3`. So we get 9 terms (3 x 3). Now, the key question is: what is the average value of each of these 9 terms?

These 9 terms fall into two groups:

Group 1: Terms where a term is multiplied by itself (like a*a, b*b, c*c)

These are the terms where the same pair is multiplied by itself. For example, `(q_1*k_1) * (q_1*k_1) = q_1^2 * k_1^2`. There are 3 such terms.

What is the average value of each? Let's use the variance formula we learned above. We know that:

```
Variance = Average of value^2    (when mean is zero)

```

Since `q_1` has mean 0 and variance 1:

```
1 = Average of q_1^2
Average of q_1^2 = 1

```

Similarly, since `k_1` has mean 0 and variance 1:

```
Average of k_1^2 = 1

```

Since `q_1` and `k_1` are independent, the average of their product is the product of their averages:

```
Average of (q_1^2 * k_1^2) = Average of q_1^2 * Average of k_1^2 = 1 * 1 = 1

```

Each of these terms has an average value of 1.

Group 2: Terms where different pairs are multiplied (like a*b, a*c, b*c)

These are the terms where two different pairs are mixed together. For example, `(q_1*k_1) * (q_2*k_2) = q_1 * k_1 * q_2 * k_2`. There are 6 such terms.

What is the average value of each? Since `q_1`, `k_1`, `q_2`, `k_2` are all independent, the average of their product is the product of their averages:

```
Average of (q_1 * k_1 * q_2 * k_2) = Average of q_1 * Average of k_1 * Average of q_2 * Average of k_2
                                    = 0 * 0 * 0 * 0
                                    = 0

```

Here, since each of them has an average (mean) of zero, the entire product becomes zero.

Each of these terms has an average value of 0.

Putting it together:

Out of 9 terms:

- 3 terms (Group 1) each contribute an average of 1
- 6 terms (Group 2) each contribute an average of 0

```
Variance = 3 * 1 + 6 * 0 = 3

```

And `d_k = 3`. So the variance equals `d_k`.

Now, this same logic works for any value of `d_k`. If `d_k = 64`, we get `64 * 64 = 4096` total terms. Out of these, 64 terms (Group 1) each contribute 1, and the remaining 4032 terms (Group 2) each contribute 0. So the variance is 64, which is exactly `d_k`.

The variance of the dot product is always exactly equal to dₖ. This is not an approximation. It is mathematically exact.

If we want to go deep into the math behind Q/K/V, self-attention, and the Transformer architecture from the ground up, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

## What Large Dot Products Do to Softmax

The softmax function converts a list of numbers into probabilities. The formula is:

```
softmax(x_i) = e^(x_i) / sum(e^(x_j) for all j)

```

Here, `e` is the mathematical constant (approximately 2.718).

Now, the important thing to understand is: `e^x` grows extremely fast as `x` increases. Let's see with real numbers to understand how fast it grows:

```
e^1   = 2.718
e^5   = 148.4
e^10  = 22,026
e^20  = 485,165,195
e^50  = 5,184,705,528,587,072,045

```

Here, we can see that the difference between `e^10` and `e^50` is astronomically large.

Now, let's say we have three attention scores: `[50, 10, 5]` (just for the sake of understanding how softmax behaves with large numbers). When we apply softmax:

```
e^50 = 5,184,705,528,587,072,045
e^10 = 22,026
e^5  = 148

softmax = [5,184,705,528,587,072,045 / total, 22,026 / total, 148 / total]

```

The first value completely dominates. The softmax output will be approximately `[1.0, 0.0, 0.0]`.

Now, compare this with smaller scores: `[5, 1, 0.5]`. When we apply softmax:

```
e^5   = 148.4
e^1   = 2.718
e^0.5 = 1.649

Sum = 152.780

softmax = [148.4/152.780, 2.718/152.780, 1.649/152.780]
        = [0.971, 0.018, 0.011]

```

Here, we can see that even with smaller scores, the first value still gets the most attention. But the other values are not completely zero. The model can still learn from all positions.

This is the problem. When `d_k` is large and we do not scale, the dot product scores become so large that softmax outputs become almost one-hot. One-hot means one value is 1.0 and the rest are 0.0. The model acts as if only one word matters and ignores everything else. The gradients vanish, and learning stops.

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

## Why √dₖ is the Right Scaling Factor

Now that we understand the problem, the solution becomes clear. We need to keep the dot product values small enough so that softmax can produce well-distributed attention weights.

We need to bring the variance of the dot product back to 1, regardless of how large `d_k` is.

We know that:

```
Variance(dot_product) = d_k

```

If we divide the dot product by some constant `c`, the variance becomes:

```
Variance(dot_product / c) = d_k / c^2

```

Note: When we divide a random variable by a constant `c`, the variance gets divided by `c^2` (not `c`). This is a standard rule in statistics. Let's understand why.

Variance measures how spread out values are from the mean. It is calculated using squared differences from the mean. So, when we divide all values by `c`, each difference from the mean also gets divided by `c`. But since variance squares those differences, the division by `c` becomes division by `c^2`.

Let's see with a simple example. Suppose we have three values: `[2, 4, 6]`.

```
Mean = (2 + 4 + 6) / 3 = 4

Differences from mean: [2-4, 4-4, 6-4] = [-2, 0, 2]

Squared differences: [4, 0, 4]

Variance = (4 + 0 + 4) / 3 = 2.67

```

Now, let's divide all values by `c = 2`. The new values are `[1, 2, 3]`.

```
New Mean = (1 + 2 + 3) / 3 = 2

Differences from mean: [1-2, 2-2, 3-2] = [-1, 0, 1]

Squared differences: [1, 0, 1]

New Variance = (1 + 0 + 1) / 3 = 0.67

```

Here, we can see that the original variance was `2.67` and the new variance is `0.67`. And `2.67 / 4 = 0.67`. We divided by `c = 2`, but the variance got divided by `c^2 = 4`.

This happens because variance uses squared differences. When each value shrinks by a factor of `c`, the squared differences shrink by a factor of `c^2`.

Now, coming back to our dot product. We had:

```
Variance(dot_product / c) = d_k / c^2

```

We want this variance to equal 1 so that the dot product values stay in a manageable range. So, we set:

```
d_k / c^2 = 1
c^2 = d_k
c = sqrt(d_k)

```

This is why we divide by `sqrt(d_k)`. It is the exact value that brings the variance back to 1.

After scaling:

```
Variance(dot_product / sqrt(d_k)) = d_k / d_k = 1

```

The scaled dot product values now have a variance of 1, meaning they stay in a manageable range regardless of how large `d_k` is. The softmax function receives reasonable inputs and produces well-distributed attention weights.

This is not an arbitrary choice. It is mathematically the correct scaling factor. The authors of the original "Attention Is All You Need" paper (the paper that introduced the Transformer architecture) chose this value for exactly this reason.

## Seeing It with Real Numbers

Now, let's see the effect of scaling with two different dimensions.

### Example 1: Small dimension (dₖ = 4)

Let's say we have:

```
q = [1, 0, 1, 0]
k = [0, 1, 1, 1]

```

```
dot_product = 1*0 + 0*1 + 1*1 + 0*1 = 1

```

```
sqrt(d_k) = sqrt(4) = 2

```

```
scaled_score = 1 / 2 = 0.5

```

The original score is `1`, the scaled score is `0.5`. Both values are small, so softmax will behave well in either case. Scaling does not matter much when `d_k` is small.

### Example 2: Large dimension (dₖ = 64)

Let's say we have three words with dot product scores: `[14, 10, 12]`.

Without scaling:

```
e^14 = 1,202,604
e^10 = 22,026
e^12 = 162,755

Sum = 1,387,386

softmax = [0.867, 0.016, 0.117]

```

Here, the first word gets 86.7% of the attention. The second word gets only 1.6%. The distribution is quite extreme even though the raw scores (14, 10, 12) are not that far apart.

With scaling (divide by sqrt(64) = 8):

Scaled scores: `[14/8, 10/8, 12/8]` = `[1.75, 1.25, 1.5]`

```
e^1.75 = 5.755
e^1.25 = 3.490
e^1.5  = 4.482

Sum = 13.727

softmax = [5.755/13.727, 3.490/13.727, 4.482/13.727]
        = [0.419, 0.254, 0.326]

```

Here, we can see the difference. After scaling, the attention is distributed much more evenly: 41.9%, 25.4%, and 32.6%. The model can now learn from all three words instead of focusing almost entirely on one word.

This is how scaling by `sqrt(d_k)` solves the problem.

## Putting It All Together

Let's summarize what we have learned:

The Problem: The dot product of the Query and Key vectors grows in magnitude as the dimension `d_k` increases. The variance of the dot product is equal to `d_k`. Large dot product values push softmax into extreme regions where it outputs values close to 0 or 1. This causes the vanishing gradient problem and the model stops learning.

The Solution: We divide the dot product by `sqrt(d_k)` before applying softmax. This brings the variance back to 1, keeping the scores in a manageable range regardless of the dimension size.

Why sqrt(d_k)? Because when we divide a value with variance `d_k` by `sqrt(d_k)`, the new variance becomes `d_k / d_k = 1`. It is mathematically the exact right value.

The full attention formula with scaling:

```
Attention(Q, K, V) = softmax(Q x K^T / sqrt(d_k)) x V

```

This single line, `/ sqrt(d_k)`, looks simple. But without it, the Transformer architecture would struggle to learn effectively, especially with larger dimensions. It is a small but very important detail that makes the entire attention mechanism work.

Now, we must have understood why we scale the dot product attention by √dₖ.

### Does scaling by sqrt(d_k) matter when d_k is small?

Not much. When `d_k` is small, the dot product stays small, so softmax behaves well with or without scaling. For example, with `d_k = 4`, a score of 1 becomes 0.5 after scaling, and both values are small. Scaling becomes important as `d_k` grows larger.

### Why do we divide by sqrt(d_k) and not some other number?

When we divide a value by a constant `c`, its variance gets divided by `c^2`. The variance of the dot product is `d_k`, so we need `d_k / c^2 = 1`, which gives `c = sqrt(d_k)`. It is the exact value that brings the variance back to 1.

### Is the variance of the dot product only approximately equal to d_k?

No. The variance of the dot product is exactly equal to `d_k`, not an approximation. This holds under the standard assumption that each element of the Query and Key vectors has mean 0 and variance 1, and the elements are independent.

### Who introduced the sqrt(d_k) scaling factor in attention?

The scaling factor comes from the original "Attention Is All You Need" paper, which introduced the Transformer architecture. The authors chose `sqrt(d_k)` because it is mathematically the correct value to keep the variance of the scores at 1.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-500 and 1228-1727 of 1727; 727 middle lines (35.8KB) elided. Read artifact://35 for full output]
