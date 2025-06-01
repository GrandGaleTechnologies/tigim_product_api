from pydantic import Field

from app.common.schemas import PaginatedResponseSchema, ResponseSchema
from app.store.schemas.base import Store, StoreSummary, UnifiedProduct


######################################################################
# Unified Product
######################################################################
class PaginatedUnifiedProductListResponse(PaginatedResponseSchema):
    """
    Paginated response schema for unified product lists
    """

    data: list[UnifiedProduct] = Field(description="The list of products")


######################################################################
# Store
######################################################################
class StoreResponse(ResponseSchema):
    """
    Response schema for stores
    """

    data: Store = Field(description="The details of the store")


class PaginatedStoreListResponse(PaginatedResponseSchema):
    """
    Paginated response schema for stores
    """

    data: list[StoreSummary] = Field(
        description="The list of stores belonging to the client"
    )
