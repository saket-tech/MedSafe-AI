"""
MedSafe AI - Main Streamlit Application
Front-end interface and main application logic
"""

import streamlit as st
from PIL import Image
import json
from datetime import datetime

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
    st.write("Check potential drug-drug interactions")
    
    # Placeholder for medicine interaction logic
    medicines = st.text_area("Enter medicine names (one per line):", height=150)
    
    if st.button("Check Interactions"):
        st.info("Medicine interaction checking functionality will be implemented in Activity 2.1")

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
