# Multimodal AI — Answer Key (1-30)

### 1. What are Multimodal AI models, and how do they process different types of data?
- Идеал: AI that handles multiple data types (text, image, audio, video, sensor) together instead of one. Core recipe: encode each modality → align in a shared embedding space → reason → generate.
- Обязательные пункты:
  - Modality = one type of data; unimodal = one type, multimodal = many together; real world is naturally multimodal (doctor: notes + X-ray + heartbeat).
  - Each input type needs its own encoder (text→vector, image pixels→vector via Vision Transformer, audio→vector); raw pixels/sound can't be read directly.
  - Encoders trained together so outputs land in one shared embedding space — matching pairs (photo "cat" + word "cat") pulled close, mismatched pushed apart (contrastive alignment).
  - A Transformer then reasons across all embeddings and produces output in any modality.
- Частые ошибки: reducing to "text + image"; forgetting per-modality encoders; "one model fits all" (sometimes unimodal is better); ignoring modality alignment data quality.
- Красные флаги: "just merge strings downstream"; "multimodal = GLUE for text only".

### 2. How do vision-language models process images?
- Идеал: images become embeddings via a vision encoder (ViT/CNN) and are combined with text embeddings in a shared space for joint reasoning.
- Обязательные пункты:
  - Image encoder turns pixels into an image embedding; text encoder turns the question into a text embedding.
  - Both go into a single Transformer that reasons across them; answer can be in text.
  - Shared space is built by contrastive training on image-caption pairs.
  - Example: kitchen photo + "How many chairs?" → "There are 4 chairs."
- Частые ошибки: claiming the model "sees" raw pixels directly; using image as pure text-alt prior only.
- Красные флаги: "VLM encodes image bytes/tokens as text"; "no encoder — image is downscaled to small grid and treated as pixels text".

### 3. How do Image Embeddings work?
- Идеал: image embeddings are dense vectors from a neural network that summarize image "meaning"; similar images get similar vectors, different images far apart.
- Обязательные пункты:
  - Raw pixels are just RGB numbers; pixel comparison is slow and ignores meaning → need learned encoders.
  - CNN/ViT layers: early edges/corners → middle parts (eye, wheel) → deep objects (cat) → final embeddings; cosine similarity (-1..1) measures similarity.
  - Created via `SentenceTransformer("clip-ViT-B-32")` → encode → `util.cos_sim`.
  - Used with vector databases (ANN) for fast retrieval by meaning.
- Частые ошибки: comparing raw pixels; using L2 as only metric.
- Красные флаги: "embedding = hash of image pixels"; "don't need training for embeddings".

### 4. How does CLIP work, and why is it important for multi-modal AI?
- Идеал: CLIP learns a shared text-image embedding space via contrastive learning on image-caption pairs.
- Обязательные пункты:
  - Positive pair = image + correct caption; negatives = image + other captions in batch; InfoNCE loss (softmax over positives vs many negatives), temperature τ controls sharpness.
  - Zero-shot classification: compute similarity to label texts, pick highest.
  - Building block for Stable Diffusion/DALL-E condition text; SigLIP replaces softmax with sigmoid loss for memory efficiency, common VLM encoder.
  - Contrastive: positive (augmented views or image-caption) vs negative pairs; similarity cosine.
- Частые ошибки: confusing contrastive with supervised classification; thinking CLIP generates images.
- Красные флаги: "CLIP trained on ImageNet labels"; "CLIP outputs class probabilities".

### 5. What are the key architectures for multi-modal models?
- Идеал: encoder-alignment-generation pipeline; three canonical patterns; shared embedding space then Transformer fusion.
- Обязательные пункты:
  - Per-modality encoders → shared embedding space (contrastively trained) → Transformer backbone → output head.
  - Three patterns: Multimodal Understanding (many inputs → text out; GPT-4V/Gemini/Claude), Cross-Modal Generation (text→image DALL-E/Midjourney; text→video Sora/Veo; audio→text Whisper), Cross-Modal Alignment (CLIP shared-space retrieval).
  - Real models mix patterns (GPT-4o: text+image+audio in, text/audio out, real-time).
  - Trade-offs: heavy/costly/slow vs unimodal; per-modality eval; data alignment quality matters; "one model fits all" false.
