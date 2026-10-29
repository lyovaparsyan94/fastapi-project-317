PORT ?= 8000

setup: install build-css migrate

install:
	uv sync
	npm ci

build-css:
	npm run build:css

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

.PHONY: setup install build-css dev migrate lint test start render-start build
