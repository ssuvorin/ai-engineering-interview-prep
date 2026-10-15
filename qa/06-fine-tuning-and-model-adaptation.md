# Fine-Tuning and Model Adaptation

> Answer under each `## Your answer` heading — short bullet form is fine.
> Say "проверь 06-fine-tuning-and-model-adaptation" (или paste файл) — я сверю с `keys/06-fine-tuning-and-model-adaptation.md`.

### 1. What is fine-tuning, and when should you fine-tune an LLM?
<sub>src: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk)</sub>

## Your answer

### 2. Explain the difference between full fine-tuning and parameter-efficient fine-tuning (PEFT).
<sub>src: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk)</sub>

## Your answer

### 3. What is LoRA (Low-Rank Adaptation), and how does it work?
<sub>src: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk)</sub>

## Your answer

### 4. What is QLoRA, and how does it enable fine-tuning on consumer hardware?
<sub>src: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk)</sub>

## Your answer

### 5. How does fine-tuning work?
<sub>src: [How does fine-tuning work?](https://outcomeschool.com/blog/how-does-fine-tuning-work)</sub>

## Your answer

### 6. Explain Prefix Tuning and Prompt Tuning. How are they different from LoRA?
<sub>src: [How does Prefix Tuning work?](https://outcomeschool.com/blog/how-does-prefix-tuning-work)</sub>

## Your answer

### 7. What is adapter-based fine-tuning?
<sub>src: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk)</sub>

## Your answer

### 8. Explain the difference between pre-training, supervised fine-tuning (SFT), and preference optimization (RLHF/DPO).
<sub>src: [Decoding InstructGPT](https://outcomeschool.com/blog/decoding-instructgpt)</sub>

## Your answer

### 9. What is RLHF (Reinforcement Learning from Human Feedback), and how is it used to align LLMs?
<sub>src: [Reinforcement Learning from Human Feedback (RLHF)](https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf)</sub>

## Your answer

### 10. What is Deep RL from Human Preferences, the paper that started RLHF?
<sub>src: [Deep RL from Human Preferences](https://outcomeschool.com/blog/decoding-deep-rl-from-human-preferences)</sub>

## Your answer

### 11. Why did DPO displace PPO-based RLHF at many labs? When is online RL still better?
<sub>src: [Direct Preference Optimization (DPO)](https://outcomeschool.com/blog/direct-preference-optimization-dpo) · [Proximal Policy Optimization (PPO)](https://outcomeschool.com/blog/proximal-policy-optimization-ppo)</sub>

## Your answer

### 12. What is instruction tuning, and why is it important for chat models?
<sub>src: [Decoding InstructGPT](https://outcomeschool.com/blog/decoding-instructgpt)</sub>

## Your answer

### 13. How do you prepare a dataset for fine-tuning an LLM?

## Your answer

### 14. What is catastrophic forgetting, and how do you prevent it during fine-tuning?
<sub>src: [Continual Learning in LLMs](https://outcomeschool.com/blog/continual-learning-in-llms)</sub>

## Your answer

### 15. When should you choose fine-tuning over RAG over prompt engineering?
<sub>src: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk)</sub>

## Your answer

### 16. How do you evaluate a fine-tuned model's performance?
<sub>src: [LLM Evaluation](https://outcomeschool.com/blog/llm-evaluation)</sub>

## Your answer

### 17. What is synthetic data generation, and how do you use it for fine-tuning?

## Your answer

### 18. What are the key hyperparameters for fine-tuning (learning rate, epochs, batch size, LoRA rank)?
<sub>src: [LoRA - Low-Rank Adaptation of LLMs](https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms)</sub>

## Your answer

### 19. Do the GPU memory math for full fine-tuning a 7B model in bf16 with Adam. Now with LoRA and QLoRA.

## Your answer

### 20. How do you fine-tune a model for a specific domain (legal, medical, finance)?

## Your answer

### 21. What is continual pre-training, and when would you use it?

## Your answer

### 22. How do you merge multiple LoRA adapters?
<sub>src: [LoRA - Low-Rank Adaptation of LLMs](https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms)</sub>

## Your answer

### 23. What is the difference between SFT (Supervised Fine-Tuning) and alignment training?
<sub>src: [Decoding InstructGPT](https://outcomeschool.com/blog/decoding-instructgpt)</sub>

## Your answer

### 24. What is RLAIF (RL from AI Feedback), and how does it differ from RLHF?

## Your answer

### 25. What is Constitutional AI, and how does it differ from RLHF?

## Your answer

### 26. What is RLVR (Reinforcement Learning with Verifiable Rewards), and when does it beat a learned reward model?
<sub>src: [Group Relative Policy Optimization (GRPO)](https://outcomeschool.com/blog/group-relative-policy-optimization-grpo)</sub>

## Your answer

### 27. What is knowledge distillation for fine-tuning, and what are the legal considerations?
<sub>src: [How does Knowledge Distillation work?](https://outcomeschool.com/blog/how-does-knowledge-distillation-work)</sub>

## Your answer

### 28. Your fine-tuned LLM produces factually wrong outputs due to training data quality issues. How do you fix it?

## Your answer

### 29. You must choose between LoRA and full fine-tuning for a domain-specific assistant. How do you decide?
<sub>src: [LoRA - Low-Rank Adaptation of LLMs](https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms)</sub>

## Your answer

### 30. Your fine-tuned model memorized training data verbatim instead of learning patterns. How do you fix overfitting?

## Your answer

### 31. Your fine-tuned LLM forgot its general capabilities after domain-specific fine-tuning. How do you fix catastrophic forgetting?
<sub>src: [Continual Learning in LLMs](https://outcomeschool.com/blog/continual-learning-in-llms)</sub>

## Your answer

### 32. Your RLHF preference data has low annotator agreement. How do you ensure data quality?

## Your answer
