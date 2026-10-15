> Source: https://outcomeschool.com/blog/how-does-fine-tuning-work

# How does fine-tuning work?
URL: https://outcomeschool.com/blog/how-does-fine-tuning-work
Published: 2026-07-27

How does fine-tuning work?

# How does fine-tuning work?

Authors
: - Name
: Amit Shekhar
Published on
: July 27, 2026

In this blog, we will learn about how Fine-tuning works. We will also see why we need it, how it works step by step with a simple example, how full fine-tuning and LoRA differ and when to use which one based on our use case.

We will cover the following:

- What is Fine-tuning?
- Why do we need Fine-tuning?
- How does Fine-tuning work step by step?
- A simple worked example with numbers
- Full Fine-tuning vs LoRA
- When to use Fine-tuning
- Tips before we Fine-tune
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Fine-tuning?

Fine-tuning is the process of taking a model that is already trained and training it a little more on our own specific data so that it becomes good at our specific task.

Fine-tuning means making small and careful adjustments to a model that already exists.

Consider a person who already knows how to cook many dishes. They have years of general cooking experience. Now, we want them to become an expert in only Italian food. We do not teach them cooking from zero. We only train them on Italian recipes for some time. Very soon, they become great at Italian food, while keeping most of the old cooking skills.

Note: Some of those old skills do get a little rusty, because all the recent practice was Italian. The same thing happens with models, so we must keep this in mind.

This is exactly what Fine-tuning does. We take a model that already knows a lot, and we teach it our special skill on top of that.

Let's visualize this as below:

```
   +---------------------+        +------------------+
   |   Base model        |        |   Our own        |
   | (already trained on |  +     |   examples       |
   |  huge general data) |        | (our task data)  |
   +---------------------+        +------------------+
              |                            |
              +-------------+--------------+
                            |
                            v
                   +------------------+
                   |   Fine-tuning    |
                   +------------------+
                            |
                            v
                   +------------------+
                   |  Fine-tuned model|
                   | (expert at our   |
                   |   task)          |
                   +------------------+

```

Here, we can see that we start with a base model that already knows a lot, add our own examples on top, and after Fine-tuning we get a new model that is an expert at our specific task.

The model we start with is called the base model or the pre-trained model. It is the cook who already knows general cooking.

Now, there is one more word that we will use again and again in this blog, so let's understand it right here. Inside a model, there are millions or even billions of small numbers. These numbers are called weights.

A weight is just a number inside the model that decides how much importance to give to something.

In simple words, weights are the "knowledge" of the model. When a model learns, it is simply adjusting these numbers again and again until it gets things right.

So, Fine-tuning means slightly adjusting these numbers by showing our own examples to the model.

## Why do we need Fine-tuning?

Let's understand the problem first, and then Fine-tuning will make complete sense.

Training a large model from zero is very costly. It needs a huge amount of data. It needs very powerful and expensive computers. It can take weeks or even months. Most people and most companies cannot afford this.

So, here comes Fine-tuning to the rescue.

Instead of building a model from zero, we take a model that big companies have already trained on massive data. This base model already understands language, grammar, facts, and general reasoning.

But, here is the catch. This general model does not know our specific needs.

Let's say we run a medical company. The general model can talk about many topics, but it does not answer in the exact medical style and accuracy we want. We do not want to spend millions to build a new model. We only want to adjust the existing one.

This way we can use Fine-tuning to solve the interesting problem of making a general model behave the way we want, without huge cost.

## How does Fine-tuning work step by step?

Now, let's understand how Fine-tuning actually works, step by step.

Step 1: Pick a base model.

First, we choose a pre-trained model. This is the model that already learned from huge general data. It already has good values for its weights.

Step 2: Prepare our own dataset.

Then, we collect examples that match our task. Each example usually has an input and the correct output.

Suppose we want our model to reply like a polite customer support agent. Our dataset will have customer questions as input and ideal polite answers as output.

The quality of this data is very important. Good examples lead to a good model. Bad examples lead to a bad model.

Step 3: Show the examples to the model.

After that, we feed our examples to the model one by one. For each input, the model makes a prediction.

