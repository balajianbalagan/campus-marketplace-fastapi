# Module 5 — Auth, roles, and photo evidence

Starting point for this module already has full complaint CRUD (copied in as "given" — you
built the equivalent in Module 1). Your job this module is exactly what Module 5 taught:
**users, passwords, JWTs, roles, and file upload.**

## What's already done for you

- `app/models.py` — `Complaint*` classes (unchanged from Module 1) plus `User`, `UserCreate`,
  `UserRead`, and `Role` (`resident`, `staff`, `admin`).
- `app/routers/complaints.py` — full CRUD, already wired to require login (it imports
  `get_current_user` from `app/auth.py` — which doesn't work yet, that's your job).

## What you need to build (`app/auth.py`, `app/routers/auth.py`)

1. **`hash_password` / `verify_password`** — bcrypt via `passlib`, same as Campus Marketplace.
2. **`create_access_token`** — JWT with `sub` = username and an expiry.
3. **`get_current_user`** — dependency: decode the token, 401 if invalid/missing, look up and
   return the `User`.
4. **`require_role(*allowed)`** — dependency factory: 403 if `user.role` isn't in `allowed`.
5. **`POST /auth/register`** and **`POST /auth/login`** in `app/routers/auth.py`.

## Then apply it to complaints (`app/routers/complaints.py` — search for `TODO(module-5)`)

- `POST /complaints` should set `reporter_id = user.id` from `Depends(get_current_user)`,
  not accept it from the client.
- Only `staff` or `admin` may change `status` via `PATCH /complaints/{id}` — residents can
  still edit their own `description`/`location`, but not `status`. Use `require_role`.
- `POST /complaints/{id}/photo` — accept an `UploadFile`, validate `content_type` is
  JPEG/PNG, save it under `uploads/complaints/` with a generated filename
  (`uuid4()` — never trust the client's filename), and only the original reporter may upload
  a photo for their own complaint.

## Rules to keep in mind (see `knowledge-base/02-blog-api-auth.md`)

- Same error for "no such user" and "wrong password" on login.
- 401 = don't know who you are; 403 = know who you are, not allowed.
- Never put `hashed_password` on `UserRead`.

Run `python -m pytest ../tests -v` from `starter/`.
