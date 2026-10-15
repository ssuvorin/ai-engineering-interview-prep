> Source: https://outcomeschool.com/blog/vectorless-rag

# What is Vectorless RAG? RAG Without Embeddings or a Vector Database
URL: https://outcomeschool.com/blog/vectorless-rag
Published: 2026-09-10

What is Vectorless RAG? RAG Without Embeddings or a Vector Database

# What is Vectorless RAG? RAG Without Embeddings or a Vector Database

Authors
: - Name
: Amit Shekhar
Published on
: September 10, 2026

In this blog, we will learn about Vectorless RAG, a way of answering questions from our own documents without converting those documents into numbers and without using any vector database. We will also see how the normal RAG works, why the vector part creates problems, how a Vectorless RAG system reads a document the way a human reads a book, how the tree structure and the search happen step by step, what the advantages and disadvantages are, and when to use which one.

We will cover the following:

- What is an LLM
- What is RAG
- How the normal Vector RAG works
- Problems with Vector RAG
- What is Vectorless RAG
- How Vectorless RAG works
- An example of Vectorless RAG
- Other Vectorless approaches
- Advantages of Vectorless RAG
- Disadvantages of Vectorless RAG
- Vector RAG vs Vectorless RAG
- When to use which one

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is an LLM

Before jumping into Vectorless RAG, we must know what an LLM is.

LLM = Large Language Model.

In simple words, an LLM is an AI Model that has read a huge amount of text and learned how language works. When we ask it something, it writes an answer one word at a time.

ChatGPT, Claude, and Gemini are all based on LLMs.

But there is a catch. An LLM only knows what it read during its training. It has never seen our office documents, our insurance policy, our company handbook, or the report we wrote last week.

So, if we ask an LLM a question about our own document, it cannot answer. It was never taught that.

We needed a solution for that, and RAG was introduced to solve this problem.

## What is RAG

RAG = Retrieval + Augmented + Generation.

Let's break it down in simple words:

- Retrieval: find the useful part of our document.
- Augmented: add that part to the question.
- Generation: let the LLM write the answer using it.

So, RAG is a very simple idea. We do not teach the model anything new. We just hand it the right page at the right time.

Let's take an example.

Suppose we have a 300 page insurance policy. We ask, "Is dental treatment covered?"

Instead of sending all 300 pages to the LLM, we find the two pages that talk about dental treatment, and we send only those two pages along with our question.

The LLM reads those two pages and answers.

Think of it like an open book exam. The LLM is the student. Our document is the book. Retrieval is the act of finding the correct page.

Now, the following question arises. Why do we not simply hand over all the 300 pages every single time?

There are three reasons. First, an LLM can read only a limited amount of text at one time, and a large pile of documents will never fit. Second, we pay for every word we send, so sending the whole book for every small question becomes very costly. Third, and the most important one, when we bury the useful two pages inside 300 pages, the model gets distracted and the answer becomes worse.

We have a detailed blog on The Lost in the Middle Problem in LLMs that explains this third reason in depth.

So, we must send less text, and that less text must be the correct text.

Now, the question is, how do we find the correct page? This is exactly where the two approaches differ.

## How the normal Vector RAG works

Most RAG systems today use vectors. Let's understand this first, because Vectorless RAG only makes sense once we know what it is replacing.

Before that, we must know what a vector is.

A vector is just a long list of numbers, something like `[0.12, -0.88, 0.45, ...]`. There can be hundreds or thousands of numbers in that list.

There is a special model called an embedding model. We give it a piece of text, and it gives back a vector. The important part is this: text with a similar meaning gets a similar list of numbers.

So, the sentence "I love dogs" and the sentence "I like puppies" will get two lists of numbers that are very close to each other. The sentence "The stock market crashed" will get a list of numbers that is far away from both.

Means, the meaning of a sentence has been turned into a position. Close numbers mean close meaning.

This way of searching by meaning instead of by exact words is called semantic search. We have a detailed blog on How does Semantic Search work? that covers this end to end.

Now, let's see how a Vector RAG system is built. It happens in two phases. Do not worry, we will learn about each of them in detail.

