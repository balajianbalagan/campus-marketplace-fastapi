# Homework: Civic Complaint Tracker

Same shape as Campus Marketplace, different domain: **residents report civic issues
(potholes, broken streetlights, garbage pickup, graffiti...) and city staff manage them.**

You build this **on your own**, one module folder at a time, following the same build order
as Campus Marketplace (`in-class/campus-marketplace/`). Don't copy Campus Marketplace's code
wholesale — port the *patterns* (four-model shape, `Depends`-based auth, dependency factories
for RBAC) to this domain. That's the actual exercise.

| Folder | Maps to |
|---|---|
| `module-1-basics/` | Module 1 — FastAPI Basics |
| `module-5-auth/` | Module 5 — Blog API with Authentication |
| `module-6-advanced/` | Module 6 — Advanced Patterns |

## How to work each module

1. Read that module's `README.md` for the spec (endpoints, models, rules).
2. Open `starter/app/` — it has working scaffolding plus `# TODO` markers for exactly the
   parts that module is teaching. Everything not marked TODO already works; don't rewrite it.
3. Run the tests. They fail on purpose until your TODOs are done, and the failure messages
   tell you what's missing — same "run it, get told what's missing" loop as the platform.

```bash
cd module-1-basics/starter
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest ../tests -v
```

Use `python -m pytest`, not bare `pytest` — the `-m` form adds the current directory (where `app/` lives) to Python's import path, which bare `pytest` doesn't always do, and you'll get `ModuleNotFoundError: No module named 'app'` otherwise.

4. When all tests pass, run the server yourself and poke at `/docs` for five minutes before
   moving to the next module — reading green test output isn't the same as seeing it work.

## Grading rubric (self-check before submitting)

- [ ] All tests in that module's `tests/` folder pass.
- [ ] You did not delete/skip a test to make it pass.
- [ ] Every endpoint has a `response_model` (no leaking internal fields).
- [ ] Every DB-backed endpoint uses the `get_session` dependency, not a global connection.
- [ ] Errors use the right status code (400 bad input, 401 not authenticated, 403 not
      authorized, 404 not found, 422 automatic validation failure — you shouldn't be raising
      422 by hand).
