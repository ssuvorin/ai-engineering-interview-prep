> Source: https://outcomeschool.com/blog/ai-is-only-as-good-as-our-definition-of-done

# AI Is Only as Good as Our Definition of Done
URL: https://outcomeschool.com/blog/ai-is-only-as-good-as-our-definition-of-done
Published: 2026-08-25
Author: Amit Shekhar

AI Is Only as Good as Our Definition of Done

# AI Is Only as Good as Our Definition of Done

Authors
: - Name
: Amit Shekhar
Published on
: August 25, 2026

AI does its best work when we can clearly check whether a task is finished, and it struggles when only a human can judge the result. That clear check is our definition of done.

In this blog, we will learn about one simple idea, AI is only as good as our definition of done, which means the clear line we draw between a task that is finished and a task that is not. We will also see what a definition of done really is, why AI feels magical on the tasks that a machine can check, why it feels unreliable on the tasks that only a human can judge, how the loop that AI runs behind the scenes creates this exact gap, and how we can write a definition of done that turns a vague task into a checkable one.

We will cover the following:

- What is a definition of done?
- Tasks where the definition of done is exact
- Tasks where the definition of done is fuzzy
- Why AI is so strong exactly where we can measure
- How to write a better definition of done

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is a definition of done?

Whenever we give a task to AI, two things are involved.

The first thing is the goal. What do we want?

The second thing is the checker. How do we find out whether the AI actually did it?

Definition of Done = Goal + A way to check the goal

Most of the time, we give the goal and forget the checker. We say "build this feature", the AI gives us two hundred lines of code, and then we sit and read those lines to decide whether it is correct. In that case, we ourselves are the checker.

A checker, also called a verifier, is anything that can look at the output and say pass or fail without any opinion. A unit test is a checker. A compiler is a checker. A human reading the code is also a checker, but a slow one that gives a different answer on a tired day.

Here is the point of this blog. AI is extremely strong on the tasks that have a fast and exact checker, and unreliable on the tasks that do not have one. The difference is not in the intelligence of the model. It is in our definition of done.

## Tasks where the definition of done is exact

The best way to learn this is by taking an example.

Suppose we write the test first, like below:

```kotlin
@Test
fun `should return the discounted price`() {
    val price = calculateDiscountedPrice(1000, 20)
    assertEquals(800, price)
}

```

Now, we give the task to AI: write the `calculateDiscountedPrice` function so that this test passes.

Here, the definition of done is not a matter of opinion. Either the test is green or it is red. The AI can write the function, run the test, see the failure, fix the code, and run the test again. It repeats this loop on its own until the test passes.

Here, we can notice one important thing. We did not have to trust the AI. We just had to run the check.

Many tasks fall in this category:

- The code must compile. The compiler gives us a clear pass or fail.
- A function must return an exact output for an exact input. We compare, and we know.
- A bug must stop reproducing. We run the steps, and the crash is either there or it is gone.
- A SQL query must produce this exact result. We run it and compare the rows.
- A math answer must match the known answer. We check it directly.

In all of these, the machine checks the machine. There is a hard boundary between done and not done, and the AI can walk right up to it by itself.

This is why AI feels magical in these cases. Give it a failing test, and it will keep working until the test passes. The checker is doing the hardest job here, telling us the truth again and again.

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

## Tasks where the definition of done is fuzzy

Now, let's move to the other side.

We open the editor and type this: "Build the login feature."

The AI builds it. The code compiles. The screen opens. The user is able to log in.

Now, the big question. Is it done?

We do not know. And the reason is that we never said what done means.

Let's see what was hiding inside that one small sentence:

- What happens when the network fails in the middle?
- Is the token stored securely?
- What happens when the password field is empty?
- Is the error message good enough for a real user?
- Will this code be easy to change after six months?

Not a single one of these was written down. So not a single one can be checked. The AI produced something that looks complete, and looking complete is not the same as being complete.

