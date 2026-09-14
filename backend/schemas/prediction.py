from pydantic import BaseModel
from typing import Optional

class Prediction(BaseModel):
    characteristic: str
    predicted_insight: str
    confidence: str # "High", "Medium", "Low", "Insufficient Evidence"
    supporting_evidence: str
    sample_size: int
    historical_frequency: Optional[float] = None
    limitations: str

class ExamPredictions(BaseModel):
    predictions: list[Prediction]
    total_papers_analyzed: int
    insufficient_data: bool
