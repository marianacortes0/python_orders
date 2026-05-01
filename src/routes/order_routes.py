from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.schemas.order import ErrorResponse, OrderCreate, OrderRead, OrderUpdate
from src.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={
        404: {"model": ErrorResponse, "description": "Orden no encontrada"},
        409: {"model": ErrorResponse, "description": "Conflicto"},
        422: {"model": ErrorResponse, "description": "Datos inválidos"},
    },
)


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db)


@router.post(
    "",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva orden",
)
def create_order(
    payload: OrderCreate,
    service: OrderService = Depends(get_order_service),
):
    return service.create_order(payload)


@router.get(
    "",
    response_model=list[OrderRead],
    summary="Listar órdenes",
)
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: OrderService = Depends(get_order_service),
):
    return service.list_orders(skip=skip, limit=limit)


@router.get(
    "/{order_id}",
    response_model=OrderRead,
    summary="Obtener una orden por id",
)
def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    return service.get_order(order_id)


@router.patch(
    "/{order_id}",
    response_model=OrderRead,
    summary="Actualizar una orden",
)
def update_order(
    order_id: int,
    payload: OrderUpdate,
    service: OrderService = Depends(get_order_service),
):
    return service.update_order(order_id, payload)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una orden",
)
def delete_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    service.delete_order(order_id)
    return None
