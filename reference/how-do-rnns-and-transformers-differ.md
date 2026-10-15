> Source: https://outcomeschool.com/blog/how-do-rnns-and-transformers-differ

# How do RNNs and Transformers differ?
URL: https://outcomeschool.com/blog/how-do-rnns-and-transformers-differ
Published: 2026-08-27
Author: Amit Shekhar

How do RNNs and Transformers differ?

# How do RNNs and Transformers differ?

Authors
: - Name
: Amit Shekhar
Published on
: August 27, 2026

An RNN reads a sequence one word at a time, carrying a memory of what it has seen so far, whereas a Transformer reads the whole sequence at once and uses attention, so that every word can look directly at every other word.

In this blog, we will learn about how RNNs and Transformers differ. These are the two main ways a computer reads a sequence like a sentence, and we will learn why one of them reads word by word, why the other reads everything at once, and when to use which one.

We will cover the following:

- What both of them are for
- What is an RNN?
- The problem with an RNN
- What is a Transformer?
- The key difference in one line
- RNN vs Transformer side by side
- Let's tabulate the difference
- When to use which one?
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What both of them are for

Both RNNs and Transformers are built to handle sequences. A sequence is data that comes in order, like the words in a sentence or the values in a time series.

The goal for both is the same: read a sequence and understand it. But they do it in two very different ways. Let's understand each one.

## What is an RNN?

An RNN, or Recurrent Neural Network, reads a sequence one step at a time, carrying a memory of what it has seen so far.

In simple words, it reads word by word, left to right. At each step, it combines the current word with a memory called the hidden state. Then it passes the updated memory to the next step.

```
   word 1  ->  word 2  ->  word 3  ->  word 4
     |           |           |           |
   memory  ->  memory  ->  memory  ->  memory
   (each step passes its memory to the next)

```

Here, we can see that an RNN works in order, one step after another. Each step must wait for the previous step to finish, because it needs that memory.

## The problem with an RNN

But, here is the catch. The step-by-step style causes two problems.

- It is slow. Because each step waits for the one before it, an RNN cannot process the whole sequence at once. This makes training slow.
- It forgets long-range information. By the time the RNN reaches the end of a long sentence, the memory of the early words has faded. So it struggles to connect words that are far apart.

```
   "The cat, which we found last summer near the old house, was ___"

   By the time the RNN reaches the blank, the memory of "cat"
   has faded, so it may struggle to fill it correctly.

```

Here, we can see the weakness. Long-range links are hard for an RNN. We needed a better solution, and the Transformer was introduced to solve this.

## What is a Transformer?

Now that we have learned about RNNs, it's time to learn about Transformers.

A Transformer reads the whole sequence at once and uses attention, which lets every word look directly at every other word.

In simple words, it does not go step by step. It looks at all the words together. Through a mechanism called attention, each word can directly focus on any other word, no matter how far away it is.

```
   All words are seen together:

   The   cat   was   on   the   mat
    \_____\_____\____/____/_____/
        every word can look directly
        at every other word (attention)

```

Here, we can see the big change. Because a Transformer sees all words at once, it can process them in parallel, which makes training fast. And because every word can look directly at every other word, long-range links are easy. The word at the end can look straight back at the word at the start.

We have a detailed blog on Encoder vs Decoder in Transformers that explains how the two parts of a Transformer work.

## The key difference in one line

> An RNN reads a sequence step by step with a fading memory. A Transformer reads it all at once, and every word can look directly at every other word.

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

## RNN vs Transformer side by side

Let's place both next to each other so that the difference becomes very clear.

```
        RNN                                 TRANSFORMER

   read one step at a time             read all words at once
   w1 -> w2 -> w3 -> w4                 w1  w2  w3  w4  (together)
   memory passed along                 attention connects all
   sequential, so slower               parallel, so faster
   long-range links fade               long-range links stay strong

```

## Let's tabulate the difference

Let me tabulate the differences between RNNs and Transformers for your better understanding.

