> Source: https://outcomeschool.com/blog/multimodal-ai

# Multimodal AI
URL: https://outcomeschool.com/blog/multimodal-ai
Published: 2026-05-10

Multimodal AI

# Multimodal AI

Authors
: - Name
: Amit Shekhar
Published on
: May 10, 2026

In this blog, we will learn about Multimodal AI, what it means, why it matters, how it works, and where we use it in the real world.

We will cover the following:

- The Big Picture
- What is a Modality?
- Unimodal AI vs Multimodal AI
- Why Multimodal AI?
- How Multimodal AI Works
- Three Common Types of Multimodal AI
- Real Examples of Multimodal AI
- Use Cases of Multimodal AI
- Common Mistakes to Avoid
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

For many years, AI models could only handle one type of data at a time. A text model could read text. An image model could see images. An audio model could listen to audio. Each model lived in its own small world, and these worlds did not talk to each other.

Multimodal AI breaks these walls.

In simple words:

Multimodal AI = AI that can understand and generate more than one type of data at the same time.

A single multimodal model can read text, see images, hear audio, and even watch video, all at once. Then it can respond in any of these forms.

Let's decompose the name:

Multimodal = Multi + Modal

Here, "Multi" means many, and "Modal" comes from "modality", which is just a fancy word for a type of data. So, Multimodal AI is simply AI that works with many types of data together.

The ability to create brand new content like this is what we call Generative AI, and we have a detailed blog on What is Generative AI? that explains it in depth.

## What is a Modality?

Before going deeper, we must understand what a "modality" means.

Modality. A specific form or channel through which information reaches us.

In simple words, a modality is just a type of data.

Common modalities are:

- Text. Words, sentences, source code, articles, chat messages.
- Image. Photos, charts, diagrams, scanned documents.
- Audio. Speech, music, ringtones, machine sounds.
- Video. Moving images, often with sound, like films and reels.
- Other. Sensor data, depth maps, 3D shapes, biometric signals.

A human is a natural multimodal system. We see, we hear, we read, we touch, we smell, and we mix all of these signals into one understanding of the world. A doctor checking a patient is doing exactly this, every single day.

Multimodal AI tries to do the same.

## Unimodal AI vs Multimodal AI

Let's understand the difference with a simple comparison.

Unimodal AI works with only one type of data.

For example:

- A spam classifier that reads only text.
- A face detector that sees only images.
- An image classifier that sees only images and tells if it is a cat or a dog.

Here, the output is just a label, a number, or a coordinate about the input. A label or a number is not a modality. The four modalities are text, image, audio, and video. So, even though the spam classifier prints the word "spam", it is not generating a piece of language - it is just attaching a tag to the input. The model is still unimodal.

Multimodal AI works with two or more types of data at the same time.

For example:

- A model that takes a photo and a question, and answers the question.
- A model that watches a video and writes a summary in text.
- A model that listens to a song and generates an album cover image.

Here is a simple picture of the difference:

```
       Unimodal AI                Multimodal AI

   Text or Image or Audio      Text   Image   Audio
   (only one at a time)            \    |     /
            |                       \   |    /
            v                     +-----v-----+
        +-------+                 |   Model   |
        | Model |                 +-----------+
        +-------+                       |
            |                           v
            v                         Output
          Output

```

Here, we can see that a unimodal model takes one type of input at a time, while a multimodal model takes many types of input together and produces one output.

Let me tabulate the differences between Unimodal AI and Multimodal AI for your better understanding so that you can decide which one to use based on your use case.

| Aspect | Unimodal AI | Multimodal AI |
| --- | --- | --- |
| Inputs | One type (text or image or audio) | Two or more types together |
| Understanding | Limited to one sense | Combined across senses |
| Use cases | Narrow tasks | Rich, real-world tasks |
| Example | Sentiment analysis on tweets | "Describe this image" assistant |
| Cost | Lower | Higher |

## Why Multimodal AI?

Now, the question is: why do we need Multimodal AI? The answer is simple - the real world is multimodal.

Let's say we walk into a doctor's clinic. The doctor:

- Reads our medical history (text).
- Looks at our X-ray (image).
- Listens to our heartbeat (audio).
- Watches how we walk (video).

The doctor combines all of these signals into one diagnosis. A doctor who could only read text would miss most of the picture.

The same is true for AI.

