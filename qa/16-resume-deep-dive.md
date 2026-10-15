# Resume Deep-Dive — Предметное интервью

> Вопросы на английском, отвечай **на английском** — надиктовывай через Handy прямо под `## Your answer`. Оценивается содержание, не грамматика диктовки.
> Вопросы сгенерированы из `resume/resume.md` (твоё резюме, verbatim). Это не теория — это то, что спросят про **твой** опыт на предметном интервью. Отвечай как на интервью: структурно, с цифрами, без воды.
> Say "проверь 16-resume-deep-dive" — я сверю с `keys/16-resume-deep-dive.md`.
> Факты, которых нет в резюме (масштабы, детали реализации), нужно озвучивать стабильно и правдиво — заготовку придумай заранее, не на интервью.

## About you & motivation

### 1. Walk me through your background. Why does a fintech risk analyst become an AI engineer?

## Your answer

### 2. Give me your two-minute self-presentation tailored to this role. What are your three strongest selling points?

## Your answer

### 3. Which single project on your resume are you most proud of, and what would you do differently if you rebuilt it today?

## Your answer

### 4. You held a full-time role at RecoLabs and part-time roles at Phii Labs and TRE simultaneously. How did you manage the overlap, and were there any conflicts of interest?

## Your answer

## Rank Wizard (RecoLabs) — flagship

### 5. How does Rank Wizard actually measure "brand visibility" in ChatGPT, Perplexity, and Gemini? Walk me through the pipeline — from client onboarding to the visibility metric they see on the dashboard.

## Your answer

### 6. Your audit pipeline produces "schema-validated model output with one guided retry". What does the schema look like, how do you validate it, what does "guided" mean in the retry, and what happens when the retry also fails?

## Your answer

### 7. $0.36 per audit — walk me through exactly how you compute and enforce that cap. What happens when an audit is about to exceed it?

## Your answer

### 8. You render client sites in a headless browser with no outbound network access. Why? Walk me through your prompt-injection threat model: which attacks did you design against, and which did you consciously accept?

## Your answer

### 9. "Scraped content reaches the model only as marked untrusted data" — concretely, how is it marked, and why isn't marking alone sufficient?

## Your answer

### 10. How do you know an audit result is actually correct? What evaluation or verification do you run on audit quality?

## Your answer

### 11. Describe your agent fleet for behavioral SEO: what does a single agent do end-to-end, how are tasks scheduled, and what breaks most often in production?

## Your answer

### 12. How do you run Playwright browsers at scale — how many concurrent sessions, how are fingerprints and proxies assigned, and how do you detect that a session got flagged as a bot?

## Your answer

### 13. You claim the fleet "replaced manual operator work". What did operators do before, what's the evidence the fleet actually works, and where do humans still intervene?

## Your answer

## Architecture & AI design decisions

### 14. You use read-only SQL views as the tool layer in two products — Rank Wizard and the TRE CRM. Why views and not direct table access, a REST layer, or raw text-to-SQL?

## Your answer

### 15. In flowss, "critical actions kept deterministic behind FastAPI". Which actions exactly, and how do you decide what the LLM is allowed to do autonomously versus what stays deterministic?

## Your answer

### 16. "Semantic memory on provider-agnostic embeddings" — why did you need provider-agnostic, and what happens to existing vectors when you switch embedding providers?

## Your answer

### 17. How do you pick an embedding model and dimensionality for pgvector? When is pgvector enough versus a dedicated vector database?

## Your answer

### 18. The WhatsApp lead qualifier: how does RAG over chat history work concretely — what do you index, what does the classifier see, what defines a "hot" lead, and what's the error-cost asymmetry between false positives and false negatives?

## Your answer

### 19. Why Celery and not something else? Where exactly does Celery sit in Rank Wizard's architecture, and what are its failure modes under your load?

## Your answer

### 20. What's the most technically risky thing you shipped, and how did you de-risk it?

## Your answer

## Engineering process & AI-first workflow

### 21. Walk me through your Spec Kit → coding agent → AI reviewer → human sign-off pipeline using one concrete recent feature. Where does it break down?

## Your answer

### 22. What does your AI PR reviewer actually check, what's its false-positive rate like, and what does a human still catch that it misses?

## Your answer

### 23. "Coding agents implement against TDD and E2E tests" — who writes the tests, and how do you prevent agents from writing tests that only test themselves?

## Your answer

### 24. Why 85% coverage in the Phii Labs CI gate? What does that gate cost you, and what did you trade for it?

## Your answer

### 25. Your uptime probe "opens and closes incident tickets". How does it decide, and how do you avoid flapping and alert noise?

## Your answer

## Data, metrics & your background

### 26. At FinSuper you "picked the change that lifted model precision ~15% and caught another that dropped the approval rate". Explain how you designed that offline A/B comparison — and why a precision lift can still be the wrong ship decision.

## Your answer

### 27. What did fraud analysis teach you that you actually use as an AI engineer?

## Your answer

### 28. You operate 37 hosts and 28 Docker environments. Biggest incident so far? How is your monitoring organized, and what's the alert-to-action path?

## Your answer

## Honesty & pressure questions

### 29. Your resume shows no fine-tuning, no model training, no formal eval-harness numbers like "eval pass rate". Be honest: where are you weakest as an LLM engineer, and what's your plan?

## Your answer

### 30. Where is the "I" versus "we" boundary on this resume? For each product — Rank Wizard, the agent fleet, allrealestate, the CRM — what did you personally build, and what existed before you?

## Your answer
