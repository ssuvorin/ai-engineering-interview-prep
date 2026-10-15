> Source: https://outcomeschool.com/blog/how-does-tree-of-thoughts-work

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
