"""MedSafe AI - Streamlit frontend application."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from typing import Dict

import requests
import streamlit as st
from PIL import Image

from frontend.api_client import ApiClient
from frontend.config import API_BASE_URL

PAGES = [
    "Home",
    "Medicine Interaction Checker",
    "Prescription OCR",
    "Symptom & Doubt Solver",
    "Side-Effect Monitor",
    "Emergency Risk Predictor",
]

FEATURES = [
    {
        "title": "Medicine Interaction Checker",
        "description": "Find exact and fuzzy medicine matches, detect interactions, and review medicine-specific warnings.",
        "highlights": ["Fuzzy medicine lookup", "Severity-based interaction alerts", "Medicine safety warnings"],
    },
    {
        "title": "Prescription OCR",
        "description": "Upload prescription images, extract text, identify medicines, and validate against the database.",
        "highlights": ["Image preprocessing", "OCR extraction", "Validation and interaction checks"],
    },
    {
        "title": "Symptom & Doubt Solver",
        "description": "Get educational symptom guidance with remedies, warning signs, and optional AI explanations.",
        "highlights": ["Rule-based symptom guidance", "Home remedies", "Optional AI explanation"],
    },
    {
        "title": "Side-Effect Monitor",
        "description": "Log medication experiences and receive severity classification with practical next-step guidance.",
        "highlights": ["Mild/moderate/severe classification", "Recommendation output", "Optional AI analysis"],
    },
    {
        "title": "Emergency Risk Predictor",
        "description": "Estimate emergency risk from symptoms, severity, age, and medical history.",
        "highlights": ["Risk score", "Affected systems", "Urgency recommendation"],
    },
]


def apply_layout_styles():
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                min-width: 280px !important;
                width: 280px !important;
            }

            section[data-testid="stSidebar"] > div {
                min-width: 280px !important;
                width: 280px !important;
            }

            [data-testid="stAppViewContainer"] .main .block-container {
                max-width: 1400px;
                padding-top: 2rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }

            .feature-card {
                border: 1px solid rgba(250, 250, 250, 0.08);
                border-radius: 16px;
                padding: 1rem 1.1rem;
                background: rgba(26, 32, 44, 0.55);
                min-height: 220px;
                margin-bottom: 1rem;
            }

            .feature-card h4 {
                margin-top: 0;
                margin-bottom: 0.5rem;
            }

            .feature-card ul {
                margin: 0.75rem 0 0 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_api_client() -> ApiClient:
    if "api_client" not in st.session_state:
        st.session_state.api_client = ApiClient()
    return st.session_state.api_client


def render_backend_status(api_client: ApiClient):
    try:
        api_client.health_check()
    except requests.RequestException:
        st.sidebar.error("Backend unavailable")
        st.sidebar.caption(f"Expected backend at {API_BASE_URL}")


def render_home():
    st.header("Welcome to MedSafe AI")
    st.write(
        """
        MedSafe AI is an educational medical safety assistant that helps with medicine checks,
        prescription OCR, symptom guidance, side-effect analysis, and emergency risk screening.
        """
    )

    st.markdown("### Available Functionalities")
    col1, col2 = st.columns(2)
    columns = [col1, col2]

    for index, feature in enumerate(FEATURES):
        with columns[index % 2]:
            bullets = "".join([f"<li>{item}</li>" for item in feature["highlights"]])
            st.markdown(
                f"""
                <div class="feature-card">
                    <h4>{feature['title']}</h4>
                    <p>{feature['description']}</p>
                    <ul>{bullets}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "Use the navigation menu to open a module. This tool is educational only and does not replace professional medical advice."
    )


def render_interaction_results(result: Dict):
    st.markdown("---")
    st.subheader("Analysis Results")
    st.markdown("### Medicine Identification")

    for match in result["matches"]:
        confidence = match["confidence"]
        if confidence == 100:
            st.success(f"**{match['input']}** -> Exact match: **{match['display_name']}**")
        else:
            st.info(
                f"**{match['input']}** -> Found: **{match['display_name']}** "
                f"(Confidence: {confidence}%)"
            )

    for medicine in result["unmatched"]:
        st.error(f"**{medicine}** -> Not found in database")

    if len(result["identified_medicines"]) >= 2:
        st.markdown("---")
        st.markdown("### Interaction Analysis")
        interactions = result["interactions"]
        if interactions:
            st.warning(f"Found {len(interactions)} potential interaction(s)")
            for index, interaction in enumerate(interactions, 1):
                severity = interaction["severity"]
                if severity == "high":
                    st.error(f"Interaction {index}: HIGH SEVERITY")
                elif severity == "moderate":
                    st.warning(f"Interaction {index}: MODERATE SEVERITY")
                else:
                    st.info(f"Interaction {index}: {severity.upper()} SEVERITY")
                st.write(
                    f"**Medicines:** {interaction['medicine1'].title()} + "
                    f"{interaction['medicine2'].title()}"
                )
                st.write(f"**Description:** {interaction['description']}")
                st.markdown("---")
        else:
            st.success("No known interactions detected between these medicines")
    elif len(result["identified_medicines"]) == 1:
        st.info("Enter at least 2 medicines to check for interactions")

    if result["identified_medicines"]:
        st.markdown("---")
        st.markdown("### Individual Medicine Warnings")
        for medicine in result["identified_medicines"]:
            warnings = result["warnings_by_medicine"].get(medicine, [])
            if warnings:
                with st.expander(f"{medicine.title()} - {len(warnings)} warning(s)"):
                    for warning in warnings:
                        st.write(warning)
            else:
                with st.expander(f"{medicine.title()} - No specific warnings"):
                    st.write("No additional warnings for this medicine")


