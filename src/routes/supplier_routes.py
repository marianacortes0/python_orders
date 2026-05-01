from fastapi import Depends, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.schemas.common import CamelAPIRouter, ErrorResponse, PaginatedResponse
from src.schemas.product import ProductRead
from src.schemas.supplier import SupplierCreate, SupplierRead, SupplierUpdate
from src.services.supplier_service import SupplierService

router = CamelAPIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
    responses={
        400: {"model": ErrorResponse, "description": "Datos inválidos"},
        404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
        500: {"model": ErrorResponse, "description": "Error interno"},
    },
)


def get_service(db: Session = Depends(get_db)) -> SupplierService:
    return SupplierService(db)


@router.get(
    "",
    response_model=PaginatedResponse[SupplierRead],
    summary="Listar proveedores",
)
def list_suppliers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    country: str | None = None,
    search: str | None = None,
    service: SupplierService = Depends(get_service),
):
    items, total = service.list_suppliers(
        page=page, limit=limit, country=country, search=search
    )
    return {"items": items, "page": page, "limit": limit, "total": total}


@router.post(
    "",
    response_model=SupplierRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear proveedor",
)
def create_supplier(
    payload: SupplierCreate, service: SupplierService = Depends(get_service)
):
    return service.create_supplier(payload)


@router.get(
    "/{supplier_id}",
    response_model=SupplierRead,
    summary="Detalle de proveedor",
)
def get_supplier(supplier_id: int, service: SupplierService = Depends(get_service)):
    return service.get_supplier(supplier_id)


@router.patch(
    "/{supplier_id}",
    response_model=SupplierRead,
    summary="Actualizar parcialmente un proveedor",
)
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdate,
    service: SupplierService = Depends(get_service),
):
    return service.update_supplier(supplier_id, payload)


@router.get(
    "/{supplier_id}/products",
    response_model=list[ProductRead],
    summary="Listar productos del proveedor",
)
def list_supplier_products(
    supplier_id: int, service: SupplierService = Depends(get_service)
):
    return service.list_supplier_products(supplier_id)
