> Source: https://outcomeschool.com/blog/what-is-okf-open-knowledge-format

# What is OKF (Open Knowledge Format)?
URL: https://outcomeschool.com/blog/what-is-okf-open-knowledge-format
Published: 2026-07-26
Author: Amit Shekhar

What is OKF (Open Knowledge Format)?

# What is OKF (Open Knowledge Format)?

Authors
: - Name
: Amit Shekhar
Published on
: July 26, 2026

OKF (Open Knowledge Format) is an open standard for writing down what an organization knows about its data and systems, as a folder of plain markdown files, so that any AI agent or any tool can read that knowledge.

In this blog, we will learn about OKF (Open Knowledge Format). We will also see why the knowledge about our data stays scattered across many places, how OKF writes that knowledge down as a folder of plain markdown files which any AI agent or any tool can read, and where it fits along with MCP and Agent Skills in the real world.

We will cover the following:

- The problem: our knowledge is scattered
- What is OKF?
- OKF = Open + Knowledge + Format
- What is inside an OKF bundle?
- The frontmatter and the one required field
- Cross-links turn files into a graph
- Why plain markdown files?
- How an agent actually uses it
- OKF, MCP, and Agent Skills
- What ships with OKF today
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The problem: our knowledge is scattered

Before jumping into OKF, we must understand the problem it solves.

Let's say we work at a company that sells things online. All of our business data sits in tables, and one of those tables is called `orders`.

Now, a new person joins our team. They are a good engineer and they know how to query a table. After a couple of weeks, they are given a simple job.

"Tell me how many sales we made last week."

It sounds easy. The table is right there, and it is not hidden from anybody. It has a `status` column, an `amount` column, and a `country` column, and the tool that lists our tables shows us those names and stops there.

But before that number is correct, there are five separate rules that have to be known, and each one of them was written down in a different place.

```
   only completed orders count        ->  one senior engineer knows this
   test orders must be removed        ->  a wiki page from two years ago
   a refund is a row with a minus     ->  a comment inside the code
   one country is counted twice       ->  a spreadsheet made last year
   data before March is not usable    ->  the same senior engineer

```

Here, we can see the problem. Every one of these rules is real, every one of them changes the final number, and no single place holds all five. The knowledge exists, but it is scattered, and nobody wrote it down in one place because each rule was learned on a different day by a different person. So the new person walks around asking people, and even then they only learn the rules somebody remembers to mention.

Now, this was always annoying. But something has changed that makes it much worse.

Today we have AI agents. An AI agent is an AI that takes actions step by step to finish a job for us. We ask an agent to build a sales report, and it goes looking at the `orders` table.

The agent faces the exact same problem as the new person, and it is in a worse position, because it cannot walk over to the senior engineer's desk and ask. It sees column names and nothing more. So it guesses. And a confident guess about what our data means is exactly how we end up with a report full of wrong numbers. We have a detailed blog on Context Engineering that explains how we give an agent the right context to work with.

Now, we can think the answer is simple. Let's just write all of it down properly in one tool.

But, here is the catch. Every tool stores this knowledge in its own private shape, behind its own way of asking for it. So if we write everything into tool A, then tool B cannot read it, and our agent has to be taught tool A's private language first. Move to a different tool next year, and the whole thing has to be redone.

So, we need one common shape for writing down what we know, which every tool and every agent can read without special treatment.

We needed a solution for that. So, here comes OKF to the rescue.

## What is OKF?

OKF, which stands for Open Knowledge Format, is an open standard for writing down what an organization knows about its data and systems, as a folder of plain markdown files, so that any AI agent or any tool can read that knowledge without custom work.

It was published by the Google Cloud Data Cloud team on 13 June 2026, as version 0.1.

In simple words, OKF is an agreed way of writing our company's knowledge into ordinary text files, so that both people and machines can read the same file.

