> Source: https://outcomeschool.com/blog/how-does-knowledge-distillation-work

# How does Knowledge Distillation work?
URL: https://outcomeschool.com/blog/how-does-knowledge-distillation-work
Published: 2026-06-11
Author: Amit Shekhar

How does Knowledge Distillation work?

# How does Knowledge Distillation work?

Authors
: - Name
: Amit Shekhar
Published on
: June 11, 2026

Knowledge Distillation is a technique where we train a small model to copy the behavior of a large model. The big model is the teacher, and the small model is the student.

In this blog, we will learn about how Knowledge Distillation works. We will also see why we need it, how a small model learns from a big model, and how this lets us run powerful AI on a phone, on an edge device, and at low cost.

We will cover the following:

- What is Knowledge Distillation?
- Why we need Knowledge Distillation
- Hard labels vs soft labels
- Dark knowledge
- Temperature in the softmax
- The distillation loss
- A step-by-step training walkthrough
- Types of Knowledge Distillation
- Real examples of Knowledge Distillation
- Wrapping up Knowledge Distillation

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Knowledge Distillation?

Knowledge Distillation is a technique where we train a small model to copy the behavior of a large model.

In simple words, we take a big, smart model and teach a small model to think like it.

The big model is called the teacher. The small model is called the student. The teacher already knows a lot. The student is new and small. Our goal is to pass the teacher's knowledge into the student.

Let's say we have a very experienced senior teacher in a school. This teacher has read thousands of books and has years of experience. But this teacher is expensive and slow, and there is only one of them. Now, we want many copies of a "good enough" teacher who can work fast and cheap. So, the senior teacher trains a young student until the student can answer almost as well. The student is not as deep as the senior, but the student is fast, cheap, and good enough for daily work.

This is exactly what Knowledge Distillation does, but with AI models.

Before we go deeper, let's understand one basic thing. An AI model is, at its heart, a huge collection of numbers that have been adjusted during training so the model can make good predictions. A large model has many such numbers, so it is powerful but heavy. A small model has fewer numbers, so it is light but, on its own, less smart.

Knowledge Distillation is the bridge. We use the heavy, smart model to make the light model smarter than it could become on its own.

We can picture it as below:

```
        +------------------------------+
        |  TEACHER (big, smart, slow)  |
        +------------------------------+
                       |
                       |  passes its knowledge
                       v
        +------------------------------+
        |  STUDENT (small, fast, cheap)|
        +------------------------------+

```

Here, we can see that the big teacher model passes its knowledge down into the small student model. The teacher stays big, smart, and slow. The student ends up small, fast, and cheap, but it has learned to behave almost like the teacher.

This is the basic idea. Now, let's understand why we even need this.

### Why we need Knowledge Distillation

Big models are very accurate. But big models are also slow and expensive.

A large model needs a lot of memory. It needs powerful and costly hardware. It takes more time to give an answer. This delay between asking and getting the answer is called latency. High latency means the user waits longer.

Now, think about where we want to use AI.

We want AI on our phones. We want AI on small devices like a smartwatch, a camera, or a car. These small devices are called edge devices, because they sit at the "edge", close to the user, far from big data centers. Edge devices have little memory and little battery. A huge model simply cannot fit there.

We also want AI to respond instantly. A chat reply that takes ten seconds feels broken. We want low latency.

And, we want AI to be cheap to run. Running a giant model for millions of users costs a lot of money.

So, the situation is this:

- The big model is accurate but slow and expensive.
- The small model is fast and cheap but less accurate on its own.

We want the best of both. We want a small, fast, cheap model that still keeps most of the accuracy of the big model.

So, here comes Knowledge Distillation to the rescue. It lets us shrink the brain into a smaller body while keeping most of the intelligence.

To go deep into Model Compression, Quantization and Optimizations, and Cloud vs On-device Deployment, check out our AI and Machine Learning Program at Outcome School.

Now, to understand how the teacher passes its knowledge, we must first understand the difference between hard labels and soft labels.

### Hard labels vs soft labels

Let's take a simple example. Suppose we are building a model that looks at a photo and decides what is in it. The possible answers are `cat`, `dog`, `car`, and `horse`. Each possible answer is called a class.

Now, suppose we show the model a photo of a cat.

A hard label is the single correct answer, and nothing more. For this photo, the hard label says: this is a `cat`. We can write it like this.

```
cat   = 1
dog   = 0
car   = 0
horse = 0

```

Here, we can see that the hard label gives full marks to `cat` and zero to everything else. It is just the plain truth, with no extra information.

