import os
import hashlib
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from backend.models.core import Document, Course
from backend.services.document import DocumentService
from backend.services.extraction.pdf_parser import PDFParser
from backend.services.extraction.knowledge_extractor import KnowledgeExtractor

class StudentUploadService:
    def __init__(self, db: Session):
        self.db = db
        self.doc_svc = DocumentService(db)

    def process_student_upload(
        self,
        file_path: str,
        filename: str,
        course_id: int,
        owner_id: str,
        resource_type: str = "student_notes",
    ) -> Document:
        # 1. Hash the file
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        file_hash = sha256.hexdigest()
        
        course = self.db.query(Course).get(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found.")

        # 2. Get or create document
        doc = self.doc_svc.get_or_create_document(
            document_hash=file_hash,
            source="student_upload",
            title=filename,
            subject=course.name,
            resource_type=resource_type,
            owner_id=owner_id
        )
        
        # If it's already processed, return
        if doc.extraction_status == "completed":
            return doc
            
        doc.processing_status = "processing"
        doc.uploaded_at = doc.uploaded_at or datetime.utcnow()
        self.db.commit()
        
        # 3. Extract knowledge
        try:
            with open(file_path, "rb") as f:
                pages_data = PDFParser.extract_text_with_pages(f)
                
            if not pages_data:
                doc.processing_status = "failed"
                self.db.commit()
                return doc
                
            result = KnowledgeExtractor.extract(pages_data)
            
            if result.successful:
                self.doc_svc.import_knowledge_extraction(
                    document_id=doc.id,
                    extraction_data=result.model_dump(),
                    course_id=course_id,
                )
                doc.processing_status = "completed"
                doc.extraction_status = "completed"
            else:
                doc.processing_status = "failed"
                
        except Exception as e:
            doc.processing_status = "error"
            print(f"Error processing upload: {e}")
            
        self.db.commit()
        self.db.refresh(doc)
        return doc
