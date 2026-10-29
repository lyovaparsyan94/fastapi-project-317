from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(UTC)


class Url(SQLModel, table=True):
    __tablename__ = "urls"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, unique=True)
    created_at: datetime = Field(default_factory=utcnow)
