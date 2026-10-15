> Source: https://outcomeschool.com/blog/small-language-models-slms

# What are Small Language Models (SLMs) and When Should We Use Them?
URL: https://outcomeschool.com/blog/small-language-models-slms
Published: 2026-05-11
Author: Amit Shekhar

What are Small Language Models (SLMs) and When Should We Use Them?

# What are Small Language Models (SLMs) and When Should We Use Them?

Authors
: - Name
: Amit Shekhar
Published on
: May 11, 2026

A Small Language Model (SLM) is a language model that typically has less than 10 billion parameters. It is cheaper and faster than a Large Language Model, and it can even run on our own devices.

In this blog, we will learn about Small Language Models (SLMs), what counts as small, why they matter, where they shine, and the trade-offs we must keep in mind.

We will cover the following:

- SLM = Small + Language Model
- What is a Language Model?
- What Counts as "Small"?
- Popular SLMs we should know
- How SLMs Stay Capable Despite Being Small
- Why SLMs Matter
- SLM vs LLM
- The Size Spectrum
- Where SLMs Shine - Use Cases
- Trade-offs of SLMs
- When to Pick an SLM
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## SLM = Small + Language Model

A Small Language Model (SLM) is a language model that is small enough to run cheaply, quickly, and even on our own laptop or phone, while still being good enough for many real tasks.

Let's decompose the name:

SLM = Small + Language Model.

- Small - the model has very few parameters compared to a large model. Typically less than `10` billion parameters, and often as small as `0.5` billion or `1` billion.
- Language Model - a neural network that learns to predict the next word in a sequence.

So, when we say "Small Language Model", we are simply saying "a language model with a small number of parameters". An SLM is a deliberate design choice. We trade some general knowledge and heavy reasoning power for speed, low cost, and the ability to run on a laptop or phone.

Now, the question is: what is a parameter? And what is a language model exactly? Let's understand both before we move forward.

## What is a Language Model?

A Language Model is a neural network trained to predict the next token (i.e. the next small chunk of text) based on the previous tokens.

A token is roughly a small piece of text - sometimes a full word, sometimes part of a word. For example, the sentence "I love AI" might be split into `3` tokens: `I`, `love`, `AI`. The model works on tokens, not characters or words directly.

Let's say we give the model the text:

```
The sky is

```

The model predicts the next token. It might predict `blue`. Then we feed the new sequence back in and it predicts the next token, and so on. This is how the model writes full sentences, paragraphs, and even code.

The "knowledge" of the model is stored inside its parameters. A parameter is just a number that the model has learned during training. More parameters means more capacity to memorize patterns, facts, and reasoning shortcuts.

For example, a `1B` model has `1` billion (`1,000,000,000`) such numbers. A `70B` model has `70` billion of them. That is a `70x` jump in capacity.

So, a Language Model = a neural network + a huge number of learned parameters + the goal of predicting the next token.

Now that we know what a language model is, let's understand what makes one "small".

## What Counts as "Small"?

There is no strict rule, but in practice:

- Small Language Model (SLM) - typically less than 10 billion parameters. Often `0.5B`, `1B`, `2B`, `3B`, `4B`, or up to about `9B`.
- Large Language Model (LLM) - typically `30B` and above. Frontier LLMs are often `70B`, `400B`, or even larger.

So, the line is roughly drawn at `10B` parameters. Anything well below that is comfortably an SLM. Anything well above that is comfortably an LLM. The middle zone (around `10B` to `30B`) is fuzzy and depends on whom we ask.

Note: "Small" is a moving target. A `7B` model was considered very small a few years back. A few years from now, today's `1B` model may feel like the new midsize. The key idea is relative size, not a fixed number.

To make this concrete, let's see real examples.

## Popular SLMs we should know

Here are some well-known SLMs we should know about:

| Model | Size | Developer | Notes |
| --- | --- | --- | --- |
| Phi-4-mini | 3.8B | Microsoft | Strong reasoning, `128K` context |
| Gemma 4 E2B | 2B (effective) | Google | Built for phones; `128K` context, text, image, and audio input |
| Gemma 4 E4B | 4B (effective) | Google | Built for edge devices; `128K` context, audio input |
| Llama 3.2 1B | 1B | Meta | Designed for mobile and edge, `128K` context |
| Llama 3.2 3B | 3B | Meta | Stronger on-device option, `128K` context |
| Qwen 3.5 0.8B | 0.8B | Alibaba | Among the smallest usable models, `256K` context |
| Qwen 3.5 2B | 2B | Alibaba | Multimodal, thinking-mode toggle, `256K` context |
| Qwen 3.5 4B | 4B | Alibaba | Multimodal, `256K` context |
| Qwen 3.5 9B | 9B | Alibaba | Sweet spot of small series, rivals older `30B` models, `256K` context |
| SmolLM3 3B | 3B | Hugging Face | Open instruct and reasoning, `128K` context |

