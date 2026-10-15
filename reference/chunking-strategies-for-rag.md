> Source: https://outcomeschool.com/blog/chunking-strategies-for-rag

# How to Chunk Documents for RAG? Chunking Strategies Explained
URL: https://outcomeschool.com/blog/chunking-strategies-for-rag
Published: 2026-09-10
Author: Amit Shekhar

How to Chunk Documents for RAG? Chunking Strategies Explained

# How to Chunk Documents for RAG? Chunking Strategies Explained

Authors
: - Name
: Amit Shekhar
Published on
: September 10, 2026

Chunking for RAG means cutting a big document into smaller pieces, called chunks, so that an AI system can find the right piece at the right time and answer our question correctly.

In this blog, we will learn about Chunking Strategies for RAG, the art of cutting a big document into smaller pieces so that an AI system can find the right piece at the right time. We will also see what RAG is, why chunking is needed at all, what happens when we chunk badly, the most useful chunking strategies one by one, how to pick the chunk size and the overlap, and where each strategy works well and where it fails.

We will cover the following:

- What is RAG?
- What is a chunk?
- Why do we need chunking?
- How retrieval actually works
- What happens when we chunk badly
- Fixed-size chunking
- Chunking by sentence
- Recursive chunking
- Document structure based chunking
- Semantic chunking
- Contextual chunking
- Small-to-big chunking
- Agentic chunking
- Chunk overlap
- How to choose the chunk size
- Comparison of all the strategies
- Common mistakes
- Conclusion

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is RAG?

Before jumping into chunking, we must know what RAG is.

RAG = Retrieval + Augmented + Generation.

Let's break the name into three plain words:

- Retrieval means finding.
- Augmented means adding something extra.
- Generation means writing the answer.

So, RAG is a system that first finds the useful information, then adds that information to our question, and then lets the AI model write the answer using it.

Let's say we have a company handbook of 500 pages. We ask the AI, "How many leave days do I get in my first year?"

The AI model has never read our handbook. It was trained on the public internet, and our handbook is a private document sitting on our laptop. So, the model has no way to know the answer.

Here comes RAG into the picture. RAG does three simple things:

- It searches our handbook and finds the small part that talks about leave days.
- It pastes that small part along with our question.
- It sends both to the AI model and asks it to answer using that part.

The model now has the right page in front of it, so it answers correctly, and that too without any retraining.

This is how RAG works. It is like giving an open-book exam to the model instead of asking it to remember everything.

Now, the question is, how does RAG search a 500-page handbook? It cannot send all 500 pages to the model every time. It is too big, too slow, and too costly. So, we cut the handbook into small pieces first.

Those small pieces are called chunks.

## What is a chunk?

A chunk is a small piece of text that we cut out from a bigger document.

In simple words, if the document is a long chocolate bar, a chunk is one square of it.

Let's say our handbook has this paragraph:

```text
Every employee gets 24 paid leave days in the first year.
Leave days do not carry forward to the next year.
Sick leave is counted separately and is limited to 12 days.

```

If we cut it into three pieces, one per sentence, we get three chunks. Each chunk is a small, self-contained note.

Later, when someone asks about sick leave, we do not need the whole handbook. We only need the third chunk.

This cutting is called chunking.

Now, we have understood the chunk. Now, let's learn why we need chunking at all.

## Why do we need chunking?

There are four solid reasons.

Reason 1: The model has a limited context window.

A model can only read a limited amount of text at once. This limit is called the context window.

This limit is counted in tokens. A token is a small piece of text, roughly three-fourth of a word. So, 100 tokens is about 75 words. We will use this word many times in this blog, so it is good to remember it now.

Our 500-page handbook has millions of tokens, and it does not fit inside the window. So, we must send only the relevant part.

Reason 2: Cost and speed.

Even if a huge document fits, sending it every single time is slow and expensive. We pay for every token we send. Sending one paragraph is far cheaper than sending 500 pages.

Reason 3: Accuracy.

