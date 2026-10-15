> Source: https://outcomeschool.com/blog/how-do-top-k-and-top-p-sampling-work

# How do Top-k and Top-p Sampling work?
URL: https://outcomeschool.com/blog/how-do-top-k-and-top-p-sampling-work
Published: 2026-09-19
Author: Amit Shekhar

How do Top-k and Top-p Sampling work?

# How do Top-k and Top-p Sampling work?

Authors
: - Name
: Amit Shekhar
Published on
: September 19, 2026

Top-k Sampling keeps only the k most likely tokens and picks randomly from them, whereas Top-p Sampling keeps the smallest group of top tokens whose probabilities add up to at least p, and picks randomly from that group.

In this blog, we will learn about how Top-k and Top-p Sampling work, the two most common ways an LLM decides which word to write next when it is replying to us. We will also see how an LLM picks one token at a time, why always picking the best token gives boring text, why picking from every token gives silly text, how Top-k keeps a fixed number of tokens, how Top-p keeps tokens based on their total probability, how both of them work with temperature, and when to use which one.

We will cover the following:

- How an LLM picks the next token
- The problem with always picking the best token
- The problem with picking from every token
- What is Top-k Sampling?
- Step-by-step example of Top-k Sampling
- The problem with Top-k Sampling
- What is Top-p Sampling?
- Step-by-step example of Top-p Sampling
- Top-k vs Top-p Sampling
- How Top-k and Top-p work with Temperature
- When to use which one

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## How an LLM picks the next token

Before jumping into Top-k and Top-p Sampling, we must know how an LLM writes text.

An LLM does not write a full sentence in one go. It writes one token at a time.

A token is a small piece of text. It can be a full word like "cat", a part of a word like "ing", or even a comma. For the sake of understanding, we can think of a token as a word.

Let's say we give the LLM the text "The cat sat on the". Now, the LLM has to decide the next token.

Inside the LLM, there is a list of every token it knows. This list is called the vocabulary. It is huge, it contains tens of thousands of tokens.

For every token in the vocabulary, the LLM gives a score. A higher score means the LLM thinks that token is a better fit as the next token. These raw scores are called logits.

Then, the LLM converts these scores into probabilities using a function called softmax. Do not worry, we do not need to go deep into softmax here. In simple words, softmax takes all the scores and turns them into percentages that add up to 100%. A probability is just the chance of that token being the next one. 40% means 40 chances out of 100.

We have a detailed blog on Cross-Entropy Loss that explains logits and softmax step by step.

So, for "The cat sat on the", the LLM gives probabilities like below:

| Token | Probability |
| --- | --- |
| mat | 40% |
| floor | 25% |
| sofa | 15% |
| bed | 10% |
| roof | 5% |
| every other token | 5% in total |

Here, we can see that "mat" has the highest probability, and thousands of other tokens together share the remaining 5%.

Note: We are showing only a few tokens in the table just for the sake of understanding. In a real LLM, this table has one row for every token in the vocabulary.

Now, the LLM has to pick one token from this list. This picking step is called sampling. The rule we follow while picking is called the decoding strategy.

Once a token is picked, it is added to the text, and the whole process repeats for the next token. This continues till the reply is complete. This way of writing, one token at a time, is called autoregressive generation, and we have a detailed blog on Autoregressive Models that explains it in depth.

So, Top-k and Top-p Sampling are all about one question: from this list of probabilities, which token do we pick?

Let's see the simple approaches first, and then we will see why we need Top-k and Top-p.

## The problem with always picking the best token

The simplest approach is to always pick the token with the highest probability. This is called Greedy Decoding.

In our example, it will always pick "mat".

Advantage: It is simple and fast.

Disadvantage: The text becomes boring and repetitive. Ask the same question twice, and we get the exact same answer. Many times, the LLM gets stuck in a loop like "I think that I think that I think that".

And, the most likely token at every step does not always give the most natural sentence overall. We humans do not always use the most common word. A little variety makes the text feel natural.

The issue with this approach is that there is no variety at all. Let's see how the next approach solve this issue.

## The problem with picking from every token

The opposite approach is to pick randomly from every token in the vocabulary based on its probability. This is called Pure Sampling.

Picking randomly based on probability is like a lottery. Suppose we have a box with 100 tickets. "mat" gets 40 tickets, "floor" gets 25 tickets, "sofa" gets 15 tickets, "bed" gets 10 tickets, "roof" gets 5 tickets, and the remaining 5 tickets are shared by every other token. We close our eyes and pick one ticket. The token written on that ticket is our next token.

