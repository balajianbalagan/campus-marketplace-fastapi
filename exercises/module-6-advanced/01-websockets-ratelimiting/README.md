# Exercise: WebSocket Broadcast + Rate Limiting

A minimal "campus alert" broadcaster: post an alert over HTTP (rate-limited), everyone
connected over a websocket gets it live.

## Task (`starter/main.py`)

- `class ConnectionManager` — `connections: list[WebSocket]`. `connect` accepts + appends;
  `disconnect` removes; `broadcast(message: dict)` sends JSON to every connection.
- `@app.websocket("/ws/alerts")` — connect, loop `receive_text()` to stay open, disconnect
  cleanly on `WebSocketDisconnect`.
- `class RateLimiter` — `__init__(self, times, seconds)`; `__call__(self, request: Request)`
  keyed by `request.client.host`, `HTTPException(429, ...)` past the limit.
- `POST /alerts` — body `{"message": str}`, behind `Depends(alert_rate_limiter)`
  (`times=3, seconds=60`), broadcasts `{"alert": message}` to `/ws/alerts`, returns
  `{"sent": True}`, `201`.

## Run

```bash
cd starter
python -m pytest ../tests -v
```
