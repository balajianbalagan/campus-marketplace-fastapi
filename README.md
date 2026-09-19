# Campus Marketplace — FastAPI

A learning kit built around three modules of [fastapiinteractive.com](https://fastapiinteractive.com):

| Site label | Folder | What it covers |
|---|---|---|
| Module 1 — FastAPI Basics | `knowledge-base/01-fastapi-basics.md` | routing, validation, dependencies, security basics, SQLModel, testing |
| Module 5 — Build a Blog API with Authentication | `knowledge-base/02-blog-api-auth.md` | data modeling, DB integration, auth, RBAC, file upload, error handling |
| Module 6 — Advanced FastAPI Patterns | `knowledge-base/03-advanced-patterns.md` | async, websockets, middleware, rate limiting, caching, versioning |

## How this repo is organized

- **`knowledge-base/`** — full written reference for all three modules (plus a course map for the rest of the platform's modules). Concept, minimal example, common mistakes, and where it shows up in the code here.
- **`in-class/campus-marketplace/`** — a complete, working reference implementation: FastAPI + SQLModel + SQLite, with auth, RBAC, file upload, websockets, and rate limiting.
- **`in-class/campus-marketplace-mcp/`** — the same marketplace, exposed as an MCP server so VS Code Copilot Chat can query/create listings directly.
- **`exercises/`** — short, focused boilerplate exercises (one concept each): starter code with `TODO`s + a pytest suite that tells you exactly what's missing when you run it.
- **`homework/civic-complaint-tracker/`** — a parallel project to build **on your own**, module by module, mirroring Campus Marketplace but for a different domain (residents reporting civic issues instead of students trading items). Each module folder has its own README, starter boilerplate, and a self-checking test suite.

## Quick start

```bash
cd in-class/campus-marketplace
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

## Suggested learning path

1. Read `knowledge-base/01-fastapi-basics.md`, then `02-blog-api-auth.md`, then `03-advanced-patterns.md`.
2. Explore `in-class/campus-marketplace/` — run it, hit the endpoints in `/docs`, read the code alongside the knowledge base.
3. Try the MCP + VS Code Copilot integration in `in-class/campus-marketplace-mcp/`.
4. Work through `exercises/`, module by module.
5. Build `homework/civic-complaint-tracker/` on your own, module by module, self-graded via `pytest`.
