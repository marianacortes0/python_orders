from __future__ import annotations
from datetime import datetime
from typing import List, Tuple

from src.core.exceptions import BadRequestError, ConflictError, NotFoundError
from src.core.store import store
from src.models.order import Order, OrderItem, OrderStatus
from src.repositories.order_repository import CustomerRepository, OrderRepository, ProductRepository
from src.schemas.order import OrderCreate, OrderItemAdd, OrderItemUpdate, OrderReplace, OrderUpdate


def _gen_number() -> str:
    return f"ORD-{1000 + store.next_id(store.orders)}"


class OrderService:
    def __init__(self):
        self.repo = OrderRepository()
        self.customers = CustomerRepository()
        self.products = ProductRepository()

    def _require_product(self, product_id: int):
        p = self.products.get(product_id)
        if p is None:
            raise NotFoundError(f"Producto {product_id} no existe")
        if p.is_discontinued:
            raise BadRequestError(f"Producto {product_id} está descontinuado")
        return p

    def _price(self, item: OrderItemAdd) -> float:
        return item.unit_price if item.unit_price is not None else self._require_product(item.product_id).unit_price

    def _build_items(self, payload: List[OrderItemAdd]) -> Tuple[List[OrderItem], float]:
        items, total = [], 0.0
        for it in payload:
            self._require_product(it.product_id)
            price = self._price(it)
            items.append(OrderItem(id=0, order_id=0, product_id=it.product_id, unit_price=price, quantity=it.quantity))
            total += price * it.quantity
        return items, round(total, 2)

    def list(self, page, limit, customer_id, date_from, date_to, status, sort):
        return self.repo.list(page=page, limit=limit, customer_id=customer_id,
                              date_from=date_from, date_to=date_to, status=status, sort=sort)

    def get(self, order_id: int) -> Order:
        o = self.repo.get(order_id)
        if o is None:
            raise NotFoundError(f"Orden {order_id} no existe")
        return o

    def create(self, payload: OrderCreate) -> Order:
        if payload.order_number and self.repo.get_by_number(payload.order_number):
            raise ConflictError(f"Ya existe la orden {payload.order_number}")
        if not self.customers.get(payload.customer_id):
            raise NotFoundError(f"Cliente {payload.customer_id} no existe")
        items, total = self._build_items(payload.items)
        return self.repo.create(Order(
            id=0,
            order_number=payload.order_number or _gen_number(),
            order_date=payload.order_date or datetime.utcnow(),
            customer_id=payload.customer_id,
            total_amount=total,
            status=OrderStatus.PENDING,
            items=items,
        ))

    def replace(self, order_id: int, payload: OrderReplace) -> Order:
        order = self.get(order_id)
        if not self.customers.get(payload.customer_id):
            raise NotFoundError(f"Cliente {payload.customer_id} no existe")
        existing = self.repo.get_by_number(payload.order_number)
        if existing and existing.id != order_id:
            raise ConflictError(f"Ya existe la orden {payload.order_number}")
        items, total = self._build_items(payload.items)
        self.repo.update(order, {"order_number": payload.order_number, "order_date": payload.order_date,
                                  "customer_id": payload.customer_id, "status": payload.status, "total_amount": total})
        self.repo.replace_items(order, items)
        return self.repo.get(order_id)

    def update(self, order_id: int, payload: OrderUpdate) -> Order:
        order = self.get(order_id)
        data = payload.model_dump(exclude_unset=True)
        if "customer_id" in data and not self.customers.get(data["customer_id"]):
            raise NotFoundError(f"Cliente {data['customer_id']} no existe")
        self.repo.update(order, data)
        return self.repo.get(order_id)

    def delete(self, order_id: int) -> None:
        order = self.get(order_id)
        if order.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise ConflictError("No se puede eliminar una orden enviada o entregada")
        self.repo.delete(order)

    def list_items(self, order_id: int) -> List[OrderItem]:
        self.get(order_id)
        return self.repo.list_items(order_id)

    def add_item(self, order_id: int, payload: OrderItemAdd) -> OrderItem:
        order = self.get(order_id)
        if order.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELLED):
            raise BadRequestError("No se pueden agregar items en este estado")
        self._require_product(payload.product_id)
        added = self.repo.add_item(
            OrderItem(id=0, order_id=order_id, product_id=payload.product_id,
                      unit_price=self._price(payload), quantity=payload.quantity)
        )
        self.repo.recalculate_total(order_id)
        return self.repo.get_item(order_id, added.id)

    def update_item(self, order_id: int, item_id: int, payload: OrderItemUpdate) -> OrderItem:
        self.get(order_id)
        if not self.repo.get_item(order_id, item_id):
            raise NotFoundError(f"Item {item_id} no existe en la orden {order_id}")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise BadRequestError("Debe especificar quantity o unitPrice")
        self.repo.update_item(item_id, data)
        self.repo.recalculate_total(order_id)
        return self.repo.get_item(order_id, item_id)

    def delete_item(self, order_id: int, item_id: int) -> None:
        self.get(order_id)
        item = self.repo.get_item(order_id, item_id)
        if not item:
            raise NotFoundError(f"Item {item_id} no existe en la orden {order_id}")
        self.repo.delete_item(item)
        self.repo.recalculate_total(order_id)
