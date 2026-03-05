Activity 1.2: Project Structure Initialization

Overview

This activity focuses on organizing the MedSafe AI project into a clear and maintainable modular structure using separate Python files for different concerns. This modular organization ensures scalability, easier debugging, and cleaner integration between deterministic logic and AI-driven components.

Objectives

1. Create modular Python files to separate concerns
2. Organize project structure for maintainability and scalability
3. Implement placeholder functions for future development
4. Establish clear interfaces between components
5. Prepare foundation for Activities 2.1, 2.2, and 2.3

Project Structure Created

MedSafe AI/
├── streamlit_app.py          Main Streamlit application and UI
├── med_db.py                  Medicine database and interaction metadata
├── symptom.py                 Rule-based symptom advice logic
├── ocr_utils.py               Prescription OCR and text extraction utilities
├── risk_engine.py             Emergency risk scoring and safety rules
├── data/                      Data storage directory
│   ├── medicines.json         Medicine database
│   └── interactions.json      Interaction rules
├── test_imports.py            Dependency verification script
├── docs/                      Documentation directory
│   ├── PREREQUISITES.md       Prerequisites documentation
│   ├── WORKFLOW.md            Workflow documentation
│   ├── ACTIVITY_1.1.md        Activity 1.1 documentation
│   └── ACTIVITY_1.2.md        Activity 1.2 documentation (this file)
└── requirements.txt           Python dependencies

Key Components

1. streamlit_app.py - Front-end Interface and Main Application Logic

Purpose: Main entry point for the Streamlit web application

Features:
- Multi-tab navigation interface
- Home page with project overview
- Medicine Interaction Checker tab
- Prescription OCR tab
- Symptom & Doubt Solver tab
- Side-Effect Monitor tab
- Emergency Risk Predictor tab

Key Functions:
- Page configuration and layout
- Tab-based navigation
- User input handling (placeholders)
- Integration points for backend modules

Status: UI skeleton created, ready for Activity 3.1 enhancement

2. med_db.py - Medicine Database and Interaction Metadata

Purpose: Manages medicine data, interactions, and database operations

Classes:
- MedicineDatabase: Main database management class

Key Methods:
- load_medicines(): Load medicine database from JSON
- load_interactions(): Load interaction rules from JSON
- get_medicine(name): Retrieve medicine information
- check_interactions(medicines): Check for drug interactions
- search_medicine(query): Search for medicines

Data Structure:
- medicines.json: Medicine properties and metadata
- interactions.json: Drug interaction rules

Status: Structure created, ready for Activity 2.1 implementation

3. symptom.py - Rule-based Symptom Advice Logic

Purpose: Provides symptom analysis and guidance

Classes:
- SymptomAnalyzer: Symptom analysis engine

Key Methods:
- analyze_symptoms(description): Analyze symptom description
- get_home_remedies(symptom): Retrieve home remedies
- get_lifestyle_suggestions(symptom): Get lifestyle advice
- check_warning_signs(symptoms): Identify warning signs

Features:
- Rule-based symptom guidance
- Home remedy suggestions
- Lifestyle recommendations
- Warning sign detection

Status: Structure created, ready for Activity 2.3 implementation

4. ocr_utils.py - Prescription OCR and Text Extraction Utilities

Purpose: Handles OCR processing and text extraction from prescription images

Classes:
- OCREngine: OCR processing engine

Key Methods:
- extract_text(image_path): Extract text from image file
- extract_text_from_pil(pil_image): Extract text from PIL Image
- preprocess_image(image): Image preprocessing for better OCR
- parse_medicines_from_text(text): Parse medicine names
- extract_structured_data(text): AI-based structured extraction

Features:
- Tesseract OCR integration
- Image preprocessing
- Medicine name parsing
- Structured data extraction (with AI)

Status: Structure created, ready for Activity 2.2 implementation

5. risk_engine.py - Emergency Risk Scoring and Safety Rules

Purpose: Calculates emergency risk scores and provides safety guidance

Classes:
- RiskLevel: Enum for risk severity (LOW, MEDIUM, HIGH)
- RiskEngine: Risk calculation engine

Key Methods:
- calculate_risk_score(symptoms, severity): Calculate risk score
- get_recommendation(risk_level): Get safety recommendations
- classify_severity(symptoms): Classify overall severity
- generate_safety_note(assessment): Generate AI safety notes

Features:
- Rule-based risk scoring
- Severity classification
- Safety recommendations
- Transparent risk calculation

Status: Structure created, ready for Activity 2.3 implementation

Data Files

1. data/medicines.json

Sample medicine database with:
- Medicine names
- Standard dosages
- Known interactions
- Special warnings (e.g., grapefruit interactions)

Sample entries:
- Atorvastatin
- Metformin
- Amoxicillin
- Ibuprofen
- Lisinopril

2. data/interactions.json

Sample interaction rules with:
- Medicine pairs
- Severity levels
- Interaction descriptions

Sample interactions:
- Atorvastatin + Clarithromycin
- Ibuprofen + Aspirin
- Ibuprofen + Warfarin

Modular Organization Benefits

1. Scalability
   - Easy to add new features
   - Independent module development
   - Clear separation of concerns

2. Maintainability
   - Easier debugging
   - Isolated testing
   - Clear code organization

3. Collaboration
   - Multiple developers can work on different modules
   - Reduced merge conflicts
   - Clear module ownership

4. Integration
   - Clean interfaces between components
   - Deterministic logic separated from AI components
   - Easy to swap implementations

Module Integration Flow

User Input (Streamlit UI)
    ↓
streamlit_app.py (Main Application)
    ↓
    ├→ med_db.py (Medicine Database)
    ├→ ocr_utils.py (OCR Processing)
    ├→ symptom.py (Symptom Analysis)
    └→ risk_engine.py (Risk Scoring)
    ↓
AI Integration (LLaMA 3 via Ollama)
    ↓
Results Display (Streamlit UI)

Testing and Verification

Module Import Test:

All modules can be imported successfully:
- streamlit_app.py: Main application
- med_db.py: MedicineDatabase class
- symptom.py: SymptomAnalyzer class
- ocr_utils.py: OCREngine class
- risk_engine.py: RiskEngine class

Data Files Test:

All data files are valid JSON:
- data/medicines.json: Valid
- data/interactions.json: Valid

Structure Verification:

Project structure matches requirements:
- Modular Python files created
- Data directory established
- Documentation organized
- Clear separation of concerns

Deliverables

1. Modular Python Files
   - streamlit_app.py (Main application)
   - med_db.py (Medicine database)
   - symptom.py (Symptom analysis)
   - ocr_utils.py (OCR utilities)
   - risk_engine.py (Risk scoring)

2. Data Directory
   - medicines.json (Sample medicine database)
   - interactions.json (Sample interaction rules)

3. Project Structure
   - Clear folder organization
   - Logical file naming
   - Consistent code structure

4. Documentation
   - This activity documentation
   - Code comments and docstrings
   - Module descriptions

5. Integration Points
   - Clear interfaces between modules
   - Placeholder functions for future implementation
   - Ready for Activities 2.1, 2.2, and 2.3

Next Steps

With Activity 1.2 completed, the project structure is ready for:

Activity 1.3: Streamlit Application Initialization
- Test streamlit_app.py
- Verify UI navigation
- Validate module imports

Activity 2.1: Medicine Interaction & Identification Module Development
- Implement fuzzy matching in med_db.py
- Complete interaction checking logic
- Integrate with medicine database

Activity 2.2: Prescription OCR and AI-Based Extraction Engine
- Implement OCR text extraction in ocr_utils.py
- Add AI-based medicine parsing
- Integrate with LLaMA 3

Activity 2.3: Symptom Interpretation, Side-Effect Analysis, and Risk Scoring Engine
- Complete symptom analysis in symptom.py
- Implement risk scoring in risk_engine.py
- Add AI-generated explanations
