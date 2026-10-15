> Source: https://outcomeschool.com/blog/kv-cache-compression

# What is KV Cache Compression?
URL: https://outcomeschool.com/blog/kv-cache-compression
Published: 2026-09-12
Author: Amit Shekhar

What is KV Cache Compression?

# What is KV Cache Compression?

Authors
: - Name
: Amit Shekhar
Published on
: September 12, 2026

KV Cache Compression is a set of techniques that shrink the memory an AI model uses to remember the conversation while it is writing its reply, so that the model can handle longer text with less memory.

In this blog, we will learn about KV Cache Compression, the set of techniques that shrink the memory an AI model uses to remember the conversation while it is writing its reply. We will also see how an LLM writes one token at a time, what the KV Cache is and why we need it, why this cache becomes so huge, how quantization stores the same memory in fewer bits, how we can throw away the tokens that do not matter, how sharing across attention heads reduces the cache, how the cache can be squeezed into a small hidden vector, and when to use which one.

We will cover the following:

- What is an LLM and how it writes text?
- What is Attention?
- What is the KV Cache?
- Why the KV Cache becomes huge
- What is KV Cache Compression?
- Approach 1: Quantization
- Approach 2: Token Eviction
- Approach 3: Sharing Keys and Values across Heads
- Approach 4: Low-Rank Compression
- Comparison of the approaches
- When to use which one

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is an LLM and how it writes text?

An LLM (Large Language Model) is an AI model that reads text and writes text. ChatGPT, Claude, Gemini, all of them are based on LLMs.

An LLM learns by reading a huge amount of text from the internet. This learning process is called training. Once the training is done, we can ask the model questions, and it writes the answers.

The most important thing to know about an LLM is that it does not write the full reply in one shot. It writes one small piece at a time. This small piece is called a token. For the sake of understanding, we can think of a token as a word.

Let's say we ask the model, "What is the capital of France?"

The model writes "The". Then it looks at everything so far and writes "capital". Then it looks at everything so far again and writes "of". Then "France". Then "is". Then "Paris".

So, to write every new token, the model has to look back at all the previous tokens. This looking back is done by something called Attention.

Now, let's understand Attention.

## What is Attention?

Attention is the way a model decides which previous tokens are important for writing the next token.

In simple words, Attention is looking back and picking what matters.

Let's say the model is writing the sentence, "The dog was tired, so it went to sleep." When the model reaches the word "it", it needs to know that "it" refers to "the dog". So, the model pays more attention to "dog" and less attention to the other words.

Now, the question is, how does the model do this?

Every token is converted into three things:

- Query (Q): What the current token is looking for.
- Key (K): What each previous token offers, like a label.
- Value (V): The actual information that each previous token carries.

Each of these is just a list of numbers. In AI, a list of numbers is called a vector. So, every token has a Query vector, a Key vector, and a Value vector.

Let's take an analogy. Suppose we are in a library. We have a question in our mind. This is the Query. Every book has a title on its spine. This is the Key. The content inside the book is the Value.

We compare our question with the title of every book. The books whose titles match our question well get more attention. Then we read the content of those books and combine what we learned.

This is exactly what Attention does. The Query of the new token is compared with the Key of every previous token. Based on how well they match, the Values are combined and passed forward to help write the next token.

We have a detailed blog on Math behind Attention - Q, K, and V that explains this step by step.

One more thing to notice: A model does this Attention not just once. It has many layers stacked one after another, and every layer has many attention heads. Each head is like a separate reader looking for a different thing. One head looks for grammar, one looks for names, one looks for what "it" refers to, and etc.

Now that we have learned about Attention, it's time to learn about the KV Cache.

To master Q, K, V Matrices, Self-Attention and Multi-Head Attention, and build a Large Language Model (LLM) from scratch, check out our AI and Machine Learning Program at Outcome School.

## What is the KV Cache?

Now, let's see the problem. For every new token, the model needs the Key and the Value of every previous token.

Let's say the model has already written 100 tokens and is now writing the 101st token. It needs the Keys and Values of all 100 previous tokens. Without any memory, the model would calculate the Keys and Values of all the 100 tokens again. Then for the 102nd token, it would calculate for all 101 tokens again. And so on.

This is a huge waste. The Key and Value of a token never change once they are computed. So, why calculate them again and again?

So, here comes the KV Cache to the rescue.

KV Cache = Key + Value + Cache

A cache is just a memory where we store something so that we do not have to compute it again.

The KV Cache is the memory where the model stores the Keys and Values of every previous token so that it can reuse them while writing the next token.

