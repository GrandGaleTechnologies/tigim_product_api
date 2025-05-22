from app.common.exceptions import NotFound, Unauthorized


class ClientNotFound(NotFound):
    """
    Exception class for 404 client not found
    """

    def __init__(self, *, loc: list | None = None):
        super().__init__("Client Not Found", loc=loc)


class InvalidAPIKey(Unauthorized):
    """
    Exception class for 401 Invalid API Key
    """

    def __init__(self, *, loc: list | None = None):
        super().__init__("Invalid API Key", loc=loc)
