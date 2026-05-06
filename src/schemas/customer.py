from __future__ import annotations
from typing import Optional
from pydantic import Field
from src.schemas.common import CamelModel


class CustomerBase(CamelModel):
    first_name: str = Field(..., min_length=1, max_length=80)
    last_name: str = Field(..., min_length=1, max_length=80)
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CamelModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=80)
    last_name: Optional[str] = Field(None, min_length=1, max_length=80)
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None


class CustomerRead(CustomerBase):
    id: int
