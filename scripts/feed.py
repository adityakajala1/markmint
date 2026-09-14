import os
import sqlite3
import json
import sys

os.environ['DATABASE_URL'] = 'sqlite:///./demo.db'

from sqlalchemy.exc import OperationalError
from app.core.database import SessionLocal, Base, engine
from app.models.core import Course
from app.services.extraction.pdf_parser import PDFParser
from app.services.extraction.question_extractor import QuestionExtractor
from app.services.extraction.knowledge_extractor import KnowledgeExtractor
from app.services.document import DocumentService


def categorize(filename):
    name = filename.lower()
    if 'syllabus' in name: return 'syllabi'
    if 'ct ' in name or 'ct-' in name or 'ct1' in name or 'ct2' in name or 'ct3' in name or 'class test' in name: return 'CT papers'
    if 'pyq' in name or 'previous' in name or 'paper' in name or 'exam' in name: return 'examination papers / PYQs'
    if 'question bank' in name or 'qb' in name: return 'question banks'
    if 'important' in name or 'imp' in name: return 'important questions'
    if 'notes' in name or 'lecture' in name or 'unit' in name or 'module' in name or 'chapter' in name: return 'lecture notes'
    if 'key' in name or 'solution' in name or 'ans' in name: return 'answer keys'
    return 'study material / other'


def process_downloads():
    print("Starting Ingestion Feeder...")
    db_path = "data/.download_cache/downloads.db"
    
    if not os.path.exists(db_path):
        print(f"Cache DB not found at {db_path}. Is the scraper running?")
        return

    # Ensure db tables exist
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        print("\n[!] CRITICAL: Could not connect to the database.")
        sys.exit(1)

    # Connect to scraper's SQLite DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if 'processed' column exists, if not add it
    cursor.execute("PRAGMA table_info(downloads)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'processed' not in columns:
        cursor.execute("ALTER TABLE downloads ADD COLUMN processed INTEGER DEFAULT 0")
        conn.commit()

    # Get unprocessed PDFs
    cursor.execute("SELECT id, local_path, source_metadata, sha256 FROM downloads WHERE processed = 0 AND local_path LIKE '%.pdf'")
    unprocessed = cursor.fetchall()
    
    if not unprocessed:
        print("No new unprocessed PDFs found in the scraper cache.")
        return
        
    print(f"Found {len(unprocessed)} unprocessed PDFs. Feeding into ExamScope Engine...")
    
    db = SessionLocal()
    doc_svc = DocumentService(db)
    
    for row_id, local_path, source_metadata, sha256_hash in unprocessed:
        print(f"\nProcessing [{row_id}]: {local_path}")
        
        if not os.path.exists(local_path):
            print(f"File missing: {local_path}")
            continue
            
        # Parse metadata
        meta = {}
        try:
            if source_metadata:
                meta = json.loads(source_metadata)
        except:
            if source_metadata and 'semester' in source_metadata:
                # Basic string parse "semester:1,subject:Calculus And Linear Algebra"
                parts = source_metadata.split(',')
                for p in parts:
                    k, v = p.split(':', 1)
                    meta[k.strip()] = v.strip()
            
        subject_name = meta.get('subject', 'Unknown Subject')
        semester = meta.get('semester', '1')
        
        filename = os.path.basename(local_path)
        title = filename[:-4] if filename.endswith('.pdf') else filename
        resource_type = categorize(filename)
        
        print(f"  [>] Type: {resource_type}")
        
        # Get or Create Course
        course = db.query(Course).filter_by(name=subject_name).first()
        if not course:
            course = Course(name=subject_name, code=f"SEM{semester}-{subject_name[:4].upper()}")
            db.add(course)
            db.commit()
            db.refresh(course)
            
        # Register Document
        doc = doc_svc.get_or_create_document(
            document_hash=sha256_hash,
            source="TheHelpers",
            title=title,
            semester=semester,
            subject=subject_name,
            resource_type=resource_type
        )
            
        print(f"  [>] Extracting text via PDFParser...")
        try:
            with open(local_path, "rb") as f:
                pages_data = PDFParser.extract_text_with_pages(f)
            
            # Route to correct extraction logic based on resource_type
            is_exam = resource_type in ['examination papers / PYQs', 'CT papers']
            
            if is_exam:
                print(f"  [>] Running Exam Question Extractor...")
                result = QuestionExtractor.extract(pages_data)
                
                if not result.successful:
                    print(f"  [!] Extraction failed: {result.error_message}")
                    cursor.execute("UPDATE downloads SET processed = 1 WHERE id = ?", (row_id,))
                    conn.commit()
                    continue
                    
                doc_svc.import_exam_extraction(
                    document_id=doc.id,
                    course_id=course.id, 
                    year=2023, 
                    term="Fall", 
                    extraction_data=result.model_dump()
                )
                print(f"  [+] Ingested {len(result.sections)} sections as EXAM")
            else:
                print(f"  [>] Running Study Material Knowledge Extractor...")
                result = KnowledgeExtractor.extract(pages_data)
                
                if not result.successful:
                    print(f"  [!] Extraction failed: {result.error_message}")
                    cursor.execute("UPDATE downloads SET processed = 1 WHERE id = ?", (row_id,))
                    conn.commit()
                    continue
                    
                doc_svc.import_knowledge_extraction(
                    document_id=doc.id,
                    extraction_data=result.model_dump()
                )
                print(f"  [+] Ingested {len(result.concepts)} concepts as KNOWLEDGE")
            
            # Mark processed
            cursor.execute("UPDATE downloads SET processed = 1 WHERE id = ?", (row_id,))
            conn.commit()
            
        except Exception as e:
            print(f"  [!] ERROR processing {local_path}: {e}")
            cursor.execute("UPDATE downloads SET processed = 2 WHERE id = ?", (row_id,))
            conn.commit()
            
    print("\nFeeder finished batch.")
    db.close()
    conn.close()

import time
if __name__ == "__main__":
    while True:
        process_downloads()
        time.sleep(10)