| Point | RNN | Transformer |
| --- | --- | --- |
| How it reads | One step at a time | All words at once |
| Speed of training | Slow, steps wait for each other | Fast, done in parallel |
| Long-range links | Fade over distance | Stay strong through attention |
| Memory of the past | A single hidden state that fades | Direct attention to any word |
| Cost on long sequences | Grows gently with length | Grows quickly, since every word looks at every word |
| Main use today | Small or streaming tasks | Most modern language and vision models |

## When to use which one?

This is the real question. Let's make it very simple.

- Use a Transformer for most modern tasks, especially language. Transformers power today's large language models, because they train fast and handle long-range links well.
- Use an RNN for smaller tasks, or when data arrives one piece at a time in a stream, or on tiny devices where a Transformer would be too heavy. An RNN can also be lighter on very long sequences, where the Transformer's all-to-all attention becomes expensive.

We have a blog on Flash Attention in LLMs that explains how this attention cost is brought down on modern hardware, and another on Sliding Window Attention that explains how the cost is cut by letting every word look only at its neighbors.

## Summary

Let's quickly recap what we have learned.

- Both RNNs and Transformers handle sequences, but in very different ways.
- An RNN reads step by step and carries a memory, which is slow and forgets long-range information.
- A Transformer reads all words at once and uses attention, so every word can look at every other word.
- This makes Transformers fast to train and strong at long-range links, which is why they dominate today.
- RNNs still help on smaller tasks, streaming data, and tiny devices.

This is how RNNs and Transformers differ, and why Transformers power most modern models.

### Are RNNs obsolete now that we have Transformers?

No. RNNs still help on smaller tasks, when data arrives one piece at a time in a stream, and on tiny devices where a Transformer would be too heavy. An RNN can also be lighter on very long sequences, where the Transformer's all-to-all attention becomes expensive.

### Is a Transformer always cheaper to run than an RNN?

No. On long sequences, the cost of a Transformer grows quickly, since every word looks at every other word. The cost of an RNN grows gently with length. Techniques like Flash Attention and Sliding Window Attention are used to bring this attention cost down.

### Why do Transformers train faster than RNNs?

Transformers train faster because they read all the words at once and process them in parallel. An RNN reads one step at a time, and each step must wait for the previous step to finish because it needs that memory. This sequential style makes RNN training slow.

### Why do large language models use Transformers instead of RNNs?

Large language models use Transformers because they train fast and handle long-range links well. In an RNN, the memory of early words fades by the end of a long sentence. In a Transformer, attention lets the word at the end look straight back at the word at the start.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# Zero-shot, one-shot, and few-shot prompting - let's understand when to use what. | Pallavi .
URL: https://www.linkedin.com/posts/pallavi-shekhar_llm-prompting-ai-activity-7441801012472078336-JsHr
Published: 2026-03-23
Author: Pallavi .

# Zero-shot, one-shot, and few-shot prompting - let's understand when to use what. | Pallavi . · LinkedIn · 2026-03-23

**Pallavi .**: Software Engineer at Outcome School for 2 years 1 month with 8 years 1 month of total professional experience. Previous roles include Senior Software Development Engineer at West Agile Labs, Software Engineer at NCR Corporation, and Software Engineer at Deloitte India (Offices of the US). Based in Bengaluru, Karnataka, India [IN].

---

Zero-shot, one-shot, and few-shot prompting - let's understand when to use what.

When the task is straightforward - like translating a sentence - the model already knows how to do it. No examples needed. That's zero-shot.

But what if we want the output in a very specific format? Something the model can't guess on its own. We give one example to show the format - and the model follows it. That's one-shot.

Now think about this - we want the model to classify bug priority as P0 or P2. This is our own custom system. The model has no idea what counts as P0 in our team. So we give it a few examples to learn the pattern. That's few-shot prompting.

Zero-shot: The model already knows the task
One-shot: The model needs to learn your format
Few-shot: The model needs to learn your custom pattern

More examples = more context = better results for non-obvious tasks.

Follow Outcome School for knowledge-packed content.

#llm #prompting #ai

Zero-shot, one-shot, and few-shot prompting - let's understand when to use what. | Pallavi . image

