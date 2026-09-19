# Campus Marketplace — Module 1 (basics)

The simplest possible version: one data model (`Listing`), three endpoints, no login. This
is the app built live — everything else in this repo builds on top of it.

## Run it

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

## Try the front end

In a second terminal (same venv):

```bash
streamlit run streamlit_app.py
```

A simple page opens in your browser: a form to post a listing, and a list of everything for
sale. It just calls the same API you're running above — no new concepts, just buttons
instead of Swagger.

## Run the tests

```bash
python -m pytest -v
```

## What's in here

- `app/models.py` — one class, `Listing`: `id`, `title`, `price_cents`, `seller_name`.
- `app/database.py` — SQLite connection + the `get_session` dependency.
- `app/main.py` — `GET /listings`, `GET /listings/{id}`, `POST /listings`.

## MCP (bonus, once the API works)

The last few lines of `app/main.py` turn this API into an MCP server with two lines:

```python
from fastapi_mcp import FastApiMCP
mcp = FastApiMCP(app)
mcp.mount()
```

No per-endpoint tool code — it reads your existing routes and turns each one into an MCP
tool automatically, served over SSE at `http://127.0.0.1:8000/mcp` while `uvicorn` is running.

To connect it to VS Code Copilot Chat:

1. Copy `.vscode/mcp.json.example` (repo root) to `.vscode/mcp.json` — it already has a
   `campus-marketplace-easy` entry pointing at that URL.
2. With `uvicorn app.main:app --reload` running, open the Command Palette →
   **"MCP: List Servers"** and confirm it shows up and is running.
3. Open Copilot Chat, switch to **Agent mode**, and ask something like *"List everything for
   sale on Campus Marketplace"* or *"Post a listing for a used bike at $40 from Sam."*

See `../campus-marketplace-mcp/README.md` for the hand-written version of the same idea.
