> Source: https://outcomeschool.com/blog/what-are-embeddings

# What are Embeddings?
URL: https://outcomeschool.com/blog/what-are-embeddings
Published: 2026-07-31

What are Embeddings?

# What are Embeddings?

Authors
: - Name
: Amit Shekhar
Published on
: July 31, 2026

In this blog, we will learn about Embeddings, one of the most important ideas behind modern AI like search engines, recommendations, and chatbots. We will also see why a computer cannot compare meaning on its own, how an embedding turns meaning into numbers so that similar things sit close together, how we measure that closeness, and where we use embeddings in the real world.

We will cover the following:

- The problem: computers cannot compare meaning
- What are Embeddings?
- A simple example with two numbers
- Why we need many more than two numbers
- How do we measure closeness?
- Where do embeddings come from?
- The famous word math example
- Embeddings are not only for words
- What we use embeddings for
- Things we must be careful about
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The problem: computers cannot compare meaning

Before jumping into embeddings, we must understand the problem they solve.

A computer is brilliant at comparing numbers. Ask it whether 5 is bigger than 3, and it answers instantly. But a computer has no idea what words mean. To a computer, a word is just a set of letters.

Let's see why that becomes a real problem.

Consider these two sentences.

```
   Sentence A:  "How do I reset my password?"
   Sentence B:  "I forgot my login details."

```

We read them and see immediately that they are about the same thing. Now let's look at them the way a plain computer does. It compares the letters. Not a single important word is shared. No "reset", no "password", no "forgot", no "login" appears in both. So the computer concludes they have nothing in common.

Now consider another pair.

```
   Sentence C:  "The bank of the river was muddy."
   Sentence D:  "I need to visit the bank today."

```

Here, both sentences share the word "bank". So the plain computer decides these two are related. But we know they are about completely different things, one about a riverside and one about money.

Here, we can see the problem clearly. Matching letters is not the same as understanding meaning. The computer got both cases backwards.

So, we need some way to hand the computer meaning in a form it is actually good at, which means numbers.

We needed a solution for that. So, here come embeddings to the rescue.

## What are Embeddings?

An embedding is a list of numbers that represents the meaning of something, arranged so that things with similar meaning get similar numbers.

In simple words, an embedding is meaning translated into numbers.

That is the whole idea, and everything else in this blog is just detail on top of it.

The word itself tells us what is happening. To embed something means to place it inside something else. We are taking a word, or a sentence, or a picture, and placing it inside a space made of numbers. Once it sits in that space, it has a position. And once things have positions, we can ask which ones are near each other.

This list of numbers has a name. A list of numbers is called a vector. So when somebody says "the vector for this sentence", they mean exactly the same thing as "the embedding for this sentence".

Let's look at what it actually looks like.

```
   "How do I reset my password?"   ->   [0.21, -0.48, 0.83, 0.02, ... ]
   "I forgot my login details."    ->   [0.19, -0.44, 0.79, 0.05, ... ]
   "The bank of the river."        ->   [-0.71, 0.33, -0.12, 0.66, ... ]

```

Here, we can notice the important part. The first two lists hold numbers that are close to each other, because the two sentences mean nearly the same thing. The third list looks completely different, because it means something else. The computer never had to understand English. It only has to notice that two lists of numbers are similar, and that is something a computer does perfectly.

## A simple example with two numbers

The best way to learn this is by taking an example. Real embeddings use hundreds of numbers, which we cannot picture, so let's start with just two.

Suppose we want to place some fruits in a space. We choose two qualities and score each fruit from 0 to 10.

- The first number is how sweet it is.
- The second number is how big it is.

Let's fill in the scores.

```
   Fruit         Sweetness    Size        Embedding
   -----         ---------    ----        ---------
   Apple             7          5         [7, 5]
   Banana            8          5         [8, 5]
   Lemon             1          3         [1, 3]
   Watermelon        6         10         [6, 10]

```

Now, each fruit has an embedding, which is simply its two scores written as a list. And because there are only two numbers, we can draw them on paper.

```
   Size
    10 |                 W
       |
     8 |
       |
     5 |                    A  B
       |
     3 |  L
       |
     0 +--------------------------------- Sweetness
       0     2     4     6     8     10

   A = Apple [7, 5]        B = Banana [8, 5]
   L = Lemon [1, 3]        W = Watermelon [6, 10]

```

Here, we can see something wonderful happen. We never told the computer that apples and bananas are similar fruits. We only gave it four pairs of numbers. And yet Apple and Banana have landed right next to each other, while Lemon sits far away in its own corner.

So now the computer can answer a real question. "Which fruit is most like an apple?" It does not need to know anything about fruit. It just measures which point is closest to `[7, 5]`, finds Banana at `[8, 5]`, and gives the right answer.

This is exactly how embeddings work. Meaning became position, and position can be measured.

## Why we need many more than two numbers

Now, two numbers were enough for fruit. But let's see where two numbers break down.

With only sweetness and size, a lemon and a lime would get almost identical scores. They would sit on top of each other, and our computer would call them the same thing. We have no way to separate them, because we never gave it a number for color.

Language is far richer than fruit. A word carries a huge amount at once. Is it a thing or an action? Is it formal or casual? Is it positive or negative? Is it about people, or money, or nature, or time? Two numbers cannot hold all of that.

So, real embeddings use many more. A typical sentence embedding today has somewhere between 384 and 3072 numbers. Each of those numbers is called a dimension.

```
   2 dimensions      ->  a flat sheet of paper
   3 dimensions      ->  a room
   768 dimensions    ->  we cannot picture it, and that is fine

```

Note: We must not try to picture 768 dimensions. Nobody can. The comforting part is that we do not need to. Everything we understood from the fruit drawing still holds true. Similar things are close, different things are far. The math for measuring distance works exactly the same, no matter how many numbers there are.

Now, one more honest point. In our fruit example, we chose the meaning of each number ourselves, sweetness and size. In a real embedding, nobody chooses.

The numbers come out of a trained model, which is a computer program that has learned patterns by studying an enormous number of examples. And here is the surprising part. No single one of those numbers stands for something we could name. Dimension 42 is not "formality". The meaning is spread across all of them together, and we cannot point at one and say what it holds.

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

## How do we measure closeness?

Now, we keep saying two embeddings are "close". Let's see how we actually measure that.

The straightforward way is to measure the plain distance between the two points, exactly as we would with a ruler on our fruit drawing. Apple is at `[7, 5]` and Banana is at `[8, 5]`, so they are 1 unit apart. Apple and Lemon are much further.

But in practice, the more common method is called cosine similarity.

Let's understand it simply. Instead of thinking of each embedding as a dot, we think of it as an arrow pointing out from the center. Cosine similarity ignores how long the arrows are, and only measures the angle between them.

```
   Small angle between the arrows  ->  very similar meaning
   Right angle between the arrows  ->  unrelated
   Opposite directions             ->  opposite meaning

```

The result is a single number between -1 and 1.

- A score near 1 means the two things mean nearly the same thing.
- A score near 0 means they are unrelated.
- A score near -1 means they point in opposite directions.

Now, why do we prefer the angle over the plain distance? Because the length of the arrow often reflects something we do not care about, like how long the text was. A two-line answer and a two-page answer about the same topic should count as similar. Ignoring the length and keeping only the direction gives us that.

Note: In real use, we will rarely see scores anywhere near -1. With most modern text models, unrelated sentences still score around 0.1 to 0.3, and related ones score around 0.7 to 0.9. So we must not expect 0 to mean unrelated in practice. What matters is how the scores compare with each other, not the raw number on its own.

So, when a search system finds the best match for our question, this is all it is doing. It turns our question into an embedding, then finds the stored embedding with the highest cosine similarity.

## Where do embeddings come from?

Now, the next big question is: who decides these numbers?

We do not write them by hand. They are produced by a trained model, called an embedding model. We hand it a piece of text, and it hands back the list of numbers. There are many of these models available today, and we simply pick one and use it.

But how did that model learn to give good numbers? The idea behind it is beautifully simple.

The model reads an enormous amount of text, and it learns from one pattern: words that appear in similar situations tend to mean similar things.

This idea is old, and it was captured perfectly long before any of these models existed.

> You shall know a word by the company it keeps.
> 
> John Rupert Firth, linguist, 1957

Let's see this with an example.

```
   "I drank a cup of tea in the morning."
   "I drank a cup of coffee in the morning."
   "She poured the tea into a cup."
   "She poured the coffee into a cup."

```

Here, we can notice that "tea" and "coffee" keep turning up in the same kinds of sentences, surrounded by the same kinds of words. They get drunk, they get poured, they come in cups, they happen in the morning.

The model sees this happen millions of times across millions of sentences. So it places "tea" and "coffee" close together in the number space. It was never told that both are hot drinks. It worked that out purely from the company they keep.

And it does the opposite too. The word "bicycle" almost never appears in those same surroundings, so it lands far away.

This is how a machine builds something that behaves like an understanding of meaning, and that too without anybody explaining a single word to it.

We have a detailed blog on Contrastive Learning that explains how a model is trained to pull similar things together and push different things apart.

## The famous word math example

Now, let's look at the most famous demonstration of embeddings, because it shows how much structure is hidden inside these numbers.

Once words are positions in a space, we can do arithmetic on them. And something remarkable falls out.

```
   king  -  man  +  woman   ->  lands very close to  queen

```

Let's understand what happened. Take the position of "king". Subtract the position of "man", which removes the male part of the meaning. Add the position of "woman", which adds the female part. The point we land on is closest to "queen".

Similar patterns show up all over the place.

```
   Paris  -  France  +  Italy   ->  lands close to  Rome

```

Here, subtracting France strips away the country, leaving something like "the capital city of". Adding Italy applies it to Italy, and we land near Rome.

Here, we can see why this is so striking. Nobody programmed the concept of gender into the model. Nobody programmed the concept of a capital city. These relationships appeared on their own, simply because they exist in the way people write.

## Embeddings are not only for words

Now, we have been talking about text throughout. But nothing in the idea is specific to words.

The idea is general. If we can train a model to turn something into numbers so that similar things land close together, then that something can be embedded.

- Words and sentences. The case we have been discussing.
- Whole documents. A full page becomes one list of numbers, so we can find similar pages.
- Images. A photo becomes a list of numbers. Two photos of dogs land near each other, while a photo of a car lands far away.
- Audio. Two recordings of the same song, or two voices with the same accent, land near each other.
- Products and users. A shop can embed its products and its shoppers, then recommend the products sitting nearest to a shopper.

There is one more thing here that is genuinely clever. Some models put different kinds of things into the same space. So a photo of a cat and the words "a cat sitting on a chair" can land in the same neighborhood, even though one is a picture and one is text.

Here, we can see what that gives us. We can search a collection of photos by typing a sentence, and no photo needs any labels or tags at all. We simply embed our sentence, and find the photos whose embeddings sit nearest to it.

We have a detailed blog on Multimodal AI that explains how a single model works across text, images, and audio together.

## What we use embeddings for

Now, we have understood what embeddings are. Let's see where they earn their keep.

Semantic search. This is the biggest one. Instead of matching words, we match meaning. This is what fixes the very first problem in this blog, where "reset my password" and "forgot my login details" needed to be recognized as the same request.

RAG. This stands for Retrieval-Augmented Generation, and it means letting an AI answer using our own documents. We embed all our documents, we embed the user's question, then we pull out the closest pieces and hand them to the AI along with the question. The whole thing rests on embeddings.

Recommendations. "Others also liked this" is often just finding the nearest neighbours in the embedding space.

Grouping. Give a company ten thousand pieces of customer feedback, embed them all, and the complaints naturally form clusters. Nobody has to read them first to invent the categories.

Finding duplicates. Two support tickets worded completely differently but reporting the same bug will sit close together, so we can catch them.

Classification. To sort messages into categories, we can embed them and check which category's examples they sit nearest to.

Now, a natural question follows. If we have millions of embeddings, how do we find the nearest ones quickly? Checking every single one would be far too slow. This is exactly what a vector database is built for. It stores embeddings and finds the nearest ones fast.

## Things we must be careful about

Embeddings are useful, but there are traps. Let's go through the important ones.

Embeddings from two different models cannot be compared. This is the mistake that bites people hardest. Each model builds its own private space with its own arrangement. A vector from model A and a vector from model B are two different languages. Comparing them produces numbers that look fine and mean nothing. Very important: If we change our embedding model, we must rebuild every stored embedding.

Similar is not the same as correct. Two sentences can sit close together and still not answer each other. Embeddings capture that things are about the same topic. They do not verify facts, and they do not catch a negation. "The medicine is safe" and "The medicine is not safe" are about exactly the same topic, and they can land uncomfortably close.

They carry the bias of their training text. The model learned from human writing, so whatever unfair associations exist in that writing get baked into the positions. This matters a great deal when embeddings are used in hiring or lending.

They are frozen in time. An embedding model knows only the language it was trained on. A brand new word, or our company's internal jargon, has no good position in its space.

Long text loses detail. Squeezing a twenty-page document into one list of numbers averages everything into a blur. This is why we normally cut long documents into smaller pieces and embed each piece separately. We have a detailed blog on how a Reranker works that explains how systems win back the precision lost in that squeeze.

Here, we can see the simple rule. One model for everything, rebuild when we change it, and never assume that close means correct.

## Summary

Let's quickly recap what we have learned.

- A computer cannot compare meaning, but it is excellent at comparing numbers.
- An embedding is a list of numbers that represents meaning, arranged so that similar things get similar numbers.
- A list of numbers is called a vector, so an embedding and a vector mean the same thing here.
- With two numbers we can draw it on paper, and similar items visibly land close together.
- Real embeddings use hundreds or thousands of numbers, called dimensions, and no single dimension has a name we could give it.
- We measure closeness with cosine similarity, which compares the angle between two arrows and returns a score between -1 and 1. In practice the scores sit in a narrow band, so we must compare them against each other rather than reading a single number on its own.
- An embedding model produces them, having learned that words appearing in similar situations tend to mean similar things.
- Word arithmetic like `king - man + woman` landing near `queen` shows the structure hidden inside these numbers.
- Anything can be embedded, including images, audio, and products, and some models put pictures and text into one shared space.
- They power semantic search, RAG, recommendations, grouping, duplicate detection, and classification, and a vector database is what searches them quickly.
- We must never mix embeddings from two different models, and we must remember that close in meaning is not the same as correct.

This is what embeddings are, meaning turned into numbers, so that a machine which only understands arithmetic can still work with what things actually mean.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
