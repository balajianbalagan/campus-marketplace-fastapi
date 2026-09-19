# Module 1 — Civic Complaint Tracker basics

Build the core API for complaints. No login yet (that's Module 5) — anyone can create and
read complaints for now.

## Data model

One class, `Complaint`, with:
- `id: int` (primary key)
- `category: str` — e.g. `"pothole"`, `"streetlight"`, `"graffiti"`, `"trash"`
- `description: str`
- `location: str`
- `reporter_name: str`
- `status: str` — defaults to `"open"`

Same shape as Campus Marketplace's `Listing` in `in-class/campus-marketplace/module-1-basics/app/models.py`.

## Endpoints to implement (see `starter/app/main.py` TODOs)

- `GET /complaints` → list complaints, optional `category` query param to filter.
- `GET /complaints/{id}` → single complaint, `404` if missing.
- `POST /complaints` → create a complaint; `status` always starts `"open"` no matter what the client sends.

## Hints

- Look at `knowledge-base/01-fastapi-basics.md` sections 2–4 for path/query params.
- Look at `in-class/campus-marketplace/module-1-basics/app/main.py` — same three endpoints, same shape, just a different model.
- Run `python -m pytest ../tests -v` from inside `starter/` and read the assertion messages — they name the exact endpoint/behavior that's missing.
