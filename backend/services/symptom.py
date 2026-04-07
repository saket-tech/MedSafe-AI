"""
Symptom Analysis Module
Rule-based symptom advice logic and AI-enhanced guidance
"""

from datetime import datetime
from typing import Dict, List

import ollama


class SymptomAnalyzer:
    """Provides symptom analysis and guidance."""

    def _build_fallback_explanation(self, description: str, symptoms: List[str]) -> str:
        if not symptoms:
            return (
                "Based on the description provided, no known symptom pattern was confidently detected. "
                "Monitor your symptoms closely and consult a healthcare professional if they worsen or persist."
            )

        highest_severity = "low"
        for symptom in symptoms:
            rule = self.symptom_rules.get(symptom, {})
            severity = rule.get("severity", "low")
            if severity == "high":
                highest_severity = "high"
                break
            if severity == "medium" and highest_severity != "high":
                highest_severity = "medium"

        severity_message = {
            "high": "Some of these symptoms can be concerning and may need urgent medical attention.",
            "medium": "These symptoms suggest a moderate level of concern and should be monitored carefully.",
            "low": "These symptoms appear lower risk based on the current rules, but they still deserve attention.",
        }

        return (
            f"The symptoms detected were: {', '.join(symptoms)}. "
            f"{severity_message[highest_severity]} "
            "This guidance is educational only and does not replace professional medical advice."
        )

    def __init__(self):
        self.symptom_rules = {}
        self.load_symptom_rules()

    def load_symptom_rules(self):
        self.symptom_rules = {
            "fever": {
                "severity": "medium",
                "advice": "Monitor temperature regularly, stay hydrated, rest",
                "home_remedies": [
                    "Drink plenty of fluids",
                    "Take lukewarm bath",
                    "Use cool compress",
                    "Wear light clothing",
                ],
                "lifestyle": [
                    "Get adequate rest",
                    "Avoid strenuous activity",
                    "Stay in cool environment",
                ],
                "warning_signs": [
                    "Temperature >103F (39.4C)",
                    "Fever lasting >3 days",
                    "Severe headache with fever",
                    "Difficulty breathing",
                ],
            },
            "headache": {
                "severity": "low",
                "advice": "Rest in quiet, dark room, stay hydrated",
                "home_remedies": [
                    "Apply cold or warm compress",
                    "Drink water",
                    "Practice relaxation techniques",
                    "Gentle neck stretches",
                ],
                "lifestyle": [
                    "Maintain regular sleep schedule",
                    "Reduce screen time",
                    "Manage stress",
                    "Avoid triggers",
                ],
                "warning_signs": [
                    "Sudden severe headache",
                    "Headache with vision changes",
                    "Headache with fever and stiff neck",
                    "Headache after head injury",
                ],
            },
            "cough": {
                "severity": "low",
                "advice": "Stay hydrated, use humidifier, avoid irritants",
                "home_remedies": [
                    "Honey and warm water",
                    "Steam inhalation",
                    "Throat lozenges",
                    "Elevate head while sleeping",
                ],
                "lifestyle": [
                    "Avoid smoking",
                    "Stay away from pollutants",
                    "Use humidifier",
                    "Drink warm fluids",
                ],
                "warning_signs": [
                    "Coughing up blood",
                    "Difficulty breathing",
                    "Chest pain",
                    "Persistent cough >3 weeks",
                ],
            },
            "nausea": {
                "severity": "low",
                "advice": "Eat bland foods, stay hydrated, rest",
                "home_remedies": [
                    "Ginger tea",
                    "Peppermint",
                    "Small frequent meals",
                    "Avoid strong odors",
                ],
                "lifestyle": [
                    "Eat slowly",
                    "Avoid fatty foods",
                    "Stay upright after eating",
                    "Fresh air",
                ],
                "warning_signs": [
                    "Severe abdominal pain",
                    "Blood in vomit",
                    "Signs of dehydration",
                    "Persistent vomiting",
                ],
            },
            "dizziness": {
                "severity": "medium",
                "advice": "Sit or lie down immediately, stay hydrated",
                "home_remedies": ["Drink water", "Deep breathing", "Ginger tea", "Rest in dark room"],
                "lifestyle": [
                    "Rise slowly from sitting/lying",
                    "Avoid sudden movements",
                    "Stay hydrated",
                    "Avoid alcohol",
                ],
                "warning_signs": [
                    "Chest pain",
                    "Difficulty breathing",
                    "Severe headache",
                    "Loss of consciousness",
                ],
            },
            "chest pain": {
                "severity": "high",
                "advice": "Seek immediate medical attention",
                "home_remedies": [],
                "lifestyle": [],
                "warning_signs": [
                    "Any chest pain",
                    "Pain radiating to arm/jaw",
                    "Shortness of breath",
                    "Sweating with chest pain",
                ],
            },
            "abdominal pain": {
                "severity": "medium",
                "advice": "Rest, avoid solid foods temporarily, stay hydrated",
                "home_remedies": [
                    "Warm compress",
                    "Chamomile tea",
                    "Small sips of water",
                    "Avoid trigger foods",
                ],
                "lifestyle": [
                    "Eat smaller meals",
                    "Avoid spicy foods",
                    "Reduce stress",
                    "Regular exercise",
                ],
                "warning_signs": [
                    "Severe pain",
                    "Blood in stool",
                    "Persistent vomiting",
                    "Fever with pain",
                ],
            },
            "fatigue": {
                "severity": "low",
                "advice": "Get adequate rest, maintain balanced diet, stay hydrated",
                "home_remedies": [
                    "Regular sleep schedule",
                    "Light exercise",
                    "Balanced nutrition",
                    "Stress management",
                ],
                "lifestyle": [
                    "7-9 hours sleep",
                    "Regular physical activity",
                    "Healthy diet",
                    "Limit caffeine",
                ],
                "warning_signs": [
                    "Extreme exhaustion",
                    "Unexplained weight loss",
                    "Persistent fatigue >2 weeks",
                    "With other symptoms",
                ],
            },
        }

    def analyze_symptoms(self, symptom_description: str, use_ai: bool = True) -> Dict:
        detected_symptoms = []
        for symptom_key in self.symptom_rules.keys():
            if symptom_key in symptom_description.lower():
                detected_symptoms.append(symptom_key)

        if not detected_symptoms and use_ai:
            detected_symptoms = self._ai_identify_symptoms(symptom_description)

        all_remedies = []
        all_lifestyle = []
        all_warnings = []
        max_severity = "low"

        for symptom in detected_symptoms:
            if symptom in self.symptom_rules:
                rule = self.symptom_rules[symptom]
                all_remedies.extend(rule.get("home_remedies", []))
                all_lifestyle.extend(rule.get("lifestyle", []))
                all_warnings.extend(rule.get("warning_signs", []))

                if rule["severity"] == "high":
                    max_severity = "high"
                elif rule["severity"] == "medium" and max_severity != "high":
                    max_severity = "medium"

        result = {
            "timestamp": datetime.now().isoformat(),
            "input_symptoms": symptom_description,
            "detected_symptoms": list(set(detected_symptoms)),
            "severity": max_severity,
            "home_remedies": list(set(all_remedies)),
            "lifestyle_suggestions": list(set(all_lifestyle)),
            "warning_signs": list(set(all_warnings)),
            "ai_explanation": "",
            "analysis_method": "AI-Enhanced" if use_ai else "Rule-Based",
        }

        if use_ai and detected_symptoms:
            result["ai_explanation"] = self._generate_ai_explanation(
                symptom_description, detected_symptoms
            )

        return result

    def _ai_identify_symptoms(self, description: str) -> List[str]:
        try:
            prompt = f"""Identify the main symptoms from this description. Return ONLY a comma-separated list of symptom keywords (e.g., fever, headache, cough).

Description: {description}

Return only the symptom keywords, nothing else:"""

            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
            symptoms_text = response["message"]["content"].strip()
            symptoms = [symptom.strip().lower() for symptom in symptoms_text.split(",")]
            return [symptom for symptom in symptoms if symptom in self.symptom_rules]
        except Exception as exc:
            print(f"AI symptom identification failed: {exc}")
            return []

    def _generate_ai_explanation(self, description: str, symptoms: List[str]) -> str:
        try:
            prompt = f"""You are a medical education assistant. Provide a brief, educational explanation about these symptoms in 2-3 sentences. Be supportive and informative, but always emphasize this is educational only.

Symptoms: {", ".join(symptoms)}
User description: {description}

Provide a brief educational explanation:"""

            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
            return response["message"]["content"].strip()
        except Exception as exc:
            print(f"AI explanation generation failed: {exc}")
            return self._build_fallback_explanation(description, symptoms)

    def get_home_remedies(self, symptom: str) -> List[str]:
        if symptom.lower() in self.symptom_rules:
            return self.symptom_rules[symptom.lower()].get("home_remedies", [])
        return []

    def get_lifestyle_suggestions(self, symptom: str) -> List[str]:
        if symptom.lower() in self.symptom_rules:
            return self.symptom_rules[symptom.lower()].get("lifestyle", [])
        return []

    def check_warning_signs(self, symptoms: List[str]) -> List[str]:
        warnings = []
        for symptom in symptoms:
            if symptom.lower() in self.symptom_rules:
                warnings.extend(self.symptom_rules[symptom.lower()].get("warning_signs", []))
        return list(set(warnings))
