import os
import sys
import json
import time
import asyncio
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('ENVIRONMENT', 'production')

from scripts.scrape import run_scrape
from scripts.ingest import process_downloads
from scripts.analyze import run_analysis
from backend.core.database import SessionLocal
from backend.models.core import Document, Exam, Question, Concept

LOG_FILE = "data/logs/sync_history.jsonl"


def get_db_counts():
    db = SessionLocal()
    try:
        return {
            "documents": db.query(Document).count(),
            "exams": db.query(Exam).count(),
            "questions": db.query(Question).count(),
            "concepts": db.query(Concept).count()
        }
    finally:
        db.close()


async def main():
    print("=" * 70)
    print("  EXAMSCOPE PERIODIC SYNC PIPELINE")
    print(f"  Start time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    start_time = datetime.now(timezone.utc)
    counts_before = get_db_counts()
    
    # Run scraping (Max 50 items per sync to prevent unbounded duration)
    print("\n--- PHASE 1: SCRAPE ---")
    try:
        scrape_stats = await run_scrape(max_downloads=50)
    except Exception as e:
        print(f"[!] Scrape phase encountered an error: {e}")
        scrape_stats = {"discovered": 0, "downloaded": 0, "skipped_no_id": 0, "errors": 1}

    # Run ingestion (Max 100 files per sync to ensure we process backlog efficiently but safely)
    print("\n--- PHASE 2: INGEST ---")
    try:
        ingest_stats = process_downloads(max_files=100)
    except Exception as e:
        print(f"[!] Ingestion phase encountered an error: {e}")
        ingest_stats = {"discovered": 0, "processed": 0, "failed": 1, "skipped": 0}

    # Update analytical caches if anything was successfully ingested
    print("\n--- PHASE 3: UPDATE ANALYSIS ---")
    try:
        if ingest_stats.get("processed", 0) > 0:
            run_analysis()
            analysis_updated = True
        else:
            print("No new documents processed. Skipping full analysis recompute.")
            analysis_updated = False
    except Exception as e:
        print(f"[!] Analysis phase encountered an error: {e}")
        analysis_updated = False

    end_time = datetime.now(timezone.utc)
    counts_after = get_db_counts()

    # Calculate delta
    db_changes = {
        "documents": counts_after["documents"] - counts_before["documents"],
        "exams": counts_after["exams"] - counts_before["exams"],
        "questions": counts_after["questions"] - counts_before["questions"],
        "concepts": counts_after["concepts"] - counts_before["concepts"]
    }

    log_entry = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": (end_time - start_time).total_seconds(),
        "scrape": scrape_stats,
        "ingest": ingest_stats,
        "analysis_updated": analysis_updated,
        "db_changes": db_changes
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print("\n" + "=" * 70)
    print("  SYNC JOB COMPLETE")
    print("=" * 70)
    print(f"Duration:   {log_entry['duration_seconds']:.2f} seconds")
    print(f"Scraped:    {scrape_stats.get('downloaded', 0)} new resources")
    print(f"Ingested:   {ingest_stats.get('processed', 0)} documents")
    print(f"DB Changes: +{db_changes['documents']} docs, +{db_changes['exams']} exams, +{db_changes['questions']} qs")
    print(f"Log saved:  {LOG_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
