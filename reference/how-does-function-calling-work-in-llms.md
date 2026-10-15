> Source: https://outcomeschool.com/blog/how-does-function-calling-work-in-llms

# How does Function Calling work in LLMs?
URL: https://outcomeschool.com/blog/how-does-function-calling-work-in-llms
Published: 2026-06-13
Author: Amit Shekhar

How does Function Calling work in LLMs?

# How does Function Calling work in LLMs?

Authors
: - Name
: Amit Shekhar
Published on
: June 13, 2026

Function Calling is a way to let an LLM use external tools, APIs, and functions to get things done. The model does not run the function itself. It only tells our code which function to call and with which inputs.

In this blog, we will learn about how Function Calling works in LLMs. We will see what it is, why we need it, the key insight behind it, and how it powers AI agents and assistants step by step.

We will cover the following:

- What is Function Calling?
- Why We Need Function Calling
- The Key Insight: The Model Does Not Run the Function
- How Function Calling Works Step by Step
- A Concrete Example: get_weather(city)
- The Conversation Loop
- Multi-Step and Parallel Function Calling
- Relation to Structured Outputs and JSON Mode
- Real-World Use: The Backbone of AI Agents
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Function Calling?

Function Calling is a way to let an LLM use external tools, APIs, and functions to get things done. It is also called tool calling, and both names mean the same thing.

Before we go further, let's make sure we understand a few words.

An LLM (Large Language Model) is the model behind tools like ChatGPT. It reads text and generates text. That is the only thing it does on its own.

A function is a small block of code that does one job. For example, a function can fetch today's weather, send an email, or look up a price in a database.

An API is a doorway that lets one program ask another program for something. For example, a weather service gives us an API so our program can ask it for the current temperature.

So, in simple words, Function Calling means we give the LLM a list of functions it is allowed to use, and the LLM can ask for one of them to be run when it needs help from the outside world.

Let's say we are building a chat assistant. A user asks, "What is the weather in Paris right now?" The LLM alone cannot answer this correctly, because it does not know the live weather. But if we connect a weather function to it, the assistant can get the real answer.

This is what Function Calling gives us. It is the bridge between the model that writes text and the real world that has live data and real actions.

### Why We Need Function Calling

To understand why we need it, we must first understand the limit of an LLM.

An LLM only generates text. It cannot fetch live data, and it cannot take real actions on its own.

Let's make this concrete with a small story.

Suppose we ask a plain LLM, "What is the weather in Paris right now?"

The model was trained on text from the past. It has no live connection to a weather station. So it can only guess based on old patterns. It will often reply with a confident sentence that sounds correct but is actually made up. This made-up answer is called a hallucination.

Now suppose we ask, "Send an email to my manager saying I will be late."

The LLM can write a perfect email. But it cannot actually send it. It has no hands. It can only produce text.

So we have two big gaps:

- Live data gap: the model does not know anything that happened after its training, and it cannot look things up.
- Action gap: the model cannot do anything in the real world - no sending, no booking, no saving, no paying.

We needed a solution for that, and Function Calling was introduced to solve this problem.

Here is the simple idea. Our application already knows how to fetch live weather and how to send emails - that is normal code we can write. The model is great at understanding language and deciding what to do. So, what if we let the model decide which function to use, and let our application actually run it?

This is exactly how Function Calling closes both gaps. It comes into the picture to connect the smart language model with the real tools our code already has.

### The Key Insight: The Model Does Not Run the Function

This is the most important idea in the whole blog, so let's slow down here.

The model does not execute the function. It only outputs a structured request to run it. Our application runs the function.

Let's read that again, because most beginners get confused at this exact point.

The LLM never touches the weather service. It never sends the email. It cannot. All it can do is generate text.

So when the model decides a function is needed, it does the only thing it can do - it generates text. But this time the text is special. It is a neat, structured message that says, "Please run the function named `get_weather` with the argument `city` set to `Paris`." Here, an argument simply means an input value we hand to a function.

This structured message is written in JSON. JSON is a simple text format for organizing data as key and value pairs. We will see real JSON in a moment.

So the flow is split between two players:

```
LLM (the brain)                  Our Application (the hands)
-----------------                ---------------------------
Reads the question
Decides a tool is needed
Outputs JSON request       -->   Reads the JSON request
  (name + arguments)             Runs the real function
                                 Gets the real result
Writes the final answer    <--   Sends the result back
in plain English

```