Now, when the model writes the 101st token, it only calculates the Key and Value of the newest token, adds them to the cache, and reads everything else from the cache.

This makes text generation very fast. Problem Solved!

But, here is the catch. This cache grows with every single token. And it grows very fast.

## Why the KV Cache becomes huge

The best way to learn this is by taking an example.

Before jumping into the example, we must know two small things. A bit is the smallest unit of memory in a computer, it is either 0 or 1. And 8 bits make 1 byte.

Let's take a model with the following. These numbers are close to the real numbers of Llama 2, a popular open-source model:

- 32 layers
- 32 attention heads in each layer
- Each head has a Key vector of 128 numbers and a Value vector of 128 numbers
- Each number is stored in 16 bits, which means 2 bytes

Now, let's calculate how much memory one token needs in the cache.

For one head in one layer, we store 128 numbers for the Key and 128 numbers for the Value. That is 256 numbers.

For 32 heads, that is 256 x 32 = 8,192 numbers.

For 32 layers, that is 8,192 x 32 = 262,144 numbers.

Each number takes 2 bytes. So, one token needs 262,144 x 2 = 524,288 bytes. That is 0.5 MB. Here, 1 MB is about a million bytes, and 1 GB is about a thousand MB.

Let's see the code for this calculation as below:

```python
layers = 32
heads = 32
head_dim = 128
bytes_per_number = 2

# Key and Value, so multiply by 2
per_token = 2 * layers * heads * head_dim * bytes_per_number
print(per_token / (1024 * 1024))  # 0.5 MB

```

Here, we are multiplying the number of layers, the number of heads, the size of each head, and the bytes per number. We multiply by 2 in the beginning because we store both the Key and the Value.

Half an MB for one token does not sound like much. But now, let's see the full picture.

Suppose the user has a conversation of 4,000 tokens. That is 4,000 x 0.5 MB = 2 GB.

Suppose the user pastes a long document of 100,000 tokens. That is 100,000 x 0.5 MB = 50 GB. Just for the cache of one user.

The model runs on a GPU, a special chip that is very fast at doing math. A GPU has a fixed amount of memory, usually between 24 GB and 80 GB. And a big part of that memory is already taken by the model itself.

Now, suppose 100 users are talking to the model at the same time on the same GPU. Each one needs their own cache. The memory required is way beyond what any GPU has.

This is the problem. The KV Cache grows with the length of the text and with the number of users, and it eats the memory of the GPU.

And, it is not just about memory. For every new token, the model has to read the full cache from memory. A bigger cache means more time to read, which means slower generation.

We needed a solution for that, and KV Cache Compression was introduced to solve this problem.

One part of the fix is to stop wasting the memory we already have, and we have a detailed blog on Paged Attention that explains how a serving system does that. The other part is to make the cache itself smaller, which is what we will learn now.

## What is KV Cache Compression?

KV Cache Compression is the set of techniques that make the KV Cache smaller while keeping the quality of the model output almost the same.

In simple words, we want to store the same memory of the conversation in less space.

There are different ways to do this. Some of them can be applied to an existing model, and some need to be built into the model before training. Let's understand each of them one by one, starting from the simplest.

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

## Approach 1: Quantization

Quantization means storing each number in the cache using fewer bits.

Let's take an example. Suppose we want to write down the height of a person. We can write 175.4837 cm. Or we can write 175 cm. The second one takes less space to write, and for most purposes, it is good enough.

This is what quantization does. Normally, each number in the KV Cache is stored in 16 bits. With quantization, we store it in 8 bits, or even 4 bits.

Let's see with an example. Suppose the Key vector has these numbers:

```
[0.31, -0.72, 0.05, 0.98]

```

To store them in fewer bits, we first find the biggest value, which is 0.98. Then we scale every number to fit in a small range of whole numbers, from -127 to 127, which fits in 8 bits, as below:

```python
values = [0.31, -0.72, 0.05, 0.98]
scale = max(abs(v) for v in values) / 127

quantized = [round(v / scale) for v in values]
print(quantized)  # [40, -93, 6, 127]

```

Here, we are dividing every number by the scale and rounding it to the nearest whole number. Now, every number is a small whole number that fits in 8 bits instead of 16 bits. We just store the scale separately, so that we can get back close to the original values when needed.

- 16 bits to 8 bits: the cache becomes half the size.
- 16 bits to 4 bits: the cache becomes one-fourth the size.

Advantage: Very simple to add. We do not throw away any token. The quality loss is very less.

Disadvantage: Below 4 bits, the rounding error becomes big, and the model starts giving worse answers. So, there is a limit to how far we can go.

