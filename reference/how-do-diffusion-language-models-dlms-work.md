> Source: https://outcomeschool.com/blog/how-do-diffusion-language-models-dlms-work

# How do Diffusion Language Models (DLMs) work?
URL: https://outcomeschool.com/blog/how-do-diffusion-language-models-dlms-work
Published: 2026-06-22

How do Diffusion Language Models (DLMs) work?

# How do Diffusion Language Models (DLMs) work?

Authors
: - Name
: Amit Shekhar
Published on
: June 22, 2026

In this blog, we will learn about Diffusion Language Models (DLMs), a new way to make models write text. They promise to generate words in a different way than the LLMs we use today, and that too much faster in many cases.

We will cover the following:

- What is a Diffusion Language Model?
- How do today's language models write text?
- The problem with the usual approach
- Where the diffusion idea comes from
- What does "noise" mean for text?
- The two phases: forward and reverse
- How a DLM actually generates text, step by step
- A tiny end-to-end example
- A simple code-style walk-through
- DLMs vs the usual language models
- Advantages of DLMs
- Limitations of DLMs
- The current state

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a Diffusion Language Model?

A Diffusion Language Model is a type of AI model that writes text by starting from a piece of pure gibberish and slowly cleaning it up into a clear, meaningful sentence.

In simple words, it does not write a sentence one word at a time from left to right. Instead, it starts with a rough, messy version of the whole sentence and then refines it again and again until it becomes correct.

Let's understand the term: Diffusion

Diffusion is a word borrowed from nature. It means something spreading out and mixing, like a drop of ink slowly spreading into a glass of water until everything is blurry.

So, a Diffusion Language Model is a model that learns to take blurry, mixed-up text and turn it back into clean text.

Do not worry, we will learn about each part in detail.

### How do today's language models write text?

Before jumping into diffusion, we must understand how the popular LLMs today write text. This will help us see why diffusion is interesting.

LLMs are built on an architecture called the Transformer, which is just a powerful kind of AI brain that is very good at understanding language. These models write in a style called autoregressive generation.

Let's decompose that word:

> Autoregressive = Auto + Regressive

In simple words, it means the model predicts the next word based on all the words that came before it. It writes one word, looks at everything written so far, then writes the next word, and keeps going.

Let's say we ask the model to complete this sentence: "The sky is".

The model writes one word at a time, like below:

```
Step 1:  The sky is ___            ->  picks "blue"
Step 2:  The sky is blue ___       ->  picks "and"
Step 3:  The sky is blue and ___   ->  picks "clear"

```

Here, we can see that the model adds one word in each step. It can never pick the third word before it has picked the second word. Each word waits for the one before it.

This is how today's language models write text. It works very well, and that is why it feel so natural.

If we want to understand how language models like this work under the hood, we build a Large Language Model (LLM) from scratch in our AI and Machine Learning Program at Outcome School.

### The problem with the usual approach

Now, the question is: if this works so well, why do we need anything new?

The issue with this approach is speed. Because the model writes strictly one word after another, it cannot do them at the same time. If a sentence has 100 words, the model must take 100 turns, one after another. It cannot jump ahead.

Let's say we are writing a long essay. Writing one word, waiting, then the next word, waiting, then the next, is slow. We are stuck in a single line, moving forward one step at a time. We cannot go back and fix an earlier word either, because we have already moved past it.

Now, the next big question is: what if a model could work on the whole sentence at once, fixing many words together instead of one at a time?

So, here comes the Diffusion Language Model to the rescue.

### Where the diffusion idea comes from

Before jumping into text, we must know where this idea was born.

The diffusion idea first became famous for creating images. Tools that turn a text prompt into a beautiful picture often use a method called diffusion.

Here is the simple idea behind image diffusion. We take a clear photo and slowly add random dots of noise to it, again and again, until the photo becomes complete static, like an old TV with no signal. Then we train a model to do the reverse: start from pure static and slowly remove the noise until a clear picture appears.

