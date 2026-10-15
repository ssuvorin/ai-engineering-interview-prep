> Source: https://outcomeschool.com/blog/n-gram-speculation-in-llms

# What is N-gram Speculation in LLMs and How Does It Speed Up Generation?
URL: https://outcomeschool.com/blog/n-gram-speculation-in-llms
Published: 2026-09-13
Author: Amit Shekhar

What is N-gram Speculation in LLMs and How Does It Speed Up Generation?

# What is N-gram Speculation in LLMs and How Does It Speed Up Generation?

Authors
: - Name
: Amit Shekhar
Published on
: September 13, 2026

N-gram Speculation is a simple trick that makes an LLM write its answer faster. It guesses the next few tokens by finding the same words earlier in the text, and then the model verifies all those guesses in one single run.

In this blog, we will learn about N-gram Speculation in LLMs, a simple trick that makes a language model write its answer faster by guessing the next few words from the text it has already seen. We will also see how an LLM writes one token at a time, why that is slow, what Speculative Decoding is, what an n-gram is, how N-gram Speculation guesses the next tokens by looking up the prompt, how the model verifies those guesses without changing the final answer, and where it works well and where it fails.

We will cover the following:

- How an LLM generates text
- Why generating text is slow
- What is Speculative Decoding?
- The cost of a draft model
- What is an N-gram?
- What is N-gram Speculation?
- N-gram Speculation step by step
- Why the output stays exactly the same
- Where it works well and where it fails
- N-gram Speculation vs Draft Model Speculative Decoding

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## How an LLM generates text

An LLM is a Large Language Model. It is an AI model that reads text and writes text. When we ask a chatbot a question, an LLM is writing the answer.

Before jumping into N-gram Speculation, we must know one thing about how an LLM writes.

An LLM writes its answer one token at a time.

A token is a small piece of text. For the sake of understanding, we can think of a token as a word. So, the sentence "The cat sat on the mat" has six tokens. Punctuation marks like "." are also tokens.

The text we give to the model is called the prompt. It can be a question, a document, a piece of code, or anything else.

Let's say our prompt asks the model to write a sentence about a cat. The model works like below:

- It reads everything written so far, which is the prompt, and predicts one token: "The"
- It adds "The" to the text, reads everything again, and predicts the next token: "cat"
- It adds "cat", reads everything again, and predicts: "sat"
- And so on, till the answer is complete.

So, to write 100 tokens, the model runs 100 times. Each run is called a decoding step.

And, every new token depends on all the tokens before it. So, the model cannot write the 10th token before it has written the 9th token. It has to go one by one.

We have a detailed blog on Autoregressive Models that explains this one-token-at-a-time generation in depth.

## Why generating text is slow

Now, the question is, why is this slow?

An LLM has billions of numbers inside it, called weights. The model runs on a special chip called the GPU. To predict even one token, the GPU has to load all these billions of weights from memory and do the math.

But, here is the catch. Loading the weights from memory takes much more time than doing the math. The GPU is very fast at math. But, it has to wait for the weights to arrive from memory. Most of the time, the GPU is just waiting.

Let's take an analogy. Assume that we have a chef who can cook ten dishes at once. But, the helper brings the ingredients from the store room for only one dish at a time. The chef cooks that one dish in a second and then waits for the helper again. The chef is fast, but the kitchen is slow because of the trips to the store room.

The GPU is the chef. The memory is the store room. Loading weights is the trip. Predicting one token is one dish.

The number of trips decides the speed, not the cooking. This is called being memory-bound. The speed is limited by memory, not by the math.

We have a detailed blog on Prefill vs Decode that explains why this decode phase of an LLM is memory-bound.

Now, one more important thing. Suppose the helper carries the ingredients for ten dishes in a single trip. The trip takes the same time as before. And, the chef cooks all ten dishes at once. So, we get ten dishes in the time we earlier got one.

Similarly, once the weights are loaded, the GPU can process many tokens at once for almost the same cost as one token.

But, there is a problem. The model cannot produce ten new tokens at once, because the second token depends on the first, the third depends on the second, and so on. It has to go one by one.

What it can do is check ten tokens at once, if someone gives it those ten tokens already. Checking means, for each position, the model tells us what it would have predicted there, and we see whether it agrees with the token we gave.

So, here comes the idea: if we can somehow guess the next few tokens cheaply, and then give all of them to the model to check in one run, we can save a lot of trips.

