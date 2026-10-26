"""Critical post-session report: grades a saved session against keys/ with a Gemini text model.

    uv run report.py sessions/<id>.json     # grade a session, e.g. one from `agent.py console`

Writes reports/<id>.json (feeds the review mode) and reports/<id>.md (gitignored).
"""

import asyncio
import datetime
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

import bank

load_dotenv(bank.HERE / ".env")

GRADES = ["pass", "partial", "fail", "not_asked"]
GRADE_MARK = {"pass": "✓", "partial": "±", "fail": "✗", "not_asked": "·"}
MODE_TITLE = {"mock": "Mock interview", "diagnostic": "Diagnostic", "review": "Review of past mistakes"}
MODE_BRIEF = {
    "mock": "realistic interview: the interviewer gave no hints and no feedback.",
    "diagnostic": "after each answer the interviewer gave a verdict and explained the gap; ignore those explanations as candidate knowledge.",
    "review": "drilled previous mistakes; each item says what was missed last time. Judge whether each mistake is fixed.",
}

SYSTEM = """You review a recorded practice session of a candidate preparing for AI Engineer interviews (mid/senior level, Dubai market, interviews in English). Write a critical report for the candidate's own preparation.

The candidate explicitly asked for no flattery. The purpose is to find everything that would cost them an offer, so they can fix it before the real interview. Be direct and specific. Do not soften, do not pad, do not encourage.

Grading:
- Grade only what the candidate actually said. Back each grade with a short quote or close paraphrase of their words in `evidence`.
- Grade the candidate's FIRST answer to each item. Anything they say after the interviewer hinted, explained, or gave the answer does not count.
- pass: covers the must-cover points of the key with the correct mechanism and terms. partial: right direction but missing must-cover points, the mechanism, or the terminology. fail: wrong, empty, "don't know", or off-topic. not_asked: never came up.
- Buzzwords without mechanism are partial at best. A confidently invented fact is a red flag even if the rest is right.
- Answering only part of a multi-part question, arguing with the premise instead of answering, rambling past about two minutes, no numbers, "we" instead of "I": list these under patterns.
- If a resume is given, check every claim against it. Claims missing from the resume or contradicting it are red flags.
- If a previous log is given, name repeated mistakes and patterns explicitly with a count ("3rd time").
- Strengths: only with evidence. An empty list is fine. Never invent strengths to balance the report.
- Questions the interviewer asked that are not in the item list: add them with ref -1 and the question in `title`.
- score: 1-5 against a real AI Engineer interview bar, 3 = borderline. In diagnostic and review modes score readiness on the covered topics.
- verdict: mock mode: one of Strong hire, Hire, Lean hire, Lean no hire, No hire. Other modes: a short readiness verdict.
- correct_core: the interview-ready answer they should have given, 2-4 sentences, in English.
- homework: 3-7 items ordered by impact, each doable within an hour and concrete: which concept to learn, which file to read (keys/<file>.md question N, reference/...), what to re-answer out loud and how many times.
- The transcript comes from speech recognition. Ignore transcription noise; penalize a misheard word only if the meaning is clearly wrong.
- Write all prose in {language}, except correct_core in English. Keep technical terms in English. Expand each acronym the first time it appears."""

STRINGS = {"type": "array", "items": {"type": "string"}}
SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "integer", "minimum": 1, "maximum": 5},
        "verdict": {"type": "string"},
        "summary": {"type": "string", "description": "2-4 blunt sentences: where the candidate stands and the single biggest blocker."},
        "problems": {**STRINGS, "description": "Most costly first."},
        "strengths": STRINGS,
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ref": {"type": "integer", "description": "Item index, or -1 for a question not in the list."},
                    "title": {"type": "string"},
                    "grade": {"type": "string", "enum": GRADES},
                    "evidence": {"type": "string"},
                    "missing": STRINGS,
                    "wrong": STRINGS,
                    "correct_core": {"type": "string"},
                },
                "required": ["ref", "title", "grade", "evidence", "missing", "wrong", "correct_core"],
            },
        },
        "patterns": STRINGS,
        "red_flags": STRINGS,
        "homework": STRINGS,
    },
    "required": ["score", "verdict", "summary", "problems", "strengths", "questions", "patterns", "red_flags", "homework"],
}


