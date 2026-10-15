> Source: https://outcomeschool.com/blog/how-do-image-embeddings-work

# How do Image Embeddings work?
URL: https://outcomeschool.com/blog/how-do-image-embeddings-work
Published: 2026-06-26

How do Image Embeddings work?

# How do Image Embeddings work?

Authors
: - Name
: Amit Shekhar
Published on
: June 26, 2026

In this blog, we will learn about how image embeddings work. We will also see why we need image embeddings, how a computer turns a picture into numbers, how we measure the similarity between two of them, and where they are used in the real world.

We will cover the following:

- What is an embedding?
- What is an image embedding?
- Why do we need image embeddings?
- How does a computer see an image?
- How are image embeddings created?
- A simple numeric walkthrough
- How do we measure similarity between two embeddings?
- A code example
- Where are image embeddings used?
- Summary

I am Amit Shekhar, Founder @ Outcome School, I have taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies. I am passionate about sharing knowledge through open-source, blogs, and videos.

I teach AI and Machine Learning at Outcome School.

Let's get started.

## What is an embedding?

An embedding is a list of numbers that represents the meaning of something.

In simple words, an embedding turns a real-world thing into a group of numbers. These numbers capture what the thing actually means.

Let's say we have a word, a sentence, or an image. A computer cannot understand any of these directly. A computer only understands numbers. So, we convert the thing into a list of numbers. That list of numbers is called an embedding.

This list of numbers is also called a vector. A vector is just a fixed-size list of numbers, like `[0.21, 0.87, 0.05, 0.64]`.

So, here is the simple idea:

> An embedding is a list of numbers that captures the meaning of something.

Now, we have understood what an embedding is. It is time to learn about what an image embedding is.

## What is an image embedding?

An image embedding is a list of numbers that represents the meaning of an image.

In simple words, we take an image, and we convert it into a list of numbers. That list of numbers captures what is inside the image.

Let's say we have a photo of a cat. We pass this photo through a special model. This model gives us back a list of numbers, something like `[0.91, 0.12, 0.77, 0.03, ...]`. This list of numbers is the image embedding of the cat photo.

The most important point is this:

> Two images that look similar in meaning will have embeddings that are close to each other.

So, the embedding of one cat photo will be close to the embedding of another cat photo. But the embedding of a cat photo will be far from the embedding of a car photo.

This is the whole magic of image embeddings. Similar images give similar numbers. Different images give different numbers.

This was all about what an image embedding is. Now, the question is, why do we even need it.

## Why do we need image embeddings?

Let's say we are building an app like Google Photos. We have one million photos stored. Now, a user types "beach" in the search box. We must show all the beach photos.

But here is the catch. The photos do not have any labels. Nobody has written "beach" under each photo. So, how do we find the beach photos?

We cannot compare the raw photos pixel by pixel. That is slow, and it does not understand meaning. Two beach photos taken at different angles look completely different at the pixel level, but they mean the same thing.

So, here comes the image embedding into the picture.

We convert every photo into an embedding. We convert the word "beach" into an embedding too. Then we simply find the photo embeddings that are closest to the "beach" embedding. Those are our beach photos.

This way we can use image embeddings to solve the interesting problem of searching images by meaning, not by exact pixels.

Finding the closest embeddings quickly across millions of photos is exactly what a vector database is built for. We have a detailed blog on how a Vector Database works that explains this end to end.

Now, the next big question is, how does a computer even see an image in the first place.

## How does a computer see an image?

Before jumping into embeddings, we must know how a computer reads an image.

An image is made up of tiny dots called pixels. A pixel is the smallest dot of color in an image. When we zoom into any photo a lot, we start seeing these small square dots. Each dot is a pixel.

Each pixel is stored as numbers. For a color image, every pixel has three numbers, one for red, one for green, and one for blue. Each of these numbers usually goes from 0 to 255.

So, for the sake of understanding, a small image of 100 by 100 pixels has 100 multiplied by 100, which is 10,000 pixels. And each pixel has 3 color numbers. So, the full image is 10,000 multiplied by 3, which is 30,000 numbers.

We can picture a single pixel as below:

```text
        One pixel
           |
           v
      +---------+
      |  pixel  |
      +---------+
       /   |   \
      v    v    v
    Red  Green  Blue
    210   180    90
   (each value goes from 0 to 255)

```

Here, we can see that one single pixel is stored as three numbers, one for red, one for green, and one for blue. Every pixel in the image is stored in this same way, so the full image becomes a very big list of these color numbers.

This is the raw image. It is just a big list of color numbers.

But here is the problem. These raw numbers only tell us the color of each dot. They do not tell us the meaning. They do not tell us "this is a cat". Two cat photos can have totally different raw numbers because of lighting, angle, and background.

So, we need to convert these raw color numbers into meaningful numbers. Those meaningful numbers are the image embedding.

Note: The raw pixels tell us how the image looks. The embedding tells us what the image means. This difference is the heart of the whole topic.

Now that we understand raw pixels, it is time to learn how the embedding is actually created.

## How are image embeddings created?

Image embeddings are created using a neural network.

In simple words, a neural network is a model that learns patterns from examples. We do not write rules for it by hand. Instead, we show it many examples, and it learns on its own.

For images, we use a special type of neural network called a CNN, which stands for Convolutional Neural Network. We can also use a newer type called a Vision Transformer. Do not worry about the exact names. The idea behind both is the same.

Let's understand the idea with a simple analogy.

Suppose a child has never seen a cat. We show the child thousands of cat photos. Slowly, the child learns the pattern. Cats have pointy ears, whiskers, fur, and a tail. Now the child can recognize a cat even in a brand new photo.

A neural network learns in the same way. We show it millions of photos. It slowly learns the patterns, like edges, shapes, ears, eyes, and textures.

Here is how it works step by step.

Step 1: The raw image, which is a big list of color numbers, goes into the neural network.

Step 2: The first layers of the network look for very simple patterns, like edges and corners.

Step 3: The next layers combine these simple patterns into bigger patterns, like an eye, an ear, or a wheel.

Step 4: The deeper layers combine these into full objects, like a full cat face or a full car.

Step 5: Near the end, the network produces a short list of numbers that summarizes everything it found in the image. This short list of numbers is the image embedding.

Let's visualize this flow as below:

```text
   Raw image
 (color numbers)
       |
       v
+-----------------+
|  Early layers   |  finds edges and corners
+-----------------+
       |
       v
+-----------------+
|  Middle layers  |  finds parts (eye, ear, wheel)
+-----------------+
       |
       v
+-----------------+
|  Deep layers    |  finds full objects (cat, car)
+-----------------+
       |
       v
+-----------------+
|  Final layer    |  summarizes everything found
+-----------------+
       |
       v
   Embedding
[0.91, 0.12, 0.77, ...]

```

Here, we can see that the raw image enters at the top, and each layer of the network understands a little more than the layer before it. The early layers see only simple edges, the middle layers see parts, and the deep layers see full objects. At the very end, the network turns all of this understanding into a short list of numbers, which is the image embedding.

So, the embedding is the network's summary of the meaning of the image.

Let me map this flow to our child analogy for your better understanding:

| In the neural network | In the child analogy |
| --- | --- |
| Raw image (color numbers) | Looking at the photo with eyes |
| Early layers finding edges | Noticing simple lines and corners |
| Middle layers finding parts | Noticing ears, eyes, and whiskers |
| Deep layers finding objects | Recognizing the full cat |
| Final embedding | The understanding "this is a cat" |

The best part is this. After the network is trained on millions of images, it learns to place similar images close together in the number space. This happens automatically during training, and that too without us writing any rule for it.

To learn how Embeddings are created and how Contrastive Learning places similar items close together, we build a Neural Network from scratch in our AI and Machine Learning Program at Outcome School.

Now, we have understood how embeddings are created. The best way to learn this further is by taking a simple numeric example.

## A simple numeric walkthrough

Let's say, just for the sake of understanding, that our embedding has only 3 numbers. In real life, an embedding has hundreds or even thousands of numbers, but 3 numbers are enough to learn the idea.

Assume that we have three photos. We pass each photo through the neural network, and we get the following embeddings:

- Cat photo A: `[0.90, 0.10, 0.05]`
- Cat photo B: `[0.88, 0.12, 0.07]`
- Car photo C: `[0.10, 0.95, 0.85]`

Here, we can notice something very important. The two cat photos, A and B, have very similar numbers. The car photo C has very different numbers.

We can picture where these embeddings sit as below:

```text
   Number space

   Cat A  Cat B
    (.)   (.)            <-- close together

                          (.) Car C    <-- far away

```

Here, we can see that the embedding of Cat A and the embedding of Cat B land very close to each other because they mean the same thing. The embedding of Car C lands far away because it means something different. This is exactly how a computer keeps similar images near each other and different images apart, using only numbers.

This is exactly what we wanted. Similar meaning gives similar numbers. Different meaning gives different numbers.

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

So, if we ask the computer "which photo is most similar to Cat photo A", the computer will compare the numbers and answer "Cat photo B". It will not pick the car photo, because its numbers are far away.

