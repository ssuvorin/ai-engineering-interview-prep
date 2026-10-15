> Source: https://outcomeschool.com/blog/self-attention-in-transformers

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

The best way to learn this is by taking an example.

Consider the sentence:

> The animal did not cross the street because it was too tired.

Now, the question is: what does the word `it` refer to?

As humans, we know that `it` refers to `the animal`, because the animal was too tired to cross.

Now, let's read one more sentence:

> The animal did not cross the street because it was too wide.

Same structure. Same word `it`. But now, what does `it` refer to?

Here, `it` refers to `the street`, because the street was too wide.

We changed just one word - from `tired` to `wide` - and the meaning of `it` completely changed.

So, how did our brain figure that out? Our brain looked at the surrounding words to understand the meaning of `it`. The word `tired` pulled our attention towards `the animal`. The word `wide` pulled our attention towards `the street`.

This is exactly what happens inside the Large Language Model. Every word looks at every other word in the same sentence to understand its meaning. The model gives more attention to the words that matter and less attention to the words that do not matter. This mechanism is called Attention.

Now, notice that every word here is looking at the other words within the SAME sentence. The sentence is attending to itself. This is why we call it Self Attention.

In the first sentence, `it` pays strong attention to `animal`. In the second sentence, `it` pays strong attention to `street`. That is how the model captures the true meaning of `it` in both cases.

Without Self Attention, the word `it` would just be a generic token with no real meaning. And Self Attention is the core idea behind every modern Large Language Model.

### Query, Key, and Value vectors

For every token, Self Attention needs to answer two questions:

- Which other tokens in this sentence are important for me?
- How much should I focus on each of them?

To answer these questions, we create three vectors for every input token:

- Query (Q): what this token is looking for.
- Key (K): what this token offers to others.
- Value (V): the actual information this token carries.

The word "Self" in Self Attention comes from one very important fact:

> Query, Key, and Value all come from the SAME input sequence.

This is what makes it "Self" Attention. The same sequence creates the questions, the same sequence creates the keys to match those questions, and the same sequence provides the values. The sequence is attending to itself.

In simple words, if our input sentence is "The animal did not cross the street", then Q, K, and V are all derived from "The animal did not cross the street" itself.

We have a detailed blog on the Math behind Attention - Q, K, and V that covers this in depth.

Note: This is the key difference between Self Attention and Cross Attention. In Cross Attention, the Query comes from one sequence and the Key and Value come from another sequence. But in Self Attention, all three come from the same sequence.

For the sake of understanding, let's take an analogy.

Suppose we are in a library and we are looking for a book on machine learning.

- The Query is the topic we are searching for: "machine learning".
- The Key is the label written on every book on the shelf.
- The Value is the actual content inside the book.

We compare our Query with every Key. The Keys that match our Query give us the most relevant Values.

Self Attention works in the same way.

### Step-by-step working of Self Attention

Now, it's time to learn the exact steps of Self Attention.

Step 1: We start with the input embeddings. Every token in the sentence is converted into a vector.

Step 2: We create three vectors for every token by multiplying the embedding with three different weight matrices.

- Q = Input x W_Q
- K = Input x W_K
- V = Input x W_V

Here, `W_Q`, `W_K`, and `W_V` are weight matrices that the model learns during training.

Step 3: We compute the dot product of `Q` with the transpose of `K`. This is a matrix multiplication that gives us the attention scores. We use the transpose so that the shapes align correctly for the multiplication.

- Scores = Q . K^T

The score tells us how much one token should attend to another token. A higher score means a stronger match between the Query of one token and the Key of another token.

Step 4: We scale the scores by dividing them by the square root of the dimension of the Key vectors. Here, `d_k` is the dimension of the Key vector.

- Scaled Scores = (Q . K^T) / sqrt(d_k)

This scaling is done to keep the numbers in a stable range so that the softmax does not produce extreme values. Without this scaling, the gradients can become very small during training. We have a detailed blog on the Math behind √dₖ Scaling Factor in Attention that explains this step by step.

Step 5: We apply softmax on the scaled scores. This converts the scores into probabilities. Every row of the matrix now sums to 1.

- Attention Weights = softmax((Q . K^T) / sqrt(d_k))

These weights tell us, for every token, how much attention it should pay to every other token.

Step 6: We multiply the attention weights by the Value matrix `V`. This gives us the final output.

- Output = Attention Weights . V

The output is a new representation of every token where the meaning of the token is enriched by the context of the other tokens.

So, the full Self Attention formula is:

Attention(Q, K, V) = softmax((Q . K^T) / sqrt(d_k)) . V

Here, we can visualize the full flow of Self Attention as below:

```
        Input Embeddings
               |
               ↓
   +-----------+-----------+
   |           |           |
   ↓           ↓           ↓
   Q           K           V
   |           |           |
   +-----+-----+           |
         |                 |
         ↓                 |
       Q . K^T             |
         |                 |
         ↓                 |
   Divide by sqrt(d_k)     |
         |                 |
         ↓                 |
       Softmax             |
         |                 |
         ↓                 |
   Attention Weights       |
         |                 |
         +--------+--------+
                  |
                  ↓
              Multiply
                  |
                  ↓
               Output

```

Here, we can see that Q, K, and V are all created from the same input. Then Q and K are used to compute the attention weights, and V is used to compute the final output.

If we want to go deep into the Attention Mechanism, Q/K/V matrices, and Transformer internals, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

### A simple example walk-through

Let's take a small example to make this concrete.

Consider the sentence:

> I love AI

We have three tokens: `I`, `love`, `AI`.

Step 1: Every token is converted into an embedding vector.

Step 2: We create Q, K, and V vectors for every token using the learned weight matrices. So now, we have:

- Q for `I`, Q for `love`, Q for `AI`
- K for `I`, K for `love`, K for `AI`
- V for `I`, V for `love`, V for `AI`

Step 3: For the token `I`, we take its Query vector and compute the dot product with the Key vectors of all three tokens: `I`, `love`, and `AI`. This gives us three scores.

Step 4: We scale these scores by `sqrt(d_k)`.

Step 5: We apply softmax to get the attention weights. Just for the sake of understanding, let's say the result for the token `I` is:

- Weight for `I` = 0.070
- Weight for `love` = 0.707
- Weight for `AI` = 0.223

This means the token `I` is paying 7% attention to itself, 70.7% to `love`, and 22.3% to `AI`.

The same calculation happens for every token. So, the full attention weight matrix looks like below:

```
                  Attends to
                 I     love    AI
            +-------+-------+-------+
         I  | 0.070 | 0.707 | 0.223 |
            +-------+-------+-------+
From   love | 0.333 | 0.333 | 0.333 |
            +-------+-------+-------+
         AI | 0.168 | 0.533 | 0.299 |
            +-------+-------+-------+

```

Here, every row sums to 1 because of softmax. The numbers are just for the sake of understanding. Each row tells us how much attention that token is paying to every other token in the sentence. Because every row must sum to 1, a token has to give its attention away even when nothing is worth attending to, which is why the first tokens end up acting as attention sinks.

Step 6: We compute the final output for `I` as a weighted sum of the Value vectors:

- Output for `I` = 0.070 x V(`I`) + 0.707 x V(`love`) + 0.223 x V(`AI`)

This output is the new representation of `I` that carries the context of the entire sentence. Since `love` got the highest weight, the new representation of `I` is heavily influenced by the meaning of `love`.

The same process happens for every other token at the same time. So, in one shot, we get the new context-aware representation of every token in the sentence.

It works perfectly.

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

### Why Self Attention works so well

Now, let's understand why Self Attention works so well.

Before Self Attention, models like RNN and LSTM processed tokens one by one in a sequence. This was slow and the connection between far-apart words became weak. Self Attention solved both of these problems.

- Parallelization: All tokens are processed at the same time. We do not have to wait for one token to finish before processing the next. This makes training very fast on GPUs.
- Long-range dependencies: Every token can directly look at every other token, even if they are very far apart in the sentence. There is no decay over distance. The price of this is cost, which is why long-context models often switch to Sliding Window Attention, where every token looks only at its nearby tokens.
- Contextual understanding: Every token gets a richer meaning based on the surrounding words. The same word can have a different representation in different sentences depending on the context.
- Flexibility: Self Attention does not care about the order of computation. It can handle long sequences and capture complex relationships.

That's the beauty of Self Attention.

### Multi-Head Self Attention

Now, let's briefly learn about Multi-Head Self Attention.

In Self Attention, we have only one set of Q, K, and V. But one set is not enough to capture all the different types of relationships in a sentence.

So, here comes Multi-Head Self Attention into the picture.

In Multi-Head Self Attention, we run Self Attention multiple times in parallel, each with its own set of `W_Q`, `W_K`, and `W_V`. Every parallel run is called a "head". Each head learns to focus on a different aspect of the sentence.

For example:

- One head may focus on the subject-object relationship.
- Another head may focus on the verb tense.
- Another head may focus on long-range word dependencies.

After all the heads have done their work, we concatenate their outputs and pass them through one more linear layer. This gives us the final output of Multi-Head Self Attention.

We can visualize Multi-Head Self Attention as below:

```
                  Input
                    |
   +--------+-------+-------+--------+
   |        |               |        |
   ↓        ↓               ↓        ↓
 Head 1   Head 2    ...   Head N-1  Head N
   |        |               |        |
   ↓        ↓               ↓        ↓
 Output1  Output2          OutputN-1 OutputN
   |        |               |        |
   +--------+-------+-------+--------+
                    |
                    ↓
              Concatenate
                    |
                    ↓
               Linear Layer
                    |
                    ↓
              Final Output

```

