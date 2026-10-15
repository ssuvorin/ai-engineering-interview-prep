> Source: https://outcomeschool.com/blog/how-does-cursor-work

# How does Cursor work?
URL: https://outcomeschool.com/blog/how-does-cursor-work
Published: 2026-07-22

How does Cursor work?

# How does Cursor work?

Authors
: - Name
: Amit Shekhar
Published on
: July 22, 2026

In this blog, we will learn about how Cursor works. We will also see what Cursor is, why it is a code editor with an AI brain on top, how it indexes our codebase into embeddings and searches it by meaning, how Tab autocomplete, Chat, and Agent mode work, how Cursor applies changes through a diff, why it uses different models for different jobs, and how it tries to keep our code private.

We will cover the following:

- What is Cursor?
- Cursor = Code Editor + AI
- The big idea behind Cursor
- How does Cursor understand our code?
- How does Cursor index our codebase?
- How does Tab autocomplete work?
- How does the Chat work?
- How does the Agent mode work?
- How does Cursor apply the changes?
- Why does Cursor use different models?
- How does Cursor keep our code private?
- The complete flow of Cursor

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Cursor?

Cursor is an AI code editor. It is a place where we write our code, but with an AI helper sitting right next to us.

Let's say we are writing code. Normally, we type every single line by ourselves. We think, we type, we fix the mistakes, and we repeat. It takes time.

Now, imagine a smart friend sitting next to us. This friend has read a lot of code. When we start typing, the friend already guesses what we want to write next. When we get stuck, we simply ask the friend, and the friend writes the code for us. When we want to build a whole feature, we just describe it in plain English, and the friend does the work across many files.

That smart friend is Cursor.

So, Cursor is a code editor where an AI is always ready to help us read, write, and change our code.

## Cursor = Code Editor + AI

Let's understand both parts.

Code Editor: A code editor is a simple app where we open our files and write our code. Cursor is built on top of a very popular code editor called VS Code. So, if we have ever used VS Code, then Cursor will feel the same. All the buttons, the file explorer on the left, the tabs on the top, everything feels familiar.

AI: This is the special part. Cursor connects our editor to powerful AI models. These AI models are the same kind of models that power tools like ChatGPT. They can read text, understand it, and write text. And code is also just text. So, these AI models can read our code and write new code for us.

So, Cursor takes a normal code editor and adds a powerful AI brain on top of it. That is the whole idea.

## The big idea behind Cursor

Before jumping into the details, we must understand the big idea. It will make everything else easy.

The AI model does not live inside Cursor. The AI model lives on a big computer far away, called a server. This server belongs to companies that build these models.

So, Cursor is like a bridge. On one side, there is us and our code. On the other side, there is the powerful AI model on the server.

We can picture it like below:

```
                        sends our code + question
   +----------------+  ----------------------------->  +-------------------+
   |     Cursor     |                                   |     AI model      |
   |  (our editor   |                                   |  (on the server)  |
   |   + our code)  |  <-----------------------------   |                   |
   +----------------+       returns the answer          +-------------------+

```

Here, we can see that our code never runs the AI by itself. Cursor sends the needed pieces to the AI model and brings the answer back.

When we ask for help, Cursor does three things:

- First, it collects the right pieces of our code. This is called context.
- Then, it sends our question along with that context to the AI model.
- Finally, it takes the answer from the AI model and puts it back into our code.

Here, the most important word is context. The AI model has never seen our project before. It does not know our files. So, Cursor must send the right pieces of our code to the AI model, so that the AI can give a useful answer.

Let's say we ask a doctor for advice over the phone. The doctor is very smart, but the doctor cannot see us. So, we must describe our problem clearly. The better we describe it, the better the advice.

In the same way, the AI model is very smart, but it cannot see our project. So, Cursor must describe our code clearly to the AI model. This is the real magic of Cursor. It is very good at picking the right pieces of our code and sending them to the AI.

Now, let's understand how Cursor does this.

## How does Cursor understand our code?

Let's say our project has a thousand files. When we ask a question, the AI model cannot read all thousand files at once. It is too much. It would be slow and very costly.

So, Cursor must find only the few files that matter for our question. This is the real problem to solve.

For example, we ask, "Where do we check the user's password?" Cursor must find the file that handles the password. It must not send the file that handles the app color or the file that handles the images.

So, how does Cursor find the right files? Here comes the indexing to the rescue. Let's understand it.

