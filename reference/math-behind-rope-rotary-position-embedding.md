> Source: https://outcomeschool.com/blog/math-behind-rope-rotary-position-embedding

# What is RoPE (Rotary Position Embedding)? The Math Behind It
URL: https://outcomeschool.com/blog/math-behind-rope-rotary-position-embedding
Published: 2026-04-23
Author: Amit Shekhar

What is RoPE (Rotary Position Embedding)? The Math Behind It

# What is RoPE (Rotary Position Embedding)? The Math Behind It

Authors
: - Name
: Amit Shekhar
Published on
: April 23, 2026

RoPE (Rotary Position Embedding) is a way to give position information to a Transformer. It rotates the Query (Q) and Key (K) vectors by an angle that depends on the token's position, so that attention depends on the relative distance between tokens.

In this blog, we will learn about the math behind Rotary Position Embedding (RoPE) and why it is used in modern Large Language Models.

Today, we will cover the following topics:

- The Big Picture
- Why a Transformer Needs Position Information
- Older Approaches and Their Problems
- The Core Idea Behind RoPE
- The 2D Rotation Math
- How RoPE Is Applied to Q and K
- Why the Dot Product Captures Relative Position
- A Small Numeric Example
- Real-World Use Cases
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

A Transformer reads all the tokens in a sentence at the same time. It does not know which word came first and which came last. So, we have to give it position information separately. RoPE is a clever way to do that. Instead of adding a position vector, RoPE rotates the Query and Key vectors based on their position. After the rotation, the dot product between any two tokens automatically reflects the relative distance between them.

In simple words:

RoPE = Rotate the Q and K vectors by an angle that depends on the token's position.

This makes the attention score depend only on the relative distance between two tokens, which is exactly what we want.

We have a detailed blog on Math Behind Attention: Q, K, V that explains how Q, K, and V are used inside attention.

## Why a Transformer Needs Position Information

A Transformer processes all the tokens in a sentence in parallel. It does not read them one by one like we do.

We have a detailed blog on Transformer Architecture that explains how a Transformer works end to end.

Let's see why this is a problem.

Consider these two sentences:

- "The cat chased the dog."
- "The dog chased the cat."

Both sentences contain the exact same words. The only difference is the order. To us, the meaning is completely different. But, to a raw Transformer, both look the same. It has no idea who chased whom.

We need to inject position information into the model so that it knows the order of the words.

## Older Approaches and Their Problems

There are two well-known older approaches to add position information.

Approach 1: Sinusoidal Positional Encoding. This is the original method from the "Attention Is All You Need" paper. We compute a fixed vector for each position using sine and cosine functions. We add this vector to the token embedding before feeding it into the model.

Approach 2: Learned Positional Embeddings. Instead of using a fixed formula, we let the model learn a separate embedding for each position. We add this learned vector to the token embedding.

Both approaches share two big problems.

- They use addition. The position vector is added to the token embedding. This mixes position information into the meaning of the word, and the two end up competing inside the same vector.
- They do not encode relative distance. With absolute positional embeddings, the model has to learn from scratch how every pair of positions relates. There is no built-in structure that says "positions 5 and 10" have the same relationship as "positions 105 and 110".
- They struggle with longer sequences. If the model was trained on sequences of length 2048 and we suddenly give it 8192 tokens at inference time, learned embeddings have nothing to fall back on. Sinusoidal encoding can technically extrapolate, and the original "Attention Is All You Need" paper actually proposed it partly for this reason. But, later research showed that this property does not hold up well in practice.

We need a smarter way. We need a method that handles position more cleanly and works at any sequence length.

So, here comes RoPE to the rescue.

## The Core Idea Behind RoPE

The full form of RoPE is Rotary Position Embedding.

Let's decompose the name:

RoPE = Rotary + Position + Embedding.

- Position means we are encoding the position of a token.
- Embedding means we are doing this inside the vector space the model uses. Learn more about Embeddings: Embeddings in Machine Learning
- Rotary means we are using rotation as the encoding mechanism.

The idea is simple. Instead of adding a position vector to the token embedding, we rotate the Query and Key vectors by an angle that depends on the token's position. The further along a token is in the sequence, the more we rotate its vector.

The magic is in the dot product. When we compute the attention score `Q · K`, the rotations combine in a way that the result depends only on the difference in positions between the two tokens, not on their absolute positions.

So, RoPE gives us relative position information for free through the dot product.

Let's take a real-world analogy. Think of each pair of dimensions inside a token's vector as a clock hand. (We will see in a later section that the vector is split into many such pairs, each acting as its own clock at its own speed.) A token at position 1 rotates the hand to "1 o'clock". A token at position 5 rotates it to "5 o'clock". When we compare two tokens, we are not asking "where does each hand point?" - we are asking "how many hours apart are the two hands?". That is exactly the relative-position information attention needs.

## The 2D Rotation Math

To understand RoPE, we must first understand how rotation works in 2D.

Suppose we have a 2D vector `v = [x, y]`. We want to rotate it by an angle `θ` (theta). The new vector `v'` is:

```
x' = x * cos(θ) - y * sin(θ)
y' = x * sin(θ) + y * cos(θ)

```

This is the standard 2D rotation. We can write it as a matrix multiplication:

```
| x' |   | cos(θ)  -sin(θ) |   | x |
|    | = |                 | * |   |
| y' |   | sin(θ)   cos(θ) |   | y |

```

That is the rotation matrix. It rotates any 2D vector by angle `θ` while keeping its length unchanged.

Here is a simple ASCII diagram showing the rotation.

```
                  y
                  |
                  |     v'
                  |    /
                  |   /
                  |  /
                  | /  θ
                  |/___________ v
                  +------------- x

```

Here, the vector `v` starts along the x-axis. After rotating by angle `θ`, it becomes `v'`. The length of the vector stays the same. Only the direction changes.

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

## How RoPE Is Applied to Q and K

Now, let's see how this rotation is used inside attention.

We have a Query vector `Q` and a Key vector `K`. These are not 2D vectors. They have many dimensions, often 64 or 128.

RoPE works on these high-dimensional vectors by splitting them into pairs of 2D vectors. If `Q` has 64 dimensions, we treat it as 32 pairs of 2D vectors. Each pair gets its own rotation.

For a token at position `m`, RoPE rotates each pair by an angle `m * θ_i`, where `θ_i` is a fixed frequency that depends on which pair we are looking at.

Here is a simple ASCII diagram showing how a Q vector with `d = 8` dimensions is split and rotated.

```
Q = [ q_1, q_2 | q_3, q_4 | q_5, q_6 | q_7, q_8 ]
      \______/   \______/   \______/   \______/
       pair 1     pair 2     pair 3     pair 4
         |           |           |           |
         v           v           v           v
      rotate      rotate      rotate      rotate
      by m*θ_1    by m*θ_2    by m*θ_3    by m*θ_4
      (fastest)                           (slowest)

```

Here, the 8-dimensional vector is split into 4 pairs. Each pair is rotated by its own angle, and the rotation amount also scales with the token's position `m`.

The standard formula for the frequencies is:

```
θ_i = 10000^(-2(i-1)/d)    for i = 1, 2, ..., d/2

```

Here, `d` is the per-head dimension. For the first pair this gives `θ_1 = 1` (largest, fastest rotation). For the last pair, with `d = 128` (a common per-head size), this gives `θ_(d/2) ≈ 0.0001` (smallest, slowest rotation). So, low-index pairs rotate fast and high-index pairs rotate slowly. This is similar to how sinusoidal positional encoding uses many frequencies, but here the frequencies are applied as rotations, not as added vectors.

Note: This formula is the exact knob that long-context techniques like YaRN and NTK-aware scaling tune. They modify these frequencies so a model trained on shorter sequences can handle much longer ones at inference.

After applying RoPE, the rotated `Q` for a token at position `m` is `R_m * Q`, where `R_m` is the rotation matrix for position `m`. Similarly, the `K` vector at position `n` gets its own rotation `R_n * K`.

Note: The original RoPE paper presents the splitting as consecutive pairs `(q_1, q_2), (q_3, q_4), ...` as shown above. In real-world implementations like LLaMA and Mistral, the splitting is done as `(q_i, q_(i + d/2))` - the first half of the vector paired with the second half. Both schemes are mathematically equivalent. They are just a permutation of dimensions, so the explanation here applies to either.

