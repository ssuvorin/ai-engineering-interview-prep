> Source: https://outcomeschool.com/blog/large-reasoning-models

# What are Large Reasoning Models (LRMs) and How Are They Different from LLMs?
URL: https://outcomeschool.com/blog/large-reasoning-models
Published: 2026-05-12
Author: Amit Shekhar

What are Large Reasoning Models (LRMs) and How Are They Different from LLMs?

# What are Large Reasoning Models (LRMs) and How Are They Different from LLMs?

Authors
: - Name
: Amit Shekhar
Published on
: May 12, 2026

A Large Reasoning Model (LRM) is a large language model that does not jump straight to the answer. It first produces a long chain of intermediate reasoning steps, and then gives the final answer.

In this blog, we will learn about Large Reasoning Models (LRMs), how they are different from standard Large Language Models, how they think before they answer, how they are trained, and when we must use them.

We will cover the following:

- The Big Picture
- What is a Large Reasoning Model (LRM)?
- LLM vs LRM
- How does an LRM actually think?
- Test-time compute: thinking longer makes them smarter
- How are LRMs trained?
- Input and Output: training phase vs prediction phase
- When to use an LRM, and when to use a regular LLM
- Popular LRMs we should know
- Common Mistakes when using LRMs
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go further, a quick word on tokens. A token is a small piece of text, roughly a word or a part of a word. The model reads and writes text one token at a time. When we say "next token", we mean the next small piece of text the model produces.

A standard Large Language Model answers as soon as we ask. It predicts the next token, one after the other, and we get the reply.

A Large Reasoning Model does something different. Before it gives the final answer, it first thinks. It writes out a long internal scratchpad of steps, checks itself, sometimes changes its mind, and only then it speaks.

In simple words:

Large Reasoning Model = A Large Language Model that is trained to think first, and answer later.

## What is a Large Reasoning Model (LRM)?

Let's decompose the name:

LRM = Large + Reasoning + Model

- Large - it has billions of parameters, often in the range of `7B` to `700B+`, just like a normal Large Language Model.
- Reasoning - it does not jump straight to the answer. It produces a long chain of intermediate steps first.
- Model - it is still a neural network that predicts the next token.

So, a Large Reasoning Model is a Large Language Model that has been specially trained to spend extra tokens thinking before it gives the final answer.

These models are also called reasoning models or thinking models. They all mean the same thing.

Examples we may have heard of: OpenAI's `GPT-5.5 Thinking`, DeepSeek `R1`, Qwen3, Google's Gemini 3 with `Deep Think`, Anthropic's `extended thinking` mode in Claude, and xAI's Grok 4.1 with `Think` mode.

## LLM vs LRM

The best way to understand LRMs is to compare them with a regular LLM.

Let's say we ask both a small word problem. We will reuse this same problem throughout the blog to keep the comparisons clean.

> A shop sells pens at `2` for `5` rupees, and notebooks at `3` for `12` rupees. We buy `6` pens and `9` notebooks. How much do we pay in total?

A regular LLM may answer in `1` second, generate just a few tokens like "`51` rupees", and sometimes get the answer wrong because it tries to guess in one shot.

A Large Reasoning Model takes a different path. It first thinks - working out the per-unit cost, multiplying, adding, and verifying the total - and only then writes the final answer. For a small problem like this, the trace may use a few hundred reasoning tokens. For harder problems, it can stretch into thousands or tens of thousands of tokens.

The reasoning tokens are usually hidden from the end user. We only see the final answer. But the model paid the cost of thinking, and that is why the answer is more accurate.

A quick visual of what each one is doing:

```
LLM:   [question] ---> [short answer]            (fast, sometimes wrong)

LRM:   [question] ---> [long thinking trace]
                          ---> [short answer]    (slow, more often right)

```

Here, we can see that the LRM adds a thinking step in the middle, which the LLM skips entirely.

Let me tabulate the differences between LLM and LRM for your better understanding so that you can decide which one to use based on your use case.

| Aspect | Standard LLM | Large Reasoning Model (LRM) |
| --- | --- | --- |
| Answering style | Direct, one shot | Thinks first, answers later |
| Tokens used | Few (`100` to `500`) | Many (`5,000` to `50,000`) |
| Latency | `1` to `3` seconds | `10` to `120` seconds |
| Cost per query | Low | `10x` to `30x` higher |
| Strength | Simple chat, summaries, drafting | Math, code, logic, planning |
| Weakness | Hard multi-step problems | Slow and expensive for easy tasks |

