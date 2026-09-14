import os
import sqlite3
import json
import sys

from sqlalchemy.exc import OperationalError
from app.core.database import SessionLocal, Base, engine
from app.models.core import Course, Topic, Exam, Section, Question
from app.services.extraction.pdf_parser import PDFParser
from app.services.extraction.question_extractor import QuestionExtractor
from app.services.exam import ExamService

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
        print("\n[!] CRITICAL: Could not connect to the PostgreSQL database.")
        print("Please ensure your database is running via: docker-compose up -d")
        print("Exiting feeder pipeline.\n")
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
    cursor.execute("SELECT id, local_path, source_metadata FROM downloads WHERE processed = 0 AND local_path LIKE '%.pdf'")
    unprocessed = cursor.fetchall()
    
    if not unprocessed:
        print("No new unprocessed PDFs found in the scraper cache.")
        return
        
    print(f"Found {len(unprocessed)} unprocessed PDFs. Feeding into ExamScope Engine...")
    
    # Initialize our application services
    db = SessionLocal()
    svc = ExamService(db)
    
    for row_id, local_path, source_metadata in unprocessed:
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
            pass
            
        subject_name = meta.get('subject', 'Unknown Subject')
        semester = meta.get('semester', '1')
        
        # 1. Get or Create Course based on the scraper's Subject
        course = db.query(Course).filter_by(name=subject_name).first()
        if not course:
            course = Course(name=subject_name, code=f"SEM{semester}-{subject_name[:4].upper()}")
            db.add(course)
            db.commit()
            db.refresh(course)
            
        # 2. Extract Data from PDF
        print(f"  [>] Extracting text via PDFParser...")
        try:
            with open(local_path, "rb") as f:
                pages_data = PDFParser.extract_text_with_pages(f)
            
            print(f"  [>] Running ML Question Extraction (Phase 2)...")
            result = QuestionExtractor.extract(pages_data)
            
            if not result.successful:
                print(f"  [!] Extraction failed: {result.error_message}")
                # Mark processed to avoid infinite loops on bad PDFs
                cursor.execute("UPDATE downloads SET processed = 1 WHERE id = ?", (row_id,))
                conn.commit()
                continue
                
            # 3. Import to Database (Phase 3 & 4)
            print(f"  [>] Importing {len(result.sections)} sections into Database...")
            # We don't have year in metadata, so default to 2023 Fall
            exam = svc.import_extraction(
                course_id=course.id, 
                year=2023, 
                term="Fall", 
                extraction_data=result.model_dump()
            )
            print(f"  [+] Successfully ingested Exam ID: {exam.id} for Course: {course.name}")
            
            # Mark processed
            cursor.execute("UPDATE downloads SET processed = 1 WHERE id = ?", (row_id,))
            conn.commit()
            
        except Exception as e:
            print(f"  [!] CRITICAL ERROR processing {local_path}: {e}")
            
    print("\nFeeder finished batch.")
    db.close()
    conn.close()

if __name__ == "__main__":
    process_downloads()