Step 4: Measure the mistake.

The model's prediction is compared with the correct answer. How far apart the two are is called the loss.

In simple words, loss is a number that tells us how wrong the model is. It is always zero or more, because it measures the size of the mistake and not its direction. A big loss means a big mistake. A small loss means the model is close to correct. A loss of zero means the answer is exactly right.

Step 5: Adjust the weights.

Now comes the heart of Fine-tuning. The model slightly changes its weights to reduce the loss. This adjustment is done using a method called backpropagation with gradient descent.

We do not need to go deep into the math here. For the sake of understanding, just remember this: the model figures out which direction to nudge each weight so that the next prediction is a little better.

Step 6: Repeat many times.

Finally, Steps 3 to 5 are repeated again and again over all our examples. Each full pass over the data is called an epoch. After enough epochs, the loss becomes small. The model now answers the way we want.

We can picture the flow as below:

```
+---------+   +------------+   +-----------+   +-------------+
| Input   |   |   Model    |   |  Compare  |   |   Adjust    |
| (our    |-->| predicts   |-->| with the  |-->| the weights |
| example)|   | an output  |   |  answer   |   | (less loss) |
+---------+   +------------+   +-----------+   +-------------+
                    ^                                 |
                    |   the updated weights go back   |
                    +---------------------------------+

```

Here, we can see that each example flows from input to a prediction, then we compare that prediction with the correct answer to get the loss, then we adjust the weights to reduce that loss. The arrow at the bottom means the updated weights go back into the model, and then the next example flows through the same path. We repeat this again and again, until the loss becomes small.

This is how Fine-tuning works from start to finish.

## A simple worked example with numbers

The best way to learn this is by taking an example.

Let's say our model has only one weight, and we call it `w`. Right now `w = 2.0`. For a given input, the correct answer should be `10`, but the model predicts using a simple rule of `input * w`.

Suppose the input is `4`.

```python
# Our tiny model
weight = 2.0
input_value = 4
correct_answer = 10

prediction = input_value * weight  # 4 * 2.0 = 8.0
error = correct_answer - prediction  # 10 - 8.0 = 2.0

```

Here, we can see that the prediction is `8.0`, but the correct answer is `10`. So our model is short by `2.0`. We call this gap the error.

Now, the model adjusts the weight a little to reduce the mistake.

```python
# A small adjustment to the weight
learning_rate = 0.05
adjustment = learning_rate * error * input_value  # 0.05 * 2.0 * 4 = 0.4
weight = weight + adjustment  # 2.0 + 0.4 = 2.4

```

Here, we have nudged the weight from `2.0` to `2.4`. The `learning_rate` is a small number that controls how big each adjustment is. We keep it small so the model does not over-correct and jump past the answer.

Let's check the prediction again with the new weight.

```python
prediction = input_value * weight  # 4 * 2.4 = 9.6

```

Here, we can notice that the prediction moved from `8.0` to `9.6`. It is much closer to `10` than before. The model will keep repeating this nudging, and the prediction will keep getting closer as below:

```
   8.00  ->  9.60  ->  9.92  ->  9.98  ->  10.00

```

Here, we can see that each round moves the prediction closer to the correct answer, and after a few rounds it settles at `10`. This is exactly what learning looks like.

This tiny example uses only one weight. A real model does the same thing, but for billions of weights at the same time. That is the only difference.

This is how the model slowly learns during Fine-tuning.

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

## Full Fine-tuning vs LoRA

Now that we have learned the basic process, it is time to learn about the two common ways of doing Fine-tuning.

The first way is Full Fine-tuning. Here, we adjust every single weight in the model.

Advantage: The model can learn deeply and change a lot.

Disadvantage: It needs a lot of memory and powerful machines, because billions of weights are being updated and stored.

So, here is the catch with Full Fine-tuning. It is heavy and expensive for large models.

But again, we can have a better solution than this too.

The second way is LoRA, which stands for Low-Rank Adaptation.

In simple words, LoRA keeps the original weights frozen and only trains a small set of new, extra weights on the side. The big model stays untouched, and these small extra pieces carry our new learning.

