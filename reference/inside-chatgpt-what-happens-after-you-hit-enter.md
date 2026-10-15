> Source: https://outcomeschool.substack.com/p/inside-chatgpt-what-happens-after

# Inside ChatGPT: What Happens After You Hit Enter
URL: https://outcomeschool.substack.com/p/inside-chatgpt-what-happens-after
Published: 2026-03-07
Author: Outcome School

Inside ChatGPT: What Happens After You Hit Enter

### What Actually Happens When You Type a Prompt into ChatGPT?

Outcome School

Mar 07, 2026

I’m Amit Shekhar from Outcome School, where I teach AI and Machine Learning.

Let’s get started.

You type a question. Hit enter. And within seconds, ChatGPT gives you a response.

It feels like magic. But here’s the truth: ChatGPT is not reading your words the way you think.

It's not thinking through your question. It’s playing a probability game. One word at a time.

Let me show you what’s really happening.

A quick note: ChatGPT is just an interface used to interact with a large language model. So, as you read this post, keep this in mind.

Step 1: Your Text Gets Converted Into Tokens

When you hit send, ChatGPT doesn’t see your sentence as words.

It sees tokens.

Example:

```
Prompt: "What is machine learning?"
```

Gets broken into:

```
["What", "is", "machine", "learning", "?"]
```

Tokens are the smallest units the model processes. Sometimes they’re full words. Sometimes they’re pieces of words. Sometimes they’re just punctuation.

Why tokens, not words?

Because language is messy. Models need a consistent way to handle:

- Common words (fast to process)
- Rare words (broken into subwords)
- Typos, slang, code, emojis

Step 2: Tokens Become Numbers

Computers don’t speak English. They speak math.

So every token gets converted into a number called a token ID.

Example:

```
"What"     → 102
"is"      → 2
"machine" → 834
"learning"→ 919
"?"        → 43
```

Your sentence is now:

```
[102, 2, 834, 919, 43]
```

But raw numbers aren’t enough.

The model needs context. It needs to know that “king” and “queen” are related. That “Paris” and “France” have a connection.

So these token IDs get transformed into embeddings, high-dimensional vectors (lists of hundreds of numbers) that capture semantic meaning.

In this space:

- Similar words cluster together
- Relationships between concepts are preserved
- The model can do math with meaning

Step 3: The Transformer Reads Your Prompt

Your tokens enter the Transformer, a neural network architecture that changed everything in AI.

You might have heard a lot of people talking about “ Attention” in AI world.

What is Attention?

Attention lets each word “look at” every other word in your prompt to understand context.

```
"The animal didn't cross the road because it was too tired."
```

When processing the word “it”, the attention mechanism:

- Looks back at “animal”
- Looks at “road”
- Decides “it” refers to “animal” (not “road”)

Now, your prompt has been transformed into a rich, context-aware representation.

Step 4: The Model Predicts the Next Token

The model doesn’t generate your entire response at once.

It predicts one token at a time.

After processing your prompt, the model outputs a probability distribution over its entire vocabulary (50,000+ tokens).

Example:

If your prompt is:

```
"Machine learning is"
```

The model might predict:

```
"a"          → 32%
"the"        → 18%
"an"         → 11%
"used"       → 8%
"powerful"   → 6%
...
```

Based on these probabilities (and some randomness controlled by “temperature”), one token is selected.

Let’s say it picks “a”.

Step 5: Repeat

Now the model adds that token to your prompt and runs the process again.

New input:

```
"Machine learning is a"
```

New prediction:

```
"field"      → 28%
"branch"     → 15%
"subset"     → 12%
"type"       → 10%
...
```

It picks “field”.

New input:

```
"Machine learning is a field"
```

This loop continues token by token until:

- The model predicts a stop token, OR
- It hits the maximum response length

It runs this loop:

```
1. Read everything so far
2. Predict the most likely next token
3. Add that token
4. Repeat
```

That’s it.

ChatGPT feels like intelligence. But it’s actually just extremely sophisticated pattern matching.

And somehow, that’s enough to feel like you’re talking to something that understands.

When you prompt ChatGPT:

- Your text → broken into tokens
- Tokens → converted to numbers
- Numbers → transformed by neural network layers
- Model → predicts next token probabilities
- One token selected → added to sequence
- Repeat until done

One token. One prediction. One loop.

If you want to get the overview of LLM, RAG, MCP, Agent, Fine-tuning, and Quantization, refer to the AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization.

Thanks

Amit Shekhar

Founder, Outcome School

May 22

Thanks for sharing this

# How Does the Transformer Architecture Work?
URL: https://outcomeschool.com/blog/decoding-transformer-architecture
Published: 2026-04-07

How Does the Transformer Architecture Work?

# How Does the Transformer Architecture Work?

Authors
: - Name
: Amit Shekhar
Published on
: April 7, 2026

The Transformer is the architecture behind every modern Large Language Model (LLM). It takes a sequence of tokens as input and produces a sequence of tokens as output, using attention to understand how the words relate to each other.

In this blog, we will learn about the Transformer architecture by decoding it piece by piece - understanding what each component does, how they work together, and why this architecture powers every modern Large Language Model (LLM).

When we hear "Transformer", it sounds complex. But do not worry. If we break it down into its individual parts, every single piece is simple. The complexity comes from how they are stacked together - not from any one piece being hard.

Our goal is to decode this architecture so clearly that by the end, we will be able to explain how a Transformer works to anyone.

We will cover the following:

- Why the Transformer was needed
- The two halves of the architecture
- Tokenization, Embedding, and Positional Encoding
- The Attention Mechanism and Multi-Head Attention
- Feed-Forward Networks, Residual Connections, and Layer Normalization
- How the Encoder and Decoder work
- How data flows through the entire architecture
- The three variants of the Transformer
- Why the Transformer is so powerful

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

A Transformer takes a sequence of tokens as input and produces a sequence of tokens as output. That is it. At a very high level, it is a tokens-in, tokens-out machine. And since tokens come from text and turn back into text, we can also think of it as a text-in, text-out machine.

For example, if we give it "Translate: I love learning" as input, it produces "J'adore apprendre" as output. If we give it "What is the capital of France?" as input, it produces "The capital of France is Paris." as output.

But how does it do this? Let's understand.

## Why Was the Transformer Needed?

Before the Transformer, models processed words one by one, in order - like reading a sentence from left to right, one word at a time.

This had two big problems:

Problem 1: Forgetting. As sentences got longer, the model would start forgetting earlier words. By the time it reached the 50th word, its memory of the 1st word was very weak.

Problem 2: Slowness. Because words were processed one after another, the 2nd word had to wait for the 1st word to finish, the 3rd word had to wait for the 2nd, and so on. This was very slow.

So, here comes the Transformer to the rescue. It processes all input tokens at the same time and lets every token look at every other token directly. Long-range connections are no longer a major problem. And because everything happens in parallel, training became much faster. We will see exactly how this works in the upcoming sections.

The Transformer was introduced in 2017 in the famous research paper "Attention Is All You Need" by researchers at Google. It changed everything.

## The Architecture Has Two Halves

The original Transformer has two main halves:

- The Encoder - this half reads and understands the input
- The Decoder - this half generates the output

Think of it like a conversation between a reader and a writer. The reader (encoder) reads a document carefully and creates detailed notes. The writer (decoder) uses those notes to write a new document. The reader focuses on understanding. The writer focuses on producing.

Now, let's understand what happens inside each half. But before jumping into the encoder and decoder, we need to understand what happens before the input even reaches them.

## Decoding Step 1: Turning Words into Numbers

The model does not understand words. It only understands numbers. So, the very first step is to convert words into numbers.

This happens in two stages:

Tokenization: The input text is split into small pieces called tokens. A token can be a word, part of a word, or even a single character. For the sake of understanding, let's treat each word as one token.

"I love learning" becomes three tokens: "I", "love", "learning".

Embedding: Each token is then converted into a vector of numbers called an embedding. An embedding is like a digital fingerprint for a word. Words with similar meanings get similar fingerprints.

For example, "happy" and "joyful" would have very similar embeddings because they mean almost the same thing. But "happy" and "car" would have very different embeddings because they are unrelated.

## Decoding Step 2: Adding Word Order

But, here is the catch. The encoder processes all input tokens at the same time - not one by one. This is great for speed, but it means the model has no idea which word comes first, second, or third.

"I love AI" and "AI love I" would look the same to the model. But they mean very different things.

Positional Encoding solves this. It adds a vector of numbers to each embedding that represents the position of the word. The 1st word gets a different position signal than the 2nd word, and so on.

Think of it like seat numbers in a theater. Even if all the audience members arrive at the same time, their seat numbers tell us exactly where each person is supposed to sit. Positional encoding is the seat number for each word.

After this step, the positional encoding numbers are combined into the embedding itself through addition. So, each token now carries a single vector of numbers that encodes both what the word means and where it sits in the sentence.

## Decoding Step 3: The Attention Mechanism

This is the heart of the Transformer. The attention mechanism is the single most important idea that makes everything work.

Attention allows each word to look at every other word in the sentence and decide how much focus to give to each one.

Let's take the sentence: "The cat sat on the mat because it was tired."

When the model processes the word "it", it needs to figure out what "it" refers to. Is it the cat? Is it the mat? The attention mechanism helps the model focus more on "cat" and less on "mat" because "cat" is more relevant to "it" in this context.

### How Attention Works

Each word is converted into three things:

- Query (Q) - what this word is looking for
- Key (K) - what this word can offer
- Value (V) - the actual information this word carries

We have a detailed blog on the Math behind Attention - Q, K, and V that explains how these are actually computed.

The process works like this:

First, each word uses its Query to compare with the Keys of all other words using a dot product. This produces attention scores - numbers that tell the model how relevant each pair of words is. Then, these scores are scaled down (divided by √dₖ) to keep them in a manageable range. We have a detailed blog on Scaling Dot Product Attention that explains why this step is needed. After scaling, the scores are normalized using softmax so they become probabilities that add up to 1. Finally, the model collects a weighted mix of the Values based on these probabilities.

