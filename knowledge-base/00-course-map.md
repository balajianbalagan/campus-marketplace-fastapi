# Course Map — fastapiinteractive.com

Full module list as published on the site (numbering is theirs; content mapping below is what this repo covers).

| # | Title | Lessons | Hours | Covered here |
|---|---|---|---|---|
| 1 | FastAPI Basics | 45 | 42 | **Core** — `01-fastapi-basics.md` |
| 2–4 | (platform's intermediate tracks — data validation deep dives, ORMs, deployment; not covered here) | — | — | Reference only, skim if curious |
| 5 | Build a Blog API with Authentication | 6 | 5 | **Core** — `02-blog-api-auth.md` |
| 6 | Advanced FastAPI Patterns | 10 | 8 | **Core** — `03-advanced-patterns.md` |

**Why only 1, 5, 6:** Module 1 is the vocabulary (routing, validation, dependencies) everything else depends on. Module 5 is where "toy endpoint" becomes "real app with a database and users" — the exact shape Campus Marketplace needs. Module 6 is what makes it feel production-grade (websockets for live "new listing" notifications, rate limiting, caching) and sets up the MCP demo.

Every lesson on the platform ships with **its own test suite** — run it and it tells you precisely what's missing before you move on. We mirror that pattern in `exercises/` and `homework/` here: starter code + `pytest` + a message telling you what to fix.

## Reading order

1. `01-fastapi-basics.md`
2. `02-blog-api-auth.md`
3. `03-advanced-patterns.md`

Each file is self-contained: concept, minimal example, common mistakes, and where it shows up in Campus Marketplace / Civic Complaint Tracker.
