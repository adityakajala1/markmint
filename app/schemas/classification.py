from pydantic import BaseModel
from typing import Optional

class ClassificationResult(BaseModel):
    question_type: Optional[str] = None
    cognitive_level: Optional[str] = None
    difficulty: Optional[float] = None
    topics: list[str] = []
    confidence: float