The result is that every word now carries information not just about itself, but about the words most relevant to it. The word "it" now carries a strong signal from "cat" because the attention mechanism figured out the connection.

In simple words, attention lets each token borrow useful information from other relevant tokens before moving to the next layer.

### Multi-Head Attention

The Transformer does not run attention just once. It runs it multiple times in parallel - each time from a different perspective. This is called multi-head attention.

Think of it like a team of editors reviewing an article. One editor checks for grammar, another checks for factual accuracy, and another checks for flow. Each editor looks at the same text but focuses on something different. Together, they provide a complete review.

Each head in multi-head attention focuses on a different type of relationship between words. One head focuses on subject-verb connections. Another head focuses on which adjective describes which noun. The outputs of all heads are combined to give the model a rich understanding of the text.

Here is a simple visual of multi-head attention. All heads run in parallel on the same input, and their outputs are combined at the end:

```
                Input
                  |
   -------------------------------
   |       |       |       |     |
 Head 1  Head 2  Head 3  ...  Head N    (all running in parallel)
   |       |       |       |     |
   -------------------------------
                  |
              Combined
                  |
                Output

```

To learn Attention, Self-Attention, Multi-Head Attention, and Q/K/V Matrices in depth, check out our AI and Machine Learning Program at Outcome School.

## Decoding Step 4: The Feed-Forward Network

After the attention mechanism processes the words, the output passes through a feed-forward network.

Think of it as a refinement step. If attention is about understanding relationships between words, the feed-forward network is about deepening the understanding of each word individually.

It takes the enriched representation from attention and processes it further - sharpening the signal and removing noise. Every word passes through the same feed-forward network independently.

## Decoding Step 5: Residual Connections and Layer Normalization

Inside each layer, there are two more important pieces that help the Transformer learn effectively. Let's understand each of them.

Residual Connection (Skip Connection): After each sub-layer (attention or feed-forward network), the original input to that sub-layer is added back to the output. Think of it like taking notes in a class. Even after the teacher adds new information, we keep our original notes and combine the new information with them. This prevents the model from losing important information as data passes through many layers.

In simple words, the output of each sub-layer is: output = sub-layer(input) + input.

Layer Normalization: After each residual connection, the numbers are normalized - adjusted so they stay in a stable range. This prevents the numbers from becoming too large or too small as they pass through many layers. It keeps the training process stable and smooth.

These two pieces are present in every single layer of both the encoder and decoder.

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

## Decoding Step 6: Stacking Multiple Layers

Now, here comes the interesting part. So far, we have talked about one multi-head attention sub-layer and one feed-forward sub-layer. Together, these two sub-layers (along with their residual connections and layer normalization) form one layer of the Transformer. Think of one layer as a complete bundle: one multi-head attention sub-layer plus one feed-forward sub-layer.

The Transformer does not use just one such layer. It stacks multiple layers on top of each other, one after another. This is where the real power comes from.

Each of these layers is also called a Transformer block. So when we say "the model has 96 layers", it means the model has 96 Transformer blocks stacked one after another. Each block has its own multi-head attention sub-layer and its own feed-forward sub-layer.

Note: This stacking is different from multi-head attention. Multi-head attention runs many attention heads in parallel inside a single attention sub-layer. Stacking layers, on the other hand, places full Transformer blocks one after another in sequence, so the output of one layer becomes the input of the next layer.

Here is a simple visual of stacked Transformer layers. Each layer is a complete block, and they are connected one after another in sequence:

```
        Input
          |
  -----------------
  |   Layer 1     |    (multi-head attention + feed-forward)
  -----------------
          |
  -----------------
  |   Layer 2     |    (multi-head attention + feed-forward)
  -----------------
          |
         ...
          |
  -----------------
  |   Layer N     |    (multi-head attention + feed-forward)
  -----------------
          |
        Output

```

The original Transformer uses 6 layers in both the encoder and decoder. Modern LLMs use even more - GPT-3 (175B) uses 96 layers.

Each layer builds on the understanding from the previous layer. Think of it like reading a book multiple times. The first read gives us a basic understanding. The second read reveals connections we missed. The third read gives us deeper insights. Each layer is like another read - the understanding gets richer and richer.

## Decoding Step 7: The Encoder in Detail

Now that we know the building blocks, let's see how they come together inside the encoder.

The encoder's job is to read and understand the input.

Each encoder layer has two components:

- Self-Attention - each word looks at all other words in the input to understand relationships
- Feed-Forward Network - each word's representation is refined individually

Both components are followed by a residual connection and layer normalization.

Let's see what happens when the sentence "I love learning" passes through the encoder.

In the first layer, the self-attention mechanism allows each word to look at every other word. The word "love" starts to notice that "I" is its subject and "learning" is its object. The feed-forward network then refines this understanding.

