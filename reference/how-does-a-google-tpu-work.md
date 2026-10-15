> Source: https://outcomeschool.com/blog/how-does-a-google-tpu-work

# How does a Google TPU work?
URL: https://outcomeschool.com/blog/how-does-a-google-tpu-work
Published: 2026-06-28
Author: Amit Shekhar

How does a Google TPU work?

# How does a Google TPU work?

Authors
: - Name
: Amit Shekhar
Published on
: June 28, 2026

A TPU (Tensor Processing Unit) is a special computer chip made by Google for machine learning. It uses a design called a systolic array to do matrix multiplication, the most important operation in machine learning, very fast.

In this blog, we will learn about how a Google TPU works. We will also see what a TPU is, why Google built it, how it is different from a CPU and a GPU, and how it makes machine learning fast.

We will cover the following:

- What is a TPU?
- Why Google built the TPU
- A quick refresher: CPU and GPU
- The one operation that matters most
- The big idea: Systolic Array
- How data flows through a TPU
- The full journey of a TPU computation
- Why a TPU is so fast and power efficient
- Where TPUs are used
- Limitations of a TPU

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a TPU?

Let's start with the name itself.

TPU = Tensor + Processing + Unit.

A TPU is a special computer chip made by Google. Its full name is Tensor Processing Unit.

In simple words, a TPU is a chip built for one main job: doing the math that machine learning needs, and doing it very fast.

Now, you may be wondering what a tensor is.

A tensor is just a fancy word for a grid of numbers. A single number is a tensor. A list of numbers is a tensor. A table of numbers, with rows and columns, is also a tensor.

So, when we say "Tensor Processing Unit", we mean a unit that processes grids of numbers.

That is the whole idea. A TPU is a chip that eats grids of numbers and gives back new grids of numbers, very quickly.

### Why Google built the TPU

Let's understand the problem first. Then the solution will make sense.

Around the year 2013, Google noticed something worrying. People were using voice search, photo search, and translation more and more. All of these use machine learning.

Machine learning means teaching a computer to do a task by showing it many examples, instead of giving it exact step-by-step instructions.

Here, the worry was simple. Google did the math and realized that if every person used voice search for just a few minutes a day, Google would need to double the number of computers in its data centers. That would cost a huge amount of money.

So, Google needed a chip that could do machine learning math much faster and using much less power than normal chips.

Normal chips were not built for this job. They were built to do many different things reasonably well. But machine learning needs one kind of math done billions of times.

So, here comes the TPU to the rescue.

Google decided to build a brand new chip from scratch, designed for only one purpose: machine learning math. That chip is the TPU.

### A quick refresher: CPU and GPU

Before we go deeper into the TPU, we must understand two other chips. Do not worry, we will keep this simple.

A CPU is the Central Processing Unit. It is the main brain inside every laptop and phone. A CPU is like a very smart single worker. It can do almost any task, but it does one or a few things at a time. It is flexible, but not great when we need the same simple task done billions of times.

A GPU is the Graphics Processing Unit. It was first built to draw images and run games. A GPU is like a big team of workers. Instead of one smart worker, it has thousands of smaller workers doing many small tasks at the same time. This is called doing things in parallel, which means many tasks happening together.

Machine learning loves parallel work. So GPUs became very popular for machine learning.

But a GPU still tries to be flexible. It can do many different kinds of tasks. That flexibility has a cost in speed and power.

So, the question is: can we build a chip that gives up some flexibility, and in return becomes even faster and more power efficient for machine learning?

The answer is yes. That chip is the TPU.

### The one operation that matters most

To understand a TPU, we must first understand the one math operation that machine learning does again and again.

That operation is called matrix multiplication.

A matrix is simply a table of numbers, with rows and columns. So, matrix multiplication means combining two tables of numbers to produce a new table of numbers.

Let's see the idea with a tiny example.

Suppose we have a small list of input numbers, and a small table of weights.

A weight is just a number that the model learned during training. It decides how important each input is.

Now, the basic step inside matrix multiplication is this: we take each input, multiply it by its matching weight, and then add all those results together.

