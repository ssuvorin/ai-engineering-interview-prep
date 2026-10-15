> Source: https://outcomeschool.com/blog/jev-and-system-one-models-explained

# Jev and System One Models Explained
URL: https://outcomeschool.com/blog/jev-and-system-one-models-explained
Published: 2026-09-17
Author: Amit Shekhar

Jev and System One Models Explained

# Jev and System One Models Explained

Authors
: - Name
: Amit Shekhar
Published on
: September 17, 2026

Jev is the first System One Model, a new kind of AI model that does not write text at all. It looks at a situation and returns a decision from a fixed list of answers, along with how sure it is, that our software can use directly.

In this blog, we will learn about Jev and System One Models, a new kind of AI model that does not write text at all but only makes fast decisions that our software can use directly. We will also see what System One and System Two thinking mean, why using a normal LLM for small decisions is slow and unreliable, how Jev answers many questions in a single pass instead of one word at a time, what a typed answer is, how the probability attached to every answer is made honest, why Jev cannot hallucinate, and where it works well and where it fails.

We will cover the following:

- What is a System One Model?
- System One vs System Two Thinking
- The Problem with Using an LLM for Decisions
- What is Jev?
- How Jev Works
- Typed Answers: Choice, Score, and Yes/No
- Calibration and RLCD
- Why Jev Cannot Hallucinate
- Jev vs LLM
- Where Jev Works Well and Where It Fails
- When to Use Which One

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a System One Model?

A System One Model is an AI model that looks at a situation and returns a decision, not text.

In simple words, we give it some information and a fixed list of possible answers. It picks one answer from that list and also gives a number telling how sure it is.

Let's say we run an online shop. A customer sends a message: "My card was charged twice." We want to know which team must handle this message. The possible answers are `billing`, `technical`, and `account`. A System One Model reads the message and returns `billing` with a probability of 0.97, which means it is 97% sure.

That is all. It does not write a reply to the customer. It does not explain its thinking. It just decides.

System One Model = System One + Model

Here, "System One" comes from a famous idea about how the human brain thinks. And "Model" is the AI model. So, a System One Model is an AI model that thinks like the System One of our brain.

Before jumping into Jev, we must know what System One and System Two thinking mean.

## System One vs System Two Thinking

Daniel Kahneman, a psychologist who won the Nobel Prize, explained that our brain has two ways of thinking.

System 1 is fast, automatic, and effortless. When we see a friend's face, we know who it is instantly. When someone asks "2 + 2?", we say "4" without thinking. We do not sit and calculate. The answer just comes.

System 2 is slow, careful, and effortful. When someone asks "17 × 24?", we stop, think step by step, and work it out. It takes time and energy.

Both are useful. System 1 handles thousands of small decisions every day. System 2 handles the hard ones.

Note: Kahneman writes them as System 1 and System 2. TypeSafe writes the model name as System One. Both mean the same thing.

Now, let's connect this to AI.

An LLM, which stands for Large Language Model, is the AI model behind a chatbot like ChatGPT. It is built to produce text, one small piece at a time. Even when we ask it a simple yes or no question, it goes through this slow writing process. And the newer reasoning models go one step further, they write out their thinking step by step before giving the final answer. This is System 2 style work. It is powerful, but slow and costly.

But most of the decisions inside real software are small and repeated. Is this email spam or not? Which team must get this ticket? Is this review positive or negative? Is this answer safe to show to the user? These are System 1 type decisions. We need an instant answer, and we need it millions of times a day.

So, the question is: why are we using a slow, System 2 style model for fast, System 1 style decisions?

This is exactly the problem that System One Models are built to solve.

## The Problem with Using an LLM for Decisions

The best way to learn this is by taking an example.

Suppose we have a support system and we want to send every incoming ticket to the right team. Today, most of us do it with an LLM as below:

```python
prompt = """
Classify this support ticket into one of: billing, technical, account.
Reply with only the category name.

Ticket: My card was charged twice.
"""

response = llm.generate(prompt)
category = response.text.strip()

```

Here, we are asking the LLM to read the ticket and reply with only the category name. It looks simple. But, here is the catch.

Problem 1: It writes the answer one token at a time.

A token is a small piece of text, roughly a word or a part of a word. An LLM writes its answer one token at a time. To write "billing", it first predicts "bill", then "ing", and so on. Every single step is a full pass through a huge model. So, even a one-word answer takes many steps. And if the model decides to add an explanation, it takes even more steps.

Problem 2: We cannot trust the output format.

We asked for only the category name. But the model can reply "The category is billing." or "Billing." or "billing, let me know if you need anything else." or even "refund", which is not in our list at all. Now we must write extra code to clean this output. Most of the time, we do mistakes while writing this cleaning code, and it breaks in surprising ways.

Problem 3: We do not know how sure it is.

The model says "billing". Was it 99% sure or 51% sure? We do not know. So, we cannot decide when to trust it and when to send the ticket to a human.

Problem 4: It is slow and costly.

A frontier LLM, which means one of the biggest and most capable models available today, takes seconds for such a call. If we have a million tickets a day, both the waiting time and the bill add up very fast.

We needed a model that only decides, does it instantly, always returns a valid answer, and tells us how sure it is.

So, here comes Jev to the rescue.

## What is Jev?

Jev is the first System One Model, built by a company called TypeSafe AI.

It was announced on September 15, 2026. TypeSafe AI was founded by Diogo Almeida, one of the people behind ChatGPT, and the team spent about two years quietly building a new way of training models. Jev is the result of that work.

The most surprising thing about Jev is this: it does not generate text at all.

We cannot chat with Jev. We cannot ask it to write an email or code. It takes a situation as input, and it returns typed decisions with probabilities as output. Nothing else.

Now, let's understand how it works.

## How Jev Works

Jev takes two things as input:

- State: the information about the situation. State is just a word for "everything the model needs to know about the situation right now". It is always text. It can be a plain string, a list of texts, or a JSON object, which is a simple way of writing data as labels and values. For example, the customer message, their last few transactions, and the refund policy.
- Questions with allowed answers: what we want to decide, and what the valid answers are. For example, "Which team?" with the allowed answers `billing`, `technical`, and `account`.

And it returns:

- Typed answers: one answer per question, always chosen from the allowed answers.
- Probabilities: for every answer, a number between 0 and 1 telling how sure the model is.

Let's see it in code. For the sake of understanding, the code below is simplified and is not the exact API:

```python
result = jev.decide(
    state={
        "message": "My card was charged twice.",
        "recent_transactions": ["$49 on Sep 10", "$49 on Sep 10"]
    },
    questions={
        "team": ["billing", "technical", "account"],
        "is_urgent": "yes_no",
        "frustration": {"min": 0, "max": 2}
    }
)

```

The result will be:

```json
{
  "team": { "answer": "billing", "probability": 0.97 },
  "is_urgent": { "answer": true, "probability": 0.88 },
  "frustration": { "answer": 1, "probability": 0.74 }
}

```

Here, we can notice a few things:

- We asked three questions in one call and got three answers.
- Every answer is one of the allowed answers. `team` can only be `billing`, `technical`, or `account`. It can never be "refund" or a sentence.
- Every answer comes with a probability.

Now, the most important part: Jev answers all these questions in a single parallel pass.

Here, parallel means all at the same time, and a pass means one run through the model. Let's understand what this means with an analogy.

An LLM is like a person writing an essay with a pen. Each word comes after the previous word. It cannot write the tenth word before writing the ninth.

Jev is like a person filling a form with checkboxes. It reads the whole state once, and then ticks all the boxes at the same time. There is no "next word" to wait for. That's the beauty of a System One Model.

This is why Jev is so fast. A decision that takes a frontier LLM 3 seconds to a few minutes takes Jev about 70 to 500 milliseconds, which is a fraction of a second. TypeSafe reports that Jev is 40 to 200 times faster than LLMs of comparable intelligence on these tasks. In their own evaluation, they report Jev to be up to 193 times faster than Claude Sonnet 5 on decision tasks.

And because there is no text output, there is nothing to charge for on the output side. Jev costs $0.042 per million input tokens and the output is free.

So, it decides instantly, always returns a valid answer, tells us how sure it is, and costs very less. All four problems that we saw with the LLM approach got solved.

This was all about how Jev works. Now, let's understand what "typed" means, because this is the heart of Jev.

## Typed Answers: Choice, Score, and Yes/No

In programming, a type tells what kind of value something can hold. A variable of type boolean can only hold `true` or `false`. It can never hold "maybe". This is what we call type safety. The program cannot even represent a wrong kind of value. This is also where the company name TypeSafe comes from.

