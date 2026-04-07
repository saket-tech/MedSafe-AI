from typing import Any, Dict, List, Optional

import requests

from frontend.config import API_BASE_URL


class ApiClient:
    def __init__(self, base_url: str = API_BASE_URL, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health_check(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/health", timeout=10)
        response.raise_for_status()
        return response.json()

    def analyze_interactions(self, medicines: List[str]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/medicines/interactions",
            json={"medicines": medicines},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def analyze_prescription(self, uploaded_file, use_ai: bool) -> Dict[str, Any]:
        uploaded_file.seek(0)
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/octet-stream",
            )
        }
        data = {"use_ai": str(use_ai).lower()}
        response = requests.post(
            f"{self.base_url}/api/prescriptions/analyze",
            files=files,
            data=data,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def analyze_symptoms(self, symptoms: str, use_ai: bool) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/symptoms/analyze",
            json={"symptoms": symptoms, "use_ai": use_ai},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def analyze_side_effects(
        self,
        *,
        medicine: str,
        dosage: str,
        experience: str,
        age: int,
        gender: str,
        use_ai: bool,
    ) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/side-effects/analyze",
            json={
                "medicine": medicine,
                "dosage": dosage,
                "experience": experience,
                "age": age,
                "gender": gender,
                "use_ai": use_ai,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def analyze_risk(
        self,
        *,
        symptoms: str,
        severity: int,
        age: Optional[int],
        gender: Optional[str],
        medical_history: Optional[List[str]],
        use_ai: bool,
    ) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/risk/analyze",
            json={
                "symptoms": symptoms,
                "severity": severity,
                "age": age,
                "gender": gender,
                "medical_history": medical_history,
                "use_ai": use_ai,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
