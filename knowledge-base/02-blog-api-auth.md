# Module 5 — Build a Blog API with Authentication (knowledge base)

6 lessons: Data Models Deep Dive → Database Connection → User Authentication → Authorization Levels → File Upload Magic → Error Handling Pro. This is where Campus Marketplace stops being toy code and gets real users, real passwords, and a real database.

## 1. Data Models Deep Dive

Separate models per *use*, not one model with everything optional:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str          # never on a response model
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str                 # plaintext, only ever exists in the request

class UserRead(UserBase):
    id: int                       # never includes hashed_password
```

Rule of thumb: if a field shouldn't leave the server (password hash, internal flags) it goes on the `table=True` model and is **absent** from every `*Read`/`*Out` model — don't rely on remembering to strip it at response time, make it structurally impossible.

## 2. Database Connection

```python
from sqlmodel import create_engine, Session

engine = create_engine("sqlite:///./marketplace.db", connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session
```

`get_session` is a dependency (Module 1's "Dependencies with Yield") — one session per request, closed automatically after the response is built, even on error. `check_same_thread=False` is SQLite-specific (needed because Starlette can serve one request per thread); Postgres/MySQL don't need it.

## 3. User Authentication

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

@app.post("/auth/register", response_model=UserRead, status_code=201)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    user = User(**user_in.model_dump(exclude={"password"}), hashed_password=hash_password(user_in.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/auth/login")
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Incorrect username or password")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}
```

Never store or compare plaintext passwords — `bcrypt` is a *slow-on-purpose* hash (resistant to brute force). Never say "user not found" vs "wrong password" separately in the error — that leaks which usernames exist.

## 4. Authorization Levels (RBAC)

```python
class Role(str, Enum):
    student = "student"
    moderator = "moderator"
    admin = "admin"

def require_role(*allowed: Role):
    def checker(user: User = Depends(get_current_user)):
        if user.role not in allowed:
            raise HTTPException(403, "Not enough permissions")
        return user
    return checker

@app.delete("/listings/{id}")
def delete_listing(id: int, user: User = Depends(require_role(Role.moderator, Role.admin))):
    ...
```

`require_role(...)` is a **dependency factory** — a function that returns a dependency, so you can parameterize it per-route. This is the standard FastAPI RBAC pattern: 401 = "I don't know who you are" (missing/invalid token), 403 = "I know who you are, and you're not allowed" (valid token, wrong role). Don't conflate the two.

## 5. File Upload Magic

```python
import uuid, shutil
from pathlib import Path as FSPath

UPLOAD_DIR = FSPath("uploads/listings")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/listings/{id}/photo")
async def upload_photo(id: int, photo: UploadFile = File(...), user: User = Depends(get_current_user)):
    if photo.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(400, "Only JPEG/PNG allowed")
    ext = photo.filename.rsplit(".", 1)[-1]
    dest = UPLOAD_DIR / f"{uuid.uuid4()}.{ext}"
    with dest.open("wb") as f:
        shutil.copyfileobj(photo.file, f)
    return {"photo_url": f"/static/listings/{dest.name}"}
```

Always generate your own filename (`uuid4`) — never trust the client's filename on disk (path traversal risk: `../../etc/passwd`). Validate `content_type` **and**, for anything security-sensitive, the actual file bytes (magic-number sniffing), since `content_type` is client-supplied and can be spoofed.

## 6. Error Handling Pro

```python
class MarketplaceError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code, self.detail = status_code, detail

@app.exception_handler(MarketplaceError)
def handle_marketplace_error(request, exc: MarketplaceError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

class ListingNotFound(MarketplaceError):
    def __init__(self, id: int):
        super().__init__(404, f"Listing {id} not found")
```

One exception hierarchy, one handler, consistent error JSON shape across the whole API — instead of `raise HTTPException(...)` scattered everywhere with slightly different `detail` formats. Pair with `RequestValidationError` override to make 422 validation errors match the same shape too.