Means, "mat" gets picked 40% of the time, "floor" gets picked 25% of the time, and so on.

Advantage: The text has variety. Every reply is different.

Disadvantage: Remember that thousands of other tokens together share 5%. Each one of them has a very tiny probability. But there are so many of them that together, one of them gets picked 5% of the time.

So, the LLM writes "The cat sat on the banana" or "The cat sat on the democracy". This looks silly.

And, this is not a one-time problem. The LLM writes hundreds of tokens in a reply. If even one silly token gets picked, the LLM builds the rest of the sentence on top of that silly token, and the whole reply goes off track.

The issue with this approach is that we let the LLM pick from the bad tokens at the bottom of the list. We need a way to keep the variety but cut off the bad tokens.

So, here comes the Top-k Sampling to the rescue.

## What is Top-k Sampling?

Top-k Sampling is a decoding strategy in which we keep only the k tokens with the highest probability, throw away all the others, and then pick randomly from those k tokens.

Top-k = Top + k

- Top: the tokens with the highest probability
- k: how many of them we keep

In simple words, we cut the list down to a fixed size k, and we run our lottery only on that short list.

Let's say we go to a restaurant and ask the waiter to pick a dish for us. A greedy waiter always picks the number one dish, every single time. A pure sampling waiter picks from the whole menu, even the dishes that nobody orders. Top-k is like a waiter who looks only at the 3 most popular dishes and picks one of them. The dishes that nobody orders are never picked.

Here, k is a number that we choose. It is a setting, not something the LLM learns. Common values are between 10 and 50.

## Step-by-step example of Top-k Sampling

The best way to learn this is by taking an example.

Let's take our example "The cat sat on the" with k = 3.

Step 1: Sort the tokens by probability, from highest to lowest.

| Token | Probability |
| --- | --- |
| mat | 40% |
| floor | 25% |
| sofa | 15% |
| bed | 10% |
| roof | 5% |
| every other token | 5% in total |

Step 2: Keep only the top k tokens.

With k = 3, we keep "mat", "floor", and "sofa". Everything else is thrown away.

| Token | Probability |
| --- | --- |
| mat | 40% |
| floor | 25% |
| sofa | 15% |

Step 3: Re-scale the probabilities so that they add up to 100% again.

Now, the three tokens add up to only 80%. So, we take each one as a share of that 80%. This is called renormalization.

| Token | New Probability |
| --- | --- |
| mat | 40 / 80 = 50% |
| floor | 25 / 80 = 31.25% |
| sofa | 15 / 80 = 18.75% |

Step 4: Pick one token randomly based on the new probabilities.

So, "mat" gets picked half of the time, "floor" gets picked around one-third of the time, and "sofa" gets picked around one-fifth of the time.

"banana" and "democracy" can never be picked. Problem Solved!

Let's see the code for Top-k Sampling, as below:

```python
import torch

def top_k_sampling(logits, k):
    # keep only the k highest scores
    top_values, top_indices = torch.topk(logits, k)
    # convert the kept scores into probabilities
    probs = torch.softmax(top_values, dim=-1)
    # pick one token randomly based on the probabilities
    chosen = torch.multinomial(probs, num_samples=1)
    return top_indices[chosen]

```

Here, we have:

- `torch.topk` gives us the k highest scores and their positions in the vocabulary.
- `torch.softmax` converts those k scores into probabilities that add up to 100%. This does the renormalization for us.
- `torch.multinomial` runs the lottery and picks one token based on the probabilities.
- Finally, we return the position of the chosen token in the vocabulary.

Note: Here, we apply softmax only on the k kept scores instead of all the scores. This gives exactly the same result as applying softmax on all the scores and then re-scaling the top k. So, we get the renormalization for free.

This is how Top-k Sampling works.

## The problem with Top-k Sampling

Top-k Sampling works well in our example. But, here is the catch.

The value of k is fixed. It does not change based on the situation. And, the situation changes at every token.

Let's see two very different situations.

Situation 1: The next token is obvious.

Let's say the text is "The capital of France is". The LLM is very sure here.

| Token | Probability |
| --- | --- |
| Paris | 95% |
| the | 2% |
| a | 1% |
| located | 1% |
| every other token | 1% in total |

With k = 3, we keep "Paris", "the", and "a". But, "the" and "a" are weak choices here. We are forcing weak tokens into the list just because k says we need three. So, once in a while, the LLM writes "The capital of France is the", which is a poor start.

Situation 2: The next token has many good options.

Let's say the text is "My favourite colour is". Many answers are equally good.

