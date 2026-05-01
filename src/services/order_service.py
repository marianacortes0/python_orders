from datetime import datetime

from sqlalchemy.orm import Session

from src.core.exceptions import BadRequestError, ConflictError, NotFoundError
from src.models.order import Order, OrderItem, OrderStatus
from src.repositories.order_repository import (
    CustomerRepository,
    OrderRepository,
    ProductRepository,
)
from src.schemas.order import (
    OrderCreate,
    OrderItemAdd,
    OrderItemUpdate,
    OrderReplace,
    OrderUpdate,
)


def _generate_order_number(db: Session) -> str:
    last = db.query(Order).order_by(Order.id.desc()).first()
    next_id = (last.id if last else 0) + 1
    return f"ORD-{1000 + next_id}"


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = OrderRepository(db)
        self.customers = CustomerRepository(db)
        self.products = ProductRepository(db)

    def _validate_product(self, product_id: int):
        product = self.products.get_by_id(product_id)
        if product is None:
            raise NotFoundError(f"Producto con id {product_id} no existe")
        if product.is_discontinued:
            raise BadRequestError(
                f"Producto con id {product_id} está descontinuado"
            )
        return product

    def _resolve_unit_price(self, item: OrderItemAdd) -> float:
        if item.unit_price is not None:
            return item.unit_price
        return self._validate_product(item.product_id).unit_price

    def _build_items(self, items_payload: list[OrderItemAdd]) -> tuple[list[OrderItem], float]:
        items: list[OrderItem] = []
        total = 0.0
        for it in items_payload:
            self._validate_product(it.product_id)
            unit_price = self._resolve_unit_price(it)
            items.append(
                OrderItem(
                    product_id=it.product_id,
                    unit_price=unit_price,
                    quantity=it.quantity,
                )
            )
            total += unit_price * it.quantity
        return items, round(total, 2)

    def _recalculate_total(self, order: Order) -> None:
        total = sum(it.unit_price * it.quantity for it in order.items)
        order.total_amount = round(total, 2)
        self.db.commit()
        self.db.refresh(order)

    def create_order(self, payload: OrderCreate) -> Order:
        if payload.order_number and self.repository.get_by_number(payload.order_number):
            raise ConflictError(
                f"Ya existe una orden con número {payload.order_number}"
            )
        if not self.customers.get_by_id(payload.customer_id):
            raise NotFoundError(f"Cliente con id {payload.customer_id} no existe")

        items, total = self._build_items(payload.items)

        order = Order(
            order_number=payload.order_number or _generate_order_number(self.db),
            order_date=payload.order_date or datetime.utcnow(),
            customer_id=payload.customer_id,
            total_amount=total,
            status=OrderStatus.PENDING,
            items=items,
        )
        self.repository.create(order)
        return self.repository.get_by_id(order.id)

    def get_order(self, order_id: int) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise NotFoundError(f"Orden con id {order_id} no existe")
        return order

    def list_orders(
        self,
        page: int,
        limit: int,
        customer_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        status: OrderStatus | None = None,
        sort: str | None = None,
    ) -> tuple[list[Order], int]:
        return self.repository.query(
            page=page,
            limit=limit,
            customer_id=customer_id,
            date_from=date_from,
            date_to=date_to,
            status=status,
            sort=sort,
        )

    def replace_order(self, order_id: int, payload: OrderReplace) -> Order:
        order = self.get_order(order_id)
        if not self.customers.get_by_id(payload.customer_id):
            raise NotFoundError(f"Cliente con id {payload.customer_id} no existe")
        existing = self.repository.get_by_number(payload.order_number)
        if existing and existing.id != order_id:
            raise ConflictError(
                f"Ya existe otra orden con número {payload.order_number}"
            )

        items, total = self._build_items(payload.items)
        order.order_number = payload.order_number
        order.order_date = payload.order_date
        order.customer_id = payload.customer_id
        order.status = payload.status
        order.total_amount = total
        self.repository.replace_items(order, items)
        self.db.commit()
        return self.repository.get_by_id(order_id)

    def update_order(self, order_id: int, payload: OrderUpdate) -> Order:
        order = self.get_order(order_id)
        data = payload.model_dump(exclude_unset=True)
        if "customer_id" in data and not self.customers.get_by_id(data["customer_id"]):
            raise NotFoundError(f"Cliente con id {data['customer_id']} no existe")
        self.repository.update(order, data)
        return self.repository.get_by_id(order_id)

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        if order.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise ConflictError(
                "No se puede eliminar una orden enviada o entregada"
            )
        self.repository.delete(order)

    def list_items(self, order_id: int) -> list[OrderItem]:
        self.get_order(order_id)
        return self.repository.list_items(order_id)

    def add_item(self, order_id: int, payload: OrderItemAdd) -> OrderItem:
        order = self.get_order(order_id)
        if order.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELLED):
            raise BadRequestError(
                "No se pueden agregar items a una orden en este estado"
            )
        self._validate_product(payload.product_id)
        unit_price = self._resolve_unit_price(payload)
        item = OrderItem(
            order_id=order_id,
            product_id=payload.product_id,
            unit_price=unit_price,
            quantity=payload.quantity,
        )
        self.repository.add_item(item)
        order = self.repository.get_by_id(order_id)
        self._recalculate_total(order)
        return self.repository.get_item(order_id, item.id)

    def update_item(
        self, order_id: int, item_id: int, payload: OrderItemUpdate
    ) -> OrderItem:
        self.get_order(order_id)
        item = self.repository.get_item(order_id, item_id)
        if item is None:
            raise NotFoundError(f"Item {item_id} no existe en la orden {order_id}")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise BadRequestError("Debe especificar quantity o unitPrice")
        for key, value in data.items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        order = self.repository.get_by_id(order_id)
        self._recalculate_total(order)
        return self.repository.get_item(order_id, item_id)

    def delete_item(self, order_id: int, item_id: int) -> None:
        self.get_order(order_id)
        item = self.repository.get_item(order_id, item_id)
        if item is None:
            raise NotFoundError(f"Item {item_id} no existe en la orden {order_id}")
        self.repository.delete_item(item)
        order = self.repository.get_by_id(order_id)
        self._recalculate_total(order)
