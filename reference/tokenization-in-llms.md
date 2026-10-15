> Source: https://outcomeschool.com/blog/tokenization-in-llms

# Tokenization in LLMs
URL: https://outcomeschool.com/blog/tokenization-in-llms
Published: 2026-10-03
Author: Amit Shekhar

Tokenization in LLMs

# Tokenization in LLMs

Authors
: - Name
: Amit Shekhar
Published on
: October 3, 2026

Tokenization in LLMs is the process of breaking text into small pieces called tokens and then converting each token into a number that the model can work with.

In this blog, we will learn about Tokenization in LLMs, the very first step where a model breaks our text into small pieces before it can understand anything. We will also see why we need it, what a token is, the different ways to break text into tokens, how Byte Pair Encoding builds a vocabulary step by step, how tokens become numbers and back into text, and where it works well and where it fails.

We will cover the following:

- What is Tokenization?
- Why do we need Tokenization?
- What is a Token?
- Approach 1: Character-level Tokenization
- Approach 2: Word-level Tokenization
- Approach 3: Subword-level Tokenization
- How does Byte Pair Encoding (BPE) work?
- Vocabulary and Token IDs
- Decoding: From Tokens back to Text
- Tokenization in action with code
- Special Tokens
- How Tokenization affects LLMs in practice
- Where it works well and where it fails

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Tokenization?

Tokenization is the process of breaking a piece of text into small pieces called tokens and then converting each token into a number.

Let's say we type the sentence "I love learning" into an LLM (Large Language Model).

We see the sentence as three words. But the model does not see it the way we see it. The model does not understand letters or words. It only understands numbers.

So, before anything else happens, the sentence is broken into small pieces like below:

```
"I" | " love" | " learning"

```

Then, each piece is converted into a number like below:

```
40 | 3021 | 6975

```

These numbers are what the model actually receives. The text never reaches the model. Only the numbers do.

Note: These numbers are just for the sake of understanding. The actual numbers depend on which tokenizer we use.

The program that does this job is called a tokenizer. Every LLM has its own tokenizer.

## Why do we need Tokenization?

An LLM is a machine learning model. At its core, it does a lot of mathematics. It multiplies numbers, adds numbers, and compares numbers. Mathematics works on numbers, not on letters.

So, we have a problem. We have text, and the model needs numbers.

We need something that converts text into numbers. So, here comes the tokenizer into the picture.

But, the tokenizer has one more job. The model must have a fixed list of pieces it knows. When the model generates a reply, it picks one piece at a time from that fixed list. If the list is too big, the model becomes slow and heavy. If the list is too small, every sentence becomes a very long chain of tiny pieces.

So, the real question is: what is the right size of each piece?

We will see three approaches, one by one, and understand why the third one is used in modern LLMs.

## What is a Token?

A token is the smallest unit of text that the model works with.

A token can be a whole word, a part of a word, a single character, a punctuation mark, or a word along with the space before it.

Let's see a few examples:

- "cat" is one token.
- "unbelievable" becomes three tokens: "un", "believ", "able".
- "!" is one token.
- " love" (with the space before it) is one token.

Here, we can notice that the space is attached to the word. This is how most modern tokenizers work. The space becomes part of the token that comes after it. This way, the model knows where a new word begins.

A simple rule of thumb for English: one token is roughly 4 characters, or about three-fourths of a word. So, 100 tokens is around 75 words.

Now, let's see the different ways to break text into tokens.

## Approach 1: Character-level Tokenization

The simplest idea is to make every character a token.

Let's take the word "learning". The tokens will be as below:

```
"l" | "e" | "a" | "r" | "n" | "i" | "n" | "g"

```

Here, we have 8 tokens for one word.

Advantage: The list of known pieces is very small. For English, it is just the letters, the digits, and a few punctuation marks. And, the model can never face a word it does not know, because every word is made of characters.

Disadvantage: Every sentence becomes very long. A short paragraph of 100 words becomes around 500 tokens. The model has to process each one of them. And, each character carries very less meaning on its own. The letter "l" alone tells us nothing. The model has to work very hard to learn that "l", "e", "a", "r", "n" together means learn.

The issue with this approach is that the sequences become very long and each token carries very less meaning. Let's see how the next approach solve this issue.

## Approach 2: Word-level Tokenization

The next idea is to make every word a token. We simply split the text at spaces.

