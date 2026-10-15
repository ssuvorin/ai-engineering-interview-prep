> Source: https://outcomeschool.com/blog/decoding-flash-attention

# What is Flash Attention and Why Is It So Fast?
URL: https://outcomeschool.com/blog/decoding-flash-attention
Published: 2026-04-11
Author: Amit Shekhar

What is Flash Attention and Why Is It So Fast?

# What is Flash Attention and Why Is It So Fast?

Authors
: - Name
: Amit Shekhar
Published on
: April 11, 2026

Flash Attention computes the same attention that Transformers already use, but in a much faster and more memory-efficient way on the GPU. It does not change the math, and it does not change the result.

In this blog, we will learn about Flash Attention by decoding it piece by piece - understanding why standard attention is slow, what makes Flash Attention fast, how it uses GPU memory cleverly, and why it is used in almost every modern Large Language Model (LLM).

When we hear "Flash Attention", it sounds complex. But do not worry. If we break it down into its individual parts, every single piece is simple. Our goal is to decode Flash Attention so clearly that by the end, we will be able to explain it to anyone.

We will cover the following:

- A quick recap of standard attention
- Why standard attention is slow
- How GPU memory actually works (HBM vs SRAM)
- The core idea behind Flash Attention
- Tiling: breaking the work into small blocks
- Online softmax: computing softmax without the full matrix
- Recomputation in the backward pass
- Flash Attention 2
- Flash Attention 3
- Advantages and impact of Flash Attention

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

Flash Attention computes the same attention that Transformers already use, but in a much faster and more memory-efficient way. It does not change the math. It does not change the result. It only changes how the attention is computed on the GPU so that it runs much faster and uses much less memory.

In simple words: Flash Attention = Same attention, computed in a much smarter way on the GPU.

## A Quick Recap of Standard Attention

Before jumping into Flash Attention, we must quickly recall how standard attention works.

In a Transformer, each token is converted into three vectors: Query (Q), Key (K), and Value (V). Attention is then computed in three steps.

First, we compute the attention scores by multiplying Q with the transpose of K. This gives us a big matrix of scores - one score for every pair of tokens.

Then, we apply softmax on these scores so that each row becomes a set of probabilities that add up to 1.

Finally, we multiply these probabilities with V to get the final output.

Attention(Q, K, V) = softmax(Q × Kᵀ / √dₖ) × V. If we want to go deeper into the math behind Q, K, and V, we can read Math Behind Attention: Q, K, V.

This is the standard attention. It works perfectly. But it has a serious problem when sequences get long.

## Why Is Standard Attention Slow?

The issue with standard attention is the giant intermediate matrix.

If our sequence has N tokens, then the score matrix `Q × Kᵀ` has a shape of N × N. Let's put this into perspective with real numbers:

- For an input of 4,000 tokens, the attention matrix has 4,000 × 4,000 = 16 million entries.
- For an input of 10,000 tokens, the attention matrix has 10,000 × 10,000 = 100 million entries.
- For an input of 100,000 tokens, the attention matrix has 100,000 × 100,000 = 10 billion entries.

The memory needed grows with the square of the number of tokens. Double the input length, and the memory needed becomes 4 times larger.

There is also a completely different way to attack this cost. We have a detailed blog on Sliding Window Attention that explains how letting each token look only at its neighbors makes the cost grow in a straight line instead of a square.

Here is what happens during standard attention. Notice that the giant N×N matrix is touched four full times by the GPU memory:

- Step 1: The GPU computes the full N×N matrix and writes it to GPU memory.
- Step 2: The matrix is read back from GPU memory to apply softmax.
- Step 3: The softmax result is written back to GPU memory.
- Step 4: It is read again from GPU memory to multiply with V.
- Step 5: Finally, the smaller output matrix is written back to GPU memory. This one is not the N×N matrix - it is the much smaller final output.

When we read the "How GPU Memory Actually Works" section below, this will become clearer.

So, the same huge matrix is being moved back and forth many times. This back-and-forth is the real bottleneck. The GPU is not slow at math. The computing cores are fast enough - they spend most of their time waiting for data to arrive from slow memory.

This is the problem Flash Attention solves.

## How GPU Memory Actually Works

To understand Flash Attention, we must first understand how GPU memory works. A GPU has two main types of memory:

HBM (High Bandwidth Memory): This is the large but slower memory on the GPU. It can hold tens of gigabytes, but reading from it and writing to it is slow compared to the GPU's compute speed.

SRAM (Static RAM): This is the small but very fast on-chip memory. Reading from SRAM is roughly 10 to 20 times faster than reading from HBM, but it can only hold a few hundred kilobytes at a time.

Think of HBM as a huge library on another floor, and SRAM as a small desk right in front of you. Walking to the library takes time. Reading on your desk is instant.

The key insight: The GPU is fast, but moving data between HBM and SRAM is slow. So if we keep moving the giant attention matrix between HBM and SRAM, we waste most of our time on data movement instead of math.

Some chips take this idea all the way and keep the whole model inside SRAM so the weights never travel at all, and we have a detailed blog on how an LPU works that explains that design step by step.

Standard attention writes the full N×N attention matrix into HBM. This is the main bottleneck.

If we want to go deep into attention internals, LLM Inference Bottleneck Analysis, and Transformer Architecture, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

## The Core Idea Behind Flash Attention

Now, here comes Flash Attention into the picture. Flash Attention says:

> Why store the giant N×N attention matrix in HBM at all? Let's compute attention in small blocks that fit inside SRAM, and never write the full matrix to HBM.

In simple words, Flash Attention avoids creating the giant intermediate matrix in slow memory. Instead, it processes small chunks at a time, fully inside the fast SRAM, and only writes the final output back to HBM.

This single idea is what makes Flash Attention so much faster than standard attention. No giant matrix in HBM means no expensive back-and-forth data movement.

But doing this is not easy. There are two challenges to solve:

- How do we break the work into small blocks? (Tiling)
- How do we compute softmax when we only see one block at a time? (Online softmax)

Let's decode each one.

## Tiling

Tiling means breaking a large matrix operation into smaller block-sized operations.

Think of it like reading a very long book from the library. The standard approach would be to bring every single page of the book from the library and spread them all over a huge table. This requires a very large table and a lot of walking back and forth to the library. The Flash Attention approach is different. We bring just one small chapter from the library, read it on our small desk, take notes, return it, and then bring the next chapter. We never need a huge table. Our small desk is enough.

Instead of computing `Q × Kᵀ` for the entire sequence at once, Flash Attention splits Q, K, and V into small blocks - for example, blocks of 256 tokens each. It then loads one block of Q and one block of K into SRAM, computes the partial attention scores there, and immediately uses those scores with the matching block of V.

Here is a simple visual of tiling:

```
      Q split into blocks:        K split into blocks:        V split into blocks:
      [Q1] [Q2] [Q3] ... [Qb]     [K1] [K2] [K3] ... [Kb]     [V1] [V2] [V3] ... [Vb]

      For each Q block:
         For each K block:
            Load Q_block and K_block into SRAM
            Compute partial scores in SRAM
            Multiply with matching V_block
            Update the running output

```

Because each block is small, both Q_block and K_block fit comfortably inside the fast SRAM. The full N×N matrix is never materialized anywhere. The GPU is busy doing math instead of moving data around.

We have a detailed blog on how CUDA Kernels work that explains how GPU threads, blocks, and the fast shared memory work together.

This is the first half of Flash Attention. But there is still one big problem - softmax.

## The Softmax Problem

Softmax is tricky because it needs to look at the entire row to work correctly. If we want to understand softmax in detail, we can watch this video on softmax.

Standard softmax for a row of scores `[s1, s2, s3, ..., sn]` works in two steps.

Step 1: It finds the maximum of the row. Let's call it `max`. We do this for numerical stability - because the scores can be very large numbers, and `exp` of a very large number can blow up the calculation and produce a NaN (Not a Number). By subtracting the max, we keep the numbers small and safe.

Step 2: For each element `si`, it computes `exp(si - max) / sum(exp(sj - max))`. The numerator makes each score positive, and the denominator makes the whole row add up to 1 - so the row becomes a set of probabilities.

For example, for a row `[2, 4, 6]`, the max is 6. We compute `exp(2-6), exp(4-6), exp(6-6)` which is `exp(-4), exp(-2), exp(0)`. Then we divide each by the sum of these three values to get the final probabilities.