| Token | Probability |
| --- | --- |
| blue | 12% |
| red | 11% |
| green | 11% |
| black | 10% |
| purple | 10% |
| yellow | 9% |
| white | 9% |
| pink | 8% |
| every other token | 20% in total |

With k = 3, we keep only "blue", "red", and "green". But, "black", "purple", and "yellow" are just as good. We are cutting off good tokens just because k says we can keep only three. So, the LLM never says "black", "purple", or "yellow", and its answers feel limited.

So, the same k = 3 is too many in Situation 1 and too few in Situation 2.

The issue with this approach is that a fixed number k cannot adapt to how confident the LLM is. Let's see how the next approach solve this issue.

Here comes the Top-p Sampling into the picture.

## What is Top-p Sampling?

Top-p Sampling is a decoding strategy in which we keep the smallest group of top tokens whose probabilities add up to at least p, throw away all the others, and then pick randomly from that group.

Top-p = Top + p

- Top: the tokens with the highest probability
- p: the total probability we want to cover

In simple words, instead of saying "keep 3 tokens", we say "keep enough tokens to cover 90% of the probability".

Top-p Sampling is also called Nucleus Sampling. Nucleus means the core or the center of something. The small group of tokens that we keep is the core of the list, hence the name. It was introduced in 2019 in a research paper named "The Curious Case of Neural Text Degeneration".

Let's go back to our restaurant. Top-p is like a waiter who looks at the dishes that together make up 90% of all the orders. On a day when almost everyone orders one dish, that is just one dish. On a day when the orders are spread out, that is many dishes. The waiter adapts to the day.

Here, p is a number between 0 and 1 that we choose. Common values are between 0.9 and 0.95.

The size of the group is not fixed anymore. It becomes small when the LLM is sure and big when the LLM is unsure. This is the key difference from Top-k.

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

## Step-by-step example of Top-p Sampling

Let's take our example "The cat sat on the" with p = 0.9, which means 90%.

Step 1: Sort the tokens by probability, from highest to lowest.

| Token | Probability |
| --- | --- |
| mat | 40% |
| floor | 25% |
| sofa | 15% |
| bed | 10% |
| roof | 5% |
| every other token | 5% in total |

Step 2: Add the probabilities from the top, one by one, till the total reaches p.

| Token | Probability | Running Total |
| --- | --- | --- |
| mat | 40% | 40% |
| floor | 25% | 65% |
| sofa | 15% | 80% |
| bed | 10% | 90% |

The total reaches 90% at "bed". So, we stop here.

Step 3: Keep the tokens up to that point and throw away all the others.

We keep "mat", "floor", "sofa", and "bed". "roof" and every other token is thrown away.

Step 4: Re-scale the probabilities so that they add up to 100% again.

The four tokens add up to 90%. So, we take each one as a share of that 90%.

| Token | New Probability |
| --- | --- |
| mat | 40 / 90 = 44.4% |
| floor | 25 / 90 = 27.8% |
| sofa | 15 / 90 = 16.7% |
| bed | 10 / 90 = 11.1% |

Step 5: Pick one token randomly based on the new probabilities.

This is how Top-p Sampling works.

Now, let's see how the same p = 0.9 handles the two situations where Top-k struggled.

Situation 1: "The capital of France is"

| Token | Probability | Running Total |
| --- | --- | --- |
| Paris | 95% | 95% |

"Paris" alone crosses 90%. So, we keep only "Paris". The weak tokens "the" and "a" are thrown away. The group has just one token.

Situation 2: "My favourite colour is"

| Token | Probability | Running Total |
| --- | --- | --- |
| blue | 12% | 12% |
| red | 11% | 23% |
| green | 11% | 34% |
| black | 10% | 44% |
| purple | 10% | 54% |
| yellow | 9% | 63% |
| white | 9% | 72% |
| pink | 8% | 80% |

These eight tokens reach only 80%. So, we keep going into the tokens below "pink" till the total reaches 90%. The group has many tokens. All the good colours stay in the list.

So, the same p = 0.9 gave one token in Situation 1 and many tokens in Situation 2. The group size adapted itself to how confident the LLM was. All problems got solved.

Let's see the code for Top-p Sampling, as below:

```python
import torch

def top_p_sampling(logits, p):
    # convert all the scores into probabilities
    probs = torch.softmax(logits, dim=-1)
    # sort from highest to lowest
    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    # running total of the probabilities
    cumulative = torch.cumsum(sorted_probs, dim=-1)
    # running total before this token
    before = cumulative - sorted_probs
    # if the total before this token already reached p, we do not need it
    sorted_probs[before >= p] = 0.0
    # re-scale so that the kept probabilities add up to 1
    sorted_probs = sorted_probs / sorted_probs.sum()
    # pick one token randomly based on the probabilities
    chosen = torch.multinomial(sorted_probs, num_samples=1)
    return sorted_indices[chosen]

```

Here, we have:

- `torch.softmax` converts all the scores into probabilities.
- `torch.sort` puts the probabilities in order from highest to lowest.
- `torch.cumsum` gives the running total, just like the "Running Total" column in our table.
- `before` is the running total without the current token. If that total has already reached p, then the current token is not needed, so we set its probability to zero. This keeps the token which makes the total reach p and removes everything after it.
- We divide by the sum to re-scale the kept probabilities. This is the renormalization.
- `torch.multinomial` runs the lottery and picks one token.
- Finally, we return the position of the chosen token in the vocabulary.

This was all about Top-p Sampling. Now, let's compare both of them.

## Top-k vs Top-p Sampling

Let me tabulate the differences between Top-k and Top-p Sampling for your better understanding so that you can decide which one to use based on your use case.

| | Top-k Sampling | Top-p Sampling |
| --- | --- | --- |
| What we fix | The number of tokens to keep | The total probability to cover |
| Size of the kept group | Always exactly k | Changes at every token |
| When the LLM is very sure | Still keeps k tokens, some of them weak | Keeps very few tokens, sometimes just one |
| When the LLM is unsure | Still keeps only k tokens, cuts off good ones | Keeps many tokens |
| Other name | No other name | Nucleus Sampling |
| Common values | 10 to 50 | 0.9 to 0.95 |
| Work needed | Less, only find the top k | More, sort everything and keep a running total |

## How Top-k and Top-p work with Temperature

Many of you must be knowing about Temperature. Temperature is another setting that controls how random the output of an LLM is.

Temperature divides all the scores by the temperature value before they are converted into probabilities. A low temperature like 0.2 makes the top token even more likely, so the probabilities become sharp. Means, one token stands out clearly. A high temperature like 1.5 brings all the tokens closer to each other, so the probabilities become flat. Means, many tokens look almost equally likely.

Top-k and Top-p do not change the shape of the probabilities. They only cut the list.

So, they do different jobs:

- Temperature decides how sharp or how flat the probabilities are.
- Top-k and Top-p decide how many tokens stay in the list.

Now, the question is: can we use all three together? Yes, we can. Inside the LLM, they are usually applied in the below order:

Scores -> Temperature -> Top-k -> Top-p -> Convert to probabilities -> Pick one token

First, temperature reshapes the scores. Then, Top-k cuts the list to k tokens. Then, Top-p cuts it further if needed. Finally, we run the lottery on whatever is left. Many tools set k = 50 and p = 0.95 by default.

When we call an LLM API, we pass these as settings named `top_k`, `top_p`, and `temperature` along with our prompt. We do not have to write the sampling code ourselves. The code we saw above is what runs behind these settings.

Note: If we set k to a very large number or p to 1.0, then that filter does nothing, and we get Pure Sampling back. If we set k = 1 or p very close to 0, then only the top token survives, and we get Greedy Decoding back. So, Greedy Decoding and Pure Sampling are just the two ends of the same idea. Top-k and Top-p let us pick any point in between.

## When to use which one

- For tasks where the answer must be correct, like answering a factual question, writing code, or summarizing a document, we want less randomness. Use a small k like 10, or a p like 0.9, along with a low temperature. The LLM must not take chances here.
- For creative tasks, like writing a story or a poem, we want more variety. Use a larger k like 50, or a p like 0.95, along with a slightly higher temperature.
- When we are not sure, Top-p is the safer default because it adapts itself at every token. This is why almost every LLM API exposes Top-p as a setting, while Top-k is not always available.

### Can we use Top-k and Top-p together?

Yes. Inside the LLM, they are usually applied in order: temperature reshapes the scores, Top-k cuts the list to k tokens, and then Top-p cuts it further if needed. Finally, one token is picked from whatever is left. Many tools set k = 50 and p = 0.95 by default.

### What happens if we set top_p to 1.0?

The Top-p filter does nothing, and we get Pure Sampling back. The same happens when we set k to a very large number. On the other side, if we set k = 1 or p very close to 0, only the top token survives, and we get Greedy Decoding back.

### Is Top-p better than Top-k?

