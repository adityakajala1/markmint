from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.models.core import Course, StudyEvidence, Concept, Document, MappingConfidence, Syllabus, Unit

router = APIRouter()

@router.get("/study/{subject}")
def get_study_for_subject(subject: str, limit: int = 20):
    db = SessionLocal()
    try:
        course = db.query(Course).filter(Course.name == subject).first()
        if not course:
            raise HTTPException(status_code=404, detail="Subject not found")

        # Real DB query â€” existing StudyEvidence + Concept + Document
        # Fetch study evidence related to concepts for this course
        # Note: We filter by the course to restrict scope. Concepts belong to courses.
        evidence_records = (
            db.query(StudyEvidence)
            .join(Concept)
            .join(Unit, Concept.unit_id == Unit.id)
            .join(Syllabus, Unit.syllabus_id == Syllabus.id)
            .filter(
                Syllabus.course_id == course.id,
                StudyEvidence.confidence.in_([MappingConfidence.HIGH, MappingConfidence.MEDIUM]),
            )
            .limit(limit)
            .all()
        )

        formatted_evidence = []
        for e in evidence_records:
            formatted_evidence.append({
                "concept": e.concept.canonical_name,
                "knowledge_type": e.knowledge_type,
                "content": e.content,
                "source_doc": e.document.title if e.document else "Unknown",
                "page": e.page_number
            })

        # Isolated from exam statistics
        return {
            "subject": subject,
            "study_evidence": formatted_evidence,
            "note": "Study material separate from exam-frequency metrics."
        }
    finally:
        db.close()
