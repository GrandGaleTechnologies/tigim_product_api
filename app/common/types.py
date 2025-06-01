from typing import Literal, NamedTuple, TypedDict


class PaginationParamsType(NamedTuple):
    """
    The pagination parameters for the application.
    """

    q: str | None
    page: int
    size: int
    order_by: Literal["asc", "desc"]


class PaginationMetaType(TypedDict):
    """
    Typed dict class for pagination metadata
    """

    total_no_items: int
    total_no_pages: int
    page: int
    size: int
    count: int
    has_next_page: bool
    has_prev_page: bool
