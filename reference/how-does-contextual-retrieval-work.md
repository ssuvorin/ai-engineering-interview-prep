> Source: https://outcomeschool.com/blog/how-does-contextual-retrieval-work

# How does Contextual Retrieval work?
URL: https://outcomeschool.com/blog/how-does-contextual-retrieval-work
Published: 2026-10-06
Author: Amit Shekhar

How does Contextual Retrieval work?

# How does Contextual Retrieval work?

Authors
: - Name
: Amit Shekhar
Published on
: October 6, 2026

Contextual Retrieval is a way to improve RAG by adding a short note to every chunk of a document before we store it. The note explains where the chunk comes from, so the system can find the right chunk even when the chunk alone does not say enough.

In this blog, we will learn about how Contextual Retrieval works. We will also see why splitting documents into chunks loses important information, how an LLM writes a short context note for every chunk, how Contextual Embeddings and Contextual BM25 use that note, how reranking makes the results better, how prompt caching keeps the cost low, and where it works well and where it fails.

We will cover the following:

- What is a chunk?
- How does normal retrieval find chunks?
- The problem: chunks lose their context
- What is Contextual Retrieval?
- How does Contextual Retrieval work step by step?
- Contextual Embeddings
- Contextual BM25
- Combining both and adding reranking
- How much does it help?
- How is the cost kept low?
- A simple code example
- When to use it and when not to use it

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a chunk?

Before jumping into Contextual Retrieval, we must know where it is used. In RAG (Retrieval-Augmented Generation), we find the right pieces of text from our own documents and give them to an LLM along with the question. If retrieval fails, the LLM gets the wrong text, and the answer is often wrong. Contextual Retrieval improves exactly this step.

Our documents are usually long. A single report can have 100 pages. We cannot give the full 100 pages to the LLM for every question. It is slow and costly.

So, we cut every document into small pieces. Each piece is called a chunk. A chunk is usually a few hundred words long.

```
       One long document
 +-----------------------------+
 | Page 1 ... Page 100         |
 +-----------------------------+
               ↓
        cut into pieces
               ↓
 [chunk 1] [chunk 2] [chunk 3] ... [chunk 500]

```

Here, we can see that one big document becomes many small chunks. When a question comes, we search among these chunks and pick the top few. Only those chunks go to the LLM.

## How does normal retrieval find chunks?

There are two popular ways to search the chunks. Let's understand both, because Contextual Retrieval improves both of them.

Way 1: Embeddings (search by meaning)

An embedding is a list of numbers that represents the meaning of a piece of text.

An embedding model reads a chunk and turns it into a list of numbers. Texts with similar meaning get similar numbers. So, "How do I reset my password?" and "Steps to change a forgotten password" end up close to each other, even though they use different words.

When a question comes, we turn the question into an embedding too, and then pick the chunks whose numbers are closest to it. This is called semantic search, which means search by meaning.

Way 2: BM25 (search by exact words)

BM25 is a classic keyword search method. It scores a chunk higher when it contains the exact words of the question, especially rare words.

Embeddings are great at meaning, but they are weak at exact matches. Let's say we search for an error code like `TS-999`. The embedding thinks it is "some error code" and brings back chunks about any error code. BM25 looks for the exact word `TS-999` and finds the right chunk.

So, most good RAG systems use both and merge the results. This is called hybrid search.

Now, let's see the problem.

## The problem: chunks lose their context

When we cut a document into chunks, each chunk is torn away from the rest of the document. It loses its context, which means the surrounding information that tells us what the chunk is about.

The best way to learn this is by taking an example.

Suppose we have a financial report of a company named ACME Corp for the second quarter of 2023, which is written as Q2 2023. Somewhere in the middle of it, there is a chunk like below:

```
The company's revenue grew by 3% over the previous quarter.

```

Now, a user asks: "What was the revenue growth for ACME Corp in Q2 2023?"

Let's look at this chunk with fresh eyes. Which company? It just says "the company". Which quarter? It just says "the previous quarter". The words "ACME" and "Q2 2023" are nowhere in the chunk. They were written on page 1 of the report, and that page went into a different chunk.

So, the following issues arise:

- The embedding of this chunk does not carry the meaning "ACME" or "Q2 2023", so semantic search does not rank it high.
- BM25 finds no match for the words "ACME" and "Q2", so keyword search also misses it.
- If we have reports of ten companies, all of them have chunks like "the company's revenue grew by...", and the system cannot tell them apart.

It is like tearing one page out of a book and handing it to someone. The page says "He opened the door", but the person has no idea who "he" is.

## What is Contextual Retrieval?

So, here comes Contextual Retrieval to the rescue.

Contextual Retrieval is a technique where, before storing each chunk, we ask an LLM to write a short note that explains where the chunk fits in the whole document, and we attach that note to the front of the chunk.

This technique was introduced by Anthropic in 2024.

Let's take our chunk again. After Contextual Retrieval, it becomes like below:

```
This chunk is from an SEC filing on ACME Corp's performance in Q2 2023;
the previous quarter's revenue was $314 million.
The company's revenue grew by 3% over the previous quarter.

```

Here, the first two lines are the new context note written by the LLM. The last line is the original chunk. An SEC filing is an official financial report that a US company submits to the government.

Now, the chunk says "ACME Corp" and "Q2 2023" clearly. Both the embedding search and the keyword search can find it.

## How does Contextual Retrieval work step by step?

Let's see the full flow.

Step 1: We split the document into chunks. This is the same as normal RAG.

Step 2: For every chunk, we ask an LLM to write a context note. We give the LLM two things: the full document and the one chunk. We ask it to write a short note that places the chunk inside the document.

Anthropic used a prompt like below:

```
<document>
{{WHOLE_DOCUMENT}}
</document>
Here is the chunk we want to situate within the whole document
<chunk>
{{CHUNK_CONTENT}}
</chunk>
Please give a short succinct context to situate this chunk within the
overall document for the purposes of improving search retrieval of the
chunk. Answer only with the succinct context and nothing else.

```

Here, `{{WHOLE_DOCUMENT}}` is replaced with the full text of the document, and `{{CHUNK_CONTENT}}` is replaced with the chunk. The LLM reads the whole document, so it knows the company name, the date, the section, and etc. Then it writes a short note, usually 50 to 100 tokens, which is roughly 2 to 4 sentences.

Step 3: We glue the note to the front of the chunk. Now we have a "contextualized chunk".

Step 4: We index the contextualized chunk. We create the embedding from it, and we also add it to the BM25 keyword index.

Step 5: We answer questions as usual. When a question comes, we search, pick the top chunks, and give them to the LLM to write the answer.

```
                Document
                    ↓
            Split into chunks
                    ↓
    LLM writes a note for each chunk
                    ↓
   Note + chunk (contextualized chunk)
           ↓                 ↓
    Embedding index     BM25 index
           ↓                 ↓
      Search both with the question
                    ↓
               Top chunks
                    ↓
                   LLM
                    ↓
                 Answer

```

Here, we can see that the only new part is the step where the LLM writes a note for each chunk. Everything else is a normal RAG pipeline.

Note: The note is added only once, while preparing the data. At question time, there is no extra LLM call for the notes. So, answering questions is not slower.

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

## Contextual Embeddings

When we create embeddings from the contextualized chunks, Anthropic calls them Contextual Embeddings.

Earlier, the embedding of "The company's revenue grew by 3%..." only meant "some company's revenue grew". Now, the embedding means "ACME Corp's revenue grew 3% in Q2 2023". So, when the user asks about ACME's Q2 growth, the meanings are close, and the chunk comes up near the top.

## Contextual BM25

Similarly, when we build the BM25 keyword index from the contextualized chunks, it is called Contextual BM25.

Earlier, the word "ACME" was not in the chunk, so BM25 could never match it. Now, "ACME", "Q2", and "2023" are inside the chunk text, so BM25 gives the chunk a high score.

This is important because keyword search is very strong for names, product codes, IDs, and dates, and these are exactly the things that chunks usually lose.

## Combining both and adding reranking

Now, let's put the pieces together.

First, we run both searches. We take the top chunks from the contextual embeddings and the top chunks from contextual BM25. Then, we merge the two lists into one list, removing duplicates. A chunk that ranks high in both lists gets a better final position. This is hybrid search.

