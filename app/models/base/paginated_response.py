from typing import Generic, List, Sequence, TypeVar

from app.models.base.camel_model import CamelModel

T = TypeVar("T")


class PaginatedResponse(CamelModel, Generic[T]):
    items: List[T] | Sequence[T]
    page: int
    per_page: int
    total_page: int
    total: int
    sort_by: str
    sort_direction: str