Consider a thick book that is already printed. We do not want to reprint the whole book to add our notes. Instead, we add a few small sticky notes on the pages. The book stays the same, and our notes hold the new information.

LoRA works like those sticky notes. This makes Fine-tuning much cheaper and faster.

The structure looks like below:

```
   Full Fine-tuning                 LoRA
   ----------------                 ----

  +----------------+         +----------------+
  | All weights    |         | Original       |
  | get updated    |         | weights FROZEN |
  | (billions of   |         | (not touched)  |
  |  numbers)      |         +----------------+
  +----------------+                  +
                                +----------------+
                                | Small extra    |
                                | weights trained|
                                | (the sticky    |
                                |  notes)        |
                                +----------------+

```

Here, we can see that Full Fine-tuning updates every single weight in the model, while LoRA freezes the big original weights and only trains a small set of extra weights on the side. That is why LoRA needs much less memory and runs much faster.

LoRA is not the only cheap option here. Prefix Tuning also keeps the model frozen, but instead of extra weights on the side, it trains a small prefix that steers every attention layer.

Let me tabulate the differences between Full Fine-tuning and LoRA for your better understanding so that you can decide which one to use based on your use case.

| Point | Full Fine-tuning | LoRA |
| --- | --- | --- |
| What it changes | All weights of the model | Only add small extra weights |
| Memory needed | Very high | Low |
| Speed | Slow | Fast |
| Cost | High | Low |

We must choose based on our use case. If we have limited machines, LoRA is the practical choice. If we have heavy resources and need deep changes, Full Fine-tuning works well.

## When to use Fine-tuning

Now, the next big question is: when must we use Fine-tuning?

We must use Fine-tuning when we want the model to learn a specific style, tone, or skill that simple instructions cannot give.

Let's say we want every answer in the exact voice of our brand. Or we want the model to follow a strict medical or legal format. Or we want it to understand the special words used inside our company. In all these cases, Fine-tuning is a strong choice.

But, here is an important note.

Note: Fine-tuning is not always the first answer. If we only need to give the model some facts to read, a simpler method like giving the information directly in the prompt is often enough. We must Fine-tune when we want to change the model's behavior, not just feed it some facts.

So, now we know where we can use Fine-tuning.

The most famous example of this is InstructGPT, where Fine-tuning on human-written answers was the first step that turned GPT-3 into an assistant. We have a detailed blog on Decoding InstructGPT that covers that story from start to finish.

## Tips before we Fine-tune

Before we end, let's go through a few important tips.

First, focus on data quality. A small set of clean and correct examples beats a large set of messy examples.

Then, keep our examples consistent. If we want a polite tone, every example must be polite. Mixed signals confuse the model.

After that, start with LoRA if we have limited machines. It gives good results at low cost.

Finally, always test the model after Fine-tuning. We must check it on new examples that it never saw during training. This tells us if it truly learned or just memorized. We have a detailed blog on LLM Evaluation that covers this end to end.

If we follow these tips, our Fine-tuning will give strong and reliable results.

## Summary

Now, we have understood how Fine-tuning works.

We started with a model that already learned from huge general data. Then we showed it our own examples. For each example, the model made a prediction, measured the loss, and slightly adjusted its weights to reduce that loss. We repeated this many times until the model answered the way we wanted.

We also learned the two ways to do it. Full Fine-tuning changes all the weights, while LoRA only trains small extra weights to save cost and time.

This way we can use Fine-tuning to turn a general model into a specialist for our own task in a very simple way.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# How does Prefix Tuning work?
URL: https://outcomeschool.com/blog/how-does-prefix-tuning-work
Published: 2026-08-24
Author: Amit Shekhar

How does Prefix Tuning work?

# How does Prefix Tuning work?

Authors
: - Name
: Amit Shekhar
Published on
: August 24, 2026

Prefix Tuning is a method where we keep the entire large language model frozen and only train a small set of extra numbers, called the prefix, that every layer of the model looks at while it works.

