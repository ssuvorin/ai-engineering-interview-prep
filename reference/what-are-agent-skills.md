> Source: https://outcomeschool.com/blog/what-are-agent-skills

# What are Agent Skills?
URL: https://outcomeschool.com/blog/what-are-agent-skills
Published: 2026-07-30
Author: Amit Shekhar

What are Agent Skills?

# What are Agent Skills?

Authors
: - Name
: Amit Shekhar
Published on
: July 30, 2026

An Agent Skill is a folder of instructions, and optionally scripts and reference files, that an AI agent loads by itself only when the task actually needs it.

In this blog, we will learn about Agent Skills. We will also see why we need them, what is inside a Skill, how the description makes an agent pick up the right Skill by itself, how progressive disclosure keeps the context window free, how Agent Skills differ from MCP, and how we can create our own Skill.

We will cover the following:

- The problem before Agent Skills
- What are Agent Skills?
- What is inside a Skill?
- The description is the trigger
- Progressive disclosure, the main idea
- A Skill can carry real code
- Where Skills live
- How do we create our own Skill?
- Agent Skills vs MCP
- A real example
- Importance of Agent Skills
- Things we must be careful about
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The problem before Agent Skills

Before jumping into Agent Skills, we must understand the problem they solve.

An AI agent is an AI that takes actions step by step to finish a job for us. It can read files, run commands, and use tools.

Now, an agent is very capable in general, but it does not know how our team does things. It does not know our company's report format. It does not know the exact steps our team follows to release software. It does not know that our brand never uses a certain word.

So, what do we do? We type all of it into the chat, every single time.

We must have faced this. We explain the same eight steps on Monday. We explain them again on Wednesday. We explain them once more the next week to a teammate. The knowledge lives in our head, and we keep paying the cost of typing it out.

```
   Monday:     we type the 8 steps again
   Wednesday:  we type the 8 steps again
   Next week:  our teammate types the 8 steps again

```

Here, we can see the waste. The knowledge is stable, but the effort repeats forever.

Now, we can think that the answer is simple. Let's write all of it into one big instruction file, and keep that file loaded at all times.

But, here is the catch. That does not work either, and we must understand why.

An agent reads everything through a limited space called the context window. Think of it as the agent's desk. Only so many pages fit on the desk at one time. Every instruction we keep loaded occupies that desk space forever, even when it has nothing to do with the current job. Load twenty procedures, and the agent is reading nineteen irrelevant ones while trying to do the twentieth.

Deciding what deserves that limited space is a discipline of its own. We have a detailed blog on Context Engineering that covers this end to end.

So, we need a way to give the agent deep knowledge without keeping all of it on the desk at all times.

We needed a solution for that. So, here come Agent Skills to the rescue.

## What are Agent Skills?

An Agent Skill is a folder of instructions, and optionally scripts and reference files, that an AI agent loads by itself only when the task actually needs it.

Agent Skills were introduced by Anthropic in October 2025, and the format is open, so anyone can write one and anyone can use one.

In simple words, a Skill is a set of written instructions that teaches an agent how to do one particular job well. We write it once, and the agent picks it up on its own whenever that job comes up.

Let's decompose the term for the sake of understanding.

> Agent Skills = Agent + Skills

The agent is the AI that does the work. A skill is one specific ability it has learned. So, Agent Skills are simply the specific abilities we hand to our agent.

Consider a new employee joining our team. They are already smart and already know their profession. But they do not know our office. So, we do not retrain them from zero. We hand them our team handbook. Inside that handbook, there are separate chapters. One chapter for filing an expense. One chapter for releasing software. One chapter for writing a report.

The new employee does not read the whole handbook every morning. They open one chapter, only when they face that particular job.

A Skill is exactly one such chapter. And the agent is smart enough to open the right chapter by itself.

## What is inside a Skill?

Now, let's open a Skill and see what is inside. A Skill is just a folder on a computer, which means we can read it, edit it, and share it like any other folder.

Inside that folder, there is one required file called `SKILL.md`. The `.md` ending means it is a markdown file, which is simply a plain text file with light formatting. Note: There is nothing special or secret about it. We can open it in any text editor.

A `SKILL.md` file has two parts.

The first part sits at the very top, between two lines of dashes. This top part is called the frontmatter, and it holds the labels that describe the Skill. The two important labels are the `name` and the `description`.

