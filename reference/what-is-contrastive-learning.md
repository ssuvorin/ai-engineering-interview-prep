> Source: https://outcomeschool.com/blog/contrastive-learning

# What is Contrastive Learning? How It Works Step by Step
URL: https://outcomeschool.com/blog/contrastive-learning
Published: 2026-05-20
Author: Amit Shekhar

What is Contrastive Learning? How It Works Step by Step

# What is Contrastive Learning? How It Works Step by Step

Authors
: - Name
: Amit Shekhar
Published on
: May 20, 2026

Contrastive Learning is a way of teaching a model by comparing things. The model learns to pull similar things close to each other and push different things far apart.

In this blog, we will learn about Contrastive Learning. We will also see how it works step-by-step and where it is used in the real world.

We will cover the following:

- What is Contrastive Learning?
- Why do we need Contrastive Learning?
- The key idea behind Contrastive Learning.
- Positive pairs and Negative pairs.
- How does Contrastive Learning work step-by-step?
- Loss functions used in Contrastive Learning.
- Popular Contrastive Learning methods.
- Real-world use cases of Contrastive Learning.

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

### What is Contrastive Learning?

Contrastive Learning is a way of teaching a model to learn good representations of data by comparing things. The model learns to pull similar things close to each other and push dissimilar things far apart in a representation space.

In simple words, Contrastive Learning = Contrast + Learning. We learn by contrasting one thing with another.

Let's say we have two photos of the same cat, taken from different angles. These two photos are similar. They should be close to each other in the representation space. Now, consider a photo of a car. This is very different from the cat photos. It should be far away from them.

This is the core idea of Contrastive Learning.

Similar things attract each other and stick together. Dissimilar things repel each other and move apart. Contrastive Learning teaches the model to behave like these magnets.

### Why do we need Contrastive Learning?

Before jumping into how it works, we must understand the problem it solves.

In traditional supervised learning, we need labeled data. For every image, we need a human to tell us "this is a cat", "this is a dog", and so on. Labeling data is expensive. It is slow. It needs a lot of human effort.

But, here is the catch. The internet has billions of images, videos, and pieces of text. Only a very small fraction of this data is labeled. We have huge amounts of unlabeled data available, but we cannot use it directly with supervised learning.

So, here comes Contrastive Learning to the rescue.

Contrastive Learning does not need any labels from humans. It is a self-supervised learning technique. The model creates its own labels from the data itself. This way, we can train the model on massive amounts of unlabeled data and still learn very useful representations.

Once these representations are learned, we can reuse them for many downstream tasks like classification, search, clustering, and etc., with very little labeled data.

This is the beauty of Contrastive Learning.

### The key idea behind Contrastive Learning

We want the model to learn a function that maps each input (an image, a sentence, a video, and etc.) to a vector. This vector is called the embedding or the representation. The space where all these vectors live is called the embedding space.

In this embedding space:

- Similar inputs should have embeddings that are close to each other.
- Dissimilar inputs should have embeddings that are far apart from each other.

If the model can do this well, then the embeddings become very useful. We can use them for many tasks like search, classification, recommendation, and etc.

This is the goal of Contrastive Learning.

### Positive pairs and Negative pairs

Now, the question is: how does the model know which things are similar and which things are different, without any labels?

The answer is: we create pairs from the data itself.

Positive pair: Two samples that are similar and should be close in the embedding space.

Negative pair: Two samples that are different and should be far apart in the embedding space.

Let's see how we create these pairs for images.

We take an image. We apply some changes to it, such as cropping, rotating, flipping, or changing the colors. These changes are called data augmentation. The two augmented versions of the same image form a positive pair, because they come from the same original image.

Now, we take any other image from the dataset. This image and the first image form a negative pair, because they are different images.

This way, we get positive pairs and negative pairs without any human labels.

The choice of augmentation is very important. The augmentations should change the look of the image but not its meaning. For example, a cropped cat is still a cat. A rotated cat is still a cat. So, the model learns that these surface-level changes do not matter, and it focuses on the actual content of the image.

For text, a positive pair can be two sentences that mean the same thing. For an image-text model, a positive pair can be an image and its caption.

Search models are trained on the same shape of data, where the query is paired with a passage that answers it as the positive and one that does not as the negative. We have a detailed blog on Decoding ColBERT that walks through this training setup with real numbers.

### How does Contrastive Learning work step-by-step?

The best way to learn this is by taking an example.

Let's say we have an image of a cat. We will follow these steps:

Step 1: We take the cat image and create two different augmented versions of it. Let's call them View 1 and View 2. View 1 and View 2 form a positive pair.

Step 2: We take another image from the dataset, let's say an image of a car. This image is a negative sample.

Step 3: We pass View 1, View 2, and the car image through a neural network. The neural network gives us three embedding vectors.

Step 4: We compute the similarity between every pair of embeddings. A common way to measure similarity is the cosine similarity, which tells us how close two vectors are in direction. The cosine similarity gives a value between -1 and 1. A value close to 1 means the two vectors are very similar. A value close to -1 means they are very different.

For the sake of understanding, let's assume after a fresh start, the model gives these similarity scores:

- Similarity(View 1, View 2) = 0.3
- Similarity(View 1, Car) = 0.6
- Similarity(View 2, Car) = 0.5

Here, we can see that the model is confused. It thinks the two cat views are less similar to each other than they are to the car. This is wrong. So, the loss will be high, and the model will update its weights.

Step 5: We train the model to make the similarity between View 1 and View 2 high, and the similarity between View 1 and the car image low, and the similarity between View 2 and the car image low.

After training for many rounds, we want the scores to look more like this:

- Similarity(View 1, View 2) = 0.9
- Similarity(View 1, Car) = 0.1
- Similarity(View 2, Car) = 0.1

Step 6: We repeat this process for many images, many times, until the model learns good embeddings.

This is how the model learns without any labels.

This was all about the high-level process. Now, the next big question is: how exactly do we tell the model that its current similarity scores are wrong, and by how much? This is where the loss function comes into the picture.

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

### Loss functions used in Contrastive Learning

To train the model, we need a loss function. The loss function tells the model how well it is doing. The model updates its weights to reduce the loss.

There are a few popular loss functions used in Contrastive Learning. Let's see each one.

Contrastive Loss

Contrastive Loss works on 2 samples at a time (a pair).

This is the simplest one. We give the model a pair of samples and tell it whether they are similar or different.

- If they are similar, the loss is small when their embeddings are close and large when their embeddings are far apart.
- If they are different, the loss is small when their embeddings are far apart (beyond a fixed margin) and large when their embeddings are close.

For the sake of understanding, let's say the margin is 1.0. If two different images have an embedding distance of 0.2, the loss will be high because they are too close. The model will push them apart. If their distance becomes 1.5, the loss for this pair becomes zero, because they are already far enough apart.

The model learns to pull similar pairs together and push dissimilar pairs apart by at least the margin.

Triplet Loss

Triplet Loss works on 3 samples at a time (a triplet).

The three samples are:

- Anchor: the reference sample.
- Positive: a sample similar to the anchor.
- Negative: a sample different from the anchor.

The loss pushes the anchor closer to the positive than to the negative by at least a fixed margin. In simple words, the distance between the anchor and the positive must be smaller than the distance between the anchor and the negative, by some safety gap.

For the sake of understanding, let's say the anchor is a photo of person A, the positive is another photo of the same person A, and the negative is a photo of person B. The triplet loss will pull the two photos of person A together and push the photo of person B away from them. This is exactly what we want in face recognition.

InfoNCE Loss

InfoNCE Loss works on 1 anchor with 1 positive and many negative samples at a time.

This is the most popular one in modern Contrastive Learning. It is used in methods like SimCLR and CLIP.

The model has to pick the positive sample out of all the samples. It is like a classification problem where the correct answer is the positive sample, and all the others are wrong answers.

The model learns to give a high similarity score to the positive sample and low similarity scores to the negative samples.

Note: InfoNCE also uses a small number called the temperature, which controls how sharp the model's decisions are. A small temperature makes the model very confident, while a large temperature makes it softer. The right temperature is important for good training.

To learn Loss Functions, Embeddings, and Cross-Entropy in depth, check out our AI and Machine Learning Program at Outcome School.

### Popular Contrastive Learning methods

Now that we have learned the basics, it's time to learn about some popular Contrastive Learning methods.

SimCLR stands for Simple Framework for Contrastive Learning of Visual Representations. It was introduced by Google.

The idea is very simple:

- Take an image, create two augmented versions of it. One version is treated as the anchor, and the other as the positive.
- Pass both versions through the same neural network to get embeddings.
- The negative samples are simply the augmented versions of the other images in the same batch.
- Use the InfoNCE loss to bring the anchor and the positive close together, and push the anchor away from all the negatives.

SimCLR showed that simple data augmentation is enough to learn very powerful image representations, without any labels.

MoCo (Momentum Contrast)

SimCLR needs a large batch size to have enough negative samples. This is a problem because large batches need a lot of GPU memory.

So, here comes MoCo to the rescue.

MoCo maintains a dynamic dictionary of negative samples as a queue. Every new mini-batch is added to the queue, and the oldest mini-batch is removed. This way, we can have many negative samples without needing a very large batch size. MoCo also uses a slowly updated copy of the model, called the momentum encoder, to compute the embeddings for the queue. This keeps the embeddings in the queue fresh and makes the training stable.

CLIP (Contrastive Language-Image Pre-training)

CLIP is from OpenAI. It learns by matching images with their text captions.

Here, the positive pair is an image and its correct caption. The negative pairs are the image and the captions of other images in the same batch.

CLIP is trained on millions of image-text pairs from the internet. After training, CLIP can do amazing things. For example, we can give CLIP a new image of a puppy and a list of labels like "a photo of a cat", "a photo of a dog", "a photo of a bird". CLIP will compute the similarity between the image and each label, and pick the one with the highest similarity, which will be "a photo of a dog". CLIP can do this without being trained on that specific task. This is called zero-shot classification.

In 2023, Google introduced SigLIP, which replaces CLIP's softmax loss with a simpler pairwise sigmoid loss. This makes training more memory-efficient and allows much larger batch sizes. SigLIP is now the vision encoder of choice in many modern vision-language models.

CLIP is now used as a building block in many famous models like Stable Diffusion and DALL-E.

Non-contrastive methods

More recent methods like BYOL, SimSiam, and DINO drop negative pairs entirely. They learn good representations using only positive pairs, with the help of architectural tricks (different methods use different combinations of stop-gradient, momentum encoders, predictor heads, and output centering) to avoid collapsing all inputs to the same embedding. These methods are sometimes called non-contrastive self-supervised learning. DINO and its successor DINOv2 from Meta are the current go-to choice for self-supervised visual representation learning. A closely related idea is the Joint Embedding Predictive Architecture (JEPA) from Yann LeCun's team, which drops negative pairs by predicting the summary of a hidden part of the input from the visible part, instead of comparing pairs at all.

If we want to go deep into Contrastive Learning, Self-supervised Learning, and Multimodal AI, we have a complete program on this - check out our AI and Machine Learning Program at Outcome School.

### Real-world use cases of Contrastive Learning

Now, let's see where Contrastive Learning is used in the real world.

- Image search: Finding images that look similar to a given image.
- Face recognition: Bringing different photos of the same person close together and photos of different people far apart in the embedding space.
- Recommendation systems: Products that users often buy together are pulled close, and unrelated products are pushed apart. This helps in recommending similar products.
- Text similarity: Finding sentences or documents with similar meaning, useful in search engines and chatbots.
- Multimodal models: CLIP-style models that connect images with text. These are used inside image generation models like Stable Diffusion and DALL-E.
- Medical imaging: Learning useful representations from large amounts of unlabeled medical images, where labeled data is very hard to get.
- Audio and speech: Learning representations of sounds and speech without labels.

In many of these use cases, once the embeddings are learned, the next step is to quickly find the most similar ones in a huge collection. We have a detailed blog on Approximate Nearest Neighbor (ANN) Search that explains how that fast search works.

This is how Contrastive Learning helps in solving many real-world problems in a very simple way.

Now, we have understood Contrastive Learning.

### Is Contrastive Learning supervised or unsupervised?

Contrastive Learning is a self-supervised learning technique. It does not need any labels from humans, because the model creates its own labels from the data itself. For example, two augmented versions of the same image form a positive pair, and any other image forms a negative pair.

### Do all self-supervised methods need negative pairs?

No. Methods like BYOL, SimSiam, and DINO drop negative pairs entirely and learn using only positive pairs. They use architectural tricks such as stop-gradient, momentum encoders, predictor heads, and output centering to avoid collapsing all inputs to the same embedding. These are called non-contrastive methods.

### What is the difference between SimCLR and MoCo?

SimCLR takes its negative samples from the other images in the same batch, so it needs a large batch size and a lot of GPU memory. MoCo keeps a queue of negative samples, adding each new mini-batch and removing the oldest one. It also uses a slowly updated momentum encoder to keep training stable.

### What is the difference between Contrastive Loss and Triplet Loss?

Contrastive Loss works on 2 samples at a time and is told whether the pair is similar or different. Triplet Loss works on 3 samples, an anchor, a positive, and a negative. It pushes the anchor closer to the positive than to the negative by at least a fixed margin.

### How does CLIP classify images it was never trained on?

CLIP computes the similarity between the new image and each text label, like "a photo of a cat" or "a photo of a dog". It then picks the label with the highest similarity. This is called zero-shot classification, because CLIP was not trained on that specific task.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School

You can connect with me on:

- X
- LinkedIn
- GitHub