- Частые ошибки: only listing model names; no encoder/space/fusion description.
- Красные флаги: "multimodal = single concatenated token stream for all modalities"; "no shared space".

### 6. How does image generation work with diffusion models (Stable Diffusion, DALL-E, Flux)?
- Идеал: start from pure noise, iteratively denoise over ~1000 steps until a clean image appears; model learns reverse process (predict noise added in forward).
- Обязательные пункты:
  - Forward: clean image → add small controlled noise per schedule ~1000 steps → pure noise x_T (no learning needed).
  - Reverse: U-Net predicts noise in noisy image; subtract → cleaner; repeat.
  - Training: sample real image, random step, add that noise, predict it, backprop — stable because the answer (noise) is known vs GANs.
  - Conditional text→image: text embedding (CLIP) guides each reverse denoising step (Stable Diffusion, DALL-E).
  - Latent diffusion (SD) denoises in compressed latent space, not pixels; generation is gradual, never one-shot.
  - Advantages: high quality, stable training, diversity, flexible control (text/sketch/other images); also used for inpainting, super-res, video, audio, molecules.
- Частые ошибки: confusing forward/reverse; "model learns forward"; "generates directly in one step".
- Красные флаги: "diffusion only random generation, no conditioning"; "noise is added after generation".

### 7. What is text-to-speech (TTS), and what models are used for it?
- Идеал: TTS converts text into natural human-like audio (Cross-Modal Generation: text in, audio out). Modern systems are neural, expressive, streaming-capable.
- Обязательные пункты:
  - Core pipeline: text → embeddings/linguistic features → acoustic model (mel-spectrogram) → vocoder → waveform; end-to-end models (e.g. VITS, VALL-E) collapse this.
  - Catalog: autoregressive transformer (Tacotron 2, VALL-E); non-autoregressive fast (FastSpeech, VITS, each parallelizable); LLM-based causal TTS, diffusion-based TTS.
  - Key properties: naturalness/prosody, speaker identity/cloning (embedding-based few-shot), multilingual support, streaming first-chunk latency.
  - For real-time agents: TTS must stream (start audio before full text) and keep within latency budget; quality-latency tradeoff with model size.
- Частые ошибки: reducing TTS to "concatenate recorded snippets"; no latency budget awareness.
- Красные флаги: "TTS is a solved problem — no streaming needed"; "TTS runs strictly after full LLM reply (bottleneck in real-time)".

### 8. How does speech-to-text (Whisper) work?
- Идеал: Whisper is a seq2seq transformer trained on large open web audio (680k hours) to transcribe speech to text, robust to noise/multilingual.
- Обязательные пункты:
  - Audio → log-mel spectrogram features → encoder; decoder autoregressively generates text tokens (special tokens for language/task).
  - Training: massive diverse weakly-supervised web audio-text pairs; self-supervised pre-training to predict transcriptions.
  - Variants by size (tiny→large) trade latency/accuracy; for real-time use cases, streaming/chunked ASR required (Whisper designed for full utterances).
  - Capabilities: transcription, translation to English, language identification, timestamping.
  - Roles in voice agents: ASR component; provides partial transcripts for streaming; robust to accents/noise but can hallucinate on silence/noise.
- Частые ошибки: saying Whisper is a keyword-spotter/classifier; using large Whisper in real-time without streaming adaptation.
- Красные флаги: "Whisper transcribes frame by frame in real time by default"; "Whisper has no translation/ multilingual capability".

### 9. Budget the end-to-end latency for a real-time voice agent (VAD, ASR, LLM, TTS, network). Where does the time go?
- Идеал: target ~800 ms from user stops speaking to first agent audio (never > 1.5 s, ideally < 1 s); humans reply in 200-500 ms. Budget is dominated by LLM first-token and ASR finalization.
- Обязательные пункты:
  - Voice-to-voice latency = time from user's last word to first agent audio heard; the single deciding metric.
  - Share budget (of ~800 ms): network/RTT ~50-150 ms (transport, WebRTC/UDP preferred over TCP); VAD/end-pointing ~100-200 ms (silence threshold to confirm user finished — must not cut off); streaming ASR ~100-300 ms to produce final transcript; LLM prefill + first token ~150-400 ms (streaming TTFT; KV-cache growth during decode); streaming TTS first chunk ~50-150 ms; jitter buffer/playback overhead.
  - Where time goes: LLM first-token latency and ASR finalization dominate; VAD end-point timeout adds a constant floor; network RTT adds per hop; TTS stays small if it streams (speech starts before full reply).
  - Techniques: stream audio in 20 ms chunks; partial (interim) transcripts let LLM start early; prompt/KV-cache prefix sharing (vLLM PagedAttention) for a stable system prompt; quantized/faster models at the edge; TTS chunk streaming.
