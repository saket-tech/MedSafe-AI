from typing import List, Optional

from pydantic import BaseModel, Field


class InteractionRequest(BaseModel):
    medicines: List[str] = Field(default_factory=list)


class SymptomAnalysisRequest(BaseModel):
    symptoms: str
    use_ai: bool = True


class SideEffectRequest(BaseModel):
    medicine: str
    dosage: str = ""
    experience: str
    age: int
    gender: str
    use_ai: bool = True


class RiskAssessmentRequest(BaseModel):
    symptoms: str
    severity: int = Field(ge=1, le=10)
    age: Optional[int] = None
    gender: Optional[str] = None
    medical_history: Optional[List[str]] = None
    use_ai: bool = True
