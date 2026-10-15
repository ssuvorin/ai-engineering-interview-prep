> Source: https://outcomeschool.com/blog/prefill-decode-disaggregation

# What is Prefill-Decode Disaggregation in LLM Inference?
URL: https://outcomeschool.com/blog/prefill-decode-disaggregation
Published: 2026-09-13
Author: Amit Shekhar

What is Prefill-Decode Disaggregation in LLM Inference?

# What is Prefill-Decode Disaggregation in LLM Inference?

Authors
: - Name
: Amit Shekhar
Published on
: September 13, 2026

Prefill-Decode Disaggregation is a way of running a large language model where the reading of the prompt (prefill) and the writing of the answer (decode) happen on separate machines, so that each one can be tuned for its own job.

In this blog, we will learn about Prefill-Decode Disaggregation, a way of running a large language model where the reading of the prompt and the writing of the answer happen on separate machines. We will also see how an LLM answers a request in two phases, what the KV Cache is, why the two phases need different things from the hardware, what goes wrong when both run on the same machine, how disaggregation solves it step by step, its advantages and disadvantages, and where it works well and where it is overkill.

We will cover the following:

- How an LLM answers a request
- What is the KV Cache?
- Prefill is compute-heavy, Decode is memory-heavy
- The problem when both run on the same GPU
- TTFT vs TPOT
- The naive approaches and their issues
- What is Prefill-Decode Disaggregation?
- How Prefill-Decode Disaggregation works
- Walkthrough of one request
- Advantages of Prefill-Decode Disaggregation
- Disadvantages of Prefill-Decode Disaggregation
- Where it works well and where it is overkill
- Co-located vs Disaggregated serving

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## How an LLM answers a request

Let's start from the very beginning.

An LLM (Large Language Model) is an AI model that reads text and writes text. When we type a question in a chat app, the LLM reads our question and writes an answer, one small piece at a time.

These small pieces are called tokens. A token is a word or a part of a word. For the sake of understanding, we can think of a token as a word.

Now, here is the important part. The LLM does not answer a request in one shot. It answers in two phases.

Phase 1: Prefill

In the prefill phase, the LLM reads the complete prompt at once. The prompt is everything we sent to the model, our question, the previous chat messages, and any instructions. The model processes all these tokens together in one go and produces the very first token of the answer.

It is called prefill because the model fills up its memory with the prompt before it starts writing. We will see this memory in the next section.

Phase 2: Decode

In the decode phase, the LLM writes the answer one token at a time. It takes everything it has seen so far, produces the next token, adds it to the answer, and repeats. This continues until the answer is complete.

This is why we see the answer appearing word by word in a chat app. Each token is shown to us as soon as it is ready. This is called streaming.

So, Prefill = read the whole prompt at once, and Decode = write the answer one token at a time.

Let's say our question is "What is the capital of India?" and we send it to the model. In the prefill phase, the model reads all the words of the question together. In the decode phase, it writes "The", then "capital", then "of", then "India", then "is", then "New", then "Delhi". One token per step.

This is how an LLM answers a request.

We have a detailed blog on Prefill vs Decode that explains these two phases in depth.

## What is the KV Cache?

Before jumping into the problem, we must know about the KV Cache, because the whole idea of disaggregation depends on it.

When the model reads the prompt in the prefill phase, it does a lot of calculation for every token. It figures out how each token is related to every other token. Now, in the decode phase, for every new token, the model needs this same information again. If it repeats the whole calculation for every new token, it will be very slow.

Here comes the KV Cache into the picture.

KV Cache is the memory where the model keeps the notes it made while reading the prompt, so that it does not have to read the prompt again for every new token.

In simple words, KV Cache = Notes.

Let's say we are reading a long book to answer questions on it. If we make notes while reading, we can answer every question by looking at the notes. We do not need to read the whole book again for every question. The KV Cache is exactly these notes.

The letters K and V stand for Key and Value. These are the two things the model stores for every token. Do not worry, we do not need to go deeper than that for this blog. Just remember: KV Cache is the notes the model makes during prefill, and it reads those notes during decode.

