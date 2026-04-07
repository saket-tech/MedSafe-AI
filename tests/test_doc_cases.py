from io import BytesIO
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from PIL import Image, ImageDraw
from fastapi.testclient import TestClient

from backend.app import app
from backend.services.risk_engine import RiskEngine


client = TestClient(app)


def make_image_bytes(text: str | None = None) -> bytes:
    image = Image.new("RGB", (900, 300), color="white")
    if text:
        draw = ImageDraw.Draw(image)
        draw.text((40, 80), text, fill="black")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_interaction_exact_match():
    response = client.post("/api/medicines/interactions", json={"medicines": ["Atorvastatin"]})
    assert response.status_code == 200
    body = response.json()
    assert body["matches"][0]["matched_name"] == "atorvastatin"
    assert body["matches"][0]["confidence"] == 100.0


def test_interaction_fuzzy_match():
    response = client.post("/api/medicines/interactions", json={"medicines": ["Ibuprofin"]})
    assert response.status_code == 200
    body = response.json()
    assert body["matches"][0]["display_name"] == "Ibuprofen"
    assert body["matches"][0]["confidence"] >= 80


def test_interaction_not_found():
    response = client.post("/api/medicines/interactions", json={"medicines": ["UnknownMedicine123"]})
    assert response.status_code == 200
    body = response.json()
    assert body["unmatched"] == ["UnknownMedicine123"]
    assert body["matches"] == []


def test_high_severity_interaction():
    response = client.post("/api/medicines/interactions", json={"medicines": ["Warfarin", "Ibuprofen"]})
    assert response.status_code == 200
    interactions = response.json()["interactions"]
    assert any(item["severity"] == "high" for item in interactions)


def test_moderate_severity_interaction():
    response = client.post(
        "/api/medicines/interactions",
        json={"medicines": ["Atorvastatin", "Clarithromycin"]},
    )
    assert response.status_code == 200
    interactions = response.json()["interactions"]
    assert any(item["severity"] == "moderate" for item in interactions)


def test_no_known_interactions():
    response = client.post("/api/medicines/interactions", json={"medicines": ["Metformin", "Lisinopril"]})
    assert response.status_code == 200
    assert response.json()["interactions"] == []


def test_single_medicine_returns_warnings_without_interactions():
    response = client.post("/api/medicines/interactions", json={"medicines": ["Aspirin"]})
    assert response.status_code == 200
    body = response.json()
    assert body["interactions"] == []
    assert "aspirin" in body["warnings_by_medicine"]


def test_special_characters_do_not_crash_lookup():
    response = client.post("/api/medicines/interactions", json={"medicines": ["Aspirin@#$%"]})
    assert response.status_code == 200
    assert response.json()["matches"] == []


def test_grapefruit_warning_present_for_atorvastatin():
    response = client.post("/api/medicines/interactions", json={"medicines": ["Atorvastatin"]})
    warnings = response.json()["warnings_by_medicine"]["atorvastatin"]
    assert any("Grapefruit Warning" in warning for warning in warnings)


def test_known_interactions_list_present_for_warfarin():
    response = client.post("/api/medicines/interactions", json={"medicines": ["Warfarin"]})
    warnings = response.json()["warnings_by_medicine"]["warfarin"]
    assert any("Known Interactions" in warning for warning in warnings)


def test_empty_medicine_input_returns_400():
    response = client.post("/api/medicines/interactions", json={"medicines": []})
    assert response.status_code == 400