## Comments

**AMIT SHEKHAR** · 2026-03-23
> Follow for knowledge-packed content.

**Shashikant pandey** · 2026-03-23
> Start lean,scale when dump everything at once.A full context window AI forget,confused and break results.

## Engagement

- Reactions: 24

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

# How does Tree of Thoughts work?
URL: https://outcomeschool.com/blog/how-does-tree-of-thoughts-work
Published: 2026-10-07
Author: Amit Shekhar

How does Tree of Thoughts work?

# How does Tree of Thoughts work?

Authors
: - Name
: Amit Shekhar
Published on
: October 7, 2026

Tree of Thoughts is a way of making an LLM solve a hard problem by trying many possible next steps, checking which ones look good, and going deeper only on the good ones, just like exploring the branches of a tree.

In this blog, we will learn about how Tree of Thoughts works. We will also see why a normal step-by-step answer fails on hard problems, what a "thought" means here, how the LLM generates and judges many thoughts, how a search algorithm walks through the tree and goes back when a path fails, a full walkthrough on the Game of 24, and where it works well and where it fails.

We will cover the following:

- How does an LLM answer?
- What is Chain of Thought?
- The problem with Chain of Thought
- What is Tree of Thoughts?
- What is a thought?
- Step 1: Breaking the problem into thoughts
- Step 2: Generating many thoughts
- Step 3: Judging the thoughts
- Step 4: Searching through the tree
- A complete example: the Game of 24
- A simple code sketch of Tree of Thoughts
- Chain of Thought vs Tree of Thoughts
- Where Tree of Thoughts works well and where it fails

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## How does an LLM answer?

Before jumping into Tree of Thoughts, we must know how an LLM gives an answer.

An LLM writes text one small piece at a time. The small piece of text that an LLM writes at a time is called a token. A token is a word or a part of a word. For the sake of understanding, we can think of a token as one word.

An LLM writes its answer from left to right, one token after another. Once it has written a token, it does not go back and change it. It just keeps moving forward.

Let's say we ask a friend to solve a puzzle, but with one strict rule: they must speak every step out loud, and they can never say "wait, let me try another way". If they take one wrong step early, the whole answer goes wrong. This is how a normal LLM answers.

## What is Chain of Thought?

Now, let's understand the idea that came before Tree of Thoughts.

Chain of Thought is a way of asking an LLM to write down its reasoning step by step before giving the final answer.

Suppose we ask: "A shop has 23 apples. It sells 20 and then buys 6 more. How many apples does it have now?"

Without Chain of Thought, the LLM jumps straight to an answer, and sometimes that answer is wrong.

With Chain of Thought, we add a line like "Let's think step by step." Now, the LLM writes:

```text
The shop starts with 23 apples.
It sells 20, so 23 - 20 = 3 apples are left.
It buys 6 more, so 3 + 6 = 9 apples.
The answer is 9.

```

Here, we can see that the LLM writes small steps one after another, like the links of a chain. Each step builds on the previous one. This trick makes LLMs much better at maths and logic problems.

We have a detailed blog on Chain-of-Thought Prompting that explains this in depth.

## The problem with Chain of Thought

Chain of Thought is still one single chain. The LLM picks one first step, then one second step, then one third step, and never looks back.

```text
Start
  ↓
Step 1
  ↓
Step 2
  ↓
Step 3
  ↓
Answer

```

If Step 1 is a bad choice, every step after it is built on a bad foundation. The LLM has no way to say, "This path is not working, let me go back and try a different Step 1."

Think about how we humans solve a hard puzzle, like a Sudoku or a maze. We try something. If it leads to a dead end, we go back and try something else. We also compare a few options in our head before picking one. We explore.

Chain of Thought does not explore. It just walks in a straight line.

So, the question is: how can we make an LLM explore many paths, check them, and go back when one path fails?

So, here comes Tree of Thoughts to the rescue.

## What is Tree of Thoughts?

Tree of Thoughts is a method where an LLM builds many possible reasoning paths in the shape of a tree, judges how promising each path is, and uses a search to keep the good paths and drop the bad ones.

