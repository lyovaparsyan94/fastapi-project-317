# Page Analyzer

## Требования

Python 3.12+, [uv](https://docs.astral.sh/uv/), PostgreSQL 16, GNU Make.

## Настройка

```bash
cp .env.example .env         # DATABASE_URL и SECRET_KEY
docker compose up -d db      # или свой локальный PostgreSQL
make setup                   # uv sync + alembic upgrade head
```

## Команды

| Команда | Что делает |
| --- | --- |
| `make setup` | готовит проект к запуску: зависимости и миграции |
| `make install` | `uv sync` |
| `make dev` | запуск с автоперезагрузкой на `http://127.0.0.1:8000` |
| `make start` | продакшен-запуск, `fastapi run` с четырьмя воркерами |
| `make migrate` | `uv run alembic upgrade head` |
| `make lint` | `uv run ruff check .` |
| `make test` | `uv run pytest -vv` |
| `make build` | `./build.sh` — сборка для деплоя |

Порт переопределяется переменной `PORT`: `make dev PORT=5000`.

## Целиком в Docker

```bash
docker compose up --build
```

Приложение поднимется на `http://localhost:8000` после того, как база пройдёт healthcheck.
