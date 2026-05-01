from datetime import datetime

from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
from src.models.order import Order, OrderItem
from src.repositories.order_repository import (
    CustomerRepository,
    OrderRepository,
    ProductRepository,
)
from src.schemas.order import OrderCreate, OrderUpdate


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = OrderRepository(db)
        self.customers = CustomerRepository(db)
        self.products = ProductRepository(db)

    def create_order(self, payload: OrderCreate) -> Order:
        if self.repository.get_by_number(payload.order_number):
            raise ConflictError(
                f"Ya existe una orden con número {payload.order_number}"
            )
        if not self.customers.get_by_id(payload.customer_id):
            raise NotFoundError(
                f"Cliente con id {payload.customer_id} no existe"
            )

        items: list[OrderItem] = []
        total = 0.0
        for item in payload.items:
            if not self.products.get_by_id(item.product_id):
                raise NotFoundError(
                    f"Producto con id {item.product_id} no existe"
                )
            items.append(
                OrderItem(
                    product_id=item.product_id,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                )
            )
            total += item.unit_price * item.quantity

        order = Order(
            order_number=payload.order_number,
            order_date=payload.order_date or datetime.utcnow(),
            customer_id=payload.customer_id,
            total_amount=round(total, 2),
            items=items,
        )
        self.repository.create(order)
        return self.repository.get_by_id(order.id)

    def get_order(self, order_id: int) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise NotFoundError(f"Orden con id {order_id} no existe")
        return order

    def list_orders(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return self.repository.list_all(skip=skip, limit=limit)

    def update_order(self, order_id: int, payload: OrderUpdate) -> Order:
        order = self.get_order(order_id)
        data = payload.model_dump(exclude_unset=True)
        if "customer_id" in data and not self.customers.get_by_id(data["customer_id"]):
            raise NotFoundError(
                f"Cliente con id {data['customer_id']} no existe"
            )
        self.repository.update(order, data)
        return self.repository.get_by_id(order_id)

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        self.repository.delete(order)