But, here is the catch. In the unit test example, a red test told us clearly that we were not done. Here, nothing turns red. The absence of a failure is not the presence of correctness.

And there is one more trap. Sometimes the test exists and still it does not save us. If the test covers only the happy path, then green only proves that the happy path works. The AI will stop the moment the test turns green, because for the AI, green means done.

The same problem exists outside code:

- "Write a good summary for this content."
- "Design a clean architecture for this app."
- "Make this code more readable."

The words "good", "clean", and "readable" are doing all the work here, and not one of them can be checked by a machine.

So, in these tasks, the only checker left is a human being. And this is exactly why we cannot completely rely on the AI output here. Not because the AI is weak, but because nothing is standing between the output and us.

We have a detailed blog on LLM as a Judge that explains how we can use another model as the checker when no exact one exists.

## Why AI is so strong exactly where we can measure

Now, the question arises. Why is this difference so sharp?

The answer is in the loop.

AI does not write the perfect answer in one shot. It works in a loop. Try something, check the result, see the mistake, fix it, try again. This loop is where the real power is.

But this loop needs one thing to keep running. After every attempt, it needs an answer to a simple question: am I done or not?

Where a checker exists, the loop runs on its own.

The AI writes the function, runs the test, sees it red, reads the error, fixes the line, and runs the test again. It can repeat this ten times or fifty times without asking us anything. Every round gives it an honest signal, and every round brings it closer. The moment the test turns green, the loop stops by itself.

So, what we finally see is not the first attempt of the AI. It is the attempt that survived many rounds of checking.

Where a checker does not exist, the loop dies after the first round.

We ask for a clean architecture. The AI writes something. Now, there is nothing to run. Nothing turns red. Nothing turns green. No signal comes back, so the AI has no reason to try again, and it stops right there.

So, what we see here is only the first attempt. One guess, and we are reading it as a final answer.

Wherever a cheap and exact checker exists, the AI gets many tries. Wherever it does not exist, the AI gets only one try.

That is the whole difference we keep feeling as developers. Same model, same intelligence, but in one case it corrected itself fifty times before showing us the output, and in the other case it showed us the output straight away.

And when the checker is missing, we become the checker. We read the output, we find the problem, we ask for a change, and the AI tries again. The loop still runs, but now it runs at our speed, and it costs our time and attention on every single round.

## How to write a better definition of done

So, what do we do about it? The answer is simple to say and hard to do. We move our tasks from the fuzzy side to the exact side.

Let's see the practical ways.

Write the test first, then give the task. This is the biggest change we can make. The AI gets a target it can hit by itself, and we get a green or red answer instead of an opinion.

Give the exact input and expected output. Instead of "parse this date properly", we say: for the input `25-08-2026`, the output must be `2026-08-25`.

Give the command that must run clean. "The build command and the test command must both pass" is a definition of done. "Make sure it works" is not.

Turn the edge cases into actual cases. Do not write "handle the errors properly". Write the list. Empty input, network timeout, expired token, duplicate request. Every line in that list can now be checked.

Turn a vague quality into a number. "Make this API faster" cannot be checked. "The response must come under 200 ms for 1000 rows" can be checked.

We have a detailed blog on Harness Engineering in AI that explains how we build this checking layer around the model.

And then, one more step, which we usually skip.

Be honest about what is still not checkable. Some parts will always need our own judgement. Is this design right for where our product is going? No checker exists here, and pretending otherwise is how weak decisions enter our codebase quietly.

When we know which part has a checker and which part does not, we know exactly which part of the AI output we can accept and which part we must read ourselves. That is much better than reading everything with equal doubt.

The model is not the limit here. Our clarity is the limit. The sharper we can say what done means, the more work we can safely hand over.

So, before we give the next task to AI, let's ask one question first: how will I check this?

### What is a checker or verifier in AI coding?

A checker, also called a verifier, is anything that can look at the output and say pass or fail without any opinion. A unit test is a checker, and so is a compiler. A human reading the code is also a checker, but a slow one that can give a different answer on a tired day.

