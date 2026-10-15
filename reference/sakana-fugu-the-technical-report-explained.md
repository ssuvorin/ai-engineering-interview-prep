> Source: https://outcomeschool.com/blog/decoding-sakana-fugu

# What is Sakana Fugu? The Technical Report Explained
URL: https://outcomeschool.com/blog/decoding-sakana-fugu
Published: 2026-06-22

What is Sakana Fugu? The Technical Report Explained

# What is Sakana Fugu? The Technical Report Explained

Authors
: - Name
: Amit Shekhar
Published on
: June 21, 2026

Sakana Fugu is a family of AI models that work like a conductor for a team of other AI models. A Fugu model reads our question, decides which powerful AI models should work on it, and combines their answers into one.

In this blog, we are going to learn about Sakana Fugu, a family of AI models that work like a conductor for a team of other AI models.

We will cover the following:

- What is Sakana Fugu?
- Why Fugu was needed
- The big picture: what Fugu does
- Collective Intelligence
- The two Fugus - Fugu and Fugu-Ultra
- How Fugu picks the right model - the lightweight selection head
- Teaching Fugu who is best - supervised fine-tuning
- Polishing Fugu on real tasks - evolutionary strategies
- How Fugu-Ultra conducts an orchestra - the Conductor
- Teaching Fugu-Ultra to conduct - GRPO
- Stopping the agents from copying each other
- How well does Fugu perform?
- The clever strategies Fugu discovered on its own
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is Sakana Fugu?

Sakana Fugu is a family of AI models. A Fugu model does not answer your question by itself. Instead, it reads your question and decides which other powerful AI models should work on it, how they should work together, and how to combine their answers into one final reply.

In simple words, Fugu is a conductor. A conductor does not play any instrument. The conductor reads the music, decides which musician should play, when, and how loud, and turns many players into one beautiful performance. Fugu does the same thing with AI models.

Fugu comes from Sakana AI, and the team describes it in the "Sakana Fugu Technical Report". Sakana AI is a research lab in Tokyo. One of its founders, Llion Jones, is a co-author of the original "Attention Is All You Need" paper, the paper that introduced the Transformer.

The paper calls models like Fugu orchestrator models. An orchestrator is the one who arranges many parts so that they work together as one. So, the whole goal of Fugu is to take a team of strong AI models and make them act as a single, smarter system.

## Why Fugu was needed

The best way to learn this is by taking an example.

Today we have many powerful AI models, often called frontier models. Frontier just means they are at the leading edge, the most powerful and latest models available. We have GPT-5.5 from OpenAI, Claude Opus 4.8 from Anthropic, and Gemini 3.1 Pro from Google. Each one is very strong. But, here is the catch. No single model is the best at everything.

The paper observed clear specializations:

- GPT models are very strong at math and at planning and combining ideas.
- Claude Opus models are very strong at software engineering and at finding security bugs, which means debugging.
- Gemini models are very strong at directly implementing known algorithms and at science like chemistry and biology.

So, if we use only one model, we get its strengths, but we are also stuck with its weaknesses.

Now, the question is: how do we get the strengths of all of them at the same time? Let's build up the answer step by step.

Approach 1: Use one model for everything. This is the simplest approach. The issue with this approach is that we are stuck with one model's weak areas. Let's see how the next approach tries to solve this.

Approach 2: Build a fixed team by hand. We could write a fixed plan ourselves, for example, "Model X always writes the code, then Model Y always reviews it." The issue with this approach is that it is rigid. We have to design and tune it ourselves, and the same fixed plan is used for every question, even when it does not fit the question. Let's see how the next approach tries to solve this.

Approach 3: A simple router. We could train a small router that looks at the question and sends it to one model. This is better, but it is still single-step. It picks one model once, it cannot change its mind partway through the task, and it cannot make two models work together. The issue with this approach is that it is too limited. Let's see how Fugu solves this.

So, here comes Sakana Fugu to the rescue. Fugu is a learned orchestrator. It reads the question and builds a plan for that specific question - which models to involve, how they should talk to each other, and when to combine their answers. The plan is not fixed. It changes based on the question.

## The big picture: what Fugu does

