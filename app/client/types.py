from typing import NamedTuple


class StoreProductListParams(NamedTuple):
    """
    The pagination parameters for the route_store_product.
    """

    page: int
    size: int
