"""
Test script to verify all required libraries are installed and importable.
This validates Activity 1.1: Python Environment and Dependency Installation
"""

import sys

print("=" * 60)
print("MedSafe AI - Dependency Verification Test")
print("=" * 60)
print(f"\nPython Version: {sys.version}")
print("-" * 60)

# Test imports
test_results = []

# Test 1: Streamlit
try:
    import streamlit as st
    print("✓ streamlit imported successfully")
    test_results.append(("streamlit", True))
except ImportError as e:
    print(f"✗ streamlit import failed: {e}")
    test_results.append(("streamlit", False))

# Test 2: PIL (Pillow)
try:
    from PIL import Image
    print("✓ PIL (Pillow) imported successfully")
    test_results.append(("Pillow", True))
except ImportError as e:
    print(f"✗ PIL import failed: {e}")
    test_results.append(("Pillow", False))

# Test 3: pytesseract
try:
    import pytesseract
    print("✓ pytesseract imported successfully")
    test_results.append(("pytesseract", True))
except ImportError as e:
    print(f"✗ pytesseract import failed: {e}")
    test_results.append(("pytesseract", False))

# Test 4: rapidfuzz
try:
    from rapidfuzz import process, fuzz
    print("✓ rapidfuzz imported successfully")
    test_results.append(("rapidfuzz", True))
except ImportError as e:
    print(f"✗ rapidfuzz import failed: {e}")
    test_results.append(("rapidfuzz", False))

# Test 5: ollama
try:
    from ollama import Client
    print("✓ ollama imported successfully")
    test_results.append(("ollama", True))
except ImportError as e:
    print(f"✗ ollama import failed: {e}")
    test_results.append(("ollama", False))

# Test 6: pandas
try:
    import pandas
    print("✓ pandas imported successfully")
    test_results.append(("pandas", True))
except ImportError as e:
    print(f"✗ pandas import failed: {e}")
    test_results.append(("pandas", False))

# Test 7: Standard libraries
try:
    import json
    import datetime
    from datetime import datetime
    print("✓ Standard libraries (json, datetime) imported successfully")
    test_results.append(("standard libraries", True))
except ImportError as e:
    print(f"✗ Standard library import failed: {e}")
    test_results.append(("standard libraries", False))

# Summary
print("-" * 60)
passed = sum(1 for _, result in test_results if result)
total = len(test_results)
print(f"\nTest Summary: {passed}/{total} imports successful")

if passed == total:
    print("\n✓ All dependencies are correctly installed!")
    print("Activity 1.1 verification: PASSED")
else:
    print("\n✗ Some dependencies failed to import")
    print("Activity 1.1 verification: FAILED")
    failed = [name for name, result in test_results if not result]
    print(f"Failed imports: {', '.join(failed)}")

print("=" * 60)