The problem is: to find the max and the sum, softmax must see all the scores in the row at the same time. But in tiling, we only see one small block of scores at a time. So, how can we compute softmax block by block without ever holding the full row? The answer is online softmax.

## Online Softmax

Online softmax is a clever trick that lets us compute softmax in pieces. As each new block arrives, we update the running max and the running sum so that the final result is exactly the same as standard softmax - as if we had seen the whole row at once.

Here is the idea in simple words:

- We keep a running max of all scores seen so far
- We keep a running sum of `exp(score - running_max)` seen so far
- We keep a running output of the weighted V values seen so far
- When a new block arrives with a higher max, we rescale the previous running sum and running output to match the new max

Let's see this with a small example. Suppose our full row of scores is `[2, 4, 6]` and we see it in two blocks - first `[2, 4]`, then `[6]`.

Step 1: The first block arrives with scores `[2, 4]`. The running max is `4`. The running sum is `exp(2-4) + exp(4-4) = exp(-2) + exp(0) ≈ 0.135 + 1 = 1.135`.

Step 2: The second block arrives with score `[6]`. The new max is now `6`, which is higher than the old max `4`. So we must rescale the old running sum to match the new max. We multiply the old sum by `exp(old_max - new_max) = exp(4-6) = exp(-2) ≈ 0.135`. The rescaled old sum becomes `1.135 × 0.135 ≈ 0.153`. Then we add the new block's contribution: `exp(6-6) = 1`. The new running sum is `0.153 + 1 ≈ 1.153`.

If we had done standard softmax on the full row `[2, 4, 6]` at once, the sum would be `exp(2-6) + exp(4-6) + exp(6-6) = exp(-4) + exp(-2) + exp(0) ≈ 0.018 + 0.135 + 1 ≈ 1.153`. Exactly the same result. The running output is rescaled in the same way whenever the max changes.

This way, we never need to hold the full row in memory. After processing all blocks, the running output is exactly the same as the final attention output we would get from standard attention. The softmax problem is solved.

This is the second half of Flash Attention. Combined with tiling, it lets the GPU compute attention without ever storing the giant N×N matrix. It works perfectly.

## Putting It All Together

Now, let's put tiling and online softmax together to see how Flash Attention runs end to end.

```
For each block of Q (loaded into SRAM):
    Initialize running_max, running_sum, running_output

    For each block of K and V (loaded into SRAM):
        Compute partial scores = Q_block × K_blockᵀ
        Update running_max
        Rescale running_sum and running_output for the new max
        Add the new contribution from this V_block

    Write the final block of output back to HBM

```

Notice what is happening here. The giant N×N matrix is never written to HBM. Only the small Q, K, V blocks move between HBM and SRAM, and only the final output is written back.

Now, a natural question arises - if Flash Attention also moves blocks back and forth many times, why is it faster? The answer is simple: the total amount of data moved is much smaller.

Let's take our earlier example of 4,000 tokens and put real numbers on it. But first, let's quickly understand two terms:

- Block size: This is how many tokens we group together in one block. In our example, the block size is 256, so one Q block contains 256 tokens.
- The dimension `d`: This is the number of values used to represent one token inside Q, K, and V. So if `d = 128`, each token in Q is a list of 128 numbers. The full Q matrix has `N × d` entries in total. Common values are 64 or 128 in modern LLMs.

Now let's compare how much data each approach moves between HBM and SRAM.

Standard attention creates the full N×N score matrix with 16 million entries (4,000 × 4,000). Let's also name two intermediate matrices used inside standard attention:

- S = Scores matrix. This is the raw output of `Q × Kᵀ` - the attention scores before softmax. Shape: N × N.
- P = Probabilities matrix. This is the output of applying softmax on S - each row is now a set of probabilities that add up to 1. Shape: N × N.

So the flow inside standard attention is `S = Q × Kᵀ`, then `P = softmax(S)`, then `O = P × V`.

Now, the N×N matrix gets touched 4 full times during one attention call:

- Write S to HBM → 16M
- Read S back to apply softmax → 16M
- Write P to HBM → 16M
- Read P back to multiply with V → 16M

