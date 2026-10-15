> Source: https://outcomeschool.com/blog/how-does-temperature-control-llm-output

# How does Temperature control LLM output?
URL: https://outcomeschool.com/blog/how-does-temperature-control-llm-output
Published: 2026-09-15

How does Temperature control LLM output?

# How does Temperature control LLM output?

Authors
: - Name
: Amit Shekhar
Published on
: September 15, 2026

In this blog, we will learn about how Temperature controls LLM output, the single number that decides whether an AI model gives us a safe and predictable answer or a creative and surprising one. We will also see how an LLM picks one token at a time, how it gives a score to every possible next token, how those scores become probabilities, how Temperature quietly changes those probabilities before the pick happens, what happens at low, high, and zero Temperature, why it is called Temperature, and when to use which value based on our use case.

We will cover the following:

- What is Temperature in LLMs?
- How does an LLM pick the next token?
- From scores to probabilities
- Where does Temperature come into the picture?
- Step-by-step example with numbers
- Low Temperature
- High Temperature
- Temperature = 1 and Temperature = 0
- Why is it called Temperature?
- When to use which Temperature?
- Common mistakes while using Temperature

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Temperature in LLMs?

Before jumping into Temperature, we must know what an LLM is.

LLM stands for Large Language Model. It is the AI model behind tools like ChatGPT. We give it some text, and it writes the next part of the text for us. That is all an LLM does. It writes text, one small piece at a time.

Now, let's understand Temperature.

Temperature is a number that controls how random or how predictable the output of an LLM is.

In simple words, Temperature is like a knob. When we turn the knob down, the model plays safe and picks the most expected words. When we turn the knob up, the model takes risks and picks surprising words.

- Low Temperature gives us focused and predictable answers.
- High Temperature gives us creative and varied answers.

Usually, the value is between 0 and 2. Many tools keep 1 as the default.

But, to really understand how this knob works, we must first understand how an LLM picks the next word. This is the most important part, so let's go slowly. Do not worry, we will see all of this with real numbers.

## How does an LLM pick the next token?

An LLM does not write a full sentence at once. It writes one small piece at a time, and then the next piece, and then the next.

This small piece is called a token. A token is a word or a part of a word. For the sake of understanding, let's assume that one token is one word.

Let's say we give the model this text:

"The sky is"

Now, the model has to pick the next token. It does not "think" of the next word like we do. Instead, it looks at every token it knows and gives each one a score. A higher score means that token is a better fit as the next token.

Let's say, for the sake of example, the model knows only four tokens: "blue", "clear", "falling", and "banana". In reality, a model knows more than 100,000 tokens, but four is enough for us to understand.

The model gives a score to each of them, like below:

| Token | Score |
| --- | --- |
| blue | 4.0 |
| clear | 3.0 |
| falling | 1.0 |
| banana | 0.0 |

Here, "blue" has the highest score because "The sky is blue" is the most common sentence. "banana" has the lowest score because "The sky is banana" makes no sense.

These raw scores are called logits. Do not worry about the name. Just remember, logits are the raw scores that the model gives to every possible next token.

Now, the question is, does the model simply pick the token with the highest score?

The answer is, not always. Let's see why.

## From scores to probabilities

The model does not directly pick the highest score. First, it converts these scores into probabilities.

A probability is just a chance. If a token has a probability of 0.70, it means there is a 70% chance that this token gets picked.

The model uses a small formula called softmax to convert scores into probabilities. Softmax does two things:

- It turns every score into a positive number.
- It makes all the probabilities add up to 1, which means 100%.

Let's not go into the math of softmax. Just remember, a higher score gives a higher probability, and a lower score gives a lower probability.

We have a detailed blog on Cross-Entropy Loss that explains logits and softmax in depth.

After softmax, our four tokens look like below:

| Token | Score | Probability |
| --- | --- | --- |
| blue | 4.0 | 0.70 |
| clear | 3.0 | 0.26 |
| falling | 1.0 | 0.03 |
| banana | 0.0 | 0.01 |

Here, we can see that "blue" has a 70% chance, "clear" has a 26% chance, "falling" has a 3% chance, and "banana" has a 1% chance. All four add up to 100%.

Now, the model picks one token based on these chances. This is like a lucky draw. Think of a box with 100 slips of paper. 70 slips say "blue", 26 slips say "clear", 3 slips say "falling", and 1 slip says "banana". The model puts its hand in the box and picks one slip without looking.

Most of the time, it will pick "blue". Sometimes, it will pick "clear". And very rarely, it will pick "banana".

This picking process is called sampling.

So, this is how an LLM picks the next token. Score, then probability, then lucky draw.

After picking one token, the model adds it to the text and repeats the whole process for the next token. This goes on till the answer is complete. This way of writing, one token at a time while looking back at everything written so far, is called autoregressive generation, and we have a detailed blog on Autoregressive Models that explains it step by step.

Now, here comes the Temperature into the picture.

## Where does Temperature come into the picture?

Temperature works on the scores, just before softmax converts them into probabilities.

