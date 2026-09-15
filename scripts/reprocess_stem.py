import os
import sys
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('ENVIRONMENT', 'production')

from backend.core.database import SessionLocal
from backend.models.core import Document, Exam, Section, Question, QuestionConcept, QuestionFamilyMembership, question_topic

def wipe_and_reset():
    db = SessionLocal()
    
    print("[1] Identifying documents to reprocess...")
    docs_to_reset = db.query(Document).all()
    print(f"Found {len(docs_to_reset)} documents.")

    doc_ids = [d.id for d in docs_to_reset]

    print("[2] Wiping downstream corrupted mappings...")
    # The models use cascading deletes on relationships usually, but we'll do it manually to be safe
    db.execute(question_topic.delete())
    db.query(QuestionFamilyMembership).delete()
    db.query(QuestionConcept).delete()

    print("[3] Wiping corrupted questions and exams...")
    db.query(Question).delete()
    db.query(Section).delete()
    db.query(Exam).delete()
    db.commit()

    print("[4] Resetting scraper cache for re-ingestion...")
    db_path = "data/.download_cache/downloads.db"
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Reset everything to 0 to be processed by ingest.py
        cursor.execute("UPDATE downloads SET processed = 0")
        conn.commit()
        conn.close()
        print("Reset scraper cache.")

    print("Cleanup complete. Ready to run `python scripts/ingest.py`.")
    db.close()

if __name__ == "__main__":
    wipe_and_reset()
