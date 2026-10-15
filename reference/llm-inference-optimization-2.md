> Source: https://www.youtube.com/watch?v=jV2sCj4lHYk

# LLM Inference Optimization
URL: https://www.youtube.com/watch?v=jV2sCj4lHYk
Author: Outcome School

The recording has started, and in this
video we will discuss LLM inference optimization. As you can see right now
on the screen, I have written a blog. In this, I have mentioned all the blogs
which I have written on LLM inference optimization. So first, let's try to
understand what exactly this is, right. So when you type something in ChatGPT
or whatever platform that you use, the request goes from the client, your
browser is the client, or whatever app you are using, to the server. So in that
request, whatever you have prompted will go to the server, and the server
will take that prompt, do some processing, like adding some system prompt or
whatever is there, or the user preferences. Then they will feed that into the LLM,
and the LLM will give some output. So we need to optimize those things so
that the user can get the response as soon as possible. So if you have to wait
a lot of time, the user experience will not be good. So from that perspective, we
must optimize the LLM inference time so that we can serve the user quickly, and
that will bring the best experience for the users. So this is all about
inference, why we need to do that. So now, there are a lot of techniques
that people have already implemented, there in the public domain. So the first
technique that came is the KV cache. It has been implemented by many
libraries that are used for solving the LLM inference. So this is by
default, actually. So whatever I am discussing today, they
are by default now, because everyone knows that. So these are the techniques,
things that improve the LLM inference time by a lot. So this first one
is the KV cache in the LLM, right. So here I will tell you in short; in
detail, you can go through this blog, which I have written here. Everything is
there, examples, everything, so you can go through this and learn a lot, in
detail, about all these optimizations. So it is completely up to you to go
through the blog and learn things in detail. That I will highly
encourage you to do. So in KV cache, what happens is that in
the LLM, which is built on the Transformer architecture. In the Transformer architecture, there
are two major things. One is the attention layer, another is
the feed-forward network. So for the KV cache, we need to focus
on the attention layer. In the attention layer, we have
three things: K, V, and the Q. So Q is not in the picture for this
discussion. So KV, you must have heard of it, K, Q, V, something like that.
So we have K and V in that attention layer. So that K and V is calculated
every time when you give the prompt. So, for example, you said "I love", so
it has to predict "AI", or it has to predict "teaching". For example, "I love
teaching AI" is the complete sentence, and "I love" is the prompt.
So if I'm giving "I love" as a prompt, it has to predict "teaching". So to predict
"teaching", it has to calculate the KV for the "I love". Now the next prompt that
will be fed to the LLM is "I love teaching", so that it can predict "AI",
"I love teaching AI". So if you see the pattern here, every time the model is
outputting only one token, "teaching", and then "AI", and every
time we have to feed the previous, whatever we have predicted till now. So if you see
the pattern, for the "I love teaching", again and again we are doing the
calculation, and that calculation happens for the KV. So we need to cache that, for
that particular window frame, so that we can keep on generating the next
token by reusing the previous computation that we have done. So these things, in
detail, you can learn when you go through this particular blog. So you can go
through it by clicking on that. Now there is something called Paged
Attention. So here, what happens is that because of
the KV cache, we will take a lot of memory to cache those things into the
memory, and there the memory will become the bottleneck. Now we need to optimize for that memory. It should not become a bottleneck,
because we implemented the KV cache to do some optimization, and again we
have come to a point where that is becoming a bottleneck. So we need to
solve that bottleneck as well, right. So here, what happens is, for
example, let's try to understand from an analogy. So what happens is, if you
create a KV cache of, for example, 2 MB, I'm just taking that as an example, but naturally, as memory that you get from the system,
that will be a block of 10 MB, right. And now what you can do is, in
that 10 MB you will store only the KV cache of 2 MB. So 8 MB will be wasted. Similarly, next time, if you create some
KV cache, and that is, for example, 4 MB, you will get the block size of 10 MB. So, because the system will give you in
blocks, right. It cannot give you the exact memory. So that is the restriction
the system has. So again, 6 MB wasted. Now, if you are caching, for example,
8 MB, then 2 MB is wasted. So like this, you will waste 70-80%
of the memory, of the overall thing. So because of that, they implemented
Paged Attention. Paged Attention means, at the software
level, they will write the code so that the 10 MB can be divided into 2 MB blocks, if needed, right. The 10 MB which is on the physical,
that is divided at the software level into 2 MB blocks, like five 2 MB blocks are
there. Earlier, we had only 10 MB blocks. Now, to do this, they have to create an
indexing as well, so they will write the address, from where to where this 2 MB
is allocated, from where to where this 2 MB is allocated. So like that, we will
have to write in that, just having a journal in association with the physical
10 MB. So we are able to divide that into five 2 MB chunks. Now, if you see
the pattern here, now the memory will not be wasted, I'm not saying 100% it will
not be wasted; it will be wasted, but now 5, 10, 20 percent, like that. Earlier,
we were wasting 70-80%. So this is the optimization that has been done in
Paged Attention. So this was all about Paged Attention. Again, you can go through
the Paged Attention blog, and you can read on the Outcome School blog. So after this
Paged Attention, we have something called Flash Attention in the LLM. So this also
I have in the blog, but I will try to simplify it with a simple
analogy, and for detail you can again go through the blog that we have linked here.
Now, in this, we have to consider that this optimization is happening at the GPU
level. So here we have something called HBM and the SRAM. Again, with the analogy,
this is a bigger memory that can do a lot of operations at a time, because that is a
very big memory. For the bigger calculation we can feed a bigger matrix for the
calculation, and here this is a smaller one which is faster. So, just for simplicity:
this is a bigger one which is very slow, very, very slow; this is a smaller one
which is very, very fast. But when you talk about this research paper,
"Attention Is All You Need", which implements the Transformer layer, so
there we have the attention layer. So in this case, we have a lot of information
about the matrix, and we have to do a lot of calculations on the smaller one, and on the bigger matrix as well. So for
that, definitely you need this at once, but with the experiment, people have found
that doing the bigger calculation
versus doing a lot of smaller matrix calculations on
the smaller one, because here we will have to-and-fro, because we will divide
our bigger matrix into smaller, smaller matrices, and then we need to club that
as well, because ultimately we need the calculation on the bigger one. But the
nature of matrix calculation is that you can actually do that in chunks. So
doing that in chunks, although having to-and-fro with the smaller memory, which
is faster, that is actually coming out to be better than doing something bigger on
the bigger memory. So that is what people have
implemented now, and in that there are two concepts which are called tiling and the
online softmax. So you can go through those, those are the two
important concepts. After that, this has evolved over the period,
Flash Attention 2 and 3. We have the research paper on that as well, right,
so you can go through. So now, after this, we were introduced to Grouped Query
Attention. And if I am correct, I think I have read this in the DeepSeek research
paper that they had published back then. So in this, we need to learn the evolution
first. So in this paper, if you see, "Attention Is All You Need", so in this
Transformer architecture, if you see, we have the Multi-Head Attention. So that was
the original attention head. So in this, for every query you need one key and one
value: Q1, K1, V1, Q2, K2, V2, like that, we need. Now
what people have done is that they implemented Multi-Query Attention.
So in this, you need, for one query, Q1, you will have the K and the V. For
another query as well, Q2, you will have the same K and V. So if you observe here,
key and value are shared for all the query. If you have 100 queries, Q1, Q2, Q3, Q100,
for all of them K and V are the same, right. So that is why we call it
Multi-Query Attention. Now the next one is Grouped Query Attention, that is something
we need to talk about. Grouped Query means: for multiple queries, you will have one
key and one value. Then, again, for the next multiple set of
queries, we will have the same K and V. So we are grouping the query, that is why the
name is Grouped Query. So for so many queries, not for all the query. So
let's say we have 100 queries; for query one to ten we will have a K and V; for
another 11 to 20 we will have some different K and V. So here we are not
having K and V the same for all the query, but we are doing the grouping here. So if
you see, if you have completely different Q, K, and V, you will have the best output
from the model, definitely, but you are doing a lot of operations and taking a lot
of memory, right. So then, if you introduce this, you will lose on accuracy,
because the same K and V is shared for all the queries, right. So we need to
find a balance, and this is the balance that
I am talking about. So this is a balance: for multiple queries we will have the same KV, then again for
the next multiple set of queries we will have the same K and V. And that is
what this Grouped Query Attention has done, right. So that is the accuracy,
that is a balance, right, a balance of accuracy plus a balance of the
computational and memory required for that, right. So that is a great optimization,
and this is how we find the solution by going through the hybrid approach. So I will recommend, in every domain,
whatever you are working on, try to find that balance, where the trade-off is, and
what optimization we can do, right. So this was all about Grouped
Query Attention. And after this, we have something called Speculative Decoding. So here, again, we need to find a better
solution to optimize for LLM inference. So here, what we do is, we will have
two models. One is the larger model, which is called
the target model; another is the smaller model, which is the draft model. The bigger model that we have will
definitely give you the best output with the best accuracy, but it will take a lot
of time, because that model is a very big model, a larger model. Now, if you have a smaller model, that
will take very little time, and less time is good for a better user experience.
But with less time, you cannot give random things to the user. So for that you
need to verify whether that smaller model is giving you something better or not,
because a smaller model is definitely not good at accuracy. The correctness will
go down because of the smaller model. So that is why we will find a smaller
model that is good enough to predict, but at the
same time we will use the larger model to verify what the smaller model is doing,
right. So here we find a balance: we use the larger model to verify. The
good thing is that we are able to optimize for time, and at the same time
we are able to optimize for the correctness, the accuracy, as well. So how do we do that? The smaller model will keep on generating. So let's say the smaller model
has to generate 100 tokens. So we can write the code that
after every 10 tokens we will verify, because if we try to verify each token,
again the larger model will take the same time for the user. They will verify the same token, so that
we will not do. Instead, we will verify in batches, and that is a technique that is
helping here. The main technique is that verifying in batches from the larger
model, because the larger model can verify in parallel. So there is one concept that
I want you to learn from here, which is that verification can happen in parallel,
but generation cannot, because once you have to generate the next token,
you must know the previous token, right. I cannot just say "I
love AI". If I have to say "I love teaching AI",
"I love teaching AI" should come in sequence. First, if I am giving the
prompt, "I love teaching" should come, then only "AI" should come. "AI" cannot
come without "teaching" here, right. So that is how the generation cannot
happen in parallel, but verification can happen in parallel. That is why this
thing is applicable and working: the larger model can verify in parallel. Now,
if the larger model finds that, okay, after seven tokens you have made some mistake,
seven tokens will be accepted, and the next eight, nine, ten will be regenerated by
the smaller model. So like that, this optimization will be done. So you can again
learn about this in detail from my blog, or you can join Outcome School to learn
all these things. Okay. So after this, we have something called
Continuous Batching, and this is also an interesting topic, right. So in this, what
happens is that let's say, on the server, you are
getting 10 requests, right. So you can do this so that you can batch
all the requests and feed into the GPU, right. So that is called static batching.
I'll discuss it in detail, right. So, but we need to move from static
batching to continuous batching. So we must understand static batching. So when 10
requests came, we batched all the requests, fed them into the GPU. Now the
GPU has to finish all the 10 requests; then only can it take the 11th
one, then only can it take the 11th one. So that is the bottleneck here,
because one user response can be very big, another user response could be very small.
So for the smaller one also, right, we can definitely serve the user quickly,
right. So that is not the question here. But when we have already served the
smaller request, that GPU slot, that GPU slot is free now,
right, sitting idle, because we have fed everything in static batching.
So we can implement a logic that all the 10 requests will go, 10 GPU slots they
will take, and till everything is not done, we cannot feed the next one, right. So even though a couple of requests have
already been finished, slots are free, GPU is sitting idle. We are not utilizing that GPU, right. So what we will do is implement a logic on
the server side that, as soon as the request is finished, we will feed, we will
not let the GPU sit idle at any point in time, as much as possible, right. So that is what continuous batching is.
Static batching means we batched and we are waiting for the last request to finish.
Continuous means we have batched. We are doing the continuous batching, means we
will not allow, we will not allow the GPU to sit idle at any point in time,
right. So that is the meaning of continuous
batching. Again, go through the blog and read about it in detail, and I highly
encourage everyone to read in detail, learn the entire internal, become the best
at what you do, right. You need to learn the internals, then only
can you actually do something great in your life, right. So after this, we have
something called Prompt Caching. So this is also another
interesting topic that we must know. All the topics are interesting that we have
discussed today. And I will encourage everyone to learn the internals as much as
possible. Your knowledge, and taking action on the knowledge, is very, very
important. Don't just learn; go and try to experiment with all these things. Use any
coding agent that you already have, or you can take any coding agent and you can try
experimenting with all these things whatever I am discussing here, right. Learn a blog a day, right. So that is
something I will encourage everyone, it's like "an apple a day keeps the doctor
away", right. Similarly, you need to read a
blog a day, regularly. Daily morning, open Outcome School. Click on the blog section, right. Read one blog. Read one blog. That's it, and I can guarantee that
within six months you will be ahead of 99.9999% of the people present on
this planet Earth, right. That is 100% guaranteed. This is something
that will happen for sure, 100%. This will happen right now. Prompt Caching. So here, what happens is
that we will have the prompt coming from the user on the
server, and we already know that for everything we
calculate the KV, right, key and value we calculate. So let's say every user is
saying "I love teaching"; so for "I love teaching", we should cache the KV
across the user, right. So that KV should be cached so that we can
use it for another user as well, right. Or, for example, that user is you, saying "I
love teaching", and after that the conversation is getting continued, right. So all the tokens, the previous token,
the previous prompt, is being cached already, right. So the prompt should be
cached, and there are multiple levels of caching that can be done, like on the user
level, on the application level, right. So, for example, everyone starts with for example a system prompt: "You are a
coding assistant. You are going to help me with better coding and
code review", right. For example, the server adds this prompt
as a system prompt in every prompt, right. So for that, KV should be cached, so we
can say that in every prompt, if you are adding some instruction and the system
prompt like that, right. So they are already a static thing, so
they will not change for any user, for that particular product, for example, right. So we can cache the KV of those things. So that is what we call prompt caching.
And this is a very interesting concept that people have implemented on the server
side to serve the user quickly. And this is all about LLM
inference optimization. Again, you can go through
this blog and learn everything about it, right. So here you
can see that I have mentioned what people are doing in this, how they are
optimizing, right. So decode-prefill is one of the concepts
that you can go through, right. I have already put one video about the
decode and prefill; you can check it on the YouTube channel of this Outcome
School, right. So something will be there, like why the
first token is slower than other tokens, so that video you can check right now. So
this blog I will link in the description as well, and you can go through all these techniques and learn effectively. That will
put you ahead of all the developers out there in the market, right. Put your
effort, grow, and learn, right. So that is very,
very important for all of us. So that's it for now. I will see you in
the next video soon.

