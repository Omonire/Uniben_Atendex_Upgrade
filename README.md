# AtendeX Grid Systems — Uniben Attendance Portal

## Layout

| Folder | Contents |
|---|---|
| `backend/` | Flask app (`index.py`), `requirements.txt`, `vercel.json` |
| `frontend/` | Jinja templates and static assets (css/js/img) |
| `docs/` | All documentation, deployment guides, and notes |
| `scripts/` | Smoke tests and data seeding utilities |

## Run (from repository root)

```powershell
venv\Scripts\python.exe backend\index.py
```

Environment is read from `.env` at the repository root (see `.env.example`).

App: http://127.0.0.1:5000

## Test

```powershell
venv\Scripts\python.exe scripts\smoke_test_local.py
```

## Docs

See [`docs/`](docs/) — start with `docs/README.md`, `docs/deployment.md`, `docs/env_keys.md`.
