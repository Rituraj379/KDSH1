# FastAPI Backend

Modern API replacement for the legacy Express backend. It keeps the same `/api/...`
contract used by the React app and adds a clean `/api/agent/chat` placeholder for
the future AI agent.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The seeded admin login is:

- Email: `admin2023@gmail.com`
- Password: `1234`

API docs are available at `http://localhost:8000/docs`.