- Частые ошибки: quoting only one model's time (LLM) and forgetting VAD + network RTT; assuming the budget starts at button-press rather than at end-of-speech; enabling "reply after full TTS render".
- Красные флаги: "800 ms is only about the LLM"; "TTS must finish before the reply starts" — it can stream.

### 10. How do you handle barge-in (user interruptions) in a voice agent?
- Идеал: detect concurrent user speech, immediately stop agent playback, drop buffered agent audio, and re-enter listen mode to take the new user input.
- Обязательные пункты:
  - While agent is speaking, keep VAD + streaming ASR running on the user's audio (agent shouldn't assume silence).
  - On user speech detected, send `clear_audio_buffer` to drops the not-yet-played agent audio and halt TTS; then process the new user text with the LLM and reply.
  - Echo cancellation (AEC) is essential — without it the agent hears its own speech from the user's speaker and interrupts itself ("agent interrupts itself").
  - Messages: client sends `audio_chunk` and `playback_progress`; orchestrator sends `clear_audio_buffer`, `agent_speech_started`, `agent_speech_ended`, transcript_interim/final.
  - Design nuance: decide which content to discard — finished replies irrelevant, partially-played reply should be dropped; barge-in must gracefully handle an actual interruption vs mic picking up background noise.
- Частые ошибки: ignoring barge-in entirely; forgetting AEC (self-interruption); playing full reply to end before listening again.
- Красные флаги: "user cannot interrupt", "we just restart the whole LLM call and lose context".

### 11. Cascaded ASR + LLM + TTS vs native speech-to-speech models: what are the trade-offs?
- Идеал: decompose into three approaches — cascaded pipeline (async/streaming), end-to-end speech-to-speech, hybrid — compare latency, quality, control, cost.
- Обязательные пункты:
  - Cascaded (STT → LLM → TTS): standards, modular (upgrade each component independently), high control, rich tool integration, easier debugging; but ≥ 3 conversion stages (compounding ASR→text errors), more total latency, and needs streaming orchestration.
  - Speech-to-speech/native: single model consumes audio in and produces audio out; lower latency, preserves prosody/emotion/para-linguistics, less compounding-text errors; but harder to debug, more opaque, limited tool/format control, still maturing, expensive to train/serve.
  - Hybrid: use cascaded pipeline for tool-heavy/agentic turns (order lookup), switch to speech-to-speech for chit-chat/emo requirement — best of both where justified.
  - Decision depends on latency budget vs controllability, tool use, and cost.
- Частые ошибки: claiming one approach always wins; ignoring streaming in cascade.
- Красные флаги: "cascaded = just call three APIs sequentially, no streaming"; "native s2s has zero latency".

### 12. What is multi-modal RAG, and how does it differ from text-only RAG?
- Идеал: extend RAG beyond text: index images, tables, audio, video (or their text descriptions/embeddings) and retrieve the relevant modality, then ground an LLM/VLM answer on it.
- Обязательные пункты:
  - Text-only RAG: embed text chunks → vector DB → retrieve top-k → prompt LLM; single modality.
  - Multimodal RAG: (1) multimodal indexing — image/audio/video stored and embedded (CLIP-style embeddings), often alongside text captions/OCR; (2) fusion retrieval — query matches one or more modalities (image by text); (3) answer either via multimodal LLM (VLM) with the retrieved image, or via a caption/OCR pipeline.
  - Key differences: richer sources (tables/charts/diagrams), need per-modality embedding alignment, image/video retrieval uses CLIP-style models, answer may reference visual context, PDFs go through layout parsing + image-text pairing.
- Частые ошибки: thinking "multimodal RAG = image in text chunk"; indexing only text extracts and losing images.
- Красные флаги: "images are always converted to captions, never retrieved directly"; "no VLM in the answer stage".

