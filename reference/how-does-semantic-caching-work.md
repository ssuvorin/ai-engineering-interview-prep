> Source: https://outcomeschool.com/blog/how-does-semantic-caching-work

# How does Semantic Caching work?
URL: https://outcomeschool.com/blog/how-does-semantic-caching-work
Published: 2026-07-08

How does Semantic Caching work?

# How does Semantic Caching work?

Authors
: - Name
: Amit Shekhar
Published on
: July 7, 2026

Semantic Caching is a cache that matches questions by their meaning instead of their exact words. So, if a new question means the same as an old one, the AI app can reuse the saved answer.

In this blog, we will learn about how Semantic Caching works. We will also see why traditional caching falls short for AI apps, how Semantic Caching uses embeddings and similarity to reuse past answers, and how setting the right threshold makes it work in the real world.

We will cover the following:

- What is a cache?
- The problem with traditional caching for AI apps
- What is Semantic Caching?
- What are embeddings?
- What is similarity between embeddings?
- How does Semantic Caching work step by step?
- A numeric walkthrough
- Setting the similarity threshold
- Advantages of Semantic Caching
- Things to keep in mind

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a cache?

A cache is a place where we store the answer to a question, so that the next time the same question comes, we can return the saved answer instantly.

In simple words, a cache is a memory of past answers.

Let's say a friend asks us, "What is the capital of France?" We answer, "Paris." If the same friend asks the same question again, we do not think again. We simply say "Paris" because we remember it.

That memory of past answers is the cache. It saves us time, and it saves us effort.

This is how a cache works in software too. The first time, we do the hard work and compute the answer. After that, we store it. The next time, we return the stored answer directly.

### The problem with traditional caching for AI apps

Now, let's understand why normal caching is not enough for AI apps.

Suppose we are building an app that uses a Large Language Model that powers tools like ChatGPT. Every time a user asks a question, our app sends that question to the model, the model thinks, and then it returns an answer.

But, here is the catch. Sending a question to the model costs money, and it also takes time. If a thousand users ask the same thing, we pay a thousand times, and each user waits.

So, we think of caching. We store each question and its answer. The next time the exact same question comes, we return the stored answer.

This is called exact-match caching. It matches the question word by word, letter by letter.

Let's see the problem with an example. Assume that two users ask these questions:

- User 1: "What is the capital of France?"
- User 2: "Tell me the capital city of France."

For us humans, both questions mean the same thing. The answer is "Paris" in both cases.

But for exact-match caching, these two are completely different. The words are different, the order is different, so the cache thinks they are two separate questions. It will send the second question to the model again, and we pay again.

The issue with this approach is that it only understands letters, not meaning. People ask the same thing in many different ways, so the cache almost never matches.

We needed a solution for that, and Semantic Caching was introduced to solve this problem.

### What is Semantic Caching?

Semantic Caching is a cache that matches questions by their meaning instead of their exact words.

Let's break the term to understand it better.

> Semantic Caching = Semantic + Caching

The word "semantic" simply means "related to meaning." So, Semantic Caching is caching based on meaning.

In simple words, if a new question means the same thing as an old question, we return the old answer, even if the words are different.

Going back to our example, "What is the capital of France?" and "Tell me the capital city of France." mean the same thing. So, Semantic Caching treats them as a match and returns "Paris" without asking the model again.

This is the beauty of Semantic Caching. It understands intent, not just text.

Now, the next big question is: how does a computer understand the meaning of a sentence? A computer only understands numbers. So, here come embeddings into the picture.

### What are embeddings?

An embedding is a list of numbers that represents the meaning of a piece of text.

In simple words, an embedding turns a sentence into numbers, in such a way that sentences with similar meaning get similar numbers.

Let's understand this with a simple picture in our mind. Imagine a big map. On this map, every sentence becomes a single point. Sentences that mean the same thing land close to each other. Sentences that mean very different things land far apart.

For the sake of understanding, consider this map:

- "What is the capital of France?" lands at one point.
- "Tell me the capital city of France." lands very close to it, because the meaning is almost the same.
- "How do I bake a chocolate cake?" lands very far away, because the meaning is totally different.

So, the embedding is just the address of that point on the map, written as a list of numbers.

Let's visualize this map of meaning as below:

```text
   meaning
      ^
      |
      |   [France capital question]
      |   [France capital city question]   <- close, same meaning
      |
      |
      |
      |                          [bake a chocolate cake]  <- far, different
      |
      +-------------------------------------------------> meaning

```

