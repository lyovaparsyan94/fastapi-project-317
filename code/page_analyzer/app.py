from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Анализатор страниц")


@app.get("/", name="index", response_class=PlainTextResponse)
async def index() -> str:
    return "Анализатор страниц"
