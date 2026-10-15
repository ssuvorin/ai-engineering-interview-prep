> Source: https://outcomeschool.com/blog/how-does-semantic-search-work

# How does Semantic Search work?
URL: https://outcomeschool.com/blog/how-does-semantic-search-work
Published: 2026-07-23

How does Semantic Search work?

# How does Semantic Search work?

Authors
: - Name
: Amit Shekhar
Published on
: July 23, 2026

In this blog, we will learn about how Semantic Search works. We will also see why we need it, how it actually works step by step, and where it is used in real systems like search engines, AI assistants, and recommendations.

We will cover the following:

- What is keyword search
- Where keyword search fails
- What is Semantic Search
- What is an embedding
- How similar meanings sit close together
- How we measure closeness with cosine similarity
- What is a vector database
- The full Semantic Search flow
- Approximate nearest neighbor for speed at scale
- Semantic Search in the real world

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is keyword search

The oldest and simplest way to search is keyword search. Before we understand it, let's quickly see what search itself means, because keyword search is just one way to do search.

Search means we have a large collection of things, we ask a question, and the system gives us back the things that match our question.

Let's say we have a website with thousands of help articles. A user types "how do I get my money back". The job of search is to look at all those articles and return the few that actually help with getting money back.

So, in any search system, there are two sides. On one side, we have the large collection of documents. On the other side, we have the user's question, which we call the query. The query is simply the text the user types in to find something.

Let's picture these two sides like below:

```
   the collection                       the user
  +----------------+
  |  Document 1    |
  |  Document 2    |              query: "how do I get my money back"
  |  Document 3    |                       |
  |  Document 4    |                       v
  |  ...           |  <------ match ------ search
  +----------------+                       |
                                           v
                              results: the few documents
                              that help with the query

```

Here, we can see that on the left we have the big pile of documents, and on the right we have the user with a query. The job of search is to sit in the middle, look at every document, and return only the few that match the query.

Now, the big question is: how does the system decide which documents match the query? The oldest and simplest answer is keyword search.

Keyword search finds documents by matching the exact words in the query with the exact words in the documents.

In simple words, a keyword is just a word. Keyword search looks for the same words. If the user types the word "refund", keyword search looks for documents that contain the word "refund". If a document has that word, it is a match. If it does not have that word, it is not a match.

Let's say we have three short documents like below:

```
Document 1:  "How to get a refund for your order"
Document 2:  "Track your shipping and delivery status"
Document 3:  "Reset your account password"

```

Now the user searches for the word "refund".

Here, we can see that only Document 1 contains the word "refund". So keyword search returns Document 1 and ignores the other two. This works perfectly here, because the user used the same word that the document used.

For a long time, this was how most search worked. It is fast, it is simple, and it is easy to understand. But it has one big weakness. Let's see it.

### Where keyword search fails

Keyword search only matches words that are spelled the same. It does not understand meaning at all.

Let's see the problem with a clear example. Suppose we have a document like below:

```
Document:  "How to repair your car at home"

```

Here, we can see that the document is about repairing a car at home. Now a user searches with this query like below:

```
Query:  "fixing my automobile"

```

Here, we can see that the query asks about "fixing my automobile". As humans, we instantly know these two are about the same thing. "Repair" and "fixing" mean the same thing. "Car" and "automobile" mean the same thing. The document is exactly what the user wants.

But keyword search looks at the actual words, and the words are different. The query has "fixing" and "automobile". The document has "repair" and "car". Not a single important word matches.

So keyword search returns nothing useful. The user does not find the article, even though the perfect article exists.

Let's compare the important words from the query and the document, pair by pair, like below:

```
Query word    Document word    Meaning    Exact word match?
fixing        repair           same       NO
automobile    car              same       NO

Matching words found: 0
Result: keyword search sees NO match

```

Here, we can notice that the meaning lines up perfectly, but the exact words do not. Keyword search only sees the words, so it fails.

This is the core weakness. The word "car" and the word "automobile" mean the same thing, but keyword search treats them as two completely unrelated words. Humans search by meaning, but keyword search matches by spelling.

