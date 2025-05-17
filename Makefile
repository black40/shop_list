SRC_DIR=.
APP_FILE=main.py

clean:
	find . -type d -name __pycache__ -exec rm -r {} +

run: clean
	poetry run python $(APP_FILE)

format:
	poetry run ruff format $(SRC_DIR)

check:
	poetry run ruff check $(SRC_DIR)

.PHONY: run format check