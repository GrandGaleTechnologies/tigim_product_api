from functools import lru_cache

from pydantic import BaseModel


class RouteTags(BaseModel):
    """
    Base model for app route tags
    """

    # Client Tags
    CLIENT: str = "Client APIs"

    # Store Tags
    STORE: str = "Store APIs"


@lru_cache
def get_tags():
    """
    Get app rotue tags
    """
    return RouteTags()
