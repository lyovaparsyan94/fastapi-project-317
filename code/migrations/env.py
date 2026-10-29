import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

from page_analyzer import models  # noqa: F401  — модели должны быть импортированы для autogenerate
from page_analyzer.settings import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Значения из ini проходят через интерполяцию, поэтому % в пароле нужно экранировать.
config.set_main_option("sqlalchemy.url", settings.database_url.replace("%", "%%"))

target_metadata = SQLModel.metadata


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations() -> None:
    engine = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


asyncio.run(run_migrations())
