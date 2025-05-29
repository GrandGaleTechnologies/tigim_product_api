from typing import cast

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.client import models as client_models
from app.common.crud import CRUDBase
from app.common.types import PaginationParamsType
from app.store import models


class StoreCRUD(CRUDBase[models.Store]):
    """
    CRUD Class for store
    """

    def __init__(self, db: AsyncSession):
        super().__init__(models.Store, db)

    async def get_list(
        self,
        client: client_models.Client,
        pag: PaginationParamsType,
    ):
        """
        Get store list
        """
        q = select(self.model).filter_by(
            client_id=client.id,
        )

        # Filter by q
        if pag.q:
            q = q.filter(self.model.name.ilike(f"%{pag.q}%"))

        # Order by
        if pag.order_by == "asc":
            q = q.order_by(self.model.created_at.asc())
        else:
            q = q.order_by(self.model.created_at.desc())

        # Paginate
        p_qs = q.limit(pag.size).offset(pag.size * (pag.page - 1))

        # Execute paginated qs
        results = await self.db.execute(p_qs)

        # Execute count query
        count = cast(
            int,
            # pylint: disable=not-callable
            await self.db.scalar(select(func.count()).select_from(q.subquery())),
        )

        return results.scalars().all(), count
