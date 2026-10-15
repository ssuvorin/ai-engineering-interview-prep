> Source: https://outcomeschool.com/blog/proximal-policy-optimization-ppo

# Proximal Policy Optimization (PPO)
URL: https://outcomeschool.com/blog/proximal-policy-optimization-ppo
Published: 2026-05-16

Proximal Policy Optimization (PPO)

Outcome School

# Proximal Policy Optimization (PPO)

Authors
: - Name
: Amit Shekhar
Published on
: May 16, 2026

In this blog, we are going to learn about Proximal Policy Optimization (PPO). We will also see how PPO works step-by-step and how it is used in training Large Language Models with RLHF.

We will cover the following:

- What is Reinforcement Learning?
- What is a Policy?
- The problem with simple policy updates.
- What is Proximal Policy Optimization (PPO)?
- The key idea behind PPO: Clipping.
- The PPO objective function in simple words.
- How PPO works step-by-step.
- PPO in Large Language Models (RLHF).
- Advantages of PPO.
- Disadvantages of PPO.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

Before jumping into PPO, we must know a few basic concepts of reinforcement learning. Do not worry, we will learn about each of them in detail.

### What is Reinforcement Learning?

Reinforcement Learning is a way of teaching a model by giving it rewards for good actions and penalties for bad actions. The model learns by trial and error, and that too without being explicitly programmed.

Let's say we are teaching a dog a new trick. When the dog does the trick correctly, we give it a treat. When the dog does it wrong, we do not give a treat. Over time, the dog learns which actions lead to treats. This is exactly how reinforcement learning works.

In simple words, the model tries different actions, sees the rewards, and slowly learns which actions are better.

This was about Reinforcement Learning. Now, let's move to the next concept.

### What is a Policy?

A policy is the strategy that the model follows to decide what action to take in a given situation.

For the sake of understanding, let's take an example. Suppose we have a robot in a room. The room has many doors. The policy tells the robot which door to open in which situation. If the policy is good, the robot picks the right door. If the policy is bad, the robot picks the wrong door.

So, the goal of reinforcement learning is to find the best policy. The best policy gives the highest total reward over time.

Now that we have learned about a policy, it's time to learn about the problem we face while improving it.

### The Problem with Simple Policy Updates

Now, the question is: how do we improve the policy?

The simple idea is to update the policy in the direction that gives more reward. This is called policy gradient. We compute how the policy should change to get a higher reward, and then we apply that change.

But, here is the catch.

If we update the policy too much in one step, the new policy becomes very different from the old policy. The model suddenly behaves in a strange way. The training becomes unstable. Sometimes the model gets worse and never recovers.

If we update the policy too little, the training becomes very slow. The model takes forever to learn.

For the sake of understanding, let's take an example. Suppose we are learning to ride a bicycle. If we turn the handle too much, we fall. If we turn the handle too little, we cannot steer. We need to turn the handle by just the right amount. This is the same problem in policy updates.

So, we need a balance. We need to update the policy enough to make progress, but not so much that the training breaks.

What is the solution to this problem? Answer: Proximal Policy Optimization (PPO).

So, here comes PPO to the rescue.

### What is Proximal Policy Optimization (PPO)?

Proximal Policy Optimization is a reinforcement learning algorithm that improves the policy in small, safe steps. It makes sure that the new policy stays close to the old policy.

Let's decompose the name:

PPO = Proximal + Policy + Optimization

- Proximal means close or nearby.
- Policy is the strategy the model follows.
- Optimization means making it better.

So, PPO is an algorithm that makes the policy better while keeping the new policy close to the old policy.

In simple words, PPO improves the model step by step, and each step is small and safe.

### The Key Idea Behind PPO: Clipping

The key idea behind PPO is clipping.

In simple words, clipping means cutting off the extreme values. If a value tries to go too high or too low, we cut it down to a safe range.

Let's say we have an old policy and a new policy. We measure how much the new policy differs from the old policy by computing a ratio.

