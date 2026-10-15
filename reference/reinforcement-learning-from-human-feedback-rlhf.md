> Source: https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf

# What is RLHF? Reinforcement Learning from Human Feedback Explained
URL: https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf
Published: 2026-05-14
Author: Amit Shekhar

What is RLHF? Reinforcement Learning from Human Feedback Explained

# What is RLHF? Reinforcement Learning from Human Feedback Explained

Authors
: - Name
: Amit Shekhar
Published on
: May 14, 2026

RLHF (Reinforcement Learning from Human Feedback) is a training technique where we teach a Large Language Model to produce the responses that humans prefer. We collect human preferences and turn them into a reward signal that guides further training.

In this blog, we will learn about Reinforcement Learning from Human Feedback (RLHF), the training technique that turns a raw pre-trained LLM into a helpful, honest, and safe assistant by teaching it from human preferences.

We will cover the following:

- What is RLHF?
- Why we need RLHF
- The Big Picture
- Stage 1: Supervised Fine-Tuning (SFT)
- Stage 2: Training the Reward Model
- Stage 3: RL Fine-Tuning with PPO
- The KL Penalty
- Putting It All Together
- Reward Hacking
- Common Mistakes
- Best Practices
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is RLHF?

RLHF (Reinforcement Learning from Human Feedback) is a training technique where we teach a Large Language Model (LLM) to produce responses that humans prefer, by collecting human preferences and converting them into a reward signal that guides further training.

In simple words, we let the model generate responses, we ask humans which response is better, and we update the model so that its future responses look more like the preferred ones.

RLHF = Reinforcement Learning + Human Feedback

Let's decode each part.

- Reinforcement Learning (RL) is a way of training a model where it learns by trial and error. The model takes an action, receives a reward, and adjusts its behavior to earn more reward over time. We have a detailed blog on Reinforcement Learning that goes deeper into this.
- Human Feedback means the reward does not come from a fixed automatic metric. It comes from real humans who compare model outputs and pick the better one.

So, RLHF is reinforcement learning, but the reward signal is shaped by what humans actually want. That is the whole idea.

This idea started with the 2017 paper Deep RL from Human Preferences, which taught games and robots this way, and OpenAI later brought it to language models in the InstructGPT paper, the work that led directly to ChatGPT. We have a detailed blog on Decoding InstructGPT that walks through that paper step by step.

## Why we need RLHF

A pre-trained LLM is trained to predict the next token (a token is a small chunk of text, i.e. a word or a part of a word) from a huge amount of internet text. After pre-training, the model knows a lot about language and the world. But it does not know how to be a good assistant.

If we just ask a pre-trained model "How do I bake a cake?", it can continue with another question, or with a list of recipe headlines, or with random text that looks like a web page. It is not because the model is broken. It is because the model was only trained to imitate text on the internet, not to be helpful.

We need a way to teach the model:

- Be helpful, not random.
- Follow instructions.
- Be honest, not make things up.
- Be safe, not produce harmful content.
- Be clear, not overly verbose.

These goals are very hard to write down as a fixed rule or a fixed loss function. There is no formula that says "this answer is helpful and that one is not".

But humans can easily look at two answers and say which one is better.

So, here comes RLHF to the rescue. RLHF is the bridge that takes simple human judgments like "Answer A is better than Answer B" and turns them into a training signal for the model.

Let's take a simple analogy for the sake of understanding. Imagine a new chef who has read every cookbook in the world. The chef knows a lot of recipes, but does not know what real customers actually like. So, the restaurant gives the chef a chance to cook many dishes, lets customers taste two versions side by side, and asks them to pick the one they prefer. Over time, the chef learns to cook the food that customers actually love. RLHF is exactly this, but the chef is the LLM and the customers are the human labelers.

## The Big Picture

Before we go into the details, let's understand the big picture.

RLHF is not a single training step. It is a pipeline with three stages.

In simple words:

RLHF = SFT + Reward Model + RL Fine-Tuning.

Here is a high-level view of the pipeline:

```
+------------------------+
|  Pre-trained Base LLM  |
+-----------+------------+
            |
            v
+------------------------+
|  Stage 1: SFT          |   <- learn to follow instructions
+-----------+------------+
            |
            v
+------------------------+
|  Stage 2: Reward Model |   <- learn what humans prefer
+-----------+------------+
            |
            v
+------------------------+
|  Stage 3: RL Fine-Tune |   <- improve LLM using reward
+-----------+------------+
            |
            v
+------------------------+
|  Aligned LLM (final)   |
+------------------------+

```

Each stage has a clear job:

- Stage 1 (SFT) teaches the model to behave like an assistant.
- Stage 2 (Reward Model) teaches a separate model to score answers the way a human would.
- Stage 3 (RL Fine-Tuning) uses that reward model to push the LLM toward higher-scoring answers.

We will learn later in the blog why we must start with SFT and not jump straight to the Reward Model or RL Fine-Tuning.

Now, let's decode each stage.

## Stage 1: Supervised Fine-Tuning (SFT)

The first stage of RLHF is Supervised Fine-Tuning, often called SFT.

Supervised Fine-Tuning is the step where we take the pre-trained base LLM and fine-tune it on a hand-picked dataset of high-quality prompt-response pairs written by humans.

The dataset is typically small but very high quality - around `10,000` to `100,000` carefully written prompt-response examples. We show the model many examples of "this is a good question, and this is a good answer", and we train it to imitate that style. This is classic supervised learning - we have inputs and we have correct outputs, and the model learns to map one to the other.

The dataset looks like this:

```
Prompt:    "Explain photosynthesis to a 10 year old."
Response:  "Photosynthesis is how plants make their food.
            They take sunlight, water, and air, and turn
            them into energy and oxygen..."

Prompt:    "Write a polite email asking for a deadline extension."
Response:  "Hi [Name], I hope you are doing well. I am writing
            to request..."

```

After SFT, the model has a much better starting behavior. It knows the shape of a good answer. It tries to follow instructions instead of continuing the prompt randomly.

But SFT alone is not enough. Why? Because we cannot write enough examples to cover every possible question and every possible nuance. And humans are much better at comparing two answers than at writing the perfect answer from scratch.

I have seen many beginners assume SFT is the final step. It is not. SFT is only the foundation that makes the next two stages work.

To learn Fine-tuning, PEFT, and LoRA in depth, check out our AI and Machine Learning Program at Outcome School.

This is where the next stage comes in.

## Stage 2: Training the Reward Model

This is where the Reward Model comes into the picture.

A Reward Model is a separate model that takes a prompt and a response and outputs a single number - a score that predicts how much a human would prefer that response.

Higher score means the human would likely prefer it. Lower score means the human would likely reject it.

How do we train the Reward Model?

We collect preference data from humans. The process is simple.

- We pick a prompt.
- We use the SFT model to generate two or more different responses to the same prompt.
- We show these responses to a human labeler.
- The human picks which response is better.

The dataset looks like this:

```
Prompt:    "How do I stay focused while studying?"

Response A: "Try the Pomodoro technique. Work for 25 minutes,
             then take a 5 minute break..."

Response B: "Just focus harder. Stop being lazy."

Human preference: A is better than B.

```

We collect thousands of such pairs - typically `30,000` to `100,000` preference pairs in real systems. Each pair gives us a clear signal: "A beats B for this prompt."

Now, we train the Reward Model. The Reward Model is usually started from the same SFT model, but its final layer is replaced with a small head that outputs a single number. For example, on the pair above, a trained Reward Model might output `Score(A) = 2.4` and `Score(B) = -1.1`. The exact numbers do not matter, only the gap: A scores higher than B.

The training objective is simple:

> Given a pair (A, B) where A is preferred, the Reward Model should give a higher score to A than to B.

Here is how the training works on one preference pair:

```
Reward Model Training (one pair):

  +-----------------------+
  | Prompt + Response A   | --> [ Reward Model ] --> Score(A)
  +-----------------------+                              |
                                                         |
                                                         | must be
                                                         | higher than
                                                         |
  +-----------------------+                              |
  | Prompt + Response B   | --> [ Reward Model ] --> Score(B)
  +-----------------------+

  Loss: push Score(A) above Score(B)
        (because the human picked A)

```