### Does a passing test mean the AI output is correct?

Not always. If the test covers only the happy path, then a green test only proves that the happy path works. The AI will stop the moment the test turns green, because for the AI, green means done. So, we turn the edge cases into actual test cases.

### Is AI weak at fuzzy tasks like clean architecture?

No. The model is not weak at these tasks. The difference is that no checker exists, so no signal comes back and the AI gets only one try. What we see is just its first attempt, while on tasks with a checker it may correct itself many times first.

### Can every part of a task be made checkable?

No. Some parts will always need our own judgement, like whether a design is right for where our product is going. We should be honest about what is still not checkable. Then we know which parts of the AI output we can accept and which parts we must read ourselves.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# LLM as a Judge
URL: https://outcomeschool.com/blog/llm-as-a-judge
Published: 2026-05-21

LLM as a Judge

Amit Shekhar

- May 21, 2026

In this blog, we will learn about LLM as a Judge. We will also see how it works, why we need it, and how we can use it to evaluate the output of other LLMs.

We will cover the following:

- What is LLM as a Judge?
- Why do we need LLM as a Judge?
- How does LLM as a Judge work?
- Types of LLM as a Judge.
- Steps to build an LLM Judge.
- A prompt template for LLM as a Judge.
- Chain-of-thought judging (G-Eval).
- Biases in LLM as a Judge.
- Best practices for LLM as a Judge.
- Real-world use cases of LLM as a Judge.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is LLM as a Judge?

LLM as a Judge is a technique where we use a large language model to evaluate the output of another large language model. The judge LLM reads the output, compares it against our criteria, and gives a score or a verdict with a reason.

In simple words, LLM as a Judge = LLM + Judge. We are using one LLM to judge the work of another LLM.

Let's say we have built a chatbot using an LLM. The chatbot gives answers to user questions. Now, we want to know how good these answers are. We can ask a human to read every answer and rate it. But this is slow and expensive. Instead, we can ask another LLM to read the answers and rate them for us.

This is the core idea of LLM as a Judge.

The judge LLM acts like a teacher checking the homework of a student. The student is another LLM. The teacher reads the homework, compares it with the expected answer, and gives a grade with feedback.

### Why do we need LLM as a Judge?

Before jumping into how it works, we must understand the problem it solves.

When we build an application using LLMs, we need to evaluate the quality of the output. The output of an LLM is open-ended text. There is no single correct answer. Two different answers can both be correct.

Let's see the traditional ways of evaluating LLM outputs and the problems with each approach.

Approach 1: Human evaluation.

We can ask humans to read every output and rate it. This gives high quality results because humans understand language well. But humans are slow. They are expensive. They get tired. They cannot evaluate millions of outputs every day.

The issue with this approach is that it does not scale. Let's see how the next approach solve this issue.

Approach 2: Rule-based metrics like BLEU and ROUGE.

We can use rule-based metrics that compare the output with a reference answer word by word. These metrics are fast and cheap. But they only check word overlap. They miss the meaning. An answer can be correct but use different words. These metrics will give it a low score.

The issue with this approach is that it does not understand meaning. Let's see how the next approach solve this issue.

Approach 3: LLM as a Judge.

We use another LLM to read the output and judge its quality. The LLM understands language. It understands meaning. It can compare two answers even if they use different words. It is fast. It is cheap compared to humans. It can evaluate millions of outputs every day.

So, here comes LLM as a Judge to the rescue.

It combines the quality of human evaluation with the speed and scale of automated metrics. This is the beauty of LLM as a Judge.

One more thing to notice. Studies have shown that strong LLM judges agree with human evaluators more than 80% of the time. This is roughly the same rate at which two humans agree with each other on the same task. So, a well-built LLM Judge is almost as reliable as a human evaluator, but much faster and much cheaper. This is the reason LLM as a Judge has become the default way of evaluating LLM applications.

The deeper question behind all of this is whether a task has an exact checker at all. We have a detailed blog on AI Is Only as Good as Our Definition of Done that explains this in depth.