Phase 1: Preparing the document.

First, we take our 300 page document and cut it into small pieces. Each piece is usually a few hundred words. These pieces are called chunks.

Then, we pass every chunk through the embedding model and get one vector for each chunk.

After that, we store all these vectors in a vector database. A vector database is a special storage that is very fast at one job, which is finding the vectors that are closest to a given vector.

Now our document is ready for searching.

Phase 2: Answering the question.

First, the user asks a question.

Then, we pass the question through the same embedding model and get a vector for the question.

After that, we ask the vector database to find the chunks whose vectors are closest to the question vector. Usually we ask for the closest 5 or 10 chunks. This number is called top-k.

Finally, we put those chunks and the question together and send them to the LLM, and the LLM writes the answer.

This is how Vector RAG works. It is a good approach, and it powers a huge number of products today.

But the following issues arise.

## Problems with Vector RAG

Problem 1: Chunking breaks the meaning.

We cut the document into pieces using a fixed size. The document does not care about our fixed size. A sentence can get cut in half. A table can get separated from its heading. A rule can get separated from its exception.

Let's say the policy says on one page, "Dental treatment is covered." And two pages later it says, "All treatments mentioned in Chapter 3 apply only after a waiting period of one year."

These two lines live in two different chunks. The system may pick the first chunk and miss the second one. The answer will be confidently wrong.

Problem 2: Similar is not the same as correct.

The vector database finds text that sounds similar to the question. Sounding similar is not the same as being the right answer.

If we ask, "Which policy does not cover dental treatment?", the word "not" is a tiny word. It barely moves the numbers. So, the system happily returns the chunks about policies that do cover dental treatment.

Problem 3: There is no thinking during the search.

The search is pure mathematics. It measures distance. It does not reason. It cannot say, "This question is about a rule and its exception, so I must look in two different chapters."

Problem 4: We cannot explain the result.

When a wrong chunk is picked, we cannot ask the vector database why. It returns numbers. Debugging becomes very hard.

Problem 5: There is a whole system to maintain.

We need an embedding model, a vector database, a chunking strategy, and a re-embedding job that runs every time a document changes. If we ever want to switch to a better embedding model, we must rebuild everything from the start.

Problem 6: Special words and numbers suffer.

Product codes, invoice numbers, medical terms, legal clause numbers, and tables do not carry much meaning for an embedding model. `Clause 14.2.b` and `Clause 14.3.b` look almost identical to it.

Problem 7: The number of chunks is fixed.

We decide the top-k value once, and it stays the same for every question. But one question may need a single line, and another question may need six full sections. A fixed number is either bringing too little or bringing too much noise.

So, here comes Vectorless RAG to the rescue.

## What is Vectorless RAG

Vectorless RAG = RAG without the vectors.

Vectorless RAG is a way of doing retrieval without converting our documents into vectors and without using any vector database. Instead of searching by number similarity, we let the LLM itself look at the structure of the document and decide which part to open, exactly the way a human finds an answer in a book.

In simple words, we replace mathematics with reading, and that too without cutting our document into pieces.

Let's understand this with something that we all must have done at some point.

Suppose we buy a washing machine and we want to know about the warranty. We get a 200 page manual.

What do we do? We do not measure the similarity of anything. We open the table of contents at the front. We run our eyes down the chapter names. We see "Chapter 9: Warranty and Service". We jump to page 154. We read it. We answer.

That is it. That is the whole idea of Vectorless RAG.

We give the LLM the table of contents, and we let it choose the page.

Note: The word "Vectorless" only means that we are not using embedding vectors for the search. We are still using an LLM to read and to write the final answer.

To learn RAG, Vector Databases, and Embeddings, check out our AI and Machine Learning Program at Outcome School, where we also build an AI Tutor from scratch.

## How Vectorless RAG works

Let's see how this happens step by step. It also has two phases.

Phase 1: Preparing the document.

So, here comes the tree into the picture. Instead of cutting the document into equal pieces, we build a tree out of it.

A tree here means the same thing as a table of contents. The book is at the top. Chapters come under the book. Sections come under the chapters. Sub-sections come under the sections.

