from datetime import datetime

from fastapi import Depends, Query, status

from src.models.order import OrderStatus
from src.schemas.common import CamelAPIRouter, ErrorResponse, PaginatedResponse
from src.schemas.order import OrderCreate, OrderItemAdd, OrderItemRead, OrderItemUpdate, OrderRead, OrderReplace, OrderUpdate
from src.services.order_service import OrderService

router = CamelAPIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)


def svc() -> OrderService:
    return OrderService()


@router.get("", response_model=PaginatedResponse[OrderRead], summary="Listar pedidos")
def list_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    customer_id: int | None = Query(None, alias="customerId"),
    date_from: datetime | None = Query(None, alias="dateFrom"),
    date_to: datetime | None = Query(None, alias="dateTo"),
    status_filter: OrderStatus | None = Query(None, alias="status"),
    sort: str | None = None,
    service: OrderService = Depends(svc),
):
    items, total = service.list(page, limit, customer_id, date_from, date_to, status_filter, sort)
    return {"items": items, "page": page, "limit": limit, "total": total}


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED, summary="Crear pedido")
def create_order(payload: OrderCreate, service: OrderService = Depends(svc)):
    return service.create(payload)


@router.get("/{order_id}", response_model=OrderRead, summary="Detalle de pedido")
def get_order(order_id: int, service: OrderService = Depends(svc)):
    return service.get(order_id)


@router.put("/{order_id}", response_model=OrderRead, summary="Reemplazar pedido")
def replace_order(order_id: int, payload: OrderReplace, service: OrderService = Depends(svc)):
    return service.replace(order_id, payload)


@router.patch("/{order_id}", response_model=OrderRead, summary="Actualizar pedido")
def update_order(order_id: int, payload: OrderUpdate, service: OrderService = Depends(svc)):
    return service.update(order_id, payload)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar pedido")
def delete_order(order_id: int, service: OrderService = Depends(svc)):
    service.delete(order_id)


@router.get("/{order_id}/items", response_model=list[OrderItemRead], summary="Listar items")
def list_items(order_id: int, service: OrderService = Depends(svc)):
    return service.list_items(order_id)


@router.post("/{order_id}/items", response_model=OrderItemRead, status_code=status.HTTP_201_CREATED, summary="Agregar item")
def add_item(order_id: int, payload: OrderItemAdd, service: OrderService = Depends(svc)):
    return service.add_item(order_id, payload)


@router.patch("/{order_id}/items/{item_id}", response_model=OrderItemRead, summary="Actualizar item")
def update_item(order_id: int, item_id: int, payload: OrderItemUpdate, service: OrderService = Depends(svc)):
    return service.update_item(order_id, item_id, payload)


@router.delete("/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar item")
def delete_item(order_id: int, item_id: int, service: OrderService = Depends(svc)):
    service.delete_item(order_id, item_id)