This is the most important reason. When we give the model a mountain of text, the useful line gets buried inside it. The model gets distracted and starts mixing up facts from two different pages. When we give it three short and relevant chunks, it answers cleanly.

Less and correct text always beats more and noisy text.

We have a detailed blog on The Lost in the Middle Problem in LLMs that explains this in depth.

Reason 4: Search itself needs small pieces.

The search step works by comparing meaning. A small chunk has one clear meaning. A giant chunk has fifty mixed meanings, so its meaning becomes blurry, and the search stops working well.

We will understand this fourth reason properly in the next section.

## How retrieval actually works

Before jumping into the strategies, we need to see how the searching happens. Once we understand this, every chunking strategy will make sense on its own.

The search inside RAG is not a keyword search. It is a meaning search.

Here is how it happens.

Step 1: Every chunk is turned into a list of numbers.

We pass each chunk through a small model called an embedding model. It reads the chunk and gives back a long list of numbers, something like `[0.12, -0.98, 0.45, ...]`.

This list of numbers is called an embedding. We can think of it as the address of the meaning of that chunk. Two chunks that talk about the same thing get two addresses that sit close to each other.

Step 2: All these number lists are stored in a vector database.

A vector database is simply a storage that is very good at one job, finding the addresses that sit closest to a given address.

This whole one-time work of cutting the document, creating the embeddings, and storing them is called indexing. We do it once, before any user asks anything.

Step 3: The user's question is also turned into numbers.

When the user asks, "How many sick leave days do I get?", we pass this question through the same embedding model and get its address.

Step 4: We pick the closest chunks.

The vector database compares the question address with all the chunk addresses and returns the closest few, usually the top 3 or top 5. In a real system, one more step often sits right here. A reranker takes these closest few and reorders them by true relevance before they go to the model. We have a detailed blog on how a Reranker works that explains this step by step.

Step 5: Those chunks go to the model.

We paste those chunks along with the question and ask the model to answer.

Here, we can notice one very important thing. The whole system stands on one assumption, that each chunk carries one clear meaning. The moment a chunk carries a mix of ten unrelated ideas, its address becomes an average of ten things, and it stops being close to anything.

This is exactly why chunking strategy matters so much.

## What happens when we chunk badly

The best way to learn this is by taking an example.

Assume that we have this text in our handbook:

```text
Every employee gets 24 paid leave days in the first year. To apply,
open the HR portal and submit the request at least 7 days in advance.

```

Now, let's say we cut blindly after a fixed number of letters, and the cut lands in the middle:

Chunk 1:

```text
Every employee gets 24 paid leave days in the first year. To apply,
open the HR portal and submit the request at least

```

Chunk 2:

```text
7 days in advance.

```

Now, the user asks, "How early do I need to apply for leave?"

Chunk 2 has the actual answer, but it is just a floating fragment. It does not contain the words leave, apply, or request. Its meaning address is nowhere near the question. So, it is never retrieved.

Chunk 1 gets retrieved instead, and it stops right before the answer. The model reads it and either says it does not know, or worse, it guesses a number.

This is the core problem. A bad chunk is not a small problem, it silently destroys the answer.

So, our whole goal in chunking is simple, we must cut at places where a complete idea ends, not at random places.

Every strategy that we will learn now is just a smarter way of finding those places.

Now that we have understood the problem, it is time to learn the strategies one by one. We will start from the simplest one and keep improving. Do not worry, we will learn about each of them in detail.

## Fixed-size chunking

Fixed-size chunking means we cut the document after every fixed number of characters or tokens, no matter what the text says.

This is the simplest strategy. We decide a number, let's say 500 characters, and we cut after every 500 characters.

Let's see the code as below:

```python
def fixed_size_chunks(text, size=500):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i + size])
    return chunks

```

Here, we are walking through the text 500 characters at a time and collecting each slice as one chunk.

Advantage:

- It is very simple and very fast.
- Every chunk has a predictable size, so nothing ever overflows the model limit.
- It works on any kind of text, even messy text with no structure.

But, here is the catch.

Disadvantage:

- It cuts in the middle of a word, a sentence, or an idea, exactly like the leave-application example we just saw.
- The retrieved chunk often reads like a broken fragment.

The issue with this approach is that the cut position is decided by counting, not by meaning. Let's see how the next approach solve this issue.

## Chunking by sentence

Sentence-based chunking means we split the text into sentences first, and then group a few sentences together to form one chunk.

So, instead of cutting after 500 characters, we cut only at a full stop. This one small change removes broken words and broken sentences completely.

Let's see the code as below:

```python
import re

def sentence_chunks(text, sentences_per_chunk=5):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        group = sentences[i:i + sentences_per_chunk]
        chunks.append(" ".join(group))
    return chunks

```

Here, we have first split the text wherever a full stop, a question mark, or an exclamation mark is followed by a space. Then we have grouped every 5 sentences into one chunk.

- No sentence is ever cut in half, so every chunk reads like proper language.
- It is still simple and fast.

- Chunk sizes become uneven, because some sentences are very long and some are very short.
- It still groups blindly. Sentence number 5 may be the last line of one topic and sentence number 6 may be the first line of a completely new topic, and this strategy happily puts them in the same chunk.

The issue with this approach is that it respects sentences but it does not respect paragraphs and sections. Let's see how the next approach solve this issue.

## Recursive chunking

Recursive chunking means we try to cut at the biggest natural boundary first, and only if the piece is still too big, we go down to a smaller boundary.

This is the most commonly used strategy in real projects, and the idea behind it is beautiful.

Every document already has natural boundaries, and they have a natural order of importance:

- A blank line between paragraphs is a strong boundary.
- A single new line is a weaker boundary.
- A full stop is weaker than that.
- A space is the weakest one.

So, the strategy works like this. First, we try to split the document at blank lines. If a resulting piece is still bigger than our chunk size, then we take that piece alone and split it at new lines. If it is still too big, we split it at full stops. If it is still too big, we split it at spaces.

We keep going down the list only when we are forced to. That is why it is called recursive.

Let's see the code as below:

```python
def recursive_chunks(text, size=500, separators=["\n\n", "\n", ". ", " "]):
    if len(text) <= size or not separators:
        return [text]

    separator = separators[0]
    parts = text.split(separator)

    chunks = []
    for part in parts:
        if len(part) <= size:
            chunks.append(part)
        else:
            # still too big, so try the next weaker separator
            chunks.extend(recursive_chunks(part, size, separators[1:]))
    return chunks

```

Here, we can see that we always start with the strongest separator `"\n\n"`, and we call the same function again with the remaining weaker separators only for the parts that are still too big.

Note: This code is kept short just for the sake of understanding. A real implementation also merges the tiny neighbouring pieces back together until they reach the chunk size, so that we do not end up with a lot of one-line chunks.

- Most chunks end up matching real paragraphs, so they carry a complete idea.
- It never blows past our size limit, because in the worst case it falls back to splitting at spaces.
- It works well on almost every kind of document, which is why it is the default choice in most RAG systems.

Disadvantage:

- It follows the shape of the text, not the meaning of the text. If the writer put two unrelated ideas in one paragraph, this strategy keeps them together.

The issue with this approach is that it treats every document as plain text and ignores the headings that the document already gives us. Let's see how the next approach solve this issue.

## Document structure based chunking

Document structure based chunking means we use the headings, sections, and tables that already exist in the document, and we cut along those lines.

Many of our documents are not plain text. A Markdown file has `#` and `##` headings. An HTML page has ` ` and ` ` tags. A PDF has chapters. A code file has functions and classes.

The writer already told us where one topic ends and the next begins. It would be a waste to ignore that.

Let's say we have this Markdown document:

```markdown
# Leave Policy

## Paid Leave

Every employee gets 24 paid leave days in the first year.

## Sick Leave

Sick leave is limited to 12 days and needs a doctor note after 3 days.

```

If we cut at every `##` heading, we get two clean chunks. One chunk is fully about paid leave, and the other chunk is fully about sick leave. Nothing is mixed.

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

There is one more trick here that makes a big difference. We must carry the parent headings into each chunk. So, the second chunk should be stored like this:

```text
Leave Policy > Sick Leave
Sick leave is limited to 12 days and needs a doctor note after 3 days.

```

Here, we have added the heading path at the top. Now the chunk knows which document and which section it belongs to, even when it is pulled out alone.

- The boundaries are decided by the person who wrote the document, so they are usually perfect.
- Adding the heading path gives every chunk a clear identity.

- It only works when the document actually has structure. A plain transcript of a meeting or a scanned page has no headings at all.
- Sections can be very uneven. One section may be two lines and another may be twenty pages, so we still need a size-based split inside the big sections.

In practice, we combine this with recursive chunking. First, we split by headings, and then we split the oversized sections recursively. This combination handles almost every real document well.

The issue with this approach is that it still depends on someone having written good headings. Let's see how the next approach solve this issue.

## Semantic chunking

The word semantic simply means related to meaning.

Semantic chunking means we cut the document at the exact points where the topic changes, and we find those points by measuring meaning.

Till now, every strategy was cutting based on shape, which means characters, sentences, paragraphs, or headings. Semantic chunking is the first strategy that cuts based on meaning.

Here is how it works.

Step 1: We split the document into sentences.

Step 2: We turn every sentence into its embedding, which is that list of numbers we learned about earlier.

Step 3: We walk from one sentence to the next and measure how similar the two meanings are. Measuring the similarity simply means checking how close the two addresses sit. Close addresses mean the same topic.

Step 4: When two neighbouring sentences are still talking about the same thing, the similarity is high, so we keep them together. When the similarity suddenly drops, it means the topic just changed, so we cut there.

Let's see it with an example:

```text
1. Every employee gets 24 paid leave days in the first year.
2. These days do not carry forward to the next year.
3. The office cafeteria is open from 8 AM to 6 PM.
4. It serves breakfast, lunch, and evening snacks.

```

Sentence 1 and sentence 2 are both about leave, so their similarity is high. Sentence 2 and sentence 3 are about two totally different things, so the similarity drops sharply. That drop is our cut point.

So, we get two chunks. One is about leave, and one is about the cafeteria. This is exactly what we wanted, and notice that no heading was needed.

- The boundaries follow the actual topics, so each chunk is genuinely about one thing.
- It works even on documents with no headings at all, like transcripts and chat logs.

- It is slow and costly, because we have to create an embedding for every single sentence before we can even start chunking.
- We have to tune the drop threshold. The threshold is the limit we set for deciding how big a drop counts as a topic change. If the threshold is too sensitive, we get hundreds of tiny chunks. If it is not sensitive enough, we get very few huge chunks.
- On a document that has one long flowing topic, it gives no clear cut points at all.

The issue with this approach is that even a perfectly cut chunk can still be useless on its own. Let's see why, and how the next approach solve this issue.

## Contextual chunking

Let's understand the problem first, because this problem is very easy to miss.

Assume that our chunking worked perfectly and we got this clean chunk:

```text
The limit was raised to 18 days from April, and the doctor note
requirement was removed.

```

Now, the user asks, "What is the current sick leave limit?"

This chunk has the exact answer, but read it once again carefully. It never says the words sick leave. It says "the limit". A human reading the full document knows which limit, because the heading two pages above said Sick Leave. But this chunk is stored alone in the database, with no memory of where it came from.

So, its meaning address is vague, and it never gets retrieved. A chunk that loses its context loses its usefulness.

So, here comes the contextual chunking to the rescue.

Contextual chunking means we add a short line of context to the top of each chunk before we store it, so that the chunk can stand on its own.

The fixed chunk looks like this:

```text
From the Employee Handbook, Leave Policy section, about sick leave:
The limit was raised to 18 days from April, and the doctor note
requirement was removed.

```

Now the chunk carries its own identity. The words sick leave are present, the section is present, and the source is present. The question now matches it easily.

[…761ln elided…]

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

[Showing lines 1-465 and 1227-1639 of 1639; 761 middle lines (37.9KB) elided. Read artifact://44 for full output]