Let's take the sentence "I love learning". The tokens will be as below:

```
"I" | "love" | "learning"

```

Here, we have 3 tokens for three words.

Advantage: Each token carries full meaning. The sequences are short.

Disadvantage: The list of known words becomes huge. English alone has hundreds of thousands of words. Add names of people, names of places, other languages, code, and new words that appear every day. The list never ends.

What happens when the model sees a word that is not in the list?

Let's say the list does not have the word "tokenization". The tokenizer has no choice. It replaces the word with a special token called unknown, usually written as ` `. The model sees ` ` and has no idea what we said.

One more thing to notice. The words "learn", "learning", "learned", and "learner" are all separate tokens in this approach. The model does not know that they are related. It has to learn each one from scratch.

The issue with this approach is the huge list of words and the unknown word problem. Let's see how the next approach solve this issue.

## Approach 3: Subword-level Tokenization

Now, we take the middle path.

The idea is simple. Common words stay as one token. Rare words get broken into smaller pieces that are common.

Let's see with an example:

- "the" is very common, so it stays as one token: "the"
- "learning" is common, so it stays as one token: "learning"
- "tokenization" is rare, so it breaks into two: "token", "ization"
- "unbelievable" is rare, so it breaks into three: "un", "believ", "able"

Here, we can see that the pieces are meaningful. "token" is a real piece. "ization" is a real piece. Means, the model can learn that "ization" usually means the act of doing something, and reuse that learning for "organization", "civilization", and many more. Hence, the model learns faster.

Advantage: The list of known pieces is manageable, usually between 50,000 and 200,000. There is no unknown word problem, because any rare word can be broken down until we reach pieces we know, in the worst case single characters. And, related words share pieces, so the model does not have to learn each one from scratch.

Disadvantage: Sometimes a word breaks at a place that does not look natural to us.

This is what almost every modern LLM uses.

Let me tabulate the differences between the three approaches for your better understanding.

| | Character-level | Word-level | Subword-level |
| --- | --- | --- | --- |
| Size of the known list | Very small | Very large | Medium |
| Tokens per sentence | Very many | Few | Few |
| Unknown word problem | Never | Often | Never |
| Meaning per token | Very less | Full | Good |
| Used in modern LLMs | No | No | Yes |

Now, the question is, how does the tokenizer decide which pieces are common and which are rare? Who makes that list?

So, here comes the Byte Pair Encoding to the rescue.

## How does Byte Pair Encoding (BPE) work?

Byte Pair Encoding, or BPE, is an algorithm that builds the list of tokens by starting from single characters and repeatedly merging the pair of pieces that appears together most often.

In simple words, BPE looks at a huge amount of text, finds two pieces that sit next to each other most often, glues them into one new piece, and repeats.

The best way to learn this is by taking an example.

Let's say our training text has only three words, appearing with the following counts:

- "hug" appears 10 times
- "pug" appears 5 times
- "hugs" appears 5 times

Step 0: Split every word into characters.

```
h u g      (10 times)
p u g      (5 times)
h u g s    (5 times)

```

Our starting list of tokens: `h`, `u`, `g`, `p`, `s`. That is 5 tokens.

Step 1: Count every pair. A pair means two pieces that sit next to each other inside a word.

- "h" + "u" appears 10 + 5 = 15 times
- "u" + "g" appears 10 + 5 + 5 = 20 times
- "p" + "u" appears 5 times
- "g" + "s" appears 5 times

The most frequent pair is "u" + "g" with 20. So, we merge them into a new token `ug`.

Our list of tokens: `h`, `u`, `g`, `p`, `s`, `ug`. That is 6 tokens.

Our words now look like below:

```
h ug       (10 times)
p ug       (5 times)
h ug s     (5 times)

```

Step 2: Count the pairs again.

- "h" + "ug" appears 10 + 5 = 15 times
- "p" + "ug" appears 5 times
- "ug" + "s" appears 5 times

The most frequent pair is "h" + "ug" with 15. So, we merge them into a new token `hug`.

Our list of tokens: `h`, `u`, `g`, `p`, `s`, `ug`, `hug`. That is 7 tokens.

Our words now look like below:

```
hug        (10 times)
p ug       (5 times)
hug s      (5 times)

```

Step 3: Count the pairs again.

- "p" + "ug" appears 5 times
- "hug" + "s" appears 5 times

