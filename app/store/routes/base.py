from typing import cast

from fastapi import APIRouter

from app.client.annotations import CurrentClient
from app.common.annotations import DatabaseSession, PaginationParams
from app.common.exceptions import BadRequest, Forbidden
from app.common.paginators import get_pagination_metadata
from app.external.magento.client import InternalMagentoClient
from app.store import models, selectors, services
from app.store.crud import StoreCRUD
from app.store.formatters import format_store, format_store_summary
from app.store.schemas import create, edit, response

# Globals
router = APIRouter()


@router.post(
    "",
    summary="Add new store",
    response_description="The details of the added store",
    status_code=201,
    response_model=response.StoreResponse,
)
async def route_store_create(
    store_in: create.StoreCreate, curr_client: CurrentClient, db: DatabaseSession
):
    """
    This endpoint is used to create/add a new store
    """

    # Create store
    store = await services.create_store(data=store_in, client=curr_client, db=db)

    return {"data": await format_store(store=store)}


@router.get(
    "",
    summary="Get stores",
    response_description="The paginated list of stores belonging to the client",
    status_code=200,
    response_model=response.PaginatedStoreListResponse,
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


@router.get(
    "/{store_id}/",
    summary="Get store details",
    response_description="The details of the store",
    status_code=200,
    response_model=response.StoreResponse,
)
async def route_store_details(
    store_id: int, curr_client: CurrentClient, db: DatabaseSession
):
    """
    This endpoint returns the details of a store
    """

    # Get store
    store = cast(models.Store, await selectors.get_store_by_id(id=store_id, db=db))

    # Check: ownership
    if store.client_id != curr_client.id:  # type: ignore
        raise Forbidden(
            "You are not allowed to access this store", loc=["path", "store_id"]
        )

    return {"data": await format_store(store=store)}


@router.put(
    "/{store_id}/",
    summary="Edit store details",
    response_description="The new details of the store",
    status_code=200,
    response_model=response.StoreResponse,
)
async def route_store_edit(
    store_id: int,
    store_in: edit.StoreEdit,
    curr_client: CurrentClient,
    db: DatabaseSession,
):
    """
    This endpoint is used to edit store details
    """

    # Get store
    store = cast(models.Store, await selectors.get_store_by_id(id=store_id, db=db))

    # Check: ownership
    if store.client_id != curr_client.id:  # type: ignore
        raise Forbidden(
            "You are not allowed to access this store", loc=["path", "store_id"]
        )

    # Edit details
    for field, value in store_in.model_dump(exclude={"auth_keys"}).items():
        setattr(store, field, value)

    # Edit auth keys
    if await InternalMagentoClient.verify_credentials(creds=store_in.auth_keys):
        setattr(store, "auth_keys", store_in.auth_keys.model_dump())
    else:
        raise BadRequest("Invalid magento credentials")

    # Save changes
    await db.commit()

    return {"data": await format_store(store=store)}
