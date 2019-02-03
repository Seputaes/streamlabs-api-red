from enum import Enum


class Method(Enum):
    """
    Valid HTTP request types for the StreamLabs API.
    """

    GET = "GET"
    POST = "POST"