- If the ratio is 1, the new policy is the same as the old policy.
- If the ratio is greater than 1, the new policy is more likely to take this action.
- If the ratio is less than 1, the new policy is less likely to take this action.

Now, PPO says: if this ratio goes too far from 1, we will clip it. We will not allow the update to push the policy too far.

In practice, PPO uses a small number called epsilon, which is usually 0.2. This means the ratio is allowed to stay between 0.8 and 1.2. If the ratio tries to go above 1.2 or below 0.8, PPO clips it.

Let's understand this with a simple number example. Suppose the new policy wants to take an action 3 times more than the old policy. Means, the ratio is 3. This is too far from 1. PPO will clip this ratio down to 1.2. So, the policy update is limited to a small change, even when the data wants to push it further.

This is how PPO keeps the new policy close to the old policy.

### The PPO Objective Function in Simple Words

The PPO objective function looks complex in math, but the idea is simple. Let's understand it in plain words.

The objective function is as below:

```
L = min( ratio * advantage, clipped_ratio * advantage )

```

Here, we have used the following:

- `ratio` is how much the new policy differs from the old policy.
- `advantage` tells us how much better or worse the action was compared to what was expected. The expected value comes from a separate value model that we train alongside the policy. A positive advantage means the action was better than expected, and a negative advantage means it was worse.
- `clipped_ratio` is the ratio clipped to stay between `1 - epsilon` and `1 + epsilon`.
- `min` means we take the smaller of the two values.

In simple words, PPO says: take the smaller value between the normal update and the clipped update. This makes sure that the policy does not change too much in one step.

Let's see a quick example. Suppose the advantage is positive, which means the action was good. The normal update would multiply the ratio by the advantage. If the ratio is very high, the policy would jump too much. The clipped value becomes the smaller one, and PPO uses that. The policy moves in the right direction, but in a small step.

Note: The `min` operation is what makes PPO safe. It prevents the policy from making large jumps even if the data suggests a big change.

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

### How PPO Works Step-by-Step

Now, let's see how PPO works step-by-step.

Step 1: Start with an initial policy. This is our old policy.

Step 2: Let the model interact with the environment using the old policy. Collect data about the actions taken and the rewards received.

Step 3: Compute the advantage for each action using the value model. The advantage tells us how much better or worse each action was compared to what the value model expected.

Step 4: Update the policy using the PPO objective function. The clipping makes sure the new policy stays close to the old policy.

Step 5: Repeat the same data multiple times to make full use of it. PPO can use the same data for many small updates, which makes it efficient.

Step 6: Replace the old policy with the new policy. Go back to Step 2 and repeat.

This is how PPO improves the policy step by step in a safe and stable way. The problem of unstable updates is solved.

To master Reinforcement Learning, PPO, and Reward Models, check out our AI and Machine Learning Program at Outcome School.

### PPO in Large Language Models (RLHF)

Now, let's take a real use case. PPO is famously used in training Large Language Models like ChatGPT. This process is called Reinforcement Learning from Human Feedback (RLHF).

The paper that made this pipeline famous is OpenAI's InstructGPT. We have a detailed blog on Decoding InstructGPT that explains all three of its steps in depth.

Let me explain how this works.

First, we have a Large Language Model that has been trained on a lot of text. This model can generate responses, but the responses are not always helpful or safe.

Then, humans rank different responses from the model. For example, for the same question, humans say which response is better.

After that, a reward model is trained on these human rankings. This idea of learning a reward from human comparisons goes back to a 2017 paper on games and robots. The reward model can give a score to any response. The higher the score, the better the response.

Once we've done that, PPO is used to update the Language Model. Here, the Language Model is the policy. The Language Model generates responses, the reward model scores them, and PPO updates the Language Model to generate higher-scoring responses.

