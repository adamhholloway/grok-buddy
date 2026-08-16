#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
export GDK_BACKEND="${GDK_BACKEND:-x11}"
export DISPLAY="${DISPLAY:-:0}"
cd "$ROOT"
exec python3 -m buddy "$@"