For example, let's say the inputs are `2, 3, 4` and the weights are `5, 6, 7`.

The result is computed like below:

```text
(2 × 5) + (3 × 6) + (4 × 7)
= 10 + 18 + 28
= 56

```

Here, we can see that the whole job is just "multiply, then add", done many times and the results added up. This pattern is called multiply-and-accumulate, because we multiply two numbers and accumulate, which means keep adding, the result into a running total.

A neural network does this multiply-and-accumulate step billions of times. So, if we can build a chip that does multiply-and-accumulate extremely fast, we win.

That is exactly what the TPU is built to do.

The neural network math we just walked through - matrix multiplication and multiply-and-accumulate - is exactly what we go deep into in our AI and Machine Learning Program at Outcome School, where we cover Neural Networks, Feed-Forward Networks, and Backpropagation, and build a Neural Network from scratch.

### The big idea: Systolic Array

Now we reach the heart of the TPU. This is the most beautiful idea in the whole design.

The main part of a TPU is called the Matrix Multiply Unit, often shortened to MXU. Inside this unit sits a special structure called a Systolic Array.

The word "systolic" comes from the word "systole", which is the squeezing beat of a heart that pushes blood through the body. The name was chosen because data moves through the chip in steady, rhythmic pulses, just like blood pumped by a heartbeat.

So, what is a Systolic Array?

A Systolic Array is a large grid of tiny calculators arranged in rows and columns. Each tiny calculator can do only one thing: multiply two numbers and add the result to a running total. That is the multiply-and-accumulate step we just learned.

Let's say the grid is 128 calculators wide and 128 calculators tall. That gives us 128 × 128, which is 16,384 tiny calculators all sitting together on one chip.

Here is the clever part. In a normal chip, after each calculation, the result is sent back to memory, and the next number is fetched from memory. Going to memory again and again is slow and wastes a lot of power.

In a Systolic Array, the calculators pass their results directly to their neighbors. The numbers flow from one calculator to the next, like water flowing down a series of steps. The data does not keep running back to memory. It just keeps moving forward through the grid.

This is the secret. The TPU keeps the data moving and the calculators busy, instead of wasting time talking to memory.

### How data flows through a TPU

Let's make the flow very concrete with a simple picture in words.

Imagine the grid of calculators. The weights are loaded into the grid first and they stay in place, one weight sitting in each calculator.

Now, the input numbers enter from the left side. They flow to the right, moving one step at a time, from one calculator to the next.

At the same time, the running totals flow from the top to the bottom.

So, at each calculator, three things meet at the right moment:

- An input number coming from the left
- A weight already sitting inside the calculator
- A running total coming from above

The calculator multiplies the input by its weight, adds that to the running total, and passes the new total downward to the next calculator.

Let's see it as below:

```
              running totals flow down
                       |   |   |
                       v   v   v
                  +---+---+---+---+
   inputs   --->  | C | C | C | C |  --->
   from left --->  +---+---+---+---+  ---> (inputs exit
   --->           | C | C | C | C |  --->  to the right)
   --->            +---+---+---+---+  --->
                  | C | C | C | C |
                   +---+---+---+---+
                       |   |   |
                       v   v   v
                  finished totals fall out

   Each C is a tiny calculator holding one weight.
   C = multiply (input x weight) + running total

```

Here, we can see that the inputs enter from the left and move right, the running totals move down, and each box C is one tiny calculator holding one weight. At every box, the input and the total meet, get combined, and move on. By the time the totals reach the bottom of the grid, the full matrix multiplication is finished. The answers simply fall out of the bottom.

Here, we can see the beauty. Thousands of multiply-and-accumulate steps happen at the same time, in a steady rhythm, with almost no trips back to memory.

This is how a TPU does in one smooth wave what a normal chip would do in many slow, separate steps.

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

### The full journey of a TPU computation

Let's now follow the complete journey from start to finish, step by step.

Step 1: The model and its data are prepared on a host computer. The host is just a normal computer that controls the TPU and feeds work to it.

Step 2: The weights and inputs are copied into the TPU's own fast memory. A TPU has memory built very close to the calculators, so data does not have to travel far. This closeness saves a lot of time and power.

