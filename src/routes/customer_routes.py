from fastapi import Depends, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.schemas.common import CamelAPIRouter, ErrorResponse, PaginatedResponse
from src.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from src.schemas.order import OrderRead
from src.services.customer_service import CustomerService

router = CamelAPIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={
        400: {"model": ErrorResponse, "description": "Datos inválidos"},
        404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
        500: {"model": ErrorResponse, "description": "Error interno"},
    },
)


def get_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(db)


@router.get(
    "",
    response_model=PaginatedResponse[CustomerRead],
    summary="Listar clientes",
)
def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    country: str | None = None,
    city: str | None = None,
    search: str | None = None,
    service: CustomerService = Depends(get_service),
):
    items, total = service.list_customers(
        page=page, limit=limit, country=country, city=city, search=search
    )
    return {"items": items, "page": page, "limit": limit, "total": total}


@router.post(
    "",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear cliente",
)
def create_customer(
    payload: CustomerCreate, service: CustomerService = Depends(get_service)
):
    return service.create_customer(payload)


@router.get(
    "/{customer_id}",
    response_model=CustomerRead,
    summary="Detalle de cliente",
)
def get_customer(customer_id: int, service: CustomerService = Depends(get_service)):
    return service.get_customer(customer_id)


@router.patch(
    "/{customer_id}",
    response_model=CustomerRead,
    summary="Actualizar parcialmente un cliente",
)
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    service: CustomerService = Depends(get_service),
):
    return service.update_customer(customer_id, payload)


@router.get(
    "/{customer_id}/orders",
    response_model=list[OrderRead],
    summary="Listar pedidos asociados al cliente",
)
def list_customer_orders(
    customer_id: int, service: CustomerService = Depends(get_service)
):
    return service.list_customer_orders(customer_id)