### 13. How do you build a system that processes both images and text?
- Идеал: an end-to-end pipeline with image + text encoders producing aligned embeddings, a fusion/reasoning model (VLM), and clean I/O contracts; reuse a pretrained VLM.
- Обязательные пункты:
  - Ingestion: parse and normalize inputs (image preprocessing/resizing, OCR for scanned text in images, text cleaning).
  - Representation: image encoder embeddings (ViT/CNN) + text embeddings in a shared space (CLIP-style contrastive training).
  - Reasoning: a multimodal LLM (VLM) that takes image + text and returns text — covers VQA, captioning, document understanding.
  - Interfaces: streaming or batch, structured outputs; schema for results.
  - Design choices: use a pretrained VLM (GPT-4V, LLaVA-style) vs train a custom fusion model; choose fusion depth (early/late, see Q24), cost/latency, per-modality eval.
- Частые ошибки: NOT aligning modalities; building a bespoke fusion from scratch without pretraining data; ignoring the labeling/OCR of images.
- Красные флаги: "just concatenate the image bytes to the prompt"; "no evaluation per modality".

### 14. What are multi-modal embeddings, and how are they used for cross-modal search?
- Идеал: embeddings from different modalities mapped into one shared vector space so that a query in one modality finds matches in another.
- Обязательные пункты:
  - Single space trained contrastively (e.g. CLIP: image + text) — similar semantics close regardless of source modality.
  - Cross-modal search: text query → embedding → nearest images in the shared space; or image → nearest text segments.
  - Retrieval = approximate nearest neighbor search over the vector database (ANN); similarity metric = cosine similarity.
  - Related: matching for retrieval, recommendation, zero-shot classification (label-text vs image).
- Частые ошибки: storing each modality in its own vector DB and never aligning; using L2 as default.
- Красные флаги: "embeddings are text-only"; "no aligned shared space".

### 15. How do you evaluate multi-modal AI systems?
- Идеал: evaluate per modality AND jointly (system-level), on task-specific metrics — reasoning accuracy, generation quality, alignment consistency.
- Обязательные пункты:
  - Task-level metrics: VQA/captioning accuracy (BLEU, CIDEr, METEOR, SPICE, Grammar), generation FID/Inception Score, text-to-image alignment (CLIP score, human eval).
  - Per-modality eval: text (perplexity, agreement) and image/video separation — don't combine only the aggregate.
  - Joint metrics: cross-modal consistency (embedding distance), factual consistency, hallucination rate for VLMs, temporal coherence for video, audio sync for video.
  - Benchmarks: standard multimodal benchmarks (VQA, GQA, COCO Captioning, MM-Vet, MMMU), robustness to noise/adversarial input, fairness per modality.
  - Process: human eval + automatic metrics, eval per use case (chat answer vs describing image).
- Частые ошибки: single metric for the whole system; only text-based eval.
- Красные флаги: "BLEU on captions covers image understanding"; "no human eval for open-ended answers".

### 16. What are the challenges of real-time multi-modal AI processing?
- Идеал: latency, continuous streams, compute cost, and synchronization across modalities are the core challenges.
- Обязательные пункты:
  - Real-time latency: strict budgets (voice < 800 ms), streaming vs batch; noise handling in audio.
  - Compute: large GPU memory for video/high-resolution images, throughput per GPU, KV cache growth, serving engines (vLLM, PagedAttention) for efficient batching.
  - Stream sync: aligning audio/video/text streams — order and timing must stay consistent, interruptions, echo.
  - Cost: expensive models at scale; use of small/quantized models where possible, on-device vs cloud offload.
  - Quality: accuracy degradation for faster/smaller models; hallucination on low-quality input; robustness to messy real inputs (noise, blurred images).
- Частые ошибки: treating each modality independently; ignoring serving/batching economics.
- Красные флаги: "stream it and it's automatically real-time"; "no need for echo cancellation for barge-in".