In this blog, we will learn about Prefix Tuning, a cheap way to adapt a large language model to a new task without changing the model itself. It saves memory, saves money, and lets one big model serve many different tasks at once. We will also see why full fine-tuning is so expensive, how the prefix is added and trained without changing the model, how Prefix Tuning differs from full fine-tuning and prompt tuning and when to use which one based on our use case, where it falls short and how it compares with LoRA, and where it is used in the real world.

We will cover the following:

- What is a large language model?
- The problem: why full fine-tuning is expensive
- What is Prefix Tuning?
- Prefix Tuning = Prefix + Tuning
- How does Prefix Tuning work?
- The prefix is not real words
- Where the prefix is added
- How the prefix is trained
- How small is the prefix really?
- A simple code example
- Prefix Tuning vs Full Fine-Tuning
- Prefix Tuning vs Prompt Tuning
- Advantages of Prefix Tuning
- Limitations of Prefix Tuning
- Where Prefix Tuning is used

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a large language model?

Before jumping into Prefix Tuning, we must know what a large language model is.

A large language model, also called an LLM, is an AI model that has read a huge amount of text and learned to predict the next word.

In simple words, it is a system that understands and writes human language. Tools like ChatGPT, Claude, and Gemini are all built on large language models.

The model has learned its skills by adjusting billions of internal numbers. We call these numbers the parameters, or the weights. These numbers are the model's brain. They hold everything the model knows.

So, remember this one idea. A large language model is just a giant collection of numbers that together know how to handle language. Keep this "giant collection of numbers" picture in mind, because it will help us in the next section.

### The problem: why full fine-tuning is expensive

Now, let's understand the problem that Prefix Tuning solves.

Suppose we have a big model, and we want it to become very good at one specific task. For example, we want it to write polite customer support replies. The model is already good at general language, but we want to specialize it.

One of the ways to do this is called fine-tuning.

Fine-tuning means we take the trained model and continue training it on our own task, so its parameters get updated for that task.

In simple words, we keep teaching the model with our own examples until it gets good at our task.

But here is the catch. When we do full fine-tuning, we change every single one of the model's parameters. A modern model can have billions of parameters. Changing all of them needs powerful machines, a lot of time, and a lot of money.

And there is a bigger problem. Suppose we have ten different tasks. With full fine-tuning, we get ten full copies of the model, one for each task. Each copy is huge.

Let's picture this problem like below:

```
            Full Fine-Tuning

   task 1  --->  [ full model copy 1 ]   (billions of numbers)
   task 2  --->  [ full model copy 2 ]   (billions of numbers)
   task 3  --->  [ full model copy 3 ]   (billions of numbers)

   ten tasks = ten giant copies = huge storage and cost

```

Here, we can see that every new task forces us to store one more giant copy of the model. This does not scale. It is slow, costly, and wasteful.

So, here comes Prefix Tuning to the rescue.

### What is Prefix Tuning?

Prefix Tuning is a method where we keep the entire large language model frozen and only train a small set of extra numbers, called the prefix, that every layer of the model gets to look at while it works.

In simple words, we do not touch the big model at all. We only learn a tiny add-on for each task.

One thing to be clear about right from the start, because this is where most explanations go wrong. The prefix is not text that we paste in front of our sentence. It is not part of our input at all. It is a block of numbers that we hand to the machinery inside the model, in every single layer. We will see exactly where it goes and how it works in a moment.

[…343ln elided…]

### Limitations of Prefix Tuning

Now, let's be honest about the other side, because no method is perfect.

- It adds work to every attention step: The prefix adds extra keys and values at every layer, so attention now looks over a longer list at each step. That costs extra computing and extra memory, and the longer the prefix, the more it costs. How much this eats into the length of text we can actu

# What is InstructGPT? How GPT-3 Learned to Follow Instructions
URL: https://outcomeschool.com/blog/decoding-instructgpt
Published: 2026-08-13

What is InstructGPT? How GPT-3 Learned to Follow Instructions

# What is InstructGPT? How GPT-3 Learned to Follow Instructions

Authors
: - Name
: Amit Shekhar
Published on
: August 12, 2026

