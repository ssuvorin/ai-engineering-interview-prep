> Source: https://outcomeschool.com/blog/react-agent

# What is a ReAct Agent? How It Thinks and Acts, Explained
URL: https://outcomeschool.com/blog/react-agent
Published: 2026-04-30
Author: Amit Shekhar

What is a ReAct Agent? How It Thinks and Acts, Explained

# What is a ReAct Agent? How It Thinks and Acts, Explained

Authors
: - Name
: Amit Shekhar
Published on
: April 30, 2026

A ReAct Agent is an AI Agent built using the ReAct (Reasoning + Acting) pattern, the most common pattern for building AI Agents. It runs in a loop where the LLM thinks, takes an action, observes the result, and repeats until the task is done.

In this blog, we will learn about the ReAct Agent - what it is, how it is built, its anatomy, how it thinks and acts, and how to handle its common failure modes.

When we hear ReAct Agent, it sounds complex. But do not worry. If we break it down into its individual parts, every single piece is simple.

We will cover the following:

- What is a ReAct Agent?
- ReAct Agent vs AI Agent
- Anatomy of a ReAct Agent
- The ReAct Prompt Template
- How a ReAct Agent Thinks and Acts
- A Full Trace Example
- Implementing a ReAct Agent
- Common Failure Modes and How to Fix Them
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a ReAct Agent?

A ReAct Agent is an AI Agent built using the ReAct (Reasoning + Acting) pattern - the most common pattern for building AI Agents. It is not a single LLM call. It is a loop around an LLM, where the LLM is given a list of tools it can recommend. At each step, the LLM reasons about what to do and recommends a tool. The loop runs the tool, appends the result back to the memory, and the LLM reasons over it on the next turn.

Let's decompose the term:

ReAct Agent = Reasoning + Acting + Agent

Reasoning is the thinking part - the LLM figures out what to do next. Acting is the doing part - the LLM picks a tool, and the loop calls it. Agent is the wrapper around the LLM that runs this loop, executes the tools, and feeds the results back.

In simple words:

ReAct Agent = LLM + Tools + A loop that lets the LLM think, act, and observe until the task is done.

Think of a ReAct Agent like a new intern on their first day. They do not solve every problem in their head. They think about what they need, open a tool, read the result, think again, and repeat. A ReAct Agent works the exact same way - but at the speed of a machine.

A plain LLM call gives us one response and stops. A ReAct Agent gives us a response, runs tools, reads results, and keeps going - until it has a final answer. So, here comes the ReAct Agent to the rescue whenever a task is too big to solve in a single LLM call.

## ReAct Agent vs AI Agent

Now, a natural question arises - if a ReAct Agent is an LLM in a loop with tools, isn't that just an AI Agent? Let's clear this up.

ReAct is a pattern to build AI Agents. It is not a different category.

AI Agent is the category - any system where an LLM is wrapped in a loop with tools and memory. It does not say how the loop is structured, how the LLM picks the next action, or whether the reasoning is visible.

ReAct is a pattern for building that loop, where the LLM follows a Thought - Action - Observation cycle. At every step, the LLM first writes its reasoning (the Thought), then picks a tool (the Action), then reads the result (the Observation), then thinks again. The reasoning is explicit, step by step, and visible at every turn. That explicit step-by-step reasoning is Chain-of-Thought (CoT) Prompting surfaced inside the agent loop.

So when we say "ReAct Agent," we mean an AI Agent built with the ReAct pattern. Other patterns like Plan-and-Execute, Reflection, and Agentic RAG also build AI Agents - they just shape the loop differently.

In simple words:

ReAct is a way to build an AI Agent. Not all AI Agents are built this way, but most are.

Let me tabulate the differences between an AI Agent and a ReAct Agent for your better understanding.

