> Source: https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization

# Prefill vs Decode: LLM Inference Optimization
URL: https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization
Published: 2026-07-05
Author: Amit Shekhar

Prefill vs Decode: LLM Inference Optimization

# Prefill vs Decode: LLM Inference Optimization

Authors
: - Name
: Amit Shekhar
Published on
: July 5, 2026

Prefill and Decode are the two phases of LLM inference. Prefill reads the entire prompt in one single pass and produces the first token, whereas Decode generates the rest of the tokens one at a time, reusing the KV cache that prefill prepared.

In this blog, we will learn about Prefill vs Decode, the two phases of LLM inference, and how understanding them helps us optimize the speed of an LLM. We will also see how the prefill and decode phases work, how the KV cache connects them, how they differ and when to use which one based on our use case, and how we optimize each phase to make an LLM faster.

We will cover the following:

- What is LLM inference?
- The two phases: Prefill and Decode
- Prefill explained in simple words
- Decode explained in simple words
- A diagram of the two phases and the KV cache flow
- The KV cache as the bridge between the two phases
- A step-by-step walkthrough of a few decode steps
- Prefill vs Decode comparison table
- Why this split matters: compute-bound vs memory-bound
- The key metrics: TTFT, TPOT, throughput, and end-to-end latency
- Optimization techniques mapped to each phase
- Conclusion

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is LLM inference?

Before we learn about prefill and decode, we must understand what LLM inference means.

An LLM is a Large Language Model. It is the model that powers chat assistants like the ones we use every day.

Inference is the act of using a trained model to produce an answer. In simple words, inference is the model actually doing its job, which means reading your question and writing back a reply.

Here is the most important thing to understand. An LLM does not write out the whole answer at once. It writes the answer one small piece at a time. Each small piece is called a token. A token is a small chunk of text, like a word or a part of a word.

So, the model generates one token, then the next token, then the next, until the full answer is complete. This is why, when you use a chat assistant, you can see the words appear one after another like someone typing. This live, token-by-token appearance is called streaming.

To get a feel for scale, a short sentence is roughly 15 to 20 tokens. So, a 1,000 token prompt is about a page of text, and a 200 token answer is a few sentences.

A request is simply one user's question sent to the model. When we say the server handles many requests, we mean it answers many users' questions.

Now, we have understood what LLM inference is. It is the model generating text token by token.

## The two phases: Prefill and Decode

Every time an LLM answers a request, it goes through two distinct phases.

- Prefill is the first phase. It reads and processes the whole input prompt that you sent.
- Decode is the second phase. It generates the output tokens one at a time.

In simple words, prefill is the model reading your question, and decode is the model writing the answer.

Both phases use the exact same model. They do not use different models or different weights. The weights are the millions of numbers the model learned during training. They are what the model "knows", and there are so many of them that they take up a large part of the GPU's memory. We will use this fact soon. Only the way the two phases work is different, and that small difference changes everything, as we will see.

Let's understand each phase deeply.

## Prefill explained in simple words

Prefill is the phase where the model reads and processes your entire input prompt in one single pass and produces the very first output token.

The best way to learn this is by taking an example.

Suppose you paste a question that is 1,000 tokens long. In the prefill phase, the model does not read these 1,000 tokens one by one. It reads all 1,000 tokens together, at the same time.

Let's say a student walks into an exam hall. Before writing anything, the student silently reads the entire question paper. The student scans every question at once and jots down quick notes about what matters. This reading-the-whole-paper part is prefill.

Because the whole prompt is already known up front, there is no need to wait. The model can process every input token at the same time. This is called parallel processing. Means, many things happen together instead of one after another.

While reading the prompt, the model also prepares some notes for later. For every input token, it computes and stores two special pieces of data, called the Key (K) and the Value (V). All of these stored Keys and Values together form the KV cache. Do not worry about what exactly Key and Value mean right now. For now, just understand that the KV cache is the model's memory of your prompt. We will learn about it in detail soon.