InstructGPT is the model that taught GPT-3 to follow human instructions in a way that is helpful, honest, and harmless, by learning from human feedback. This work led directly to ChatGPT.

In this blog, we are going to learn about InstructGPT, the model that taught GPT-3 to actually follow our instructions, and the work that led directly to ChatGPT.

We will cover the following:

- What is the InstructGPT paper?
- The building blocks we must know first
- The big picture: what InstructGPT does
- Why GPT-3 was not enough
- Helpful, Honest, and Harmless
- The three-step method
- Step 1: Supervised Fine-Tuning
- Step 2: The Reward Model
- Step 3: Reinforcement Learning with PPO
- The alignment tax
- The results
- What alignment looks like today
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is the InstructGPT paper?

InstructGPT takes GPT-3, which only knows how to predict the next word, and teaches it to follow a human's instructions in a way that is helpful, honest, and harmless. It does this by learning from human feedback.

This research was introduced by OpenAI in the paper "Training language models to follow instructions with human feedback" by Long Ouyang, Jeff Wu, Xu Jiang, and their team.

The idea is the bridge between a raw language model and a real assistant. GPT-3 was powerful, but it often did not do what people actually asked. InstructGPT fixed that. And the method it used, called RLHF, is the same method that powered ChatGPT later that year.

## The building blocks we must know first

Before jumping into the paper, we must know a few simple words.

- Pre-training - GPT-3 first reads a huge pile of internet text and learns to predict the next word. This gives it raw language skill.
- Fine-tuning - training the model a little more on a smaller, specific dataset to shape its behavior.
- Alignment - making the model do what the user actually wants, not just what is statistically likely. This is the whole goal of the paper.
- Reward - a single number that says how good an answer is. Higher is better.
- Reinforcement Learning (RL) - a way of training where the model tries something, gets a reward, and adjusts to earn more reward next time. We have a full blog on reinforcement learning.
- RLHF - Reinforcement Learning from Human Feedback. The reward comes from human opinions. We have a full blog on RLHF.

That is everything we need. Now, let's move to the big picture.

## The big picture: what InstructGPT does

Before going into the details, let's see the simple input-to-output view.

```
   GPT-3:        predicts the next word on internet text
                          |
                          |  add human feedback (RLHF)
                          v
   InstructGPT:  follows the user's instruction, helpfully and safely

```

Here, we start with GPT-3 and add a layer of human feedback on top. The result is a model that listens to instructions. The architecture does not change at all. It is the same GPT-3. Only the training changes.

## Why GPT-3 was not enough

GPT-3 was trained to do one thing: predict the next word on internet text. But "predict the next word" is not the same as "do what the user asked". This gap is called misalignment.

Let's see it with an example. Suppose we type this instruction:

```
Explain the moon landing to a 6 year old in a few sentences.

```

A raw next-word model has seen a lot of internet text where a line like this is followed by more lines like it. So it continues with lines like these:

```
Explain the theory of gravity to a 6 year old.
Explain the big bang theory to a 6 year old.

```

That is a perfectly reasonable next-word prediction. It is also completely useless. The model continued the pattern instead of answering the question. It did not understand that we wanted an answer, not more instructions.

So, here is the problem. The model is smart, but it does not know what we want from it. We needed a way to teach it our intent, and InstructGPT was introduced to solve this problem.

## Helpful, Honest, and Harmless

Before fixing the model, the paper had to define what "good behavior" even means. It used three simple goals, often called the three H's:

- Helpful - the answer should actually solve the user's task.
- Honest - the answer should not make up facts or mislead.
- Harmless - the answer should not cause harm to people.

These three words are the target. Everything InstructGPT does is aimed at making the model more helpful, more honest, and more harmless.

These three goals are trained into the model, and a separate safety layer checks inputs and outputs at runtime. We have a detailed blog on How do LLM guardrails work? that explains this layer step by step.

## The three-step method

InstructGPT teaches the model in three steps. This is the famous RLHF recipe. Here is the whole pipeline at a glance:

```
   Step 1            Step 2            Step 3
   +----------+      +----------+      +----------+
   |   SFT    | -->  |  Reward  | -->  |   PPO    |
   |          |      |  Model   |      |  (RL)    |
   +----------+      +----------+      +----------+

```

- Step 1 (SFT): humans write good answers, and the model imitates them.
- Step 2 (Reward Model): humans rank the model's answers, and a model learns to score them.
- Step 3 (PPO): the model writes answers, the reward model scores them, and the model learns to score higher.

The idea is simple. First we show the model good answers (Step 1). Then we teach a second model to judge answers the way humans do (Step 2). Then we let the first model practice, using the judge as its coach (Step 3). Let's decode each step.

## Step 1: Supervised Fine-Tuning

In the first step, OpenAI hired about 40 people, called labelers, to write good answers to many prompts. This created about 13,000 examples of "here is a prompt, and here is a good answer to it".

Then we fine-tune GPT-3 to imitate these answers. This is plain supervised learning: show the model the prompt, ask it to produce the answer, and correct it when it is wrong. We call the result the SFT model (Supervised Fine-Tuning).

This already helps a lot. The model now knows the basic style of following instructions. But it is not enough. We can only write so many examples by hand, and we can never show the model a good answer for every possible prompt in the world. We need a way for the model to keep improving on its own. That is where the next two steps come in.

## Step 2: The Reward Model

Writing good answers by hand is slow. But there is something humans find much easier than writing: comparing. It is hard to write the perfect answer, but it is easy to look at a few answers and say which one is best.

So in Step 2, we take a prompt, have the model produce several answers (between 4 and 9 of them), and ask a labeler to rank them from best to worst. The labeler does not give scores. They just put the answers in order.

Then we turn each ranking into pairs. If a labeler ranked 4 answers, we can make every possible pair of "this one is better than that one". The number of pairs from 4 answers is:

```
C(4, 2) = (4 x 3) / 2 = 6 pairs

```

For 9 answers, we get even more:

```
C(9, 2) = (9 x 8) / 2 = 36 pairs

```

So one ranking of 9 answers gives us 36 training pairs. This is why ranking is so efficient. A little human effort produces a lot of training data.

Now we train a separate model, called the Reward Model, to read a (prompt, answer) and output a single number: how good humans would find that answer. The reward model is a 6 billion parameter model, much smaller than the 175 billion GPT-3.

Training a scorer from human comparisons is not new here. It comes from the 2017 paper Deep RL from Human Preferences, which used the same math to teach a simulated robot a backflip.

How does it learn from pairs? For each pair, the reward model gives a score to the winning answer and a score to the losing answer. We want the winner's score to be higher. The exact formula it uses is:

```
loss = -log( sigmoid( r_w - r_l ) )

```

Let's define every symbol:

- `r_w` is the reward score the model gives the winning (preferred) answer.
- `r_l` is the reward score it gives the losing answer.
- `sigmoid` is a function that squashes any number into a value between 0 and 1. It turns the score gap into a probability.
- `log` is the natural logarithm.

Do not worry, we will break this down with actual numbers. The key part is `r_w - r_l`, the gap between the winner's score and the loser's score. The bigger this gap, the more sure the model is that the winner is better.

We will use small, round numbers here, just for the sake of understanding. In real training, the reward model produces these scores itself, and they can be any value.

Let's compute. Suppose the model scores the winning answer `r_w = 2.0` and the losing answer `r_l = 1.0`. The gap is `2.0 - 1.0 = 1.0`. Now apply sigmoid:

```
sigmoid(1.0) = 1 / (1 + e^-1.0) = 1 / (1 + 0.368) = 1 / 1.368 = 0.731

```

So the model thinks the winner is better with probability 0.731, about 73%. The loss for this pair is:

```
loss = -log(0.731) = 0.313

```

Now suppose training makes the model better, and it gives a bigger gap: `r_w = 3.0` and `r_l = 0.0`, a gap of 3.0:

```
sigmoid(3.0) = 1 / (1 + e^-3.0) = 1 / (1 + 0.050) = 0.953
loss = -log(0.953) = 0.048

```