We repeat this for thousands of pairs. After training, the Reward Model has learned a rich, fuzzy idea of "what a good response looks like". It is not a hard rule. It is a learned function shaped by thousands of human judgments.

Note: The exact loss function used here is called the Bradley-Terry pairwise preference loss. For our purposes, the intuition "push Score(A) above Score(B)" is enough.

Note: The Reward Model is not the final LLM. It is a helper model. We will use it in the next stage to teach the actual LLM.

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

## Stage 3: RL Fine-Tuning with PPO

This is the stage that puts the RL in RLHF.

In RL Fine-Tuning, we treat the LLM as a policy and use a reinforcement learning algorithm to update its weights so that it generates responses that score higher on the Reward Model.

A policy, in reinforcement learning, is simply the function that decides what action to take next given the current situation. For our LLM, the "situation" is the prompt plus the tokens generated so far, and the "action" is which token to generate next. So, the LLM itself is the policy.

The most commonly used algorithm here is PPO (Proximal Policy Optimization). It is a popular reinforcement learning algorithm that updates the policy in small, controlled steps so that training stays stable. PPO uses a clip ratio (usually around `0.2`) which limits how much the new policy can differ from the previous policy in a single update.

Along with the policy, PPO also trains a Value Model, also called the Critic. The Value Model predicts how good a response is expected to be before we see the actual reward. PPO uses the difference between the actual reward from the Reward Model and the Value Model's prediction to compute the advantage. The advantage tells us how much better or worse the response was compared to what was expected. This advantage is what PPO uses inside the clipped objective to update the policy.

So, in RLHF with PPO, we have four models working together:

- Policy Model - the LLM being trained
- Value Model (Critic) - predicts expected rewards, used to compute the advantage
- Reward Model - scores responses based on human preferences (from Stage 2)
- Reference Model - a frozen copy of the SFT model, used for the KL penalty

This is a big part of why PPO-based RLHF is expensive. Newer algorithms like GRPO (Group Relative Policy Optimization), used in DeepSeek-R1, remove the Value Model entirely by computing the baseline from a group of sampled responses, which brings the count down to three models.

Let's see how the loop works.

- We sample a prompt from a training dataset.
- The current LLM (the policy) generates a response.
- The Reward Model scores that response.
- PPO uses this score to update the LLM's weights so that responses like this one become more likely if the score was high, and less likely if the score was low.

```
RL Fine-Tuning Loop:

   +---------------------+
   |   Sample a prompt   |
   +----------+----------+
              |
              v
   +---------------------+
   |  LLM generates a    |
   |  response           |
   +----------+----------+
              |
              v
   +---------------------+
   |  Reward Model gives |
   |  a score            |
   +----------+----------+
              |
              v
   +---------------------+
   |  PPO updates the    |
   |  LLM weights        |
   +----------+----------+
              |
              v
   +---------------------+
   |  Repeat for many    |
   |  prompts            |
   +---------------------+

```

After many such steps, the LLM becomes much better at producing responses that humans prefer. The improvement is not because we wrote better answers. It is because the model figured out, through trial and reward, what answers earn higher scores.

This is the heart of RLHF.

## The KL Penalty

There is one important detail we must understand.

If we let PPO push the LLM purely toward higher rewards, the LLM can drift very far from the SFT model. It can start generating strange, repetitive, or off-topic responses that happen to score high on the Reward Model but are actually bad.

This is a real problem in RLHF, and it is closely related to reward hacking which we will cover next.

To prevent this drift, we add a KL penalty to the training objective. KL stands for Kullback-Leibler divergence, which is a way to measure how different two probability distributions are. When two distributions are identical, KL is `0`. When they are very different, KL is a large positive number.

The KL penalty is a term that punishes the LLM if its output distribution moves too far away from the original SFT model's output distribution.

In simple words, we tell the model: "Yes, try to maximize the reward. But do not stray too far from how the SFT model was talking."

The full RL objective looks roughly like this:

```
Objective = Reward(response) - beta * KL(LLM, SFT_model)

```

Here:

- Reward(response) is the score from the Reward Model. We want this to be high.
- KL(LLM, SFT_model) measures how different the current LLM is from the SFT model. We want this to be small.
- beta is a knob that controls how strong the penalty is. In practice, `beta` is small, often somewhere between `0.01` and `0.2`.

A small numeric example. Suppose the Reward Model gives a response a score of `3.0`, and the KL divergence between the current LLM and the SFT model on that response is `4.0`, with `beta = 0.1`. The final objective value is `3.0 - 0.1 * 4.0 = 2.6`. If the model drifts further and KL jumps to `20.0`, the objective drops to `3.0 - 0.1 * 20.0 = 1.0`. So, drifting too far costs us reward, even when the raw Reward score is high.

Note: In real implementations, the KL penalty is usually applied per-token during generation and folded into the reward signal at every step, rather than computed once on the whole response. The formula above is the high-level abstraction.

Without the KL penalty, the model can collapse into nonsense that fools the Reward Model. With the KL penalty, the model stays grounded in good language while still learning to score higher.

## Putting It All Together

Now, let's put everything together to see how RLHF runs end to end.

```
+--------------------------------+
|     Pre-trained Base LLM       |
+----------------+---------------+
                 |
                 | (train on high-quality
                 |  prompt-response examples)
                 v
+--------------------------------+
|          SFT Model             |
|  (knows how to follow          |
|   instructions)                |
+----------------+---------------+
                 |
                 | (generate pairs of responses,
                 |  humans pick the better one)
                 v
+--------------------------------+
|       Preference Dataset       |
|   (A is better than B, etc.)   |
+----------------+---------------+
                 |
                 v
+--------------------------------+
|       Reward Model             |
|  (predicts human preference)   |
+----------------+---------------+
                 |
                 v
+--------------------------------+
|     RL Fine-Tuning Loop        |
|                                |
|  prompt -> LLM -> response     |
|        -> Reward Model -> score|
|        -> KL penalty vs SFT    |
|        -> PPO updates LLM      |
+----------------+---------------+
                 |
                 v
+--------------------------------+
|       Aligned Final LLM        |
+--------------------------------+

```

Three datasets, three models, one final aligned LLM. That is the full RLHF pipeline.

We have a detailed blog on Direct Preference Optimization (DPO) that explains a simpler alternative which skips the reward model and PPO entirely.

## Reward Hacking

Before we move on, we must talk about a very real problem in RLHF: reward hacking.

Reward hacking happens when the LLM finds a trick that earns a high score from the Reward Model, but the response is not actually good for the human.

The Reward Model is just a model. It is not a perfect judge. It has its own blind spots. If the LLM discovers one of those blind spots, it can exploit it.

Some examples:

- The model becomes overly long and confident, because the Reward Model was trained on data where long confident answers were often preferred.
- The model adds excessive "I am a helpful assistant" fluff, because that pattern correlated with high scores.
- The model refuses harmless questions out of caution, because refusals were sometimes safer than risky answers in the preference data.

This is why the KL penalty matters. This is also why we keep updating the preference data, retrain the Reward Model, and run multiple rounds of RLHF in practice. The Reward Model is only a proxy for human preference, and our job is to keep that proxy honest as the LLM gets better at exploiting it.

I am sure many of us must have seen chatbots that sound overly polite but say very less of substance. That pattern itself is a classic sign of reward hacking creeping into the model.

We have a complete program on RLHF, Evaluation of LLMs, and Fine-tuning - check out our AI and Machine Learning Program at Outcome School.

## Common Mistakes

Let's look at the common mistakes people make when applying RLHF.

Mistake 1: Skipping SFT. Some try to run RL fine-tuning directly on a base pre-trained model. The base model is too far from being a useful assistant, and PPO struggles to find any good signal. Always start with SFT.

Mistake 2: Using a weak Reward Model. The Reward Model is the heart of RLHF. If it is small, poorly trained, or trained on noisy data, the entire pipeline learns the wrong thing. The LLM can only become as aligned as the Reward Model allows.

Mistake 3: Ignoring the KL penalty. Without the KL penalty, the LLM drifts into reward-hacked nonsense. The KL penalty is not optional. It is what keeps the model grounded.

