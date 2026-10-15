> Source: https://outcomeschool.com/blog/decoding-transformer-architecture

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