For every node of this tree, we store three things:

- The title of that section, for example "3.4 Dental Treatment".
- A short summary of what that section says, written in one or two lines.
- The location of the real text, for example pages 41 to 43.

We do not store any numbers. We do not cut anything. The original document stays as it is, whole and untouched.

Building this tree is a one time job. If the document already has a table of contents, we can use it directly. If it does not have one, we let the LLM read section by section and write the titles and the summaries for us.

Phase 2: Answering the question.

Step 1: The user asks a question.

Step 2: We show the LLM only the top level of the tree, which is just the chapter names and their one line summaries. This is very small, maybe one page of text, even for a document of 300 pages. So, this step stays cheap and fast.

Step 3: We ask the LLM a simple question: "Based on these chapter names and summaries, which chapters can hold the answer?" The LLM picks one or more chapters and also tells us why it picked them.

Step 4: We open only the chosen chapters and show the LLM the sections inside them. The LLM picks again.

Step 5: We keep going down, level by level, until we reach the actual sections. This walking down the tree is called tree search.

Step 6: Now we pull the real, full text of those chosen sections. Nothing is cut in the middle, because we are taking complete sections.

Step 7: We send the question and that full text to the LLM, and it writes the final answer, along with the section number it used.

Here, we can notice one beautiful thing. At every step, a thinking model made the decision, and at every step it told us why. So, if the answer is wrong, we can open the trail and see exactly where it took the wrong turn.

Note: This is also called reasoning based retrieval, because the system reasons its way to the answer instead of measuring a distance between numbers.

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

## An example of Vectorless RAG

The best way to learn this is by taking an example.

Let's come back to our 300 page insurance policy. Our question is, "Is dental treatment covered in the first year?"

Assume that we have already built the tree of this policy, kept short here just for the sake of understanding, like below:

```text
Insurance Policy
|
|-- Chapter 1: Definitions
|-- Chapter 2: How to Buy the Policy
|-- Chapter 3: What is Covered
|     |-- 3.1 Hospital Stay
|     |-- 3.2 Surgery
|     |-- 3.3 Eye Care
|     |-- 3.4 Dental Treatment
|-- Chapter 4: What is Not Covered
|-- Chapter 5: Waiting Periods
|-- Chapter 6: How to Claim

```

Let's first see what a Vector RAG system does.

It looks for chunks that sound like "dental treatment covered first year". The word "dental" appears in Chapter 3 many times, so it returns five chunks from `3.4 Dental Treatment`. All five chunks talk about dental treatment being covered.

Chapter 5 says, "Dental treatment has a waiting period of 12 months." But that single line was sitting inside a long chunk about many different waiting periods, and it did not sound close enough to our question.

So, the LLM sees only the chunks that say yes, and it answers, "Yes, dental treatment is covered."

The answer is wrong.

Now, let's see what a Vectorless RAG system does.

The LLM sees the six chapter names. It thinks like this: "The user is asking two things. One, is dental treatment covered. Two, is it covered in the first year. The first part is in Chapter 3. The second part is about time, so it is in Chapter 5."

It picks Chapter 3 and Chapter 5.

Then it goes one level down inside Chapter 3 and picks `3.4 Dental Treatment`.

Then we pull the full text of `3.4` and the full text of Chapter 5, and we send both to the LLM.

Now the LLM has both halves of the truth in front of it, and it answers, "Dental treatment is covered, but not in the first year. There is a waiting period of 12 months, as per Chapter 5."

The answer is correct. Problem Solved!

Here, we can see the real difference. The vector system searched for words that sound alike. The vectorless system understood the question and went to look for the rule and its exception, the way a careful human would.

> In Vector RAG, we search with mathematics. In Vectorless RAG, we search with reading.

This way we can use Vectorless RAG to solve the interesting problem of finding an answer that is hiding in two different places at once.

If we want to go deep into how to design a RAG System (Chat with Your Documents), along with AI Agent and Agentic AI, check out our AI and Machine Learning Program at Outcome School.

## Other Vectorless approaches

