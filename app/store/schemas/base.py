from typing import Literal

from pydantic import BaseModel, Field, field_validator


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


class UnifiedProduct(BaseModel):
    """
    Base schema for unified product representations
    """

    id: str = Field(description="The ID of the product")
    name: str = Field(description="The name of the products")
    description: UnifiedProductDescription = Field(
        description="The description of the product"
    )
    price: UnifiedProductPrice = Field(description="The price of the products")
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
