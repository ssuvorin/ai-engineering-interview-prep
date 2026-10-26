#!/usr/bin/env bash
# Starts the local LiveKit server, the interviewer agent and the web UI. Ctrl+C stops all three.
set -euo pipefail
cd "$(dirname "$0")"
trap 'kill 0' EXIT

livekit-server --dev >/dev/null 2>&1 &
uv run agent.py dev &
uv run web.py
