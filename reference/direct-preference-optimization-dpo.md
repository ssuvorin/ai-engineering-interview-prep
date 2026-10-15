> Source: https://outcomeschool.com/blog/direct-preference-optimization-dpo

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

In RLHF, we first train a reward model. The reward model gives a score to any response. Then, we use this score to train the Language Model.

The authors of DPO noticed something important. They noticed that the Language Model itself can act as its own reward model. We do not need a separate reward model at all.

In simple words, the probabilities that the Language Model gives to different responses already tell us how much the model prefers each response. If we use these probabilities in a clever way, we can train the model directly on the preference data.

So, DPO removes the reward model from the picture. The model is its own reward model. The training becomes a single step.

Let's take an example. Imagine asking a chef to make better dishes. With RLHF, we first hire a food critic, train the critic to score dishes, and then ask the chef to cook based on the critic's scores. With DPO, we directly tell the chef: this dish is better, this one is worse, learn from these examples. There is no food critic in between. The chef learns directly from the comparison.

Now, let's see how this works for our Language Model. Suppose we have a Language Model. For a given prompt, it assigns a higher probability to the rejected response than to the chosen response. This means the model prefers the rejected response, which is wrong. DPO will update the model so that the probability of the chosen response goes up and the probability of the rejected response goes down. After training, the model assigns a higher probability to the chosen response. Means, the model now agrees with human preferences.

This way, DPO turns the complex reinforcement learning problem into a simple supervised learning problem. The problem is solved.

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

### The DPO Loss Function in Simple Words

The DPO loss function looks scary in math, but the idea is simple. Let's understand it in plain words.

The DPO loss is as below:

```
Loss = -log( sigmoid( beta * ( log_ratio_chosen - log_ratio_rejected ) ) )

```

Here, we have used the following:

- `log_ratio_chosen` is the log of the ratio of the new model's probability to the reference model's probability for the chosen response.
- `log_ratio_rejected` is the log of the ratio of the new model's probability to the reference model's probability for the rejected response.
- `beta` is a small number that controls how much we are allowed to move away from the reference model. A common value is 0.1.
- `sigmoid` is a function that squashes any number into a value between 0 and 1.
- The reference model is the original model before training. We keep a frozen copy of it.

In simple words, DPO says the following.

We want the new model to give a higher probability to the chosen response than to the rejected response. At the same time, we do not want the new model to move too far away from the reference model. The `beta` controls this balance.

If `beta` is small, the new model is allowed to change a lot. If `beta` is large, the new model is forced to stay close to the reference model.

Note: The reference model is the safety anchor. It plays a similar role to the reference model used in RLHF with PPO. The new model is not allowed to drift too far from it and forget what it already knows.

For the sake of understanding, let's see what this loss does in practice. If the new model already strongly prefers the chosen response over the rejected response, the value inside `sigmoid` becomes large, `sigmoid` becomes close to 1, and the loss becomes close to 0. Means, the model is doing the right thing, so there is nothing to learn. But if the new model prefers the rejected response over the chosen response, the value inside `sigmoid` becomes negative, `sigmoid` becomes small, and the loss becomes large. The model then updates itself to fix this.

This is how DPO trains the model. It is just one loss function, and we minimize it like any normal supervised learning task.

### How DPO Works Step-by-Step

Now, let's see how DPO works step-by-step.

Step 1: Start with a pretrained Language Model. This model has usually been fine-tuned on instructions also. We also keep a frozen copy of this model. This frozen copy is called the reference model.

Step 2: Collect preference data. Each example has a prompt, a chosen response, and a rejected response.

Step 3: For each example, compute the probabilities of the chosen response and the rejected response. Compute these probabilities using both the new model and the reference model.

Step 4: Use the DPO loss function to compute the loss. The loss is high when the new model does not prefer the chosen response enough over the rejected response, compared to the reference model.

Step 5: Update the new model by minimizing the loss. This is the same as any normal training step using gradient descent, just like how we train any other neural network.

Step 6: Repeat Steps 3 to 5 for many examples and many epochs.

Once we've done that, the model is trained to follow human preferences. No reward model. No reinforcement learning. Just one simple training loop.