The second part is the body, which is everything below the frontmatter. The body holds the actual instructions, written in plain English.

Let's see a small one as below:

```markdown
---
name: weekly-report
description: Creates the weekly team report in our company format. Use this whenever the user asks for a weekly report or a team update.
---

# Weekly report

Follow these steps.

First, collect all the tasks finished in the last seven days.
Then, group them under three headings: Shipped, In Progress, and Blocked.
After that, write one short line for each task. Never write more than one line.
Finally, put the total count at the top.

Never include internal ticket numbers in the final report.

```

Here, we can see the whole idea in one small file. The top part tells the agent what this Skill is and when to reach for it. The body tells the agent exactly how to do the job. Both parts are plain English, and we did not write a single line of programming code.

Note: The `name` must be written in small letters, with hyphens in place of spaces, like `weekly-report`. The `description` is plain English, and we must keep it short enough to read in one breath.

A Skill folder can also hold other files next to `SKILL.md`, like a reference document, a template, or a script. We will come to those shortly.

## The description is the trigger

Now, the most important question is: how does the agent know when to use our Skill?

The answer is the `description`.

The agent reads the `name` and the `description` of every available Skill. Then, when we ask for something, it compares our request against those descriptions and decides which Skill fits.

So, the `description` is not decoration. It is the trigger. A vague description means the Skill sits unused. A clear description means the Skill fires at the right moment.

Let's compare two descriptions.

```
   Weak:    "Report helper."
            The agent cannot tell when this applies. It stays unused.

   Strong:  "Creates the weekly team report in our company format.
             Use this whenever the user asks for a weekly report
             or a team update."
            The agent knows exactly what it does and when to use it.

```

Here, we can see the difference clearly. The strong one says what the Skill does and when to use it. Those are the two things the agent needs.

Note: We must write the description for the agent to read, not for a human to admire.

## Progressive disclosure, the main idea

Now, we come to the heart of Agent Skills. This one idea is what makes them work, so let's go slowly.

Remember our problem. The agent's desk is small, and we cannot keep everything on it.

Agent Skills solve this with something called progressive disclosure. The words sound heavy, but the idea is simple. It means revealing information in stages, and only as much as is needed right now.

It works in three levels.

Level 1. At the start, the agent loads only the `name` and the `description` of each Skill. That is a couple of lines each. So even fifty Skills cost almost nothing on the desk. At this point the agent knows only that the Skill exists, and nothing more about it.

Level 2. We ask for something. The agent matches our request to a description and decides this Skill is needed. Only now does it read the full body of `SKILL.md`. The detailed instructions arrive exactly when they become useful.

Level 3. If the body points to another file in the folder, like a long reference document, the agent opens that file only if it actually needs it.

```
   Level 1  ->  name + description only          (always loaded, tiny)
   Level 2  ->  the full SKILL.md instructions   (loaded when it matches)
   Level 3  ->  extra files in the folder        (loaded only if needed)

```

Let's put some real numbers on this, because they show why it works so well.

The unit we measure desk space in is called a token, which is roughly a piece of a word. Level 1 costs only about a hundred tokens for each Skill. Level 2, the full body, is normally kept under five thousand tokens, and we pay that cost only for the one Skill we are actually using.

Now, let's compare the two numbers, because the comparison is striking. Fifty Skills at Level 1 cost around five thousand tokens in total. That is the same as the body of one single Skill. So knowing that fifty procedures exist costs us no more than reading one of them in full.

Here, we can see why this is clever. The agent behaves as if it knows fifty procedures in depth, while its desk stays almost empty. Nothing is loaded until it earns its place.

This is exactly what a good handbook does. The table of contents is short and always in front of us. The chapter is long, and we open it only when we need it.

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

## A Skill can carry real code

Now, let's learn one more thing that makes Skills powerful.

A Skill folder can hold a script, which is a small program that can be run. When the job involves an exact, repeatable operation, we put a script in the folder and the instructions tell the agent to run it.

Now, why does this matter so much? Let's understand the difference.

Without a script, the agent has to write the code itself, every single time. It thinks, it writes, it sometimes writes it slightly differently, and it fills up the desk with all of that writing.

With a script, the agent runs one ready-made, tested file. The result is the same every time, and it costs almost nothing on the desk.

