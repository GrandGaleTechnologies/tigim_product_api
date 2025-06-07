from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


######################################################################
# Unified Product
######################################################################
class UnifiedProductPrice(BaseModel):
    """
    Base schema for unified product representation prices
    """

    currency: Literal["USD"] = Field(
        default="USD", description="The currency of the product"
    )
    price: float = Field(description="The price of the product")


class UnifiedProductDescription(BaseModel):
    """
    Base schema for unified product descriptions
    """

    format: Literal["html", "text"] = Field(
        description="The text formatting for the description"
    )
    content: str = Field(description="The content of the description")


class UnifiedProductImage(BaseModel):
    """
    Base schema for unified product images
    """

    url: str = Field(description="The URL of the image")
    label: str | None = Field(description="The image label")


class UnifiedProduct(BaseModel):
    """
    Base schema for unified product representations
    """

    id: str = Field(description="The ID of the product")
    sku: str = Field(description="The product's sku")
    name: str = Field(description="The name of the products")
    images: list[UnifiedProductImage] = Field(description="The list of images")
    link: str | None = Field(description="The product's link")
    description: UnifiedProductDescription = Field(
        description="The description of the product"
    )
    price: UnifiedProductPrice | None = Field(description="The price of the product")
    status: bool = Field(description="Indicates if the product is active or not")
    categories: list[str | None] = Field(
        description="The list of the product's categories"
    )
    type: Literal["magentoproduct"] = Field(
        # default="magentoproduct",
        description="The origin service of the product, used as a discriminator",
    )

    @field_validator("categories", mode="before")
    def val_categories(cls, values: list[str | None]):
        """
        Tasks:
            - Remove all None fields
        """
        return [v for v in values if v]


######################################################################
# Store
######################################################################
class MagentoStoreAuthKeys(BaseModel):
    """
        Base schema for store auth keys
        {
      "base_url": "https://magento.tigim.co",
      "consumer_key": "rzq7mqfnmft7op1ubw76eadwip278ds6",
      "consumer_secret": "c3x793fjhdu0u6nr2gnhv33vfzuc3jja",
      "access_token": "3tz6l9s5352mq48vwcytt3d72jjmx51z",
      "access_token_secret": "8pro69xfcb65lagczw9q9a00c5sa0twu"
    }
    """

    type: Literal["magento"] = Field(description="The store auth-key type")
    base_url: str = Field(description="The magento base url")
    # NOTE: intentional lack of 'Field'
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


class Store(BaseModel):
    """
    Base schema for stores
    """

    id: int = Field(description="The ID of the store")
    name: str = Field(description="The name of the store")
    type: Literal["magento"] = Field(description="The store's type")
    auth_keys: MagentoStoreAuthKeys = Field(
        discriminator="type", description="The store's auth keys"
    )
    updated_at: datetime | None = Field(
        description="The time the store was last updated"
    )
    created_at: datetime = Field(description="The time the store was created")


class StoreSummary(BaseModel):
    """
    Base schema for store summaries
    """

    id: int = Field(description="The ID of the store")
    name: str = Field(description="The name of the store")
    type: Literal["magento"] = Field(description="The store's type")
    updated_at: datetime | None = Field(
        description="The time the store was last updated"
    )
    created_at: datetime = Field(description="The time the store was created")