Now, this idea did not appear out of nowhere. For a while, teams had already been keeping a folder of notes written specially for their AI to read, and people started calling this an "LLM wiki". The habit worked well, but every team invented its own arrangement, so one team's notes could not be shared with anybody else. OKF takes that habit and writes down the rules for it, so that the notes one team keeps can be read by another team's agent.

Let's be clear about the most important design choice, because it explains everything else.

> OKF is just markdown. Just files. Just YAML frontmatter.

There is no software to install. There is no server to run. There is no special program needed to read it. We will understand what each of those words means as we go.

Let's see the change it brings.

```
   Without a common format:

     Catalog tool   ->  shape A  ->  needs a reader built only for shape A
     Company wiki   ->  shape B  ->  needs a reader built only for shape B
     Code comment   ->  shape C  ->  needs a reader built only for shape C

     3 sources, 3 different shapes, 3 readers to build and maintain

   With OKF:

     Catalog tool   --+
     Company wiki   --+-->  the same OKF files  ->  one reader for all of them
     Code comment   --+

     3 sources, 1 shape, 0 readers to build

```

In this diagram, "shape" means the arrangement each tool uses to store the knowledge, and a "reader" is the extra code our agent needs so it can understand that one arrangement.

Here, we can see the whole point of a standard. In the first case, adding one more source means building one more reader, so the work keeps growing forever. In the second case, everybody writes the same shape once, and a single reader understands all of them, including the sources we add next year. The people writing the knowledge and the tools reading it no longer need to know about each other at all.

## OKF = Open + Knowledge + Format

The name is doing exactly what it says, so let's break it down.

> OKF = Open + Knowledge + Format

- Open means the rules are published for everybody. Anyone can write these files, and anyone can read them.
- Knowledge means the part that is not the data itself. Not the rows in the table, but what the table means, why it exists, what its columns are for, and what to watch out for.
- Format means an agreed shape for writing it down, so that everybody writes it the same way.

Means, OKF is an agreed and openly published shape for writing down what we know.

Now, let's be very clear about that middle word, because it is the part people misread. OKF does not store our data. It stores the understanding that sits around our data.

Let's see the difference side by side.

```
   THE DATA lives in the table:

     order_id | amount | status    | country
     ---------+--------+-----------+--------
     1001     | 250    | complete  | IN
     1002     | 90     | cancelled | IN
     1003     | 410    | complete  | US
     ...      | ...    | ...       | ...       (a million more rows)

   THE KNOWLEDGE lives in the OKF file:

     "One row per order. Only completed ones count as a sale."

```

Here, we can see it clearly. The table holds a million rows and never explains itself. The OKF file holds one short sentence, and that sentence is what tells us the cancelled row must not be counted. The data is the what. The knowledge is the meaning.

## What is inside an OKF bundle?

Now, let's open one up. A collection of OKF files is called a bundle, and a bundle is simply a folder on a computer.

Let's look at a real one.

```
   sales/
   ├── index.md
   ├── datasets/
   │   ├── index.md
   │   └── orders_db.md
   ├── tables/
   │   ├── index.md
   │   ├── orders.md
   │   └── customers.md
   └── metrics/
       ├── index.md
       └── weekly_active_users.md

```

Here, we can see the whole idea at a glance. It is folders and files, exactly like the folders on our own laptop. Nothing more.

The rule is simple. One file per concept. The `orders` table gets one file. The `customers` table gets its own file. The "weekly active users" measurement gets its own file too.

Every file ends in `.md`, which means it is a markdown file. Markdown is simply plain text with very light formatting, the kind we already use for a README file. We can open it in any text editor.

There is one more clever detail here. The location of the file is the name of the concept. The `orders` table is at `tables/orders.md`, so its identity is that path. Nobody needs to invent a separate identification system, because the folder structure already provides one.

Note: Those `index.md` files are optional. They act like the front page of each folder, giving a short overview so that a reader can understand the folder without opening every file in it. There is also an optional `log.md`, which keeps a dated history of what changed.

## The frontmatter and the one required field

