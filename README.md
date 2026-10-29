# Анализатор страниц

[![hexlet-check](https://github.com/lyovaparsyan94/fastapi-project-317/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lyovaparsyan94/fastapi-project-317/actions)

Веб-приложение на FastAPI, которое проверяет страницы на SEO-пригодность: сохраняет
адреса сайтов, по запросу ходит к ним, записывает код ответа и содержимое тегов
`h1`, `title` и `meta[name=description]`.

**Демо:** ссылка появится после деплоя.

Развёртывание на render.com описано в [code/README.md](code/README.md#деплой).

## Стек

FastAPI · SQLModel · Alembic · PostgreSQL · Jinja2 · Tailwind CSS · uv · ruff

## Запуск

Код проекта лежит в каталоге [`code/`](code/), команды выполняются оттуда:

```bash
cd code
cp .env.example .env
docker compose up -d db
make setup
make dev
```

Подробности — в [code/README.md](code/README.md).
