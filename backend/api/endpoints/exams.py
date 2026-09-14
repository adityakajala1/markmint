from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from backend.core.database import get_db
from backend.schemas import Exam, ExamCreate, Question
from backend.schemas import Page
from backend.schemas import ExamDNA
from backend.schemas import ExamPredictions
from backend.services.exam import ExamService

router = APIRouter()

@router.post("/", response_model=Exam)
def create_exam(exam_in: ExamCreate, db: Session = Depends(get_db)) -> Exam:
    service = ExamService(db)
    return service.create_exam(exam_in)

from pydantic import BaseModel
from backend.schemas import DocumentExtractionResult

class ExamImportRequest(BaseModel):
    course_id: int
    year: int
    term: str
    extraction: DocumentExtractionResult

@router.post("/import", response_model=Exam)
def import_exam_extraction(import_req: ExamImportRequest, db: Session = Depends(get_db)) -> Exam:
    service = ExamService(db)
    exam = service.import_extraction(
        course_id=import_req.course_id,
        year=import_req.year,
        term=import_req.term,
        extraction_data=import_req.extraction.model_dump()
    )
    return exam

@router.get("/{exam_id}", response_model=Exam)
def get_exam(exam_id: int, db: Session = Depends(get_db)) -> Exam:
    service = ExamService(db)
    exam = service.get_exam(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@router.get("/{exam_id}/questions", response_model=Page[Question])
def get_exam_questions(
    exam_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    unit: Optional[str] = None,
    topic: Optional[str] = None,
    question_type: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Page[Question]:
    service = ExamService(db)
    return service.get_exam_questions(exam_id, page, size, unit, topic, question_type) # type: ignore