| Property | AI Agent (the category) | ReAct Agent (built with the ReAct pattern) |
| --- | --- | --- |
| Definition | Any LLM in a loop with tools | LLM that loops through Thought, Action, Observation |
| Reasoning | May or may not be visible | Surfaced as an explicit Thought step (in the classic form) |
| Loop pattern | Not specified | Thought -> Action -> Observation -> repeat |
| Examples | ReAct, Plan-and-Execute, Reflection, Agentic RAG | Just the ReAct pattern |
| When to use the term | When speaking generally about agents | When you mean the Thought - Action - Observation loop specifically |

A computer-use agent is another type of AI Agent that runs this same think-act loop, but it operates a computer the way a human does - looking at the screen and clicking. We have a detailed blog on How do Computer-Use Agents work? that covers this in depth.

## Anatomy of a ReAct Agent

A ReAct Agent has five parts. Let's decode each one.

```
+------------------------------------------------+
|                Loop Controller                 |
|                                                |
|   System Prompt --->  +-------+                |
|                       |       |                |
|   Memory        --->  |  LLM  | <-----+        |
|                       +-------+       |        |
|                           |           |        |
|                           | pick      | obs    |
|                           v           |        |
|                       +-------+       |        |
|                       | Tools | ------+        |
|                       +-------+                |
+------------------------------------------------+

```

1. The LLM. This is the brain. It does the reasoning. It reads the conversation history and decides the next step - either pick a tool for the loop to call, or produce the final answer.

2. The System Prompt. This tells the LLM how to behave. It explains the ReAct pattern, lists the available tools, and sets the rules. Without a good system prompt, the LLM may not think, act, or stop reliably.

3. The Tools. These are the actions the agent can take - search the web, query a database, run a calculator, send an email, read a file, and etc. Each tool has a name, a description, and an input schema.

4. The Memory. This is the running history of the conversation - the user's question, every thought, every action, every observation. The LLM reads this memory at every step to decide what to do next.

5. The Loop Controller. This is the code that runs the loop. It sends the memory to the LLM, executes any tool calls, appends the results back to the memory, and checks if the agent is done. It also handles the stop conditions - like a maximum number of steps. Designing this controller well - the budget, the observations, and the exits - is Loop Engineering.

All five parts work together. Remove any one of them, and it is no longer a ReAct Agent.

To master the ReAct pattern, tool use, agent memory, and agent architecture in depth, check out our AI and Machine Learning Program at Outcome School.

## The ReAct Prompt Template

A good system prompt is what makes a plain LLM behave reliably as a ReAct Agent. Without one, the LLM may answer too early, skip the reasoning, or use the tools poorly. With one, the LLM knows to think, act, observe, and loop.

Here is a simple ReAct prompt template:

```
You are a helpful assistant that solves problems by thinking step by step and recommending tools when needed.

You have access to the following tools:
- search(query): Search the web for information.
- calculator(expression): Evaluate a math expression.

At each step, respond in one of these two formats:

Format 1 - When you need to recommend a tool:
Thought: <your reasoning about what to do next>
Action: <tool_name>(<tool_input>)

Format 2 - When you have the final answer:
Thought: <your final reasoning>
Final Answer: <the answer to the user's question>

Rules:
- Always start with a Thought.
- Recommend one tool per turn, unless multiple independent tools would clearly help in parallel.
- Wait for the Observation before continuing.
- Stop as soon as you have the final answer.

```

Here, we can see that the prompt does three things:

- Explains the ReAct pattern (Thought, Action, Observation, Final Answer).
- Lists the available tools with their inputs.
- Sets rules to keep the agent from going off the rails.

Note: The literal `Action: tool(input)` string format above is the classic ReAct string format - the original paper used square brackets like `Action: search[Apple Remote]`, and later versions and tutorials use parentheses. Either way, if we are using Claude, GPT, or Gemini, we must not copy this string format - we must define our tools using the API's tool/function-calling schema instead. The API handles the action format for us, validates the inputs, and parses the tool call. The core idea is the same - the prompt tells the LLM when to think, when to act, and when to stop - but the wiring is cleaner.