# 5 LLM optimization techniques. Let's understand each of them. | Pallavi .
URL: https://www.linkedin.com/posts/pallavi-shekhar_5-llm-optimization-techniques-lets-understand-activity-7442067281532325888-4aOS
Published: 2026-03-24
Author: Pallavi .

# 5 LLM optimization techniques. Let's understand each of them. | Pallavi . · LinkedIn · 2026-03-24

**Pallavi .**: Software Engineer at Outcome School with 8 years 1 month of experience. Previous roles include Senior Software Development Engineer at West Agile Labs, Software Engineer at NCR Corporation, and Software Engineer at Deloitte India (Offices of the US). Based in Bengaluru, Karnataka, India [IN].

---

5 LLM optimization techniques.

Let's understand each of them.

Quantization - It reduces the precision of model weights from 32-bit to 8-bit or 4-bit. This makes the model smaller and faster with very less impact on quality. It is one of the most commonly used techniques.

Pruning - It removes the weights or neurons that contribute very less to the output. Think of it as trimming the unnecessary parts of the model to make it lighter and faster.

[…551ln elided…]

Now, the question is, how do we tell the GPU what work to do? The answer is: by writing a kernel.

## What is a CUDA Kernel?

A CUDA Kernel is a function that runs on the GPU, and it is executed by many threads at the same time.