So, here comes Semantic Search to the rescue.

### What is Semantic Search

Let's decompose the term first.

> Semantic Search = Semantic + Search

The word "semantic" simply means "related to meaning". So Semantic Search is search based on meaning.

Semantic Search finds documents by their meaning, not by their exact words.

In simple words, Semantic Search understands what the user is asking, and it returns documents that mean the same thing, even if they use completely different words.

Let's go back to our last example. The user searches "fixing my automobile". Semantic Search understands that this means the same as "repair your car". So it returns the document about repairing a car, even though the words are different.

The problem is solved. The user finds the right article, because Semantic Search matches meaning instead of spelling.

But now a very natural question arises. A computer does not actually "understand" meaning the way we do. It only works with numbers. So how can a computer compare the meaning of two pieces of text?

The answer is a beautiful idea called embeddings. Let's learn it.

### What is an embedding

This is the most important concept in the whole blog, so let's go slowly.

An embedding is a list of numbers that represents the meaning of a piece of text.

In simple words, an embedding is a way to turn words into numbers, so that a computer can work with the meaning of the words.

A list of numbers like this is called a vector. A vector is just an ordered list of numbers. That is the only thing we need to know about the word "vector" for now. So an embedding is a vector that stands for the meaning of some text.

Let's see what an embedding looks like for a word like below:

```
"car"  ->  [ 0.91, 0.12, 0.88, 0.05, ... ]

```

Here, we can see that the word "car" has been turned into a list of numbers. A real embedding usually has hundreds or even thousands of numbers, but the idea is the same. Each piece of text becomes one list of numbers.

Now, how do we get these numbers? We use a special model called an embedding model. An embedding model is a program that has read a huge amount of text and has learned the meaning of words and sentences. We give it some text, and it gives us back the embedding, which is the list of numbers for that text.

The magic is in how these numbers are chosen. Let's understand that next, because this is what makes Semantic Search actually work.

### How similar meanings sit close together

Here is the key property of embeddings, and the heart of Semantic Search.

The embedding model is built so that texts with similar meanings get similar numbers, and texts with different meanings get very different numbers.

In simple words, if two pieces of text mean the same thing, their lists of numbers will be close to each other. If two pieces of text mean very different things, their lists of numbers will be far apart.

The best way to understand this is to picture the numbers as points in space.

Let's say, just for the sake of understanding, that each embedding has only two numbers. With two numbers, we can draw each text as a point on a simple grid, like a point on a map. The first number is the position left to right, and the second number is the position bottom to top.

Now let's place a few words on this map like below:

```
        meaning space (simplified to 2 numbers)

   ^
   |                                    dog .
   |                              cat .
   |
   |        automobile .
   |        car .
   |     vehicle .
   |
   +----------------------------------------->

```

Here, we can see something very important. The words "car", "automobile", and "vehicle" are all sitting close together, because they mean almost the same thing. The words "cat" and "dog" are sitting close together too, because they are both animals. But the car group and the animal group are far apart, because a car and a cat have nothing to do with each other.

So the embedding model has placed similar meanings near each other and different meanings far away. This is the whole trick.

Now we can finally answer our earlier question. To compare the meaning of two texts, the computer does not need to understand language like a human. It just needs to check how close their two points are. Close points mean similar meaning. Far points mean different meaning.

So, the next question is: how does the computer measure how close two points are? Let's see.

### How we measure closeness with cosine similarity

To measure how close two embeddings are, we use a method called cosine similarity.

Cosine similarity is a number that tells us how similar two embeddings are in meaning.

In simple words, we give cosine similarity two lists of numbers, and it gives us back one score that says how alike they are.

We do not need any heavy math to understand it. We only need to understand what the score means:

- If the score is close to 1, the two texts point in almost the same direction, which means they have very similar meaning.
- If the score is close to 0, the two texts are unrelated in meaning.
- If the score is close to -1, the two texts point in opposite directions, which means they are very different.

So a higher cosine similarity means more similar meaning. That is all we need to remember.

