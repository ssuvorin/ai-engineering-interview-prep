> Source: https://www.linkedin.com/posts/pallavi-shekhar_ai-aiagents-machinelearning-share-7440257380707364864-5Ycc

# #ai #aiagents #machinelearning #llm #outcomeschool #agentdesign | Pallavi .
URL: https://www.linkedin.com/posts/pallavi-shekhar_ai-aiagents-machinelearning-share-7440257380707364864-5Ycc
Published: 2026-03-19
Author: Pallavi .

#ai #aiagents #machinelearning #llm #outcomeschool #agentdesign | Pallavi .

# Pallavi .’s Post

 Pallavi . 

You have built an AI agent that uses an LLM as the reasoning engine and has access to multiple tools like web search, calculator, and database query. During testing, the agent gets stuck in a loop - the LLM keeps recommending the same tool with the same input over and over again, and the agent keeps executing it. The LLM seems unable to realize the tool already returned a result. How do you fix this? Answer: The LLM does not have a built-in understanding of state or memory across tool calls. If the conversation history is not structured properly, the model cannot see that it already recommended the same tool and the agent already executed it and received a result. Another common reason is that the tool returns an error or unexpected format, and the LLM keeps recommending the same tool again because it does not know how to handle the failure. We set a hard limit on the number of tool calls the agent can make in a single task - for example, 10 iterations. If the agent hits this limit, we force it to stop and return the partial result. Every production agent must have this guard. We pass the complete history of tool recommendations and their results back to the LLM at each step. The LLM needs to see that it already recommended "web_search" with query "X", the agent executed it, and got result "Y". We structure the conversation as a clear sequence of Thought, Action, Observation entries. We implement loop detection in the agent runtime - if the LLM recommends the same tool with the same input more than 2 times consecutively, we break the loop and inject a message saying "You have already recommended this tool with the same input. The agent executed it and here is the result. Please proceed with a different action or provide the final answer." We also format error responses clearly with fallback instructions so the LLM can recommend a different action instead of blindly recommending the same tool. For a more structured approach, we use a planner-executor architecture where the planner creates a complete plan first and the agent executes it step by step. This is how we solve the infinite loop problem in AI agents. Follow Outcome School for knowledge-packed content. Keep Learning, Keep Sharing, and Keep Growing. #AI #AIAgents #MachineLearning #LLM #OutcomeSchool #AgentDesign 

 AMIT SHEKHAR 6mo 

#Agent #AI

 Outcome School 6mo 

Follow Outcome School for knowledge-packed content.

# How do Computer-Use Agents work?
URL: https://outcomeschool.com/blog/how-do-computer-use-agents-work
Published: 2026-06-24
Author: Amit Shekhar

How do Computer-Use Agents work?

# How do Computer-Use Agents work?

Authors
: - Name
: Amit Shekhar
Published on
: June 24, 2026

A computer-use agent is an AI program that can operate a computer the way a human does. It looks at the screen, moves the mouse, clicks buttons, and types on the keyboard to complete the goal we give it.

In this blog, we will learn about how computer-use agents work.

We will cover the following:

- What is a computer-use agent?
- Why do we need a computer-use agent?
- The perceive, think, act loop
- How does the agent see the screen?
- How does the agent decide what to do?
- How does the agent take actions?
- A step-by-step walkthrough with an example
- The system prompt and tools
- Safety and guardrails
- Limitations of computer-use agents
- Conclusion

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a computer-use agent?

A computer-use agent is an AI program that can operate a computer the way a human does. It looks at the screen, moves the mouse, clicks buttons, and types on the keyboard.

In simple words, we give it a goal in plain language, and it uses the computer to complete that goal.

Let's decompose the name to make it clear:

> Computer-Use Agent = Computer + Use + Agent

- Computer is the machine with a screen, a mouse, and a keyboard.
- Use means it actually operates that machine, just like we do.
- Agent means it acts on its own to reach a goal, step by step, without us guiding every click.

So, a computer-use agent is an AI that uses a computer on our behalf to get a task done.

Let's say we tell it, "Open the browser and book a table for two at 7 PM." The agent will find the browser icon, click it, type the website address, fill the form, and click the book button. We did not write any code for these clicks. We only gave the goal in plain words.

We have a detailed blog on AI Agent Explained that covers what an AI agent is from the ground up.

