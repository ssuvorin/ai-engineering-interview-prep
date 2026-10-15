> Source: https://outcomeschool.com/blog/continual-learning-in-llms

# What is Continual Learning in LLMs? Solving Catastrophic Forgetting
URL: https://outcomeschool.com/blog/continual-learning-in-llms
Published: 2026-06-01
Author: Amit Shekhar

What is Continual Learning in LLMs? Solving Catastrophic Forgetting

# What is Continual Learning in LLMs? Solving Catastrophic Forgetting

Authors
: - Name
: Amit Shekhar
Published on
: June 1, 2026

Continual Learning is the ability of a model, like an LLM, to keep learning new information over time, without forgetting what it has already learned.

In this blog, we will learn about Continual Learning in LLMs. We will understand what it is, why we need it, the big problem of catastrophic forgetting, the approaches used to solve it, and where it is used in the real world.

We will cover the following:

- What is Continual Learning?
- Why do we need Continual Learning in LLMs?
- The big problem: Catastrophic Forgetting
- Approaches to Continual Learning in LLMs
- Challenges in Continual Learning
- Real-world use cases

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Continual Learning?

Continual Learning is the ability of a model to keep learning new information over time, without forgetting what it has already learned.

In simple words, Continual Learning = Continual + Learning. The model continues to learn, again and again, as new data arrives.

The best way to learn this is by taking an example. Let's say we have a child. The child learns how to walk. Then the child learns how to talk. Then the child learns how to read. The child does not forget how to walk just because the child learned how to read. The child keeps adding new skills on top of the old skills.

This is exactly what we want from our LLMs. We want them to keep learning new things, without losing the knowledge they already have.

### Why do we need Continual Learning in LLMs?

The world keeps changing every single day. New events happen. New facts arrive. New technologies come into the picture. New words get added to our language. Our LLMs must keep up with this changing world.

Let's say we trained an LLM in the year 2023. The LLM knows everything till 2023. But what about the events of 2024, 2025, and 2026? The LLM does not know about them. The knowledge of the LLM becomes outdated.

So, we have two options to keep the LLM updated:

- Option 1: Train the LLM again from scratch with all the old data and the new data. This is very expensive. It takes a lot of time, money, and computing power.
- Option 2: Take the existing LLM and teach it only the new information. This is cheap and fast.

Option 2 is what we call Continual Learning. We keep updating the LLM with new knowledge, without training it from scratch.

The training step inside Option 2 is Fine-tuning. We have a detailed blog on How does fine-tuning work? that explains it step by step.

But, here is the catch. Option 2 has a big problem. The problem is called Catastrophic Forgetting.

### The big problem: Catastrophic Forgetting

Catastrophic Forgetting is when a model forgets the old knowledge while learning new knowledge.

The best way to understand this is by taking an example. Let's say we have an LLM that knows about Math, History, and Science. Now, we want to teach it about Sports. We take the LLM and train it only on Sports data.

What happens? The LLM now knows about Sports very well. But, the LLM has forgotten Math, History, and Science.

This is Catastrophic Forgetting. The model forgets the old things in a catastrophic way when it learns new things.

Why does this happen? Inside an LLM, there are billions of parameters. These parameters store all the knowledge. When we train the LLM on new data, these parameters get updated. The updation of these parameters overwrites the old knowledge.

It is like writing on a whiteboard. If we write new things on top of the old things, the old things get erased.

Here is a simple diagram showing what happens.

```
  Before training on Sports:
  +------+---------+---------+
  | Math | History | Science |
  +------+---------+---------+

  Train ONLY on Sports:
  +---------------------------+
  | Sports  Sports  Sports    |
  +---------------------------+
   ^ old knowledge overwritten

```

Here, we can see that the old knowledge of Math, History, and Science gets overwritten by the new Sports knowledge. The model is left knowing only the new thing.

So, the question is: how can we teach the LLM new things, without erasing the old things? The answer is the different approaches of Continual Learning. Let's learn about them.