We can picture each embedding as an arrow pointing in some direction, and cosine similarity simply tells us how much two arrows point the same way, like below:

```
  score close to 1            score close to 0            score close to -1
  (same meaning)              (unrelated)                 (opposite)

      A   B                       A                            A
       \ /                        |                            |
        *  same direction         *----- B                     *
                                  (right angle)                |
                                                               B
       almost on top              pointing in totally          pointing in
       of each other              different directions         opposite directions

```

Here, we can notice that when two arrows point almost the same way, the score is close to 1, which means similar meaning. When they sit at a right angle, the score is close to 0, which means unrelated. When they point in opposite directions, the score is close to -1, which means very different.

Let's see it with our example like below:

```
similarity( "car", "automobile" )  =  0.95   -> very similar, almost the same meaning
similarity( "car", "vehicle"    )  =  0.88   -> similar, related meaning
similarity( "car", "banana"     )  =  0.04   -> not related at all

```

Here, we can see that "car" and "automobile" get a very high score, so the system knows they mean almost the same thing. The word "banana" gets a tiny score, so the system knows it is unrelated.

This is exactly the power that keyword search did not have. Cosine similarity lets the computer compare meaning using numbers. Now the word "car" and the word "automobile" are no longer unrelated strings. They are two points sitting very close together, with a high similarity score.

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

Now we have all the pieces. Let's put them together to build a real search system.

### What is a vector database

When we have many documents, we cannot turn each one into an embedding every time a user searches. That would be slow and wasteful. So we do it ahead of time and store the results.

A vector database is a special storage system that holds embeddings and can quickly find the embeddings that are closest to a given one.

In simple words, a vector database is a place where we keep all our lists of numbers, and it is very good at one job: finding which stored lists are nearest to a new list we give it.

Here is the important workflow to understand:

Step 1: We take every document in our collection and pass it through the embedding model. Each document becomes an embedding, which is its list of numbers.

Step 2: We store all these embeddings in the vector database. We do this only once, ahead of time. We can also store the original text next to each embedding, so we can show it to the user later.

So, each document is embedded once and saved. We do not redo this work on every search. This is the same idea as preparing everything in advance so that the actual search is fast.

In a real system, we rarely embed a whole document as one piece. We first cut it into smaller chunks, so that every piece carries one clear meaning. We have a detailed blog on Chunking Strategies for RAG that explains this in depth.

The flow looks like below:

```
PREPARE ONCE (done ahead of time):

  Document 1  -->  embedding model  -->  [numbers]  -->  +-----------------+
  Document 2  -->  embedding model  -->  [numbers]  -->  | vector database |
  Document 3  -->  embedding model  -->  [numbers]  -->  | (all embeddings)|
  ...                                                    +-----------------+

```

Here, we can see that every document is turned into an embedding just once and then placed into the vector database. After this one-time step, our collection is ready to be searched. Now, let's see what happens when a user actually searches.

### The full Semantic Search flow

Now we have everything we need to see the complete picture. Let's walk through a single search from start to finish.

Step 1: The user types a query, for example "fixing my automobile".

Step 2: We pass this query through the same embedding model we used for the documents. This turns the query into its own embedding, which is its list of numbers. It is very important that we use the same embedding model for both the documents and the query, so that they live in the same meaning space and can be compared fairly.

Step 3: We hand this query embedding to the vector database and ask a simple question: which stored embeddings are closest to this one? The vector database uses cosine similarity to compare the query embedding against the stored document embeddings.

Step 4: The vector database returns the documents whose embeddings have the highest similarity scores. These are the nearest ones in meaning. We call them the nearest neighbors, because they are the points sitting nearest to the query point in the meaning space.

Step 5: We show these top documents to the user as the search results.

Let's see the whole flow in one diagram like below:

```
SEARCH (done on every query):

  user query
  "fixing my automobile"
        |
        v
  embedding model  -->  query embedding [numbers]
                              |
                              v
                     +-----------------+
                     | vector database |   find nearest by cosine similarity
                     +-----------------+
                              |
                              v
              top matches (highest similarity):
              1. "How to repair your car at home"   (0.93)
              2. "Car maintenance basics"           (0.81)
              3. "Replacing a flat tyre"            (0.67)

```

