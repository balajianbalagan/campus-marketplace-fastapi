from fastapi import Request
from fastapi.responses import JSONResponse


class MarketplaceError(Exception):
    """Base for app-specific errors so every error response has the same JSON shape."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail


async def marketplace_error_handler(request: Request, exc: MarketplaceError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
