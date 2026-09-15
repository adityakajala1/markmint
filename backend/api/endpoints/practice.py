from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.models.core import Course, Exam, Section, Question

router = APIRouter()

@router.get("/practice/{subject}")
def get_practice_questions(subject: str, limit: int = 20):
    db = SessionLocal()
    try:
        course = db.query(Course).filter(Course.name == subject).first()
        if not course:
            raise HTTPException(status_code=404, detail="Subject not found")

        # Fetch recent historical questions
        questions = db.query(Question, Exam.year).join(Section).join(Exam).filter(
            Exam.course_id == course.id
        ).order_by(Exam.year.desc()).limit(limit).all()

        formatted_questions = []
        for q, year in questions:
            formatted_questions.append({
                "id": q.id,
                "text": q.original_text,
                "year": year,
                "marks": q.marks,
                "family": q.family.canonical_name if q.family else None
            })

        return {
            "subject": subject,
            "questions": formatted_questions
        }
    finally:
        db.close()
