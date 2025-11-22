from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# Racine du projet (D:/artdle)
ROOT_DIR = Path(__file__).resolve().parents[3]

# Dossier env (D:/artdle/env)
ENV_DIR = ROOT_DIR / "env"

# Nom du fichier env à utiliser (par défaut: .env_dev)
ENV_FILE_NAME = os.getenv("APP_ENV_FILE", ".env.dev")


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=ENV_DIR / ENV_FILE_NAME,
        env_file_encoding="utf-8",
    )


settings = Settings()
