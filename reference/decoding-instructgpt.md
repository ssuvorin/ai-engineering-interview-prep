> Source: https://outcomeschool.com/blog/decoding-instructgpt

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
