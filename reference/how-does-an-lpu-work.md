> Source: https://outcomeschool.com/blog/how-does-an-lpu-work

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
- A GPU is a huge team of workers. It was made for graphics, and later we found that it is also very good at the heavy parallel math that machine learning needs.
- An LPU is a specialist. It was made only for running a language model that is already trained.

Google took a similar specialist route with its own chip for machine learning, and we have a detailed blog on how a Google TPU works that walks through that design step by step.

Here, two words are very important, "already trained". An LPU is built for inference, which means using a model that has already finished learning. It is not built for training a model.

The term LPU was introduced by a company called Groq, which builds these chips. But the ideas behind it are general, and those ideas are what we are going to understand here.

Now, the obvious question is, we already have GPUs, and they are extremely powerful, so why do we need a new chip at all?

To answer that, we must first understand what a language model actually does when it writes text. Once we understand that, the design of the LPU will feel obvious.

## How an LLM writes text, one token at a time

Before jumping into the hardware, we must know how a language model produces an answer.

A language model does not write the full answer in one shot. It writes one token at a time. A token is a small piece of text, sometimes a full word, sometimes a part of a word.

Let's say we ask the model, "The capital of France is".

- The model reads the whole sentence and produces one token, "Paris".
- Now the model reads "The capital of France is Paris" and produces the next token, ".".
- Now the model reads "The capital of France is Paris." and decides that the answer is over.

We can write this loop like below:

```
input = "The capital of France is"

loop:
    read the entire model
    compute the next token
    add that token to the input
    if the token means "the answer is over":
        stop

```

Here, we can notice the most important thing about this loop. Every token must wait for the token before it. We cannot compute token number five before we have token number four, because token number four is part of the input for token number five.

So, text generation is a chain.

This single sentence explains almost everything about the LPU. A chain cannot be made faster by adding more workers. It can only be made faster by making each link of the chain finish quicker.

Now, let's see what actually takes time inside one link of that chain.

## The real bottleneck is memory, not math

A language model is just a very large pile of numbers. These numbers are called weights, or parameters, and both words mean the same thing here. They were learned during training, and they are the entire knowledge of the model. When we hear "a 70B model", it simply means a model that carries 70 billion such numbers.

Each of these numbers takes up some space. If we store each one in 8 bits, which is 1 byte, then 70 billion numbers take around 70 GB of space. So, the model itself is a 70 GB pile of numbers sitting in memory.

Storing each weight in fewer bits shrinks this pile directly, and we have a detailed blog on how Model Quantization works that explains this in depth.

To produce one single token, the chip must read every single weight of the model, from the first one to the last one.

And what does the chip do with each weight? It multiplies it with a number and adds the result. That is one multiply and one add. That is all.

So, for every number that we move from memory into the chip, we do almost no work with it. We move a lot and we compute very less. The chip finishes the math and then sits idle, waiting for the next batch of numbers to arrive.

Let's take an analogy for the sake of understanding.

Suppose there is a chef in a kitchen. The chef is incredibly fast and can cook any dish in a few seconds. But all the recipe books are kept in a warehouse across the road. For every single dish, the chef must walk to the warehouse, carry all the books back, read one line from each book, and cook.

The cooking takes seconds. The walking takes minutes.

Making the chef faster will not help at all. The chef is not the problem. The distance to the books is the problem.

This is exactly the situation inside a chip that is running a language model. The math is not the bottleneck. Moving the weights is the bottleneck. In simple words, the work is memory bound, not compute bound.

Now that we have understood where the time actually goes, it is time to see why a GPU has a hard time with this.

## Why a GPU struggles here

A GPU is a wonderful machine, and it is the reason modern AI exists at all. But it was designed for a different shape of problem.

A GPU keeps the model weights in a memory called HBM, which stands for High Bandwidth Memory. HBM sits right beside the chip, on the same small board, and it is genuinely fast. But it is still outside the chip, and the numbers still have to travel across a wire to reach the compute units, which are the parts of the chip that actually do the multiplying and the adding.

Before we put numbers on it, we must know one word, bandwidth. Bandwidth is simply how many bytes the memory can hand over to the chip in one second. If a memory has a bandwidth of 3 TB per second, it can deliver 3,000 GB of data every second.

Now, let's put rough numbers on it, just for the sake of understanding.

```
Weights of a 70B model, stored in 8-bit = 70 GB
Weights that must be read per token     = 70 GB

HBM bandwidth on a modern GPU           = around 3 TB per second

Time for one token  = 70 / 3000 = 0.023 seconds = 23 milliseconds
Tokens in a second  = 1 / 0.023 = around 43 tokens

```