def render_prescription_results(result: Dict):
    st.markdown("### Step 1: OCR Text Extraction")
    st.success("Text extracted successfully")
    with st.expander("View Raw Extracted Text"):
        st.text(result["raw_text"])

    structured_data = result["structured_data"]
    medicines = structured_data.get("medicines", [])
    st.markdown("---")
    st.markdown("### Step 2: Medicine Identification")

    if not medicines:
        st.warning("No medicines detected in the prescription.")
        return

    st.success(f"Found {len(medicines)} medicine(s)")
    st.info(f"Extraction Method: {structured_data.get('extraction_method', 'Unknown')}")
    for index, medicine in enumerate(medicines, 1):
        with st.expander(f"Medicine {index}: {medicine.get('name', 'Unknown')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {medicine.get('name', 'Unknown')}")
                st.write(f"**Form:** {medicine.get('form', 'Unknown')}")
            with col2:
                st.write(f"**Active Salt:** {medicine.get('active_salt', 'Unknown')}")
                st.write(f"**Dosage:** {medicine.get('dosage', 'Unknown')}")

    st.markdown("---")
    st.markdown("### Step 3: Database Validation")
    validated_medicines = result["validated_medicines"]
    for validation in result["validations"]:
        if validation["matched_name"]:
            confidence = validation["confidence"]
            if confidence >= 90:
                st.success(
                    f"**{validation['input']}** -> Found in database: "
                    f"**{validation['display_name']}** ({confidence}% match)"
                )
            else:
                st.info(
                    f"**{validation['input']}** -> Possible match: "
                    f"**{validation['display_name']}** ({confidence}% match)"
                )
        else:
            st.warning(f"**{validation['input']}** -> Not found in database")

    if len(validated_medicines) >= 2:
        st.markdown("---")
        st.markdown("### Step 4: Interaction Analysis")
        interactions = result["interactions"]
        if interactions:
            st.error(f"Found {len(interactions)} potential interaction(s)")
            for index, interaction in enumerate(interactions, 1):
                severity = interaction["severity"]
                if severity == "high":
                    st.error(f"Interaction {index}: HIGH SEVERITY")
                elif severity == "moderate":
                    st.warning(f"Interaction {index}: MODERATE SEVERITY")
                else:
                    st.info(f"Interaction {index}: {severity.upper()} SEVERITY")
                st.write(
                    f"**Medicines:** {interaction['medicine1'].title()} + "
                    f"{interaction['medicine2'].title()}"
                )
                st.write(f"**Description:** {interaction['description']}")
                st.markdown("---")
        else:
            st.success("No known interactions detected between validated medicines")
    elif len(validated_medicines) == 1:
        st.info("Only one medicine validated. Need at least 2 medicines to check interactions.")

    if validated_medicines:
        st.markdown("---")
        st.markdown("### Step 5: Safety Recommendations")
        for medicine in validated_medicines:
            warnings = result["warnings_by_medicine"].get(medicine, [])
            if warnings:
                with st.expander(f"{medicine.title()} - {len(warnings)} warning(s)"):
                    for warning in warnings:
                        st.write(warning)


def render_symptom_analysis(analysis: Dict):
    st.markdown("---")
    st.subheader("Analysis Results")
    severity = analysis["severity"]
    if severity == "high":
        st.error("Severity Level: HIGH")
    elif severity == "medium":
        st.warning("Severity Level: MEDIUM")
    else:
        st.info("Severity Level: LOW")

    if analysis["detected_symptoms"]:
        st.markdown("### Detected Symptoms")
        for symptom in analysis["detected_symptoms"]:
            st.write(f"- {symptom.title()}")

    if analysis["ai_explanation"]:
        st.markdown("---")
        st.markdown("### AI Educational Explanation")
        st.info(analysis["ai_explanation"])

    if analysis["home_remedies"]:
        st.markdown("---")
        st.markdown("### Home Remedies")
        for remedy in analysis["home_remedies"]:
            st.write(f"- {remedy}")

    if analysis["lifestyle_suggestions"]:
        st.markdown("---")
        st.markdown("### Lifestyle Suggestions")
        for suggestion in analysis["lifestyle_suggestions"]:
            st.write(f"- {suggestion}")

    if analysis["warning_signs"]:
        st.markdown("---")
        st.markdown("### Warning Signs")
        for warning in analysis["warning_signs"]:
            st.error(warning)


