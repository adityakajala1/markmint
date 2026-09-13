from pydantic import BaseModel
from typing import Optional


class ExtractedQuestion(BaseModel):
    question_number: str
    original_text: str
    marks: Optional[float] = None
    page_number: int
    confidence: float


class ExtractedSection(BaseModel):
    name: str
    instructions: Optional[str] = None
    questions: list[ExtractedQuestion]


class DocumentExtractionResult(BaseModel):
    sections: list[ExtractedSection]
    total_pages: int
    successful: bool
    error_message: Optional[str] = None
