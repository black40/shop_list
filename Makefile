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

install:
	poetry install

test:
	poetry run pytest

help:
	@echo "Доступные цели:"
	@echo "  clean      — удалить __pycache__"
	@echo "  run        — запустить приложение"
	@echo "  format     — автоформатирование кода"
	@echo "  check      — проверка стиля кода"
	@echo "  fix        — автоисправление стиля кода"
	@echo "  typecheck  — проверка типов mypy"
	@echo "  verify     — все проверки и запуск"
	@echo "  install    — установка зависимостей"
	@echo "  test       — запуск тестов"

.PHONY: run clean format check fix typecheck verify install test help
