from enum import Enum
from typing import Generic, TypeVar

from pydantic import Field

from app.models.base.camel_model import CamelModel

T = TypeVar("T")


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


class PaginatedRequest(CamelModel, Generic[T]):
    page: int = Field(gt=0)
    per_page: int = Field(gt=0)
    sort_by: T
    sort_direction: SortDirection