Before going into the details, let's see the simple input-to-output view.

You give Fugu a question. Fugu reads it, picks the right model or the right team of models from its pool, lets them work, and gives you back one final answer. From the outside, it feels like you are talking to a single model.

```
                  +-----------------------+
   "Write me      |    Fugu Orchestrator  |
    binary    --> |  (reads the question, | --> picks the right worker(s)
    search"       |    builds a plan)     |
                  +-----------------------+
                       |       |       |
                       v       v       v
                   +------+ +------+ +------+
                   | GPT  | | Opus | |Gemini|   <- pool of frontier workers
                   +------+ +------+ +------+
                       |       |       |
                       +-------+-------+
                               |
                               v
                          Final Answer

```

Here, we can see that Fugu sits in the middle. The user talks only to Fugu. Behind the scenes, Fugu uses a pool of frontier models as workers and combines their work into one answer.

Now, let's decode each piece one by one. The paper itself says that the complexity does not come from any single piece being hard. It comes from how the pieces are stacked together. So, if we understand each piece on its own, the whole system becomes simple.

## Collective Intelligence

Collective intelligence is when a group of limited individuals, by working together, produces behavior that is smarter than any single member could be alone.

We see this everywhere. A single ant is simple, but an ant colony builds complex nests. A single person knows a little, but a good team solves big problems. Fugu brings this idea to AI models. Each frontier model is one expert. Fugu turns them into a team.

The paper makes a bigger point here. It treats orchestration as a new scaling axis. Until now, we made AI better mostly by training one bigger and more expensive model. Fugu says there is another way to get better: make many existing models cooperate well.

This brings real benefits:

- When a new model is released, we just add it to the pool. We do not retrain anything.
- We can remove a model, or favor one provider, or block a model for privacy or policy reasons, without retraining.

This flexibility matters in the real world too. A model can become unavailable for many reasons, such as access restrictions, outages, or price changes. Because Fugu's pool of models is swappable, it can simply route around any model that becomes unavailable. The team keeps working even if one member leaves.

## The two Fugus - Fugu and Fugu-Ultra

The paper releases two versions, built for two different needs. The trade-off is between quality and latency. Latency means the time you wait for an answer.

- Fugu balances quality with speed. For each input, it picks a single best worker model. So it is about as fast as just calling one model. It is meant for everyday use, like coding and chat.
- Fugu-Ultra aims for the highest quality on the hardest problems. It builds a plan that uses multiple models per input. This is slower, but it gives better answers. It is meant for the most complex tasks.

Let me tabulate the differences between Fugu and Fugu-Ultra for your better understanding so that you can decide which one to use based on your use case.

| Point | Fugu | Fugu-Ultra |
| --- | --- | --- |
| Goal | balance speed and quality | maximum quality |
| Models per input | one worker | many workers in a plan |
| Speed | fast, like one model | slower |
| Built on | Trinity | Conductor |
| Best for | everyday coding and chat | hardest multi-step problems |

Here, Trinity and Conductor are two earlier research papers from Sakana AI. Fugu builds on Trinity, and Fugu-Ultra builds on Conductor. We will understand both as we decode each variant.

## How Fugu picks the right model - the lightweight selection head

Let's first understand the fast variant, Fugu.

Fugu uses a normal language model as its backbone, which means its brain. A language model is an AI that reads text and predicts what comes next, word by word. It is pre-trained, which means it has already learned from a huge amount of text before we use it. When you type a question, the language model reads it and forms a hidden state, which is simply a list of numbers that captures the meaning of what the model has read. We call it `h`.

Normally, a language model has an LM head that turns the hidden state into the next word. Fugu adds a second small head right next to it, called the lightweight selection head. This head takes the hidden state `h` and outputs `L` numbers called logits, one score for each worker model in the pool. The model with the highest score is selected.

```
  Question --> [ Language Model backbone ] --> hidden state h
                                                  |
                            +---------------------+---------------------+
                            |                                           |
                       [ LM Head ]                        [ Lightweight Selection Head ]
                    (writes normal text)                              |
                                                          L scores, one per worker model
                                                                      |
                                                          pick the highest -> dispatch

```

