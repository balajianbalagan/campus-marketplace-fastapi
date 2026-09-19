# Module 5: Simple UI

This stage keeps the SQLite CRUD API and adds a Streamlit screen. Start the API with `uvicorn app.main:app --reload`, then run `streamlit run streamlit_app.py` in a second terminal. The UI only talks to the API; it never opens SQLite directly.