def test_prescription_ai_disabled_basic_parsing(monkeypatch):
    from backend.api import routes

    monkeypatch.setattr(
        routes.ocr_engine,
        "extract_text_from_pil",
        lambda image: "TAB Aspirin 75mg\nCAP Ibuprofen 200mg",
    )

    response = client.post(
        "/api/prescriptions/analyze",
        files={"file": ("rx.png", make_image_bytes("demo"), "image/png")},
        data={"use_ai": "false"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["structured_data"]["extraction_method"] == "Basic Pattern Matching"
    assert isinstance(body["structured_data"]["medicines"], list)


def test_prescription_ai_enabled_with_mock(monkeypatch):
    from backend.services import ocr_utils

    def fake_chat(model, messages):
        return {
            "message": {
                "content": '{"medicines": [{"name": "Aspirin", "active_salt": "Acetylsalicylic Acid", "dosage": "75mg", "form": "tablet"}]}'
            }
        }

    monkeypatch.setattr(ocr_utils.ollama, "chat", fake_chat)

    response = client.post(
        "/api/prescriptions/analyze",
        files={"file": ("rx.png", make_image_bytes("Aspirin 75mg"), "image/png")},
        data={"use_ai": "true"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["structured_data"]["extraction_method"] == "AI (LLaMA 3)"


def test_prescription_invalid_file_rejected():
    response = client.post(
        "/api/prescriptions/analyze",
        files={"file": ("rx.txt", b"not an image", "text/plain")},
        data={"use_ai": "false"},
    )
    assert response.status_code == 400


def test_prescription_no_text_extracted(monkeypatch):
    from backend.api import routes

    monkeypatch.setattr(routes.ocr_engine, "extract_text_from_pil", lambda image: "")

    response = client.post(
        "/api/prescriptions/analyze",
        files={"file": ("blank.png", make_image_bytes(), "image/png")},
        data={"use_ai": "false"},
    )
    assert response.status_code == 400
    assert "No text could be extracted" in response.text


def test_symptom_analysis_medium_without_ai():
    response = client.post(
        "/api/symptoms/analyze",
        json={"symptoms": "fever, headache, cough", "use_ai": False},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["severity"] == "medium"
    assert body["ai_explanation"] == ""


def test_symptom_analysis_high_severity():
    response = client.post(
        "/api/symptoms/analyze",
        json={"symptoms": "chest pain, difficulty breathing, dizziness", "use_ai": False},
    )
    assert response.status_code == 200
    assert response.json()["severity"] == "high"


def test_symptom_analysis_with_ai_explanation(monkeypatch):
    from backend.services import symptom

    def fake_chat(model, messages):
        prompt = messages[0]["content"]
        if "Identify the main symptoms" in prompt:
            return {"message": {"content": "fever, cough"}}
        return {"message": {"content": "This is an educational AI explanation."}}

    monkeypatch.setattr(symptom.ollama, "chat", fake_chat)

    response = client.post(
        "/api/symptoms/analyze",
        json={"symptoms": "I have fever and cough", "use_ai": True},
    )
    assert response.status_code == 200
    assert response.json()["ai_explanation"] == "This is an educational AI explanation."


def test_symptom_analysis_vague_without_ai():
    response = client.post(
        "/api/symptoms/analyze",
        json={"symptoms": "runny nose", "use_ai": False},
    )
    assert response.status_code == 200
    assert response.json()["severity"] == "low"


def test_side_effect_severe():
    response = client.post(
        "/api/side-effects/analyze",
        json={
            "medicine": "Ibuprofen",
            "dosage": "400mg",
            "experience": "severe swelling and difficulty breathing",
            "age": 30,
            "gender": "Male",
            "use_ai": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["severity"] == "severe"


def test_side_effect_moderate():
    response = client.post(
        "/api/side-effects/analyze",
        json={
            "medicine": "Ibuprofen",
            "dosage": "400mg",
            "experience": "nausea and painful dizziness",
            "age": 30,
            "gender": "Male",
            "use_ai": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["severity"] == "moderate"


def test_side_effect_mild_with_ai_mock(monkeypatch):
    from backend.services import risk_engine

    monkeypatch.setattr(
        risk_engine.ollama,
        "chat",
        lambda model, messages: {"message": {"content": "Educational side-effect analysis."}},
    )
    response = client.post(
        "/api/side-effects/analyze",
        json={
            "medicine": "Ibuprofen",
            "dosage": "200mg",
            "experience": "slight stomach discomfort",
            "age": 30,
            "gender": "Male",
            "use_ai": True,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["severity"] == "mild"
    assert body["ai_analysis"] == "Educational side-effect analysis."


def test_risk_high():
    response = client.post(
        "/api/risk/analyze",
        json={"symptoms": "chest pain and difficulty breathing", "severity": 9, "use_ai": False},
    )
    assert response.status_code == 200
    assert response.json()["risk_level"] == "HIGH"


def test_risk_medium():
    response = client.post(
        "/api/risk/analyze",
        json={"symptoms": "chest tightness", "severity": 6, "use_ai": False},
    )
    assert response.status_code == 200
    assert response.json()["risk_level"] == "MEDIUM"


def test_risk_low():
    response = client.post(
        "/api/risk/analyze",
        json={"symptoms": "mild fatigue", "severity": 2, "use_ai": False},
    )
    assert response.status_code == 200
    assert response.json()["risk_level"] == "LOW"


def test_risk_ai_guidance_mock(monkeypatch):
    from backend.services import risk_engine

    monkeypatch.setattr(
        risk_engine.ollama,
        "chat",
        lambda model, messages: {"message": {"content": "Educational safety note."}},
    )
    response = client.post(
        "/api/risk/analyze",
        json={"symptoms": "chest pain", "severity": 7, "use_ai": True},
    )
    assert response.status_code == 200
    assert response.json()["ai_safety_note"] == "Educational safety note."


def test_risk_medical_history_and_age_increase_score():
    engine = RiskEngine()
    baseline = engine.calculate_risk_score("weakness", severity=5, use_ai=False)
    elevated = engine.calculate_risk_score(
        "weakness",
        severity=5,
        age=70,
        medical_history=["diabetes"],
        use_ai=False,
    )
    assert elevated["risk_score"] > baseline["risk_score"]
