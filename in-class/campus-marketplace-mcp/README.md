# Campus Marketplace as an MCP Server

Turns the Campus Marketplace FastAPI app into an MCP (Model Context Protocol) server so
VS Code Copilot Chat can search, view, and create marketplace listings using plain English.

`server.py` is a thin adapter: each MCP "tool" just makes an HTTP call to the FastAPI app
running locally on `http://127.0.0.1:8000`. FastAPI still owns validation, auth, and the
database — MCP is just a new front door.

## 1. Install

```bash
cd in-class/campus-marketplace-mcp
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## 2. Start Campus Marketplace first

MCP tools call the REST API, so the API has to already be running:

```bash
cd ../campus-marketplace
uvicorn app.main:app --reload
```

Leave that terminal running. In a second terminal, sanity-check the MCP server on its own:

```bash
cd in-class/campus-marketplace-mcp
python -c "from server import mcp; print('OK:', mcp.name)"
```

(Optional) Use the MCP Inspector to poke at it directly before wiring it into VS Code:

```bash
npx @modelcontextprotocol/inspector python server.py
```

## 3. Connect it to VS Code Copilot

VS Code's Copilot Chat can launch and talk to local MCP servers via a workspace config file.

1. Copy the template at the repo root: `.vscode/mcp.json.example` → `.vscode/mcp.json`
   (the real `mcp.json` is gitignored since its Python path is machine-specific).
   On macOS/Linux, change `.venv/Scripts/python.exe` to `.venv/bin/python` in the copy.

   `type: "stdio"` matches `mcp.run(transport="stdio")` in `server.py` — VS Code starts the
   script as a subprocess and speaks MCP over its stdin/stdout, no port to configure.

2. Open the Command Palette → **"MCP: List Servers"** → confirm `campus-marketplace` shows up
   and is running (VS Code shows a green dot / "Running" status).
   - If it's not there, reload the window (Command Palette → **"Developer: Reload Window"**).
   - Requires a VS Code build with MCP support in Copilot Chat (Insiders, or a recent stable
     release with the MCP setting enabled — check **Settings → search "chat.mcp"**).

3. Open Copilot Chat, switch to **Agent mode**, and ask it something like:
   - *"Search Campus Marketplace for listings under $20."*
   - *"Log me in as alice with password s3cret! and post a listing for a used graphing calculator at $25."*

   Copilot should show it's calling the `search_listings` / `login` / `create_listing` tools,
   and return the same data you'd get calling the REST API directly.

## Troubleshooting

- **Tool calls fail with connection errors** → the FastAPI app (Step 2) isn't running, or is on a different port than `127.0.0.1:8000`.
- **`create_listing` says "Not logged in"** → call `login` first in the same chat session; the token is cached in-process and lost when the MCP server restarts.
- **VS Code doesn't see the server** → check the `command` path in `mcp.json` points at the venv's real Python interpreter, and that `server.py`'s absolute path is correct for your OS.