Step 3: The weights are loaded into the Systolic Array. Each tiny calculator holds its own weight, ready and waiting.

Step 4: The input numbers start flowing into the grid from the left, pulse by pulse, like a heartbeat.

Step 5: Inside the grid, every calculator does its multiply-and-accumulate step and passes results to its neighbors. Thousands of these happen together.

Step 6: The finished totals come out of the bottom of the grid.

Step 7: These totals often pass through an activation step. An activation is a simple rule that decides how strong each result should be, for example turning negative numbers into zero. This helps the neural network learn complex patterns.

Step 8: The results are stored back, and they become the input for the next layer of the neural network. The cycle repeats for each layer until the model produces its final answer.

Here is the full flow:

```
   Host computer (prepares model and data)
                  |
                  v
   TPU fast memory (weights + inputs copied in)
                  |
                  v
   Weights loaded into the Systolic Array grid
                  |
                  v
   Inputs flow in from the left, pulse by pulse
                  |
                  v
   Grid does multiply-and-accumulate together
                  |
                  v
   Finished totals fall out of the bottom
                  |
                  v
   Activation step (for example, negatives -> zero)
                  |
                  v
   Stored back, becomes input for the next layer
                  |
                  +--- repeats for each layer --->
                  |
                  v
   Final answer (for example, "this is a cat")

```

Here, we can see the data travels in one direction, from the host computer, through the grid, and back out as a result, layer after layer, until the model gives its final answer. This is how a single prediction, such as recognizing a cat in a photo, travels through a TPU.

### Why a TPU is so fast and power efficient

Now that we understand the design, the reasons for its speed become clear.

Reason 1: It does one job extremely well. A TPU does not try to be flexible like a CPU. It is built for matrix multiplication. By giving up flexibility, it gains speed.

Reason 2: Thousands of calculators work together. With tens of thousands of tiny calculators in the grid, a huge amount of math happens at the same instant.

Reason 3: Less talking to memory. This is the big one. In normal chips, moving data to and from memory uses most of the time and most of the power. The Systolic Array keeps data moving between neighbors, so it avoids most of these slow memory trips.

Reason 4: Simpler number math. For many machine learning tasks, we do not need very precise numbers. A TPU can use smaller, simpler numbers, which means each calculation uses less energy and finishes faster. Simpler numbers also mean we can fit more calculators on the same chip.

Put these together, and the TPU does far more machine learning math per second, while using far less electricity, than a normal chip.

This is why Google can run huge models for billions of people without building a mountain of new data centers.

### Where TPUs are used

So, now we know how a TPU works. Let's see where it is actually used.

TPUs power many Google products that we use every day. Here are a few examples:

- Search uses TPUs to understand what we are really asking.
- Google Translate uses TPUs to convert text from one language to another.
- Google Photos uses TPUs to recognize faces, places, and objects in our pictures.
- Voice assistants use TPUs to understand our spoken words.

TPUs are also used to train very large models, including large language models, which are the models behind modern chatbots.

And, through Google Cloud, other companies can rent TPUs to train and run their own machine learning models, without buying any hardware themselves.

There is also a smaller cousin called the Edge TPU. This is a tiny TPU made to run inside small devices, such as cameras and sensors, so they can do machine learning right where they are, without sending data to a data center.

To learn how large models are trained, served, and deployed across the cloud and on-device - LLM Inference Engineering, Model Deployment and Serving, and Cloud vs On-device Deployment - check out our AI and Machine Learning Program at Outcome School.

### Limitations of a TPU

A TPU is powerful, but it is not the right tool for every job. We must understand this clearly.

A TPU is built for machine learning math, mainly matrix multiplication. It is not a general-purpose chip.

So, we cannot use a TPU to run a normal program, browse the web, or play a regular game. For those everyday tasks, we still need a CPU.

A TPU also works best with large amounts of similar math done together. For small or irregular tasks, a CPU or GPU often does better.

Here, we can see the simple trade-off. A TPU gives up flexibility and, in return, gives us amazing speed and power efficiency for one specific kind of work.

Another chip pushes this specialization even further by dropping training altogether, and we have a detailed blog on how an LPU works that explains how it runs only already-trained language models.

And that one kind of work, machine learning math, happens to be exactly what modern artificial intelligence needs the most.

So, this is how a Google TPU works. It is a chip filled with thousands of tiny calculators, arranged in a grid, that pass numbers to each other in a steady heartbeat rhythm, doing the multiply-and-accumulate math of machine learning faster and with less power than any normal chip.

### Is a TPU better than a GPU for machine learning?

For large amounts of similar machine learning math, a TPU can be faster and more power efficient. A GPU still tries to be flexible, and that flexibility has a cost in speed and power. A TPU gives up flexibility to do matrix multiplication extremely well. For small or irregular tasks, a CPU or GPU often does better.

### Can we use Google TPUs without buying any hardware?

Yes. Through Google Cloud, other companies can rent TPUs to train and run their own machine learning models without buying any hardware themselves. TPUs also power many Google products, such as Search, Google Translate, and Google Photos.

### Are TPUs used to train large language models?

Yes. TPUs are used to train very large models, including large language models, which are the models behind modern chatbots. A neural network does the multiply-and-accumulate step billions of times, and the TPU is built to do exactly that step extremely fast.

### Does a TPU work on its own without a normal computer?

No. A host computer, which is just a normal computer, controls the TPU and feeds work to it. The model and its data are prepared on the host and then copied into the TPU's own fast memory. Also, a TPU cannot run a normal program or browse the web, so we still need a CPU for everyday tasks.

### What is an Edge TPU?

An Edge TPU is a tiny TPU made to run inside small devices, such as cameras and sensors. It lets these devices do machine learning right where they are, without sending data to a data center. It is the smaller cousin of the TPUs used in Google's data centers.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# How does an LPU work?
URL: https://outcomeschool.com/blog/how-does-an-lpu-work
Published: 2026-09-03
Author: Amit Shekhar

How does an LPU work?

# How does an LPU work?

Authors
: - Name
: Amit Shekhar
Published on
: September 3, 2026

An LPU (Language Processing Unit) is a chip built for one single job: running a large language model that is already trained, and producing text as fast as possible.

In this blog, we will learn about how an LPU works, the chip that was built for one single job, running a large language model and printing words on our screen as fast as possible. We will also see what an LPU actually is, how a language model writes text one token at a time, why memory and not math is the real bottleneck, how an LPU keeps the model right next to the compute, how the compiler plans every single cycle in advance, how hundreds of chips work together like an assembly line, and where it works well and where it fails.

We will cover the following:

- What is an LPU?
- How an LLM writes text, one token at a time
- The real bottleneck is memory, not math
- Why a GPU struggles here
- Idea 1: Keep the model on the chip
- The problem with on-chip memory
- Idea 2: Remove all the guesswork
- Idea 3: A network that never waits
- The assembly line
- What happens when we send a prompt
- Why an LPU is fast, all in one place
- Where an LPU works well
- Where an LPU does not work well
- LPU vs GPU
- When to use which one

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is an LPU?

An LPU is a chip that is built for one single job, running a large language model that is already trained, and producing text as fast as possible.

LPU = Language Processing Unit.

In simple words, it is a processor that has been designed around the way a language model writes text, and around nothing else.

Let's compare it with the chips that we already know.

- A CPU is a general worker. It can do almost anything, but it does only a few things at a time.
[…855ln elided…]

This is the gap that Speculative Decoding fills.

## The core idea behind Speculative Decoding

Speculative Decoding has a very simple idea behind it.

Let's say we have two models:

- A small model called the draft model. It is fast. Say, 1 billion parameters.
- A large model called the target model. It is the smart one. Say, 70 billion parameters.

The plan is:

- The draft model writes the next 4 or 5 tokens quickly, one after the other.
- The target model takes all those draft tokens together and checks them in a single forward pass.
- For each draft token, the target model decides: "Yes, I would have written this too" or "No, this is wrong."
- We keep all the tokens that the target model accepts. We throw away the rest. We continue from there.