Here, we can see that the model is the brain and our application is the hands. The brain decides what to do, and the hands actually do it.

This split is what keeps everything safe and correct. Our code stays fully in control. The model can only suggest a function call. It can never run anything by itself. We decide whether to run it, and we decide what to do with the result.

This is the key insight. Once we understand this, the rest is easy.

This decide-then-run split is the foundation that real agents are built on. To go deep into the AI Agent, Agentic AI, and Agent Architecture, check out our AI and Machine Learning Program at Outcome School, where we cover them from the ground up.

### How Function Calling Works Step by Step

Now, let's walk through the full process from start to finish. There are five clear steps. We will go through each of them in detail.

Before we read each step, let's see the full round-trip as one loop. We can picture it as below:

```
       user prompt + tool schemas
                    |
                    v
        +-----------------------+
        |          LLM          |
        |  decides a tool is    |
        |  needed, emits a      |
        |  JSON function call   |
        +-----------------------+
                    |
       JSON call    |   (name + arguments)
                    v
        +-----------------------+
        |    Our Application    |
        |  runs the real        |
        |  function / API       |
        +-----------------------+
                    |
      real result   |   (live data)
                    v
        +-----------------------+
        |          LLM          |
        |  reads the result,    |
        |  writes the final     |
        |  plain answer         |
        +-----------------------+
                    |
                    v
           final answer to user

```

Here, we can see that everything moves in a circle. The user prompt and the tool schemas go into the model. The model does not answer right away - it emits a JSON function call. That call goes to our application, which runs the real function and gets live data. The result travels back into the model, and only then does the model write the final answer for the user. The model and our application take turns, and our code runs every real action.

Step 1: We describe the available functions.

Before the conversation starts, we tell the model which functions exist. For each function, we provide three things:

- name - what the function is called, for example `get_weather`.
- description - a plain-English sentence saying what it does, for example "Get the current weather for a city."
- parameters - the inputs the function needs, written as a JSON schema.

A JSON schema is just a description of the shape of the data. It says what fields exist, what type each field is (text, number, and etc.), and which ones are required. It does not contain real values. It is like a blank form that describes which boxes must be filled.

Step 2: The user asks a question.

The user types something, for example "What is the weather in Paris?" We send this message to the model together with the function descriptions from Step 1.

Step 3: The model decides and returns a JSON call.

The model reads the question and the function list. It understands that answering needs live weather. So it does not write a normal sentence. Instead it returns a structured JSON request naming the function `get_weather` and the argument `city` set to `Paris`.

Step 4: Our code executes the function.

Our application reads that JSON. It calls the real `get_weather` function with `city = "Paris"`. This function talks to the weather API and gets the real result, for example 18 degrees and sunny.

Step 5: We send the result back, and the model writes the final answer.

We send the weather result back to the model. Now the model has the live data it was missing. It writes a clean, natural sentence: "The weather in Paris is currently 18 degrees and sunny."

That is the whole loop. The model asked for a tool, we ran it, we handed back the result, and the model finished the answer in plain language.

Let me put these five steps in one simple picture:

```
Step 1: We describe functions  -->  [ name, description, parameters ]
Step 2: User asks question     -->  "What is the weather in Paris?"
Step 3: Model returns JSON      -->  { "name": "get_weather",
                                        "arguments": { "city": "Paris" } }
Step 4: Our code runs it        -->  get_weather("Paris") => 18C, sunny
Step 5: We send result back     -->  model writes the final sentence

```

This is how Function Calling works at a high level. Now, let's make it fully concrete with real JSON.

### A Concrete Example: get_weather(city)

The best way to learn this is by taking an example. Let's build the weather assistant end to end.

First, in Step 1, we describe our function to the model. We do this as below:

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a given city.",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "The name of the city, for example Paris."
      }
    },
    "required": ["city"]
  }
}

```

Here, we can see the three parts we talked about. The `name` is `get_weather`. The `description` tells the model what the function does. The `parameters` part is the JSON schema. It says there is one input called `city`, its `type` is `string` (which means text), and it is `required`. Notice there is no real city here yet - this is just the blank form that describes the shape.

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

Next, in Step 2, the user asks a question, and we send it to the model along with the description above.

In Step 3, the model decides the function is needed and returns a JSON call as below:

```json
{
  "name": "get_weather",
  "arguments": {
    "city": "Paris"
  }
}