def render_side_effect_analysis(analysis: Dict):
    st.markdown("---")
    st.subheader("Side Effect Analysis")
    severity = analysis["severity"]
    if severity == "severe":
        st.error("Severity: SEVERE")
    elif severity == "moderate":
        st.warning("Severity: MODERATE")
    else:
        st.info("Severity: MILD")

    st.markdown("### Medicine Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Medicine:** {analysis['medicine']}")
        st.write(f"**Dosage:** {analysis['dosage']}")
    with col2:
        st.write(f"**Age:** {analysis['age']}")
        st.write(f"**Gender:** {analysis['gender']}")

    if analysis["ai_analysis"]:
        st.markdown("---")
        st.markdown("### AI Analysis")
        st.info(analysis["ai_analysis"])

    st.markdown("---")
    st.markdown("### Recommendation")
    if severity == "severe":
        st.error(analysis["recommendation"])
    elif severity == "moderate":
        st.warning(analysis["recommendation"])
    else:
        st.info(analysis["recommendation"])


def render_risk_assessment(assessment: Dict):
    st.markdown("---")
    st.subheader("Risk Assessment Results")
    risk_score = assessment["risk_score"]
    risk_level = assessment["risk_level"]

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if risk_level == "HIGH":
            st.error(f"### {risk_score}%")
            st.error("**HIGH RISK**")
        elif risk_level == "MEDIUM":
            st.warning(f"### {risk_score}%")
            st.warning("**MEDIUM RISK**")
        else:
            st.info(f"### {risk_score}%")
            st.info("**LOW RISK**")

    if assessment["risk_factors"]:
        st.markdown("---")
        st.markdown("### Identified Risk Factors")
        for factor in assessment["risk_factors"]:
            st.write(f"- {factor}")

    if assessment["affected_categories"]:
        st.markdown("---")
        st.markdown("### Affected Systems")
        for category in assessment["affected_categories"]:
            st.write(f"- {category.title()}")

    if assessment["ai_safety_note"]:
        st.markdown("---")
        st.markdown("### AI Safety Guidance")
        st.info(assessment["ai_safety_note"])

    st.markdown("---")
    st.markdown("### Recommendation")
    if risk_level == "HIGH":
        st.error(assessment["recommendation"])
    elif risk_level == "MEDIUM":
        st.warning(assessment["recommendation"])
    else:
        st.info(assessment["recommendation"])

    with st.expander("View Calculation Details"):
        details = assessment["calculation_details"]
        st.write(f"**Base Score:** {details['base_score']}")
        st.write(f"**Severity Factor:** {details['severity_factor']}")
        st.write(f"**Age Factor:** {details['age_factor']}")
        st.write(f"**Medical History Factor:** {details['history_factor']}")
        st.write(f"**Final Score:** {risk_score}%")