## How does Cursor index our codebase?

Indexing means Cursor reads all our files once and prepares them in a smart way, so that later it can search through them very fast.

Let's understand this step by step.

Step 1: Cursor breaks our code into small pieces. Each piece is called a chunk. A chunk is usually a small part of a file, like one function or a few lines that belong together.

Step 2: Cursor turns each chunk into a special list of numbers. This list of numbers is called an embedding.

Now, the word embedding sounds scary, so let's understand it in simple words.

An embedding is a list of numbers that captures the meaning of a piece of text.

The idea is beautiful. Two chunks that mean similar things get similar numbers. Two chunks that mean different things get very different numbers.

Let's say we have two chunks. One chunk is about checking a user's password. Another chunk is also about logging in a user. These two are about similar things. So, their numbers will be close to each other. But a chunk about changing the app color will have very different numbers.

Step 3: Cursor stores all these numbers in a special database. This database is very good at one job. Given some numbers, it can quickly find other numbers that are close to them.

So, now our whole codebase is turned into numbers and stored, ready to be searched.

We have a detailed blog on how a Vector Database works that covers this in depth.

The whole indexing pipeline looks like below:

```
   Our code files
        |
        |  break into small pieces
        v
     Chunks        (one function, or a few related lines)
        |
        |  turn each chunk into numbers
        v
   Embeddings      (a list of numbers that captures the meaning)
        |
        |  store all the numbers
        v
   Vector database (ready to search by meaning)

```

Now, when we ask, "Where do we check the user's password?", here is what happens:

- Cursor turns our question into numbers, the same way it turned the code chunks into numbers.
- Then, it searches the database for the code chunks whose numbers are closest to our question's numbers.
- The closest chunks are most likely the ones that matter for our question.

This way, Cursor finds the right pieces of code without reading the whole project. This search by meaning is often called semantic search.

Note: Cursor is careful here. For most plans, it does not store our actual code on its own servers. It mainly stores these numbers. We will talk more about this in the privacy section.

This is how Cursor understands our codebase. Now, let's move to the features we use every day.

To learn how indexing, embeddings, Vector Databases, and RAG work in depth, check out our AI and Machine Learning Program at Outcome School.

## How does Tab autocomplete work?

The first feature we notice in Cursor is Tab. When we type code, Cursor shows a grey suggestion for the next lines. We press the Tab key, and the suggestion becomes real code.

But this is not a normal autocomplete. A normal editor only completes one word. Cursor predicts the next full edit. It can suggest many lines at once. It can even suggest changes a few lines away from where we are typing.

Let's understand how it works.

Cursor uses a special AI model that is trained for one job only, to predict the next edit. When we type, Cursor sends the model a few things:

- The code around our cursor, both above and below.
- The recent changes we just made.
- Some related pieces from the rest of our project.

The model looks at all this and guesses what we are most likely to write next. Then, it shows that guess as a grey suggestion.

Here, the important point is speed. This suggestion must appear in a fraction of a second. If it is slow, it becomes annoying. So, Cursor uses a smaller and faster model for Tab, not the big heavy model. This smaller model is quick, and it is trained to be very good at this one task.

Let's say we just wrote a line that creates a variable for the user's name. The model sees this. It guesses that our next line will probably use that name to greet the user. So, it suggests that line for us. We press Tab, and it is done.

This is how the Tab autocomplete makes our life easier. It removes the boring typing and lets us move fast.

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

## How does the Chat work?

The next feature is Chat. On the side of the editor, there is a chat box. We can ask any question about our code, and we get an answer.

For example, we can ask, "What does this function do?" or "Why is this test failing?" We can also ask it to write new code for us.

Here is how the Chat works, step by step.

Step 1: We type our question in the chat box.

Step 2: Cursor gathers the context. It uses the indexing we learned about above to find the code chunks that matter for our question. It also adds the file we are currently looking at. We can also point to specific files ourselves.

Step 3: Cursor builds a full message for the AI model. This message contains our question and the gathered context. This step of building a good message is called the prompt.

Step 4: Cursor sends this prompt to the big AI model on the server.

Step 5: The AI model reads everything and writes an answer. The answer comes back to Cursor and appears in the chat.

So, the Chat is just a smart conversation. But the reason it feels smart is the context. Because Cursor sends the right pieces of our code, the AI can answer about our actual project and not just talk in general.

