> Source: https://outcomeschool.com/blog/group-relative-policy-optimization-grpo

# Group Relative Policy Optimization (GRPO)
URL: https://outcomeschool.com/blog/group-relative-policy-optimization-grpo
Published: 2026-05-18

Group Relative Policy Optimization (GRPO)

# Group Relative Policy Optimization (GRPO)

Authors
: - Name
: Amit Shekhar
Published on
: May 18, 2026

In this blog, we are going to learn about Group Relative Policy Optimization (GRPO). We will also see how GRPO works step-by-step and when to use it based on our use case.

We will cover the following:

- What is GRPO?
- Why do we need GRPO?
- The problem with PPO.
- How does GRPO work?
- Step-by-step example.
- The GRPO objective in simple words.
- Advantages of GRPO.
- Practical things to keep in mind.
- When to use GRPO.
- Conclusion.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is GRPO?

Group Relative Policy Optimization is a reinforcement learning algorithm used to train Large Language Models. It improves the model by comparing a group of answers for the same question and pushing the model toward the better answers.

In simple words, GRPO does not need a separate value model to predict an expected reward at every step. Instead, it asks the model to produce many answers for the same question, scores all of them, and then teaches the model to prefer the answers that scored above the group average. Do not worry, we will learn about the value model in detail in the next sections.

Let's decompose the name:

GRPO = Group + Relative + Policy + Optimization

- Group: We generate a group of answers for the same question.
- Relative: We compare each answer relative to the others in the group.
- Policy: The policy is our Language Model that decides which words to generate.
- Optimization: We update the model so that it generates better answers next time.

GRPO was introduced by DeepSeek and was used to train their popular reasoning models. It is one of the key reasons their training was so efficient.

Let's say a teacher asks the same math question to 8 students in a class. Some students get it right, some get it wrong. The teacher does not give an absolute score to each student. Instead, the teacher looks at the class average and tells each student: "You did better than the class average, keep doing this." or "You did worse than the class average, try to do what the toppers did." This is exactly the spirit of GRPO.

### Why Do We Need GRPO?

We need GRPO because training Large Language Models with reinforcement learning is very expensive. The older approach, PPO, requires multiple large models running at the same time, which costs a lot of memory and compute. GRPO removes the most expensive part of PPO and still trains strong models.

Before jumping into GRPO in detail, we must first understand the problem with PPO. Once we see the cost of PPO, the design of GRPO will feel very natural.

### The Problem with PPO

PPO stands for Proximal Policy Optimization. PPO is a popular reinforcement learning algorithm used to train Language Models. It works, but it has a big cost.

In PPO, we use multiple models during training. The two most important ones for our discussion are:

- The policy model: This is the Language Model we are training. It generates the answer.
- The value model: This is a separate model that predicts how good a partial answer is at every step.

The value model is also called the critic.

Note: The value model is not the same as a reward model. A reward model gives a final score for a complete answer. The value model predicts the expected future reward at every step while the answer is still being generated. PPO uses both a reward model and a value model. GRPO keeps the reward model but removes the value model. This is the key point we must remember.

Now, the next big question arises: if we already have a reward model, why do we need a value model at all?

The reward model only gives one score for the complete answer. But the Language Model generates the answer one word at a time. We need to know which words helped and which words hurt. The reward model cannot tell us this because it only sees the full answer at the end.

This is where the value model comes in. The value model predicts the expected future reward at every step. Using this, we can calculate something called the advantage, which tells us how much better or worse each decision was compared to what was expected.

In simple words:

- The reward model scores the full answer.
- The value model helps us assign credit to each step inside the answer.

Without the value model, every word would get the same credit or blame for the final reward, which makes training unstable. So, the value model gives us a per-step learning signal. This is why PPO uses both models.

Now, the reverse question may also arise: if the value model predicts the reward, why do we still need a reward model?

The reason is simple. The value model is a learned predictor. It learns to predict what the reward will be at each step. But to learn this, it needs the actual reward as the truth. The reward model provides this truth.

In simple words:

- The reward model gives the actual score for the answer.
- The value model learns to predict what the reward model will say at each step.

Without the reward model, the value model has nothing to learn from. So, the reward model is the source of truth, and the value model is a learned approximator. They are not duplicates. They serve different roles.

But, here is the catch. The value model is almost the same size as the policy model. So, we are training two very large models at the same time. This means:

- We need a lot of memory.
- We need a lot of compute.
- Training becomes slow and expensive.
- The value model itself is hard to train accurately.

Now, the question is: can we get rid of the value model and still train the policy correctly? The answer is yes. We can keep the reward model and remove the value model. So, here comes GRPO to the rescue.

### How Does GRPO Work?

The main idea of GRPO is very simple.

Instead of using a separate value model to provide a baseline for each answer, GRPO uses the average score of a group of answers as the baseline.

That's the beauty of GRPO. The group itself becomes the baseline.

Now, an important question arises: if PPO needed the value model to give credit to each step inside the answer, how does GRPO work without one?

The answer is simple. GRPO does not try to assign credit to each step inside a single answer. Instead, it generates many complete answers for the same question and compares them as full sequences.

GRPO does not ask which word inside an answer was good or bad. It asks which complete answer was better than the group average. Then, every word in a good answer gets a small push to be more likely, and every word in a bad answer gets a small push to be less likely. Over many training examples, the model learns the patterns that lead to good answers.

In simple words:

- PPO assigns credit to each step inside one answer using the value model.
- GRPO assigns credit to each full answer using the group average.

This works very well for tasks where the final answer is what matters, like math, code, and reasoning. For these tasks, we do not need to know which word in the middle was the best. We only need to know which complete answer was the best, and that is exactly what GRPO learns.

Let's break it down step by step.

Step 1: Take a question from the training data.

Step 2: Ask the current policy model to generate a group of answers for the same question. Let's say we generate 8 answers.

Step 3: Score each of the 8 answers using a reward function. The reward can come from:

- A reward model trained on human preferences.
- A rule-based check, for example, did the answer solve the math problem correctly.
- A code execution check, for example, did the generated code pass the test cases.

Note: Remember, the reward model used here is not the value model we discussed in PPO. The reward model only gives a final score for each complete answer. We are not using a value model in GRPO.

Step 4: Calculate the average reward of the group. This average is our baseline.

Step 5: For each answer, calculate the relative advantage:

- If the answer scored above the average, it gets a positive advantage.
- If the answer scored below the average, it gets a negative advantage.

Step 6: Update the policy model. We push the model to make answers with positive advantage more likely, and answers with negative advantage less likely.

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
