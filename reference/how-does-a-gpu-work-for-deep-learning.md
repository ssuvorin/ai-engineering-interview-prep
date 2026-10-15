> Source: https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning

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

On top of CUDA, NVIDIA built another library called cuDNN, which stands for CUDA Deep Neural Network library.

cuDNN is a ready-made toolbox of highly optimized deep learning operations, such as matrix multiplication and the building blocks of neural networks. The NVIDIA engineers spent huge effort making these operations run as fast as possible on the GPU.

Now, here is the part that makes life easy for us. Most people never write CUDA or cuDNN directly. We use deep learning frameworks like PyTorch or TensorFlow.

These frameworks sit on top of cuDNN, which sits on top of CUDA, which sits on top of the GPU.

Let us see the full stack as a simple picture:

```
Our Python code (PyTorch / TensorFlow)
            |
          cuDNN   (fast deep learning operations)
            |
          CUDA    (bridge to the GPU)
            |
          GPU     (the hardware doing the math)

```

So, when we write a few simple lines in PyTorch, all these layers work together to run our math on the thousands of GPU cores.

For example, in PyTorch we move our work to the GPU with one short line as below:

```python
import torch

# create a tensor (a matrix of numbers) and send it to the GPU
x = torch.randn(1000, 1000).to("cuda")
y = torch.randn(1000, 1000).to("cuda")

# this matrix multiplication now runs on the GPU
result = x @ y

```

Here, we can see that `.to("cuda")` moves our numbers onto the GPU. After that, the multiplication `x @ y` runs on the GPU using all those cores and Tensor Cores. We wrote simple code, and CUDA and cuDNN did the heavy lifting underneath.

NVIDIA builds one more layer on top of this stack, meant only for running a finished large language model as fast as the hardware allows. We have a detailed blog on how TensorRT-LLM works that walks through it step by step.

This is how the software stack lets us use the full power of the GPU without writing low-level code.

### Training vs inference on GPUs

We have used the words training and inference. Now, let us understand both clearly, because the GPU is used in both, but in different ways.

Training is the phase where the model learns. We show the model lots of data, it makes guesses, we measure how wrong it is, and then it adjusts its weights to do better next time. This loop repeats again and again over huge amounts of data.

Training is extremely heavy. It does the matrix math forward to make a guess, and then it does even more math backward to update the weights. So, training needs a lot of GPU power and a lot of VRAM. This is the most expensive part of building an AI model.

Inference is the phase where we use the already trained model to get answers. For example, when we type a question into a chatbot and it replies, that is inference.

Inference is lighter than training. It only does the forward math to produce an answer. It does not do the backward updating, because the model is already trained.

Let me tabulate the difference between training and inference for your better understanding.

| Point | Training | Inference |
| --- | --- | --- |
| Goal | Teach the model | Use the trained model |
| Math involved | Forward and backward | Forward only |
| GPU power needed | Very high | Lower |
| When it happens | Once, while building | Every time a user asks |

The lower precision like INT8 is often used in inference, because we want answers to come out fast and cheap once the model is already trained.

So, the GPU helps us both build the model and then serve it to users.

### Multiple GPUs working together

Sometimes one GPU is simply not enough. The model can be too big to fit in one GPU's VRAM, or the training can be so heavy that one GPU would take too long.

So, here comes the idea of using multiple GPUs working together.

There are two main ways to do this. Let us understand both in simple words.

Data parallelism. We put a full copy of the model on each GPU. Then we split the training data into pieces and give a different piece to each GPU. Each GPU trains on its piece at the same time, and then they share what they learned and stay in sync. This makes training faster because many GPUs learn together.

Model parallelism. When the model is too big to fit on one GPU, we cut the model itself into parts and put different parts on different GPUs. Each GPU holds and runs only its part, and they pass results to each other. This lets us run a model that is far larger than any single GPU's VRAM.

For the GPUs to work together well, they must talk to each other very fast. NVIDIA built a high-speed connection called NVLink for this, so GPUs can pass numbers between them quickly without slowing down.

Here is a simple picture of data parallelism:

```
        Training data split into pieces
        /            |            \
    GPU 1          GPU 2          GPU 3
  (full model)  (full model)  (full model)
        \            |            /
          share and stay in sync

```

So, by combining many GPUs, we can train very large models that one GPU could never handle alone.

### Why NVIDIA GPUs power modern AI

Now, let us tie everything together and answer a question many people ask: why is NVIDIA the name we hear behind almost all modern AI?

There are a few clear reasons.

First, NVIDIA GPUs have the right hardware. Thousands of cores, special Tensor Cores, large VRAM, high memory bandwidth, and fast NVLink connections between GPUs. All of this is exactly what deep learning needs.

Second, and this is just as important, NVIDIA built the software too. CUDA and cuDNN have been around for many years and are deeply trusted. The most popular frameworks, PyTorch and TensorFlow, are built to work smoothly on top of them. So, when a researcher writes code, it just works on NVIDIA GPUs.

This combination of strong hardware and mature software is why NVIDIA became the default choice.

NVIDIA is not the only company building chips for this. Google built its own accelerator, the TPU, for the same job. We have a detailed blog on how a Google TPU works that walks through it step by step. Others went one step further and built a chip that only runs already-trained language models, and we have a detailed blog on how an LPU works that explains that design in depth.

This is why large language models, the kind of AI behind chatbots and writing assistants, are trained on huge clusters of NVIDIA GPUs. These models have billions of weights and need billions of matrix multiplications. Training them can take thousands of GPUs running together for weeks.

Let us recall the whole journey in one breath. Deep learning is mostly matrix multiplication. Matrix multiplication is millions of small, independent multiply-add operations. A GPU has thousands of cores that do these operations in parallel, Tensor Cores that do them even faster at lower precision, and fast VRAM to feed them. CUDA and cuDNN let our simple code use all of this power. And when one