The tree search is the most popular way, but it is not the only vectorless way. Let's see a few more.

Keyword search. This is the old and trusted way of matching the actual words, the same way we search inside a file. If the user asks for `Invoice INV-2024-8891`, keyword search will find that exact string every single time, while an embedding model may bring back a hundred similar looking invoice numbers.

Filtering on structured data. If our data lives in a normal database with columns like date, city, and amount, we do not need any search at all. We let the LLM write a query, we run it, and we give the rows back to the LLM. Numbers and dates are handled perfectly this way.

Giving the full document. Modern LLMs can read a very large amount of text in one go. If our document is small enough to fit, we can simply give the whole thing along with the question. There is no retrieval step at all. It is the simplest approach, and for a single contract or a single report, it works perfectly.

Letting the model browse the files. We can also give the LLM a set of tools, such as list the folders, open a file, and search inside a file. Then the LLM explores our files on its own, one step at a time, the way a developer explores a new codebase. This is often called agentic search.

All of these are vectorless. Not a single vector is created in any of them.

A coding agent works exactly this way inside our codebase. We have a detailed blog on how Claude Code works that explains how it finds the right file without creating a single embedding.

This was all about the different vectorless approaches. Now, let's discuss the advantages and the disadvantages of Vectorless RAG.

## Advantages of Vectorless RAG

- No chunking. We always read complete sections, so a rule never gets separated from its exception.
- No vector database and no embedding model. There is one less system to build, to pay for, and to maintain.
- Easy updates. When a document changes, we update the summary of that one section. There is no re-embedding of anything.
- We can see the reasoning. At every step, the LLM tells us why it opened a particular chapter. Debugging becomes simple.
- Special words work well. Clause numbers, product codes, and medical terms are read as real words, not turned into a blur of numbers.
- Better answers on long and structured documents. Reports, policies, manuals, and legal papers already have a clean structure, and this approach uses that structure instead of throwing it away.
- Real reasoning during the search. The system can decide to look in two far apart chapters because the question needs both.

In short, it makes our life easy when the documents are long and the answers must be correct.

## Disadvantages of Vectorless RAG

- It is slower. Walking down the tree needs a few LLM calls, one for each level. A vector search finishes in milliseconds.
- It costs more per question. Every LLM call costs money. A vector search is close to free once the vectors are stored.
- It needs structure. If our data is ten million random support chat messages with no titles and no sections, there is no meaningful tree to build.
- The quality depends on the summaries. If a section summary is written poorly, the LLM may skip that section. The summary is doing the job that the vector used to do.
- It does not scale to millions of documents on its own. Searching inside one long document is easy. Choosing between five million documents needs some cheap first filter before the tree search can begin.

## Vector RAG vs Vectorless RAG

Now that we have learned about both of them, it's time to put them side by side.

Let me tabulate the differences between Vector RAG and Vectorless RAG for your better understanding so that you can decide which one to use based on your use case.

| Vector RAG | Vectorless RAG |
| --- | --- |
| Documents are converted into vectors. | Documents are kept as they are. |
| Needs an embedding model. | Does not need an embedding model. |
| Needs a vector database. | Does not need a vector database. |
| Documents are cut into fixed size chunks. | Documents are kept whole and read section by section. |
| Search happens by measuring distance between numbers. | Search happens by the LLM reading titles and summaries and choosing. |
| There is no reasoning during the search. | There is reasoning at every step of the search. |
| Very fast, in milliseconds. | Slower, because it needs a few LLM calls. |
| Very cheap for each question. | Costlier for each question. |
| Hard to explain why a chunk was picked. | Easy to explain, because the LLM gives its reason. |
| Scales very well to millions of documents. | Works best on long and well structured documents. |
| Updating a document needs re-embedding. | Updating a document needs only a summary update. |
| Struggles with exact codes, numbers, and negation. | Handles exact codes, numbers, and negation well. |

## When to use which one

[…553ln elided…]
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

# How does HyDE work in RAG?
URL: https://outcomeschool.com/blog/how-does-hyde-work
Published: 2026-07-06

How does HyDE work in RAG?

# How does HyDE work in RAG?

