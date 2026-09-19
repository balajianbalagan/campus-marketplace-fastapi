# CEG-CAF FastAPI: Campus Marketplace

A deliberately small teaching repository for one finished outcome:

- a Campus Marketplace REST API built with FastAPI and SQLite;
- a small Streamlit UI that calls that API; and
- the same API exposed as MCP tools for VS Code Copilot.

Authentication, roles, WebSockets, rate limiting, file uploads, background jobs, and deployment are out of scope. They add setup and failure modes without helping this course's core outcome.

## Course ownership

| Module | Owner | Focus |
|---|---|---|
| 1 | You | FastAPI foundations, request/response models, Swagger, and the first API calls |
| 2 | Your colleague | project structure, SQLite, SQLModel, and CRUD |
| 3 | Your colleague | testing the API in `/docs` and with pytest |
| 5 | You | Streamlit UI as a client of the API |
| 6 | You | MCP annotation and VS Code Copilot consumption |

The modules use the same Marketplace domain in separate, independently runnable folders. Each stage adds one visible part of the final app.

## Run the project locally

```powershell
cd in-class/campus-marketplace/module-6-mcp
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to make API calls. In a second terminal, from the same folder and environment:

```powershell
streamlit run streamlit_app.py
```

The UI opens in a browser and calls the FastAPI API. SQLite creates `campus_marketplace.db` automatically; it is ignored by Git.

## Using FastAPI Interactive

Use [FastAPI Interactive Playground](https://www.fastapiinteractive.com/playground) for short live examples and the first SQLite experiments. It runs FastAPI, SQLModel, and SQLite in the browser. Use the local project for the Streamlit UI and the Copilot MCP demo, because Copilot needs to reach a running MCP endpoint.

## API surface

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/listings` | browse listings; optional `q` and `max_price_cents` filters |
| `GET` | `/listings/{listing_id}` | read one listing |
| `POST` | `/listings` | create a listing |
| `PUT` | `/listings/{listing_id}` | update fields on a listing |
| `DELETE` | `/listings/{listing_id}` | remove a listing |

## Copilot MCP demo

`module-6-mcp/app/main.py` mounts `FastApiMCP`, which reads the FastAPI OpenAPI routes and exposes them at `http://127.0.0.1:8000/mcp`. No login state or custom MCP tools are needed.

1. Start the API with `uvicorn app.main:app --reload`.
2. Copy `.vscode/mcp.json.example` to `.vscode/mcp.json`.
3. In VS Code, run **MCP: List Servers** and check that `campus-marketplace` is running.
4. In Copilot Chat agent mode, try: `List Campus Marketplace listings under 1000 rupees` or `Create a listing for a used calculator for 500 rupees from Asha`.

## Homework

There are no time-boxed in-class exercises. The single homework brief is [Civic Complaint Tracker](homework/civic-complaint-tracker/README.md). Students have longer to build a comparable SQLite API, UI, tests, and MCP configuration in a different domain.

## Repository map

- `in-class/campus-marketplace/module-1-basics/` - routes, Pydantic models, and Swagger using in-memory data.
- `in-class/campus-marketplace/module-2-database-crud/` - SQLite, SQLModel, filters, and CRUD.
- `in-class/campus-marketplace/module-3-testing-docs/` - the same API with a testing and documentation focus.
- `in-class/campus-marketplace/module-5-ui/` - the SQLite API plus Streamlit UI.
- `in-class/campus-marketplace/module-6-mcp/` - the SQLite API exposed to Copilot over MCP.
- `homework/civic-complaint-tracker/` - one substantial take-home assignment.
- `knowledge-base/` - concise module notes aligned with the revised course.
- `course-materials/` - the revised teaching deck.