Note: The "E" in Gemma 4 E2B and E4B stands for "Effective" parameters. Gemma 4 uses Per-Layer Embeddings, so the parameter count that matters at inference time is smaller than the total parameter count.

Here, we can see that the parameter counts range from `0.8B` to `9B`. The smaller ones can run on a phone, while the larger ones run on a laptop with a decent GPU. Compare this to a `70B` LLM, which needs a heavy GPU server to run at all.

Now, a natural question arises - how can a `3B` model be useful at all when a `70B` model has so much more capacity? Let's understand.

## How SLMs Stay Capable Despite Being Small

A few years back, a `3B` model was very weak. Today, a `3B` SLM can be surprisingly capable. So, what changed? I am sure many of us must be knowing the headline answer - better data, better training, better architecture. Let's see all three:

1. Better training data.

Modern SLMs are trained on carefully filtered, very high-quality data. Instead of dumping the whole internet into the training pipeline, teams now filter, clean, and pick the best `1` to `15` trillion tokens. Quality beats quantity.

2. Better training techniques.

Techniques like knowledge distillation (where a small "student" model learns from a large "teacher" model), better optimizers, and longer training runs squeeze more capability out of every parameter.

3. Smarter architecture choices.

Choices like Grouped-Query Attention, RoPE (Rotary Position Embedding), and other recent ideas make small models faster and stronger without needing more parameters. If we want to go deeper, we have a detailed blog on Grouped Query Attention that explains one such technique.

So, a modern `3B` SLM today is far stronger than a `3B` model from a few years ago, thanks to better data and better training.

To learn Knowledge Distillation, SLMs and Model Distillation, and the LLM Internals that make modern small models capable, check out our AI and Machine Learning Program at Outcome School.

Now, let's understand why we even care about SLMs.

## Why SLMs Matter

Now, the question is: why do we need SLMs when LLMs are so powerful? The answer is: SLMs win on cost, speed, privacy, and on-device deployment.

Let's go through each reason.

1. Lower cost.

LLMs are expensive to run. Every token we generate costs money, either in API (Application Programming Interface, i.e. the cloud service we call to use the model) charges or in GPU (Graphics Processing Unit) time. SLMs cost a tiny fraction of that.

Let's put this into perspective with real numbers. For a typical workload of `1` million output tokens:

- A frontier LLM might cost around `$25` per million output tokens via an API.
- A `3B` SLM running on our own GPU might cost around `$0.10` to `$0.20` per million output tokens in electricity and hardware time.

That is roughly a `100x` to `200x` cost reduction. For a product that processes `100` million tokens per day, this is the difference between `$2,500` per day and around `$15` per day.

2. Lower latency.

Smaller models respond faster. Less computation per token means less time per token.

For the same prompt, the time to first token (i.e. how long before the first word appears) looks like:

- A `70B` model on a single GPU might take around `2` seconds.
- A `3B` SLM on the same hardware might take around `100` milliseconds (`0.1` second).

That is a `20x` speedup. For a chat or voice assistant, that difference is the gap between "feels slow" and "feels instant".

3. Privacy.

SLMs are small enough to run on our own machine. No data leaves our laptop or our server. This matters for medical records, financial data, internal company documents, and any case where sending data to a cloud API is not allowed.

We have a detailed blog on how Ollama works that explains step by step how we run a model on our own computer.

4. On-device and edge deployment.

A `3B` model can run on a modern phone. A `1B` model can run on a small laptop CPU. A `0.5B` model can run on tiny edge devices. This opens up offline AI - apps that work without internet, on the user's own device. For example, a smart keyboard that suggests the next sentence, a note-taking app that summarizes our notes locally, or a translator that works on a long flight without WiFi. These on-device models are usually packaged in the GGUF format and run through an engine like llama.cpp. We have a detailed blog on how GGUF works that explains the single-file format these models run from.

5. Easier fine-tuning.

