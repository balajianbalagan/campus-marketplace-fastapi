# Exercise: JWT Auth + Role-Based Access Control

In-memory user store (no DB, to keep this short) — the point is the auth mechanics from
Module 5, not persistence (you already did that in the homework project).

## Task (`starter/main.py`)

- `hash_password` / `verify_password` — bcrypt via `passlib.context.CryptContext`.
- `create_token(username)` / `decode_token(token)` — JWT via `python-jose`, `sub` claim.
- `POST /register` — body `{"username": str, "password": str, "role": "member"|"officer"}`
  (default role `"member"`). 400 if username taken. Store the hash in `USERS` dict. Return
  `{"username": ..., "role": ...}`, `201`.
- `POST /login` — `OAuth2PasswordRequestForm`. 401 (same message) for bad username or bad
  password. Return `{"access_token": ..., "token_type": "bearer"}`.
- `get_current_user` — dependency, decode token, 401 if invalid, return the user dict.
- `require_officer` — dependency built on top of `get_current_user`, 403 if `role != "officer"`.
- `DELETE /club-funds/{amount}` — officer-only (use `require_officer`), returns
  `{"approved_by": username, "amount": amount}`.

## Run

```bash
cd starter
python -m pytest ../tests -v
```
