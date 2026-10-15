> Source: https://outcomeschool.com/blog/how-does-llm-watermarking-work

# How Does LLM Watermarking Work?
URL: https://outcomeschool.com/blog/how-does-llm-watermarking-work
Published: 2026-08-18

How Does LLM Watermarking Work?

# How Does LLM Watermarking Work?

Authors
: - Name
: Amit Shekhar
Published on
: August 17, 2026

LLM watermarking is a hidden signal that a model quietly leaves inside the text it writes. A secret key slightly nudges which words the model picks, without changing the meaning, and a detector with the same key can find this pattern later.

In this blog, we will learn about how LLM watermarking works, the hidden signal that a model quietly leaves inside the text it writes. We will also see why we need it, how an LLM picks one token at a time, how a secret key silently changes those choices without touching the meaning, how a detector finds that hidden pattern later, why the quality of the text does not break, how it is different from an AI text detector, and where it works well and where it fails.

We will cover the following:

- What is a watermark?
- Why do we need a watermark in LLM-generated text?
- How does an LLM write text?
- How does an LLM choose the next word?
- The hidden freedom that makes watermarking possible
- Here comes the secret key into the picture
- Preferred tokens and other tokens
- Slightly changing the probabilities
- Why the preferred set keeps changing
- One token vs thousands of tokens
- How does the detection work?
- How is this different from an AI text detector?
- Why the quality of the text does not break
- What happens when someone edits the text?
- Where is LLM watermarking used in the real world?
- Advantages and disadvantages of LLM watermarking

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a watermark?

Let's start with something we have all seen.

Take a currency note in our hand and hold it against the light. We will see a hidden design inside the paper. That hidden design is called a watermark.

Here, we can notice two things.

First, the watermark is not printed on top of the note like normal ink. It is created inside the paper itself.

Second, we do not see it while using the note in our daily life. It shows up only when we hold the note against the light and look for it.

So, a watermark is a hidden mark that stays quiet until someone checks for it. It answers one simple question: who created this?

Now, LLM watermarking does the same job for text.

LLM Watermarking = LLM + Watermarking

In simple words, it means putting a hidden mark inside the text that an LLM writes.

But here is the catch. Text has no paper and no light. We cannot hide a design inside a sentence. So, the watermark has to be hidden somewhere else.

In LLM watermarking, the mark is hidden inside the choice of words.

Do not worry, we will understand exactly how this happens, step by step.

### Why do we need a watermark in LLM-generated text?

Today, an LLM can write an essay, an email, an answer, a news article, or a review. And the text looks exactly like human writing.

So, the following question arises.

If someone shows us a piece of text, how do we know whether a human wrote it or a machine wrote it?

Let's see a few real situations.

A student submits a homework assignment. The teacher wants to know whether the student wrote it.

A website receives thousands of product reviews. The company wants to know whether real customers wrote them.

A news article spreads on social media. People want to know whether a human reporter wrote it.

In all these cases, we need a way to check the source of the text.

We cannot solve this by just reading the text, because good LLM writing looks completely normal. We needed a solution for that, and here comes LLM watermarking to the rescue.

The idea is simple. While the LLM is writing the text, it quietly leaves a hidden signal inside the text. Later, anyone who has the secret key can check that signal.

Now, to understand how this signal is hidden, we must first understand how an LLM writes text.

### How does an LLM write text?

Before jumping into watermarking, we must know one very important thing.

An LLM generates one token at a time.

Now, the question is, what is a token?

A token is a small piece of text. Most of the time, a token is a word or a part of a word. For the sake of understanding, we can think of a token as a word.

The LLM does not write the full answer in one shot. It writes one token, then looks at everything written so far, then writes the next token, and it keeps doing this again and again until the answer is complete.

This way of writing is called autoregressive generation. We have a detailed blog on Autoregressive Models that explains it in depth.

So, writing a paragraph of a few hundred words means the LLM made a few hundred separate decisions.

This is very important for us. Every one of those decisions is a chance to hide a signal.

### How does an LLM choose the next word?

The best way to learn this is by taking an example.

Suppose the text written so far is:

```
I am going to the ___

```

Now, the LLM has to pick the next token.

Here, we must understand that the LLM does not directly give us one word. First, the LLM gives a probability to every possible next token.

For our example, it can look like below:

```
office → 0.31
park   → 0.29
market → 0.22
gym    → 0.18

```

Here, we can see that the LLM is telling us how likely each token is.

The number `0.31` for `office` means the model thinks there is a 31 percent chance that `office` is the right next token. The number `0.29` for `park` means a 29 percent chance, and so on.

After this, the model picks one token from this list.

Without any watermark, the model picks the strongest option here.

```
Without watermark → office

```

So, the sentence becomes "I am going to the office".

