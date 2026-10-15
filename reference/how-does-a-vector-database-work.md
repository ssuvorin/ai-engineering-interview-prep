> Source: https://outcomeschool.com/blog/how-does-a-vector-database-work

# How does a Vector Database work?
URL: https://outcomeschool.com/blog/how-does-a-vector-database-work
Published: 2026-06-06
Author: Amit Shekhar

How does a Vector Database work?

# How does a Vector Database work?

Authors
: - Name
: Amit Shekhar
Published on
: June 6, 2026

A Vector Database is a special kind of database that stores data as lists of numbers and helps us find items that are similar in meaning, not just items that match exactly.

In this blog, we will learn about how a Vector Database works. This is one of the most important pieces behind modern AI search, recommendations, and tools like ChatGPT that answer questions from our own documents.

We will cover the following:

- What is a Vector Database?
- A quick recap of embeddings
- Why normal databases fall short
- What a Vector Database actually stores
- How do we measure similarity?
- Cosine similarity
- Dot product
- Euclidean distance
- The nearest neighbour problem
- Why brute force is too slow
- Approximate Nearest Neighbour (ANN) and indexing
- HNSW explained simply
- IVF explained simply
- PQ explained simply
- A small code example
- Real-world applications of Vector Databases

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a Vector Database?

A Vector Database is a special kind of database that stores data as numbers and helps us find items that are similar in meaning, not just items that match exactly.

In simple words, a normal database is good at finding exact matches. A vector database is good at finding things that are close in meaning.

Let's decompose the term:

Vector Database = Vector + Database

A Database is just an organized place to store data so that we can find it later. A Vector is simply a list of numbers, for example `[0.21, 0.87, 0.13]`.

So, a Vector Database is a database built to store lists of numbers and to quickly find the lists that are most similar to a given list.

Now, the obvious question is: why would we store data as a list of numbers? To answer that, we must first recall what embeddings are.

### A quick recap of embeddings

Before jumping into vector databases, we must know about embeddings, because vectors come from embeddings.

An embedding is a list of numbers that represents the meaning of something, for example a word, a sentence, an image, or a song.

A special AI model reads our data and turns it into these numbers. The model is trained in such a way that things with similar meaning get similar numbers. Since calling embedding models costs both time and money, we have a detailed blog on how an Embedding Cache works that explains how to avoid recomputing them for the same text.

Let's say we turn three words into embeddings:

```
"king"   ->  [0.91, 0.12, 0.55]

"queen"  ->  [0.89, 0.15, 0.58]

"banana" ->  [0.10, 0.95, 0.03]

```

Here, we can see that `king` and `queen` have numbers that are close to each other, because they are related in meaning. The word `banana` has very different numbers, because it has nothing to do with kings and queens.

This is the key idea: similar meaning gives similar numbers. Each embedding is a vector, and that is exactly what we store inside a vector database.

If we are curious how a model learns to place similar meanings close together and push different ones apart, we have a detailed blog on Contrastive Learning that explains how it works.

Now that we have recalled embeddings, let's understand why a normal database is not enough.

### Why normal databases fall short

A normal database, for example MySQL or PostgreSQL, is excellent at exact matching.

Suppose we search for the word `apple`. A normal database will find every row that contains exactly the word `apple`. This works perfectly when we know the exact value we are looking for.

But, here is the catch. What if the user searches for `fruit that keeps the doctor away`? A normal database will look for those exact words. It does not understand that the answer is `apple`. It has no sense of meaning.

Let's say we have these documents:

- "An apple a day keeps the doctor away."
- "Bananas are rich in potassium."
- "The doctor recommended eating more fruits."

If we search `healthy fruit advice from a doctor`, a normal database will struggle, because none of the documents contain that exact phrase. It matches words, not meaning.

We can picture this difference like below:

```
Query: "healthy fruit advice from a doctor"

        |                              |
        v                              v

  Normal Database                 Vector Database
  (matches EXACT words)           (matches MEANING)

        |                              |
        v                              v

  No row has these                Finds the apple article
  exact words                     and the doctor article

        |                              |
        v                              v

  Result: misses the meaning      Result: closest in meaning

```

Here, we can see that the same query goes to both, but the normal database fails because no row contains those exact words, while the vector database succeeds because it looks at meaning and returns the closest matches.

Note: Out of the box, a normal database matches exact words and falls short here. Some databases can now add vector search through an extension, for example PostgreSQL with `pgvector`. But they do this using the very same vector search ideas we are about to learn. So the real question is not normal database versus vector database. It is whether the database can search by meaning at all.

So, we need a system that understands meaning and finds the closest matches even when the exact words are different. This is where the vector database comes into the picture.

### What a Vector Database actually stores

A vector database stores three things together for each item:

- The vector - the list of numbers (the embedding) that represents the meaning.
- The original data - the actual text, image link, or product, so that we can show it back to the user.
- The metadata - extra information like category, date, author, or price, used for filtering.

Let's say we store an article about apples. Inside the vector database, it looks like below:

```
ID:        101

Vector:    [0.91, 0.12, 0.55, ... ]

Data:      "An apple a day keeps the doctor away."

Metadata:  { "category": "health", "year": 2024 }

```

Here, we can see that the vector carries the meaning, the data is what we show to the user, and the metadata helps us filter results, for example showing only articles from the year 2024.

There are two ways to use this metadata while searching. We can filter first and then run the similarity search only on the items that pass the filter, which is called pre-filtering. Or we can run the similarity search first and then drop the results that do not match the filter, which is called post-filtering. Pre-filtering is usually the better choice, because it does not waste the search on items we will throw away anyway.

This is how a vector database keeps both the meaning and the original content side by side.

To learn Embeddings, Vector Databases, and how they power search by meaning in depth, check out our AI and Machine Learning Program at Outcome School.

### How do we measure similarity?

Now we have a bunch of vectors stored. When a user searches, we convert their search into a vector too. Then we need to find the stored vectors that are most similar to it.

But, how do we measure how similar two vectors are? We use a similarity metric. A similarity metric is just a formula that takes two vectors and gives back a number that tells us how close they are.

There are three common metrics: cosine similarity, dot product, and euclidean distance. Do not worry, we will learn about each of them in detail, with a formula, an example, and a diagram.

### Cosine similarity

Cosine similarity measures the angle between two vectors. It does not care how long the vectors are. It only cares about the direction they point in.

In simple words, if two vectors point in the same direction, they are similar, even if one is longer than the other.

The result is always between -1 and 1:

- A value close to 1 means the vectors point in almost the same direction, so they are very similar.
- A value close to 0 means the vectors are at a right angle, so they are unrelated.
- A value close to -1 means the vectors point in opposite directions, so they are very different.

We can picture it like below:

```
small angle  ->  cosine near 1  (very similar)

       B
      /
     /
    /
   +---------- A

right angle  ->  cosine near 0  (unrelated)

   B
   |
   |
   |
   +---------- A

```

Here, we can see that a small angle means the arrows point almost the same way, which gives a value near 1. A right angle means they are unrelated, which gives a value near 0.

The formula is as below:

```
cosine similarity = (A · B) / (|A| × |B|)

```

Here, `A · B` is the dot product, which we get by multiplying the matching numbers of the two vectors and adding them up. `|A|` and `|B|` are the lengths, or sizes, of the two vectors. We will look at the dot product more closely in the very next section, but this one line is all we need for now.

Let's see it in action with an example. Suppose we have two vectors:

```
A = [2, 3]
B = [4, 6]

```

Notice that B is just A with every number doubled, so both point in the exact same direction.

Step 1: Multiply the matching numbers and add them up. This gives the dot product.

```
A · B = (2 × 4) + (3 × 6) = 8 + 18 = 26

```

Step 2: Find the length of A. The length is found by squaring each number, adding them, and taking the square root.

```
|A| = √(2² + 3²) = √(4 + 9) = √13 ≈ 3.61

```

Step 3: Find the length of B in the same way.

```
|B| = √(4² + 6²) = √(16 + 36) = √52 ≈ 7.21

```

