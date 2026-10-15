> Source: https://outcomeschool.com/blog/design-a-real-time-voice-ai-agent

# Design a Real-Time Voice AI Agent
URL: https://outcomeschool.com/blog/design-a-real-time-voice-ai-agent
Published: 2026-09-16

Design a Real-Time Voice AI Agent

# Design a Real-Time Voice AI Agent

Authors
: - Name
: Amit Shekhar
Published on
: September 15, 2026

A Real-Time Voice AI Agent is a system that listens to a person speaking, understands what they said, thinks about it, takes actions if needed, and talks back in a natural human-like voice, all within a fraction of a second.

In this blog, we will learn about how to design a Real-Time Voice AI Agent, a system that listens to a person speaking, understands what they said, thinks about it, takes actions if needed, and talks back in a natural human-like voice, all within a fraction of a second. We will also see why voice is much harder than a text chatbot, the two big ways to build it (the cascaded pipeline of Speech-to-Text, LLM, and Text-to-Speech versus the end-to-end Speech-to-Speech model), how the agent knows when the user has stopped talking, how we handle interruptions, how tools and memory fit in, how we scale it to thousands of calls, the edge cases that break a voice agent in production, the pros and cons of every approach, and when to use which one.

We will cover the following:

- What is a Voice AI Agent?
- Why is Real-Time Voice hard?
- Requirements
- Back-of-the-envelope estimation
- High-Level Architecture
- Component 1: Audio Transport
- Component 2: Voice Activity Detection and Turn Detection
- Component 3: Speech-to-Text (STT)
- Component 4: The Brain - LLM with Tools
- Component 5: Text-to-Speech (TTS)
- Approach 1: Cascaded Pipeline (STT -> LLM -> TTS)
- Approach 2: Speech-to-Speech Model
- Approach 3: Hybrid Approach
- Cascaded vs Speech-to-Speech: Comparison
- Latency Budget: Where every millisecond goes
- Handling Interruptions (Barge-in)
- Tool Calling in a Voice Agent
- Memory and Context
- Telephony: Connecting to real phone calls
- Scaling the system
- Edge Cases and how to handle them
- Observability and Evaluation
- Safety, Security, and Privacy
- Cost
- How to present this design in an interview

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a Voice AI Agent?

A Voice AI Agent is a software program that we can talk to using our voice, and it talks back to us, just like a phone call with a human, but the one on the other side is an AI.

Let's break the term down.

Voice AI Agent = Voice + AI + Agent

- Voice: The input and the output are sound. We speak, and it speaks. No typing, no reading.
- AI: The understanding and the thinking is done by an AI model, mainly a Large Language Model (LLM). An LLM is a model trained on a huge amount of text so that it can understand language and generate a sensible reply.
- Agent: It does not just chat. It can take actions like looking up your order, booking an appointment, cancelling a subscription, or transferring the call to a human. It does this by calling tools, which we will learn about later.

A few real examples of a Voice AI Agent:

- A customer support line where you call and say "Where is my order?" and the agent checks and tells you.
- A restaurant booking agent that takes reservations over the phone.
- A drive-thru agent that takes your food order.
- A language tutor in an app that talks with you to practice English.
- An outbound agent that calls customers to remind them about an appointment.

Now, what does Real-Time mean here?

In a normal human conversation, when one person stops speaking, the other person replies within about 200 to 500 milliseconds. A millisecond is one-thousandth of a second, so 500 milliseconds is half a second. This gap feels natural to us.

If the reply takes more than one second, it starts to feel slow. If it takes more than two or three seconds, people say "Hello? Are you there?" and the whole experience is broken.

So, Real-Time means the agent must reply fast enough that the conversation feels like talking to a human. Our target is that the agent starts speaking within about 800 milliseconds after the user stops speaking. This single number will drive most of our design decisions.

## Why is Real-Time Voice hard?

We all must be knowing about text chatbots. The user types a message, presses Enter, and the chatbot replies. Building a voice agent looks like just adding a microphone and a speaker to that chatbot. But, here is the catch. Voice brings many new problems that text never had.

Problem 1: Nobody presses Enter.