This is how the Chat works.

## How does the Agent mode work?

Now, it's time to learn about the most powerful feature of Cursor, the Agent mode.

In the Chat, the AI only talks to us. In the Agent mode, the AI can do the work by itself. It can read files, write files, and even run commands. It keeps working step by step until the whole task is done.

Let's understand it with an example. We tell the Agent, "Add a dark mode to my app."

A normal chat would just tell us what to do. But the Agent actually does it. Here is how.

The AI model is given a set of tools. A tool is simply an action that the AI is allowed to take. For example:

- A tool to read a file.
- A tool to search the codebase.
- A tool to make an edit in a file.
- A tool to run a command in the terminal.

Cursor can also reach tools beyond these built-in ones, like a database or an issue tracker, through an open standard called MCP. We have a detailed blog on What is MCP (Model Context Protocol)? that explains this step by step.

Now, the Agent works in a loop. Let's see the loop.

- First, the AI thinks about the task and decides the next step. Let's say it decides to first read the settings file.
- Then, it uses the read tool to open that file. Cursor runs the tool and gives the file content back to the AI.
- After that, the AI reads the content and decides the next step. Now, it decides to edit the file to add the dark mode option.
- Then, it uses the edit tool to make the change.
- After that, it may run the app to check if the change works.

This loop keeps going. Think, act, look at the result, think again. The AI repeats this until the task is complete. This think-act-repeat loop is what makes it an agent.

We can picture the loop like below:

```
          +-----------------------+
    +----> |  Think about the      |
    |      |  next step            |
    |      +-----------------------+
    |                 |
    |                 v
    |      +-----------------------+
    |      |  Use a tool           |
    |      |  (read / edit / run)  |
    |      +-----------------------+
    |                 |
    |                 v
    |      +-----------------------+
    |      |  Look at the result   |
    +------|  Task not done yet?   |
    (loop) +-----------------------+
                      |
                      v  Task done!
          +-----------------------+
          |  Stop and show us     |
          |  the final result     |
          +-----------------------+

```

Here, we can see that the AI does not do everything in one shot. It works one small step at a time, and it checks the result after every step.

Here, we are still in control. Cursor can ask us for permission before it does something risky, like running a command. We can review every change before we accept it.

So, the Agent mode turns Cursor from a helper that talks into a helper that works. This is the beauty of Cursor.

If we want to go deep into AI Agents and tool use, we can build an AI Coding Agent from scratch in our AI and Machine Learning Program at Outcome School.

## How does Cursor apply the changes?

Now, the next question is: when the AI writes new code, how does it go into our files?

Let's say the AI wants to change ten lines in a big file of five hundred lines. Sending the whole new file every time would be slow and wasteful.

So, Cursor is smart here. The big AI model does not rewrite the whole file. It only describes the change. It says something like, "In this function, replace these lines with these new lines."

Then, Cursor uses another small and fast model, called the Apply model. The only job of this model is to take that described change and merge it neatly into our real file.

After that, Cursor shows us the change as a diff. A diff is a simple view that shows the old lines in red and the new lines in green. So, we can clearly see exactly what will change.

We look at the diff. If we like it, we click Accept, and the change becomes real. If we do not like it, we click Reject, and nothing changes.

This is how Cursor applies the changes. We always stay in control, because nothing changes until we accept it.

## Why does Cursor use different models?

By now, we have noticed something. Cursor does not use only one AI model. It uses different models for different jobs. This is a smart choice.

The reason is simple. A big and heavy model is very smart, but it is slow and costly. A small and fast model is quick, but it is not as smart. So, Cursor uses the right model for the right job.

Let me tabulate these models for your better understanding so that the whole picture becomes clear.

| Job | Model used | Why |
| --- | --- | --- |
| Tab autocomplete | A small, fast model | The suggestion must appear instantly while we type. |
| Chat and Agent | A big, smart model | The hard thinking and code writing need the smartest model. |
| Applying the change | A small, fast Apply model | Merging a described change into a file is a simple, quick task. |

Here, we can see that each model has one clear job. The big model does the deep thinking. The small models handle the quick tasks. This mix makes Cursor both smart and fast.

## How does Cursor keep our code private?

Our code is important, so a natural question arises. Is our code safe?

Cursor has a setting called Privacy Mode. When Privacy Mode is on, our code is not stored by Cursor after our request is done. The code is used only to answer our question, and then it is not kept.