def build_prompt(session: dict) -> str:
    items = []
    for i, item in enumerate(session["plan"]):
        text = f"[{i}] ({item['kind']}) {item['title']}\nKey:\n{item['key']}"
        if last := item.get("last"):
            text += f"\nLast attempt ({last['grade']}): missing {last['missing']}; wrong {last['wrong']}"
        items.append(text)
    transcript = "\n".join(f"{t['role'].capitalize()}: {t['text']}" for t in session["transcript"])
    parts = [
        f"Mode: {session['mode']}: {MODE_BRIEF[session['mode']]}",
        "Items (ref, kind, question, grading key):\n" + ("\n\n".join(items) or "none, see the transcript"),
    ]
    if resume := bank.read_optional(bank.RESUME):
        parts.append(f"Resume:\n{resume}")
    if log := bank.read_optional(bank.NOTES / "diagnostic.md"):
        parts.append(f"Previous log:\n{log}")
    parts.append(f"Transcript:\n{transcript}")
    return "\n\n---\n\n".join(parts)


def candidate_turns(session: dict) -> int:
    return sum(t["role"] == "candidate" for t in session["transcript"])


async def generate(session: dict) -> dict:
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = await client.aio.models.generate_content(
        model=os.environ.get("REPORT_MODEL", "gemini-3.8-flash"),
        contents=build_prompt(session),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM.format(language=session.get("language", "English")),
            response_mime_type="application/json",
            response_json_schema=SCHEMA,
            thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
        ),
    )
    raw = json.loads(response.text)

    plan = session["plan"]
    questions = []
    for q in raw.pop("questions"):
        item = plan[q["ref"]] if 0 <= q["ref"] < len(plan) else {"kind": "extra", "section": "", "title": q["title"], "key": ""}
        questions.append({**{k: item[k] for k in ("kind", "section", "title", "key")}, **{k: q[k] for k in ("grade", "evidence", "missing", "wrong", "correct_core")}})
    # Spares the interviewer never used are noise, not "not asked".
    questions = [q for q in questions if not (q["kind"] == "spare" and q["grade"] == "not_asked")]

    report = {
        "session_id": session["id"],
        "mode": session["mode"],
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
        **raw,
        "questions": questions,
    }
    bank.REPORTS.mkdir(exist_ok=True)
    (bank.REPORTS / f"{session['id']}.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    (bank.REPORTS / f"{session['id']}.md").write_text(to_markdown(report))
    return report


def to_markdown(r: dict) -> str:
    def bullets(items: list[str], numbered: bool = False) -> str:
        return "\n".join(f"{f'{i}.' if numbered else '-'} {x}" for i, x in enumerate(items, 1)) or "—"

    out = [
        f"# {MODE_TITLE[r['mode']]} — {r['session_id'][:10]}",
        f"**Score:** {r['score']}/5 · **Verdict:** {r['verdict']}",
        r["summary"],
        f"## Problems\n\n{bullets(r['problems'], numbered=True)}",
        f"## Strengths\n\n{bullets(r['strengths'])}",
        "## Questions",
    ]
    for q in r["questions"]:
        block = [f"### {GRADE_MARK[q['grade']]} {q['title']}"]
        if q["evidence"]:
            block.append(f"> {q['evidence']}")
        if q["wrong"]:
            block.append("**Wrong:**\n" + bullets(q["wrong"]))
        if q["missing"]:
            block.append("**Missing:**\n" + bullets(q["missing"]))
        if q["correct_core"]:
            block.append(f"**Correct core:** {q['correct_core']}")
        out.append("\n\n".join(block))
    out += [
        f"## Patterns\n\n{bullets(r['patterns'])}",
        f"## Red flags\n\n{bullets(r['red_flags'])}",
        "## Homework\n\n" + ("\n".join(f"- [ ] {h}" for h in r["homework"]) or "—"),
    ]
    return "\n\n".join(out) + "\n"


if __name__ == "__main__":
    session = json.loads(Path(sys.argv[1]).read_text())
    report = asyncio.run(generate(session))
    print(bank.REPORTS / f"{report['session_id']}.md")