### 17. How do you handle video understanding with AI?
- Идеал: treat video as a spatio-temporal signal —sample frames plus audio stream, encode per-frame appearance, and model temporal structure explicitly.
- Обязательные пункты:
  - Sample frames (uniform or keyframe-based); pipe them into a vision encoder (ViT/CNN) producing per-frame embeddings.
  - Add a temporal axis: video transformer / 3D CNN / attention over frame embeddings so motion and ordering are captured, not just static content.
  - Align video + audio (ASR transcript) with text in a shared space; use a video-language model (CLIP-style dual encoder) for retrieval/captioning/VQA.
  - For real-time: stream chunks, process incrementally with buffering; for offline: batch, subsample (~2-10 FPS).
  - Bottlenecks: compute/memory for long videos, temporal coherence, audio/video sync, frame redundancy.
- Частые ошибки: feeding every frame at native resolution (explodes compute); ignoring the audio track.
- Красные флаги: "video understanding = average of per-frame captions"; "no temporal modelling at all".

### 18. What is visual question answering (VQA)?
- Идеал: a model answers a natural-language question given an image — a canonical VLM task requiring both vision and reasoning.
- Обязательные пункты:
  - Inputs: image + question → text answer; requires encoding image into embeddings and fusing with the question.
  - Paradigms: end-to-end VLM (vision encoder + LLM cross-attention) is the standard; retrieval-based VQA indexes similar image-QA pairs; use OCR in document VQA.
  - Benchmarks: VQA v2 (anti-bias), GQA (reasoning), OK-VQA (outside knowledge), VizWiz (assistive), DocVQA (documents).
  - Metrics: accuracy, exact/match, hallucination rate, answer consistency; human eval for open-ended.
  - Cross-modal generation pattern: image+text in, text out.
- Частые ошибки: assuming captioning the image is enough; ignoring reasoning needed for "how many".
- Красные флаги: "VQA doesn't need to see the image at all"; "VQA = object detection".

### 19. What is document understanding, and how do models parse documents with layouts?
- Идеал: extraction and reasoning over formatted documents (text + tables + figures + reading order), not just OCR text — layout-aware parsing.
- Обязательные пункты:
  - OCR (if scanned) → combine with layout analysis: detect text blocks, tables, figures, headers, reading order; serialise into markup the LLM can structure-aware process — spatial/LayoutLM-style models encode 2D layout tokens.
  - Layout models: LayoutLM (position embeddings), modern VLMs directly consume rendered pages (image patches) + text.
  - Handle tables: convert to structured (HTML/markdown/TSV) rather than flatten; figures get captions.
  - Multi-page docs: chunk into regions, merge, link vision + text representations.
- Частые ошибки: naive OCR-to-string flattening loses layout/table structure.
- Красные флаги: "document understanding = plain text extraction only"; "layout detection is optional".

### 20. How do you fine-tune a vision-language model?
- Идеал: freeze/preserve pretrained VLM and adapt via LoRA/adapter on a task dataset (image+text pairs), keep backbone, evaluate domain quality.
- Обязательные пункты:
  - Data: paired (image, text) or (image, question, answer); augment with pairs 1:1.
  - Fine-tuning methods: full fine-tune, LoRA (low-rank adaptation) to keep pretrained base + adapters; PEFT (LoRA, QLoRA) for efficiency — include instruct-tuning.
  - Loss: contrastive loss for alignment; CE/correspondence loss for matching — balance Wisdom.
  - Keep vision + language equal; use mixed-modality batch; eval on a held-out eval, and per domain, avoid overfit.
- Частые ошибки: freezing vision component entirely and only tuning head; no eval split.
- Красные флаги: "just add more pairs without validation"; "fine-tune = prompt" (not fine-tune).

### 21. What are the latency and cost considerations for multi-modal AI in production?
- Идеал: latency is dominated by model size + token count + server batching/indexing; cost scales with GPU, tokens, and chosen model.
- Обязательные пункты:
  - Latency: inference engine (vLLM/PagedAttention batching), KV-cache reuse for prefixes, quantization (less latency+VRAM), smaller models, distillation — leverage existing infra.
  - Cost per request: tokens per modality (images cost more than text), video expansion; usage plans; batch vs real-time tension; caching with RAG + KV-cache reuse.
  - Optimizations: chunk caching, retrieval to trim input, on-device preprocessing (VAD local to avoid sending).
  - Evaluation thresholds; if latency too high — increase batch GPUs/quantize; if cost too high — distill reuse.
- Частые ошибки: underestimating KV cache, ignoring per-modality token cost.
- Красные флаги: "quantization has zero downside", "image tokens are free".

### 22. How do you handle multi-modal content moderation?
- Идеал: every modality (text, image, audio, video) gets a dedicated policy check — textual, visual, audio — before user-visible output.
- Обязательные пункты:
  - Layered checks: input guard (over user prompt/media), output guard (model-generated content), agent and classifier pipelines.
  - Text: unsafe rhetoric moderation; Image: NSFW/violence/flags via classification; Audio/video: speech + appearance filters.
  - Distinct policy engines per modality — use dedicated classifiers (content-safety classifiers) and combine results.
  - Cost: routing/risk-based; low-risk gendered to classifier, high-risk to human review.
  - Red-teaming, ongoing tuning, vendor vs self-built.
- Частые ошибки: moderating only the text part of a response; no output guard.
- Красные флаги: "moderation = only text classifier"; "no output guard after generation".

### 23. What is text-to-video generation, and what are the current state-of-the-art approaches?
- Идеал: generate a coherent video clip from a text prompt — conditions appearance, motion, and temporal consistency.
- Обязательные пункты:
  - Models: diffusion-based video generators (Sora, Veo, Pika, Runway Gen-3) that denoise a latent video tensor conditioned on text; some are autoregressive LLM hybrids.
  - Approach: text encoding (CLIP-style), 3D VAE compresses video → latent, conditional diffusion (temporal U-Net/DiT) generates frames, decoder/waveform reconstruct.
  - Challenges: temporal coherence (flicker), motion plausibility, length, resolution/cost, and conditioning precision; evaluating with CLIP score + user studies.
- Частые ошибки: concatenated independent frames → grain/flicker.
- Красные флаги: "text-to-video = generate one keyframe, then copy it"; "no temporal modelling".

### 24. Explain Multimodal Fusion Techniques: Early Fusion vs Late Fusion.
- Идеал: early fusion merges raw inputs/feature maps at the very beginning of the model; late fusion merges high-level predictions at the end.
- Обязательные пункты:
  - Early fusion: concatenate raw data/early features to feed one model; enables cross-modal low-level interaction (e.g. text + image at 240px input); single model, but requires entangled feature alignment and shared capacity.
  - Late fusion: train separate encoders per modality, get separate representations/predictions, then combine (average/weighted vote, or a small fusion layer); keeps per-modality models specialized; easier to keep unimodal components; interaction occurs late (post-hoc), may miss fine-grained joint cues.
  - In CLIP both encoders are contrastively tied (not classic early/late): the fusion is in the shared embedding space; modern VLMs fuse via cross-attention (a form of intermediate fusion) — explain trade-offs.
  - Factors: data type, task (QA needs joint reasoning → early/intermediate better), ability to reuse pretrained per-modality models (late), compute constraints, label alignment.
- Частые ошибки: "early = better", generalizing that late is only used for score fusion (it also covers feature-level fusion at the end).
- Красные флаги: "early fusion always loses information", "late fusion always better than early".


### 25. Your vision-language model generates factually incorrect image descriptions. How do you fix it?
- Идеал: diagnose root cause (hallucination, low-res input, bias) then apply grounding + input/output checks and eval.
- Обязательные пункты:
  - Improve input resolution/unclear visuals; add caption to retrieve correct region.
  - Add prompt/system instruction: "describe only what you see"; add verification step (human/LLM judge).
  - Tune: fine-tune on truthful pairs RLHF/RLAIF penalizing hallucinations; use grounding/tools to verify objects (OCR).
  - Eval with a vision QA set that penalizes fabrication; iterate on feedback.
  - Post-processing guard: compare claims against detected objects (SynthID-class check) and refuse uncertain answers.
- Частые ошибки: fixing symptoms by prompt alone when model consistently fabricates; no eval split punishing hallucination.
- Красные флаги: "the image is irrelevant, LLM generates captions from text priors" (that IS the bug).