Here is the flow at a high level as below:

```
                 [ draft model ]
                       |
             writes 4 tokens sequentially
                       v
           +--------------------------+
           |  draft: t1  t2  t3  t4   |
           +--------------------------+
                       |
                       v
                [ target model ]
                       |
            single forward pass on all 4
                       |
                       v
       +----------------------------------+
       | accept t1, accept t2, reject t3, |
       |     fix t3, drop t4              |
       +----------------------------------+
                       |
                       v
              continue from accepted prefix

```

Here, the magic is in the second step. The target model is checking 4 or 5 tokens at once in a single pass. It is using the GPU's compute power that was sitting idle. The memory cost of loading the model weights is paid only once, but we get multiple tokens back.

Let's use a real-world analogy.

Suppose there is a senior engineer who is very careful and very slow. There is also a junior engineer who is fast but makes some mistakes. Without Speculative Decoding, the senior engineer writes every single line of code by themselves. With Speculative Decoding, the junior engineer writes a quick draft of 5 lines. The senior engineer then reads all 5 lines together and approves the correct ones, fixes the first wrong one, and continues from there. Most of the time, the junior gets at least the first few lines right. So the senior gets to review a batch instead of writing every line from scratch.

That is the entire idea.

## Step-by-step walkthrough

Now, let's walk through one round of Speculative Decoding to see how this looks in practice. Suppose the prompt so far is "I love teaching AI" and the draft length is 4.

Step 1: The draft model takes "I love teaching AI" and generates 4 tokens one by one as below:

```
Draft tokens: "and", "Machine", "Learning", "today"

```

The draft model is small, so this is very fast.

Step 2: The target model takes the prompt plus the 4 draft tokens together. In a single forward pass, the target model produces the probability distribution for each position as below:

```
Position 1 (after "AI"):                          target predicts "and"      -> matches draft
Position 2 (after "AI and"):                      target predicts "Machine"  -> matches draft
Position 3 (after "AI and Machine"):              target predicts "Learning" -> matches draft
Position 4 (after "AI and Machine Learning"):     target predicts "everyday" -> does NOT match "today"

```

Step 3: We accept the tokens until the first rejection.

- "and" is accepted
- "Machine" is accepted
- "Learning" is accepted
- "today" is rejected. The target model wanted "everyday" instead.

Step 4: We replace the rejected token with the target model's choice. So we accept "and Machine Learning everyday".

Step 5: We start the next round with the prompt "I love teaching AI and Machine Learning everyday".

Before we see the verification visually, let's see all the inputs that go into the target model at the same time in one parallel forward pass, as below:

```
All 8 inputs go into the target model in parallel (one forward pass):

  Position:     1       2        3            4       5       6          7           8
  Input:       "I"    "love"  "teaching"    "AI"    "and"  "Machine"  "Learning"  "today"
              \____________ prompt ____________/    \___________ 4 draft tokens ____________/
                |       |        |           |       |        |          |           |
                v       v        v           v       v        v          v           v
              +---------------------------------------------------------------------+
              |              Target model (ONE parallel forward pass)               |
              +---------------------------------------------------------------------+
                |       |        |           |       |        |          |           |
                v       v        v           v       v        v          v           v
  Predicts     next    next     next        next    next     next       next        next
  next token:  token   token    token       token   token    token      token       token

```

All 8 positions are processed at the same time. At every position, the target model predicts what the NEXT token should be. So we get 8 next-token predictions in one shot, in a single parallel forward pass. We compare these predictions against the 4 draft tokens to decide which ones to accept - all 4 verified at the same time, not one by one.

Here is the same round shown visually as below:

```
+----------+--------+----------+------------+------------+
| Position |   1    |    2     |     3      |     4      |
+----------+--------+----------+------------+------------+
| Draft    | "and"  |"Machine" | "Learning" |  "today"   |
| Target   | "and"  |"Machine" | "Learning" | "everyday" |
| Decision |  [OK]  |  [OK]    |    [OK]    |   [FIX]    |
+----------+--------+----------+------------+------------+

What happens:
  - Positions 1, 2, 3: accepted (draft matches target)
  - Position 4: rejected, replaced with target's "everyday"

Tokens added this round: "and" + "Machine" + "Learning" + "everyday"  =  4 tokens
Target model forward passes used: 1

```