Here, we can see two heads reading the same hidden state. The LM head is the normal one that writes text. The selection head is the new one that scores the worker models.

Let's define the symbols:

- `h` is the hidden state, the list of numbers that captures the meaning of the question.
- `L` is the number of worker models in the pool.
- `logits` are the raw scores, one per model, before turning them into probabilities.

Now, here is the key trick that makes Fugu fast. Fugu uses the logits, not generated text. It does not need to write out a full answer to make its decision. It computes the hidden state at an early position, applies the selection head, reads the scores, picks the highest, and immediately sends your question to the chosen worker. Because it skips the slow word-by-word writing, the decision is very fast. This is why Fugu has low latency.

This is also where Fugu differs from Trinity, the earlier Sakana model it builds on. Trinity also assigned a role to the chosen model, like Thinker, Worker, or Verifier. Fugu drops the roles and always uses the chosen model as a worker. Fewer choices means a smaller and faster decision, which is exactly what we want for everyday use.

One more thing to notice. To adapt its brain cheaply, Fugu does not retrain the whole model. Think of the model as having millions of tiny dials. Instead of changing all of them, Fugu changes only a small set of adjustment dials and leaves the rest fixed. This keeps training small and fast. The math trick that picks which small set of dials to turn is called SVD, which means Singular Value Decomposition, and it comes from an earlier Sakana paper called Transformer-squared. We do not need to understand the trick itself. We just need to remember that it lets Fugu adjust a few dials instead of all of them. The selection head itself is also kept small and simple.

## Teaching Fugu who is best - supervised fine-tuning

Now, Fugu must learn which model is best for which kind of question. The paper trains it in two stages. The first stage is supervised fine-tuning, often called SFT.

To train Fugu in this stage, the Fugu team collects a big set of questions where the correct answer is already known. For each question, they run every worker model several times and check how well each one did. They give each model a reward, a score for how well it solved the question.

The best way to learn this is by taking an example.

Suppose we have a pool of 3 worker models. Call them GPT, Opus, and Gemini. We give them a math question. We run each one a few times and average the scores. The reward is between 0 and 1, where 1 means it solved the question perfectly. Say we get:

- GPT: average reward 0.9
- Opus: average reward 0.6
- Gemini: average reward 0.3

So our score vector is `s = (0.9, 0.6, 0.3)`.

Now, the simple approach would be to just say "GPT is the best, so the label is GPT." But this throws away useful information. It hides the fact that Opus was also quite good, and that Gemini was weak. So instead, the paper turns these scores into a soft target distribution using the softmax function. Softmax is a simple function that takes any list of scores and turns them into probabilities, which are all positive, all add up to 1, and keep the bigger scores bigger. Do not worry, we will compute it with real numbers.

The formula is:

```
p(j) = exp(r_j / T) / sum over all j' of exp(r_j' / T)

```

Where:

- `p(j)` is the target probability for model `j`.
- `r_j` is the average reward of model `j`.
- `T` is the temperature, a knob that controls how sharp or how flat the result is.
- `exp(x)` means `e` raised to the power `x`.
- `sum over all j'` means we add up the term for every model.

Do not worry if this formula looks complex. We will break it down step by step with actual numbers. Let us use temperature `T = 1`, because dividing by 1 changes nothing.

Here, `e` is just a fixed number, about 2.718, that shows up everywhere in math. So `exp(0.9)` simply means 2.718 raised to the power 0.9. You do not need to compute this by hand. A calculator gives the value. What matters is the pattern: a bigger score gives a bigger `exp` value.

Step 1: Compute `exp(x)` for each score.

- `exp(0.9) = 2.460`
- `exp(0.6) = 1.822`
- `exp(0.3) = 1.350`

Step 2: Add them up.

- Sum = `2.460 + 1.822 + 1.350 = 5.632`

Step 3: Divide each by the sum.

- `p(GPT) = 2.460 / 5.632 = 0.437`
- `p(Opus) = 1.822 / 5.632 = 0.324`
- `p(Gemini) = 1.350 / 5.632 = 0.240`

