> Source: https://outcomeschool.com/blog/how-does-token-streaming-work

# How does Token Streaming work?
URL: https://outcomeschool.com/blog/how-does-token-streaming-work
Published: 2026-06-10

How does Token Streaming work?

# How does Token Streaming work?

Authors
: - Name
: Amit Shekhar
Published on
: June 9, 2026

Token Streaming is a technique where the server sends the model's reply to us piece by piece, as each piece is produced, instead of waiting for the whole reply to be ready.

In this blog, we will learn about how Token Streaming works. We will also see why we need it, how the server and the browser talk to each other to make it happen, and where it is used in real systems like ChatGPT and Claude.

We will cover the following:

- What is token streaming?
- A quick recap of how an LLM generates text
- Why we need streaming at all
- What is SSE?
- How the HTTP connection stays open
- The format of a streamed message
- A full walkthrough from server to screen
- The [DONE] marker that ends the stream
- SSE vs WebSockets
- Token streaming in the real world

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is token streaming?

Before we talk about how it works, we must first understand what token streaming is.

Token streaming is a technique where the server sends the model's reply to us piece by piece, as each piece is produced, instead of waiting for the whole reply to be ready.

In simple words, streaming means we start receiving the answer while it is still being written, not after it is fully finished.

Let's say we ask ChatGPT a question. We have all seen the words appear on the screen one small chunk at a time, like someone is typing the answer live. That live typing effect is token streaming in action.

So, token streaming is the model handing us the reply gradually, word by word, the moment each word is ready.

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