Along with the policy, PPO also trains a value model, also called the critic. The value model predicts how good a response is expected to be before we see the actual reward. PPO uses the difference between the actual reward from the reward model and the value model's prediction to compute the advantage. The advantage tells us how much better or worse the response was compared to what was expected. This advantage is what PPO uses inside the clipped objective to update the policy.

So, in RLHF with PPO, we have four models working together. The policy model is the Language Model being trained. The value model predicts expected rewards. The reward model scores responses based on human preferences. The reference model is a frozen copy of the original Language Model.

We have a detailed blog on Direct Preference Optimization (DPO) that explains a simpler alternative for LLM alignment which avoids PPO and the reward model entirely.

Here is the important part. The updated Language Model must not become very different from the original Language Model. This is very important. If we update the model too much, it can start writing strange text or forget its language skills. Two things keep the model safe. First, PPO's clipping prevents large policy changes in any single update. Second, in RLHF we keep a frozen copy of the original model called the reference model. A KL penalty is added to the reward, which grows when the new model drifts away from the reference model. This pulls the new model back toward what it already knew.

That's the beauty of PPO. It improves the model while protecting what the model already knows.

This is how PPO helps in training models like ChatGPT to be more helpful and aligned with human preferences.

We have a complete program on RLHF, Fine-tuning, and LLM Internals - check out our AI and Machine Learning Program at Outcome School.

### Advantages of PPO

- Stable training. PPO does not make big jumps in policy updates. The training is smooth and reliable.
- Simple to implement. Compared to other advanced reinforcement learning methods, PPO is easier to code and understand.
- Sample efficient. PPO can use the same collected data for multiple updates, which saves time and computation.
- Works well in many domains. PPO has been used in robotics, games, and language models.
- Widely adopted. PPO is one of the most popular reinforcement learning algorithms in the industry.

### Disadvantages of PPO

- Hyperparameter sensitive. The value of epsilon and other settings can affect performance.
- Needs a value model. PPO trains a separate value model to estimate the advantage at each step. The value model is almost the same size as the policy, which adds significant memory and compute cost.
- Slower than some newer methods. Methods like GRPO are designed to be more efficient for specific tasks like training Language Models.
- Can still be unstable in some cases. Even with clipping, training can fail if the reward signal is noisy.

### Conclusion

Now, we have understood Proximal Policy Optimization.

PPO is a reinforcement learning algorithm that improves the policy in small, safe steps. The key idea is clipping, which keeps the new policy close to the old policy. This makes the training stable and reliable.

PPO is used in many areas, including training Large Language Models like ChatGPT through RLHF. Hence, it is one of the most important algorithms in modern AI.

Prepare yourself for AI Engineering Interview: AI Engineering Interview Questions

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# What is Direct Preference Optimization (DPO) and How Does It Work?
URL: https://outcomeschool.com/blog/direct-preference-optimization-dpo
Published: 2026-05-17
Author: Amit Shekhar

What is Direct Preference Optimization (DPO) and How Does It Work?

# What is Direct Preference Optimization (DPO) and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: May 17, 2026

Direct Preference Optimization (DPO) is a method to train a Large Language Model directly on human preference data, without using a separate reward model and without using reinforcement learning.

In this blog, we are going to learn about Direct Preference Optimization (DPO). We will also see how DPO works step-by-step and how it differs from RLHF (PPO).

We will cover the following:

- What is RLHF and why do we need it?
- The problem with RLHF.
- What is Direct Preference Optimization (DPO)?
- What is preference data?
- The key idea behind DPO.
- The DPO loss function in simple words.
- How DPO works step-by-step.
- DPO vs RLHF (PPO).
- Advantages of DPO.
- Disadvantages of DPO.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

Before jumping into DPO, we must know a few basic concepts. Do not worry, we will learn about each of them in detail.

### What is RLHF and Why Do We Need It?

RLHF stands for Reinforcement Learning from Human Feedback. It is a way of training a Large Language Model so that its responses match what humans actually prefer.