Note: The KV Cache is big. For a long prompt, it can take many gigabytes of memory. Keep this in mind, it will matter later.

## Prefill is compute-heavy, Decode is memory-heavy

Now, let's understand why these two phases are so different from each other.

The best way to learn this is by taking an example.

Consider a chef in a kitchen. A customer hands over a long recipe of ten pages.

First, the chef reads the entire recipe in one sitting and makes short notes. This needs a lot of thinking and focus, but very less walking around. The chef is sitting at one place and processing a lot of information. This is the prefill phase, and the notes are the KV Cache. It needs a lot of brain power.

Then, the chef starts cooking, step by step. Add salt, stir, wait, add oil, stir, wait. Each step is small and simple. But for each step, the chef walks to the shelf, looks at the notes, comes back, and does one small thing. Most of the time is spent walking to the shelf and back, not in the actual cooking. This is the decode phase. It needs very less brain power per step, but a lot of moving things around.

Now, let's map this to the GPU.

A GPU is the special chip that runs the LLM. It has two important parts, the compute units which do the maths, and the memory which stores the data.

Prefill is compute-heavy. The model processes thousands of prompt tokens at the same time. The compute units are fully busy doing the maths. The GPU is working at its full power.

Decode is memory-heavy. The model produces only one token per step. The maths for one token is very less. But for every single step, the GPU must read the entire model (billions of numbers that the model has learned, called weights) and the entire KV Cache from the memory. So, the compute units sit mostly idle, waiting for the data to arrive from the memory.

So, prefill keeps the GPU compute busy. Decode keeps the GPU memory busy. They stress two completely different parts of the same chip.

In simple words, prefill is limited by how fast the GPU can think, and decode is limited by how fast the GPU can fetch data from its memory.

This is the key insight of this whole blog. Keep it in mind.

To learn LLM Inference Bottleneck Analysis and the KV Cache from the ground up, check out our AI and Machine Learning Program at Outcome School.

## The problem when both run on the same GPU

Now, let's see what happens in the normal setup.

In the normal setup, one GPU does both prefill and decode for every request. This is called co-located serving because both phases are located on the same GPU.

Let's say our server is serving many users at the same time. To do this efficiently, the GPU handles many requests together in one go instead of one by one. This is called batching.

Suppose ten users are in the middle of the decode phase. Their answers are being written one token at a time. Everything is smooth.

Now, an eleventh user sends a very long prompt, let's say a document of ten thousand tokens.

The GPU has to do a big prefill for this new user. This prefill is compute-heavy and takes a long time, say one full second.

But, here is the catch.

While the GPU is busy with this big prefill, the other ten users are waiting. Their next token does not come. Their answer freezes for one second in the middle of a sentence. Then it continues. Then another long prompt arrives and it freezes again.

This is called generation stall or interference. One user's prefill stalls the decode of everyone else.

The waiting time that a user experiences is called latency. Every time a long prompt arrives, the latency of everyone else spikes.

The reverse is also true. If the GPU is busy decoding for many users, a new user's prefill has to wait, and the first token of their answer arrives late.

So, the two phases keep fighting for the same GPU, and both of them lose.

## TTFT vs TPOT

To measure this problem properly, we need two simple terms.

TTFT (Time To First Token) is the time from when the user presses enter till the first token of the answer appears on the screen. This is mostly decided by the prefill phase.

TPOT (Time Per Output Token) is the time between one token and the next token while the answer is being written. This is decided by the decode phase.

In simple words, TTFT is how long we wait before the answer starts, and TPOT is how smoothly the answer flows once it starts.

For example, let's say TTFT is 500 milliseconds and TPOT is 30 milliseconds. Means, the answer starts in half a second, and after that around 30 tokens appear every second.

For a good user experience, we want both to be low. We want the answer to start quickly and flow smoothly.

But, in co-located serving, if we optimize for one, the other gets worse. If we give priority to prefill, TTFT becomes good but TPOT becomes bad because decode gets stalled. If we give priority to decode, TPOT becomes good but TTFT becomes bad because new users wait longer.

We needed a solution for that.

## The naive approaches and their issues

Approach 1: Add more GPUs and let each GPU do both phases

