from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings, Environment
from backend.api.router import api_router
from backend.core.database import engine, Base

# Create all tables in the database ONLY if not in production
if settings.ENVIRONMENT != Environment.PRODUCTION:
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    docs_url="/docs" if settings.ENVIRONMENT != Environment.PRODUCTION else None, # Disable swagger in prod if wanted, but standard is to keep it or just disable debug
    redoc_url="/redoc" if settings.ENVIRONMENT != Environment.PRODUCTION else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    """Lightweight health endpoint."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}

app.include_router(api_router, prefix="/api")