Fine-tuning means we take a pre-trained model and train it a little more on our own data so that it gets better at our specific task. Fine-tuning a `70B` model needs a small data center. Fine-tuning a `3B` model can be done on a single consumer GPU in a few hours. So, teams can build their own custom models for their specific domain very easily.

6. Reliability and control.

There is no API rate limit when we run an SLM ourselves. No outages from a third party. No surprise price changes. We own the model and we own the deployment.

So, SLMs open up use cases that LLMs cannot reach at all - on-device, fully offline, fully private, and fully under our control.

Now, let's compare SLMs and LLMs side by side.

## SLM vs LLM

Let me tabulate the differences between SLMs and LLMs for your better understanding so that you can decide which one to use based on your use case.

| Aspect | SLM | LLM |
| --- | --- | --- |
| Parameters | `0.5B` to `~10B` | `30B` to `400B+` |
| Memory needed | `1` to `18 GB` | `60` to `800+ GB` |
| Hardware | Phone, laptop, single GPU | Multi-GPU server |
| Latency (first token) | `~50-200 ms` | `~500 ms - 3 s` |
| Cost per `1M` output tokens | `~$0.10 - $1` | `~$5 - $30` |
| General knowledge | Decent, but limited | Very broad |
| Complex reasoning | Weak to medium | Strong |
| Long context quality | Decent at `128K` | Strong at `1M+` |
| Privacy | Easy (run locally) | Hard (cloud APIs) |
| Fine-tuning effort | Easy and cheap | Hard and expensive |

Here, we can see that each side has its own strengths. SLMs win in deployment, cost, latency, and privacy. LLMs win in general knowledge, reasoning depth, and handling very long contexts.

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

There is no clear winner here. It depends on our use case.

Let's put this into perspective with a small example. Suppose we want to summarize a paragraph of text into one line:

- With a `1B` SLM: takes around `100 ms`, uses around `2 GB` of memory, costs almost nothing.
- With a `70B` LLM: takes around `2` seconds, uses around `140 GB` of memory, costs around `$0.0002` per call via API.

For one user, both are fine. For `1` million calls per day, the SLM saves us thousands of dollars and gives a much better user experience. I have used round numbers here for the sake of understanding, the real numbers depend on the exact hardware and the exact API price.

Now, let's visualize where SLMs sit on the size spectrum.

## The Size Spectrum

Here is a simple diagram showing where SLMs fit:

```
   Tiny         Small (SLM)         Mid           Large (LLM)         Frontier
   ----         -----------         ---           -----------         --------
   < 0.5B       0.5B - 10B        10B - 30B       30B - 70B          100B - 1T+
   |              |                  |                 |                   |
   |              |                  |                 |                   |
   v              v                  v                 v                   v
   tiny          phone /            single            single              multi-GPU
   embedded      laptop /           server            server              cluster
   devices       single GPU         GPU               (multi-GPU)         (data center)

```

Here, we can see five rough buckets along the size axis:

- Tiny (`<0.5B`) - very small models for embedded use.
- Small / SLM (`0.5B` to `~10B`) - the SLM zone. Smaller ones run on a phone; larger ones on a laptop or single GPU.
- Mid (`10B` to `30B`) - the fuzzy middle between SLM and LLM. Could go either way.
- Large / LLM (`30B` to `70B`) - serious GPU servers needed.
- Frontier (`100B` and beyond) - large clusters needed.

The SLM bucket is the sweet spot for most production use cases that do not need deep reasoning. It is small enough to deploy easily and large enough to do useful work.

Now, let's see where SLMs really shine in practice.

## Where SLMs Shine - Use Cases

SLMs are the right tool for many real tasks. Let's go through the most common ones.

1. On-device assistants.

A `1B` to `3B` SLM can run on a phone or laptop. So, we can build a writing assistant, a code helper, or a chat assistant that works offline. No internet, no cloud, no API key. The model lives inside the app.

For example, a `1B` model uses around `2 GB` of memory and can produce around `30` tokens per second on a modern phone. That is fast enough for real-time chat.

2. Classification.

Many real tasks are simply: "given this input, pick one label out of N categories". For example, classifying a support ticket as `billing`, `technical`, or `account`. An SLM, especially after a small fine-tune, handles this very well.

A `0.5B` fine-tuned model can classify thousands of inputs per second on a single CPU. For high-volume classification, this is hard to beat.

A newer option for this exact job is a System One Model like Jev, which does not generate text at all and returns the label with a calibrated probability in a single pass.

3. Structured extraction.