The loss dropped from 0.313 to 0.048. So a bigger gap in favor of the winner gives a smaller loss, which is exactly what we want. And if the two answers tie (`r_w = r_l`), then sigmoid(0) = 0.5 and the loss is `-log(0.5) = 0.693`, the model is unsure. Training pushes the model to give better answers a clearly higher score.

This was the loss for one pair. Now, remember the 36 pairs we made from a single ranking of 9 answers. The model computes this same loss for every one of those 36 pairs and takes the average. So one human ranking teaches the model 36 times over.

Here is the full formula again:

```
loss = -log( sigmoid( r_w - r_l ) )

```

Now, every part of this formula is clear. We take the winner's score, subtract the loser's score, squash that gap with sigmoid to turn it into a probability, and take the negative log of it. That is the whole reward model in one line.

Now we have a model that can score any answer the way humans would. This is our automatic judge.

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

## Step 3: Reinforcement Learning with PPO

Now the final step. We have the SFT model that writes answers, and the reward model that scores them. We connect them in a loop:

```
   1. give the model a prompt
   2. the model writes an answer
   3. the reward model scores the answer
   4. nudge the model to make higher-scoring answers next time
   5. repeat

```

This loop is reinforcement learning. The algorithm used to do the nudging is called PPO (Proximal Policy Optimization), which we cover in detail in the PPO blog.

But there is a catch. If we only tell the model "get the highest score", it will cheat. It will find weird, broken text that fools the reward model into giving a high score, even though the text is nonsense. This is called reward hacking.

To stop this, we add a leash. We compare the new model to the SFT model from Step 1, and we punish it for drifting too far away. This leash is called a KL penalty. The reward the model actually receives is:

```
final reward = reward model score  -  beta x (how far it drifted from the SFT model)

```

Here `beta` is a small number that sets how strong the leash is. Let's see it with numbers. Suppose an answer gets a reward model score of `5.0`, and it drifted from the SFT model by an amount of `3.0`, with `beta = 0.2`:

```
final reward = 5.0 - 0.2 x 3.0 = 5.0 - 0.6 = 4.4

```

Now suppose the model drifts much further, by `10.0`:

```
final reward = 5.0 - 0.2 x 10.0 = 5.0 - 2.0 = 3.0

```

The further it drifts, the more reward is taken away. So the model is free to improve, but it cannot wander off into nonsense. The leash keeps it close to sensible language while still letting it climb toward better answers. Again, these numbers are just for the sake of understanding, the real training measures the drift for every word the model writes.

## The alignment tax

There was one more problem to solve. When we fine-tune the model with reinforcement learning, it gets better at following instructions, but it can get a little worse at some standard tasks it used to do well, like answering trivia or translating. This drop is called the alignment tax.

The fix was simple. While doing the reinforcement learning, OpenAI also mixed in a bit of the original next-word prediction task. This reminds the model to stay good at plain language while it learns to follow instructions. This version is called PPO-ptx, and it pays off most of the alignment tax without hurting how well the model follows instructions.

## The results

Human labelers preferred the answers from the 1.3 billion parameter InstructGPT over the answers from the 175 billion parameter GPT-3. Let's see how big that size gap is:

```
175 billion / 1.3 billion = about 135

```

So GPT-3 carried about 135 times more parameters, and the much smaller aligned model was still preferred. Size lost to alignment.

When comparing the same size, the 175B InstructGPT was preferred over the 175B GPT-3 about 85% of the time. The other improvements were:

- More honest. On closed tasks, InstructGPT made up facts about half as often as GPT-3 (a 21% hallucination rate, down from 41%).
- Less toxic. When asked to be respectful, it produced about 25% fewer toxic outputs than GPT-3.
- Much cheaper than pre-training. The whole alignment process used about 1.6% of the compute it took to pre-train GPT-3 in the first place. A tiny extra cost for a very big gain.

The lesson was huge. Alignment, not just size, is what makes a model useful. A smaller model that listens beats a giant model that does not. This is the insight that shaped every assistant we use today.

Later that year, OpenAI used the same recipe, adapted for conversations, to build ChatGPT. So InstructGPT is the direct ancestor of the chatbot that changed everything.

