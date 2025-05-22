from app.common.exceptions import InternalServerError
from app.external.magento.client import InternalMagentoClient
from app.store import models

# Globals


async def get_products(store: models.Store, page: int, size: int):
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
