> Source: https://outcomeschool.com/blog/bpe-in-llms

# What is Byte Pair Encoding (BPE) in LLMs?
URL: https://outcomeschool.com/blog/bpe-in-llms
Published: 2026-03-31
Author: Amit Shekhar

What is Byte Pair Encoding (BPE) in LLMs?

# What is Byte Pair Encoding (BPE) in LLMs?

Authors
: - Name
: Amit Shekhar
Published on
: March 31, 2026

BPE (Byte Pair Encoding) is the tokenization algorithm used by most modern Large Language Models (LLMs). It starts with single characters and keeps merging the most frequent pair of pieces until it builds a vocabulary of common subwords.

In this blog, we will learn about BPE (Byte Pair Encoding) - the tokenization algorithm used by most modern Large Language Models (LLMs) to break text into smaller pieces before processing it.

We will understand what BPE is, why it is needed, and how it works step by step with a simple example.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Tokenization?

Before we understand BPE, we must first understand tokenization.

When we type a sentence like "I love teaching AI", we see words. But a model does not understand words directly. It works with numbers. So, the first step is to break the text into small pieces called tokens. Each token is then converted into a number. This process of breaking text into tokens is called tokenization.

Think of it like a chocolate bar. The full bar is the sentence. Each small part you break off is a token. The model processes multiple tokens at a time.

Now, the question is: how do we decide where to cut? How big or small should each token be?

This is where different tokenization approaches come into the picture.

## The Problem: How to Break Text into Tokens?

There are different ways to break text into tokens. Let's look at the two simplest approaches and understand why they do not work well.

Approach 1: Word-Level Tokenization

The simplest idea is to treat each word as one token.

For the sentence "I love teaching", the tokens would be: "I", "love", "teaching".

This seems easy. But the issue with this approach is that the model needs to know every word in the language. Think about it - there are hundreds of thousands of words in English alone. And then there are names, technical terms, words from other languages, misspellings, and new words being created every day.

If the model sees a word it has never seen before - like "ChatGPT" or "tokenization" - it does not know what to do. It treats the entire unknown word as a single "unknown" token and loses all meaning.

Approach 2: Character-Level Tokenization

The other extreme is to treat each character as one token.

For the sentence "I love", the tokens would be: "I", " ", "l", "o", "v", "e".

Now the model can handle any word - because every word is made up of characters, and the number of unique characters is very small compared to the number of words. For example, English has only 26 letters. Even if we include digits, punctuation, and spaces, the total is still very small. No word is ever "unknown."

But the issue with this approach is that the tokens are too small. The model has to process many more tokens for the same text. A 10-word sentence can become 50+ tokens. This makes training very slow and makes it harder for the model to understand meaning - because a single character like "l" carries very little meaning on its own.

We needed a solution that gives us the best of both worlds - not too big, not too small. So, here comes BPE to the rescue.

## What is BPE (Byte Pair Encoding)?

BPE (Byte Pair Encoding) is a tokenization algorithm that breaks text into pieces that are somewhere between characters and words.

It works by repeatedly finding the most common pair of adjacent tokens and merging them into one.

So, BPE starts with individual characters and keeps merging the most frequent pairs until it builds up a vocabulary of common pieces - called subwords. These subwords can be full words (like "the"), parts of words (like "ing", "un", "tion"), or even single characters.

Think of it like learning shorthand. When you first start taking notes, you write every letter. But over time, you notice that some combinations appear very often - like "ing" or "tion". So, you create shortcuts for them. BPE does the same thing automatically.

## How BPE Works: Step by Step

The best way to learn this is by taking an example.

Let's say we have the following text that we want to build our vocabulary from:

```
low low low low low
lower lower
newest newest newest newest newest newest
widest widest widest

```

For the sake of understanding, let's count the word frequencies:

- "low" appears 5 times
- "lower" appears 2 times
- "newest" appears 6 times
- "widest" appears 3 times

### Step 1: Start with Characters

We start by breaking every word into individual characters. We also add a special end-of-word symbol "_" at the end of each word so the model knows where words end.

```
l o w _        (frequency: 5)
l o w e r _    (frequency: 2)
n e w e s t _  (frequency: 6)
w i d e s t _  (frequency: 3)

```

Our initial vocabulary is all the individual characters: `{l, o, w, e, r, n, s, t, i, d, _}`

### Step 2: Find the Most Frequent Pair

Now, we look at all pairs of adjacent tokens across our entire text and count how often each pair appears.

For the sake of understanding, let's count a few important pairs:

- "e s" appears in "newest" (6 times) and "widest" (3 times) = 9 times
- "s t" appears in "newest" (6 times) and "widest" (3 times) = 9 times
- "t _" appears in "newest" (6 times) and "widest" (3 times) = 9 times
- "l o" appears in "low" (5 times) and "lower" (2 times) = 7 times
- "o w" appears in "low" (5 times) and "lower" (2 times) = 7 times

