> Source: https://outcomeschool.com/blog/llm-as-a-judge

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

- The task description.
- The user input.
- The model output to be judged.
- The scoring scale and the rules.
- The output format we want.

Step 4: Run the judge on a sample.

We run the judge on a small sample of outputs. We read the scores and reasons given by the judge. We check if the judge is doing a good job.

Step 5: Compare with human ratings.

We ask humans to rate the same sample. We compare the human ratings with the judge ratings. If they match closely, our judge is good. If they do not match, we need to improve the judge prompt.

Step 6: Iterate and improve.

Based on the comparison, we update the judge prompt. We add more rules. We give better examples. We test again. We keep doing this until the judge ratings match the human ratings.

Step 7: Use the judge at scale.

Once we trust the judge, we can use it to evaluate thousands or millions of outputs. We can also use it to compare different models, different prompts, and different versions of our application.

Now, our LLM Judge is ready.

To master Evaluation of LLMs and Agents, LLM as a Judge, and Prompt Engineering, check out our AI and Machine Learning Program at Outcome School.

### A prompt template for LLM as a Judge

Let's see a complete prompt template that we can use for LLM as a Judge.

```
You are an expert evaluator. Your task is to evaluate the response given by an AI assistant to a user question.

Evaluate the response based on the following criteria:

1. Accuracy: Is the response factually correct?
2. Helpfulness: Does the response solve the user's problem?
3. Clarity: Is the response easy to understand?

User question:
{user_question}

Assistant response:
{assistant_response}

Give your evaluation in the following format:

Accuracy score (1-5): <score>
Helpfulness score (1-5): <score>
Clarity score (1-5): <score>
Overall score (1-5): <score>
Reason: <short explanation of your scores>

Be fair and consistent. Base your scores only on the response given above.

```

Here, we have built a clear and structured prompt. The judge LLM knows the task, the criteria, the input, and the output format. This makes the judge reliable and consistent.

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

### Chain-of-thought judging (G-Eval)

The basic prompt we have built so far works well, but we can make it much better. The trick is to ask the judge to think first and score later. This technique is called chain-of-thought judging and it is also known as G-Eval.

In simple words, G-Eval = Generate evaluation steps + Score. The judge first writes down the steps it will use to evaluate, then applies those steps to the answer, and only then gives a score.

Let's see why this works.

When we ask the judge to give a score directly, the judge picks a number quickly without much thinking. The score is often shallow. But when we ask the judge to first write the evaluation steps, the judge slows down. It reads the answer more carefully. It applies each step one by one. The final score is much more reliable.

A G-Eval style prompt can be as below:

```
You are an expert evaluator. Your task is to evaluate the response below.

Criterion: Helpfulness

Step 1: Write down the evaluation steps you will use to check if the response is helpful. Think carefully.
Step 2: Apply each step to the response one by one. Write your reasoning for each step.
Step 3: Based on your reasoning, give a final score from 1 to 5.

User question:
{user_question}

Assistant response:
{assistant_response}

Now, follow Step 1, Step 2, and Step 3 in order.

```

Here, we have asked the judge to think before scoring. The judge first builds its own checklist, then applies it, and finally gives the score. This is the same idea as chain-of-thought prompting, applied to evaluation.

Note: G-Eval gives much better agreement with human ratings than the basic scoring prompt. If we want a reliable judge, we must use chain-of-thought judging.

If we want to go deep into Chain of Thought (CoT) Prompting, Prompt Engineering, and LLM as a Judge, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

### Biases in LLM as a Judge

LLM as a Judge is powerful, but it is not perfect. The judge LLM can have biases. We must understand these biases so that we can handle them in the right way.

Style bias.

This is the most dominant bias in LLM judges today. The judge often prefers a certain writing style, for example bullet points over paragraphs, or formal tone over casual tone. This style preference can be very strong and it can override the actual quality of the answer. The judge rewards the look and feel of the answer, not just the content. So, we must tell the judge in the prompt exactly what style is expected for our use case.

Position bias.

When we ask the judge to pick between Answer A and Answer B, the judge often prefers the answer that comes first. This is called position bias. To fix this, we can swap the order and run the judge twice. We take the average of the two results.

Verbosity bias.

The judge often prefers longer answers, even when the shorter answer is better. The judge sees more words and thinks the answer is more detailed. To fix this, we can tell the judge in the prompt to not prefer longer answers.

Self-preference bias.

This bias shows up at the time of evaluation. When the judge is asked to compare two answers, it gives a higher score to the answer that was generated by itself or by a model from its own family. For example, if we ask GPT-5 to pick between a GPT-5 answer and a Claude answer, GPT-5 picks itself more often than it should. The judge is doing the comparison fairly in its own mind, but it has a hidden preference for its own style. To fix this, we can use a different model as the judge, or use a Panel of Judges from different families.

