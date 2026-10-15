> Source: https://outcomeschool.com/blog/how-does-chain-of-thought-prompting-work

# How does Chain-of-Thought (CoT) Prompting work?
URL: https://outcomeschool.com/blog/how-does-chain-of-thought-prompting-work
Published: 2026-07-11
Author: Amit Shekhar

How does Chain-of-Thought (CoT) Prompting work?

# How does Chain-of-Thought (CoT) Prompting work?

Authors
: - Name
: Amit Shekhar
Published on
: July 11, 2026

Chain-of-Thought (CoT) Prompting is a technique where we ask the model to write out its reasoning steps before giving the final answer. In simple words, we ask the model to think out loud first, and this makes its answers more accurate.

In this blog, we will learn about how Chain-of-Thought (CoT) Prompting works. We will also see why a model that jumps straight to the answer often gets it wrong, how making it reason step by step fixes this, the difference between zero-shot and few-shot CoT, and where this technique is truly useful.

We will cover the following:

- What is a prompt?
- What is an LLM?
- The problem: when the model jumps straight to the answer
- What is Chain-of-Thought (CoT) Prompting?
- A simple example without CoT and with CoT
- Zero-shot CoT vs Few-shot CoT
- A step-by-step walkthrough of a reasoning chain
- Why does Chain-of-Thought Prompting work?
- Where Chain-of-Thought Prompting is useful
- Things to keep in mind

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a prompt?

Before jumping into Chain-of-Thought Prompting, we must know what a prompt is.

A prompt is the text instruction we give to an AI model. In simple words, a prompt is the question or the task we type in.

Let's say we open a chat-based AI tool and type, "What is the capital of France?". That sentence is the prompt. The model reads the prompt and gives us an answer.

So, a prompt is just our way of telling the model what we want.

### What is an LLM ?

Now, let's understand the kind of model we are talking about.

LLM = Large Language Model.

In simple words, an LLM is a model that has read a huge amount of text and learned to predict the next word. That is the most important idea here.

Let's say we type, "The sky is". The model has seen this kind of sentence many times, so it predicts the next word as "blue". It keeps doing this, one word after another, until the full answer is formed.

So, an LLM builds its answer word by word. It does not see the whole answer at once. It writes the answer the same way we speak a sentence, one word at a time.

This one-word-at-a-time way of generating text is called autoregression. We have a detailed blog on autoregressive models that explains it in depth.

This single idea will help us understand why Chain-of-Thought Prompting works so well.

### The problem: when the model jumps straight to the answer

Consider a simple math word problem.

> A shop has 12 apples. It sells 5 apples in the morning and buys 8 more in the evening. How many apples does the shop have now?

The correct answer is 15. We get this by doing 12 - 5 = 7, and then 7 + 8 = 15.

Now, suppose we just ask the model for the answer directly. The model tries to predict the final number immediately. It has not worked out the small steps. For an easy problem, it may get it right. But for harder problems, it often jumps to a wrong number.

Why does this happen? Because we forced the model to produce the answer in one shot. We did not give it room to think step by step.

The model writes word by word, so if it commits to a final number too early, it has no chance to correct itself.

This is the core problem. So, here comes Chain-of-Thought Prompting to the rescue.

### What is Chain-of-Thought (CoT) Prompting?

Chain-of-Thought (CoT) Prompting is a technique where we ask the model to write out its reasoning steps before giving the final answer.

In simple words, instead of asking for the answer directly, we ask the model to "think out loud" first.

Let's decompose the name to make it clearer.

Chain-of-Thought = Chain + of + Thought.

A thought is one small reasoning step. A chain is many small steps linked together, one after another. So a Chain-of-Thought is a series of small reasoning steps that lead us to the final answer.

Let's say we are solving the apple problem. The thoughts in the chain are like this:

- Thought 1: Start with 12 apples.
- Thought 2: Sell 5, so 12 - 5 = 7 apples.
- Thought 3: Buy 8 more, so 7 + 8 = 15 apples.
- Final answer: 15.

Here, we can see that each thought builds on the previous one. This is the chain. This is how Chain-of-Thought Prompting guides the model.

Let's visualize the difference between the two ways as below:

```text
   Without CoT (jump straight to the answer)

   Question --> [ guess the final number ] --> Answer (often wrong)

   With CoT (think step by step)

   Question
      |
      v
   Thought 1: start with 12 apples
      |
      v
   Thought 2: 12 - 5 = 7 apples
      |
      v
   Thought 3: 7 + 8 = 15 apples
      |
      v
   Final answer: 15 (more reliable)

```

Here, we can see that without `CoT` the model goes from the question straight to the answer in one jump. With `CoT` the question flows through small thoughts, one after another, and only the last thought gives the final answer.

### A simple example without CoT and with CoT

The best way to learn this is by taking an example.

First, let's see a prompt without Chain-of-Thought, as below:

```text
Q: A shop has 12 apples. It sells 5 in the morning and buys 8 in the evening.
How many apples does it have now? Give only the final number.

```

Here, we have told the model to give only the final number. The model is forced to jump straight to the answer with no thinking space. On harder problems, this often leads to mistakes.

Now, let's add Chain-of-Thought to the same prompt, as below:

```text
Q: A shop has 12 apples. It sells 5 in the morning and buys 8 in the evening.
How many apples does it have now? Let's think step by step.

```

Here, we have added one simple line at the end: "Let's think step by step." This small line is the trigger. It tells the model to write out its reasoning before the answer.

Now the model responds like below:

```text
We start with 12 apples.
After selling 5, we have 12 - 5 = 7 apples.
After buying 8 more, we have 7 + 8 = 15 apples.
So, the final answer is 15.

```

Here, we can notice that the model first writes the steps and only then gives the final answer. The reasoning is laid out clearly. This is Chain-of-Thought Prompting in action.

Problem Solved!

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

### Zero-shot CoT vs Few-shot CoT

Now, let's learn that there are two common ways to do Chain-of-Thought Prompting.

The first one is Zero-shot CoT.

In simple words, "zero-shot" means we give zero examples. We just add a line like "Let's think step by step" and the model starts reasoning on its own. This is the easiest way, and we already saw it above.

Let's see the Zero-shot CoT prompt again, as below:

```text
Q: If a train travels 60 km in 1 hour, how far does it travel in 3 hours?
Let's think step by step.

```

Here, we have given no example at all. We only added the magic line "Let's think step by step." The model figures out the steps by itself.

The second one is Few-shot CoT.

In simple words, "few-shot" means we give a few examples first. We show the model one or two solved problems with full reasoning. Then we ask our real question. The model copies the same step-by-step style.

Let's see a Few-shot CoT prompt, as below:

```text
Q: A box has 4 pens. We add 3 more pens. How many pens now?
A: We start with 4 pens. We add 3, so 4 + 3 = 7. The answer is 7.

Q: A jar has 10 candies. We eat 6. How many candies now?
A: We start with 10 candies. We eat 6, so 10 - 6 = 4. The answer is 4.

Q: A shelf has 8 books. We add 5 more. How many books now?
A:

```

Here, we have given two solved examples first. Each example shows the reasoning, not just the answer. After seeing this pattern, the model answers the third question in the same step-by-step way. It will write, "We start with 8 books. We add 5, so 8 + 5 = 13. The answer is 13."

So, Zero-shot CoT uses a simple instruction, and Few-shot CoT uses solved examples to teach the pattern.

Let me tabulate the differences between Zero-shot CoT and Few-shot CoT for your better understanding.

| Point | Zero-shot CoT | Few-shot CoT |
| --- | --- | --- |
| Examples given | None | A few solved examples |
| How reasoning is triggered | A line like "Let's think step by step" | Showing solved examples with steps |
| Prompt length | Short | Longer |
| Effort to write | Very less | More, because we write examples |
| Best for | Quick, common problems | Harder or unusual problems |

### A step-by-step walkthrough of a reasoning chain

Now, let's take a slightly bigger problem and walk through the chain step by step.

> Suppose a class has 30 students. 12 of them play football. Half of the remaining students play cricket. How many students play cricket?

Let's follow the chain.

Step 1: Start with 30 students in total.

Step 2: 12 students play football. So the remaining students are 30 - 12 = 18.

Step 3: Half of the remaining 18 students play cricket. So 18 divided by 2 = 9.

Step 4: So, the final answer is 9 students play cricket.

We can picture how the result of each step flows into the next as below:

```text
  Step 1            Step 2              Step 3            Step 4
+--------+      +-------------+     +-------------+     +--------+
| total  | ---> | remaining   | --> | cricket     | --> | final  |
| = 30   |      | = 30 - 12   |     | = 18 / 2    |     | answer |
|        |      | = 18        |     | = 9         |     | = 9    |
+--------+      +-------------+     +-------------+     +--------+
                     ^                    ^
                     |                    |
              uses total from      uses remaining from
                  Step 1                Step 2

```

Here, we can see that each step uses the result of the step before it. Step 2 needs the total from Step 1. Step 3 needs the remaining count from Step 2. This linking of steps is exactly why we call it a chain.

If the model tried to guess "9" in one shot, it could easily slip. But by working through each step, it stays on track. This is how Chain-of-Thought Prompting reduces mistakes.

### Why does Chain-of-Thought Prompting work?

Now, the next big question is: why does this simple trick work so well?

Remember the idea from earlier. An LLM writes its answer one word at a time, and each new word depends on the words written before it.

When the model writes out its reasoning, those reasoning words become part of what it reads next. So the model is now building its final answer on top of correct, visible steps, instead of guessing from nothing.

Let's say we are doing a hard calculation in our head. It is easy to make a mistake. But if we write each step on paper, we are far more likely to get it right. Chain-of-Thought Prompting gives the model that same "paper to write on".

Another reason is this. Breaking a big problem into small steps makes each step easy. The model is good at small, simple steps. By chaining many easy steps, it can solve a problem that looked hard as a whole.

So, the model is not getting smarter. We are just giving it room to think, and that too in a structured way. That's the beauty of Chain-of-Thought Prompting.

Some newer models are trained to produce these reasoning steps on their own, without us adding any special prompt. We have a detailed blog on large reasoning models that explains how this works.

### Where Chain-of-Thought Prompting is useful

Now, we know how it works. Let's see where we can use it.

- Math word problems, where we need many small calculations.
- Logic puzzles, where one wrong step breaks the whole answer.
- Multi-step questions, where the answer depends on earlier facts.
- Decision-making tasks, where we must weigh a few options before choosing.
- Reading comprehension, where we must connect different parts of a passage.

In all of these, the answer is not a single fact. It needs several steps. Chain-of-Thought Prompting fits these cases perfectly.

When one wrong first step can break the whole answer, we can go one step further and let the model try many paths, judge them, and go back when a path fails. We have a detailed blog on Tree of Thoughts that explains this step by step.

### Things to keep in mind

Now, let's discuss a few important points before we close.

- Chain-of-Thought Prompting helps most on hard, multi-step problems. For very simple questions like "What is the capital of France?", we do not need it. The answer is a single fact, so there is nothing to break into steps.
- The reasoning the model writes is helpful, but it is not always perfect. The model can write steps that look correct but still reach a wrong answer. So, for important tasks, we must check the steps ourselves and not blindly trust them.
- Writing out the steps means the model produces more text. More text takes a little more time and cost. For most tasks this is a fair trade for better answers, but we must keep it in mind based on our use case.

So, the idea is simple. Instead of asking the model for the answer directly, we ask it to think step by step. The model writes a chain of small thoughts, and each thought leads to the next, until we reach a reliable final answer.

This is how Chain-of-Thought Prompting works, and this is why such a small change in our prompt can make such a big difference.

### Does Chain-of-Thought Prompting make the model smarter?

No. The model is not getting smarter. We are just giving it room to think in a structured way. The reasoning words it writes become part of what it reads next, so it builds the final answer on top of visible steps instead of guessing from nothing.

### Should we use Chain-of-Thought Prompting for simple questions?

No. It helps most on hard, multi-step problems. For a simple question like "What is the capital of France?", the answer is a single fact, so there is nothing to break into steps. It fits math word problems, logic puzzles, and multi-step questions much better.

### Can we fully trust the reasoning steps the model writes?

No. The reasoning is helpful, but it is not always perfect. The model can write steps that look correct but still reach a wrong answer. So, for important tasks, we must check the steps ourselves and not blindly trust them.

### Does Chain-of-Thought Prompting increase time and cost?

Yes. Writing out the steps means the model produces more text, and more text takes a little more time and cost. For most tasks, this is a fair trade for better answers, but we must keep it in mind based on our use case.

### Do all models need a special prompt to reason step by step?

No. Some newer models are trained to produce these reasoning steps on their own, without us adding any special prompt. For other models, a simple line like "Let's think step by step" or a few solved examples triggers the reasoning.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