Let's break this down.

A function is just a piece of code that does one job. We must be knowing this from any programming language.

A thread is one worker that runs the code. In simple words, a thread is one helper from our kitchen example.

So, CUDA Kernel = Function + Runs on GPU + Executed by thousands of threads together.

Here is the most important idea, and I want you to remember this:

We write the kernel once, as if it is for a single thread. Then the GPU runs that same kernel thousands of times in parallel, once per thread.

Let's go back to the kitchen. We do not write 5,000 different instructions for 5,000 helpers. We write one instruction: "Pick up a potato and peel it." Then all 5,000 helpers follow the same instruction at the same time. The only difference is, each helper picks up a different potato.

That is exactly how a CUDA Kernel works. One instruction, thousands of workers, and each worker handles a different piece of data.

Now, we have understood what a CUDA Kernel is.

## Threads, Blocks, and Grids

Now, if we have thousands of threads, we need some way to organize them. Otherwise, it will be a mess. CUDA organizes threads in three levels.

- Thread: A single worker. It runs the kernel code once.
- Block: A group of threads. Let's say 256 threads in one block. Threads inside the same block can talk to each other and share a small amount of memory.
- Grid: A group of blocks. All the blocks together make up one kernel launch.

So, Grid = Many Blocks, and Block = Many Threads.

Let's understand this with our kitchen.

- A thread is one helper.
- A block is one team of helpers standing at one table. They can pass things to each other easily because they are at the same table.
- A grid is the whole kitchen with all the tables.

When we launch a kernel, we tell CUDA two things: how many blocks we want, and how many threads we want in each block. CUDA then creates all those threads and runs the kernel on each one.

Note: There is a limit on how many threads can be in one block, usually 1024. That is why we use many blocks. There is no practical limit on the number of blocks, so we can have millions of threads in total.

Now that we have learned how threads are organized, it's time to learn how the CPU and the GPU talk to each other.

## Host and Device

Before writing the code, we need to understand two words that we will see everywhere in CUDA.

- Host: The CPU and its memory (RAM, the main memory of the computer).
- Device: The GPU and its own memory (VRAM, the memory that sits on the graphics card itself).

The host and the device have separate memory. For the sake of understanding, assume that the CPU cannot directly read the GPU memory, and the GPU cannot directly read the CPU memory. So, whenever we want the GPU to work on some data, we must copy that data from the host to the device. And when the work is done, we must copy the result back from the device to the host.

Means, a CUDA program always follows these steps:

Step 1: Prepare the data on the host (CPU).

Step 2: Allocate memory on the device (GPU). Allocate just means reserve some space for our data.

Step 3: Copy the data from host to device.

Step 4: Launch the kernel on the device.

Step 5: Copy the result from device back to host.

Step 6: Free the device memory, which means give the reserved space back.

Think of it like this. The master chef (CPU) has all the potatoes in the store room. The helpers (GPU) work in a different room. So, the chef must carry the potatoes to the helpers' room, let them peel, and then carry the peeled potatoes back. The carrying takes time, and we will see later why this matters.

## Writing our first CUDA Kernel

The best way to learn this is by taking an example.

Let's say we have two lists of numbers, `a` and `b`, each with one million numbers. We want to add them and store the result in a third list `c`. Means, `c[i] = a[i] + b[i]` for every position `i`.

First, let's see how we do this on a CPU without CUDA:

```c
void add(int n, float *a, float *b, float *c) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

```

Here, we have a function named `add`. The word `void` means the function does not return anything. `float` means a number with a decimal point, and `float *a` means a list of such numbers. Inside, we have a loop that goes from `0` to `n - 1`. In each step, it adds one pair of numbers. For one million numbers, this loop runs one million times, one after another. One master chef, one potato at a time.

Now, let's see the same thing as a CUDA Kernel:

```c
__global__ void add(int n, float *a, float *b, float *c) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

```

Here, we can notice a few things:

- `__global__` is a special keyword. It tells CUDA that this function is a kernel. It will be called from the host (CPU) and will run on the device (GPU).
- One more thing to notice, the loop is gone. There is no `for` loop anymore. Each thread handles only one `i`. The GPU will run this function one million times in parallel, once for each thread, and each thread will take care of one position.
- `int i = blockIdx.x * blockDim.x + threadIdx.x;` is how each thread finds out which `i` it is responsible for. Do not worry, we will understand this line in detail in the next section.
- `if (i < n)` is a safety check. Sometimes we launch a few more threads than the number of items. This check makes sure the extra threads do nothing.

This is the whole kernel. Just a few lines. And it does the work of one million loop iterations at once.

Now, let's see how we launch this kernel from the host (CPU):