In the second layer, the connections become richer. Now "love" does not just know about "I" and "learning" individually - it starts to understand the combined meaning of "I love learning" as a complete thought.

By the sixth layer, each word carries a deep, context-aware representation. The word "learning" is no longer just a dictionary definition - it now encodes the fact that it is something "I" loves to do, in this specific sentence.

After all encoder layers, we have a rich understanding of the input. This understanding is then passed to the decoder.

## Decoding Step 8: The Decoder in Detail

The decoder's job is to generate the output, one token at a time.

Each decoder layer has three components:

- Masked Self-Attention - each output word looks at all previous output words, but not future ones. This is because when generating text, future words do not exist yet. The word "love" can look at "I" but not at "learning" because "learning" has not been generated yet. This restriction is called causal masking. We have a detailed blog on Causal Masking in Attention that explains how this works.
- Cross-Attention - this is how the decoder connects to the encoder. Each output word looks at the encoder's output to pull in relevant information from the input. Here, the Query comes from the decoder, while the Key and Value come from the encoder's output. This is what makes it different from self-attention - and this is the bridge between understanding the input and generating the output.
- Feed-Forward Network - the same refinement step as in the encoder.

All three components are followed by a residual connection and layer normalization, just like in the encoder.

### How the Decoder Picks the Next Word

Now, the question is: after the output passes through all decoder layers, how does the decoder pick the actual next word? At this point, the output is still a vector of numbers - not a word.

So, the decoder passes these numbers through a linear layer that converts them into a score for every word in the vocabulary. If the vocabulary has 50,000 words, we get 50,000 scores.

Then, softmax converts these scores into probabilities - numbers between 0 and 1 that add up to 1. The model then picks the next word based on these probabilities. In practice, models use different strategies to pick the next word - like temperature, top-k, and top-p sampling - which control how creative or focused the output is. But for the sake of understanding, let's say it picks the word with the highest probability.

For example, if the model is translating "I love learning" to French and it has already generated "J'", the probabilities after the linear layer and softmax look like this:

- "adore": 0.72
- "aime": 0.15
- "mange": 0.01
- ... (50,000 words, most with very small probabilities)

The model picks "adore" because it has the highest probability. This is how the decoder decides which word to output next.

We have a complete program on Causal Masked Attention, Cross Attention, and Transformer Architecture - check out our AI and Machine Learning Program at Outcome School.

## Decoding Step 9: The Complete Flow

Now that we have learned about all the building blocks, let's walk through the complete flow with a concrete example. The best way to learn this is by taking an example.

Let's say we want to translate "I love learning" to French.

### The Encoder Phase

The English sentence "I love learning" goes through the following steps:

Tokenize: "I love learning" becomes three tokens: "I", "love", "learning".

Embed: Each token is converted into a vector of numbers (an embedding).

Add position: Positional encoding is added so the model knows "I" is 1st, "love" is 2nd, and "learning" is 3rd.

Pass through 6 encoder layers: In each layer, self-attention lets every word look at every other word, and the feed-forward network refines the understanding. Residual connections and layer normalization keep things stable.

After all 6 layers, the encoder produces a rich representation of the input. Each word now carries deep contextual information. This representation is passed to the decoder.

### The Decoder Phase

The decoder generates the French translation one word at a time.

Generating "J'" (the 1st word):

The decoder starts with a special "start" token. Masked self-attention has nothing to look back at since this is the first token. Cross-attention looks at the encoder's output to understand the English input. The output passes through the linear layer and softmax. The model picks "J'" as the most probable first word.

Generating "adore" (the 2nd word):

Now the decoder has ["start", "J'"]. Masked self-attention looks at "start" and "J'" to understand what has been generated so far. Cross-attention looks at the encoder's output again to pull in relevant information from the English input. The linear layer and softmax produce probabilities. The model picks "adore".

Generating "apprendre" (the 3rd word):

Now the decoder has ["start", "J'", "adore"]. Masked self-attention looks at all three previous tokens. Cross-attention connects to the encoder's output. The model picks "apprendre".

Generating the "end" token:

The decoder generates a special "end" token, signaling that the translation is complete.

The final output: "J'adore apprendre" (which means "I love learning" in French).

This is how the Transformer works from start to finish.

## The Three Variants

The original Transformer uses both an encoder and a decoder. But we do not always need both. This gives us three variants:

Encoder-Only (Example: BERT)

Uses only the encoder. The model reads and understands the input but does not generate new text. This is used for tasks like classifying emails as spam or not, understanding the sentiment of a review, or finding answers within a given text.

Decoder-Only (Example: GPT)

Uses only the decoder. The model generates text one token at a time. Each token can look at all previous tokens but not future ones. This is the variant behind most modern LLMs. It is used for generating text, answering questions, writing code, and having conversations.

Encoder-Decoder (Example: T5, the original Transformer)

Uses both parts. The encoder understands the input, and the decoder generates the output based on that understanding. This is used for translation, summarization, and other tasks where one text is transformed into another.

We can choose the right variant based on our use case.

