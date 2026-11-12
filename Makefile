PYTHON ?= python3
VENV ?= .venv

.PHONY: install test lint security run

install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && pip install -U pip && pip install -r requirements-dev.txt

test:
	. $(VENV)/bin/activate && pytest -q

lint:
	. $(VENV)/bin/activate && ruff check orchestrator apps || true

security:
	bash security/scripts/run_sast.sh
	bash security/scripts/run_dependency_scan.sh
	bash security/scripts/run_fuzz.sh

run:
	. $(VENV)/bin/activate && python -m orchestrator.main --intent intent.md