Both are equal. In such a case, the tokenizer follows a fixed rule to pick one. Let's merge "p" + "ug" into `pug`.

Our list of tokens: `h`, `u`, `g`, `p`, `s`, `ug`, `hug`, `pug`. That is 8 tokens.

We keep doing this until our list reaches the size we want. In real tokenizers, that size is decided beforehand, for example 100,000 tokens.

Here, we have done three merges. Every merge is saved as a rule, in order:

```
Rule 1: u + g  -> ug
Rule 2: h + ug -> hug
Rule 3: p + ug -> pug

```

Now, when a new piece of text comes in, the tokenizer does not count anything. It simply splits the text into characters and applies these rules in the same order.

Let's say the new text is "pugs". The tokenizer works as below:

- Start: `p`, `u`, `g`, `s`
- Apply Rule 1: `p`, `ug`, `s`
- Apply Rule 2: nothing to merge, because "h" + "ug" is not here
- Apply Rule 3: `pug`, `s`
- Final tokens: `pug`, `s`

And, the word "pugs" never appeared in our training text. Still, we got meaningful tokens.

Note: In many modern tokenizers, like the ones used by GPT models, the starting list is not the letters. It is all 256 possible byte values. Every character in every language, every emoji, and every symbol is stored as bytes. So, the tokenizer can never face something unknown. This variant is called byte-level BPE.

One more thing to notice. The tokenizer is trained separately, before the LLM is trained. Once the list of tokens is ready, it is frozen. The LLM is then trained using that frozen list. The LLM never changes the tokenizer.

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

## Vocabulary and Token IDs

The vocabulary is the complete list of all tokens that the tokenizer knows.

Each token in the vocabulary gets a unique number. This number is called the Token ID.

Think of it as a dictionary where every entry has a serial number. The tokenizer looks up the piece, finds the serial number, and hands over the number to the model.

For our small example, the vocabulary looks like below:

| Token | Token ID |
| --- | --- |
| h | 0 |
| u | 1 |
| g | 2 |
| p | 3 |
| s | 4 |
| ug | 5 |
| hug | 6 |
| pug | 7 |

So, the text "pugs" becomes tokens `pug`, `s`, and then Token IDs `7`, `4`.

This is the complete journey:

```
Text   -> Tokens        -> Token IDs
"pugs" -> ["pug", "s"]  -> [7, 4]

```

Here, `[7, 4]` is what goes into the LLM.

Now, why does the vocabulary size matter? When the LLM generates a reply, at every step it picks one token from this vocabulary. So, a vocabulary of 100,000 tokens means the model chooses from 100,000 options at every step. Bigger vocabulary means fewer tokens per sentence but a heavier model. Smaller vocabulary means a lighter model but longer sequences. Real models pick a size somewhere in between, based on their use case.

Note: Inside the model, each Token ID is used to look up a long list of numbers called an embedding. That is where the real understanding begins, and it is a topic for another blog. For now, we just need to know that Tokenization is the step that comes before it.

If we want to go deep into Tokenization, LLM Fundamentals, and LLM Internals, and build a Large Language Model (LLM) from scratch, check out our AI and Machine Learning Program at Outcome School.

## Decoding: From Tokens back to Text

Now, let's see how text comes out of the model.

The LLM does not produce text. It produces Token IDs, one at a time.

Let's say the model produces `6`, `4`. The tokenizer looks up the vocabulary in reverse:

- `6` is `hug`
- `4` is `s`

Then, it joins them: "hugs".

This reverse step is called decoding. It is the exact opposite of what we did earlier.

```
Token IDs -> Tokens        -> Text
[6, 4]    -> ["hug", "s"]  -> "hugs"

```

This is why, when we watch an LLM type its answer on the screen, sometimes we see half a word appear first and then the rest. That is a token boundary. The model produced one token, the tokenizer decoded it, and it was shown to us.

## Tokenization in action with code

Let's see the whole thing in action. We will use `tiktoken`, which is OpenAI's library that contains the tokenizers used by OpenAI models.

```python
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

token_ids = encoding.encode("I love learning")
print(token_ids)

text = encoding.decode(token_ids)
print(text)

```

It will print something like the following:

```
[40, 3021, 6975]
I love learning

```