Let's say we have a Large Language Model that has already been trained on a huge amount of text. The model can generate responses to any question. But, here is the catch. The responses are not always helpful, safe, or in the tone that humans like.

Let's take an example. Suppose we ask the model: "How do I learn to code?" The model can give a very long, dry, and academic answer. But humans prefer a short, friendly, and step-by-step answer.

So, we need a way to teach the model what humans prefer. This is where RLHF comes into the picture.

In RLHF, humans look at different responses from the model and rank them. Then, a separate model called the reward model is trained on these rankings. After that, an algorithm like PPO (Proximal Policy Optimization) is used to update the Language Model so that it generates higher-scoring responses. During this update, we also keep a frozen copy of the original Language Model. This frozen copy is called the reference model, and it acts as a safety anchor so that the new model does not drift too far from what it already knew.

This full recipe comes from OpenAI's InstructGPT paper, which itself built on the 2017 Deep RL from Human Preferences paper. We have a detailed blog on Decoding InstructGPT that covers that pipeline end to end.

This was about RLHF. Now, let's see the problem with this approach.

### The Problem with RLHF

RLHF works, but it is complex. Let's see why.

First, we need to train a separate reward model. This reward model is another neural network that we must train, save, and run during training.

Then, we need to run a reinforcement learning algorithm like PPO. PPO is not easy to use. It needs careful tuning. The training can become unstable. The model can also start generating strange text if the reward model is not perfect.

On top of this, PPO also needs a value model, also called the critic. The value model predicts the expected reward at every step and helps PPO compute the advantage. The value model is almost the same size as the Language Model, so we are training two very large models at the same time. This makes the whole pipeline even more expensive.

So, the full RLHF pipeline has many moving parts: the base model, the reward model, the reference model, the value model, and the PPO algorithm. Each part can fail. Each part needs careful tuning. And that too, the whole process is slow and expensive.

For the sake of example, suppose we are trying to bake a cake. RLHF is like baking a cake using ten different machines, each with its own temperature setting. If any one machine fails, the whole cake is ruined. We need a simpler way.

What is the solution to this problem? Answer: Direct Preference Optimization (DPO).

So, here comes DPO to the rescue.

To learn RLHF, Reinforcement Learning, check out our AI and Machine Learning Program at Outcome School.

### What is Direct Preference Optimization (DPO)?

Direct Preference Optimization is a method to train a Large Language Model directly on human preference data, without using a separate reward model and without using reinforcement learning.

Let's decompose the name:

DPO = Direct + Preference + Optimization

- Direct means we go straight to training the model on preferences. No reward model in between.
- Preference is the human choice between two responses, telling us which one is better.
- Optimization means making the model better.

So, DPO is a method that makes the Language Model better by directly using human preferences, without any extra steps.

In simple words, DPO replaces the whole complex RLHF pipeline with a single, simple training step. It is like baking the cake using just one oven. It makes our life easy.

### What is Preference Data?

Before we go deeper, we must understand what preference data is.

Preference data is a collection of examples, where each example has three parts:

- A prompt, i.e., the question or instruction.
- A chosen response, i.e., the response that humans preferred.
- A rejected response, i.e., the response that humans did not prefer.

Let's see an example.

```
Prompt: How do I learn to code?

Chosen response: Start with one language like Python. Build small projects every day. Slowly take on bigger challenges. Stay consistent.

Rejected response: Coding is a vast field with many languages, frameworks, paradigms, and tools that one must learn over years of dedicated study.

```

Here, we can see that humans preferred the chosen response because it is short, friendly, and gives clear steps. The rejected response is too academic and not very helpful.

This is the kind of data that DPO uses. We give DPO many such pairs, and DPO teaches the model to generate responses that look like the chosen ones and not like the rejected ones.

Now that we have understood preference data, it's time to learn about the key idea behind DPO.

### The Key Idea Behind DPO

The key idea behind DPO is very clever.

[…313ln elided…]

That is the full idea. Notice that we never trained a separate value model. The group itself acts as the baseline. This is the core insight of GRPO and the reason it saves so much compute.

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

### Step-by-Step Example

The best way to learn this is by taking an example.

Let's say the question is:

> What is 12 + 7?

The correct answer is 19.

We ask our current policy model to generate 4 answers for this same question. We use a simple rule-based reward: 1 if the answer is correct, 0 if it is wrong.

- Answer 1: "The answer is 19." Reward = 1
- Answer 2: "It is 18." Reward = 0
- Answer 3: "19." Reward = 1
- Answer 4: "I think it is 20." Reward = 0

Now, let's calculate the group average.

- Group average reward = (1 + 0 + 1 + 0) / 4 = 0.5

Now, let's calculate the relative advantage for each answer:

- Answer 1: 1 - 0.5 = +0.5 (above average, good)
- Answer 2: 0 - 0.5 = -0.5 (below average, bad)
- Answer 3: 1 - 0.5 = +0.5 (above average, good)
- Answer 4: 0 - 0.5 = -0.5 (below average, bad)

In practice, GRPO also divides this difference by the standard deviation of the rewards in the group, so the advantages are normalized. But the core idea is the same.

Here, we can notice that the bad answers get a negative signal and the good answers get a positive signal. The model has been told what to do more and what to do less, all without a value model.

Now, we update the policy model:

- Increase the probability of generating Answer 1 and Answer 3 next time.
- Decrease the probability of generating Answer 2 and Answer 4 next time.

This is how the model slowly learns to produce more correct answers without ever needing a separate value model.

### The GRPO Objective in Simple Words

GRPO uses an objective function that has three parts. Do not worry, we will understand each part in simple words.

Part 1: The policy ratio

For each answer in the group, we compare the probability of producing that answer under the new policy versus the old policy. This ratio tells us how much the policy has changed for that answer.

Part 2: The clipping

We do not want the new policy to move too far from the old policy in one step. So, we clip the ratio inside a small range, for example between 0.8 and 1.2. This keeps training stable. This is the same idea as PPO.

Part 3: The KL penalty

We add a penalty that keeps the new policy close to a reference model. The reference model is usually the model right after supervised fine-tuning. This prevents the model from drifting too far and forgetting what it already learned.

Putting it all together:

- Multiply the clipped ratio by the group-based advantage.
- Subtract the KL penalty.
- Average this over all answers in the group and over all questions in the batch.

That is the full GRPO objective. The key change compared to PPO is that the advantage now comes from the group, not from a value model.

Let's see the simplified pseudocode for one training step of GRPO as below:

```python
# question: a single training prompt
# policy: the current Language Model we are training
# reward_fn: a function that scores an answer
# G: group size, for example 8

answers = [policy.generate(question) for _ in range(G)]
rewards = [reward_fn(question, a) for a in answers]

mean_r = mean(rewards)
std_r = std(rewards)
advantages = [(r - mean_r) / (std_r + 1e-8) for r in rewards]

# update the policy using the clipped ratio, advantages, and KL penalty
loss = grpo_loss(policy, old_policy, ref_policy, answers, advantages)
loss.backward()
optimizer.step()

```

Here, we can see that the only thing we need from the reward function is a score for each full answer. We do not need any value model. The group gives us the baseline for free.

### Advantages of GRPO

Let me tabulate the advantages of GRPO compared to PPO.

| Aspect | PPO | GRPO |
| --- | --- | --- |
| Value model needed | Yes | No |
| Reward model needed | Yes | Yes |
| Memory usage | High | Lower |
| Compute cost | High | Lower |
| Training speed | Slower | Faster |
| Baseline | Learned by value model | Average reward of the group |
| Implementation | Complex | Simpler |
| Best fit | Open-ended tasks | Reasoning tasks with verifiable rewards |

Here, we can see that GRPO removes the need for a value model, which is the most expensive part of PPO. This makes training much cheaper and easier to scale.

A few more advantages:

- Simpler implementation: We do not need to design and train a separate critic.
- Better for verifiable rewards: GRPO works very well when we can check the answer with a rule, for example math problems, code problems, and logic problems.
- Strong reasoning models: GRPO was used to train DeepSeek's reasoning models, which showed strong performance on math and coding benchmarks.

GRPO is also what trains Sakana's Fugu-Ultra to write effective multi-model workflows. We have a detailed blog on Sakana Fugu that explains how it uses GRPO to learn good orchestration.

### Practical Things to Keep in Mind

There are a few practical things we must know when using GRPO.

The group size matters. The group size is the number of answers we generate per question. A typical choice is 8 to 64. A larger group gives us a more stable baseline, but it also costs more compute. A smaller group is cheaper, but the average can be noisy. We must pick the group size based on our use case.

All answers in a group can sometimes get the same reward. Let's say all 8 answers are wrong, or all 8 answers are correct. Then the group average equals every individual reward, and the advantage becomes zero. In this case, the model gets no learning signal from this question. This is fine when it happens occasionally, but if it happens too often, we must pick harder or easier questions to balance the training data.

The reward function must be good. GRPO is only as good as the reward signal we give it. If the reward function is wrong, the model will learn the wrong behavior. For verifiable tasks like math and code, this is easy. For open-ended tasks, we need a strong reward model.

The reference model keeps things in check. The KL penalty against a reference model is very important. Without it, the model can drift and start producing strange outputs that score high on the reward function but are not actually useful. This is called reward hacking.

### When to Use GRPO

So, now we know where we can use GRPO. GRPO is a great fit in the following situations:

- When we want to train a Large Language Model with reinforcement learning.
- When we have a reward signal, especially a rule-based or verifiable reward.
- When we want to save memory and compute by avoiding a separate value model.
- When we are training reasoning models that need to think step by step before answering.

GRPO is now one of the most popular algorithms for training reasoning models. Many open-source teams have adopted it because it is simple, efficient, and effective. It makes our life easier.

### Conclusion

Now, we have understood Group Relative Policy Optimization.

GRPO is a reinforcement learning algorithm that trains Large Language Models by comparing a group of answers and pushing the model toward the better ones. The key idea is that the group average acts as the baseline, which removes the need for a separate value model. This makes training much cheaper, simpler, and faster than PPO.

GRPO has been used to train strong reasoning models, especially for tasks with verifiable rewards like math and code. Hence, it is one of the most important developments in modern AI training.

That's it for now.

Thanks

# What are Recursive Language Models (RLMs) and How Do They Work?
URL: https://outcomeschool.com/blog/recursive-language-models
Published: 2026-05-19

What are Recursive Language Models (RLMs) and How Do They Work?

# What are Recursive Language Models (RLMs) and How Do They Work?

Authors
: - Name
: Amit Shekhar
Published on
: May 19, 2026

In this blog, we will learn about Recursive Language Models (RLMs), a new way of using language models to handle very large inputs that do not fit in the model's context window.

We will cover the following:

- What is a Recursive Language Model (RLM)?
- Why do we need RLMs?
- How an RLM works
- How the model writes and runs code
- Why RLMs work better
- Recursion inside RLMs
- How RLMs differ from simple chunking
- Advantages of RLMs
- Limitations of RLMs
- When to use RLMs
- RLM vs RAG
- A real use case

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a Recursive Language Model (RLM)?

A Recursive Language Model (RLM) is a way of using a language model where the model can call another language model (or itself) on smaller parts of the input to solve a bigger problem.

In simple words, instead of putting the entire input into the model at once, the model breaks the input into smaller pieces and calls another language model (or itself) on those smaller pieces.

RLM = Recursive + Language Model

Here, Recursive means the model can call itself (or another model) again and again on smaller parts of the problem. Language Model is the LLM that understands and generates text.

## Why do we need RLMs?

The best way to learn this is by taking an example.