## Why the Transformer is So Powerful

Now that we have decoded the entire architecture, let's understand why it changed everything:

Parallel processing: The encoder processes all input tokens at the same time instead of one by one. Even the decoder runs in parallel during training. This makes training much faster and allows models to learn from massive amounts of data.

No more long-range forgetting: Through attention, every word can directly look at every other word. The 1st word is just as accessible as the 1000th word, so the long-range memory problem of older models is largely solved.

Scalability: By adding more layers, more attention heads, and more data, the model keeps getting better. This is why we have models with billions of parameters today. Parameters are the numbers inside the model that it learns during training.

Versatility: The same architecture handles translation, question answering, text generation, code writing, summarization, and much more. One design, countless applications.

The Transformer is the single architecture behind the entire modern AI revolution. It enables us to do complex things very simply.

## Quick Summary

Let's recap what we have decoded:

- Tokenization and Embedding turn words into numbers that the model can work with.
- Positional Encoding adds word order information since all words are processed at the same time.
- Attention lets every word look at every other word and decide which ones to focus on. Multi-head attention does this from multiple perspectives.
- Feed-Forward Networks refine the understanding of each word individually.
- Residual Connections and Layer Normalization keep the numbers stable as data flows through many layers.
- The Encoder stacks these building blocks to read and understand the input.
- The Decoder adds cross-attention to connect to the encoder, and uses a linear layer + softmax to pick the next word.
- Three variants exist: encoder-only for understanding, decoder-only for generating, and encoder-decoder for transforming one text into another.

Now, we have decoded the Transformer architecture piece by piece and understood how it works.

### Does GPT use the full Transformer architecture?

No. GPT uses only the decoder half of the Transformer. It generates text one token at a time, and each token can look at all previous tokens but not future ones. This decoder-only variant is the one behind most modern LLMs.

### Is multi-head attention the same as stacking layers?

No. Multi-head attention runs many attention heads in parallel inside a single attention sub-layer. Stacking layers places full Transformer blocks one after another in sequence, so the output of one layer becomes the input of the next layer. Each block has its own multi-head attention and its own feed-forward sub-layer.

### How many layers does a Transformer have?

The original Transformer uses 6 layers in both the encoder and the decoder. Modern LLMs use even more layers. For example, GPT-3 with 175B parameters uses 96 layers, which means 96 Transformer blocks stacked one after another.

### Does the decoder always pick the word with the highest probability?

No. In practice, models use different strategies to pick the next word, like temperature, top-k, and top-p sampling. These strategies control how creative or focused the output is. Picking the highest-probability word is just the simplest way to understand how the decoder works.

### Why can a decoder not look at future words?

A decoder cannot look at future words because, when generating text, future words do not exist yet. So each output word looks only at the previous output words. This restriction is called causal masking, and it is applied in the masked self-attention of every decoder layer.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# Tokenization in LLMs
URL: https://outcomeschool.com/blog/tokenization-in-llms
Published: 2026-10-03
Author: Amit Shekhar

Tokenization in LLMs

# Tokenization in LLMs

Authors
: - Name
: Amit Shekhar
Published on
: October 3, 2026

Tokenization in LLMs is the process of breaking text into small pieces called tokens and then converting each token into a number that the model can work with.

In this blog, we will learn about Tokenization in LLMs, the very first step where a model breaks our text into small pieces before it can understand anything. We will also see why we need it, what a token is, the different ways to break text into tokens, how Byte Pair Encoding builds a vocabulary step by step, how tokens become numbers and back into text, and where it works well and where it fails.

We will cover the following:

- What is Tokenization?
- Why do we need Tokenization?
- What is a Token?
- Approach 1: Character-level Tokenization
- Approach 2: Word-level Tokenization
- Approach 3: Subword-level Tokenization
- How does Byte Pair Encoding (BPE) work?
- Vocabulary and Token IDs
- Decoding: From Tokens back to Text
- Tokenization in action with code
- Special Tokens
- How Tokenization affects LLMs in practice
- Where it works well and where it fails

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Tokenization?

Tokenization is the process of breaking a piece of text into small pieces called tokens and then converting each token into a number.

Let's say we type the sentence "I love learning" into an LLM (Large Language Model).

We see the sentence as three words. But the model does not see it the way we see it. The model does not understand letters or words. It only understands numbers.

So, before anything else happens, the sentence is broken into small pieces like below:

```
"I" | " love" | " learning"

```

Then, each piece is converted into a number like below:

```
40 | 3021 | 6975

```

These numbers are what the model actually receives. The text never reaches the model. Only the numbers do.

Note: These numbers are just for the sake of understanding. The actual numbers depend on which tokenizer we use.

The program that does this job is called a tokenizer. Every LLM has its own tokenizer.

## Why do we need Tokenization?

An LLM is a machine learning model. At its core, it does a lot of mathematics. It multiplies numbers, adds numbers, and compares numbers. Mathematics works on numbers, not on letters.

So, we have a problem. We have text, and the model needs numbers.

We need something that converts text into numbers. So, here comes the tokenizer into the picture.

But, the tokenizer has one more job. The model must have a fixed list of pieces it knows. When the model generates a reply, it picks one piece at a time from that fixed list. If the list is too big, the model becomes slow and heavy. If the list is too small, every sentence becomes a very long chain of tiny pieces.

So, the real question is: what is the right size of each piece?

We will see three approaches, one by one, and understand why the third one is used in modern LLMs.

## What is a Token?

A token is the smallest unit of text that the model works with.

A token can be a whole word, a part of a word, a single character, a punctuation mark, or a word along with the space before it.

Let's see a few examples:

- "cat" is one token.
- "unbelievable" becomes three tokens: "un", "believ", "able".
- "!" is one token.
- " love" (with the space before it) is one token.

Here, we can notice that the space is attached to the word. This is how most modern tokenizers work. The space becomes part of the token that comes after it. This way, the model knows where a new word begins.

A simple rule of thumb for English: one token is roughly 4 characters, or about three-fourths of a word. So, 100 tokens is around 75 words.

Now, let's see the different ways to break text into tokens.

## Approach 1: Character-level Tokenization

The simplest idea is to make every character a token.

Let's take the word "learning". The tokens will be as below:

```
"l" | "e" | "a" | "r" | "n" | "i" | "n" | "g"

```

Here, we have 8 tokens for one word.

Advantage: The list of known pieces is very small. For English, it is just the letters, the digits, and a few punctuation marks. And, the model can never face a word it does not know, because every word is made of characters.

Disadvantage: Every sentence becomes very long. A short paragraph of 100 words becomes around 500 tokens. The model has to process each one of them. And, each character carries very less meaning on its own. The letter "l" alone tells us nothing. The model has to work very hard to learn that "l", "e", "a", "r", "n" together means learn.

The issue with this approach is that the sequences become very long and each token carries very less meaning. Let's see how the next approach solve this issue.

## Approach 2: Word-level Tokenization

The next idea is to make every word a token. We simply split the text at spaces.

Let's take the sentence "I love learning". The tokens will be as below:

```
"I" | "love" | "learning"

```

Here, we have 3 tokens for three words.

Advantage: Each token carries full meaning. The sequences are short.

Disadvantage: The list of known words becomes huge. English alone has hundreds of thousands of words. Add names of people, names of places, other languages, code, and new words that appear every day. The list never ends.

What happens when the model sees a word that is not in the list?

Let's say the list does not have the word "tokenization". The tokenizer has no choice. It replaces the word with a special token called unknown, usually written as ` `. The model sees ` ` and has no idea what we said.

One more thing to notice. The words "learn", "learning", "learned", and "learner" are all separate tokens in this approach. The model does not know that they are related. It has to learn each one from scratch.

The issue with this approach is the huge list of words and the unknown word problem. Let's see how the next approach solve this issue.

## Approach 3: Subword-level Tokenization

Now, we take the middle path.

The idea is simple. Common words stay as one token. Rare words get broken into smaller pieces that are common.

Let's see with an example:

- "the" is very common, so it stays as one token: "the"
- "learning" is common, so it stays as one token: "learning"
- "tokenization" is rare, so it breaks into two: "token", "ization"
- "unbelievable" is rare, so it breaks into three: "un", "believ", "able"

Here, we can see that the pieces are meaningful. "token" is a real piece. "ization" is a real piece. Means, the model can learn that "ization" usually means the act of doing something, and reuse that learning for "organization", "civilization", and many more. Hence, the model learns faster.

Advantage: The list of known pieces is manageable, usually between 50,000 and 200,000. There is no unknown word problem, because any rare word can be broken down until we reach pieces we know, in the worst case single characters. And, related words share pieces, so the model does not have to learn each one from scratch.

Disadvantage: Sometimes a word breaks at a place that does not look natural to us.

This is what almost every modern LLM uses.

Let me tabulate the differences between the three approaches for your better understanding.

| | Character-level | Word-level | Subword-level |
| --- | --- | --- | --- |
| Size of the known list | Very small | Very large | Medium |
| Tokens per sentence | Very many | Few | Few |
| Unknown word problem | Never | Often | Never |
| Meaning per token | Very less | Full | Good |
| Used in modern LLMs | No | No | Yes |

Now, the question is, how does the tokenizer decide which pieces are common and which are rare? Who makes that list?

So, here comes the Byte Pair Encoding to the rescue.

## How does Byte Pair Encoding (BPE) work?

Byte Pair Encoding, or BPE, is an algorithm that builds the list of tokens by starting from single characters and repeatedly merging the pair of pieces that appears together most often.

In simple words, BPE looks at a huge amount of text, finds two pieces that sit next to each other most often, glues them into one new piece, and repeats.

The best way to learn this is by taking an example.

Let's say our training text has only three words, appearing with the following counts:

- "hug" appears 10 times
- "pug" appears 5 times
- "hugs" appears 5 times

Step 0: Split every word into characters.