### 26. Your VLM answers single-image questions but fails on multi-page documents. How do you fix it?
- Идеал: single-image model lacks cross-page context — feed pages in parallel and/or RAG across pages with layout-aware chunking.
- Обязательные пункты:
  - Cause: context limit, page reads truncated, no document layout reading — model answers from whichever page fits.
  - Fix: chunk pages into regions/layout-aware passages; retrieve the relevant pages via embeddings (multimodal RAG) before the LLM call; pass multiple page images at once when supported.
  - For reasoning: convert document to structured layout (markdown/HTML), retrieval → answer with citations to page/region.
  - Tune a document-VLM (DocVQA fine-tuned) on layout-aware data.
- Частые ошибки: trying to force the entire PDF into one prompt; ignoring retrieval.
- Красные флаги: "pass all pages at full res" (context blowout); "just OCR every page to a string".

### 27. Your multimodal LLM ignores the image and generates descriptions from text alone. How do you fix it?
- Идеал: force the model to actually consume the image pathway — check image was encoded and returned to the model, not dropped.
- Обязательные пункты:
  - Debug: verify the image embedding is attached (not the "ignore image" bias); test with image-only prompts and graded image feature (CLIP) feedback.
  - Fix: ensure image actually reaches encoder — pass through CLIP/ViT, not placeholder tokens; use graded examples requiring visual reasoning in training; add instruction "look at the image".
  - Fine-tune on pairs that REQUIRE the image for correct answer (so text-only shortcut fails) — e.g. "what color is the car in the image?".
  - Eval: remove text, compare; test that answer changes when image changes.
- Частые ошибки: blaming the model, not the pipeline (image dropped upstream).
- Красные флаги: "the model doesn't see images at all"; "answers identical regardless of image" — that's the bug.

### 28. Your diffusion model ignores precise control requirements in text prompts. How do you improve controllability?
- Идеал: strengthen conditioning — better text encoder, cross-attention alignment, ControlNet/guidance, or fine-tune on paired data.
- Обязательные пункты:
  - Use higher-quality text encoder (CLIP → T5/large) and stronger conditioning: CFG guidance (guidance scale), cross-attention mapping to model regions (ControlNet, LoRA layers).
  - Provide structural conditioning: ControlNet (pose, depth, sketch), reference images, keyframe region input.
  - Fine-tune / LoRA on data with explicit attribute tags so the model learns precise tokens.
  - Evaluate controllability: prompt-following metrics (CLIP score, human), rather than visual quality only.
- Частые ошибки: relying on a text prompt alone and expecting exact spatial/region adherence; no guidance conditioning.
- Красные флаги: "ControlNet not needed, prompt embeds it all"; "only quality matters".

### 29. Your diffusion model generates sharp but repetitive images. How do you balance quality vs diversity?
- Идеал: strike a balance between stable/quality and diversity — tune sampling randomness, guidance, and sampling steps.
- Обязательные пункты:
  - High CFG guidance scale → sharper but less diverse (over-saturation); lower guidance → more diverse but blurrier/weak alignment.
  - Seed/random noise diversity, classifier-free guidance strength, temperature in latent (if applicable), stochastic sampling (DDPM/ancestral) vs deterministic (DDIM) — ancestral sampling brings more variation.
  - Increase number of denoising steps for quality; add stochastic noise injection at reverse steps (SDE) for diversity.
  - Measure on eval: FID vs CLIP score tradeoff; accept trade-off tuned to product goals.
- Частые ошибки: extremes — pure quality (0 diversity) or pure diversity (gibberish).
- Красные флаги: "quality and diversity are independent", "just raise guidance".

### 30. Your diffusion model takes too long per image. How do you speed up sampling?
- Идеал: accelerate denoising — fewer steps (distillation/schedulers), latent space, and efficient sampling — while preserving quality.
- Обязательные пункты:
  - Fewer/larger steps: DDIM / improved schedulers that allow 20-50 steps instead of 1000; progressive distillation to 4-8 steps; consistency models (single-step).
  - Latent diffusion: denoise in a compressed latent, decode once — big win.
  - Model/arch: U-Net/DiT distillation, token/weight quantization, compile (TensorRT/ONNX), diffusion sampling parallelization (SDXL) / CFG; batch on GPU, cache text embeddings.
  - Distillation/distillation-free acceleration, on good GPU, SD-Turbo/etc.
- Частые ошибки: throwing compute at a slow number of steps; no scheduler tuning.
- Красные флаги: "1000 steps required always", "speed not a constraint".