Here, we can see that even in the perfect case, where the GPU never wastes a single moment, one token takes around 23 milliseconds, and one user gets around 43 tokens per second. That is the ceiling. No amount of extra math power will push it higher, because the wire is the limit.

So, how does a GPU cope with this today? The answer is batching. The GPU waits for many users to arrive, and then it reads the model once and serves all of them together in the same trip. One walk to the warehouse, many dishes cooked.

Advantage: The total number of tokens per second, counting all the users together, becomes very high. This total is called throughput.

Disadvantage: Every individual user still waits, because their own chain of tokens is still moving at the same slow pace. And to fill a batch, the GPU sometimes has to wait for more users to show up, which adds even more delay.

So, batching gives us high throughput. It does not give us speed for one person.

There is one more thing to notice. A GPU is a flexible machine. It has caches that guess which data we will need next, schedulers that decide while running which work goes where, and waiting lines that reorder the instructions. All of this flexibility is very useful when we do not know what the program will look like. But it costs chip area, it costs power, and it makes the timing unpredictable.

So, we have two problems now. The model is too far away, and the chip spends a lot of its effort on guessing.

The LPU attacks both of these problems directly. Let's see how.

## Idea 1: Keep the model on the chip

The first idea is the simplest one to say and the hardest one to build.

Do not keep the weights in a memory outside the chip. Keep them inside the chip itself.

The memory that lives inside a chip is called SRAM. It sits right next to the compute units, so the numbers barely have to travel at all. Because there is no long wire and no separate memory chip to reach, SRAM is dramatically faster than HBM.

Let's redo our calculation with on-chip memory.

```
Weights that must be read per token = 70 GB

On-chip SRAM bandwidth              = around 80 TB per second

Time for one token  = 70 / 80000 = 0.000875 seconds = 0.875 milliseconds
Tokens in a second  = 1 / 0.000875 = around 1,100 tokens

```

Here, we can see that the same read now takes less than one millisecond instead of 23 milliseconds. That is roughly 26 times faster, and it turns 43 tokens per second into more than a thousand tokens per second, for a single user, without any batching at all.

Note: These are rough numbers used only to show the idea. The real numbers change with the model, with how the numbers are stored, and with the hardware generation. The point to remember is the gap between the two, not the exact digits.

To feel what this means, an average person reads around 5 words per second. So a model producing a thousand tokens per second is writing far faster than any of us can read. The words stop appearing one by one and start appearing in whole paragraphs.

The chef is no longer walking across the road. The recipe books are now lying open on the kitchen counter.

This is the single biggest reason an LPU feels so fast when we watch it write.

To learn how these bandwidth numbers turn into real serving decisions - LLM Inference Bottleneck Analysis, Numbers Every AI Engineer Should Know, and designing an LLM Inference Platform - check out our AI and Machine Learning Program at Outcome School.

## The problem with on-chip memory

Now, if putting the model inside the chip is such a good idea, why does everyone not do it?

Because on-chip memory is tiny.

SRAM is expensive and it takes a lot of physical space on the chip itself, and the space on a chip is the most costly thing a chip designer has. An LPU chip carries around 230 MB of it, which is a very generous amount for on-chip memory, but it is nothing compared to what a large model needs.

```
Size of a 70B model in 8-bit = 70,000 MB
On-chip SRAM per LPU chip    = 230 MB

Chips needed = 70,000 / 230 = around 305 chips

```

So, one chip cannot hold the model. Not even close.

Here is the trade at the heart of the LPU. It gives up memory size to gain memory speed. A GPU chip can hold tens of GB but reads them slowly. An LPU chip holds only 230 MB but reads them incredibly fast. The LPU chose speed, and now it has to live with the consequence of that choice.

So, here comes a simple idea to the rescue. We cut the model into slices and give one slice to each chip.

A language model is made of layers stacked one after the other. So, chip number 1 holds the first few layers, chip number 2 holds the next few layers, and so on, until the last chip holds the final layers. Together, the hundreds of chips hold the whole model, and every chip holds its own slice permanently, right inside itself.

Now, the next big question is, if the model is spread across 300 chips, will they not spend all their time sending data to each other?

The answer is no, and the reason is simple.

The slice of weights sitting on a chip is huge, hundreds of megabytes. But the thing that travels from one chip to the next is not the weights. It is the activation, which is the small bundle of numbers that represents the sentence so far after passing through those layers. For one token, that bundle is only a few kilobytes.

So, the huge thing stays still, and only the tiny thing moves.

This is the trade that makes the whole design work. We accept that we need many chips, and in return we never have to move the model again.

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

This was all about keeping the model close to the compute. Now, let's learn about the second idea.

## Idea 2: Remove all the guesswork

The second idea is about the chip itself.

A normal processor decides things while it is running. It has a cache that guesses which data will be needed next. It has a branch predictor that guesses which way the program will turn. It has a scheduler that decides, while the program is running, which unit does which piece of work. All of this happens on the fly, thousands of times per second.

An LPU throws all of that away.

In an LPU, the compiler decides everything before the chip is ever switched on.

Here, a compiler is simply a program that takes our work and turns it into the exact instructions a chip will follow. On a normal machine, the compiler prepares the instructions and the chip still makes many decisions on its own. On an LPU, the compiler makes all of those decisions too, and it makes them in advance.

Here, one more word will help us, clock cycle. Every chip has an internal heartbeat, and each single beat is called a clock cycle. A modern chip beats more than a billion times per second, and every small action inside the chip happens on one of these beats.

Now, the compiler knows the model completely. It knows every layer, every multiplication, and every number that has to move. So it writes out a full plan that says which unit does what on which exact beat, and which piece of data sits on which wire on which exact beat.

The chip does not decide anything. It only follows the plan.

Let's take an analogy.

Consider a busy road crossing with traffic lights. Every car arrives whenever it wants. The lights react, cars wait, some cars slip through, some get stuck. It works, but nobody can tell you exactly when a particular car will reach the other side.

Now consider a railway timetable. The train leaves at 9:00, reaches the next station at 9:14, and leaves again at 9:15. Nothing is decided in the moment. Everything was decided months ago, and the whole network is built so that the plan holds.

A GPU is the traffic crossing. An LPU is the railway timetable.

This gives us two big wins.

First, all the chip space that would have gone into caches, predictors, and schedulers is now free. That space is given to more compute units and more SRAM instead. Nothing is spent on guessing.

Second, the timing becomes exact. If we ask an LPU how long a request will take, it can tell us the answer down to the clock cycle, before running it. This kind of predictability is very hard to get on a normal chip.

This approach is called deterministic execution, which simply means that the same work always takes exactly the same time, because nothing is left to chance. It is also described as software-defined hardware, because the software plan is doing the job that the hardware normally does by itself.

Till now, we have learned how one chip behaves. Now, it is time to learn how hundreds of them behave together.

## Idea 3: A network that never waits

We have hundreds of chips, and each of them holds one slice of the model. Now those chips have to talk to each other for every single token.

Normally, chips talk to each other the way computers talk on a network. One chip sends a message, the other chip replies to say that it has received the message, two messages sometimes arrive at the same moment and one of them has to wait, and the waiting line sometimes gets full. Every one of these little events adds a small delay, and nobody can say in advance how big that delay will be. When the data has to pass through hundreds of chips one after the other, these small delays pile up into a big delay.

An LPU handles this differently. All the chips run on a synchronized clock, and the compiler plans the movement between chips exactly the way it plans the movement inside a chip.

So, chip number 7 knows that on cycle number 4,120 the data from chip number 6 will arrive on a particular wire. It does not ask. It does not wait. It does not check. It simply reaches out at that cycle, and the data is there.

There is no handshake, no acknowledgement, and no retry, because there is nothing to be uncertain about.

This is how the machine keeps behaving like one big chip even though it is made of hundreds of small ones.

## The assembly line

Now that we have all three ideas, let's put them together and see the machine as a whole.

Think of a car factory assembly line. Station 1 fits the frame, station 2 fits the engine, station 3 fits the doors, and so on. The car moves from station to station, and every station has its own tools kept right beside it, permanently.

A group of LPU chips working together is exactly this.

- Every chip is a station.
- The slice of model weights is the set of tools kept permanently at that station.
- The activation, that small bundle of numbers, is the car moving down the line.
- The compiler is the factory schedule that says which station does what at which second.

The activation enters the first chip, passes through its layers, moves to the second chip, and keeps flowing forward until it comes out of the last chip as the next token.

And here is one more advantage. The moment chip number 1 has passed its work to chip number 2, chip number 1 is free. It does not sit idle waiting for the token to finish the whole journey. It immediately starts working on the next request. So, the line always stays full, exactly like a real assembly line.

This is how hundreds of small chips behave like one very fast machine. Now, let's walk through one actual request from start to end.

## What happens when we send a prompt

Step 1: The model is loaded, once.

Long before our request arrives, the compiler prepared the plan and the model was spread across the chips. Each chip loaded its slice into its own SRAM. This happens one time. After that, the weights never move again.

Step 2: The prompt is read.

We send "The capital of France is". All the words of this prompt are already known, so there is no chain to wait for, and every word can be pushed through the machine together. This first stage is called prefill.

[…579ln elided…]

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

[Showing lines 1-330 and 910-1326 of 1326; 579 middle lines (31.4KB) elided. Read artifact://91 for full output]