Now, let's look at what the teacher model actually produces. When the teacher sees the cat photo, it does not output just one word. It outputs a probability for every class. A probability is a number between 0 and 1 that tells us how confident the model is. All the probabilities add up to 1.

This full set of probabilities is called a soft label or a probability distribution. It can look like this.

```
cat   = 0.90
dog   = 0.08
car   = 0.01
horse = 0.01

```

Here, we can see that the teacher is 90% sure it is a `cat`. But it also gives a small 8% to `dog`, and almost nothing to `car` and `horse`.

So, the difference is simple.

- A hard label says only "it is a cat".
- A soft label says "it is mostly a cat, a little bit like a dog, and not at all like a car".

This small extra information turns out to be very powerful. Let's understand why.

### Dark knowledge

The soft label carries hidden information that the hard label throws away. This hidden information is called dark knowledge.

In simple words, dark knowledge is what the teacher knows about how the classes relate to each other.

Let's go back to our cat photo. The teacher gave `dog` an 8% chance and `car` almost 0%. Think about what this is telling us. The teacher is saying: a cat looks somewhat like a dog, but a cat looks nothing like a car.

This is true knowledge about the world. Cats and dogs are both furry, four-legged animals, so they can be confused. A cat and a car have nothing in common, so they are never confused.

A hard label can never teach this. A hard label only says "cat", and treats "dog" and "car" as equally wrong. But they are not equally wrong. Being a little bit "dog" is a reasonable mistake. Being "car" is a silly mistake.

So, when the student learns from the soft labels, it learns these relationships. It learns that cats and dogs are close. It learns that cats and cars are far apart. This is much richer than just memorizing the single right answer.

This is the heart of Knowledge Distillation. The soft labels of the teacher teach the student far more than a plain hard label ever could.

Let's make this concrete with a comparison.

```
   HARD LABEL                 SOFT LABEL (from teacher)
   -----------                -------------------------
   cat   = 1                  cat   = 0.90   <- the answer
   dog   = 0                  dog   = 0.08   <- "a bit like a dog"
   car   = 0                  car   = 0.01   <- "nothing like a car"
   horse = 0                  horse = 0.01   <- "nothing like a horse"

   Tells: only the answer     Tells: the answer + how classes relate

```

Here, we can see that the soft label on the right is doing extra teaching that the hard label on the left simply cannot do.

Now, there is one more problem. Sometimes the teacher is too confident. It can say `cat = 0.99` and give almost nothing to the others. When that happens, the useful dark knowledge becomes very tiny and hard to see. We need a way to bring out these small numbers. So, here comes temperature into the picture.

### Temperature in the softmax

Before we explain temperature, we must understand one small step that happens inside the model.

When a model makes a prediction, it first produces raw scores for each class. These raw, unprocessed scores are called logits. A logit can be any number, like `8.2` or `-1.4`. These raw scores are hard to read directly.

To turn these raw scores into clean probabilities that add up to 1, the model uses a function called the softmax. The softmax takes the logits and squashes them into nice probabilities between 0 and 1.

We have a detailed blog on Cross-Entropy Loss that explains logits and the softmax in depth.

Now comes the clever part. The softmax has a knob we can turn, called the temperature, often written as `T`.

In simple words, temperature controls how soft or how sharp the probabilities come out.

- A low temperature (like `T = 1`) gives sharp probabilities. One class gets a very high value, and the rest get tiny values.
- A high temperature (like `T = 4`) gives softer, more spread-out probabilities. The smaller values grow bigger and become easier to see.

Let's see this with our cat example. At a normal temperature, the teacher is very confident.

```
T = 1  (sharp):    cat = 0.95   dog = 0.04   car = 0.005   horse = 0.005

```

Now, if we raise the temperature, the same prediction spreads out.

```
T = 4  (soft):     cat = 0.70   dog = 0.22   car = 0.05    horse = 0.03

```

Here, we can see that at the higher temperature, the `dog` value jumped from 0.04 to 0.22. The dark knowledge, which means the relationship between cat and dog, is now clear and loud. The student can learn from it much more easily.

So, during distillation, we raise the temperature so the teacher's soft labels reveal these subtle relationships. The student gets a clearer, richer lesson.

Note: We use the higher temperature only during training. When the finished student is actually used in the real world, we go back to the normal temperature.

Now, we have soft labels, dark knowledge, and temperature. The next question is: how exactly do we train the student using all this? The answer is the distillation loss.

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

### The distillation loss

To train any model, we need a way to measure how wrong it is. This measure of wrongness is called the loss. Training means slowly changing the model's numbers to make the loss as small as possible. A smaller loss means the model is making better predictions.

In Knowledge Distillation, the student must do two things at the same time.

First, it must match the teacher's soft labels. The student looks at a photo, produces its own soft probabilities, and we compare them to the teacher's soft probabilities. We want them to be as close as possible. The measure of how different two probability distributions are is called KL divergence. We do not need the math. We only need to know that a smaller KL divergence means the two distributions are more similar. This part is called the distillation loss.

Second, the student must also get the true answer right. We compare the student's prediction to the real hard label, the actual truth. This part is the normal loss, the same loss we would use to train any model from scratch.

Now, why do we keep both? Because each one helps.

- The distillation loss teaches the rich dark knowledge from the teacher.
- The normal loss keeps the student grounded in the real, correct answers, so it does not blindly copy the teacher's mistakes.

So, the total loss is a blend of the two.

```
Total loss  =  part 1  +  part 2

part 1  =  weight       x  distillation loss   (student vs teacher soft labels)
part 2  =  (1 - weight) x  normal loss         (student vs true hard labels)

```

Here, we can see that the total loss is just a weighted mix. The `weight` is a number we choose that decides how much the student must listen to the teacher versus the true answer. For example, we often give more weight to the teacher's soft labels, because that is where the extra knowledge lives.

The flow looks like below:

```
                    +----------------+        +----------------+
   same photo --->  |  TEACHER       |        |  STUDENT       |  <--- same photo
                    |  (big model)   |        |  (small model) |
                    +----------------+        +----------------+
                            |                         |
                teacher     |                         |  student
                soft labels v                         v  soft labels
                    +------------------------------------------+
                    |  distillation loss  (student vs teacher) |
                    +------------------------------------------+
                                        |
                                        v
                              +--------------------+
                              |     TOTAL LOSS     |
                              |   (weighted mix)   |
                              +--------------------+
                                        ^
                                        |
                    +------------------------------------------+
                    |  normal loss  (student vs true label)    |
                    +------------------------------------------+
                            ^                         ^
                            |                         |
                    true hard label           student prediction

```

Here, we can see that the same photo goes into both the teacher and the student. The distillation loss measures how far the student's soft labels are from the teacher's soft labels. The normal loss measures how far the student's prediction is from the true hard label. Both losses are then blended into one total loss, which is the single number we make smaller during training.

This combined loss is the engine of Knowledge Distillation. By making this total loss small, the student learns the correct answers and the teacher's wisdom together.

Now, let's put all the pieces into one clear walkthrough.

### A step-by-step training walkthrough

Let's walk through exactly what happens when we distill knowledge from the teacher into the student. We will use our animal photo example.

Step 1: We start with a trained teacher model. The teacher is big and already accurate. We do not change the teacher at all during distillation. It only gives lessons.

Step 2: We take a fresh, small student model. The student starts with random numbers and knows nothing yet.

Step 3: We take a photo from our training data, for example, our cat photo.

Step 4: We pass the photo through the teacher. We use a high temperature so the teacher produces soft labels full of dark knowledge, like `cat = 0.70, dog = 0.22, car = 0.05, horse = 0.03`.

Step 5: We pass the same photo through the student. The student produces its own soft labels at the same high temperature, for example, `cat = 0.50, dog = 0.30, car = 0.15, horse = 0.05`.

Step 6: We calculate the distillation loss by comparing the student's soft labels to the teacher's soft labels using KL divergence. Right now they are different, so this loss is high.

Step 7: We also calculate the normal loss by comparing the student's normal prediction to the true hard label, `cat = 1`. For this part, we use the normal temperature.

Step 8: We blend the two losses into the total loss using our chosen weight.

Step 9: We slightly adjust the student's numbers to make this total loss smaller. This single adjustment is called one training step.

Step 10: We repeat Steps 3 to 9 for thousands of photos, again and again.

Slowly, the student's soft labels start to match the teacher's. The student learns not just the answers, but also the rich relationships between classes. After enough training, the student becomes a small, fast model that behaves almost like the big teacher.

We have a detailed blog on Gradient Descent that explains how this adjustment to the model's numbers works step by step.

This is how Knowledge Distillation actually trains the student. Now, let's see the different types of it.

### Types of Knowledge Distillation

Everything we have learned so far is the most common form, but there are three main types. The difference is simply about which part of the teacher the student copies. Let's keep it simple.

Response-based distillation. This is what we have been doing the whole time. The student copies the teacher's final output, which means the soft labels at the end. The student watches what the teacher answers and learns to answer the same way. This is the simplest and most popular type.

