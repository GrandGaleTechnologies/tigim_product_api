from app.client.types import StoreProductListParams


def route_store_product_list_params(
    page: int = 1,
    size: int = 50,
):
    """
    Helper Dependency for pagination
    """
    return StoreProductListParams(page=page, size=size)
