from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from page_analyzer.settings import settings

engine = create_async_engine(settings.database_url)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
