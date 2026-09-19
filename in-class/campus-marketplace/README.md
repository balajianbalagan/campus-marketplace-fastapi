# Campus Marketplace

A reference FastAPI app: students buy/sell items on campus. Covers Modules 1, 5, and 6 from
`../../knowledge-base/` — routing/validation/dependencies, auth + RBAC + file upload, and
websockets + rate limiting.

## Run it

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

## Run the tests

```bash
python -m pytest -v
```

## Layout

- `app/models.py` — `User`/`Listing` and their `*Create`/`*Read` variants (SQLModel).
- `app/database.py` — SQLite engine + the `get_session` dependency.
- `app/auth.py` — password hashing, JWT issuing/verification, `get_current_user`, `require_role`.
- `app/rate_limit.py` — a class-based rate-limiting dependency.
- `app/ws.py` — the websocket connection manager for live listing notifications.
- `app/routers/` — `auth.py` (register/login) and `listings.py` (search/create/update/delete/photo upload).
- `tests/` — pytest + `TestClient` coverage for auth and listings.

Try it end to end in `/docs`: register → login → Authorize → create a listing → search for it.
Then connect to `ws://127.0.0.1:8000/ws/listings` (e.g. from a browser console) and watch it
get a message when a new listing is created.
