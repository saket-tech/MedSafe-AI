"""Basic environment and project import verification."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

print("=" * 60)
print("MedSafe AI - Dependency Verification Test")
print("=" * 60)
print(f"\nPython Version: {sys.version}")
print("-" * 60)

test_results = []

checks = [
    ("streamlit", "import streamlit"),
    ("Pillow", "from PIL import Image"),
    ("pytesseract", "import pytesseract"),
    ("rapidfuzz", "from rapidfuzz import process, fuzz"),
    ("ollama", "import ollama"),
    ("pandas", "import pandas"),
    ("fastapi", "import fastapi"),
    ("requests", "import requests"),
    ("backend.app", "from backend.app import app"),
    ("frontend.streamlit_app", "from frontend.streamlit_app import main"),
]

for name, statement in checks:
    try:
        exec(statement, {})
        print(f"[OK] {name} imported successfully")
        test_results.append((name, True))
    except Exception as exc:
        print(f"[FAIL] {name} import failed: {exc}")
        test_results.append((name, False))

print("-" * 60)
passed = sum(1 for _, result in test_results if result)
total = len(test_results)
print(f"\nTest Summary: {passed}/{total} imports successful")

if passed == total:
    print("\nAll dependencies are correctly installed.")
else:
    failed = [name for name, result in test_results if not result]
    print(f"\nFailed imports: {', '.join(failed)}")

print("=" * 60)
