from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

VALID_API_KEYS = {"campus-secret-key"}

EVENTS = [{"id": i, "title": f"Event {i}"} for i in range(1, 31)]


# TODO: read the X-API-Key header (FastAPI auto-converts x_api_key -> X-API-Key),
# raise HTTPException(401, "Invalid API key") if it's not in VALID_API_KEYS.
def verify_api_key(x_api_key: str = Header(...)):
    raise NotImplementedError("TODO: implement verify_api_key")


class Paginator:
    def __init__(self, default_limit: int = 10, max_limit: int = 50):
        self.default_limit = default_limit
        self.max_limit = max_limit

    # TODO: validate 0 < limit <= self.max_limit (HTTPException(422, ...) if not),
    # then return {"limit": limit, "offset": offset}.
    def __call__(self, limit: int = 10, offset: int = 0):
        raise NotImplementedError("TODO: implement Paginator.__call__")


events_paginator = Paginator(max_limit=25)


# TODO: use Depends(events_paginator) and Depends(verify_api_key), slice EVENTS accordingly,
# return the slice.
@app.get("/events")
def get_events():
    raise NotImplementedError("TODO: implement get_events")
