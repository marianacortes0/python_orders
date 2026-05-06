from __future__ import annotations
from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/health", summary="Estado del servicio")
def health():
    return {"status": "ok"}