Let's say we have a very long document with 1 million tokens, and we want to ask a question about it.

When we put a lot of text into a language model, the following issues arise:

- The model has a context window limit. It cannot accept too many tokens at once.
- The quality of the answer goes down as the context gets longer. The model gets confused with too much information and misses important details in the middle. This is called context rot.
- The cost of running the model goes up.
- The speed of the model goes down.

This means, just making the context window bigger does not solve the problem. We need a better approach.

We have a detailed blog on The Lost in the Middle Problem in LLMs that covers this problem end to end.

So, here comes the Recursive Language Model to the rescue.

## How an RLM works

In an RLM, the main model does not directly read the full input. Instead, the full input stays inside a Python environment as a variable. The model gets a small prompt that only names this variable and explains how to use it. The model then writes code to read parts of the input and call other language models on those parts. The smaller calls return short answers, which the main model combines into the final answer.

The next section walks through this with a concrete example.

Now, the question is: why is this called recursive? The answer is, the model can call another model, which can again call another model, and so on. Each call works on a smaller piece. This is just like recursion in programming.

## How the model writes and runs code

Let's understand this with a real example. Suppose we have a long meeting transcript and we want to ask: "What were the action items?"

The model only generates text. It cannot run code by itself. So, we wrap the model with a Python environment. This environment has a variable `context` that stores the full transcript, and a function `call_llm(prompt)` that calls another language model.

Now, we send a short prompt to the main model:

```
Question: What were the action items?
Write Python code to answer this. The Python environment has:
- A variable named `context` that stores the full transcript.
- A function `call_llm(prompt)` that calls another language model.

```

Very important: The full transcript is never sent to the main model. Only the variable name `context` is sent in the prompt, not its actual content. The transcript stays inside the Python environment. The model can read parts of it through code, but the model never reads the whole thing. This is what keeps the main model's context small even when the input is huge.

Now, the loop runs as below:

Step 1: The model writes Python code as its response:

```python
turns = context.split("\n")
results = [call_llm(f"Find action items in: {turn}") for turn in turns]
print(results)

```

Here, the model decides to split `context` by turn and call `call_llm` on each one.

Step 2: The code runs in the Python environment. Each `call_llm` call sends one turn to another language model and gets back a short answer. All answers are collected into a list.

Step 3: The list is sent back to the model. The model now sees only the short answers, not the full transcript.

Step 4: The model reads the list and returns the final list of action items as the answer. If the answer was not clear yet, the model would write more code and the loop would continue.

This back-and-forth between the model and the Python environment is called an agentic loop.

So, the model is only generating text. The text just happens to be Python code. The Python environment runs the code. And `call_llm` is just an API call to another language model.

## Why RLMs work better

Here, we can notice that each smaller call gets a small input. In our transcript example, each `call_llm` call works on just one turn, not the full meeting. A small input is easy for the model to handle. The model can focus on the small piece and give a good answer.

Also, the main model only sees the small answers, not the full input. So, the main model has a clean and small context.

This way, we avoid context rot. The problem is solved.

## Recursion inside RLMs

Now, let's understand the recursive part more clearly.

Let's say one piece is still too long for the smaller call. The smaller call can also act as an RLM. It can again split its piece into even smaller parts and call another language model on each part.

So, the structure looks like below:

- The main RLM works on the full input.
- The main RLM calls sub-RLMs on each big piece.
- Each sub-RLM can again call sub-RLMs on each smaller piece.
- The smallest calls work on tiny pieces of text.

This is just like a tree. The top of the tree handles the big problem. The leaves of the tree handle the small pieces. Each level passes its answer up to the next level.

Note: The depth of recursion depends on the size of the input and the type of question. The model itself decides how deep to go.

That's the beauty of Recursive Language Models.

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

## How RLMs differ from simple chunking

Now, the next big question is: how is this different from just splitting the input into chunks and processing each chunk?

In simple chunking, we fix the chunk size beforehand. We send each chunk to the model, get an answer, and combine the answers. The split is fixed, and we always do the same steps.

