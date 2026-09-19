# Campus Marketplace reference project

This folder contains the same Campus Marketplace domain split into teaching stages. It has no accounts, passwords, roles, WebSockets, or rate limiting.

## What students build

- `module-1-basics/` uses in-memory listings for the first FastAPI routes.
- `module-2-database-crud/` adds SQLite, SQLModel, filters, and CRUD.
- `module-3-testing-docs/` focuses on Swagger and pytest.
- `module-5-ui/` adds a Streamlit client.
- `module-6-mcp/` mounts the existing routes as MCP tools.

## Start it

```powershell
cd module-2-database-crud
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Each module README gives its own run command.
