"""
Risk Scoring Engine
Emergency risk scoring and safety rules
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
from langchain_community.llms import Ollama

class RiskLevel(Enum):
    """Risk severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class RiskEngine:
    """
    Calculates emergency risk scores and provides safety guidance
    """
    
    def __init__(self):
        """
        Initialize risk scoring engine
        """
        self.risk_rules = {}
        self.load_risk_rules()
    
    def load_risk_rules(self):
        """
        Load rule-based risk scoring criteria
        """
        self.risk_rules = {
            "chest pain": {"base_score": 85, "severity_multiplier": 1.5, "category": "cardiac"},
            "difficulty breathing": {"base_score": 80, "severity_multiplier": 1.4, "category": "respiratory"},
            "severe headache": {"base_score": 65, "severity_multiplier": 1.3, "category": "neurological"},
            "confusion": {"base_score": 75, "severity_multiplier": 1.4, "category": "neurological"},
            "loss of consciousness": {"base_score": 95, "severity_multiplier": 1.5, "category": "neurological"},
            "seizure": {"base_score": 90, "severity_multiplier": 1.5, "category": "neurological"},
            "severe bleeding": {"base_score": 85, "severity_multiplier": 1.4, "category": "trauma"},
            "severe abdominal pain": {"base_score": 70, "severity_multiplier": 1.3, "category": "abdominal"},
            "high fever": {"base_score": 50, "severity_multiplier": 1.2, "category": "infection"},
            "persistent vomiting": {"base_score": 45, "severity_multiplier": 1.2, "category": "gastrointestinal"},
            "severe allergic reaction": {"base_score": 90, "severity_multiplier": 1.5, "category": "allergic"},
            "difficulty swallowing": {"base_score": 60, "severity_multiplier": 1.3, "category": "respiratory"},
            "sudden vision loss": {"base_score": 80, "severity_multiplier": 1.4, "category": "sensory"},
            "severe dizziness": {"base_score": 55, "severity_multiplier": 1.2, "category": "neurological"},
            "chest tightness": {"base_score": 70, "severity_multiplier": 1.3, "category": "cardiac"},
            "irregular heartbeat": {"base_score": 65, "severity_multiplier": 1.3, "category": "cardiac"},
            "numbness": {"base_score": 60, "severity_multiplier": 1.3, "category": "neurological"},
            "weakness": {"base_score": 50, "severity_multiplier": 1.2, "category": "general"},
            "coughing blood": {"base_score": 85, "severity_multiplier": 1.4, "category": "respiratory"},
            "severe pain": {"base_score": 60, "severity_multiplier": 1.3, "category": "general"}
        }
    
    def calculate_risk_score(self, symptoms: str, severity: int, 
                            age: Optional[int] = None, 
                            gender: Optional[str] = None,
                            medical_history: Optional[List[str]] = None,
                            use_ai: bool = True) -> Dict:
        """
        Calculate emergency risk score based on symptoms and factors
        
        Args:
            symptoms: Symptom description
            severity: Severity level (1-10)
            age: Patient age (optional)
            gender: Patient gender (optional)
            medical_history: List of medical conditions (optional)
            use_ai: Whether to use AI for enhanced analysis
            
        Returns:
            Risk assessment dictionary
        """
        # Identify risk factors from symptoms
        risk_factors = []
        base_score = 0
        categories = set()
        
        symptoms_lower = symptoms.lower()
        for keyword, rule in self.risk_rules.items():
            if keyword in symptoms_lower:
                base_score += rule["base_score"]
                risk_factors.append(keyword)
                categories.add(rule["category"])
        
        # If no keywords matched, use base severity
        if base_score == 0:
            base_score = severity * 5
        
        # Adjust for severity (1-10 scale)
        severity_factor = severity / 10
        adjusted_score = base_score * severity_factor
        
        # Age adjustments
        age_factor = 1.0
        if age:
            if age < 5 or age > 65:
                age_factor = 1.2
                risk_factors.append(f"Age factor: {age} years")
            elif age > 75:
                age_factor = 1.3
                risk_factors.append(f"Advanced age: {age} years")
        
        adjusted_score *= age_factor
        
        # Medical history adjustments
        history_factor = 1.0
        if medical_history:
            high_risk_conditions = ["heart disease", "diabetes", "hypertension", "asthma", "copd"]
            for condition in medical_history:
                if any(risk_cond in condition.lower() for risk_cond in high_risk_conditions):
                    history_factor = 1.15
                    risk_factors.append(f"Medical history: {condition}")
                    break
        
        adjusted_score *= history_factor
        
        # Cap score at 100
        final_score = min(adjusted_score, 100)
        
        # Determine risk level
        if final_score >= 70:
            risk_level = RiskLevel.HIGH
        elif final_score >= 40:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Generate AI safety note if enabled
        ai_safety_note = ""
        if use_ai:
            ai_safety_note = self.generate_safety_note({
                "symptoms": symptoms,
                "risk_level": risk_level.value,
                "risk_factors": risk_factors,
                "categories": list(categories)
            })
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "risk_score": round(final_score, 1),
            "risk_level": risk_level.value,
            "risk_factors": risk_factors,
            "affected_categories": list(categories),
            "severity_input": severity,
            "age": age,
            "gender": gender,
            "recommendation": self.get_recommendation(risk_level),
            "ai_safety_note": ai_safety_note,
            "calculation_details": {
                "base_score": round(base_score, 1),
                "severity_factor": severity_factor,
                "age_factor": age_factor,
                "history_factor": history_factor
            }
        }
        
        return result
    
    def get_recommendation(self, risk_level: RiskLevel) -> str:
        """
        Get recommendation based on risk level
        
        Args:
            risk_level: Calculated risk level
            
        Returns:
            Recommendation string
        """
        recommendations = {
            RiskLevel.HIGH: "🚨 SEEK IMMEDIATE MEDICAL ATTENTION. Call emergency services (911) or go to the nearest emergency room immediately.",
            RiskLevel.MEDIUM: "⚠️ CONSULT A HEALTHCARE PROVIDER SOON. Schedule an appointment within 24 hours. Monitor symptoms closely and seek immediate care if they worsen.",
            RiskLevel.LOW: "ℹ️ MONITOR SYMPTOMS. Consider consulting a healthcare provider if symptoms persist for more than 2-3 days or worsen. Practice self-care and rest."
        }
        return recommendations.get(risk_level, "Consult a healthcare provider for proper evaluation.")
    
    def classify_severity(self, symptoms: Dict) -> str:
        """
        Classify overall severity based on symptom analysis
        
        Args:
            symptoms: Dictionary of symptoms with details
            
        Returns:
            Severity classification
        """
        # Check for high-risk keywords
        high_risk_keywords = ["chest pain", "difficulty breathing", "loss of consciousness", "severe bleeding"]
        
        if any(keyword in str(symptoms).lower() for keyword in high_risk_keywords):
            return "HIGH"
        
        return "MEDIUM"
    
    def generate_safety_note(self, risk_assessment: Dict) -> str:
        """
        Generate AI-enhanced safety note
        
        Args:
            risk_assessment: Risk assessment results
            
        Returns:
            Safety note string
        """
        try:
            prompt = f"""You are a medical safety assistant. Based on this risk assessment, provide a brief, supportive safety note in 2-3 sentences. Be clear, compassionate, and emphasize this is educational guidance only.

Risk Level: {risk_assessment['risk_level']}
Symptoms: {risk_assessment['symptoms']}
Risk Factors: {', '.join(risk_assessment['risk_factors'][:3])}

Provide a brief safety note:"""

            llm = Ollama(model='llama3')
            return llm.invoke(prompt).strip()
            
        except Exception as e:
            print(f"AI safety note generation failed: {e}")
            return "Please consult with a healthcare professional for personalized medical advice."
    
    def analyze_side_effects(self, medicine: str, dosage: str, experience: str, 
                            age: int, gender: str, use_ai: bool = True) -> Dict:
        """
        Analyze post-medication side effects
        
        Args:
            medicine: Medicine name
            dosage: Dosage taken
            experience: User's experience description
            age: Patient age
            gender: Patient gender
            use_ai: Whether to use AI analysis
            
        Returns:
            Side effect analysis
        """
        # Identify severity keywords
        severe_keywords = ["severe", "extreme", "unbearable", "emergency", "allergic", "swelling", "difficulty breathing"]
        moderate_keywords = ["uncomfortable", "painful", "dizzy", "nausea", "headache"]
        
        experience_lower = experience.lower()
        
        severity = "mild"
        if any(keyword in experience_lower for keyword in severe_keywords):
            severity = "severe"
        elif any(keyword in experience_lower for keyword in moderate_keywords):
            severity = "moderate"
        
        # Generate AI analysis
        ai_analysis = ""
        if use_ai:
            ai_analysis = self._generate_side_effect_analysis(medicine, dosage, experience, age, gender, severity)
        
        # Recommendation based on severity
        if severity == "severe":
            recommendation = "🚨 STOP taking the medicine and seek immediate medical attention. This may be a serious adverse reaction."
        elif severity == "moderate":
            recommendation = "⚠️ Contact your healthcare provider soon. They may need to adjust your dosage or switch medications."
        else:
            recommendation = "ℹ️ Monitor the side effects. If they persist or worsen, consult your healthcare provider."
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "medicine": medicine,
            "dosage": dosage,
            "experience": experience,
            "age": age,
            "gender": gender,
            "severity": severity,
            "recommendation": recommendation,
            "ai_analysis": ai_analysis
        }
        
        return result
    
    def _generate_side_effect_analysis(self, medicine: str, dosage: str, experience: str, 
                                      age: int, gender: str, severity: str) -> str:
        """
        Generate AI analysis of side effects
        
        Args:
            medicine: Medicine name
            dosage: Dosage
            experience: Experience description
            age: Age
            gender: Gender
            severity: Detected severity
            
        Returns:
            AI-generated analysis
        """
        try:
            prompt = f"""You are a medical education assistant. Analyze this post-medication experience and provide brief educational guidance in 2-3 sentences. Be supportive and informative.

Medicine: {medicine}
Dosage: {dosage}
Experience: {experience}
Age: {age}, Gender: {gender}
Severity: {severity}

Provide brief educational analysis:"""

            llm = Ollama(model='llama3')
            return llm.invoke(prompt).strip()
            
        except Exception as e:
            print(f"AI side effect analysis failed: {e}")
            return "Unable to generate AI analysis. Please consult your healthcare provider about these side effects."


# Example usage
if __name__ == "__main__":
    engine = RiskEngine()
    print("Risk Scoring Engine Module - Activity 2.3 implementation complete")
    
    # Test risk calculation
    test_result = engine.calculate_risk_score(
        symptoms="chest pain and difficulty breathing",
        severity=8,
        age=65,
        use_ai=False
    )
    print(f"Test Risk Assessment: {test_result}")
