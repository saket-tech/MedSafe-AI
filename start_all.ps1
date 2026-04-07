$ErrorActionPreference = "Stop"
$backend = Join-Path $PSScriptRoot "start_backend.ps1"
$frontend = Join-Path $PSScriptRoot "start_frontend.ps1"
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$backend`""
Start-Sleep -Seconds 3
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$frontend`""
Write-Host "Started backend and frontend in separate windows."
