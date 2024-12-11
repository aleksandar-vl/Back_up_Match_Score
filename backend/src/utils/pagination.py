from fastapi import Query


class PaginationParams:
    def __init__(self, offset: int, limit: int):
        self.offset = offset
        self.limit = limit


def get_pagination(
    offset: int = Query(default=0, ge=0), limit: int = Query(default=10, ge=1, le=100)
) -> PaginationParams:
    """
    Retrieves pagination parameters from the query string.

    Args:
        offset (int): The number of items to skip before starting to
        collect the result set. Default is 0.
        limit (int): The maximum number of items to return.
        Default is 10, minimum is 1, and maximum is 100.

    Returns:
        PaginationParams: An instance of PaginationParams
        containing the offset and limit.
    """
    return PaginationParams(offset=offset, limit=limit)
