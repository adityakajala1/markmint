from fastapi import APIRouter
from backend.api.endpoints import papers, courses, exams

api_router = APIRouter()

@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

api_router.include_router(papers.router, tags=["papers"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(exams.router, prefix="/exams", tags=["exams"])