Here comes the Speculative Decoding into the picture.

## What is Speculative Decoding?

Speculative Decoding is a technique where we first guess the next few tokens quickly, and then ask the big model to verify all those guesses in one single run.

Here, the big model means our actual LLM, the one whose answer we want.

Speculate means to guess. So, Speculative Decoding = Guess first + Verify later.

It has two parts:

- Draft: Something cheap and fast guesses the next few tokens. Let's say it guesses 5 tokens.
- Verify: The big model takes all 5 guessed tokens together and checks them in one run. It accepts the guesses it agrees with and throws away the rest.

If the big model agrees with all 5 guesses, we get 5 tokens in the time of 1 run. If it agrees with only 2, we get 2 tokens plus one more correct token from the big model itself. Either way, we never get less than 1 token per run. So, we never lose.

Now, the next big question is: who does the guessing?

In the original Speculative Decoding, the guessing is done by a small LLM called the draft model. It is a smaller version of the big model, so it is fast, and it guesses reasonably well.

## The cost of a draft model

The draft model works, but it has its own problems.

- We need a second model. It has to be trained or found, and it must use the same vocabulary as the big model. Vocabulary means the list of tokens that the model knows. If the two models break text into different tokens, the guesses cannot be compared.
- It takes extra memory on the GPU. Memory is what we are short of.
- It takes time to run. Even if it is small, it still runs once for every guessed token.
- When the big model is updated, the draft model also needs to be updated to match it.

So, the question is, can we guess the next tokens without any extra model at all?

The answer is yes. We just look at the text we already have.

So, here comes the N-gram Speculation to the rescue.

## What is an N-gram?

Before jumping into N-gram Speculation, we must know what an n-gram is.

N-gram = N + gram

- gram means a piece or a unit. Here, one unit is one token.
- N is a number. It tells how many units are together.

In simple words, an n-gram is just N tokens standing next to each other in the text.

Let's take the sentence: "the cat sat on the mat"

- 1-grams: "the", "cat", "sat", "on", "the", "mat"
- 2-grams: "the cat", "cat sat", "sat on", "on the", "the mat"
- 3-grams: "the cat sat", "cat sat on", "sat on the", "on the mat"

That's it. An n-gram is just a small window of N tokens sliding over the text.

Now, one interesting observation. Text repeats a lot. If we see "sat on the" once, and later we see "sat on" again, there is a good chance the next token is "the" again. N-gram Speculation uses exactly this observation.

Now that we have learned about n-grams, it's time to learn about N-gram Speculation.

## What is N-gram Speculation?

N-gram Speculation is a form of Speculative Decoding where the guesses come from matching n-grams in the text we already have, instead of from a draft model.

The text we already have means the prompt plus the tokens generated so far.

In simple words, we take the last few tokens we have written. We search for the same few tokens earlier in the text. If found, we copy the tokens that came after that earlier match and use them as the guess.

There is no draft model here. The draft comes from the text itself.

This is also called Prompt Lookup Decoding, because we look up the prompt to make the guess.

Let's understand with an analogy.

Suppose we are copying a long paragraph from a book by hand. We have written "the quick brown". We do not need to think hard about what comes next. We just look at the book, find "the quick brown", and see that "fox jumps over" comes after it. We copy those words quickly. Then we double check that we copied correctly.

The book is our prompt. Looking at the book is the lookup. Copying "fox jumps over" is the draft. Double checking is the verification by the big model.

Why does this work? Because in many real tasks, the answer repeats big chunks of the input. For example, when we ask the model to summarize a document, fix a bug in a code file, or answer from a given passage, the model copies many phrases from the input word by word.

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

## N-gram Speculation step by step

The best way to learn this is by taking an example.

Let's say the prompt given to the model is:

"The cat sat on the mat. The dog sat on the rug. Now, repeat the first sentence:"

And the model has started writing the answer. Till now, it has written:

"The cat sat"

So, the full text is the prompt plus "The cat sat". We will use the last 2 tokens as the search key, so n = 2. And, we will draft up to 3 tokens, so k = 3.

Step 1: Take the last n-gram.

The last 2 tokens written are: "cat sat". This is our search key.

Step 2: Look up.

We search the full text for "cat sat". We skip the last 2 tokens themselves, because that is the key. We find a match in the prompt: "The cat sat on the mat."

Step 3: Draft.