If we want to go deep into prompt engineering, the ReAct pattern, and tool use end to end, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## How a ReAct Agent Thinks and Acts

Now, let's put all the parts together to see how a ReAct Agent runs end to end.

Here is the shape of the loop:

```
        +-----------------+
        |  User Question  |
        +-----------------+
                 |
                 v
        +-----------------+
        |    Thought      |  <-- LLM reasons about the next step
        +-----------------+
                 |
        +--------+--------+
        |                 |
        v                 v
  +-----------+    +---------------+
  |  Action   |    | Final Answer  | ---> back to user
  +-----------+    +---------------+
        |
        v
  +-----------+
  |   Tool    |
  +-----------+
        |
        v
  +-------------+
  | Observation | --+
  +-------------+   |
                    |
                    +---> back to Thought (loop continues)

```

The user's question goes in at the top. The LLM produces a Thought, and from that Thought it picks one of two paths - either an Action that the loop turns into a tool call, or a Final Answer that ends the loop. When the LLM picks an Action, the loop runs the tool, the result comes back as an Observation, and the Observation feeds into the next Thought. This Thought - Action - Observation cycle keeps going until the LLM produces the Final Answer.

Note: The classic ReAct form runs one tool per Thought, which is what the diagram shows. Modern APIs like Claude, GPT, and Gemini can return multiple independent tool calls from a single Thought, and the loop runs them in parallel before the next Thought. The shape is the same - we just process a list of Actions instead of a single Action.

Here are the steps the agent follows:

Step 1: The user sends a question. The Loop Controller adds it to the Memory.

Step 2: The Loop Controller sends the Memory (system prompt + user question + history) to the LLM.

Step 3: The LLM responds with either a Thought + Action, or a Final Answer.

Step 4: If the response is a Final Answer, the Loop Controller returns it to the user. The agent is done.

Step 5: If the response is a Thought + Action, the Loop Controller executes the tool and gets the result. This result is the Observation.

Step 6: The Loop Controller appends the Thought, Action, and Observation to the Memory.

Step 7: Go back to Step 2.

This loop continues until the LLM produces a Final Answer or the maximum step limit is reached.

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

## A Full Trace Example

Let's trace through a real example to see every part in action.

User: "What is 15% of the population of Tokyo?"

```
Thought 1: I need to find the population of Tokyo first. I do not know the exact current number, so I will search for it.
Action 1: search("current population of Tokyo")
Observation 1: The population of Tokyo is approximately 14 million.

Thought 2: Now I need to calculate 15% of 14 million. Let me use the calculator to be accurate.
Action 2: calculator("14000000 * 0.15")
Observation 2: 2100000

Thought 3: I now have the answer. 15% of the population of Tokyo (14 million) is 2.1 million.
Final Answer: 15% of the population of Tokyo is approximately 2.1 million people.

```

Here, we can see how the agent:

- Recognized that it did not have the population data and reached for a tool.
- Chained the output of the search into the input of the calculator.
- Stopped as soon as it had the final answer.

That's the beauty of a ReAct Agent. Each step is small and simple, but the loop lets it solve problems that a single LLM call cannot.

Now, let's see how to build this in code.

## Implementing a ReAct Agent

Now, here is the important realization:

If we write code that takes the user's question, sends it to an LLM, runs the tools the LLM picks, feeds the observations back, and repeats this loop until the LLM has a final answer - our piece of code is a ReAct Agent.

That is all a ReAct Agent is. No magic. No black box. Just a loop, an LLM, some tools, and memory - all wired together in code.

Let's see what this looks like in real Python code, as below. Here, `call_llm` is any function that sends the messages and the list of tools to the LLM of our choice - Claude, GPT, Gemini, or any other - and returns its response. And `call_tool` is any function that runs a tool by name with the given arguments and returns the result. The code below is independent of any specific provider, so the message shapes are the conceptual form - real APIs use slightly different fields (OpenAI uses `tool_call_id`, Anthropic wraps the result in a `tool_result` block) and we adapt the shape to match.

