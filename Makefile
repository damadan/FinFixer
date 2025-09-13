.PHONY: format lint test run-example

format:
	black .
	ruff check --fix .

lint:
	pre-commit run --all-files

test:
	pytest

run-example:
	python example.py