One more thing to notice: Keys and Values do not behave the same way. In Keys, a few positions always carry very big numbers, and normal rounding does not handle them well. So, good techniques like KIVI quantize Keys and Values in slightly different ways to keep the error small. Do not worry about the details, just remember that Keys and Values are treated differently for the best result.

The issue with this approach is that even with 4 bits, the cache still grows with every token. For very long conversations, it is still too big. Let's see how the next approach solve this issue.

If we want to go deep into Quantization and Optimizations, Model Compression, and KV Cache, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

## Approach 2: Token Eviction

Token Eviction means throwing away the Keys and Values of the tokens that are not important.

Eviction simply means kicking something out. Here, we kick unimportant tokens out of the cache.

Let's take an analogy. Suppose we are reading a 500-page novel. We do not remember every single sentence. We remember the important characters, the important events, and the last few pages we just read. Everything else, we forget. And still, we understand the story perfectly.

The same idea applies here. Not every previous token is equally important for writing the next token. When the model computes Attention, most of the attention goes to a few tokens. The rest of the tokens get almost zero attention.

So, why keep them in the cache?

Now, the question is, how do we know which tokens are important?

The answer is in the Attention itself. Every time the model writes a new token, it computes how much attention every previous token receives. We can keep a running total of this for every token. The tokens with the highest total are the important ones. These are called heavy hitters. This is what the H2O (Heavy Hitter Oracle) technique does.

So, the rule is simple:

- Fix a budget, let's say 1,000 tokens.
- Always keep the most recent tokens, because the recent context is almost always important.
- From the older tokens, keep only the heavy hitters.
- Throw away the rest.

Now, the cache never grows beyond 1,000 tokens, no matter how long the conversation is.

But, here is the catch. There is one very interesting thing that was found. The very first few tokens of the text always receive a huge amount of attention, no matter what they are. Even if the first token is just a "start" marker with no meaning.

Why? Because Attention is like distributing 100 percent among all the previous tokens. The total must always be 100 percent. When no previous token is really useful, the model still has to put that attention somewhere. It learns to dump it on the first token. So, the first token acts like a sink where the unwanted attention goes.

Here comes the Attention Sink into the picture.

If we throw away the first token, the model output becomes meaningless. This was found by the StreamingLLM technique. So, the final rule is: always keep the first few tokens, always keep the recent tokens, and choose the heavy hitters from the middle.

Advantage: The cache has a fixed size. It does not matter how long the conversation is. This is the only approach that truly solves the unlimited growth problem.

Disadvantage: Once a token is thrown away, it is gone forever. If the user later asks about something that was in an evicted token, the model cannot remember it. This is a real loss of information. So, it works well for tasks like chatting and summarizing, but it fails for tasks that need exact recall, like "find the phone number mentioned on page 40".

The issue with this approach is the risk of forgetting something important. Let's see how the next approach solve this issue without throwing away anything.

## Approach 3: Sharing Keys and Values across Heads

Till now, we have compressed the cache after the model is trained. This approach is different. Here, we change the design of the model itself before training.

Remember that every layer has many attention heads, and every head has its own Key and Value. In our example, 32 heads means 32 sets of Keys and Values per layer.

Now, the question is, do all 32 heads really need their own separate Keys and Values?

The answer is no. It was found that many heads can share the same Keys and Values and still work well. Only the Query needs to be separate for each head.

Let's take an analogy. Suppose 32 students are in a library. Each student has a different question in mind. This is the Query. But, the library does not need 32 separate copies of every book. All 32 students can look at the same shelf, the same book titles, and the same book contents. Only their questions are different.

There are two ways to do this:

- Multi-Query Attention (MQA): All the heads share one single Key and one single Value. In our example, 32 heads share 1 set. The cache becomes 32 times smaller.
- Grouped-Query Attention (GQA): Heads are divided into groups, and each group shares one Key and one Value. In our example, 32 heads divided into 8 groups means 8 sets instead of 32. The cache becomes 4 times smaller.

MQA compresses more but loses some quality. GQA is the middle ground. It gets most of the memory saving with almost no loss in quality. This is why most modern models like Llama 3, Mistral, and Gemma use GQA.

Advantage: No token is thrown away. No rounding error. The saving is built into the model, so it works all the time with no extra work while the model is running.

Disadvantage: This must be decided before training the model. We cannot apply it to an already trained model without retraining it. And, the cache still grows with every token, just at a slower rate.

The issue with this approach is that the saving is limited by the number of groups. Let's see how the next approach compress even further.

To learn Grouped Query Attention, KV Cache, and LLM Inference Engineering in depth, check out our AI and Machine Learning Program at Outcome School.

