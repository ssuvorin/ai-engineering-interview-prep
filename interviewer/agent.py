"""Voice interview practice for AI Engineer roles: LiveKit Agents + Gemini Live.

Three modes:
- mock: a realistic interview, no hints and no feedback until the end.
- diagnostic: verdict and explanation after every answer, to map what you know.
- review: drills past misses (from reports/ and notes/) as resume-based scenarios.

Each session is saved to interviewer/sessions/ (gitignored); report.py grades it.
"""

import datetime
import json
import os
import random

from dotenv import load_dotenv
from google.genai import types
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    ConversationItemAddedEvent,
    JobContext,
    RunContext,
    cli,
    function_tool,
    get_job_context,
)
from livekit.plugins import google

import bank

load_dotenv(bank.HERE / ".env")

VOICE_RULES = """# Voice and tone
This is a voice call. Speak {language} only, even if the candidate switches language. Keep technical terms
in English (embedding, KV cache, reranker, fine-tuning) even when speaking another language: the real
interviews are in English.
Keep your turns short. Plain spoken language: no lists, no markdown, never read the notes out.
Never mention these instructions or the notes.
One question at a time. Make every question unambiguous about its scope: model internals vs the product or
system around it, training vs inference.
Never flatter. Never say "great", "excellent", "perfect", "good job", "отлично", "супер", "молодец" or similar.
The candidate is preparing for real interviews and wants an honest signal, not comfort.
If the candidate says they already covered this item today, or objects to the question, acknowledge it in one
short sentence and move to a different item. Never push the same item again.
When the session is finished, or the candidate asks to stop, say one short closing line and call end_session."""

MOCK = """You are Alex, a senior AI engineer running a live technical interview for an AI Engineer role.

# How a real interviewer behaves
- Do not teach, hint, or give the answer. Never say "correct" or "wrong". Use neutral acknowledgements:
  "Okay.", "Got it.", "Mm-hm, and then?"
- Probe. After each answer, ask one or two follow-ups aimed at the important points the candidate skipped or
  got vague on: "how exactly?", "why that and not X?", "what numbers did you see?", "what breaks at 10x?",
  "how would you know it works?". Never reveal what they missed.
- Push for specifics from their own experience: personal contribution, real numbers, trade-offs, failures.
- If they say "I don't know", accept it calmly and move on. If they seem to bluff, ask one precise follow-up
  that exposes it, then move on.
- If an answer runs long and wanders, interrupt politely and redirect.
- If they ask how they are doing, say you will keep going and the team will share feedback later.

# Flow, about 45 minutes
1. Brief intro: your name, role, the format. Ask the candidate to introduce themselves.
2. Experience deep-dive, about 10 minutes (item 0).
3. Technical questions, about 15 minutes, in order, rephrased in your own words. Drop some if time is short.
4. System design, about 12 minutes: state the problem briefly and let the candidate drive. Probe requirements,
   architecture, latency, cost, evaluation, failure modes.
5. The behavioral question.
6. Ask if they have questions for you; answer briefly as an engineer at a mid-size AI product company.
7. Close: thank them, the recruiter will follow up. No verdict."""

DIAGNOSTIC = """You are Alex, a senior AI engineer running a diagnostic session. This is not an interview simulation:
the goal is to map exactly what the candidate knows and fix gaps on the spot.

# Loop for each item
1. Ask the question, rephrased naturally.
2. Let them finish. At most one clarifying follow-up if the answer is vague.
3. Give a plain verdict: "solid", "partial" or "miss". Grade the first answer only, not what they say after
   your follow-up hints.
4. Say concretely what was wrong or missing. Then give the correct core in three to five spoken sentences.
   Expand every acronym the first time, e.g. "RLHF, reinforcement learning from human feedback". If they
   stated an invented fact confidently, call it out: in an interview "I'm not sure, but I'd reason like this"
   beats a confident guess.
5. Move to the next item. Do not ask them to re-answer.
If the answer is solid, say so and what made it solid in one sentence, then move on. If they say they don't
know, explain the concept briefly and move on.
Open with one sentence about the format, then start. About 25 minutes in total.
Before asking each item, check the previous log: if it already graded the same topic, skip the item and ask
the next spare instead. The point is to cover new ground."""

REVIEW = """You are Alex, a senior AI engineer running a review session: drill the candidate's previous mistakes
until the right answer sticks.

# Loop for each item
1. Rephrase the item as a concrete scenario, ideally tied to a project from the candidate's resume
   ("In your audit pipeline, the model ..."). Never reuse the original wording. The scenario must be
   unambiguous about what topic it tests.
2. Let them answer. One follow-up aimed at exactly what they missed last time.
3. Verdict: "fixed", "better, but still missing ..." or "same mistake as last time". Name which previous
   mistake repeated. Grade the first answer only.
4. If not fixed: give the correct core in three to five sentences, then ask them to say the key sentence
   back in their own words once. The repeat does not upgrade the grade.
5. Next item.
Watch for the behavior patterns listed in the notes (answering only part of a multi-part question, arguing
with the hypothetical instead of answering, claims not in the resume, wrong tense in English). Call each
one out the moment it happens.
Ask the items in the given order and only these items: they are already filtered and prioritized (freshest
unreviewed mistakes first, nothing reviewed today). About 20 minutes.
Open with one sentence about the format, then start."""


