from __future__ import annotations
from typing import Optional
from pydantic import Field
from src.schemas.common import CamelModel
from src.schemas.supplier import SupplierRead


class ProductBase(CamelModel):
    product_name: str = Field(..., min_length=1, max_length=150)
    unit_price: float = Field(..., gt=0)
    package: Optional[str] = None
    is_discontinued: bool = False


class ProductCreate(ProductBase):
    supplier_id: int


class ProductReplace(ProductBase):
    supplier_id: int


class ProductUpdate(CamelModel):
    product_name: Optional[str] = Field(None, min_length=1, max_length=150)
    supplier_id: Optional[int] = None
    unit_price: Optional[float] = Field(None, gt=0)
    package: Optional[str] = None
    is_discontinued: Optional[bool] = None


class ProductRead(ProductBase):
    id: int
    supplier_id: int
    supplier: SupplierRead
