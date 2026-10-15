> Source: https://outcomeschool.com/blog/paged-attention-in-llms

# What is Paged Attention in LLMs and How Does It Work?
URL: https://outcomeschool.com/blog/paged-attention-in-llms
Published: 2026-03-29
Author: Amit Shekhar

What is Paged Attention in LLMs and How Does It Work?

# What is Paged Attention in LLMs and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: March 29, 2026

Paged Attention is a technique that manages the KV Cache memory more efficiently by breaking it into small, fixed-size blocks called pages. This removes the memory waste and lets LLMs serve many more users at the same time.

In this blog, we will learn about Paged Attention, a technique that solves the memory waste problem of KV Cache, allowing LLMs to serve many more users at the same time.

We will start with a quick recap of KV Cache, understand the memory problem it creates, see how traditional memory allocation wastes space through an example, and then walk through how Paged Attention solves this problem by borrowing an idea from how computers manage memory.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## Quick Recap: KV Cache

When an LLM generates text, it predicts one token at a time. A token is a small piece of text. It can be a word, part of a word, or even a single character.

At each step, the model computes a Key and a Value for the new token and needs the Keys and Values of all previous tokens.

Without KV Cache, the model would recompute the Key and Value for every previous token at every step, wasting computation. KV Cache solves this by storing the Key and Value of each token after it is computed, so they can be reused in future steps.

KV Cache makes text generation much faster. But it comes with a trade-off: it uses memory to store all those Keys and Values.

Now, let's understand the memory problem this creates.

## The Problem: Memory Waste in KV Cache

When a user sends a request to an LLM, the system needs to set aside memory for the KV Cache of that request. But here is the challenge: the system does not know in advance how long the response will be.

A user can ask a simple question that results in a 20-token response, or a complex question that results in a 2,000-token response. The system has no way of knowing upfront.

In the traditional approach, the system reserves one large block of memory for each request - where all the slots are right next to each other - enough to handle the maximum possible response length. This means reserving memory for, say, 2,048 tokens, even if the actual response turns out to be only 50 tokens.

Let's understand this with an analogy.

### The Hotel Analogy

Imagine a hotel where guests check in but do not know how many nights they will stay. Some will stay 1 night, some will stay 30 nights.

Traditional approach: When a guest checks in, the hotel reserves 30 rooms in a row on the same floor, just in case the guest stays for 30 nights. Even if the guest stays for only 2 nights, all 30 rooms remain reserved and cannot be given to anyone else.

Now imagine 10 guests check in. The hotel reserves 30 × 10 = 300 rooms in a row. But if most guests stay only a few nights, hundreds of rooms sit empty and wasted.

This is exactly what happens with KV Cache memory in the traditional approach.

The waste shows up in two ways:

1. Internal waste: Memory is reserved but never used. If a request only generates 50 tokens but memory was reserved for 2,048 tokens, the remaining space for 1,998 tokens is wasted.
2. External waste: Because memory must be allocated in one large block with all slots next to each other, small gaps of free memory scattered around cannot be used, even if together they would be enough to serve a new request.

This memory waste is a serious problem. A large portion of the reserved memory is never actually used.

Because memory is limited, this waste means the system can serve fewer users at the same time. If the system could use memory more efficiently, it could handle many more requests simultaneously.

This is the problem that Paged Attention solves.

## What is Paged Attention?

Paged Attention is a technique that manages KV Cache memory more efficiently by breaking it into small, fixed-size blocks called pages. These pages do not need to be next to each other in memory.

The word "Paged" comes from a concept in operating systems. An operating system manages memory for all the programs running on the computer.

Instead of giving each program one large block of memory with all slots next to each other, the operating system breaks memory into small, fixed-size pieces called pages. Each program gets as many pages as it needs, and these pages can be scattered anywhere in memory. The operating system keeps track of where each page is using a page table, a simple list that maps each page of a program to its actual location in memory.

Paged Attention applies the same idea to KV Cache.

Let's go back to our hotel analogy to understand how this works.

### The Hotel Analogy: Paged Approach

Paged approach: Instead of reserving 30 rooms in a row for each guest, the hotel gives rooms one at a time, as needed. When a guest checks in, they get 1 room. When they need another night, they get another room, wherever one is available. It does not have to be next to the first room. The hotel keeps a list that tracks which rooms belong to which guest.