```python
REACT_SYSTEM_PROMPT = "..."  # the ReAct prompt template from the previous section

async def run_react_agent(user_question, tools, max_steps=10):
    messages = [
        {"role": "system", "content": REACT_SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]
    step = 0

    while True:
        # Safety stop: bail out if we hit the step limit
        if step >= max_steps:
            return "Reached step limit without a final answer."
        step += 1

        # Ask the LLM to think, then either act or give the final answer
        response = await call_llm(messages, tools)

        # If the LLM has the final answer, stop the loop and return it
        if response.is_done:
            return response.final_answer

        # Otherwise, run each tool the LLM picked and feed the observation back
        for tool_call in response.tool_calls:
            observation = await call_tool(tool_call.name, tool_call.arguments)
            messages.append({
                "role": "tool",
                "name": tool_call.name,
                "content": str(observation),
            })

```

Here, we have the entire ReAct Agent in about 20 lines of Python. Let's walk through the important parts:

- The initial messages. We seed the memory with the ReAct system prompt and the user's question. The system prompt is what makes the LLM follow the Thought - Action - Observation pattern, so it must be the first message in the memory.
- The `while True` loop. This is the Loop Controller. It keeps going until either the LLM has the final answer or we hit the step limit.
- The step limit. We bail out after `max_steps` iterations. This protects us from infinite loops - one of the most common failure modes for ReAct Agents.
- The LLM call. We send the full memory (the conversation history) along with the list of tools. The LLM does the Thought step here - it reasons about the next move and either picks an Action or returns the Final Answer.
- The stop check. If `response.is_done` is `True`, the LLM is telling us "I am done, here is the final answer." We return that answer and exit the loop.
- The tool-call branch. If the LLM picked one or more tools, we run each one with `call_tool` using the arguments the LLM gave, append the observation back to the memory, and the loop continues.

That is the complete skeleton of a ReAct Agent - a `while` loop, an LLM call inside it, a check for the final answer, and a tool-call branch that feeds observations back. Everything else we add on top - structured tracing of Thoughts, retries, reflection, parallel tool calls - is polish around this core loop.

Now, let's look at what can go wrong.

## Common Failure Modes and How to Fix Them

ReAct Agents are powerful, but they can fail in specific ways. Let's decode each one.

1. Infinite loops. The agent keeps calling the same tool with the same input and never produces a final answer.

How to fix: Set a hard `max_steps` limit. Also, detect repeated identical actions and either stop or inject a message telling the agent to try a different approach.

2. Wrong tool selection. The agent calls the wrong tool for the job - like using search for a math problem.

How to fix: Write very clear tool descriptions. The description is what the LLM uses to pick the tool, so every word matters. Say exactly what the tool does and when to use it.

3. Hallucinated tool calls. The agent calls a tool that does not exist or passes invalid arguments.

How to fix: Use an LLM with native tool-use support (like Claude, GPT, or Gemini) so the schema is enforced. Always validate tool inputs before executing, and return a clear error message as the Observation if they are invalid.

4. Context explosion. After many steps, the conversation history becomes too long for the LLM's context window.

How to fix: Summarize older steps, drop stale observations, or use a separate memory store. For long-running agents, we must actively manage the context - this is the discipline of Context Engineering. We have a detailed blog on Recursive Language Models (RLMs) that takes a different angle - keeping the main context small by recursively offloading work to sub-models.

5. Premature stopping. The agent gives a final answer before gathering enough information.

How to fix: Add a critic step that reviews the final answer before it is returned, or require the agent to check its answer against a checklist (Did I cover all the parts of the question? Did I cite a source? Did I verify the math?) before emitting the Final Answer. The system prompt should make this verification step explicit, not optional.

6. Getting stuck after a tool error. A tool fails, and the agent does not know how to recover.

How to fix: Catch tool errors, convert them into natural-language Observations (e.g., "Error: the search API timed out. Try again or use a different query."), and let the LLM reason its way out.

