#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v python >/dev/null 2>&1; then
  echo "python is required but not found in PATH." >&2
  exit 1
fi

python scripts/bootstrap_local_postgres.py
