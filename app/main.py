from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api.diet import diet_router


class DietLogApp:
    def __init__(self) -> None:
        self.static_folder: str = "static"
        self.app: FastAPI = FastAPI()

    def _load_env(self) -> None:
        _ = load_dotenv()

    def _setup_routes(self) -> None:
        self.app.include_router(diet_router)

    def _setup_static_files(self) -> None:
        static_path: Path = Path(__file__).parent / self.static_folder
        self.app.mount(f"/{self.static_folder}", StaticFiles(directory=static_path), name=self.static_folder)

    def bootstrap(self) -> FastAPI:
        self._load_env()
        self._setup_routes()
        self._setup_static_files()

        return self.app


app = DietLogApp().bootstrap()