Note: The model does not always pick the token with the highest number. Sometimes it picks a lower one on purpose, so that the writing does not feel repetitive. But the higher the number, the higher the chance of getting picked. That part stays true always, and this is the only part we need for this blog.

To learn Tokenization, LLM Internals, and Transformer Architecture, and to build a Large Language Model (LLM) from scratch, check out our AI and Machine Learning Program at Outcome School.

### The hidden freedom that makes watermarking possible

Now, let's look at those numbers once again.

```
office → 0.31
park   → 0.29
market → 0.22
gym    → 0.18

```

Here, we can notice something very interesting.

The gap between `office` at `0.31` and `park` at `0.29` is very small.

And more importantly, all four sentences are perfectly correct.

```
I am going to the office
I am going to the park
I am going to the market
I am going to the gym

```

If we read any one of these, nothing feels wrong. No grammar mistake. No strange meaning. Nobody would notice anything.

This small freedom is exactly where the watermark lives.

Means, at most of the steps, the LLM has many good options and no single option is the only correct one. So, we can gently push the model towards some of those good options without damaging the text.

Now, the next big question is: which options should we push?

If we always push the same words, people would notice a strange repeated style. So, the choice must look random. But at the same time, we must be able to reproduce the same choice later during the check, otherwise we can never detect the watermark.

So, how can we get something that looks random but can be reproduced? The answer is the secret key.

### Here comes the secret key into the picture

The secret key is used as a seed to create a random-looking but reproducible selection of tokens.

Let's understand the word seed with a simple example.

Suppose we have a deck of cards and a shuffling machine. We give the machine a number, and the machine shuffles the deck based on that number.

If we give the number `7`, the machine produces a particular order of cards. The order looks completely shuffled to us.

Now, if we give the number `7` again to a second machine with a fresh deck, we get exactly the same order again.

So, the number `7` is the seed. Here, we have got two things at the same time.

- The result looks random to anyone who does not know the seed.
- The result can be produced again by anyone who knows the seed.

This is exactly what the secret key does in LLM watermarking. The company that owns the model keeps this key private.

### Preferred tokens and other tokens

Before jumping into this part, we must know one more word: vocabulary.

The vocabulary is the full list of every token the model is allowed to write. Think of it as the dictionary of the model. A real model has around fifty thousand to a few hundred thousand tokens in its vocabulary.

We have a detailed blog on Byte Pair Encoding in LLMs that explains how this vocabulary is built in the first place.

Now, let's come back to our example.

The model is about to pick the next token after "I am going to the". At this exact step, the algorithm uses the secret key and splits the whole vocabulary into two groups.

For this particular step, the algorithm divides the vocabulary into two groups like below:

```
Preferred tokens: park, market, school...
Other tokens:     office, gym, house...

```

Note: This split has nothing to do with meaning or quality. It is not that `park` is a better word than `office`. It is more like a coin toss for every word in the vocabulary, and the secret key decides the result of every toss. The words simply landed on different sides.

In research papers, these two groups are called the green list and the red list. The name does not matter. The idea is the same. One group gets a small push, and the other group does not.

### Slightly changing the probabilities

Now, we have the original probabilities from the LLM, and we have the two groups.

The LLM's original probabilities are then slightly modified. The preferred tokens get a small boost, and the other tokens go down a little.

For example:

```
office → 0.31 → 0.25
park   → 0.29 → 0.36
market → 0.22 → 0.25
gym    → 0.18 → 0.14

```

Here, we can see what happened.

`park` and `market` are preferred tokens, so their numbers went up.

`office` and `gym` are other tokens, so their numbers went down.

And the order changed. Earlier `office` was on top with `0.31`. Now `park` is on top with `0.36`.

One more thing to notice. In both the lists, the four numbers add up to 1. The boost did not create anything extra. It only moved a little probability from the other tokens to the preferred tokens.

Now the model picks `park`.

So, the sentence becomes "I am going to the park".

And this sentence is completely normal. A reader has no way to feel that anything special happened here. The text reads exactly like ordinary writing.

Here, we must also know that the size of the push is a setting we can control.

A bigger push makes the watermark easier to detect, but it pulls the model away from its best words more often, so the quality drops. A smaller push keeps the writing better, but then we need a longer text before the pattern becomes clear.

So, there is a trade-off here, and we choose the value based on our use case.

### Why the preferred set keeps changing

The important part is:

The secret key does NOT permanently mark `park` as preferred.

At the next token, the key plus the current context can produce a different preferred set. In that new set, `park` can easily land in the other group and `office` can land in the preferred group.

So, the process keeps changing at every single step.

```
Secret key + context → preferred token set → small probability boost → next token

```

Let's read this flow once more, because this is the heart of LLM watermarking.

Secret key + context: At every step, the algorithm mixes the secret key with the text written so far.

