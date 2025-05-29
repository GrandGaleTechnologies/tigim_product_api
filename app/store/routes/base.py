from fastapi import APIRouter

from app.client.annotations import CurrentClient
from app.common.annotations import DatabaseSession, PaginationParams
from app.common.paginators import get_pagination_metadata
from app.store.crud import StoreCRUD
from app.store.formatters import format_store_summary
from app.store.schemas import response

# Globals
router = APIRouter()


@router.get(
    "",
    summary="Get stores",
    response_description="The paginated list of stores belonging to the client",
    response_model=response.PaginatedStoreListResponse,
    status_code=200,
)
async def route_store_list(
    pag: PaginationParams, curr_client: CurrentClient, db: DatabaseSession
):
    """
    This endpoint returns the paginated list of stores
    """

    # Init crud
    store_crud = StoreCRUD(db=db)

    # Get pagianted stores
    stores, tno_stores = await store_crud.get_list(client=curr_client, pag=pag)

    return {
        "data": [await format_store_summary(store=store) for store in stores],
        "meta": await get_pagination_metadata(
            tno_items=tno_stores, count=len(stores), page=pag.page, size=pag.size
        ),
    }