Now, we have understood what a ReAct Agent is and how to handle the common failure modes. Let's wrap up with a quick recap.

## Quick Summary

Let's recap what we have learned:

- A ReAct Agent is an AI Agent that loops through Thought, Action, and Observation until the task is done. It is an LLM wrapped in a loop with tools and memory.
- The anatomy has five parts: the LLM, the System Prompt, the Tools, the Memory, and the Loop Controller. Remove any one, and it is no longer a ReAct Agent.
- The system prompt is what makes a plain LLM behave reliably as a ReAct Agent. It explains the pattern, lists the tools, and sets the rules.
- The loop is simple: send memory to LLM -> if tool call, execute and append observation -> if final answer, return.
- Common failure modes include infinite loops, wrong tool selection, hallucinated tool calls, context explosion, premature stopping, and errors after tool failures. Handling these is the real work of building a production agent.
[…1032ln elided…]

This is what makes the problem dangerous. There is no error. There is no warning. The model answers confidently with a wrong or incomplete answer, and we have no idea that the correct answer was already sitting right in front of it.

### Let's understand it with an example

The best way to learn this is by taking an example.

Let's say we are building an app that answers questions about our company. We have 20 documents about the company. We put all 20 documents into the prompt and then ask a question as below:

```text
Here are 20 documents about our company.

Document 1: ...
Document 2: ...
...
Document 20: ...

Question: What is our refund policy?

```

Let say the refund policy is written inside Document 2. The model reads Document 2 early, because it is sitting close to the top, and it answers correctly.

Now, let's move the same document to a different place. Let say the refund policy is now written inside Document 10, right in the middle of the pile. Everything else is exactly the same. The same 20 documents, the same question, the same model.

This time the model replies with something like "I could not find the refund policy in the given documents."

Nothing changed except the position. The content was identical. Only the seat number changed.

Let's move it once more, this time into Document 19, near the end. The model answers correctly again.

Same information. Same model. Same question. Three different positions, and two correct answers with one silent failure in the middle.

This is the Lost in the Middle problem.

### The U-shaped curve

Now, let's understand this behaviour in a slightly more measurable way.

If we take one small fact, keep moving it from the first position to the last position, and note down the accuracy at every position, we get a very clear shape.

- When the fact sits at the beginning, accuracy is high
- When the fact moves towards the middle, accuracy keeps dropping
- When the fact reaches the end, accuracy goes high again

If we draw this on a graph with the position on one side and the accuracy on the other side, the line goes down and then comes back up. It looks like the letter U.

Let's see it visually as below:

```text
Accuracy
  high  |  *                                   *
        |     *                             *
        |         *                     *
        |             *     *     *
  low   |________________________________________
          start          middle             end

                  Position of the answer

```

This is called the U-shaped performance curve.

Two very well known human behaviours explain this nicely:

- Primacy bias: we remember the first thing very well
- Recency bias: we remember the last thing very well

The model behaves in the same way. It is strong at the first thing, strong at the last thing, and weak in between.

Note: The dip in the middle becomes deeper as the input becomes longer. With a short prompt, we may not notice anything at all. With a very long prompt, the middle almost disappears.

### Why does this happen

Now, the next big question is: why does a model that can technically see all the text still ignore the middle?

There is no single reason. There are four reasons working together. Do not worry, we will learn about each of them in detail.

Reason 1: Attention gets spread very thin

An LLM uses a mechanism called attention. In simple words, attention decides how much importance every word should give to every other word while producing the answer.

Attention works by distributing a fixed budget of importance. Let's say the model has one full unit of importance to give away. If there are 10 other words, each one can get a healthy share. If there are 100,000 other words, each one gets a tiny share.

Let's take a simple comparison. Think about a torch light in a dark room. If the room is small, the light falls strongly on every corner. If the room is very big, the same torch has to cover a much larger area, so everything becomes dim. Attention behaves in exactly the same way.

