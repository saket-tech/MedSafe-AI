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

## Deploy on Render

This repository includes a ready-to-use Render blueprint in `render.yaml`.

### Services

- `medsafe-backend`: FastAPI API deployed from `backend/Dockerfile`
- `medsafe-frontend`: Streamlit UI deployed from `frontend/Dockerfile`

### Deploy steps

1. In Render, create a new Blueprint instance from this GitHub repository.
2. Render will create both web services from `render.yaml`.
3. The frontend receives `MEDSAFE_API_BASE_URL` automatically from the backend service.

### Deployment notes

- The backend Docker image installs `tesseract-ocr` for prescription OCR.
- The frontend pins `streamlit==1.41.0` to avoid blank-page/static-asset issues seen with newer unpinned builds on some hosted deployments.
- `ollama`-powered features are optional in production. If no Ollama server is available, the app falls back to its built-in non-AI logic for symptom, side-effect, and OCR parsing flows.
- The large local demo video at `assets/samples/MEDSAFE_DEMO.mp4` is intentionally excluded from GitHub and deployment builds.

## Notes

Some activity documents in `docs/` describe earlier milestone states of the project and may reference the old flat layout. The current source of truth for structure is `docs/PROJECT_STRUCTURE.md`.
