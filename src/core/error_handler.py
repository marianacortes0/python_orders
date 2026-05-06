from __future__ import annotations
import logging
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions import AppException

logger = logging.getLogger(__name__)


def _body(code: int, error: str, message: str, errors: Optional[list] = None) -> dict:
    out = {"code": code, "error": error, "message": message}
    if errors:
        out["errors"] = errors
    return out


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def _(request: Request, exc: AppException):
        return JSONResponse(content=_body(exc.status_code, type(exc).__name__, exc.detail), status_code=exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def _(request: Request, exc: RequestValidationError):
        errors = [
            {
                "field": ".".join(str(x) for x in e.get("loc", []) if x != "body") or "body",
                "message": e.get("msg", "Dato inválido"),
                "type": e.get("type", "value_error"),
            }
            for e in exc.errors()
        ]
        return JSONResponse(content=_body(400, "ValidationError", "Datos inválidos en la solicitud", errors), status_code=400)

    @app.exception_handler(StarletteHTTPException)
    async def _(request: Request, exc: StarletteHTTPException):
        name = {400: "BadRequestError", 404: "NotFoundError", 409: "ConflictError"}.get(
            exc.status_code, "HTTPException"
        )
        return JSONResponse(content=_body(exc.status_code, name, str(exc.detail)), status_code=exc.status_code)

    @app.exception_handler(Exception)
    async def _(request: Request, exc: Exception):
        logger.exception("Unhandled error: %s", exc)
        return JSONResponse(content=_body(500, "InternalServerError", "Error interno del servidor"), status_code=500)