### Approaches to Continual Learning in LLMs

There are mainly three approaches to solve this problem. Do not worry, we will learn about each of them in detail.

- Replay-based methods
- Regularization-based methods
- Parameter isolation methods

Let's understand each one.

#### Approach 1: Replay-based methods

In Replay-based methods, we mix the new data with some of the old data, and then train the model.

Let's take the same example. We have an LLM that knows about Math, History, and Science. Now, we want to teach it about Sports.

Instead of training the LLM only on Sports data, we mix some Math, History, and Science examples along with the Sports data. Then, we train the LLM on this mixed data.

This way, the LLM learns Sports, but it also keeps practicing Math, History, and Science. The LLM does not forget the old things.

It is like a student preparing for an exam. The student does not study only the new chapter. The student also revises the old chapters. So, the student remembers everything.

Advantage: It is simple and works well in practice.

Disadvantage: It brings back the training cost. To avoid forgetting, we mix the old data with the new data, so we end up training on a lot of extra data every time. This costs more computing power, more time, and more money. If we mix in too much old data, it becomes almost as expensive as training the model from scratch. That is the very thing we were trying to avoid.

The issue with this approach is the high training cost. Let's see how the next approach solve this issue.

#### Approach 2: Regularization-based methods

In Regularization-based methods, we protect the important parameters of the model from being changed too much.

Let's understand this with an example.

Inside an LLM, there are billions of parameters. Some parameters are very important for the old knowledge. Some parameters are not so important.

When we train the LLM on new data, we tell the model: "Hey, you can change the unimportant parameters freely. But, please do not change the important parameters too much."

This way, the important parameters stay almost the same. The old knowledge is preserved. The model uses the unimportant parameters to learn the new knowledge.

A popular method here is called Elastic Weight Consolidation (EWC). EWC figures out which parameters are important for the old knowledge, and it protects them during the new training.

It is like a person who is moving to a new city. The person learns the new roads, the new shops, and the new people. But, the person does not forget their family and old friends, because those memories are very important. The brain protects the important memories.

Advantage: We do not need to store the old data.

Disadvantage: It is hard to figure out which parameters are important. Also, if we protect too many parameters, the model cannot learn new things well.

The issue with this approach is the balance between protecting old knowledge and learning new knowledge. Let's see how the next approach solve this issue.

#### Approach 3: Parameter isolation methods

In Parameter isolation methods, we keep the old parameters frozen, and we add a small set of new parameters to learn the new knowledge.

Let's say we have an LLM with billions of parameters. We do not touch these parameters at all. We freeze them.

Then, we add a small set of new parameters on top of the LLM. We train only these new parameters on the new data.

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

This way, the old knowledge stays safe inside the frozen parameters. The new knowledge gets stored in the new parameters.

Here comes LoRA (Low-Rank Adaptation) to the rescue. In LoRA, we add small matrices to the LLM. We train only these small matrices on the new data. The original LLM is not touched.

It is like adding a new chapter to a book. The old chapters stay the same. The new chapter is added at the end.

Prefix Tuning belongs to this same family. There, the new parameters are a small prefix that supplies extra keys and values inside every attention layer, while the original LLM stays frozen.

Here, we can see that the old knowledge is fully safe, because we never touch the original parameters of the LLM.

Advantage: The old knowledge is fully preserved. It is also cheap because we train only a few parameters.

Disadvantage: Over time, if we keep adding new parameters for every new task, the model becomes bigger and bigger.

Now that we have learned about all three approaches, let's see them side by side. Here is a simple diagram comparing them.

```
  Replay-based:
    New Data + Old Data
        |
        v
    Train whole model

  Regularization-based (EWC):
    Important params .... [LOCKED]
    Unimportant params .. [free to change]
        |
        v
    Train on New Data

  Parameter isolation (LoRA):
    Original params ..... [FROZEN]
    Small new params .... [trainable]
        |
        v
    Train only new params

```