So the soft target is `(0.437, 0.324, 0.240)`. This is a probability distribution, which is just a set of numbers that say how likely each option is and that add up to 1, like all probabilities should.

Let's read this in plain words. The target says GPT is the best choice about 44% of the time, Opus about 32%, and Gemini about 24%. Notice that it did not say "always GPT." It kept the fact that Opus is also a strong backup. That is the richer signal that helps Fugu make robust choices when several models are similarly good.

What does the temperature `T` do? A smaller `T` makes the distribution sharper, putting more weight on the best model. A larger `T` makes it flatter, making the models more equal. It lets us control how strongly Fugu favors the top model.

Now Fugu is trained to predict this target. Just like we turned the rewards into probabilities, Fugu's own selection head scores are also passed through softmax, so Fugu also outputs a set of numbers that add up to 1, one for each model. We call this Fugu's predicted distribution. Fugu's predicted distribution is then compared to the soft target using KL divergence, which measures how far apart two probability distributions are.

The training loss is:

```
L_SFT = average over all questions of D_KL( p( . ) || pi( . | q ) )

```

Where:

- `pi( . | q )` is Fugu's own predicted distribution over the models for question `q`.
- `p( . )` is the soft target we just computed.
- The dot inside `p( . )` just means the whole set of numbers, one for every model.
- `D_KL` is the KL divergence, the gap between the two distributions. The double bar `||` just separates the two distributions we are comparing, so `D_KL( p || pi )` reads as the gap between distribution `p` and distribution `pi`.
- We average over all questions in the training set.

Let's see KL divergence with numbers. Suppose right now Fugu predicts `(0.5, 0.3, 0.2)` for our question, while the target is `(0.437, 0.324, 0.240)`. The KL divergence is computed as:

```
D_KL = sum over all j of p(j) * ln( p(j) / pi(j) )

```

Here, `p(j)` is the target probability for model `j`, and `pi(j)` is the single probability Fugu gives to model `j`. This `pi` is just a name for Fugu's prediction, not the number 3.14.

- GPT term: `0.437 * ln(0.437 / 0.5) = 0.437 * ln(0.874) = 0.437 * (-0.135) = -0.059`
- Opus term: `0.324 * ln(0.324 / 0.3) = 0.324 * ln(1.080) = 0.324 * 0.077 = 0.025`
- Gemini term: `0.240 * ln(0.240 / 0.2) = 0.240 * ln(1.200) = 0.240 * 0.182 = 0.044`

Add them: `-0.059 + 0.025 + 0.044 = 0.010`

So the KL divergence is about `0.010`, a small positive number. It is small because Fugu's guess is already close to the target. Training nudges Fugu's prediction toward `(0.437, 0.324, 0.240)`, which pushes the KL divergence toward 0. When the two distributions match exactly, the KL divergence is 0.

Here, `ln` is a standard math function on any calculator. You do not need to compute it by hand. We just plug the numbers in. The one thing to notice is that when the two numbers being compared are equal, `ln` of their ratio is 0, which is why a perfect match gives a KL divergence of 0. Remember, these are small numbers just for the sake of understanding. Real training uses a huge set of questions and many worker models.

To learn Fine-tuning, Logits and Cross-Entropy, and Supervised and Unsupervised Learning from the ground up, explore our AI and Machine Learning Program at Outcome School.

## Polishing Fugu on real tasks - evolutionary strategies

Stage 1 taught Fugu using single-step questions, where we can cleanly score each model. But real work is not single-step. Real coding happens over many turns - reading a code repository, editing files, running tools, reading the errors, and trying again. So Stage 2 trains Fugu on full, end-to-end tasks.

Here is the problem. Normally, AI models learn using a method called gradient training. It needs a clear math signal at every small step that tells the model exactly which way to adjust itself. But in an end-to-end task, we only find out at the very end whether the task was completed. We get a single reward, 1 if done and 0 if not done. There is no clear step-by-step signal to follow through a long chain of tool calls and model handoffs. So normal gradient training does not fit well here.

So, here comes evolutionary strategies to the rescue. The paper uses a method called sep-CMA-ES. The idea is simple, and it copies how nature improves through evolution: try many small variations, keep the ones that perform best, and move toward them. No gradients are needed. We only need to measure how well each variation does.