Here, we must understand one thing clearly. To answer our question, Cursor must send some pieces of our code to the AI model on the server. This is needed, because the AI lives on the server, not on our computer. But with Privacy Mode, that code is not saved for later.

Also, as we learned, the codebase index mostly stores numbers, the embeddings, and not our full code text. This adds another layer of safety.

So, Cursor gives us the power of AI, while still trying to protect our code.

## The complete flow of Cursor

Now that we have learned about all the parts, let's put the whole flow together in simple steps.

- First, Cursor reads our project once and turns it into numbers, the embeddings, and stores them. This is indexing.
- Then, when we type, the fast Tab model predicts our next edit and shows a grey suggestion.
- After that, when we ask a question in Chat, Cursor searches the index, finds the right code chunks, and builds a prompt.
- Then, it sends the prompt to the big AI model on the server, and shows us the answer.
- In Agent mode, the AI uses tools to read, edit, and run code in a loop until the task is done.
- Finally, the Apply model merges the AI's changes into our files, and we accept or reject each change through a diff.

So, Cursor is a bridge between our code and a powerful AI model. It is very good at picking the right pieces of our code, sending them to the AI, and putting the answer back into our files.

This is the beauty of Cursor. It makes our life easy by removing the boring work, while keeping us fully in control of every change.

Now, we must have understood how Cursor works.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# How does Prompt Caching work?
URL: https://outcomeschool.com/blog/how-does-prompt-caching-work
Published: 2026-06-09
Author: Amit Shekhar

How does Prompt Caching work?

# How does Prompt Caching work?

Authors
: - Name
: Amit Shekhar
Published on
: June 9, 2026

Prompt Caching is a technique where the model saves the work it already did for a repeated part of a prompt, so that next time it can reuse that saved work instead of doing it all over again.

In this blog, we will learn about how Prompt Caching works. We will also see why we need it, how it actually works inside a large language model, and where it is used in real systems like AI assistants and agents.

We will cover the following:

- What is a prompt?
- A quick recap of how an LLM reads a prompt
- What is Prompt Caching?
- Why we need Prompt Caching
- The core idea behind Prompt Caching
- The exact-prefix rule
- Cache write vs cache read and TTL
- What we should put in the cache
- The benefits of Prompt Caching
- Prompt Caching in the real world

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a prompt?

Before we talk about Prompt Caching, we must first understand what a prompt is.

A prompt is simply the text we send to a large language model.

[…285ln elided…]

So, anywhere we keep sending the same large beginning of a prompt, Prompt Caching helps us a lot.

If we want to go deep into RAG, Vector Databases, and AI Agents, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

This is how Prompt Caching works. We save the model's internal work for a fixed, repeated beginning of the prompt, we keep that beginning exactly the same and place it first, and then we reuse it again and again to get faster and cheaper responses.

### What is the difference between prompt caching and semantic caching?

Prompt caching reuses the model's internal work, the KV cache, for a repeated beginning of a prompt. The model still reads the new part and writes a fresh reply. Semantic caching reuses the final answer whenever a new question means the same thing, even if the words are different.

### Does prompt caching change the quality of the answers?

No. Prompt caching makes our application faster and cheaper without changing the quality of the answers. The model still sees the full prompt. It just avoids redoing the work for the repeated part that it has already done.

### Why is our prompt cache not getting any hits?

A very common reason is something that changes near the top of the prompt, like the current date, a random ID, or a user name. The cached part must match exactly, character for character, so even one early change breaks the cache for everything after it. We should put the stable part first and the changing part last.

### Is prompt caching always cheaper?

Not for the first request. A cache write costs a little more than normal processing, around 1.25 times the normal price. The savings come from later cache reads, which cost around one-tenth of the normal price. So caching pays off when many requests share the same beginning and arrive within the TTL window.

### How do we know if prompt caching is actually working?

We can check the response from the provider. It shows how many tokens were written to the cache and how many were read from it. If later requests show tokens read from the cache, the caching is working.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# How does Semantic Caching work?
URL: https://outcomeschool.com/blog/how-does-semantic-caching-work
Published: 2026-07-08

How does Semantic Caching work?

# How does Semantic Caching work?

Authors
: - Name
: Amit Shekhar
Published on
: July 7, 2026

Semantic Caching is a cache that matches questions by their meaning instead of their exact words. So, if a new question means the same as an old one, the AI app can reuse the saved answer.

