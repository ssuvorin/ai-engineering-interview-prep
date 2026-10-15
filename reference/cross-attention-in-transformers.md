> Source: https://outcomeschool.com/blog/cross-attention-in-transformers

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

This is exactly what Cross Attention does. The output sequence attends to the input sequence. The two sequences are different, but one looks at the other. Since the attention crosses from one sequence to another, we call it Cross Attention.

For the sake of understanding, let's take an analogy.

Suppose we are a student writing an exam answer. We have our own thoughts in our head (this is one sequence). We also have a reference book open on the table (this is another sequence). While writing each line of our answer, we look at our own thoughts (Query) and check the reference book (Key and Value) to pick up the relevant information.

That is exactly what Cross Attention does in a model. One sequence is reading from another sequence.

So, Cross Attention lets the output sequence read from the input sequence at every step. Now, let's understand how it does this using Query, Key, and Value.

### Query, Key, and Value in Cross Attention

For each word the decoder is generating, Cross Attention needs to answer two questions:

- Which tokens of the input sequence are important for me?
- How much should I focus on each of them?

To answer these questions, we create three vectors:

- Query (Q): what the decoder is looking for at the current step.
- Key (K): what each input token offers.
- Value (V): the actual information each input token carries.

The word "Cross" in Cross Attention comes from one very important fact:

> Query comes from one sequence, and Key and Value come from a different sequence.

This is what makes it "Cross" Attention. The two sequences are different, but one is attending to the other.

In simple words, if our input is "How are you" and our output is "Cómo estás", then:

- The Query comes from the decoder side, which is generating "Cómo estás" (the output sequence).
- The Key and Value come from "How are you" (the input sequence).

Note: This is the key difference between Self Attention and Cross Attention. In Self Attention, all three (Q, K, V) come from the same sequence. In Cross Attention, Q comes from one sequence, while K and V come from a different sequence.

### Self Attention vs Cross Attention

Let me tabulate the differences between Self Attention and Cross Attention for your better understanding.

| Aspect | Self Attention | Cross Attention |
| --- | --- | --- |
| Source of Query (Q) | Same sequence | Output sequence (decoder) |
| Source of Key (K) | Same sequence | Input sequence (encoder) |
| Source of Value (V) | Same sequence | Input sequence (encoder) |
| Masking | Usually masked in the decoder | Not masked |
| Attention matrix shape | Square (N x N) | Rectangular (output length x input length) |
| Purpose | Understand relationships within one sequence | Connect information from two different sequences |
| Common use | Encoder layers, decoder self-attention | Encoder-decoder bridge, multi-modal models |

A few of these differences are very important, so let's understand them one by one. Do not worry, we will learn about each of them now.

First, the decoder of a Transformer uses both types of attention. It first uses Self Attention to look at the words it has already generated. Then it uses Cross Attention to look at the encoder's output. So, Cross Attention does not replace Self Attention. They work together inside the decoder.

Second, Cross Attention is not masked. In the decoder's Self Attention, a word is not allowed to look at the future words, because the model has not generated them yet. But in Cross Attention, the whole input sentence is already known. So, every output word is allowed to look at every input word, with no restriction.

Third, the Key and Value are computed only once. The encoder reads the input sentence a single time and creates the Key and Value. The decoder then reuses the same Key and Value for every output word it generates. This makes Cross Attention very efficient.

Now, we have understood the difference. Let's see how Cross Attention actually works.

To master Cross Attention, Self-Attention, and Causal Masked Attention in depth, check out our AI and Machine Learning Program at Outcome School.

### Step-by-step working of Cross Attention

Now, it's time to learn the exact steps of Cross Attention.

The classic place where Cross Attention is used is the original Transformer from the paper "Attention Is All You Need". The Transformer has two parts:

- The Encoder: reads the input sequence and creates a rich representation of it.
- The Decoder: generates the output sequence, one token at a time.

We have a detailed blog on Encoder vs Decoder in Transformers that explains how these two parts differ.

Inside the decoder, there are actually two attention steps. First, the decoder uses Self Attention to look at the words it has already generated. Then, it uses Cross Attention to look at the encoder's output. Here, we are focusing on the second step, the Cross Attention.

So, here comes Cross Attention to the rescue. It is the bridge between the encoder and the decoder.

Step 1: The encoder reads the input sequence and produces a set of vectors. From these vectors, we create the Key (K) and the Value (V).

- K = Encoder Output x W_K
- V = Encoder Output x W_V

