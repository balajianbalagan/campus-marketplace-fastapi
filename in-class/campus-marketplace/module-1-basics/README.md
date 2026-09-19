# Module 1: FastAPI foundations

Build the first Campus Marketplace API in memory. This stage teaches routes, path parameters, JSON request bodies, response models, status codes, and `/docs`.

The data resets whenever the server restarts. SQLite arrives in Module 2.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `/docs`, create a listing with `POST /listings`, then read it with `GET /listings/{listing_id}`. Use FastAPI Interactive for the live coding version of this stage.