Now, if a guest stays for only 2 nights, only 2 rooms are used. The remaining rooms are free for other guests. No waste.

If 10 guests check in, each gets only the rooms they actually need. The hotel can serve far more guests with the same number of rooms.

This is how Paged Attention works with KV Cache.

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

## How Paged Attention Works

In Paged Attention, the KV Cache memory is divided into small, fixed-size blocks. Each block can store the Key and Value for a fixed number of tokens. For example, if the block size is 4, each block can store the Key and Value for 4 tokens.

Let's walk through an example.

Let's say a user sends a request and the model is generating the response: "I love teaching AI and Machine Learning at Outcome School".

### Without Paged Attention (Traditional Approach)

The system reserves one large block of memory for, say, 16 tokens upfront:

```
Memory: [__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __]
         Reserved for this request (16 slots)

```

As the model generates tokens, it fills the slots one by one:

```
Memory: [I  love  teaching  AI  and  Machine  Learning  at  Outcome  School  __  __  __  __  __  __]
         Used: 10 tokens                                                      Wasted: 6 slots

```

The remaining 6 slots are reserved but never used - wasted memory.

### With Paged Attention

The system allocates memory in small blocks of 4 tokens each, only when needed:

Step 1: The model starts generating. The system allocates Block 1 from wherever available in memory:

```
Block 1: [I  love  teaching  AI]

```

Step 2: Block 1 is full. The system allocates Block 2. It does not have to be next to Block 1:

```
Block 1: [I  love  teaching  AI]
Block 2: [and  Machine  Learning  at]

```

Step 3: Block 2 is full. The system allocates Block 3:

```
Block 1: [I  love  teaching  AI]
Block 2: [and  Machine  Learning  at]
Block 3: [Outcome  School  __  __]

```

Only 2 slots are wasted in Block 3, compared to 6 in the traditional approach. And no memory was reserved upfront that went unused.

### The Block Table

But if the blocks are scattered across memory, how does the model find them?

The system keeps track of which blocks belong to which request using a block table, just like how an operating system uses a page table.

```
Block Table for Request 1:
  Block 0 → Location 5 in memory
  Block 1 → Location 12 in memory
  Block 2 → Location 3 in memory

```

The blocks are numbered in order (0, 1, 2) and each one points to its actual location in memory. When the model needs to read the Key and Value of a previous token, it uses the block table to find the right block.

This is how the model can access the Key and Value of any previous token, even though the blocks are scattered across memory.

To learn Paged Attention, KV Cache, vLLM, and inference infrastructure end to end, check out our AI and Machine Learning Program at Outcome School.

## Why Paged Attention Is So Effective

Paged Attention solves the two types of memory waste we discussed earlier:

1. Internal waste is nearly eliminated. Memory is allocated only as needed, block by block. The only waste is in the last block, which will not always be completely full. In our example, only 2 out of 4 slots were wasted in the last block, compared to 6 out of 16 in the traditional approach.
2. External waste is eliminated. Because blocks do not need to be next to each other, any free block anywhere in memory can be used. There are no unusable gaps.

The result: Paged Attention can use memory much more efficiently. This means the system can serve significantly more requests at the same time with the same amount of memory.

Note that Paged Attention does not make the KV Cache itself smaller, it only stops the memory around it from being wasted. Shrinking the cache itself is the job of KV Cache Compression.

## Memory Sharing Across Requests

Paged Attention also enables an important optimization: memory sharing.

Let's say two users ask the same question. The input tokens (the question) are the same for both requests. With Paged Attention, both requests can share the same blocks for the input tokens, because the Key and Value for those tokens will be identical.

Instead of storing two copies, the system stores one copy and both requests point to the same blocks in their block tables. This saves even more memory.

This is especially useful in scenarios like:

- Parallel sampling: Sometimes we want the model to generate multiple different responses for the same question, so we can pick the best one. Since the question is the same for all responses, the input blocks can be shared across all of them.
- Beam search: Sometimes the model explores multiple possible completions at the same time to find the best one. Again, the shared input can be stored once and reused across all the parallel sequences.

