#!/usr/bin/env bash
# GutGraph Dispensary 1-Click Production Launcher
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo " 🌿 LAUNCHING GUTGRAPH BOTANICAL DISPENSARY"
echo "=========================================================="
echo " [1] Checking Python environment..."
python3 -c "import fastapi, uvicorn, pydantic, sqlite3; print(' ✅ Environment OK')" || {
  echo " ❌ Missing dependencies. Installing...";
  pip install -r "$DIR/requirements.txt";
}

echo " [2] Starting Backend Server on http://localhost:8000 ..."
echo " [3] Live Frontend & Assets served automatically at http://localhost:8000"
echo "=========================================================="
echo " Press Ctrl+C to stop the server."
echo ""

cd "$DIR/backend"
python3 server.py
