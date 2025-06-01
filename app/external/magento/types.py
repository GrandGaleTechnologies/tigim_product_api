from typing import List, Literal, Optional, TypedDict


class ProductImageType(TypedDict):
    """
    Typed dict class for product images
    """

    url: str
    label: Optional[str]


class ProductDescriptionType(TypedDict):
    """
    Typed dict class for product descriptions
    """

    format: Literal["html"]
    content: str


class ProductPriceType(TypedDict):
    """
    Typed dict class for product price
    """

    currency: Literal["USD"]
    price: float


class MagentoProductType(TypedDict):
    """
    Typed dict class for magento products
    """

    id: str
    sku: str
    name: str
    images: List[ProductImageType]
    link: str
    description: ProductDescriptionType
    price: ProductPriceType
    status: bool
    categories: List[Optional[str]]
    type: Literal["magentoproduct"]