Here, we can see the full journey. The query is turned into an embedding, the vector database finds the document embeddings nearest to it, and the closest documents are returned. Notice that the top result is the car repair article, even though it does not share a single important word with the query. The meanings matched, so the search succeeded.

This is exactly what keyword search could not do. The problem is solved.

Note: We must use the same embedding model for both the documents and the query. If we embed the documents with one model and the query with a different model, their numbers will live in different meaning spaces, and the closeness scores will be meaningless.

In real systems, there is often one more step after this. A second model takes the top matches and re-orders them so that the best documents land at the very top. We have a detailed blog on Reranker that covers this end to end.

### Approximate nearest neighbor for speed at scale

So far so good. But there is one practical problem we must handle.

To find the nearest neighbors perfectly, the vector database would have to compare the query embedding against every single document embedding it stores. If we have a few hundred documents, that is fine. But real systems often have millions or even billions of documents. Comparing against every one of them on every search would be too slow.

So, here comes approximate nearest neighbor to the rescue. It is often shortened to ANN.

> ANN = Approximate Nearest Neighbor

Approximate nearest neighbor is a technique that finds the nearest embeddings very quickly, without checking every single one.

In simple words, instead of comparing the query against all billion documents one by one, the vector database uses a clever structure that lets it jump close to the right area and check only a small number of candidates.

The word "approximate" is the key. It means the result is almost always the true nearest neighbors, but not guaranteed to be perfect every single time. We give up a tiny bit of accuracy, and in return we get a massive boost in speed.

Let's compare the two approaches like below:

```
Exact search:        compare query against ALL embeddings   -> perfect, but slow at scale
Approximate (ANN):   compare query against a SMALL subset   -> almost perfect, and very fast

```

Here, we can see the trade-off clearly. Exact search checks everything and is always correct, but it becomes too slow when there are millions of documents. ANN checks only a small, smart selection and is almost always correct, but it stays fast no matter how large the collection grows.

For real systems, this trade is well worth it. A result that is 99 percent as accurate but returned in a few milliseconds is far better than a perfect result that takes several seconds. This is why almost every large vector database uses approximate nearest neighbor under the hood.

So, now we know how Semantic Search stays fast even with a huge number of documents.

### Semantic Search in the real world

Now, let's see where Semantic Search is used in real systems.

The first and most obvious place is search itself. When we search inside an app, a help center, or a website, Semantic Search lets us find the right result even when we do not use the exact words present in the documents. We can ask in our own natural language, and the system still understands what we mean.

In real products, Semantic Search often runs together with keyword search, and their results are merged into one final list. We have a detailed blog on Hybrid Search that explains how this works.

The second place is RAG. RAG stands for Retrieval-Augmented Generation. In simple words, it is a system where we first fetch some relevant documents and then send them to a large language model along with the user's question, so the model can answer using real information. A large language model, or LLM, is the technology behind tools like ChatGPT and Claude. The "fetch the relevant documents" part of RAG is done with Semantic Search. We embed the user's question, find the nearest document embeddings, and feed those documents to the model. This is how AI assistants answer questions about our own private documents accurately.

The fetching part of RAG does not always have to work this way. We have a detailed blog on Vectorless RAG that explains how a model can reach the right section by reading the structure of a document step by step.

The third place is recommendations. When an app suggests "items similar to this one", it can embed each item and then find the items whose embeddings are nearest to the one we are looking at. Since nearby embeddings mean similar items, the app recommends things that are genuinely related. This is the same nearest-neighbor idea, just applied to products, songs, or videos instead of search queries.

So, anywhere we need to match things by meaning rather than by exact words, Semantic Search helps us a lot.

This is how Semantic Search works. We turn every document into an embedding and store it in a vector database once, we turn the user's query into an embedding using the same model, we use cosine similarity with approximate nearest neighbor to quickly find the closest embeddings, and we return those documents as results, so the user finds the right answer by meaning even when not a single word matches.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
