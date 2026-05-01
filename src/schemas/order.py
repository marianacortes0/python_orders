from datetime import datetime

from pydantic import Field

from src.models.order import OrderStatus
from src.schemas.common import CamelModel
from src.schemas.customer import CustomerRead
from src.schemas.product import ProductRead


class OrderItemAdd(CamelModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float | None = Field(None, gt=0)


class OrderItemUpdate(CamelModel):
    quantity: int | None = Field(None, gt=0)
    unit_price: float | None = Field(None, gt=0)


class OrderItemRead(CamelModel):
    id: int
    unit_price: float
    quantity: int
    product: ProductRead


class OrderCreate(CamelModel):
    order_number: str | None = Field(None, min_length=1, max_length=50)
    order_date: datetime | None = None
    customer_id: int
    items: list[OrderItemAdd] = Field(..., min_length=1)


class OrderReplace(CamelModel):
    order_number: str = Field(..., min_length=1, max_length=50)
    order_date: datetime
    customer_id: int
    status: OrderStatus = OrderStatus.PENDING
    items: list[OrderItemAdd] = Field(..., min_length=1)


class OrderUpdate(CamelModel):
    order_date: datetime | None = None
    customer_id: int | None = None
    status: OrderStatus | None = None


class OrderRead(CamelModel):
    id: int
    order_number: str
    order_date: datetime
    total_amount: float
    status: OrderStatus
    customer: CustomerRead
    items: list[OrderItemRead]