### Why do we need a computer-use agent?

Before computer-use agents, automating a task on a computer was hard for us.

Let's say we wanted a program to book that table automatically. We had two old approaches, and both had problems.

Approach 1: Write a script for every step.

We write code that says click here, type this, click there. This works only if the screen never changes. The moment the website changes its design, the script breaks. The button moves, and our code clicks the wrong place.

The issue with this approach is that it is fragile and breaks easily. Let's see how the next approach solve this issue.

Approach 2: Use a special connection called an API.

An API is a direct doorway that a website or app provides for programs to talk to it. It is reliable and fast. But, here is the catch. Not every website or app gives us this doorway.

The issue with this approach is that most apps do not offer this doorway. So, we are stuck for those apps.

So, here comes the computer-use agent to the rescue.

The computer-use agent does not need a special doorway. It uses the same screen, mouse, and keyboard that we use. If a human can do the task by looking at the screen, the agent can do it too. This is the big idea, and it makes our life easy.

For the apps that do give us that doorway, an open standard called MCP now gives the model one common way to reach them, which stays far more reliable than clicking through a screen. We have a detailed blog on What is MCP (Model Context Protocol)? that explains this in depth.

### The perceive, think, act loop

Every computer-use agent runs on one simple cycle. We can call it the perceive, think, act loop.

In simple words, the agent keeps repeating three steps until the task is done:

- Perceive: Look at the current screen.
- Think: Decide the next single action.
- Act: Perform that action on the computer.

After acting, the screen changes. So, the agent looks again, thinks again, and acts again. The loop continues until the goal is reached. Do not worry, we will learn about each of these three steps in detail.

We can picture the flow as below:

```text
        +-----------------------------+
        |                             |
        v                             |
   +----------+   +---------+   +----------+
   | Perceive |-->|  Think  |-->|   Act    |
   | (see the |   | (decide |   | (click,  |
   |  screen) |   |  next   |   |  type,   |
   |          |   | action) |   |  scroll) |
   +----------+   +---------+   +----------+
        ^                             |
        |     screen changes,         |
        +-----so look again ----------+

   The loop repeats until the goal is reached.

```

Here, we can see that the three steps form a circle. The agent moves from `Perceive` to `Think` to `Act`, and then the screen changes, so it goes back to `Perceive` and starts the next round. The loop keeps spinning until the goal is reached.

Let's understand this loop with a simple analogy.

Consider a person playing a video game. The person looks at the screen, decides to jump, and presses the jump button. The screen updates, so the person looks again and decides the next move. A computer-use agent works exactly like this person.

Let me tabulate the loop against the human player for your better understanding.

| Step | Human Player | Computer-Use Agent |
| --- | --- | --- |
| Perceive | Eyes look at the screen | Takes a screenshot of the screen |
| Think | Brain decides the next move | The AI model decides the next action |
| Act | Hand presses the button | Sends a click or keystroke to the computer |

Now, we have understood the core loop. Let's understand each of these three steps in detail.

### How does the agent see the screen?

The agent cannot see the screen the way we do with our eyes. So, the system takes a screenshot, which is a picture of the current screen, and sends it to the AI model.

In simple words, the screenshot is the eyes of the agent.

The AI model used here is a vision model. A vision model can look at an image and understand what is inside it. It can read the text on the screen, find the buttons, and understand the layout.

But, here is the catch. The model needs to know the exact position of things on the screen to click them.

A screen is measured in pixels, which are the tiny dots that make up the picture. Every spot on the screen has an address written as two numbers, the horizontal position and the vertical position. We write this address as `(x, y)`.

So, when the model looks at the screenshot, it finds the button and reports its address, for example `(640, 400)`. This address tells the computer exactly where to click.

Let's visualize this as below:

```text
   Screen (measured in pixels)

   (0,0)                              (1280,0)
     +------------------------------------+
     |                                    |
     |          +-------------+           |
     |          |   Search    | <-- button at (640, 400)
     |          +-------------+           |
     |                                    |
     |  [browser]                         |
     |   icon at (50, 760)                |
     +------------------------------------+
   (0,800)                          (1280,800)

   x grows to the right -->
   y grows downward     v

```

Here, we can see that every spot on the screen has an address written as `(x, y)`. The `x` value grows as we move to the right, and the `y` value grows as we move downward. The model reads the screenshot, finds the `Search` button, and reports its address as `(640, 400)` so the computer knows exactly where to click.