We can picture it like below:

```
Clear image  ->  add noise  ->  more noise  ->  pure static
                                                     |
                                                     v  (now reverse it)
Clear image  <-  remove noise  <-  less noise  <-  pure static

```

Here, we can see that the model learns to walk backward, from total mess to a clean image, one small cleanup step at a time.

Now, the next big question is: can we do the same thing for text instead of images? The answer is yes, and that is exactly what a Diffusion Language Model does.

### What does "noise" mean for text?

For an image, adding noise was easy. We just add random dots to the pixels.

But text is different. A sentence is made of words, not pixels. We cannot add a "half word". So we need a different idea of noise for text.

For text, noise means hiding or replacing words with a blank or a random word.

In simple words, to make a clean sentence noisy, we hide some of its words. The more words we hide, the noisier the sentence becomes. When every word is hidden, the sentence is pure noise. This is just like the ink drop spreading in water until everything is blurry.

Let's say our clean sentence is "The cat sat on the mat". We use the symbol `[?]` for a hidden word. Adding more and more noise looks like below:

```
Clean:        The cat sat on the mat
A little noise: The cat [?] on the mat
More noise:     The [?] [?] on [?] mat
Pure noise:     [?] [?] [?] [?] [?] [?]

```

Here, we can see that as we add more noise, more words turn into `[?]`. At the end, the whole sentence is just blanks. This blank-filled sentence is the text version of "pure static".

This way of hiding words is called masking, and the hidden spot is called a mask. So, for text, adding noise simply means masking more words.

This is how we bring the idea of noise into the world of text. It makes our life easy, because hiding words is something a computer can do instantly.

### The two phases: forward and reverse

A Diffusion Language Model works in two phases. Let's understand each one.

The forward phase (adding noise): This is the easy part, and it happens only during training. We take a clean sentence from our training data and slowly hide its words until the whole sentence is masked. We do not need any intelligence for this. We are just deleting words on purpose.

The reverse phase (removing noise): This is the hard part, and this is what the model actually learns. The model takes a masked sentence and tries to guess the hidden words to make it clean again. It does this again and again, filling in more words each time.

We can picture both phases like below:

```
FORWARD (training only, just hide words)
The cat sat on the mat  ->  The [?] sat on [?] mat  ->  [?] [?] [?] [?] [?] [?]

REVERSE (what the model learns to do)
[?] [?] [?] [?] [?] [?]  ->  The [?] sat on [?] mat  ->  The cat sat on the mat

```

Here, we can see that the forward phase destroys the sentence and the reverse phase rebuilds it. The model only needs to become very good at the reverse phase. The forward phase is just a teacher creating practice questions.

So, during training, we hide words and ask the model to guess them. By practicing on millions of sentences, the model gets very good at filling in blanks. This is how it learns. It is just like a student who keeps solving fill-in-the-blanks exercises until the answers come naturally.

### How a DLM actually generates text, step by step

Now comes the most interesting part. Till now, we have learned how the model is trained. Now it's time to learn how it writes a brand new sentence for us.

It starts with a sentence that is all blanks and refines it step by step. Let's understand the full process.

Step 1: Start from pure noise. The model begins with a sentence where every word is masked. It is a blank canvas of `[?]` symbols.

Step 2: Guess all the words at once. Here is the beauty of it. Unlike the usual models, the DLM looks at every blank at the same time and makes a guess for each one in a single pass. It does not go left to right. It works on the whole sentence together.

Step 3: Keep the confident words, blank out the rest. Some guesses will be good and some will be shaky. The model keeps the words it is most confident about and turns the unsure ones back into `[?]`. This is the key trick that makes the result better over time. Do not worry, we will see this with a clear example soon.

Step 4: Repeat. The model looks at the partly-filled sentence and guesses the remaining blanks again, now with more context to help it. It keeps the confident ones and blanks the rest.

