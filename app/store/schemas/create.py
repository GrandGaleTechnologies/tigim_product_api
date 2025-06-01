from typing import Literal

from pydantic import BaseModel, Field

from app.store.schemas import base


class StoreCreate(BaseModel):
    """
    Create schema for stores
    """

    name: str = Field(max_length=255, description="The name of the store")
    type: Literal["magento"] = Field(description="The store's type")
    auth_keys: base.MagentoStoreAuthKeys = Field(
        discriminator="type", description="The store's auth keys"
    )
