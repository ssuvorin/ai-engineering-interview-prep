> Source: https://x.com/amitiitbhu/status/1927927814923207146

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