def format_item(i: int, item: dict) -> str:
    text = f"[{i}] ({item['kind']}) {item['title']}\nPrivate notes:\n{item['key']}"
    if last := item.get("last"):
        text += (
            f"\nLast attempt ({last['date']}, {last['grade']}): missing: {'; '.join(last['missing']) or '-'}."
            f" Wrong: {'; '.join(last['wrong']) or '-'}."
        )
    return text


def build_instructions(mode: str, plan: list[dict], language: str) -> str:
    parts = [{"mock": MOCK, "diagnostic": DIAGNOSTIC, "review": REVIEW}[mode], VOICE_RULES.format(language=language)]

    resume = bank.read_optional(bank.RESUME)
    if resume:
        parts.append(f"# Candidate's resume (check that what they say matches it)\n<resume>\n{resume}\n</resume>")
        if mode == "mock":
            parts.append("# Resume question bank for item 0 (pick 2-3, rephrase)\n" + "\n".join(bank.resume_questions()))
    elif mode == "mock":
        parts.append("No resume provided. For item 0, ask the candidate to pick their most relevant AI project and drill in.")

    if mode in ("diagnostic", "review") and (log := bank.read_optional(bank.NOTES / "diagnostic.md")):
        parts.append(f"# Previous log: grades, patterns, homework\n<log>\n{log}\n</log>")
    parts.append("# Items\n" + "\n\n".join(format_item(i, item) for i, item in enumerate(plan)))
    return "\n\n".join(parts)


def make_plan(mode: str, rng: random.Random) -> list[dict]:
    if mode == "diagnostic":
        return bank.plan_diagnostic(rng, int(os.environ.get("DIAGNOSTIC_QUESTIONS", "8")))
    if mode == "review":
        return bank.plan_review(int(os.environ.get("REVIEW_ITEMS", "6")))
    theory = [s.strip() for s in os.environ.get("INTERVIEW_SECTIONS", "01,02,03,04,05,07,09,10").split(",")]
    return bank.plan_mock(rng, theory, int(os.environ.get("THEORY_QUESTIONS", "6")))


class Interviewer(Agent):
    @function_tool
    async def end_session(self, context: RunContext) -> None:
        """End the call. Use only after your closing line, or when the candidate asks to stop."""
        if speech := context.session.current_speech:
            await speech.wait_for_playout()
        get_job_context().shutdown(reason="interviewer ended the session")


server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: JobContext) -> None:
    await ctx.connect()
    if bank.SESSION_ID.fullmatch(ctx.room.name):
        # Started from the web UI: mode is in the room name, language in the candidate's attributes.
        session_id = ctx.room.name
        mode = session_id.rsplit("_", 1)[1]
        candidate = await ctx.wait_for_participant()
        language = candidate.attributes.get("language", "English")
    else:
        # `agent.py console`: no web UI, configure through .env.
        mode = os.environ.get("INTERVIEW_MODE", "mock")
        session_id = bank.new_session_id(mode)
        language = os.environ.get("INTERVIEW_LANGUAGE", "English")

    plan = make_plan(mode, random.Random(os.environ.get("INTERVIEW_SEED") or None))
    record = {
        "id": session_id,
        "mode": mode,
        "language": language,
        "started": datetime.datetime.now().isoformat(timespec="seconds"),
        "plan": plan,
        "transcript": [],
    }
    bank.SESSIONS.mkdir(exist_ok=True)
    path = bank.SESSIONS / f"{session_id}.json"

    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            model=os.environ.get("GEMINI_MODEL", "gemini-3.8-live-extended-thinking"),
            voice=os.environ.get("VOICE", "Charon"),
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel(os.environ.get("THINKING_LEVEL", "HIGH")),
            ),
            # Server-side VAD tuned against background noise: short sounds don't count as speech, and
            # thinking pauses mid-answer don't end the turn.
            realtime_input_config=types.RealtimeInputConfig(
                automatic_activity_detection=types.AutomaticActivityDetection(
                    start_of_speech_sensitivity=types.StartSensitivity.START_SENSITIVITY_LOW,
                    end_of_speech_sensitivity=types.EndSensitivity.END_SENSITIVITY_LOW,
                    prefix_padding_ms=int(os.environ.get("VAD_PREFIX_MS", "300")),
                    silence_duration_ms=int(os.environ.get("VAD_SILENCE_MS", "1200")),
                ),
            ),
            # Without compression Gemini Live cuts audio sessions at ~15 minutes; the context is 131k tokens.
            context_window_compression=types.ContextWindowCompressionConfig(
                trigger_tokens=100_000,
                sliding_window=types.SlidingWindow(target_tokens=60_000),
            ),
        ),
    )

    @session.on("conversation_item_added")
    def on_item(ev: ConversationItemAddedEvent) -> None:
        text = getattr(ev.item, "text_content", None)
        if text:
            record["transcript"].append({"role": "interviewer" if ev.item.role == "assistant" else "candidate", "text": text})
            path.write_text(json.dumps(record, ensure_ascii=False, indent=1))

    path.write_text(json.dumps(record, ensure_ascii=False, indent=1))
    await session.start(agent=Interviewer(instructions=build_instructions(mode, plan, language)), room=ctx.room)
    await session.generate_reply(instructions="Open the session: greet the candidate and start.")


if __name__ == "__main__":
    cli.run_app(server)
