from sqlalchemy.ext.asyncio import AsyncSession

from app.client import models as client_models
from app.common.exceptions import BadRequest, InternalServerError
from app.external.magento.client import InternalMagentoClient
from app.store import models
from app.store.crud import StoreCRUD
from app.store.schemas import create


######################################################################
# Stores
######################################################################
async def create_store(
    data: create.StoreCreate, client: client_models.Client, db: AsyncSession
):
    """
    Create store

    Args:
        data (create.StoreCreate): The store's details
        client (client_models.Client): The client
        db (AsyncSession): The database session

    Raises:
        BadRequest: Invalid credentials

    Returns:
        models.Store: The details of the store
    """
    # Init crud
    store_crud = StoreCRUD(db=db)

    # Check: valid credentials
    if data.type == "magento" and not await InternalMagentoClient.verify_credentials(
        creds=data.auth_keys
    ):
        raise BadRequest("Invalid magento credentials")

    # Create store
    obj = await store_crud.create(data={"client_id": client.id, **data.model_dump()})

    return obj


######################################################################
# Products
######################################################################
async def get_products(store: models.Store, page: int, size: int):
    """
    Get store products

    Args:
        store (models.Store): The store obj
        page (int): The page number
        size (int): The max size of the base

    Raises:
        InternalServerError: Invalid store type

    Returns:
        typle[list[UnifiedProduct], PaginationMetaType]: The list of products and pagination detaisl
    """
    # Check: store type
    if store.type == "magento":  # type: ignore
        client = InternalMagentoClient(
            base_url=store.auth_keys["base_url"],  # type: ignore
            access_token=store.auth_keys["access_token"],  # type: ignore
        )

        products, pagination = await client.get_products(page=page, size=size)

    else:
        raise InternalServerError(
            f"Invalid store type {store.type}", loc="app.store.services.get_products"
        )

    return products, pagination
