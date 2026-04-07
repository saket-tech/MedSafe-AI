# MedSafe AI

MedSafe AI is organized as a strict frontend/backend project.

## Project structure

- `backend/`: FastAPI API, request models, config, and backend services
- `frontend/`: Streamlit UI and API client
- `tests/`: automated test suite
- `scripts/`: verification and performance utilities
- `data/`: medicine and interaction datasets
- `assets/`: sample media
- `docs/`: documentation and reports

The current structure rules are documented in `docs/PROJECT_STRUCTURE.md`.

## Run the project

### Start backend

```powershell
.\start_backend.ps1
```

### Start frontend

```powershell
.\start_frontend.ps1
```

### Start both

```powershell
.\start_all.ps1
```

## Manual commands

```powershell
.\medsafe_env\Scripts\python.exe -m uvicorn backend.app:app --reload
.\medsafe_env\Scripts\python.exe -m streamlit run frontend/streamlit_app.py
```

## Verification

```powershell
.\medsafe_env\Scripts\python.exe scripts\test_imports.py
.\medsafe_env\Scripts\python.exe -m pytest tests\test_doc_cases.py -q
.\medsafe_env\Scripts\python.exe scripts\performance_test.py
```

## Notes

Some activity documents in `docs/` describe earlier milestone states of the project and may reference the old flat layout. The current source of truth for structure is `docs/PROJECT_STRUCTURE.md`.