The most frequent pair is "e s" with 9 occurrences. We merge this pair into a single token "es".

### Step 3: Merge and Update

After merging "e s" into "es", our words now look like this:

```
l o w _         (frequency: 5)
l o w e r _     (frequency: 2)
n e w es t _    (frequency: 6)
w i d es t _    (frequency: 3)

```

Our vocabulary is now: `{l, o, w, e, r, n, s, t, i, d, _, es}`

Here, we can see that "e" and "s" have been merged into "es" wherever they appeared together.

### Step 4: Repeat

We repeat the same process. We find the next most frequent pair. Now "es t" appears 9 times (6 from "newest" and 3 from "widest"). We merge it into "est".

```
l o w _         (frequency: 5)
l o w e r _     (frequency: 2)
n e w est _     (frequency: 6)
w i d est _     (frequency: 3)

```

Vocabulary: `{l, o, w, e, r, n, s, t, i, d, _, es, est}`

We keep repeating this process. The next merge could be "est _" into "est_". Then "l o" into "lo". Then "lo w" into "low". And so on.

With each merge, our vocabulary grows by one token, and our text gets represented using fewer, larger pieces.

### Step 5: Stop When Done

We keep merging until we reach a desired vocabulary size. This size is a number we choose in advance. Modern LLMs typically use vocabulary sizes between 32,000 and 256,000 tokens. For example, LLaMA 3 uses a vocabulary of about 128K tokens, while Gemma uses about 256K tokens.

The final vocabulary contains a mix of:

- Full common words like "the", "is", "and"
- Common subwords like "ing", "tion", "est", "un"
- Individual characters for rare combinations

This is how BPE builds its vocabulary.

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

## How BPE Tokenizes New Text

Once BPE has finished training, it has two things: a vocabulary and an ordered list of merge rules. The order matters. During training, BPE learned these merges in a specific sequence - first "e s" into "es", then "es t" into "est", then "l o" into "lo", and so on. This exact sequence is saved.

Now, when BPE needs to tokenize new text, it does not simply look up subwords in the vocabulary. Instead, it replays the same merge rules in the same order they were learned during training.

Let's say we want to tokenize the word "lowest". Here is how it works:

Start: Break the word into individual characters: `l o w e s t`

Apply merge rule 1 ("e s" into "es"): `l o w es t`

Apply merge rule 2 ("es t" into "est"): `l o w est`

Apply merge rule 3 ("l o" into "lo"): `lo w est`

Apply merge rule 4 ("lo w" into "low"): `low est`

Result: "lowest" is tokenized as ["low", "est"].

Similarly, for the word "newer":

Start: `n e w e r`

The merge rules are applied in order. The rules that match adjacent pairs in this word get applied step by step, eventually producing: ["new", "er"].

For a rare word like "widestness":

Start: `w i d e s t n e s s`

The merge rules are applied in order. Common merges like "es" into "es" and "est" into "est" will fire when they match. The remaining characters stay as smaller pieces. The word gets broken into known subwords from the vocabulary.

Why does the order matter? Because different merge orders can produce different results. If we just did a greedy lookup - trying to find the longest matching subwords in the vocabulary - we could get different tokenizations than what the model expects. By replaying the merge rules in the exact training order, we get consistent and correct tokenizations every time.

This is the beauty of BPE. It never encounters a completely unknown word. Even if a word has never been seen before, BPE can break it down into smaller pieces by applying the merge rules. In the worst case, it falls back to individual characters - but that rarely happens for common languages. Problem Solved.

This is how BPE tokenizes new text.

## Why BPE is Used in Modern LLMs

BPE is the tokenization algorithm used by most modern LLMs. Here is why:

Handles unknown words: BPE can tokenize any word, even words it has never seen before, by breaking them into known subword pieces. No word is ever completely "unknown."

Efficient vocabulary size: Instead of needing millions of entries for every possible word, BPE creates a compact vocabulary of 32,000 to 256,000 tokens that can represent any text. It makes our life easy.

Balances meaning and efficiency: Common words like "the" and "is" are kept as single tokens - fast to process and meaningful. Rare words are broken into subword pieces - still understandable and manageable. This gives us the best of both worlds.

Works across languages: BPE works at the character level, so it can handle any language, any script, and any special characters. The same algorithm works for English, Chinese, Arabic, code, and that too without any changes to the algorithm itself.

Models use a variant of BPE, but the core idea remains the same - BPE or its variants are at the heart of how modern LLMs read and process text.

Once the text is split into tokens, the Transformer takes over. We have a detailed blog on Encoder vs Decoder in Transformers that explains the two blocks which process these tokens.

