from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config import settings
from src.core.database import init_db
from src.core.error_handler import register_error_handlers
from src.core.seed import seed_database
from src.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_database()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

register_error_handlers(app)
app.include_router(router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Bienvenido a Python Orders API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