Step 4: Divide the dot product by the two lengths multiplied together.

```
cosine similarity = 26 / (3.61 × 7.21) ≈ 26 / 26.0 ≈ 1.0

```

The result is 1.0, which means the two vectors are as similar as possible. This matches what we expected, because they point in the same direction.

Note: The full range of cosine similarity is -1 to 1. But many modern embedding models give us normalized vectors, and with those the value usually stays between 0 and 1 in practice. So in real text search, we rarely see negative values.

This is why cosine similarity is the most popular choice for text and semantic search. Two sentences with the same meaning point in the same direction, even if one is much longer than the other.

### Dot product

Dot product is the simplest of the three. We multiply the matching numbers of the two vectors and add up all the results into a single number.

The formula is as below:

```
A · B = (a₁ × b₁) + (a₂ × b₂) + (a₃ × b₃) + ...

```

In simple words, we line up the two lists of numbers, multiply them position by position, and add everything together.

Let's see it with an example. Suppose we have:

```
A = [1, 2, 3]
B = [4, 5, 6]

```

Then the dot product is below:

```
A · B = (1 × 4) + (2 × 5) + (3 × 6)
      =    4    +   10    +   18
      =            32

```

We can picture the same idea like below:

```
A:    1      2      3
      ×      ×      ×        (multiply each matching pair)
B:    4      5      6
      =      =      =
      4   +  10  +  18   =   32     (then add the results)

```

Here, we can see that each number in A is multiplied with the number right below it in B, and then all of them are added to give a single number, 32.

A larger dot product means more similarity. Let's check this with one more vector:

```
C = [0, 0, 1]

A · C = (1 × 0) + (2 × 0) + (3 × 1) = 0 + 0 + 3 = 3

```

Here, we can see that A and B give 32, while A and C give only 3. So A is much more similar to B than to C.

But, here is the catch. The dot product is affected by the size of the vectors, not just their direction. A longer vector can give a bigger dot product even when the direction is not a great match. This is why the dot product works best when all vectors are normalized, which means scaled to the same length. When the vectors are the same length, the dot product and cosine similarity agree with each other.

This is why the dot product is a fast and popular choice when our vectors are already normalized.

### Euclidean distance

Euclidean distance measures the straight-line distance between two points. It is the same distance we would measure with a ruler between two dots on paper.

For this metric, we treat each vector as a point in space. The closer the two points are, the more similar they are. So, unlike the previous two metrics, here a smaller value means more similar.

The formula is as below:

```
distance = √( (a₁ - b₁)² + (a₂ - b₂)² + ... )

```

In simple words, we subtract the matching numbers, square each result, add them up, and take the square root.

Let's see it with an example. Suppose we have two points:

```
A = [1, 2]
B = [4, 6]

```

Step 1: Subtract the matching numbers.

```
(1 - 4) = -3      and      (2 - 6) = -4

```

Step 2: Square each result.

```
(-3)² = 9      and      (-4)² = 16

```

Step 3: Add them and take the square root.

```
distance = √(9 + 16) = √25 = 5

```

So the distance between A and B is 5.

We can picture it on a simple grid like below:

```
 y
 6 |                  B (4, 6)
 5 |                / :
 4 |              /   :  vertical gap = 4
 3 |            /     :
 2 | A (1, 2) ........:
 1 |          horizontal gap = 3
 0 +----------------------- x
   0   1   2   3   4   5

```

Here, we can see that the horizontal gap is 3 and the vertical gap is 4, and the euclidean distance is just the length of the straight line joining the two points, which comes out to 5.

Let's check with one more point:

```
C = [1, 3]

distance from A = √( (1 - 1)² + (2 - 3)² ) = √(0 + 1) = 1

```

Here, we can see that C is at a distance of 1 from A, while B is at a distance of 5. So C is much closer to A, which means C is more similar to A than B is.

This is why euclidean distance is a natural choice for image and spatial data, where the actual position and the gap between points carry meaning.

Now that we have learned all three metrics, let me tabulate the differences between them for your better understanding so that you can decide which one to use based on your use case.