Top-p is the safer default when we are not sure, because it adapts itself at every token. It keeps very few tokens when the LLM is sure and many tokens when the LLM is unsure. This is why almost every LLM API exposes Top-p as a setting, while Top-k is not always available. Top-k does need less work, since it only finds the top k.

### Is Top-p the same as temperature?

No. Temperature decides how sharp or how flat the probabilities are by dividing the scores before they become probabilities. Top-k and Top-p do not change the shape of the probabilities. They only decide how many tokens stay in the list.

### Do we need to write Top-k or Top-p code when we use an LLM API?

No. When we call an LLM API, we pass settings named `top_k`, `top_p`, and `temperature` along with our prompt. The sampling code runs behind these settings, so we do not have to write it ourselves.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# Stop Tokens in LLMs
URL: https://outcomeschool.com/blog/stop-tokens-in-llms
Published: 2026-10-04
Author: Amit Shekhar

Stop Tokens in LLMs

# Stop Tokens in LLMs

Authors
: - Name
: Amit Shekhar
Published on
: October 4, 2026

A Stop Token is a special token in the vocabulary of an LLM that means the text ends here. When the model produces it, the generation loop stops writing.

In this blog, we will learn about Stop Tokens in LLMs. We will also see why an LLM needs to be told when to stop, how the model learns to produce the stop token during training, how it is different from a stop sequence that we set ourselves, what happens when the model never stops, how chat models use it, and the common mistakes we do while using it.

We will cover the following:

- What is a Token?
- How does an LLM generate text?
- Why does an LLM need to stop?
- What is a Stop Token?
- How does the model learn to produce a Stop Token?
- Stop Token vs Stop Sequence
- What happens if the model never stops?
- Stop Tokens in Chat Models
- Common mistakes with Stop Tokens

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a Token?

Before jumping into Stop Tokens, we must know what a token is.

A token is a small piece of text that an LLM (Large Language Model) reads and writes.

An LLM does not read text letter by letter, and it does not read text word by word. It reads text in small pieces called tokens.

A token can be a full word, a part of a word, a single character, a space, or a punctuation mark.

Let's say we have a sentence as below:

```
I love learning.

```

An LLM breaks it into tokens like below:

```
["I", " love", " learning", "."]

```

Here, we can see that each piece is one token. The space before "love" is part of the token itself. This is how the model keeps track of where one word ends and the next one begins.

Every token has a number attached to it. The model does not work with the text directly, it works with these numbers. The full list of all the tokens that a model knows is called its vocabulary.

For the sake of understanding, think of the vocabulary as a big dictionary where every entry has a serial number. The model only sees the serial numbers.

We have a detailed blog on Tokenization in LLMs that explains step by step how text is broken into tokens.

Now that we know what a token is, let's see how an LLM uses tokens to write text.

## How does an LLM generate text?

An LLM writes text one token at a time. This writing is called generation.

It does not write the full answer in one go. It picks one token, adds it to the text, and then picks the next token by looking at everything written so far.

The best way to learn this is by taking an example.

The text we give to the model is called a prompt. Let's say our prompt is as below:

```
The capital of India is

```

The model works like below:

Step 1: It looks at "The capital of India is" and picks the next token: " New"

Step 2: It looks at "The capital of India is New" and picks the next token: " Delhi"

Step 3: It looks at "The capital of India is New Delhi" and picks the next token: "."

At every step, the model does the same thing. It looks at the full text so far and gives a score to every token in its vocabulary. A token with a high score is more likely to come next. Then one token is picked based on these scores and added to the text.

This loop has a name, autoregressive generation.

Autoregressive = Auto + Regressive

Auto means self. Regressive here means going back to what has already been produced. So, the model feeds its own output back as its input, again and again.

We can write this loop as below:

```python
tokens = tokenize(prompt)

while True:
    next_token = model.predict_next(tokens)
    tokens.append(next_token)

```

Here, `tokenize` breaks the prompt into tokens. `while True` means the loop runs again and again without any end. Inside the loop, we ask the model for the next token, add it to the list, and ask again.

Look at the loop carefully. When does it end?

## Why does an LLM need to stop?

The loop we just saw has no exit. There is nothing in it that says "you are done".

If nothing stops it, the model will keep going. After "New Delhi." it will pick another token, and another, and another. It will start writing about the history of Delhi, then about the weather, then about something else. It will never stop on its own.

So, we need a way to tell the model when the answer is complete.

There are two ways to stop the loop:

- We set a fixed limit. Say, stop after 100 tokens.
- We let the model itself say "I am done".

