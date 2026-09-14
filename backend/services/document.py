from typing import Any
from sqlalchemy.orm import Session
from backend.models.core import Document, Exam, Section, Question, Concept, StudyEvidence

class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_document(self, document_hash: str, **kwargs) -> Document:
        query = self.db.query(Document).filter(Document.document_hash == document_hash)
        
        original_url = kwargs.get("original_url")
        if original_url:
            query = self.db.query(Document).filter(
                (Document.document_hash == document_hash) | (Document.original_url == original_url)
            )
            
        doc = query.first()
        
        if not doc:
            doc = Document(document_hash=document_hash, **kwargs)
            self.db.add(doc)
            self.db.commit()
            self.db.refresh(doc)
        return doc

    def _get_or_create_concept(self, canonical_name: str) -> Concept:
        concept = self.db.query(Concept).filter(Concept.canonical_name == canonical_name).first()
        if not concept:
            concept = Concept(canonical_name=canonical_name)
            self.db.add(concept)
            self.db.flush()
        return concept

    def import_exam_extraction(self, document_id: int, course_id: int, year: int, term: str, extraction_data: dict) -> Exam:
        # Idempotency check: if Exam exists for this document, delete its children and it to prepare for fresh insert
        existing_exam = self.db.query(Exam).filter(Exam.document_id == document_id).first()
        if existing_exam:
            for sec in existing_exam.sections:
                self.db.query(Question).filter(Question.section_id == sec.id).delete()
                self.db.delete(sec)
            self.db.delete(existing_exam)
            self.db.flush()

        new_exam = Exam(course_id=course_id, document_id=document_id, year=year, term=term)
        self.db.add(new_exam)
        self.db.flush()
        
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
                    marks=q_data.get('marks'),
                    is_alternative=q_data.get('is_alternative', False)
                )
                self.db.add(new_q)
                
        # Mark document as completed
        doc = self.db.query(Document).get(document_id)
        if doc:
            doc.extraction_status = "completed"
            doc.extraction_confidence = 0.9
            
        self.db.commit()
        self.db.refresh(new_exam)
        return new_exam

    def import_knowledge_extraction(self, document_id: int, extraction_data: dict):
        for concept_data in extraction_data.get('concepts', []):
            concept = self._get_or_create_concept(concept_data.get('concept_name', 'Unknown'))
            
            evidence = StudyEvidence(
                document_id=document_id,
                concept_id=concept.id,
                knowledge_type=concept_data.get('knowledge_type', 'context'),
                content=concept_data.get('content', ''),
                original_text=concept_data.get('original_text', ''),
                page_number=concept_data.get('page_number')
            )
            self.db.add(evidence)
            
        doc = self.db.query(Document).get(document_id)
        if doc:
            doc.extraction_status = "completed"
            doc.extraction_confidence = 0.8
            
        self.db.commit()