### How does LLM as a Judge work?

The best way to learn this is by taking an example.

Let's say we have built a customer support chatbot. A user asks a question. The chatbot gives an answer. We want to know if the answer is helpful.

Here is how LLM as a Judge works step-by-step:

- Step 1: We take the user question and the chatbot answer.
- Step 2: We write a prompt for the judge LLM. The prompt tells the judge what to do. It includes the question, the answer, and the rules for judging.
- Step 3: We send this prompt to the judge LLM.
- Step 4: The judge LLM reads everything and gives a score with a reason.
- Step 5: We use this score to decide if our chatbot is doing a good job.

A simple prompt for the judge can be as below:

```
You are an expert evaluator. Read the user question and the assistant answer below. Rate the answer on a scale of 1 to 5 based on helpfulness.

User question: How do I reset my password?

Assistant answer: To reset your password, click on the Forgot Password link on the login page. Enter your email address. You will receive a reset link in your email.

Give your score as a number from 1 to 5. Also give a short reason for your score.

```

Here, we have given the judge a clear task. We have given the question, the answer, and the scoring rule.

The judge LLM will respond as below:

```
Score: 5
Reason: The answer is clear, step-by-step, and directly addresses the user question. It tells the user exactly what to do.

```

This is how LLM as a Judge works.

In a real system, this judge usually sits as one step inside a bigger flow, where a low score sends the work back for another attempt. We have a detailed blog on Graph Engineering that explains how such steps are wired together.

### Types of LLM as a Judge

There are four common ways to use LLM as a Judge. Let's learn about each of them.

Type 1: Single answer scoring.

We give the judge one answer and ask it to rate the answer on a scale, for example 1 to 5 or 1 to 10. The judge gives a score based on our criteria.

This is useful when we want to track the quality of our LLM over time. We can see if the average score is going up or down.

Type 2: Pairwise comparison.

We give the judge two answers to the same question. We ask the judge to pick the better one. The judge picks Answer A or Answer B and gives a reason.

This is useful when we are comparing two models or two versions of a prompt. We want to know which one is better.

Type 3: Reference-based evaluation.

We give the judge an answer and a reference answer. The reference answer is the correct or expected answer. The judge compares the two and gives a score based on how close they are in meaning.

This is useful when we have a ground truth answer and we want to check how close our LLM output is to that ground truth.

Type 4: Rubric-based evaluation.

We give the judge a rubric with multiple criteria. For each criterion, the judge gives a separate score. For example, the rubric can have accuracy, helpfulness, clarity, and tone as separate criteria. The judge gives a score for each one and an overall score at the end.

This is useful when quality is not a single number. A good answer must be correct, clear, and polite at the same time. Rubric-based evaluation tells us exactly where the answer is strong and where it is weak. This is the most common type used in production today.

Now, we have understood the types of LLM as a Judge. Let's see how we can build one.

### Steps to build an LLM Judge

Now, let's learn how to build our own LLM Judge step-by-step.

Step 1: Define the evaluation criteria.

First, we need to be very clear about what we want to evaluate. Are we evaluating helpfulness? Accuracy? Tone? Safety? We must write down the criteria in simple words.

For example, for a customer support chatbot, the criteria can be:

- Is the answer correct?
- Is the answer clear?
- Is the answer polite?

Step 2: Choose the judge model.

We need to pick which LLM will act as our judge. Generally, we use a strong model like GPT-5, Claude Opus 4.7, or Gemini 3.1 Pro as the judge. The judge must be at least as capable as the model we are evaluating. Otherwise, the judge will miss the mistakes.

We can also explore open-source judge models when we do not want to send our data to a closed API like OpenAI or Anthropic.

Step 3: Write the judge prompt.

We write a prompt that tells the judge what to do. The prompt must include:

[…585ln elided…]

This is how image embeddings work. They turn pictures into numbers that carry meaning, and that too in a way a computer can compare very easily.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

