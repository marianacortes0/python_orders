import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions import AppException

logger = logging.getLogger(__name__)


def _payload(code: int, error: str, message: str, errors: list | None = None) -> dict:
    out: dict = {"code": code, "error": error, "message": message}
    if errors is not None:
        out["errors"] = errors
    return out


def _format_validation_errors(exc: RequestValidationError) -> list[dict]:
    out: list[dict] = []
    for err in exc.errors():
        loc = ".".join(str(x) for x in err.get("loc", []) if x != "body")
        out.append(
            {
                "field": loc or "body",
                "message": err.get("msg", "Dato inválido"),
                "type": err.get("type", "value_error"),
            }
        )
    return out


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload(exc.status_code, exc.__class__.__name__, exc.detail),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content=_payload(
                400,
                "ValidationError",
                "Datos inválidos en la solicitud",
                _format_validation_errors(exc),
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        name = {
            400: "BadRequestError",
            404: "NotFoundError",
            405: "MethodNotAllowed",
            409: "ConflictError",
        }.get(exc.status_code, "HTTPException")
        message = exc.detail if isinstance(exc.detail, str) else "Error en la solicitud"
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload(exc.status_code, name, message),
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.exception("Database error: %s", exc)
        return JSONResponse(
            status_code=500,
            content=_payload(500, "DatabaseError", "Error en la base de datos"),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled error: %s", exc)
        return JSONResponse(
            status_code=500,
            content=_payload(500, "InternalServerError", "Error interno del servidor"),
        )