In a text chatbot, we know exactly when the user has finished, because they press Enter. In voice, there is no Enter key. The user just stops speaking. But a pause can mean "I am done" or "I am thinking about what to say next". The agent has to guess. Guess too early, and it cuts off the user. Guess too late, and it feels slow.

Problem 2: The time budget is tiny.

A text chatbot can take two to three seconds to reply and nobody complains. A voice agent has less than one second. And, in that one second, we have to convert speech to text, think with an LLM, convert text back to speech, and send the audio over the network. Every step eats into the budget.

Problem 3: Users interrupt.

Humans interrupt each other all the time. If the agent is reading a long answer and the user says "No, wait, I meant the other order", the agent must stop talking immediately and listen. A text chatbot never has this problem.

Problem 4: Audio is messy.

Text is clean. Audio has background noise, a TV playing, a child crying, a bad phone line, accents, people speaking too fast, people mumbling, two people talking at once. Every one of these can confuse the system.

Problem 5: Speech has no punctuation or spelling.

When someone says "my order id is A B one two three", the system has to figure out if it is "AB123" or "A B 1 2 3" or "Abe one two three". Names, numbers, emails, and codes are very hard in voice.

Problem 6: The output must sound human.

The agent must not only say the right words, it must say them with the right rhythm, pauses, and tone. A robotic voice reading "forty-five dollars point five zero" instead of "forty-five dollars and fifty cents" sounds wrong.

Problem 7: Everything is a continuous stream.

In text, one message is one request. In voice, audio is flowing in and flowing out continuously during the whole call. We must handle it as a stream, not as a request and response.

So, a Voice AI Agent is not "a chatbot with a microphone". It is a real-time streaming system with a strict time budget. Now that we know why it is hard, let's define what exactly we are building.

## Requirements

In a system design interview, we must always start by clarifying the requirements. Let's do that.

### Functional Requirements

- The user speaks, and the agent listens, understands, and replies by voice.
- The agent holds a multi-turn conversation, which means it remembers what was said earlier in the same call.
- The agent can take actions using tools, like looking up an order, booking a slot, or sending a confirmation message.
- The user can interrupt the agent while it is speaking, and the agent must stop and listen.
- The agent works over a normal phone call and also inside a mobile app or a web browser.
- The agent can transfer the call to a human when needed.
- The agent supports multiple languages (we can keep this as a stretch goal).

### Non-Functional Requirements

- Latency: The agent must start speaking within 800 milliseconds after the user stops speaking, and never more than 1.5 seconds.
- Availability: The system must be up 99.9% of the time or more. A dropped call is a very bad experience.
- Scalability: The system must handle thousands of calls at the same time.
- Reliability: The agent must never leave a sentence half-finished or go silent without reason.
- Cost: The cost per minute of the call must be low enough to make business sense.
- Privacy and Security: Voice is personal data. Recordings and transcripts must be protected.
- Observability: We must be able to see what happened in every call, step by step, to debug and improve.

### The most important metric

For a voice agent, the most important metric is Voice-to-Voice Latency.

Voice-to-Voice Latency is the time between the moment the user stops speaking and the moment the user hears the first sound of the agent's reply.

We will keep coming back to this number. Everything we design is to keep this number small while keeping the answer correct.

## Back-of-the-envelope estimation

Let's do some simple math to understand the scale. Let say we are designing this for a company that gets 1 million calls per day, with an average call length of 5 minutes.

Concurrent calls:

1 million calls per day is around 12 calls per second on average. Each call lasts 5 minutes, which is 300 seconds. So, at any moment, around 12 x 300 = 3,600 calls are going on. Calls are not spread evenly across the day, so at peak, we can assume 3 times that, around 10,000 concurrent calls.

Audio bandwidth:

Sound is captured as numbers. A phone call is usually captured 8,000 times per second (we call it 8 kHz sample rate). A good quality voice for AI models is 16,000 times per second (16 kHz). Each number is stored in 2 bytes.

So, 16 kHz audio = 16,000 x 2 bytes = 32,000 bytes per second = 256 kilobits per second (kbps) in raw form. This raw form is called PCM (Pulse Code Modulation).

We do not send raw audio over the network. We compress it using a codec (a program that shrinks audio). A common codec called Opus can bring it down to around 32 kbps with good quality. Phone networks use a codec called G.711 at 64 kbps.

