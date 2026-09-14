from sqlalchemy.orm import Session
from backend.models.core import Course
from backend.schemas.core import CourseCreate
from backend.repositories.base import BaseRepository

class CourseRepository(BaseRepository[Course]):
    pass

class CourseService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CourseRepository(Course)

    def create_course(self, course_in: CourseCreate) -> Course:
        return self.repo.create(self.db, obj_in=course_in.model_dump())

    def get_course(self, course_id: int) -> Course | None:
        return self.repo.get(self.db, course_id)
