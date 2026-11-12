#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

python -m pip install --quiet safety >/dev/null 2>&1 || true
safety check -r requirements-dev.txt || true