For 10,000 concurrent calls, with audio going both ways: 10,000 x 2 x 64 kbps = 1.28 Gbps (gigabits per second). This is easily handled by modern servers.

Storage for recordings:

1 million calls x 5 minutes = 5 million call-minutes per day. One minute of Opus audio at 32 kbps is around 240 KB. So, 5 million x 240 KB = 1.2 TB per day if we record every call. Transcripts are text and are tiny in comparison, a 5-minute call is around 5 to 10 KB of text.

Compute:

This is the real bottleneck. Every concurrent call needs:

- One streaming Speech-to-Text session
- One LLM session generating tokens
- One streaming Text-to-Speech session

All three run on GPUs, the special processors that run AI models. So, for 10,000 concurrent calls, we need a large GPU fleet, and our cost is mainly GPU cost. This is why we will care a lot about using small and fast models wherever possible.

Now, we have a feel of the scale. Let's move to the architecture.

## High-Level Architecture

The best way to learn this is by taking an example. Let's say a user calls our support number and says, "Where is my order 4 5 6 7 8?"

Here is what must happen:

- Step 1: The user's voice is captured and streamed to our server as small audio chunks.
- Step 2: The system detects that the user is speaking, and later detects that the user has stopped.
- Step 3: The audio is converted to text: "Where is my order 45678?"
- Step 4: The LLM reads the text, decides it needs to look up the order, calls the `get_order_status` tool, gets the result, and writes a reply: "Your order 45678 was shipped yesterday and will arrive tomorrow."
- Step 5: The reply text is converted to speech.
- Step 6: The speech audio is streamed back to the user.

Let's see the high-level architecture as below:

```
   User (Phone / Mobile App / Browser)
                 |
                 |  audio stream in both directions
                 |  (SIP/RTP for phone, WebRTC for app and browser)
                 v
   +-----------------------------------+
   |        Media Gateway (Edge)       |
   |  handles call setup, codecs,      |
   |  echo cancellation, jitter buffer |
   +-----------------------------------+
                 |
                 |  clean audio chunks (20 ms each)
                 v
   +-----------------------------------+
   |    Voice Agent Orchestrator       |
   |     (one session per call)        |
   |                                   |
   |  Voice Activity Detection (VAD)   |
   |  Turn Detection                   |
   |  Speech-to-Text (streaming)   --> |---> STT Service (GPU)
   |  LLM + Tools (streaming)      --> |---> LLM Service (GPU)
   |  Text-to-Speech (streaming)   --> |---> TTS Service (GPU)
   |  Interruption Handling            |
   +-----------------------------------+
          |                  |
          v                  v
   +--------------+   +---------------------------+
   | Tools / APIs |   | Storage                   |
   | (order DB,   |   | (recordings, transcripts, |
   |  booking,    |   |  logs, metrics)           |
   |  CRM, etc.)  |   +---------------------------+
   +--------------+

```

Let's understand each part.

Media Gateway: This is the entry point. It talks to the phone network or to the app, accepts the call, and converts audio into a clean and standard format that our system understands. It also does audio clean-up like echo cancellation and noise suppression. Do not worry, we will learn about each of them in detail.

Voice Agent Orchestrator: This is the heart of the system. For every call, one orchestrator session is created (a session is the living record of one call, with its state and open connections). It receives audio chunks, decides when the user has finished speaking, sends audio to Speech-to-Text, sends text to the LLM, sends the LLM's reply to Text-to-Speech, and streams the audio back. It also handles interruptions. Think of it as the conductor of an orchestra, it does not play any instrument itself, but it makes everyone play at the right time.

STT, LLM, TTS Services: These are the three AI models. They run on GPUs and are shared by many calls.

Tools / APIs: The real business systems, like the order database, the booking system, or the CRM (the customer records system). An API is simply a way for one program to ask another program for something.

Storage: Recordings, transcripts, logs, and metrics for debugging, compliance, and improvement.

### The messages between the client and the orchestrator

The client (the app or the media gateway) and the orchestrator talk to each other using a small set of messages. Let's see them, because they will come up again and again:

- From client to orchestrator: `audio_chunk` (20 ms of the user's audio), and `playback_progress` (how much of the agent's audio has actually been played so far).
- From orchestrator to client: `agent_audio_chunk` (20 ms of the agent's voice), `transcript_interim` and `transcript_final` (to show text on screen in an app), `agent_speech_started` and `agent_speech_ended`, and `clear_audio_buffer` (drop everything not yet played, used for interruptions).

Keep these in mind, especially `playback_progress` and `clear_audio_buffer`. They are the two messages that make interruption handling work, as we will see later.

Now, let's go deep into each component, one by one.

## Component 1: Audio Transport

Before jumping into the AI models, we must know how sound travels from the user's mouth to our server.

### How sound becomes data

A microphone measures air pressure thousands of times per second and gives a number each time. These numbers are called samples. How many samples we take per second is the sample rate.

- Phone calls: 8,000 samples per second (8 kHz). This is why phone voices sound a bit muffled.
- Speech AI models: 16,000 samples per second (16 kHz). Good enough for speech.
- Music: 44,100 or 48,000 samples per second. Overkill for voice.

Each sample is stored as a 16-bit number (2 bytes). This raw list of numbers is called PCM (Pulse Code Modulation). It is the simplest form of digital audio.

### Chunks (Frames)

We do not send audio one sample at a time, and we do not wait for the whole sentence either. We cut the audio into small chunks, usually 20 milliseconds each. At 16 kHz, a 20 ms chunk has 320 samples. These chunks are sent continuously, 50 chunks per second. This is what makes real-time possible. Every component in our system works on these small chunks as they arrive.

### Codecs

Raw PCM is big. A codec compresses the audio before sending and decompresses it after receiving. The most common one for real-time voice on the internet is Opus. It is designed for speech, works well even when some packets are lost, and gives good quality at 24 to 32 kbps. Phone networks use older codecs like G.711.

### Transport options

Now, how do we send these chunks over the internet? We have three main options.

Option 1: WebSocket

A WebSocket is a long-lived two-way connection between the client and the server, built on top of TCP. TCP is the internet protocol that guarantees every packet arrives, and in the correct order.

This sounds good, but for real-time audio it has a problem. If one packet is lost, TCP stops and waits for it to be re-sent before delivering the later packets. This is called head-of-line blocking. In a voice call, a 20 ms chunk that arrives 500 ms late is useless. We would rather skip it and keep going.

WebSocket is simple and good for server-to-server audio (for example, our orchestrator talking to the STT service inside our datacenter, where the network is reliable). It is not the best choice for a user on a mobile network.

Option 2: WebRTC

WebRTC is a technology built into every modern browser and mobile platform specifically for real-time audio and video calls. It uses UDP instead of TCP. UDP does not wait for lost packets, it just keeps going. That is exactly what we want for voice.

WebRTC also comes with a full toolbox for real-time audio:

- Jitter buffer: Packets arrive at uneven timing over the internet. The jitter buffer holds them for a few milliseconds and plays them smoothly.
- Packet loss concealment: If a chunk is lost, it fills the gap with a guess based on the neighbouring chunks, so we hear a tiny glitch instead of a silence.
- Acoustic Echo Cancellation (AEC): This is very important, and we will discuss it just below.
- Noise suppression and automatic gain control (keeping the volume steady).
- Encryption by default.

It makes our life easy. So, for mobile apps and browsers, WebRTC is the right choice.

Option 3: SIP and RTP (Telephony)

When the user calls from a normal phone, the audio comes through the telephone network (called PSTN, which stands for Public Switched Telephone Network). To connect a phone call to our software, we use a telephony provider. The provider receives the phone call and forwards the audio to us using protocols called SIP (Session Initiation Protocol, for setting up and ending the call) and RTP (Real-time Transport Protocol, for carrying the audio). We will discuss telephony in its own section later.

### Acoustic Echo Cancellation (AEC)

But, here is the catch. When our agent speaks, its voice comes out of the user's speaker. The user's microphone picks up that voice and sends it back to our server. Now, our system hears the agent's own voice and thinks the user is speaking. The agent interrupts itself. This is called echo.

Acoustic Echo Cancellation solves this. The system knows exactly what audio it is playing on the speaker, so it subtracts that from what the microphone hears. What remains is only the user's real voice. WebRTC does this automatically on the client. On phone calls, the phone network handles most of it. If we build our own client, we must make sure AEC is on, otherwise interruption handling will never work correctly.

### Why do we send audio to the server at all?

Now, the question is, why not run everything on the phone? The answer is that good STT, LLM, and TTS models are big and need GPUs. A phone cannot run them at the quality we need. So, we stream the audio to the server. The only thing we can run on the device is a small Voice Activity Detection model, which we will see next.

We have a detailed blog on Cloud vs On-device Model Deployment that explains when a model should run on the device and when it should run in the cloud.

[…543ln elided…]

Here is why the KV cache matters so much. To write each new token during decode, the model needs the notes for every token that came before it. Without the KV cache, the model would have to recompute all those notes again for every single new word. That would be painfully slow. So, the model stores the notes once and reuses them. The KV cache is what makes generating long answers fast.

Here is the key point to remember:

The KV cache grows as the answer grows. Every new token adds one more set of notes to the KV cache, and all of these notes sit in GPU memory.

We can picture the two phases and the growing KV cache as below:

```
PREFILL then DECODE: the KV cache grows one set of notes per token

prompt tokens:  [ Tell ][ me ][ a ][ joke ]
                   |      |     |     |
PREFILL writes:   [n]    [n]   [n]   [n]      (one note per prompt token)

so KV cache =   [n][n][n][n]                  (4 notes after prefill)

DECODE step 1:  writes "Why"      KV cache: [n][n][n][n][n]
DECODE step 2:  writes "did"      KV cache: [n][n][n][n][n][n]
DECODE step 3:  writes "the"      KV cache: [n][n][n][n][n][n][n]
                   ...                          (grows by one each step)

```

Here, we can notice that prefill creates one set of notes for every prompt token in one go. Then decode writes the reply one token at a time, and each new token adds one more set of notes to the KV cache. So, the longer the answer, the larger the KV cache becomes in GPU memory.

This is the foundation we needed. Now we are ready to see the real problem.

### The problem: the KV cache eats GPU memory

Now that we know what the KV cache is, let's see the trouble it causes.

The model itself takes up a big chunk of GPU memory. Whatever memory is left over is used to hold the KV cache for all the requests we are serving right now.

So, the KV cache is the thing that decides how many users we can serve at once. The more KV cache memory we have free, the more requests we can run together.

Let's put it simply. Each request that is being served has its own KV cache, and that KV cache keeps growing as its answer grows. If we are serving many users, all of their KV caches live in GPU memory together, fighting for the same limited space.

So, the real bottleneck in serving an LLM is not the math speed. It is the KV cache memory. KV Cache Compression techniques make each cache smaller, but no matter how small it gets, the engine still has to manage it well.

This means the whole challenge of serving an LLM comes down to managing memory. If we manage the KV cache memory well, we serve more users. If we manage it badly, we waste the GPU and serve fewer users.

Now, the next question is, how does the naive approach manage this memory, and why is it bad? Let's see.

### Why naive serving wastes memory

Let's understand how a simple, naive serving engine handles the KV cache, and where it goes wrong.

The naive approach does something that feels safe but is actually very wasteful. When a request comes in, the engine does not know how long the answer will be. So, to be safe, it reserves one big continuous block of memory large enough to hold the longest possible answer.

Let's say the model can produce up to 2,000 tokens. For every single request, the naive engine reserves space for 2,000 tokens of KV cache right away, even before the model has written anything.

Here is the catch. Most answers are short. If a user's answer is only 50 tokens long, then the space for the other 1,950 tokens just sits there, reserved but unused, doing nothing. We blocked a huge amount of memory for an answer that never needed it.

This waste has two names, and we must understand both.

The first is over-reservation. This means we reserved far more memory than the request actually used. The reserved-but-unused space cannot be given to anyone else, so it is wasted.

The second is fragmentation. Fragmentation means the free memory is broken into small scattered pieces that we cannot use. Let's understand this with a picture.

We can picture the naive approach as below:

```
NAIVE SERVING: one big continuous block reserved per request

Request A: [#### used (50) ............... wasted, reserved for 2000 ..............]
Request B: [###### used (120) ............ wasted, reserved for 2000 ..............]
Request C: [## used (20) ................. wasted, reserved for 2000 ..............]

free memory left: scattered tiny gaps  ->  cannot fit a new request

```

Here, we can see that each request grabbed a giant continuous block but only used a tiny part of it at the front. The rest is wasted. And the small leftover gaps between blocks are too small and too scattered to hold a new request. So, even though a lot of memory is technically free, we cannot use it. This is fragmentation.

The result is poor. The GPU has plenty of memory on paper, but because it is wasted and scattered, we can only serve a few users at a time. We are paying for a powerful GPU and using only a small part of it.

So, here comes vLLM to the rescue.

### What is vLLM?

Now that we understand the problem, let's understand the solution.

vLLM is a high-throughput engine for serving LLMs. It is built to serve as many requests as possible on a GPU by managing the KV cache memory very efficiently.

In simple words, vLLM is a smart serving engine that stops wasting GPU memory, so it can serve many more users at the same time.

Let's understand the word throughput, because it sits right in the name "high-throughput". Throughput means how much work we finish in a given amount of time. High throughput means we serve a large number of tokens and requests every second. That is exactly what vLLM is built to maximize.

vLLM solves the memory problem with two main ideas working together:

- PagedAttention, which manages the KV cache in small fixed-size blocks instead of one giant block, so no memory is wasted.
- Continuous batching, which keeps the GPU busy by swapping finished requests out and new ones in at every step.

Do not worry, we will learn about each of them in detail. Let's start with PagedAttention, because it is the heart of vLLM.

### PagedAttention, the core idea

Let's understand the core idea behind vLLM step by step.

PagedAttention manages the KV cache in small fixed-size blocks, allocating memory on demand instead of reserving one big block upfront.

In simple words, instead of grabbing a huge block of memory for each request, vLLM hands out memory in small equal-sized pieces, only when the request actually needs more.

This idea is borrowed from how an operating system manages memory. The operating system manages memory using small fixed-size pieces called pages. When a program needs more memory, the operating system gives it one more page. The pages do not have to sit next to each other in memory. The operating system keeps a small table that remembers where each page is.

vLLM does exactly the same thing for the KV cache. It splits the KV cache memory into small fixed-size blocks, where each block holds the notes for a fixed number of tokens, for example 16 tokens. When a request needs to store more tokens, vLLM gives it one more block. The blocks do not have to sit next to each other. vLLM keeps a small table, called a block table, that remembers which blocks belong to which request and in what order.

Let's walk through it with an example.

Step 1: A request comes in and starts generating an answer. vLLM gives it one block, enough for 16 tokens. The request starts filling that block.

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

Step 2: The answer crosses 16 tokens. The first block is full. vLLM simply gives the request one more block, wherever a free block is available in memory. It does not need to be next to the first block.

After that: The answer keeps growing, and vLLM keeps handing out one block at a time, only as needed. When the answer is finished, vLLM frees all of that request's blocks at once, and those blocks immediately become available for other requests.

We can picture this with a simple diagram as below:

```
PAGED ATTENTION: KV cache split into small fixed-size blocks

GPU memory:  [B1][B2][B3][B4][B5][B6][B7][B8][B9] ... (a pool of equal blocks)

Request A's block table  ->  B1, B4, B7      (3 blocks, given as needed)
Request B's block table  ->  B2, B3          (2 blocks, given as needed)
Request C's block table  ->  B5              (1 block, just started)

free blocks ready to hand out: B6, B8, B9

```

Here, we can see that the memory is one shared pool of equal-sized blocks. Each request gets only the blocks it actually needs, and they can be scattered anywhere in the pool. The block table is the small map that ties a request to its blocks in the right order. When a request finishes, its blocks go straight back into the free pool for the next request to use.

The problem is solved. There is no over-reservation, because we only allocate a block when it is truly needed. And there is almost no fragmentation, because every block is the same size, so any free block fits any request. The wasted memory drops to nearly nothing.

To learn PagedAttention, the KV Cache, and vLLM in depth, check out our AI and Machine Learning Program at Outcome School.

### How PagedAttention shares memory

There is one more beautiful thing PagedAttention gives us, and it comes for free once we have blocks. It is sharing.

Because the KV cache is now made of small blocks, two different requests can point their block tables at the very same block in memory, instead of each keeping its own copy. This means they share the memory for the part that is identical.

Let's understand this with two real cases where sharing helps a lot.

The first case is identical prefixes. A prefix is the starting part of something. Suppose many users send requests that all begin with the same long system instructions, for example "You are a polite customer support agent for a car dealership." That long beginning is identical for everyone. With blocks, vLLM can store the KV cache for that shared beginning once, and let every request point to those same blocks. We do not store the same notes many times. We store them once and share. We have a detailed blog on prompt caching that explains how reusing the KV cache for an identical prefix works.

The second case is beam search. Beam search is a way of generating text where the model explores several possible answers at the same time and then keeps the best one. These several answers, called beams, all share the same beginning and only differ later. With blocks, all the beams can share the blocks for the common beginning and only use separate blocks where they actually diverge.

We can picture sharing as below:

```
SHARING WITH BLOCKS

shared beginning:   [B1][B2]   <- one copy in memory, used by all
                       |
        +--------------+--------------+
        |              |              |
   Request A      Request B       Beam C
   adds [B5]      adds [B6]       adds [B7]

```

Here, we can see that the blocks `B1` and `B2` hold the identical beginning and are stored only once. Three different paths all point to those same two blocks for the shared part, and each one adds its own separate blocks only for the part that is unique to it. We saved the memory of storing that beginning three times.

This is how PagedAttention not only stops waste but also lets requests share memory, which packs even more users onto the same GPU.

### Continuous batching

Now, let's learn about the second big idea in vLLM, which works together with PagedAttention.

To understand it, we first need to understand batching. Batching means running many requests together in one go, instead of one at a time. A GPU is much more efficient when it processes many requests together, so batching is how we keep the GPU busy and get high throughput.

But the naive way of batching has a problem. Let's see it.

The naive way is called static batching. In static batching, we collect a batch of requests, run them all together, and we must wait for every request in the batch to finish before we start the next batch.

Here is the catch. Different requests produce answers of very different lengths. One user's answer is 20 tokens, while another's is 800 tokens. In static batching, the short request finishes early and then just sits there idle, waiting for the long request to finish, because the whole batch moves together. During that wait, the GPU slot for the finished request is doing nothing. That is wasted GPU time.

So, here comes continuous batching to the rescue.

Continuous batching swaps finished requests out and brings new waiting requests in at every single step, instead of waiting for the whole batch to finish.

In simple words, the moment a request finishes, vLLM removes it and immediately pulls in a new request from the waiting line to take its place. The GPU never sits idle waiting.

Remember, decode produces the answer one token at a time, so there are many small steps. At each step, vLLM checks: did any request just finish? If yes, it drops that request and adds a new one. The batch is always kept full of active work.

Let's compare the two approaches with a diagram as below:

```
STATIC BATCHING (naive): the whole batch waits for the slowest one

step:   1    2    3    4    5    6    7    8
Req A:  X    X    X    done -    -    -    -     <- idle, wasting the slot
Req B:  X    X    X    X    X    X    X    done

CONTINUOUS BATCHING (vLLM): finished slots are refilled right away

step:   1    2    3    4    5    6    7    8
slot1:  A    A    A    C    C    C    D    D     <- A finished, C jumped in, then D
slot2:  B    B    B    B    B    B    B    done

```

Here, we can see that in static batching, request A finished early but its slot stayed empty and idle until the slow request B finished. In continuous batching, the moment A finished, request C jumped into that slot, and when C finished, request D jumped in. The GPU is kept busy the whole time. No slot is wasted.

Continuous batching and PagedAttention fit together perfectly. PagedAttention frees a finished request's blocks instantly, and continuous batching immediately uses that freed memory and that freed slot for a new waiting request. Together, they keep the GPU memory and the GPU compute both fully used.

This is how vLLM keeps the GPU working at full speed.

To master Continuous Batching, LLM Inference Engineering, and how to design an LLM Inference Platform (vLLM-as-a-Service) end to end, check out our AI and Machine Learning Program at Outcome School.

### The OpenAI-compatible API server

Now, let's see how we actually use vLLM in practice.

vLLM exposes an OpenAI-compatible API server.

vLLM can run as a server that listens for chat requests and sends back the model's replies.

This matters a lot because a huge number of tools and applications are already written to talk to OpenAI's API. If vLLM speaks the same language, then we can point those existing tools at our own vLLM server by just changing the address, without rewriting our code. We can run our own model on our own GPU and our application talks to it the same way it talked to OpenAI.

So, vLLM gives us the high-throughput engine on the inside, and a familiar, easy-to-use API on the outside. This is the part we must appreciate, because it makes vLLM very simple to adopt in real projects.

### The benefits of vLLM

Let's quickly bring together the benefits, because they are the reason we use vLLM.

- Much higher throughput. Because PagedAttention stops wasting memory and continuous batching stops wasting GPU time, vLLM can serve far more tokens and far more users per second than a naive engine.
- Better GPU utilization. Utilization means how much of the GPU we are actually using. vLLM keeps both the GPU memory and the GPU compute close to fully used, so we get more value out of the expensive hardware.
- Lower cost per request. Since one GPU now serves many more users, the cost spread across each user drops a lot.
- Easy to adopt. The OpenAI-compatible API means we can plug vLLM into our existing applications with very little change.

In simple words, vLLM lets us serve more users, faster, and cheaper, on the same GPU, without changing the quality of the answers. The model still produces the same replies. vLLM just stops wasting memory and time. We have a detailed blog on LLM inference optimization that covers the broader set of techniques behind fast serving.

That's the beauty of vLLM.

### vLLM in the real world

Now, let's see where vLLM is used in real systems.

vLLM is one of the most popular open-source serving engines, and it is widely used by companies that want to run open large language models on their own GPUs. Anywhere we need to serve a model to many users at once, vLLM is a strong choice.

vLLM is not the only serving engine. We have a detailed blog on how SGLang works that takes a different approach to prefix sharing, matching shared text precisely with a radix tree instead of fixed-size blocks. On NVIDIA hardware there is also TensorRT-LLM, NVIDIA's own engine, which goes all the way down to kernels tuned for each GPU generation.

It is especially powerful in two kinds of systems.

The first is high-traffic chat applications. When many users are chatting at the same time, continuous batching keeps every GPU slot full, and PagedAttention packs many users' KV caches into the same memory. So, we serve a large crowd on fewer GPUs.

The second is agent systems. An agent is an AI program that works on a task step by step, often calling tools and taking many turns to finish a job. Agents send the same big block of instructions on every step, so the identical-prefix sharing in PagedAttention saves a lot of memory, and continuous batching keeps the many short steps flowing without idle time.

So, anywhere we need to serve an LLM to many users efficiently and cheaply, vLLM helps us a lot.

This is how vLLM works. It treats the KV cache like an operating system treats memory, handing out small fixed-size blocks on demand and sharing them across requests through PagedAttention, it keeps the GPU always busy by swapping requests in and out every step through continuous batching, and it wraps all of this behind a familiar OpenAI-compatible API, so we get much higher throughput and far better GPU utilization on the same hardware.

### Does vLLM change the quality of the model's answers?

No. vLLM does not change the quality of the answers. The model still produces the same replies. vLLM just stops wasting GPU memory and GPU time, so we can serve more users, faster, and cheaper, on the same GPU.

### Is math speed the main bottleneck when serving an LLM?

No. The real bottleneck in serving an LLM is the KV cache memory, not the math speed. Every request has its own KV cache that keeps growing with the answer, and all of them share the limited GPU memory. So, how well we manage that memory decides how many users we can serve.

### Do we need to rewrite our application to use vLLM instead of OpenAI's API?

No. vLLM exposes an OpenAI-compatible API server. So, we can point our existing tools at our own vLLM server by just changing the address, without rewriting our code. Our application talks to our own model the same way it talked to OpenAI.

### Is vLLM the only LLM serving engine?

No. vLLM is one of the most popular open-source serving engines, but there are others. SGLang takes a different approach to prefix sharing, matching shared text precisely with a radix tree instead of fixed-size blocks. On NVIDIA hardware, there is also TensorRT-LLM, NVIDIA's own engine.

### Why is vLLM a good fit for agent systems?

Agents send the same big block of instructions on every step. The identical-prefix sharing in PagedAttention stores that shared beginning once, which saves a lot of memory. At the same time, continu

[Showing lines 1-318 and 862-1155 of 1155; 543 middle lines (31.5KB) elided. Read artifact://85 for full output]