The encoder does this only once. The same Key and Value are then reused for every token the decoder generates. This is what makes Cross Attention efficient.

Step 2: The decoder takes the tokens generated so far and produces its own hidden states. From these hidden states, we create the Query (Q).

- Q = Decoder Hidden State x W_Q

Here, `W_Q`, `W_K`, and `W_V` are weight matrices that the model learns during training.

Step 3: We compute the dot product of `Q` with the transpose of `K`. This is a matrix multiplication that gives us the attention scores. We use the transpose so that the shapes align correctly for the multiplication.

- Scores = Q . K^T

The score tells us how much each decoder token should attend to each encoder token. A higher score means a stronger match between the Query of a decoder token and the Key of an encoder token.

Step 4: We scale the scores by dividing them by the square root of the dimension of the Key vectors. Here, `d_k` is the dimension of the Key vector.

- Scaled Scores = (Q . K^T) / sqrt(d_k)

This scaling is done to keep the numbers in a stable range so that the softmax does not produce extreme values. Without this scaling, the gradients can become very small during training. We have a detailed blog on the Math behind √dₖ Scaling Factor in Attention that explains the math behind it.

Step 5: We apply softmax on the scaled scores. This converts the scores into probabilities. Every row of the matrix now sums to 1.

- Attention Weights = softmax((Q . K^T) / sqrt(d_k))

These weights tell us, for every decoder token, how much attention it should pay to every encoder token.

Step 6: We multiply the attention weights by the Value matrix `V`. This gives us the final output.

- Output = Attention Weights . V

The output is a new vector for each decoder position, now enriched with the relevant information from the encoder. The decoder uses this vector to decide the next word it should generate.

So, the full Cross Attention formula is:

Attention(Q, K, V) = softmax((Q . K^T) / sqrt(d_k)) . V

Notice that the formula itself is exactly the same as Self Attention. The difference is not in the math. The difference is in where Q, K, and V come from. In Cross Attention, Q comes from the decoder, while K and V come from the encoder. We have also seen the other differences earlier: Cross Attention is not masked, and its attention matrix is rectangular, because the two sequences can have different lengths.

Here, we can visualize the full flow of Cross Attention as below:

```
       Encoder Output             Decoder Hidden State
      (Input Sequence)              (Output Sequence)
              |                             |
        +-----+-----+                       ↓
        ↓           ↓                       Q
        V           K                       |
        |           |                       |
        |           +-----------+-----------+
        |                       |
        |                       ↓
        |                    Q . K^T
        |                       |
        |                       ↓
        |              Divide by sqrt(d_k)
        |                       |
        |                       ↓
        |                    Softmax
        |                       |
        |                       ↓
        |               Attention Weights
        |                       |
        +-----------+-----------+
                    |
                    ↓
                Multiply
                    |
                    ↓
                 Output

```

Here, we can see that Q comes from the decoder, while K and V come from the encoder. Then Q and K are used to compute the attention weights, and V is used to compute the final output.

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

### A simple example walk-through

Let's take a small example to make this concrete.

Suppose we want to translate the English sentence "How are you" into Spanish: "Cómo estás".

The decoder produces the Spanish words one at a time. It has already produced the first word, `Cómo`. Now, let's see how it predicts the next word. It does not know that word yet.

Step 1: The encoder produces a Key (K) and a Value (V) for every English token.

- K for `How`, K for `are`, K for `you`
- V for `How`, V for `are`, V for `you`

These Keys and Values are created only once. The decoder reuses them at every step.

Step 2: The decoder looks at what it has produced so far (`Cómo`) and creates a Query (Q) for the next word.

Step 3: We take this Query and compute the dot product with the Key vectors of all three English tokens: `How`, `are`, and `you`. This gives us three scores.

Step 4: We scale these scores by `sqrt(d_k)`.

Step 5: We apply softmax to get the attention weights. Just for the sake of understanding, let's say the result is:

- Weight for `How` = 0.050
- Weight for `are` = 0.500
- Weight for `you` = 0.450

So, the decoder is paying 5% attention to `How`, 50% to `are`, and 45% to `you`. It is focusing on `are` and `you`.

Step 6: We combine the Value vectors using these weights. This gives us an output vector.

- Output = 0.050 x V(`How`) + 0.500 x V(`are`) + 0.450 x V(`you`)

This output vector carries the most relevant English information for the next word.