Now, we have understood BPE (Byte Pair Encoding) and how it works.

### Is BPE better than word-level tokenization?

Yes. Word-level tokenization needs the model to know every word, and an unseen word like "ChatGPT" becomes a single "unknown" token that loses all meaning. BPE breaks such a word into known subword pieces instead. So, no word is ever completely unknown.

### Why not just use character-level tokenization?

Character-level tokenization makes the tokens too small. A 10-word sentence can become 50+ tokens, which makes training very slow. It also makes it harder for the model to understand meaning, because a single character carries very little meaning on its own. BPE sits between characters and words.

### What vocabulary size do LLMs use with BPE?

Modern LLMs typically use vocabulary sizes between 32,000 and 256,000 tokens. This size is a number we choose in advance, and BPE keeps merging pairs until it reaches it. For example, LLaMA 3 uses about 128K tokens, while Gemma uses about 256K tokens.

### Does BPE use a greedy longest-match lookup to tokenize new text?

No. BPE replays the ordered list of merge rules in the same sequence they were learned during training. A greedy lookup of the longest matching subwords could give different tokenizations than what the model expects. Replaying the merges in order gives consistent and correct tokenizations every time.

### Can BPE ever fail to tokenize a word?

No. BPE can break any word, even one it has never seen, into smaller pieces by applying the merge rules. In the worst case, it falls back to individual characters. That rarely happens for common languages.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

# Positional Embeddings in LLMs - Outcome School Newsletter
URL: https://outcomeschool.substack.com/p/positional-embeddings-in-llms
Published: 2026-01-08
Author: Outcome School

Positional Embeddings in LLMs - Outcome School Newsletter

# Outcome School Newsletter

SubscribeSign in

# Positional Embeddings in LLMs

### How positional embeddings give meaning to word order in LLMs

Jan 08, 2026

7

1

Share

Today, we are going to understand positional embeddings and why they are essential for Large Language Models.

I’m Amit Shekhar from Outcome School, where I teach AI and Machine Learning, and Android.

Let’s get started.

Large Language Models do NOT have any notion of the order of words, because they process tokens in parallel, not sequentially like RNNs.

To inject information about the position of each token in the sequence, positional embeddings are added.

So, it helps in providing the information about the position of the word to the model.

For example: Outcome School

If we do not provide positional information, the model has no way of knowing whether it is "Outcome School" or "School Outcome".

So, before feeding the input into the transformers, we need to do the following:

Tokenization: Converting raw text into smaller units (tokens) and mapping them to numbers that the model can understand and process.

Token Embedding + Positional Embedding

So, the Positional Embedding helps in providing the information about the position of the word to the model.

I teach these types of concepts at Outcome School and help you become a better software engineer.

Thanks

Amit Shekhar

Founder, Outcome School

7

1

Share

#### Discussion about this post

CommentsRestacks

No posts

### Ready for more?

Subscribe

© 2026 Outcome School · Privacy∙ Terms∙ Collection notice

Start your Substack Get the app

Substack is the home for great culture

# Embeddings in Machine Learning
URL: https://www.youtube.com/watch?v=LedXW6xl21s
Author: Outcome School

Hey guys, welcome to outcome school. I am Amit and today I'm going to teach you what are embeddings in machine learning. So let's begin with the learning as usual. Okay. So first let's try to understand with the definition of the embeddings. So embeddings are the representations of objects like text, images and audio into a vector according to their properties and the relationships between them. So we will try to understand this with the examples and the use cases so that you understand it in a better way. So for that if you see on the screen right now we have the text embedding model and the audio embedding model. So this is the model and what we will do we will pass the text the document data the text data in this model and it will give you a vector representation for that. Similarly if we have some audio we can pass through the embedding model and again we will get some audio embedding factor like this. So ultimately what we are doing we are converting a format into the vector format so that machines can actually learn about the similarities. So it enables the machine learning model to find the similar object and that is going to help us in many use cases and for that we also need to learn about the vectors. So let's try to learn few things about the vectors as well. A vector is an array of numbers that define a point in a multi-dimensional space. So here we have the 2D space and here we have the 3D space. As you can see a point here 4A 5. So 4A 5 is a vector here and that is present in a twodimensional space. Similarly here we have the 4a 5a 3. So this is a point. A vector is an array of numbers that defines a point in a multi-dimensional space. So this is a point. So this is a array. This is a vector and this is present in a threedimensional space. So these were the examples of vectors in 2D and the 3D space. And what we will do now we will again look into the definition of embeddings with what we have learned so far. So here is the definition once again. Embeddings are the representations of objects like text, images and the audio into the vectors. So this is what we have learned so far according to their properties and the relationships between them. So we'll learn about this and this now. So for that we will take the example of the dog and the goldfish. So here we have properties. So we are going to learn about the properties and the relationships. So first let's try to understand the properties. So for example for the dog we have the properties like this high friendliness medium large size high energy. So here we have the low small and the less like this for the goldfish. So these are the properties that we have defined for the dog and the goldfish. As we have learned that vectors can be defined in 1D, 2D, 3D and it could be anything like n is equal to 1,000, 2,000, it could be anything as such based on the requirements. So here if you see if we are saying that we will take only one property like friendliness. So because of that we will have only one D space here and because the dog has more friendliness than the cat than the goldfish. So we are keeping the dog here and we are keeping the cat in the middle of the goldfish and the dog. So here these numbers are defining who is more friendly than the others. So that is what we have done here in 1D space. Similarly, if we have to define something in 2D space because we have the two properties like friendliness and we have the size because of that we will have the 2D space and as you can see again with the help of the numbers we are representing the dog cat and the gold face in this 2D space. Similarly if we have three properties like size, friendliness and the energy. So because of that again we have the 3D space here because of three properties. So here we have defined the dog, cat and the goldfish. So this is how the vectors are helping us in organizing the properties in the n dimensional space based on the requirements. As earlier I mentioned it enables machine learning models to find the similar object. Now it will make more sense when we see this. Okay. So we will wait for that. And before moving forward, I want to highlight that actual embeddings will have hundreds and thousands of dimensions for the embeddings, not just 1D, 2D and 3D because of the nature of the data that we are going to play with. And now let's get back to the point which is it enables the machine learning models to find the similar objects. So embeddings are going to help us in finding the similar objects. So when we feed the input features in the embedding models that model is going to provide us the vector representations and that is going to look like this 9A 4A 8A 6A 7 like this we will have the vector embeddings. So let's say we have the data set that we are going to feed into the embedding models and that is going to generate something like this. So after the generation when you observe this because dog and puppy are related to each other. So that is why they are close to each other. Similarly cat and kitten are similar right because of that they are again close to each other and as we know the goldfish and the dog are quite different from each other. So that is why they are placed far from each other. And if you see this thing, this embedding is going to help us in finding the similar object because we can easily calculate the distance between two object at any point in time. So this is how the embedding helps us in finding the similar objects. And now we are going to discuss the examples and the use cases of the embeddings. So embeddings are created by training models on the large corpus of data. So we have some already created models. So one example is word to ve and that is for the text. So if we have some text data that we can feed into this model and that will give us the embeddings which is what the vector representation of the data. And similarly for the images we have the restnet. So there are many models available in the market for the different different use cases that we can use as the embedding models to create the vector representation of the data that we have. And now it's time to learn about the use cases of the embeddings in the machine learning. How finding the similarities between the object is going to help us in solving many many use cases because of that vector representations. So now let's begin with the use cases. So the first is document similarity. So we can feed the text into the embedding models to find the vector representation of those data and that will finally help us in measuring how conceptually similar texts are to each other because of the vector representations. Right? Similarly contentbased recommendations. So here again we can feed the items. So for example we want to create a movie recommendation system. So our data will be video, title, descriptions. So those things we will pass into the embedding model and again it will generate the vector representation for those data and that will help us in suggesting similar items based on the feature embeddings. Features are video, title, descriptions and the next example is collaborative filtering. So here what we are going to do we are going to push user as well with the items. So with the video so for example video recommendation system so items are video title text but in addition to those features we are going to push the users as well. So here same thing but we will have extra users on the top of that and how this is going to help us let's try to understand. So suppose for example I watch videos related to football and you do watch the videos related to football but in addition to football I like cricket as well. So I do watch the videos related to cricket. So what this collaborative filtering will do because it has the videos plus the users as well and it knows that we both are similar users right. So because I watch football plus cricket and you only watch football so it can recommend you cricket as well and that was not possible in the contentbased recommendation. So so this is how adding this user in that embedding thing is going to help us in serving the new videos related to cricket to those users as well. So this is how collaborative filtering is helpful and this also uses the embeddings as well. And the next example is image retrieval finding visually similar images. So again what we can do we can feed all the images into the embedding models and that will create the vector representations in n dimensional array and that is going to help us in finding similar images. So we can simply find the visually similar images by using the embeddings. And the next is face recognition. Creating face embeddings for the comparison and the identification. Again we are going to feed all the images of the faces into the model to generate the vector representation and that embedding is going to help us. Again next example is vector database. Now we have seen there are many many vector databases. There they are using the embeddings to store and query the data based on the semantic similarity. And finally we have the large language model which is something everybody is talking about that also uses the embeddings to convert the tokens into the vectors and I think I might plan a video on how embeddings are internally used in the large language models and I hope this video has helped you in understanding what are embedded in machine learning. So that's it for now I will see you in the next video. [Music]
