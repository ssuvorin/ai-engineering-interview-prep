> Source: https://outcomeschool.com/blog/autoregressive-models

# What are Autoregressive Models?
URL: https://outcomeschool.com/blog/autoregressive-models
Published: 2026-05-13
Author: Amit Shekhar

What are Autoregressive Models?

# What are Autoregressive Models?

Authors
: - Name
: Amit Shekhar
Published on
: May 13, 2026

An Autoregressive Model is a model that generates one piece at a time, like one word, by predicting the next piece from everything it has generated so far. This is how GPT-style models write text.

In this blog, we will learn about Autoregressive Models, the family of models that generate one piece at a time by predicting the next step from the past.

We will cover the following:

- What is an Autoregressive Model?
- The Chain Rule of Probability
- The Generation Loop
- Step-by-Step Numeric Example
- Why GPT-style Models are Autoregressive
- Why Autoregressive Models Need Causal Masking
- The Connection with KV Cache
- Autoregressive vs Non-Autoregressive Generation
- Popular Autoregressive Models we should know
- Pros and Cons of Autoregressive Models
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is an Autoregressive Model?

Before we go further, let's quickly understand what a token is. A token is a small piece of text that the model reads and writes - it can be a word, a part of a word, or even a single character. For example, the sentence `"I love AI"` can be split into the three tokens `"I"`, `"love"`, and `"AI"`. We will use the word "token" all over this blog.

Now, let's decode the name itself.

Autoregressive = Auto (self) + Regressive (predicting from past values)

- Auto means self. The model uses its own previous outputs as the next input.
- Regressive means predicting a value from past values. In simple words, we look at history, and we predict the next number. A simple example: predicting tomorrow's temperature from the temperatures of the last `7` days.

So, putting them together:

Autoregressive Model = A model that predicts the next token from all the previous tokens, one step at a time.

Means, the model looks at the past, and from the past it predicts the next step. Then it adds that new step to the past, and predicts the next one again. This loop continues until the model is done.

Let's say we have the sentence:

```
"I love AI"

```

An autoregressive language model will:

1. See `"I"` and predict `"love"`.
2. See `"I love"` and predict `"AI"`.
3. See `"I love AI"` and predict the next token (often an end-of-sentence marker).

Here, we can see the pattern. At every step, the model uses the full history so far to guess the next token. That is the heart of the idea.

This is exactly how ChatGPT writes a sentence, how WaveNet generates audio samples, and how PixelCNN paints an image pixel by pixel.

Now, the question is: how do we write this idea in a precise mathematical form? The answer is: the chain rule of probability.

## The Chain Rule of Probability

The autoregressive idea has a clean mathematical form. We use the chain rule of probability.

The chain rule of probability says that the joint probability (the probability of all the tokens occurring together as a sequence) of a full sequence can be written as a product of conditional probabilities, like below:

```
P(x_1, x_2, ..., x_n) = P(x_1) * P(x_2 | x_1) * P(x_3 | x_1, x_2) * ... * P(x_n | x_1, x_2, ..., x_{n-1})

```

Here:

- `x_1, x_2, ..., x_n` are the tokens in the sequence.
- `P(x_1, x_2, ..., x_n)` is the joint probability of the whole sequence.
- `P(x_i | x_1, ..., x_{i-1})` is the conditional probability (probability under a condition) of the `i`-th token given all the previous tokens.
- `*` means multiplication.
- `|` means given. So `P(B | A)` reads as "the probability of B given A".

The idea is simple. To find the probability of a full sentence, we multiply the probability of each word, conditioned on every word that came before it.

Let's put this into perspective with a small example. Suppose our sentence is `"I love AI"`. Then:

```
P("I love AI") = P("I") * P("love" | "I") * P("AI" | "I", "love")

```

Here, we can see that every term on the right side asks the same question: given everything I have seen so far, what is the probability of the next word?

This is exactly the question an autoregressive model is trained to answer.

Now, let's see what this loop looks like in practice.

## The Generation Loop

Autoregressive generation is a loop. The same step repeats again and again, with the past growing by one token each time.

Let's see the loop as a simple diagram:

```
              +---------------------+
              |  Past tokens so far |
              +---------------------+
                        |
                        v
              +---------------------+
              |   Autoregressive    |
              |       Model         |
              +---------------------+
                        |
                        v
              +---------------------+
              |  Probabilities for  |
              |   the next token    |
              +---------------------+
                        |
                        v
              +---------------------+
              | Sample / pick one   |
              |     next token      |
              +---------------------+
                        |
                        v
              +---------------------+
              |  Append to past     |
              |  Repeat the loop    |
              +---------------------+

```

Here, we can see the four moves of one generation step:

1. Feed the past tokens into the model.
2. The model gives us a probability for every possible next token.
3. We pick one token from those probabilities (this is called sampling).
4. We append that token to the past, and we go back to step 1.

