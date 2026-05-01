from datetime import datetime

from fastapi import Depends, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.order import OrderStatus
from src.schemas.common import CamelAPIRouter, ErrorResponse, PaginatedResponse
from src.schemas.order import (
    OrderCreate,
    OrderItemAdd,
    OrderItemRead,
    OrderItemUpdate,
    OrderRead,
    OrderReplace,
    OrderUpdate,
)
from src.services.order_service import OrderService

router = CamelAPIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={
        400: {"model": ErrorResponse, "description": "Datos inválidos"},
        404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
        409: {"model": ErrorResponse, "description": "Conflicto"},
        500: {"model": ErrorResponse, "description": "Error interno"},
    },
)


def get_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db)


@router.get("", response_model=PaginatedResponse[OrderRead], summary="Listar pedidos")
def list_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    customer_id: int | None = Query(None, alias="customerId"),
    date_from: datetime | None = Query(None, alias="dateFrom"),
    date_to: datetime | None = Query(None, alias="dateTo"),
    status_filter: OrderStatus | None = Query(None, alias="status"),
    sort: str | None = Query(None, description="Ej: orderDate:desc"),
    service: OrderService = Depends(get_service),
):
    items, total = service.list_orders(
        page=page,
        limit=limit,
        customer_id=customer_id,
        date_from=date_from,
        date_to=date_to,
        status=status_filter,
        sort=sort,
    )
    return {"items": items, "page": page, "limit": limit, "total": total}


@router.post(
    "",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un pedido",
)
def create_order(payload: OrderCreate, service: OrderService = Depends(get_service)):
    return service.create_order(payload)


@router.get("/{order_id}", response_model=OrderRead, summary="Detalle de pedido")
def get_order(order_id: int, service: OrderService = Depends(get_service)):
    return service.get_order(order_id)


@router.put(
    "/{order_id}",
    response_model=OrderRead,
    summary="Reemplazar completamente un pedido",
)
def replace_order(
    order_id: int,
    payload: OrderReplace,
    service: OrderService = Depends(get_service),
):
    return service.replace_order(order_id, payload)


@router.patch(
    "/{order_id}",
    response_model=OrderRead,
    summary="Actualizar parcialmente un pedido",
)
def update_order(
    order_id: int,
    payload: OrderUpdate,
    service: OrderService = Depends(get_service),
):
    return service.update_order(order_id, payload)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar o anular un pedido",
)
def delete_order(order_id: int, service: OrderService = Depends(get_service)):
    service.delete_order(order_id)
    return None


@router.get(
    "/{order_id}/items",
    response_model=list[OrderItemRead],
    summary="Listar items del pedido",
)
def list_items(order_id: int, service: OrderService = Depends(get_service)):
    return service.list_items(order_id)


@router.post(
    "/{order_id}/items",
    response_model=OrderItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar item al pedido",
)
def add_item(
    order_id: int,
    payload: OrderItemAdd,
    service: OrderService = Depends(get_service),
):
    return service.add_item(order_id, payload)


@router.patch(
    "/{order_id}/items/{item_id}",
    response_model=OrderItemRead,
    summary="Actualizar item del pedido",
)
def update_item(
    order_id: int,
    item_id: int,
    payload: OrderItemUpdate,
    service: OrderService = Depends(get_service),
):
    return service.update_item(order_id, item_id, payload)


@router.delete(
    "/{order_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar item del pedido",
)
def delete_item(
    order_id: int,
    item_id: int,
    service: OrderService = Depends(get_service),
):
    service.delete_item(order_id, item_id)
    return None