That gives `4 × 16M = ~64 million entries` just from the N×N matrix moving back and forth. On top of that, there are smaller movements - reading Q, K, V once each, and writing the final output - but these are tiny compared to the N×N matrix and do not change the picture much. So the total data movement for standard attention is roughly ~64 million entries for one attention call, ignoring any kernel fusion or caching optimizations.

Flash Attention never creates that 16 million entry matrix at all. It works in blocks of 256 tokens. Let's break the numbers down:

- Number of blocks: `4,000 / 256 = 16 blocks` (for each of Q, K, V)
- Size of one block: `256 × 128 = 32,768 entries ≈ 32K`

Flash Attention has two loops - an outer loop over Q blocks (16 iterations), and an inner loop over K and V blocks (16 iterations inside each outer iteration).

For each Q block (one outer iteration):

- Load 1 Q block into SRAM → 32K
- Load all 16 K blocks (one per inner iteration) → `16 × 32K = 512K`
- Load all 16 V blocks (one per inner iteration) → `16 × 32K = 512K`
- Subtotal per outer iteration ≈ ~1M

Across all 16 outer iterations: `16 × 1M ≈ 16M entries` of reads. Plus the final output write of `~0.5M` - the output has shape `N × d = 4,000 × 128 = 512K entries`, which is written back to HBM only once at the very end. So the total data movement for Flash Attention is roughly ~17 million entries - approximate, and the exact number depends on the implementation details and caching.

Here, we can notice that K and V blocks are re-read once per Q block. Even with this re-reading, ~17M is still much smaller than ~64M for standard attention because Flash Attention never creates the giant N×N matrix.

Compare the two:

- Standard attention: ~64 million entries moved
- Flash Attention: ~17 million entries moved

That is roughly 4 times less data movement, and the gap grows even larger as the sequence length grows. Even though Flash Attention re-reads K and V blocks many times, the total data moved is still far smaller because it never creates the giant N×N matrix. The GPU spends most of its time doing math instead of waiting for data. That is why Flash Attention is faster.

Note: We have simplified a few things here to make it easier to understand. In a real Transformer, attention runs in multiple heads in parallel, and `d` is actually the head dimension (the per-head slice of the full token embedding). We have skipped the multi-head detail because it does not change the core comparison. The exact numbers also depend on the GPU, the block size, and how the implementation is written. The core idea stays the same - Flash Attention moves far less data between HBM and SRAM, and that is why it is faster.

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

## Recomputation in the Backward Pass

There is one more trick that Flash Attention uses during training. During training, we need a backward pass to compute gradients. The backward pass normally needs the attention matrix that was computed in the forward pass.

But Flash Attention never stored that matrix in HBM. So how does the backward pass work?

The answer is simple: Flash Attention recomputes the attention scores in SRAM during the backward pass. It does not start completely from scratch - during the forward pass, it saves a small amount of softmax statistics for each row (just the running max and the running sum), which is only O(N) extra memory. In the backward pass, it uses these saved statistics together with Q, K, and V to quickly rebuild the attention scores inside fast SRAM, without ever writing the giant matrix back to HBM. This sounds wasteful, but it is actually faster overall because recomputing in fast SRAM is cheaper than reading a giant matrix from slow HBM.

This trade-off - less memory traffic, more compute - is one of the key reasons Flash Attention is so fast on modern GPUs. Modern GPUs have far more compute than memory bandwidth, so trading memory for compute is a great deal.

## Flash Attention 2

After Flash Attention was introduced, the researchers improved it further and released Flash Attention 2. Flash Attention 2 uses the same core idea - tiling and avoiding the full attention matrix in HBM. But it reduces wasted work even further by reorganizing the computation in three ways.

Change 1 - Fewer non-matmul operations. In Flash Attention 1, the running output is rescaled every time a new K, V block arrives. This rescaling is a non-matmul operation, and non-matmul operations run much slower on modern GPUs than matrix multiplications - because modern GPUs have special tensor cores that are extremely fast at matmuls but not at anything else. Flash Attention 2 delays this rescaling and does it only once at the very end of each Q block. This removes a lot of slow work from the inner loop.