After that, we can add one more step called reranking.

A reranker is a model that reads the question and each candidate chunk together, and gives a precise score for how relevant that chunk is.

Let's say the first search brings back 150 candidate chunks. The reranker carefully reads each one with the question and reorders them. Then, we keep only the best 20 and send them to the LLM.

Why not use the reranker on all chunks from the start? Because it is slow. It reads every chunk with the question one pair at a time. Running it on millions of chunks would take too long. So, we use the fast search to shortlist, and the careful reranker to pick the final chunks.

It is like a job hiring process. First, a quick screening of resumes gives a shortlist of 150. Then, a detailed interview picks the best 20.

To learn RAG, Vector Databases, and Embeddings in depth, check out our AI and Machine Learning Program at Outcome School.

## How much does it help?

Anthropic tested this on many kinds of data, like codebases, fiction, research papers, and science papers. They measured the retrieval failure rate, which means how often the correct chunk was missing from the top 20 results. Lower is better.

Let me tabulate the results for your better understanding.

| Setup | Failure rate in top 20 | Reduction |
| --- | --- | --- |
| Normal embeddings | 5.7% | baseline |
| Contextual Embeddings | 3.7% | 35% fewer failures |
| Contextual Embeddings + Contextual BM25 | 2.9% | 49% fewer failures |
| Contextual Embeddings + Contextual BM25 + Reranking | 1.9% | 67% fewer failures |

Here, we can see that each layer helps. Adding the context note alone removes about one-third of the failures. Adding keyword search and reranking on top removes about two-thirds of the failures.

## How is the cost kept low?

Now, the question is: if we have 500 chunks in a document, we have to send the full document to the LLM 500 times. Is that not very costly?

Here comes prompt caching into the picture.

Prompt caching means the LLM provider remembers the processed version of a long, repeated part of the prompt, so the next request with the same part is cheaper and faster.

In our prompt, the full document is the same for all 500 chunks of that document. Only the small chunk part changes. So, we load the document into the cache once, and for every chunk we reuse it. We pay full price for the document only once, and the rest of the calls cost much less.

Anthropic estimated the one-time cost to be about $1.02 per million document tokens when using Claude 3 Haiku, a small and fast LLM from Anthropic, with prompt caching. A small, cheap model is enough here because writing a two-line note is an easy job.

Note: This cost is paid once when we prepare the data. If the documents change, we only redo the notes for the changed documents.

## A simple code example

Let's see the code for creating contextualized chunks. For the sake of understanding, we will keep it short and use a placeholder function `call_llm` that sends a prompt to any LLM and returns the reply.

```python
PROMPT = """<document>
{doc}
</document>
Here is the chunk we want to situate within the whole document
<chunk>
{chunk}
</chunk>
Please give a short succinct context to situate this chunk within the
overall document for the purposes of improving search retrieval of the
chunk. Answer only with the succinct context and nothing else."""

def contextualize(document, chunks):
    result = []
    for chunk in chunks:
        note = call_llm(PROMPT.format(doc=document, chunk=chunk))
        result.append(note + "\n" + chunk)
    return result

```

Here, we have:

- `PROMPT`: the same prompt that we saw earlier, with two blanks for the document and the chunk.
- `contextualize`: it takes one document and its chunks.
- For every chunk, we fill the prompt and call the LLM to get the `note`.
- We glue the note in front of the chunk and save it.

After this, we index these contextualized chunks as below:

```python
contextual_chunks = contextualize(document, chunks)

vectors = embed_model.embed(contextual_chunks)  # Contextual Embeddings
vector_db.add(vectors, contextual_chunks)

bm25_index.add(contextual_chunks)               # Contextual BM25

```

Here, we can see that the rest of the pipeline is unchanged. We just pass the contextualized chunks instead of the raw chunks. `embed_model`, `vector_db`, and `bm25_index` stand for whatever embedding model, vector database, and keyword index we already use.

Note: In real code, we turn on prompt caching for the document part so that the repeated document is not charged at full price every time.

If we want to go deep into Prompt Caching and RAG, and build an AI Tutor from scratch, we cover them in our AI and Machine Learning Program at Outcome School.

## When to use it and when not to use it

Contextual Retrieval works well when:

- Chunks often use words like "the company", "it", "this method", or "the above table" that point to something outside the chunk.
- We have many similar documents, like reports of many companies or many versions of a manual.
- Our users search with names, codes, and dates that usually appear only at the top of a document.

It has some limits:

- It adds one LLM call per chunk while preparing data. For a huge collection, this takes time and money, even with caching.
- The note is written by an LLM, and an LLM can get things wrong. A wrong note can mislead the search.
- If our chunks are already self-contained, like an FAQ where each answer repeats the question, the gain is small.
- If our whole knowledge base is small, we often do not need RAG at all. Anthropic suggests that if the knowledge base is smaller than about 200,000 tokens (roughly 500 pages), we can put the whole thing in the prompt.

We can also customize the prompt for our domain. For example, for a legal knowledge base, we can ask the LLM to always mention the case name and the section number in the note.

Contextual Retrieval improves the chunk side of the search. There is also a trick that improves the question side, where the model first writes a hypothetical answer and we search with that. Another one is Query Rewriting and Multi-Query Retrieval, where an LLM turns the question into one clearer query or several different ones. We have a detailed blog on how HyDE works in RAG that explains this step by step.

Let me tabulate the differences between normal retrieval and Contextual Retrieval for your better understanding so that you can decide which one to use based on your use case.

| Point | Normal retrieval | Contextual Retrieval |
| --- | --- | --- |
| What we store | Raw chunk | Context note + chunk |
| Knows the company, date, section | Only if written inside the chunk | Yes, the note adds it |
| Extra work while preparing data | None | One LLM call per chunk |
| Extra work at question time | None | None |
| Cost | Lower | Slightly higher, one time |
| Retrieval quality | Good | Better, fewer missed chunks |

Now we must have understood how Contextual Retrieval works, how it adds the lost context back to every chunk, and when to use it.

### Does Contextual Retrieval make answering questions slower?

No. Contextual Retrieval does not slow down answering questions. The context note is written only once, while we prepare the data. When a question comes, there is no extra LLM call for the notes. We search the contextualized chunks, pick the top ones, and give them to the LLM, just like normal RAG.

### Do we need a large LLM to write the context notes?

No. A small, cheap model is enough, because writing a short two-line note is an easy job. Anthropic used Claude 3 Haiku, a small and fast LLM, with prompt caching and estimated the one-time cost to be about $1.02 per million document tokens.

### Can we use Contextual Embeddings without BM25 and reranking?

Yes. Contextual Embeddings alone reduce the retrieval failure rate in the top 20 results from 5.7% to 3.7%, which is 35% fewer failures. Adding Contextual BM25 brings it to 2.9%, and adding reranking on top brings it to 1.9%, which is 67% fewer failures.

### What happens when our documents change?

We only redo the context notes for the documents that changed. The cost of writing the notes is paid once when we prepare the data, so the unchanged documents keep their existing contextualized chunks and do not need any new LLM calls.

### Do we always need RAG and Contextual Retrieval?

No. If our whole knowledge base is small, we often do not need RAG at all. Anthropic suggests that if the knowledge base is smaller than about 200,000 tokens, which is roughly 500 pages, we can put the whole thing in the prompt instead.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

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

[…264ln elided…]

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

# Agentic RAG
URL: https://outcomeschool.com/blog/agentic-rag
Published: 2026-05-01

Agentic RAG

# Agentic RAG

Authors
: - Name
: Amit Shekhar
Published on
: May 1, 2026

In this blog, we will learn about Agentic RAG - what it is, why standard RAG falls short, the agentic RAG loop, the three building blocks, the common patterns, when to use it, and the limitations to keep in mind.

A hard question often needs more than one search. Some of those searches need different sources. Some depend on what the previous search found. Standard RAG cannot do any of this. Agentic RAG can.

Agentic RAG = Agentic + RAG

We will cover the following in this blog:

- The Big Picture
- A Quick Recap of RAG
- A Quick Recap of AI Agent
- Why Standard RAG Falls Short
- What is Agentic RAG
- The Agentic RAG Loop
- The Three Building Blocks
- A Walkthrough with a Real Example
- Common Patterns of Agentic RAG
- Standard RAG vs Agentic RAG
- When to Use Agentic RAG
- Limitations of Agentic RAG
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

The best way to think about this is with a real-world analogy. Suppose we want to find an answer in a big library.

Standard RAG is like a librarian who fetches one book. We hand over the question. The librarian picks the book that matches the words best, gives it to us, and the LLM reads it to write the answer. One shot. Done.

Agentic RAG is like a researcher. The researcher reads the question, thinks about where to look, picks a section, reads it, and decides whether the answer is in there. If not, the researcher goes back, picks a different shelf, runs a follow-up search, and keeps going until the answer is found.

The librarian flow is fast but cannot adapt to the question. The researcher flow is slower but can handle questions that need many steps.

This is exactly the difference between Standard RAG and Agentic RAG. Agentic RAG turns the one-shot retrieval into a loop driven by an AI Agent that keeps working until it can answer well.

In simple words:

Agentic RAG = RAG + an AI Agent that controls the retrieval steps.

## A Quick Recap of RAG

Before jumping into Agentic RAG, we must quickly recall what RAG is.

RAG stands for Retrieval-Augmented Generation. The flow is simple:

- The user asks a question.
- We convert the question into an embedding.
- We search a vector database and pull the top relevant chunks.
- We pass those chunks plus the question to the LLM.
- The LLM generates the final answer.

One clever twist on the second step is HyDE, where instead of embedding the raw question, we first ask the model to write a hypothetical answer and search with that - a trick that often retrieves better chunks.

We can see this flow as below:

```
User Question
     |
     v
+------------------+
|     Embed        |
|   the question   |
+------------------+
     |
     v
+------------------+
|  Vector Search   |
|  (top-k chunks)  |
+------------------+
     |
     v
+------------------+
|       LLM        |
|  (generate)      |
+------------------+
     |
     v
  Final Answer

```

Here, we can see that the flow is a straight line. There are no decisions in the middle. Retrieve once. Generate once. Return. This is the librarian flow.

In a production RAG system, a Reranker often sits between retrieval and the LLM to reorder those top chunks by true relevance. We have a detailed blog on how a Reranker works that covers this step end to end.

## A Quick Recap of AI Agent

Now, let's recall what an AI Agent is.

An AI Agent is a system that uses an LLM as its brain and runs in a loop. The LLM plans the next step, recommends a tool, observes the result, and decides what to do next. It is not a one-shot prompt. It is a thinking loop with access to tools. This is the researcher in our analogy.

## Why Standard RAG Falls Short

Standard RAG works for simple questions. But the moment the question gets harder, it breaks down. The reason is simple. Our librarian only knows how to match words. The librarian cannot think, cannot ask follow-up questions, and cannot decide where to look.

Let's see the problems this causes.

Problem 1: Multi-hop questions.

Suppose the user asks:

> "What was the Q4 revenue of the company that acquired Acme in 2023?"

To answer this, we first need to find out which company acquired Acme in 2023. Only after that, we can retrieve the Q4 revenue of that company. One single retrieval cannot do this. The librarian sees the long question and tries to find one matching book. There is no such book.

Problem 2: Ambiguous queries.

The user asks: "What about the new policy?"

The retrieval system has no idea which policy. Standard RAG will pull random chunks and the answer will be wrong. The librarian does not stop to ask "which policy?". The librarian just matches words and hands over a book.

Problem 3: Multiple data sources.

Some questions need a SQL database. Some need a vector store. Some need a live web search. Standard RAG hits one source. It cannot pick the right one. Our librarian only knows one library. If the answer lives in a database, on the web, or in a graph of relationships, the librarian cannot reach it.

Problem 4: Bad retrieval quality.

Sometimes the top retrieved chunks are not relevant. Standard RAG does not know this. It just passes whatever it found to the LLM. The LLM then makes up the answer. The librarian hands over whatever matched the words best, without checking if the book actually has the answer.

