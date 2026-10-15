> Source: https://outcomeschool.com/blog/batch-normalization-vs-layer-normalization

# Batch Normalization vs Layer Normalization

Batch Normalization normalizes each feature across all the examples in a batch, whereas Layer Normalization normalizes all the features within each single example.

We will cover:

- What is Normalization?
- Why do we need Normalization?
- What is Batch Normalization?
- What is Layer Normalization?
- Batch Normalization vs Layer Normalization
- When to use which one?

## What is Normalization?

Normalization is the process of adjusting values so they are on a similar scale. For example, age (0-100) and salary (0-10,00,000) have very different scales, which creates problems during training because the network gives more importance to the larger-valued feature. Normalization brings all values to a similar scale, typically with mean 0 and variance 1.

## Why do we need Normalization?

When we train a deep neural network, values flowing through layers can become very large or very small, causing:

- Training to become slow.
- The model to become unstable.
- Gradients to explode or vanish.

## What is Batch Normalization?

Batch Normalization normalizes values across the batch dimension for each feature. For each feature, it calculates mean and variance across all examples in the batch, then normalizes using those.

Example with a batch of 4 examples, each with 3 features:

```
Example 1: [10, 12, 14]
Example 2: [20, 22, 24]
Example 3: [30, 32, 34]
Example 4: [40, 42, 44]
```

In Batch Normalization, we normalize column by column. For the first feature, we take all 4 values from the first column [10, 20, 30, 40], calculate the mean and variance, then normalize. Mean of feature 1 = (10 + 20 + 30 + 40) / 4 = 25.

The formula:

```
x_normalized = (x - mean) / sqrt(variance + epsilon)
```

After normalization, we apply two learnable parameters `gamma` (scale) and `beta` (shift):

```
output = gamma * x_normalized + beta
```

Note: During training, we use the mean and variance of the current batch. During inference, we often process one example at a time, so we use the average of the mean and variance tracked across all batches during training. Batch Normalization behaves differently during training and inference.

Advantages: Faster training; allows higher learning rates; reduces need for careful weight initialization; acts as a regularizer.

Disadvantages: Does not work well with small batch sizes; different behavior during training and inference; not suitable for sequence models like RNNs and Transformers because sequence lengths vary and computing batch statistics becomes very difficult.

## What is Layer Normalization?

Layer Normalization normalizes values across the feature dimension for each example. For each example, it calculates mean and variance across all its features.

Using the same example, Layer Normalization normalizes row by row. For Example 1, we take all 3 values [10, 12, 14], calculate the mean and variance, then normalize. Mean of Example 1 = (10 + 12 + 14) / 3 = 12.

The formula is the same, the only difference is the dimension over which we compute mean and variance.

Note: Layer Normalization behaves the same way during training and inference, because it does not depend on the batch.

Advantages: Works with any batch size, even 1; same behavior in training and inference; works very well for RNNs and Transformers; used in BERT, GPT, and other LLMs.

Disadvantages: Not always the best choice for CNNs, where Batch Normalization usually performs better.

## Batch Normalization vs Layer Normalization

Think of a classroom with 4 students and 3 subjects:

- Batch Normalization is like comparing the marks of a single subject across all 4 students.
- Layer Normalization is like comparing the marks of all 3 subjects for a single student.

| Aspect | Batch Normalization | Layer Normalization |
| --- | --- | --- |
| Direction of normalization | Across the batch (column-wise) | Across the features (row-wise) |
| Depends on batch size | Yes | No |
| Behavior in training and inference | Different | Same |
| Works with batch size of 1 | No | Yes |
| Best for | CNNs and image data | RNNs, Transformers, and LLMs |

In simple words:

- Batch Normalization normalizes one feature across all examples in the batch.
- Layer Normalization normalizes all features of one example.

## When to use which one?

- Image data and CNNs with large batch sizes -> Batch Normalization.
- Sequence data, RNNs, Transformers, or LLMs -> Layer Normalization.
- Very small batch sizes -> Layer Normalization.

### Why does Batch Normalization behave differently during inference?

During inference, we often process one example at a time, so we cannot calculate batch mean/variance and instead use the running averages tracked during training.

### What are gamma and beta in normalization?

Gamma and beta are two learnable parameters applied after normalization. Gamma scales, beta shifts. Both BN and LN use them.

### Why do we add epsilon in the normalization formula?

To avoid division by zero. Epsilon is a very small number added to the variance before the square root.

### Does Batch Normalization work with small batch sizes?

No. It does not work well with small batch sizes and not at all with batch size 1. Layer Normalization is better there.