The first way is simple, but it is not enough on its own. If the answer needs only 5 tokens, we waste time and money producing 95 more tokens of junk. And if the answer needs 200 tokens, we cut it in the middle.

The second way is much better. The model knows when the answer is complete. It just needs a way to say so.

So, here comes the Stop Token to the rescue.

## What is a Stop Token?

A Stop Token is a special token in the vocabulary of the model that means "the text ends here".

It is not a normal word. It is not part of the answer that we read. It is a hidden marker that the model produces when it believes the answer is complete.

When the generation loop sees this token, it stops. No more tokens are produced.

A normal full stop "." ends a sentence. A stop token ends the entire response.

Different models give different names to this token. Some common ones are:

- `<|endoftext|>` used by GPT-2 and many older models
- ` ` used by Llama 2 and many models built on top of it
- `<|eot_id|>` used by Llama 3
- `<|im_end|>` used by Qwen and many other chat models
- `<end_of_turn>` used by Gemma

The name of the token does not matter. What matters is that it is one token in the vocabulary with its own number, and the generation loop treats it as a signal to stop.

Many people also call it the EOS token. EOS stands for End Of Sequence. A sequence is just the full piece of text. So, End Of Sequence means the end of the text. Stop Token and EOS token are often used to mean the same thing.

Our updated loop with the stop token:

```python
tokens = tokenize(prompt)

while True:
    next_token = model.predict_next(tokens)
    if next_token == STOP_TOKEN:
        break
    tokens.append(next_token)

print(detokenize(tokens))

```

Here, we have added a check. Before adding the token to the list, we see if it is the stop token. If yes, we `break`, which means we come out of the loop and it stops. The stop token is never added to the list, so it never shows up in the final text. At the end, `detokenize` joins the tokens back into text.

Let's see our example again with the stop token.

Step 1: " New"

Step 2: " Delhi"

Step 3: "."

Step 4: `<|endoftext|>` and the loop stops.

The output shown to us: "The capital of India is New Delhi."

It works perfectly.

Here, we can notice that the stop token is produced by the model just like any other token. It gets a score at every step. At Step 1, the stop token gets a very low score, because "The capital of India is" is clearly not complete. At Step 4, it gets the highest score, because the answer is complete now.

Now, the next big question is: how does the model know when to produce this token?

## How does the model learn to produce a Stop Token?

The model is not given a rule like "stop after answering the question". The model learns this from data, just like it learns everything else.

Let's understand how.

An LLM is trained on a huge amount of text. This text is made of many separate documents like articles, books, web pages, code files, conversations, and etc.

Before training, a stop token is attached at the end of every document. So, the training data looks like below:

```
This is the full text of document one. <|endoftext|>
This is the full text of document two. <|endoftext|>
This is the full text of document three. <|endoftext|>

```

During training, the model has only one job. It looks at the text so far and tries to guess the next token. When it guesses wrong, it gets corrected a little. This happens billions of times.

Now, think about what happens at the end of each document. The text so far is the full document, and the correct next token is the stop token. Every time the model fails to guess the stop token here, it gets corrected.

The stop token also does one more job here. It marks where one document ends and the next one begins. So, the model learns that the text after the stop token is a fresh start.

Slowly, the model learns a pattern. When a piece of text feels complete, which means the story has ended, or the question is answered, or the code file is closed, the next token is very likely the stop token.

This is why the model can stop on its own. It has seen millions of endings, and it has learned what an ending looks like.

For the sake of understanding, think of a child who has been read thousands of stories. After a while, the child knows that "and they lived happily ever after" is followed by closing the book. Nobody taught this rule directly. The child picked it up from seeing it many times.

The stop token works the same way. It is learned, not written as a fixed rule.

For chat models, there is one more round of training where the data looks like a conversation between a user and an assistant. Every assistant reply ends with a stop token. So, the model learns to produce the stop token when its reply is done, and this hands the turn back to the user. We will see this in detail in a later section.

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

Now that we know how the model learns to produce the stop token, let's see one more concept that is very often confused with it.

## Stop Token vs Stop Sequence

Many times, people use these two terms as if they are the same. They are not.

A Stop Token is a single special token built into the vocabulary of the model. The model learns to produce it during training.

A Stop Sequence is any piece of text that we, as users of the model, ask the system to watch for. When that text appears in the output, generation stops.

Let's say we are using an LLM through an API. Most LLM APIs allow us to pass a list of stop sequences as below:

```python
response = client.completions.create(
    model="some-model",
    prompt="Q: What is 2 + 2?\nA:",
    stop=["\n", "Q:"]
)

```

