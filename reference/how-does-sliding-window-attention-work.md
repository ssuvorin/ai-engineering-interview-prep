> Source: https://outcomeschool.com/blog/how-does-sliding-window-attention-work

# How does Sliding Window Attention work?
URL: https://outcomeschool.com/blog/how-does-sliding-window-attention-work
Published: 2026-09-05

How does Sliding Window Attention work?

# How does Sliding Window Attention work?

Authors
: - Name
: Amit Shekhar
Published on
: September 5, 2026

Sliding Window Attention is a type of attention where each word looks only at a fixed number of nearby words, instead of looking at all the words. This keeps attention fast and cheap, even for very long text.

In this blog, we will learn about how sliding window attention works. We will also see why normal attention becomes slow and expensive for long text, and how sliding window attention comes to the rescue.

We will cover the following:

- What is attention?
- The problem with normal attention
- What is sliding window attention?
- A simple step-by-step walkthrough
- How information still travels far away
- Comparing normal attention and sliding window attention
- Where sliding window attention is used
- Advantages and trade-offs

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is attention?

Before we learn about sliding window attention, we must first understand what attention means.

A modern language model, like the one behind a chatbot, reads text and tries to predict the next word. To do this well, it must understand how words connect to each other.

Let's say we read this sentence:

> The cat sat on the mat because it was tired.

Now, the word `it` refers to the `cat`. As humans, we know this without thinking. But a model has to figure it out.

Attention is the mechanism a model uses to look back at earlier words and decide which ones matter for understanding the current word.

In simple words, attention lets every word "pay attention" to other words in the text.

Let's use a simple analogy. Imagine we are in a classroom, and each student is a word. When a new student speaks, that student looks around the room to see who else is relevant to the topic. The new student listens more carefully to some students and ignores others. This act of looking around and deciding who to listen to is attention.

So, attention is how a word gathers information from other words.

Now, we have understood attention. Let's see the problem with it.

### The problem with normal attention

In normal attention, every word looks at every other word. This is called full attention, because nothing is left out.

Let's understand this with our classroom analogy again.

Suppose there are 10 students in the room. When a new student speaks, that student looks at all 10 students. That is fine. The room is small.

But now, suppose there are 10,000 students in a giant hall. When a new student speaks, that student must still look at all 10,000 students. This becomes very slow and tiring.

This is exactly the problem with normal attention.

Let's put it in numbers. If we have a piece of text with `100` words, then each word looks at `100` words. So the total number of connections is `100 x 100`, which is `10,000`.

Now, suppose the text has `1,000` words. Then the total connections become `1,000 x 1,000`, which is `1,000,000`.

Here, we can notice that when the text gets 10 times longer, the work becomes 100 times bigger.

This is because the cost grows with the square of the number of words. In simple words, doubling the text makes the work four times bigger. Making the text 10 times longer makes the work 100 times bigger.

So, full attention works perfectly for short text. But for very long text, like a full book or a long document, it becomes extremely slow and uses a huge amount of memory.

We needed a solution for that, and sliding window attention was introduced to solve this problem.

### What is sliding window attention?

Let's break the term down.

Sliding Window Attention = Sliding + Window + Attention

A window is a small range of nearby words. Instead of looking at all words, a word only looks at a fixed number of words around it.

Sliding means this window moves along as we move from one word to the next. Each word has its own window centered on its neighbors.

So, sliding window attention is a method where every word only pays attention to a small, fixed number of nearby words, instead of all the words in the text.

Let's go back to our classroom analogy.

Earlier, when a new student spoke, that student looked at all 10,000 students. That was the slow part.

Now, with sliding window attention, the student only looks at the few students sitting nearby. For example, the student looks at the 3 students on the left and the 3 students on the right. That is it.

This small group of nearby students is the window.

When the next student speaks, that student also looks at their own nearby students. So the window slides along the room, one seat at a time.

This is the core idea. A word does not look at everyone. A word looks only at its neighbors.

The size of this window is fixed. We choose a number, for example `4`, `512`, or `4096`. This number is called the window size. It tells us how many nearby words each word is allowed to look at.