That's the beauty of DPO. It takes a problem that used to need a full reinforcement learning setup and solves it with a single loss function.

This is how DPO improves the model in a very simple way.

### DPO vs RLHF (PPO)

Now that we have learned about DPO, it's time to compare it with the RLHF approach.

Let me tabulate the differences between DPO and RLHF (PPO) for your better understanding.

| Aspect | DPO | RLHF (PPO) |
| --- | --- | --- |
| Reward model | Not needed | Needed |
| Value model (critic) | Not needed | Needed |
| Algorithm | Supervised learning | Reinforcement learning |
| Training stability | Stable | Can be unstable |
| Implementation | Simple | Complex |
| Compute cost | Lower | Higher |
| Hyperparameter tuning | Easy | Hard |
| Memory usage | Lower | Higher |
| Performance | Competitive in many cases | Strong, but harder to achieve |

In simple words, DPO is simpler, faster, and more stable. RLHF can sometimes give better results, but it needs much more effort.

Based on our use case, if we want a simple and reliable way to train on preferences, DPO is the better choice. If we have the resources and need the absolute best performance on complex tasks, RLHF is still useful in certain settings.

Both methods have their place. But DPO has become very popular because of its simplicity.

### Advantages of DPO

- No reward model. We do not need to train a separate reward model. This saves time, compute, and memory.
- No reinforcement learning. DPO uses simple supervised learning. We do not need to deal with the complexity of PPO.
- Stable training. Since there is no reinforcement learning, the training is much more stable.
- Simple to implement. The DPO loss function can be implemented in a few lines of code.
- Lower compute cost. DPO needs less memory and less computation than RLHF.
- Competitive performance. In many cases, DPO matches or beats RLHF in terms of final model quality.

### Disadvantages of DPO

- Needs paired data. DPO needs preference pairs (chosen and rejected). Collecting this data still requires human effort.
- Limited by data quality. If the preference data is noisy, the model can learn the wrong preferences.
- Hyperparameter sensitive. The value of `beta` affects performance and must be tuned carefully.
- Can overfit. Since DPO is supervised learning, it can overfit to the preference data, especially with small datasets.
- Less exploration. DPO does not explore new responses like reinforcement learning does. It only learns from the data we give it.
- Needs a good starting model. DPO works best when the model has already been fine-tuned on instructions. If the starting model is weak, DPO cannot fully fix it.

### Conclusion

Now, we have understood Direct Preference Optimization.

DPO is a simple and powerful method to train Large Language Models on human preferences. It removes the need for a separate reward model and reinforcement learning. The Language Model itself acts as its own reward model. The training becomes a single supervised learning step.

DPO has made it much easier to align Language Models with human preferences. Hence, it is one of the most important developments in modern AI training. Many state-of-the-art open-source Language Models today use DPO as part of their training.

### Does DPO remove the need for human preference data?

No. DPO removes the reward model and reinforcement learning, but it still needs preference pairs. Each example has a prompt, a chosen response, and a rejected response. Collecting this data still requires human effort, and if the data is noisy, the model can learn the wrong preferences.

### Why does DPO need a reference model?

The reference model is the safety anchor. It is a frozen copy of the original model, and it stops the new model from drifting too far and forgetting what it already knows. DPO compares the new model's probabilities against the reference model's probabilities for both the chosen and rejected responses.

### What value of beta should we use in DPO?

A common value of `beta` is 0.1. If `beta` is small, the new model is allowed to change a lot. If `beta` is large, the new model is forced to stay close to the reference model. Since `beta` affects performance, it must be tuned carefully.

### Can we apply DPO to a base model that is not instruction-tuned?

We can, but DPO works best when the model has already been fine-tuned on instructions. If the starting model is weak, DPO cannot fully fix it. DPO only learns from the preference data we give it, and it does not explore new responses like reinforcement learning does.

### Is DPO used to train real language models?

Yes. Many state-of-the-art open-source Language Models today use DPO as part of their training. It became very popular because of its simplicity. It replaces the complex RLHF pipeline with a single loss function that we minimize like any normal supervised learning task.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

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