Here, we can notice the key difference. Replay-based methods retrain the whole model with old data mixed in. Regularization-based methods protect the important parameters while training. Parameter isolation methods freeze the original parameters completely and train only a small set of new parameters.

To learn Fine-tuning, Parameter-Efficient Fine-Tuning (PEFT), and LoRA in depth, check out our AI and Machine Learning Program at Outcome School.

### An alternative: Retrieval-Augmented Generation (RAG)

Now, the question is: do we always need to update the LLM to give it new knowledge? The answer is no. Here comes RAG into the picture.

There is another way. We can keep the LLM as it is, and we can give it the new knowledge from outside.

This approach is called Retrieval-Augmented Generation (RAG).

In RAG, we store the new knowledge in an external database. When the user asks a question, we first fetch the relevant information from the database. Then, we give this information to the LLM along with the question. The LLM uses this information to answer.

That external store is usually a vector database. We have a detailed blog on How does a Vector Database work? that explains how it stores and searches by meaning.

Here is a simple diagram showing how RAG works.

```
      User Question
           |
           v
  +-----------------+      +------------------+
  |   Retrieve      |<-----|  External        |
  |   relevant      |      |  Knowledge       |
  |   information   |      |  Database        |
  +-----------------+      +------------------+
           |
           v
  +-----------------------------+
  |   LLM                       |
  | (Question + Information)    |
  +-----------------------------+
           |
           v
        Answer

```

Here, we can see that the LLM itself is never changed. The new knowledge lives in the external database. The LLM simply reads the relevant information at the time of answering.

It is like a student giving an open-book exam. The student does not need to remember everything. The student can look up the book whenever needed.

Advantage: The LLM does not need to be retrained. New information can be added instantly by just updating the database.

Disadvantage: The LLM does not truly learn the new information. It just reads it when needed.

So, RAG is not exactly Continual Learning. But, it is a very popular way to keep LLMs updated with new information, without the problem of Catastrophic Forgetting.

If we want to go deep into RAG and Vector Databases, we have a complete program - check out our AI and Machine Learning Program at Outcome School.

### Challenges in Continual Learning

Continual Learning is a hard problem. Let's see the main challenges.

- Catastrophic Forgetting: As we discussed, this is the biggest problem.
- Cost of replay: If we use replay-based methods, we train on the old data again and again, which adds a lot of extra training cost.
- Computing cost: Training an LLM, even partially, is expensive.
- Evaluation: How do we know if the LLM has actually learned the new knowledge without forgetting the old? We need good evaluation methods.
- Stability vs Plasticity: The model must be stable enough to remember old things, and plastic enough to learn new things. Getting this balance right is hard.
- Data quality: If the new data has mistakes or bias, the LLM will learn those mistakes too. We must be very careful about the quality of the new data.

### Real-world use cases

Where do we use Continual Learning in LLMs? Let's see a few important use cases.

- Keeping the LLM updated with current events: News, sports scores, stock prices, and etc.
- Domain adaptation: Teaching a general LLM to become an expert in a specific field, like medicine or law.
- Personalization: Teaching the LLM about a specific user's preferences and style.
- Fixing mistakes: If the LLM gives a wrong answer, we can teach it the correct answer without retraining from scratch.
- Adding new languages: Teaching the LLM a new language without losing the old languages.

So, now we know where we can use Continual Learning in LLMs.

### Summary

This was all about Continual Learning in LLMs. Let's quickly recap what we have learned:

- Continual Learning is the ability of a model to keep learning new information, without forgetting the old.
- The main problem is Catastrophic Forgetting, where the model forgets old knowledge while learning new knowledge.
- There are three main approaches: Replay-based, Regularization-based, and Parameter isolation.
- RAG is a popular alternative that gives the LLM new knowledge from outside, instead of updating the LLM itself.
- Continual Learning is hard because of storage cost, computing cost, and the stability vs plasticity trade-off.

Now we must have understood Continual Learning in LLMs. The world of AI is changing very fast. Continual Learning is one of the most important areas of research today, because it helps our LLMs stay relevant in a world that never stops changing. It is a beautiful idea, because it brings our LLMs one step closer to how we humans learn.