In these cases, memory sharing significantly reduces the total memory needed.

This idea of sharing identical prefixes is taken even further by SGLang, which organizes shared text in a radix tree to match shared prefixes even more precisely.

Paged Attention is the core idea behind vLLM, the popular high-throughput serving engine. We have a detailed blog on vLLM that explains how it works. The same block-based idea shows up in NVIDIA's engine under the name paged KV cache, and we have a detailed blog on how TensorRT-LLM works that covers it end to end.

Now, we have understood Paged Attention and how it borrows the idea of paging from operating systems to manage KV Cache memory efficiently, eliminate waste, and serve more users at the same time.

In the next blog, we will learn about Continuous Batching, which pairs with Paged Attention to keep the GPU busy by adding new requests to the batch the moment any old request finishes.

### Does Paged Attention make the KV Cache smaller?

No. Paged Attention does not make the KV Cache itself smaller. It only stops the memory around it from being wasted. Shrinking the cache itself is the job of KV Cache Compression.

### Why can't the system reserve the exact memory needed for each request?

Because the system does not know in advance how long the response will be. A simple question may need a 20-token response, while a complex one may need 2,000 tokens. So, the traditional approach reserves memory for the maximum possible length, and a large portion of it goes unused.

### Does Paged Attention remove all memory waste?

Almost. External waste is eliminated, because blocks do not need to be next to each other and any free block can be used. Internal waste is nearly eliminated, since memory is allocated block by block. The only waste left is in the last block, which will not always be completely full.

### Is Paged Attention the same thing as vLLM?

No. Paged Attention is a technique, and vLLM is a popular high-throughput serving engine built on it. Paged Attention is the core idea behind vLLM. The same block-based idea also shows up in NVIDIA's TensorRT-LLM under the name paged KV cache.

### How does Paged Attention work with Continuous Batching?

Continuous Batching pairs with Paged Attention to keep the GPU busy. It adds new requests to the batch the moment any old request finishes. Paged Attention makes room for these extra requests by using memory much more efficiently.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# What is RLHF? Reinforcement Learning from Human Feedback Explained
URL: https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf
Published: 2026-05-14
Author: Amit Shekhar

What is RLHF? Reinforcement Learning from Human Feedback Explained

# What is RLHF? Reinforcement Learning from Human Feedback Explained

Authors
: - Name
: Amit Shekhar
Published on
: May 14, 2026

RLHF (Reinforcement Learning from Human Feedback) is a training technique where we teach a Large Language Model to produce the responses that humans prefer. We collect human preferences and turn them into a reward signal that guides further training.

In this blog, we will learn about Reinforcement Learning from Human Feedback (RLHF), the training technique that turns a raw pre-trained LLM into a helpful, honest, and safe assistant by teaching it from human preferences.

We will cover the following:

- What is RLHF?
- Why we need RLHF
- The Big Picture
- Stage 1: Supervised Fine-Tuning (SFT)
- Stage 2: Training the Reward Model
- Stage 3: RL Fine-Tuning with PPO
- The KL Penalty
- Putting It All Together
- Reward Hacking
- Common Mistakes
- Best Practices
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is RLHF?

RLHF (Reinforcement Learning from Human Feedback) is a training technique where we teach a Large Language Model (LLM) to produce responses that humans prefer, by collecting human preferences and converting them into a reward signal that guides further training.

In simple words, we let the model generate responses, we ask humans which response is better, and we update the model so that its future responses look more like the preferred ones.

RLHF = Reinforcement Learning + Human Feedback

Let's decode each part.

- Reinforcement Learning (RL) is a way of training a model where it learns by trial and error. The model takes an action, receives a reward, and adjusts its behavior to earn more reward over time. We have a detailed blog on Reinforcement Learning that goes deeper into this.
- Human Feedback means the reward does not come from a fixed automatic metric. It comes from real humans who compare model outputs and pick the better one.

So, RLHF is reinforcement learning, but the reward signal is shaped by what humans actually want. That is the whole idea.

This idea started with the 2017 paper Deep RL from Human Preferences, which taught games and robots this way, and OpenAI later brought it to language models in the InstructGPT paper, the work that led directly to ChatGPT. We have a detailed blog on Decoding InstructGPT that walks through that paper step by step.

## Why we need RLHF

A pre-trained LLM is trained to predict the next token (a token is a small chunk of text, i.e. a word or a part of a word) from a huge amount of internet text. After pre-training, the model knows a lot about language and the world. But it does not know how to be a good assistant.

If we just ask a pre-trained model "How do I bake a cake?", it can continue with another question, or with a list of recipe headlines, or with random text that looks like a web page. It is not because the model is broken. It is because the model was only trained to imitate text on the internet, not to be helpful.

We need a way to teach the model:

- Be helpful, not random.
- Follow instructions.
- Be honest, not make things up.
- Be safe, not produce harmful content.
- Be clear, not overly verbose.

These goals are very hard to write down as a fixed rule or a fixed loss function. There is no formula that says "this answer is helpful and that one is not".

But humans can easily look at two answers and say which one is better.

So, here comes RLHF to the rescue. RLHF is the bridge that takes simple human judgments like "Answer A is better than Answer B" and turns them into a training signal for the model.

Let's take a simple analogy for the sake of understanding. Imagine a new chef who has read every cookbook in the world. The chef knows a lot of recipes, but does not know what real customers actually like. So, the restaurant gives the chef a chance to cook many dishes, lets customers taste two versions side by side, and asks them to pick the one they prefer. Over time, the chef learns to cook the food that customers actually love. RLHF is exactly this, but the chef is the LLM and the customers are the human labelers.

## The Big Picture

Before we go into the details, let's understand the big picture.

RLHF is not a single training step. It is a pipeline with three stages.

In simple words:

RLHF = SFT + Reward Model + RL Fine-Tuning.

Here is a high-level view of the pipeline:

```
+------------------------+
|  Pre-trained Base LLM  |
+-----------+------------+
            |
            v
+------------------------+
|  Stage 1: SFT          |   <- learn to follow instructions
+-----------+------------+
            |
            v
+------------------------+
|  Stage 2: Reward Model |   <- learn what humans prefer
+-----------+------------+
            |
            v
+------------------------+
|  Stage 3: RL Fine-Tune |   <- improve LLM using reward
+-----------+------------+
            |
            v
+------------------------+
|  Aligned LLM (final)   |
+------------------------+

```

Each stage has a clear job:

- Stage 1 (SFT) teaches the model to behave like an assistant.
- Stage 2 (Reward Model) teaches a separate model to score answers the way a human would.
- Stage 3 (RL Fine-Tuning) uses that reward model to push the LLM toward higher-scoring answers.

We will learn later in the blog why we must start with SFT and not jump straight to the Reward Model or RL Fine-Tuning.

Now, let's decode each stage.

## Stage 1: Supervised Fine-Tuning (SFT)

The first stage of RLHF is Supervised Fine-Tuning, often called SFT.

Supervised Fine-Tuning is the step where we take the pre-trained base LLM and fine-tune it on a hand-picked dataset of high-quality prompt-response pairs written by humans.

The dataset is typically small but very high quality - around `10,000` to `100,000` carefully written prompt-response examples. We show the model many examples of "this is a good question, and this is a good answer", and we train it to imitate that style. This is classic supervised learning - we have inputs and we have correct outputs, and the model learns to map one to the other.

The dataset looks like this:

```
Prompt:    "Explain photosynthesis to a 10 year old."
Response:  "Photosynthesis is how plants make their food.
[…308ln elided…]

## Quick Summary

Let's recap what we have learned.

- RLHF stands for Reinforcement Learning from Human Feedback. It is the technique that aligns a pre-trained LLM with what humans actually want.
- RLHF = SFT + Reward Model + RL Fine-Tuning.
- Stage 1: SFT teaches the base model to follow instructions using human-written prompt-response pairs.
- Stage 2: Reward Model is trained on pairs of responses where humans picked the better one. It learns to score any response the way a human would.
- Stage 3: RL Fine-Tuning uses PPO to update the LLM so its responses earn higher scores from the Reward Model.
- The KL penalty keeps the LLM close to the SFT model and prevents it from drifting into nonsense.
- Reward hacking is the model finding tricks that fool the Reward Model. Good labeling, KL penalty, and iteration are the main defenses.
- Common mistakes include skipping SFT, using a weak Reward Model, ignoring the KL penalty, and treating the Reward Model as ground truth.
- Best practices are strong SFT, high-quality preference data, careful KL tuning, iterative rounds, real human evaluation beyond the reward score, and balanced safety plus helpfulness data.

This is how RLHF turns a raw pre-trained LLM into a helpful, honest, and safe assistant.

### Why does RLHF ask humans to compare answers instead of writing perfect ones?

Humans are much better at comparing two answers than at writing the perfect answer from scratch. We also cannot write enough examples to cover every possible question and nuance. So, RLHF turns simple judgments like "Answer A is better than Answer B" into a training signal for the model.

### How many models are involved in RLHF with PPO?

Four models work together. The Policy Model is the LLM being trained. The Value Model, or Critic, predicts expected rewards to compute the advantage. The Reward Model scores responses based on human preferences, and the Reference Model is a frozen copy of the SFT model, used for the KL penalty.

### Is PPO the only way to do the RL stage of RLHF?

No. PPO is the most commonly used algorithm, but newer algorithms like GRPO remove the Value Model entirely by computing the baseline from a group of sampled responses, bringing

# What is a Vision Transformer (ViT) and How Does It Work?
URL: https://outcomeschool.com/blog/decoding-vision-transformer-vit
Published: 2026-04-15
Author: Amit Shekhar

What is a Vision Transformer (ViT) and How Does It Work?

# What is a Vision Transformer (ViT) and How Does It Work?

Authors
: - Name
: Amit Shekhar
Published on
: April 15, 2026

A Vision Transformer (ViT) treats an image the same way a transformer treats a sentence. It splits the image into small patches, treats each patch as a token, and processes them with a transformer to classify the image.

In this blog, we will learn about the Vision Transformer (ViT) by decoding how it splits an image into patches, turns those patches into tokens, and processes them with a transformer to classify the image.

Before Vision Transformers, image classification was dominated by Convolutional Neural Networks (CNNs) like ResNet, VGG, and etc. The transformer architecture was only used for text. Then, in 2020, Google researchers asked a simple question - "Can we apply the transformer architecture directly to images?" The answer was yes, and the Vision Transformer (ViT) was born in the paper titled "An Image is Worth 16x16 Words".

When we hear "applying transformers to images", it sounds complex. But do not worry. If we break it down into its individual parts, every single piece is simple.

Our goal is to decode ViT so clearly that by the end, we will be able to explain how ViT works to anyone.

We will cover the following:

- The Big Picture
- Decoding Step 1: Splitting the Image into Patches
- Decoding Step 2: Patch Embedding
- Decoding Step 3: The CLS Token
- Decoding Step 4: Position Embeddings
- Decoding Step 5: The Transformer Encoder
- Decoding Step 6: The Classification Head
- Putting It All Together
- ViT vs CNN
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

ViT treats an image the same way a transformer treats a sentence. A sentence is a sequence of words (tokens). ViT splits an image into a sequence of small patches and treats each patch as a token. These patch tokens are then processed by a standard transformer encoder, just like text tokens.

In simple words:

Vision Transformer = Split image into patches (like words) + Process patches with a transformer (like processing a sentence).

Think of a jigsaw puzzle. We take a complete image, cut it into small square pieces, line up the pieces in a row, and hand them to the transformer. The transformer then looks at all the pieces together, understands how they relate to each other, and tells us what the image is.

The idea behind ViT is simple - if transformers work well for sequences of text tokens, they should also work for sequences of image patches.

A sentence like "the cat sat on the mat" is a sequence of 6 tokens. In the same way, an image becomes a sequence of patches. For example, a 224x224 image cut into 16x16 patches gives us 196 patches. Each patch is treated as a "visual word". The transformer does not care whether the tokens are words or image patches. It just processes the sequence and learns the relationships.

Now, let's decode ViT step by step.

## Decoding Step 1: Splitting the Image into Patches

The first thing ViT does is split the input image into small non-overlapping square patches.

First, we take the input image. A standard ViT uses 224x224 pixel images. Then, we divide the image into non-overlapping square patches, each of size 16x16 pixels. Since 224 / 16 = 14, we get 14 patches along each side of the image. So the image becomes a 14 x 14 grid of patches, which gives us 14 x 14 = 196 patches in total.

Think of it like a chessboard, but with 14 rows and 14 columns instead of 8. Each square of this 14 x 14 board is one patch.

Now, a natural question arises - why 16x16? It is a sweet spot. Smaller patches (say 8x8) give us more tokens and finer detail, but the sequence length grows quickly and self-attention becomes very expensive. Bigger patches (say 32x32) give us fewer tokens and faster training, but the model loses fine-grained detail. 16x16 balances both, and that is why it became the default.

```
Original Image (224 x 224 pixels)
+----+----+----+----+----+ ... +----+
|P1  |P2  |P3  |P4  |P5  |     |P14 |
+----+----+----+----+----+ ... +----+
|P15 |P16 |P17 |P18 |P19 |     |P28 |
+----+----+----+----+----+ ... +----+
|    |    |    |    |    |     |    |
  ...  ...  ...  ...  ...       ...