In this blog, we will learn about how Semantic Caching works. We will also see why traditional caching falls short for AI apps, how Semantic Caching uses embeddings and similarity to reuse past answers, and how setting the right threshold makes it work in the real world.

We will cover the following:

- What is a cache?
- The problem with traditional caching for AI apps
- What is Semantic Caching?
- What are embeddings?
- What is similarity between embeddings?
- How does Semantic Caching work step by step?
- A numeric walkthrough
- Setting the similarity threshold
- Advantages of Semantic Caching
- Things to keep in mind

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a cache?

A cache is a place where we store the answer to a question, so that the next time the same question comes, we can return the saved answer instantly.

In simple words, a cache is a memory of past answers.

Let's say a friend asks us, "What is the capital of France?" We answer, "Paris." If the same friend asks the same question again, we do not think again. We simply say "Paris" because we remember it.

That memory of past answers is the cache. It saves us time, and it saves us effort.

This is how a cache works in software too. The first time, we do the hard work and compute the answer. After that, we store it. The next time, we return the stored answer directly.

### The problem with traditional caching for AI apps

Now, let's understand why normal caching is not enough for AI apps.

Suppose we are building an app that uses a Large Language Model that powers tools like ChatGPT. Every time a user asks a question, our app sends that question to the model, the model thinks, and then it returns an answer.

But, here is the catch. Sending a question to the model costs money, and it also takes time. If a thousand users ask the same thing, we pay a thousand times, and each user waits.

So, we think of caching. We store each question and its answer. The next time the exact same question comes, we return the stored answer.

This is called exact-match caching. It matches the question word by word, letter by letter.

Let's see the problem with an example. Assume that two users ask these questions:

- User 1: "What is the capital of France?"
- User 2: "Tell me the capital city of France."

For us humans, both questions mean the same thing. The answer is "Paris" in both cases.

But for exact-match caching, these two are completely different. The words are different, the order is different, so the cache thinks they are two separate questions. It will send the second question to the model again, and we pay again.

The issue with this approach is that it only understands letters, not meaning. People ask the same thing in many different ways, so the cache almost never matches.

We needed a solution for that, and Semantic Caching was introduced to solve this problem.

### What is Semantic Caching?

Semantic Caching is a cache that matches questions by their meaning instead of their exact words.

Let's break the term to understand it better.

> Semantic Caching = Semantic + Caching

The word "semantic" simply means "related to meaning." So, Semantic Caching is caching based on meaning.

In simple words, if a new question means the same thing as an old question, we return the old answer, even if the words are different.

Going back to our example, "What is the capital of France?" and "Tell me the capital city of France." mean the same thing. So, Semantic Caching treats them as a match and returns "Paris" without asking the model again.

This is the beauty of Semantic Caching. It understands intent, not just text.

Now, the next big question is: how does a computer understand the meaning of a sentence? A computer only understands numbers. So, here come embeddings into the picture.

### What are embeddings?

An embedding is a list of numbers that represents the meaning of a piece of text.

In simple words, an embedding turns a sentence into numbers, in such a way that sentences with similar meaning get similar numbers.

Let's understand this with a simple picture in our mind. Imagine a big map. On this map, every sentence becomes a single point. Sentences that mean the same thing land close to each other. Sentences that mean very different things land far apart.

For the sake of understanding, consider this map:

- "What is the capital of France?" lands at one point.
- "Tell me the capital city of France." lands very close to it, because the meaning is almost the same.
- "How do I bake a chocolate cake?" lands very far away, because the meaning is totally different.

So, the embedding is just the address of that point on the map, written as a list of numbers.

Let's visualize this map of meaning as below:

```text
   meaning
      ^
      |
      |   [France capital question]
      |   [France capital city question]   <- close, same meaning
      |
      |
      |
      |                          [bake a chocolate cake]  <- far, different
      |
      +-------------------------------------------------> meaning

```

Here, we can see that the two questions about the capital of France land close to each other, because they mean almost the same thing. The question about baking a cake lands far away, because its meaning is completely different. This closeness on the map is exactly what we measure later.

A real embedding has hundreds of numbers. But for the sake of understanding, let's pretend each embedding has only two numbers. We can write them like below:

```python
# Just for understanding, real embeddings have hundreds of numbers
"What is the capital of France?"      -> [0.91, 0.10]
"Tell me the capital city of France." -> [0.89, 0.12]
"How do I bake a chocolate cake?"     -> [0.05, 0.95]

```

