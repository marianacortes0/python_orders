from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SupplierBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=120)
    contact_name: str | None = None
    contact_title: str | None = None
    city: str | None = None
    country: str | None = None
    phone: str | None = None
    fax: str | None = None


class SupplierCreate(SupplierBase):
    pass


class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=150)
    unit_price: float = Field(..., gt=0)
    package: str | None = None
    is_discontinued: bool = False


class ProductCreate(ProductBase):
    supplier_id: int


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    supplier: SupplierRead


class CustomerBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=80)
    last_name: str = Field(..., min_length=1, max_length=80)
    city: str | None = None
    country: str | None = None
    phone: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class OrderItemCreate(BaseModel):
    product_id: int
    unit_price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    unit_price: float
    quantity: int
    product: ProductRead


class OrderCreate(BaseModel):
    order_number: str = Field(..., min_length=1, max_length=50)
    order_date: datetime | None = None
    customer_id: int
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderUpdate(BaseModel):
    order_number: str | None = Field(None, min_length=1, max_length=50)
    order_date: datetime | None = None
    customer_id: int | None = None


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_number: str
    order_date: datetime
    total_amount: float
    customer: CustomerRead
    items: list[OrderItemRead]


class ErrorResponse(BaseModel):
    error: str
    detail: str | list | dict