A model that can only read text cannot help us when we paste a screenshot of an error. A model that can only see images cannot answer a question about that image. A model that can only listen to audio cannot read the meeting notes that came along with the recording.

This is when Multimodal AI comes into the picture. By combining modalities, the model gets a much fuller view of the world, just like the doctor.

This is why Multimodal AI matters.

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

## How Multimodal AI Works

At the core, every Multimodal AI system follows the same recipe.

The idea behind Multimodal AI is simple: convert every type of input into a common numeric form the model can understand, and then process all of them together.

Here is the high-level anatomy:

```
   +-------+    +-------+    +-------+
   | Text  |    | Image |    | Audio |
   +---+---+    +---+---+    +---+---+
       |            |            |
       v            v            v
   +-------+    +-------+    +-------+
   | Text  |    | Image |    | Audio |
   |Encoder|    |Encoder|    |Encoder|
   +---+---+    +---+---+    +---+---+
       |            |            |
       +-----+------+------+-----+
             |
             v
       +-----------+
       | Shared    |
       | Embedding |
       |   Space   |
       +-----+-----+
             |
             v
       +-----------+
       | Multimodal|
       |   Model   |
       +-----+-----+
             |
             v
       +-----------+
       |  Output   |
       | (text,    |
       |  image,   |
       |  audio)   |
       +-----------+

```

Let's decode each step. We will keep our doctor analogy from the previous section to make every part easy to follow.

1. Encoders for each modality.

A model cannot understand raw text, raw pixels, or raw sound waves directly. It only understands numbers. So, we need a way to turn each input into numbers.

Each type of input needs its own encoder. An encoder is a small model that turns raw data into a list of numbers, called a vector.

Just like our doctor uses eyes for X-rays, ears for the heartbeat, and reading skills for the notes, the multimodal model uses different encoders for different modalities.

- A Text Encoder turns words into vectors.
- An Image Encoder turns pixels into vectors. This often uses a Vision Transformer.
- An Audio Encoder turns sound waves into vectors.

These vectors are called embeddings. An embedding is just a vector that captures the meaning of the input in a form the model can use.

2. Shared Embedding Space.

Here is the key trick of Multimodal AI.

All the encoders are trained together so that their outputs land in the same vector space. The training pulls matching pairs (a photo of a cat and the word "cat") close to each other, and pushes mismatched pairs (a photo of a cat and the word "car") apart.

So a photo of a cat and the word "cat" end up close to each other in this space, even though one came from pixels and the other came from letters.

Let's see this with a simple picture:

```
   Shared Embedding Space (simplified)

         ^
         |
         |   "cat"  *     * cat photo
         |
         |
         |
         |   "dog"  *     * dog photo
         |
         +----------------------------->

```

Here, we can see that the word "cat" and the photo of a cat sit near each other in the same space. Same for "dog" and the dog photo. The model now treats them as related, no matter the input type.

This shared space is what lets the model "compare" a photo to a sentence, or align a sound to a video frame. In our doctor analogy, this is the moment when the doctor combines the X-ray, the notes, and the heartbeat into one mental picture of the patient.

3. The Multimodal Model.

The shared embeddings are passed into a single model, usually a Transformer, which is a kind of neural network that learns relationships between pieces of data. The model can now reason across all the inputs at once.

For example, if we give the model a photo of a kitchen and ask "How many chairs are there?", the model looks at both the image embedding and the text embedding, and produces an answer.

Just like the doctor combines all the signals into one diagnosis, the multimodal model combines all the embeddings into one answer.

4. The Output.

The output can be text, image, audio, or even video, depending on the model and the task.

So, the recipe is: encode every modality → align them in a shared space → reason → generate.

Now, let's put this end to end with a quick example.

Step 1: We upload a photo of a kitchen and type the question "How many chairs are there?".

Step 2: The image encoder turns the photo into an image embedding. The text encoder turns the question into a text embedding.

Step 3: Both embeddings go into the multimodal model. The model looks at the image embedding and the text embedding together.

Step 4: The model produces the answer in text, for example "There are 4 chairs.".

This is how Multimodal AI works under the hood.

To master Multimodal AI, Embeddings, and Transformer Architecture in depth, check out our AI and Machine Learning Program at Outcome School.

## Three Common Types of Multimodal AI

Now that we have learned how Multimodal AI works, it is time to learn the three common patterns we see in the real world.

1. Multimodal Understanding.

The model takes inputs in many modalities and replies in one modality, often text.

For example, we send a photo and ask "What is in this image?", and the model replies in text. GPT-4V, Gemini, and Claude (with vision) follow this pattern.

2. Cross-Modal Generation.

The model takes input in one modality and produces output in another.

For example, text in, image out (DALL-E, Midjourney). Text in, video out (Sora, Veo). Audio in, text out (Whisper).

3. Cross-Modal Alignment.

The model places two or more modalities in the same shared embedding space so we can compare them directly.

For example, CLIP places text and images in a shared space, so we can search images using a text query.

Every multimodal model uses a shared embedding space inside it. In Cross-Modal Alignment, that shared space is itself the product. The model is trained mainly to build this space and to expose it, so we can compare or search across modalities directly, without going through a generated answer.

These three patterns cover most Multimodal AI systems we see today. Many real models mix two or more of these patterns together.

## Real Examples of Multimodal AI

Now, let's put names to the three patterns. Here are some well-known multimodal models we may already know.

- GPT-4 with Vision (GPT-4V). Reads text and images, replies in text.
- GPT-4o. Reads text, images, and audio, and replies in text or audio in real time.
- Google Gemini. Reads text, images, audio, video, and code in one go.
- Claude (with vision). Reads text and images, answers in text.
- CLIP (Contrastive Language-Image Pretraining). Connects text and images in a shared embedding space.
- DALL-E and Midjourney. Take a text prompt and generate an image, powered by diffusion models.
- Whisper. Listens to audio and produces text.
- Sora and Veo. Take text and produce video.

Each of these is a real-world Multimodal AI system already in use today.

## Use Cases of Multimodal AI

- Visual Question Answering (VQA). Upload a photo, ask a question, get an answer.
- Document Understanding. Read a PDF that has text, tables, and charts together.
- Medical Imaging. Combine X-rays, scans, and patient notes for better diagnosis.
- Self-Driving Cars. Mix camera, radar, and LIDAR (Light Detection and Ranging) data to drive safely.
- Accessibility. Describe images for people who cannot see them. Read text aloud for people who cannot read.
- Content Creation. Generate images, videos, and music from a simple text prompt.
- Customer Support. Let the user send a screenshot or a voice note instead of typing a long message.
- Education. Explain a diagram, solve a handwritten math problem, or read a textbook page aloud.
- Mobile Apps. Snap a photo of a foreign menu and get an instant translation, with the dish names spoken aloud.

This is how Multimodal AI is quietly changing the way we use computers.

## Common Mistakes to Avoid

Let's look at a few common mistakes people make when thinking about Multimodal AI.

- Treating it as just "text + image". Multimodal means many modalities, not only two. Audio, video, sensor data, and 3D shapes also count.
- Assuming one model fits all. Some tasks still need a focused unimodal model. Multimodal is not always better.
- Ignoring data quality. A multimodal model is only as good as the alignment between its modalities. Bad pairings, like a wrong caption for a photo, lead to bad results.
- Forgetting cost. Multimodal models are heavier and slower than unimodal ones. We must use them where the extra signal is worth the cost.
- Skipping evaluation per modality. A model may be strong on text but weak on audio. We must test each modality on its own and also together.
- Mixing too many modalities at once. More modalities is not always better. Each new modality adds noise, latency, and risk. We must add a modality only when it brings clear value to the task.
- Forgetting about bias. Multimodal models can carry biases from each modality and from the training pairs. We must check the outputs for unfair patterns, just like we do for unimodal models.

## Quick Summary

Let's recap what we have learned about Multimodal AI:

- Multimodal AI is AI that can handle more than one type of data, like text, image, audio, and video, together.
- A modality is just a type of data.
- Unimodal AI works with one type of data. Multimodal AI works with many types together.
- Real-world tasks are multimodal in nature, and Multimodal AI fits them better.
- Just like a doctor combines reports, X-rays, and heartbeats into one diagnosis, a multimodal model combines all the embeddings into one answer.
- The core recipe is: encode each modality → align in a shared space → reason → generate.
- The three common patterns are Multimodal Understanding, Cross-Modal Generation, and Cross-Modal Alignment.
- Models like GPT-4V, Gemini, Claude, CLIP, DALL-E, and Whisper are all examples of Multimodal AI.

Thanks

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

[…783ln elided…]

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

[Showing lines 1-444 and 1228-1521 of 1521; 783 middle lines (47.3KB) elided. Read artifact://54 for full output]
