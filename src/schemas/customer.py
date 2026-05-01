from pydantic import Field

from src.schemas.common import CamelModel


class CustomerBase(CamelModel):
    first_name: str = Field(..., min_length=1, max_length=80)
    last_name: str = Field(..., min_length=1, max_length=80)
    city: str | None = None
    country: str | None = None
    phone: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CamelModel):
    first_name: str | None = Field(None, min_length=1, max_length=80)
    last_name: str | None = Field(None, min_length=1, max_length=80)
    city: str | None = None
    country: str | None = None
    phone: str | None = None


class CustomerRead(CustomerBase):
    id: int