Here, `\n` means a new line. We have passed `stop=["\n", "Q:"]`. This tells the system: if the model writes a new line or writes "Q:", stop right there.

The model does not know anything about our stop sequence. It keeps producing tokens as usual. The system around the model checks the output after every token, and when it finds a match, it cuts the generation.

Why do we need this? Because sometimes the model does not produce a stop token where we want it to.

In the above example, without a stop sequence, the model often answers "4" and then keeps going. It starts writing "Q: What is 3 + 3?" on its own, because it is just continuing the pattern it sees. In its training data, a list of questions and answers usually continues with more questions. So, the stop token does not get a high score here.

The stop sequence "Q:" catches this and stops it.

We can add this check to our loop as below:

```python
tokens = tokenize(prompt)

while True:
    next_token = model.predict_next(tokens)
    if next_token == STOP_TOKEN:
        break
    tokens.append(next_token)
    text = detokenize(tokens)
    if ends_with_any(text, stop_sequences):
        break

```

Here, after adding each token, we convert the tokens back to text. Then `ends_with_any` checks if the text ends with any one of our stop sequences. If yes, we break out of the loop.

Let me tabulate the differences between Stop Token and Stop Sequence for your better understanding.

| | Stop Token | Stop Sequence |
| --- | --- | --- |
| What is it? | One special token in the vocabulary | Any piece of text we choose |
| Who decides it? | Decided during the training of the model | Decided by us at the time of use |
| Who produces it? | The model itself | The model does not know about it |
| Who checks it? | The generation loop | The code around the model |
| Shown in output? | No, it is removed | Usually removed from the output |
| Example | ` `, `<end_of_turn>` | `"\n"`, `"Q:"`, `"###"` |

In practice, both work together. The stop token is always active. The stop sequence is an extra check that we add based on our use case.

## What happens if the model never stops?

Now, let's think about a bad case. What if the model never produces the stop token, and no stop sequence appears either?

This can happen. Sometimes the model gets into a loop where it repeats the same phrase again and again. Sometimes it is a badly trained model. Sometimes the prompt is so unusual that the model never feels the text is complete.

If we rely only on the stop token, the generation will run forever. It will waste time, memory, and money.

Remember the fixed limit we set aside earlier? It comes back now, but as a backup, not as the main way to stop.

This is why every system also sets a maximum token limit. It is usually called `max_tokens` or `max_new_tokens`.

Our updated loop with all three checks:

```python
tokens = tokenize(prompt)
generated = 0

while generated < max_tokens:
    next_token = model.predict_next(tokens)
    if next_token == STOP_TOKEN:
        break
    tokens.append(next_token)
    generated += 1
    text = detokenize(tokens)
    if ends_with_any(text, stop_sequences):
        break

```

Here, the loop now runs only while the count of generated tokens is less than `max_tokens`. So, generation stops when any one of the following happens first:

- The model produces the stop token.
- A stop sequence appears in the output.
- The maximum token limit is reached.

So, there are three brakes on the generation loop. The stop token is the natural brake. The stop sequence is the brake we add. The maximum token limit is the emergency brake.

Most APIs also tell us which brake was used. This is returned as `finish_reason` or `stop_reason`. A value like `stop` or `end_turn` means the model ended on its own with the stop token, or a stop sequence was found. A value like `length` or `max_tokens` means the limit cut it.

If we see `length` too often, it means our limit is too small and the answers are getting cut in the middle. We must increase the limit.

## Stop Tokens in Chat Models

Now, let's take a real use-case. When we chat with an AI assistant, how does it know when its turn is over?

The chat is formatted with special tokens that mark who is speaking. A simplified version looks like below:

```
<|user|>
What is the capital of India?
<|end|>
<|assistant|>
The capital of India is New Delhi.
<|end|>

```

Here, `<|user|>` and `<|assistant|>` mark who is speaking, and `<|end|>` marks the end of a turn. All three are special tokens in the vocabulary, just like the stop token we saw earlier.

During training, the model sees many conversations in this format. Every assistant reply ends with `<|end|>`. So, when the model is answering, it produces `<|end|>` as soon as it feels the reply is complete. The system sees this token, stops the generation, removes the token, and shows the reply to us. Then it waits for our next message.

Here, `<|end|>` is the stop token for this chat model. In Llama 3, it is `<|eot_id|>`. In Qwen, it is `<|im_end|>`. The idea is the same.

Note: Some models have more than one stop token. Llama 3 uses `<|end_of_text|>` to mark the end of a document and `<|eot_id|>` to mark the end of a turn in a chat. Both are treated as signals to stop.

