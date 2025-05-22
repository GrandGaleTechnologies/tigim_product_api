from typing import Annotated

from fastapi import Depends

from app.client.types import StoreProductListParams
from app.store.dependency import route_store_product_list_params

RouteStoreProductListParams = Annotated[
    StoreProductListParams, Depends(route_store_product_list_params)
]
