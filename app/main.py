"""DietLogApp API entry point.

This module initializes and configures the FastAPI application for the DietLogApp.
It sets up environment variables, API routes, and static file serving.
"""

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api.diet import diet_router


class DietLogApp:
    """Main application class for DietLogApp.

    This class handles the initialization and configuration of the FastAPI application,
    including environment setup, route configuration, and static file serving.

    Attributes
    ----------
    static_folder : str
        The name of the folder containing static files.
    app : FastAPI
        The FastAPI application instance.

    """

    def __init__(self) -> None:
        """Initialize the DietLogApp instance.

        Sets up the static folder path and creates a new FastAPI application instance.
        """
        self.static_folder: str = "static"
        self.app: FastAPI = FastAPI()

    def _load_env(self) -> None:
        """Load environment variables from .env file.

        Uses python-dotenv to load environment variables from a .env file
        in the project root directory.
        """
        _ = load_dotenv()

    def _setup_routes(self) -> None:
        """Configure API routes.

        Registers all API routers with the FastAPI application.
        Currently includes the diet-related routes.
        """
        self.app.include_router(diet_router)

    def _setup_static_files(self) -> None:
        """Configure static file serving.

        Sets up static file serving from the specified static folder.
        The static files are mounted at '/static' endpoint.
        """
        static_path: Path = Path(__file__).parent / self.static_folder
        self.app.mount(f"/{self.static_folder}", StaticFiles(directory=static_path), name=self.static_folder)

    def bootstrap(self) -> FastAPI:
        """Initialize and configure the application.

        Performs all necessary setup steps including:
        - Loading environment variables
        - Setting up API routes
        - Configuring static file serving

        Returns
        -------
        FastAPI
            The fully configured FastAPI application instance ready for use.

        """
        self._load_env()
        self._setup_routes()
        self._setup_static_files()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["POST", "OPTIONS"],
            allow_headers=["*"],
        )

        return self.app


app = DietLogApp().bootstrap()
