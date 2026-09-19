# Campus Marketplace — Module 5 (auth)

Builds on `../module-1-basics/`: adds user accounts, login, roles, and photo upload.
Reference material for going deeper after the core session — not built line-by-line live.

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

## What's new compared to Module 1

- `app/models.py` — adds `User`, roles, and gives `Listing` a real owner (`seller_id`).
- `app/auth.py` — password hashing (bcrypt), JWT tokens, `get_current_user`, `require_role`.
- `app/routers/auth.py` — `/auth/register`, `/auth/login`.
- `app/routers/listings.py` — listings now require login to create; only the owner can edit;
  only a moderator/admin can delete; `POST /listings/{id}/photo` for image upload.

See `knowledge-base/02-blog-api-auth.md` for the concepts behind each piece.
