from app.store import models


async def format_store_summary(store: models.Store):
    """
    Format store obj to store summary dict
    """

    return {
        "id": store.id,
        "name": store.name,
        "type": store.type,
        "updated_at": store.updated_at,
        "created_at": store.created_at,
    }
