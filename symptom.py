"""
Symptom Analysis Module
Rule-based symptom advice logic and AI-enhanced guidance
"""

from typing import Dict, List, Optional
from datetime import datetime
import ollama
import re

class SymptomAnalyzer:
    """
    Provides symptom analysis and guidance
    """
    
    def __init__(self):
        """
        Initialize symptom analyzer
        """
        self.symptom_rules = {}
        self.load_symptom_rules()
    
    def load_symptom_rules(self):
        """
        Load rule-based symptom guidance
        """
        self.symptom_rules = {
            "fever": {
                "severity": "medium",
                "advice": "Monitor temperature regularly, stay hydrated, rest",
                "home_remedies": ["Drink plenty of fluids", "Take lukewarm bath", "Use cool compress", "Wear light clothing"],
                "lifestyle": ["Get adequate rest", "Avoid strenuous activity", "Stay in cool environment"],
                "warning_signs": ["Temperature >103°F (39.4°C)", "Fever lasting >3 days", "Severe headache with fever", "Difficulty breathing"]
            },
            "headache": {
                "severity": "low",
                "advice": "Rest in quiet, dark room, stay hydrated",
                "home_remedies": ["Apply cold or warm compress", "Drink water", "Practice relaxation techniques", "Gentle neck stretches"],
                "lifestyle": ["Maintain regular sleep schedule", "Reduce screen time", "Manage stress", "Avoid triggers"],
                "warning_signs": ["Sudden severe headache", "Headache with vision changes", "Headache with fever and stiff neck", "Headache after head injury"]
            },
            "cough": {
                "severity": "low",
                "advice": "Stay hydrated, use humidifier, avoid irritants",
                "home_remedies": ["Honey and warm water", "Steam inhalation", "Throat lozenges", "Elevate head while sleeping"],
                "lifestyle": ["Avoid smoking", "Stay away from pollutants", "Use humidifier", "Drink warm fluids"],
                "warning_signs": ["Coughing up blood", "Difficulty breathing", "Chest pain", "Persistent cough >3 weeks"]
            },
            "nausea": {
                "severity": "low",
                "advice": "Eat bland foods, stay hydrated, rest",
                "home_remedies": ["Ginger tea", "Peppermint", "Small frequent meals", "Avoid strong odors"],
                "lifestyle": ["Eat slowly", "Avoid fatty foods", "Stay upright after eating", "Fresh air"],
                "warning_signs": ["Severe abdominal pain", "Blood in vomit", "Signs of dehydration", "Persistent vomiting"]
            },
            "dizziness": {
                "severity": "medium",
                "advice": "Sit or lie down immediately, stay hydrated",
                "home_remedies": ["Drink water", "Deep breathing", "Ginger tea", "Rest in dark room"],
                "lifestyle": ["Rise slowly from sitting/lying", "Avoid sudden movements", "Stay hydrated", "Avoid alcohol"],
                "warning_signs": ["Chest pain", "Difficulty breathing", "Severe headache", "Loss of consciousness"]
            },
            "chest pain": {
                "severity": "high",
                "advice": "Seek immediate medical attention",
                "home_remedies": [],
                "lifestyle": [],
                "warning_signs": ["Any chest pain", "Pain radiating to arm/jaw", "Shortness of breath", "Sweating with chest pain"]
            },
            "abdominal pain": {
                "severity": "medium",
                "advice": "Rest, avoid solid foods temporarily, stay hydrated",
                "home_remedies": ["Warm compress", "Chamomile tea", "Small sips of water", "Avoid trigger foods"],
                "lifestyle": ["Eat smaller meals", "Avoid spicy foods", "Reduce stress", "Regular exercise"],
                "warning_signs": ["Severe pain", "Blood in stool", "Persistent vomiting", "Fever with pain"]
            },
            "fatigue": {
                "severity": "low",
                "advice": "Get adequate rest, maintain balanced diet, stay hydrated",
                "home_remedies": ["Regular sleep schedule", "Light exercise", "Balanced nutrition", "Stress management"],
                "lifestyle": ["7-9 hours sleep", "Regular physical activity", "Healthy diet", "Limit caffeine"],
                "warning_signs": ["Extreme exhaustion", "Unexplained weight loss", "Persistent fatigue >2 weeks", "With other symptoms"]
            }
        }
    
    def analyze_symptoms(self, symptom_description: str, use_ai: bool = True) -> Dict:
        """
        Analyze symptoms and provide guidance
        
        Args:
            symptom_description: User's symptom description
            use_ai: Whether to use AI for enhanced analysis
            
        Returns:
            Analysis results with guidance
        """
        # Basic keyword matching
        detected_symptoms = []
        for symptom_key in self.symptom_rules.keys():
            if symptom_key in symptom_description.lower():
                detected_symptoms.append(symptom_key)
        
        # If no symptoms detected, use AI to identify
        if not detected_symptoms and use_ai:
            detected_symptoms = self._ai_identify_symptoms(symptom_description)
        
        # Compile guidance
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
                
                # Update severity
                if rule["severity"] == "high":
                    max_severity = "high"
                elif rule["severity"] == "medium" and max_severity != "high":
                    max_severity = "medium"
        
        # Remove duplicates
        all_remedies = list(set(all_remedies))
        all_lifestyle = list(set(all_lifestyle))
        all_warnings = list(set(all_warnings))
        
        # Generate AI explanation if enabled
        ai_explanation = ""
        if use_ai and detected_symptoms:
            ai_explanation = self._generate_ai_explanation(symptom_description, detected_symptoms)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "input_symptoms": symptom_description,
            "detected_symptoms": detected_symptoms,
            "severity": max_severity,
            "home_remedies": all_remedies,
            "lifestyle_suggestions": all_lifestyle,
            "warning_signs": all_warnings,
            "ai_explanation": ai_explanation,
            "analysis_method": "AI-Enhanced" if use_ai else "Rule-Based"
        }
        
        return result
    
    def _ai_identify_symptoms(self, description: str) -> List[str]:
        """
        Use AI to identify symptoms from description
        
        Args:
            description: Symptom description
            
        Returns:
            List of identified symptoms
        """
        try:
            prompt = f"""Identify the main symptoms from this description. Return ONLY a comma-separated list of symptom keywords (e.g., fever, headache, cough).

Description: {description}

Return only the symptom keywords, nothing else:"""

            response = ollama.chat(
                model='llama3',
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            symptoms_text = response['message']['content'].strip()
            symptoms = [s.strip().lower() for s in symptoms_text.split(',')]
            
            # Filter to known symptoms
            return [s for s in symptoms if s in self.symptom_rules]
            
        except Exception as e:
            print(f"AI symptom identification failed: {e}")
            return []
    
    def _generate_ai_explanation(self, description: str, symptoms: List[str]) -> str:
        """
        Generate AI-enhanced educational explanation
        
        Args:
            description: Original symptom description
            symptoms: Detected symptoms
            
        Returns:
            AI-generated explanation
        """
        try:
            prompt = f"""You are a medical education assistant. Provide a brief, educational explanation about these symptoms in 2-3 sentences. Be supportive and informative, but always emphasize this is educational only.

Symptoms: {', '.join(symptoms)}
User description: {description}

Provide a brief educational explanation:"""

            response = ollama.chat(
                model='llama3',
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            print(f"AI explanation generation failed: {e}")
            return "Unable to generate AI explanation at this time."
    
    def get_home_remedies(self, symptom: str) -> List[str]:
        """
        Get home remedies for specific symptom
        
        Args:
            symptom: Symptom name
            
        Returns:
            List of home remedies
        """
        if symptom.lower() in self.symptom_rules:
            return self.symptom_rules[symptom.lower()].get("home_remedies", [])
        return []
    
    def get_lifestyle_suggestions(self, symptom: str) -> List[str]:
        """
        Get lifestyle suggestions for symptom management
        
        Args:
            symptom: Symptom name
            
        Returns:
            List of lifestyle suggestions
        """
        if symptom.lower() in self.symptom_rules:
            return self.symptom_rules[symptom.lower()].get("lifestyle", [])
        return []
    
    def check_warning_signs(self, symptoms: List[str]) -> List[str]:
        """
        Check for warning signs that require immediate attention
        
        Args:
            symptoms: List of symptoms
            
        Returns:
            List of warning signs
        """
        warnings = []
        for symptom in symptoms:
            if symptom.lower() in self.symptom_rules:
                warnings.extend(self.symptom_rules[symptom.lower()].get("warning_signs", []))
        return list(set(warnings))


# Example usage
if __name__ == "__main__":
    analyzer = SymptomAnalyzer()
    print("Symptom Analyzer Module - Activity 2.3 implementation complete")
