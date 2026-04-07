$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot "medsafe_env\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Virtual environment Python not found at $python"
}
& $python -m uvicorn backend.app:app --reload