| Metric | What it measures | Similar means | Common use |
| --- | --- | --- | --- |
| Cosine similarity | Angle between vectors | Value close to 1 | Text and semantic search |
| Dot product | Direction and size combined | Larger value | When vectors are normalized |
| Euclidean distance | Straight-line gap | Smaller distance | Image and spatial data |

Here, we can notice that cosine similarity and dot product give a higher number for similar items, while euclidean distance gives a lower number for similar items. We just pick the metric that fits our data.

This is how we measure similarity. Now, let's understand the actual problem of finding the closest vectors.

### The nearest neighbour problem

When a user searches, we convert their query into a vector. Then we want to find the stored vectors that are nearest to it.

This is called the nearest neighbour problem. In simple words, given one vector, find the closest vectors from millions of stored vectors.

Let's say the user searches `healthy fruit`. We turn it into a vector. Then we compare it against every stored vector and pick the top few that are most similar.

The top results will be the apple article and the banana article, because both are about healthy fruits, even though the user never typed those exact words. That is the magic of searching by meaning.

Let's see the full journey of a search from start to finish as below:

```
User query (text)
"healthy fruit"

      |
      v

Embedding Model
(turns text into numbers)

      |
      v

Query Vector
[0.90, 0.13, 0.56, ...]

      |
      v

Vector Database
(similarity search)

      |
      v

Top matching results
(apple article, banana article)

```

Here, we can see that the user types plain text, the embedding model turns it into a query vector, the vector database compares that vector against the stored ones, and finally it returns the top matching results that are closest in meaning.

So, the goal is simple: find the nearest neighbours of the query vector. Now, the next big question is how to do this fast.

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

### Why brute force is too slow

The simplest way to find the nearest neighbours is brute force.

In brute force, we compare the query vector with every single stored vector, one by one, and keep the closest ones.

Let's say we have 10 vectors. Comparing against all 10 is easy and quick. But, real applications do not have 10 vectors. They have millions or even billions.

Suppose we have 100 million vectors, and each vector has 1000 numbers. For one search, we would do 100 million comparisons, and each comparison touches 1000 numbers. That is 100 billion calculations for a single search.

And, users expect results in a few milliseconds. Brute force simply cannot keep up at this scale.

The issue with this approach is that it is too slow for large data. Let's see how the next approach solves this issue.

### Approximate Nearest Neighbour (ANN) and indexing

So, here comes the idea of Approximate Nearest Neighbour, often written as ANN, to the rescue.

The key insight is this: we do not always need the perfect closest match. We need a very close match, returned very fast.

In simple words, ANN trades a tiny bit of accuracy for a huge gain in speed. Instead of checking every vector, it cleverly skips most of them and only checks the ones that are likely to be close.

Let's compare the two approaches like below:

```
Brute force (exact):
query  ->  compare with ALL 100,000,000 vectors  ->  perfect match, but very slow

ANN (approximate):
query  ->  jump to the promising area  ->  check only a few thousand  ->  very close match, super fast

```

Here, we can see that brute force checks everything to be perfectly correct, while ANN jumps close to the answer and checks only a small part of the data.

Now, the question is: how close is good enough? We measure this with recall. Recall tells us how many of the truly closest vectors our search managed to find.

Let's say the true top 10 closest vectors are the perfect answer. If ANN returns 9 of those 10, the recall is 90 percent. In most real applications, returning 9 out of 10 in a few milliseconds is far better than returning all 10 but taking several seconds.

To make this skipping possible, the vector database builds an index. An index is a smart structure that organizes the vectors in advance, so that during a search we can jump straight to the promising area instead of scanning everything.

Let's understand this with a simple example. Suppose we want to find a friend living in a city. Brute force means knocking on every single door in the whole country. An index is like first going to the right city, then the right street, and only then checking a few houses. We reach the answer much faster.

Three of the most popular techniques here are HNSW, IVF, and Product Quantization, often written as PQ. HNSW and IVF help us decide which vectors to check, while PQ helps us shrink each vector to save memory. Let's understand them one by one.

### HNSW explained simply

