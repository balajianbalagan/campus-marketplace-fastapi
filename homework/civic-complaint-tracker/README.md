# Homework: Civic Complaint Tracker

Build one complete, SQLite-backed FastAPI project over the course. This replaces short in-class exercises and the previous module-by-module homework series.

## Required outcome

Your application lets residents create and browse civic complaints. It must include:

- a SQLite database connected through SQLModel;
- `GET /complaints`, `GET /complaints/{complaint_id}`, `POST /complaints`, `PUT /complaints/{complaint_id}`, and `DELETE /complaints/{complaint_id}`;
- optional `category` and `status` filters on the list route;
- request validation and a 404 response for a missing complaint;
- a small Streamlit UI that creates and lists complaints through the API;
- pytest tests for create, read, update, delete, filters, and the missing-record case; and
- an MCP mount plus a `.vscode/mcp.json` configuration so Copilot can browse and create complaints.

Do not add user accounts, JWTs, roles, WebSockets, rate limiting, uploads, or deployment work.

## Suggested milestones

| When | Deliverable |
|---|---|
| After Module 1 | `GET /complaints` and `POST /complaints` work in `/docs` |
| After Modules 2-3 | SQLite, all CRUD routes, and passing tests |
| After Module 5 | Streamlit UI calls the API |
| After Module 6 | Copilot can use the MCP endpoint |

Start from `starter/`. The starter intentionally leaves route bodies for you to implement.

```powershell
cd homework/civic-complaint-tracker/starter
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
python -m pytest ../tests -v
```

Use FastAPI Interactive for quick experiments. Complete and demonstrate the final UI and Copilot MCP flow locally.
