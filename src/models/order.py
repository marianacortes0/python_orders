from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class Supplier:
    id: int
    company_name: str
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None


@dataclass
class Product:
    id: int
    product_name: str
    supplier_id: int
    unit_price: float
    package: Optional[str] = None
    is_discontinued: bool = False
    supplier: Optional["Supplier"] = field(default=None, compare=False, repr=False)


@dataclass
class Customer:
    id: int
    first_name: str
    last_name: str
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class Order:
    id: int
    order_number: str
    order_date: datetime
    total_amount: float
    customer_id: int
    status: OrderStatus = OrderStatus.PENDING
    customer: Optional["Customer"] = field(default=None, compare=False, repr=False)
    items: list = field(default_factory=list, compare=False, repr=False)


@dataclass
class OrderItem:
    id: int
    order_id: int
    product_id: int
    unit_price: float
    quantity: int
    product: Optional["Product"] = field(default=None, compare=False, repr=False)
