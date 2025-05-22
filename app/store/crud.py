from sqlalchemy.ext.asyncio import AsyncSession

from app.common.crud import CRUDBase
from app.store import models


class StoreCRUD(CRUDBase[models.Store]):
    """
    CRUD Class for store
    """

    def __init__(self, db: AsyncSession):
        super().__init__(models.Store, db)