Change 2 - Better parallelism across the sequence. Flash Attention 1 only parallelized work across batch size × number of heads, which works well for short sequences with large batches but leaves the GPU underused for long sequences with small batches. Flash Attention 2 adds one more axis of parallelism - it also parallelizes across Q blocks along the sequence dimension. Different Q blocks can be processed completely in parallel by different GPU workers, with no need to share results between them. This lets Flash Attention 2 use the full GPU much more efficiently, especially for long sequences.

Change 3 - Better work split inside each worker. Inside each GPU worker, Flash Attention 2 also splits the work differently among its threads, which reduces extra reads and writes to fast memory.

Here is a simple way to remember the difference. Flash Attention 1 is mostly about cutting the trips to slow HBM. It took the trips from very high down to a small number. Flash Attention 2 is mostly about keeping the GPU fully busy doing fast matmul work once those trips are already cut. It makes sure the tensor cores are not sitting idle while the GPU does slow rescaling or waits for other workers. Because of these improvements, Flash Attention 2 is roughly 2x faster than Flash Attention 1, and that too with the same mathematical output.

Note: The pseudocode we saw in the "Putting It All Together" section above already follows the Flash Attention 2 style - Q on the outside, K and V on the inside.

## Flash Attention 3

After Flash Attention 2, the researchers also released Flash Attention 3, which is built specifically for the latest NVIDIA Hopper GPUs (like the H100 and H200). It uses the same core ideas but takes advantage of new hardware features to go even faster.

The key trick in Flash Attention 3 is asynchronous copy. In Flash Attention 2, the GPU still had to wait a little bit for each new K, V block to arrive from HBM before it could compute on it. Flash Attention 3 uses the H100's Tensor Memory Accelerator (TMA) - a special hardware unit that moves data in the background while the tensor cores keep doing math at the same time. This overlap means the GPU is almost never waiting - it is always computing.

Since Flash Attention 3 needs the latest Hopper GPUs, Flash Attention 2 is still the most widely used version today - most developers are still on A100s or consumer cards like the RTX 3090 and RTX 4090. Flash Attention 3 is strictly for the H100 and H200 generation, where it is the fastest option available. That's the beauty of it - as GPUs keep evolving, Flash Attention keeps getting better along with them.

## Advantages of Flash Attention

Let's understand why Flash Attention has become the default in almost every modern LLM:

Much faster: Flash Attention is typically 2x to 4x faster than standard attention for long sequences. The longer the sequence, the bigger the speedup.

Much less memory: Memory usage drops from O(N²) to O(N). This means we can train models on much longer sequences using the same GPU.

Exactly the same result: Flash Attention is not an approximation. The output is exactly the same as standard attention. There is no quality loss.

Enables long context windows: Before Flash Attention, processing very long inputs (like a 100,000-word document) was extremely expensive because the attention matrix was too large to fit in memory. Flash Attention makes this possible by never creating the full matrix. This is one of the key reasons modern LLMs can handle very long conversations and documents.

Drop-in replacement: Flash Attention works with the same Q, K, V interface as standard attention. We can replace standard attention with Flash Attention without changing anything else in the model.

Used everywhere in modern AI: Today, almost every serious LLM training run and inference engine uses Flash Attention or one of its successors (Flash Attention 2, Flash Attention 3). It has quietly become one of the most important pieces of infrastructure in modern AI. One such inference engine is vLLM, and we have a detailed blog on how vLLM works that explains LLM serving in depth. NVIDIA ships the same fused-kernel idea inside TensorRT-LLM as its custom attention kernels.

I personally believe that Flash Attention is one of the most elegant pieces of systems engineering in modern AI. It takes the same math, keeps the same result, and still makes everything run much faster - that too on the same hardware. It makes our life easier.

## Quick Summary

Let's recap what we have decoded:

- Flash Attention computes the exact same attention as standard attention, just in a much smarter way on the GPU.
- Standard attention is slow because it creates a giant N×N matrix in slow HBM and moves it back and forth many times.
- GPUs have two memory types: HBM (large but slow) and SRAM (small but very fast). Data movement between them is the real bottleneck.
- Tiling breaks Q, K, and V into small blocks that fit in SRAM, so the giant matrix is never materialized.
- Online softmax lets us compute softmax block by block by tracking a running max, running sum, and running output.
- Recomputation in the backward pass trades a little extra compute for huge memory savings.
- The result is the same as standard attention - just much faster and lighter.
- Flash Attention 2