```
h u g      (10 times)
p u g      (5 times)
h u g s    (5 times)

```

Our starting list of tokens: `h`, `u`, `g`, `p`, `s`. That is 5 tokens.

Step 1: Count every pair. A pair means two pieces that sit next to each other inside a word.

- "h" + "u" appears 10 + 5 = 15 times
- "u" + "g" appears 10 + 5 + 5 = 20 times
- "p" + "u" appears 5 times
- "g" + "s" appears 5 times

The most frequent pair is "u" + "g" with 20. So, we merge them into a new token `ug`.

Our list of tokens: `h`, `u`, `g`, `p`, `s`, `ug`. That is 6 tokens.

Our words now look like below:

```
h ug       (10 times)
p ug       (5 times)
h ug s     (5 times)

```

Step 2: Count the pairs again.

- "h" + "ug" appears 10 + 5 = 15 times
- "p" + "ug" appears 5 times
- "ug" + "s" appears 5 times

The most frequent pair is "h" + "ug" with 15. So, we merge them into a new token `hug`.

Our list of tokens: `h`, `u`, `g`, `p`, `s`, `ug`, `hug`. That is 7 tokens.

Our words now look like below:

```
hug        (10 times)
p ug       (5 times)
hug s      (5 times)

```

Step 3: Count the pairs again.

- "p" + "ug" appears 5 times
- "hug" + "s" appears 5 times

Both are equal. In such a case, the tokenizer follows a fixed rule to pick one. Let's merge "p" + "ug" into `pug`.

Our list of tokens: `h`, `u`, `g`, `p`, `s`, `ug`, `hug`, `pug`. That is 8 tokens.

We keep doing this until our list reaches the size we want. In real tokenizers, that size is decided beforehand, for example 100,000 tokens.

Here, we have done three merges. Every merge is saved as a rule, in order:

```
Rule 1: u + g  -> ug
Rule 2: h + ug -> hug
Rule 3: p + ug -> pug

```

Now, when a new piece of text comes in, the tokenizer does not count anything. It simply splits the text into characters and applies these rules in the same order.

Let's say the new text is "pugs". The tokenizer works as below:

- Start: `p`, `u`, `g`, `s`
- Apply Rule 1: `p`, `ug`, `s`
- Apply Rule 2: nothing to merge, because "h" + "ug" is not here
- Apply Rule 3: `pug`, `s`
- Final tokens: `pug`, `s`

And, the word "pugs" never appeared in our training text. Still, we got meaningful tokens.

Note: In many modern tokenizers, like the ones used by GPT models, the starting list is not the letters. It is all 256 possible byte values. Every character in every language, every emoji, and every symbol is stored as bytes. So, the tokenizer can never face something unknown. This variant is called byte-level BPE.

One more thing to notice. The tokenizer is trained separately, before the LLM is trained. Once the list of tokens is ready, it is frozen. The LLM is then trained using that frozen list. The LLM never changes the tokenizer.

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

## Vocabulary and Token IDs

The vocabulary is the complete list of all tokens that the tokenizer knows.

Each token in the vocabulary gets a unique number. This number is called the Token ID.

Think of it as a dictionary where every entry has a serial number. The tokenizer looks up the piece, finds the serial number, and hands over the number to the model.

For our small example, the vocabulary looks like below:

| Token | Token ID |
| --- | --- |
| h | 0 |
| u | 1 |
| g | 2 |
| p | 3 |
| s | 4 |
| ug | 5 |
| hug | 6 |
| pug | 7 |

So, the text "pugs" becomes tokens `pug`, `s`, and then Token IDs `7`, `4`.

This is the complete journey:

```
Text   -> Tokens        -> Token IDs
"pugs" -> ["pug", "s"]  -> [7, 4]

```

Here, `[7, 4]` is what goes into the LLM.

Now, why does the vocabulary size matter? When the LLM generates a reply, at every step it picks one token from this vocabulary. So, a vocabulary of 100,000 tokens means the model chooses from 100,000 options at every step. Bigger vocabulary means fewer tokens per sentence but a heavier model. Smaller vocabulary means a lighter model but longer sequences. Real models pick a size somewhere in between, based on their use case.

Note: Inside the model, each Token ID is used to look up a long list of numbers called an embedding. That is where the real understanding begins, and it is a topic for another blog. For now, we just need to know that Tokenization is the step that comes before it.

If we want to go deep into Tokenization, LLM Fundamentals, and LLM Internals, and build a Large Language Model (LLM) from scratch, check out our AI and Machine Learning Program at Outcome School.

## Decoding: From Tokens back to Text

Now, let's see how text comes out of the model.

The LLM does not produce text. It produces Token IDs, one at a time.

Let's say the model produces `6`, `4`. The tokenizer looks up the vocabulary in reverse:

- `6` is `hug`
- `4` is `s`

Then, it joins them: "hugs".

This reverse step is called decoding. It is the exact opposite of what we did earlier.

```
Token IDs -> Tokens        -> Text
[6, 4]    -> ["hug", "s"]  -> "hugs"

```

This is why, when we watch an LLM type its answer on the screen, sometimes we see half a word appear first and then the rest. That is a token boundary. The model produced one token, the tokenizer decoded it, and it was shown to us.

## Tokenization in action with code

Let's see the whole thing in action. We will use `tiktoken`, which is OpenAI's library that contains the tokenizers used by OpenAI models.

```python
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

token_ids = encoding.encode("I love learning")
print(token_ids)

text = encoding.decode(token_ids)
print(text)

```

It will print something like the following:

```
[40, 3021, 6975]
I love learning

```

Here, we have used `cl100k_base`, which is the name of one tokenizer with around 100,000 tokens in its vocabulary. The `encode` function converts our text into Token IDs. The `decode` function converts the Token IDs back into text. We got the exact same sentence back.

Now, let's see which piece of text each Token ID stands for.

```python
for token_id in token_ids:
    print(token_id, "->", "[" + encoding.decode([token_id]) + "]")

```

It will print the following:

```
40 -> [I]
3021 -> [ love]
6975 -> [ learning]

```

Here, we can see that the space is attached to the word, exactly as we discussed earlier. " love" is one token and " learning" is one token.

Note: The exact Token IDs depend on the tokenizer. A different model with a different tokenizer will give different numbers for the same sentence.

## Special Tokens

Along with the tokens that come from text, the vocabulary has a few special tokens. These are not words. They are signals.

Few important ones:

- End of text: tells the model that the text has ended. Usually written as `<|endoftext|>` or ` `. When the model produces this token, it stops generating.
- Beginning of text: marks where the text starts. Usually written as ` `.
- Padding: a filler token used to make many inputs the same length when the model processes them together.
- Chat markers: tokens that mark where the user's message begins and ends, and where the assistant's reply begins. This is how a chat model knows who said what.

Here, we can notice that a special token is never produced by breaking normal text. It is added on purpose by the tokenizer or by the system around the model.

## How Tokenization affects LLMs in practice

Tokenization happens before the model, and the model can never look inside a token. This one fact explains many strange things that LLMs do.

Counting letters: Let's say we ask, how many times does the letter "r" appear in "strawberry"? The tokenizer breaks the word into something like "str", "aw", "berry". The model sees three Token IDs. It never sees the individual letters. So, it has to guess from memory how many "r" are inside those pieces. This is why LLMs sometimes get such questions wrong.

Math on numbers: The number "12345" is split into pieces like "123" and "45". The model does not see five digits. It sees two tokens. Doing addition on such pieces is much harder than doing it digit by digit.

Cost and limits: Every LLM has a limit on how many tokens it can read at once. This is called the context window. And, the pricing of an LLM is also per token. So, the number of tokens decides both what fits and what it costs.

Other languages: Most tokenizers are trained on text that is mostly English. So, English words get compact tokens. A sentence in Hindi, Tamil, or Japanese is broken into many more small pieces. The same sentence can take several times more tokens in these languages. This means it costs more and fills the context window faster.

Code: Spaces and indentation are tokens too. Four spaces of indentation can become one token or four tokens depending on the tokenizer. This affects how well a model reads and writes code.

## Where it works well and where it fails

Let me summarize where subword tokenization works well:

- It handles any input without an unknown word problem.
- It keeps sequences short for common text.
- It shares meaningful pieces across related words, so the model learns faster.
- It works for text, code, and many languages with one single vocabulary.

And where it fails:

- Tasks that need to see individual letters, like counting letters or reversing a word.
- Math on long numbers, because digits get grouped in unnatural ways.
- Languages that were less present in the training text, because they get more tokens, which means higher cost and less room in the context window.
- Any word broken at a strange place can confuse the model, because the pieces do not carry the meaning we expect.

Now we must have understood what Tokenization in LLMs is, how BPE builds the vocabulary, how text becomes Token IDs and back, and where it works well and where it fails.

### Do all LLMs use the same tokenizer?

No. Every LLM has its own tokenizer. A different model with a different tokenizer will give different Token IDs for the same sentence. So, the exact numbers we get always depend on which tokenizer we use.

### Does the LLM change its tokenizer during training?

No. The tokenizer is trained separately, before the LLM is trained. Once the list of tokens is ready, it is frozen, and the LLM is then trained using that frozen list. The LLM never changes the tokenizer.

### How many words are 100 tokens?

For English, 100 tokens is around 75 words. A simple rule of thumb is that one token is roughly 4 characters, or about three-fourths of a word.

### Why do LLMs struggle to count letters in a word?

Because the model never sees the individual letters. A word like "strawberry" is broken into pieces like "str", "aw", "berry", and the model sees only their Token IDs. So, it has to guess from memory how many times a letter appears inside those pieces.

### Why does text in Hindi or Japanese use more tokens than English?

Most tokenizers are trained on text that is mostly English, so English words get compact tokens. A sentence in Hindi, Tamil, or Japanese is broken into many more small pieces. This means it costs more and fills the context window faster.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