The simplest idea is to buy more GPUs. Each GPU does both prefill and decode, just like before, but now we have more of them, so the load per GPU goes down.

The issue with this approach is that the interference does not go away. Every GPU still has the same fight between prefill and decode inside it. We have only made the fight happen less often, at a very high cost. Also, we cannot tune the hardware for one phase, because every GPU must be good at both. Let's see how the next approach solve this issue.

Approach 2: Chunked prefill

Another idea is to break a long prefill into small chunks and mix a small chunk of prefill with the decode steps in every batch. This way, no single prefill blocks the decode for a long time.

This helps. It is used in many real systems. But the issue with this approach is that prefill and decode still share the same GPU. Every decode step now carries some extra prefill work, so TPOT increases a little for everyone. And the prefill takes longer to finish because it is done in pieces, so TTFT also increases. We have spread the pain instead of removing it.

Let's see how the next approach solve this issue.

## What is Prefill-Decode Disaggregation?

So, here comes Prefill-Decode Disaggregation to the rescue.

Let's break the name.

Prefill-Decode Disaggregation = Prefill + Decode + Disaggregation

- Prefill: the phase where the model reads the prompt.
- Decode: the phase where the model writes the answer.
- Disaggregation: a big word that simply means separating things that were joined together. Aggregation means joining. Disaggregation means un-joining.

So, Prefill-Decode Disaggregation is the technique of running the prefill phase and the decode phase on separate GPUs, so that they never fight for the same hardware.

In simple words, we have one group of GPUs whose only job is to read prompts, and another group of GPUs whose only job is to write answers.

Let's go back to our kitchen. Instead of one chef who reads the recipe and also cooks, we now have a reader who reads the recipe and makes the notes, and a cook who takes the notes and cooks. The reader never stops reading to cook. The cook never stops cooking to read. Both do one thing and do it well.

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

## How Prefill-Decode Disaggregation works

Now that we have learned what Prefill-Decode Disaggregation is, it's time to learn how it works.

There are four main parts in this setup.

Router: This is a small program that receives every request and decides which prefill worker and which decode worker will handle it.

Prefill workers: These are GPUs that only do prefill. They receive the prompt, process all the tokens at once, produce the first token, and build the KV Cache. They are tuned for heavy compute.

Decode workers: These are GPUs that only do decode. They receive the KV Cache, and generate the answer one token at a time. They are tuned for fast memory access and can serve many users at once.

KV Cache transfer: This is the bridge between the two. After the prefill worker builds the KV Cache, it sends the KV Cache to the decode worker over the network. The decode worker loads it into its own memory and continues from there.

We can write the flow as below:

```
Request
   |
   v
[Router] --> picks a Prefill worker and a Decode worker
   |
   v
[Prefill worker] --> reads the full prompt
                 --> builds the KV Cache
                 --> produces the first token
   |
   v  (KV Cache is sent over the network)
   |
[Decode worker]  --> loads the KV Cache
                 --> writes token 2, token 3, token 4 ...
   |
   v
Answer streamed to the user

```

Here, we have a router that decides which prefill worker and which decode worker will handle the request. The prefill worker does the heavy reading and hands over the notes. The decode worker does the light but repeated writing. The KV Cache transfer is the hand-over of the notes from the reader to the cook.

We can also write the same flow as a simple pseudo code as below:

```python
def handle_request(prompt):
    prefill_worker = pick_prefill_worker()
    decode_worker = pick_decode_worker()

    # Phase 1: Prefill on the prefill worker
    first_token, kv_cache = prefill_worker.prefill(prompt)
    send_to_user(first_token)

    # Hand-over: KV Cache goes over the network
    decode_worker.load(kv_cache)

    # Phase 2: Decode on the decode worker
    while not finished:
        next_token = decode_worker.decode_step()
        send_to_user(next_token)

```

Here, we have a function `handle_request` that takes the prompt. It picks one prefill worker and one decode worker. The prefill worker reads the prompt and returns the first token along with the KV Cache. We send the first token to the user right away. Then, the KV Cache is loaded into the decode worker, which means it travels over the network. After that, the decode worker keeps producing the next token in a loop till the answer is finished, and each token is sent to the user as soon as it is ready.

Note: The KV Cache transfer must be fast. If the transfer is slow, we lose all the benefit. So, real systems use very fast connections between the GPUs, like NVLink, InfiniBand, or RDMA, which are simply very fast cables and protocols that copy memory from one machine to another with very less delay. This fast connection between the machines is called the interconnect.

Serving systems like SGLang support this setup out of the box. We have a detailed blog on how SGLang works that covers this end to end.

## Walkthrough of one request

Let's take one complete request and see what happens at each step, with example numbers just for the sake of understanding.

Suppose a user sends a prompt of 4000 tokens and the answer will be 200 tokens long.

Step 1: The request arrives at the router. The router looks at the prefill workers and picks the one with the least load. It also reserves a slot on a decode worker.

Step 2: Prefill worker reads the prompt. All 4000 tokens are processed together. The compute units run at full power. This takes, say, 400 milliseconds. At the end, we have the first token of the answer and a KV Cache of, say, 2 GB.

Step 3: The first token is sent to the user. The user sees the answer start. Our TTFT is around 400 milliseconds.

Step 4: The KV Cache is transferred. The 2 GB KV Cache is copied over the fast network to the decode worker. With a fast interconnect, this takes, say, 20 to 50 milliseconds. Real systems often start this transfer in pieces while the prefill is still running, so that the wait is hidden.

Step 5: Decode worker takes over. It loads the KV Cache and starts producing token 2, token 3, and so on. Each token takes, say, 20 milliseconds. So, our TPOT is 20 milliseconds, and the 200 tokens take about 4 seconds.

Step 6: The prefill worker is already free. Once the prefill worker handed over the KV Cache, it moved on to the next user's prompt. It never waited for the decode of this user.

Step 7: The decode worker is never interrupted. While it is writing this user's answer, no big prefill comes and stalls it, because prefills do not happen on this GPU at all.

So, the user got a quick start (low TTFT) and a smooth flow (low TPOT), both at the same time. That's the beauty of Prefill-Decode Disaggregation.

The problem is solved.

This was all about how it works. Now, let's see its advantages and disadvantages.

## Advantages of Prefill-Decode Disaggregation

Independent scaling: If our users send very long prompts but want short answers, we add more prefill workers. If our users send short prompts but want long answers, we add more decode workers. We scale each phase based on our use case, not both together.

No interference: A long prefill from one user can never stall the decode of another user. TTFT and TPOT can both be tuned separately.

Different hardware per phase: Prefill workers can use GPUs with the strongest compute. Decode workers can use GPUs with faster and bigger memory, which are often cheaper. We are not forced to buy one expensive GPU that is good at everything.

Better batching: Decode workers can pack many users into one big batch, because all of them are doing the same small step. This makes the memory reads more efficient and the cost per token goes down.

Predictable latency: Because the two phases do not fight, the response time becomes stable. Users do not see random freezes in the middle of an answer.

## Disadvantages of Prefill-Decode Disaggregation

KV Cache transfer cost: The KV Cache must be moved over the network for every request. For long prompts, this is gigabytes of data. Without a fast interconnect, this transfer can take longer than the benefit we gained.

Needs fast interconnect: This technique needs high speed connections like NVLink or InfiniBand between the machines. Normal networks are too slow. This adds cost.

More complexity: Now we have a router, two kinds of workers, a transfer system, and failure handling for each of them. If a decode worker crashes mid-answer, the KV Cache is lost and the request must be redone. Building and operating this is much harder than one GPU doing everything.

Idle capacity: If at some moment there are no long prompts, the prefill workers sit idle while the decode workers are overloaded, or the other way round. We must monitor the traffic and balance the workers.

Overkill for small scale: If we are serving a small number of users, all of this machinery is not worth the effort.

If we want to go deep into LLM Inference Engineering, Model Deployment and Serving, and how to design an LLM Inference Platform (vLLM-as-a-Service), we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Where it works well and where it is overkill

It works well when:

[…510ln elided…]

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

[Showing lines 1-336 and 847-1174 of 1174; 510 middle lines (31.0KB) elided. Read artifact://87 for full output]
