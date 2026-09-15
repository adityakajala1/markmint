import hashlib
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.api.endpoints.predictions import get_prediction
from backend.core.database import SessionLocal
from backend.models.core import Course
from backend.services.student_uploads import StudentUploadService
from backend.services.study_intelligence import StudyIntelligenceService

router = APIRouter(prefix="/study", tags=["study"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProgressRequest(BaseModel):
    user_id: str = "anonymous"
    topic_id: int
    status: Optional[str] = None
    viewed_resource: bool = False
    practice_attempted: bool = False
    practice_accuracy: Optional[float] = None


def _course(db: Session, course_name: str) -> Course:
    course = db.query(Course).filter(Course.name == course_name).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


def _topic_predictions(course_name: str, target_year: Optional[int], db: Session):
    prediction_payload = get_prediction(course_name, target_year, db)
    return prediction_payload, prediction_payload.get("predictions", [])


@router.get("/priorities/{course_name}")
def get_study_priorities(
    course_name: str,
    target_year: Optional[int] = None,
    user_id: str = "anonymous",
):
    db = SessionLocal()
    try:
        course = _course(db, course_name)
        payload, predictions = _topic_predictions(course.name, target_year, db)
        topic_predictions = [p for p in predictions if p.get("category") == "topic"]
        from backend.services.prediction.engine import PredictionResult

        model_predictions = [
            PredictionResult(
                target=item.get("category", "topic"),
                name=item["name"],
                rank=item.get("rank", index),
                score=float(item.get("score", 0.0)),
                confidence=item.get("confidence", "LOW"),
                evidence=item.get("evidence_details", {}),
            )
            for index, item in enumerate(topic_predictions, start=1)
        ]
        plan = StudyIntelligenceService(db).generate_study_plan(
            model_predictions, course.id, user_id
        )
        return {
            "course": course.name,
            "target_year": payload["target_year"],
            "priorities": plan,
            "prediction_evidence": payload.get("evidence"),
            "data_quality": payload.get("data_quality"),
        }
    finally:
        db.close()


@router.get("/plan/{course_name}")
def get_study_plan(course_name: str, target_year: Optional[int] = None, user_id: str = "anonymous"):
    return get_study_priorities(course_name, target_year, user_id)


@router.get("/resources/{course_name}/{topic_name}")
def get_topic_resources(course_name: str, topic_name: str, limit: int = 20):
    db = SessionLocal()
    try:
        course = _course(db, course_name)
        resources = StudyIntelligenceService(db).get_topic_resources(topic_name, course.id)
        return {"course": course.name, "topic": topic_name, "resources": resources[:limit]}
    finally:
        db.close()


@router.post("/uploads")
def upload_study_resource(
    file: UploadFile = File(...),
    course_id: int = Form(...),
    user_id: str = Form("anonymous"),
    resource_type: str = Form("student_notes"),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF study resources are supported")
    safe_name = Path(file.filename).name
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    content = file.file.read()
    stored_name = f"{hashlib.sha256(content).hexdigest()}_{safe_name}"
    file_path = upload_dir / stored_name
    file_path.write_bytes(content)

    upload_svc = StudentUploadService(db)
    try:
        doc = upload_svc.process_student_upload(
            str(file_path), safe_name, course_id, user_id, resource_type=resource_type
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "success": True,
        "document_id": doc.id,
        "filename": doc.title,
        "owner_id": doc.owner_id,
        "resource_type": doc.resource_type,
        "status": doc.processing_status,
    }


@router.post("/progress/{course_id}")
def update_progress(course_id: int, req: ProgressRequest, db: Session = Depends(get_db)):
    try:
        progress = StudyIntelligenceService(db).record_progress(
            student_id=req.user_id,
            course_id=course_id,
            topic_id=req.topic_id,
            status=req.status,
            viewed_resource=req.viewed_resource,
            practice_attempted=req.practice_attempted,
            practice_accuracy=req.practice_accuracy,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "success": True,
        "status": progress.status,
        "last_studied": progress.last_studied_at,
    }
