import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Python Orders API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API REST para gestión de órdenes"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./orders.db")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


settings = Settings()
