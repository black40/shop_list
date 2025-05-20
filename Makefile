SRC_DIR=.
APP_FILE=main.py

clean:
	find . -type d -name __pycache__ -exec rm -r {} +

run:	clean
	poetry run python $(APP_FILE)

format:
	poetry run ruff format $(SRC_DIR)

check:
	poetry run ruff check $(SRC_DIR)

fix:
	poetry run ruff  check --fix $(SRC_DIR)

typecheck:
	poetry run mypy src/

verify: clean format fix check typecheck run

.PHONY: run format check all typecheck fix verify