Pulling structured data out of unstructured text. For example, given an email, extract the sender, the date, the action item, and the deadline. SLMs do this very well, especially when we use constrained decoding (i.e. forcing the model to produce valid JSON).

4. Agent task heads.

In a larger agent system, many small steps do not need a heavy reasoning model. Routing a request, selecting a tool from a list, formatting an output - all of these can be done by an SLM. The big LLM is only called when complex reasoning is actually needed.

If we want to go deeper into how agents work end to end, we can read AI Agent.

5. Fine-tuned domain models.

Suppose we work in a niche field - for example, a specific style of legal contracts in our country. Fine-tuning a `3B` SLM on `10,000` examples of our domain often beats a generic `70B` LLM on that specific task. We get a model that is small, fast, cheap, and very accurate within our domain.

6. High-volume pipelines.

Imagine processing `10` million customer reviews per day to extract sentiment. An LLM API would cost around `$10,000` per day. A self-hosted SLM might cost around `$100` per day for the same job. The math speaks for itself.

So, SLMs shine wherever the task is narrow, latency-sensitive, or privacy-sensitive.

We have a complete program on AI Agents, Tool use in Agents, Fine-tuning, and Orchestration and Routing - check out our AI and Machine Learning Program at Outcome School.

Now, let's be honest about where SLMs do not shine.

## Trade-offs of SLMs

SLMs are great, but they are not magic. Let's understand the trade-offs.

1. Less general knowledge.

A `1B` model has `70x` fewer parameters than a `70B` model. So, it has memorized far fewer facts about the world. Ask it about a niche historical event or a rare scientific concept, and it may simply not know.

2. Weaker complex reasoning.

For multi-step reasoning - long math chains or complex planning - SLMs often struggle. They may give wrong answers with high confidence.

3. Weaker long-context quality.

Most modern SLMs already support `128K` tokens or more, so the size of the context window is no longer the main limit. The real gap is in how well the model actually uses that window. For tasks like needle-in-haystack search across `100K` tokens, or long multi-document reasoning, a `3B` SLM is meaningfully weaker than a `200B+` frontier LLM, even when both technically support the same window size. We have a detailed blog on Recursive Language Models (RLMs) that sidesteps this entirely by splitting a long input into small pieces and letting an SLM-sized model work on one piece at a time.

4. More fragile.

SLMs can be more sensitive to prompt wording. A small change in phrasing can lead to a very different answer. So, we often need careful prompting or fine-tuning to get reliable behavior.

5. Less polished writing.

For long-form creative writing, marketing copy, or careful multi-step reasoning, the gap between an SLM and a top LLM is real. The SLM may sound less natural and less coherent.

This trade-off - less reasoning power and general knowledge, more speed and lower cost - is the core deal we are making when we choose an SLM.

Note: The gap between SLMs and LLMs keeps shrinking with every new generation. A `3B` SLM today often matches or beats a `13B` model from two years ago. So, the trade-off list above is correct today, but the gap will keep getting smaller.

Now, the natural question is: when do we pick an SLM?

## When to Pick an SLM

Based on our use case, here is a simple decision guide:

Pick an SLM when:

- The task is narrow and well-defined (classification, extraction, routing).
- We expect very high volume (millions of calls per day).
- We need very low latency (under `200 ms`).
- The data is sensitive and must stay on our own server or device.
- We need offline / on-device deployment.
- We have training data and can fine-tune for our domain.

Pick an LLM when:

- The task needs deep reasoning over multiple steps.
- The task needs broad world knowledge.
- The task needs very long context (i.e. large documents or long histories).
- The volume is low enough that API cost is not a concern.
- We need the highest possible quality and we are willing to pay for it.

Pick a hybrid (SLM + LLM) when:

- Most steps in our workflow are simple, but a few need heavy reasoning.

This is where the hybrid setup comes into the picture. The SLM handles routing, classification, extraction, and tool-selection, while the LLM is called only for the hard reasoning steps. This gives us the speed and cost of an SLM with the depth of an LLM where it really matters.

Here is a simple diagram of the hybrid pattern:

```
            +---------------------+
  Input --> |  SLM (router)       |
            |  small + fast       |
            +----------+----------+
                       |
            simple?    |    complex?
            +----------+----------+
            |                     |
            v                     v
       +---------+          +-----------+
       |  SLM    |          |    LLM    |
[…971ln elided…]

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

[Showing lines 1-377 and 1349-1727 of 1727; 971 middle lines (50.9KB) elided. Read artifact://43 for full output]
