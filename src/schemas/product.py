from pydantic import Field

from src.schemas.common import CamelModel
from src.schemas.supplier import SupplierRead


class ProductBase(CamelModel):
    product_name: str = Field(..., min_length=1, max_length=150)
    unit_price: float = Field(..., gt=0)
    package: str | None = None
    is_discontinued: bool = False


class ProductCreate(ProductBase):
    supplier_id: int


class ProductReplace(ProductBase):
    supplier_id: int


class ProductUpdate(CamelModel):
    product_name: str | None = Field(None, min_length=1, max_length=150)
    supplier_id: int | None = None
    unit_price: float | None = Field(None, gt=0)
    package: str | None = None
    is_discontinued: bool | None = None


class ProductRead(ProductBase):
    id: int
    supplier: SupplierRead
