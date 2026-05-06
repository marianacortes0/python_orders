from __future__ import annotations
from typing import Optional
from pydantic import Field
from src.schemas.common import CamelModel


class SupplierBase(CamelModel):
    company_name: str = Field(..., min_length=1, max_length=120)
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(CamelModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=120)
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None


class SupplierRead(SupplierBase):
    id: int