Authors
: - Name
: Amit Shekhar
Published on
: July 6, 2026

In this blog, we will learn about how HyDE works in RAG, which is the clever trick of searching with a fake answer. We will also see why searching with the plain question is weak, why a fake answer searches better, how HyDE works step by step with a worked example, and when to use it in the real world.

We will cover the following:

- What is RAG in simple words
- What is the search problem in RAG
- Why searching with the question is weak
- What is HyDE
- Why searching with a fake answer works better
- How HyDE works step by step
- A worked example of HyDE
- A simple code example of HyDE
- Advantages of HyDE
- Disadvantages of HyDE
- When to use HyDE
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is RAG in simple words

Before jumping into HyDE, we must know what RAG is.

RAG stands for Retrieval-Augmented Generation. It is a way to make an AI model answer using our own documents instead of only using what it already knows.

RAG = Retrieval + Augmented + Generation.

Let's break it down:

- Retrieval means searching and fetching the right pieces of text from our documents.
- Augmented means adding the retrieved information to the prompt (context) before sending it to the AI model.
- Generation means the AI model writing an answer using those pieces of text.

Let's say we have a big company handbook with thousands of pages. A new employee asks, "How many holidays do I get in a year?" The AI model has never read our private handbook. So, it cannot answer correctly on its own.

So, here comes RAG to the rescue. First, RAG searches the handbook and finds the few lines that talk about holidays. Then, it gives those lines to the AI model. Finally, the model reads those lines and writes a clear answer.

This is how RAG lets the model answer from our own data. If we want a deeper look at the full RAG flow, we can read the blog on Agentic RAG.

## What is the search problem in RAG

The whole power of RAG depends on one thing. The search step must find the right text.

If the search brings the wrong pages, the model gets wrong information. And then the answer will also be wrong.

So, the search step is the heart of RAG. Now, let's understand how this search actually happens.

The search in RAG does not work by matching exact words. It works by matching meaning.

To match meaning, we convert text into numbers. These numbers are called an embedding.

An embedding is a list of numbers that represents the meaning of a piece of text.

In simple words, an embedding is the meaning of text written in the language of numbers.

The important rule is simple. Two texts with similar meaning get similar numbers. Two texts with different meaning get different numbers.

We also cut our big documents into small pieces. Each small piece is called a chunk, which means a short block of text, like a single paragraph.

So, in RAG, we do the following. First, we convert every chunk of our document into an embedding and store it. Then, when a user asks a question, we convert the question into an embedding too. After that, we compare the question embedding with all the stored embeddings. Finally, we pick the chunks whose embeddings are closest to the question embedding.

This is how RAG finds the right text by comparing meaning.

The store that holds all these embeddings and finds the closest ones is called a vector database. We have a detailed blog on how a vector database works that explains this in depth.

## Why searching with the question is weak

Now, here is the catch.

A question and an answer often do not look alike. They live in different worlds.

Let's say the user asks, "Why is my laptop battery draining so fast?"

The real answer inside our documents may say something like this:

> Background applications, high screen brightness, and old battery health reduce battery life. Closing unused apps and lowering brightness improves battery duration.

Notice the problem. The question is short and uses words like "draining" and "fast". The answer is detailed and uses words like "background applications", "brightness", and "battery health".

A question and its answer are written in two different styles. So, their embeddings are not always close to each other.

Means, when we search using only the question, the meaning gap is large. The search may miss the perfect answer that is actually sitting in our documents.

This is the weakness of searching with the question. We are comparing a question to answers, but questions and answers are shaped differently.

## What is HyDE

So, here comes HyDE into the picture.

HyDE stands for Hypothetical Document Embeddings. It is a technique where we first ask the AI model to write a fake answer to the question, and then we search using that fake answer instead of the question.

In simple words, HyDE = Hypothetical + Document + Embeddings.

Let's break it down:

- Hypothetical means imaginary or made-up. It is a guess answer.
- Document means a piece of text that looks like a real answer.
- Embeddings means the meaning of that text written as numbers.

The core idea is one beautiful trick. An answer looks like an answer. So, if we want to find a real answer, we must search using something that looks like an answer.

