"""Local browser UI: serves web/, mints LiveKit tokens, generates and lists reports.

Binds to 127.0.0.1 only — the API is unauthenticated.
"""

import asyncio
import datetime
import json
import os

from aiohttp import web
from dotenv import load_dotenv
from livekit import api

import bank
import report

load_dotenv(bank.HERE / ".env")

STATIC = bank.HERE / "web"
_report_locks: dict[str, asyncio.Lock] = {}


async def index(request: web.Request) -> web.FileResponse:
    return web.FileResponse(STATIC / "index.html")


async def state(request: web.Request) -> web.Response:
    reports = [
        {"id": r["session_id"], "mode": r["mode"], "score": r["score"], "verdict": r["verdict"]}
        for r in reversed(bank.load_reports())
    ]
    return web.json_response(
        {
            "review_items": len(bank.review_queue()),
            "review_available": bank.review_available(),
            "languages": bank.LANGUAGES,
            "reports": reports[:12],
            "model": os.environ.get("GEMINI_MODEL", "gemini-3.8-live-extended-thinking"),
            "thinking": os.environ.get("THINKING_LEVEL", "HIGH"),
        }
    )


async def token(request: web.Request) -> web.Response:
    body = await request.json()
    mode, language = body.get("mode"), body.get("language", "English")
    if mode not in bank.MODES or language not in bank.LANGUAGES:
        raise web.HTTPBadRequest(text="unknown mode or language")
    if mode == "review" and not bank.review_available():
        raise web.HTTPConflict(text="Nothing to review yet: run a diagnostic first.")
    # The room name is the session id; a fresh room per session gets a fresh agent job.
    room = bank.new_session_id(mode)
    jwt = (
        api.AccessToken(os.environ.get("LIVEKIT_API_KEY", "devkey"), os.environ.get("LIVEKIT_API_SECRET", "secret"))
        .with_identity("candidate")
        .with_name("Candidate")
        .with_attributes({"language": language})
        .with_grants(api.VideoGrants(room_join=True, room=room))
        .with_ttl(datetime.timedelta(hours=2))
        .to_jwt()
    )
    return web.json_response({"url": os.environ.get("LIVEKIT_URL", "ws://localhost:7880"), "token": jwt, "room": room})


def _session_id(request: web.Request) -> str:
    sid = request.match_info["sid"]
    if not bank.SESSION_ID.fullmatch(sid):
        raise web.HTTPBadRequest(text="bad session id")
    return sid


async def get_report(request: web.Request) -> web.Response:
    path = bank.REPORTS / f"{_session_id(request)}.json"
    if not path.exists():
        raise web.HTTPNotFound()
    return web.json_response(json.loads(path.read_text()))


async def make_report(request: web.Request) -> web.Response:
    sid = _session_id(request)
    async with _report_locks.setdefault(sid, asyncio.Lock()):
        cached = bank.REPORTS / f"{sid}.json"
        if cached.exists():
            return web.json_response(json.loads(cached.read_text()))
        await asyncio.sleep(2)  # let the agent flush the last transcript lines
        path = bank.SESSIONS / f"{sid}.json"
        if not path.exists():
            raise web.HTTPNotFound(text="Session not found.")
        session = json.loads(path.read_text())
        if report.candidate_turns(session) < 2:
            raise web.HTTPUnprocessableEntity(text="Too short to grade: fewer than two answers.")
        return web.json_response(await report.generate(session))


app = web.Application()
app.add_routes(
    [
        web.get("/", index),
        web.get("/api/state", state),
        web.post("/api/token", token),
        web.get("/api/report/{sid}", get_report),
        web.post("/api/report/{sid}", make_report),
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("WEB_PORT", "5180"))
    web.run_app(app, host="127.0.0.1", port=port, print=lambda _: print(f"UI: http://localhost:{port}", flush=True))
