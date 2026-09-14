from fastapi import APIRouter
from app.api.endpoints import papers, courses, exams, analysis, concepts, search

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
