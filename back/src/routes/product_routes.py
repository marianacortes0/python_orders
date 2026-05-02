from fastapi import Depends, Query, status

from src.schemas.common import CamelAPIRouter, ErrorResponse, PaginatedResponse
from src.schemas.product import ProductCreate, ProductRead, ProductReplace, ProductUpdate
from src.services.product_service import ProductService

router = CamelAPIRouter(
    prefix="/products",
    tags=["Products"],
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse},
               409: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)


def svc() -> ProductService:
    return ProductService()


@router.get("", response_model=PaginatedResponse[ProductRead], summary="Listar productos")
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    supplier_id: int | None = Query(None, alias="supplierId"),
    search: str | None = None,
    discontinued: bool | None = None,
    service: ProductService = Depends(svc),
):
    items, total = service.list(page, limit, supplier_id, search, discontinued)
    return {"items": items, "page": page, "limit": limit, "total": total}


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED, summary="Crear producto")
def create_product(payload: ProductCreate, service: ProductService = Depends(svc)):
    return service.create(payload)


@router.get("/{product_id}", response_model=ProductRead, summary="Detalle de producto")
def get_product(product_id: int, service: ProductService = Depends(svc)):
    return service.get(product_id)


@router.put("/{product_id}", response_model=ProductRead, summary="Reemplazar producto")
def replace_product(product_id: int, payload: ProductReplace, service: ProductService = Depends(svc)):
    return service.replace(product_id, payload)


@router.patch("/{product_id}", response_model=ProductRead, summary="Actualizar producto")
def update_product(product_id: int, payload: ProductUpdate, service: ProductService = Depends(svc)):
    return service.update(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar producto")
def delete_product(product_id: int, service: ProductService = Depends(svc)):
    service.delete(product_id)