Some agents also read a hidden text list of everything on the screen, called the accessibility tree. In simple words, it is a plain list that says, "There is a button named Search at this position." This helps the agent find buttons without guessing. Many agents use both the screenshot and this list together.

This is how the agent sees and locates things on the screen.

If we want to go deep into how a single model reads an image and reasons over it in words - Multimodal AI and LLM Fundamentals - we cover it in depth in our AI and Machine Learning Program at Outcome School.

### How does the agent decide what to do?

Now that the agent can see, it must decide the next action. This is the think step.

Here, a special kind of AI model comes into the picture. It is built on a Large Language Model, which is an AI trained to understand language and reason about it. We join this language ability with the vision model from the previous step. So, the same model can both see the screen and reason about the next step in words.

We give the model three things:

- The goal: what we want, in plain language.
- The current screenshot: what the screen looks like right now.
- The history: the actions already taken so far.

The model looks at all three and answers one question, "What is the single next action that moves me closer to the goal?"

The model thinks like this, "The goal is to book a table. The screen shows a browser. The browser is closed. So, my next action is to click the browser icon at `(50, 760)`."

The model does not decide all steps at once. It decides only the next step. This is important. Because after the action, the screen changes, and the new screenshot may be different from what the model expected. So, deciding one step at a time keeps the agent flexible.

This is how the agent thinks.

### How does the agent take actions?

Now we reach the act step. The model has decided an action in words. But words alone cannot click a mouse. So, the system translates the model's decision into a real command for the computer.

The agent can perform a small set of basic actions. These are the same actions we perform every day:

- `click(x, y)` to click at a position.
- `type("some text")` to type text.
- `scroll(direction)` to scroll the page up or down.
- `key("Enter")` to press a special key.
- `screenshot()` to take a fresh picture of the screen.

The model outputs its choice in a clean, structured form so the system can read it easily. This form is called JSON, which is just a simple way of writing data using labels and values so a program can understand it. Let's see an example of what the model returns as below:

```json
{
  "reasoning": "The browser is closed. I will open it first.",
  "action": "click",
  "x": 50,
  "y": 760
}

```

Here, we can see that the model returned three useful things. The `reasoning` explains why it chose this action, which helps us trust it. The `action` is `click`. The `x` and `y` are the address on the screen where the click must happen.

The system reads this and performs a real mouse click at `(50, 760)`. The browser opens, a new screenshot is taken, and the loop continues.

This is how the agent turns a decision into a real action on the computer.

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

### A step-by-step walkthrough with an example

The best way to learn this is by taking an example. Let's say our goal is, "Search for the weather in London."

Let's walk through the loop step by step.

Step 1: The system takes a screenshot. The screen shows a desktop with a browser icon. The model thinks, "I need a browser. I will click the browser icon." It returns a click action at the icon position. The system clicks. The browser opens.

Step 2: A new screenshot is taken. The model sees an empty browser with an address bar. It thinks, "I will click the address bar first." It returns a click on the address bar. The system clicks.

Step 3: A new screenshot is taken. The address bar is now active. The model thinks, "Now I will type the search." It returns a type action with the text `weather in London`. The system types it.

Step 4: A new screenshot is taken. The text is in the bar. The model thinks, "Now I will press Enter to search." It returns a key action for `Enter`. The system presses Enter.

Step 5: A new screenshot is taken. The search results show the weather of London. The model thinks, "The goal is complete." So, it returns a done action and stops.

Let me show this as a small table so we can see the loop clearly.

| Step | What the model sees | Action taken |
| --- | --- | --- |
| 1 | Desktop with browser icon | Click the browser icon |
| 2 | Empty browser | Click the address bar |
| 3 | Active address bar | Type `weather in London` |
| 4 | Text in the bar | Press `Enter` |
| 5 | Weather results | Done |

Here, we can notice the pattern. Look, decide one action, do it, look again. The agent never plans all five steps in advance. It reacts to each new screenshot. This is what makes it work even when the screen behaves in an unexpected way.

This way we can use the perceive, think, act loop to solve the interesting problem of operating any app.

### The system prompt and tools

Now, the question is, how does the model know what actions it is allowed to take? The answer is the system prompt and the tools.

A system prompt is a set of starting instructions we give the model before the task begins. It tells the model who it is and how it must behave.

