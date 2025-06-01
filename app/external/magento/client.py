import math
import time
from typing import Any, cast

import logfire

from app.common.exceptions import BadGatewayError
from app.common.types import PaginationMetaType
from app.core.settings import get_settings
from app.external._request import InternalRequestClient
from app.external.magento import utils
from app.external.magento.types import MagentoProductType

# Configs
settings = get_settings()
logfire.configure(
    token=settings.LOGFIRE_TOKEN, environment="dev" if settings.DEBUG else "prod"
)


class InternalMagentoClient:
    """
    Internal client class for magento interactions
    """

    def __init__(self, base_url: str, access_token: str) -> None:
        self.base_url = base_url
        self.access_token = access_token
        self.req = InternalRequestClient(base_url=self.base_url)

        # Internal cache: category_id -> (timestamp, name)
        self._category_cache: dict[str, tuple[float, str]] = {}
        self._cache_ttl_seconds = 30 * 60  # 30 minutes

    async def get_pagination_metadata(self, response: dict[str, Any], count: int):
        """
        Generate pagination metadata from Magento API-style response.

        Params:
            response: Magento-like API response containing search_criteria and total_count
            count: Number of items returned in the current page

        Returns:
            Dictionary with pagination metadata
        """
        total_no_items = response["total_count"]  # type: ignore
        page = response["search_criteria"]["current_page"]  # type: ignore
        size = response["search_criteria"]["page_size"]  # type: ignore

        total_no_pages = math.ceil(total_no_items / size)

        return {
            "total_no_items": total_no_items,
            "total_no_pages": total_no_pages,
            "page": page,
            "size": size,
            "count": count,
            "has_next_page": page < total_no_pages,
            "has_prev_page": page > 1,
        }

    async def get_category_name(self, id: str, raise_exc: bool = True):
        """
        Get category name by ID with 30-minute caching
        """

        now = time.time()
        cached = self._category_cache.get(id)

        # Return from cache if fresh
        if cached and (now - cached[0]) < self._cache_ttl_seconds:
            return cached[1]

        # Make request
        resp = await self.req.get(
            f"/categories/{id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Check success
        if resp.status_code != 200:
            if raise_exc:
                raise BadGatewayError(
                    f"Category {id} not found",
                    loc="app.external.magento.client.InternalMagentoClient.get_category_name",
                    service="magento",
                    payload=None,
                    response_status_code=resp.status_code,
                    response=resp.json(),
                )
            return None

        data = resp.json()
        category_name: str = data["name"]

        # Cache result
        self._category_cache[id] = (now, category_name)

        return category_name

    async def get_products(
        self, page: int, size: int
    ) -> tuple[list[MagentoProductType], PaginationMetaType]:
        """
        Get products
        """

        with logfire.span(
            "InternalMagentoClient.get_products", service="magento"
        ) as span:
            # Make req
            resp = await self.req.get(
                f"/products?searchCriteria[pageSize]={size}&searchCriteria[currentPage]={page}",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )

            # Check: success
            if resp.status_code != 200:
                span.set_attribute("response.code", resp.status_code)
                span.set_attribute("response.body", resp.text)
                raise BadGatewayError(
                    msg="Error getting products",
                    loc="app.external.magento/client.InternalMagentoClient.get_products",
                    service="magento",
                    payload=None,
                    response_status_code=resp.status_code,
                    response=resp.text,
                )

            # Form data
            data = resp.json()

            products = []
            for prod in data["items"]:
                # Form permalink
                link = None
                for attr in prod["custom_attributes"]:
                    if attr["attribute_code"] == "url_key":
                        link = (
                            self.base_url.removesuffix("rest/V1")
                            + attr["value"]
                            + ".html"
                        )

                products.append(
                    {
                        "id": str(prod["id"]),
                        "sku": prod["sku"],
                        "name": prod["name"],
                        "images": [
                            {
                                "url": await utils.form_magento_image_url(
                                    base_url=self.base_url, filepath=img["file"]
                                ),
                                "label": img["label"],
                            }
                            for img in prod["media_gallery_entries"]
                        ],
                        "link": link,
                        "description": {
                            "format": "html",
                            "content": [
                                attr
                                for attr in prod["custom_attributes"]
                                if attr["attribute_code"] == "description"
                            ][0]["value"],
                        },
                        "price": {"currency": "USD", "price": prod["price"]},
                        "status": True if prod["status"] == 1 else False,
                        "categories": [
                            await self.get_category_name(
                                id=cat["category_id"], raise_exc=False
                            )
                            for cat in prod["extension_attributes"]["category_links"]
                        ],
                        "type": "magentoproduct",
                    }
                )

        return products, cast(
            PaginationMetaType,
            await self.get_pagination_metadata(
                response={
                    "search_criteria": data["search_criteria"],
                    "total_count": data["total_count"],
                },
                count=data["total_count"],
            ),
        )
