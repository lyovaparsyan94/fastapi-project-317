from datetime import UTC, datetime

from sqlmodel import Field, Relationship, SQLModel


def utcnow() -> datetime:
    return datetime.now(UTC)


class Url(SQLModel, table=True):
    __tablename__ = "urls"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, unique=True)
    created_at: datetime = Field(default_factory=utcnow)

    checks: list["UrlCheck"] = Relationship(
        back_populates="url",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "desc(UrlCheck.id)"},
    )


class UrlCheck(SQLModel, table=True):
    __tablename__ = "url_checks"

    id: int | None = Field(default=None, primary_key=True)
    url_id: int = Field(foreign_key="urls.id", ondelete="CASCADE")
    status_code: int | None = None
    h1: str | None = None
    title: str | None = None
    description: str | None = None
    created_at: datetime = Field(default_factory=utcnow)

    url: Url | None = Relationship(back_populates="checks")