In an RLM, the model itself decides how to split the input. The model also decides what to ask for each piece. The model can change its strategy based on the question.

So, how can we say RLM is smarter? The answer is, the RLM is more like a human reader. A human reader does not chunk a book into fixed pages. A human reader skims, jumps, reads carefully, and decides on the fly. An RLM works in a similar way.

This makes RLMs more flexible than simple chunking.

## Advantages of RLMs

- Handles very long inputs. RLMs can work with inputs much larger than the model's context window.
- Better accuracy on long context. Since each call works on a small piece, the model can focus and give better answers.
- Lower cost in some cases. We do not need to send the full input every time. We only send small pieces when needed.
- Modular thinking. The model can break a big problem into small problems, just like a human would.
- Flexible. The model decides how to split the input based on the question.

## Limitations of RLMs

- More complex to build. We need to set up a code environment and tool calls.
- Many model calls. One question can lead to many small calls. This can be slow.
- Errors can stack up. If a smaller call gives a wrong answer, the final answer can also become wrong.
- Hard to debug. Since the model writes its own code, it can be hard to know what went wrong.

So, RLMs are powerful, but we must use them carefully.

## When to use RLMs

I will highly recommend using RLMs for the following cases:

- We have a very long document and need to ask questions about it.
- We need to analyze a large codebase.
- We need to summarize a long meeting or transcript.
- We need to compare many files at once.
- The task can be broken into smaller, independent sub-tasks.

For short inputs, we do not need RLMs. A simple language model call is enough. We must choose the approach based on our use case.

## RLM vs RAG

Now that we have learned about RLMs, it's time to compare RLMs with another popular approach called RAG (Retrieval-Augmented Generation).

In RAG, we first search for the most relevant parts of a document and then send only those parts to the language model.

In RLM, the model itself decides how to explore the input. The model can write code, split the input, and call smaller models.

Let me tabulate the differences between RAG and RLM for your better understanding so that you can decide which one to use based on your use case.

| Feature | RAG | RLM |
| --- | --- | --- |
| How it picks data | A search step picks relevant parts first | The model itself explores the data |
| Flexibility | Less flexible, depends on the search step | More flexible, model decides what to do |
| Code execution | No code execution by the model | The model can write and run code |
| Best for | Question answering on a fixed knowledge base | Complex tasks on long inputs |
| Complexity | Easier to build | Harder to build |

For simple question answering, RAG is enough. For complex analysis on long inputs, RLM is a better fit.

To master RAG, Context Engineering, and Orchestration and Routing, check out our AI and Machine Learning Program at Outcome School.

## A real use case

A real use case in software development:

Let's say we want to find all the security issues in a large codebase. The codebase has hundreds of files. The total size is much bigger than what a normal model can read in one go.

With an RLM, we can do the following:

- Store the codebase as a variable.
- Ask the RLM: "Find all security issues."
- The RLM writes code to loop through each file.
- For each file, the RLM calls a smaller language model to find security issues in that file.
- The smaller calls return short lists of issues.
- The RLM combines all the issues into a final report.

Here, we can see that the main RLM does not read the full codebase. The main RLM only sees small summaries from each file. This keeps the main context clean and small.

This way we can use RLMs to solve the interesting problem of large codebase analysis.

## Summary

We have learned the following:

- A Recursive Language Model (RLM) is a way of using a language model that can recursively call other language models on smaller parts of the input.
- RLMs solve the problem of long context and context rot.
- The main model writes code to split the input and call smaller models.
- RLMs are powerful for long documents, codebases, and complex tasks.
- We must use RLMs carefully because they have more complexity and more model calls.

Now, we have understood Recursive Language Models (RLMs).

This way we can use RLMs to solve any problem on long inputs in a very simple way.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-364 and 678-1108 of 1108; 313 middle lines (18.9KB) elided. Read artifact://40 for full output]
