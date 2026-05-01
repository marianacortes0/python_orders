from fastapi import Depends, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.schemas.common import CamelAPIRouter, ErrorResponse, PaginatedResponse
from src.schemas.product import ProductCreate, ProductRead, ProductReplace, ProductUpdate
from src.services.product_service import ProductService

router = CamelAPIRouter(
    prefix="/products",
    tags=["Products"],
    responses={
        400: {"model": ErrorResponse, "description": "Datos inválidos"},
        404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
        409: {"model": ErrorResponse, "description": "Conflicto"},
        500: {"model": ErrorResponse, "description": "Error interno"},
    },
)


def get_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.get(
    "",
    response_model=PaginatedResponse[ProductRead],
    summary="Listar productos",
)
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    supplier_id: int | None = Query(None, alias="supplierId"),
    search: str | None = None,
    discontinued: bool | None = None,
    service: ProductService = Depends(get_service),
):
    items, total = service.list_products(
        page=page,
        limit=limit,
        supplier_id=supplier_id,
        search=search,
        discontinued=discontinued,
    )
    return {"items": items, "page": page, "limit": limit, "total": total}


@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto",
)
def create_product(
    payload: ProductCreate, service: ProductService = Depends(get_service)
):
    return service.create_product(payload)


@router.get(
    "/{product_id}",
    response_model=ProductRead,
    summary="Detalle de producto con proveedor",
)
def get_product(product_id: int, service: ProductService = Depends(get_service)):
    return service.get_product(product_id)


@router.put(
    "/{product_id}",
    response_model=ProductRead,
    summary="Reemplazar producto",
)
def replace_product(
    product_id: int,
    payload: ProductReplace,
    service: ProductService = Depends(get_service),
):
    return service.replace_product(product_id, payload)


@router.patch(
    "/{product_id}",
    response_model=ProductRead,
    summary="Actualizar parcialmente producto",
)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    service: ProductService = Depends(get_service),
):
    return service.update_product(product_id, payload)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar o descontinuar producto",
)
def delete_product(product_id: int, service: ProductService = Depends(get_service)):
    service.delete_product(product_id)
    return None