Do you see the problem? Standard RAG is rigid. It cannot adapt.

So, here comes Agentic RAG to the rescue. We replace the librarian with a researcher.

## What is Agentic RAG

Agentic RAG is a system where an AI Agent drives the retrieval process. Instead of one fixed retrieve-then-generate step, the agent decides every step in a loop.

The agent decides:

- Does this question even need retrieval?
- Which tool or data source should we use?
- What should the search query look like?
- Are the retrieved chunks good enough to answer?
- Should we retrieve again with a better query?
- Should we combine results from multiple sources?
- When can we stop and write the final answer?

This is a big shift. The retrieval is no longer a fixed pipeline. It is a decision made by the agent at every step. The librarian has been replaced by the researcher.

## The Agentic RAG Loop

Let's see the loop.

```
User Question
     |
     v
+------------------+
|    AI Agent      |
|   (the LLM)      |
+------------------+
     |
     | thinks: "Do I need to retrieve?
     |          Which tool? What query?"
     v
+------------------+
|  Retrieval Tool  |
|  (vector / SQL / |
|   web / graph)   |
+------------------+
     |
     | returns chunks
     v
+------------------+
|    AI Agent      |
|   evaluates:     |
|  "Good enough?"  |
+------------------+
     |
     +--- No  --> retrieve again with a new query
     |
     +--- Yes --> generate the final answer

```

Here, we can see that the agent is in control. It loops until it has enough information.

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

## The Three Building Blocks

Agentic RAG has three building blocks. Let's decode each one.

1. The Agent (The Brain)

This is the researcher's mind. It is an LLM that does the thinking. It reads the question, plans the next step, recommends the tool, and evaluates the result.

2. The Tools (The Hands)

These are the resources our researcher can reach for. A real researcher uses different sources for different questions. The agent has the same options:

- Vector search: for finding text by meaning over documents
- Keyword search: for exact term matches
- SQL query: for structured data in a database
- Web search: for fresh information on the internet
- Knowledge graph query: for relationships between entities

The agent recommends the right tool based on the question, just like a researcher walks to the right shelf.

3. The Loop (The Workflow)

This is the back-and-forth between the researcher's mind and the resources. The runtime that ties the agent and the tools together. It calls the agent, runs the tool the agent recommended, feeds the result back to the agent, and repeats.

Across the loop, the runtime keeps track of every past step - the actions the agent took and the results it saw. This running record is called the scratchpad or agent memory. The agent reads this record on every step so it knows what it has already tried and what it has already learned.

Note: The LLM inside the agent does not call the tool itself. The LLM only outputs text - the name of the tool to use and the arguments. The runtime around the LLM is what actually calls the tool and feeds the result back. This distinction is important.

To build an AI Tutor from scratch - learning RAG, Agentic RAG, agent memory, and vector databases - check out our AI and Machine Learning Program at Outcome School.

## A Walkthrough with a Real Example

The best way to learn this is by taking an example.

Let's say the user asks:

> "What was the Q4 revenue of the company that acquired Acme in 2023?"

Here is how Agentic RAG handles it. Watch the agent act like a researcher.

Step 1: The agent reads the question. It thinks: "This is a multi-hop question. I first need to find who acquired Acme in 2023."

Step 2: The agent recommends the web search tool with the query: `company that acquired Acme in 2023`.

Step 3: The web search returns: "Globex acquired Acme in 2023."

Step 4: The agent updates its plan. Now it needs Globex's Q4 2023 revenue.

Step 5: The agent recommends the vector search tool over the internal financial reports with the query: `Globex Q4 2023 revenue`.

Step 6: The vector search returns chunks from Globex's Q4 financial report.

Step 7: The agent evaluates the chunks: "Yes, these chunks contain the revenue number. I have enough."

Step 8: The agent generates the final answer using the gathered information.

Note: In practice, the web search returns several noisy snippets. The agent reads them and pulls out the answer. We have shown a clean answer above just for the sake of understanding.

Sometimes, the agent combines results from two sources in a single step. For example, it pulls a definition from a vector store and fresh news from a web search before answering.

Standard RAG could not do this. It would have made one retrieval with the original question and failed. Agentic RAG broke the question into two steps, used two different tools, and answered correctly. The researcher did the job that the librarian could not.

