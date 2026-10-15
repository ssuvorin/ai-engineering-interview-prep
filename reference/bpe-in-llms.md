> Source: https://outcomeschool.com/blog/bpe-in-llms

# What is Byte Pair Encoding (BPE) in LLMs?

BPE (Byte Pair Encoding) is the tokenization algorithm used by most modern Large Language Models (LLMs). It starts with single characters and keeps merging the most frequent pair of pieces until it builds a vocabulary of common subwords.

## What is Tokenization?

Tokenization is the process of breaking text into small pieces called tokens, each converted into a number. The model processes multiple tokens at a time.

## The Problem: How to Break Text into Tokens?

Approach 1: Word-Level Tokenization

Treat each word as one token. The model needs to know every word in the language, including new words. An unseen word like "ChatGPT" becomes a single "unknown" token and loses all meaning.

Approach 2: Character-Level Tokenization

Treat each character as one token. No word is ever "unknown", but tokens are too small. A 10-word sentence can become 50+ tokens, making training slow and harder for the model to understand meaning.

We needed a solution giving the best of both worlds.

## What is BPE (Byte Pair Encoding)?

BPE is a tokenization algorithm that breaks text into pieces between characters and words. It repeatedly finds the most common pair of adjacent tokens and merges them into one.

## How BPE Works: Step by Step

Example text:

```
low low low low low
lower lower
newest newest newest newest newest newest
widest widest widest
```

Word frequencies: "low" 5, "lower" 2, "newest" 6, "widest" 3.

Step 1: Start with Characters

Break every word into individual characters, adding an end-of-word symbol "_":

```
l o w _        (frequency: 5)
l o w e r _    (frequency: 2)
n e w e s t _  (frequency: 6)
w i d e s t _  (frequency: 3)
```

Initial vocabulary: {l, o, w, e, r, n, s, t, i, d, _}

Step 2: Find the Most Frequent Pair

- "e s" appears in "newest" (6) and "widest" (3) = 9 times
- "s t" appears in "newest" (6) and "widest" (3) = 9 times
- "t _" appears 9 times
- "l o" appears in "low" (5) and "lower" (2) = 7 times
- "o w" appears 7 times

The most frequent pair is "e s" with 9 occurrences. We merge into "es".

Step 3: Merge and Update

```
l o w _         (frequency: 5)
l o w e r _     (frequency: 2)
n e w es t _    (frequency: 6)
w i d es t _    (frequency: 3)
```

Vocabulary: {l, o, w, e, r, n, s, t, i, d, _, es}

Step 4: Repeat

Now "es t" appears 9 times. Merge into "est".

```
l o w _         (frequency: 5)
l o w e r _     (frequency: 2)
n e w est _     (frequency: 6)
w i d est _     (frequency: 3)
```

Vocabulary: {l, o, w, e, r, n, s, t, i, d, _, es, est}

Keep repeating. Next merges could be "est _" into "est_", then "l o" into "lo", then "lo w" into "low", and so on.

Step 5: Stop When Done

We keep merging until we reach a desired vocabulary size. Modern LLMs typically use between 32,000 and 256,000 tokens. For example, LLaMA 3 uses about 128K tokens, Gemma about 256K tokens.

The final vocabulary contains full common words, subwords like "ing" and "tion", and individual characters for rare combinations.

## How BPE Tokenizes New Text

Once BPE has finished training, it has a vocabulary and an ordered list of merge rules. When tokenizing new text, BPE replays the same merge rules in the same order they were learned during training.

Example: tokenizing "lowest"

Start: `l o w e s t`

Apply merge rule 1 ("e s" into "es"): `l o w es t`

Apply merge rule 2 ("es t" into "est"): `l o w est`

Apply merge rule 3 ("l o" into "lo"): `lo w est`

Apply merge rule 4 ("lo w" into "low"): `low est`

Result: "lowest" is tokenized as ["low", "est"].

Similarly "newer" eventually produces ["new", "er"].

Why does order matter? Different merge orders can produce different results. Replaying merge rules in the exact training order gives consistent tokenizations. BPE never encounters a completely unknown word - in the worst case it falls back to individual characters.

## Why BPE is Used in Modern LLMs

- Handles unknown words: any word can be broken into known subword pieces.
- Efficient vocabulary size: 32,000 to 256,000 tokens can represent any text.
- Balances meaning and efficiency: common words like "the" stay single tokens; rare words break into subwords.
- Works across languages: character-level, so it handles any language, script, and special characters.

Models use a variant of BPE, but the core idea remains the same.

### Is BPE better than word-level tokenization?

Yes. Word-level needs the model to know every word; unseen words become "unknown" tokens. BPE breaks them into known subword pieces instead.

### Why not just use character-level tokenization?

Character tokens are too small, making training slow and meaning hard to capture. BPE sits between characters and words.

### What vocabulary size do LLMs use with BPE?

Between 32,000 and 256,000 tokens. LLaMA 3 uses about 128K, Gemma about 256K.

### Does BPE use a greedy longest-match lookup to tokenize new text?

No. BPE replays the ordered list of merge rules in the training order. A greedy lookup could produce different tokenizations.

### Can BPE ever fail to tokenize a word?

No. In the worst case it falls back to individual characters.