Note: RoPE is applied only to the Query and Key vectors. The Value vector `V` is left untouched. This is because the relative-position property we want comes from the `Q · K` dot product. The `V` vector is just the content being weighted by attention scores, so it does not need any position information.

To learn positional encodings, Q/K/V matrices, and the Transformer architecture in depth, check out our AI and Machine Learning Program at Outcome School.

## Why the Dot Product Captures Relative Position

This is where the magic happens.

When we compute the attention score between a query at position `m` and a key at position `n`, we calculate:

```
score = (R_m * Q) · (R_n * K)

```

Because of how rotation matrices work, this expression simplifies to:

```
score = Q · (R_(n-m) * K)

```

This works because rotation matrices are orthogonal, which means `R_m^T = R_(-m)`. The intuition is simple: rotating by `-m` undoes a rotation by `m`. So, rotating by `-m` and then by `n` combines into a single rotation by `n - m`. The full derivation is just one line of matrix algebra:

```
(R_m * Q) · (R_n * K) = Q^T * R_m^T * R_n * K
                      = Q^T * R_(-m) * R_n * K
                      = Q^T * R_(n-m) * K
                      = Q · (R_(n-m) * K)

```

The `m` rotation on `Q` effectively cancels, leaving a single net rotation by `n - m` on `K`.

The score depends only on `n - m`, which is the relative distance between the two tokens. The absolute positions `m` and `n` disappear from the formula.

This is the beauty of RoPE. The model does not see "token at position 5" and "token at position 12". Instead, it sees "these two tokens are 7 positions apart". This relative view of position is exactly what attention needs.

Let's see why this matters with a concrete example. Consider these two sentences:

- "The cat sat on the mat."
- "Yesterday, the cat sat on the mat."

In sentence 1, "cat" is at position 2 and "mat" is at position 6. The distance between them is 4.

In sentence 2, "cat" is at position 3 and "mat" is at position 7. The distance is again 4.

The relationship between "cat" and "mat" is identical in both sentences. They are 4 words apart, and the meaning of how they relate is the same. The fact that the whole sentence shifted by one word does not change anything about how "cat" relates to "mat".

Now, what if we used absolute positions instead? The model would have to separately learn:

- How (cat at pos 2) relates to (mat at pos 6)
- How (cat at pos 3) relates to (mat at pos 7)
- How (cat at pos 100) relates to (mat at pos 104)
- And so on, for every possible pair

That is wasteful. All of these are the same relationship - "two specific words, 4 positions apart". RoPE lets the model learn this once, and reuse it everywhere.

Going back to our clock analogy, when we look at two clock hands, we do not need to know what time each one shows individually. We only care about the angle between them. RoPE gives the model the same view of position.

Note: This relative-position property comes out of the math automatically. We did not design the model to learn relative positions. The rotation operation gives it to us for free.

## A Small Numeric Example

Let's put this into perspective with a small example.

Suppose we have a 2D Query vector `Q = [1, 0]` for the token at position `m = 1`. Let `θ = π / 4` (45 degrees).

The rotation matrix at position 1 is:

```
R_1 = | cos(π/4)  -sin(π/4) |   | 0.707  -0.707 |
      |                     | = |               |
      | sin(π/4)   cos(π/4) |   | 0.707   0.707 |

```

The rotated Query is:

```
R_1 * Q = | 0.707  -0.707 |   | 1 |   | 0.707 |
          |               | * |   | = |       |
          | 0.707   0.707 |   | 0 |   | 0.707 |

```

Now, suppose we have a Key vector `K = [1, 0]` at position `n = 2`. The rotation angle is `2 * π/4 = π/2`.

```
R_2 = | cos(π/2)  -sin(π/2) |   | 0  -1 |
      |                     | = |       |
      | sin(π/2)   cos(π/2) |   | 1   0 |

```

The rotated Key is:

```
R_2 * K = | 0  -1 |   | 1 |   | 0 |
          |       | * |   | = |   |
          | 1   0 |   | 0 |   | 1 |

```

The attention score is the dot product:

```
score = (R_1 * Q) · (R_2 * K)
      = 0.707 * 0 + 0.707 * 1
      = 0.707

```

