from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import SearchQuery, SearchResult
from app.services.search.discovery import DiscoverySearchEngine

router = APIRouter()

@router.post("/", response_model=list[SearchResult])
def search_intelligence(query: SearchQuery, db: Session = Depends(get_db)):
    """
    Executes a hybrid semantic and metadata search across the entire ExamScope graph.
    Automatically identifies intent (e.g., trend requests vs static concept queries).
    """
    engine = DiscoverySearchEngine(db)
    return engine.search(query)
