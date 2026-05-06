from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class Settings:
    APP_NAME = "Python Orders API"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "API REST para gestión de órdenes"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")


settings = Settings()