If we want to go deep into this, we build a Large Language Model (LLM) from scratch and design the full ChatGPT training-to-serving pipeline in our AI and Machine Learning Program at Outcome School.

## What alignment looks like today

The three-step RLHF recipe became the foundation of the whole field. But the field did not stop there. Let's decode the modern view, piece by piece.

- DPO (Direct Preference Optimization). Step 2 and Step 3 are a lot of work: train a reward model, then run a full reinforcement learning loop. In 2023, researchers found a shortcut. DPO skips the separate reward model and the RL loop entirely. It learns directly from the preference pairs with one simple loss. It is simpler, more stable, and cheaper, and it became the default for many open models.
- AI feedback instead of human feedback. Hiring 40 people to rank answers is slow and expensive. So labs started using another AI model as the judge, an idea called LLM as a judge. Anthropic's Constitutional AI takes this further: the model critiques and improves its own answers against a written list of principles, called a constitution.
- Verifiable rewards for reasoning. For tasks with a checkable answer, like math or code, we do not even need a human opinion. We just check if the answer is correct. This is called RL with verifiable rewards, and it powers the newest large reasoning models. The popular algorithm here is GRPO, which grades a whole group of answers together instead of training a separate scorer.

Through all of these changes, the core idea from InstructGPT stays the same: start with a base model, give it a signal of what good looks like, and keep it on a leash so it improves without breaking. That backbone is still the heart of alignment in 2026.

## Quick Summary

We have decoded the InstructGPT paper piece by piece. Let's recap each piece in one line.

- InstructGPT teaches GPT-3 to follow instructions using human feedback, without changing the architecture.
- The alignment problem is that "predict the next word" is not the same as "do what the user asked".
- Helpful, honest, harmless are the three goals of good behavior.
- Step 1, SFT: humans write about 13,000 good answers, and the model imitates them.
- Step 2, Reward Model: humans rank answers, we turn rankings into pairs, and a 6B model learns to score answers like humans do.
- Step 3, PPO: the model writes answers, the reward model scores them, and a KL leash stops it from cheating.
- The alignment tax is the small drop on other tasks, fixed by mixing in the original next-word training (PPO-ptx).
- The result: a 1.3B InstructGPT beat the 175B GPT-3, proving alignment matters more than size, and the same recipe gave us ChatGPT.
- Today: DPO simplifies it, AI feedback replaces human labeling, and verifiable rewards with GRPO power reasoning models.

Now, we have decoded InstructGPT piece by piece and understood how human feedback turned a raw word predictor into a helpful assistant.

### Does InstructGPT change the architecture of GPT-3?

No. The architecture does not change at all. InstructGPT is the same GPT-3, and only the training changes. It adds a layer of human feedback on top through supervised fine-tuning, a reward model, and reinforcement learning with PPO.

### Is a bigger language model always better than a smaller aligned one?

No. Human labelers preferred the answers from the 1.3 billion parameter InstructGPT over the answers from the 175 billion parameter GPT-3. GPT-3 carried about 135 times more parameters, and the smaller aligned model was still preferred. Alignment, not just size, is what makes a model useful.

### Why do labelers rank answers instead of writing more good answers?

Ranking is much easier and more efficient than writing. It is hard to write the perfect answer, but it is easy to look at a few answers and say which one is best. Also, one ranking of 9 answers gives 36 training pairs, so a little human effort produces a lot of training data.

### Is InstructGPT the same as ChatGPT?

No. ChatGPT came later that year, when OpenAI used the same RLHF recipe, adapted for conversations, to build it. So InstructGPT is the direct ancestor of ChatGPT. Both rely on the same idea of learning from human feedback.

### Do we still need a reward model and PPO to align a language model?

Not always. DPO skips the separate reward model and the reinforcement learning loop entirely, and learns directly from the preference pairs with one simple loss. It is simpler, more stable, and cheaper, and it became the default for many open models.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-426 and 770-1134 of 1134; 343 middle lines (19.2KB) elided. Read artifact://83 for full output]
