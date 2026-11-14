#!/usr/bin/env bash
# Runs the full test suite
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/backend/tests/test_server.py"