Step 5: Stop when nothing is masked. After a few rounds, there are no blanks left. The sentence is complete.

We can picture the whole generation like below:

```
Round 1:  [?]  [?]  [?]  [?]  [?]      (start, all masked)
            |    |    |    |    |
            v    v    v    v    v       (guess all at once, keep the confident ones)
Round 2:  The  [?]  [?]   is  [?]
            |    |    |    |    |
            v    v    v    v    v       (guess the rest again)
Round 3:  The  food [?]   is good
            |    |    |    |    |
            v    v    v    v    v
Round 4:  The  food here  is good       (done, no blanks left)

```

Here, we can see that the model fills in the easy, confident words first, like "The" and "is". Then it uses those words as hints to fill in the harder words like "food", "here", and "good". Step by step, the messy blank sentence becomes a clean, meaningful one.

This is how a Diffusion Language Model generates text. The big difference is that it can fix many words in parallel, instead of one at a time. It enables us to do complex things very simply.

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

### A tiny end-to-end example

The best way to learn this is by taking an example. Let's say we ask the model to answer: "What is the capital of France?"

The model needs to produce a short answer of, let's say, 4 word-slots. It starts with all of them masked.

```
Question: What is the capital of France?
Answer slots:  [?]  [?]  [?]  [?]

```

Round 1: The model guesses every slot at once. Suppose it produces:

```
The   is   capital   Paris

```

The model is very confident about "Paris" and fairly confident about "The". It is unsure about "is" and "capital" in those spots. So it keeps the confident words and blanks the rest.

```
The   [?]   [?]   Paris

```

Round 2: Now the model looks at "The [?] [?] Paris" and guesses the two blanks again. With "The" and "Paris" already in place, the context is clearer. This time it produces:

```
The   capital   is   Paris

```

Here, we can see that the answer is now correct and complete. The model used the words it was sure about as anchors to figure out the rest.

So, in just two rounds, the model went from total blanks to a correct answer. This way we can use a Diffusion Language Model to write text by refining the whole sentence together.

### A simple code-style walk-through

Now, let's see this idea in a small, simplified code-style form using Python. This is just for the sake of understanding, not a real library. We can write it as below:

```python
# A simplified view of how a DLM generates text

sentence = ["[?]", "[?]", "[?]", "[?]"]   # start: everything masked

for current_round in range(num_rounds):
    # 1. Ask the model to guess EVERY position at once
    guesses, confidence = model.predict_all(sentence)

    # 2. Keep only the most confident guesses, mask the rest
    for i in range(len(sentence)):
        if confidence[i] > threshold:
            sentence[i] = guesses[i]      # lock in this word
        else:
            sentence[i] = "[?]"           # send it back to be re-guessed

    # 3. Stop early if no masks are left
    if "[?]" not in sentence:
        break

print(sentence)   # the final clean sentence

```

Here, we have written the core loop of a Diffusion Language Model. Let me explain each part.

- `sentence` starts as a list full of `[?]`, which means every position is masked.
- `model.predict_all(sentence)` is the key step. The model guesses all positions at the same time and also tells us how confident it is about each guess.
- The `if confidence[i] > threshold` check keeps the words the model is sure about and sends the unsure ones back to `[?]` to be guessed again next round. Here, `threshold` is just a confidence bar we set, for example "only keep words the model is more than 90 percent sure about".
- The loop repeats, and each round the sentence gets cleaner.
- When there are no `[?]` left, we stop, and the sentence is ready.

Notice that there is no left-to-right loop here. The model works on the whole sentence in every round. This is the heart of the difference. Here, we can see that many words can be decided together.

### DLMs vs the usual language models

Now that we have learned how a DLM works, it's time to compare it with the usual autoregressive models we discussed earlier.

The usual model is a decoder-only Transformer that writes left to right, one word at a time. The diffusion model fills the whole sentence and refines it over a few rounds. We can picture the contrast like below:

```
Autoregressive (usual):                 Diffusion (DLM):

word1                                    [?] [?] [?] [?] [?]   (all at once)
word1 word2                                    |
word1 word2 word3                              v
word1 word2 word3 word4                  the [?] cat on mat   (refine)
... one new word each step                     |
                                               v
                                         the big cat on mat   (refine again)

one direction, one word per step         whole sentence, refined over rounds

```

Here, we can see the core difference. The usual model takes as many steps as there are words. The diffusion model takes a small number of refinement rounds that does not grow with every extra word, and it works on many words together in each round.

Let me tabulate the differences between Autoregressive Models and Diffusion Language Models for your better understanding.

| Feature | Autoregressive Model | Diffusion Language Model |
| --- | --- | --- |
| Writing order | Left to right, one word at a time | Whole sentence at once, refined in rounds |
| Parallel work | No, each word waits for the previous | Yes, many words decided together |
| Number of steps | Equal to the number of words | A small number of rounds, not tied to the word count |
| Can revise earlier words | No, once written it stays | Yes, it can re-mask and fix words |

One important thing to clear up: Diffusion Language Models (DLMs) often use a Transformer-based architecture internally, similar to the large language models. The difference is not the brain, it is the way the text is written. The usual model writes one word at a time, and the diffusion model fills and refines the whole sentence together.

We have a complete program on this - in our AI and Machine Learning Program at Outcome School, we cover Autoregressive Models, Diffusion Models, and the rest of generative AI in depth.

### Advantages of DLMs

- Speed through parallel work: Because the model decides many words together, it can produce text in far fewer steps than writing one word at a time. This can make generation much faster.
- It can fix its own mistakes: A word that was placed early can be sent back to `[?]` and corrected in a later round. The usual model cannot undo a word once it is written.
- Whole-sentence view: The model sees the entire sentence in every round, so a word near the end can influence a word near the start. This global view can help with consistency.
- Good control over the output: Since the model fills in blanks, it is naturally suited to tasks where we give a partial sentence and ask it to complete the missing parts.

### Limitations of DLMs

- Choosing how many rounds is tricky: Too few rounds give messy text, and too many rounds slow things down. Finding the right balance takes care.
- Fixed length can be awkward: Many DLM setups need to know how many word-slots to fill ahead of time. The usual models can simply keep writing until they decide to stop, which feels more natural for open-ended writing.
- Less mature tooling: The usual autoregressive models have years of tuning, tools, and tricks behind them. DLMs are catching up but are still younger.
- Quality is still being proven: For some tasks, the very best autoregressive models are still ahead on quality, though the gap keeps shrinking.

So, DLMs are a promising direction, but they are still an active area of research.

### The current state

Now, let's discuss where things stand today, in 2026.

Diffusion for text started as a research idea, but it has moved quickly into real, working models. Researchers have built large diffusion-based language models that can chat, answer questions, and write code, and some of them run noticeably faster than the usual word-by-word models because of the parallel refinement.

A few important points about the current state:

- Several real diffusion-style language models are now in use, and the main selling point is high speed. Their speed is measured in tokens per second, where a token is a small chunk of a word. For example, Mercury from Inception Labs can generate over a thousand tokens per second on a single chip, which is several times faster than the usual word-by-word models. Google has released DiffusionGemma, an open model that anyone can download and run, and it reaches a similar speed on a single chip. LLaDA is another popular open model that anyone can download and run.
- Newer diffusion models can also reason. They no longer just write fast, they can solve hard math and coding problems too, which earlier diffusion models struggled with.
- Many practical systems are hybrids. They borrow the strong Transformer brain from the usual models and add the diffusion-style refinement on top, so they get the best of both worlds. A common trick is to start from a normal trained model and then continue training it with the diffusion idea, instead of starting from scratch.

So, now we know where Diffusion Language Models fit and how they work.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
