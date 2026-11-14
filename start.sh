#!/usr/bin/env bash
# Canonical launcher — GutGraph Botanical Dispensary (full-stack SPA + API)
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/GutGraph_Dispensary_FullStack/start.sh" "$@"