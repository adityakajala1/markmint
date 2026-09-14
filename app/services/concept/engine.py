from typing import Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.core import (
    Concept, StudyEvidence, Document, Exam, Section, Question, QuestionConcept,
    syllabus_concept, Unit, Subtopic
)
from app.schemas import (
    ConceptEvidenceReport,
    ExamEvidenceStats,
    StudyEvidenceStats,
    SyllabusEvidenceStats
)

class ConceptIntelligenceEngine:
    def __init__(self, db: Session):
        self.db = db

    def _determine_coverage_strength(self, num_docs: int, num_chunks: int) -> str:
        if num_docs == 0 or num_chunks == 0:
            return "NONE"
        if num_docs >= 3 and num_chunks >= 5:
            return "STRONG"
        if num_docs >= 1 and num_chunks >= 2:
            return "MODERATE"
        return "WEAK"

    def get_concept_evidence(self, concept_id: int) -> Optional[ConceptEvidenceReport]:
        concept = self.db.query(Concept).filter(Concept.id == concept_id).first()
        if not concept:
            return None

        # 1. Exam Evidence
        exam_query = (
            self.db.query(Exam)
            .join(Section, Section.exam_id == Exam.id)
            .join(Question, Question.section_id == Section.id)
            .join(QuestionConcept, QuestionConcept.question_id == Question.id)
            .filter(QuestionConcept.concept_id == concept_id)
        )
        
        exams = exam_query.all()
        exam_ids = {e.id for e in exams}
        exam_years = sorted(list({e.year for e in exams if e.year}))
        exam_types = list({e.document.exam_type for e in exams if e.document and e.document.exam_type})

        questions = (
            self.db.query(Question)
            .join(QuestionConcept, QuestionConcept.question_id == Question.id)
            .filter(QuestionConcept.concept_id == concept_id)
            .all()
        )
        total_marks = sum(q.marks or 0.0 for q in questions)
        q_ids = [q.id for q in questions]
        
        families = list({q.family.name for q in questions if q.family})

        # Calculate recurrence interval roughly based on years
        interval = 0.0
        if len(exam_years) > 1:
            diffs = [exam_years[i] - exam_years[i-1] for i in range(1, len(exam_years))]
            interval = sum(diffs) / len(diffs)

        exam_stats = ExamEvidenceStats(
            number_of_papers=len(exam_ids),
            number_of_questions=len(questions),
            total_marks=total_marks,
            years=exam_years,
            exam_types=exam_types,
            question_ids=q_ids,
            question_families=families,
            recurrence_interval=interval
        )

        # 2. Study Evidence
        study_chunks = (
            self.db.query(StudyEvidence)
            .filter(StudyEvidence.concept_id == concept_id)
            .all()
        )
        
        doc_ids = {s.document_id for s in study_chunks}
        source_types = list({s.document.resource_type for s in study_chunks if s.document and s.document.resource_type})
        
        num_docs = len(doc_ids)
        num_chunks = len(study_chunks)
        coverage_strength = self._determine_coverage_strength(num_docs, num_chunks)

        study_stats = StudyEvidenceStats(
            number_of_documents=num_docs,
            number_of_evidence_chunks=num_chunks,
            source_types=source_types,
            source_diversity=len(set(source_types)),
            coverage_strength=coverage_strength,
            evidence_chunk_ids=[s.id for s in study_chunks]
        )

        # 3. Syllabus Evidence
        units = []
        unit_name = None
        subtopic_name = None

        if concept.unit_id:
            unit = self.db.query(Unit).filter(Unit.id == concept.unit_id).first()
            if unit:
                units.append(unit.name)
                unit_name = unit.name
                
        if concept.subtopic_id:
            sub = self.db.query(Subtopic).filter(Subtopic.id == concept.subtopic_id).first()
            if sub:
                subtopic_name = sub.name

        m2m_units = (
            self.db.query(Unit)
            .join(syllabus_concept, syllabus_concept.c.unit_id == Unit.id)
            .filter(syllabus_concept.c.concept_id == concept_id)
            .all()
        )
        for u in m2m_units:
            if u.name not in units:
                units.append(u.name)

        syllabus_stats = SyllabusEvidenceStats(
            units=units,
            syllabus_references=len(units)
        )
        
        related_ids = [c.id for c in concept.related_concepts]

        return ConceptEvidenceReport(
            concept_id=concept.id,
            canonical_name=concept.canonical_name,
            unit=unit_name,
            subtopic=subtopic_name,
            related_concept_ids=related_ids,
            exam_evidence=exam_stats,
            study_evidence=study_stats,
            syllabus_evidence=syllabus_stats
        )
