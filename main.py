from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import Response

from src.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from src.core.error_handler import register_error_handlers
from src.core.seed import seed_database
from src.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_database()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones de cualquier dominio (Vercel, localhost, etc)rr
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)
app.include_router(router, prefix=settings.API_PREFIX)


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Python Orders API", "docs": "/docs", "version": settings.APP_VERSION}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
