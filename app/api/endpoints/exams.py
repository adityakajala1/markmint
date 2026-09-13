from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.schemas.core import Exam, ExamCreate, Question
from app.schemas.pagination import Page
from app.schemas.dna import ExamDNA
from app.schemas.prediction import ExamPredictions
from app.services.exam import ExamService

router = APIRouter()

@router.post("/", response_model=Exam)
def create_exam(exam_in: ExamCreate, db: Session = Depends(get_db)) -> Exam:
    service = ExamService(db)
    return service.create_exam(exam_in)

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

@router.get("/{exam_id}/dna", response_model=ExamDNA)
def get_exam_dna(exam_id: int, db: Session = Depends(get_db)) -> ExamDNA:
    service = ExamService(db)
    return service.get_exam_dna(exam_id)

@router.get("/{exam_id}/predictions", response_model=ExamPredictions)
def get_exam_predictions(exam_id: int, db: Session = Depends(get_db)) -> ExamPredictions:
    service = ExamService(db)
    return service.get_exam_predictions(exam_id)
