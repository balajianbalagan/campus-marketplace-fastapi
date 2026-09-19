# Module 1 — FastAPI Basics (knowledge base)

Covers all 45 lessons of the platform's Module 1, grouped by theme. Each section: **what it is → minimal example → gotcha → where it shows up in Campus Marketplace**.

## 1. First steps & routing

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Campus Marketplace API"}
```

`uvicorn app.main:app --reload` serves it; `/docs` gives you a free Swagger UI generated from your type hints. That auto-docs page is FastAPI's core pitch — you get it for free from function signatures, no extra annotation library.

## 2. Path parameters (+ numeric validation)

```python
from fastapi import Path

@app.get("/listings/{listing_id}")
def get_listing(listing_id: int = Path(..., gt=0)):
    ...
```

- Type hint (`int`) does the parsing *and* the validation — a non-numeric `listing_id` is a 422 before your function body runs.
- `Path(..., gt=0)` adds constraints beyond type (greater-than-zero). Order of path operations matters: a literal route like `/listings/mine` must be declared **before** `/listings/{listing_id}`, or `"mine"` gets swallowed as an int and 422s.

## 3. Query parameters (+ string validation, query models)

```python
from fastapi import Query
from typing import Annotated

@app.get("/listings")
def search_listings(
    q: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
    max_price: float | None = None,
    limit: int = Query(20, le=100),
):
    ...
```

- Anything with a default value and a scalar/`Optional` type that isn't in the path becomes a query param automatically.
- `Query(...)` lets you set `min_length`, regex, etc. **Query parameter models** (Pydantic model used as the whole query signature) exist for when you have 5+ related filters — group them into one `Annotated[FilterParams, Query()]` instead of a long parameter list.

## 4. Request body, multiple params, nested models, Field

```python
from pydantic import BaseModel, Field

class ListingCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=80)
    description: str = ""
    price_cents: int = Field(..., ge=0)
    tags: list[str] = []

@app.post("/listings")
def create_listing(listing: ListingCreate, notify: bool = False):
    ...
```

- A `BaseModel` parameter is read from the JSON body; scalar params in the same signature (`notify`) stay query params — FastAPI infers this from type, not position.
- **Body — Multiple Parameters**: you can take two body models in one endpoint; FastAPI nests them under their param names in the expected JSON (`{"listing": {...}, "buyer": {...}}`) unless you use `Body(embed=True)`.
- **Nested Models**: a `BaseModel` field can itself be a `BaseModel` or `list[SubModel]` — validation recurses automatically.
- **Extra Data Types**: `UUID`, `datetime`, `Decimal`, etc. are validated/parsed for free via Pydantic.

## 5. Cookie / Header parameters (+ their "model" forms)

```python
from fastapi import Cookie, Header

@app.get("/me")
def read_me(session_id: str | None = Cookie(None), user_agent: str | None = Header(None)):
    ...
```

Same idea as query params, different source. Header names auto-convert (`user_agent` ⇄ `User-Agent`). Param **models** group several related headers/cookies into one class, same pattern as query models.

## 6. Response models, extra models, status codes

```python
class ListingOut(BaseModel):
    id: int
    title: str
    price_cents: int
    # NOT seller's raw password/email — response_model filters output shape

@app.post("/listings", response_model=ListingOut, status_code=201)
def create_listing(listing: ListingCreate):
    ...
```

`response_model` is a **security boundary as much as a docs feature** — it strips any field on your DB object that isn't declared on the output model, so you can't accidentally leak a password hash by returning the ORM row directly. "Extra Models" = the standard pattern of `UserIn` / `UserOut` / `UserInDB` as three separate Pydantic classes instead of one model with optional fields.

## 7. Forms & file uploads

```python
from fastapi import UploadFile, File, Form

@app.post("/listings/{id}/photo")
async def upload_photo(id: int, caption: str = Form(...), photo: UploadFile = File(...)):
    contents = await photo.read()
    ...
```

`UploadFile` streams to a spooled temp file (doesn't load huge files fully into memory like raw `bytes` would). Mixing `Form` and `File` in one endpoint means the whole request must be `multipart/form-data` — you cannot mix a JSON body with form fields in the same request.

## 8. Handling errors

```python
from fastapi import HTTPException