Now, the work no longer grows with the square of the text length. Instead, it grows in a straight line with the text length. If the text becomes 10 times longer, the work becomes only 10 times bigger, not 100 times bigger.

So, here comes sliding window attention to the rescue.

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

### A simple step-by-step walkthrough

The best way to learn this is by taking an example.

Let's say we have a short sentence with 6 words. We will give each word a number so it is easy to follow:

```
Position:  1    2    3    4    5    6
Word:      I    love  to   learn  new  things

```

Here, we have 6 words placed at positions 1 to 6.

Now, let's choose a small window size. For the sake of understanding, assume that each word can look at itself and the 2 words before it. So the window covers 3 words at a time.

Note: In a chatbot, a word usually looks only at past words and itself, not at future words, because the model reads from left to right and predicts the next word. So in our example, each word looks backward.

We have a detailed blog on Causal Masking in Attention that explains how a model blocks future words step by step.

Let's now go word by word and see which words each one pays attention to.

Position 1 (`I`): There are no words before it. So `I` looks only at itself.

Position 2 (`love`): It looks at itself and one word before it. So `love` looks at `I` and `love`.

Position 3 (`to`): It looks at itself and the 2 words before it. So `to` looks at `I`, `love`, and `to`.

Position 4 (`learn`): The window now slides. So `learn` looks at `love`, `to`, and `learn`. Notice that `I` is now outside the window.

Position 5 (`new`): It looks at `to`, `learn`, and `new`.

Position 6 (`things`): It looks at `learn`, `new`, and `things`.

Here, we can see that the window slides forward by one position each time. Every word looks at a small, fixed group of nearby words.

Let's see it as below:

```
Words:     I    love   to   learn  new  things
Position:  1     2     3     4     5     6

Pos 1:   [ I ]
Pos 2:   [ I    love ]
Pos 3:   [ I    love   to ]
Pos 4:         [ love   to    learn ]
Pos 5:                [ to    learn  new ]
Pos 6:                      [ learn  new   things ]

```

Here, we can see that each row is the window for one word. The box holds the small group of words that the current word looks at. At position 4, the window has moved forward and `I` has dropped out. The box keeps sliding one step to the right, one word at a time.

This is how sliding window attention keeps the work small and steady.

Now, a very natural question comes to mind. If a word only looks at its neighbors, how does it ever connect to words that are far away?

Do not worry, we will learn about that next.

### How information still travels far away

This is the most beautiful part of sliding window attention.

At first, it looks like a problem. Word number 100 cannot directly look at word number 1, because word 1 is far outside its window. So how can far away words still connect?

The answer is layers.

A modern model is not a single step. It is made of many layers stacked on top of each other. A layer is one full round of attention. The output of one layer becomes the input of the next layer.

We have a detailed blog on Decoding Transformer Architecture that covers how these layers are stacked end to end.

Let's understand this with a simple chain analogy.

Suppose information can only pass between neighbors who are sitting next to each other.

In layer 1, student A whispers to student B, who is sitting right next to A. Student B now knows a little about A.

In layer 2, student B whispers to student C. Now C knows a little about B, and since B already knew about A, C indirectly learns a little about A too.

In layer 3, student C whispers to student D. Now D indirectly learns about A as well.

So, even though no one talks to a far away person directly, information slowly travels across the whole room, one neighbor at a time, through the layers.

Here is the flow:

```
            A     B     C     D

Layer 1:    A --> B
                  B --> C
                        C --> D

Layer 2:    A ......... C  (A reaches C through B)
                  B ......... D  (B reaches D through C)

Layer 3:    A ............... D  (A reaches D through B and C)

```

Here, we can see that in layer 1 each person only talks to a direct neighbor. After layer 2, A has reached C. After layer 3, A has reached D, even though A and D never talked directly. The dotted lines show the indirect path that information takes through the layers.

This is exactly how sliding window attention reaches far away words.

Let's put a simple number to it. Suppose the window allows a word to look 4 words back in each layer. With 1 layer, a word reaches 4 words back. With 2 layers, it reaches about 8 words back. With 10 layers, it reaches about 40 words back.

