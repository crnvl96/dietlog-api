from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = Field(default="")
    model_config = SettingsConfigDict(env_file=".env")  # pyright: ignore[reportUnannotatedClassAttribute]


@lru_cache
def load_env():
    return Settings()
