"""
MedSafe AI - Main Streamlit Application
Front-end interface and main application logic
"""

import streamlit as st
from PIL import Image
import json
from datetime import datetime
from med_db import MedicineDatabase
from ocr_utils import OCREngine
from symptom import SymptomAnalyzer
from risk_engine import RiskEngine

# Page configuration
st.set_page_config(
    page_title="MedSafe AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("💊 MedSafe AI - AI-Driven Medical Safety Assistant")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module:",
    [
        "🏠 Home",
        "💊 Medicine Interaction Checker",
        "📄 Prescription OCR",
        "🩺 Symptom & Doubt Solver",
        "⚠️ Side-Effect Monitor",
        "🚨 Emergency Risk Predictor"
    ]
)

# Home page
if page == "🏠 Home":
    st.header("Welcome to MedSafe AI")
    st.write("""
    MedSafe AI is an intelligent healthcare assistance platform designed to enhance 
    medicine safety awareness, symptom understanding, and early risk identification.
    
    **Key Features:**
    - Medicine Interaction Checker
    - Prescription OCR and Analysis
    - Symptom Guidance and Advice
    - Side-Effect Monitoring
    - Emergency Risk Assessment
    
    **Note:** This is an educational tool and does not replace professional medical consultation.
    """)

# Medicine Interaction Checker
elif page == "💊 Medicine Interaction Checker":
    st.header("Medicine Interaction Checker")
    st.write("Check potential drug-drug interactions using fuzzy matching")
    
    # Initialize medicine database
    if 'med_db' not in st.session_state:
        st.session_state.med_db = MedicineDatabase()
        st.session_state.med_db.load_medicines()
        st.session_state.med_db.load_interactions()
    
    med_db = st.session_state.med_db
    
    # Input area for medicines
    medicines_input = st.text_area(
        "Enter medicine names (one per line):",
        height=150,
        placeholder="Example:\nAtorvastatin\nIbuprofen\nMetformin"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        check_button = st.button("Check Interactions", type="primary")
    with col2:
        if st.button("Clear"):
            st.rerun()
    
    if check_button and medicines_input:
        # Parse medicine names
        medicine_list = [med.strip() for med in medicines_input.split('\n') if med.strip()]
        
        if len(medicine_list) == 0:
            st.warning("Please enter at least one medicine name.")
        else:
            st.markdown("---")
            st.subheader("Analysis Results")
            
            # Step 1: Identify medicines using fuzzy matching
            st.markdown("### 🔍 Medicine Identification")
            identified_medicines = []
            
            for med_input in medicine_list:
                match = med_db.find_medicine(med_input, threshold=70)
                
                if match:
                    identified_medicines.append(match['name'])
                    confidence = match['confidence']
                    
                    if confidence == 100:
                        st.success(f"✅ **{med_input}** → Exact match: **{match['data']['name']}**")
                    else:
                        st.info(f"🔍 **{med_input}** → Found: **{match['data']['name']}** (Confidence: {confidence}%)")
                else:
                    st.error(f"❌ **{med_input}** → Not found in database")
            
            # Step 2: Check for interactions
            if len(identified_medicines) >= 2:
                st.markdown("---")
                st.markdown("### ⚠️ Interaction Analysis")
                
                interactions = med_db.check_interactions(identified_medicines)
                
                if interactions:
                    st.warning(f"Found {len(interactions)} potential interaction(s)")
                    
                    for idx, interaction in enumerate(interactions, 1):
                        severity = interaction['severity']
                        
                        # Color code by severity
                        if severity == 'high':
                            st.error(f"**Interaction {idx}: HIGH SEVERITY**")
                        elif severity == 'moderate':
                            st.warning(f"**Interaction {idx}: MODERATE SEVERITY**")
                        else:
                            st.info(f"**Interaction {idx}: {severity.upper()} SEVERITY**")
                        
                        st.write(f"**Medicines:** {interaction['medicine1'].title()} + {interaction['medicine2'].title()}")
                        st.write(f"**Description:** {interaction['description']}")
                        st.markdown("---")
                else:
                    st.success("✅ No known interactions detected between these medicines")
            
            elif len(identified_medicines) == 1:
                st.info("ℹ️ Enter at least 2 medicines to check for interactions")
            
            # Step 3: Individual medicine warnings
            if identified_medicines:
                st.markdown("---")
                st.markdown("### 📋 Individual Medicine Warnings")
                
                for med_name in identified_medicines:
                    warnings = med_db.get_medicine_warnings(med_name)
                    
                    if warnings:
                        with st.expander(f"⚠️ {med_name.title()} - {len(warnings)} warning(s)"):
                            for warning in warnings:
                                st.write(warning)
                    else:
                        with st.expander(f"✅ {med_name.title()} - No specific warnings"):
                            st.write("No additional warnings for this medicine")
            
            # Educational disclaimer
            st.markdown("---")
            st.info("📌 **Disclaimer:** This is an educational tool. Always consult healthcare professionals for medical advice.")
    
    elif check_button:
        st.warning("Please enter at least one medicine name.")

# Prescription OCR
elif page == "📄 Prescription OCR":
    st.header("Prescription OCR")
    st.write("Upload prescription image to extract medicine information using AI")
    
    # Initialize OCR engine and medicine database
    if 'ocr_engine' not in st.session_state:
        st.session_state.ocr_engine = OCREngine()
    
    if 'med_db' not in st.session_state:
        st.session_state.med_db = MedicineDatabase()
        st.session_state.med_db.load_medicines()
        st.session_state.med_db.load_interactions()
    
    ocr_engine = st.session_state.ocr_engine
    med_db = st.session_state.med_db
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a prescription image",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of your prescription"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(image, caption="Uploaded Prescription", use_column_width=True)
        
        with col2:
            st.info("📸 **Image uploaded successfully!**")
            st.write(f"**File name:** {uploaded_file.name}")
            st.write(f"**Image size:** {image.size[0]} x {image.size[1]} pixels")
            st.write(f"**Format:** {image.format}")
        
        st.markdown("---")
        
        # Extraction options
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            extract_button = st.button("🔍 Extract Medicines", type="primary")
        with col2:
            use_ai = st.checkbox("Use AI Parsing", value=True, help="Use LLaMA 3 for better extraction")
        
        if extract_button:
            with st.spinner("🔄 Reading prescription..."):
                # Step 1: Extract text using OCR
                st.markdown("### 📝 Step 1: OCR Text Extraction")
                
                raw_text = ocr_engine.extract_text_from_pil(image)
                
                if raw_text and raw_text.strip():
                    st.success("✅ Text extracted successfully!")
                    
                    with st.expander("📄 View Raw Extracted Text"):
                        st.text(raw_text)
                    
                    # Step 2: Parse medicines using AI
                    st.markdown("---")
                    st.markdown("### 💊 Step 2: Medicine Identification")
                    
                    with st.spinner("🤖 AI is parsing medicine information..."):
                        structured_data = ocr_engine.extract_structured_data(raw_text, use_ai=use_ai)
                    
                    if structured_data and 'medicines' in structured_data:
                        medicines = structured_data['medicines']
                        
                        if len(medicines) > 0:
                            st.success(f"✅ Found {len(medicines)} medicine(s)")
                            st.info(f"**Extraction Method:** {structured_data.get('extraction_method', 'Unknown')}")
                            
                            # Display detected medicines
                            st.markdown("#### 💊 Detected Medicines & Drugs")
                            
                            for idx, med in enumerate(medicines, 1):
                                with st.expander(f"Medicine {idx}: {med.get('name', 'Unknown')}"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"**Name:** {med.get('name', 'Unknown')}")
                                        st.write(f"**Form:** {med.get('form', 'Unknown')}")
                                    with col2:
                                        st.write(f"**Active Salt:** {med.get('active_salt', 'Unknown')}")
                                        st.write(f"**Dosage:** {med.get('dosage', 'Unknown')}")
                            
                            # Step 3: Validate against database
                            st.markdown("---")
                            st.markdown("### 🔍 Step 3: Database Validation")
                            
                            validated_medicines = []
                            
                            for med in medicines:
                                med_name = med.get('name', '')
                                if med_name and med_name != 'Unknown':
                                    match = med_db.find_medicine(med_name, threshold=60)
                                    
                                    if match:
                                        validated_medicines.append(match['name'])
                                        confidence = match['confidence']
                                        
                                        if confidence >= 90:
                                            st.success(f"✅ **{med_name}** → Found in database: **{match['data']['name']}** ({confidence}% match)")
                                        else:
                                            st.info(f"🔍 **{med_name}** → Possible match: **{match['data']['name']}** ({confidence}% match)")
                                    else:
                                        st.warning(f"⚠️ **{med_name}** → Not found in database (may need manual verification)")
                            
                            # Step 4: Check interactions
                            if len(validated_medicines) >= 2:
                                st.markdown("---")
                                st.markdown("### ⚠️ Step 4: Interaction Analysis")
                                
                                interactions = med_db.check_interactions(validated_medicines)
                                
                                if interactions:
                                    st.error(f"🚨 Found {len(interactions)} potential interaction(s)!")
                                    
                                    for idx, interaction in enumerate(interactions, 1):
                                        severity = interaction['severity']
                                        
                                        if severity == 'high':
                                            st.error(f"**Interaction {idx}: HIGH SEVERITY**")
                                        elif severity == 'moderate':
                                            st.warning(f"**Interaction {idx}: MODERATE SEVERITY**")
                                        else:
                                            st.info(f"**Interaction {idx}: {severity.upper()} SEVERITY**")
                                        
                                        st.write(f"**Medicines:** {interaction['medicine1'].title()} + {interaction['medicine2'].title()}")
                                        st.write(f"**Description:** {interaction['description']}")
                                        st.markdown("---")
                                else:
                                    st.success("✅ No known interactions detected between validated medicines")
                            
                            elif len(validated_medicines) == 1:
                                st.info("ℹ️ Only one medicine validated. Need at least 2 medicines to check interactions.")
                            
                            # Step 5: Safety recommendations
                            if validated_medicines:
                                st.markdown("---")
                                st.markdown("### 📋 Step 5: Safety Recommendations")
                                
                                for med_name in validated_medicines:
                                    warnings = med_db.get_medicine_warnings(med_name)
                                    
                                    if warnings:
                                        with st.expander(f"⚠️ {med_name.title()} - {len(warnings)} warning(s)"):
                                            for warning in warnings:
                                                st.write(warning)
                            
                            # Educational disclaimer
                            st.markdown("---")
                            st.info("📌 **Disclaimer:** This is an educational tool. OCR may have errors. Always verify with healthcare professionals.")
                        
                        else:
                            st.warning("⚠️ No medicines detected in the prescription. Please try:")
                            st.write("- Uploading a clearer image")
                            st.write("- Ensuring good lighting")
                            st.write("- Making sure text is readable")
                    
                    else:
                        st.error("❌ Failed to parse medicine information")
                
                else:
                    st.error("❌ No text could be extracted from the image. Please try:")
                    st.write("- Uploading a clearer image")
                    st.write("- Ensuring the prescription is well-lit")
                    st.write("- Making sure the text is not blurry")
    
    else:
        # Instructions when no file is uploaded
        st.info("👆 Please upload a prescription image to get started")
        
        st.markdown("### 📋 Tips for Best Results:")
        st.write("✅ Use a clear, well-lit image")
        st.write("✅ Ensure text is readable and not blurry")
        st.write("✅ Avoid shadows or glare")
        st.write("✅ Supported formats: JPG, JPEG, PNG")
        
        st.markdown("### 🔬 How it works:")
        st.write("1. **OCR Extraction:** Tesseract OCR reads text from your prescription")
        st.write("2. **AI Parsing:** LLaMA 3 identifies medicines and active ingredients")
        st.write("3. **Database Validation:** Fuzzy matching validates against medicine database")
        st.write("4. **Interaction Check:** Analyzes potential drug-drug interactions")
        st.write("5. **Safety Recommendations:** Provides warnings and precautions")

# Symptom & Doubt Solver
elif page == "🩺 Symptom & Doubt Solver":
    st.header("Symptom & Doubt Solver")
    st.write("Get AI-enhanced guidance for your symptoms")
    
    # Initialize symptom analyzer
    if 'symptom_analyzer' not in st.session_state:
        st.session_state.symptom_analyzer = SymptomAnalyzer()
    
    analyzer = st.session_state.symptom_analyzer
    
    # Input area
    symptoms = st.text_area(
        "Describe your symptoms:",
        height=150,
        placeholder="Example: I have a headache and feel dizzy. It started this morning..."
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        analyze_button = st.button("Get Guidance", type="primary")
    with col2:
        use_ai = st.checkbox("Use AI Analysis", value=True, help="Use LLaMA 3 for enhanced analysis")
    
    if analyze_button and symptoms:
        with st.spinner("🔍 Analyzing symptoms..."):
            # Analyze symptoms
            analysis = analyzer.analyze_symptoms(symptoms, use_ai=use_ai)
            
            st.markdown("---")
            st.subheader("📊 Analysis Results")
            
            # Severity indicator
            severity = analysis['severity']
            if severity == "high":
                st.error(f"🚨 **Severity Level: HIGH**")
            elif severity == "medium":
                st.warning(f"⚠️ **Severity Level: MEDIUM**")
            else:
                st.info(f"ℹ️ **Severity Level: LOW**")
            
            # Detected symptoms
            if analysis['detected_symptoms']:
                st.markdown("### 🔍 Detected Symptoms")
                for symptom in analysis['detected_symptoms']:
                    st.write(f"• {symptom.title()}")
            
            # AI Explanation
            if analysis['ai_explanation']:
                st.markdown("---")
                st.markdown("### 🤖 AI Educational Explanation")
                st.info(analysis['ai_explanation'])
            
            # Home Remedies
            if analysis['home_remedies']:
                st.markdown("---")
                st.markdown("### 🏠 Home Remedies")
                for remedy in analysis['home_remedies']:
                    st.write(f"✓ {remedy}")
            
            # Lifestyle Suggestions
            if analysis['lifestyle_suggestions']:
                st.markdown("---")
                st.markdown("### 💪 Lifestyle Suggestions")
                for suggestion in analysis['lifestyle_suggestions']:
                    st.write(f"✓ {suggestion}")
            
            # Warning Signs
            if analysis['warning_signs']:
                st.markdown("---")
                st.markdown("### ⚠️ Warning Signs - Seek Immediate Care If:")
                for warning in analysis['warning_signs']:
                    st.error(f"🚨 {warning}")
            
            # Disclaimer
            st.markdown("---")
            st.info("📌 **Disclaimer:** This is an educational tool only. Always consult healthcare professionals for medical diagnosis and treatment.")
    
    elif analyze_button:
        st.warning("Please describe your symptoms to get guidance.")
    
    else:
        # Instructions
        st.markdown("### 📋 How to Use:")
        st.write("1. Describe your symptoms in detail")
        st.write("2. Click 'Get Guidance' to analyze")
        st.write("3. Review home remedies and lifestyle suggestions")
        st.write("4. Watch for warning signs that need immediate care")

# Side-Effect Monitor
elif page == "⚠️ Side-Effect Monitor":
    st.header("Side-Effect Monitor")
    st.write("Log and analyze post-medication experiences")
    
    # Initialize risk engine
    if 'risk_engine' not in st.session_state:
        st.session_state.risk_engine = RiskEngine()
    
    risk_engine = st.session_state.risk_engine
    
    # Input form
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    with col2:
        medicine = st.text_input("Medicine taken", placeholder="e.g., Ibuprofen")
        dosage = st.text_input("Dosage", placeholder="e.g., 400mg")
    
    experience = st.text_area(
        "Post-medication experience:",
        height=150,
        placeholder="Describe any side effects or reactions you experienced..."
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        analyze_button = st.button("Analyze", type="primary")
    with col2:
        use_ai = st.checkbox("Use AI Analysis", value=True, help="Use LLaMA 3 for enhanced analysis")
    
    if analyze_button and medicine and experience:
        with st.spinner("🔍 Analyzing side effects..."):
            # Analyze side effects
            analysis = risk_engine.analyze_side_effects(
                medicine=medicine,
                dosage=dosage,
                experience=experience,
                age=age,
                gender=gender,
                use_ai=use_ai
            )
            
            st.markdown("---")
            st.subheader("📊 Side Effect Analysis")
            
            # Severity indicator
            severity = analysis['severity']
            if severity == "severe":
                st.error(f"🚨 **Severity: SEVERE**")
            elif severity == "moderate":
                st.warning(f"⚠️ **Severity: MODERATE**")
            else:
                st.info(f"ℹ️ **Severity: MILD**")
            
            # Medicine info
            st.markdown("### 💊 Medicine Information")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Medicine:** {analysis['medicine']}")
                st.write(f"**Dosage:** {analysis['dosage']}")
            with col2:
                st.write(f"**Age:** {analysis['age']}")
                st.write(f"**Gender:** {analysis['gender']}")
            
            # AI Analysis
            if analysis['ai_analysis']:
                st.markdown("---")
                st.markdown("### 🤖 AI Analysis")
                st.info(analysis['ai_analysis'])
            
            # Recommendation
            st.markdown("---")
            st.markdown("### 📋 Recommendation")
            if severity == "severe":
                st.error(analysis['recommendation'])
            elif severity == "moderate":
                st.warning(analysis['recommendation'])
            else:
                st.info(analysis['recommendation'])
            
            # Disclaimer
            st.markdown("---")
            st.info("📌 **Disclaimer:** This analysis is for educational purposes. Always consult your healthcare provider about medication side effects.")
    
    elif analyze_button:
        st.warning("Please fill in medicine name and experience to analyze.")
    
    else:
        # Instructions
        st.markdown("### 📋 How to Use:")
        st.write("1. Enter your age and gender")
        st.write("2. Specify the medicine and dosage taken")
        st.write("3. Describe your post-medication experience")
        st.write("4. Click 'Analyze' to get AI-enhanced analysis")

# Emergency Risk Predictor
elif page == "🚨 Emergency Risk Predictor":
    st.header("Emergency Risk Predictor")
    st.write("Assess emergency risk level based on symptoms")
    
    # Initialize risk engine
    if 'risk_engine' not in st.session_state:
        st.session_state.risk_engine = RiskEngine()
    
    risk_engine = st.session_state.risk_engine
    
    # Input form
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (optional)", min_value=0, max_value=120, value=0, help="Leave as 0 if you prefer not to specify")
        gender = st.selectbox("Gender (optional)", ["Not specified", "Male", "Female", "Other"])
    
    with col2:
        medical_history = st.multiselect(
            "Medical History (optional)",
            ["Heart Disease", "Diabetes", "Hypertension", "Asthma", "COPD", "None"]
        )
    
    symptoms = st.text_area(
        "Describe symptoms:",
        height=150,
        placeholder="Example: Severe chest pain radiating to left arm, difficulty breathing, sweating..."
    )
    
    severity = st.slider("Symptom severity (1-10)", 1, 10, 5, help="1 = Mild, 10 = Severe")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        calculate_button = st.button("Calculate Risk", type="primary")
    with col2:
        use_ai = st.checkbox("Use AI Safety Note", value=True, help="Generate AI-enhanced safety guidance")
    
    if calculate_button and symptoms:
        with st.spinner("🔍 Calculating risk score..."):
            # Calculate risk
            risk_assessment = risk_engine.calculate_risk_score(
                symptoms=symptoms,
                severity=severity,
                age=age if age > 0 else None,
                gender=gender if gender != "Not specified" else None,
                medical_history=medical_history if medical_history and "None" not in medical_history else None,
                use_ai=use_ai
            )
            
            st.markdown("---")
            st.subheader("📊 Risk Assessment Results")
            
            # Risk Score Display
            risk_score = risk_assessment['risk_score']
            risk_level = risk_assessment['risk_level']
            
            # Create visual risk meter
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if risk_level == "HIGH":
                    st.error(f"### {risk_score}%")
                    st.error(f"**{risk_level} RISK**")
                elif risk_level == "MEDIUM":
                    st.warning(f"### {risk_score}%")
                    st.warning(f"**{risk_level} RISK**")
                else:
                    st.info(f"### {risk_score}%")
                    st.info(f"**{risk_level} RISK**")
            
            # Risk Factors
            if risk_assessment['risk_factors']:
                st.markdown("---")
                st.markdown("### ⚠️ Identified Risk Factors")
                for factor in risk_assessment['risk_factors']:
                    st.write(f"• {factor}")
            
            # Affected Categories
            if risk_assessment['affected_categories']:
                st.markdown("---")
                st.markdown("### 🏥 Affected Systems")
                for category in risk_assessment['affected_categories']:
                    st.write(f"• {category.title()}")
            
            # AI Safety Note
            if risk_assessment['ai_safety_note']:
                st.markdown("---")
                st.markdown("### 🤖 AI Safety Guidance")
                st.info(risk_assessment['ai_safety_note'])
            
            # Recommendation
            st.markdown("---")
            st.markdown("### 📋 Recommendation")
            if risk_level == "HIGH":
                st.error(risk_assessment['recommendation'])
            elif risk_level == "MEDIUM":
                st.warning(risk_assessment['recommendation'])
            else:
                st.info(risk_assessment['recommendation'])
            
            # Calculation Details (expandable)
            with st.expander("🔍 View Calculation Details"):
                details = risk_assessment['calculation_details']
                st.write(f"**Base Score:** {details['base_score']}")
                st.write(f"**Severity Factor:** {details['severity_factor']}")
                st.write(f"**Age Factor:** {details['age_factor']}")
                st.write(f"**Medical History Factor:** {details['history_factor']}")
                st.write(f"**Final Score:** {risk_score}%")
            
            # Disclaimer
            st.markdown("---")
            st.error("🚨 **IMPORTANT:** This is an educational risk assessment tool only. It does NOT replace professional medical evaluation. If you are experiencing a medical emergency, call 911 or your local emergency number immediately.")
    
    elif calculate_button:
        st.warning("Please describe your symptoms to calculate risk.")
    
    else:
        # Instructions and examples
        st.markdown("### 📋 How to Use:")
        st.write("1. Describe your symptoms in detail")
        st.write("2. Rate the severity (1-10)")
        st.write("3. Optionally provide age and medical history")
        st.write("4. Click 'Calculate Risk' for assessment")
        
        st.markdown("### ⚠️ High-Risk Symptoms (Seek Immediate Care):")
        st.write("• Chest pain or pressure")
        st.write("• Difficulty breathing")
        st.write("• Sudden severe headache")
        st.write("• Loss of consciousness")
        st.write("• Severe bleeding")
        st.write("• Signs of stroke (facial drooping, arm weakness, speech difficulty)")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("MedSafe AI v1.0 - Educational Tool")
