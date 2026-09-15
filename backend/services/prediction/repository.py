from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List
from backend.models.core import Exam, Section, Question, QuestionFamily, QuestionFamilyMembership
from backend.services.prediction.context import HistoricalContext

class HistoricalRepository:
    """
    Enforces absolute temporal isolation. Every method in this repository MUST
    apply `Exam.year < cutoff_year` and `Exam.year IS NOT NULL`.
    """
    def __init__(self, db: Session, context: HistoricalContext):
        self.db = db
        self.context = context

    def get_historical_exams(self) -> List[Exam]:
        """Returns only exams strictly before the cutoff year."""
        return self.db.query(Exam).filter(
            Exam.course_id == self.context.course_id,
            Exam.year != None,
            Exam.year < self.context.cutoff_year
        ).order_by(Exam.year.asc()).all()

    def get_historical_questions(self) -> List[Question]:
        """Returns only questions belonging to historical exams."""
        return self.db.query(Question).join(Section).join(Exam).filter(
            Exam.course_id == self.context.course_id,
            Exam.year != None,
            Exam.year < self.context.cutoff_year
        ).all()

    def get_historical_family_memberships(self) -> List[QuestionFamilyMembership]:
        """Returns only memberships corresponding to historical questions."""
        return self.db.query(QuestionFamilyMembership).join(Question).join(Section).join(Exam).filter(
            Exam.course_id == self.context.course_id,
            Exam.year != None,
            Exam.year < self.context.cutoff_year
        ).all()

    def get_target_exams(self) -> List[Exam]:
        """Returns ONLY the target year exams. Never use this for historical feature generation!"""
        return self.db.query(Exam).filter(
            Exam.course_id == self.context.course_id,
            Exam.year == self.context.cutoff_year
        ).all()