@app.get("/listings/{id}")
def get_listing(id: int):
    listing = db.get(id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
```

Raise `HTTPException` anywhere in the call stack (including inside a dependency) — FastAPI converts it to a JSON error response. Custom exception classes + an `@app.exception_handler(MyError)` let you centralize error shape across the whole app instead of repeating `HTTPException` everywhere.

## 9. Path operation configuration, schema examples, JSON encoder, body updates

- `@app.post(..., tags=["listings"], summary=..., deprecated=False)` — controls how `/docs` groups and labels the endpoint.
- `model_config = {"json_schema_extra": {"examples": [...]}}` on a Pydantic model — the example payload shown in Swagger.
- `jsonable_encoder(obj)` — turns a Pydantic model / datetime / UUID into plain JSON-safe types before handing it to something that isn't FastAPI-aware (e.g. writing to a non-ORM cache).
- **Body — Updates**: for `PATCH`, use `listing.model_dump(exclude_unset=True)` so you only overwrite fields the client actually sent, not every field with its default.

## 10. Dependencies (the big one)

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db          # "Dependencies with Yield": code after yield runs on teardown
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> User:
    ...                    # "Sub-dependencies": a dependency can itself depend on others

@app.get("/listings", dependencies=[Depends(rate_limit)])  # path-operation-level dependency, no return value used
def list_listings(db=Depends(get_db), user: User = Depends(get_current_user)):
    ...
```

- **Classes as dependencies**: a callable class (`__call__`) works as a dependency too — useful when the dependency needs constructor config (e.g. `RateLimiter(times=5, seconds=60)`).
- **Global dependencies**: `FastAPI(dependencies=[Depends(...)])` applies to every route in the app (e.g. a request-logging dependency).
- FastAPI caches a dependency's result **per request** by default — call `get_db` from three different places in the same request and it only runs once.

## 11. Security — OAuth2 & JWT

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form.username, form.password)
    if not user:
        raise HTTPException(401, "Incorrect username or password")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return db.get_user(payload["sub"])
```

`OAuth2PasswordBearer` doesn't implement auth itself — it's a dependency that (a) tells `/docs` to show an "Authorize" button and (b) extracts the `Authorization: Bearer <token>` header, 401-ing if it's missing. Real verification (password hash check, JWT decode/expiry) is on you. This is the direct foundation for Module 5's auth system.

## 12. Middleware (basics + CORS)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Process-Time"] = "..."
    return response
```

Middleware wraps *every* request/response, before routing decides which endpoint runs. Order matters — middleware added last runs first on the way in.

## 13. SQL databases with SQLModel

```python
from sqlmodel import SQLModel, Field, create_engine, Session

class Listing(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    price_cents: int
    seller_id: int = Field(foreign_key="user.id")

engine = create_engine("sqlite:///campus_marketplace.db")
SQLModel.metadata.create_all(engine)
```

SQLModel = Pydantic (validation) + SQLAlchemy (ORM/queries) fused into one class, so your API schema and DB table are (usually) the same class, removing a whole layer of duplicate model definitions. For anything beyond a toy app you'll still often split `ListingCreate`/`ListingOut`/`Listing(table=True)` — same "Extra Models" pattern as above.

## 14. Bigger applications — multiple files (APIRouter)

```python
# app/routers/listings.py
router = APIRouter(prefix="/listings", tags=["listings"])

@router.get("/")
def list_listings(): ...

# app/main.py
app.include_router(listings.router)
```

This is how a real app stays organized past ~5 endpoints: one router module per resource, wired together in `main.py`. Directly reused in Module 6's "API Versioning & Router Composition."

## 15. Background tasks, static files, metadata/docs config, testing

```python
from fastapi import BackgroundTasks

@app.post("/listings")
def create_listing(listing: ListingCreate, background_tasks: BackgroundTasks):
    saved = db.save(listing)
    background_tasks.add_task(send_new_listing_email, saved.id)  # runs AFTER response is sent
    return saved
```

- `BackgroundTasks` = fire-and-forget work that shouldn't delay the response (not a real task queue — for that you'd reach for Celery/RQ; fine for "send a notification").
- `app.mount("/static", StaticFiles(directory="static"))` serves listing photos directly.
- `FastAPI(title=..., version=..., docs_url=..., redoc_url=...)` configures the generated docs pages.
- **Testing**: `TestClient` (wraps `httpx`) lets you call your app in-process, no running server needed:

```python
from fastapi.testclient import TestClient
client = TestClient(app)

def test_create_listing():
    r = client.post("/listings", json={"title": "Textbook", "price_cents": 1500})
    assert r.status_code == 201
    assert r.json()["title"] == "Textbook"
```

This is exactly the pattern every `tests/` folder in this repo uses.