It was introduced in 2023 in a research paper named "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" by Shunyu Yao and others from Princeton University and Google DeepMind.

Here, the thoughts are small steps of reasoning, and they are arranged like the branches of a tree. One starting point splits into many branches, and each branch splits again.

It looks like below:

```text
                     [Problem]
                         ↓
          +--------------+--------------+
          ↓              ↓              ↓
     [Thought A]    [Thought B]    [Thought C]
          ↓              ↓              ↓
     +----+----+        [B1]         dropped
     ↓         ↓         ↓
    [A1]      [A2]      [B2]
     ↓         ↓
  [Answer]  dropped

```

Here, we can notice that the LLM did not commit to one path. It tried three first thoughts. Path C looked hopeless, so it was dropped. Path A2 also failed. Path A1 reached the answer.

Tree of Thoughts is built from four parts:

- Breaking the problem into thoughts
- Generating many thoughts
- Judging the thoughts
- Searching through the tree

We will learn about each of them in detail.

## What is a thought?

Before going to the steps, we must understand what a "thought" means here.

A thought is one meaningful middle step towards solving the problem.

It is bigger than a single token, but smaller than the whole answer. The size of a thought depends on the problem:

- In a maths puzzle, one thought can be one equation, like `4 + 9 = 13`.
- In a crossword, one thought can be one word filled into the grid.
- In creative writing, one thought can be a short plan of the story.

A state is everything we have so far: the original problem plus all the thoughts on the current path. Each box in the tree above is a state.

Now, let's move to the four steps.

## Step 1: Breaking the problem into thoughts

First, we need to decide how to cut the problem into thought-sized steps.

The size matters a lot. If a thought is too small, like one word, the LLM cannot judge whether it is good or bad. If a thought is too big, like the whole answer, the LLM cannot create many different options for it.

So, we pick a size where the LLM can create a few different options and also judge them. This choice is made by us, the people designing the system, based on our use case.

## Step 2: Generating many thoughts

Then, at every state, we ask the LLM to create a few possible next thoughts. This part is called the thought generator.

There are two common ways to do it:

- Sample: We ask the LLM the same question a few times, separately. Each time, it gives a slightly different next thought. This works well when there are many open choices, like in creative writing.
- Propose: We ask the LLM once to list several different next thoughts in one answer. This works well when the choices are small and limited, like in a maths puzzle, because it avoids getting the same thought again and again.

Let's say we have a small maths puzzle: we get the numbers 4, 9, 10, 13, and we must combine them to make 24. We will see this puzzle in detail later. For the first step, the LLM can propose:

```text
4 + 9 = 13  (left: 10, 13, 13)
10 - 4 = 6  (left: 6, 9, 13)
13 - 9 = 4  (left: 4, 4, 10)

```

Here, each line is one candidate thought, and each one opens a new branch in the tree.

## Step 3: Judging the thoughts

Now, we have many branches. But we cannot follow all of them, because the tree grows very fast. We need to know which branches look promising.

This part is called the state evaluator. The same LLM does the judging. We simply ask it to think about each state and give an opinion.

We have a detailed blog on LLM as a Judge that explains how an LLM can grade the work of an LLM.

There are two common ways:

- Value: We show the LLM one state and ask it to rate it. For example, in the maths puzzle, the LLM labels each state as sure, likely, or impossible to reach the goal. These labels are turned into scores.
- Vote: We show the LLM all the states together and ask, "Which one is the most promising?". The LLM votes for one. We repeat the vote a few times and count.

Let's say the state is "left: 4, 4, 10". The LLM can reason like below:

```text
10 - 4 = 6, 6 * 4 = 24. We can reach 24.
Judgement: sure

```

And for a state like "left: 1, 1, 2", it can reason:

```text
The biggest we can make is (1 + 1) * 2 = 4. Too small to reach 24.
Judgement: impossible

```

This is like a chess player who looks at a board position and says, "This looks winning" or "This looks lost", without playing the whole game till the end.