### Is RAG the same as Continual Learning?

No. RAG is not exactly Continual Learning. In RAG, the LLM is never changed, and it just reads the new knowledge from an external database when needed. The LLM does not truly learn the new information, but RAG avoids Catastrophic Forgetting and new information can be added instantly.

### Why not just retrain the LLM from scratch with the new data?

Training the LLM again from scratch with all the old data and the new data is very expensive. It takes a lot of time, money, and computing power. Teaching the existing LLM only the new information is cheap and fast, and that is Continual Learning.

### Is LoRA a good choice for Continual Learning?

Yes. LoRA is a parameter isolation method, where the original LLM is frozen and only small new matrices are trained. The old knowledge is fully preserved, and it is cheap because we train only a few parameters. The downside is that the model keeps growing if we add new parameters for every new task.

### What is Elastic Weight Consolidation (EWC)?

Elastic Weight Consolidation (EWC) is a popular Regularization-based method for Continual Learning. It figures out which parameters are important for the old knowledge and protects them during the new training. The model then uses the unimportant parameters to learn the new knowledge.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# What is Recursive Self-Improvement (RSI)?
URL: https://outcomeschool.com/blog/what-is-recursive-self-improvement-rsi
Published: 2026-09-15
Author: Amit Shekhar

What is Recursive Self-Improvement (RSI)?

# What is Recursive Self-Improvement (RSI)?

Authors
: - Name
: Amit Shekhar
Published on
: September 15, 2026

Recursive Self-Improvement (RSI) is a process in which an AI system improves its own abilities, and then the improved version improves itself further, and this cycle keeps repeating.

In this blog, we will learn about Recursive Self-Improvement (RSI), the idea of an AI system that makes itself smarter, and then uses that new smartness to make itself even smarter, again and again. We will also see why it matters, how an AI gets better today, how the self-improvement loop works step by step, a simple example with numbers, what already exists in the real world today, why people talk about an intelligence explosion, where it works well and where it fails, and why keeping humans in the loop is very important.

We will cover the following:

- What is Recursive Self-Improvement?
- Why does Recursive Self-Improvement matter?
- How does an AI get better today?
- How does Recursive Self-Improvement work?
- A simple example with numbers
- Two kinds of improvement
- What exists in the real world today?
- Intelligence explosion
- Where it works well and where it fails
- Keeping humans in the loop
- Recursive Self-Improvement vs Normal Training

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Recursive Self-Improvement?

Recursive Self-Improvement is a process in which an AI system improves its own abilities, and then the improved version improves itself further, and this cycle keeps repeating.

In simple words, it is an AI that makes itself better, again and again, without waiting for a human to do it.

Here, AI means Artificial Intelligence, which is a computer program that can learn from data and do tasks that normally need human thinking.

Let's break the term into parts.

Recursive Self-Improvement = Recursive + Self + Improvement

- Improvement: Getting better at something. For an AI, this means solving more problems correctly, making fewer mistakes, or working faster.
- Self: The AI does the improving by itself. No human is sitting there and fixing it.
- Recursive: The result of one round becomes the starting point of the next round. The improved AI is the one that does the next improvement.

The word "recursive" is the most important word here. So, let's understand it with a simple example.

Let's say there is a student preparing for an exam.

A normal student studies from the notes given by the teacher. The teacher finds the weak topics of the student and tells the student what to study. Here, the teacher is doing the work of improvement.

A self-improving student finds the weak topics on their own and studies them without the teacher. Here, the student is doing the work of improvement.

Now, a recursively self-improving student does one more thing. After each round of study, the student not only knows more but also becomes better at the act of studying. The student learns how to find weak topics faster, how to make a better study plan, and how to remember things for longer. So, the next round of study is better and faster than the last one.

[…753ln elided…]

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

[Showing lines 1-384 and 1138-1566 of 1566; 753 middle lines (44.9KB) elided. Read artifact://41 for full output]
