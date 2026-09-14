from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import time

from backend.core.database import get_db
from backend.schemas import ConceptEvidenceReport, StudyPriorityProfile
from backend.services.concept.engine import ConceptIntelligenceEngine
from backend.services.concept.priority import ConceptPriorityService

router = APIRouter()

# Concept cache to prevent hammering the DB for complex joins
_CONCEPT_CACHE = {}
CACHE_TTL = 300

@router.get("/{concept_id}/evidence", response_model=ConceptEvidenceReport)
def get_concept_evidence(concept_id: int, db: Session = Depends(get_db)):
    """
    Returns strictly segregated evidence (Exam vs Study vs Syllabus).
    """
    cache_key = (concept_id, "evidence")
    if cache_key in _CONCEPT_CACHE:
        ts, data = _CONCEPT_CACHE[cache_key]
        if time.time() - ts < CACHE_TTL:
            return data

    engine = ConceptIntelligenceEngine(db)
    report = engine.get_concept_evidence(concept_id)
    if not report:
        raise HTTPException(status_code=404, detail="Concept not found")
        
    _CONCEPT_CACHE[cache_key] = (time.time(), report)
    return report

@router.get("/{concept_id}/priority", response_model=StudyPriorityProfile)
def get_concept_priority(concept_id: int, db: Session = Depends(get_db)):
    """
    Returns the transparent study priority calculation for a concept.
    """
    cache_key = (concept_id, "priority")
    if cache_key in _CONCEPT_CACHE:
        ts, data = _CONCEPT_CACHE[cache_key]
        if time.time() - ts < CACHE_TTL:
            return data

    engine = ConceptIntelligenceEngine(db)
    report = engine.get_concept_evidence(concept_id)
    if not report:
        raise HTTPException(status_code=404, detail="Concept not found")
        
    # In a real app we'd fetch total historical papers for this specific subject/course.
    # Stubbing with 10 for demonstration as priority calculates ratio.
    profile = ConceptPriorityService.calculate_priority(report, total_historical_papers=10)
    
    _CONCEPT_CACHE[cache_key] = (time.time(), profile)
    return profile
