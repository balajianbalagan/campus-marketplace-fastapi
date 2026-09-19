# Exercise: Path & Query Parameters

Build a tiny "campus room booking" lookup endpoint using only path/query params — no
database, no body, just what Module 1's early lessons cover.

## Task (`starter/main.py`, look for `# TODO`)

- `GET /buildings/{building_id}/rooms/{room_number}` — `building_id: int > 0`, `room_number`
  a string. Return `{"building_id": ..., "room_number": ...}`.
- `GET /rooms` — query params: `capacity_min: int | None`, `has_projector: bool = False`,
  `limit: int = 10` (must be `<= 50`). Filter the in-memory `ROOMS` list accordingly and
  return matches.

## Run

```bash
cd starter
python -m pytest ../tests -v
```
