"""
MedSafe AI - Main Streamlit Application
Front-end interface and main application logic
"""

import streamlit as st
from PIL import Image
import json
from datetime import datetime
from med_db import MedicineDatabase

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
    st.write("Upload prescription image to extract medicine information")
    
    # Placeholder for OCR logic
    uploaded_file = st.file_uploader("Choose a prescription image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Prescription", use_column_width=True)
        
        if st.button("Extract Medicines"):
            st.info("OCR extraction functionality will be implemented in Activity 2.2")

# Symptom & Doubt Solver
elif page == "🩺 Symptom & Doubt Solver":
    st.header("Symptom & Doubt Solver")
    st.write("Get guidance for your symptoms")
    
    # Placeholder for symptom analysis logic
    symptoms = st.text_area("Describe your symptoms:", height=150)
    
    if st.button("Get Guidance"):
        st.info("Symptom analysis functionality will be implemented in Activity 2.3")

# Side-Effect Monitor
elif page == "⚠️ Side-Effect Monitor":
    st.header("Side-Effect Monitor")
    st.write("Log and analyze post-medication experiences")
    
    # Placeholder for side-effect monitoring logic
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    with col2:
        medicine = st.text_input("Medicine taken")
        dosage = st.text_input("Dosage")
    
    experience = st.text_area("Post-medication experience:", height=100)
    
    if st.button("Analyze"):
        st.info("Side-effect analysis functionality will be implemented in Activity 2.3")

# Emergency Risk Predictor
elif page == "🚨 Emergency Risk Predictor":
    st.header("Emergency Risk Predictor")
    st.write("Assess emergency risk level based on symptoms")
    
    # Placeholder for risk scoring logic
    symptoms = st.text_area("Describe symptoms:", height=150)
    severity = st.slider("Symptom severity (1-10)", 1, 10, 5)
    
    if st.button("Calculate Risk"):
        st.info("Risk scoring functionality will be implemented in Activity 2.3")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("MedSafe AI v1.0 - Educational Tool")