Here, we have used `cl100k_base`, which is the name of one tokenizer with around 100,000 tokens in its vocabulary. The `encode` function converts our text into Token IDs. The `decode` function converts the Token IDs back into text. We got the exact same sentence back.

Now, let's see which piece of text each Token ID stands for.

```python
for token_id in token_ids:
    print(token_id, "->", "[" + encoding.decode([token_id]) + "]")

```

It will print the following:

```
40 -> [I]
3021 -> [ love]
6975 -> [ learning]

```

Here, we can see that the space is attached to the word, exactly as we discussed earlier. " love" is one token and " learning" is one token.

Note: The exact Token IDs depend on the tokenizer. A different model with a different tokenizer will give different numbers for the same sentence.

## Special Tokens

Along with the tokens that come from text, the vocabulary has a few special tokens. These are not words. They are signals.

Few important ones:

- End of text: tells the model that the text has ended. Usually written as `<|endoftext|>` or ` `. When the model produces this token, it stops generating.
- Beginning of text: marks where the text starts. Usually written as ` `.
- Padding: a filler token used to make many inputs the same length when the model processes them together.
- Chat markers: tokens that mark where the user's message begins and ends, and where the assistant's reply begins. This is how a chat model knows who said what.

Here, we can notice that a special token is never produced by breaking normal text. It is added on purpose by the tokenizer or by the system around the model.

## How Tokenization affects LLMs in practice

Tokenization happens before the model, and the model can never look inside a token. This one fact explains many strange things that LLMs do.

Counting letters: Let's say we ask, how many times does the letter "r" appear in "strawberry"? The tokenizer breaks the word into something like "str", "aw", "berry". The model sees three Token IDs. It never sees the individual letters. So, it has to guess from memory how many "r" are inside those pieces. This is why LLMs sometimes get such questions wrong.

Math on numbers: The number "12345" is split into pieces like "123" and "45". The model does not see five digits. It sees two tokens. Doing addition on such pieces is much harder than doing it digit by digit.

Cost and limits: Every LLM has a limit on how many tokens it can read at once. This is called the context window. And, the pricing of an LLM is also per token. So, the number of tokens decides both what fits and what it costs.

Other languages: Most tokenizers are trained on text that is mostly English. So, English words get compact tokens. A sentence in Hindi, Tamil, or Japanese is broken into many more small pieces. The same sentence can take several times more tokens in these languages. This means it costs more and fills the context window faster.

Code: Spaces and indentation are tokens too. Four spaces of indentation can become one token or four tokens depending on the tokenizer. This affects how well a model reads and writes code.

## Where it works well and where it fails

Let me summarize where subword tokenization works well:

- It handles any input without an unknown word problem.
- It keeps sequences short for common text.
- It shares meaningful pieces across related words, so the model learns faster.
- It works for text, code, and many languages with one single vocabulary.

And where it fails:

- Tasks that need to see individual letters, like counting letters or reversing a word.
- Math on long numbers, because digits get grouped in unnatural ways.
- Languages that were less present in the training text, because they get more tokens, which means higher cost and less room in the context window.
- Any word broken at a strange place can confuse the model, because the pieces do not carry the meaning we expect.

Now we must have understood what Tokenization in LLMs is, how BPE builds the vocabulary, how text becomes Token IDs and back, and where it works well and where it fails.

### Do all LLMs use the same tokenizer?

No. Every LLM has its own tokenizer. A different model with a different tokenizer will give different Token IDs for the same sentence. So, the exact numbers we get always depend on which tokenizer we use.

### Does the LLM change its tokenizer during training?

No. The tokenizer is trained separately, before the LLM is trained. Once the list of tokens is ready, it is frozen, and the LLM is then trained using that frozen list. The LLM never changes the tokenizer.

### How many words are 100 tokens?

For English, 100 tokens is around 75 words. A simple rule of thumb is that one token is roughly 4 characters, or about three-fourths of a word.

### Why do LLMs struggle to count letters in a word?

Because the model never sees the individual letters. A word like "strawberry" is broken into pieces like "str", "aw", "berry", and the model sees only their Token IDs. So, it has to guess from memory how many times a letter appears inside those pieces.

### Why does text in Hindi or Japanese use more tokens than English?

Most tokenizers are trained on text that is mostly English, so English words get compact tokens. A sentence in Hindi, Tamil, or Japanese is broken into many more small pieces. This means it costs more and fills the context window faster.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