+----+----+----+----+----+ ... +----+
|P183|P184|P185|P186|P187|     |P196|
+----+----+----+----+----+ ... +----+

Each patch is 16 x 16 pixels
Total: 14 x 14 = 196 patches

```

Each patch captures a small region of the image. Some patches contain parts of the main object, some contain background, and some contain edges or textures.

This is how the image is broken down into a sequence. Now, let's move to the next step.

## Decoding Step 2: Patch Embedding

Now, we have 196 patches. But the transformer does not understand raw pixels. It expects each token to be a fixed-size vector of numbers, called an embedding.

Each patch is a 16x16 pixel region with 3 color channels (RGB). So each patch is a small 3D block of 16 x 16 x 3 = 768 numbers, which is then flattened into a single vector of 768 numbers.

To turn each patch into a token that the transformer can process, we use a linear projection - a simple matrix multiplication that converts these 768 numbers into a vector of a fixed dimension (768 for ViT-Base). Even though the input and output dimensions are the same here, this is not an identity mapping. The projection matrix is learned during training so that the output embedding captures the useful visual features of the patch, not just raw pixel values.

```
Patch (16 x 16 x 3, a 3D block of pixels)
        |
        v
[Flatten into a 768-dimensional vector]
        |
        v
[Linear Projection (768 -> 768)]
        |
        v
Patch Embedding (768-dimensional vector)

```

In practice, this linear projection is implemented as a convolution with kernel size 16x16 and stride 16. Do not worry if this sounds heavy. It is just an implementation detail, not a new concept - it is mathematically the same as cutting the image into 16x16 patches and projecting each one.

After this step, we have 196 patch embeddings, each of dimension 768. This is our sequence of "visual tokens", ready for the transformer.

This was all about converting patches to embeddings. Now, let's decode the next piece.

## Decoding Step 3: The CLS Token

Now, a natural question arises - once the transformer has processed all 196 patch tokens, which token do we use to make the final prediction? Each patch only sees a small part of the image, so no single patch token fully represents the whole image.

The answer is simple: we add a special learnable token called the CLS token (short for "classification token") to the beginning of the sequence.

```
Sequence: [CLS, Patch1, Patch2, Patch3, ..., Patch196]
Total tokens: 197 (1 CLS + 196 patches)

```

The CLS token does not correspond to any image patch. It starts as a learnable vector of 768 numbers. As the transformer processes the sequence, the CLS token attends to every patch and gathers information from all of them. By the end of the transformer, the CLS token contains a global summary of the entire image.

Think of the CLS token as a class representative. Every patch is like a student in a classroom. The CLS token listens to all the students, collects their information, and speaks on behalf of the whole class when the final answer is needed.

Now, let's decode the next piece.

## Decoding Step 4: Position Embeddings

Here is the catch. When we split the image into patches and line them up as a sequence, the patches lose their spatial position. The transformer only sees a list of tokens. It does not know which patch was on the top-left and which was on the bottom-right.

But the position of a patch matters. A patch containing an eye on the top of the image and a patch containing a tail on the bottom together tell us it is a cat. If we shuffle the patches randomly, the image no longer makes sense.

So, here comes the position embedding to the rescue. For each position in the sequence (0 to 196), we add a learnable vector of 768 numbers. This vector acts like a tag that tells the transformer, "This patch came from position 5 in the original image."

```
Final input = Patch Embedding + Position Embedding

