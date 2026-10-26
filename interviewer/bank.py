"""Question bank and session history shared by the agent, the grader and the web UI."""

import datetime
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parent
KEYS = REPO / "keys"
QA = REPO / "qa"
NOTES = REPO / "notes"
RESUME = REPO / "resume" / "resume.md"
SESSIONS = HERE / "sessions"
REPORTS = HERE / "reports"

MODES = ("mock", "diagnostic", "review")
# Languages the interviewer can speak (Gemini Live native audio). English first: it's the default.
LANGUAGES = (
    "English", "Arabic", "Bengali", "Chinese (Mandarin)", "Dutch", "French", "German", "Hindi", "Indonesian",
    "Italian", "Japanese", "Korean", "Marathi", "Polish", "Portuguese", "Russian", "Spanish", "Tamil", "Telugu",
    "Thai", "Turkish", "Ukrainian", "Vietnamese",
)
SESSION_ID = re.compile(r"\d{4}-\d\d-\d\d_\d{6}_(mock|diagnostic|review)")

SYSTEM_DESIGN_SECTION = "08"
BEHAVIORAL_SECTION = "15"
RESUME_SECTION = "16"

EXPERIENCE_ITEM = {
    "kind": "experience",
    "section": RESUME_SECTION,
    "title": "Experience deep-dive: self-introduction and defending resume claims",
    "key": (
        "- Opener: 60-90 seconds, current role, flagship product, 1-2 numbers, why this role.\n"
        "- Flagship project: problem, own contribution (I, not we), architecture, trade-offs, results with numbers.\n"
        "- Every claim consistent with the resume; nothing big that the resume does not mention.\n"
        "- Red flags: rambling list of everything, zero numbers, ToS-sensitive projects, vague 'we did'."
    ),
}


def new_session_id(mode: str) -> str:
    return f"{datetime.datetime.now():%Y-%m-%d_%H%M%S}_{mode}"


def read_optional(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def sections() -> list[str]:
    """Theory section prefixes in study order, without the resume section."""
    return sorted({p.name[:2] for p in QA.glob("[0-9][0-9]-*.md")} - {RESUME_SECTION})


def key_entries(section: str) -> list[dict]:
    """Every question of a section with its grading key, across .partN files."""
    entries = []
    for path in sorted(KEYS.glob(f"{section}-*.md")):
        for block in re.split(r"(?m)^(?=### \d+\. )", path.read_text())[1:]:
            title, _, body = block.partition("\n")
            entries.append({"section": section, "title": title.removeprefix("### ").strip(), "key": body.strip()})
    return entries


def resume_questions() -> list[str]:
    path = next(QA.glob(f"{RESUME_SECTION}-*.md"), None)
    if path is None:
        return []
    return re.findall(r"(?m)^### (\d+\. .+)$", path.read_text())


def load_reports() -> list[dict]:
    """Reports in chronological order (file names start with a timestamp)."""
    return [json.loads(p.read_text()) for p in sorted(REPORTS.glob("*.json"))]


def asked_titles() -> set[str]:
    return {q["title"] for r in load_reports() for q in r["questions"] if q["grade"] != "not_asked"}


def mistakes_queue() -> list[dict]:
    """Questions whose latest grade is fail or partial: fails first, then most recent."""
    latest: dict[str, dict] = {}
    for report in load_reports():
        for q in report["questions"]:
            if q["grade"] != "not_asked":
                latest[q["title"]] = {**q, "date": report["session_id"][:10]}
    misses = [q for q in latest.values() if q["grade"] in ("fail", "partial")]
    misses.sort(key=lambda q: q["date"], reverse=True)
    misses.sort(key=lambda q: q["grade"] != "fail")
    return misses


def plan_mock(rng: random.Random, theory_sections: list[str], n_theory: int) -> list[dict]:
    pool = [e for s in theory_sections for e in key_entries(s)]
    return [
        EXPERIENCE_ITEM,
        *({"kind": "theory", **e} for e in rng.sample(pool, min(n_theory, len(pool)))),
        {"kind": "system_design", **rng.choice(key_entries(SYSTEM_DESIGN_SECTION))},
        {"kind": "behavioral", **rng.choice(key_entries(BEHAVIORAL_SECTION))},
    ]


def plan_diagnostic(rng: random.Random, n: int, spares: int = 3) -> list[dict]:
    """Breadth first: round-robin across sections in study order, skipping questions already graded."""
    asked = asked_titles()
    queues = []
    for s in sections():
        fresh = [e for e in key_entries(s) if e["title"] not in asked]
        rng.shuffle(fresh)
        queues.append(fresh)
    picked = []
    while len(picked) < n + spares and any(queues):
        for q in queues:
            if q and len(picked) < n + spares:
                picked.append(q.pop(0))
    return [{"kind": "diagnostic" if i < n else "spare", **e} for i, e in enumerate(picked)]


REVIEWED = re.compile(r"повторени\w*[^\n\d]{0,3}(\d{4}-\d\d-\d\d)", re.IGNORECASE)
MISTAKE = re.compile(r"ошибк\w*[^\n\d]{0,20}(\d{4}-\d\d-\d\d)", re.IGNORECASE)
# Delivery and resume cards are drilled by the mock interview, not by review.
SKIP_NOTE_SECTIONS = ("Mock",)


def note_cards() -> list[dict]:
    """Cards from notes/review.md that record a mistake, with the dates they were made and reviewed."""
    text = read_optional(NOTES / "review.md")
    cards = []
    for chunk in re.split(r"(?m)^(?=## )", text):
        section, _, body = chunk.partition("\n")
        section = section.removeprefix("## ").strip()
        if section.startswith(SKIP_NOTE_SECTIONS):
            continue
        for block in re.split(r"(?m)^(?=### )", body)[1:]:
            title, _, card = block.partition("\n")
            if "ошибк" not in card.lower():
                continue
            reviewed = REVIEWED.findall(card)
            cards.append(
                {
                    "section": section,
                    "title": title.removeprefix("### ").strip(),
                    "key": card.strip(),
                    "mistake_date": max(MISTAKE.findall(card), default=""),
                    "last_reviewed": max(reviewed, default=""),
                }
            )
    return cards


def review_queue() -> list[dict]:
    """What review mode drills, in order. Anything drilled today waits for another day.

    1. Misses from graded reports (fails first).
    2. Note cards never reviewed, freshest mistake first.
    3. Note cards reviewed before, longest-ago first.
    """
    today = datetime.date.today().isoformat()
    from_reports = [
        {
            "kind": "review",
            "section": q["section"],
            "title": q["title"],
            "key": q["key"],
            "last": {"date": q["date"], "grade": q["grade"], "missing": q["missing"], "wrong": q["wrong"]},
        }
        for q in mistakes_queue()
        if q["date"] != today
    ]
    cards = [c for c in note_cards() if c["last_reviewed"] != today]
    fresh = sorted((c for c in cards if not c["last_reviewed"]), key=lambda c: c["mistake_date"], reverse=True)
    stale = sorted((c for c in cards if c["last_reviewed"]), key=lambda c: c["last_reviewed"])
    from_notes = [{"kind": "review", "section": c["section"], "title": c["title"], "key": c["key"]} for c in fresh + stale]
    return from_reports + from_notes


def plan_review(n: int) -> list[dict]:
    return review_queue()[:n]


def review_available() -> bool:
    return bool(review_queue())