The loop runs until we hit an end-of-sentence marker, or until we reach a maximum length we set.

In pseudocode, the loop looks like below:

```
past = [start_token]

while not done:
    probs = model(past)              # probabilities for the next token
    next_token = sample(probs)       # pick one token
    past = past + [next_token]       # append
    if next_token == end_token:
        done = True

output = past

```

Here, we have a tight loop. Each pass through the loop produces exactly one token. So, to generate `100` tokens, the model runs `100` times.

This is the price we pay for being autoregressive. The output is high quality, because every new token is conditioned on the full past, but the generation is slow, because we cannot parallelize across tokens. I will come back to this trade-off later in the blog.

This one-token-at-a-time generation is also what makes token streaming possible - the moment each token is produced, an app can push it to the user instead of waiting for the whole reply. We have a blog on how Token Streaming works that explains this step by step.

Now, let's run this loop on real numbers.

## Step-by-Step Numeric Example

The best way to learn this is by taking an example. Let's say our model has a tiny vocabulary of just `5` words:

```
vocab = ["I", "love", "AI", "code", "<end>"]

```

We start the generation with the first token `"I"`, and we will run the loop for a few steps.

I am using simple round numbers here for the sake of understanding. Real models work with vocabularies of `50,000+` tokens, but the idea is exactly the same.

Step 1: Predict the next token after `"I"`.

We give the past `["I"]` to the model. The model returns a probability for every word in the vocabulary, like below:

```
P(next | "I") =
  "I"     -> 0.05
  "love"  -> 0.60
  "AI"    -> 0.15
  "code"  -> 0.15
  "<end>" -> 0.05

```

Here, we can see that all probabilities add up to `1.0` (`100%`). The model thinks `"love"` is the most likely next word, with `P("love" | "I") = 0.60`.

Now, we sample one token from this distribution. Sampling can be as simple as picking the highest-probability token (called greedy decoding), or it can be more random (called temperature sampling). For this example, we go with greedy and pick the highest. We pick `"love"`. Our past becomes `["I", "love"]`.

Step 2: Predict the next token after `"I love"`.

We give the past `["I", "love"]` to the model. The model now uses both `"I"` and `"love"` to decide:

```
P(next | "I", "love") =
  "I"     -> 0.05
  "love"  -> 0.05
  "AI"    -> 0.70
  "code"  -> 0.15
  "<end>" -> 0.05

```

Here, the probability of `"AI"` jumps to `0.70`. Because the model has now seen `"love"` as well, and `"I love AI"` is a common sentence, so the model leans heavily towards `"AI"`.

We sample, and we pick `"AI"`. Our past becomes `["I", "love", "AI"]`.

Step 3: Predict the next token after `"I love AI"`.

We give the past `["I", "love", "AI"]` to the model:

```
P(next | "I", "love", "AI") =
  "I"     -> 0.05
  "love"  -> 0.05
  "AI"    -> 0.05
  "code"  -> 0.05
  "<end>" -> 0.80

```

Here, the model thinks the sentence is complete, and ` ` has the highest probability of `0.80`.

We sample, and we pick ` `. The loop stops.

Step 4: Compute the probability of the full sentence.

Using the chain rule of probability:

```
P("I love AI <end>")
= P("I") * P("love" | "I") * P("AI" | "I", "love") * P("<end>" | "I", "love", "AI")

```

Let's say `P("I") = 0.20` (the probability of starting with `"I"`). Then:

```
P("I love AI <end>") = 0.20 * 0.60 * 0.70 * 0.80 = 0.0672

```

Here, we can see that the probability of the full sentence is just the product of each step's probability. This is exactly what the chain rule of probability told us at the start. The model never computes the full joint probability in one shot. It builds it up, one token at a time. This is the essence of an autoregressive model.

Now, let's connect this to the model family we hear about every day.

## Why GPT-style Models are Autoregressive

GPT (Generative Pre-trained Transformer) is autoregressive by design. The first word, Generative, is the key. The language models like Claude, Gemini, and LLaMA - they are all autoregressive, and they are all decoder-only Transformers.

A GPT-style model is trained on one simple task: given the past tokens, predict the next token.

That is it. Just next-token prediction, again and again, on huge amounts of text.

So, when we ask ChatGPT a question, here is what happens at a high level:

1. Our prompt is the starting `past`.
2. The model predicts the next token.
3. The new token is appended to the past.
4. The model predicts the next token again.
5. This repeats until the model decides to stop.

This is the autoregressive loop we just saw. GPT is autoregressive by design. That is why GPT-style models can keep writing as long as we let them - they always have a past to look at, and they always know how to predict one more token from it.

If we want to go deeper into how the Transformer works inside GPT-style models, we can read Decoding Transformer Architecture.

Now, here is a natural question. If the model only looks at the past, how do we make sure it does not accidentally peek at the future during training? This is where causal masking comes into the picture.

## Why Autoregressive Models Need Causal Masking

During training, an autoregressive model sees the full sentence at once, but it must still predict each token using only the tokens that came before it. The model must never peek at the future tokens. If it does, training is broken - the model just copies the answer instead of learning to predict it.

So, here comes Causal Masking to the rescue. Causal masking is a simple trick inside the attention layer that hides future tokens from each position.

Let's say we have the sentence `"I love AI"`. During training:

- When the model is predicting the token at position `1` (`"love"`), it can look at position `0` (`"I"`) only.
- When the model is predicting the token at position `2` (`"AI"`), it can look at positions `0` and `1` (`"I"`, `"love"`).
- And so on.

This rule is enforced inside attention by setting the attention scores for future positions to a very small number (negative infinity), so after softmax their attention weight becomes `0`. Here, softmax is a function that turns a list of raw scores into probabilities that add up to `1.0`. When we feed it negative infinity for a position, that position gets a probability of `0`, which means it is fully ignored.

The mask looks like below for a `3`-token sentence:

```
            "I"     "love"   "AI"
"I"      [   1        0        0   ]
"love"   [   1        1        0   ]
"AI"     [   1        1        1   ]

```

Here, `1` means "allowed to look", and `0` means "blocked". The first row is for the token `"I"` - it can only look at itself. The second row is for `"love"` - it can look at `"I"` and itself. The third row is for `"AI"` - it can look at all three. The upper triangle is full of `0` s, which is why this is called a triangular mask.

Means, the model is forced to behave autoregressively, even when it sees the whole sentence at once during training.

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

Note: During training, the model sees the full sentence in one shot, and causal masking enforces the autoregressive rule. During inference (generation), the model produces one token at a time, so the rule is enforced naturally - there is no future token to peek at. Same model, two slightly different behaviors.

We have a detailed blog on Causal Masking in Attention that explains this in depth.

Now, let's see another important consequence of being autoregressive.

## The Connection with KV Cache

Autoregressive generation is slow because the model runs once per token. For a `1,000`-token output, the model runs `1,000` times.

And, here is the painful part. At every step, the model looks at the full past. If the past has `999` tokens, the attention layer must compute Keys and Values for all `999` tokens, plus the new one. This is repeated work, because we have already computed those Keys and Values in the previous steps.

So, here comes the KV Cache into the picture. The idea is simple: store the Keys and Values from previous steps, and reuse them in the next step. We only compute the Key and Value for the new token, not for all the old ones again.

This stored memory is called the KV Cache - where K stands for Key and V stands for Value. We have a detailed blog on KV Cache in LLMs that explains this in depth.

Let's put this into perspective with real numbers. Suppose we are generating `1,000` tokens. Without KV Cache, at step `t` we recompute Keys and Values for all `t` past tokens. Across all `1,000` steps, that adds up to roughly `1 + 2 + 3 + ... + 1000 = 500,500` units of Key/Value work. With KV Cache, at every step we compute the Key and Value for only the new token, so total Key/Value work is roughly `1,000` units.

Means, KV Cache turns roughly `500,500` units of redundant Key/Value work into roughly `1,000` units. That is a huge speedup, and it exists because the model is autoregressive.

I am sure we can now see why KV Cache exists. It exists because autoregressive generation has a very specific shape - the past does not change between steps, only one new token is added. So, we cache the past.

Now, let's compare autoregressive generation with the other side of the coin.

## Autoregressive vs Non-Autoregressive Generation

Autoregressive generation is sequential. We produce one token, then the next, then the next. Each token depends on all the previous tokens.

Non-autoregressive generation is parallel. The model tries to produce many tokens at the same time, in one shot, without waiting for the previous ones.

Let me tabulate the differences between Autoregressive and Non-Autoregressive generation for your better understanding so that you can decide which one to use based on your use case.

| Aspect | Autoregressive | Non-Autoregressive |
| --- | --- | --- |
| Generation order | One token at a time, left to right | Many tokens at once, in parallel |
| Each token depends on | All previous tokens | Limited or no dependence on other generated tokens |
| Speed | Slow (one model run per token) | Fast (one model run for many tokens) |
| Quality | Generally higher, fluent text | Generally lower, can produce repeated or off-topic tokens |
| Training | Simple - just next-token prediction | More complex objectives |
| Examples | GPT, WaveNet, PixelCNN | Some translation models, parallel decoders |

A Variational Autoencoder is a classic example of a non-autoregressive generative model - it produces a whole output in one shot by sampling from a smooth latent space, rather than one piece at a time. A Generative Adversarial Network (GAN) is another non-autoregressive example - two networks compete to produce a whole image at once, again rather than one piece at a time.