The question does not look like an answer. But a fake answer does look like an answer.

So, we tell the AI model, "Pretend you know the answer and write it." This made-up answer is called the hypothetical document.

We do not show this fake answer to the user. We do not even trust that it is correct. We only use it as a better search key, which means the text we search with.

This is the heart of HyDE. We search with a fake answer to find the real answer.

## Why searching with a fake answer works better

Now, the question is, why does a fake answer help when it may even contain wrong facts?

The answer is about shape, not facts.

When the model writes a fake answer about battery draining, it naturally uses words like "background apps", "screen brightness", and "battery health". These are the same kinds of words that the real answer in our documents uses.

So, the fake answer and the real answer now look alike. Their embeddings become close. And close embeddings mean a strong search match.

Let's picture this meaning space as below:

```text
        Meaning space (similar meaning sits closer)

   [ Question ]                                  ----- far -----+
   "battery draining fast"                                      |
                                                                v
                                          +--------------------------+
   [ Fake answer ]  ----- close ------->  | [ Real answer chunk ]    |
   "background apps, brightness,          | "background apps, high   |
    battery health"                       |  brightness, battery     |
                                          |  health reduce life"     |
                                          +--------------------------+

```

Here, we can see that the question sits far from the real answer chunk, because it is shaped differently. The fake answer sits close to the real answer chunk, because both use the same answer-like words. So, searching with the fake answer lands much nearer to the real answer.

> We are not searching with the question. We are searching with something that is shaped like the answer.

Even if the fake answer gets a fact wrong, it still points the search in the right direction. The wrong facts get thrown away later, because we only use the real documents to write the final answer.

This is how a fake answer becomes a powerful search key.

To learn how embeddings, Vector Databases, and RAG fit together, check out our AI and Machine Learning Program at Outcome School.

## How HyDE works step by step

The best way to learn this is by taking an example. Let's walk through HyDE step by step.

Step 1: The user asks a question. For example, "Why is my laptop battery draining so fast?"

Step 2: We send this question to the AI model with a simple instruction. We say, "Write a short answer to this question, even if you are not sure." The model writes a fake answer, which is our hypothetical document.

Step 3: We convert this fake answer into an embedding, which means we turn it into a list of numbers that holds its meaning.

Step 4: We compare this embedding with all the stored embeddings of our real document chunks. We pick the chunks that are closest in meaning.

Step 5: We take these real chunks and send them to the AI model along with the original question.

Step 6: The model reads the real chunks and writes the final answer. This final answer is based on our real documents, not on the fake one.

So, the fake answer is used only in the middle, only to improve the search. The final answer comes from real data.

We can picture the full flow as below:

```text
   [ User question ]
          |
          v
   +-------------------+
   | AI model writes   |   <- "even if not sure"
   | a fake answer     |
   +-------------------+
          |
          v
   +-------------------+
   | Turn fake answer  |
   | into embedding    |
   +-------------------+
          |
          v
   +-------------------+        +----------------------+
   | Search the stored | -----> | Pick closest real    |
   | document chunks   |        | document chunks      |
   +-------------------+        +----------------------+
                                          |
              [ User question ] --------> |
                                          v
                               +----------------------+
                               | AI model writes the  |
                               | final answer from    |
                               | real chunks only     |
                               +----------------------+
                                          |
                                          v
                                  [ Final answer ]

```

Here, we can see that the fake answer is used only in the middle to improve the search. The real chunks and the original question flow into the last step, and the final answer is written from the real documents only.

This is how HyDE works from start to finish.

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

## A worked example of HyDE

Let me tabulate the difference between the normal RAG search and the HyDE search for your better understanding.

| Stage | Normal RAG | HyDE |
| --- | --- | --- |
| What we search with | The user's question | A fake answer written by the model |
| Shape of the search text | Short and question-like | Detailed and answer-like |
| Closeness to real answers | Often far in meaning | Often close in meaning |
| Final answer source | Real documents | Real documents |

Here, we can see the key difference. Normal RAG searches with a question. HyDE searches with a fake answer. Both write the final answer from real documents, but HyDE usually finds better chunks to start with.

