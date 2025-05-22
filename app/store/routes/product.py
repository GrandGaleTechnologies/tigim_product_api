from typing import cast

from fastapi import APIRouter

from app.client.annotations import CurrentClient
from app.common.annotations import DatabaseSession
from app.store import models, selectors, services
from app.store.annotations import RouteStoreProductListParams
from app.store.exceptions import ForbiddenStore
from app.store.schemas import response

# Globals
router = APIRouter()


@router.get(
    "",
    summary="Get Store Products",
    response_description="The paginated list of stores",
    response_model=response.PaginatedUnifiedProductListResponse,
    status_code=200,
)
async def store_product_list(
    store_id: int,
    pag: RouteStoreProductListParams,
    curr_client: CurrentClient,
    db: DatabaseSession,
):
    """
    This endpoint returns the list of products of a store
    """

    # Get store
    store = cast(models.Store, await selectors.get_store_by_id(id=store_id, db=db))

    # Check: ownership
    if store.client_id != curr_client.id:  # type: ignore
        raise ForbiddenStore()

    # Get products
    products, pagination = await services.get_products(
        store=store, page=pag.page, size=pag.size
    )

    return {"data": products, "meta": pagination}