This is how a computer understands the meaning of images using only numbers.

Now, the question is, how exactly does the computer measure that two lists of numbers are close or far. Let's understand that now.

## How do we measure similarity between two embeddings?

To find how similar two embeddings are, we measure the distance between them.

In simple words, if two lists of numbers are close to each other, the images are similar. If they are far apart, the images are different.

The most common method to measure this is called cosine similarity.

In simple words, cosine similarity checks whether two lists of numbers point in the same direction. If they point in the same direction, the similarity is high. If they point in different directions, the similarity is low.

The cosine similarity value goes from -1 to 1.

- A value close to 1 means the two images are very similar.
- A value close to 0 means they are not related.
- A value close to -1 means they are opposite.

Let's take our earlier example. Cat photo A is `[0.90, 0.10, 0.05]` and Cat photo B is `[0.88, 0.12, 0.07]`. These two point in almost the same direction, so the cosine similarity will be very close to 1. This tells us they are very similar.

This is how we find similar images using their embeddings.

To master Embeddings and the similarity search behind a Multimodal Search System, check out our AI and Machine Learning Program at Outcome School.

Now that we have learned the theory, it is time to see a small code example.

## A code example

Let's see the code for creating an image embedding and comparing two images. We will use Python, which is the most common language for machine learning.

First, we load a ready-made model and create embeddings for two images as below:

```python
from sentence_transformers import SentenceTransformer
from PIL import Image

# Load a ready-made model that can create image embeddings
model = SentenceTransformer("clip-ViT-B-32")

# Open two images from our computer
cat_image = Image.open("cat.jpg")
dog_image = Image.open("dog.jpg")

# Convert each image into an embedding (a list of numbers)
cat_embedding = model.encode(cat_image)
dog_embedding = model.encode(dog_image)

print(cat_embedding.shape)

```

Here, we have done a few simple things.

- We loaded a ready-made model called `clip-ViT-B-32`. This model already knows how to turn images into embeddings, so we do not have to train anything ourselves.
- We opened two image files, one cat and one dog.
- We called `model.encode()` on each image. This gives us back the embedding, which is the list of numbers.

This will print the following:

```
(512,)

```

Here, we can see that each embedding is a list of 512 numbers. So, this model summarizes the full image into 512 meaningful numbers.

Now, let's compare these two embeddings to see how similar the images are as below:

```python
from sentence_transformers import util

# Measure how similar the two embeddings are
similarity = util.cos_sim(cat_embedding, dog_embedding)

print(similarity)

```

Here, we have used `cos_sim`, which calculates the cosine similarity between the two embeddings. It tells us how close the two images are in meaning.

A cat and a dog are both animals, so the value will be somewhat high. If we compared a cat with a car instead, the value would be much lower, because a cat and a car are very different in meaning.

This is how, with only a few lines of code, we can convert images into numbers and compare their meaning. It works perfectly.

Note: The same `clip-ViT-B-32` model can also turn a word like "beach" into an embedding. So, we can compare a word embedding with image embeddings, and that is exactly how searching photos by typing words works.

Models that connect text and images in the same embedding space like this are called multimodal models. We have a detailed blog on Multimodal AI that explains how it works.

Now, we have understood the full flow. Let's see where image embeddings are used in real life.

## Where are image embeddings used?

Image embeddings are used in many products that we use every day. Here are a few real use cases:

- Image search: We search for photos by typing words like "beach" or "birthday", and the app finds matching photos by comparing embeddings.
- Similar product search: On shopping apps, we upload a photo of a shoe, and the app shows similar shoes by comparing embeddings.
- Duplicate photo detection: The phone gallery groups similar or duplicate photos together by comparing their embeddings.
- Face grouping: Photo apps group all photos of the same person together using embeddings.
- Recommendation systems: Apps recommend images or videos similar to the ones we liked, using embeddings.

So, now we know where we can use image embeddings.

## Summary

Let's quickly recap everything in simple words.

A computer cannot understand an image directly. It only understands numbers. The raw image is just a big list of color numbers, and these raw numbers do not capture meaning.

So, we pass the image through a neural network. The network summarizes the image into a short list of meaningful numbers. This list of numbers is the image embedding.

Similar images get similar embeddings, and different images get different embeddings. We measure how similar two embeddings are using cosine similarity. This lets us search, group, and compare images by their meaning, not by their exact pixels.

This is how image embeddings work. They turn pictures into numbers that carry meaning, and that too in a way a computer can compare very easily.

That's it for now.

Thanks

Amit Shekhar Founder @ Outcome School