Jev brings the same idea to AI answers. Every question we ask has a type, and the answer must fit that type. Jev supports three kinds of typed answers:

Choice: pick one option from a fixed list. Example: `billing`, `technical`, or `account`. Jev supports up to 255 options in one list.

Score: pick a number from a fixed range. Example: frustration level from 0 to 2, or a quality score from 1 to 5.

Yes/No: a `true` or `false` answer. Example: "Is this urgent?"

And every one of these comes with a probability.

Now, the question is: how does Jev make sure the answer always fits the type?

Answer: Jev does not write the answer as text, it scores the options. Just for the sake of understanding, think of it like this. For a choice question with three options, Jev produces three probabilities, one for each option, and they add up to 1. The answer is simply the option with the highest probability. There is no way to output a fourth option, because there is no fourth slot.

This is very different from asking an LLM to "reply in JSON". With an LLM, the JSON is still written token by token, and we hope it comes out valid. With Jev, the shape of the answer is fixed before the model even runs.

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

## Calibration and RLCD

Till now, we have learned that Jev returns a probability with every answer. Now, the next big question is: can we trust that probability?

This is where calibration comes into the picture.

A model is calibrated when its probabilities match reality. In simple words, if we take all the answers where the model said "I am 90% sure", then about 90% of them must actually be correct. Not 60%. Not 99%. Around 90%.

Let's say a weather app says "70% chance of rain" on 100 different days. If it rained on about 70 of those days, the app is calibrated. If it rained on only 30 of those days, the app is not calibrated, and its 70% means nothing.

Most LLMs are not trained for this. They are trained to write text that humans like. So, when an LLM says "I am confident", it is just writing words that sound confident.

Jev is trained differently, using a method that TypeSafe calls RLCD.

RLCD = Reinforcement Learning for Calibrated Decisions

Let's break it down.

Reinforcement Learning is a way of training where the model makes a decision, gets a reward when the decision turns out to be good, and gets a penalty when it turns out to be bad. Over millions of tries, the model learns to make better decisions.

For Calibrated Decisions means the reward is not just for being right. The reward is for being right and being honest about how sure it is. Let's see with an example:

- The model says 99% and is right: big reward.
- The model says 99% and is wrong: big penalty.
- The model says 55% and is right: small reward.
- The model says 55% and is wrong: small penalty.

So, the only way for the model to score well is to say a high probability when it is truly likely to be right, and a low probability when it is not. This is how the probabilities become honest.

And this honest probability is very useful for us. Now, we can write code like below:

```python
if result["team"]["probability"] > 0.9:
    route_to(result["team"]["answer"])
else:
    send_to_human()

```

Here, we are trusting Jev when it is very sure, and sending the ticket to a human when it is not. We could never write these lines with a normal LLM, because it never gave us an honest number. This makes our life easy.

Note: Calibration does not mean every single answer is correct. A 90% answer is still wrong 10% of the time. Calibration only means the number is honest, so we know how much to trust it.

If we want to go deep into RLHF (Reinforcement Learning from Human Feedback), Reward Models, and Proximal Policy Optimization (PPO), we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Why Jev Cannot Hallucinate

You must have heard that LLMs hallucinate. In simple words, hallucination means the model confidently says something that is not true or does not exist. It can invent a book that was never written, a function that does not exist, or a category that is not in our list.

TypeSafe makes a strong claim: Jev cannot hallucinate. Let's understand exactly what this means, because it is easy to misread.

There are two kinds of mistakes a model can make when we ask it to decide something:

Type error: the answer is not even a valid kind of answer. We asked for `billing`, `technical`, or `account`, and the model said "refund" or wrote a paragraph.

Wrong answer: the answer is valid, but it is the wrong one. The ticket was about a login problem, and the model said `billing`.

Jev can never make a type error. This is a mathematical guarantee, not a promise. The answer is always one of the allowed options, because the model only scores the allowed options. There is no path inside the model that can produce anything else. TypeSafe even says that a single counterexample would be enough to prove this claim false.

Jev can still give a wrong answer. But when it is unsure, the probability will be lower, because it is calibrated. So, most of the wrong answers can be caught by looking at the probability, and we can send those cases to a human.

This is the meaning of "cannot hallucinate" here: it can never invent an answer that does not exist, and when it is unsure, it tells us.

One more thing to notice. Normally, we think System 1 is fast but error-prone, and System 2 is slow but reliable. TypeSafe turns this idea around. For these decision tasks, a System One Model can be made more reliable than the slow alternative, because its answers are limited to the allowed options by design, and its confidence is honest by training.

## Jev vs LLM

Now that we have learned about Jev in detail, it's time to compare it with an LLM side by side.

Let me tabulate the differences between Jev and an LLM for your better understanding.

| Aspect | Jev (System One Model) | LLM |
| --- | --- | --- |
| Output | Typed decisions with probabilities | Free-form text |
| How it answers | All answers in one parallel pass | One token at a time |
| Can write text, code, replies | No | Yes |
| Can reason step by step | No | Yes |
| Output format guarantee | Always valid, by design | Must be cleaned and checked by our code |
| Confidence | Calibrated probability with every answer | Not available or not honest |
| Speed | 70 to 500 milliseconds | Seconds to minutes |
| Cost | $0.042 per million input tokens, output free | Much higher, and output tokens cost extra |
| Input | Text, JSON, lists of text | Text, images, audio, and more |
| Best for | Classify, route, score, check, decide | Chat, write, code, reason, explain |

## Where Jev Works Well and Where It Fails

Where it works well:

- Routing: which team, which model, or which workflow must handle this?
- Classification: spam or not, positive or negative, which category?
- Scoring: how relevant is this document, or how good is this answer, from 1 to 5?
- Guardrails, which means safety checks: is this LLM output safe, on topic, and correct? Jev can check an LLM's answer in a fraction of a second before the user sees it.
- Real-time decisions: anything inside a user-facing app where we cannot wait for seconds.
- Large datasets: running the same decision over millions of rows, where cost and speed matter the most.

Where it fails:

- Writing anything: Jev cannot write a reply, an email, a summary, or code. There is no text output.
- Open-ended reasoning: if the task needs many steps of thinking, like solving a hard math problem, Jev is not the right tool.
- Explanations: Jev gives the answer and the probability, not the reason behind it.
- Images and audio: as of now, Jev accepts text only.
- Very large option lists: one choice question supports up to 255 options.

## When to Use Which One

The simplest rule is this:

If the answer is a decision, use Jev. If the answer is text, use an LLM.

And in real systems, we use both together. Let's say we are building a customer support system that replies to customers automatically.

First, Jev reads the ticket and decides the team, the urgency, and whether it is safe to reply automatically. This takes a fraction of a second.

Then, if Jev is sure it is safe, the LLM writes the reply.

After that, Jev checks the reply and decides whether it is correct and polite before it is sent.

Here, the LLM does the System 2 work: writing and reasoning. Jev does the System 1 work: deciding, fast and many times. Each one does what it is good at.

This kind of flow, where one step decides the path and another step does the work, is a common pattern. We have a detailed blog on AI Orchestration that covers these patterns end to end.

Now we must have understood Jev and System One Models, how they think like the fast System 1 of our brain, how they answer all questions in a single pass instead of one token at a time, how typed answers make wrong formats impossible, how RLCD makes the probability honest, and when to use them along with an LLM.

### Who built Jev?

Jev was built by a company called TypeSafe AI and announced on September 15, 2026. TypeSafe AI was founded by Diogo Almeida, one of the people behind ChatGPT. The team spent about two years building a new way of training models, and Jev is the result of that work.

### Can we ask Jev several questions in one call?

Yes. We can ask many questions in one call, and Jev answers all of them in a single parallel pass. It reads the whole state once and then ticks all the answers at the same time, like filling a form with checkboxes. Each answer comes with its own probability.

### Is asking an LLM to reply in JSON the same as Jev's typed answers?

No. With an LLM, the JSON is still written token by token, and we hope it comes out valid. With Jev, the shape of the answer is fixed before the model even runs. Jev scores only the allowed options, so it cannot output anything outside them.

### Does a calibrated probability mean Jev is always right?

No. Calibration does not mean every single answer is correct. A 90% answer is still wrong about 10% of the time. Calibration only means the number is honest, so we know how much to trust it and can send the unsure cases to a human.

### How much does Jev cost to use?

Jev costs $0.042 per million input tokens, and the output is free. Since Jev does not generate any text, there is nothing to charge for on the output side. With an LLM, the cost is much higher, and output tokens cost extra.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