# What are Diffusion Models and How Do They Generate Images?
URL: https://outcomeschool.com/blog/diffusion-models
Published: 2026-06-03
Author: Amit Shekhar

What are Diffusion Models and How Do They Generate Images?

# What are Diffusion Models and How Do They Generate Images?

Authors
: - Name
: Amit Shekhar
Published on
: June 3, 2026

A Diffusion Model is a type of AI model that creates new data, such as images, by starting from pure random noise and slowly cleaning it up step by step until a clear image appears.

In this blog, we will learn about Diffusion Models. We will understand what they are, why we need them, how they work step by step, and how they generate amazing images like the ones we see in tools such as DALL-E, Stable Diffusion, and Midjourney.

We will cover the following:

- What is a Diffusion Model?
- Why do we need Diffusion Models?
- The two processes: Forward and Reverse
- The Forward Process (adding noise)
- The Reverse Process (removing noise)
- A step-by-step example walk-through
- How the model is trained
- A simple code example
- Conditional Diffusion (text to image)
- Advantages of Diffusion Models
- Where Diffusion Models are used

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is a Diffusion Model?

A Diffusion Model is a type of AI model that learns to create new data, such as images, by starting from pure random noise and slowly cleaning it up step by step until a clear image appears.

In simple words, a Diffusion Model learns how to turn noise into something meaningful.

So, where does the name come from? The word diffusion means spreading out, like a drop of ink spreading slowly in water until it mixes everywhere. A Diffusion Model first spreads noise into an image until the image is destroyed, and then learns to reverse this spreading to bring the image back.

So, what is noise? Noise is just random dots, like the static we see on an old television screen when there is no signal. It carries no meaning. It is pure randomness.

Now, the magic is this: a Diffusion Model takes this meaningless noise and gradually transforms it into a beautiful, meaningful image, one small step at a time.

Let's say we have a screen full of random dots. The Diffusion Model looks at it and removes a little bit of the randomness. Then it looks again and removes a little more. It keeps repeating this until a clear picture of, for example, a cat appears.

That is the core idea of a Diffusion Model.

Diffusion Models are one family inside the bigger world of Generative AI, and we have a detailed blog on What is Generative AI? that explains the whole idea from the ground up.

### Why do we need Diffusion Models?

The best way to learn this is by understanding the problem.

We want computers to create new images, new art, new designs, and new pictures that have never existed before. This is called image generation.

So, the question is: how can a computer create a brand new image from scratch?

This is a very hard problem. An image is made of millions of pixels, and every pixel must have the right color and the right place. If even a few pixels are wrong, the image looks broken and unrealistic.

Before Diffusion Models, we used models called GANs, which stands for Generative Adversarial Networks. GANs were powerful, but they were very hard to train. They were unstable, which means they often failed to learn properly, and sometimes they produced the same image again and again.

We needed a solution for that, and Diffusion Models were introduced to solve this problem.

Diffusion Models are stable to train, they produce very high quality and diverse images, and they have a simple core idea that is easy to understand. This is why Diffusion Models have become the most popular method for image generation today.

### The two processes: Forward and Reverse

A Diffusion Model is built on two processes that are opposite to each other.

- Forward Process: We take a clean image and slowly add noise to it, step by step, until it becomes pure noise.
- Reverse Process: We take pure noise and slowly remove the noise, step by step, until it becomes a clean image.

We can visualize both processes on the same chain like below:

```
             ADD NOISE   (forward, easy)   --------->

        +--------+--------+--------+-- ... --+--------+
        |  x_0   |  x_1   |  x_2   |         |  x_T   |
        +--------+--------+--------+-- ... --+--------+

          clean    little    more               pure
          image    noise     noise              noise

        <---------   (reverse, hard)   REMOVE NOISE

```

Here, we can see that the same chain runs in two opposite directions. Going left to right is the Forward Process, where we add a little noise at every step until the clean image `x_0` becomes pure noise `x_T`. Going right to left is the Reverse Process, where we remove a little noise at every step until the pure noise `x_T` becomes a clean image `x_0` again. The top arrow is easy and needs no learning. The bottom arrow is hard and is the part that the AI model must learn.

