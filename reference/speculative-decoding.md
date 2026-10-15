> Source: https://outcomeschool.com/blog/speculative-decoding

# What is Speculative Decoding and How Does It Make LLMs Faster?
URL: https://outcomeschool.com/blog/speculative-decoding
Published: 2026-05-06
Author: Amit Shekhar

What is Speculative Decoding and How Does It Make LLMs Faster?

# What is Speculative Decoding and How Does It Make LLMs Faster?

Authors
: - Name
: Amit Shekhar
Published on
: May 6, 2026

Speculative Decoding is a technique that makes an LLM generate text faster without losing quality. A small draft model quickly guesses the next few tokens, and the big model verifies all those guesses in one single run.

In this blog, we will learn about Speculative Decoding - what it is, why LLM generation is slow without it, how a small draft model and a big target model work together to produce tokens faster, the rejection sampling math that guarantees no quality loss, real numbers showing the 2x to 3x speedup, where it is used in production, and the trade-offs to watch out for.

We will cover the following:

- What problem does Speculative Decoding solve?
- The Big Picture
- Why is LLM generation slow?
- The core idea behind Speculative Decoding
- Step-by-step walkthrough
- The verification step
- Real numbers and speedup
- Where it is used
- Trade-offs
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What problem does Speculative Decoding solve?

When we use ChatGPT, Claude, or Gemini that use LLM internally, we notice that the model writes one word at a time. It does not write a full paragraph in one shot. It writes a token, then the next token, then the next.

This is slow.

The bigger the model, the slower it gets. Every single token forces the entire model to do one full forward pass. Billions of parameters get loaded from GPU memory just to produce one token. Then the same thing happens again for the next token. And again. And again.

Speculative Decoding is a technique that makes this faster, without changing the model and without losing any quality.

## The Big Picture

Before we go into the details, let's understand the big picture.

Speculative Decoding uses two models. One small model that is fast but not very smart. One large model that is slow but very smart. The small model writes a quick draft of the next few tokens. The large model then verifies all those tokens in one shot.

In simple words:

Speculative Decoding = A small model drafts tokens + The big model verifies them in parallel.

If the draft is good, we get many tokens for the price of one big-model step. If the draft is bad, we throw away the wrong tokens and continue from where the draft was correct.

The output is exactly the same as if we had used the big model alone. There is no quality loss.

## Why is LLM generation slow?

To understand Speculative Decoding, we must first understand why normal LLM generation is slow.

LLMs generate text in an autoregressive way. This means the model produces one token, then takes that token as input, and produces the next one.

Let's say we want the model to write "I love teaching AI and Machine Learning." The model does this like below:

```
Step 1: Input "I"               -> Output "love"
Step 2: Input "I love"          -> Output "teaching"
Step 3: Input "I love teaching" -> Output "AI"
... and so on

```

For each step, the entire large model runs once. If the model has 70 billion parameters, then for every single token, those 70 billion parameters are read from GPU memory.

Now, here is the interesting part. The GPU is not slow at math. The GPU is slow at moving memory. Most of the time during a single token generation is spent loading the model weights into the compute units, not doing the actual math.

This means the GPU has a lot of free compute power that is sitting idle while it waits for memory.

Do you see the problem? We are paying the full memory cost for every single token, but we are barely using the GPU's compute.

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