def main():
    st.set_page_config(
        page_title="MedSafe AI",
        page_icon="M",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_layout_styles()
    st.title("MedSafe AI")
    st.markdown("---")

    api_client = get_api_client()
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Module:", PAGES)
    render_backend_status(api_client)

    if page == "Home":
        render_home()

    elif page == "Medicine Interaction Checker":
        st.header("Medicine Interaction Checker")
        medicines_input = st.text_area(
            "Enter medicine names (one per line):",
            height=150,
            placeholder="Example:\nAtorvastatin\nIbuprofen\nMetformin",
        )
        col1, col2 = st.columns([1, 3])
        with col1:
            check_button = st.button("Check Interactions", type="primary")
        with col2:
            if st.button("Clear"):
                st.rerun()

        if check_button and medicines_input:
            medicine_list = [medicine.strip() for medicine in medicines_input.split("\n") if medicine.strip()]
            try:
                with st.spinner("Analyzing medicines and checking interactions..."):
                    result = api_client.analyze_interactions(medicine_list)
                render_interaction_results(result)
                st.info("Disclaimer: This is an educational tool.")
            except requests.RequestException as exc:
                st.error(f"Backend request failed: {exc}")
        elif check_button:
            st.warning("Please enter at least one medicine name.")

    elif page == "Prescription OCR":
        st.header("Prescription OCR")
        uploaded_file = st.file_uploader("Choose a prescription image", type=["jpg", "jpeg", "png"])
        use_ai = st.checkbox("Use AI Parsing", value=True)

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(image, caption="Uploaded Prescription", use_container_width=True)
            with col2:
                st.info("Image uploaded successfully")
                st.write(f"**File name:** {uploaded_file.name}")
                st.write(f"**Image size:** {image.size[0]} x {image.size[1]} pixels")
                st.write(f"**Format:** {image.format}")

            if st.button("Extract Medicines", type="primary"):
                try:
                    with st.spinner("Reading prescription image and extracting medicines..."):
                        result = api_client.analyze_prescription(uploaded_file, use_ai)
                    render_prescription_results(result)
                    st.info("Disclaimer: OCR may have errors. Always verify with a professional.")
                except requests.RequestException as exc:
                    detail = getattr(exc.response, "text", str(exc))
                    st.error(f"Backend request failed: {detail}")
        else:
            st.info("Upload a prescription image to get started.")

    elif page == "Symptom & Doubt Solver":
        st.header("Symptom & Doubt Solver")
        symptoms = st.text_area(
            "Describe your symptoms:",
            height=150,
            placeholder="Example: I have a headache and feel dizzy.",
        )
        col1, col2 = st.columns([1, 3])
        with col1:
            analyze_button = st.button("Get Guidance", type="primary")
        with col2:
            use_ai = st.checkbox("Use AI Analysis", value=True)

        if analyze_button and symptoms:
            try:
                with st.spinner("Analyzing symptoms and preparing guidance..."):
                    result = api_client.analyze_symptoms(symptoms, use_ai)
                render_symptom_analysis(result)
                st.info("Disclaimer: Educational guidance only.")
            except requests.RequestException as exc:
                st.error(f"Backend request failed: {exc}")
        elif analyze_button:
            st.warning("Please describe your symptoms to get guidance.")

    elif page == "Side-Effect Monitor":
        st.header("Side-Effect Monitor")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col2:
            medicine = st.text_input("Medicine taken", placeholder="e.g., Ibuprofen")
            dosage = st.text_input("Dosage", placeholder="e.g., 400mg")

        experience = st.text_area("Post-medication experience:", height=150)
        col1, col2 = st.columns([1, 3])
        with col1:
            analyze_button = st.button("Analyze", type="primary")
        with col2:
            use_ai = st.checkbox("Use AI Analysis", value=True)

        if analyze_button and medicine and experience:
            try:
                with st.spinner("Analyzing side effects and preparing guidance..."):
                    analysis = api_client.analyze_side_effects(
                        medicine=medicine,
                        dosage=dosage,
                        experience=experience,
                        age=age,
                        gender=gender,
                        use_ai=use_ai,
                    )
                render_side_effect_analysis(analysis)
                st.info("Disclaimer: Educational analysis only.")
            except requests.RequestException as exc:
                st.error(f"Backend request failed: {exc}")
        elif analyze_button:
            st.warning("Please fill in medicine name and experience to analyze.")

    elif page == "Emergency Risk Predictor":
        st.header("Emergency Risk Predictor")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input(
                "Age (optional)",
                min_value=0,
                max_value=120,
                value=0,
                help="Leave as 0 if you prefer not to specify",
            )
            gender = st.selectbox("Gender (optional)", ["Not specified", "Male", "Female", "Other"])
        with col2:
            medical_history = st.multiselect(
                "Medical History (optional)",
                ["Heart Disease", "Diabetes", "Hypertension", "Asthma", "COPD", "None"],
            )

        symptoms = st.text_area("Describe symptoms:", height=150)
        severity = st.slider("Symptom severity (1-10)", 1, 10, 5)
        col1, col2 = st.columns([1, 3])
        with col1:
            calculate_button = st.button("Calculate Risk", type="primary")
        with col2:
            use_ai = st.checkbox("Use AI Safety Note", value=True)

        if calculate_button and symptoms:
            try:
                with st.spinner("Calculating emergency risk assessment..."):
                    assessment = api_client.analyze_risk(
                        symptoms=symptoms,
                        severity=severity,
                        age=age if age > 0 else None,
                        gender=gender if gender != "Not specified" else None,
                        medical_history=medical_history if medical_history and "None" not in medical_history else None,
                        use_ai=use_ai,
                    )
                render_risk_assessment(assessment)
                st.error(
                    "IMPORTANT: This is an educational tool only. If this is an emergency, call local emergency services immediately."
                )
            except requests.RequestException as exc:
                st.error(f"Backend request failed: {exc}")
        elif calculate_button:
            st.warning("Please describe your symptoms to calculate risk.")

    st.sidebar.markdown("---")
    st.sidebar.caption("MedSafe AI v2.0")


if __name__ == "__main__":
    main()
