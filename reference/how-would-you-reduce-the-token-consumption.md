> Source: https://www.linkedin.com/posts/pallavi-shekhar_ai-aiagents-machinelearning-activity-7439550125015994368-LTmE

# You have built an AI agent that performs multi-step tasks like researching a topic and writing a summary. The agent works well but consumes an excessive number of tokens per task - … | Pallavi .
URL: https://www.linkedin.com/posts/pallavi-shekhar_ai-aiagents-machinelearning-activity-7439550125015994368-LTmE
Published: 2026-03-17
Author: Pallavi .

# You have built an AI agent that performs multi-step tasks like researching a topic and writing a summary. The agent works well but consumes an excessive number of tokens per task - … | Pallavi . · LinkedIn · 2026-03-17

**Pallavi .**: Software Engineer at Outcome School with 8 years 1 month of experience. Previous roles include Senior Software Development Engineer at West Agile Labs, Software Engineer at NCR Corporation, and Software Engineer at Deloitte India (Offices of the US). Based in Bengaluru, Karnataka, India [IN].

---

You have built an AI agent that performs multi-step tasks like researching a topic and writing a summary. The agent works well but consumes an excessive number of tokens per task - sometimes 50,000+ tokens for a simple research query. This is making the system very expensive to run. How would you reduce the token consumption?

Answer:

Token consumption is one of the biggest cost drivers in AI agent systems. An agent that is not optimized for tokens can burn through the budget very quickly.

Many agents run in a plan-act-observe loop. If the stopping criteria is not well-defined, the agent keeps looping and consuming tokens. We must set a maximum number of iterations and add a clear stopping condition so the agent stops immediately once it has gathered enough information.

As the agent takes more steps, the conversation history grows and each new LLM call includes the entire history. We can summarize the conversation history after every few steps instead of passing the full history. This significantly reduces the input token count for each subsequent call.

Not every step needs the most powerful model. We implement a model routing strategy - the orchestrator uses a powerful model for complex reasoning and routes simpler tasks like data extraction to a smaller, cheaper model. We also add a caching layer for tool results so the agent reuses cached results instead of making duplicate calls.

Long system prompts consume tokens on every single call. If the system prompt is 2000 tokens and the agent makes 20 calls, that is 40,000 tokens just for the system prompt. We keep prompts concise and use dynamic prompts where only the relevant instructions are included based on the current step.

This is how we can solve the excessive token consumption problem in AI agents.

Follow Outcome School for knowledge-packed content.

Keep Learning, Keep Sharing, and Keep Growing.

#AI #AIAgents #MachineLearning #LLM #OutcomeSchool #TokenOptimization #CostOptimization

You have built an AI agent that performs multi-step tasks like researching a topic and writing a summary. The agent works well but consumes an excessive number of tokens per task - … | Pallavi . image

## Comments

**Outcome School** · 2026-03-17
> Follow for knowledge-packed content.

**AMIT SHEKHAR** · 2026-03-17
> #Agent #AI #LLM

## Engagement

- Reactions: 17
