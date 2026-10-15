> Source: https://outcomeschool.com/blog/how-does-gguf-work

# How does GGUF work?
URL: https://outcomeschool.com/blog/how-does-gguf-work
Published: 2026-06-12
Author: Amit Shekhar

How does GGUF work?

# How does GGUF work?

Authors
: - Name
: Amit Shekhar
Published on
: June 12, 2026

GGUF is a single file format that stores everything needed to run a large language model on our own computer, like the model's weights, the tokenizer, and all the settings, packed together in one file.

In this blog, we will learn about how GGUF works. We will also see what problem it solves, what is stored inside a GGUF file, how quantization makes big models fit on a normal laptop, and where it is used in real tools.

We will cover the following:

- What is a model and what are weights?
- What is local inference?
- The problem before GGUF
- What is GGUF?
- What is stored inside a GGUF file?
- What is quantization?
- Understanding quantization names like Q4_K_M
- How GGUF loads fast with memory mapping
- Why GGUF is cross-platform and extensible
- GGUF in the real world

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a model and what are weights?

Before we talk about GGUF, we must first understand a few simple things.

A large language model, or LLM, is the technology behind tools like ChatGPT and Claude. We give it some text, and it gives us back some text.

Now, the natural question is, what is this model actually made of?

A model is made of a huge collection of numbers called weights.

In simple words, the weights are the numbers the model learned during training. When the model was trained, it read a lot of text and slowly adjusted these numbers until it became good at predicting the next word. These learned numbers are the brain of the model.

Let's say a model has 7 billion weights. That means it is a list of 7 billion numbers. When we ask the model a question, it does a lot of math using these numbers to produce an answer.

These weights are usually stored as tensors. A tensor is just a fancy word for a grid of numbers. For the sake of understanding, we can simply think of tensors as big tables full of the model's learned numbers. Do not worry, we do not need any math here, we only need to remember that a tensor is a block of numbers.

So, a model is basically a giant pile of numbers, the weights, arranged as tensors.

This is the foundation we needed. Now let's understand where we want to run this model.

### What is local inference?

When we use the model to get an answer, that act of running the model is called inference.

In simple words, training is when the model learns, and inference is when the model is used. Inference is the model doing its job, taking our text and producing a reply.

Now, there are two places we can run inference.

The first is on a big server in the cloud, far away, owned by a company. We send our text over the internet, the server runs the model, and it sends the answer back.

The second is local inference. Local means on our own machine. So, local inference is running the model directly on our own laptop or computer, without sending anything to a far-away server.

Let's picture both places as below:

```
CLOUD INFERENCE:

  our laptop  ---- our text over internet ---->  cloud server (runs model)
  our laptop  <--- answer over internet --------  cloud server

LOCAL INFERENCE:

  our laptop (runs model)
     our text  --->  model  --->  answer
     nothing leaves the machine

```

Here, we can see that with cloud inference our text travels over the internet to a far-away server and the answer travels back. With local inference, everything happens on our own laptop, and nothing leaves the machine.

People want local inference for good reasons. It keeps our data private, because nothing leaves our machine. It works without the internet. And it has no per-use cost from a cloud provider.

So, our goal is clear. We want to take this giant pile of weights and run it on a normal laptop. Now let's see why this was hard before GGUF.

### The problem before GGUF

To run a model on our laptop, the program needs more than just the weights. It needs a few things together:

- The weights, which are the model's learned numbers, stored as tensors.
- The tokenizer, which is the tool that breaks our text into small pieces the model can read, and joins the pieces back into text. We will understand this better soon.
- The config and metadata, which is the information that describes the model, for example what kind of model it is, how it is built, and how much text it can handle at once.

In the early days, these pieces were often scattered across many separate files in different formats. One file for the weights, other files for the tokenizer, another file for the settings. To load the model, the program had to find all of them, read each one correctly, and stitch them together.

This caused real problems:

- It was fragile. If one file was missing or in a slightly different format, loading failed.
- It was not portable. Sharing a model meant sharing a folder of many files, and another person's tool may read them differently.
- It was slow to load. Reading and combining many files takes time before the model is even ready.

There was an earlier format called GGML that tried to pack things together for running models on normal computers. GGML was a good start and made local inference possible. But as models grew and changed, GGML had limits. It was not flexible enough, and adding new information to the file was painful. Every time the model design changed, the format struggled to keep up.

Let's picture the old scattered way against the single-file goal as below:

```
THE OLD WAY (scattered files):

  +----------------+   +------------------+   +-----------------+
  |  weights file  |   |  tokenizer file  |   |  settings file  |
  +----------------+   +------------------+   +-----------------+
          |                    |                      |
          +--------------------+----------------------+
                               |
                       program must find,
                       read, and stitch all
                       of them together

  fragile, not portable, slow to load

THE GOAL (one organized file):

  +----------------------------------------+
  |  weights + tokenizer + settings        |
  |  all packed together in one file       |
  +----------------------------------------+

  open it and run, nothing to stitch

```

Here, we can see that the old way kept the weights, the tokenizer, and the settings in separate files, so the program had to find each one, read it correctly, and stitch them together. The goal is one organized file that holds everything, so the program can open it and run right away.

We needed a single, well-organized file that holds everything, loads fast, and is easy to extend.

So, here comes GGUF to the rescue.

### What is GGUF?

GGUF is a single file format that stores everything needed to run a large language model for local inference, all in one self-contained file.

GGUF stands for GPT-Generated Unified Format. The key idea for us is in the words Unified Format, where "Unified" means everything the model needs is brought together into one single, organized file, instead of being scattered across many separate files.

In simple words, GGUF is one file that contains the model's weights, the tokenizer, and all the settings, packed neatly together so a program can open it and start running the model right away.

It is the successor to the older GGML format. GGUF was created to fix GGML's limits, and today it is the standard format for running models locally.

Let's use a simple analogy. Suppose we want to move into a new house and we need a bed, a table, and a chair. The old way was like getting these as loose parts in three different boxes, with instructions in three different languages, and we had to assemble everything ourselves. GGUF is like getting one neatly packed box that has everything inside, clearly labeled, ready to use the moment we open it.

So, GGUF is the one box that holds the whole model, ready for our laptop to run.

Now, let's open the box and see what is inside.

### What is stored inside a GGUF file?

A GGUF file is built to hold three kinds of things together. Let's look at each one.

First, the tensors. These are the model's weights, the learned numbers we talked about earlier. This is the biggest part of the file, because a model can have billions of numbers.

Second, the key-value metadata. Metadata is data that describes other data. It is stored as simple pairs of a key and a value, like a label and its answer. For example, a key could be the architecture, which means the type of model and how it is built, and its value tells the program which kind of model this is. Another key could be the context length, which means how many tokens the model can read at once, and its value is a number like 4096. There are many such pairs that fully describe the model.

Third, the tokenizer. A model cannot read raw text. It first breaks the text into small pieces called tokens. A token is a small chunk of text, roughly a word or part of a word. The tokenizer is the tool that does this splitting and also joins tokens back into text. GGUF stores the tokenizer's vocabulary and rules right inside the file, so the program does not need any extra file to understand our text.

We have a detailed blog on Byte Pair Encoding in LLMs that explains how this tokenization step works.

Let's picture the layout of a GGUF file as below:

```
A SINGLE GGUF FILE

+--------------------------------------------------+
|  HEADER                                          |
|    marker "GGUF" + version + counts              |
+--------------------------------------------------+
|  KEY-VALUE METADATA                              |
|    architecture      = "llama"                   |
|    context length    = 4096                      |
|    tokenizer vocab   = [ ...tokens... ]          |
|    quantization info = ...                       |
+--------------------------------------------------+
|  TENSOR INFO (a small table of contents)         |
|    names, shapes, and where each tensor sits     |
+--------------------------------------------------+
|  TENSOR DATA (the weights, the big part)         |
|    [ billions of numbers, the model's brain ]    |
+--------------------------------------------------+

```

Here, we can see that the file starts with a small header. The header begins with the four letters `GGUF`, which is a marker that tells any program "this is a GGUF file". After that comes the key-value metadata, which describes the model in plain labeled pairs. Then comes a small tensor info table, which is like a table of contents that lists every tensor's name, its shape, and where it sits in the file. Finally comes the actual tensor data, the huge block of weights.

So, with one file, the program has the weights, the description, and the tokenizer, all in one place. The problem of scattered files is solved.

Now, there is still one big challenge. These models are huge. Let's see how GGUF helps them fit on a normal laptop.

### What is quantization?

A model with billions of weights is very large. If each weight is stored as a very detailed, very exact number, the file becomes too big to fit in a laptop's memory.

Let's understand the size problem with a simple idea. Each number can be stored using a certain number of bits. A bit is the smallest unit of computer memory, a single 0 or 1. The more bits we use per number, the more precise the number is, but the more space it takes.

Suppose every weight is stored using 16 bits. A model with 7 billion weights would then need about 14 gigabytes just for the weights. That is too big for many laptops to handle comfortably.

So, here comes quantization to the rescue.

Quantization is the technique of storing each weight using fewer bits, so the model becomes much smaller.

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

In simple words, quantization means we round the model's numbers to a simpler, shorter form that takes less space.

Let's use a simple analogy. Suppose a price is 19.997 rupees. If we round it to 20 rupees, it is shorter and easier to store, and for most purposes it is close enough. We lost a tiny bit of exactness, but we saved space. Quantization does the same thing to the model's weights. It stores them with fewer bits, so each number is a little less exact but takes much less room.

Let's see the effect with numbers. If we drop from 16 bits per weight down to about 4 bits per weight, our 7 billion weight model shrinks from around 14 gigabytes to roughly 4 gigabytes. Now it fits on a normal laptop and can run on its CPU or GPU.

But, here is the catch. There is a trade-off.

- Fewer bits means smaller size and faster running, but slightly lower quality. The answers can become a little less accurate, because we made the numbers less exact.
- More bits means larger size and slower running, but higher quality. The answers stay closer to the original model.

So, we choose the level of quantization based on our use case. If we have a small laptop and want speed, we pick a smaller form. If we have more memory and want the best quality, we pick a larger form.

GGUF supports many quantization levels, and it stores the quantized weights directly inside the file. This is one of the biggest reasons GGUF is so useful for local inference.

Quantization is one way to make a model smaller. Another is knowledge distillation, where a small model learns to copy a larger one. We have a detailed blog on how Knowledge Distillation works that explains this in depth.

Now, these quantization levels have names that look strange at first, like `Q4_K_M`. Let's decode them.

### Understanding quantization names like Q4_K_M

When we download a GGUF model, we will see names like `Q4_K_M`, `Q5_K_M`, and `Q8_0`. These look confusing, but they follow a simple pattern. Let's break one down.

Take `Q4_K_M` as below:

```
Q4_K_M
 | | |
 | | +---  M  =  the size variant (S = small, M = medium, L = large)
 | +-----  K  =  a smarter, modern quantization method
 +-------  4  =  about 4 bits used per weight

```

Here, we can see that the name has three parts. The `Q` simply means quantized. The number after it, the `4`, tells us roughly how many bits are used per weight. So `Q4` means about 4 bits per weight, and `Q8` means about 8 bits per weight. The `K` means it uses a smarter, modern method that spends bits more wisely to keep quality high. The last letter, `M`, is a size variant, where `S` is small, `M` is medium, and `L` is large.

So, the simple rule to remember is this:

The number is the bits per weight. A bigger number means more bits, which means bigger file and better quality. A smaller number means fewer bits, which means smaller file and slightly lower quality.

Let me tabulate the common quantization levels for your better understanding so that you can decide which one to use based on your use case.

| Name | Bits per weight | File size | Quality | Good for |
| --- | --- | --- | --- | --- |
| `Q4_K_M` | about 4 | smallest of these | good | laptops with limited memory, a great balance |
| `Q5_K_M` | about 5 | medium | better | a bit more memory, slightly better answers |
| `Q8_0` | about 8 | largest of these | best | plenty of memory, quality matters most |

Here, we can notice that `Q4_K_M` gives the smallest size with good quality, which is why it is one of the most popular choices. As we move to `Q5_K_M` and then `Q8_0`, the file gets bigger and the quality improves, but we need more memory to run it.

Note: If we are not sure which one to pick, `Q4_K_M` is a safe starting point for most laptops, because it balances size and quality very well. If our answers feel a little off and we have spare memory, we can move up to `Q5_K_M` or `Q8_0`.

So, now we know how to read these names and pick the right one based on our use case.

To master Quantization and Model Compression, check out our AI and Machine Learning Program at Outcome School.

### How GGUF loads fast with memory mapping

We learned that a GGUF model can still be a few gigabytes. Now the question is, how does it start so fast without filling up our memory?

The answer is a technique called memory mapping, often written as mmap.

Let's first understand the slow way. The simple way to load a file is to read the whole thing from the disk into memory before we use it. For a 4 gigabyte model, that means waiting until all 4 gigabytes are copied into memory. That is slow, and it uses a lot of memory right away.

So, here comes memory mapping to the rescue.

Memory mapping lets the program treat the file on disk as if it were already in memory, without copying the whole thing first.

In simple words, instead of loading everything up front, the program only reads the parts of the file it actually needs, exactly when it needs them.

Let's use a simple analogy. Suppose we have a thick book. The slow way is to photocopy the entire book before reading a single page. Memory mapping is like keeping the book on the table and simply opening the exact page we need, only when we need it. We do not copy the whole book first. We just read pages on demand.

Let's see the difference as below:

```
WITHOUT memory mapping:

  disk file (4 GB)  ===> copy all 4 GB into memory ===> then start
       slow start, uses a lot of memory immediately

WITH memory mapping (GGUF):

  disk file (4 GB)  --- start immediately --->
       the program reads only the needed parts, when needed
       fast start, memory used efficiently

```

Here, we can see that without memory mapping the program must copy all 4 gigabytes before it even starts, which is slow and heavy on memory. With memory mapping, the program starts right away and pulls in only the parts of the model it needs, when it needs them. This is why a GGUF model can start so quickly.

GGUF is designed to work perfectly with memory mapping. Because the tensors are laid out in a clean, ordered way inside the file, the program can jump straight to any tensor it needs and read it directly. The model starts fast and uses memory efficiently.

This is how GGUF gives us a fast startup on a normal machine.

If we want to go deep into LLM Inference Engineering and Cloud vs On-device Deployment, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

### Why GGUF is cross-platform and extensible

There are two more qualities of GGUF that make it so widely used. Let's understand both.

First, GGUF is cross-platform. Cross-platform means it works the same way across different operating systems and devices. The same GGUF file runs on Windows, macOS, and Linux, and on different kinds of processors. We do not need a different file for each system. We download one GGUF file and it just works wherever we run it.

Second, GGUF is extensible. Extensible means it is easy to add new information to the format without breaking older files. Remember, the metadata inside GGUF is stored as simple key-value pairs. So, when a new kind of model needs a new setting, the format simply adds a new key-value pair. Old programs can still read the file, and new programs can read the new key. This is exactly the weakness that the older GGML format had, and GGUF fixed it.

So, GGUF is portable across machines and flexible enough to grow with new models. This is why it became the standard.

Now, let's see where GGUF is actually used.

### GGUF in the real world

GGUF is the format used by llama.cpp and the popular tools built on top of it.

Let's understand `llama.cpp` first. It is an open-source program written to run large language models efficiently on normal computers, including laptops, using the CPU or the GPU. It is fast, lightweight, and it reads models in the GGUF format. GGUF was created as part of this `llama.cpp` world to be the clean, single-file format these models use.

Many friendly tools are built on top of `llama.cpp`, and they all use GGUF:

- Ollama. This is a tool that lets us download and run models locally with a simple command. Under the hood, it uses GGUF files and `llama.cpp`.
- LM Studio. This is a desktop app with a nice screen where we can search for models, download GGUF files, and chat with them, all on our own machine.

Let's picture how these pieces stack together as below:

```
  +-----------------+        +-----------------+
  |     Ollama      |        |    LM Studio    |   the friendly tools we use
  +-----------------+        +-----------------+
            |                         |
            +------------+------------+
                         |
                +------------------+
                |    llama.cpp     |   runs the model efficiently
                +------------------+
                         |
                +------------------+
                |  .gguf file      |   weights + tokenizer + metadata
                +------------------+

```

Here, we can see that the GGUF file sits at the bottom holding everything the model needs. The `llama.cpp` program reads that file and runs the model. The friendly tools like Ollama and LM Studio sit on top of `llama.cpp`, giving us a simple way to use it. So they all rely on the same single GGUF file underneath.

In all of these, the flow is the same. We download a single file that ends with `.gguf` for the model and the quantization level we want, the tool opens it using memory mapping, reads the weights, the tokenizer, and the metadata from that one file, and we start chatting. There is nothing to assemble and no scattered files to manage.

So, anywhere we want to run a large language model on our own machine, GGUF is very likely the format we will use.

The models we run locally like this are often Small Language Models, compact enough to fit on a laptop or phone. We have a detailed blog on Small Language Models (SLMs) that explains why smaller models matter.

This is how GGUF works. It packs the model's weights, its tokenizer, and its metadata into one self-contained file, it uses quantization to shrink the weights so big models fit on a normal laptop, and it loads quickly with memory mapping, which is why it became the standard format for running large language models locally.

### What is the difference between GGUF and GGML?

GGUF is the successor to the older GGML format. GGML made local inference possible, but it was not flexible enough, and adding new information to the file was painful. GGUF fixed this by storing metadata as simple key-value pairs, so new settings can be added without breaking older files.

### Which GGUF quantization level should we pick?

`Q4_K_M` is a safe starting point for most laptops, because it balances size and quality very well. If the answers feel a little off and we have spare memory, we can move up to `Q5_K_M` or `Q8_0`. A bigger number means a bigger file and better quality.

### Does a quantized GGUF model give worse answers?

Slightly. Fewer bits per weight make the numbers a little less exact, so the answers can become a little less accurate. In return, the model becomes much smaller and faster. With more bits, the file is larger but the answers stay closer to the original model.

### Do we need separate tokenizer files to run a GGUF model?

No. GGUF stores the tokenizer's vocabulary and rules right inside the file, along with the weights and the metadata. So the program does not need any extra file to understand our text. We download a single `.gguf` file and start running the model.

### Do Ollama and LM Studio use GGUF?

Yes. Both Ollama and LM Studio are built on top of `llama.cpp`, and they use GGUF files. The GGUF file holds everything the model needs, `llama.cpp` reads it and runs the model, and these tools give us a simple way to use it.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
