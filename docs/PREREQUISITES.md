Prerequisites - MedSafe AI

Overview

Before using MedSafe AI, ensure that your development environment is properly configured. The following components and tools are required to run the application smoothly and enable all AI-powered features.

1. Python Environment Setup

MedSafe AI is developed using Python 3.10+, leveraging libraries for web deployment, OCR processing, fuzzy matching, rule-based logic, and AI model interaction.

Requirements:
- Python version: 3.10 or higher
- Virtual environment tool: venv (included with Python)

Installation:
1. Download Python from: https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Verify installation:
   python --version

Virtual Environment Setup:
Create and activate a dedicated virtual environment (e.g., medsafe_env) to isolate dependencies and maintain a clean setup.

Windows:
   python -m venv medsafe_env
   medsafe_env\Scripts\activate

Linux/Mac:
   python3 -m venv medsafe_env
   source medsafe_env/bin/activate

Reference:
- Official Python documentation: https://www.python.org/downloads/
- Virtual environment guide: https://docs.python.org/3/library/venv.html

2. Streamlit Installation and Configuration

Streamlit powers the interactive front-end dashboard of MedSafe AI, enabling tab-based navigation, real-time analysis, and user-friendly visual outputs.

Installation:
   pip install streamlit

Or install via requirements.txt:
   pip install -r requirements.txt

Verification:
   streamlit --version

Key Features Used:
- Multi-tab interface
- File upload widgets
- Real-time data visualization
- Session state management
- Custom styling

Reference:
- Streamlit documentation: https://docs.streamlit.io/library/get-started/installation
- Introductory tutorial: https://www.youtube.com/watch?v=JwSS70SZdyM
- Components gallery: https://streamlit.io/components

3. OCR Engine Setup (Tesseract OCR)

MedSafe AI uses Tesseract OCR to extract text from uploaded prescription images. Proper installation and configuration are required.

Installation:

Windows:
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (e.g., tesseract-ocr-w64-setup-5.3.x.exe)
3. Note the installation path (usually C:\Program Files\Tesseract-OCR)
4. Add to system PATH if not done automatically

Linux (Ubuntu/Debian):
   sudo apt update
   sudo apt install tesseract-ocr

Mac:
   brew install tesseract

Verification:
   tesseract --version

Configuration:
The Tesseract executable path must be correctly configured in the code. Default paths:
- Windows: C:\Program Files\Tesseract-OCR\tesseract.exe
- Linux: /usr/bin/tesseract
- Mac: /usr/local/bin/tesseract

Reference:
- Official repository: https://github.com/tesseract-ocr/tesseract
- Documentation: https://tesseract-ocr.github.io/

4. Library Installation and Core Dependencies

MedSafe AI relies on several Python libraries for text extraction, fuzzy matching, AI interaction, and UI rendering. All dependencies can be installed using a requirements.txt file.

Key Libraries:

- streamlit (1.31.0) - Interactive web interface
- pytesseract (0.3.10) - OCR text extraction
- Pillow/PIL (10.2.0) - Image loading and processing
- rapidfuzz (3.6.1) - Fuzzy string matching for medicine detection
- ollama (0.1.6) - Local LLM interaction (LLaMA 3)
- pandas (2.2.0) - Data manipulation
- python-dateutil (2.8.2) - Date/time handling

Installation:
   pip install -r requirements.txt

Verification:
   pip list

5. LLM Runtime Setup (Ollama)

MedSafe AI uses LLaMA 3 via Ollama for AI-powered summarization, extraction, and explanation tasks.

Installation:

Windows:
1. Download from: https://ollama.com/download
2. Run the installer
3. Ollama will run as a background service

Linux:
   curl -fsSL https://ollama.com/install.sh | sh

Mac:
   brew install ollama

Pull the LLaMA 3 Model:
   ollama pull llama3

Verification:
   ollama list

You should see llama3 in the list.

Start Ollama Service (if needed):
   ollama serve

Reference:
- Ollama documentation: https://ollama.com
- Model library: https://ollama.com/library

6. Development Environment

A modern IDE is recommended for efficient development, testing, and debugging of the MedSafe AI codebase.

Recommended IDEs:

Visual Studio Code (Recommended)
- Download: https://code.visualstudio.com/
- Extensions:
  - Python (Microsoft)
  - Pylance
  - Streamlit Snippets

PyCharm Community Edition
- Download: https://www.jetbrains.com/pycharm/download/

Git for Version Control:
   git --version

If not installed:
- Download: https://git-scm.com/downloads

7. Optional Learning and Reference Resources

For deeper understanding and customization of MedSafe AI components:

- Streamlit Components Gallery: https://streamlit.io/components
- Tesseract OCR Documentation: https://tesseract-ocr.github.io/
- RapidFuzz Documentation: https://maxbachmann.github.io/RapidFuzz/
- Prompt Engineering for LLMs: https://www.promptingguide.ai/
- Python Best Practices: https://docs.python-guide.org/

