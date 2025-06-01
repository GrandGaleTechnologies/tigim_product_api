async def form_magento_image_url(base_url: str, filepath: str):
    """
    Form magento image url from the file path
    """
    return f"{base_url}/media/catalog/product/cache/1/thumbnail/75x75/s/r{filepath}"