Preference leakage.

This is a bigger problem and it works at the pipeline level, not at the single answer level. Self-preference bias is the mechanism. Preference leakage is what happens when this mechanism contaminates our whole evaluation setup.

Let's see an example. Suppose we use GPT-5 to generate synthetic training data for our model. Then we use GPT-5 again as the judge to evaluate the trained model. The judge silently rewards answers that look like GPT-5 style, because the training data already pushed our model in that direction. Our scores look amazing on paper. But in the real world, with real users, the model does not perform as well as the scores suggest.

The data generator and the judge are not independent anymore. The eval is contaminated. To avoid this, the judge model family must be different from the family used to generate training data, prompts, or any other input that touches our pipeline.

Authority and bandwagon bias.

The judge often defers to confident-sounding answers and answers that quote experts or sources. Even if the content is wrong, the judge gives a high score because the answer sounds authoritative. Similarly, the judge can follow the crowd. If many earlier answers agree, the judge tends to agree as well, even when it should not. To fix this, we must remind the judge in the prompt to focus only on correctness, not on tone or confidence.

Now, we have understood the biases. Even frontier judge models still fail on bias-heavy tasks, so we must always test our judge against these biases before trusting it in production.

### Best practices for LLM as a Judge

Few important points to keep in mind:

- Use a strong judge model. The judge must be at least as capable as the model being judged.
- Write a clear prompt. The prompt must include the task, the criteria, the input, the output, and the format.
- Give examples in the prompt. Few-shot examples help the judge understand what a good score looks like.
- Use a clear scoring scale. A 1 to 5 scale is easier than a 1 to 100 scale. The judge gives more consistent scores on a small scale.
- Ask for a reason with the score. This makes the judge think more carefully. It also helps us debug the judge.
- Validate against humans. Always compare the judge ratings with human ratings on a sample. This tells us if we can trust the judge.
- Handle position bias. When doing pairwise comparison, swap the order and average the results.
- Use a Panel of LLM Judges. This is also called the Jury approach. We use more than one judge model from different families and average the scores. A panel reduces self-preference bias and gives more reliable results than any single judge.
- Keep the criteria simple. Do not ask the judge to evaluate too many things at once. Break it into separate evaluations if needed.

If we follow these practices, our LLM Judge will be reliable and useful.

### Real-world use cases of LLM as a Judge

LLM as a Judge is used in many real-world scenarios across the industry. Let's see some of them.

Model evaluation.

When we train or fine-tune an LLM, we need to know if the new version is better than the old version. We use LLM as a Judge to compare the outputs side by side. This is much faster than human evaluation.

Chatbot quality monitoring.

In a production chatbot, we cannot read every conversation. We use LLM as a Judge to score the conversations automatically. We get a daily report on how well the chatbot is doing.

Content moderation.

We can use LLM as a Judge to check if the output is safe. The judge reads the output and decides if it contains harmful content. We block such outputs before they reach the user. This is exactly how an output guardrail works, and we have a detailed blog on How do LLM guardrails work? that explains it step by step.

RAG system evaluation.

In a Retrieval-Augmented Generation (RAG) system, we need to check if the answer is grounded in the retrieved documents. LLM as a Judge can check if the answer matches the documents. This helps us catch hallucinations, where the LLM makes up information that is not present in the documents.

Prompt engineering.

When we try different prompts for the same task, we need to know which prompt gives the best results. LLM as a Judge helps us compare prompts at scale.

Agent trajectory evaluation.

In agentic systems, the agent takes multiple steps to solve a task. The agent calls tools, reads results, plans next actions, and so on. This full sequence of steps is called the trajectory. LLM as a Judge can read the full trajectory and decide if the agent picked the right tools, used them correctly, and reached the right answer. This is one of the fastest growing applications of LLM as a Judge because agentic systems are hard to evaluate with any other method. We have a detailed blog on AI Agent Evaluation that explains this in depth.

This way we can use LLM as a Judge to solve any evaluation problem in a very simple way.

Now we must have understood LLM as a Judge. It is a powerful technique that combines the quality of human evaluation with the speed and scale of automation. As LLM applications grow, LLM as a Judge becomes more and more important because we cannot scale human evaluation easily, but we can scale LLM evaluation very easily.

I will highly recommend that we always validate our LLM Judge against human ratings before trusting it.

This way we can use LLM as a Judge to evaluate the quality of our AI systems and build better products for our users.

[…384ln elided…]

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

[Showing lines 1-371 and 756-1124 of 1124; 384 middle lines (17.0KB) elided. Read artifact://89 for full output]