```

Here, we can notice that the model filled in the blank form. It chose the function `get_weather` and set the argument `city` to `Paris`. The model did not run anything. It only produced this neat request. This is the structured request we kept talking about.

Now comes Step 4. Our application reads this JSON and calls the real function. In simple terms, our code runs:

```python
result = get_weather(city="Paris")
# result = { "temperature": 18, "condition": "sunny" }

```

Here, we have called the real `get_weather` function with `city` set to `Paris`. This function talks to the weather API and gives us back the live result - 18 degrees and sunny.

Finally, in Step 5, we send this result back to the model as a new message. The model now has the missing live data, so it writes the final answer:

> The weather in Paris is currently 18 degrees and sunny.

Problem Solved! The user got a correct, live answer. The model supplied the language, and our function supplied the real data. This way we can use Function Calling to solve this kind of problem in a very simple way.

### The Conversation Loop

Now, let's understand the conversation as a back-and-forth, because the messages flow in a specific order.

A Function Calling conversation is not a single question and answer. It is a small loop of messages between us and the model. Each turn adds a new message to the history, and we keep the full history so the model always sees what happened before.

Let's follow the messages one by one for our weather example:

```
Message 1 (user)      : "What is the weather in Paris?"
Message 2 (model)     : function call -> get_weather(city="Paris")
Message 3 (tool)      : result -> { "temperature": 18, "condition": "sunny" }
Message 4 (model)     : "The weather in Paris is 18 degrees and sunny."

```

Here, we can see four messages. The user speaks first. The model replies, but instead of a sentence it asks for a tool. We run the tool and add the result as a special `tool` message. Then the model reads the result and writes the final sentence.

The important thing to notice is the role of each message. The `user` message is what the person typed. The `model` message can be either a normal sentence or a function call. The `tool` message is the result that our code feeds back.

So, after our code runs a function, we always send the result back into the same conversation. The model then decides what to do next. Sometimes it writes the final answer. Sometimes it asks for another function. This is the loop, and we keep it going until the model produces a normal answer with no more function calls.

This back-and-forth is exactly the loop an AI agent runs on. We have a detailed blog on the AI Agent Loop that explains how an agent keeps cycling through tool calls until the task is done.

### Multi-Step and Parallel Function Calling

So far we used one function. But real tasks often need more. Let's see two cases.

Multi-step function calling.

Sometimes the model needs functions to be run one after another, where the second request depends on the first.

Let's say the user asks, "What should I wear in Paris today?" To answer well, the model first needs the weather. So it recommends `get_weather(city="Paris")`. Our code runs it and sends back "18 degrees and sunny". Now the model has what it needs and writes the clothing advice. If the task needed even more data, the model could recommend another function before answering. Each round is one turn of the same loop we just learned.

Parallel function calling.

Sometimes the model needs several pieces of data that do not depend on each other. In that case it can ask for more than one function call at the same time.

Let's say the user asks, "Compare the weather in Paris and London." The two cities are independent, so the model can return two function calls together as below:

```json
[
  { "name": "get_weather", "arguments": { "city": "Paris" } },
  { "name": "get_weather", "arguments": { "city": "London" } }
]

