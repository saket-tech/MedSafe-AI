from io import BytesIO

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from PIL import Image

from backend.models import InteractionRequest, RiskAssessmentRequest, SideEffectRequest, SymptomAnalysisRequest
from backend.services.med_db import MedicineDatabase
from backend.services.ocr_utils import OCREngine
from backend.services.risk_engine import RiskEngine
from backend.services.symptom import SymptomAnalyzer


router = APIRouter()

med_db = MedicineDatabase()
med_db.load_medicines()
med_db.load_interactions()
ocr_engine = OCREngine()
symptom_analyzer = SymptomAnalyzer()
risk_engine = RiskEngine()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/api/medicines/interactions")
def analyze_interactions(request: InteractionRequest):
    if not request.medicines:
        raise HTTPException(status_code=400, detail="Provide at least one medicine.")

    identified_medicines = []
    matches = []
    unmatched = []

    for medicine in request.medicines:
        match = med_db.find_medicine(medicine, threshold=70)
        if match:
            identified_medicines.append(match["name"])
            matches.append(
                {
                    "input": medicine,
                    "matched_name": match["name"],
                    "display_name": match["data"]["name"],
                    "confidence": match["confidence"],
                }
            )
        else:
            unmatched.append(medicine)

    warnings_by_medicine = {
        medicine: med_db.get_medicine_warnings(medicine) for medicine in identified_medicines
    }

    return {
        "identified_medicines": identified_medicines,
        "matches": matches,
        "unmatched": unmatched,
        "interactions": med_db.check_interactions(identified_medicines),
        "warnings_by_medicine": warnings_by_medicine,
    }


@router.post("/api/prescriptions/analyze")
async def analyze_prescription(file: UploadFile = File(...), use_ai: bool = Form(True)):
    try:
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image upload: {exc}") from exc

    raw_text = ocr_engine.extract_text_from_pil(image)
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from the image.")

    structured_data = ocr_engine.extract_structured_data(raw_text, use_ai=use_ai)
    medicines = structured_data.get("medicines", [])

    validated_medicines = []
    validations = []
    for medicine in medicines:
        med_name = medicine.get("name", "")
        if med_name and med_name != "Unknown":
            match = med_db.find_medicine(med_name, threshold=60)
            if match:
                validated_medicines.append(match["name"])
                validations.append(
                    {
                        "input": med_name,
                        "matched_name": match["name"],
                        "display_name": match["data"]["name"],
                        "confidence": match["confidence"],
                    }
                )
            else:
                validations.append(
                    {
                        "input": med_name,
                        "matched_name": None,
                        "display_name": None,
                        "confidence": 0,
                    }
                )

    warnings_by_medicine = {
        medicine: med_db.get_medicine_warnings(medicine) for medicine in validated_medicines
    }

    return {
        "raw_text": raw_text,
        "structured_data": structured_data,
        "validated_medicines": validated_medicines,
        "validations": validations,
        "interactions": med_db.check_interactions(validated_medicines),
        "warnings_by_medicine": warnings_by_medicine,
    }


@router.post("/api/symptoms/analyze")
def analyze_symptoms(request: SymptomAnalysisRequest):
    return symptom_analyzer.analyze_symptoms(request.symptoms, use_ai=request.use_ai)


@router.post("/api/side-effects/analyze")
def analyze_side_effects(request: SideEffectRequest):
    return risk_engine.analyze_side_effects(
        medicine=request.medicine,
        dosage=request.dosage,
        experience=request.experience,
        age=request.age,
        gender=request.gender,
        use_ai=request.use_ai,
    )


@router.post("/api/risk/analyze")
def analyze_risk(request: RiskAssessmentRequest):
    return risk_engine.calculate_risk_score(
        symptoms=request.symptoms,
        severity=request.severity,
        age=request.age,
        gender=request.gender,
        medical_history=request.medical_history,
        use_ai=request.use_ai,
    )
