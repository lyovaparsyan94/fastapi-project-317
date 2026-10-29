PORT ?= 8000

setup: install migrate

install:
	uv sync

dev:
	uv run fastapi dev page_analyzer/app.py --port $(PORT)

migrate:
	uv run alembic upgrade head

lint:
	uv run ruff check .

test:
	uv run pytest -vv

start:
	uv run fastapi run page_analyzer/app.py --port $(PORT) --workers 4

render-start:
	fastapi run page_analyzer/app.py --port $(PORT) --workers 5

build:
	./build.sh

.PHONY: setup install dev migrate lint test start render-start build