HNSW stands for Hierarchical Navigable Small World. The name sounds heavy, but the idea is simple. Let's decompose it:

- Hierarchical means it is built in layers, stacked on top of each other.
- Navigable Small World means the points are connected to each other like friends in a social network, where we can reach anyone in just a few hops.

So, we can think of it as a layered map of connections, where similar vectors are linked to each other like friends in a network.

Let's understand it layer by layer.

The top layer has very few points, spread far apart. It is like a map showing only big cities. We can jump across large distances quickly.

The middle layers have more points, closer together. It is like a map showing towns within a region.

The bottom layer has all the points, very close together. It is like a street-level map showing every house.

When we search, we start at the top layer and take big jumps toward the area near our query. Then we move down to the next layer and take smaller, more careful steps. We keep going down until we reach the bottom layer, where we find the final closest neighbours.

Here is a simple picture of the search. Let's say we are looking for the point closest to our query, and the answer turns out to be `E`:

```
Layer 2 (top):     A --------------- F        few points, big jumps
                                     |
                                     v
Layer 1 (middle):  A --- C --- D --- F        more points, medium steps
                           |
                           v
Layer 0 (bottom):  A-B-C-D-E-F-G-H            all points, fine steps  ->  reach E

```

Here, we can see that we begin with big jumps at the top, then take medium steps in the middle, and finally take fine steps at the bottom to land on the closest point `E`. We never had to check every single point.

Let's walk through it once more in simple words:

- Step 1: Enter at the top layer, where only a few points exist. Move to the point closest to our query. This covers a lot of ground in one big jump.
- Step 2: Drop down to the middle layer. From the point we reached, move to an even closer neighbour.
- Step 3: Drop down to the bottom layer. Take small, careful steps among the closely packed points until we reach the nearest one.

This is how HNSW gives us very fast and very accurate searches. It is the most widely used index in modern vector databases.

### IVF explained simply

IVF stands for Inverted File Index. This is another clever way to speed up the search.

The idea is to group similar vectors into clusters before any search happens. This grouping is done once, in advance.

Let's say we group all our vectors into a few clusters. Each cluster has a center point, which represents the average of that group. We can picture the clusters like below:

```
   Cluster 1          Cluster 2          Cluster 3
  +----------+       +----------+       +----------+
  |  x    x  |       |  x   x   |       |  x  x  x |
  |    C1    |       |    C2    |       |    C3    |
  |  x    x  |       |   x   x  |       |   x   x  |
  +----------+       +----------+       +----------+

  C1, C2, C3 are the center points (the average of each group)
  each x marks one stored vector inside the cluster

```

Here, we can see that the vectors are divided into groups, and each group has one center point that sits in the middle of it.

Now, when a user searches, we do the following.

First, we compare the query vector with only the cluster centers, not the millions of vectors. Then, we pick the few clusters whose centers are closest to the query. After that, we search only inside those few clusters and ignore the rest.

Let's see the search journey like below:

```
Query
  |
  v
Compare with cluster centers only      (cheap, just a few comparisons)
  |
  v
Pick the closest clusters              (say, the 3 nearest clusters)
  |
  v
Search only inside those clusters      (ignore all the other clusters)

```

Here, we can see that IVF first narrows down to a few clusters, then searches only inside them.

Let's put real numbers to see the saving. Suppose we have 100 million vectors split into 100 clusters, so each cluster holds 1 million vectors. If we search only the 3 closest clusters, we check 3 million vectors instead of 100 million. That is a huge saving, and the search becomes much faster than brute force.

Note: There is a small trade-off. If the true closest vector happens to sit in a cluster we skipped, we will miss it. To reduce this risk, we can search a few more clusters, which improves accuracy but takes a little more time. We tune this based on our use case.

### PQ explained simply

PQ stands for Product Quantization. As we just saw, HNSW and IVF help us pick which vectors to check. PQ is different. It does not pick vectors. It shrinks each vector so that it takes much less memory.

Let's understand the memory problem first. Suppose each vector has 128 numbers, and each number takes 4 bytes. That is 512 bytes fo
