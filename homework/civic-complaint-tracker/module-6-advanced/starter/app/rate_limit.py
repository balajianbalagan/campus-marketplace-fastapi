import time
from collections import defaultdict

from fastapi import HTTPException, Request


class RateLimiter:
    """Class-based dependency: config on the instance, __call__ makes it usable via Depends().

    See Campus Marketplace's app/rate_limit.py for the reference implementation.
    """

    def __init__(self, times: int, seconds: int) -> None:
        self.times = times
        self.seconds = seconds
        self.hits: dict[str, list[float]] = defaultdict(list)

    # TODO(module-6):
    # 1. key = request.client.host (fall back to "unknown" if request.client is None)
    # 2. prune self.hits[key] to only timestamps within the last `self.seconds`
    # 3. if there are already >= self.times hits in that window, raise HTTPException(429, ...)
    # 4. otherwise, record `now` as a new hit
    def __call__(self, request: Request) -> None:
        raise NotImplementedError("TODO: implement RateLimiter.__call__")


complaint_rate_limit = RateLimiter(times=5, seconds=60)