In one round, we got 4 tokens instead of just 1. The target model only ran once. That is the speedup.

If all 4 draft tokens had been accepted, we would have got 5 tokens in one round. That is 4 draft tokens plus 1 bonus token. The bonus comes for free because the target model's single forward pass produces a probability distribution at every position, including the one right after the last draft token. So we get one more token at no extra cost.

It works perfectly.

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

## The verification step

Now, a natural question arises - how does the target model decide whether to accept or reject a draft token?

The simple version is: if the draft token is the same as what the target model would have picked, accept it.

But this is not the full story. LLMs are probabilistic. They do not always pick the single most likely token. They sample from a probability distribution. So we cannot just check "did the draft token match the top choice of the target." We need a smarter rule.

So, here comes rejection sampling into the picture. The rule works like this:

For each draft token, we have two probabilities:

- `q(x)` = probability that the draft model would pick this token
- `p(x)` = probability that the target model would pick this token

The accept rule is as below:

```
If p(x) >= q(x):
    Always accept
Else:
    Accept with probability p(x) / q(x)

```

Let's see this with concrete numbers.

Example 1: Draft token "Machine" - target agrees strongly.

- `q("Machine") = 0.6` (the draft model picks "Machine" with 60% probability)
- `p("Machine") = 0.8` (the target model picks "Machine" with 80% probability)

Since `p >= q` (0.8 >= 0.6), we always accept "Machine". The target model agrees, even more strongly than the draft model. So no reason to reject.

Example 2: Draft token "today" - target disagrees.

- `q("today") = 0.5` (the draft model picks "today" with 50% probability)
- `p("today") = 0.1` (the target model picks "today" with only 10% probability)

Since `p < q` (0.1 < 0.5), we do not always accept. We accept with probability:

```
p / q = 0.1 / 0.5 = 0.2

```

So 20% of the time we accept "today", and 80% of the time we reject it. We flip a biased coin to decide.

The intuition is simple. When the target model agrees with the draft (`p >= q`), the draft is fine - accept it. When the target model disagrees (`p < q`), the draft is risky - we accept it only sometimes, proportional to how much the target model still believes in it.

If the token is rejected, we do not just give up. We sample a fresh token from a corrected distribution that fills the gap between the two models. This gap is calculated as `max(0, p(x) - q(x))` and then normalized.

Let's see this with numbers. Suppose at the rejected position, three tokens are possible: "everyday", "today", "tomorrow". The draft and target probabilities are as below:

```
              q(x)    p(x)
"everyday"    0.2     0.5
"today"       0.5     0.1
"tomorrow"    0.3     0.4

```

The draft picked "today" but it got rejected by the accept rule. Now we compute the corrected distribution `max(0, p - q)` for every token, then normalize, as below:

```
"everyday": max(0, 0.5 - 0.2) = 0.3
"today":    max(0, 0.1 - 0.5) = 0
"tomorrow": max(0, 0.4 - 0.3) = 0.1

Sum = 0.4

corrected("everyday") = 0.3 / 0.4 = 0.75
corrected("today")    = 0
corrected("tomorrow") = 0.1 / 0.4 = 0.25

```

So the replacement is sampled from this corrected distribution: "everyday" with 75% probability and "tomorrow" with 25% probability. The mass shifts toward the tokens the target model wanted more than the draft did. "today" gets nothing because the target did not want it - the draft over-favored it.

The math here is carefully designed so that the final output of Speculative Decoding has exactly the same probability distribution as if we had run the target model alone, token by token. This is not an approximation. It is mathematically the exact right value.

Note: We have intentionally skipped the full mathematical proof here to keep this blog short and accessible. The proof shows that the probability of ending up with any token `x` works out to exactly `p(x)`, no matter which path the algorithm takes. If you are curious about the details, you can find the full proof in the original Speculative Decoding papers.

This is the most important property of Speculative Decoding. We get the speed benefit, and we lose nothing in quality. That's the beauty of Speculative Decoding.

Not every technique leaves this distribution untouched, though. Some shift it on purpose by a tiny amount. We have a detailed blog on How Does LLM Watermarking Work? that explains how such a small shift hides a signal inside the generated text.

## Real numbers and speedup

Let's put this into perspective with real numbers so we can clearly see how much time we are saving.

Suppose:

- The target model takes 50 milliseconds per token
- The draft model takes 5 milliseconds per token
- We use a draft length of 4 tokens

Without Speculative Decoding (the baseline):

Each token forces one full target-model pass.

```
1 token = 1 target pass = 50 ms

```

So generating any N tokens takes `N x 50 ms`.

With Speculative Decoding, one round costs:

```
4 draft tokens x 5 ms = 20 ms  (drafting)
1 target verification = 50 ms  (verification of all 4 in parallel)
Total per round        = 70 ms

```

The cost per round is fixed at 70 ms. What changes is how many tokens we produce in that round, which depends on how many draft tokens get accepted.

Let's see all three cases.

Best case - all 4 draft tokens are accepted. We get 4 accepted tokens plus 1 free bonus token from the target model, so 5 tokens in 70 ms.

```
Without spec dec: 5 tokens x 50 ms = 250 ms
With spec dec:                      = 70 ms
Speedup: 250 / 70 = 3.57x

```

Average case - 3 of 4 draft tokens are accepted. The first 3 draft tokens are accepted, and the 4th is rejected and replaced by the target model's choice. So we get 3 accepted + 1 corrected = 4 tokens forward (this is the same case shown in our walkthrough above).

```
Without spec dec: 4 tokens x 50 ms = 200 ms
With spec dec:                      = 70 ms
Speedup: 200 / 70 = 2.86x

```

Worst case - 0 draft tokens accepted. Even here, we still move 1 token forward. When the very first draft token is rejected, we sample a replacement from the corrected distribution `max(0, p - q)` at that position, so progress is guaranteed and never zero. But we wasted the drafting time.

```
Without spec dec: 1 token x 50 ms = 50 ms
With spec dec:                     = 70 ms
Speedup: 50 / 70 = 0.71x  (slower!)

```

So Speculative Decoding is a bet. When the draft model agrees with the target model, we win big. When it disagrees, we pay a small penalty. The bet pays off as long as the average acceptance rate is high enough, which it usually is for similar model families.

Now, let's see the user-visible impact for a full response.

Suppose the user asks a question and the target model needs to generate a 200-token answer. As an example, take the average case from above where the agent moves 4 tokens forward per round (3 draft tokens accepted plus 1 corrected token at the rejection position). In real workloads this number can be anywhere from 1 to 5 - we are using 4 just as an illustrative example. The math works out as below:

```
Without Speculative Decoding:
  200 tokens x 50 ms = 10,000 ms = 10.0 seconds

With Speculative Decoding:
  Cost per round: 4 draft tokens x 5 ms + 1 target pass x 50 ms = 70 ms
  Tokens per round (average): 4
  Rounds needed: 200 tokens / 4 tokens per round = 50 rounds
  Total time: 50 rounds x 70 ms = 3,500 ms = 3.5 seconds

Time saved: 6.5 seconds (a 2.86x speedup)

```

Here is the same comparison shown on a timeline as below:

```
Time (seconds):  0    1    2    3    4    5    6    7    8    9    10

Without:         |==================================================|  10.0s
                 (200 target passes, one per token)

With:            |==================|                                   3.5s
                 (50 rounds, 4 tokens each)

                                     <-------- 6.5s saved -------->

```

The user waits 3.5 seconds instead of 10 seconds for the same answer. That is the user-visible win.

In practice, the speedup ranges from 2x to 3x for most workloads. The exact number depends on:

- How well the small draft model matches the big target model
- How long the draft is
- How similar the input style is to what the draft model has seen

The closer the draft model behaves like the target model, the higher the acceptance rate, and the bigger the speedup.

## Where it is used

Speculative Decoding is used in many production LLM systems today.

Some real examples:

- vLLM, SGLang, and TensorRT-LLM support Speculative Decoding out of the box for serving large models.
- Llama models often pair a small Llama with a large Llama to speed up inference.
- DeepSeek-V3 trains the model with an auxiliary objective called Multi-Token Prediction (MTP), which adds a lightweight extra module (a transformer layer plus an output head) that learns to predict the next token at a future position. At inference, this module acts as a built-in drafter for speculative decoding, so no separate draft model is needed. DeepSeek reports about 1.8x generation speedup from this.

The idea has so many variants because it is one of the cheapest ways to get a 2x to 3x speedup on LLM serving without retraining the big model.

## Trade-offs

Speculative Decoding makes generation faster, but it comes with a trade-off:

- We need a second model. The draft model takes extra GPU memory. For very large deployments, this matters.
- The two models must share the same tokenizer. If their token vocabularies are different, the draft tokens will not line up with the target model's expected input.
- The acceptance rate depends on how well the draft and target models agree. If the draft model is too different from the target, most draft tokens get rejected, and we waste time.
- For very short outputs, the overhead of running two models can cancel out the speedup.
- The draft length must be tuned. Too short and we do not get much speedup. Too long and we waste tokens that get rejected.
- The speedup shows up best at low batch sizes, where decoding is memory-bandwidth bound and the GPU's compute is sitting idle. At very high batch sizes, the GPU is already kept busy by Continuous Batching, so the spare compute that Speculative Decoding feeds on is no longer there. The gain shrinks, and in some cases it can even invert.

For most large-model serving workloads, the trade-off is worth it. The user sees a faster response, and the GPU is used more efficiently.

Later methods drop the second model altogether by letting the big model draft for itself. We have a detailed blog on Medusa that explains how extra decoding heads do the drafting.

EAGLE takes that a step further by drafting the model's smooth internal features instead of its noisy output tokens. We have a detailed blog on EAGLE that covers this end to end.

N-gram Speculation goes the other way and needs no model for drafting at all. It looks up the last few tokens in the prompt, copies whatever came after them as the draft, and lets the big model verify, which works very well when the answer repeats the input.

## Quick Summary

Let's recap what we have learned:

- The problem: LLMs generate one token at a time. Each token forces the full big model to run once. The GPU's compute power sits idle while memory is loaded. This is slow.
- The core idea: Use a small fast draft model to write a few tokens. Use the big slow target model to verify all of them in a single parallel pass.
- The accept rule: Each draft token is accepted or rejected based on a math rule called rejection sampling. The math guarantees the final output matches what the big model would have produced alone.
- The benefit: A 2x to 3x speedup with no quality loss.
- The cost: Extra GPU memory for the draft model, and the speedup depends on how well the two models agree.
- In simple words: Speculative Decoding = A small model drafts tokens + The big model verifies them in parallel.

Speculative Decoding is one of those rare techniques that gives us speed without giving up quality. It does not change the model. It does not change the output. It just uses the GPU more cleverly.

This is why almost every modern LLM serving system supports it today.

### Does Speculative Decoding reduce the quality of the output?

No. The rejection sampling rule is designed so that the final output has exactly the same probability distribution as running the target model alone, token by token. This is not an approximation. We get the speed benefit and lose nothing in quality.

### Can Speculative Decoding make generation slower?

Yes, in some cases. If no draft tokens are accepted, a round costs more than a single target pass, for example 70 ms instead of 50 ms. The gain can also shrink or even invert at very high batch sizes, and very short outputs may not benefit because of the overhead of two models.

### Do the draft model and the target model need the same tokenizer?

Yes. The two models must share the same tokenizer. If their token vocabularies are different, the draft tokens will not line up with the target model's expected input.

### Do we always need a separate draft model?

No. DeepSeek-V3 uses Multi-Token Prediction, where a lightweight extra module acts as a built-in drafter. Medusa lets the big model draft for itself using extra decoding heads. N-gram Speculation needs no model for drafting at all, as it copies the draft from the prompt.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

[Showing lines 1-398 and 1254-1670 of 1670; 855 middle lines (48.8KB) elided. Read artifact://61 for full output]
