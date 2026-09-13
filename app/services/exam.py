from typing import Optional, Any
from sqlalchemy.orm import Session
from app.models.core import Exam, Question, Topic
from app.schemas.core import ExamCreate
from app.repositories.base import BaseRepository
from app.schemas.pagination import Page
from app.schemas.dna import ExamDNA
from app.schemas.prediction import ExamPredictions
from app.services.dna.analyzer import DNAAnalyzerService
from app.services.prediction.engine import PredictionEngineService

class ExamRepository(BaseRepository[Exam]):
    pass

class ExamService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ExamRepository(Exam)

    def create_exam(self, exam_in: ExamCreate) -> Exam:
        return self.repo.create(self.db, obj_in=exam_in.model_dump())

    def get_exam(self, exam_id: int) -> Exam | None:
        return self.repo.get(self.db, exam_id)

    def get_exam_questions(
        self, 
        exam_id: int, 
        page: int = 1, 
        size: int = 50,
        unit: Optional[str] = None,
        topic: Optional[str] = None,
        question_type: Optional[str] = None
    ) -> Page[Any]: # Any used for simplicity here, but should be QuestionSchema
        
        query = self.db.query(Question).filter(Question.section.has(exam_id=exam_id))
        
        if question_type:
            query = query.filter(Question.question_type == question_type)
            
        if topic:
            query = query.filter(Question.topics.any(Topic.name == topic))
            
        # Add unit filtering if unit relation exists from topic -> unit
        # if unit: ...
            
        total = query.count()
        pages = (total + size - 1) // size
        
        items = query.offset((page - 1) * size).limit(size).all()
        
        return Page(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    def get_exam_dna(self, exam_id: int) -> ExamDNA:
        # In a real scenario, this would query historical exams for the same course.
        # Here we mock retrieving the structured dict required by DNAAnalyzer.
        # This prevents DB logic leaking directly into routes.
        
        # Mock payload:
        mock_exams = [
            {
                "id": "e1",
                "year": 2023,
                "questions": [
                    {"id": "q1", "marks": 5.0, "topic": "Graphs", "question_type": "explanation"}
                ]
            }
        ]
        return DNAAnalyzerService.analyze(mock_exams)

    def get_exam_predictions(self, exam_id: int) -> ExamPredictions:
        engine = PredictionEngineService()
        mock_exams = [
            {"id": "e1", "year": 2021, "questions": [{"id": "q1", "topic": "Trees", "marks": 20.0}]},
            {"id": "e2", "year": 2022, "questions": [{"id": "q2", "topic": "Trees", "marks": 25.0}]},
            {"id": "e3", "year": 2023, "questions": [{"id": "q3", "topic": "Trees", "marks": 25.0}]}
        ]
        return engine.generate_predictions(mock_exams)