So, prefill fills up this KV cache with the model's notes about every input token. And at the end of prefill, the model produces the very first output token.

Here is a very important point. Prefill produces only the first output token, not the whole answer. All the remaining tokens come later, in the decode phase.

Prefill is compute-bound. The compute-bound means the speed is held back by the math, nothing else. A GPU is the powerful chip that runs the model. Inside the GPU there are math units, which are the parts that actually do the multiplication. During prefill, these math units are kept very busy doing heavy math. On a high-end GPU, the math units can stay highly used during prefill, often approaching 90 percent or more on large prompts. The GPU is well used.

Why is prefill so heavy on math? Because when many tokens are processed together, the work becomes very large multiplication of big tables of numbers. A big table of numbers like this is called a matrix, and multiplying two big tables together is exactly what GPUs are built for. So, the GPU runs near its full power.

There is one more thing to know. Longer prompts mean longer prefill. A short question feels almost instant. But if we paste a huge document in front of the model, prefill takes longer, and we wait longer before the first word appears.

In fact, part of the prefill work grows even faster than the prompt length. Inside the model there is a step, called attention, where every token must look at every other token to understand the context. So, doubling the prompt roughly quadruples this part of the work. For a concrete number, doubling the prompt from 100 to 200 tokens makes this part of the work about 4 times bigger, not 2 times. Means, very long prompts can feel slow before the first word appears. Here is a simple picture. In a room of 10 people, everyone shaking hands with everyone is manageable. But in a room of 100 people, the number of handshakes explodes. The bigger the room, which means the longer the prompt, the much faster the work piles up.

This wait before the first word is so important that it has its own name, which we will learn in the metrics section. For now, remember this simple line.

> Faster prefill means sooner you see the first token.

Now, we have understood prefill. Let's move to decode.

## Decode explained in simple words

Decode is the phase where the model generates the output tokens one at a time, reusing the KV cache that prefill prepared.

Let's continue our exam example. Reading the question paper was prefill. Now the student starts writing the answer, word by word. The student writes one word, thinks about it, then writes the next word, and so on. This slow, word-by-word writing is decode.

In decode, the model generates only one new token per step. Then it feeds that token back into itself to help produce the next token. Because each new token depends on the token just produced, the tokens must come strictly one after another. This is called autoregressive generation. In simple words, the model keeps feeding its own output back as new input.

So, decode is sequential. It cannot process all the output tokens at once the way prefill processes all the input tokens at once. Each token must wait for the one before it.

Now, here is the clever part. At each decode step, the model does not re-read and re-process your whole prompt again. That would be very slow and wasteful. Instead, it reads the KV cache, which is the memory that prefill already prepared. It computes the Key and Value for just the one new token, reads all the older Keys and Values from the cache, produces the next token, and then appends the new token's Key and Value to the cache.

So, at each decode step, the cache grows by exactly one entry.

Decode is memory-bandwidth-bound. This is the opposite of prefill. The speed of decode is held back by how fast data can be moved from the GPU's memory into its math units, not by the math itself.

Let's understand why, one small step at a time.

In decode, only one token is processed per step. So, instead of multiplying two big tables together like prefill does, decode multiplies the big table by a single thin row of numbers, which is the one new token. A single thin row like this is called a vector. So, the math for one token is tiny.

But to produce even that one token, the GPU must still read the entire model's weights and the whole growing KV cache from its memory. Remember, the weights are huge, so this is a lot of data to move. Memory bandwidth is the speed at which data can be moved out of the GPU's memory. Here is the key fact to hold on to. Inside a GPU, doing the math is very fast, but fetching a large amount of data from its memory is comparatively slow.

So, the GPU spends most of its time waiting for data to arrive, and its math units sit mostly idle. During decode, the math units of a high-end GPU can sit only around 20 to 40 percent busy for a single request.

Here is a simple analogy. Think of a chef who must walk into a giant pantry, grab one ingredient, walk back, chop it, and repeat, one ingredient per trip. The walking back and forth (moving data from memory) takes far longer than the chopping (the tiny math). The knives (the GPU's math units) sit unused most of the time.

So, prefill keeps the GPU busy with math, but decode keeps the GPU waiting on memory.

Here is one more interesting point. For a typical request, prefill often finishes in a fraction of a second, but decode can run for several seconds, because it produces many tokens one after another. So, decode usually takes most of the total time, even though it uses only a small part of the GPU's math power. This is exactly why so many optimizations focus on the decode phase.

Remember this simple line.

> Faster decode means faster you see the rest of the answer.

Now, we have understood both prefill and decode. Let's visualize them together.

## A diagram of the two phases and the KV cache flow

Let's see a clean diagram of how a request flows through prefill and then decode.

```
INPUT PROMPT (for example, 1,000 tokens)
        |
        v
+-----------------------------+
|   PREFILL  (one big step)   |
|  - reads ALL input tokens   |
|    in parallel              |
|  - writes the KV cache      |
|  - GPU compute very busy    |
+-----------------------------+
        |
        | produces the FIRST output token
        v
+-----------------------------+        +------------------+
|   DECODE  (many small steps)| <----> |     KV CACHE     |
|  - one token per step       |  read  |  (the memory of  |
|  - reads the KV cache       |  and   |   all tokens so  |
|  - appends one new entry    |  grow  |   far)           |
|  - GPU mostly waits on      |        +------------------+
|    memory                   |
+-----------------------------+
        |
        | token 2, token 3, token 4, ... token N
        v
   FULL ANSWER

```

Here, we can see the timeline clearly. There is exactly one prefill pass, and then there are many decode steps. If your answer is 200 tokens long, that is 1 prefill pass plus 200 sequential decode steps. The KV cache is written once by prefill, and then it is read and extended by every single decode step.

This is how the two phases work together.

## The KV cache as the bridge between the two phases

The KV cache is the bridge that connects prefill and decode. So, we must understand it well.

Let's understand the problem it solves first.

Inside the model, to produce the next token, the model must look back at every previous token. For every token, the model computes three things: a Query (Q), a Key (K), and a Value (V). The new token compares its Query against the Keys of all previous tokens, and then it mixes their Values to decide what to say next.

Here is the key observation. A past token's Key and Value never change once they are computed. They do not depend on tokens that come after. So, instead of computing them again and again at every step, we can compute them once and store them. This store of Keys and Values is the KV cache.

The KV cache stores only the Keys and the Values of past tokens. It does not store the Queries. The Query is freshly computed for the current token at every step, so there is no need to store it.

Now, let's see why this matters so much with a small numeric walkthrough. For the sake of understanding, think of one entry in the cache as one token's stored Key and Value.

Suppose prefill has already processed a 3-token prompt. So, the KV cache already has 3 entries. Now decode begins.

Step 1: The model takes the first output token's input, computes its Key and Value, and reads the 3 cached entries to look back. It produces token 4. Then it appends token 4's Key and Value to the cache. The cache now has 4 entries.

Step 2: The model takes token 4, computes its Key and Value, and reads the 4 cached entries to look back. It produces token 5. Then it appends token 5's Key and Value to the cache. The cache now has 5 entries.

Step 3: The model takes token 5, computes its Key and Value, and reads the 5 cached entries to look back. It produces token 6. Then it appends token 6's Key and Value to the cache. The cache now has 6 entries.

Let's visualize how the cache grows across these steps.

```
After prefill   |P1|P2|P3|           ->  cache has 3 entries
Decode step 1   |P1|P2|P3|T4|        ->  append T4, now 4 entries
Decode step 2   |P1|P2|P3|T4|T5|     ->  append T5, now 5 entries
Decode step 3   |P1|P2|P3|T4|T5|T6|  ->  append T6, now 6 entries

```

Here, the boxes P1, P2, and P3 are the prompt tokens written by prefill, and T4, T5, and T6 are appended by decode, one box per step.

Here, we can notice the pattern. At every step, the model computes the Key and Value for only one new token. It reads all the older Keys and Values from the cache instead of computing them again. And the cache grows by exactly one entry per step.

Note: Without the KV cache, every decode step would recompute the Keys and Values of all previous tokens from scratch. Since step N redoes the work for all N earlier tokens, the total work summed over the whole answer grows roughly with the square of the length, which is very slow. The KV cache reduces this so that each token's Key and Value is computed exactly once. This is why the KV cache is not just a small optimization. Without it, decode would be much slower.

But there is a catch. The KV cache keeps growing. It starts at the size of the prompt after prefill, and it grows by one entry for every generated token. It also grows with the number of users being served together, because each user needs their own cache. In extreme cases, such as very long contexts combined with many concurrent users, the total KV cache can even exceed the size of the model weights and fill up the GPU's memory. This growing cache is the reason many of the optimizations we will see later exist. It is also why a whole family of KV Cache Compression techniques exists to shrink the cache itself.

This is how the KV cache works as the bridge between prefill and decode.

To master the KV Cache, the Q, K, and V matrices, and build a Large Language Model (LLM) from scratch, check out our AI and Machine Learning Program at Outcome School.

## Prefill vs Decode comparison table

Let me tabulate the differences between Prefill and Decode for your better understanding.

| Aspect | Prefill | Decode |
| --- | --- | --- |
| What it does | Processes the whole input prompt | Generates output tokens one by one |
| Parallelism | Parallel (all prompt tokens at once) | Sequential (one token at a time) |
| Steps | One big step | Many small steps (N of them) |
| Math shape | Big table times big table | Big table times a thin vector |
| Bottleneck | Compute-bound (limited by math speed) | Memory-bandwidth-bound (limited by data movement) |
| GPU utilization | High (math units busy, can approach 90 percent or more) | Low (math units mostly idle, around 20 to 40 percent) |
| KV cache action | Writes the cache | Reads and extends the cache |
| Latency metric | Time To First Token (TTFT) | Time Per Output Token (TPOT) |
| Cost driver | Grows with prompt length | Streams full weights plus KV cache every step |

This table sums up the whole story. Prefill and decode are mirror images of each other.

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

## Why this split matters: compute-bound vs memory-bound

Now, the question is: why do we care so much about this split into two phases?

The answer is that the two phases have opposite bottlenecks, and almost every optimization comes from this single fact. A bottleneck is the one slow part that holds back the whole process, like the narrow neck of a bottle that limits how fast water pours out.

Prefill is compute-bound. It does heavy math on many tokens at once, so it keeps the GPU's math units very busy. The work becomes large table-times-table multiplication, which GPUs love.

Decode is memory-bandwidth-bound. It does tiny math on one token, but it must stream the whole model plus the growing KV cache from memory at every step. So, the GPU spends most of its time waiting on memory, and the math units sit idle.

Here is a simple way to remember the difference. Prefill is like a chef chopping a whole pile of vegetables at once, where the hands are fully busy. Decode is like plating one finished dish at a time while walking to the fridge for every single dish, where the trips to the fridge are the slow part, not the plating.

Let's put the two phases side by side.

```
PREFILL (compute-bound)           DECODE (memory-bound)
many tokens processed at once     one token processed at a time

GPU math units: [#########-]      GPU math units: [##--------]
  about 90% busy                    about 20 to 40% busy

held back by: doing the MATH      held back by: MOVING DATA
                                  (model weights + KV cache)

```

Here, we can see the mirror image clearly. Prefill keeps the math units almost full, while decode leaves them mostly idle and waits on memory instead.

This single difference explains two big things.

First, it explains why long prompts make us wait longer before the answer starts. Long prompts mean more prefill math.

Second, it explains why we can serve many users at the same time during decode without much extra cost. Since one decode step barely uses the GPU's math, we can run many users' decode steps together. We will see this idea, called batching, in the optimization section.

[…905ln elided…]

Now, to understand why this is even possible, we must understand one thing about how an LLM writes text. Let's see that next.

### A quick recap of how an LLM generates text

To understand streaming, we must understand how a large language model writes its reply.

A large language model, or LLM, is the technology behind tools like ChatGPT and Claude. We give it some text, and it gives us back some text.

Here is the key thing to know. The model does not write the whole reply in one shot. It writes the reply one token at a time. A token is a small chunk of text, roughly a word or part of a word. For example, a short word like `cat` is usually one token, while a longer word like `running` is often split into two tokens.

How text is broken into these tokens is called tokenization, and we have a blog on Byte Pair Encoding (BPE) that explains how it works.

The model writes the first token, then looks at everything so far and writes the next token, then looks again and writes the next one, and so on. This way of writing, where each new token is produced based on all the tokens that came before it, is called autoregressive decoding.

Let's decompose it.

> Autoregressive = Auto + Regressive

In simple words, "auto" means it does this on its own, step by step, and "regressive" means each new step looks back at the steps that came before. So the model keeps looking back at what it has already written to decide the next word.

We can picture it as below:

```
Step 1:  The
Step 2:  The cat
Step 3:  The cat sat
Step 4:  The cat sat on
Step 5:  The cat sat on the
Step 6:  The cat sat on the mat

```

Here, we can see that the model produces one token at each step, and each step builds on the previous one. The full sentence is ready only at the last step.

This is the foundation we needed. Since the model is already producing the reply one token at a time, we have a choice. We can wait for all the tokens and send the full reply at the end, or we can send each token to the user the moment it is generated. Streaming is the second choice.

Not every model writes one token at a time, though. We have a detailed blog on Diffusion Language Models (DLMs) that explains how some models generate the whole sentence in parallel instead.

Now, the question is, why do we even want to send tokens one by one? Let's see.

### Why we need streaming at all

Let's understand the problem with sending the reply only at the end.

Suppose we ask the model to write a long answer of 500 tokens. If we wait for the whole reply, the user stares at a blank screen until all 500 tokens are produced. Producing 500 tokens takes time. So the user waits, sees nothing, and starts to feel that the app is stuck or broken.

This brings us to a very important idea called time to first token.

Time to first token is the time the user waits before seeing the very first piece of the reply on the screen.

In simple words, it is how long the user stares at nothing before words start showing up.

Without streaming, the time to first token is large, because the first word the user sees is actually the last word the model produces. The user has to wait for the entire answer.

With streaming, the time to first token is tiny. The very first token is sent the instant it is ready. The user starts reading immediately while the rest of the reply is still being written.

The time to first token is set mainly by the prefill phase, where the model reads the whole prompt before producing the first token. We have a detailed blog on Prefill vs Decode that explains this end to end.

Let's put the two side by side as below:

```
WITHOUT streaming:

  user asks  -->  [ model writes all 500 tokens ]  -->  full reply appears at once
                  user sees a blank screen this whole time (long wait)

WITH streaming:

  user asks  -->  token 1 appears  -->  token 2  -->  token 3  -->  ...  -->  done
                  user starts reading almost instantly (short wait)

```

Here, we can see that without streaming the user waits through the entire generation before seeing anything, while with streaming the user sees the first word almost immediately and keeps reading as more words arrive.

So, streaming gives us two big wins. The user sees words as they are generated, and the wait before the first word is very short. The app feels alive and fast. That's the beauty of streaming.

So, here comes SSE to the rescue. Now, the next big question is: how does the server actually push these tokens to the browser one by one? The answer is a technique called SSE. Let's understand it.

### What is SSE?

Now, it's time to learn about SSE, the technique that actually carries the tokens to the user.

SSE is a simple way for a server to keep sending new data to the browser over a single connection that stays open.

Let's decompose the term.

> SSE = Server-Sent Events

In simple words, the server is the computer that has the answer, the browser is the program in front of the user, and an event is just one small piece of data being sent. So "Server-Sent Events" literally means events that the server sends to the browser, on its own, one after another.

Before we go further, let's understand one normal idea first. Usually, on the web, the browser asks the server a question and the server gives back one answer, and then the conversation is over. The browser asks, the server replies, done. This is the request-response model.

But for streaming, one single reply at the end is not enough. We want the server to keep sending small pieces over time. SSE is built exactly for this. With SSE, the browser asks once, and then the server is allowed to keep sending piece after piece for as long as it wants, all over that same single connection.

Let's put the two models side by side as below:

```
NORMAL request-response:

  browser  --- asks once --->  server
  browser  <-- one reply ----  server
  (connection closed, conversation over)

SSE (Server-Sent Events):

  browser  --- asks once --->  server
  browser  <-- piece 1 ------  server
  browser  <-- piece 2 ------  server
  browser  <-- piece 3 ------  server
  (connection stays open, server keeps sending)

```

Here, we can see that in the normal model the browser asks once and gets back a single reply, and then the connection is closed. In the SSE model the browser still asks only once, but the server keeps sending piece after piece over the same connection that stays open.

So, SSE is the channel through which the tokens flow from the server to the browser, one event at a time.

Now, to make this work, two things must be set up correctly. The connection must stay open, and the data must be sent in a special format. Let's understand both, starting with the open connection.

### How the HTTP connection stays open

Let's understand the connection first.

When the browser talks to a server on the web, it uses HTTP. HTTP is simply the set of rules that browsers and servers follow to talk to each other. Every time we open a website, HTTP is being used behind the scenes.

Normally, the flow is short. The browser opens a connection, sends a request, the server sends back the full response, and then the connection is closed. It is like making one phone call, getting one answer, and hanging up.

For streaming, we do not want to hang up after one answer. We want to keep the line open so the server can keep talking. It is like making one phone call and staying on the line while the other person reads out a long message to us, sentence by sentence.

With SSE, the HTTP connection is opened once and kept open. The server holds the line and keeps pushing new pieces of data through it until the reply is complete.

So, the browser opens one connection, and that single connection stays alive for the entire reply. The server does not close it after the first token. It sends token 1, keeps the line open, sends token 2, keeps it open, and so on.

How does the server tell the browser "this is going to be a stream, do not expect just one answer"? It does this using something called the Content-Type.

The Content-Type is a small label the server attaches to its response to say what kind of data is coming. For example, a normal web page has the Content-Type `text/html`. A normal data response often has `application/json`.

For SSE, the server sets the Content-Type to a special value as below:

```
Content-Type: text/event-stream

```

Here, we can see the value is `text/event-stream`. The word `stream` is the important part. This label tells the browser, "Do not wait for one complete answer. Keep this connection open and read the pieces as they arrive." The browser sees this label and switches into streaming mode.

So, the open connection plus the `text/event-stream` label together set the stage. Now the server can start pushing data. But the data must be sent in a specific shape so the browser can read it correctly. Let's understand that shape next.

### The format of a streamed message

Now, let's understand how each piece of data is actually written when the server sends it.

SSE uses a very simple text format. Each piece of data is sent as a line that starts with the word `data:`, followed by the actual content. After each piece, the server sends a blank line to mark the end of that piece.

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

So the rule is simple.

Each event is a line starting with `data:`, and each event is separated from the next one by a blank line.

Let's see what the server sends when the model produces the words "The cat sat". The raw stream looks like below:

```
data: The

data: cat

data: sat

```

Here, we can see three events. The first event carries the word `The`, the second carries `cat`, and the third carries `sat`. Notice the blank line after each one. That blank line is how the browser knows where one event ends and the next one begins.

In real systems, the content after `data:` is usually not a plain word but a small piece of structured data called JSON, which holds the token along with a little extra information. For the sake of understanding, we are keeping it as plain words here so the idea is crystal clear. The important point stays the same. Every token is wrapped in a `data:` line and followed by a blank line.

So, this simple format is the language the server and browser agree to speak. Every token travels as one `data:` line.

Now we have all the pieces. We know the connection stays open, we know the Content-Type, and we know the format. Let's put it all together in a full walkthrough.

### A full walkthrough from server to screen

Let's walk through the entire journey of a streamed reply, from the moment the user asks to the moment words fill the screen. Suppose the user asks a question and the model is about to reply with "The cat sat".

Step 1: The browser opens one HTTP connection to the server and sends the user's question. This connection will stay open for the whole reply.

Step 2: The server starts the response and sets the Content-Type to `text/event-stream`. This tells the browser that a stream is coming and the connection must stay open.

Step 3: The model produces its first token, `The`, using autoregressive decoding, which we learned means producing one token at a time while looking back at what came before. The server does not wait. It immediately wraps this token in a `data:` line and pushes it through the open connection.

Step 4: The browser reads that `data:` line, takes out the word `The`, and appends it to the screen. The user sees the first word almost instantly. This is the small time to first token we wanted.

Step 5: The model produces the next token, `cat`. The server pushes it as another `data:` line. The browser appends `cat` to the screen, right after `The`. The user now sees "The cat".

Step 6: The model produces `sat`. The server pushes it, and the browser appends it. The user now sees "The cat sat", and the whole thing looks like it is being typed live.

Let's see the whole flow in one diagram as below:

```
   MODEL                 SERVER                         BROWSER (screen)
   -----                 ------                         ----------------
   token "The"   --->    data: The      ---[open]--->   The
   token "cat"   --->    data: cat      ---[open]--->   The cat
   token "sat"   --->    data: sat      ---[open]--->   The cat sat
                         data: [DONE]   ---[open]--->   (stop, close)

```

Here, we can see that each token travels from the model, to the server, through the single open connection, and onto the screen, one at a time. The connection stays open the whole way down, which is why the server can keep pushing without reopening anything. The browser appends each new piece to what is already on the screen, and this constant appending is what creates the live typing effect.

The problem is solved. The user reads the reply as it is being written, instead of waiting for the full answer.

But there is one last thing. The server needs a way to say, "I am finished, there are no more tokens." Let's see how it does that.

### The [DONE] marker that ends the stream

Now, here is a small but important question. The connection is open and tokens are flowing. How does the browser know when the reply is complete and it can stop listening?

The answer is a special final message called the [DONE] marker.

After the very last token, the server sends one final event that contains `[DONE]`. This is a signal that means the stream is over.

In simple words, `[DONE]` is the server saying "that was the last piece, you can stop now."

The end of the stream looks like below:

```
data: sat

data: [DONE]

```

Here, we can see that after the last real token `sat`, the server sends one more event with `[DONE]`. The browser reads this, understands that no more tokens are coming, stops listening, and the connection is closed.

So, the `[DONE]` marker is the clean ending of the stream. Without it, the browser would not know whether the reply is finished or whether the next token is still on its way.

This is how the full streaming cycle begins, runs, and ends. Now, let's compare SSE with another technology people often confuse it with.

### SSE vs WebSockets

When we talk about a server sending live data, many people immediately think of WebSockets. So let's understand the difference, because choosing the right tool matters.

A WebSocket is a technology that opens a two-way connection between the browser and the server. Over that connection, both sides can send messages to each other at any time, freely, in both directions.

SSE is different. SSE is one-way only, from the server to the browser. The server can keep pushing data to the browser, but the browser cannot send messages back over that same SSE stream.

Now, the natural question is, if WebSockets can do two-way and SSE can only do one-way, why use SSE at all?

The answer is that for token streaming, we do not need two-way traffic during the reply. The browser asks its question once at the start, and after that it only needs to receive tokens. The whole job is the server pushing data to the browser. That is exactly the one-way job SSE is built for.

And SSE is much simpler. Let me tabulate the differences between SSE and WebSockets for your better understanding so that you can decide which one to use based on your use case.

| Point | SSE (Server-Sent Events) | WebSockets |
| --- | --- | --- |
| Direction | One-way, server to browser only | Two-way, both sides can send |
| Built on | Plain HTTP | A separate set of rules added on top of HTTP |
| Setup | Simple, uses normal HTTP | More complex |
| Best for | Streaming a reply, live updates | Chat rooms, games, live collaboration |
| Reconnect | Reconnects automatically | We handle reconnection ourselves |

Here, we can see that SSE runs over plain HTTP, which means it uses the same simple web rules we already use everywhere, with nothing extra to set up. WebSockets need a separate, more complex setup because they support full two-way traffic.

So, for token streaming, where the server simply needs to push tokens to the browser, SSE is the simpler and very natural fit. We use WebSockets when we genuinely need both sides to talk freely at the same time, like in a live chat room or a multiplayer game.

So, now we know when to use which one.

### Token streaming in the real world

Now, let's see where token streaming is used in real systems.

The most familiar example is right in front of us. When we use ChatGPT or Claude and watch the reply appear word by word, like it is being typed live, that is token streaming over SSE. The server is producing tokens one at a time with autoregressive decoding, wrapping each one in a `data:` line, and pushing it through a single open `text/event-stream` connection. The browser appends each piece to the screen, and we get that smooth typing effect.

Behind these streamed replies sits a serving engine that has to produce those tokens fast and serve many users at once. We have a detailed blog on vLLM that explains how high-throughput LLM serving works.

This is not just a nice visual trick. It is a real improvement to the experience. The user sees that the system is working, starts reading right away, and never sits in front of a frozen blank screen. The time to first token is tiny, so the whole app feels fast and responsive.

The same pattern is used far beyond chat windows. Any application built on top of an LLM, such as a coding assistant that writes code as we watch, a writing tool that drafts text live, or a customer support bot that types out its answer, uses this exact streaming approach to feel quick and alive.

So, anywhere a model produces a reply and we want the user to start reading it immediately, token streaming over SSE is the technique that makes it happen.

To learn how to build and serve LLM-powered apps like these - Model Deployment and Serving, AI and ML System Design, and building ChatGPT from scratch - check out our AI and Machine Learning Program at Outcome School.

This is how token streaming over SSE works. The model produces the reply one token at a time, the server keeps a single HTTP connection open with the Content-Type `text/event-stream`, it pushes each token the moment it is ready as a `data:` line followed by a blank line, the browser appends each piece to the screen to create the live typing effect, and a final `[DONE]` marker tells the browser the reply is complete.

### Does token streaming change how the model generates the reply?

No. The model still writes the reply one token at a time using autoregressive decoding. Streaming only changes when each token is sent to the user. Instead of waiting for all the tokens, the server sends each token the moment it is generated, so the time to first token becomes tiny.

### Is each streamed piece a plain word?

Usually not. In real systems, the content after `data:` is usually a small piece of structured data called JSON. It holds the token along with a little extra information. The rule stays the same, as every token is wrapped in a `data:` line and followed by a blank line.

### What would happen if the server did not send the [DONE] marker?

The browser would not know whether the reply is finished or whether the next token is still on its way. The `[DONE]` marker is the clean ending of the stream. When the browser reads it, it stops listening, and the connection is closed.

### Does SSE reconnect automatically if the connection drops?

Yes. SSE reconnects automatically, while with WebSockets we have to handle reconnection ourselves. SSE is also built on plain HTTP, so it is simpler to set up.

### Is token streaming used only in chat apps?

No. Any application built on top of an LLM can use it. A coding assistant that writes code as we watch, a writing tool that drafts text live, or a customer support bot that types out its answer all use the same streaming approach to feel quick and alive.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-291 and 1197-1524 of 1524; 905 middle lines (55.7KB) elided. Read artifact://63 for full output]