```
   Without a script:  the agent writes the code again each time
                      (slower, and the result can vary)

   With a script:     the agent runs one tested file
                      (fast, and the result is the same every time)

```

Here, we can see a simple rule. If the task needs judgment, we write instructions in plain English and let the agent think. If the task needs exactness, we write a script and let the agent run it.

## Where Skills live

Now, let's see where we keep these folders. There are two common places, and the difference matters.

Personal Skills. These live in our own home folder, in a place like `~/.claude/skills/`. Note: That `~` symbol is just a short way of writing our home folder. These Skills are ours alone, and they are available in every project we work on. Good for our personal working habits.

Project Skills. These live inside the project itself, in a place like `.claude/skills/`. Because they sit inside the project, they travel along with it. When a teammate copies the project onto their own computer, they get all the Skills automatically, without anybody telling them.

```
   ~/.claude/skills/   ->  our personal Skills, in every project
   .claude/skills/     ->  the project's Skills, shared with the whole team

```

Here, we can notice the real benefit of Project Skills. Our team's knowledge stops living inside one person's head and starts living inside the project, where everybody gets it for free.

The `.claude` name in these paths belongs to a coding agent that reads such folders at the start of a session. We have a detailed blog on How does Claude Code work? that explains how it picks up our project files.

## How do we create our own Skill?

Now, let's create one ourselves. The best part is that there is nothing to install and no code to write.

Step 1: Inside our project, create a folder path `.claude/skills/`.

Step 2: Inside that, create one folder named after our Skill, like `weekly-report`.

Step 3: Inside that folder, create a file named `SKILL.md`.

Step 4: At the top of that file, write the frontmatter with the `name` and the `description`.

Step 5: Below the frontmatter, write the steps in plain English, exactly as we would explain them to a new teammate.

The whole thing will look like below:

```
   our-project/
     .claude/
       skills/
         weekly-report/
           SKILL.md

```

Here, we can see how small this really is. One folder and one text file, and our Skill is ready.

Now, here is the best way to write the body. We must imagine we are writing for a capable new teammate, somebody who already knows the profession but does not know our office. So, we skip everything they already know, and we write down only what is specific to us. That single habit produces good Skills.

## Agent Skills vs MCP

Now, the following question arises. There is another thing called MCP that also gives an agent new abilities, so how are the two different?

First, let's recall what MCP is. MCP, which stands for Model Context Protocol, is one common standard that lets an AI application connect to outside tools and data, like our database or our GitHub.

Both are useful, and they are not competing at all. They answer two different questions.

MCP connects the agent to the outside world. It answers the question "what can the agent reach?" It gives the agent hands.

Agent Skills teach the agent our way of working. They answer the question "how should the agent do this?" They give the agent know-how, so it follows our exact steps and our exact format.

So, one gives reach and the other gives know-how.

Let me tabulate the differences between Agent Skills and MCP for your better understanding.

| Point | Agent Skills | MCP |
| --- | --- | --- |
| What it gives | Know-how, our steps and our format | Reach, a connection to outside systems |
| What it is made of | A folder of instructions, and sometimes scripts | A running program that offers tools and data |
| Question it answers | How should this be done? | What can the agent reach? |
| Needs a server running | No | Yes |
| Best for | Procedures, formats, style, checklists | Databases, apps, live data, actions |

In real work we often use both together. MCP connects the agent to our issue tracker, and a Skill tells it how our team writes an issue.

There is also a third piece in this space, built almost exactly like a Skill. OKF (Open Knowledge Format) writes down the knowledge about our data as a folder of plain markdown files, so the agent knows what our tables actually mean. We have a detailed blog on What is OKF (Open Knowledge Format)? that explains where it sits along with these two.

## A real example

The best way to learn this is by taking an example. Let's follow one request from start to finish, using the `weekly-report` Skill from earlier.

Step 1: The session begins. The agent loads only the names and descriptions of the available Skills. Our `weekly-report` description is now known to it, but the instructions are not loaded yet.

Step 2: We type, "prepare this week's team update."

Step 3: The agent compares our sentence with the descriptions it holds. Our description mentions "a weekly report or a team update", so it matches.

Step 4: The agent now reads the full body of `SKILL.md`. At this moment, it learns the three headings, the one-line rule, the total count at the top, and the rule about never including ticket numbers.

Step 5: It follows those steps and produces the report in our exact format.

Here, we can notice the best part. We never mentioned the format. We never mentioned the headings. We never reminded it about ticket numbers. We wrote all of that down once, weeks ago, and the agent applied it by itself at the right moment.

This way we can use Agent Skills to solve the interesting problem of teaching an agent our way of working, permanently, without repeating ourselves.

We have a complete program on AI Agents, Context Engineering, and Model Context Protocol (MCP) - check out our AI and Machine Learning Program at Outcome School to learn all of these in depth.

## Importance of Agent Skills

Now, we have understood how Agent Skills work. Let's see why they are important.

- Write once, use forever. We stop repeating the same instructions in every chat.
- The desk stays clean. Because of progressive disclosure, deep knowledge costs almost nothing until the moment it is used.
- Team knowledge becomes shared. A Project Skill turns one person's experience into something the whole team gets automatically.
- No programming needed. A Skill is plain English in a plain text file. Anyone who can write clear steps can write one.
- They are portable. Because the format is open and it is just a folder, the same Skill works across different tools that support it.
- They compose. The agent can combine more than one Skill in a single job, using one for the format and another for the checks.

## Things we must be careful about

Skills change how an agent behaves, so we must use them with care.

A Skill can run code. If a Skill folder contains a script, the agent can run it. That is exactly like installing any program on our computer. So, we must use Skills only from sources we trust, and we must read a Skill before using it.

A vague description is a wasted Skill. This is the most common mistake. We write good instructions, but the description does not say when to use them, so the Skill never fires. If a Skill seems to be ignored, the description is almost always the reason.

Too long is as bad as too vague. The body must hold only what the agent cannot guess by itself, which means our steps, our format, and our rules. It must not explain general knowledge that the agent already has. A tight Skill beats a long one.

One Skill, one job. It feels tempting to put everything into one giant Skill. We must not do that. Many small and focused Skills match better and load less.

Here, we can see that the rule is simple. Keep each Skill small and specific, write the description for the agent, and trust only the Skills we have read.

## Summary

Let's quickly recap what we have learned.

- An agent does not know our team's procedures, formats, and rules, so we end up typing them again and again.
- We cannot simply keep everything loaded, because the agent's context window is limited.
- An Agent Skill is a folder of instructions, and optionally scripts and files, that the agent loads by itself only when the task needs it.
- The folder needs one file called `SKILL.md`, which has a frontmatter with a `name` and a `description`, plus a body with the instructions.
- The `description` is the trigger. The agent uses it to decide when the Skill applies.
- Progressive disclosure works in three levels. Names and descriptions always, the full instructions when matched, and extra files only if needed.
- A Skill can carry a script, so exact and repeatable work runs the same way every time.
- Personal Skills live in our home folder, and Project Skills live in the project and travel to the whole team.
- Creating one needs no installation and no code. One folder and one `SKILL.md` file is a complete Skill.
- The best way to write a Skill is to write for a capable new teammate, skipping what they already know and recording only what is specific to us.
- MCP gives the agent reach, while Skills give the agent know-how. We often use both together.

This is what Agent Skills are, a simple folder that turns our own way of working into something our agent knows and applies on its own.

### Who created Agent Skills?

Agent Skills were introduced by Anthropic in October 2025. The format is open, so anyone can write a Skill and anyone can use one. Because a Skill is just a folder with a `SKILL.md` file, the same Skill works across the different tools that support the format.

### Why is my Agent Skill not being used by the agent?

The reason is almost always a vague description. The agent decides when to use a Skill by comparing our request against each Skill's description. If the description does not clearly say what the Skill does and when to use it, the Skill never fires, even when its instructions are good.

### Does adding many Skills fill up the context window?

No. At the start, the agent loads only the name and description of each Skill, which costs about a hundred tokens per Skill. So, fifty Skills cost around five thousand tokens in total. The full instructions of a Skill are loaded only when a request matches it.

### Can an agent use more than one Skill in a single task?

Yes. Skills compose, so the agent can combine more than one Skill in a single job. For example, it can use one Skill for the format and another Skill for the checks. Also, many small and focused Skills match better and load less than one giant Skill.

### Is it safe to use Agent Skills from the internet?

Only if we trust the source. A Skill folder can contain a script, and the agent can run it, which is exactly like installing a program on our computer. So, we must use Skills only from sources we trust, and we must read a Skill before using it.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:
