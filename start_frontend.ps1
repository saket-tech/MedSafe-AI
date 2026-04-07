$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot "medsafe_env\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Virtual environment Python not found at $python"
}
$env:MEDSAFE_API_BASE_URL = if ($env:MEDSAFE_API_BASE_URL) { $env:MEDSAFE_API_BASE_URL } else { "http://localhost:8000" }
& $python -m streamlit run frontend/streamlit_app.py
