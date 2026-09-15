from fastapi import APIRouter
from backend.api.endpoints import (
    analysis,
    concepts,
    courses,
    exams,
    papers,
    predictions,
    practice,
    search,
    study_connection,
)

api_router = APIRouter()

@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

api_router.include_router(papers.router, tags=["papers"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(exams.router, prefix="/exams", tags=["exams"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(concepts.router, prefix="/concepts", tags=["concepts"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(predictions.router, tags=["predictions"])
api_router.include_router(study_connection.router, tags=["study"])
api_router.include_router(practice.router, tags=["practice"])

from backend.api.router_study import router as study_router
api_router.include_router(study_router)