To make the judgement more stable, we can ask the LLM the same rating question a few times and add up the scores. A "sure" gets a big score, a "likely" gets a small score, and an "impossible" gets almost zero.

The judgement does not need to be perfect. It just needs to be good enough to guide the search.

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

## Step 4: Searching through the tree

Finally, we need a plan for walking through the tree. This is the search algorithm. The paper uses two well-known ones.

### Breadth-First Search (BFS)

Breadth-First Search goes level by level. At each level, it keeps only the best few states and drops the rest.

The number of states we keep at each level is called the breadth limit, and we write it as `b`. Let's say `b = 5`.

```text
Level 1: generate many thoughts, judge, keep best 5
   ↓
Level 2: from those 5, generate many, judge, keep best 5
   ↓
Level 3: from those 5, generate many, judge, keep best 5

```

It is like a talent show with rounds. In every round, many people perform, and only the top 5 go to the next round.

BFS works well when the number of steps is small and fixed, like our maths puzzle, which always needs exactly 3 steps.

### Depth-First Search (DFS)

Depth-First Search goes deep along the most promising path first. If a state is judged as hopeless, it goes back to the previous state and tries the next option.

Going back like this is called backtracking.

```text
        Problem
           ↓
           A
           ↓
     +-----+-----+
     ↓           ↓
     A1          A2
     ↓           ↓
 impossible     A2a
 back to A       ↓
               Answer

```

It is like exploring a maze. We walk down one corridor as far as we can. If we hit a wall, we come back to the last turning and take another corridor.

DFS works well when the path is long and there are many steps, like filling a crossword. In fact, the paper used DFS for small 5x5 crossword puzzles, where each thought fills one word and a word that breaks the grid sends the search back.

Chain of Thought can never go back. Tree of Thoughts can.

Now that we have learned about all the four parts, it's time to see them working together.

## A complete example: the Game of 24

The best way to learn this is by taking an example.

The Game of 24 is a maths puzzle. We get four numbers. We must use each number exactly once, with `+`, `-`, `*`, and `/`, to make 24.

Let's take the numbers `4, 9, 10, 13`.

Step 1: We break the problem into thoughts. Each thought is one equation that combines two numbers. So, we need exactly 3 thoughts to go from 4 numbers down to 1 number.

Step 2: We generate at level 1. The LLM proposes a few first moves:

```text
(a) 4 + 9 = 13    left: 10, 13, 13
(b) 10 - 4 = 6    left: 6, 9, 13
(c) 13 - 9 = 4    left: 4, 4, 10
(d) 9 * 4 = 36    left: 10, 13, 36

```

Step 3: We judge level 1. The LLM rates each state:

```text
(a) 10, 13, 13  -> impossible
(b) 6, 9, 13    -> sure
(c) 4, 4, 10    -> sure
(d) 10, 13, 36  -> impossible

```

Step 4: We search. With BFS, we keep the best ones, which are (c) and (b), and drop (a) and (d).

Level 2: From (c) "4, 4, 10", the LLM proposes:

```text
10 - 4 = 6    left: 4, 6   -> sure (4 * 6 = 24)
4 + 4 = 8     left: 8, 10  -> impossible

```

We keep "4, 6". The state (b) is also expanded in the same way, but just for the sake of understanding, we are following only the path of (c) here.

Level 3: From "4, 6", the LLM proposes `4 * 6 = 24`. We reached 24.

Now, we just read the path back from the root:

```text
13 - 9 = 4
10 - 4 = 6
4 * 6 = 24

```

Means, `(10 - (13 - 9)) * 4 = 24`. It works perfectly.

In the paper, GPT-4 with Chain of Thought solved only 4% of these puzzles. GPT-4 with Tree of Thoughts, keeping the best 5 states at each level, solved 74%.

With Chain of Thought, if the first equation was (a), the whole answer failed. With Tree of Thoughts, (a) was judged as impossible and dropped early.

## A simple code sketch of Tree of Thoughts