In simple words, the system prompt is the rulebook for the agent.

A simplified system prompt looks like below:

```text
You are a computer-use agent.
You can see the screen through screenshots.
You can perform these actions: click, type, scroll, key, screenshot.
Always return one action at a time in JSON format.
Explain your reasoning before each action.
Stop when the goal is complete.

```

Here, we have told the model three important things. We told it what it is, a computer-use agent. We told it the actions it is allowed to use. We told it the format to reply in, which is the structured JSON we saw earlier.

The list of allowed actions is often called the tools of the agent. A tool is simply one capability the agent can use, like clicking or typing. The model picks the right tool for each step.

This is how the model learns its role and its powers before it begins.

To master the system prompt, Tool use in Agents, Agent Architecture, and the ReAct Pattern - and to build an AI Coding Agent from scratch - check out our AI and Machine Learning Program at Outcome School.

### Safety and guardrails

A computer-use agent can do real things on a real computer. So, safety is very important.

Let's say the agent is filling a form and reaches a button that says delete account. We do not want the agent to click it without our permission.

So, here comes the idea of guardrails to the rescue. A guardrail is a safety rule that stops the agent from doing dangerous actions on its own.

A few common guardrails:

- Human approval: For risky actions like payments or deleting data, the agent pauses and asks us first.
- Blocked actions: Some actions, like changing system settings, are simply not allowed.
- Limited area: The agent often runs inside a safe, separate space so it cannot touch our important personal files.

These guardrails make sure the agent stays helpful and does not cause harm. We must always keep a human in control for sensitive tasks.

### Limitations of computer-use agents

Now that we have learned how the agent works, it is time to understand its limits. Computer-use agents are powerful, but they are not perfect.

- They can be slow. Each step needs a screenshot and a model decision. Many steps mean many rounds, and that takes time.
- They can do mistakes. The model may misread the screen and click the wrong button.
- They can get stuck. If a screen looks confusing, the agent may keep trying the same action again and again.
- They cost more. Looking at images and reasoning at every step uses a lot of computing power.

This is why, for now, we use them mostly for tasks where a special doorway, the API, does not exist. When an API is available, we prefer it, because it is faster and more reliable.

The technology is improving very fast. The agents are getting better at seeing the screen, deciding actions, and recovering from mistakes.

### Conclusion

Now we must have understood how computer-use agents work.

A computer-use agent looks at the screen, decides one action, and performs it, again and again, until the goal is reached. This is the perceive, think, act loop. It uses a vision model to see, a language model to reason, and a small set of actions like click and type to act.

The beauty of this idea is simple. If a human can do a task by looking at the screen and using the mouse and keyboard, the agent can do it too, without any special doorway into the app.

### Should we use a computer-use agent or an API?

When an API is available, we prefer the API, because it is faster and more reliable. Computer-use agents are slower, cost more, and can misread the screen. So, for now, we use them mostly for tasks where the app does not offer an API. For apps that do offer one, MCP gives the model one common way to reach them.

### Does a computer-use agent plan all the steps in advance?

No. The model decides only the single next action. After each action, the screen changes, and the new screenshot may be different from what the model expected. Deciding one step at a time keeps the agent flexible, so it works even when the screen behaves in an unexpected way.

### Why is a computer-use agent better than a click script when a website changes?

A click script only works if the screen never changes, so it breaks when the button moves. A computer-use agent looks at a fresh screenshot at every step, finds the button wherever it is, and then decides where to click. If a human can do the task by looking at the screen, the agent can do it too.

### Does a computer-use agent only use screenshots to see the screen?

Not always. Some agents also read a hidden text list of everything on the screen, called the accessibility tree, which says things like "There is a button named Search at this position." This helps the agent find buttons without guessing. Many agents use both the screenshot and this list together.

### Can a computer-use agent click risky buttons like delete account on its own?

It should not, and guardrails stop it. For risky actions like payments or deleting data, the agent pauses and asks us first. Some actions are blocked entirely, and the agent often runs inside a safe, separate space so it cannot touch our important personal files.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# How does LangChain work?
URL: https://outcomeschool.com/blog/how-does-langchain-work
Published: 2026-07-01
Author: Amit Shekhar

How does LangChain work?

# How does LangChain work?

Authors
: - Name
: Amit Shekhar
Published on
: July 1, 2026

LangChain is a framework that helps us build applications powered by Large Language Models. It sits between us and the LLM, and connects the LLM with our data, our tools, and our logic.

In this blog, we will learn about how LangChain works. We will also see why we need it, what chains, prompts, memory, and output parsers are, how retrieval and agents fit in, and how the full flow works together in the real world.

We will cover the following:

- What is LangChain?
- Why do we need LangChain?
- The core idea behind LangChain
- LLM and Prompt Template
- What is a Chain?
- Output Parser
- Memory
- Retrieval and RAG
- Tools and Agents
- A complete flow of how LangChain works

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is LangChain?

LangChain is a framework that helps us build applications powered by Large Language Models.

Before we go further, let's understand one term first. A Large Language Model, also called an LLM, is a model that understands and generates human-like text. ChatGPT is built on top of an LLM. We give it some text, and it gives us back some text.

Now, LangChain is a tool that sits between us and the LLM. It helps us connect the LLM with other things like our data, our tools, and our logic.

In simple words, LangChain helps us build smart apps that talk to an LLM and do useful work for us.

Let's decompose the name to understand it better.

> LangChain = Lang + Chain

Here, `Lang` stands for Language, which points to the language model. And `Chain` means joining many steps together, one after another. So LangChain is about chaining many steps into one smooth flow.

This idea of joining prompts step by step, where the output of one prompt becomes the input of the next, is called Prompt Chaining. We have a detailed blog on How does Prompt Chaining work that explains it step by step.

Now, we have understood what LangChain is. Now, let's understand why we even need it.

## Why do we need LangChain?

Let's say we want to build a simple app. We give it a question, and it gives us an answer using an LLM. This is easy. We send our text to the LLM and get the reply.

But real apps are not this simple. Let's see why.

Suppose we want our app to do the following:

- Take a question from the user.
- Look up answers from our own documents.
- Remember the previous messages in the conversation.
- Call a calculator or a search engine when needed.
- Format the final answer in a clean way.

Now, doing all of this by hand becomes messy. We have to write a lot of code to glue every piece together. We have to manage the order of steps. We have to handle the data moving from one step to the next.

This is hard to build and harder to maintain.

So, here comes LangChain to the rescue.

LangChain gives us ready-made building blocks. We just connect these blocks like Lego pieces. Each block does one job, and LangChain joins them together.

This way we can use LangChain to solve the interesting problem of building complex LLM apps in a very simple way.

Now that we have learned why we need LangChain, it's time to understand the core idea behind it.

## The core idea behind LangChain

The core idea of LangChain is very simple.

> Take small building blocks and chain them together to build a complete flow.

Let's understand this with an analogy.

Consider a factory assembly line. A car is built step by step. First, the body is made. Then, the engine is added. After that, the wheels are fixed. Finally, the paint is done. Each station does one job and passes the car to the next station.

LangChain works in the same way. Each block does one small job. The output of one block becomes the input of the next block. This is the chain.

Let me map this analogy to LangChain for our better understanding.

| Assembly line | LangChain |
| --- | --- |
| Raw material entering | User input |
| A single work station | A building block |
| The car moving forward | Data passing to the next step |
| The finished car | The final answer |

Now, we have the big picture. Now, let's learn about each building block one by one. Do not worry, we will learn about each of them in detail.

## LLM and Prompt Template

The first block is the LLM, which is the brain of our app. We already know that the LLM takes text and returns text.

But before sending text to the LLM, we must prepare the text carefully. The text we send to the LLM is called a Prompt.

In simple words, a prompt is the instruction we give to the LLM.

Now, most of the time our prompt is not fixed. A part of it changes based on the user. So, here comes the Prompt Template into the picture.

A Prompt Template is a ready-made prompt with some blank spaces that we fill at runtime.

Let's see the code for a prompt template as below:

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Explain {topic} in simple words for a beginner."
)

prompt = template.format(topic="LangChain")