Token 0:   CLS_embedding      + Position_0
Token 1:   Patch1_embedding   + Position_1
Token 2:   Patch2_embedding   + Position_2
...
Token 196: Patch196_embedding + Position_196

```

The position embedding is simply added (element-wise) to the patch embedding. Now every token carries both "what" the patch looks like and "where" it was in the image.

Now, our sequence of 197 tokens is ready for the transformer. Let's move to the next step.

## Decoding Step 5: The Transformer Encoder

The sequence of 197 tokens (CLS + 196 patches) is passed through a standard transformer encoder. We must be knowing how a transformer encoder works from text models - the same one comes into the picture here.

We have a detailed blog on Decoding Transformer Architecture that explains the transformer encoder in depth.

The encoder consists of multiple layers, and each layer contains three main components.

1. Multi-Head Self-Attention: Each token attends to every other token. This allows the model to learn relationships between different parts of the image. For example, a patch containing a cat's ear can attend to a patch containing a cat's eye, helping the model understand that they belong to the same object. This is the heart of ViT.

2. Feed-Forward Network: A two-layer neural network applied to each token independently. This adds non-linearity and increases the model's capacity. We have a detailed blog on Feed-Forward Networks in LLMs that explains this in depth.

3. Layer Normalization and Residual Connections: Standard transformer components that help with training stability.

```
Input: 197 tokens (each 768-dimensional)
        |
        v
[Layer 1: Multi-Head Self-Attention -> Feed-Forward Network]
        |
        v
[Layer 2: Multi-Head Self-Attention -> Feed-Forward Network]
        |
        v
... (12 layers in total)
        |
        v
Output: 197 tokens (each 768-dimensional)

```

After all the layers, each token has been enriched with information from all other tokens. The CLS token, in particular, has gathered information from all 196 patches and now contains a global representation of the entire image.

This is how the transformer encoder processes our sequence of visual tokens. Now, let's move to the final step.

To learn Transformer Architecture, Multi-Head Attention, and Self-Attention in depth, check out our AI and Machine Learning Program at Outcome School.

## Decoding Step 6: The Classification Head

The final CLS token representation is passed through a classification head, which is a simple linear layer that maps the 768-dimensional vector to the number of classes.

```
CLS token output (768-dimensional)
        |
        v
[Linear Layer (768 -> 1000)]
        |
        v
Class probabilities (1000 classes)
        |
        v
Prediction: "Golden Retriever" (class with highest probability)

```

The class with the highest probability is the model's prediction. It works perfectly.

Now, we have decoded every piece of ViT. Let's put them all together to see how ViT runs end to end.

## Putting It All Together

Let's trace through the entire ViT pipeline end to end with concrete numbers for ViT-Base:

```
Input image (224 x 224 x 3 RGB)
        |
        v
[Step 1: Split into 14 x 14 = 196 patches of 16 x 16]
        |
        v
[Step 2: Patch embedding -> 196 vectors, each 768-dim]
        |
        v
[Step 3: Prepend CLS token -> 197 vectors, each 768-dim]
        |
        v
[Step 4: Add position embeddings -> 197 vectors, each 768-dim]
        |
        v
[Step 5: Transformer encoder (12 layers, 12 heads each)]
        |
        v
[Step 6: Take CLS token -> Linear (768 -> 1000)]
        |
        v
Prediction: "Golden Retriever"