So, here is the key insight. The Forward Process is easy because adding noise is simple. We do not need any learning for it. We just keep adding random noise.

But the Reverse Process is the hard part. Removing noise to recover a real image is difficult. This is where the AI model comes into the picture. The model learns how to reverse the noise.

Let's understand this with an analogy.

Suppose we have a clear glass of water, and we slowly add drops of ink to it. Drop by drop, the water becomes more and more cloudy, until it is completely dark. This is the Forward Process. Adding ink is easy.

Now, the Reverse Process is like cleaning the water drop by drop until it becomes perfectly clear again. This is very hard, and we need a skilled helper to do it. In a Diffusion Model, the AI model is that skilled helper.

So, the model spends all its effort learning the Reverse Process. The Forward Process is only used during training to teach the model what noise looks like at every step.

### The Forward Process (adding noise)

Now, let's understand the Forward Process in detail.

We start with a real image. Let's call it the image at time step `0`, written as `x_0`.

Then, we add a small amount of random noise to it. Now we have a slightly noisy image at step `1`, called `x_1`.

We add a little more noise. Now we have `x_2`, which is noisier.

We keep repeating this for many steps, usually around `1000` steps. At the final step, called `x_T`, the image is completely destroyed and becomes pure random noise.

So, the Forward Process looks like below:

```
   x_0   ->   x_1   ->   x_2   ->   ...   ->   x_T

  clean      little     more                  pure
  image      noise      noise                 noise

```

Here, we can see that we move from a clean image on the left to pure noise on the right, by adding a small amount of noise at every step.

A very important point to understand is that the amount of noise added at each step is small and controlled. We use a schedule that decides how much noise to add at every step. This is called the noise schedule.

The good thing about the Forward Process is that it needs no learning at all. It is just a simple, fixed mathematical process of adding random noise. The model does not even take part in the Forward Process.

### The Reverse Process (removing noise)

Now, let's learn the Reverse Process, which is the heart of a Diffusion Model.

The Reverse Process does the exact opposite of the Forward Process. It starts from pure noise `x_T` and slowly removes the noise, step by step, until it reaches a clean image `x_0`.

So, the Reverse Process looks like below:

```
   x_T   ->   ...   ->   x_2   ->   x_1   ->   x_0

  pure                  more       little     clean
  noise                 noise      noise      image

```

Here, we can see that we move from pure noise on the left to a clean image on the right, by removing a small amount of noise at every step.

But here is the catch. Removing noise is very hard. We cannot do it with a simple fixed rule. We need a model that has learned what a real image looks like.

So, here comes the neural network to the rescue. A neural network is a model made of many connected layers that learns patterns from data.

The job of this neural network is simple to state. At every step, it looks at the noisy image and predicts the noise that was added. Once we know the noise, we can subtract it and get a cleaner image.

In simple words, the model is a noise predictor. We give it a noisy image, and it tells us, "Here is the noise that is hiding inside this image." We remove that noise and move one step closer to a clean image.

The neural network used here is usually a special architecture called a U-Net. A U-Net is good at taking an image as input and producing an image as output of the same size, which is exactly what we need to predict noise.

To learn how neural networks work from the ground up, we have a complete program on Deep Learning - Neural Networks, Backpropagation, and Optimizers - check out our AI and Machine Learning Program at Outcome School.

### A step-by-step example walk-through

Let's take a small example to make this concrete.

Suppose we want to generate a picture of a cat. We do not start with a cat. We start with pure noise.

Step 1: We begin with a screen full of random noise. This is `x_T`. It looks like the static on an old television screen when there is no signal. There is no cat anywhere in it.

Step 2: We pass this noise to the trained neural network. The model predicts the noise hidden inside it. We subtract a part of that noise. Now we have `x_(T-1)`, which is very slightly less noisy.