```

Here, we have created a template with a blank space called `topic`. When we call `format` and pass `topic="LangChain"`, the blank space gets filled. The final prompt becomes "Explain LangChain in simple words for a beginner."

This is how a prompt template helps us reuse the same prompt with different values. It makes our life easy.

Now, we have a prompt ready. Now, let's learn how to join the prompt template with the LLM. This is where the chain comes in.

## What is a Chain?

A Chain is the joining of many blocks so that the output of one block flows into the next block.

In simple words, a chain is a pipeline of steps.

Let's say we want a simple chain. First, the prompt template fills in the user topic. Then, the LLM reads that prompt and gives an answer. This is a chain of two steps.

Let's see the code for a chain as below:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

template = PromptTemplate.from_template(
    "Explain {topic} in simple words for a beginner."
)

chain = template | llm

result = chain.invoke({"topic": "LangChain"})

```

Here, we can see a few important things. We created the `llm` block and the `template` block. Then we joined them using the `|` symbol. This `|` symbol is the pipe, and it means "send the output of the left side into the right side."

So, `template | llm` means the filled prompt from the template goes straight into the LLM. When we call `invoke` with our topic, the data flows through the chain and we get a result.

This is the heart of LangChain. We build small blocks and join them with the pipe.

Let's visualize this chain as below:

```text
  user input              filled prompt              answer
   {topic}                    text                    text
      |                        |                        |
      v                        v                        v
  +----------+    pipe    +----------+    pipe    +----------+
  | Template | ---------> |   LLM    | ---------> |  Parser  |
  +----------+            +----------+            +----------+
   fills the              the brain:              cleans the
   blank space            reads the prompt,       answer into a
                          gives an answer         clean result

```

Here, we can see that the data flows from left to right. The top row shows the data on each wire, and the bottom row shows what each block does. The `Template` fills the blank space and passes the filled prompt to the `LLM`. The `LLM` is the brain. It reads the prompt and passes its answer forward to the `Parser`. The `|` pipe between each block is what carries the output of one block into the next block. This is exactly what a chain means.

To learn how to build LLM apps with LangChain and LangGraph in depth, check out our AI and Machine Learning Program at Outcome School.

Now, we have understood the chain. But the LLM gives us plain text. Many times we need the answer in a clean structure. So, let's learn about the output parser.

## Output Parser

An Output Parser takes the raw text from the LLM and converts it into a clean, structured form.

In simple words, the LLM speaks in plain text, and the output parser turns that text into something our program can use easily.

Let's say we ask the LLM for a list of three fruits. The LLM returns "apple, banana, mango" as plain text. But in our code, we need an actual list of three separate items. The output parser does this conversion for us.

Let's see the code for an output parser as below:

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

chain = template | llm | parser

result = chain.invoke({"topic": "LangChain"})

```

Here, we have added one more block called `parser` to our chain. Now the data flows through three blocks. The template fills the prompt, the LLM gives an answer, and the parser cleans that answer into a simple string. The `StrOutputParser` simply gives us back clean text instead of the full message object.

This is how an output parser makes the final result neat and ready to use.

Now, our chain can take input, talk to the LLM, and clean the output. But there is a problem. Our app forgets everything after every message. Let's solve this with memory.

## Memory

Let's say we are chatting with our app. We ask, "Who is Albert Einstein?" The app answers correctly. Then we ask, "Where was he born?"

But here is the catch. The app does not know who "he" is, because it forgot the previous message. Every call to the LLM is fresh, and it does not remember the past on its own.

So, here comes Memory to the rescue.

Memory is the part of LangChain that stores the previous messages of a conversation so the app can remember the context.

In simple words, memory gives our app the power to recall what was said before.

Let's understand how it works. Each time the user sends a new message, LangChain takes the old messages from memory and adds them to the new prompt. So the LLM sees the full conversation, not just the latest message.

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

Let's see a simple flow of memory as below:

```python
# Turn 1
# Stored in memory: "User: Who is Albert Einstein?"

# Turn 2
# Memory + new message are sent together:
# "User: Who is Albert Einstein?
#  AI: Albert Einstein was a famous physicist.
#  User: Where was he born?"

```

Here, we can notice that in the second turn, the old conversation is added before the new question. So now the LLM knows that "he" means Albert Einstein. The memory carries the context forward.

This is how memory makes our app feel like a real conversation. Problem Solved.

Now, our app can remember the chat. But what if we want the app to answer using our own documents? The LLM does not know about our private data. Let's solve this with retrieval.

## Retrieval and RAG

The LLM is trained on general data from the internet. It does not know about our company documents, our personal notes, or our latest files.

Let's say we have a 200-page company handbook. We want our app to answer questions from this handbook. The LLM has never seen it. So how do we teach the app about it?

So, here comes Retrieval into the picture.

Retrieval means fetching the most relevant pieces of our own data and giving them to the LLM along with the question.

This full pattern has a name. It is called RAG, which stands for Retrieval-Augmented Generation. In simple words, we first retrieve the right information, then we let the LLM generate the answer using that information.

Let's understand the steps of how retrieval works.

Step 1: We break our big document into small pieces called chunks.

Step 2: We convert each chunk into a list of numbers called an embedding. An embedding is just a way to represent text as numbers so the computer can compare meaning.

Step 3: We store all these embeddings in a special database called a Vector Store. A vector store is a database built to search by meaning, not just by exact words.

Step 4: When the user asks a question, we turn the question into an embedding too, and we search the vector store for the closest matching chunks.

Step 5: We send those matching chunks plus the question to the LLM, and the LLM answers using them.

We can picture the RAG flow as below:

```text
  Our document
       |
       v
  +----------+    +-----------+    +--------------+
  |  Chunks  | -> | Embeddings | -> | Vector Store |
  +----------+    +-----------+    +--------------+
                                          ^
                                          | search by meaning
                                          |
  User question --> Embedding ------------+
                                          |
                                          v
                                  matching chunks
                                          |
                                          v
                           User question + matching chunks
                              combined into one prompt
                                          |
                                          v
                              +-----------------------+
                              |          LLM          | --> Answer
                              +-----------------------+

```

Here, we can see that the top row prepares our data once. We split the document into chunks, turn each chunk into an embedding, and store all of them in the `Vector Store`. When the user asks a question, we turn the question into an embedding too and search the `Vector Store` by meaning. The matching chunks and the question are then combined into one single prompt, and that single prompt is sent to the `LLM`, which generates the final answer from our own data.

Let's see a simplified code for retrieval as below:

```python
# Find the chunks that match the user question
relevant_chunks = vector_store.similarity_search("What is the leave policy?")

# Send the chunks and the question to the LLM
chain = prompt_with_context | llm | parser

result = chain.invoke({
    "context": relevant_chunks,
    "question": "What is the leave policy?"
})

```

Here, we can see that we first search the vector store for chunks related to the leave policy. Then we pass both the chunks and the question into our chain. The LLM now reads our own data and answers from it.

This is how retrieval and RAG let the LLM answer questions from our private data. That's the beauty of LangChain.

We have a detailed blog on Agentic RAG that takes this retrieval pattern further.

Now, our app can use memory and our own documents. But sometimes the LLM needs to take action in the real world, like searching the web or doing math. Let's learn about tools and agents.

## Tools and Agents

The LLM is very good at language, but it is not good at everything. For example, the LLM is weak at exact math, and it does not know today's live information.

Let's say we ask, "What is the weather in Delhi right now?" The LLM cannot know this, because it has no live connection to the weather.

So, here comes the idea of Tools to the rescue.

A Tool is an external function, such as a calculator, a search engine, or a weather service, that can be run to do something the LLM cannot do on its own.

In simple words, a tool is a helper that gets run when the LLM cannot do the job by itself.

Now, here is one very important point that people often get wrong. The LLM does not run the tool by itself. The LLM only recommends which tool to use and what input to pass to it. The actual call to the tool is made by our code. The LLM is the advisor, and our code is the doer.

So, the next big question is: who takes the LLM's recommendation and actually runs the tool? This is where the Agent comes in.

An Agent is a smart controller that uses the LLM to decide which tool to use and in what order, then runs that tool, takes back the result, and gives it to the LLM, until the task is complete.

In simple words, the agent works in a loop. It asks the LLM what to do next. The LLM recommends a tool and the input for it. The agent runs that tool, sees the result, and sends the result back to the LLM. Then it asks the LLM for the next step again. It keeps doing this until the task is done.

Let's see a numeric walkthrough of how an agent works. Suppose the user asks, "What is 25 times 18, and is that more than 400?"

Step 1: The agent sends the question to the LLM. The LLM recommends the calculator tool with the input `25 * 18`.

Step 2: The agent runs the calculator tool with `25 * 18`. The tool returns `450`.

Step 3: The agent sends `450` back to the LLM. The LLM compares `450` with `400` and sees that `450` is more than `400`.

Step 4: The LLM forms the final answer: "25 times 18 is 450, which is more than 400."

Here, we can notice that the math was not guessed. The agent ran a real tool for the calculation, and then the LLM reasoned about the result. This makes the answer reliable.

When these agent steps, decisions, and loops grow complex, we can lay them out as a graph and let the framework run them for us. We have a detailed blog on how LangGraph works that explains this step by step.

Note: The agent uses the LLM as its brain to make decisions, and the tools as its hands to take actions.

This is how tools and agents give our app the power to do real work.

To go deep into AI Agents and Tool use, and to build an AI Coding Agent from scratch, check out our AI and Machine Learning Program at Outcome School.

Now, we have learned about every building block. Now, let's put them all together into one complete flow.

## A complete flow of how LangChain works

Let's connect everything we have learned into a single story. Suppose a user opens our app and asks a question about our company handbook.

Step 1: The user types the question into our app.

Step 2: LangChain pulls the previous messages from memory and adds them for context.

Step 3: LangChain uses retrieval to fetch the matching chunks from the vector store.

Step 4: The prompt template combines the question, the memory, and the retrieved chunks into one final prompt.

Step 5: This prompt flows into the LLM through the chain.

Step 6: If the task needs an action, the LLM recommends a tool, and the agent runs that tool and brings the result back to the LLM.

Step 7: The LLM produces an answer.

Step 8: The output parser cleans the answer into a neat form.

Step 9: The clean answer is shown to the user, and the new messages are saved into memory for the next turn.

The complete flow looks like below:

```text
   User question
        |
        v
  +-----------+        +-----------+        +--------------+
  |  Memory   | -----> |  Prompt   | <----- | Retrieval /  |
  | (context) |        | Template  |        | Vector Store |
  +-----------+        +-----------+        +--------------+
        ^                    |
        |                    v
        |              +-----------+  agent calls   +-------+
        |              |    LLM    | <------------> | Tools |
        |              +-----------+ (LLM advises)  +-------+
        |                    |
        |                    v
        |              +-----------+
        |              |  Parser   |
        |              +-----------+
        |                    |
        |                    v
        |          Clean answer to user
        |                    |
        +--------------------+
              saves new messages

