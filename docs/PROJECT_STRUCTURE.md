# Project Structure

This repository follows a strict split between frontend and backend.

## Source of truth

- `backend/`
  API routes, request models, config, and all backend service logic.
- `frontend/`
  Streamlit user interface and API client code.
- `tests/`
  Automated tests only.
- `scripts/`
  Utility scripts such as verification and performance checks.
- `data/`
  Application datasets used by backend services.
- `assets/`
  Sample media and non-code assets.
- `docs/`
  Documentation and generated reports.

## Root-level rules

Only these kinds of files belong at the repository root:

- project metadata: `README.md`, `requirements.txt`, `.gitignore`
- developer launchers: `start_backend.ps1`, `start_frontend.ps1`, `start_all.ps1`
- top-level folders listed above

## Developer rules

- Do not add business logic at the repo root.
- Do not add UI pages at the repo root.
- New backend code must go under `backend/`.
- New frontend code must go under `frontend/`.
- New automated tests must go under `tests/`.
- New helper scripts must go under `scripts/`.
- Sample images, videos, and archives must go under `assets/`.

## Current entry points

- Backend: `backend/app.py`
- Frontend: `frontend/streamlit_app.py`
- Tests: `tests/test_doc_cases.py`
