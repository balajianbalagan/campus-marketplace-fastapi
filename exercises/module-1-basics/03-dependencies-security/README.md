# Exercise: Dependencies (function-based, class-based, sub-dependencies)

A "campus events" read API protected by a simple API key, using three dependency patterns
from Module 1: a plain function dependency, a class-based dependency, and a sub-dependency.

## Task (`starter/main.py`)

- `verify_api_key(x_api_key: str = Header(...))` — function dependency. Valid keys are in
  `VALID_API_KEYS`. Raise `HTTPException(401, "Invalid API key")` if not valid.
- `class Paginator` — class-based dependency. `__init__(self, default_limit=10, max_limit=50)`
  stores config; `__call__(self, limit: int = 10, offset: int = 0)` validates
  `0 < limit <= self.max_limit` (else `HTTPException(422, ...)`) and returns `{"limit": limit,
  "offset": offset}`.
- `get_events(pagination: dict = Depends(events_paginator), _: None = Depends(verify_api_key))`
  — **sub-dependency**: `events_paginator = Paginator(max_limit=25)` is itself a `Depends(...)`
  used inside another route's dependency list. Return a slice of `EVENTS` using
  `pagination["offset"]`/`pagination["limit"]`, behind the API key check.

## Run

```bash
cd starter
python -m pytest ../tests -v
```