Preferred token set: This mix decides which words are preferred at this exact step.

Small probability boost: The preferred words get a gentle push in their probability.

Next token: The model picks a token from these modified probabilities, and this new token becomes part of the context for the next step.

Then the whole cycle runs again for the next token, with a fresh preferred set.

This is why the watermarked text does not develop any visible habit. There is no fixed word that keeps coming back again and again. The preferred group is different at every step, so nothing repeats in a way that a reader can catch.

And there is one more reason, and it is a very important one.

Suppose the preferred group was fixed forever. Then anyone could generate a lot of text from the model, count which words keep coming a little too often, and slowly figure out the whole preferred group. After that, they could remove the watermark, or even worse, they could add a fake watermark to their own text and blame the model for it.

Because the group changes at every step, this attack does not work. Without the secret key, an outsider only sees ordinary words in an ordinary order.

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

### One token vs thousands of tokens

Now, let's ask the most natural question.

If the change at each step is so small, how can it ever be detected?

The answer is in the numbers.

One token → tiny change → looks completely normal.

But across thousands of tokens, preferred tokens appear more often than they would by chance.

Let's understand this with a coin.

Suppose we toss a fair coin 10 times and we get 6 heads. Nobody will find this strange. This happens all the time.

Now, suppose we toss the same coin 10,000 times and we get 8,000 heads. Now we know something is going on. A fair coin cannot behave like this. The number is too far from what luck can produce.

The same thing happens in watermarked text.

For any normal text written by a human or by a model without a watermark, roughly half of the tokens will fall in the preferred group and roughly half will fall in the other group. That is what pure chance gives us, because the split itself was like a coin toss.

But in watermarked text, the preferred group keeps getting a small push at every step. So, far more than half of the tokens end up in the preferred group.

Let's put some numbers on it. Suppose we have a text of 1000 tokens.

If the text has no watermark, around 500 tokens will fall in the preferred group. It can be 480 or 520, because chance is never exact.

If the text has a watermark, we can see something like 750 tokens in the preferred group.

Now, 750 out of 1000 is not something luck can produce. Getting that number by pure chance is like tossing a fair coin 1000 times and getting 750 heads. It simply does not happen.

For one sentence, this difference means nothing. For a long paragraph, this difference becomes very hard to explain by luck.

This creates a statistical pattern.

Here, the word statistical simply means a pattern that cannot be seen in one place. We can find it only by counting over a large amount of text.

And that pattern is our watermark.

### How does the detection work?

Now that we have learned how the watermark is added, it is time to learn how it is detected.

The flow is like below:

```
Generated text → watermark detector → uses the secret key → checks the statistical pattern → Watermark detected

```

Let's go through it step by step.

Step 1: We give the text to the detector. The detector breaks the text into tokens, the same small pieces the model works with.

Step 2: The detector goes to the first token and looks at the context before it. Using the secret key and that context, the detector rebuilds the exact same preferred set that was used at that step. This is possible because the secret key is a seed, and the same seed with the same context always gives the same result.

Step 3: The detector checks whether this token belongs to the preferred group or to the other group, and keeps a count.

Step 4: The detector moves to the next token and repeats the same thing, and it keeps going till the end of the text.

Step 5: At the end, the detector compares the count with what pure chance would give. If the number of preferred tokens is close to half, the text has no watermark. If the number is far above half, the watermark is there.

Now, we have understood the detection.

Here, we must notice a few very important points.

- The detector does not need the LLM. It only needs the text and the secret key.
- The detector does not need the original prompt.
- The detector does not need a stored copy of the generated text anywhere. Nothing is saved in a database. The proof is inside the text itself.
- The detector gives a confidence. It can say how unlikely this pattern is by chance, which makes the answer measurable.

One more thing to notice. The detector counts token by token, so it can also work on a part of the text. Suppose a student wrote half of the essay and the model wrote the other half. The detector can show that the pattern is strong in one part and absent in the other part.

But the detector does need the secret key.

This is a very important limitation. We cannot check a piece of text on our own. Only the company that owns the model, or someone they trust with the key, can run this check. And the moment the key leaks, anyone can strip the watermark or fake it, so the whole system depends on keeping that key safe.

This is how a watermark detector works.

### How is this different from an AI text detector?

Many of us must have used a tool that claims to tell whether a text was written by AI. Let's see how that is different from what we have learned here.

An AI text detector only reads the final text and guesses. It looks at the writing style, the sentence length, how predictable the words are, and things like that. Nobody gave it any secret. It is making an educated guess from the outside.

A watermark detector does not guess. The mark was placed inside the text on purpose while the text was being written, and the detector opens it with the secret key.

Let me tabulate the differences between the two for your better understanding.