This is how a chat model knows when its turn is over. It does not keep talking forever, and it does not start writing our next question for us. It stops, because it has learned that its turn ends with this token.

## Common mistakes with Stop Tokens

Most of the time, we do mistakes while using stop tokens. Let's see the common ones.

Mistake 1: Using the wrong stop token for the model.

When we download a model and run it on our own machine, we must use the stop token that the model was trained with. Let's say the model was trained to end its turn with `<|eot_id|>`, but our setup is waiting for ` `. The model will produce `<|eot_id|>`, our setup will not recognize it, and the model will keep going. It will start writing the user's next message on its own.

Many people faced this exact issue when Llama 3 was released. The fix is to set the correct stop token in the generation settings.

Mistake 2: Setting the maximum token limit too small.

If the limit is too small, the answer gets cut in the middle of a sentence. The model never gets the chance to produce the stop token. We must always check the `finish_reason`. If it says `length`, we must increase the limit.

Mistake 3: Forgetting the stop token in fine-tuning data.

Fine-tuning means training an already trained model a little more on our own data. When we fine-tune a model, every training example must end with the stop token. If we forget it, the model never learns when to stop for our type of data. After fine-tuning, it will keep rambling after every answer.

Mistake 4: Showing the stop token to the user.

Sometimes the code that converts tokens back to text does not remove the special tokens. Then the user sees `<|endoftext|>` or ` ` at the end of every answer. Most tools have an option like `skip_special_tokens=True` to handle this. We must make sure it is turned on.

Now we must have understood what Stop Tokens in LLMs are, how the model learns to produce them, and how they work together with stop sequences and the maximum token limit.

### Is the stop token shown in the final answer?

No. The stop token is a hidden marker, not part of the answer we read. The generation loop stops when it sees the token and does not add it to the text. If the code that converts tokens back to text does not remove special tokens, the user may see it, so an option like `skip_special_tokens=True` must be turned on.

### Is a Stop Token the same as an EOS token?

Yes. Stop Token and EOS token are often used to mean the same thing. EOS stands for End Of Sequence, and a sequence is just the full piece of text. Different models give this token different names, like `<|endoftext|>`, ` `, or `<|eot_id|>`, but the name does not matter.

### Why does an LLM keep writing the user's next message on its own?

This usually happens when our setup waits for the wrong stop token. If the model ends its turn with `<|eot_id|>` but our setup waits for ` `, the model's stop token is not recognized and it keeps going. Many people faced this when Llama 3 was released. The fix is to set the correct stop token in the generation settings.

### Can a model have more than one stop token?

Yes. Some models have more than one stop token. Llama 3 uses `<|end_of_text|>` to mark the end of a document and `<|eot_id|>` to mark the end of a turn in a chat. Both are treated as signals to stop the generation.

### What does a finish_reason of length mean?

It means the maximum token limit cut the answer, not the model. The model never got the chance to produce the stop token, so the answer may end in the middle of a sentence. If we see `length` too often, our limit is too small and we must increase it.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# Residual Connections in Transformers: Preserving Knowledge | AMIT SHEKHAR posted on the topic | LinkedIn
URL: https://www.linkedin.com/posts/amit-shekhar-iitbhu_machinelearning-llm-deeplearning-share-7414239846707392512-pQdQ
Published: 2026-01-06
Author: AMIT SHEKHAR

Residual Connections in Transformers: Preserving Knowledge | AMIT SHEKHAR posted on the topic | LinkedIn

# Residual Connections in Transformers: Preserving Knowledge

 AMIT SHEKHAR 

What residual (skip) connections do in Transformers In a Transformer block, you'll always see patterns like: x = x + f(x) That is the residual connection. It allows the model to learn a refinement on top of the input, rather than learning everything from scratch. So, the residual connections let layers add knowledge instead of replacing it. Let's try to understand with an analogy. Imagine you are learning a topic over a period of time. Without a residual (skip) connection: x = f(x) • Whatever you learn each day, you REWRITE your notes from scratch. • Old knowledge is NOT preserved. With a residual (skip) connection: x = x + f(x) • You keep your existing notes and only add what is useful from today's learning. • Old knowledge is preserved. • If today's lesson isn't useful, you add nothing. This is what residual (skip) connections do in Transformers. Keep Learning, Keep Sharing, and Keep Growing. #machinelearning #llm #deeplearning #ai #transformers

 Outcome School 9mo 

#MachineLearning

Error fetching https://x.com/amitiitbhu/status/1927927814923207146: SOURCE_NOT_AVAILABLE
