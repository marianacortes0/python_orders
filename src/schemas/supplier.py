from pydantic import Field

from src.schemas.common import CamelModel


class SupplierBase(CamelModel):
    company_name: str = Field(..., min_length=1, max_length=120)
    contact_name: str | None = None
    contact_title: str | None = None
    city: str | None = None
    country: str | None = None
    phone: str | None = None
    fax: str | None = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(CamelModel):
    company_name: str | None = Field(None, min_length=1, max_length=120)
    contact_name: str | None = None
    contact_title: str | None = None
    city: str | None = None
    country: str | None = None
    phone: str | None = None
    fax: str | None = None


class SupplierRead(SupplierBase):
    id: int