## Approach 4: Low-Rank Compression

Low-Rank Compression means storing a small compressed version of the Key and Value, and expanding it back only when needed.

A low rank means the same information can be held in fewer numbers.

Let's take an analogy. Suppose we want to send a big photo to a friend. Instead of sending the full photo, we send a zipped file. The friend unzips it when they want to see it. The zipped file takes less space, and the photo is almost the same.

Here, instead of storing the full Key and Value of every token, the model stores one small vector called a latent vector. Latent simply means hidden. It is a hidden, compressed form of the Keys and Values. When the model needs the Key and Value, it expands the latent vector back using a small set of numbers it learned during training.

Let's see the numbers. In our example, each head stores 128 numbers for the Key and 128 numbers for the Value. For 32 heads, that is 8,192 numbers per layer per token. With Low-Rank Compression, the model stores a single latent vector of, let's say, 512 numbers per layer per token. That is 16 times smaller.

This is what the Multi-Head Latent Attention (MLA) technique does. It was introduced by DeepSeek in their DeepSeek-V2 model, and it is also used in DeepSeek-V3.

Now, you must be thinking, if we compress and then expand, do we not lose quality?

This is the beauty of this approach. The model is trained with this compression from the beginning. So, the model learns to put only the useful information inside the latent vector. Nothing important is lost.

Advantage: Huge memory saving. No token is thrown away. The quality is as good as the full Attention, and in some cases even better.

Disadvantage: Like GQA, this must be built into the model before training. We cannot apply it to an existing model. And, the model has to do a little extra computation to expand the latent vector.

DeepSeek-V4 pushes this idea even further by merging several consecutive tokens into one compressed cache entry. We have a detailed blog on Decoding DeepSeek-V4 that covers this end to end.

Now, we have understood all the four approaches.

## Comparison of the approaches

One more thing to notice: These approaches are not competing with each other. They can be combined. A model can use MLA in its design, then we can apply quantization to the latent vectors, and then apply token eviction on top of that.

Let me tabulate the differences between these approaches for your better understanding.

| | Quantization | Token Eviction | Sharing across Heads | Low-Rank Compression |
| --- | --- | --- | --- | --- |
| How it saves memory | Fewer bits per number | Fewer tokens stored | Fewer Keys and Values per layer | Smaller vector per token |
| Needs retraining | No | No | Yes | Yes |
| Throws away tokens | No | Yes | No | No |
| Typical saving | 2x to 4x | Fixed cache size | 4x to 8x | 10x or more |
| Quality loss | Very less | Depends on the task | Very less | Almost none |
| Example | KIVI | H2O, StreamingLLM | GQA, MQA | MLA (DeepSeek) |

## When to use which one

So, based on our use case:

- If we are running an existing model and want a quick memory saving, use Quantization. It is the easiest thing to add.
- If we have a very long conversation, or text that keeps coming in without an end, use Token Eviction with Attention Sinks.
- If we need exact recall of everything in a long document, do not use Token Eviction. Use Quantization, or a model that has GQA or MLA built in.
- If we are training a new model, use GQA or MLA in the design from day one.
- If we want the maximum saving, combine them. Start with a model that has MLA or GQA, then quantize the cache, and then evict if the task allows.

This is how KV Cache Compression lets an LLM remember a very long conversation, serve many users at the same time, and write faster, and that too without needing a bigger GPU.

Now, we must have understood KV Cache Compression.

### Does a smaller KV Cache also make text generation faster?

Yes. For every new token, the model has to read the full cache from memory. A bigger cache means more time to read, which means slower generation. So, a smaller cache helps the model write faster, not just use less GPU memory.

### Is Paged Attention a KV Cache Compression technique?

No. Paged Attention and KV Cache Compression solve two different parts of the memory problem. Paged Attention stops wasting the memory we already have in a serving system. KV Cache Compression makes the cache itself smaller.

### Can we use more than one KV Cache Compression approach together?

Yes. These approaches are not competing with each other, and they can be combined. A model can use MLA in its design, then we can apply quantization to the latent vectors, and then apply token eviction on top of that for the maximum saving.

### Why should we never evict the first tokens from the cache?

The very first few tokens always receive a huge amount of attention, no matter what they are. The model learns to dump its unwanted attention there, so they act like an attention sink. If we throw away the first token, the model output becomes meaningless.

### Can we add Grouped-Query Attention to an already trained model?

No. Sharing Keys and Values across heads, like in GQA or MQA, must be decided before training the model. We cannot apply it to an already trained model without retraining it. The same is true for Low-Rank Compression like MLA.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
