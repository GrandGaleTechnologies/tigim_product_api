from pydantic import Field

from app.common.schemas import PaginatedResponseSchema
from app.store.schemas.base import UnifiedProduct


class PaginatedUnifiedProductListResponse(PaginatedResponseSchema):
    """
    Paginated response schema for unified product lists
    """

    data: list[UnifiedProduct] = Field(description="The list of products")