Step 7: Finally, the decoder uses this output vector to predict the next word. It gives a score to every word in its Spanish vocabulary and picks the most likely one. Just for the sake of understanding, let's say the probabilities are:

- `estás` = 0.70
- `gracias` = 0.20
- `Hola` = 0.10

The word `estás` has the highest probability. So, the decoder predicts `estás` as the next word. This makes sense, because the decoder was focusing on `are` and `you`, and the single Spanish word `estás` carries the meaning of both of them.

The decoder then adds `estás` to the output and repeats the whole process to predict the next word, until the sentence is complete.

If we collect the attention weights from every step, the full attention matrix looks like below:

```
                          English (Encoder)
                           How       are       you
                       +---------+---------+---------+
 Spanish     Cómo      |  0.800  |  0.100  |  0.100  |
 (Decoder)             +---------+---------+---------+
             estás     |  0.050  |  0.500  |  0.450  |
                       +---------+---------+---------+

```

Here, every row sums to 1 because of softmax. The numbers are just for the sake of understanding. Each row is one step of the output, and it tells us how much attention that step paid to every English word.

Notice that this matrix is not a square. It has 2 rows (one for every Spanish word) and 3 columns (one for every English word), because the two sequences have different lengths. This is a key sign of Cross Attention. In Self Attention, the matrix is always square, because a sequence attends to itself.

It works perfectly.

### Where Cross Attention is used

Now, let's see where Cross Attention is used.

Cross Attention is not limited to translation. It is used in many modern AI systems.

- Encoder-Decoder Transformers: The original Transformer for machine translation, summarization, and question answering uses Cross Attention to connect the encoder and decoder.
- Stable Diffusion: In text-to-image models like Stable Diffusion, Cross Attention is used to condition image generation on a text prompt. The image features form the Query, and the text embeddings form the Key and Value. This is how the model "listens" to our prompt while drawing the image.
- Flamingo: A multi-modal model from DeepMind that uses Cross Attention to mix visual information with language. The text tokens form the Query, and the image features form the Key and Value.
- Whisper: OpenAI's speech-to-text model uses an encoder-decoder Transformer where Cross Attention helps the decoder attend over audio features.
- Multi-modal models in general: Whenever a model needs to combine two different types of information (text and image, audio and text, video and text, and etc.), Cross Attention comes into the picture.

So, now we know where we can use Cross Attention.

If we want to go deep into Multimodal AI, the Encoder-Decoder Architecture, and Transformer internals from the ground up, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

### Importance of Cross Attention

Now, the question is: why is Cross Attention so important?

The answer is simple. Many real-world AI tasks involve two different sources of information, and we need to combine them in a smart way.

- In translation, we have the input language and the output language.
- In text-to-image, we have the text prompt and the image we are generating.
- In speech-to-text, we have the audio and the text.

Without Cross Attention, the decoder would have to guess what the input was about. With Cross Attention, the decoder can directly look at the encoder's output and pick the most relevant information for every step.

That's the beauty of Cross Attention. It lets one sequence guide the generation of another sequence.

This was all about Cross Attention in Transformers.

Now we must have understood what Cross Attention is, how it works step by step, how it is different from Self Attention, and where it is used.

### Does Cross Attention replace Self Attention in the decoder?

No. The decoder of a Transformer uses both. It first uses Self Attention to look at the words it has already generated. Then it uses Cross Attention to look at the encoder's output. They work together inside the decoder.

### Is Cross Attention masked like decoder Self Attention?

No. Cross Attention is not masked. In the decoder's Self Attention, a word cannot look at future words because they are not generated yet. But in Cross Attention, the whole input sentence is already known, so every output word is allowed to look at every input word.

### Is the Cross Attention formula different from the Self Attention formula?

No. The formula is exactly the same: softmax of Q times K transpose divided by sqrt(d_k), multiplied by V. The difference is in where Q, K, and V come from. In Cross Attention, Q comes from the decoder, while K and V come from the encoder.

### Are the Key and Value recomputed for every output token in Cross Attention?

No. The encoder reads the input sentence a single time and creates the Key and Value. The decoder then reuses the same Key and Value for every output token it generates. This makes Cross Attention very efficient.

### Why is the Cross Attention matrix not square?

The Cross Attention matrix is rectangular because the input and output sequences can have different lengths. Its shape is output length by input length. For example, "Cómo estás" attending to "How are you" gives 2 rows and 3 columns. In Self Attention, the matrix is always square.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:
