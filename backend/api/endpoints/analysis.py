from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
import time

from backend.core.database import get_db
from backend.models.core import Exam, Course, Section, Question, QuestionConcept
from backend.schemas import ExamDNA
from backend.schemas import EvolutionReport
from backend.services.dna.analyzer import DNAAnalyzerService
from backend.services.dna.evolution import ExamEvolutionService
from backend.services.prediction.backtester import BacktestEngine, BacktestReport

router = APIRouter()

# Simple in-memory cache for expensive analysis to avoid repeated DB hits
# Key: (course_id, analysis_type), Value: (timestamp, data)
_ANALYSIS_CACHE = {}
CACHE_TTL = 300 # 5 minutes

def _get_exams_as_dicts(course_id: int, db: Session) -> list[dict]:
    """
    Eagerly loads exams to avoid N+1 queries.
    Maps ORM objects to the dict structure expected by DNA Analyzer.
    """
    # Eager load relationships to prevent N+1
    exams = (
        db.query(Exam)
        .options(
            joinedload(Exam.document),
            joinedload(Exam.sections).joinedload(Section.questions).joinedload(Question.family)
        )
        .filter(Exam.course_id == course_id)
        .all()
    )
    
    out = []
    for ex in exams:
        ex_dict = {
            "id": ex.id,
            "year": ex.year,
            "exam_type": ex.document.exam_type if ex.document else None,
            "questions": []
        }
        for sec in ex.sections:
            for q in sec.questions:
                ex_dict["questions"].append({
                    "id": q.id,
                    "marks": q.marks,
                    "topic": q.topic,
                    "unit": None, # Unit mapped via concepts typically, stubbed here
                    "question_type": q.question_type,
                    "repetition_type": q.repetition_type,
                    "family_name": q.family.name if q.family else None,
                    "difficulty": None # Fallback
                })
        out.append(ex_dict)
    return out

@router.get("/dna", response_model=ExamDNA)
def get_course_dna(
    course_id: int = Query(..., description="The ID of the course to analyze"),
    db: Session = Depends(get_db)
):
    cache_key = (course_id, "dna")
    if cache_key in _ANALYSIS_CACHE:
        ts, data = _ANALYSIS_CACHE[cache_key]
        if time.time() - ts < CACHE_TTL:
            return data
            
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    exams_dict = _get_exams_as_dicts(course_id, db)
    dna_report = DNAAnalyzerService.analyze(exams_dict)
    
    _ANALYSIS_CACHE[cache_key] = (time.time(), dna_report)
    return dna_report

@router.get("/evolution", response_model=EvolutionReport)
def get_course_evolution(
    course_id: int = Query(..., description="The ID of the course to track"),
    db: Session = Depends(get_db)
):
    cache_key = (course_id, "evolution")
    if cache_key in _ANALYSIS_CACHE:
        ts, data = _ANALYSIS_CACHE[cache_key]
        if time.time() - ts < CACHE_TTL:
            return data

    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    exams_dict = _get_exams_as_dicts(course_id, db)
    evolution_report = ExamEvolutionService.analyze_evolution(course_id, exams_dict)
    
    _ANALYSIS_CACHE[cache_key] = (time.time(), evolution_report)
    return evolution_report

@router.get("/backtest", response_model=BacktestReport)
def get_course_backtest(
    course_id: int = Query(..., description="The ID of the course to backtest predictions"),
    db: Session = Depends(get_db)
):
    cache_key = (course_id, "backtest")
    if cache_key in _ANALYSIS_CACHE:
        ts, data = _ANALYSIS_CACHE[cache_key]
        if time.time() - ts < CACHE_TTL:
            return data

    engine = BacktestEngine(db)
    report = engine.run_backtest(course_id)
    if not report:
        raise HTTPException(status_code=422, detail="Insufficient chronological data for sliding-window backtest.")
        
    _ANALYSIS_CACHE[cache_key] = (time.time(), report)
    return report
