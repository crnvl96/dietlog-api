from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.diet import diet_router

static_dir = Path(__file__).parent / "static"


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(diet_router)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    return app


app = create_app()