Here, every head runs Self Attention in parallel with its own `W_Q`, `W_K`, and `W_V`. Their outputs are joined together and passed through a linear layer to produce the final output.

So, Multi-Head Self Attention = many Self Attentions running in parallel.

This way, the model captures many different types of relationships in the same sentence at the same time.

To master Self-Attention, Multi-Head Attention, and Transformer Architecture from the ground up, check out our AI and Machine Learning Program at Outcome School.

### Where Self Attention is used

Now, let's see where Self Attention is used.

- Encoder of Transformers: Self Attention is the core building block of the encoder. Every encoder layer uses Self Attention so that every input token can look at every other input token.
- Decoder of Transformers (Masked Self Attention): The decoder also uses Self Attention, but with a small change. The decoder generates one token at a time, and a token must not look at future tokens. So, we use Masked Self Attention, where the future tokens are hidden using a mask. Every token can look at itself and the tokens before it, but not the tokens after it.

Self Attention is the reason why models like BERT, GPT, and many other modern Large Language Models work so well. Without Self Attention, the Transformer architecture would not exist as we know it today.

This was all about Self Attention in Transformers.

Now we must have understood what Self Attention is, how it works step by step, and why it works so well.

### What is the difference between Self Attention and Cross Attention?

In Self Attention, the Query, Key, and Value all come from the same input sequence. In Cross Attention, the Query comes from one sequence and the Key and Value come from another sequence. This is why Self Attention is described as a sequence attending to itself.

### Does Self Attention process tokens one by one like an RNN?

No. Self Attention processes all tokens at the same time, so we do not wait for one token to finish before processing the next. RNN and LSTM processed tokens one by one, which was slow. Parallel processing makes training very fast on GPUs.

### Does a token pay attention to itself in Self Attention?

Yes. Every token looks at every other token in the same sequence, including itself. For example, in the sentence "I love AI", the token `I` can pay some attention to itself along with `love` and `AI`, and the weights for each row sum to 1.

### Why does the decoder use Masked Self Attention?

The decoder generates one token at a time, and a token must not look at future tokens. So, a mask hides the future tokens. Every token can look at itself and the tokens before it, but not the tokens after it.

### Are the Q, K, and V weight matrices fixed?

No. The weight matrices `W_Q`, `W_K`, and `W_V` are learned by the model during training. We multiply each input embedding by these three matrices to create the Query, Key, and Value vectors for every token.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# What is Cross Attention in Transformers and How Does It Work?
URL: https://outcomeschool.com/blog/cross-attention-in-transformers
Published: 2026-05-30
Author: Amit Shekhar

What is Cross Attention in Transformers and How Does It Work?

# What is Cross Attention in Transformers and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: May 30, 2026

Cross Attention is a mechanism in Transformers where one sequence looks at a different sequence. In simple words, one sequence asks the questions, and the other sequence provides the answers.

In this blog, we will learn about Cross Attention in Transformers. We will understand what it is, how it works step by step, how it is different from Self Attention, and where it is used.

We will cover the following:

- What is Cross Attention?
- Why do we need Cross Attention?
- Query, Key, and Value in Cross Attention
- Self Attention vs Cross Attention
- Step-by-step working of Cross Attention
- A simple example walk-through
- Where Cross Attention is used
- Importance of Cross Attention

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Cross Attention?

Cross Attention is a mechanism where one sequence looks at a different sequence, using its own Queries against the Keys and Values of the other sequence.

In simple words, Cross Attention = Cross + Attention. The word "Cross" means the information crosses over from one sequence to another. The word "Attention" means the model decides how much it should focus on each part of the other sequence.

So, one sequence asks the questions, and a different sequence provides the answers.

### Why do we need Cross Attention?

The best way to learn this is by taking an example.

Suppose we want to translate the English sentence "How are you" into Spanish. The Spanish translation is "Cómo estás".

Now, the question is: when the model is generating the Spanish word `Cómo`, how does it know that `Cómo` should mean `How`?

The model must look at the original English sentence to figure this out. It must look at the input ("How are you") while it is generating each word of the output ("Cómo estás").

So, we now have two sequences:

- The input sequence: "How are you" (3 words)
- The output sequence: "Cómo estás" (2 words)

Notice that the two sequences do not even have the same number of words. The English sentence has three words, but the Spanish translation has only two. This happens all the time in real life, and Cross Attention handles it naturally.

The output sequence must constantly look at the input sequence to produce the correct translation. The Spanish word being generated must attend to the most relevant English word.

[…333ln elided…]
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

[Showing lines 1-439 and 773-1272 of 1272; 333 middle lines (17.9KB) elided. Read artifact://67 for full output]
