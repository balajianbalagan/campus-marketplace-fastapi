import time
from collections import defaultdict

from fastapi import HTTPException, Request


class RateLimiter:
    """Class-based dependency: config lives on the instance, __call__ makes it usable via Depends().

    In-memory + per-process, which is fine for a classroom demo. A real deployment with
    multiple worker processes would back this with Redis instead of a dict.
    """

    def __init__(self, times: int, seconds: int) -> None:
        self.times = times
        self.seconds = seconds
        self.hits: dict[str, list[float]] = defaultdict(list)

    def __call__(self, request: Request) -> None:
        key = request.client.host if request.client else "unknown"
        now = time.time()
        window = [t for t in self.hits[key] if now - t < self.seconds]
        if len(window) >= self.times:
            raise HTTPException(status_code=429, detail="Too many requests, slow down")
        window.append(now)
        self.hits[key] = window


create_listing_rate_limit = RateLimiter(times=5, seconds=60)