Both are useful, just for different jobs.

## How does an LRM actually think?

This was all about the difference between LLMs and LRMs. Now, let's understand what really happens inside an LRM when it thinks.

The thinking inside an LRM is just more text. There is no magic new component. The model writes out its thought process as tokens, the same way it writes any other tokens.

This long block of internal text is often called the reasoning trace or thinking trace. For our pen and notebook question above, it looks somewhat like below:

```
<think>
Pens: 2 pens cost 5 rupees, so 1 pen costs 2.5 rupees.
6 pens cost 6 * 2.5 = 15 rupees.

Notebooks: 3 notebooks cost 12 rupees, so 1 notebook costs 4 rupees.
9 notebooks cost 9 * 4 = 36 rupees.

Total = 15 + 36 = 51 rupees.

Let me verify. 6 pens means 3 packs of 2 pens, each pack 5 rupees, so 3 * 5 = 15. Correct.
9 notebooks means 3 packs of 3 notebooks, each pack 12 rupees, so 3 * 12 = 36. Correct.
Total 15 + 36 = 51. Correct.
</think>

We pay 51 rupees in total.

```

Here, we can see three things happening:

- The model breaks the problem into smaller steps.
- It tries an approach, computes intermediate values, and writes them down.
- It checks its own answer at the end before giving the final reply.

This is the same pattern a careful student follows on a rough sheet during an exam. The rough sheet is the reasoning trace. The final answer is what the student writes on the answer sheet.

A simple flow diagram:

```
   User question
        |
        v
   +-------------------+
   |   LRM thinking    |    <-- long internal scratchpad
   |  (reasoning trace)|        (often hidden from user)
   +-------------------+
        |
        v
   Final short answer

```

The reasoning trace is hidden in many products (like `GPT-5.5 Thinking`, where we only see a short summary), and visible in some others (like DeepSeek `R1`).

We have a complete program on Reasoning Models, LLM Internals, and Chain of Thought (CoT) Prompting - check out our AI and Machine Learning Program at Outcome School.

## Test-time compute: thinking longer makes them smarter

Here comes one of the most important ideas behind LRMs.

In a normal LLM, we make the model smarter by training a bigger model on more data. That is train-time compute. We pay once during training, and then every answer is fast.

LRMs add a second knob, called test-time compute. This means the model becomes smarter at the moment of answering, by thinking for longer.

Let's put this into perspective with the actual published numbers from OpenAI on the AIME 2024 math competition (a hard high school contest):

- GPT-4o (a regular LLM, no extended reasoning): around `12%` correct.
- o1 (an LRM with one full reasoning attempt): around `74%` correct.
- o1 with majority vote across `64` parallel attempts: around `83%` correct.
- o1 re-ranking across `1,000` attempts: around `93%` correct.

The first row is a regular LLM shown for baseline. The next three rows are the same `o1` model - what changes from row to row is purely how much test-time compute we let it spend at answer time. This is why we say LRMs scale with test-time compute.

In our student analogy, this is like giving the same student more pages of rough sheet during an exam. Same student, same brain, but a longer rough sheet often leads to a better final answer.

We can also spend extra compute at answer time from the outside, by making a regular LLM try many reasoning paths, judge them, and keep only the good ones. We have a detailed blog on Tree of Thoughts that covers this end to end.

But, here is the catch. More thinking is not free. More tokens means more time and more cost. Doubling the thinking tokens roughly doubles the output cost of that query, and the output cost is usually most of the bill for an LRM.

This trade-off - less speed, more accuracy - is the core reason LRMs exist as a separate class of models.

How fast those thinking tokens actually come out is a hardware question, and we have a detailed blog on how an LPU works that explains a chip built to make exactly this part fast.

Note: Many LRM APIs let us control how much the model is allowed to think. For example, we can set a thinking budget of `1,024`, `8,192`, or `32,768` tokens. A small budget gives a fast and cheap answer. A large budget gives a slow but more accurate answer. We can tune this knob based on our use case. Newer APIs are moving toward adaptive thinking, where the model decides how much to think based on the complexity of the query, instead of us setting a fixed budget.

## How are LRMs trained?

Now that we have understood how an LRM thinks at answer time, let's understand how it learns to think in the first place.

A regular LLM is trained in two main stages: pre-training on a huge amount of text from the internet, and instruction tuning so it learns to follow our prompts.

LRMs add one more stage on top: reinforcement learning on reasoning tasks.

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

The idea is simple:

- Give the model a hard problem with a known correct answer.
- Let it generate many long reasoning traces in parallel (a group of `16`, `32`, or `64` traces for the same problem).
- Check which traces lead to the correct final answer. Math problems have a clear right answer, so this check is easy and automatic.
- Score each trace relative to the rest of the group. The traces that did better than the group average are reinforced. The ones that did worse are penalised.
- Update the model so it becomes more likely to follow the good reasoning patterns next time.

Note: This group-relative scoring is the heart of GRPO (Group Relative Policy Optimization), the algorithm used to train DeepSeek `R1`. The "compare to the group, not to an absolute target" trick is what makes RLVR stable at this scale.

This is called Reinforcement Learning with Verifiable Rewards (RLVR). The word verifiable is important. Means, the reward comes from a simple automatic checker, not from a human opinion the way it does in Deep RL from Human Preferences. The checker can be:

- Math: does the final number match the correct answer?
- Code: does the generated code pass all unit tests?
- Logic: does the answer match the puzzle's known solution?

Because the reward is automatic, we can run this training loop millions of times without any human in the middle. In our student analogy, we are teaching the student which kinds of rough sheet patterns lead to the right final answer. We let them try many times, score each attempt, and reward the winners. Over time, the model learns useful habits like:

- Break the problem down before solving.
- Try a step, check the unit, then continue.
- Spot a mistake, go back, and try a different approach.

This is exactly what we see in the long reasoning traces.

## Input and Output: training phase vs prediction phase

Now, let's put everything together by looking at exact examples of what went into the model and what came out, in both the training phase and the prediction phase, for both LLM and LRM.

### Training phase: Standard LLM

In LLM training, the model is shown a piece of text with the next token hidden. It must predict that token.

Input to the model:

```
The capital of France is

```

Output from the model (the predicted next token):

```
Paris

```

The actual next token in the data is also "Paris". The model got it right, so the loss is small. If the model had predicted "London", the loss would be large, and the weights would be nudged to fix this.

### Training phase: Large Reasoning Model

In LRM training, the model is shown a hard problem with a known correct answer. It generates several full attempts to solve it.

Input to the model:

```
A shop sells pens at 2 for 5 rupees, and notebooks at 3 for 12 rupees.
We buy 6 pens and 9 notebooks. How much do we pay in total?

```

Output from the model (one of the `16` attempted traces):

```
<think>
Pens: 2 pens cost 5 rupees, so 1 pen costs 2.5 rupees.
6 pens cost 6 * 2.5 = 15 rupees.

Notebooks: 3 notebooks cost 12 rupees, so 1 notebook costs 4 rupees.
9 notebooks cost 9 * 4 = 36 rupees.

Total = 15 + 36 = 51 rupees.

Let me verify. 6 pens means 3 packs of 2 pens, each pack 5 rupees, so 3 * 5 = 15. Correct.
9 notebooks means 3 packs of 3 notebooks, each pack 12 rupees, so 3 * 12 = 36. Correct.
Total 15 + 36 = 51. Correct.
</think>

We pay 51 rupees in total.

```

During training, the model is asked to produce many such attempts for the same problem - say `16` traces in parallel. A simple checker compares the final answer of each trace against the known correct answer "51 rupees". Maybe `6` traces got `51`, and `10` got something wrong like `48` or `54`. The `6` good ones score above the group average and are reinforced. The `10` wrong ones score below the group average and are penalised. The model is then updated to produce more of the rewarding kinds of traces.

### Prediction phase: Standard LLM

The model is already trained. We give it a prompt, it produces an answer.

Input to the model:

```
Write a haiku about rain.

```

Output from the model:

```
Soft drops on the leaves,
A grey sky weeps to the earth,
Spring whispers goodbye.

```

The model goes straight from prompt to answer. There is no internal thinking step. The user sees the full output.

### Prediction phase: Large Reasoning Model

The model is already trained. We give it a prompt, it produces a thinking trace and then the final answer.

Input to the model:

```
A shop sells pens at 2 for 5 rupees, and notebooks at 3 for 12 rupees.
We buy 6 pens and 9 notebooks. How much do we pay in total?

```

Output from the model:

```
<think>
Pens: 2 pens cost 5 rupees, so 1 pen costs 2.5 rupees.
6 pens cost 6 * 2.5 = 15 rupees.

Notebooks: 3 notebooks cost 12 rupees, so 1 notebook costs 4 rupees.
9 notebooks cost 9 * 4 = 36 rupees.

Total = 15 + 36 = 51 rupees.

Let me verify. 6 pens means 3 packs of 2 pens, each pack 5 rupees, so 3 * 5 = 15. Correct.
9 notebooks means 3 packs of 3 notebooks, each pack 12 rupees, so 3 * 12 = 36. Correct.
Total 15 + 36 = 51. Correct.
</think>

We pay 51 rupees in total.

```

The text inside `... ` is the long reasoning trace. The line after it is the final answer. In many products, the user only sees "We pay 51 rupees in total." - the trace is hidden.

Notice that this is the same problem we used in the training example above. During training, this was one of `16` attempted traces that got scored against the known answer "51". During prediction, the model now produces the same kind of trace because that is exactly what training rewarded it to do.

### Quick recap of the four cases

In LLM training, the input is a chunk of text and the output is the next token. The loss measures how close the predicted token is to the actual next token. In LRM training, the input is a hard problem with a known answer, and the output is a full reasoning trace ending in a final answer. The reward checks if the final answer is correct.

In LLM prediction, the input is a user prompt and the output is a direct answer. In LRM prediction, the input is a user prompt and the output is a long internal thinking trace followed by a short final answer.

## When to use an LRM, and when to use a regular LLM

Now that we have seen exactly what goes in and what comes out of both models, the most practical question for any AI Engineer: when to use an LRM and when to use a regular LLM.

We use a regular LLM when:

- The task is short and direct.
- We want a quick chat reply, a simple summary, or a draft email.
- Latency matters more than perfect correctness.
- Cost per query must be low because we are doing millions of calls.

We use an LRM when:

- The task needs multiple steps of careful thought.
- A wrong answer is costly. Examples: complex math, hard coding problems, scientific questions, multi-step planning, deep data analysis, debugging tricky logic.
- We can afford to wait `30` seconds or more.
- We can afford the higher token cost.

And when the answer is not text at all but a decision, like which category, which team, or safe or not, there is a third option built just for that. We have a detailed blog on Jev and System One Models that explains how such a model returns a typed decision with a calibrated probability in a fraction of a second.

## Popular LRMs we should know

Now, let's look at the popular LRMs we should know:

- OpenAI GPT-5.5 Thinking - the current OpenAI reasoning flagship. The raw reasoning trace is hidden, and we only see a short summary plus the final answer.
- DeepSeek `R1` and `R1-Zero` - open weights, shows the full reasoning trace, uses RLVR as a key training stage. `R1-Zero` is the purest RLVR demonstration, trained with only rule-based rewards on top of the base model, with no SFT (Supervised Fine-Tuning, i.e. training on human-written examples) in between. DeepSeek's newer line (V3.1 and V4) packs both thinking and non-thinking modes into one model.
- Qwen3 - open weights from Alibaba. One unified model that supports both a thinking mode and a non-thinking mode, with an explicit thinking budget knob.
- Google Gemini 3 with Deep Think - Google's reasoning mode inside the Gemini family. It can spend tens of seconds, and sometimes minutes, of test-time compute on a truly hard problem.
- Anthropic Claude Opus 4.7 with extended thinking - Anthropic's reasoning mode, available as a first-class feature across the Claude 4.7 family.
- xAI Grok 4.1 with Think mode - xAI's reasoning model. It pairs the thinking step with DeepSearch over X and the web.

All of them share the same core idea: think first, answer later. The differences are in the size of the model, the training data, and whether the reasoning trace is shown to us or hidden.

## Common Mistakes when using LRMs

Now, let's look at a few common mistakes we must avoid.

Mistake 1: Using an LRM for everything.

If we use an LRM for a simple "translate this sentence" or "summarize this paragraph", we are paying `10x` to `30x` more cost and waiting `30` seconds for a task that a normal LLM would finish in `1` second. We must route only the hard tasks to the LRM.

Mistake 2: Ignoring the cost of reasoning tokens.

Even if the reasoning trace is hidden, we still pay for it. A query that returns `200` visible tokens may have used `15,000` reasoning tokens behind the scenes. We must always check the billing model.

Mistake 3: Adding "think step by step" to an LRM prompt.

The model is already trained to think step by step. Adding extra "think carefully" instructions usually does not help, and sometimes confuses the model. Keep the prompt clean and just state the problem.

Mistake 4: Not setting a thinking budget on production traffic.

[…493ln elided…]

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

[Showing lines 1-416 and 910-1288 of 1288; 493 middle lines (27.2KB) elided. Read artifact://73 for full output]
