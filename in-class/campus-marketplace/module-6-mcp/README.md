# Module 6: MCP and Copilot

Use Python 3.14.7 for this module. Create and activate the virtual environment before installing the pinned dependencies in `requirements.txt`.

This final stage adds `FastApiMCP(app)` after the same SQLite CRUD routes. Start `uvicorn app.main:app --reload`, then connect Copilot to `http://127.0.0.1:8000/mcp` using the repo's `.vscode/mcp.json.example`. Ask Copilot to list listings or create one. No custom tool functions, authentication, or WebSockets are included.
