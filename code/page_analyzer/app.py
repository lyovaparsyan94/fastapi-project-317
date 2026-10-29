from pathlib import Path
from typing import Annotated

import httpx
from fastapi import FastAPI, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import selectinload
from sqlmodel import col, func, select
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_302_FOUND, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_CONTENT

from page_analyzer.db import SessionDep
from page_analyzer.flash import flash, get_flashed_messages
from page_analyzer.models import Url, UrlCheck
from page_analyzer.settings import settings
from page_analyzer.urls import is_valid_url, normalize_url

BASE_DIR = Path(__file__).parent
REQUEST_TIMEOUT = 5

app = FastAPI(title="Анализатор страниц")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages


@app.get("/", name="index", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.post("/urls", name="urls_create")
async def urls_create(
    request: Request,
    session: SessionDep,
    url: Annotated[str, Form()] = "",
) -> Response:
    if not is_valid_url(url):
        flash(request, "Некорректный URL", "danger")
        return templates.TemplateResponse(
            request,
            "index.html",
            {"url": url},
            status_code=HTTP_422_UNPROCESSABLE_CONTENT,
        )

    name = normalize_url(url)
    existing = await session.scalar(select(Url).where(Url.name == name))
    if existing is not None:
        flash(request, "Страница уже существует", "warning")
        return _redirect_to_url(request, existing.id)

    created = Url(name=name)
    session.add(created)
    await session.commit()
    await session.refresh(created)
    flash(request, "Страница успешно добавлена")
    return _redirect_to_url(request, created.id)


@app.get("/urls", name="urls_index", response_class=HTMLResponse)
async def urls_index(request: Request, session: SessionDep) -> HTMLResponse:
    last_check_id = (
        select(func.max(col(UrlCheck.id)))
        .where(col(UrlCheck.url_id) == col(Url.id))
        .correlate(Url)
        .scalar_subquery()
    )
    statement = (
        select(Url, UrlCheck)
        .outerjoin(UrlCheck, col(UrlCheck.id) == last_check_id)
        .order_by(col(Url.id).desc())
    )
    rows = (await session.execute(statement)).all()
    return templates.TemplateResponse(request, "urls.html", {"rows": rows})


@app.get("/urls/{id}", name="url_show", response_class=HTMLResponse)
async def url_show(request: Request, session: SessionDep, id: int) -> HTMLResponse:
    statement = select(Url).where(col(Url.id) == id).options(selectinload(Url.checks))
    url = await session.scalar(statement)
    if url is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    return templates.TemplateResponse(request, "url.html", {"url": url})


@app.post("/urls/{id}/checks", name="url_checks_create")
async def url_checks_create(request: Request, session: SessionDep, id: int) -> Response:
    url = await session.get(Url, id)
    if url is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(url.name)
            response.raise_for_status()
    except httpx.HTTPError:
        flash(request, "Произошла ошибка при проверке", "danger")
        return _redirect_to_url(request, id)

    session.add(UrlCheck(url_id=id, status_code=response.status_code))
    await session.commit()
    flash(request, "Страница успешно проверена")
    return _redirect_to_url(request, id)


def _redirect_to_url(request: Request, id: int) -> RedirectResponse:
    return RedirectResponse(request.url_for("url_show", id=id), status_code=HTTP_302_FOUND)