Feature-based distillation. A model does not jump straight from input to answer. It processes the input step by step through inner stages called layers. The output of these inner stages is called a feature, which is the model's internal understanding before the final answer. In feature-based distillation, the student copies these inner features of the teacher, not just the final output. It is like a student copying not only the senior's final answer but also the rough working and notes the senior wrote on the way.

Relation-based distillation. Here, the student learns the relationships between different things the teacher saw. For example, the teacher can treat two photos as very similar to each other. The student learns to keep those same two photos similar in its own understanding. So, the student copies the connections the teacher draws between examples, not just single answers.

So, to summarize the three types simply.

```
Response-based  ->  copy the teacher's FINAL answer (soft labels)
Feature-based   ->  copy the teacher's INNER understanding (features in layers)
Relation-based  ->  copy the RELATIONSHIPS the teacher sees between examples

```

Here, we can see that all three share the same goal. The student tries to behave like the teacher. They only differ in which part of the teacher's behavior the student copies. We can pick one based on our use case.

To master Knowledge Distillation, SLMs and Model Distillation, and Model Compression in depth, check out our AI and Machine Learning Program at Outcome School.

Now, let's look at where Knowledge Distillation is used in the real world.

### Real examples of Knowledge Distillation

DistilBERT. BERT is a famous language model used to understand text. It is powerful but big. DistilBERT is a distilled version of BERT. It is much smaller and faster, around 40% smaller and about 60% faster, while keeping roughly 97% of BERT's language understanding. This is a perfect example of the trade we want: a much lighter model that keeps almost all the accuracy.

Smaller chat models. Many small chat models are distilled from much larger chat models. The large model acts as the teacher and produces high-quality answers. The small model is trained to copy those answers. The result is a compact chat model that can run cheaply and reply fast, while still sounding close to the big one. We have a detailed blog on Small Language Models (SLMs) that covers these compact models end to end.

On-device AI. This is where distillation truly shines. When we want AI to run directly on a phone, a smartwatch, or a camera, the model must be tiny and quick. We distill a big, accurate model into a small student that fits on the device. So, features like offline translation, voice typing, and smart photo sorting can run right on the device, without sending data to a server. This means faster results, lower cost, and better privacy, because our data stays on the device. On-device models like these are usually shipped in the GGUF format. We have a detailed blog on how GGUF works that explains how these models are packed into one file.

So, now we know where we can use Knowledge Distillation, and why it matters so much for real products.

Distillation is one way to get a smaller model. Another is quantization, where we keep the same model but store its numbers using fewer bits. We have a detailed blog on how Model Quantization works that explains this from the ground up.

### Wrapping up Knowledge Distillation

Let's quickly recap everything in simple words.

A big model, the teacher, is accurate but slow and expensive. A small model, the student, is fast and cheap but less smart on its own. Knowledge Distillation trains the student to copy the teacher, so we get a small model that keeps most of the big model's accuracy.

The key idea is that the teacher does not just give the right answer. It gives soft labels, a full set of probabilities over all classes. These soft labels carry dark knowledge, which means they reveal how the classes relate to each other, like a cat being a little bit "dog" and nothing like a "car". We use a higher temperature in the softmax to make this dark knowledge clear and easy to learn.

We train the student with a combined loss. The distillation loss pulls the student toward the teacher's soft labels using KL divergence, and the normal loss keeps the student correct on the true hard labels. We repeat this over many examples until the student behaves like the teacher.

This is how Knowledge Distillation works.

### Does the teacher model change during Knowledge Distillation?

No. The teacher is a big model that is already trained and accurate. We do not change the teacher at all during distillation. It only gives lessons in the form of soft labels, and only the student's numbers are adjusted to make the total loss smaller.

### Why not train the small model only on the true labels?

Because hard labels throw away useful information. A hard label only says "it is a cat" and treats every other class as equally wrong. The teacher's soft labels also show how classes relate, like a cat being a little bit like a dog and nothing like a car. This dark knowledge teaches the student far more.

### Is the high temperature also used when the student model is deployed?

No. We use the higher temperature only during training, so the teacher's soft labels reveal the subtle relationships between classes. When the finished student is actually used in the real world, we go back to the normal temperature.

### Does the student simply copy the teacher's mistakes?

Not blindly. The total loss blends two parts. The distillation loss pulls the student toward the teacher's soft labels, and the normal loss compares the student to the true hard labels. This normal loss keeps the student grounded in the real, correct answers, so it does not blindly copy the teacher's mistakes.

### What is the difference between Knowledge Distillation and quantization?

Both make a model smaller, but in different ways. Knowledge Distillation trains a separate small student model to copy a big teacher model. Quantization keeps the same model but stores its numbers using fewer bits.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
