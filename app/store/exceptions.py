from app.common.exceptions import Forbidden, NotFound


class StoreNotFound(NotFound):
    """
    Exception class for 404 Store Not Found
    """

    def __init__(self, *, loc: list | None = None):
        super().__init__("Store Not Found", loc=loc)


class ForbiddenStore(Forbidden):
    """
    Exception class for 403 You are not allowed to access this store
    """

    def __init__(self, *, loc: list | None = None):
        super().__init__("You are not allowed to access this store", loc=loc)
