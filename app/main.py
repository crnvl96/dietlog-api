from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api.diet import diet_router


def create_app() -> FastAPI:
    _ = load_dotenv()

    app = FastAPI()
    app.include_router(diet_router)

    static_path = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    return app


app = create_app()
