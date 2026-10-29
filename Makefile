PORT ?= 8000
# Render сам задаёт WEB_CONCURRENCY по размеру инстанса: на free-тарифе это 1,
# пять воркеров в 512 МБ не помещаются и их убивает OOM.
WORKERS ?= $(if $(WEB_CONCURRENCY),$(WEB_CONCURRENCY),5)

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

reset-db:
	uv run alembic downgrade base
	uv run alembic upgrade head

lint:
	uv run ruff check .

test:
	uv run pytest -vv

start:
	uv run fastapi run page_analyzer/app.py --port $(PORT) --workers 4

render-start:
	fastapi run page_analyzer/app.py --port $(PORT) --workers $(WORKERS)

# Запуск на хостинге: миграции накатываются при старте контейнера,
# на этапе сборки образа базы ещё нет.
render-deploy: migrate render-start

build:
	./build.sh

.PHONY: setup install build-css dev migrate reset-db lint test start render-start render-deploy build
