from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["System"])


@router.get("/health", summary="Verificar disponibilidad del servicio")
def health():
    return {"status": "ok"}


@router.get("/docs", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")
