from typing import Optional, Any
from sqlalchemy.orm import Session
from backend.models.core import Exam, Question, Topic
from backend.schemas import ExamCreate
from backend.repositories.base import BaseRepository
from backend.schemas import Page
from backend.schemas import ExamDNA
from backend.schemas import ExamPredictions
from backend.services.dna.analyzer import DNAAnalyzerService
from backend.services.prediction.engine import PredictionEngineService

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
        target_exam = self.get_exam(exam_id)
        if not target_exam:
            # Fallback or raise, but for now we return an empty DNA if not found
            return DNAAnalyzerService._empty_dna()
            
        # Fetch all exams for this course
        historical_exams = self.db.query(Exam).filter(Exam.course_id == target_exam.course_id).all()
        
        # Build the payload expected by DNAAnalyzerService
        exam_payloads = []
        for ex in historical_exams:
            q_payloads = []
            for sec in ex.sections:
                for q in sec.questions:
                    # Get the first topic if it exists
                    topic_name = q.topics[0].name if q.topics else None
                    q_payloads.append({
                        "id": str(q.id),
                        "marks": q.marks or 0.0,
                        "topic": topic_name,
                        "unit": q.topics[0].unit.name if q.topics and q.topics[0].unit else None,
                        "question_type": q.question_type,
                        "cognitive_level": q.cognitive_level,
                        "difficulty": q.difficulty,
                        "repetition_type": q.family.repetition_type if q.family else None,
                        "year": ex.year
                    })
            exam_payloads.append({
                "id": str(ex.id),
                "year": ex.year,
                "questions": q_payloads
            })
            
        return DNAAnalyzerService.analyze(exam_payloads)

    def get_exam_predictions(self, exam_id: int) -> ExamPredictions:
        engine = PredictionEngineService()
        target_exam = self.get_exam(exam_id)
        if not target_exam:
            return ExamPredictions(predictions=[], total_papers_analyzed=0, insufficient_data=True)
            
        historical_exams = self.db.query(Exam).filter(Exam.course_id == target_exam.course_id).all()
        
        exam_payloads = []
        for ex in historical_exams:
            q_payloads = []
            for sec in ex.sections:
                for q in sec.questions:
                    topic_name = q.topics[0].name if q.topics else None
                    q_payloads.append({
                        "id": str(q.id),
                        "topic": topic_name,
                        "marks": q.marks or 0.0
                    })
            exam_payloads.append({
                "id": str(ex.id),
                "year": ex.year,
                "questions": q_payloads
            })
            
        return engine.generate_predictions(exam_payloads)

    def import_extraction(self, course_id: int, year: int, term: str, extraction_data: dict) -> Exam:
        from backend.models.core import Section
        
        # Create exam
        new_exam = Exam(course_id=course_id, year=year, term=term)
        self.db.add(new_exam)
        self.db.flush() # get ID
        
        for sec_data in extraction_data.get('sections', []):
            new_section = Section(
                exam_id=new_exam.id,
                name=sec_data.get('name', 'General'),
                instructions=sec_data.get('instructions')
            )
            self.db.add(new_section)
            self.db.flush()
            
            for q_data in sec_data.get('questions', []):
                new_q = Question(
                    section_id=new_section.id,
                    question_number=q_data.get('question_number', '?'),
                    original_text=q_data.get('original_text', ''),
                    marks=q_data.get('marks')
                )
                self.db.add(new_q)
                
        self.db.commit()
        self.db.refresh(new_exam)
        return new_exam