So, the more layers we stack, the farther the information can travel.

In simple words, one layer connects nearby words directly, and many layers connect far away words indirectly.

The problem is solved.

To learn the Attention Mechanism, Transformer Architecture, and LLM Internals, and to build a Large Language Model (LLM) from scratch, check out our AI and Machine Learning Program at Outcome School.

### Comparing normal attention and sliding window attention

Let me tabulate the differences between normal attention and sliding window attention for your better understanding.

| Point | Normal attention | Sliding window attention |
| --- | --- | --- |
| What each word looks at | Every other word | Only nearby words in a fixed window |
| Cost as text grows | Grows with the square of the length | Grows in a straight line with the length |
| Speed on long text | Slow | Fast |
| Memory on long text | Very high | Low |
| Far away connections | Direct, in a single layer | Indirect, through many layers |
| Best for | Short text | Long text |

Here, we can see that normal attention is powerful but expensive. Sliding window attention is lighter and scales nicely for long text.

So, now we know where each one fits.

### Where sliding window attention is used

Sliding window attention is used in many modern language models that need to handle long inputs.

The reason is simple. When we want a model to read a very long input, full attention becomes too slow and too costly. Sliding window attention lets the model handle that long input quickly while still understanding the overall meaning through its layers.

A real use case is a chatbot that remembers a long conversation. The conversation can grow very long over time. With sliding window attention, the model can keep up without slowing down too much. It also stops the model's memory of the conversation from growing without limit, which is why a sliding window shows up as one of the KV Cache Compression techniques.

Another real use case is reading a long legal document or a long book. The model can process page after page efficiently, because each word only looks at its neighbors directly and reaches far away words through layers.

This is how sliding window attention makes long text practical.

If we want to go deep into how long inputs are served efficiently, we cover KV Cache, Paged Attention, Grouped Query Attention, and vLLM in depth in our AI and Machine Learning Program at Outcome School.

### Advantages and trade-offs

Now, let's summarize the good parts and the things we must keep in mind.

- It is much faster on long text, because the work grows in a straight line instead of the square of the length.
- It uses much less memory, which means we can handle longer inputs on the same hardware.
- It still understands long range connections, through the stacking of many layers.
- It is simple to reason about, because each word focuses on a clear, fixed neighborhood.

- Far away words are connected only indirectly, through layers. So we need enough layers and a reasonable window size for distant information to travel well.
- A very small window with very few layers can miss some long range connections. We must choose the window size based on our use case.
- For short text, full attention is already fast enough, so sliding window attention gives little benefit there.
- If the window slides far enough that the very first tokens fall out, the quality can collapse, because those tokens act as attention sinks that soak up the leftover attention.

So, sliding window attention is the right choice when the text is long. For short text, normal full attention works perfectly well.

This way we can use sliding window attention to solve the problem of long text in a very simple way. A word looks only at its neighbors, the window slides along, and many layers carry information across the whole text.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# How do Attention Sinks work?
URL: https://outcomeschool.com/blog/how-do-attention-sinks-work
Published: 2026-09-05
Author: Amit Shekhar

How do Attention Sinks work?

# How do Attention Sinks work?

Authors
: - Name
: Amit Shekhar
Published on
: September 5, 2026

Attention sinks are the first few tokens of the text that always get a huge share of the attention in a Large Language Model. If we keep these tokens while dropping the old ones, the model can handle very long conversations without breaking.

In this blog, we will learn about how attention sinks work in Large Language Models. We will also see why streaming long conversations becomes a problem, why the first tokens become a sink that the naive fix breaks, and how StreamingLLM uses attention sinks in the real world to keep models running.

We will cover the following:

- What is a Large Language Model?
- What is attention?
- The problem of streaming with long conversations
- The naive fix and why it fails
- What is an attention sink?
- Why the first tokens become a sink
- A step-by-step numeric walkthrough
- The fix in code
- StreamingLLM and modern attention sinks
- Importance of attention sinks

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a Large Language Model?

Before jumping into attention sinks, we must know what a Large Language Model is.

