from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: SecretStr = SecretStr(secret_value="")
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def load_env():
    return Settings()