Let me explain the idea with a tiny example. Imagine Fugu's trained values are just a single number `theta`. In reality it is a long list of numbers, but one number is enough to see the idea.

- Current value, the parent: `theta = 0.0`
- Step size: `sigma = 1.0`, which controls how far we explore
- We will try `4` variations, called the population

Step 1: Create variations. We add small random nudges `z` to the parent.

- `z1 = 0.5`, so candidate `theta1 = 0.0 + 1.0 * 0.5 = 0.5`
- `z2 = -0.3`, so candidate `theta2 = -0.3`
- `z3 = 1.0`, so candidate `theta3 = 1.0`
- `z4 = -0.8`, so candidate `theta4 = -0.8`

Step 2: Measure fitness. We run each candidate on the end-to-end tasks and record the fraction of tasks it completed. This is the fitness.

[…544ln elided…]

- Take a question from the user.
- Look up answers from our own documents.
- Remember the previous messages in the conversation.
- Call a calculator or a search engine when needed.
- Format the final answer in a clean way.

Now, doing all of this by hand becomes messy. We have to write a lot of code to glue every piece together. We have to manage the order of steps. We have to handle the data moving from one step to the next.

This is hard to build and harder to maintain.

So, here comes LangChain to the rescue.

LangChain gives us ready-made building blocks. We just connect these blocks like Lego pieces. Each block does one job, and LangChain joins them together.

This way we can use LangChain to solve the interesting problem of building complex LLM apps in a very simple way.

Now that we have learned why we need LangChain, it's time to understand the core idea behind it.

## The core idea behind LangChain

The core idea of LangChain is very simple.

> Take small building blocks and chain them together to build a complete flow.

Let's understand this with an analogy.

Consider a factory assembly line. A car is built step by step. First, the body is made. Then, the engine is added. After that, the wheels are fixed. Finally, the paint is done. Each station does one job and passes the car to the next station.

LangChain works in the same way. Each block does one small job. The output of one block becomes the input of the next block. This is the chain.

Let me map this analogy to LangChain for our better understanding.

| Assembly line | LangChain |
| --- | --- |
| Raw material entering | User input |
| A single work station | A building block |
| The car moving forward | Data passing to the next step |
| The finished car | The final answer |

Now, we have the big picture. Now, let's learn about each building block one by one. Do not worry, we will learn about each of them in detail.

## LLM and Prompt Template

The first block is the LLM, which is the brain of our app. We already know that the LLM takes text and returns text.

But before sending text to the LLM, we must prepare the text carefully. The text we send to the LLM is called a Prompt.

In simple words, a prompt is the instruction we give to the LLM.

Now, most of the time our prompt is not fixed. A part of it changes based on the user. So, here comes the Prompt Template into the picture.

A Prompt Template is a ready-made prompt with some blank spaces that we fill at runtime.

Let's see the code for a prompt template as below:

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Explain {topic} in simple words for a beginner."
)

prompt = template.format(topic="LangChain")

```

Here, we have created a template with a blank space called `topic`. When we call `format` and pass `topic="LangChain"`, the blank space gets filled. The final prompt becomes "Explain LangChain in simple words for a beginner."

This is how a prompt template helps us reuse the same prompt with different values. It makes our life easy.

Now, we have a prompt ready. Now, let's learn how to join the prompt template with the LLM. This is where the chain comes in.

## What is a Chain?

A Chain is the joining of many blocks so that the output of one block flows into the next block.

In simple words, a chain is a pipeline of steps.

Let's say we want a simple chain. First, the prompt template fills in the user topic. Then, the LLM reads that prompt and gives an answer. This is a chain of two steps.

Let's see the code for a chain as below:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

template = PromptTemplate.from_template(
    "Explain {topic} in simple words for a beginner."
)

chain = template | llm

result = chain.invoke({"topic": "LangChain"})

```

Here, we can see a few important things. We created the `llm` block and the `template` block. Then we joined them using the `|` symbol. This `|` symbol is the pipe, and it means "send the output of the left side into the right side."