So, as the input grows, the importance given to any single token becomes very small. The loudest tokens still win, and the ones sitting quietly in the middle get crushed.

Reason 2: The way position is handled

A model does not naturally know the order of the words. We have to tell it. We do this using positional encoding, which is a way of tagging every token with information about where it sits.

Many modern models use a scheme where tokens that are far away from each other get a weaker connection than tokens that are close to each other. This is very useful in general, because nearby words are usually more related to each other.

But this creates a side effect. The last part of the input sits very close to the place where the model is writing the answer, so it stays strong. The first part usually holds the instruction, and the model gets trained again and again to respect it, so it also stays strong. The middle is far from the answer and it is not anchored by anything, so it becomes the weakest region. The very first tokens get one more pull on top of this, because the model uses them as attention sinks, a dumping ground for the attention it does not need anywhere else.

Reason 3: Human writing teaches this habit

Models learn from human text. And human text has a very strong structure.

Think about an article, a research paper, an email, or a report. The important thing is usually stated at the beginning as the introduction, and repeated at the end as the conclusion. The middle carries the supporting details.

The model learns this pattern from millions of documents. So, it slowly develops a habit of trusting the start and the end more than the middle. It is doing exactly what we taught it to do.

Reason 4: Training rarely uses the full length

A model may support a context window of 128,000 tokens, but most of the examples it learned from were much shorter than that. The long window is usually added in a later stage of training, where the model is taught to handle much bigger inputs than it originally saw.

So, the model has a lot of practice with short inputs and very less practice with genuinely long inputs where the answer is buried deep inside. It supports the long window, but it is not equally skilled across the entire window.

It is like a student who studied five page chapters for years and is now handed a five hundred page book. The student can turn every page, but the attention is not evenly spread across the book.

These four reasons together create the dip in the middle.

### Where this hurts us in real life

Till now, we have learned about what the problem is and why it happens. Now, it is time to see where it actually bites us. Let's take a few real use cases.

RAG systems

RAG which means Retrieval Augmented Generation is a very common setup. We take all our documents, cut them into small pieces called chunks, and store them. When a question comes, a retriever searches through those chunks, picks the ones that look most related to the question, puts them into the prompt, and asks the model to answer using them.

But, here is the catch. Most of us stuff 20 or 50 chunks into the prompt, thinking that more context means a better answer. The chunks sitting in the middle get ignored. So, we retrieve the right answer, we place it in the prompt, and the model still fails.

The retrieval was perfect. The generation failed. And when we debug this, we usually blame the retriever, which was never the problem in the first place.

Note: If our retriever puts the correct chunk at rank 12 out of 30, we have technically retrieved it. But rank 12 sits deep in the middle of the prompt, so the model behaves as if we never retrieved it at all.

Long chat history

In a long conversation, the early messages and the latest messages stay strong. The instruction that we gave somewhere in the middle of the conversation quietly loses its power.

This is why a chatbot often follows a rule for some time and then starts breaking it. The rule did not get deleted. It just moved into the weak middle region.

This is also the reason why a long chat gets shrunk as it grows. We have a detailed blog on How does context compaction work? that explains how the older part of a conversation is summarized without losing the important points.

Long document analysis

When we give a 200 page contract or a huge log file and ask the model to find every issue, it reliably catches the issues near the start and near the end. The issues sitting in the middle sections get missed.

This is very dangerous, because the output looks complete. The model never says "I skipped the middle." It just gives a confident partial answer.

Multi-document comparison

When we ask the model to compare 10 reports, the reports placed in the middle get a very shallow treatment. The summary looks balanced, but it is quietly weighted towards the first and the last reports.

AI agents

An AI agent works step by step. It thinks, it uses a tool, it reads the result, and then it repeats. Every step adds its own output into the context.

After 30 steps, the goal that we gave at the very beginning is still safe, and the most recent step is still safe. But everything that the agent discovered in between starts fading away. This is why a long running agent slowly drifts away from what we originally asked it to do.

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

### How to test for the Lost in the Middle problem

This was all about the places where the problem hurts us. Now, let's learn how to catch it inside our own system.

Before fixing something, we must be able to measure it. There is a very simple and popular test for this, called the Needle in a Haystack test.

Here is how it works.

Step 1: Take a very long text that has nothing to do with our question. This is the haystack. It can be any long filler content.

Step 2: Write one small unique fact. This is the needle. For the sake of understanding, let's take "The secret code for the Mumbai office is BLUE-4471."

Step 3: Insert the needle at a chosen depth inside the haystack, for example at 10 percent depth.

Step 4: Ask the model a question whose answer is present only in the needle, for example "What is the secret code for the Mumbai office?"

Step 5: Note down whether the model found it or not.

After that, we repeat the whole thing by placing the needle at 0 percent, 10 percent, 20 percent, and so on, till 100 percent. We also repeat it at different input lengths.

Once we put all these results into a grid, we get a very clear picture. We can see exactly where our model becomes weak, and how long the input can become before the middle starts collapsing.

Note: We must run this test with our own model, our own prompt format, and our own kind of content. Every model has a different weak zone, and it changes with every new model version.

If we want to go deep into Evaluation of LLMs and Agents, and LLM as a Judge, check out our AI and Machine Learning Program at Outcome School, where we cover them from the ground up.

### How to solve the Lost in the Middle problem

Now that we have learned about the problem and we know how to measure it, it is time to learn how to solve it.

We will go through the approaches one by one, starting from the naive one.

Approach 1: Put everything into the context

This is what most of us do first. The model supports a huge context window, so we simply push everything into it and hope that the model will figure it out.

The issue with this approach is that a large context window is a capacity number, not a quality guarantee. The middle still gets lost, and on top of that we pay for every single token and we wait longer for the response. Let's see how the next approach solve this issue.

Approach 2: Send less, but send the right thing

Here comes the simplest and the most effective fix into the picture. Instead of sending 50 chunks, we send 5 good chunks.

A short and precise context has a very small middle, so there is almost nothing left to lose. The model reads all of it properly.

To do this well, we improve the retrieval step using a reranker. A reranker is a smaller model that takes the retrieved chunks and scores how well each chunk actually answers our question. We keep only the top few and we throw away the rest.

The issue with this approach is that sometimes we genuinely need many chunks, because the answer is spread across several documents. Let's see how the next approach solve this issue.

Approach 3: Order the chunks smartly

If we must send many chunks, then we must decide their seating arrangement very carefully. This is the cheapest fix of all, because we are not removing anything, we are only changing the order.

We already know the shape of the curve. The beginning is strong, the end is strong, and the middle is weak. So, we place the most relevant chunk at the very beginning, the second most relevant chunk at the very end, the third one just after the first, the fourth one just before the last, and we keep folding inwards like this.

The weakest chunks land in the middle, which is exactly where we can afford to lose them.

Let's see it visually as below:

```text
Ranked chunks:   1   2   3   4   5   6   7

Final order:     1   3   5   7   6   4   2
                 ^                       ^
              strongest              strongest
              position                position

```

This simple reordering costs us nothing and it gives a real improvement.

Note: We must also keep the actual question at the very end of the prompt, right before the answer begins. That is the strongest position in the whole prompt.

One more thing to notice here. If we have a critical instruction, such as "answer only from the given documents", then we must write it twice, once at the very beginning and once again at the very end. Repeating it costs a few tokens, and it makes sure that the instruction never falls into the weak middle.

Deciding what goes into the prompt, and in which order, is a skill of its own. We have a detailed blog on Context Engineering that covers it end to end.

The issue with this approach is that it only reduces the damage, it does not remove it. If the answer needs a chunk that landed in the middle, we still fail. Let's see how the next approach solve this issue.

Approach 4: Break the big job into small jobs

Instead of asking one question over one giant prompt, we break the input into small pieces and we process each piece separately.