The idea is very simple. The model divides every score by the Temperature before converting them into probabilities.

New Score = Score / Temperature

That's it. This one small division is the whole trick.

Let's see what this division does:

- When Temperature is 1, every score gets divided by 1. Nothing changes.
- When Temperature is less than 1, like 0.5, every score gets divided by 0.5, which means every score gets doubled. The gap between the high and low scores becomes bigger.
- When Temperature is more than 1, like 2, every score gets divided by 2, which means every score gets halved. The gap between the high and low scores becomes smaller.

Now, the next big question is: why does the gap matter?

The answer is, softmax cares about the gap. Softmax looks at how far apart the scores are. If one score is far ahead of the others, it gets almost all the probability. If all the scores are close together, the probability gets shared among them.

Means, Temperature changes the number of slips in our lucky draw box. Low Temperature gives the top token almost all the slips. High Temperature spreads the slips more evenly among all the tokens.

The best way to learn this is by taking an example.

## Step-by-step example with numbers

Let's take the same four tokens with the same scores and see what happens at different Temperatures.

Step 1: Temperature = 1

Every score is divided by 1. So, the scores stay the same.

| Token | Score / 1 | Probability |
| --- | --- | --- |
| blue | 4.0 | 0.70 |
| clear | 3.0 | 0.26 |
| falling | 1.0 | 0.03 |
| banana | 0.0 | 0.01 |

This is the original behavior of the model. Nothing is changed.

Step 2: Temperature = 0.5

Every score is divided by 0.5, which doubles it.

| Token | Score / 0.5 | Probability |
| --- | --- | --- |
| blue | 8.0 | 0.88 |
| clear | 6.0 | 0.12 |
| falling | 2.0 | 0.00 |
| banana | 0.0 | 0.00 |

Here, we can notice that "blue" went up from 70% to 88%. And "falling" and "banana" have almost zero chance now. The gap became bigger. The model became more sure about its top choice.

Step 3: Temperature = 0.1

Every score is divided by 0.1, which multiplies it by 10.

| Token | Score / 0.1 | Probability |
| --- | --- | --- |
| blue | 40.0 | 1.00 |
| clear | 30.0 | 0.00 |
| falling | 10.0 | 0.00 |
| banana | 0.0 | 0.00 |

Here, "blue" has almost a 100% chance. The model will pick "blue" every single time.

Step 4: Temperature = 2

Every score is divided by 2, which halves it.

| Token | Score / 2 | Probability |
| --- | --- | --- |
| blue | 2.0 | 0.51 |
| clear | 1.5 | 0.31 |
| falling | 0.5 | 0.11 |
| banana | 0.0 | 0.07 |

Here, "blue" dropped from 70% to 51%. And "banana" went up from 1% to 7%. The gap became smaller. Now, the weak tokens have a real chance of getting picked.

Let me put all of this in one table for your better understanding:

| Temperature | blue | clear | falling | banana |
| --- | --- | --- | --- | --- |
| 0.1 | 1.00 | 0.00 | 0.00 | 0.00 |
| 0.5 | 0.88 | 0.12 | 0.00 | 0.00 |
| 1 | 0.70 | 0.26 | 0.03 | 0.01 |
| 2 | 0.51 | 0.31 | 0.11 | 0.07 |

We found the pattern here. As Temperature goes down, the top token takes everything. As Temperature goes up, the chances spread out and every token gets a fair share.

Note: Temperature does not change the order of the tokens. "blue" is always the top choice at every Temperature. Temperature only changes how far ahead "blue" is from the rest.

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

Let's see the code for this, so that we can try it ourselves:

```python
import math

def softmax_with_temperature(scores, temperature):
    scaled = [score / temperature for score in scores]
    exps = [math.exp(score) for score in scaled]
    total = sum(exps)
    return [round(e / total, 2) for e in exps]

scores = [4.0, 3.0, 1.0, 0.0]  # blue, clear, falling, banana

print(softmax_with_temperature(scores, 1.0))
print(softmax_with_temperature(scores, 0.5))
print(softmax_with_temperature(scores, 2.0))

```

Here, we have done the following:

- First, we divide every score by the Temperature. This is the Temperature step.
- Then, we apply `math.exp` on each scaled score. This turns every score into a positive number. This is the first part of softmax.
- After that, we divide each number by the total. This makes them all add up to 1. This is the second part of softmax.
- Finally, we round the result to two decimal places so that it is easy to read.

It will print the following:

```
[0.7, 0.26, 0.03, 0.01]
[0.88, 0.12, 0.0, 0.0]
[0.51, 0.31, 0.11, 0.07]

```

These are the same numbers we saw in our tables. It works perfectly.

This was all about how Temperature works inside the model. Now, let's understand what this means for the actual text we get from the model.

## Low Temperature

A low Temperature is a value close to 0, like 0.1 or 0.2.

At low Temperature, the model almost always picks the top token. So, the output is:

- Focused and predictable.
- Same or nearly the same every time we ask.
- Safe and to the point.