So, `template | llm` means the filled prompt from the template goes straight into the LLM. When we call `invoke` with our topic, the data flows through the chain and we get a result.

This is the heart of LangChain. We build small blocks and join them with the pipe.

Let's visualize this chain as below:

```text
  user input              filled prompt              answer
   {topic}                    text                    text
      |                        |                        |
      v                        v                        v
  +----------+    pipe    +----------+    pipe    +----------+
  | Template | ---------> |   LLM    | ---------> |  Parser  |
  +----------+            +----------+            +----------+
   fills the              the brain:              cleans the
   blank space            reads the prompt,       answer into a
                          gives an answer         clean result

```

Here, we can see that the data flows from left to right. The top row shows the data on each wire, and the bottom row shows what each block does. The `Template` fills the blank space and passes the filled prompt to the `LLM`. The `LLM` is the brain. It reads the prompt and passes its answer forward to the `Parser`. The `|` pipe between each block is what carries the output of one block into the next block. This is exactly what a chain means.

To learn how to build LLM apps with LangChain and LangGraph in depth, check out our AI and Machine Learning Program at Outcome School.

Now, we have understood the chain. But the LLM gives us plain text. Many times we need the answer in a clean structure. So, let's learn about the output parser.

## Output Parser

An Output Parser takes the raw text from the LLM and converts it into a clean, structured form.

In simple words, the LLM speaks in plain text, and the output parser turns that text into something our program can use easily.

Let's say we ask the LLM for a list of three fruits. The LLM returns "apple, banana, mango" as plain text. But in our code, we need an actual list of three separate items. The output parser does this conversion for us.

Let's see the code for an output parser as below:

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

chain = template | llm | parser

result = chain.invoke({"topic": "LangChain"})

```

Here, we have added one more block called `parser` to our chain. Now the data flows through three blocks. The template fills the prompt, the LLM gives an answer, and the parser cleans that answer into a simple string. The `StrOutputParser` simply gives us back clean text instead of the full message object.

This is how an output parser makes the final result neat and ready to use.

Now, our chain can take input, talk to the LLM, and clean the output. But there is a problem. Our app forgets everything after every message. Let's solve this with memory.

## Memory

Let's say we are chatting with our app. We ask, "Who is Albert Einstein?" The app answers correctly. Then we ask, "Where was he born?"

But here is the catch. The app does not know who "he" is, because it forgot the previous message. Every call to the LLM is fresh, and it does not remember the past on its own.

So, here comes Memory to the rescue.

Memory is the part of LangChain that stores the previous messages of a conversation so the app can remember the context.

In simple words, memory gives our app the power to recall what was said before.

Let's understand how it works. Each time the user sends a new message, LangChain takes the old messages from memory and adds them to the new prompt. So the LLM sees the full conversation, not just the latest message.

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

Let's see a simple flow of memory as below:

```python
# Turn 1
# Stored in memory: "User: Who is Albert Einstein?"

# Turn 2
# Memory + new message are sent together:
# "User: Who is Albert Einstein?
#  AI: Albert Einstein was a famous physicist.
#  User: Where was he born?"

```

Here, we can notice that in the second turn, the old conversation is added before the new question. So now the LLM knows that "he" means Albert Einstein. The memory carries the context forward.

This is how memory makes our app feel like a real conversation. Problem Solved.

Now, our app can remember the chat. But what if we want the app to answer using our own documents? The LLM does not know about our private data. Let's solve this with retrieval.

## Retrieval and RAG

The LLM is trained on general data from the internet. It does not know about our company documents, our personal notes, or our latest files.

Let's say we have a 200-page company handbook. We want our app to answer questions from this handbook. The LLM has never seen it. So how do we teach the app about it?

So, here comes Retrieval into the picture.

Retrieval means fetching the most relevant pieces of our own data and giving them to the LLM along with the question.

This full pattern has a name. It is called RAG, which stands for Retrieval-Augmented Generation. In simple words, we first retrieve the right information, then we let the LLM generate the answer using that information.

Let's understand the steps of how retrieval works.

Step 1: We break our big document into small pieces called chunks.

Step 2: We convert each chunk into a list of numbers called an embedding. An embedding is just a way to represent text as numbers so the computer can compare meaning.

Step 3: We store all these embeddings in a special database called a Vector Store. A vector store is a database built to search by meaning, not just by exact words.

Step 4: When the user asks a question, we turn the question into an embedding too, and we search the vector store for the closest matching chunks.

Step 5: We send those matching chunks plus the question to the LLM, and the LLM answers using them.

We can picture the RAG flow as below:

```text
  Our document
       |
       v
  +----------+    +-----------+    +--------------+
  |  Chunks  | -> | Embeddings | -> | Vector Store |
  +----------+    +-----------+    +--------------+
                                          ^
                                          | search by meaning
                                          |
  User question --> Embedding ------------+
                                          |
                                          v
                                  matching chunks
                                          |
                                          v
                           User question + matching chunks
                              combined into one prompt
                                          |
                                          v
                              +-----------------------+
                              |          LLM          | --> Answer
                              +-----------------------+

```

Here, we can see that the top row prepares our data once. We split the document into chunks, turn each chunk into an embedding, and store all of them in the `Vector Store`. When the user asks a question, we turn the question into an embedding too and search the `Vector Store` by meaning. The matching chunks and the question are then combined into one single prompt, and that single prompt is sent to the `LLM`, which generates the final answer from our own data.

Let's see a simplified code for retrieval as below:

```python
# Find the chunks that match the user question
relevant_chunks = vector_store.similarity_search("What is the leave policy?")

# Send the chunks and the question to the LLM
chain = prompt_with_context | llm | parser

result = chain.invoke({
    "context": relevant_chunks,
    "question": "What is the leave policy?"
})

```

Here, we can see that we first search the vector store for chunks related to the leave policy. Then we pass both the chunks and the question into our chain. The LLM now reads our own data and answers from it.

This is how retrieval and RAG let the LLM answer questions from our private data. That's the beauty of LangChain.

We have a detailed blog on Agentic RAG that takes this retrieval pattern further.

Now, our app can use memory and our own documents. But sometimes the LLM needs to take action in the real world, like searching the web or doing math. Let's learn about tools and agents.

## Tools and Agents

The LLM is very good at language, but it is not good at everything. For example, the LLM is weak at exact math, and it does not know today's live information.

Let's say we ask, "What is the weather in Delhi right now?" The LLM cannot know this, because it has no live connection to the weather.

So, here comes the idea of Tools to the rescue.

A Tool is an external function, such as a calculator, a search engine, or a weather service, that can be run to do something the LLM cannot do on its own.

In simple words, a tool is a helper that gets run when the LLM cannot do the job by itself.

Now, here is one very important point that people often get wrong. The LLM does not run the tool by itself. The LLM only recommends which tool to use and what input to pass to it. The actual call to the tool is made by our code. The LLM is the advisor, and our code is the doer.

So, the next big question is: who takes the LLM's recommendation and actually runs the tool? This is where the Agent comes in.

An Agent is a smart controller that uses the LLM to decide which tool to use and in what order, then runs that tool, takes back the result, and gives it to the LLM, until the task is complete.

In simple words, the agent works in a loop. It asks the LLM what to do next. The LLM recommends a tool and the input for it. The agent runs that tool, sees the result, and sends the result back to the LLM. Then it asks the LLM for the next step again. It keeps doing this until the task is done.

Let's see a numeric walkthrough of how an agent works. Suppose the user asks, "What is 25 times 18, and is that more than 400?"

Step 1: The agent sends the question to the LLM. The LLM recommends the calculator tool with the input `25 * 18`.

Step 2: The agent runs the calculator tool with `25 * 18`. The tool returns `450`.

Step 3: The agent sends `450` back to the LLM. The LLM compares `450` with `400` and sees that `450` is more than `400`.

Step 4: The LLM forms the final answer: "25 times 18 is 450, which is more than 400."

Here, we can notice that the math was not guessed. The agent ran a real tool for the calculation, and then the LLM reasoned about the result. This makes the answer reliable.

When these agent steps, decisions, and loops grow complex, we can lay them out as a graph and let the framework run them for us. We have a detailed blog on how LangGraph works that explains this step by step.

Note: The agent uses the LLM as its brain to make decisions, and the tools as its hands to take actions.

This is how tools and agents give our app the power to do real work.

To go deep into AI Agents and Tool use, and to build an AI Coding Agent from scratch, check out our AI and Machine Learning Program at Outcome School.

Now, we have learned about every building block. Now, let's put them all together into one complete flow.

## A complete flow of how LangChain works

Let's connect everything we have learned into a single story. Suppose a user opens our app and asks a question about our company handbook.

Step 1: The user types the question into our app.

Step 2: LangChain pulls the previous messages from memory and adds them for context.

Step 3: LangChain uses retrieval to fetch the matching chunks from the vector store.

Step 4: The prompt template combines the question, the memory, and the retrieved chunks into one final prompt.

Step 5: This prompt flows into the LLM through the chain.

Step 6: If the task needs an action, the LLM recommends a tool, and the agent runs that tool and brings the result back to the LLM.

Step 7: The LLM produces an answer.

Step 8: The output parser cleans the answer into a neat form.

Step 9: The clean answer is shown to the user, and the new messages are saved into memory for the next turn.

The complete flow looks like below:

```text
   User question
        |
        v
  +-----------+        +-----------+        +--------------+
  |  Memory   | -----> |  Prompt   | <----- | Retrieval /  |
  | (context) |        | Template  |        | Vector Store |
  +-----------+        +-----------+        +--------------+
        ^                    |
        |                    v
        |              +-----------+  agent calls   +-------+
        |              |    LLM    | <------------> | Tools |
        |              +-----------+ (LLM advises)  +-------+
        |                    |
        |                    v
        |              +-----------+
        |              |  Parser   |
        |              +-----------+
        |                    |
        |                    v
        |          Clean answer to user
        |                    |
        +--------------------+
              saves new messages

