"""Deterministic study-priority and resource services."""

from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from backend.models.core import (
    Concept, Course, Document, Exam, MappingConfidence, Question, Section,
    StudentTopicProgress, StudyEvidence, Syllabus, Topic, Unit,
)
from backend.services.prediction.engine import PredictionResult


class StudyPriority(str):
    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class PriorityResult:
    def __init__(self, topic: str, prediction_score: float, priority: str,
                 reasons: List[str], resources: List[Dict[str, Any]]):
        self.topic = topic
        self.prediction_score = prediction_score
        self.priority = priority
        self.reasons = reasons
        self.resources = resources

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "prediction_score": self.prediction_score,
            "priority": self.priority,
            "reasons": self.reasons,
            "resources": self.resources,
        }


class StudyIntelligenceService:
    def __init__(self, db: Session):
        self.db = db

    def _course_topic(self, topic_name: str, course_id: int) -> Topic | None:
        if self.db is None:
            return None
        return self.db.query(Topic).join(Unit).join(Syllabus).filter(
            Topic.name == topic_name, Syllabus.course_id == course_id
        ).first()

    def _course_topic_by_id(self, topic_id: int, course_id: int) -> Topic | None:
        if self.db is None:
            return None
        return self.db.query(Topic).join(Unit).join(Syllabus).filter(
            Topic.id == topic_id, Syllabus.course_id == course_id
        ).first()

    def get_topic_resources(self, topic_name: str, course_id: int) -> List[Dict[str, Any]]:
        if self.db is None:
            return []
        topic = self._course_topic(topic_name, course_id)
        if not topic:
            return []
        course = self.db.query(Course).filter(Course.id == course_id).first()
        concept = self.db.query(Concept).filter(
            Concept.canonical_name == topic.name,
            Concept.unit_id == topic.unit_id,
        ).first()
        resources: List[Dict[str, Any]] = []
        if concept and course:
            evidence_rows = (
                self.db.query(StudyEvidence)
                .join(Document, StudyEvidence.document_id == Document.id)
                .filter(
                    StudyEvidence.concept_id == concept.id,
                    StudyEvidence.confidence.in_([MappingConfidence.HIGH, MappingConfidence.MEDIUM]),
                    Document.subject == course.name,
                )
                .all()
            )
            seen = set()
            for evidence in evidence_rows:
                if evidence.document_id in seen:
                    continue
                seen.add(evidence.document_id)
                document = evidence.document
                resources.append({
                    "id": document.id,
                    "title": document.title or "Untitled Document",
                    "source": document.source or "local",
                    "resource_type": document.resource_type or "study_material",
                    "original_url": document.original_url,
                    "uploaded_at": document.uploaded_at.isoformat() if document.uploaded_at else None,
                    "owner_id": document.owner_id,
                })

        question_count = (
            self.db.query(Question)
            .join(Section, Question.section_id == Section.id)
            .join(Exam, Section.exam_id == Exam.id)
            .join(Question.topics)
            .filter(Exam.course_id == course_id, Topic.id == topic.id)
            .count()
        )
        if question_count:
            resources.append({
                "id": None,
                "title": f"Previous exam questions for {topic.name}",
                "source": "historical_exams",
                "resource_type": "previous_exam_questions",
                "question_count": question_count,
            })
        return resources

    def calculate_study_priority(
        self, prediction: PredictionResult, course_id: int | None = None, student_id: str = "anonymous"
    ) -> PriorityResult:
        score = float(prediction.score)
        evidence = prediction.evidence or {}
        if score >= 0.8:
            priority = StudyPriority.VERY_HIGH
            reasons = [
                "Exceptionally high predicted probability.",
                "Very high predicted exam probability.",
            ]
        elif score >= 0.6:
            priority = StudyPriority.HIGH
            reasons = ["High predicted exam probability."]
        elif score >= 0.4:
            priority = StudyPriority.MEDIUM
            reasons = ["Moderate predicted exam probability."]
        else:
            priority = StudyPriority.LOW
            reasons = ["Lower predicted exam probability."]

        if evidence.get("occurrences", 0) >= 2 or evidence.get("freq", 0) > 0.3:
            reasons.append("Appears repeatedly in historical papers.")
        if evidence.get("recent_freq", 0) > 0.2:
            reasons.append("Appeared recently in historical papers.")
        if evidence.get("marks_weight", 0) > 0.15:
            reasons.append("Carries significant historical marks weight.")

        resources = self.get_topic_resources(prediction.name, course_id) if course_id is not None else []
        reasons.append(
            "Study material or related past questions are available."
            if resources else "No trusted topic-mapped study material is available."
        )

        topic = self._course_topic(prediction.name, course_id) if course_id is not None else None
        progress = (
            self.db.query(StudentTopicProgress).filter_by(
                student_id=student_id, topic_id=topic.id
            ).first() if topic else None
        )
        weak = course_id is not None and self.db is not None and not progress
        if progress and progress.practice_attempted:
            weak = (progress.practice_correct or 0) / progress.practice_attempted < 0.6
            if weak:
                reasons.append("Recorded practice accuracy is below 60%.")
        elif weak:
            reasons.append("No student progress evidence is recorded.")
        if weak and priority == StudyPriority.HIGH:
            priority = StudyPriority.VERY_HIGH
        elif weak and priority == StudyPriority.MEDIUM:
            priority = StudyPriority.HIGH

        return PriorityResult(prediction.name, round(score, 4), priority, reasons, resources)

    def generate_study_plan(
        self, predictions: List[PredictionResult], course_id: int, student_id: str = "anonymous"
    ) -> List[Dict[str, Any]]:
        priorities = [
            self.calculate_study_priority(prediction, course_id, student_id)
            for prediction in predictions if prediction.target == "topic"
        ]
        order = {StudyPriority.VERY_HIGH: 0, StudyPriority.HIGH: 1,
                 StudyPriority.MEDIUM: 2, StudyPriority.LOW: 3}
        priorities.sort(key=lambda item: (order[item.priority], -item.prediction_score, item.topic))
        return [{"order": index, **priority.to_dict()} for index, priority in enumerate(priorities, 1)]

    def record_progress(
        self, user_id: str, course_id: int, topic_id: int, status: str = None,
        viewed_resource: bool = False, practice_attempted: bool = False,
        practice_accuracy: float = None,
    ) -> StudentTopicProgress:
        if not self._course_topic_by_id(topic_id, course_id):
            raise ValueError("Topic does not belong to the selected course")
        progress = self.db.query(StudentTopicProgress).filter_by(
            student_id=user_id, topic_id=topic_id
        ).first()
        if not progress:
            progress = StudentTopicProgress(student_id=user_id, topic_id=topic_id)
            self.db.add(progress)
        if status:
            if status not in {"NOT_STARTED", "STARTED", "COMPLETED"}:
                raise ValueError("status must be NOT_STARTED, STARTED, or COMPLETED")
            progress.status = status
        if practice_attempted:
            progress.practice_attempted = (progress.practice_attempted or 0) + 1
            if practice_accuracy is not None and practice_accuracy >= 0.5:
                progress.practice_correct = (progress.practice_correct or 0) + 1
        progress.last_studied_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(progress)
        return progress