So, the score for two tokens at a relative distance of `1` is `0.707`.

Now, let's verify the relative-position property. Let's pick a different pair with the same relative distance: `m = 2, n = 3`.

The rotated Query at position 2 uses the same `R_2` matrix from before:

```
R_2 * Q = | 0  -1 |   | 1 |   | 0 |
          |       | * |   | = |   |
          | 1   0 |   | 0 |   | 1 |

```

The rotated Key at position 3 uses angle `3 * π/4`:

```
R_3 * K = | cos(3π/4)  -sin(3π/4) |   | 1 |   | -0.707 |
          |                       | * |   | = |        |
          | sin(3π/4)   cos(3π/4) |   | 0 |   |  0.707 |

```

The attention score:

```
score = (R_2 * Q) · (R_3 * K)
      = 0 * (-0.707) + 1 * 0.707
      = 0.707

```

The score is `0.707` again. The absolute positions changed from `(1, 2)` to `(2, 3)`, but the relative distance stayed at `1`, so the score stayed at `0.707`. This is exactly the property RoPE was designed to give us.

## Real-World Use Cases

RoPE has become the standard for positional encoding in modern Large Language Models. Let's see where RoPE is used in practice.

- LLaMA family. All LLaMA models from Meta use RoPE.
- Mistral and Mixtral. Both use RoPE for positional encoding.
- Qwen. Alibaba's Qwen models use RoPE.
- DeepSeek. DeepSeek models use RoPE as well.
- Gemma. Google's open-weight Gemma models use RoPE.

Note: RoPE is also the foundation for many long-context techniques. Methods like YaRN, Position Interpolation, and NTK-aware scaling all extend RoPE so that a model trained on, say, 4K tokens can be used on 32K or 128K tokens at inference time. None of this would be possible if we were still using learned positional embeddings.

## Quick Summary

Let's recap what we have decoded:

- A Transformer reads all tokens in parallel. It does not naturally know the order of words, so we must inject position information.
- Older methods add a position vector to the token embedding. Sinusoidal encoding and learned embeddings lack built-in relative-distance structure and struggle with longer sequences.
- RoPE rotates the Q and K vectors instead of adding to them. The rotation angle depends on the token's position.
- The high-dimensional vector is split into pairs. Each pair is rotated by its own frequency.
- The dot product of two rotated vectors depends only on relative position. This gives us relative position information for free.
- No learned parameters. RoPE itself introduces no additional learned parameters, unlike learned positional embeddings.
- RoPE is the standard in modern LLMs. LLaMA, Mistral, Qwen, DeepSeek, and Gemma all use it.
- RoPE makes long-context extension possible. Techniques like YaRN and Position Interpolation rely on RoPE's structure.

This is how RoPE gives modern Large Language Models a clean, scalable, and elegant way to understand position.

### Is RoPE applied to the Value vector too?

No. RoPE is applied only to the Query and Key vectors, and the Value vector is left untouched. The relative-position property comes from the `Q · K` dot product. The Value vector is just the content being weighted by the attention scores, so it does not need any position information.

### Does RoPE add any learned parameters to the model?

No. RoPE itself introduces no additional learned parameters. The rotation angles come from a fixed frequency formula and the token's position. This is different from learned positional embeddings, where the model learns a separate embedding for each position.

### Can a model with RoPE handle longer text than it was trained on?

Yes, with the help of long-context techniques built on top of RoPE. Methods like YaRN, Position Interpolation, and NTK-aware scaling extend RoPE so that a model trained on, say, 4K tokens can be used on 32K or 128K tokens at inference time.

### Does rotating the Query and Key vectors change their length?

No. A rotation keeps the length of the vector unchanged, and only its direction changes. RoPE uses this rotation as the encoding mechanism, instead of adding a position vector that mixes position into the meaning of the word.

### Does it matter how the vector is split into pairs?

No. The original RoPE paper splits the vector into consecutive pairs, while implementations like LLaMA and Mistral pair the first half of the vector with the second half. Both schemes are mathematically equivalent, since they are just a permutation of dimensions.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

Our vision is to make tech education outcome-focused. Our mission is to help students master the internals and become great at system design to achieve the outcome they aspire to.
