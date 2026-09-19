# Module 1 — Civic Complaint Tracker basics

Build the core CRUD API for complaints. No auth yet (that's Module 5) — anyone can create
and read complaints for now.

## Data model

A `Complaint` has:
- `id: int` (primary key)
- `category: str` — e.g. `"pothole"`, `"streetlight"`, `"graffiti"`, `"trash"`
- `description: str` (min length 10 — a one-word complaint isn't actionable)
- `location: str`
- `status: str` — one of `"open"`, `"in_progress"`, `"resolved"` (default `"open"`)
- `reporter_name: str`
- `created_at: datetime`

Follow the **four-class pattern** from Campus Marketplace's `models.py`: `ComplaintBase` /
`Complaint(table=True)` / `ComplaintCreate` / `ComplaintRead`.

## Endpoints to implement (see `starter/app/main.py` TODOs)

- `POST /complaints` → create a complaint, `status` forced to `"open"` regardless of what the client sends, `201`.
- `GET /complaints` → list complaints, with optional query params `category` and `status` to filter, and `limit` (default 20, max 100).
- `GET /complaints/{id}` → single complaint, `404` if missing.
- `PATCH /complaints/{id}` → update `status` only (use `exclude_unset`), `404` if missing.

## Hints

- Look at `knowledge-base/01-fastapi-basics.md` sections 2–4 and 6 for path/query params and response models.
- Look at Campus Marketplace's `app/database.py` and `app/models.py` for the exact SQLModel setup — the pattern transfers directly, just rename `Listing` → `Complaint`.
- Run `python -m pytest ../tests -v` from inside `starter/` and read the assertion messages — they name the exact endpoint/behavior that's missing.
