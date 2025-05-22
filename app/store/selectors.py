from sqlalchemy.ext.asyncio import AsyncSession

from app.store.crud import StoreCRUD
from app.store.exceptions import StoreNotFound


async def get_store_by_id(id: int, db: AsyncSession, raise_exc: bool = True):
    """
    Get store by ID

    Args:
        id (int): The store ID
        db (AsyncSession): The database session
        raise_exc (bool, optional): raise a 404 if not. Defaults to True.

    Raises:
        StoreNotFound

    Returns:
        models.Store: The store obj
    """
    # Init crud
    store_crud = StoreCRUD(db=db)

    # Get store
    store = await store_crud.get(id=id)

    if not store and raise_exc:
        raise StoreNotFound()

    return store
