import os


def _normalize_api_base_url(value: str) -> str:
    value = value.strip()
    if not value:
        return "http://localhost:8000"
    if value.startswith(("http://", "https://")):
        return value.rstrip("/")
    return f"http://{value.rstrip('/')}"


API_BASE_URL = _normalize_api_base_url(
    os.getenv("MEDSAFE_API_BASE_URL", "http://localhost:8000")
)