| AI text detector | Watermark detector |
| --- | --- |
| Reads the final text and guesses from the style | Reads the hidden signal that was planted on purpose |
| Needs no key and no help from the model owner | Needs the secret key of the model owner |
| Works on text from any model | Works only on text from a model that added the watermark |
| Often marks human writing as AI writing by mistake | Gives a measurable chance of a mistake |

So, both have their place. The watermark detector is far more reliable, but it works only where the model owner has already done the work of adding the watermark.

If we want to go deep into Evaluation of LLMs and Agents, and LLM as a Judge, check out our AI and Machine Learning Program at Outcome School, where we cover them end to end.

### Why the quality of the text does not break

Now, one doubt must be coming to our mind.

If we are pushing the model away from its best answer, are we not making the text worse?

Let's understand this carefully.

The push is very small. Look at our example once again. `office` went from `0.31` to `0.25`, and `park` went from `0.29` to `0.36`. The model still picked a word that it already considered a good option. It just picked the second good option instead of the first one.

And there is one more thing. In many places, the model has almost no freedom at all.

For example, consider the text "The capital of France is ___". Here, the model gives something like below:

```
Paris → 0.99
Lyon  → 0.004
Nice  → 0.003

```

Here, `Paris` is at `0.99`. A small boost to some other token cannot beat `0.99`. So, the model still writes `Paris`.

This is very good for us. Where the answer must be a fact, the watermark stays out of the way. Where the model genuinely has many equally good options, the watermark does its work.

So, the watermark takes its space only from the freedom that the model already had.

This also tells us something about short text. If the text is only a few words long, there were very few free choices, so there is very little pattern to measure. A watermark detector needs enough tokens to be confident. Short text is hard to check, and long text is easy to check.

### What happens when someone edits the text?

This is a very practical question. Let's see a few cases.

Case 1: Changing a few words. Suppose someone changes ten words in a long article. The remaining hundreds of tokens still carry the pattern. The detector will still find the watermark, with slightly less confidence.

Case 2: Rewriting every sentence in different words. Now, most of the tokens are new choices made by a human or by another model. Those new tokens know nothing about our secret key, so they land in the preferred group only by chance. The pattern becomes much weaker, and the detector can miss the watermark.

Case 3: Translating the text into another language. Almost every token changes. The watermark is mostly gone.

So, the honest summary is:

- LLM watermarking is good against small edits.
- LLM watermarking is weak against heavy rewriting and translation.
- LLM watermarking works only when the model owner adds it, so text from a model without a watermark can never be caught this way.

This is why we must treat watermarking as one useful signal, and not as a final proof.

### Where is LLM watermarking used in the real world?

Now, let's take a real use case.

Google DeepMind built a system called SynthID, and one part of it, SynthID-Text, does exactly what we have learned in this blog. It changes the token selection slightly while the model writes, and a detector with the key can check the text later.

The same idea is used beyond text too. For images, audio, and video, a hidden signal is placed inside the pixels or inside the sound in a way that our eyes and ears cannot catch, but a detector can. We have a detailed blog on Multimodal AI that covers how models work across all of these together.

So, the core idea stays the same everywhere. Hide a signal in the small choices that nobody notices, and read it back later with the key.

### Advantages and disadvantages of LLM watermarking

Let's see the advantages and disadvantages of LLM watermarking.

Advantages:

- The text quality stays almost the same.
- Nothing needs to be stored in any database.
- The detection gives a measurable confidence, not a guess.
- The reader sees completely normal text.

- Heavy rewriting or translation removes the pattern.
- Short text cannot be checked with confidence.
- The secret key must be protected, because leaking it breaks everything.
- It works only for models that chose to add a watermark.

So, now we know where we can use LLM watermarking and where we must be careful.

### Summary

Let's recall everything in a short form.

An LLM writes one token at a time. At every step, it gives a probability to every possible next token, and then it picks one.

At most of those steps, many different tokens would give perfectly good text. This freedom is where the watermark lives.

The secret key acts as a seed. At every step, the key plus the current context splits the vocabulary into preferred tokens and other tokens. The preferred tokens get a small boost in their probability.

The preferred set is not fixed. It changes at every single step, so the text never develops a visible habit.

One token gets a tiny change, so nothing looks unusual. Thousands of tokens together produce far more preferred tokens than chance allows, and this becomes a statistical pattern.

The detector takes the text and the secret key, rebuilds the preferred set at every step, counts the preferred tokens, and compares the count with chance.

So, the watermark is not a visible mark.

It is a statistical pattern created by slightly changing the probability of which tokens get selected.

Now we must have understood how LLM watermarking works.

### Can anyone check whether a text has an LLM watermark?

No. The detector needs the secret key of the model owner. Only the company that owns the model, or someone they trust with the key, can run this check. If the key leaks, anyone can strip the watermark or fake it, so the whole system depends on keeping that key safe.

### Does the watermark detector need the original prompt o
