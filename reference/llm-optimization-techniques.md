> Source: https://www.linkedin.com/posts/pallavi-shekhar_5-llm-optimization-techniques-lets-understand-activity-7442067281532325888-4aOS

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

Knowledge Distillation - We train a smaller model (student) to mimic the behavior of a larger model (teacher). The student learns the patterns from the teacher and becomes efficient enough for production use.

KV Cache - During text generation, the model recomputes attention for all previous tokens at each step. KV Cache stores the key-value pairs so that we do not recompute them. This significantly reduces latency. Also, we add Paged Attention on top of it.

Speculative Decoding - A smaller and faster model generates candidate tokens, and the larger model verifies them in parallel. This speeds up generation because verification is faster than generation.

These techniques help us deploy LLMs efficiently without compromising much on quality.

5 LLM optimization techniques. Let's understand each of them. | Pallavi . image

## Comments

**Shashikant pandey** · 2026-03-24
> Absolutely right but Every technique trades off something.

**AMIT SHEKHAR** · 2026-03-24
> Follow for knowledge-packed content.

## Engagement

- Reactions: 24

# How does a GPU work for Deep Learning?
URL: https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning
Published: 2026-07-03
Author: Amit Shekhar

How does a GPU work for Deep Learning?

# How does a GPU work for Deep Learning?

Authors
: - Name
: Amit Shekhar
Published on
: July 3, 2026

A GPU works for Deep Learning by doing a huge number of simple calculations at the same time. Deep learning is mostly matrix multiplication, which can be split into many small parallel calculations, so the GPU makes it very fast.

In this blog, we will learn about how a GPU works for Deep Learning. We will also see why the GPU is perfect for deep learning, how they do so much math at the same time, and why companies like NVIDIA power almost all of modern AI.

We will cover the following:

- What is a GPU?
- Why is the GPU perfect for deep learning?
- CPU vs GPU
- The math professor and the thousands of students
- Why deep learning is mostly matrix multiplication
- Serial work vs parallel work
- GPU memory (VRAM) and memory bandwidth
- Why the model must fit in VRAM
- Tensor Cores and lower precision (FP16, BF16, INT8)
- CUDA and the software stack (cuDNN)
- Training vs inference on GPUs
- Multiple GPUs working together
- Why NVIDIA GPUs power modern AI

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a GPU?

A GPU is a special chip inside a computer that is very good at doing a huge number of simple calculations at the same time.

GPU stands for Graphics Processing Unit. As the name says, it was first made to draw graphics, like the images in video games.

Let's think about why graphics need so much calculation. A screen is made of tiny dots called pixels. A normal screen has millions of these pixels. To draw a game, the computer must decide the color of each one of these millions of pixels, many times every second.

That is a huge amount of work. But here is the interesting part. Each pixel can be calculated on its own, without waiting for the others. They are independent.

So, engineers built a chip that could do millions of small, independent calculations together. That chip is the GPU.

Later, people noticed something. Deep learning needs exactly the same kind of work. It also needs millions of small, independent calculations done at the same time. So, the GPU, which was made for games, became the heart of modern AI.

### Why is the GPU perfect for deep learning?

Before we go deeper, let us quickly remember what deep learning is.

Deep learning is a way of teaching a computer to learn patterns from data using something called a neural network.

In simple words, a neural network is a big collection of numbers, called weights, that get adjusted again and again until the computer starts giving correct answers.

Now, the important question is: what does a neural network actually do with these numbers?

The answer is simple. It does a lot of multiplication and addition. That is the main work, repeated millions and millions of times.

A CPU can do this work too, but it does it slowly because it does only a few calculations at a time. A GPU can do thousands of these calculations at the same time.

So, here comes the GPU to the rescue. It is built for exactly the kind of work deep learning needs.

To understand this clearly, we must first understand the difference between a CPU and a GPU.

### CPU vs GPU

A CPU is the main brain of a computer. CPU stands for Central Processing Unit.

A CPU has a small number of very powerful cores. A core is the part that actually does the calculation. A normal laptop CPU has something like 4, 8, or 16 cores.

Each CPU core is very smart and very fast. It can handle complicated tasks, make decisions, and switch between many different jobs quickly. This is why the CPU runs our operating system, our apps, and almost everything on the computer.

A GPU is different. A GPU has thousands of smaller, simpler cores.

Each GPU core is not as smart as a CPU core. It is not good at complicated decision-making. But it is very good at doing one simple thing: multiply and add numbers. And because there are thousands of them, they can do thousands of these simple jobs all at the same time.

Let me tabulate the difference between a CPU and a GPU for your better understanding.

| Point | CPU | GPU |
| --- | --- | --- |
| Number of cores | A few (4 to 64) | Thousands |
| Power of each core | Very powerful and smart | Simpler |
| Best at | Complex tasks, decisions, running apps | Many simple calculations at once |
| Style of work | A few things, very fast | A huge number of things, together |

So, the CPU is built for a few hard jobs done quickly. The GPU is built for a massive number of easy jobs done together.

We can picture the two chips side by side as below:

```
        CPU                              GPU
+-------------------+      +-------------------------------+
|  +-----+ +-----+  |      | [] [] [] [] [] [] [] [] [] [] |
|  |Core | |Core |  |      | [] [] [] [] [] [] [] [] [] [] |
|  +-----+ +-----+  |      | [] [] [] [] [] [] [] [] [] [] |
|  +-----+ +-----+  |      | [] [] [] [] [] [] [] [] [] [] |
|  |Core | |Core |  |      | [] [] [] [] [] [] [] [] [] [] |
|  +-----+ +-----+  |      | [] [] [] [] [] [] [] [] [] [] |
+-------------------+      +-------------------------------+
   A few big cores              Thousands of small cores

```

Here, we can see that the CPU has a few large, powerful cores, while the GPU has thousands of small, simple cores packed together. The CPU's big cores are great for a few hard jobs, and the GPU's many small cores are great for a huge number of easy jobs done at the same time.

Now, the best way to understand this is by taking an example.

### The math professor and the thousands of students

Let's say we have a giant worksheet with one million simple sums on it. Each sum is something like `3 x 4` or `7 + 2`. Nothing hard. Just a million of them.

Approach 1: One math professor.

Imagine one brilliant math professor. This professor is extremely smart and very fast. The professor sits down and starts solving the sums one after another.

The professor is fast, but there is only one professor. So, even at high speed, solving one million sums one by one takes a long time.

This professor is like a CPU core. Very powerful, but it does the sums in a line, one after the other.

The issue with this approach is that one worker, however fast, still does the sums one at a time. Let's see how the next approach solves this issue.

Approach 2: Thousands of students.

Now imagine a big hall with thousands of school students. Each student is not as fast or as clever as the professor. But each student can easily do a simple sum like `3 x 4`.

We give one sum to each student. All of them solve their sum at the same moment. In one go, thousands of sums are done together.

This is like a GPU. Thousands of simple workers, all solving simple sums at the same time.

For one hard problem, the professor wins. But for a million simple sums, the thousands of students finish much faster, because they all work together.

This is the whole idea. Deep learning is exactly the second kind of problem. It is a giant pile of small, simple sums. So, the GPU, with its thousands of small workers, is the perfect tool.

But why is deep learning a giant pile of simple sums? Let us understand that now.

### Why deep learning is mostly matrix multiplication

This is the most important idea in the whole blog, so let us go slowly.

Inside a neural network, the numbers are not stored as a single long list. They are arranged in grids of numbers. A grid of numbers is called a matrix.

In simple words, a matrix is just numbers arranged in rows and columns, like a table.

For example, a small matrix looks like this:

```
[ 1  2 ]
[ 3  4 ]

```

A neural network takes the input data as a matrix, and it has its own weights stored as a matrix. To produce an answer, it combines these two matrices using an operation called matrix multiplication.

We do not need the full math. We only need to understand what matrix multiplication really is at heart.

Matrix multiplication is just a huge number of "multiply and add" steps.

To get one single number in the result, we multiply some numbers together and then add them up. That single small action is called a multiply-add. Then we repeat this for every position in the result.

Let me show a tiny example so it feels real.

Suppose we multiply these two matrices:

```
[ 1  2 ]     [ 5  6 ]
[ 3  4 ]  x  [ 7  8 ]

```

To get the top-left number of the result, we take the first row `[1, 2]` and the first column `[5, 7]`, then we do:

```
(1 x 5) + (2 x 7) = 5 + 14 = 19

```

That is one multiply-add chain for one position. We then repeat the same idea for the other three positions to fill the result.

Now, here is the key point. Each result position is calculated on its own. The top-left number does not need the top-right number. They are independent.

In a real neural network, these matrices are not 2 by 2. They have thousands of rows and thousands of columns. So, a single matrix multiplication can be millions of multiply-add operations, and all of them are independent.

Millions of small, independent multiply-add operations. This is exactly the worksheet of a million simple sums from our example. And we already know who is best at that kind of work. The GPU, with its thousands of cores, all working together.

This is why we keep saying it: deep learning is mostly matrix multiplication, and matrix multiplication is millions of small independent sums done at the same time.

To learn how neural networks turn data into these matrix multiplications, and even build a Neural Network from scratch, check out our AI and Machine Learning Program at Outcome School.

### Serial work vs parallel work

Now, let us put two important words clearly side by side.

Serial means doing things one after another, in a line. First finish one, then start the next.

Parallel means doing many things at the same time, together.

A CPU mostly works in a serial way for this kind of math. It is like the single professor. It does multiply-add number one, then number two, then number three. Even though each step is fast, doing millions of them in a line takes time.

A GPU works in a parallel way. It is like the thousands of students. It hands out thousands of multiply-add operations to its thousands of cores, and they all finish together.

Here is a simple picture of the difference:

```
CPU (serial):
  add 1 -> add 2 -> add 3 -> add 4 -> ... -> add 1,000,000

GPU (parallel):
  add 1 ---|
  add 2 ---|
  add 3 ---|---> all done together, in batches
  add 4 ---|
  ...   ---|

```

Because the multiply-add operations in matrix multiplication are independent, they are a perfect fit for parallel work. Nothing has to wait for anything else.

So, the GPU finishes the same mountain of math much faster than the CPU. That speed is exactly what deep learning needs, because training a model means doing this math billions of times over.

This is how the GPU turns days of work into hours, and hours into minutes.

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

### GPU memory (VRAM) and memory bandwidth

Doing the math fast is only half the story. The GPU also needs all those numbers close to it so it can work without waiting.

For this, a GPU has its own special memory called VRAM, which stands for Video Random Access Memory.

Put simply, VRAM is the GPU's own personal workspace. It is where the GPU keeps the numbers it is currently working on, such as the model's weights and the data being processed.

Think of it like a desk. The bigger the desk, the more papers we can spread out and work on at once. VRAM is that desk for the GPU.

Now, there is one more important word: memory bandwidth.

Memory bandwidth is how fast the GPU can move numbers between its memory and its cores.

Let's say we have a desk full of papers, but a very narrow door to bring papers in and out. Even with a big desk, work slows down because papers cannot move quickly. A wide door means papers move fast. Memory bandwidth is the width of that door.

GPUs are built with very high memory bandwidth. This means the thousands of cores never sit idle waiting for numbers. The numbers keep flowing in fast, and the cores keep working.

We can picture how the numbers flow inside the GPU as below:

```
+-----------------------------+
|   VRAM (the big desk)       |
|   weights + data live here  |
+-----------------------------+
              |
              |  memory bandwidth
              |  (how wide the door is)
              v
+-----------------------------+
|   Thousands of GPU cores    |
|   do the multiply-add math  |
+-----------------------------+

```

Here, we can see that the numbers sit in VRAM, the GPU's big desk, and then travel down to the thousands of cores through the memory bandwidth, the door. A wider door means the cores are fed faster and never wait, so the math keeps moving without pause.

So, two things matter for a GPU: how many calculations it can do, and how fast it can feed numbers to those calculations. A good GPU is strong at both.

### Why the model must fit in VRAM

This brings us to a very practical point that everyone working with AI runs into.

To train or run a model on a GPU, the model and its data must fit inside the VRAM.

Remember, VRAM is the GPU's desk. If the model is too big for the desk, we simply cannot spread it out to work on it.

Let's understand the size with a simple idea. Every weight in a neural network is a number, and each number takes up some space in memory. A large model has billions of weights. Billions of numbers take up a lot of space.

For example, a model with billions of weights can need many gigabytes of VRAM just to hold the weights. During training, it needs even more space to hold extra working numbers.

This is why we hear about GPUs with large VRAM, such as 24 GB, 40 GB, or 80 GB. The bigger the model, the more VRAM we need.

Note: This is also why very large models are split across many GPUs. One GPU's desk is not big enough, so several GPUs share the load. We will talk about multiple GPUs a little later.

So, when we choose a GPU for deep learning, we do not only look at its speed. We also look at how much VRAM it has, because that decides how big a model we can run.

### Tensor Cores and lower precision (FP16, BF16, INT8)

We now know the GPU has thousands of normal cores doing multiply-add operations. But GPU makers added something even better for deep learning.

These special units are called Tensor Cores.

A Tensor Core is a special unit inside the GPU built to do matrix multiplication even faster than a normal core.

In simple words, a normal core does a few multiply-adds at a time. A Tensor Core is designed to chew through a whole small block of matrix math in one shot. Since deep learning is mostly matrix math, Tensor Cores give a big speed boost.

To go even faster, Tensor Cores use something called lower precision. Let us understand what that means.

A number on a computer can be stored with more detail or less detail.

- FP32 means a number stored with 32 bits of detail. This is high precision, very accurate, but it takes more space and time.
- FP16 and BF16 mean a number stored with 16 bits of detail. This is lower precision, a little less exact, but it takes half the space and is faster to compute.
- INT8 means a number stored as a small whole number using only 8 bits. This is even lower precision, even smaller, and even faster.

Here, FP stands for floating point, which simply means a number that can have a decimal part, like `3.14`. BF stands for brain floating point, a format made specially for deep learning. INT stands for integer, which means a whole number.

Now, the natural question is: if lower precision is less exact, why use it?

The answer is that deep learning does not always need perfect precision. A neural network is doing approximate pattern matching, not exact bank accounting. A tiny rounding here and there usually does not change the final answer in a meaningful way.

So, by using FP16 or BF16, the GPU does the math roughly twice as fast and uses half the memory, with almost no loss in the quality of the model. This is a wonderful trade, and it is why lower precision is used so much in deep learning.

INT8 is often used for inference, which means using a model after it is trained, to make it run even faster and lighter. We will explain inference clearly in the next section.

Deliberately converting a trained model's numbers down to this lower precision is called quantization. We have a detailed blog on how Model Quantization works that explains how we do it without losing much accuracy.

So, Tensor Cores plus lower precision are a big reason modern GPUs are so fast at deep learning.

If we want to go deep into Quantization, Model Compression, and the optimizations that make models smaller and faster, our AI and Machine Learning Program at Outcome School covers them end to end.

### CUDA and the software stack (cuDNN)

So far we have talked about the GPU hardware. But hardware alone is not enough. We need software to tell the GPU what to do. This is where CUDA comes into the picture.

CUDA is the software platform from NVIDIA that lets programmers run their code on the GPU.

Here is the simple idea. Normal code is written for the CPU. CUDA is the bridge that lets a program send its heavy math to the GPU instead.

[…180ln elided…]

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

[Showing lines 1-390 and 571-907 of 907; 180 middle lines (10.7KB) elided. Read artifact://90 for full output]