```

Total parameters for ViT-Base: ~86 million.

ViT comes in three standard sizes - ViT-Base (~86M parameters, 12 layers), ViT-Large (~307M parameters, 24 layers), and ViT-Huge (~632M parameters, 32 layers). The bigger the model, the more data it needs to train well, but the better it performs once trained.

This is the complete flow of ViT from an input image to a final prediction.

A quick note for you

No matter which tech domain you work in, get familiar with these topics:

- LLM
- RAG
- MCP
- Agent
- Fine-tuning
- Quantization

We put it all together in one video:

No need to stop reading - bookmark it and watch later when you get time. Future you will thank you.

Now, let's get back to the topic.

## ViT vs CNN

Now, a natural question arises - how does ViT compare to CNNs, which have been the standard for image classification for years?

Let me tabulate the differences between ViT and CNN for your better understanding so that you can decide which one to use based on your use case.

| Property | ViT | CNN (e.g. ResNet) |
| --- | --- | --- |
| Core operation | Self-attention | Convolution |
| What each layer sees | The whole image from the very first layer | Only nearby pixels at first, more with depth |
| Built-in assumptions | Almost none, learns everything from data | Strong, assumes nearby pixels are related |
| Data requirement | Needs large datasets | Works with smaller datasets |
| Scalability | Scales well with data and compute | Scales, but less steeply at very large scale |
| Architecture | Uniform (same attention blocks) | Varied (different block types) |
| Image understanding | Understands global relationships | Understands local patterns first |

CNNs come with a built-in assumption that nearby pixels are more related than distant pixels. This assumption acts like a head start - the CNN does not have to learn this from scratch. ViT does not have this head start. It learns all spatial relationships from the data itself. This is why ViT needs more data to train well, but once trained on enough data, it can outperform CNNs because it is not limited by any built-in assumption.

Let's put this into perspective with real numbers:

- When trained only on ImageNet (~1.3 million images), ViT performs worse than a well-tuned ResNet of similar size.
- When pre-trained on JFT-300M (~300 million images) and then fine-tuned on ImageNet, ViT beats the best CNNs of the time.
- The lesson is simple - more data, more ViT wins. With small data, CNNs win because of their built-in head start.

## Quick Summary

In one line:

ViT = image patches + transformer encoder.

Let's recap what we have decoded:

- Vision Transformer (ViT) applies the transformer architecture to images by treating image patches as tokens, just like words in a sentence.
- The process is - split the image into 16x16 patches, project each patch into an embedding, add a CLS token and position embeddings, process through a transformer encoder, and use the CLS token for classification.
- Patch embedding converts each 16x16x3 patch into a 768-dimensional vector using a linear projection.
- The CLS token aggregates information from all patches and is used for the final classification.
- Position embeddings tell the transformer where each patch came from in the original image.
- The transformer encoder uses multi-head self-attention so every patch can attend to every other patch, learning global relationships from the very first layer.
- ViT vs CNN: ViT looks at the whole image from the very first layer, while CNNs look at nearby pixels first. ViT needs more data but scales better.
- ViT has become the foundation for many modern vision models, including CLIP, DINO, self-supervised methods like I-JEPA, and the vision encoders used in multimodal models.

So we have learned about the Vision Transformer (ViT), how it splits an image into patches, processes them with a transformer encoder, and uses the CLS token to make the final prediction. We have also seen how ViT compares to CNNs and why it scales so well with more data.

### Does ViT work well on small datasets?

No. ViT needs large datasets to train well. When trained only on ImageNet, which has about 1.3 million images, ViT performs worse than a well-tuned ResNet of similar size. CNNs win with small data because they assume nearby pixels are related, which gives them a head start.

### Why does ViT use 16x16 patches?

16x16 is a sweet spot between detail and cost. Smaller patches give more tokens and finer detail, but the sequence grows quickly and self-attention becomes very expensive. Bigger patches give fewer tokens and faster training, but the model loses fine-grained detail. That is why 16x16 became the default.

### Does ViT use a transformer decoder?

No. ViT uses a standard transformer encoder, the same one used for text tokens. The encoder lets every patch attend to every other patch. The final CLS token is then passed through a simple linear classification head to make the prediction.

### Does ViT know where each patch came from in the image?

Only because of position embeddings. When the patches are lined up as a sequence, they lose their spatial position, so a learnable position vector is added to each patch embedding. Without it, the transformer would not know which patch was on the top-left and which was on the bottom-right.

### Which modern models are built on ViT?

ViT has become the foundation for many modern vision models. These include CLIP, DINO, self-supervised methods like I-JEPA, and the vision encoders used in multimodal models.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-392 and 701-1072 of 1072; 308 middle lines (15.7KB) elided. Read artifact://72 for full output]
