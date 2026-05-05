from fastapi import Depends, Query, status

from src.schemas.common import CamelAPIRouter, ErrorResponse, PaginatedResponse
from src.schemas.product import ProductRead
from src.schemas.supplier import SupplierCreate, SupplierRead, SupplierUpdate
from src.services.supplier_service import SupplierService

router = CamelAPIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)


def svc() -> SupplierService:
    return SupplierService()


@router.get("", response_model=PaginatedResponse[SupplierRead], summary="Listar proveedores")
def list_suppliers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    country: str | None = None,
    search: str | None = None,
    service: SupplierService = Depends(svc),
):
    items, total = service.list(page, limit, country, search)
    return {"items": items, "page": page, "limit": limit, "total": total}


@router.post("", response_model=SupplierRead, status_code=status.HTTP_201_CREATED, summary="Crear proveedor")
def create_supplier(payload: SupplierCreate, service: SupplierService = Depends(svc)):
    return service.create(payload)


@router.get("/{supplier_id}", response_model=SupplierRead, summary="Detalle de proveedor")
def get_supplier(supplier_id: int, service: SupplierService = Depends(svc)):
    return service.get(supplier_id)


@router.patch("/{supplier_id}", response_model=SupplierRead, summary="Actualizar proveedor (parcial)")
@router.put("/{supplier_id}", response_model=SupplierRead, summary="Actualizar proveedor (completo)")
def update_supplier(supplier_id: int, payload: SupplierUpdate, service: SupplierService = Depends(svc)):
    return service.update(supplier_id, payload)


@router.delete("/{supplier_id}", status_code=status.HTTP_200_OK, summary="Eliminar proveedor")
def delete_supplier(supplier_id: int, service: SupplierService = Depends(svc)):
    service.delete(supplier_id)
    return {"message": "eliminado exitosamente"}


@router.get("/{supplier_id}/products", response_model=list[ProductRead], summary="Productos del proveedor")
def list_supplier_products(supplier_id: int, service: SupplierService = Depends(svc)):
    return service.list_products(supplier_id)
