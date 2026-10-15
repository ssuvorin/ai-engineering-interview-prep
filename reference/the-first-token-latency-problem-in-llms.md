> Source: https://www.youtube.com/watch?v=XD8DD4cEHu0

# The First-Token Latency Problem in LLMs
URL: https://www.youtube.com/watch?v=XD8DD4cEHu0
Author: Outcome School

So, in this video, we will learn why is
the first token slower than rest in an LLM. Let's understand. When we send a prompt
to an LLM, we feel a small delay before the first word appears. After that, the words flow out
quickly, one after another. LLM inference has two
phases, Prefill and Decode. Let's understand both. Prefill is the first phase. Here the model reads our
entire prompt at once. It computes the attention for every
input token and then it stores the results in something called KV Cache. The KV Cache is the model's memory
of what it has already seen. It saves us from doing the
same work again and again. Suppose our prompt has 1000 tokens. The model must process all the 1000
tokens before it can generate even one new word. And this takes time. And this is why the first token
feels slow and we call this time to first token or TTFT. Now, Decode is the second phase. Here the model generates
one token at a time. But here is the beauty. The
KV Cache is already built. For each new token, the model
only computes attention for one new token, not the whole prompt again. So each new token is fast
and we call this time per output token or TPOT. In simple words, prefill is
equal to heavy work done once, decode is equal to light
work done many times. And this is why the first token is
slow and rest feels like a stream. The longer our prompt, the
slower the first token. And this is how the LLM
inference works behind the scene. And that's it for now, I will
see you in the next video.
