> Source: https://outcomeschool.com/blog/what-is-generative-ai

# What is Generative AI?
URL: https://outcomeschool.com/blog/what-is-generative-ai
Published: 2026-08-05

What is Generative AI?

# What is Generative AI?

Authors
: - Name
: Amit Shekhar
Published on
: August 5, 2026

Generative AI is a type of AI that can create new things, like text, images, audio, video, and code, that did not exist before.

In this blog, we will learn about Generative AI. We will understand what the word "generate" actually means, how Generative AI is different from the older AI, how it learns from a huge amount of examples, how it creates something completely new, where we use it every day, and the limitations we must know.

We will cover the following:

- What is Generative AI?
- Generative AI = Generative + AI
- What does "generate" mean here?
- How is Generative AI different from the old AI?
- How does Generative AI learn?
- How does Generative AI actually create something new?
- What can Generative AI create?
- What is a model in Generative AI?
- The complete flow of Generative AI
- Where do we use Generative AI every day?
- The limitations we must know
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Generative AI?

Generative AI is a type of artificial intelligence that can create new things, like text, images, audio, video, and code.

Let's say we ask a computer, "Write me a short poem about the rain." A few years back, a normal computer could not do this. It could search for a poem that someone else had already written, but it could not write a fresh new poem on its own.

Now, things have changed. Today, we can ask, and the computer writes a brand new poem in seconds. Nobody wrote that exact poem before. The computer created it for us right now.

That power to create something new is what we call Generative AI.

## Generative AI = Generative + AI

The best way to understand this term is to break it into two parts.

Generative: This word comes from "generate", which means to create or to produce something new.

AI: This is short for Artificial Intelligence. It means making a computer do tasks that normally need human intelligence, like understanding language, seeing pictures, or making decisions.

So, when we join both parts:

> Generative AI = An artificial intelligence that can create new content on its own.

In simple words, it can produce fresh text, images, sound, and more, just like a human creator would.

## What does "generate" mean here?

This is the most important word, so let's be very clear about it.

To generate means to create something that did not exist before.

Let's say we have a calculator. We type `2 + 2`, and it gives `4`. This is not generating. The calculator just follows a fixed rule. The answer is always the same, and it is not new.

Now, let's say we ask Generative AI to "draw a cat riding a bicycle on the moon." No such picture existed before. The AI creates that picture, pixel by pixel, just for us. This is generating.

So, the key idea is this. Generative AI does not copy and paste an old answer. It creates a new one.

## How is Generative AI different from the old AI?

Before Generative AI became popular, we already had AI. But that older AI mostly did one job. It looked at something and gave a label or a decision.

Let's understand this with an example. The old AI was very good at answering questions like these:

- Is this email spam or not spam?
- Is there a cat in this photo or not?
- Is this review positive or negative?

Here, we can notice one thing. The old AI only chooses from options that already exist. It does not create anything new. We can call this kind of AI "the AI that decides."

Generative AI is different. It does not just decide. It creates. We can call it "the AI that creates."

Let me tabulate the difference between the two for your better understanding so that the whole picture becomes clear.

| Old AI (the AI that decides) | Generative AI (the AI that creates) |
| --- | --- |
| Looks at input and picks a label | Looks at input and produces new content |
| "Is this a cat or a dog?" | "Draw me a new cat." |
| Chooses from fixed options | Creates something that did not exist before |
| Output is a decision | Output is fresh text, image, audio, or video |

We can also picture this difference like below:

```
   Old AI (decides)                    Generative AI (creates)

   Photo of an animal                  Text: "a cat on the moon"
        |                                     |
        v                                     v
   +-----------+                        +-----------+
   |    AI     |                        |    AI     |
   +-----------+                        +-----------+
        |                                     |
        v                                     v
   "It is a cat"                        A brand new picture
   (a label)                            of a cat on the moon

```

Here, we can see the clear difference. On the left, the AI only puts a label. On the right, the AI creates a whole new picture.

Both kinds are built on Machine Learning, and we have a detailed blog on What is Machine Learning? that explains how a machine learns from data in the first place.

Now that we know what Generative AI does, the next question is: how does it learn to do this? Let's understand it.

## How does Generative AI learn?

Generative AI learns by looking at a huge amount of examples. This is the heart of everything, so let's go slowly.

Let's say we want to teach a child to write stories. We would let the child read thousands of storybooks. After reading so many stories, the child starts to understand how a story works. The child learns which words go together, how a sentence flows, and how a story begins and ends.

Generative AI learns in the same way. We show it a massive amount of examples. For a text AI, we show it a large part of the writing available on the internet, like books, articles, and websites. It reads all of this during a stage that we call training.

During training, the AI is not memorizing the text word for word. Instead, it is learning the patterns. It learns which words usually come after which words. It learns how ideas connect. It learns the style and the structure of language.

So, after training, the AI has learned the deep patterns of language. Now, it can use these patterns to create new sentences on its own.

Note: The same idea works for images. To create images, the AI is trained on a huge collection of pictures along with their descriptions. It learns what a "cat", a "bicycle", and the "moon" look like. Later, it can mix these learned patterns to draw a cat riding a bicycle on the moon, even though it never saw that exact picture before.

If we want to go deep into how this learning actually happens - Machine Learning fundamentals, Supervised and Unsupervised Learning, Neural Networks, and Backpropagation - check out our AI and Machine Learning Program at Outcome School.

## How does Generative AI actually create something new?

Now, this is the most magical part. Let's understand how a text Generative AI writes a sentence.

The secret is surprisingly simple. The AI predicts the next word, again and again. Inside the model, this writing job is done by the Decoder.

Let's say we give it the starting words, "The sky is". The AI now thinks, "What word usually comes next?" From all its training, it knows that "blue" is a very likely next word. So, it adds "blue".

Now the sentence is "The sky is blue". The AI again asks, "What comes next?" Now it adds "and". Then it asks again, and adds "clear". It keeps doing this, one word at a time, until the sentence is complete.

We can picture this step by step like below:

```
   Step 1:  "The sky is"          ->  predict next word  ->  "blue"
   Step 2:  "The sky is blue"     ->  predict next word  ->  "and"
   Step 3:  "The sky is blue and" ->  predict next word  ->  "clear"
   Step 4:  "The sky is blue and clear"  ->  and so on...

```

Here, we can see the beautiful trick. The AI never writes a whole paragraph in one shot. It writes one word, then looks at everything so far, then writes the next word. It repeats this until the full answer is ready.

So, a long and smart answer is really just the AI predicting the next word, over and over, very fast. And whether it plays safe with "blue" or takes a chance on a surprising word is controlled by a knob called Temperature, along with two more settings called Top-k and Top-p.

This way of creating, one word at a time, is called autoregressive generation, and we have a detailed blog on Autoregressive Models that explains it step by step.

This is how Generative AI creates new text. It creates images, audio, and video in a similar spirit, by using the patterns it learned during training, just with different methods for each type of content.

## What can Generative AI create?

Generative AI is not limited to text. It can create many kinds of content. Let's see a few.

- Text: It can write emails, stories, articles, answers, and summaries.
- Images: It can create paintings, photos, logos, and art from a simple description.
- Audio: It can create music, and it can create a human-like voice that reads text aloud.
- Video: It can create short video clips from a text description.
- Code: It can write computer programs and help developers build software.

So, whatever kind of content a human can create, Generative AI is learning to create it too.

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

## What is a model in Generative AI?

We keep saying "the AI", but let's give it a proper name. The trained brain of Generative AI is called a model.

A model is the final result of all that training. Think of it as a brain that has already read a huge amount of data and has learned the patterns inside it. When we chat with a Generative AI tool, we are really talking to this trained model.

When a model works mainly with text and language, we call it a Large Language Model, or LLM for short.

- Large: It has learned from a very large amount of text, and it has a very large number of internal settings that store what it learned.
- Language: Its main job is to understand and create human language.
- Model: It is the trained brain that holds all this learned knowledge.

So, when we hear names like the models behind ChatGPT, Claude, or Gemini, these are all Large Language Models. They are the trained brains that power the Generative AI tools we use.

## The complete flow of Generative AI

Now that we have learned about all the parts, let's put the whole flow together in simple steps.

- First, we collect a huge amount of examples, like text or images. This is the data.
- Then, the AI reads all this data and learns the patterns inside it. This is training.
- After that, the trained brain is ready. We call this brain the model.
- Then, we give the model a request in plain words. This request is called a prompt.
- Finally, the model uses its learned patterns to create a brand new answer for us.

We can picture the whole flow like below:

```
   Huge amount of data (text, images, code)
              |
              |  the AI reads and learns the patterns
              v
          Training
              |
              v
        Trained model  (the brain that has learned)
              |
              |  we give a prompt: "Write a poem about rain"
              v
        New content  (a fresh poem, created just now)

```

Here, we can see the full journey. First, the model learns from data. Then, we give it a prompt. Finally, it creates something new for us.

## Where do we use Generative AI every day?

Let's see a few common places.

- Chat assistants: We ask a question in plain English and get a helpful answer.
- Writing help: It helps us write emails, fix our grammar, and summarize long text.
- Image creation: We type a description, and it draws a picture for us.
- Coding help: It helps developers write and fix code faster.
- Customer support: Many company chatbots now use Generative AI to answer our questions.

It is helping millions of people every single day.

## The limitations we must know

Generative AI is powerful, but it is not perfect. We must understand its limits so that we use it wisely.

- It can be wrong. The AI predicts what sounds right, but sometimes it makes up facts that are not true. This is called a hallucination. So, we must always check important information.
- It does not truly understand. It is very good at patterns, but it does not "know" things the way a human does. It has no real feelings or life experience.
- It learns from human data. Since it learns from what humans wrote, it can also pick up the mistakes and biases present in that data.
- It needs a good prompt. The quality of the answer depends a lot on how clearly we ask. A clear prompt gives a better result.

So, Generative AI is a very helpful tool, but we must use it as a smart helper, not as a source of final truth.

## Summary

Let's quickly recap what we have learned.

- Generative AI is a type of AI that creates new content, like text, images, audio, video, and code.
- The word "generate" means to create something that did not exist before.
- The old AI mostly decided or labeled things. Generative AI creates new things.
- It learns by reading a huge amount of examples and understanding the patterns inside them.
- A text Generative AI creates a sentence by predicting the next word, again and again.
- The trained brain is called a model, and a text model is called a Large Language Model.
- It is powerful, but it can be wrong, so we must always check important facts.

This is how Generative AI works. It reads a huge amount of data, learns the patterns, and then uses those patterns to create something fresh and new for us.

Now, we must have understood what Generative AI is.

### Does Generative AI copy answers from its training data?

No. Generative AI does not copy and paste an old answer, and during training, it is not memorizing text word for word. It learns the patterns, like which words usually come after which words and how ideas connect. Then, it uses these patterns to create new content that did not exist before.

### Is an LLM the same as Generative AI?

Not exactly. Generative AI is the broad type of AI that creates new text, images, audio, video, and code. A Large Language Model, or LLM, is a trained model that works mainly with text and language. LLMs are the trained brains that power many of the Generative AI tools we use.

### Is ChatGPT an example of Generative AI?

Yes. The models behind ChatGPT, Claude, and Gemini are all Large Language Models, and they power Generative AI tools. When we ask such a tool a question in plain English, it creates a brand new answer by predicting the next word again and again, using the patterns it learned during training.

### What decides whether Generative AI picks a safe word or a surprising one?

A setting called Temperature controls this, along with two more settings called Top-k and Top-p. When the AI predicts the next word, it can play safe with the most likely word or take a chance on a more surprising one. These settings decide which way it leans.

### Is Generative AI built on Machine Learning?

Yes. Both the old AI that decides and Generative AI that creates are built on Machine Learning. Generative AI learns by looking at a huge amount of examples during a stage called training. The trained result is called a model, and it uses the learned patterns to create new content.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