Let's say we ask the model, "Write one line about the sky." At low Temperature, we will get "The sky is blue." almost every time.

Advantage: The answers are reliable. We can trust that the model is not going off track.

Disadvantage: The answers can become boring and repetitive. If we ask for ten different story ideas, we can get ten very similar ideas.

## High Temperature

A high Temperature is a value above 1, like 1.5 or 2.

At high Temperature, the weak tokens get a real chance. So, the output is:

- Creative and surprising.
- Different every time we ask.
- Sometimes strange or wrong.

Let's say we ask the same question, "Write one line about the sky." At high Temperature, we can get "The sky is clear." or "The sky is falling." or even "The sky is banana."

Advantage: The answers are varied and creative. This is great for brainstorming and stories.

Disadvantage: The model can pick a bad token, and one bad token can spoil the whole answer.

Here, one thing is very important to understand. Remember, the model picks one token at a time, and it uses the tokens already picked to pick the next one. So, if a high Temperature makes the model pick "banana", now the model has to continue the sentence "The sky is banana". The model picks every next token based on this strange start, and things go downhill from there. Hence, a very high Temperature often gives us nonsense.

## Temperature = 1 and Temperature = 0

Two values are special.

Temperature = 1 means no change. The model uses its original probabilities. This is the natural behavior of the model, exactly as it was trained.

Temperature = 0 means the model always picks the token with the highest score. No lucky draw at all. This is called greedy decoding, because the model greedily grabs the best token every time.

Strictly speaking, we cannot divide by 0. So, when we set Temperature to 0, the software behind the model does not actually divide. It simply skips the lucky draw and picks the top token directly.

Note: Even at Temperature 0, the output can sometimes differ a little between two runs. This happens because of tiny rounding differences inside the computer chips that run the model, not because of Temperature. So, Temperature 0 gives us "almost always the same", not "guaranteed the same".

If we want to go deep into LLM Internals, Logits and Cross-Entropy, and build a Large Language Model (LLM) from scratch, check out our AI and Machine Learning Program at Outcome School.

## Why is it called Temperature?

The name comes from physics.

Think of water. When water is cold, its tiny particles move very less and stay fixed in their place, like ice. When water is hot, the particles move a lot and jump around freely, like steam.

The same thing happens with our tokens. At low Temperature, the model stays fixed on its top choice, like ice. At high Temperature, the model jumps around between many choices, like steam.

Researchers borrowed this idea from a formula in physics, and the name Temperature stayed with it.

## When to use which Temperature?

Now, we know what Temperature does. So, which value must we use? The answer is, it depends on our use case.

Let me tabulate the common use cases for your better understanding so that you can decide which value to use based on your use case.

| Use case | Temperature | Why |
| --- | --- | --- |
| Writing code | 0 to 0.2 | Code must be correct, not creative |
| Maths and facts | 0 to 0.2 | There is only one right answer |
| Summarizing a document | 0.2 to 0.5 | Must stay close to the original |
| Customer support chat | 0.3 to 0.7 | Friendly, but still accurate |
| General chat | 0.7 to 1 | Natural and human-like |
| Story writing and poems | 0.8 to 1.2 | Creative and surprising |
| Brainstorming ideas | 1 to 1.5 | We want many different ideas |

Here, we can see the pattern. When there is one correct answer, keep the Temperature low. When there are many good answers, keep the Temperature high.

These ranges are just a starting point. The right value depends on our use case, so we must try a few values and see which one works best.

When developers use an LLM inside their own app, they send a request to the model, and this request has a place for Temperature. We can set it like below:

```python
response = model.generate(
    prompt="Write one line about the sky.",
    temperature=0.2
)

```

Here, `prompt` is the text we give to the model, and `temperature` is our knob. We have passed `temperature=0.2`, so the model will give a focused and predictable answer. If we change it to `temperature=1.2`, the same prompt will give a creative and varied answer. Nothing else changes, only this one number.

## Common mistakes while using Temperature

Most of the time, we do mistakes while using Temperature. Let's see the common ones.

Mistake 1: Thinking that Temperature makes the model smarter.

Temperature does not add any knowledge to the model. It does not make the model more correct. It only changes how the model picks from what it already knows. If the model does not know the answer, no Temperature can fix that.

Mistake 2: Setting a very high Temperature to get creativity.

Above 1.5 or so, the output quickly turns into nonsense. Creativity comes from a slightly high Temperature, not a very high one.

Mistake 3: Expecting Temperature 0 to give exactly the same output every time.

As we learned, tiny rounding differences can still change the output a little. If we need exactly the same output, we must save it and reuse it, not ask the model again.

Mistake 4: Changing Temperature and Top-p together.

Top-p is another setting that controls randomness. It works by removing the weak tokens from the lucky draw box, so that only the strong tokens remain. Both Temperature and Top-p change the randomness of the output. So, if we change both at the same time, we will not know which one caused the change.

Now, we must have understood how Temperature controls LLM output. It is just one small division before the lucky draw, but that one division decides whether the model gives us a safe answer or a creative one.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:
