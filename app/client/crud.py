from sqlalchemy.ext.asyncio import AsyncSession

from app.client import models
from app.common.crud import CRUDBase


class ClientCRUD(CRUDBase[models.Client]):
    """
    CRUD Class for clients
    """

    def __init__(self, db: AsyncSession):
        super().__init__(models.Client, db)