```c
int n = 1000000;
int threadsPerBlock = 256;
int blocks = (n + threadsPerBlock - 1) / threadsPerBlock;

add<<<blocks, threadsPerBlock>>>(n, d_a, d_b, d_c);

```

Here, we have:

- `threadsPerBlock = 256` means each block will have 256 threads.
- `blocks = (n + threadsPerBlock - 1) / threadsPerBlock` calculates how many blocks we need to cover all one million numbers. This formula is just a trick to round up. For one million numbers and 256 threads per block, we get 3907 blocks. 3907 multiplied by 256 gives 1,000,192 threads, which is a little more than one million. That is why we needed the `if (i < n)` check inside the kernel.
- `<<<blocks, threadsPerBlock>>>` is the special CUDA syntax for launching a kernel. The three angle brackets tell CUDA: "Run this function with this many blocks and this many threads per block."
- `d_a`, `d_b`, `d_c` are the addresses of our data in the device memory. In simple words, they tell the kernel where the data lives on the GPU. The `d_` prefix is just a naming convention that means "device". We copied our data there before calling the kernel.

Let's see the complete flow with the memory steps we discussed earlier:

```c
// Step 1: a, b, and c are already prepared on the host

// Step 2: Allocate memory on the device
float *d_a, *d_b, *d_c;
cudaMalloc(&d_a, n * sizeof(float));
cudaMalloc(&d_b, n * sizeof(float));
cudaMalloc(&d_c, n * sizeof(float));

// Step 3: Copy data from host to device
cudaMemcpy(d_a, a, n * sizeof(float), cudaMemcpyHostToDevice);
cudaMemcpy(d_b, b, n * sizeof(float), cudaMemcpyHostToDevice);

// Step 4: Launch the kernel
add<<<blocks, threadsPerBlock>>>(n, d_a, d_b, d_c);

// Step 5: Copy result from device to host
cudaMemcpy(c, d_c, n * sizeof(float), cudaMemcpyDeviceToHost);

// Step 6: Free the device memory
cudaFree(d_a);
cudaFree(d_b);
cudaFree(d_c);

```

Here, we have:

- `cudaMalloc` reserves space in the GPU memory. In simple words, it tells the GPU: "Keep this much space ready for my data."
- `cudaMemcpy` copies data between host and device. The last argument tells the direction: `cudaMemcpyHostToDevice` or `cudaMemcpyDeviceToHost`.
- The kernel launch line is the same as before.
- `cudaFree` releases the GPU memory once we are done.

It works perfectly. All one million additions are done in parallel by the GPU.

Note: CUDA code is saved in a file with the `.cu` extension and compiled using a special tool from NVIDIA called `nvcc`. It understands both the normal C++ code for the host and the kernel code for the device.

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

## How a thread finds its own work

Now, let's understand the most important line in our kernel:

```c
int i = blockIdx.x * blockDim.x + threadIdx.x;

```

Remember, every thread runs the exact same code. So, how does each thread know which number to add? The answer is: CUDA gives every thread some built-in variables that tell it where it is. These variables are called indexes, and index just means the position number, starting from 0.

- `threadIdx.x` is the index of the thread inside its block. If a block has 256 threads, this goes from `0` to `255`.
- `blockIdx.x` is the index of the block inside the grid. If we have 3907 blocks, this goes from `0` to `3906`.
- `blockDim.x` is the number of threads in each block. In our case, it is `256`.

So, the global index `i` is calculated as below:

`i = (block number) * (threads per block) + (thread number inside the block)`

Let's take an example for the sake of understanding.

- Thread 0 in Block 0: `i = 0 * 256 + 0 = 0`
- Thread 5 in Block 0: `i = 0 * 256 + 5 = 5`
- Thread 0 in Block 1: `i = 1 * 256 + 0 = 256`
- Thread 10 in Block 2: `i = 2 * 256 + 10 = 522`

Every thread gets a unique `i`, and no two threads get the same `i`. This is how the same code, running on thousands of threads, works on different data.

Let's go back to the kitchen one last time. Every helper has a table number (`blockIdx`) and a seat number at that table (`threadIdx`). Each table has 256 seats (`blockDim`). So, a helper at table 2, seat 10 knows that the potato to pick is number 522. The helper does not need to ask anyone. The helper just calculates it and picks up potato number 522.

Note: We used `.x` everywhere because CUDA allows threads and blocks to be arranged in one dimension (like a line), two dimensions (like a grid on paper), or three dimensions (like a cube). For a simple list, one dimension is enough. For an image or a matrix, two dimensions are natural, and we would also use `.y`. The idea remains the same.

Now, we have understood how a thread finds its own work.

## What happens inside the GPU when a kernel runs

Till now, we have learned how to write and launch a kernel. Now, let's see what the GPU actually does with it.

A GPU is made of many Streaming Multiprocessors (SMs). In simple words, an SM is one big work unit inside the GPU that contains many small cores. A modern GPU can have more than 100 SMs.

When we launch a kernel with 3907 blocks, CUDA does not run all of them at once. It distributes the blocks to the SMs. Each SM takes a few blocks, finishes them, and then takes the next few. This continues until all the blocks are done.

Inside an SM, threads do not run one by one either. The SM groups threads into bunches of 32, and this bunch is called a warp. All 32 threads in a warp execute the same instruction at the same moment. That is why CUDA is so fast. One instruction is fetched once and applied to 32 threads together.

Let's connect this to our kitchen. The kitchen (GPU) is divided into many sections (SMs). Each section handles a few tables (blocks) at a time. At every table, the helpers (threads) are organized in rows of 32 (warps). The head of the table says one instruction, "peel", and all 32 helpers in a row do it together.

But, here is the catch. Because all 32 threads in a warp must run the same instruction, if our kernel has an `if` condition and some threads go one way and some go the other way, the warp has to run both paths one after another. This is called warp divergence, and it slows things down. That is why good CUDA kernels try to keep the threads doing the same thing as much as possible.

Note: Our `if (i < n)` check causes divergence only in the very last block, so it is not a problem in practice.

To learn LLM Inference Engineering and LLM Inference Bottleneck Analysis, which build directly on how the GPU runs our work, check out our AI and Machine Learning Program at Outcome School.

## Memory in CUDA

We have already seen that the host and device have separate memory. Now, let's look inside the device memory, because this is where most of the performance comes from.

There are three main types of memory in a GPU that we must know about:

- Global Memory: This is the big memory of the GPU (the VRAM, let's say 24 GB or 80 GB). All threads can read and write it. This is where `d_a`, `d_b`, and `d_c` live. It is large but slow, because it is far from the cores.
- Shared Memory: This is a small, very fast memory inside each SM. Only the threads of the same block can use it. It is like a whiteboard at each table that all helpers at that table can see and write on.
- Registers: These are the fastest memory of all, and each thread gets its own. Our variable `i` lives in a register. It is like the notepad in each helper's hand.

Global memory is around 100 times slower than shared memory. So, a common trick in CUDA programming is: load a chunk of data from global memory into shared memory once, let all the threads in the block work on it many times from shared memory, and then write the result back to global memory.

For our simple addition example, each number is used only once, so shared memory does not help. But for matrix multiplication (multiplying large tables of numbers, which we will see in the next section), where the same numbers are used again and again, this trick makes a huge difference. We have a detailed blog on Flash Attention that explains how this exact trick makes attention in LLMs much faster.

This was all about the memory in CUDA. Now, let's connect all of this to AI.

## Why CUDA Kernels matter for AI

An AI model, like an LLM (Large Language Model, the kind of model behind ChatGPT), is basically a very large collection of numbers called weights. When we give it an input, the model multiplies the input with those weights, adds them up, applies a few simple mathematical functions, and repeats this many times across many layers. Almost everything inside an AI model is matrix multiplication, which means multiplying and adding large tables of numbers.

A matrix multiplication with millions of numbers is the perfect "peeling potatoes" problem. Every output number can be calculated independently. So, we write one CUDA kernel for matrix multiplication and launch it with millions of threads.

When we use a library like PyTorch (a popular tool for building AI models) and write `torch.matmul(a, b)`, we are not writing any CUDA code ourselves. But behind the scenes, PyTorch calls a highly optimized CUDA kernel written by NVIDIA. These kernels come from NVIDIA libraries like cuBLAS, which is a collection of ready-made kernels for math operations. They do exactly what we learned today, but with many more tricks for speed. We have a detailed blog on how TensorRT-LLM works that covers how NVIDIA fuses and tunes these kernels to run an LLM as fast as possible.

So, every time an LLM generates a word, thousands of CUDA kernels are launched on the GPU, one after another. Every step inside the model, whether it is a big matrix multiplication or a small mathematical function, is a CUDA kernel. This is why we cannot imagine modern AI without GPUs and CUDA.

If we want to go deep into PyTorch and the math inside an LLM, and build a Large Language Model (LLM) from scratch, our AI and Machine Learning Program at Outcome School covers it end to end.

## Where CUDA Kernels work well and where they fail

CUDA Kernels work well when:

- The same operation has to be done on a large amount of data, like matrix multiplication, image processing, and scientific simulations.
- The calculations for different pieces of data do not depend on each other.
- The amount of work is big enough that the time saved is more than the time spent copying data between host and device.

CUDA Kernels fail or do not help when:

- The task is small. Copying 10 numbers to the GPU and back takes more time than adding them on the CPU. Carrying potatoes to the other room is not worth it for 10 potatoes.
- The work is sequential. If step 2 needs the result of step 1, and step 3 needs the result of step 2, then thousands of threads cannot help. Only one thread can work at a time.
- The threads keep taking different paths. Heavy branching causes warp divergence, and the GPU ends up doing things one by one.
- The data is too big for the GPU memory. Then we have to keep moving data in and out, and the copying becomes the bottleneck.

Let me tabulate the differences between CPU and GPU for your better understanding.

| CPU | GPU |
| --- | --- |
| Few powerful cores, let's say 4 to 64 | Thousands of small cores |
| Great at doing one task after another | Great at doing the same task on lots of data at once |
| Good for logic, decisions, and running the operating system | Good for math on big lists and tables of numbers, graphics, and AI |
| No copying needed, data is already in RAM | Data must be copied to the GPU and back |

So, we must choose between the CPU and the GPU based on our use case.

## Summary

Let's summarize what we have learned.

- A GPU has thousands of small cores that work at the same time. It is built for doing the same operation on a lot of data.
- CUDA is the platform from NVIDIA that lets us write programs for the GPU.
- A CUDA Kernel is a function that runs on the GPU and is executed by thousands of threads in parallel.
- We write the kernel once, for a single thread. The GPU runs it thousands of times, and each thread finds its own piece of data using `blockIdx`, `blockDim`, and `threadIdx`.
- Threads are organized into blocks, and blocks are organized into a grid.
- The host (CPU) and the device (GPU) have separate memory, so we allocate, copy, launch, copy back, and free.
- Inside the GPU, blocks run on SMs, and threads run in warps of 32.
- Global memory is big but slow, shared memory is small but fast, and registers are the fastest.
- Almost every operation in an AI model is a CUDA kernel running behind the scenes.

This is how CUDA Kernels work.

### Do we need to write CUDA code to use a GPU with PyTorch?

No. When we write `torch.matmul(a, b)` in PyTorch, we do not write any CUDA code ourselves. Behind the scenes, PyTorch calls a highly optimized CUDA Kernel written by NVIDIA, from libraries like cuBLAS, which is a collection of ready-made kernels for math operations.

### Why does a CUDA Kernel need the if (i < n) check?

Because we often launch a few more threads than the number of items. The number of blocks is rounded up, so for one million numbers and 256 threads per block, we get 3907 blocks and 1,000,192 threads. The `if (i < n)` check makes sure the extra threads do nothing.

### How many threads can one CUDA block have?

Usually up to 1024 threads. That is why we use many blocks in one kernel launch. There is no practical limit on the number of blocks, so a single kernel can run millions of threads in total.

### What is warp divergence in CUDA?

Warp divergence happens when threads in the same warp take different paths in an `if` condition. All 32 threads in a warp must run the same instruction, so the warp has to run both paths one after another, and this slows things down. Good CUDA Kernels keep the threads doing the same thing as much as possible.

### How is CUDA code compiled?

CUDA code is saved in a file with the `.cu` extension and compiled using `nvcc`, a special tool from NVIDIA. It understands both the normal C++ code for the host (CPU) and the kernel code for the device (GPU).

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

[Showing lines 1-269 and 821-1157 of 1157; 551 middle lines (29.5KB) elided. Read artifact://60 for full output]
