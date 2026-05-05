from fastapi import Depends, Query, status

from src.schemas.common import CamelAPIRouter, ErrorResponse, PaginatedResponse
from src.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from src.schemas.order import OrderRead
from src.services.customer_service import CustomerService

router = CamelAPIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)


def svc() -> CustomerService:
    return CustomerService()


@router.get("", response_model=PaginatedResponse[CustomerRead], summary="Listar clientes")
def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    country: str | None = None,
    city: str | None = None,
    search: str | None = None,
    service: CustomerService = Depends(svc),
):
    items, total = service.list(page, limit, country, city, search)
    return {"items": items, "page": page, "limit": limit, "total": total}


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED, summary="Crear cliente")
def create_customer(payload: CustomerCreate, service: CustomerService = Depends(svc)):
    return service.create(payload)


@router.get("/{customer_id}", response_model=CustomerRead, summary="Detalle de cliente")
def get_customer(customer_id: int, service: CustomerService = Depends(svc)):
    return service.get(customer_id)


@router.patch("/{customer_id}", response_model=CustomerRead, summary="Actualizar cliente (parcial)")
@router.put("/{customer_id}", response_model=CustomerRead, summary="Actualizar cliente (completo)")
def update_customer(customer_id: int, payload: CustomerUpdate, service: CustomerService = Depends(svc)):
    return service.update(customer_id, payload)


@router.delete("/{customer_id}", status_code=status.HTTP_200_OK, summary="Eliminar cliente")
def delete_customer(customer_id: int, service: CustomerService = Depends(svc)):
    service.delete(customer_id)
    return {"message": "eliminado exitosamente"}


@router.get("/{customer_id}/orders", response_model=list[OrderRead], summary="Pedidos del cliente")
def list_customer_orders(customer_id: int, service: CustomerService = Depends(svc)):
    return service.list_orders(customer_id)
