# AI Infrastructure and Scalability

> Answer under each `## Your answer` heading — short bullet form is fine.
> Say "проверь 13-ai-infrastructure-and-scalability" (или paste файл) — я сверю с `keys/13-ai-infrastructure-and-scalability.md`.

### 1. How do you improve inference speed in production LLM deployments?
<sub>src: [LLM Inference Optimization](https://www.youtube.com/watch?v=jV2sCj4lHYk)</sub>

## Your answer

### 2. LLM optimization techniques
<sub>src: [LLM optimization techniques](https://www.linkedin.com/posts/pallavi-shekhar_5-llm-optimization-techniques-lets-understand-activity-7442067281532325888-4aOS)</sub>

## Your answer

### 3. How do you select GPUs for LLM inference?
<sub>src: [How does a GPU work for Deep Learning?](https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning)</sub>

## Your answer

### 4. How does a GPU work for Deep Learning?
<sub>src: [How does a GPU work for Deep Learning?](https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning)</sub>

## Your answer

### 5. How do CUDA Kernels work?
<sub>src: [How do CUDA Kernels work?](https://outcomeschool.com/blog/how-do-cuda-kernels-work)</sub>

## Your answer

### 6. How does a Google TPU work?
<sub>src: [How does a Google TPU work?](https://outcomeschool.com/blog/how-does-a-google-tpu-work)</sub>

## Your answer

### 7. How does an LPU work?
<sub>src: [How does an LPU work?](https://outcomeschool.com/blog/how-does-an-lpu-work)</sub>

## Your answer

### 8. Estimate the GPU memory needed to serve a 70B model (weights, KV cache, activations). Does it fit on a single 80 GB GPU?

## Your answer

### 9. Do the roofline math: how many tokens/sec can one H100 produce for a 70B model at batch size 1?

## Your answer

### 10. What is model parallelism vs data parallelism in distributed training?

## Your answer

### 11. What is tensor parallelism, and how does it help serve large models?

## Your answer

### 12. What is pipeline parallelism?

## Your answer

### 13. How does continuous batching improve LLM inference throughput?
<sub>src: [Continuous Batching in LLMs](https://outcomeschool.com/blog/continuous-batching-in-llms)</sub>

## Your answer

### 14. What is speculative decoding, and how does it speed up inference?
<sub>src: [Speculative Decoding](https://outcomeschool.com/blog/speculative-decoding)</sub>

## Your answer

### 15. How does Medusa (multi-head speculative decoding) work?
<sub>src: [Medusa - Multi-Head Speculative Decoding](https://outcomeschool.com/blog/decoding-medusa)</sub>

## Your answer

### 16. How does EAGLE (feature-level speculative decoding) work?
<sub>src: [EAGLE - Feature-Level Speculative Decoding](https://outcomeschool.com/blog/decoding-eagle)</sub>

## Your answer

### 17. What is N-gram Speculation in LLMs, and how does it speed up generation?
<sub>src: [N-gram Speculation in LLMs](https://outcomeschool.com/blog/n-gram-speculation-in-llms)</sub>

## Your answer

### 18. What is KV cache, and how do you manage memory for it?
<sub>src: [What is KV Cache in LLMs?](https://outcomeschool.com/blog/kv-cache-in-llms)</sub>

## Your answer

### 19. What is Paged Attention?
<sub>src: [Paged Attention in LLMs](https://outcomeschool.com/blog/paged-attention-in-llms)</sub>

## Your answer

### 20. How does GGUF work?
<sub>src: [How does GGUF work?](https://outcomeschool.com/blog/how-does-gguf-work)</sub>

## Your answer

### 21. How do you optimize inference for edge and mobile deployment?
<sub>src: [How does llama.cpp run LLMs on everyday hardware?](https://outcomeschool.com/blog/how-does-llama-cpp-run-llms-on-everyday-hardware) · [How does Model Quantization work?](https://outcomeschool.com/blog/how-does-model-quantization-work)</sub>

## Your answer

### 22. What is model quantization (INT8, INT4, FP16, BF16), and how does it affect quality?
<sub>src: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk) · [How does Model Quantization work?](https://outcomeschool.com/blog/how-does-model-quantization-work)</sub>

## Your answer

### 23. How do you implement auto-scaling for AI workloads?

## Your answer

### 24. What is the role of load balancing in AI serving infrastructure?

## Your answer

### 25. How do you manage GPU memory for serving multiple models?

## Your answer

### 26. What is model sharding, and when would you use it?

## Your answer

### 27. How do you implement request queuing and priority scheduling for AI services?

## Your answer

### 28. What are the cost trade-offs between self-hosted and API-based AI inference?

## Your answer

### 29. How do you handle cold start latency for serverless AI deployments?

## Your answer

### 30. How do you implement model caching to reduce redundant computations?
<sub>src: [How does Prompt Caching work?](https://outcomeschool.com/blog/how-does-prompt-caching-work)</sub>

## Your answer

### 31. What is the difference between synchronous and asynchronous inference, and when do you use each?

## Your answer

### 32. What is FSDP (Fully Sharded Data Parallel), and how does it differ from DeepSpeed ZeRO?

## Your answer

### 33. What are TTFT, TPOT, and throughput, and how do they trade against each other?
<sub>src: [Prefill vs Decode: LLM Inference Optimization](https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization)</sub>

## Your answer

### 34. How do you monitor and profile LLM inference in production (TTFT, inter-token latency, GPU utilization)?

## Your answer

### 35. What is model routing at the infrastructure level, and how do you route requests based on complexity and cost?
<sub>src: [LLM Routing](https://outcomeschool.com/blog/llm-routing)</sub>

## Your answer
