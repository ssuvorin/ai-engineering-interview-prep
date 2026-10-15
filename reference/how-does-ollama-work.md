> Source: https://outcomeschool.com/blog/how-does-ollama-work

# How does Ollama work?
URL: https://outcomeschool.com/blog/how-does-ollama-work
Published: 2026-10-05
Author: Amit Shekhar

How does Ollama work?

# How does Ollama work?

Authors
: - Name
: Amit Shekhar
Published on
: October 5, 2026

Ollama is a free tool that lets us download and run LLMs on our own computer with one simple command. It works by running a small server in the background that downloads compressed model files, loads them into memory, and uses a fast engine to generate text when we send it a prompt.

In this blog, we will learn about how Ollama works. We will also see why model files must be shrunk before they fit on a laptop, how Ollama's client and server talk to each other, what happens step by step when we type a command, how models are downloaded, stored, and loaded onto the CPU and GPU, what a Modelfile is and how other apps use Ollama through its API, and where it works well and where it fails.

We will cover the following:

- What does running an LLM locally mean?
- What is Ollama?
- The big problem: models are huge
- Quantization and the GGUF file format
- The architecture: client and server
- What happens when we run a model?
- How models are downloaded and stored
- How the model runs on CPU and GPU
- What is a Modelfile?
- Using Ollama from code through its API
- Where it works well and where it fails

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What does running an LLM locally mean?

Before jumping into Ollama, we must know what running an LLM locally means.

An LLM (Large Language Model) reads a prompt and writes a reply, one small piece of text at a time. These small pieces of text are called tokens. A token is usually a word or a part of a word.

When we use an LLM on a website, the LLM is not running on our computer. Our message travels over the internet to a big computer owned by a company, the model runs there, and the reply travels back to us.

Running an LLM locally means the model runs on our own computer, and our messages never leave our machine.

Let's say we compare this with food. Using an online LLM is like ordering food from a restaurant. Running locally is like cooking at home. Cooking at home needs our own kitchen and ingredients, but we control everything, nobody else sees what we eat, and it works even when the restaurants are closed.

So, running locally gives us:

- Privacy: Our data stays on our machine.
- Works offline: No internet is needed once the model is downloaded.
- No per-message cost: We do not pay for each request.
- Full control: We choose which model to run and how.

We have a detailed blog on Cloud vs On-device Model Deployment that explains when a model should run on a far-away server and when it should run on our own device.

But, running an LLM locally used to be hard. We had to find the right model file, install many libraries, set up the GPU, and write code. Here comes Ollama into the picture.

## What is Ollama?

Ollama is an open-source tool that makes it easy to download, run, and manage LLMs on our own computer.

In simple words, Ollama does for LLMs what an app store does for apps. We just say which model we want, and Ollama takes care of downloading it, setting it up, and running it.

After installing Ollama, we can start chatting with a model using just one command:

```bash
ollama run llama3.2

```

Here, `ollama run` tells Ollama to run a model, and `llama3.2` is the name of the model. If the model is not on our computer yet, Ollama downloads it first. Then, it opens a chat right in the terminal.

It works on macOS, Windows, and Linux. Now, let's understand what happens behind this simple command.

## The big problem: models are huge

An LLM is made of billions of numbers called weights. These weights are what the model learned during training.

Normally, each weight is stored using 16 bits, which is 2 bytes.

Let's calculate the size of a model with 8 billion weights:

```text
8 billion weights x 2 bytes = 16 GB

```

Here, we can see that even a medium-sized model needs 16 GB just to hold its weights. Many laptops have only 8 GB or 16 GB of memory in total, and that memory is also needed by the operating system and other apps.

Also, to generate every single token, the computer must read through all of these weights. So, a bigger file means slower replies.

The question is: how do we fit this on a normal laptop? The answer is: we shrink the numbers.

## Quantization and the GGUF file format

Quantization means storing each weight with fewer bits, for example 4 bits instead of 16 bits.

In simple words, it is like rounding prices. Instead of writing 49.97, we write 50. We lose a tiny bit of detail, but the number becomes shorter.

Let's do the math again for the same 8 billion weight model:

```text
16-bit:  8 billion x 2 bytes    = 16 GB
4-bit:   8 billion x 0.5 bytes  =  4 GB  (a little more in practice)

```

Here, we can see that the 4-bit version is about four times smaller. It now fits easily on a laptop, and it runs faster too, because there is less data to read for every token. The answer quality drops only a little.

Most models that Ollama downloads by default are already quantized to around 4 bits.

Now, these shrunk models are saved in a file format called GGUF. GGUF is the file format used to store models that run on GGML, a library for running LLMs efficiently. A GGUF file packs everything a model needs into one single file:

- The quantized weights.
- The details of the model's architecture, like how many layers it has.
- The tokenizer, which is the part that splits text into tokens and turns tokens back into text.

GGUF comes from the llama.cpp project. llama.cpp is a popular open-source program, written in C and C++, that runs LLMs very efficiently on normal computers, including computers without a powerful GPU. Ollama has been built on top of llama.cpp and its underlying library GGML. Newer versions of Ollama also have their own engine for some models, built on the same GGML library.

So, the actual heavy math of running the model is done by this engine. A program that runs a trained model to produce answers is called an inference engine. Ollama is the layer on top that handles everything else.

To learn Quantization and Optimizations and LLM Inference Engineering in depth, check out our AI and Machine Learning Program at Outcome School.

## The architecture: client and server

Now, let's understand how Ollama is organized.

Ollama has two parts:

- The server: A program that runs in the background. It manages the models, loads them into memory, and runs them. It is started with `ollama serve`, and the desktop app starts it for us automatically.
- The client: The thing that sends requests to the server. The `ollama` command we type in the terminal is a client. But, any other app can also be a client.

They talk to each other using HTTP. The server listens at the address `http://localhost:11434`. Here, `localhost` means "this same computer", and `11434` is the port, which is like a door number where the server waits for requests.

```text
+-------------+   +-------------+   +-------------+
| ollama CLI  |   | Python app  |   | A chat app  |
|  (client)   |   |  (client)   |   |  (client)   |
+-------------+   +-------------+   +-------------+
       ↓                 ↓                 ↓
       +-----------------+-----------------+
                         ↓
                   HTTP requests
                         ↓
         +-------------------------------+
         |  Ollama server (port 11434)   |
         |  - manages models             |
         |  - loads them into memory     |
         |  - runs the inference engine  |
         +-------------------------------+
                         ↓
                 +---------------+
                 |   CPU / GPU   |
                 +---------------+

```

Here, we can see that many different clients can use the same Ollama server. There is one server and one place where the models live, and every app on our computer can use it.

## What happens when we run a model?

Now, let's follow what happens when we type `ollama run llama3.2` and ask a question.

Step 1: The client contacts the server. The `ollama` command sends a request to the server at `localhost:11434`.

Step 2: The server checks if the model is on disk. If it is not, the server downloads it from the Ollama model library on the internet. We will see how this works in the next section.

Step 3: The server loads the model into memory. It reads the GGUF file and places the weights into the GPU memory, the normal computer memory, or a mix of both. This can take a few seconds.

Step 4: The prompt is prepared. Each model expects the conversation in a special layout, with markers that show where the system instructions, the user's message, and the assistant's reply begin. This layout is called a chat template. Ollama wraps our message in the right template for that model automatically.

Step 5: The prompt is turned into tokens. The tokenizer splits the text into tokens, and each token becomes a number.

Step 6: The model generates the reply. The engine runs the model to predict the next token, adds it to the text, and repeats. This happens again and again until the reply is complete.

Step 7: The reply is streamed back. Each new token is sent back to the client as soon as it is ready. That is why we see the words appear one by one on the screen, instead of waiting for the whole reply.

Step 8: The model stays in memory for a while. After the reply, the model is not removed right away. By default, Ollama keeps it loaded for 5 minutes. If we ask another question within that time, the reply starts instantly because Step 3 is skipped. If nothing happens for 5 minutes, the model is unloaded to free the memory. We can change this time with a setting called `keep_alive`.

This is how one simple command turns into a full chat with a local LLM.

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

## How models are downloaded and stored

Now, let's see how Step 2 works.

Ollama has an online model library at ollama.com. Each model has a name and a tag, like `llama3.2:3b` or `qwen2.5:7b`. The tag usually tells the size or the version. If we do not give a tag, Ollama uses the default one, called `latest`.

We can download a model without running it, as below:

```bash
ollama pull llama3.2

```

Here, `pull` downloads the model and stores it on our computer, so that it is ready for later.

A model in Ollama is not stored as one single file with a name. It is stored as a set of pieces, called layers. One layer is the big GGUF weights file. Other small layers hold things like the chat template, the default settings, and the license.

There is also a small file called a manifest. It is a list that says which layers make up this model.

Each layer is saved with a name made from its hash. A hash is a short fingerprint calculated from the content of a file. The same content always gives the same fingerprint.

Why is this useful? Let's say we create two custom versions of the same model, each with a different system instruction. Both versions use the exact same weights file. Since the weights layer has the same hash, Ollama stores it only once. Only the tiny different layers are stored separately. This saves a lot of disk space.

For example, on a Mac, these files live in a folder named `.ollama/models` inside our home folder.

We can manage our models with a few simple commands:

```bash
ollama list            # show all downloaded models
ollama ps              # show models currently loaded in memory
ollama rm llama3.2     # delete a model from disk

```

Here, `list` shows what is on disk, `ps` shows what is loaded in memory right now, and `rm` removes a model we no longer need.

## How the model runs on CPU and GPU

Now, the next big question is: where does the actual math happen?

The model can run on the CPU or on the GPU. A GPU can do thousands of calculations at the same time. LLMs need exactly this kind of work, so a GPU makes them much faster.

When Ollama starts, it checks which GPU our computer has. It supports NVIDIA GPUs, many AMD GPUs, and Apple Silicon chips on Macs. On Apple Silicon, the CPU and GPU share the same memory, which works well for LLMs.

An LLM is built from many layers stacked one after the other. Here, layer means a stage of the model's computation, not the storage layer we saw earlier. The input passes through the first layer, then the second, and so on, until the last one.

Ollama decides how many of these model layers fit into the GPU memory:

- If the whole model fits, all layers go to the GPU. This is the fastest.
- If only part of it fits, some layers go to the GPU and the rest stay in normal memory and run on the CPU. This is called partial offloading.
- If there is no usable GPU, everything runs on the CPU.

```text
Model with 32 layers, GPU can hold 20:

  [Layer 1 ... Layer 20]  -> GPU  (fast)
  [Layer 21 ... Layer 32] -> CPU  (slower)

```

Here, we can see that Ollama makes the best use of whatever hardware we have, without us having to set anything. We can run `ollama ps` to see how much of a loaded model is on the GPU and how much is on the CPU.

Note: Memory is needed not only for the weights but also for the conversation itself. As the model reads more text, it saves its work on earlier tokens in memory, which is called the KV cache. A longer conversation needs more memory. The maximum amount of text the model can see at once is called the context length, and a bigger context length uses more memory.

If we want to go deep into LLM Inference Engineering and Cloud vs On-device Deployment, we have a complete program on it - check out our AI and Machine Learning Program at Outcome School.

## What is a Modelfile?

Now, let's say we want our own version of a model, for example, one that always answers like a friendly teacher, with less randomness.

Ollama lets us do this with a Modelfile. A Modelfile is a small text file that describes how to build a custom model from an existing one.

In simple words, it is a recipe. It says which model to start from and what to change.

Let's see the code for a Modelfile as below:

```text
FROM llama3.2

PARAMETER temperature 0.3
PARAMETER num_ctx 4096

SYSTEM """
You are a friendly teacher. Explain everything in simple words.
"""

```

Here, we have:

- `FROM llama3.2` is the base model we start from.
- `PARAMETER temperature 0.3` sets the temperature, which controls randomness. A lower value gives more focused and predictable answers.
- `PARAMETER num_ctx 4096` sets the context length to 4096 tokens.
- `SYSTEM` sets the system message, which is the instruction the model sees before every conversation.

Now, we can create and run our custom model like below:

```bash
ollama create teacher -f Modelfile
ollama run teacher

```

Here, `create` builds a new model named `teacher` using the recipe, and `run` starts chatting with it.

The best part is that no new copy of the weights is made. Our `teacher` model points to the same weights layer as `llama3.2`. Only the small settings layers are new. This is the same layer sharing we learned about earlier.

## Using Ollama from code through its API

So far, we have used Ollama from the terminal. But, since the server talks HTTP, any program can use it through its API.

Let's see the code for sending a chat request with Python as below:

```python
import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.2",
        "messages": [
            { "role": "user", "content": "Why is the sky blue?" }
        ],
        "stream": False,
    },
)

print(response.json()["message"]["content"])

```

Here, we have:

- We send a request to the `/api/chat` address of the local Ollama server.
- `model` says which model to use.
- `messages` is the conversation. Each message has a `role`, like `user` or `assistant`, and its `content`.
- `stream` set to `False` means we want the full reply at once. By default, Ollama streams the reply piece by piece, like we saw in the terminal.
- Finally, we print the reply text.

It will print the model's answer about why the sky is blue.

Ollama also offers an address that follows the same request format as OpenAI's API, at `http://localhost:11434/v1`. This means many apps and libraries that were built for OpenAI can use a local Ollama model just by changing the address.

## Where it works well and where it fails

Let me tabulate the differences between using a cloud LLM service and running a model with Ollama for your better understanding.

| Point | Cloud LLM service | Ollama (local) |
| --- | --- | --- |
| Where the model runs | Company's servers | Our own computer |
| Privacy | Data is sent over the internet | Data stays on our machine |
| Internet needed | Yes | Only for downloading models |
| Cost | Pay per use or subscription | Free, but needs our own hardware |
| Model size | Very large models | Limited by our computer's memory |
| Speed | Fast, powerful servers | Depends on our CPU and GPU |
| Setup | Just an account and an API key | Install Ollama and pull a model |

It works well when:

- We want privacy, for example, working with personal notes or company documents.
- We want to build and test apps without paying for every request.
- We need to work offline.
- We want to try many open models quickly.

It struggles when:

- We need the largest and smartest models. Those are too big for most personal computers.
- Our computer has little memory or no good GPU. Then, replies come out slowly.
- We need to serve many users at the same time. Ollama is designed mainly for one person or a small team on one machine. For serving a large number of users, tools built for high traffic, like vLLM, are a better fit.

For most personal computers, smaller models are the sweet spot. We have a detailed blog on Small Language Models (SLMs) that covers when to pick them.

Now we must have understood how Ollama works.

### Is Ollama free to use?

Yes. Ollama is a free and open-source tool. We do not pay for each request we send to a local model. The only cost is our own hardware, because the model runs on our own computer instead of a company's servers.

### Does Ollama need an internet connection?

Only for downloading models. Once a model is pulled from the Ollama model library, it runs fully on our own computer, so we can keep using it offline. Our prompts and replies never leave our machine.

### Can Ollama run without a GPU?

Yes. If there is no usable GPU, Ollama runs the whole model on the CPU. It works, but replies come out more slowly. When a GPU is present, Ollama puts as many model layers on it as fit and runs the rest on the CPU.

### Can apps built for the OpenAI API use Ollama?

Yes. Ollama offers an address that follows the same request format as OpenAI's API, at `http://localhost:11434/v1`. So many apps and libraries that were built for OpenAI can use a local Ollama model just by changing the address they send requests to.

### Why is the first reply from Ollama slower than the next ones?

The first request has to load the model from disk into memory, which can take a few seconds. After that, Ollama keeps the model loaded for 5 minutes by default, so the next questions skip the loading step and the reply starts instantly. We can change this time with the `keep_alive` setting.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:
