from typing import Annotated

from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.client.crud import ClientCRUD
from app.client.exceptions import ClientNotFound, InvalidAPIKey
from app.common.annotations import DatabaseSession


async def get_current_client(
    api_key: Annotated[str, Header(alias="X-API-KEY")], db: DatabaseSession
):
    """
    Get current client using the client's API ey

    Args:
        db (DatabaseSession): The database session
        api_key (str, optional): The client's api key. Defaults to "X-API-KEY")].

    Raises:
        InvalidAPIKey

    Returns:
        models.Client: The client obj
    """
    # Get Client
    client = await get_client_by_apikey(api_key=api_key, db=db, raise_exc=False)

    # Check: valid api key
    if not client:
        raise InvalidAPIKey()

    return client


async def get_client_by_apikey(api_key: str, db: AsyncSession, raise_exc: bool = True):
    """
    Get client by api key

    Args:
        api_key (str): The client's API Key
        db (AsyncSession): The database session
        raise_exc (bool, optional): raise a 404 if not found. Defaults to True.

    Raises:
        ClientNotFound

    Returns:
        models.Client: The client obj
    """
    # Init crud
    client_crud = ClientCRUD(db=db)

    # Get client API Key
    client = await client_crud.get(api_key=api_key)

    if not client and raise_exc:
        raise ClientNotFound()

    return client
