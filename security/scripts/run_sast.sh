#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

python -m pip install --quiet bandit semgrep >/dev/null 2>&1 || true
bandit -r apps --exclude .venv -q || true
semgrep --config auto --exclude .venv apps || true