```

Here, we can see two calls in one list. Our application runs both functions, collects both results, and sends them both back to the model. The model then writes one combined answer comparing the two cities.

Note: Even with multi-step and parallel calls, the key insight does not change. The model only suggests the calls. Our code always runs them. We stay in control the whole time.

This is how Function Calling scales from one simple tool to many tools working together.

This pattern of running a tool, reading the result, then deciding the next step is exactly how a ReAct Agent works, which we cover in a separate blog.

### Relation to Structured Outputs and JSON Mode

We have seen that the model returns clean JSON for a function call. Now let's connect this to two related ideas, because beginners often mix them up.

Structured outputs mean asking the model to return its answer in a fixed, predictable shape instead of free-flowing text. For example, we may want the answer always as JSON with the fields `name`, `age`, and `city`.

JSON mode is a setting that forces the model to reply only with valid JSON, never with extra words around it.

So how do these relate to Function Calling? They share the same foundation. Function Calling works because the model is able to produce a strict, well-formed JSON object that matches the schema we gave it. That ability to follow a schema is the same ability behind structured outputs and JSON mode.

Let me tabulate the difference between them for your better understanding:

| Idea | What it does | Who runs anything |
| --- | --- | --- |
| Structured outputs | Forces the answer into a fixed data shape | Nobody runs code; it is just the answer |
| JSON mode | Forces the reply to be valid JSON only | Nobody runs code; it is just the reply |
| Function Calling | Returns a JSON request naming a function and its arguments | Our application runs the real function |

Here, we can see the key difference. Structured outputs and JSON mode are about the shape of the answer. Function Calling goes one step further - the JSON it returns is a request for our code to take a real action. Function Calling is structured output put to work.

Function Calling is where real tool-using agents begin. We cover Tool use in Agents, the Model Context Protocol (MCP), and how to build an AI Coding Agent from scratch in our AI and Machine Learning Program at Outcome School.

### Real-World Use: The Backbone of AI Agents

Now that we understand how it works, let's see why it matters so much.

Function Calling is the backbone of AI agents and assistants.

An AI agent is a system that does not just chat - it works toward a goal by taking actions. To take actions, it must use tools. And the way it uses tools is Function Calling. Without it, an agent would only be able to talk, never act.

Let's look at a few real-world uses:

- A travel assistant calls `search_flights`, then `book_flight`, then `send_confirmation_email`.
- A coding assistant calls `read_file`, `edit_file`, and `run_tests` to fix a bug.
- A support bot calls `lookup_order`, `check_refund_policy`, and `issue_refund`.
- A data assistant calls `run_sql_query` to answer questions from a live database.

In every case the pattern is the same one we learned. We describe the tools. The user states a goal. The model recommends which tools to run and in what order. Our code runs them and feeds the results back. The model keeps going until the goal is done.

Describing those tools once, in a way that every AI application can reuse, is exactly what an open standard called MCP gives us. We have a detailed blog on What is MCP (Model Context Protocol)? that covers this end to end.

This is why Function Calling is so powerful. It turns a model that can only write text into a system that can act in the real world, and that too in a safe and controlled way, because our code runs every action.

That last point is also our strongest security boundary. The model only asks, our code decides, so a model that has been tricked still cannot do what our code refuses to run. We have a detailed blog on Prompt Injection in LLMs that explains how a model gets tricked and how we design around it.

> Function Calling is the bridge between language and action.

### Quick Summary

Let's quickly recap everything we learned.

- Function Calling (also called tool calling) lets an LLM use external tools, APIs, and functions.
- We need it because an LLM only generates text - it cannot fetch live data or take real actions on its own.
- The key insight is that the model does not run the function. It only outputs a structured JSON request with the function name and arguments. Our application runs the function.
- The flow has five steps: we describe the functions, the user asks, the model returns a JSON call, our code runs the function, and we send the result back so the model can write the final answer.
- The conversation is a loop of `user`, `model`, and `tool` messages that continues until the model gives a normal answer.
- The model can recommend functions in multiple steps or several in parallel, but our code always runs them.
- Function Calling builds on the same schema-following ability behind structured outputs and JSON mode.
- It is the backbone of AI agents and assistants, because it lets a text model take real, controlled actions.

This is how Function Calling works in LLMs.

### Is Function Calling the same as tool calling?

Yes. Function Calling is also called tool calling, and both names mean the same thing. In both cases, we give the LLM a list of functions it is allowed to use, and the LLM can ask for one of them to be run when it needs help from the outside world.

### What is the difference between Function Calling and MCP?

Function Calling is how the model asks for a tool to be run, with the function name and arguments in JSON. MCP is an open standard for describing those tools once, in a way that every AI application can reuse. So, MCP is about describing tools for reuse, and Function Calling is about the model requesting them.

### Is Function Calling safe if the model gets tricked?

It is our strongest security boundary. The model only asks for a function call, and our code decides whether to run it. So a model that has been tricked still cannot do what our code refuses to run. Our application stays fully in control of every real action.

### Does the model always return a function call when tools are available?

No. The model returns a function call only when it decides a tool is needed. After our code sends back a result, sometimes the model asks for another function, and sometimes it writes the final answer. The loop ends when the model gives a normal answer with no more function calls.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