Here, we can notice that the first two lists of numbers are very close to each other. The third one is far away. This matches our understanding, because the first two questions mean the same thing, and the third one means something completely different.

This is how a model converts meaning into numbers. We use a special model called an embedding model to create these numbers for any text we give it.

To learn embeddings, Vector Databases, and RAG in depth, we cover all of these in our AI and Machine Learning Program at Outcome School.

### What is similarity between embeddings?

Now that we have learned about embeddings, it's time to learn how we compare two embeddings.

Similarity is a number that tells us how close two embeddings are in meaning.

In simple words, we take two lists of numbers and we calculate a single score. A high score means the meanings are close. A low score means the meanings are far apart.

The most common score used here is called cosine similarity. We do not need to learn the math today. We just need to remember one thing.

> Higher similarity score means closer meaning.

For the sake of understanding, the score usually goes from 0 to 1.

- A score near 1 means the two sentences mean almost the same thing.
- A score near 0 means the two sentences mean very different things.

So, when a new question comes, we find its embedding, and we compare it with the embeddings of all our saved questions. If any saved question has a high enough similarity score, we treat it as a match.

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

### How does Semantic Caching work step by step?

Before we see the full flow, let me map each piece to a simple real-world role for your better understanding.

| Piece in Semantic Caching | Real-world role |
| --- | --- |
| Embedding model | A translator that turns a sentence into numbers |
| Embedding | The address of a sentence on the map of meaning |
| Similarity score | A judge that tells how close two meanings are |
| Threshold | A rule that decides "close enough or not" |
| Cache | A notebook of past questions and their answers |

Now, let's put everything together and see the full flow.

Step 1: A user sends a question to our app.

Step 2: We convert the question into an embedding using the embedding model. Now the question is a list of numbers.

Step 3: We compare this embedding with the embeddings of all the questions already stored in our cache. We calculate a similarity score for each.

Step 4: We find the saved question with the highest similarity score.

Step 5: Now, the decision. If the highest score is above a chosen limit, we call it a cache hit. We return the saved answer directly, without calling the model. This is fast and free.

Step 6: If no saved question crosses that limit, we call it a cache miss. We send the question to the model, get a fresh answer, and then store the new question, its embedding, and its answer in the cache for the future.

This is how Semantic Caching serves answers by meaning.

We can picture the full flow as below:

```text
        User question
              |
              v
   +----------------------+
   |   Embedding model    |   (turn text into numbers)
   +----------------------+
              |
              v
   +----------------------+
   |  Search the cache    |   (compare with saved embeddings)
   |  for the best score  |
   +----------------------+
              |
              v
       score >= threshold ?
        /              \
      yes               no
       |                 |
       v                 v
  +-----------+   +--------------------+
  | Cache hit |   |    Cache miss      |
  | return    |   | ask the model,     |
  | saved     |   | then store the new |
  | answer    |   | question + answer  |
  +-----------+   +--------------------+

```

Here, we can see that every question first becomes numbers through the embedding model. We then search the cache for the closest saved question and its score. If the score crosses the threshold, we take the left path and return the saved answer, which is a cache hit. If it does not, we take the right path, ask the model for a fresh answer, and store it, which is a cache miss.

In a real system, these saved embeddings live in a vector database that is built to store embeddings and find the closest ones fast using Approximate Nearest Neighbor (ANN) search.

Let's see this flow in simple code as below:

```python
def get_answer(question):
    new_embedding = embed(question)            # Step 2: text to numbers

    best_match, score = search_cache(new_embedding)  # Step 3 and 4

    if score >= 0.85:                          # Step 5: cache hit
        return best_match.answer

    answer = ask_model(question)               # Step 6: cache miss
    store_in_cache(question, new_embedding, answer)
    return answer

```

Here, we can see the whole idea in one place. The `embed` function turns the question into numbers. The `search_cache` function finds the closest saved question and its similarity `score`. If the `score` is high enough, which is `0.85` in our example, we return the saved answer. If not, we ask the model, and then we save the new result so that the next similar question becomes a cache hit.

Here, the number `0.85` is the limit we talked about. It is called the similarity threshold, and we will understand it in detail next.

### A numeric walkthrough

The best way to learn this is by taking an example. Let's walk through it step by step with numbers.

Assume that our cache already has one saved question.