Now, let's look inside a single file. Each file has two parts.

The top part sits between two lines of dashes, and it is called the frontmatter. It holds the labeled facts about this concept. It is written in a style called YAML, which is simply "label: value" on each line.

The bottom part is the body, which is ordinary markdown, where we explain things in normal sentences.

Let's see a whole file at once, so the two parts are clear.

```
   tables/orders.md
   +----------------------------------------------------+
   |  ---                                               |
   |  type: BigQuery Table                              |   <- frontmatter
   |  title: Orders                                     |      (labeled facts,
   |  description: One row per order ...                |       read by machines)
   |  ---                                               |
   |                                                    |
   |  # Orders                                          |   <- body
   |                                                    |      (plain sentences,
   |  This table is loaded every night at 2 AM.         |       read by people)
   |  Cancelled orders are never counted as sales.      |
   +----------------------------------------------------+

```

Here, we can see both halves in one place. The top half holds short labeled facts, which a machine can sort and filter on. The bottom half holds everything a person would say out loud, the kind of detail that never fits into a label. Both live in the same file, so they can never drift apart.

Now, let's look closely at the top of a real file.

```yaml
---
type: BigQuery Table
title: Orders
description: One row per order. Only completed ones count as a sale.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, revenue]
timestamp: 2026-05-28T14:30:00Z
---

```

Here, we can read every line without knowing anything technical.

- `type` says what kind of thing this is. Here it is a table inside BigQuery, which is Google's service for storing very large amounts of data.
- `title` is the human name.
- `description` is the one-line explanation. Notice how much this single line solves. The first rule our new person had to hunt for, that only completed orders count as sales, is answered right here.
- `resource` is a link to the actual thing, so we can go and look at it.
- `tags` are labels for grouping, written as a list.
- `timestamp` records when this was last true, written in a standard date style.

Now, here is the part that surprises people. Out of all of these, only `type` is required. Everything else is optional.

Why would a standard ask for so little? Because a standard that demands twenty fields is a standard nobody fills in. By asking for almost nothing, OKF makes it easy to start with a single line and add more later. The other fields are simply the agreed names to use when we do want them, so that everybody uses the same word instead of one team writing `description` and another writing `desc`.

And the types themselves are deliberately loose. `BigQuery Table` is just an example. A `Dataset`, a `Metric`, an `API`, a `Runbook`, a `Playbook`, all of these are fine. OKF does not hand us a fixed list to pick from.

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

## Cross-links turn files into a graph

Now, let's learn the part that makes a bundle more than a pile of files.

Concepts in the real world point at each other. The `orders` table has a column that refers to a customer, and customers live in a different table. So how do we record that connection?

We use an ordinary markdown link, exactly the kind we would write in any document.

```markdown
| `customer_id` | STRING | FK to [customers](/tables/customers.md). |

```

Here, we can see a row from a table description inside the `orders.md` file. It says there is a column called `customer_id`, and it holds text. Then `FK` is short for foreign key, which simply means the value in this column identifies a row sitting in a different table. And notice how that connection is recorded. It is a plain clickable link to the other file.

Now, why does this matter so much? Because once every file can link to other files, the whole bundle stops being a flat list and becomes a graph, which simply means a set of things joined by connections.

```
   orders.md  ---- points to ---->  customers.md
       |
       +---------- points to ---->  orders_db.md

```

Here, we can see what that gives an agent. It starts at the `orders` file, discovers that customers matter, and follows the link to go and read about them. It can walk through our knowledge the same way we walk through linked pages, one step at a time, learning only what it needs.

## Why plain markdown files?

Now, the following question arises. Why did they choose something as plain as text files, when far more powerful options exist?

The plainness is the whole point. Let's see what we get for free because of it.