Mistake 4: One-shot data collection. RLHF is not a single pass. The first round of RLHF reveals weaknesses in the Reward Model and in the LLM. We must collect new preference data on the new model's outputs and retrain. Many real-world systems do this for several rounds.

Mistake 5: Confusing the Reward Model with the truth. The Reward Model is a learned approximation. It is not the ground truth of human preference. Treating it as if it were the truth leads straight to reward hacking.

Mistake 6: Ignoring the labelers. The whole pipeline rests on the quality and consistency of the human labelers. If labelers disagree a lot, or if the instructions are unclear, the Reward Model learns conflicting signals. Good RLHF starts with good labeling guidelines.

## Best Practices

Now, let's see the best practices that make RLHF actually work.

Best Practice 1: Start with strong SFT. A good SFT model gives the RL stage a clean starting point. Better SFT means easier and more stable RL fine-tuning.

Best Practice 2: Invest heavily in preference data quality. Clear labeling guidelines, multiple labelers per item, and ongoing audits of label quality matter more than the size of the dataset alone.

Best Practice 3: Keep the KL penalty alive throughout training. Tune the beta value carefully. Too low and the model drifts. Too high and the model barely learns anything new. I will highly recommend starting with a small `beta`, around `0.01` to `0.05`, and adjusting based on how the model behaves.

Best Practice 4: Iterate. Run RLHF in rounds. After each round, generate new responses with the updated LLM, collect fresh preferences on those responses, and retrain the Reward Model. This keeps the Reward Model from going stale.

Best Practice 5: Evaluate beyond the reward score. A high Reward Model score is not the goal. The goal is real human preference. Keep a held-out evaluation set where humans rate the final LLM directly, so we can catch reward hacking early.

Best Practice 6: Watch for over-refusal. RLHF often pushes models to be overly cautious. Track refusal rates on normal prompts. If the model refuses harmless questions, the preference data is biased and needs rebalancing.

Best Practice 7: Mix safety and helpfulness preferences. Use preference data that covers both helpfulness ("which answer is more useful") and safety ("which answer is safer"). This keeps the model balanced instead of drifting toward only one of the two.

## Quick Summary

Let's recap what we have learned.

- RLHF stands for Reinforcement Learning from Human Feedback. It is the technique that aligns a pre-trained LLM with what humans actually want.
- RLHF = SFT + Reward Model + RL Fine-Tuning.
- Stage 1: SFT teaches the base model to follow instructions using human-written prompt-response pairs.
- Stage 2: Reward Model is trained on pairs of responses where humans picked the better one. It learns to score any response the way a human would.
- Stage 3: RL Fine-Tuning uses PPO to update the LLM so its responses earn higher scores from the Reward Model.
- The KL penalty keeps the LLM close to the SFT model and prevents it from drifting into nonsense.
- Reward hacking is the model finding tricks that fool the Reward Model. Good labeling, KL penalty, and iteration are the main defenses.
- Common mistakes include skipping SFT, using a weak Reward Model, ignoring the KL penalty, and treating the Reward Model as ground truth.
- Best practices are strong SFT, high-quality preference data, careful KL tuning, iterative rounds, real human evaluation beyond the reward score, and balanced safety plus helpfulness data.

This is how RLHF turns a raw pre-trained LLM into a helpful, honest, and safe assistant.

### Why does RLHF ask humans to compare answers instead of writing perfect ones?

Humans are much better at comparing two answers than at writing the perfect answer from scratch. We also cannot write enough examples to cover every possible question and nuance. So, RLHF turns simple judgments like "Answer A is better than Answer B" into a training signal for the model.

### How many models are involved in RLHF with PPO?

Four models work together. The Policy Model is the LLM being trained. The Value Model, or Critic, predicts expected rewards to compute the advantage. The Reward Model scores responses based on human preferences, and the Reference Model is a frozen copy of the SFT model, used for the KL penalty.

### Is PPO the only way to do the RL stage of RLHF?

No. PPO is the most commonly used algorithm, but newer algorithms like GRPO remove the Value Model entirely by computing the baseline from a group of sampled responses, bringing