- Saved question: "What is the capital of France?"
- Saved answer: "Paris"

Now, a new user sends a question, and we compare it with our saved question.

Step 1: New question is "Tell me the capital city of France." We compute its embedding and compare it with the saved one. The similarity score comes out to be `0.93`. Our threshold is `0.85`. Since `0.93` is greater than `0.85`, this is a cache hit. We return "Paris" instantly, and we do not call the model.

Step 2: New question is "What is the population of France?" We compute its embedding and compare it. The similarity score comes out to be `0.40`. This is below `0.85`, so this is a cache miss. We send it to the model, get the fresh answer, and store it in the cache.

Step 3: New question is "How do I bake a chocolate cake?" We compute its embedding and compare it. The similarity score comes out to be `0.05`. This is far below `0.85`, so this is again a cache miss. We send it to the model and store the new answer.

Here, we can notice the pattern. Same meaning gives a high score and becomes a cache hit. Different meaning gives a low score and becomes a cache miss. This is exactly what we wanted.

### Setting the similarity threshold

The similarity threshold is the limit we choose to decide whether a new question is close enough to a saved one.

This single number is very important, so let's understand it carefully.

If we set the threshold too high, like `0.99`, then almost nothing matches. Only an exact copy would pass. We lose most of the benefit of Semantic Caching.

If we set the threshold too low, like `0.50`, then very different questions start matching. We may return a wrong answer. For example, "capital of France" could wrongly match "capital of Germany" and return the wrong city.

So, the threshold is a balance. A value around `0.85` to `0.95` works well for many apps, but the right value depends on our use case. We must test it with real questions from our users and adjust it.

> A high threshold means fewer matches but safer answers. A low threshold means more matches but a higher chance of a wrong answer.

To learn embeddings, Vector Databases, and RAG in depth, we cover all of these in our AI and Machine Learning Program at Outcome School.

### Advantages of Semantic Caching

Now, let's quickly look at why Semantic Caching is so useful.

- It saves money, because we call the expensive model far less often.
- It is much faster, because returning a saved answer takes very less time compared to asking the model.
- It reduces load on the model, so our app can handle many more users.
- It matches questions by meaning, so it works even when users phrase the same thing in different ways.

This is how Semantic Caching makes our AI apps cheaper and faster at the same time.

Semantic Caching is one way to cut the cost of LLM calls. Another is prompt caching, which reuses the model's internal work on a repeated prompt prefix. We have a detailed blog on how Prompt Caching works that explains this step by step.

### Things to keep in mind

Semantic Caching is powerful, but we must use it carefully. Let me share a few important points.

First, it is best for questions whose answers do not change quickly. A question like "What is the capital of France?" is perfect, because the answer stays the same. But a question like "What is the weather right now?" is not a good fit, because the correct answer changes every hour.

Second, we must pick a good threshold. As we learned, a wrong threshold can either kill the benefit or return wrong answers.

Third, we may want to clear or refresh the cache from time to time, so that old answers do not stay forever when the real answer has changed.

Now, we have understood how Semantic Caching works. We started with a simple cache, we saw why exact-match caching fails for AI apps, we learned about embeddings and similarity, and finally we put it all together into a clear step-by-step flow with a numeric walkthrough.

### What is the difference between semantic caching and prompt caching?

Semantic caching reuses the saved final answer when a new question means the same as an old one, so the model is not called at all. Prompt caching reuses the model's internal work on a repeated prompt prefix. Both help cut the cost of LLM calls.

### Can semantic caching return a wrong answer?

Yes, if the similarity threshold is set too low. With a low threshold like 0.50, very different questions start matching. For example, a question about the capital of France could wrongly match a question about the capital of Germany and return the wrong city. We must test the threshold with real user questions.

### Is semantic caching a good fit for questions like the current weather?

No. Semantic caching is best for questions whose answers do not change quickly, like the capital of France. A question about the weather right now is not a good fit, because the correct answer changes every hour. We may also refresh the cache from time to time so old answers do not stay forever.

### Where are the embeddings stored in a semantic cache?

In a real system, the saved embeddings live in a vector database. A vector database is built to store embeddings and find the closest ones fast using Approximate Nearest Neighbor search. Each entry keeps the question, its embedding, and its answer.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

[Showing lines 1-401 and 687-1069 of 1069; 285 middle lines (17.6KB) elided. Read artifact://86 for full output]