Problem solved. This is the power of Agentic RAG.

## Common Patterns of Agentic RAG

Agentic RAG is a general idea. Over time, a few specific patterns have become popular. Let's quickly look at three of them.

ReAct-style RAG. The agent follows a "think, act, observe" loop. It thinks about what to do, takes an action like a retrieval, observes the result, and repeats. Our walkthrough above is a ReAct-style flow. We have a detailed blog on ReAct Agent that explains this pattern in depth.

Self-RAG. The agent grades its own retrievals on two things - relevance (are the chunks about the question?) and support (do the chunks actually back up the answer?). If not, the agent skips or trusts them less before generating. Self-RAG is about quality control on what the agent fetches.

Corrective RAG (also called CRAG). The agent recommends a fallback source when the main retrieval is bad. For example, if the vector search returns nothing useful, the agent falls back to a live web search. CRAG is about robustness when the main source fails.

All three share the same core idea. The agent decides what happens at every step. They differ in what they focus on - reasoning style, quality control, or robustness.

If we want to go deep into the ReAct pattern, and end-to-end evaluation of agents, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Standard RAG vs Agentic RAG

Let me tabulate the differences between Standard RAG and Agentic RAG for your better understanding so that you can decide which one to use based on your use case.

| Aspect | Standard RAG | Agentic RAG |
| --- | --- | --- |
| Flow | Fixed pipeline | Dynamic loop |
| Number of retrievals | One | Many, as needed |
| Tools used | One (usually vector search) | Many (vector, SQL, web, and etc.) |
| Query rewriting | No | Yes |
| Quality check on retrieved chunks | No | Yes |
| Multi-hop questions | Cannot handle | Can handle |
| Latency | Low | Higher |
| Cost | Low | Higher |
| Complexity to build | Simple | More complex |

## When to Use Agentic RAG

Use Agentic RAG when:

- The user asks multi-hop questions that need information from more than one search.
- The data lives in multiple sources (vector DB, SQL, web, files).
- The questions are ambiguous and need rewriting before retrieval.
- The quality of retrieval matters more than latency, like in research, legal, or medical use cases.
- The system needs to decide if retrieval is even needed. For greetings or small talk, no retrieval is needed.

Use Standard RAG when:

- The questions are simple and direct.
- The data lives in one place.
- Latency and cost matter more than depth.

## Limitations of Agentic RAG

A researcher takes more time and costs more than a librarian. The same is true for Agentic RAG. It is powerful, but it has trade-offs.

- Higher latency. Each loop step is one or more LLM calls. The user waits longer.
- Higher cost. Each loop step is one LLM call, and the tool results are fed back into the next prompt. More steps mean more tokens, which means a higher API bill.
- Harder to debug. The agent's decisions are not fixed. The same question can take different paths on different runs.
- Can loop too long. Without a stopping rule, the agent can keep retrying and never stop. Common stopping rules are: the LLM signals it is done, the agent's confidence in the answer is high enough, or a max step count is hit.
- More moving parts. We need to design tools, prompts, evaluation steps, and stopping rules. A simple system becomes a complex one.

We must keep these trade-offs in mind while designing the system.

## Quick Summary

Let's recap what we have learned:

- Standard RAG is a fixed pipeline: retrieve once, generate once.
- Agentic RAG is a loop where an AI Agent drives every step of retrieval.
- The agent decides when to retrieve, what to retrieve, from where, and whether to retrieve again.
- It has three parts: the agent, the tools, and the loop, with a scratchpad that tracks the past steps.
- Common patterns are ReAct-style RAG, Self-RAG, and Corrective RAG (CRAG).
- It shines on multi-hop questions, multiple data sources, and ambiguous queries.
- The trade-offs are higher latency, higher cost, and more complexity.

Standard RAG is the librarian who fetches one book. Agentic RAG is the researcher who keeps digging until the answer is found. We use Agentic RAG when Standard RAG is not enough.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

[Showing lines 1-407 and 672-1084 of 1084; 264 middle lines (13.6KB) elided. Read artifact://76 for full output]