Now, let's see the meaning gap with simple numbers, just for the sake of understanding.

Suppose closeness is measured from 0 to 1, where 1 means identical meaning and 0 means completely different meaning.

- Question embedding compared to the real answer chunk: closeness is 0.55.
- Fake answer embedding compared to the real answer chunk: closeness is 0.88.

Here, we can notice that the fake answer is much closer to the real answer. So, the search picks the correct chunk more easily with HyDE.

Note: These numbers are just for the sake of understanding. The real values depend on the model and the data.

## A simple code example of HyDE

Now, let's see the code for HyDE in a simple form. We will write it in `python` as below:

```python
def hyde_search(question, model, vector_store):
    # Step 1: ask the model to write a fake answer
    prompt = "Write a short answer to this question: " + question
    fake_answer = model.generate(prompt)

    # Step 2: turn the fake answer into an embedding
    fake_answer_embedding = model.embed(fake_answer)

    # Step 3: search using the fake answer's embedding
    top_chunks = vector_store.search(fake_answer_embedding, top_k=5)

    return top_chunks

```

Here, we have done three simple things:

- First, we ask the model to write a `fake_answer` to the question.
- Then, we convert that `fake_answer` into a `fake_answer_embedding`, which is its meaning as numbers.
- After that, we call `vector_store.search` with that embedding to get the top five closest chunks.

Notice that we never search with the original `question`. We search with the `fake_answer`. That is the whole trick of HyDE.

Now, let's see how we use these chunks to write the final answer as below:

```python
def answer_with_hyde(question, model, vector_store):
    chunks = hyde_search(question, model, vector_store)

    # combine the real chunks into one block of context
    context = "\n".join(chunks)

    # ask the model to answer using only the real chunks
    final_prompt = (
        "Use the context below to answer the question.\n"
        "Context: " + context + "\n"
        "Question: " + question
    )
    return model.generate(final_prompt)

```

Here, we can see the full flow. First, we get the real `chunks` using `hyde_search`. Then, we join them into one `context`, which means one block of helpful text. After that, we send the real `context` and the original `question` to the model. Finally, the model writes the answer using only the real documents.

So, the fake answer helped us find the chunks, but it never touched the final answer. The problem is solved.

If we want to go deep into RAG and build an AI Tutor from scratch, we cover it in our AI and Machine Learning Program at Outcome School.

## Advantages of HyDE

Now, let's understand why HyDE is useful.

- It closes the gap between questions and answers, because we search with answer-shaped text.
- It often finds better chunks, which leads to better final answers.
- It works well even when the user's question is short or vague.
- It needs no extra training of the model. We only change how we search.

## Disadvantages of HyDE

But again, no technique is perfect. HyDE has some costs too.

- It is slower, because we make an extra call to the model to write the fake answer.
- It costs more, because that extra call uses extra computing power.
- The fake answer can drift off topic, and then the search may go in the wrong direction.
- For very simple questions, the question itself may already be enough, so HyDE adds cost without much gain.

So, HyDE makes our search smarter, but we pay with a little extra time and cost.

## When to use HyDE

Now, the question is, when must we use HyDE.

We should use HyDE when our questions and answers look very different from each other. This happens a lot with short questions, support tickets, and search over technical documents.

But, for very short and direct lookups, plain RAG search may be enough. So, we must choose HyDE based on our use case.

A good practice is to test both. We can run plain RAG search and HyDE search on the same set of questions, and then we keep the one that finds better chunks for our data.

## Summary

Let's quickly recap what we have learned.

RAG searches our documents by matching meaning using embeddings. But a question and its answer are shaped differently, so searching with the question alone is weak.

So, here comes HyDE. We ask the model to write a fake answer first. We search with that fake answer, because it is shaped like a real answer and lands close to the real chunks. Then, we write the final answer using only the real documents.

This way we can use HyDE to solve the search problem in RAG in a very simple way. We search with a fake answer to find the real one.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-363 and 917-1353 of 1353; 553 middle lines (22.1KB) elided. Read artifact://78 for full output]
