import os
import sqlite3
import json
import sys
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.exc import OperationalError
from backend.core.database import SessionLocal, Base, engine
from backend.models.core import Course
from backend.services.extraction.pdf_parser import PDFParser
from backend.services.extraction.question_extractor import QuestionExtractor
from backend.services.extraction.knowledge_extractor import KnowledgeExtractor
from backend.services.extraction.vision_extractor import VisionExtractor
from backend.services.document import DocumentService


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


def process_downloads(max_files: int = 50):
    print(f"Starting Ingestion Feeder (Max files: {max_files})...")
    
    stats = {
        "discovered": 0,
        "processed": 0,
        "failed": 0,
        "skipped": 0
    }
    
    db_path = "data/.download_cache/downloads.db"
    
    if not os.path.exists(db_path):
        print(f"Cache DB not found at {db_path}. Is the scraper running?")
        return stats

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
    cursor.execute("SELECT id, local_path, source_metadata, sha256 FROM downloads WHERE processed = 0 AND local_path LIKE '%.pdf' LIMIT ?", (max_files,))
    unprocessed = cursor.fetchall()
    
    stats["discovered"] = len(unprocessed)
    
    if not unprocessed:
        print("No new unprocessed PDFs found in the scraper cache.")
        return stats
        
    print(f"Found {len(unprocessed)} unprocessed PDFs. Feeding into ExamScope Engine...")
    
    db = SessionLocal()
    doc_svc = DocumentService(db)
    
    for row_id, local_path, source_metadata, sha256_hash in unprocessed:
        print(f"\nProcessing [{row_id}]: {local_path}")
        
        if not os.path.exists(local_path):
            print(f"File missing: {local_path}")
            stats["skipped"] += 1
            cursor.execute("UPDATE downloads SET processed = 2 WHERE id = ?", (row_id,))
            conn.commit()
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
        
        # Try extracting year from title
        year = None
        year_match = re.search(r'(20\d{2})', title)
        if year_match:
            year = int(year_match.group(1))
        
        print(f"  [>] Type: {resource_type}, Year: {year}")
        
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
            
        try:
            # Route to correct extraction logic based on resource_type
            is_exam = resource_type in ['examination papers / PYQs', 'CT papers']
            is_syllabus = resource_type == 'syllabi'
            
            if is_exam:
                # Attempt Vision Extraction first
                print(f"  [>] Running Exam Question Extractor (Vision Mode)...")
                result = VisionExtractor.extract_pdf(local_path)
                
                # Fallback to Legacy OCR if API Key missing or error
                if not result.successful:
                    print(f"  [!] Vision Extraction failed/skipped: {result.error_message}. Falling back to OCR...")
                    with open(local_path, "rb") as f:
                        pages_data = PDFParser.extract_text_with_pages(f)
                    if pages_data:
                        result = QuestionExtractor.extract(pages_data)
                
                if not result.successful:
                    print(f"  [!] Extraction failed completely: {result.error_message}")
                    stats["failed"] += 1
                    cursor.execute("UPDATE downloads SET processed = 2 WHERE id = ?", (row_id,))
                    conn.commit()
                    continue
                    
                doc_svc.import_exam_extraction(
                    document_id=doc.id,
                    course_id=course.id, 
                    year=year,  # Passes None if unknown, preserving data integrity!
                    term="Fall", 
                    extraction_data=result.model_dump()
                )
                print(f"  [+] Ingested {len(result.sections)} sections as EXAM")
                stats["processed"] += 1
            elif not is_syllabus:
                print(f"  [>] Running Study Material Knowledge Extractor (OCR Mode)...")
                with open(local_path, "rb") as f:
                    pages_data = PDFParser.extract_text_with_pages(f)
                
                if not pages_data:
                    print("  [!] Document is empty or unreadable.")
                    stats["failed"] += 1
                    cursor.execute("UPDATE downloads SET processed = 2 WHERE id = ?", (row_id,))
                    conn.commit()
                    continue

                result = KnowledgeExtractor.extract(pages_data)
                
                if not result.successful:
                    print(f"  [!] Extraction failed: {result.error_message}")
                    stats["failed"] += 1
                    cursor.execute("UPDATE downloads SET processed = 2 WHERE id = ?", (row_id,))
                    conn.commit()
                    continue
                    
                doc_svc.import_knowledge_extraction(
                    document_id=doc.id,
                    extraction_data=result.model_dump()
                )
                print(f"  [+] Ingested {len(result.concepts)} concepts as KNOWLEDGE")
                stats["processed"] += 1
            else:
                stats["processed"] += 1
            
            # Mark processed
            cursor.execute("UPDATE downloads SET processed = 1 WHERE id = ?", (row_id,))
            conn.commit()
            
        except Exception as e:
            print(f"  [!] ERROR processing {local_path}: {e}")
            stats["failed"] += 1
            cursor.execute("UPDATE downloads SET processed = 2 WHERE id = ?", (row_id,))
            conn.commit()
            db.rollback()
            
    print("\nFeeder finished batch.")
    db.close()
    conn.close()
    return stats

if __name__ == "__main__":
    process_downloads(max_files=5)
