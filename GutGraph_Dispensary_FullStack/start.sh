#!/usr/bin/env bash
# GutGraph Dispensary 1-Click Production Launcher
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$DIR/venv"

if [[ ! -x "$VENV/bin/python" ]]; then
  echo " [1] Creating virtualenv..."
  if command -v python3.11 >/dev/null 2>&1; then
    python3.11 -m venv "$VENV"
  else
    python3 -m venv "$VENV"
  fi
fi

echo "=========================================================="
echo " 🌿 LAUNCHING GUTGRAPH BOTANICAL DISPENSARY"
echo "=========================================================="
echo " [2] Checking Python environment..."
"$VENV/bin/python" -c "import fastapi, uvicorn, pydantic, sqlite3; print(' ✅ Environment OK')" || {
  echo " ❌ Missing dependencies. Installing...";
  "$VENV/bin/pip" install -r "$DIR/requirements.txt";
}

echo " [3] Starting Backend Server on http://localhost:8000 ..."
echo " [4] Live Frontend & Assets served automatically at http://localhost:8000"
echo "=========================================================="
echo " Press Ctrl+C to stop the server."
echo ""

cd "$DIR/backend"
exec "$VENV/bin/python" server.py