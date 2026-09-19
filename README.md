# Campus Marketplace — FastAPI

A learning kit built around three modules of [fastapiinteractive.com](https://fastapiinteractive.com):

| Site label | Folder | What it covers |
|---|---|---|
| Module 1 — FastAPI Basics | `knowledge-base/01-fastapi-basics.md` | routing, validation, a database, testing |
| Module 5 — Build a Blog API with Authentication | `knowledge-base/02-blog-api-auth.md` | user accounts, login, roles, file upload |
| Module 6 — Advanced FastAPI Patterns | `knowledge-base/03-advanced-patterns.md` | live updates (websockets), rate limiting |

## How this repo is organized

- **`knowledge-base/`** — full written reference for all three modules. Concept, minimal example, common mistakes, and where it shows up in the code here.
- **`in-class/campus-marketplace/`** — the reference app, split into three folders you can run independently, each building on the last:
  - `module-1-basics/` — the core app: one data model, three endpoints, no login, plus a tiny Streamlit front end and an MCP server built in with two lines of code.
  - `module-5-auth/` — adds user accounts, login, and roles.
  - `module-6-advanced/` — adds live websocket notifications and rate limiting.
- **`in-class/campus-marketplace-mcp/`** — a hand-written MCP server (one Python function per tool) showing what `FastApiMCP` is doing under the hood.
- **`exercises/`** — short, focused boilerplate exercises (one concept each): starter code with `TODO`s + a pytest suite that tells you exactly what's missing when you run it.
- **`homework/civic-complaint-tracker/`** — a parallel project to build **on your own**, module by module, mirroring Campus Marketplace but for a different domain (residents reporting civic issues instead of students trading items). Each module folder has its own README, starter boilerplate, and a self-checking test suite.

## Quick start

```bash
cd in-class/campus-marketplace/module-1-basics
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs

# in a second terminal, same folder + venv:
streamlit run streamlit_app.py
```

## Two ways to get MCP

- **The easy way** (`module-1-basics/app/main.py`, and the same two lines in `module-5-auth`
  and `module-6-advanced`): `FastApiMCP(app).mount()` turns every existing route into an MCP
  tool automatically, straight from the app's OpenAPI schema. No new code per endpoint.
- **The explicit way** (`in-class/campus-marketplace-mcp/`): one Python function per tool,
  each calling the REST API directly. More code, but it shows exactly what an MCP tool call
  actually does.

## Suggested learning path

1. Read `knowledge-base/01-fastapi-basics.md`, then `02-blog-api-auth.md`, then `03-advanced-patterns.md`.
2. Run `in-class/campus-marketplace/module-1-basics/` — hit the endpoints in `/docs`, try the Streamlit page, then connect it to VS Code Copilot via MCP.
3. Explore `module-5-auth/` and `module-6-advanced/` to see the same app grow.
4. Work through `exercises/`, module by module.
5. Build `homework/civic-complaint-tracker/` on your own, module by module, self-graded via `pytest`.