A Large Language Model is an AI model that reads text and predicts the next word.

In simple words, it is a very good guessing machine. We give it some words, and it guesses the word that comes next. Then it adds that word and guesses again. It keeps doing this, one word at a time.

Let's say we type "The sky is". The model guesses "blue". Now the text becomes "The sky is blue". The model reads all of it again and guesses the next word. This is how a model like ChatGPT writes long answers, one word after another.

Note: The model actually works with small pieces of words called tokens. A token can be a full word, a part of a word, or even a single letter. For the sake of understanding, we can think of a token as a word.

This is how a Large Language Model works. Now, let's understand attention.

### What is attention?

When the model guesses the next word, it does not look at all the past words equally. Some past words matter more than others.

Attention is the method the model uses to decide which earlier words to focus on while guessing the next word.

In simple words, attention is like focus. When we read a sentence, we focus on the important words and ignore the rest. The model does the same thing.

Let's say we have the sentence "Amit kept his keys on the table, and later he could not find them."

To understand the word "them", the model must focus back on the word "keys". That focusing is attention. The model gives a high score to "keys" and low scores to the other words.

So, attention is just a set of scores. Each past word gets a score that says how important it is for the current word. A high score means high focus. A low score means low focus.

One very important rule: all these scores must add up to 1. This is like sharing one full pie among all the past words. If one word takes a big slice, the others get smaller slices. The model is forced to give away the full pie every single time.

This is how attention works. Now, let's see the problem that creates the need for attention sinks.

### The problem of streaming with long conversations

Suppose we are building a chatbot. We want to talk to it for hours and hours without restarting it. The conversation keeps growing longer and longer.

Here is the catch. The model has a limit on how many words it can hold in its memory at once. We call this the context window.

In simple words, the context window is the size of the model's short-term memory. If the limit is 4000 words, the model can only keep the last 4000 words in mind.

When the conversation crosses this limit, we have a problem. We must remove some old words to make room for new ones. If we do not remove them, the model runs out of memory and slows down or crashes.

We have a detailed blog on KV Cache in LLMs that explains why this memory keeps growing with every new word.

So, the question is: which old words do we throw away?

### The naive fix and why it fails

The most obvious idea is simple. When memory is full, throw away the oldest words and keep only the most recent ones. This is called a sliding window.

In simple words, a sliding window keeps a window of recent words and lets the old ones fall off the back, like a moving train window where old scenery slides away.

Let's say the window holds 4 words. The conversation is:

```text
Word1 Word2 Word3 Word4 Word5 Word6

```

When Word5 arrives, we drop Word1. When Word6 arrives, we drop Word2. We always keep the latest 4 words.

Let's visualize this as below:

```text
Window holds 4 words. New words enter on the right.

Start:     [ Word1 Word2 Word3 Word4 ]
                ^
                first word

Word5 in:  Word1 dropped
           [ Word2 Word3 Word4 Word5 ]

Word6 in:  Word2 dropped
           [ Word3 Word4 Word5 Word6 ]

```

Here, we can see that the oldest word falls off the left every time a new word enters on the right. Word1, the very first word, is the first one to be thrown away.

[…222ln elided…]

### How many sink tokens should we keep in a streaming window?

Keeping just the first 4 tokens as sinks is usually enough to keep the model stable. We join these sink tokens with a sliding window of recent tokens and throw away only the middle. This way, the leftover attention always has a home.

### Does StreamingLLM use more memory as the conversation grows?

No. StreamingLLM keeps a few sink tokens plus a sliding window of recent tokens, so it uses only a small, fixed amount of memory. With this, a model can handle millions of words of conversation without crashing or turning to nonsense.

### What is the difference between the first-token sink and a learnable attention sink?

A learnable attention sink is a special, dedicated token that the model is trained to dump extra attention onto. Instead of borrowing the first real word as a drain, the model gets its own private drain that holds no meaning. This is even cleaner, because the drain is no longer mixed up with a real word.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

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

[Showing lines 1-416 and 639-1066 of 1066; 222 middle lines (10.8KB) elided. Read artifact://71 for full output]