```

Here, we can see how all the blocks work together. The question first gathers context from `Memory` and matching chunks from `Retrieval`. The `Prompt Template` combines everything into one prompt and sends it to the `LLM`. When an action is needed, the `LLM` recommends a tool, and the `Agent` runs that tool and feeds the result back to the `LLM`. The answer then passes through the `Parser` to become clean, and finally goes back to the user while the new messages are saved into `Memory` for the next turn.

Here, we can see how each block does one job and passes its result to the next block. The input flows in from one side, moves through the chain, and the final answer comes out from the other side. This is exactly the assembly line we talked about at the start.

This is how LangChain works, end to end. Let's quickly recap what we have learned.

LangChain is a framework that helps us build applications powered by LLMs. It gives us small building blocks and lets us chain them together.

We learned about the prompt template that prepares the text, the chain that joins the blocks, and the output parser that cleans the result. We learned about memory that remembers the conversation, retrieval and RAG that bring in our own data, and tools and agents that take real actions.

Now, we must have understood how LangChain works.

### Is LangChain an LLM?

No. LangChain is not an LLM. It is a framework that sits between us and the LLM. It gives us ready-made building blocks, like prompt templates, chains, output parsers, memory, retrieval, and tools, and helps us connect the LLM with our data, our tools, and our logic.

### Does the LLM run tools by itself in LangChain?

No. The LLM only recommends which tool to use and what input to pass to it. The actual call to the tool is made by our code through the agent. The agent runs the tool, takes back the result, and gives it to the LLM, until the task is complete.

### Does an LLM remember earlier messages without memory?

No. Every call to the LLM is fresh, and it does not remember the past on its own. LangChain memory stores the previous messages and adds them to each new prompt, so the LLM sees the full conversation and knows, for example, who "he" refers to.

### What does the pipe symbol do in a LangChain chain?

The `|` pipe sends the output of the left side into the right side. For example, `template | llm | parser` means the filled prompt goes into the LLM, and the LLM's answer goes into the parser. This is how we join small blocks into one chain.

### When should we use LangGraph instead of a simple LangChain chain?

We should use LangGraph when agent steps, decisions, and loops grow complex. In that case, we can lay them out as a graph and let the framework run them for us.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

[Showing lines 1-293 and 838-1252 of 1252; 544 middle lines (28.8KB) elided. Read artifact://64 for full output]
