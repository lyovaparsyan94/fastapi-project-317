# Анализатор страниц

[![hexlet-check](https://github.com/lyovaparsyan94/fastapi-project-317/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lyovaparsyan94/fastapi-project-317/actions)

Веб-приложение на FastAPI, которое проверяет страницы на SEO-пригодность: сохраняет
адреса сайтов, по запросу ходит к ним, записывает код ответа и содержимое тегов
`h1`, `title` и `meta[name=description]`.

**Демо:** ссылка появится после деплоя.

## Стек

FastAPI · SQLModel · Alembic · PostgreSQL · Jinja2 · Tailwind CSS · uv · ruff

## Требования

Python 3.12+, [uv](https://docs.astral.sh/uv/), Node.js 20+ (сборка стилей),
PostgreSQL 16, GNU Make.

## Настройка

```bash
cp .env.example .env         # DATABASE_URL и SECRET_KEY
docker compose up -d db      # или свой локальный PostgreSQL
make setup                   # зависимости, сборка стилей, миграции
make dev                     # http://127.0.0.1:8000
```

## Команды

| Команда | Что делает |
| --- | --- |
| `make setup` | готовит проект к запуску: зависимости, стили и миграции |
| `make install` | `uv sync` + `npm ci` |
| `make build-css` | собирает `page_analyzer/static/css/main.css` из Tailwind |
| `make dev` | `uv run fastapi dev` с автоперезагрузкой на `http://127.0.0.1:8000` |
| `make start` | продакшен-запуск, `fastapi run` с четырьмя воркерами |
| `make migrate` | `uv run alembic upgrade head` — применяет миграции |
| `make reset-db` | откатывает миграции до нуля и накатывает заново |
| `make lint` | `uv run ruff check .` |
| `make test` | `uv run pytest -vv` |
| `make build` | `./build.sh` — сборка для деплоя |

Порт переопределяется переменной `PORT`: `make dev PORT=5000`.

`make test` очищает таблицы базы, на которую указывает `DATABASE_URL`. Для локальной
разработки держите отдельную базу под тесты, иначе прогон сотрёт ваши данные.

## Целиком в Docker

```bash
docker compose up --build
```

Приложение поднимется на `http://localhost:8000` после того, как база пройдёт healthcheck.

## Деплой

Проект разворачивается на render.com.

В корне есть `Dockerfile`, поэтому Render определяет рантайм как **Docker**. В настройках
сервиса достаточно одного поля:

| Поле | Значение |
| --- | --- |
| Docker Command | `make render-deploy` |
| `DATABASE_URL` | строка подключения созданной базы |
| `SECRET_KEY` | любая случайная строка |

`render-deploy` накатывает миграции и запускает сервер: при сборке образа база ещё
недоступна, поэтому миграции идут при старте контейнера. Порт Render передаёт
переменной `PORT`, Makefile её подхватывает.

Число воркеров берётся из `WEB_CONCURRENCY`, которую Render выставляет по размеру
инстанса, а без неё по умолчанию равно пяти. На free-тарифе с 512 МБ пять воркеров
не помещаются в память и их убивает OOM. Переопределить можно переменной `WORKERS`.

Для нативного Python-рантайма (его выбирает `render.yaml` в корне, вариант через
Blueprints) значения другие: Build Command — `make build`, Start Command —
`make render-start`. В этом случае миграции выполняет `build.sh` на этапе сборки,
а `render-start` запускается без `uv run`, чтобы использовать интерпретатор Render.