Now, let's see the code for a very simple version of Tree of Thoughts with BFS. Here, `llm_propose` and `llm_judge` are helper functions that send a prompt to an LLM and read back its answer. We are hiding their details for the sake of understanding.

```python
def tree_of_thoughts(problem, steps=3, keep=5):
    states = [problem]                  # level 0: only the problem

    for level in range(steps):
        candidates = []
        for state in states:
            for thought in llm_propose(state):      # Step 2: generate
                candidates.append(state + "\n" + thought)

        scored = [(llm_judge(c), c) for c in candidates]  # Step 3: judge
        scored.sort(reverse=True)                         # best first
        states = [c for score, c in scored[:keep]]        # Step 4: keep best

    return states[0]                    # the best final path

```

Here, we have:

- `states` holds the paths we are currently keeping. At the start, it only has the problem.
- In each level, for every kept state, we ask the LLM to propose new thoughts and attach each one to the path. This is the thought generator.
- `llm_judge` gives a score to every new path. For example, "sure" can become a high score and "impossible" a very low score. This is the state evaluator.
- We sort by score and keep only the top `keep` paths. This is the BFS search with breadth limit `b`.
- After the last level, we return the best path.

This is how the four parts fit together in a few lines of code.

## Chain of Thought vs Tree of Thoughts

Let me tabulate the differences between Chain of Thought and Tree of Thoughts for your better understanding.

| Point | Chain of Thought | Tree of Thoughts |
| --- | --- | --- |
| Shape of reasoning | One straight chain | A tree with many branches |
| Options at each step | One | Many |
| Judges its own steps | No | Yes |
| Can go back after a mistake | No | Yes, with backtracking |
| Number of LLM calls | One | Many, often dozens or more |
| Cost and time | Low | High |
| Best for | Simple, step-by-step problems | Hard problems that need trying and checking |

## Where Tree of Thoughts works well and where it fails

- It solves problems where the first move matters a lot, like puzzles, planning, and crosswords.
- It can recover from a bad step by dropping it or going back.
- It needs no new training. It works with any existing LLM.
- We can tune it: change the breadth limit, the size of a thought, or the search algorithm.

- It is expensive. One question can need many LLM calls, so it costs more money and takes more time.
- The judging step can be wrong. If the LLM rates a good path as "impossible", that path is dropped forever.
- We must design the thought size, the prompts, and the search for each new type of problem.
- For easy questions, it is a waste. Chain of Thought already does the job.

Note: Newer reasoning models are trained to explore, check, and go back inside their own long chain of reasoning. But the idea of Tree of Thoughts is still very useful when we build our own agents and want clear control over how many paths are tried and how they are judged.

Now, we must have understood how Tree of Thoughts works.

### Does Tree of Thoughts need a new model or extra training?

No. Tree of Thoughts needs no new training and works with any existing LLM. The same LLM proposes the next thoughts and also judges them. We only design the thought size, the prompts, and the search algorithm around it, and we can tune the breadth limit or the search to fit our use case.

### Who introduced Tree of Thoughts?

Tree of Thoughts was introduced in 2023 in a research paper named "Tree of Thoughts: Deliberate Problem Solving with Large Language Models". It was written by Shunyu Yao and others from Princeton University and Google DeepMind. The paper tested it on puzzles like the Game of 24 and small 5x5 crosswords.

### Is Tree of Thoughts more expensive than Chain of Thought?

Yes. Chain of Thought needs one LLM call, while Tree of Thoughts often needs dozens of calls or more for a single question, because it generates and judges many thoughts. So, it costs more money and takes more time. For easy questions, Chain of Thought already does the job.

### What happens if the LLM judges a good path wrongly?

That path is dropped forever. If the LLM rates a good path as "impossible", the search never comes back to it. To make the judgement more stable, we can ask the same rating question a few times and add up the scores. The judgement does not need to be perfect, just good enough to guide the search.

### Do reasoning models make Tree of Thoughts unnecessary?

No. Newer reasoning models are trained to explore, check, and go back inside their own long chain of reasoning. But Tree of Thoughts is still very useful when we build our own agents and want clear control over how many paths are tried and how they are judged.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