We copy the tokens that came right after the match: "on the mat". These 3 tokens are our guess.

Draft = "on", "the", "mat"

Step 4: Verify.

Now, we give the big model the text "The cat sat on the mat" in one single run. The model reads all these tokens together and gives us a prediction at every position at the same time. This is the checking that we talked about earlier.

- After "The cat sat", the model predicts "on". Draft says "on". Match. Accept.
- After "The cat sat on", the model predicts "the". Draft says "the". Match. Accept.
- After "The cat sat on the", the model predicts "mat". Draft says "mat". Match. Accept.
- After "The cat sat on the mat", the model predicts ".". This is a bonus token that we get for free from the same run. We take it too.

So, in one run of the big model, we got 4 tokens: "on", "the", "mat", ".". Without speculation, we would have got only 1 token in that one run.

Now, let's see a case where the guess is wrong.

Suppose the prompt was "The cat sat on the mat. The cat sat on the sofa. Now, repeat the second sentence:" and the model has written "The cat sat".

Search key: "cat sat". We search from the start and find the first match: "The cat sat on the mat". Draft = "on", "the", "mat".

Verify:

- After "The cat sat", the model predicts "on". Match. Accept.
- After "The cat sat on", the model predicts "the". Match. Accept.
- After "The cat sat on the", the model predicts "sofa". Draft says "mat". Mismatch. Reject.

We keep "on" and "the", and we take the model's own token "sofa" in place of the rejected one. Everything after the first rejected token is thrown away, because those guesses were built on top of a wrong token.

So, in this run, we got 3 tokens: "on", "the", "sofa". Still better than 1.

Step 5: Repeat.

Now, the text is longer. We take the last 2 tokens again, look up again, draft again, verify again. This continues till the answer is complete.

What if the lookup finds nothing? Then, there is no draft. The big model simply predicts one token as usual. We lose nothing.

Let's see the code for the lookup as below:

```python
def ngram_draft(tokens, n, k):
    key = tokens[-n:]
    for i in range(len(tokens) - n):
        if tokens[i:i + n] == key:
            return tokens[i + n : i + n + k]
    return []

```

Here, we have:

- `tokens` is the full text so far, the prompt plus everything generated.
- `n` is the size of the n-gram that we use as the search key.
- `k` is the maximum number of tokens we want to guess.
- We take the last `n` tokens as the `key`.
- We slide over the text and find where the same `n` tokens appear earlier.
- When we find a match, we return the `k` tokens that come after it as the draft.
- If nothing matches, we return an empty list, which means no guess.

Now, let's see how the main loop uses it as below:

```python
while not done:
    draft = ngram_draft(tokens, n=2, k=3)
    accepted, next_token = big_model.verify(tokens, draft)
    tokens = tokens + accepted + [next_token]

```

Here, we have:

- We get a draft by looking up the text.
- The big model verifies all the draft tokens in one single run and returns the accepted ones and one extra token of its own.
- We add the accepted tokens and the extra token to our text.
- We repeat till the answer is done.

Note: Real implementations try multiple sizes of n, like 3, then 2, then 1, and search from the end of the text first, because recent text is more likely to repeat. In our second example, searching from the end would have found "cat sat on the sofa" first and the guess would have been correct. But the core idea is the same.

This was all about how N-gram Speculation works step by step. Now, let's understand why the final answer does not change.

If we want to go deep into LLM Inference Engineering and how to design an LLM Inference Platform (vLLM-as-a-Service), we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

## Why the output stays exactly the same

This is the most important thing to understand.

N-gram Speculation does not change what the model writes. It only changes how fast the model writes it.

The reason is verification. The draft is just a suggestion. The big model has the final say at every single position.

Let's think about it. At every position, we compare the draft token with what the big model itself predicts. If they match, we keep it. But, that is exactly the token the big model would have produced anyway. If they do not match, we throw the draft away and use the big model's own token.

So, in every case, every token in the final answer is a token that the big model chose. The draft only helped us skip some runs. The answer is the same as if we had never used speculation.

Note: This is exactly true when the model picks the single most likely token every time, which is called greedy decoding. When the model picks tokens randomly based on their probabilities, which is called sampling, a slightly smarter verification rule is used so that the answers still come out with the same probabilities as before. For the sake of understanding, we can say the final output quality is the same.

Now, let's see where we must use it and where we must not.

## Where it works well and where it fails

N-gram Speculation works well when the output repeats the input.

- Summarization: The summary reuses many phrases from the document.
- Code editing: When we ask the model to fix a small bug, most of the returned code is the same as the input code.
- RAG (Retrieval Augmented Generation): Here, we first search for related passages and put them in the prompt. The model then answers from those passages, so it copies facts and sentences from them.
- Repetitive text: JSON, tables, lists, where the same structure repeats again and again.

In these cases, the draft is often correct, and we can get 2 to 4 times faster generation for free, without any extra model.

N-gram Speculation fails when the output is new text that is not in the prompt.

- Creative writing: A poem or a story from a short prompt. There is nothing to look up.
- Open-ended chat: "Tell me about black holes." The prompt is short, the answer is long and new.
- Translation: The output is in a different language, so the words do not match the input.

In these cases, the lookup finds nothing or finds wrong guesses. We do not get slower in any big way, because a failed lookup is very cheap, but we also do not get faster.

So, based on our use case, we must decide. If the task copies from the input, N-gram Speculation is a free win.

Now that we have learned about N-gram Speculation, let's compare it with the draft model approach.

To master RAG, LLM Inference Performance Metrics, and Model Deployment and Serving, check out our AI and Machine Learning Program at Outcome School.

## N-gram Speculation vs Draft Model Speculative Decoding

Let me tabulate the differences between N-gram Speculation and Draft Model Speculative Decoding for your better understanding so that you can decide which one to use based on your use case.

| | N-gram Speculation | Draft Model Speculative Decoding |
| --- | --- | --- |
| Who makes the guess | A simple lookup in the existing text | A small neural network model |
| Extra model needed | No | Yes |
| Extra GPU memory | Almost none | Yes, for the draft model |
| Cost of making a guess | Very less, just a text search | Small, but it is a model run for every guessed token |
| Works best for | Tasks that copy from the input: summarization, code editing, RAG | Any task, including creative and open-ended text |
| Quality of guess on new text | Poor, nothing to look up | Good, the draft model can think |
| Setup effort | Very less, works with any model | Needs a matching draft model with the same vocabulary |
| Final output | Exactly the same as the big model | Exactly the same as the big model |

If our workload is mostly summarization, editing, or RAG, N-gram Speculation gives a good speed-up with zero extra cost. If our workload is open-ended, a draft model is the better choice. Many production systems use both together: try the n-gram lookup first, and fall back to the draft model when the lookup finds nothing.

There are also methods that drop the separate draft model in a different way, by training small extra heads on the big model so that it can draft for itself. We have detailed blogs on Medusa and EAGLE that explain how these work.

Let's summarize what we have learned.

An LLM writes one token at a time, and each step is slow because the GPU spends most of its time loading weights from memory. Speculative Decoding guesses a few tokens first and verifies them all in one run. A draft model can make the guesses, but it costs memory and time. N-gram Speculation makes the guesses by simply looking up the last few tokens in the text we already have and copying what came after them. The big model verifies every guess, so the final answer is exactly the same, just faster. It works very well when the answer repeats the input, and does nothing harmful when it does not.

This is how N-gram Speculation makes an LLM faster without any extra model.

### Is Prompt Lookup Decoding the same as N-gram Speculation?

Yes. N-gram Speculation is also called Prompt Lookup Decoding, because we look up the prompt to make the guess. We take the last few tokens, find the same tokens earlier in the text, and copy what came after them as the draft.

### Can N-gram Speculation make generation slower?

Not in any big way. When the lookup finds nothing, there is no draft and the big model simply predicts one token as usual. A failed lookup is very cheap, so we do not lose much, but we also do not get faster on such tasks.

### How much faster can N-gram Speculation make an LLM?

When the output repeats the input, like in summarization, code editing, or RAG, the draft is often correct and we can get 2 to 4 times faster generation. This speed-up comes for free, without any extra model.

### Can we use N-gram Speculation and a draft model together?

Yes. Many production systems use both together. They try the n-gram lookup first and fall back to the draft model when the lookup finds nothing. This way, copy-heavy tasks get a free speed-up, and open-ended tasks still get good guesses from the draft model.

### Does N-gram Speculation help with translation?

No. In translation, the output is in a different language, so the words do not match the input. The lookup finds nothing or finds wrong guesses. The same is true for creative writing and open-ended chat, where the answer is new text that is not in the prompt.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
