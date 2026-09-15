from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.schemas import Course, CourseCreate
from backend.services.course import CourseService

router = APIRouter()

@router.post("/", response_model=Course)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)) -> Course:
    service = CourseService(db)
    return service.create_course(course_in)

@router.get("/", response_model=list[Course])
def get_courses(db: Session = Depends(get_db)) -> list[Course]:
    service = CourseService(db)
    return service.db.query(service.repo.model).all()

@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int, db: Session = Depends(get_db)) -> Course:
    service = CourseService(db)
    course = service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

