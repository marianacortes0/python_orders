from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base


class OrderStatus(str, PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(120), nullable=False, index=True)
    contact_name = Column(String(120), nullable=True)
    contact_title = Column(String(120), nullable=True)
    city = Column(String(120), nullable=True)
    country = Column(String(120), nullable=True)
    phone = Column(String(50), nullable=True)
    fax = Column(String(50), nullable=True)

    products = relationship("Product", back_populates="supplier")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(150), nullable=False, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    unit_price = Column(Float, nullable=False)
    package = Column(String(120), nullable=True)
    is_discontinued = Column(Boolean, nullable=False, default=False)

    supplier = relationship("Supplier", back_populates="products")
    items = relationship("OrderItem", back_populates="product")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    city = Column(String(120), nullable=True)
    country = Column(String(120), nullable=True)
    phone = Column(String(50), nullable=True)

    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING
    )
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")
