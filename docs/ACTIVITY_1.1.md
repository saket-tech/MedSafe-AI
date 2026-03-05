Activity 1.1: Python Environment and Dependency Installation

Overview

This activity focuses on creating a stable and isolated development environment for MedSafe AI by setting up a Python virtual environment and installing all required dependencies.

Objectives

1. Create and activate a dedicated virtual environment (medsafe_env)
2. Install all required dependencies from requirements.txt
3. Verify Python 3.10+ compatibility
4. Test library imports and ensure core components operate correctly

Tasks Completed

1. Virtual Environment Setup

Created and activated a Python virtual environment named medsafe_env to ensure:
- Dependency isolation from system Python
- Reproducible execution across different systems
- Clean package management

Commands used:
   python -m venv medsafe_env
   medsafe_env\Scripts\activate (Windows)

2. Dependency Installation

Installed all required dependencies using pip:

Core Dependencies:
- streamlit (1.55.0) - Web interface framework
- pytesseract (0.3.13) - OCR text extraction
- Pillow (11.3.0) - Image loading and processing
- rapidfuzz (3.14.3) - Fuzzy string matching for medicine detection
- ollama (0.6.1) - Local LLM interaction (LLaMA 3)
- pandas (2.3.2) - Data manipulation
- python-dateutil (2.9.0.post0) - Date/time handling

Supporting Dependencies:
- altair (6.0.0) - Data visualization
- protobuf (6.33.5) - Data serialization
- requests (2.32.5) - HTTP library
- numpy (2.2.6) - Numerical computing
- And other supporting libraries

Installation command:
   pip install streamlit pytesseract Pillow rapidfuzz ollama pandas python-dateutil

3. Python Version Verification

Verified Python version compatibility:
- Installed Version: Python 3.13.7
- Required Version: Python 3.10+
- Status: Compatible

Verification command:
   python --version

4. Library Import Testing

Created and executed test_imports.py to verify all core components:

Test Results:
- streamlit: PASSED
- PIL (Pillow): PASSED
- pytesseract: PASSED
- rapidfuzz: PASSED
- ollama: PASSED
- pandas: PASSED
- Standard libraries (json, datetime): PASSED

Overall Status: 7/7 imports successful

Test Components Verified:
- OCR processing capability (pytesseract, PIL)
- Fuzzy matching functionality (rapidfuzz)
- AI model interaction (ollama)
- UI rendering framework (streamlit)
- Data manipulation (pandas)

Deliverables

1. Active Virtual Environment
   - Location: D:\MedSafe AI\medsafe_env
   - Python Version: 3.13.7
   - Status: Active and functional

2. Installed Dependencies
   - All required packages installed
   - Verified via pip list
   - No dependency conflicts

3. requirements.txt File
   - Complete list of dependencies with versions
   - Enables reproducible installation
   - Ready for deployment

4. Import Verification Script
   - test_imports.py created
   - All imports tested successfully
   - Automated verification for future use

5. Documentation
   - This activity documentation
   - Installation verification results
   - Ready for mentor review

Verification Evidence

Python Version:
   Python 3.13.7

Installed Packages (Core):
   streamlit                 1.55.0
   pytesseract               0.3.13
   pillow                    11.3.0
   rapidfuzz                 3.14.3
   ollama                    0.6.1
   pandas                    2.3.2

Import Test Results:
   All 7/7 core dependencies imported successfully
   No runtime errors detected
   All components operational

Next Steps

With Activity 1.1 completed, the development environment is ready for:
- Activity 1.2: Project Structure Initialization
- Activity 1.3: Streamlit Application Initialization

The stable foundation ensures:
- Consistent execution across team members
- Isolated dependency management
- Verified component functionality
- Ready for core development work