For text specifically, the leading non-autoregressive approach is the Diffusion Language Model, which fills and refines the whole sentence in parallel instead of one token at a time. We have a blog on how Diffusion Language Models (DLMs) work that covers this end to end.

Now, let's see where autoregressive models are used.

## Popular Autoregressive Models we should know

Autoregressive models are not just for text. The same one-step-at-a-time idea applies to any kind of sequence. Let's see a few popular examples.

1. Language models (GPT family). The most famous example. The model generates text one token at a time, conditioned on the prompt and everything generated so far.

2. PixelCNN (image generation). The model generates an image one pixel at a time. Each new pixel is predicted from the pixels above and to the left of it. The image is the sequence.

3. WaveNet (audio generation). The model generates raw audio one sample at a time. Audio sampled at `16,000` samples per second means the model runs `16,000` times to produce just `1` second of audio. Slow, but very high quality.

4. Music generation models. Many music models generate notes one at a time, conditioned on all the previous notes, just like words in a sentence.

Here, we can notice the common pattern. Whatever the data is - text, pixels, audio samples, notes - if we can lay it out as a sequence, we can apply the autoregressive idea on top of it.

Now, let's look at the trade-offs.

## Pros and Cons of Autoregressive Models

Let's understand what we gain and what we lose by being autoregressive.

On the good side, the output is coherent and fluent, because the model uses the full past at every step. The training objective is also as simple as it gets - just predict the next token. The length is flexible too. The model can keep generating as long as we want, and we control when to stop. One more big win: a single autoregressive language model can do translation, summarization, question answering, code generation, and many other tasks. One model, many jobs.

On the painful side, generation is slow. We must produce tokens one by one. To generate `100` tokens, the model runs `100` times. The wait time grows with output length too. A `1,000`-token answer takes roughly `10x` longer to generate than a `100`-token answer. And then there is the error compounding problem. A bad early token can hurt the whole output, because every later token is conditioned on it. If token `5` is wrong, tokens `6`, `7`, `8`, and so on are all conditioned on a wrong past. We also cannot parallelize generation. Token `t+1` cannot be computed before token `t` is known.

To soften these problems, we use techniques like KV Cache, Speculative Decoding, and better sampling strategies. We have a detailed blog on Medusa that explains how a model can guess several of its own next tokens in one pass, and one on EAGLE that makes those guesses more accurate by drafting at the feature level. But the core trade-off - slower generation, higher quality - is built into the autoregressive idea itself.

## Quick Summary

Let's recap what we have learned:

- Autoregressive Model. A model that predicts the next token using all the previous tokens, one step at a time.
- Auto + Regressive. Auto means self, regressive means predicting from past values. So the model uses its own past outputs to predict the next one.
- Chain rule of probability.`P(x_1, ..., x_n) = P(x_1) * P(x_2 | x_1) * ... * P(x_n | x_1, ..., x_{n-1})`. The math behind autoregressive generation.
- Generation loop. Feed the past, get probabilities, sample one token, append, repeat.
- GPT-style models. Trained purely on next-token prediction. They are autoregressive by design.
- Causal masking. Hides future tokens during training so the model is forced to be autoregressive.
- KV Cache. Caches the Keys and Values of past tokens, so each new step computes Key and Value for only the new token. For `1,000` tokens, this turns roughly `500,500` units of redundant work into roughly `1,000` units. Exists because of the autoregressive shape.
- Autoregressive vs Non-Autoregressive. Autoregressive is sequential and high-quality. Non-autoregressive is parallel and faster, but quality often suffers.
- Use cases. Text (GPT), images (PixelCNN), audio (WaveNet), music. Anything that can be viewed as a sequence.
- Trade-off. High quality and simple training, at the cost of slow, sequential generation.

Now, we have understood Autoregressive Models.

### When does an autoregressive model stop generating?

An autoregressive model stops when it produces an end-of-sentence marker, or when it reaches a maximum length we set. Until then, the loop keeps running. It feeds the past tokens in, picks one next token, appends it, and repeats.

### Why do longer LLM answers take longer to generate?

The model runs once per token, so the wait time grows with the output length. To generate 100 tokens, the model runs 100 times. A 1,000-token answer takes roughly 10x longer than a 100-token answer, because token t+1 cannot be computed before token t is known.

### What is greedy decoding in autoregressive models?

Greedy decoding means picking the highest-probability token at every step. It is the simplest way to sample the next token from the model's probabilities. Sampling can also be more random, which is called temperature sampling.

### Can one wrong token spoil the rest of the output?

Yes. This is called the error compounding problem. Every later token is conditioned on the earlier ones, so a bad early token can hurt the whole output. If token 5 is wrong, tokens 6, 7, 8, and so on are all conditioned on a wrong past.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