Step 3: We pass `x_(T-1)` to the model again. It predicts the noise again. We subtract it again. Now we have `x_(T-2)`. A very faint shape starts to appear.

Step 4: We keep repeating this process again and again. With every step, the image becomes cleaner. Slowly, the rough outline of a cat appears. Then the ears appear. Then the eyes. Then the fur details.

Step 5: After all the steps are done, we reach `x_0`. Now we have a clear, sharp image of a cat that never existed before.

So, the journey looks like below:

```
   Pure Noise   ->   Faint Shape   ->   Rough Cat   ->   Clear Cat

      x_T               x_500             x_100             x_0

```

Here, we can see that each step removes a little noise, and the cat slowly emerges out of the randomness. The model never draws the cat in one shot. It reveals the cat gradually, like cleaning a foggy mirror wipe by wipe.

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

### How the model is trained

Now, the next big question is: how does the model learn to predict the noise?

This is where the Forward Process becomes useful during training.

Let's understand the training in simple steps.

Step 1: We take a real image from our training data. Let's say it is a real photo of a cat.

Step 2: We pick a random time step, for example step `400`. Then we add the exact amount of noise for step `400` to the image. Since we are the ones adding the noise, we know precisely what noise we added.

Step 3: We give this noisy image to the neural network and ask it to predict the noise.

Step 4: We compare the noise predicted by the model with the actual noise that we added. The difference between them is the error, also called the loss.

Step 5: We adjust the model so that next time its prediction is closer to the real noise. This adjustment is done using a method called backpropagation, which slowly improves the model.

We repeat these steps millions of times with millions of images and random time steps. Over time, the model becomes an expert at predicting the noise at any step.

So, the beauty of the training is this. We always know the correct answer, because we added the noise ourselves. This makes the training stable and reliable, which is the big advantage over GANs.

### A simple code example

Let's see a simple code example to make the idea concrete.

First, let's see how we add noise in the Forward Process, as below:

```python
import torch

def add_noise(image, noise, alpha_bar_t):
    # alpha_bar_t controls how much original image remains
    noisy_image = (alpha_bar_t ** 0.5) * image + ((1 - alpha_bar_t) ** 0.5) * noise
    return noisy_image

```

Here, we have a function that takes a clean `image`, some random `noise`, and a value `alpha_bar_t` that controls how much of the original image stays. When `alpha_bar_t` is close to `1`, the image stays mostly clean. When it is close to `0`, the image becomes mostly noise. So, this single line mixes the clean image and the noise in the right proportion for that time step.

Now, let's see the training step where the model learns to predict the noise, as below:

```python
def training_step(model, image):
    t = torch.randint(0, 1000, (1,))          # pick a random time step
    noise = torch.randn_like(image)           # create random noise
    noisy_image = add_noise(image, noise, alpha_bar[t])

    predicted_noise = model(noisy_image, t)   # model predicts the noise
    loss = ((noise - predicted_noise) ** 2).mean()   # compare with real noise
    return loss

```

Here, we can see the full training logic. First, we pick a random time step `t`. Then, we create random `noise` and add it to the image to get a `noisy_image`. After that, the `model` predicts the noise from the noisy image. Finally, we compute the `loss`, which is the difference between the real noise and the predicted noise. We want this loss to become as small as possible.

Now, let's see how we generate a new image in the Reverse Process, as below:

```python
def generate(model):
    x = torch.randn(1, 3, 64, 64)             # start from pure noise
    for t in reversed(range(1000)):           # go from step 999 down to 0
        predicted_noise = model(x, t)         # predict the noise
        x = remove_noise(x, predicted_noise, t)   # subtract a part of it
    return x                                   # final clean image

```

Here, we can see the generation logic. We start with pure random noise `x`. Then, we loop from the last step down to the first step. In every step, the `model` predicts the noise, and we remove a part of it using `remove_noise`. After the loop finishes, `x` becomes a clean, brand new image.

This is how, in code, we add noise, train the model, and generate new images.