We take each chunk, ask the model the same question on that chunk alone, and collect a small answer from each one. After that, we take all these small answers, which are now very short, and ask the model to combine them into the final answer.

Here, every chunk gets its own turn to sit at the beginning and at the end of a short prompt. There is no weak middle, because there is no long input at all.

This is often called the map and reduce style of processing. Map means we run the same small job on every piece, and reduce means we join all those small results into one final result.

For the sake of understanding, let's say we have 30 documents. Instead of one call with 30 documents, we make 30 small calls with one document each, and then one final call with the 30 short answers. The final call is tiny, so nothing gets buried in it.

There is a smarter version of this idea, where the model itself decides how to split the input and what to ask for every piece. We have a detailed blog on Recursive Language Models (RLMs) that explains how that works.

Advantage: Nothing gets ignored, because every piece is read inside a short context.

Disadvantage: We make many model calls, so it costs more and it takes more time.

Approach 5: Force the model to look before it answers

Sometimes we can fix a lot by simply changing the instruction.

Instead of asking the model to answer directly, we first ask it to go through the documents and copy out the lines that are relevant, along with the document number. After that, we ask it to answer using only those copied lines.

This works because copying is a much easier job than reasoning. The model scans and extracts, and the extracted lines then become a short and fresh context where nothing is buried.

We can write the instruction as below:

```text
First, list the document number and the exact sentences that are relevant
to the question. Do not answer the question yet.

Then, using only the sentences that you have listed above, write the
final answer.

```

Here, we have split one hard job into two easy jobs, which is a simple form of prompt chaining. The first job pulls the buried information up to the surface, and the second job works on a clean and short input.

Approach 6: Choose the model carefully

Every model has a different weak zone. Some models hold the middle very well up to 30,000 tokens and then collapse after that. Some models hold it much longer.

So, we must never pick a model by looking at the advertised context window size. We must pick it by running the Needle in a Haystack test at the length that we actually use, with the kind of content that we actually have.

A model that advertises a one million token window is not promising that it understands one million tokens equally well. It is only promising that it will accept them.

This way we can use these simple approaches to solve the interesting problem, and it makes our life easy, because we stop fighting the model and we start working with the way it actually reads.

### Key points to remember

Let me summarize the important points for our better understanding:

- The context window tells us how much text the model will accept, not how well it understands every part of it
- The accuracy is high at the beginning, it drops in the middle, and it rises again at the end, which gives us the U-shaped curve
- The problem becomes worse as the input becomes longer
- It happens because attention gets spread thin, position handling favours the nearby and the starting tokens, and human writing trains the model to trust the start and the end
- It fails silently, so we get a confident wrong answer instead of an error message
- The best fix is to send less context and better context
- If we must send a lot, then we must put the most important content at the start and at the end
- Breaking the work into small pieces removes the weak middle completely
- It is not only a RAG problem, it hits long chats and long running AI agents in exactly the same way
- We must test our own model using the Needle in a Haystack test instead of trusting the advertised numbers

Now, we have understood the Lost in the Middle problem in LLMs.

The next time our system gives a wrong answer even though the correct information was present in the prompt, we must not assume that the model failed to understand it. We must first check where that information was sitting.

Most of the time, the answer was already there. It was just sitting in the middle.

### Is the Lost in the Middle problem the same as text getting cut off?

No. When text is too big for the context window, some part of it gets removed before it ever reaches the model. In the Lost in the Middle problem, nothing is removed and everything reaches the model. The model still behaves as if the middle was never there.

### Does a bigger context window fix the Lost in the Middle problem?

No. A large context window is a capacity number, not a quality guarantee. It tells us how much text the model will accept, not how well it understands every part of it. The middle still gets lost, and we also pay for every token and wait longer for the response.

### Where should we put the question in a long prompt?

We should keep the question at the very end of the prompt, right before the answer begins. That is the strongest position in

[Showing lines 1-366 and 1399-1729 of 1729; 1,032 middle lines (45.7KB) elided. Read artifact://47 for full output]