```

Here, we can see how all the blocks work together. The question first gathers context from `Memory` and matching chunks from `Retrieval`. The `Prompt Template` combines everything into one prompt and sends it to the `LLM`. When an action is needed, the `LLM` recommends a tool, and the `Agent` runs that tool and feeds the result back to the `LLM`. The answer then passes through the `Parser` to become clean, and finally goes back to the user while the new messages are saved into `Memory` for the next turn.

Here, we can see how each block does one job and passes its result to the next block. The input flows in from one side, moves through the chain, and the final answer comes out from the other side. This is exactly the assembly line we talked about at the start.

This is how LangChain works, end to end. Let's quickly recap what we have learned.

LangChain is a framework that helps us build applications powered by LLMs. It gives us small building blocks and lets us chain them together.

We learned about the prompt template that prepares the text, the chain that joins the blocks, and the output parser that cleans the result. We learned about memory that remembers the conversation, retrieval and RAG that bring in our own data, and tools and agents that take real actions.

Now, we must have understood how LangChain works.

### Is LangChain an LLM?

No. LangChain is not an LLM. It is a framework that sits between us and the LLM. It gives us ready-made building blocks, like prompt templates, chains, output parsers, memory, retrieval, and tools, and helps us connect the LLM with our data, our tools, and our logic.

### Does the LLM run tools by itself in LangChain?

No. The LLM only recommends which tool to use and what input to pass to it. The actual call to the tool is made by our code through the agent. The agent runs the tool, takes back the result, and gives it to the LLM, until the task is complete.

### Does an LLM remember earlier messages without memory?

No. Every call to the LLM is fresh, and it does not remember the past on its own. LangChain memory stores the previous messages and adds them to each new prompt, so the LLM sees the full conversation and knows, for example, who "he" refers to.

### What does the pipe symbol do in a LangChain chain?

The `|` pipe sends the output of the left side into the right side. For example, `template | llm | parser` means the filled prompt goes into the LLM, and the LLM's answer goes into the parser. This is how we join small blocks into one chain.

### When should we use LangGraph instead of a simple LangChain chain?

We should use LangGraph when agent steps, decisions, and loops grow complex. In that case, we can lay them out as a graph and let the framework run them for us.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
