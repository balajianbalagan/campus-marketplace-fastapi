# Campus Marketplace — Module 6 (advanced)

Builds on `../module-5-auth/`: adds live websocket notifications and rate limiting.
Reference material / optional short demo — not built line-by-line live.

## Run it

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m pytest -v      # 8 tests should pass
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

## What's new compared to Module 5

- `app/ws.py` + the `/ws/listings` route in `app/main.py` — everyone connected gets a live
  message the instant someone posts a new listing.
- `app/rate_limit.py` — `POST /listings` is capped at 5 per minute per caller (`429` past that).

## Quick demo of the websocket

1. Run the server, open two browser tabs' dev consoles, and in each:
   ```js
   const ws = new WebSocket("ws://127.0.0.1:8000/ws/listings");
   ws.onmessage = (e) => console.log("got:", e.data);
   ```
2. Create a listing from a third tab via `/docs`.
3. Both consoles log the broadcast instantly.

See `knowledge-base/03-advanced-patterns.md` for the concepts behind each piece.
