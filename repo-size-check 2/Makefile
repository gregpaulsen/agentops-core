.PHONY: setup lint format test precommit

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt && pre-commit install

lint:
	ruff check .

format:
	black . && isort .

test:
	pytest

precommit:
	pre-commit run --all-files
