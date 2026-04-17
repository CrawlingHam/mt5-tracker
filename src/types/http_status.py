from enum import IntEnum

__all__ = ["HTTPStatusCode"]

class HTTPStatusCode(IntEnum):
    INTERNAL_SERVER_ERROR = 500
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    UNAUTHORIZED = 401
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    OK = 200