- Humans can read it. The same file that the agent reads is the file we read. There is no separate version for people, so the two can never drift apart.
- It renders anywhere. Put the bundle in a code repository, and it displays as neat formatted pages. Search tools can index it.
- It travels easily. It is a folder, so we can zip it up, share it, or copy it onto a machine.
- It versions with our code. Because these are files, we can keep them beside our code and track every change over time, exactly as we do with code.
- Nothing needs installing. No program to buy, no service to keep running, no library to add to our project.

## How an agent actually uses it

Now, let's follow one real request from start to finish, so the whole thing becomes concrete.

Suppose we ask our AI agent the same job we gave the new person at the start, "how many sales did we make last week?"

Step 1: Before touching any data, the agent looks in the OKF bundle. It reads `index.md` to see what exists.

Step 2: It sees a `tables` folder and opens `tables/orders.md`.

Step 3: It reads the frontmatter and learns the important sentence straight away. One row is one order, and only the completed ones count as a sale. So it now knows it must not count orders that were cancelled or still in progress.

Step 4: It reads the body, sees the `customer_id` column, and follows the link to `customers.md` if it needs to.

Step 5: It uses the `resource` link to find where the real table actually lives.

Step 6: Only now does it go and do the actual work, and it produces the right number.

We can picture the whole flow as below:

```
   our question
        |
        v
   read the OKF bundle FIRST        <-  this is the new step
        |
        v
   learn the rule: "completed orders only"
        |
        v
   now go to the real table
        |
        v
   the right answer

```

Here, we can see that only one step was added, and it was added at the front. Everything after it stays the same. That one step is the difference between an answer and a guess.

Here, we can notice the most important point. The agent did not become smarter. It simply stopped guessing. All the knowledge it needed was written down once, by somebody who knew, in a file that the agent could read.

This way we can use OKF to solve the interesting problem of giving an agent our own context, without teaching it any special tool.

## OKF, MCP, and Agent Skills

Now, there are two other open standards that come up in the same conversation, and it helps a lot to see how the three differ. They are not competing. Each answers a different question.

- MCP, which stands for Model Context Protocol, connects an agent to outside tools and data. It answers "what can the agent reach?"
- Agent Skills are folders of instructions that teach an agent our way of doing a job. They answer "how should the agent do this?"
- OKF records what our data and systems actually mean. It answers "what is this thing?"

Agent Skills are already in use today. A coding agent picks up our team's way of working from a plain markdown file kept inside the project, exactly like this. We have a detailed blog on How does Claude Code work? that explains this step by step.

Let me tabulate the differences between the three for your better understanding so that you can decide which one to use based on your use case.

| Point | OKF | Agent Skills | MCP |
| --- | --- | --- | --- |
| What it carries | Knowledge about our things | Know-how, our steps and format | Reach, a live connection |
| Question it answers | What is this thing? | How should this be done? | What can the agent reach? |
| What it is made of | A folder of markdown files | A folder of markdown files | A running program |
| Needs something running | No | No | Yes |
| Best for | Data meaning, definitions, context | Procedures, checklists, style | Databases, apps, live actions |

They solve different problems. In real work they fit together. MCP connects the agent to our database, OKF tells it what the tables in that database mean, and a Skill tells it how our team wants the report written.

Note: We can notice from the table that OKF and Agent Skills are built almost the same way, as a folder of markdown files with frontmatter at the top.

If we want to go deep into the Model Context Protocol (MCP), Tool use in Agents, and Agent Architecture, check out our AI and Machine Learning Program at Outcome School.

## What ships with OKF today

Now, a standard on its own is only a document. So let's see what was actually released alongside it.

An enrichment agent. This walks through a company's existing data, and drafts the OKF files automatically. This matters more than it sounds, because writing hundreds of files by hand is the reason such efforts usually die. Here, a first draft is generated for us, and people then correct and improve it.

A visualizer. This turns any bundle into a single web page showing the graph of concepts and their links, so we can look at our knowledge instead of reading folders.

## Summary

[…813ln elided…]

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

[Showing lines 1-379 and 1193-1557 of 1557; 813 middle lines (42.2KB) elided. Read artifact://52 for full output]
