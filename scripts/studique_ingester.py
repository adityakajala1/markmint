import os
import sys
import time
import requests
import json
import hashlib
import logging
from typing import List, Dict, Any

sys.path.append('.')
from backend.core.database import SessionLocal
from backend.models.core import Document, Course
from backend.services.document import DocumentService
from backend.services.extraction.pdf_parser import PDFParser
from backend.services.extraction.knowledge_extractor import KnowledgeExtractor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = "data/studique_production"
BATCH_SIZE = 5

def download_file_with_retry(file_key: str, dest_path: str, max_retries: int = 3) -> bool:
    if os.path.exists(dest_path):
        return True
    
    url = f"https://drive.google.com/uc?export=download&id={file_key}"
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Downloading {file_key} -> {dest_path} (Attempt {attempt+1})")
            r = requests.get(url, stream=True, timeout=30)
            if r.status_code == 200:
                with open(dest_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            else:
                logger.warning(f"Failed to download. Status code: {r.status_code}")
        except requests.RequestException as e:
            logger.error(f"Download exception: {e}")
            
        time.sleep(2 ** attempt)
        
    return False

def get_file_hash(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def process_resource(item: Dict[str, Any], subject_name: str, resource_type: str, subject_dir: str, db, doc_svc: DocumentService) -> bool:
    name = item.get('name')
    file_key = item.get('fileKey')
    if not name or not file_key:
        return False
        
    original_url = f"https://studique.in/api/resource/download?fileKey={file_key}"
    
    existing = db.query(Document).filter_by(original_url=original_url).first()
    if existing:
        logger.info(f"Skipping '{name}' - already exists (ID: {existing.id})")
        return True
        
    dest_path = os.path.join(subject_dir, f"{name.replace('/', '_')}.pdf")
    if not download_file_with_retry(file_key, dest_path):
        logger.error(f"Failed to download '{name}' after retries.")
        return False
        
    file_hash = get_file_hash(dest_path)
    
    doc = doc_svc.get_or_create_document(
        document_hash=file_hash,
        source="studique",
        original_url=original_url,
        title=name,
        subject=subject_name,
        resource_type=resource_type
    )
    logger.info(f"Created Document ID: {doc.id}")
    
    if resource_type == "lecture notes":
        try:
            with open(dest_path, "rb") as f:
                pages_data = PDFParser.extract_text_with_pages(f)
                
            if pages_data:
                result = KnowledgeExtractor.extract(pages_data)
                if result.successful:
                    doc_svc.import_knowledge_extraction(
                        document_id=doc.id,
                        extraction_data=result.model_dump()
                    )
                    logger.info(f"Extracted {len(result.concepts)} concepts for Document ID: {doc.id}")
                else:
                    logger.error(f"Extraction failed: {result.error_message}")
        except Exception as e:
            logger.error(f"Processing failed for Document ID {doc.id}: {e}")
            
    # Optional rate limiting between downloads
    time.sleep(1)
    return True

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    logger.info("Fetching Studique resource list...")
    try:
        r = requests.get("https://studique.in/api/resource/list", timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        logger.error(f"Failed to fetch resource list: {e}")
        return
        
    db = SessionLocal()
    doc_svc = DocumentService(db)
    
    processed_count = 0
    
    try:
        for subject_data in data.get('subjects', []):
            if processed_count >= BATCH_SIZE:
                logger.info(f"Reached batch limit of {BATCH_SIZE} resources. Exiting.")
                break
                
            subject_name = subject_data.get('name')
            if not subject_name or subject_name not in ["Calculus and Linear Algebra", "Chemistry"]:
                continue
                
            course = db.query(Course).filter(Course.name.ilike(subject_name)).first()
            if not course:
                course = Course(name=subject_name, code=subject_name[:5].upper())
                db.add(course)
                db.commit()
                db.refresh(course)
                
            subject_dir = os.path.join(OUTPUT_DIR, subject_name.replace(" ", "_").replace("/", "_"))
            os.makedirs(subject_dir, exist_ok=True)
            
            logger.info(f"Processing Subject: {subject_name}")
            
            # Process PPTs
            for ppt in subject_data.get('ppts', []):
                if processed_count >= BATCH_SIZE:
                    break
                if process_resource(ppt, subject_name, "lecture notes", subject_dir, db, doc_svc):
                    processed_count += 1
            
            # Process PYQs
            for pyq in subject_data.get('pyqs', []):
                if processed_count >= BATCH_SIZE:
                    break
                if process_resource(pyq, subject_name, "examination papers / PYQs", subject_dir, db, doc_svc):
                    processed_count += 1

    finally:
        db.close()
        logger.info(f"Ingestion job complete. Processed {processed_count} resources.")

if __name__ == "__main__":
    main()
