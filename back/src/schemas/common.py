from typing import Any, Callable, Generic, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


class CamelAPIRouter(APIRouter):
    def add_api_route(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
        kwargs.setdefault("response_model_by_alias", True)
        super().add_api_route(path, endpoint, **kwargs)


class PaginatedResponse(CamelModel, Generic[T]):
    items: list[T]
    page: int
    limit: int
    total: int


class ErrorResponse(CamelModel):
    code: int
    error: str
    message: str
    errors: list[dict] | None = None