Here, we can see that the two questions about the capital of France land close to each other, because they mean almost the same thing. The question about baking a cake lands far away, because its meaning is completely different. This closeness on the map is exactly what we measure later.

A real embedding has hundreds of numbers. But for the sake of understanding, let's pretend each embedding has only two numbers. We can write them like below:

```python
# Just for understanding, real embeddings have hundreds of numbers
"What is the capital of France?"      -> [0.91, 0.10]
"Tell me the capital city of France." -> [0.89, 0.12]
"How do I bake a chocolate cake?"     -> [0.05, 0.95]

```

Here, we can notice that the first two lists of numbers are very close to each other. The third one is far away. This matches our understanding, because the first two questions mean the same thing, and the third one means something completely different.

This is how a model converts meaning into numbers. We use a special model called an embedding model to create these numbers for any text we give it.

To learn embeddings, Vector Databases, and RAG in depth, we cover all of these in our AI and Machine Learning Program at Outcome School.

### What is similarity between embeddings?

Now that we have learned about embeddings, it's time to learn how we compare two embeddings.

Similarity is a number that tells us how close two embeddings are in meaning.

In simple words, we take two lists of numbers and we calculate a single score. A high score means the meanings are close. A low score means the meanings are far apart.

The most common score used here is called cosine similarity. We do not need to learn the math today. We just need to remember one thing.

> Higher similarity score means closer meaning.

For the sake of understanding, the score usually goes from 0 to 1.

- A score near 1 means the two sentences mean almost the same thing.
- A score near 0 means the two sentences mean very different things.

So, when a new question comes, we find its embedding, and we compare it with the embeddings of all our saved questions. If any saved question has a high enough similarity score, we treat it as a match.

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

### How does Semantic Caching work step by step?

Before we see the full flow, let me map each piece to a simple real-world role for your better understanding.

| Piece in Semantic Caching | Real-world role |
| --- | --- |
| Embedding model | A translator that turns a sentence into numbers |
| Embedding | The address of a sentence on the map of meaning |
| Similarity score | A judge that tells how close two meanings are |
| Threshold | A rule that decides "close enough or not" |
| Cache | A notebook of past questions and their answers |

Now, let's put everything together and see the full flow.

Step 1: A user sends a question to our app.

Step 2: We convert the question into an embedding using the embedding model. Now the question is a list of numbers.

Step 3: We compare this embedding with the embeddings of all the questions already stored in our cache. We calculate a similarity score for each.

Step 4: We find the saved question with the highest similarity score.

Step 5: Now, the decision. If the highest score is above a chosen limit, we call it a cache hit. We return the saved answer directly, without calling the model. This is fast and free.

Step 6: If no saved question crosses that limit, we call it a cache miss. We send the question to the model, get a fresh answer, and then store the new question, its embedding, and its answer in the cache for the future.

This is how Semantic Caching serves answers by meaning.

We can picture the full flow as below:

```text
        User question
              |
              v
   +----------------------+
   |   Embedding model    |   (turn text into numbers)
   +----------------------+
              |
              v
   +----------------------+
   |  Search the cache    |   (compare with saved embeddings)
   |  for the best score  |
   +----------------------+
              |
              v
       score >= threshold ?
        /              \
      yes               no
       |                 |
       v                 v
  +-----------+   +--------------------+
  | Cache hit |   |    Cache miss      |
  | return    |   | ask the model,     |
  | saved     |   | then store the new |
  | answer    |   | question + answer  |
  +-----------+   +--------------------+

```

Here, we can see that every question first becomes numbers through the embedding model. We then search the cache for the closest saved question and its score. If the score crosses the threshold, we take the left path and return the saved answer, which is a cache hit. If it does not, we take the right path, ask the model for a fresh answer, and store it, which is a cache miss.

In a real system, these saved embeddings live in a vector database that is built to store embeddings and find the closest ones fast using Approximate Nearest Neighbor (ANN) search.

Let's see this flow in simple code as below:

```python
def get_answer(question):
    new_embedding = embed(question)            # Step 2: text to numbers

    best_match, score = search_cache(new_embedding)  # Step 3 and 4

    if score >= 0.85:                          # Step 5: cache hit
        return best_match.answer

    answer = ask_model(question)               # Step 6: cache miss
    store_in_cache(question, new_embedding, answer)
    return answer

```

Here, we can see the whole idea in one place. The `embed` function turns the question into numbers. The `search_cache` function finds the closest saved question and its similarity `score`. If the `score` is high enough, which is `0.85` in our example, we return the saved answer. If not, we ask the model, and then we save the new result so that the next similar question becomes a cache hit.

Here, the number `0.85` is the limit we talked about. It is called the similarity threshold, and we will understand it in detail next.

### A numeric walkthrough

The best way to learn this is by taking an example. Let's walk through it step by step with numbers.

Assume that our cache already has one saved question.

- Saved question: "What is the capital of France?"
- Saved answer: "Paris"

Now, a new user sends a question, and we compare it with our saved question.

Step 1: New question is "Tell me the capital city of France." We compute its embedding and compare it with the saved one. The similarity score comes out to be `0.93`. Our threshold is `0.85`. Since `0.93` is greater than `0.85`, this is a cache hit. We return "Paris" instantly, and we do not call the model.

Step 2: New question is "What is the population of France?" We compute its embedding and compare it. The similarity score comes out to be `0.40`. This is below `0.85`, so this is a cache miss. We send it to the model, get the fresh answer, and store it in the cache.

Step 3: New question is "How do I bake a chocolate cake?" We compute its embedding and compare it. The similarity score comes out to be `0.05`. This is far below `0.85`, so this is again a cache miss. We send it to the model and store the new answer.

Here, we can notice the pattern. Same meaning gives a high score and becomes a cache hit. Different meaning gives a low score and becomes a cache miss. This is exactly what we wanted.

### Setting the similarity threshold

The similarity threshold is the limit we choose to decide whether a new question is close enough to a saved one.

This single number is very important, so let's understand it carefully.

If we set the threshold too high, like `0.99`, then almost nothing matches. Only an exact copy would pass. We lose most of the benefit of Semantic Caching.

If we set the threshold too low, like `0.50`, then very different questions start matching. We may return a wrong answer. For example, "capital of France" could wrongly match "capital of Germany" and return the wrong city.

So, the threshold is a balance. A value around `0.85` to `0.95` works well for many apps, but the right value depends on our use case. We must test it with real questions from our users and adjust it.

> A high threshold means fewer matches but safer answers. A low threshold means more matches but a higher chance of a wrong answer.

To learn embeddings, Vector Databases, and RAG in depth, we cover all of these in our AI and Machine Learning Program at Outcome School.

### Advantages of Semantic Caching

Now, let's quickly look at why Semantic Caching is so useful.

- It saves money, because we call the expensive model far less often.
- It is much faster, because returning a saved answer takes very less time compared to asking the model.
- It reduces load on the model, so our app can handle many more users.
- It matches questions by meaning, so it works even when users phrase the same thing in different ways.

This is how Semantic Caching makes our AI apps cheaper and faster at the same time.

Semantic Caching is one way to cut the cost of LLM calls. Another is prompt caching, which reuses the model's internal work on a repeated prompt prefix. We have a detailed blog on how Prompt Caching works that explains this step by step.

### Things to keep in mind

Semantic Caching is powerful, but we must use it carefully. Let me share a few important points.

First, it is best for questions whose answers do not change quickly. A question like "What is the capital of France?" is perfect, because the answer stays the same. But a question like "What is the weather right now?" is not a good fit, because the correct answer changes every hour.

Second, we must pick a good threshold. As we learned, a wrong threshold can either kill the benefit or return wrong answers.

Third, we may want to clear or refresh the cache from time to time, so that old answers do not stay forever when the real answer has changed.

Now, we have understood how Semantic Caching works. We started with a simple cache, we saw why exact-match caching fails for AI apps, we learned about embeddings and similarity, and finally we put it all together into a clear step-by-step flow with a numeric walkthrough.

### What is the difference between semantic caching and prompt caching?

Semantic caching reuses the saved final answer when a new question means the same as an old one, so the model is not called at all. Prompt caching reuses the model's internal work on a repeated prompt prefix. Both help cut the cost of LLM calls.

### Can semantic caching return a wrong answer?

Yes, if the similarity threshold is set too low. With a low threshold like 0.50, very different questions start matching. For example, a question about the capital of France could wrongly match a question about the capital of Germany and return the wrong city. We must test the threshold with real user questions.

### Is semantic caching a good fit for questions like the current weather?

No. Semantic caching is best for questions whose answers do not change quickly, like the capital of France. A question about the weather right now is not a good fit, because the correct answer changes every hour. We may also refresh the cache from time to time so old answers do not stay forever.

### Where are the embeddings stored in a semantic cache?

In a real system, the saved embeddings live in a vector database. A vector database is built to store embeddings and find the closest ones fast using Approximate Nearest Neighbor search. Each entry keeps the question, its embedding, and its answer.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:
