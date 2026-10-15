> Source: https://outcomeschool.com/blog/decoding-deep-rl-from-human-preferences

# What is Deep RL from Human Preferences? The Paper That Started RLHF
URL: https://outcomeschool.com/blog/decoding-deep-rl-from-human-preferences
Published: 2026-08-17

What is Deep RL from Human Preferences? The Paper That Started RLHF

# What is Deep RL from Human Preferences? The Paper That Started RLHF

Authors
: - Name
: Amit Shekhar
Published on
: August 17, 2026

In this blog, we are going to learn about Deep Reinforcement Learning from Human Preferences, the 2017 paper that started it all. It taught machines what we want by simply asking us to pick which of two behaviors looks better. This is the origin of RLHF, the technique behind ChatGPT.

We will cover the following:

- The building blocks we must know first
- The big picture: what the paper does
- Why it was needed: the reward problem
- Trajectory segments, or clips
- The human comparison
- The reward model and the preference math
- Training the reward model
- Training the agent with reinforcement learning
- The loop and the smart bits
- The results: the backflip and beyond
- The legacy: this is RLHF
- What this looks like today
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

The paper showed how to teach a machine a goal without ever writing down a reward. Instead of hand-coding what "good" means, we show a human two short clips of the agent's behavior and let them pick the better one. From thousands of these simple choices, the machine learns what we want.

The paper is "Deep Reinforcement Learning from Human Preferences" by Paul Christiano, Jan Leike, and their team, a collaboration between OpenAI and DeepMind.

This is the origin of RLHF (Reinforcement Learning from Human Feedback), the exact technique that later aligned InstructGPT and ChatGPT. Here, the agent learned to play games and control robots. Later, the same idea was used on language models, where the game clips became text answers.

## The building blocks we must know first

Before jumping into the paper, we must know a few simple words.

- Agent - the thing being trained to act, like a game player or a robot.
- Reward - a number telling the agent how well it is doing. Normal reinforcement learning maximizes this.
- Reward function - the rule that produces the reward. Usually hand-written, and that is the problem.
- Policy - the agent's strategy: given a situation, which action to take.
- Trajectory - a sequence of the agent's observations and actions over time.

That is everything we need. Now, let's move to the big picture.

## The big picture: what the paper does

Before going into the details, let's see the simple input-to-output view.

```
   Agent acts  ->  produces short clips of behavior
                            |
                            v
   Human is shown two clips  ->  picks the better one
                            |
                            v
   A reward model learns what "better" means
                            |
                            v
   Agent is trained by RL to get more of that "better"
                            |
                            +--------> loops back, again and again

```

These three pieces, the agent, the human comparisons, and the reward model, run together in a loop. The human never gives a number. They only compare. From those comparisons, the machine figures out the reward on its own.

## Why it was needed: the reward problem

Normal reinforcement learning needs a reward function: a rule that scores how well the agent is doing. But for many real tasks, we cannot write a good reward function.

How do we write a number for "do a backflip"? Or "summarize this article well"? These goals are easy to recognize but very hard to put into a formula. And when we try, the agent often games our formula: it maximizes the literal number in a way that misses what we actually wanted. A famous example: a boat-racing agent rewarded for points learned to drive in circles collecting points forever, instead of finishing the race. This is called reward hacking.

So the question was: what if we never write the reward at all, and instead learn it from human judgment? That is exactly what this paper did.

## Trajectory segments, or clips

The agent's behavior is broken into short clips, called trajectory segments, each about one to two seconds long. A clip is a little movie of what the agent did: its observations and its actions over that short window.

Why clips and not single frames? Because behavior only makes sense over time. We cannot tell if a robot is doing a backflip from a single freeze-frame; we need to see the motion. So the unit of comparison is a short clip.

## The human comparison

Here is the key human step. We show a person two clips side by side, and they simply click the one that looks better (or mark them equal, or skip if they cannot tell).

This is what the person sees:

```
   +------------------+          +------------------+
   |      Clip 1      |          |      Clip 2      |
   |   (1-2 seconds)  |    vs    |   (1-2 seconds)  |
   +------------------+          +------------------+
             |                             |
             +--------------+--------------+
                            |
                            v
                  The human picks one of:
             [ Clip 1 ]          [ Clip 2 ]
             [ Both equal ]      [ Cannot tell ]

```

Here, we can see that the human has only four buttons. Two of them say which clip is better, one says they are the same, and one says the person cannot tell. There is no place to type a number anywhere on this screen.

That is all the human does. No scores, no numbers, no writing a reward function. Just "this one is better than that one." Comparing two things is far easier and more reliable for people than assigning an absolute score. From many such comparisons, the machine will learn the reward.

## The reward model and the preference math

Now the math, and it is the same idea later used in RLHF for language models. We train a small neural network, the reward model `r`, that predicts a reward for each step. For a clip, we add up its predicted rewards to get the clip's total.

Let's see how one clip gets its total:

```
   Clip 1 (a short window of the agent's behavior)

    step 1        step 2        step 3
      |             |             |
      v             v             v
   [ reward ]    [ reward ]    [ reward ]     <- the same reward model
   [ model  ]    [ model  ]    [ model  ]        runs on every step
      |             |             |
      v             v             v
      1      +      0      +      1      =  2   <- the clip's total

```

Here, we can see that the reward model looks at one step at a time and gives each step a number. We then add those numbers to get one total for the whole clip. So a clip is not scored by a special "clip model", it is just the sum of the step scores.

Then we turn two clip totals into a probability that one is preferred, using the Bradley-Terry formula:

```
P(clip 1 preferred) = exp(total reward of clip 1) / ( exp(total of clip 1) + exp(total of clip 2) )

```

Let's define every symbol:

- `total reward of a clip` is the sum of the reward model's predictions over every step in that clip.
- `exp` means `e` to the power of that total.
- `P(clip 1 preferred)` is the probability the model thinks clip 1 is the better one.

Suppose clip 1 has predicted step rewards `[1, 0, 1]`, so its total is `1 + 0 + 1 = 2`. And clip 2 has `[0, 0, 1]`, so its total is `1`. Now:

```
exp(2) = 7.389
exp(1) = 2.718
P(clip 1 preferred) = 7.389 / (7.389 + 2.718) = 7.389 / 10.107 = 0.731
P(clip 2 preferred) = 2.718 / 10.107 = 0.269

```

So the model is about 73% sure clip 1 is better. The two probabilities add to 1.0. And if both clips have the same total, say both `2`, then `7.389 / (7.389 + 7.389) = 0.5`, a coin flip, exactly as it should be.

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

## Training the reward model

Now we train the reward model so its predictions match the human's choices. We use cross-entropy loss (see the math behind cross-entropy loss): if the human picked clip 1, the loss is `-log(P(clip 1 preferred))`.

Let's see it. The human picked clip 1, and our model said `P(clip 1 preferred) = 0.731`:

```
loss = -log(0.731) = 0.313

```

Now suppose the model had been wrong, saying only `P(clip 1 preferred) = 0.20`:

```
loss = -log(0.20) = 1.609

```

The loss is much bigger when the model disagrees with the human. So training pushes the reward model to give the human's preferred clip a higher total reward. Over thousands of comparisons, the reward model learns to score behavior the way the human would.

So the whole training of the reward model is this one formula:

```
loss = -log( exp(total of the clip the human picked) / ( exp(total of clip 1) + exp(total of clip 2) ) )

```

Now, every part of this formula is clear. We run the reward model on every step of a clip and add up the numbers to get the clip's total. We turn the two totals into a probability with the Bradley-Terry formula. Then we take the negative log of the probability of the clip the human actually picked, and we train the reward model to make that loss small.

Note: the numbers we used, like `[1, 0, 1]`, are just for the sake of understanding. In real training, a clip is one to two seconds long, so it holds many more steps than three, and the reward model is a neural network whose predictions are any real numbers, not neat `0` s and `1` s. The weights of that network are learned during training. But the math is exactly the one we just did by hand.

## Training the agent with reinforcement learning

Once we have a reward model, the rest is ordinary reinforcement learning. The agent is trained with a standard RL algorithm, the paper used A2C for Atari games and TRPO for robots, modern RLHF uses PPO to maximize the predicted reward from the reward model. The agent never sees a true game score. It only chases the learned reward.

So the missing reward function has been replaced by one learned from human preferences, and normal RL takes over from there.

## The loop and the smart bits

All three pieces run together. The agent keeps acting and producing clips, humans keep comparing some of them, the reward model keeps improving, and the agent keeps chasing the latest reward model. The reward is a moving target that gets better over time.

Two clever touches made it efficient:

- Ask about the confusing clips. They trained several reward models, called an ensemble, and asked the human to compare the clip pairs where these models disagreed the most. The idea is to spend scarce human attention where the machine is most unsure. The paper is honest about this one: it calls the trick a crude approximation, and its own ablation experiments show that on some tasks it actually made the results worse. So this is a good idea, not a solved problem.
- Normalize the rewards. Only the relative reward matters, so they scaled the reward model's outputs to have zero mean and a constant standard deviation. This keeps the numbers in a steady range and keeps training stable, even while the reward model itself keeps changing.

## The results: the backflip and beyond

- The backflip. A simulated robot learned to do a backflip from only about 900 human comparisons, collected in under an hour. There is no natural reward function for "do a backflip", yet the behavior was learned purely from human clicks.
- Less than 1% feedback. Across Atari games and robot tasks, the agent learned complex behaviors with human feedback on less than 1% of its interactions, never seeing the true reward.
- Sometimes better than the true reward. On the game Enduro, learning from preferences matched or beat training on the real game score. Human labelers reward any small progress, which gives a smoother, easier-to-learn signal than the sparse true score.

## The legacy: this is RLHF

This paper is the seed of everything.

- 2017, this paper: learn a reward from human preferences, for games and robots.
- 2020, Learning to Summarize: the same recipe applied to a language task, summarization.
- 2022, InstructGPT: RLHF applied to GPT-3, which produced helpful, instruction-following models.
- Late 2022, ChatGPT: the same recipe in a chat product, which changed the world.

The recipe never changed: collect human comparisons, train a Bradley-Terry reward model, optimize a policy with reinforcement learning. The only difference is that game clips became pairs of text answers, and A2C became PPO.

## What this looks like today

The core idea is still here, but the field has learned a lot since 2017. Now, let's see what changed.

- Reward hacking came back, and we found a leash for it. The agent chases the learned reward, so it learns to fool the reward model instead of doing the real task. In language models, this shows up as weird text that scores high and reads like nonsense. The fix used in RLHF today is a KL penalty: we subtract a small amount of reward when the model drifts too far from the original model. Notice that the problem this paper solved for hand-written rewards comes right back for learned ones, just in a milder form.
- The separate reward model became optional. DPO showed that the same Bradley-Terry math can be rearranged so the language model is its own reward model. So we train directly on the preference pairs, with no reward model and no RL loop.
- AI feedback replaced a lot of human feedback. Paying people to compare clips is slow and expensive. So labs now often use another model as the judge, an idea called LLM as a judge. Constitutional AI goes further, where the model critiques its own answers against a written list of principles.
- For checkable tasks, we do not need an opinion at all. In math and code, we can simply check whether the answer is correct. This is called reinforcement learning with verifiable rewards, and it powers the newest large reasoning models. The popular algorithm here is GRPO, which grades a whole group of answers against each other instead of training a separate scorer.

So today, human preferences are used for taste and safety, where there is no right answer, and verifiable rewards are used for reasoning, where there is one. But it all traces back to this one idea: do not write the reward, learn it from what humans prefer.

## Quick Summary

We have decoded the Deep RL from Human Preferences paper piece by piece. Let's recap each piece in one line.

- The paper learns a reward from human preferences instead of hand-coding it; this is the origin of RLHF.
- The reward problem: many goals (a backflip, a good summary) cannot be written as a formula, and bad formulas get hacked.
- Clips: behavior is broken into short one-to-two-second clips, because behavior only makes sense over time.
- The human comparison: a person just picks the better of two clips, no scores, which is easy and reliable.
- The preference math: a reward model sums each clip's rewards, and the Bradley-Terry formula turns two totals into a preference probability.
- Training the reward model: cross-entropy loss pushes the human's preferred clip to a higher reward.
- Training the agent: ordinary RL (A2C, TRPO, or modern PPO) maximizes the learned reward.
- The loop: agent, human, and reward model run together, asking about the most confusing clips, though the paper admits that trick does not always help.
- The results: a backflip from about 900 comparisons, complex tasks with under 1% feedback, sometimes beating the true reward.
- The legacy: this exact recipe became RLHF, the technique behind InstructGPT and ChatGPT.
- Today: a KL leash holds back reward hacking, DPO removes the separate reward model, AI feedback replaces much of the human labeling, and verifiable rewards with GRPO power reasoning models.

Now, we have decoded Deep RL from Human Preferences piece by piece and understood how learning a reward from simple human comparisons became the foundation of how we align AI today.

That's it for now.

Thanks

# What is LoRA (Low-Rank Adaptation) and How Does It Fine-Tune LLMs?
URL: https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms
Published: 2026-04-24

What is LoRA (Low-Rank Adaptation) and How Does It Fine-Tune LLMs?

# What is LoRA (Low-Rank Adaptation) and How Does It Fine-Tune LLMs?

Authors
: - Name
: Amit Shekhar
Published on
: April 23, 2026

LoRA (Low-Rank Adaptation) is a way to fine-tune a large model without updating all of its weights. It keeps the original weights frozen and learns a tiny pair of extra matrices on the side.

In this blog, we will learn about LoRA - Low-Rank Adaptation of Large Language Models.

Today, we will cover the following topics:

- The Big Picture
- Why Full Fine-Tuning Is Expensive
- The Core Idea Behind LoRA
- How LoRA Works Step by Step
- A Small Numeric Example
- Where LoRA Is Applied in a Transformer
- Merging LoRA Back Into the Model
- Real-World Use Cases
- Quick Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

LoRA is a way to fine-tune a large model without updating all of its weights. Instead of changing the original weight matrix, we keep it frozen and learn a tiny pair of extra matrices on the side. These tiny matrices capture the "adjustment" we want.

In simple words:

LoRA = Frozen original weights + A small low-rank update learned on the side.

This makes fine-tuning much cheaper, faster, and lighter on storage. And, we still get strong task-specific performance.

## Why Full Fine-Tuning Is Expensive

Before jumping into LoRA, we must first understand why full fine-tuning is hard.

We can learn everything about fine-tuning in this video.

A modern Large Language Model can have billions of parameters. For example, a 7 billion parameter model has 7 billion numbers inside it. When we do full fine-tuning, we update every single one of these numbers.

This causes the following issues:

- GPU memory explodes. We need to keep the weights, the gradients, and the optimizer states in memory. For Adam, this can be 3 to 4 times the size of the model itself.
- Training is slow. Updating billions of parameters takes a lot of compute.
- Storage is heavy. Each fine-tuned copy of the model is the same size as the original. If we have 10 different tasks, we need 10 full copies of a multi-gigabyte model.
- Sharing is hard. A multi-gigabyte checkpoint per task is not easy to ship to users.

We need a smarter way. We need a way to adapt the model to a new task without touching most of its weights.

So, here comes LoRA to the rescue.

## The Core Idea Behind LoRA

The full form of LoRA is Low-Rank Adaptation.

Let's decompose the name:

LoRA = Low-Rank + Adaptation.

- Adaptation means we are adapting the model to a new task or a new style.
- Low-Rank means the change we apply to the weights is represented in a very compact form using two small matrices.

The idea is based on a powerful observation from the original LoRA paper from Microsoft:

> When we fine-tune a large model, the actual update that we apply to the weights is very low-rank. We do not need a full giant update matrix - a much smaller one is enough.

[…634ln elided…]

Now, here is something important to notice. To get this list of numbers, we have to send the text to a model and ask it to compute the embedding. This step is not free. We will come back to this point soon, because it is the heart of the Embedding Cache.

### A quick recap of how we get an embedding

To understand the Embedding Cache, we must understand one thing about how we get an embedding.

We do not compute embeddings by hand. We use an embedding model. An embedding model is a special model whose only job is to take text and return its embedding, that list of numbers we just talked about.

So, the flow is simple. We send some text to the embedding model, and it sends back the embedding.

We can picture it as below:

```
   "I love dogs"   -->   [ Embedding Model ]   -->   [0.12, -0.85, 0.33, ...]
       (text)                (does work)                  (the embedding)

```

Here, we can see that the text goes in on the left, the embedding model does some work in the middle, and the list of numbers comes out on the right.

Now, here is the key point to remember.

Asking the embedding model to compute an embedding costs real money and real time.

Most embedding models run on a server, and we usually pay based on how much text we send. Even if we run the model on our own machine, computing an embedding uses real computing power and takes real time. So, every single embedding we compute has a cost, both in money and in delay.

So, if we ask the model to compute the embedding for the same text many times, we pay for the same work again and again. That is wasteful.

This is the foundation we needed. Now we are ready to understand the problem.

To learn how embeddings work and how they power modern AI systems, we cover Embeddings from the ground up in our AI and Machine Learning Program at Outcome School.

### What is an Embedding Cache?

Now that we know how we get an embedding, let's understand the Embedding Cache.

An Embedding Cache is a place where we store embeddings we have already computed, so that the next time we need the embedding for the same text, we grab the stored one instead of computing it again.

In simple words, an Embedding Cache means: compute the embedding once, then reuse it.

The word "cache" simply means a place where we store something so we can grab it quickly later, instead of making it again from scratch.

Let's connect this to what we just learned. Computing an embedding costs money and time. So, the first time we compute the embedding for a piece of text, we save it in the cache. The next time we need the embedding for that exact same text, we do not call the embedding model at all. We simply look it up in the cache and return the saved list of numbers.

So, an Embedding Cache is about never paying to compute the embedding for the same text twice.

Now, the question is, why do we even need this? Let's see.

### Why we need an Embedding Cache

The same text comes up again and again, far more often than we would expect. Let's understand this with two common situations.

The first situation is re-ingestion. Ingestion means the process of taking our documents, breaking them into small pieces, and computing an embedding for each piece so we can search them later. Now, suppose we update one paragraph in a large document and run the ingestion again. Most of the document did not change at all. But if we are not careful, we recompute the embedding for every single piece, even the ones that are exactly the same as before. We pay all over again for work we already did.

We can picture this re-ingestion like below:

```
   document broken into pieces, then re-ingested after editing one piece

   piece 1   unchanged   -->  reuse from cache   (free)
   piece 2   unchanged   -->  reuse from cache   (free)
   piece 3   EDITED      -->  compute again      (pay once)
   piece 4   unchanged   -->  reuse from cache   (free)
   piece 5   unchanged   -->  reuse from cache   (free)

```

Here, we can see that only piece 3 changed, so only piece 3 needs a new embedding. With a cache, the four unchanged pieces are reused for free. Without a cache, we would recompute all five, paying for work we already did.

The second situation is repeated queries. Imagine we have a search system used by thousands of people. Many people search for the same popular things. Hundreds of users type the same query, such as "return policy" or "reset my password." Each time, we need the embedding of that query to search. Without a cache, we compute the embedding for "return policy" hundreds of times, even though it is the exact same text every time.

Let's put some numbers to it for the sake of understanding. Suppose:

- A popular query is searched 1,000 times in a day.
- Without a cache, we compute its embedding 1,000 times.
- With a cache, we compute it once and reuse it 999 times.

That is 999 calls saved for just one popular query.

This causes two real problems when we have no cache:

- It is costly. We pay for every embedding we compute. Recomputing the same embedding again and again means we pay for the same work over and over.
- It is slow. Calling the embedding model adds delay. If the model runs on a server, we also wait for the network. Doing this for text we have already processed adds delay for no reason.

So, here comes the Embedding Cache to the rescue.

### The core idea behind an Embedding Cache

Let's understand the core idea step by step.

We learned that computing an embedding is the costly part. The Embedding Cache takes a simple but powerful step.

The idea is to store every embedding we compute, paired with the text it came from. Before computing a new embedding, we first check the cache. If the embedding for that text is already there, we reuse it and skip the costly computation.

Let's walk through it with our example.

Step 1: A user searches for "return policy." We check the cache. The embedding is not there yet, because this is the first time. So, we call the embedding model, get the embedding, and save it in the cache. Then we use it for the search.

Step 2: Another user searches for "return policy" later in the day. We check the cache. This time, the embedding is already there, because we saved it in Step 1. So, we skip the embedding model completely and use the saved embedding directly.

So, the second search did not pay any cost to compute the embedding. It simply read the saved one.

Let's see a simple diagram to make this clear as below:

```
WITHOUT an embedding cache (every time):

   "return policy"  -->  call the model  -->  compute embedding   (slow, costly, repeated)

WITH an embedding cache (after the first time):

   "return policy"  -->  found in cache  -->  return saved embedding   (fast, cheap)
                         skip the model

```

The problem is solved. We now compute the embedding for a piece of text only once. So, for our popular query searched 1,000 times, we pay for one computation and reuse it the other 999 times.

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

### The cache key, a hash of the text plus the model

Now, there is one very important detail we must understand, because this is what makes the cache reliable.

To store and find something in a cache, we need a key. A key is a label we attach to a stored item, so we can find it again later. Think of it like the name on a folder in a filing cabinet. We need the right name to pull out the right folder.

So, the question is, what should we use as the key for an embedding?

The simplest answer is to use the text itself. But there are two problems with using the raw text directly. First, the text can be very long, like an entire paragraph, which makes for a clumsy key. Second, and much more important, the same text can be sent to different embedding models, and each model produces a different embedding for the same text.

Let's understand this clearly. Suppose we have two embedding models, an older one and a newer one. We send "return policy" to both. They return different lists of numbers, because they are different models. The same thing happens if we simply upgrade one model to a new version, because a new version also produces different numbers. If our key was just the text "return policy," then both models would try to use the same cache spot. The newer model would read the older model's embedding and get the wrong numbers. This is called a collision, which means two different things accidentally landing on the same key.

So, here is the rule we must follow.

The cache key is built from the text plus the model name and version. This way, different models never collide.

To turn this into a short, neat key, we use a hash. A hash is a function that takes any input, no matter how long, and turns it into a short fixed-length string of characters. The same input always produces the same hash, and even a tiny change in the input produces a completely different hash. So, a hash is a perfect way to make a compact, unique key from a long piece of text.

We can picture the key like below:

```
   text:  "return policy"
   model: "text-embedding-v3"
                  |
                  v
        combine them together
                  |
                  v
            apply a hash
                  |
                  v
   key:  "a3f9c1...b27"   (short, unique, model-specific)

```

Here, we can see that we take the text and the model name together, then run them through a hash to get a short unique key. Because the model name is part of the key, the older model and the newer model get different keys for the same text, so they never read each other's embeddings.

This is how the cache stays correct even when we use more than one embedding model.

### The request flow, a hit and a miss

Now, let's put the whole thing together and walk through exactly what happens on a single request.

Before that, we must learn two simple words.

A cache hit means the embedding we are looking for is already in the cache. We found it, so we reuse it.

A cache miss means the embedding is not in the cache yet. We did not find it, so we have to compute it.

Let's see the full flow as below:

```
   request: need embedding for some text
                  |
                  v
        hash the text + model name  -->  get the key
                  |
                  v
        is the key in the cache?
            |                 |
           YES               NO
        (cache HIT)       (cache MISS)
            |                 |
            v                 v
     return the saved    call the embedding model
        embedding         and compute it
                              |
                              v
                        store it in the cache
                        under the key
                              |
                              v
                        return the embedding

```

Here, we can see the complete journey. First, we take the text and the model name and hash them to get the key. Then, we check whether that key is already in the cache. If it is a hit, we return the saved embedding right away and we are done, no model call needed. If it is a miss, we call the embedding model, compute the embedding, store it in the cache under that key, and then return it.

Notice the beautiful part. After a miss, we store the result. So, the very next time the same text comes in, it becomes a hit. The first request pays the cost, and every request after that for the same text is fast and free.

The problem is solved. Every piece of text is computed at most once.

### Eviction, LRU and TTL

Now, the next question is, does the cache keep growing forever? The answer is no. A cache has limited space, and we cannot store everything forever. So, at some point, we must remove old items to make room for new ones. This removing of items is called eviction.

In simple words, eviction is the cache throwing out some old stored items so it does not run out of space.

There are two common ways to decide what to evict. Let's understand both.

The first way is LRU, which stands for Least Recently Used. The idea is simple. When the cache is full and we need room, we throw out the item that has not been used for the longest time. The thinking is that if we have not needed an embedding in a long while, we probably will not need it soon, so it is the safest one to remove.

Let's understand LRU with a small example as below:

```
   Cache is full. We need to add a new item.

   item A  -->  last used 1 minute ago
   item B  -->  last used 2 minutes ago
   item C  -->  last used 30 minutes ago   <-- least recently used, evict this one

```

Here, we can see that item C has not been used for the longest time, so LRU picks it for eviction. We remove item C and use that freed space for the new item.

The second way is TTL, which stands for time to live. TTL is how long an item is allowed to stay in the cache before it expires and gets removed, no matter what. For example, if we set a TTL of one hour, then every stored embedding is removed one hour after it was saved.

TTL is useful when our text or our model can change over time and we do not want to keep old embeddings forever. The word "stale" simply means old and no longer fresh. LRU is useful when we simply have limited space and want to keep the items we use most often.

Note: We can even use both together. We keep popular items with LRU, and we still let everything expire after the TTL, so nothing stays stale forever. We choose the eviction strategy based on our use case.

So, eviction keeps our cache from growing out of control while keeping the useful items around.

### Where the cache lives, memory or disk

Now, let's understand where this cache actually lives. There are two common choices, and each one fits a different need.

The first choice is in-memory, often using a tool called Redis. In-memory means the cache lives in the computer's memory, which is the fast working space of a computer. Redis is a popular tool that stores data in memory and gives it back extremely quickly. Looking up an embedding from an in-memory cache is very fast, often a tiny fraction of a second. This is great for repeated queries in a live system, where speed matters the most.

The second choice is on disk. On disk means the cache lives in files on the hard drive. Disk is slower than memory, but it can hold far more data, and the data stays even if the program restarts. This is great for ingestion, where we may compute embeddings for millions of document pieces and want to keep them around for a long time, even across restarts.

We can compare the two as below:

```
   IN-MEMORY (like Redis)        ON DISK
   ----------------------        ----------------------------
   very fast lookups             slower lookups
   limited space                 large space
   lost on restart               kept across restarts
   good for live queries         good for big ingestion jobs

```

Here, we can see that in-memory is fast but limited and temporary, while on disk is slower but roomy and lasting. Many real systems use both together, a fast in-memory cache in front and a larger disk cache behind it.

So, we pick where the cache lives based on our use case.

Keeping an AI system fast and cheap at scale - decisions like where a cache lives and how we serve it - is exactly what LLM Inference Engineering is about, and we cover it end to end in our AI and Machine Learning Program at Outcome School.

### The benefits of an Embedding Cache

Let's quickly bring together the benefits, because they are the reason we use this technique.

- Lower cost. We pay to compute an embedding only the first time for any given text. Every repeat is served from the cache for free. For popular queries and for re-ingestion of mostly unchanged documents, this saves a huge amount of money.
- Lower latency. Latency means the delay before we get a result. Reading from the cache is far faster than calling the embedding model. This matters even more when the model runs on a server, because then we also skip the wait for the network. So, our system feels faster.

In simple words, an Embedding Cache makes our application cheaper and faster at the same time, without changing the quality of the results. The embeddings are exactly the same numbers we would have computed. We just avoid computing them more than once.

That's the beauty of an Embedding Cache.

### An Embedding Cache in the real world

Now, let's see where an Embedding Cache is used in real systems.

The first place is RAG. RAG stands for Retrieval-Augmented Generation. In simple words, it is a system where we first fetch some relevant documents and then send them to a large language model along with the user's question. RAG depends on embeddings in two places. During ingestion, we compute an embedding for every piece of every document. During a query, we compute an embedding for the user's question to find the matching pieces. An Embedding Cache helps in both places. It saves the embeddings of document pieces so re-ingestion does not recompute the unchanged ones, and it saves the embeddings of popular queries so we do not recompute them for every user.

The second place is semantic search. Semantic search means searching by meaning instead of by exact words. The word "semantic" simply means related to meaning. In semantic search, we turn both the documents and the user's query into embeddings, then we find the documents whose embeddings are closest to the query's embedding. Finding those nearest embeddings fast across millions of documents is exactly what Approximate Nearest Neighbor (ANN) search does. Just like in RAG, the same documents and the same popular queries come up again and again. So, an Embedding Cache cuts down the cost and the delay here too.

So, anywhere we keep computing embeddings for the same text, whether during document ingestion or for repeated and popular queries, an Embedding Cache helps us a lot.

The same embeddings also power semantic caching, where we reuse a past answer whenever a new question means the same thing as an old one, so we can skip calling the model again.

This is how an Embedding Cache works. We compute the embedding for a piece of text once, we store it under a key built from a hash of the text plus the model name and version, and then we reuse it on every later request for the same text, while eviction with LRU or TTL keeps the cache from growing forever, so we get cheaper and faster results.

### Does an Embedding Cache change the quality of search results?

No. An Embedding Cache does not change the quality of the results. The cached embeddings are exactly the same numbers we would have computed by calling the model again. We just avoid computing them more than once, which makes the application cheaper and faster at the same time.

### What is the difference between an Embedding Cache and a Semantic Cache?

An Embedding Cache reuses the embedding for the exact same text, so we skip calling the embedding model. Semantic caching reuses a past answer whenever a new question means the same thing as an old one, so we skip calling the model that writes the answer. Both rely on embeddings, but they save different work.

### Will a similar but not identical text hit the Embedding Cache?

No. The cache key is a hash of the text plus the model name and version. The same input always produces the same hash, but even a tiny change in the input produces a completely different hash. So, only the exact same text sent to the same model becomes a cache hit.

### What happens to cached embeddings when we upgrade the embedding model?

The new model version gets its own keys, so it never reads the old model's embeddings. This is why the model name and version are part of the cache key. Without them, the new model could read the old embeddings and get the wrong numbers. A TTL also helps here, because old embeddings expire instead of staying stale forever.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

[Showing lines 1-361 and 996-1320 of 1320; 634 middle lines (34.1KB) elided. Read artifact://53 for full output]