### Conditional Diffusion (text to image)

Till now, we have learned how a Diffusion Model generates a random image. But tools like DALL-E and Stable Diffusion do something more powerful. We type a sentence, and they create exactly that image.

So, now the question is: how does the model know what to draw?

This is where Conditional Diffusion comes into the picture.

In Conditional Diffusion, we give the model an extra input called a condition. The condition tells the model what we want. For text to image, the condition is our text prompt, for example "a cat sitting on a red sofa".

So, at every step of the Reverse Process, the model does not only look at the noisy image. It also looks at the meaning of our text. This way, it removes the noise in a direction that matches our text.

The text is first converted into numbers that capture its meaning. This conversion is done by a text understanding model such as CLIP. These numbers are then fed into the U-Net at every step, so the noise removal stays guided by our words.

In simple words, the text acts like a guide. Without the text, the model would create any random image. With the text, the model creates the specific image that we asked for.

This is exactly how we type "a cat sitting on a red sofa" and get that exact image.

### Advantages of Diffusion Models

Now, let's understand why Diffusion Models have become so popular.

- High quality: Diffusion Models produce very sharp, detailed, and realistic images.
- Stable training: Unlike GANs, Diffusion Models are stable to train because we always know the correct noise during training. The model rarely fails to learn.
- Diversity: Diffusion Models can produce a wide variety of different images. They do not get stuck producing the same image again and again.
- Flexible control: We can guide the generation using text, sketches, or other images. This gives us a lot of control over the final result.
- Simple core idea: The main idea, which is to add noise and then learn to remove it, is simple and easy to understand.

That's the beauty of Diffusion Models.

### Where Diffusion Models are used

Now, let's see where Diffusion Models are used in the real world.

- Text to image generation: Tools like DALL-E, Stable Diffusion, and Midjourney use Diffusion Models to create images from text prompts.
- Image editing: We can change a part of an image, remove an object, or fill in a missing area. This is called inpainting.
- Super resolution: We can take a low quality, blurry image and make it sharp and high resolution.
- Video generation: Newer models extend the same idea to create short videos from text.
- Audio generation: The same noise to signal idea is also used to generate music and speech.
- Science and medicine: Diffusion Models are used to design new molecules and to improve medical images.

Diffusion Models are the reason why we can now create stunning images just by typing a few words. The simple idea of adding noise and then learning to remove it has changed the way computers create art and content.

The same add-noise-then-remove-noise idea has now been carried over to text, where it powers a new kind of model. We have a blog on Diffusion Language Models (DLMs) that explains how this works for words.

This was all about Diffusion Models.

Now we must have understood what Diffusion Models are, why we need them, how they work step by step, and where they are used.

### Are Diffusion Models better than GANs?

Yes, for most image generation today. GANs were powerful but hard to train, unstable, and sometimes produced the same image again and again. Diffusion Models are stable to train because we always know the correct noise during training, and they produce very high quality and diverse images.

### Does a Diffusion Model create an image in one step?

No. A Diffusion Model never draws the image in one shot. It starts from pure noise and removes a little noise at every step, usually over around 1000 steps. The image is revealed gradually, like cleaning a foggy mirror wipe by wipe.

### Does the model have to learn the Forward Process?

No. The Forward Process needs no learning at all. It is a simple, fixed mathematical process of adding random noise, controlled by a noise schedule. The model spends all its effort learning the Reverse Process, and the Forward Process is only used during training to create noisy images.

### Can Diffusion Models generate things other than images?

Yes. Newer models extend the same idea to create short videos from text, and the same noise to signal idea is used to generate music and speech. Diffusion Models are also used to design new molecules and improve medical images. The idea has even been carried over to text through Diffusion Language Models.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

Our vision is to make tech education outcome-focused. Our mission is to help students master the internals and become great at system design to achieve the outcome they aspire to.

[Showing lines 1-387 and 973-1341 of 1341; 585 middle lines (28.4KB) elided. Read artifact://59 for full output]
