# Architecture

## Component Overview
ExamScope Backend follows a Service-Repository pattern over FastAPI and SQLAlchemy.

1. **Ingestion & Scraping**: `thehelpers/` handles scraping of publicly available historical papers from app.services.scraper.tech and deduplicates/caches them as raw documents.
2. **Extraction Engine**: Deterministic PDF parsers map raw documents into structured questions.
3. **Classification Engine**: Leverages `SentenceTransformers` and Bloom's Taxonomy rules to map questions to known Syllabus Topics, Question Types, and Cognitive Levels.
4. **Similarity Engine**: Uses embedding cosine-similarity matrices with strict false-positive heuristic guardrails to detect semantic question repetition (exact, conceptual, structural).
5. **DNA Analyzer**: Aggregates datasets to compute topic weights, distributions, and strict evidence-backed historical statistics.
6. **Prediction Engine**: Employs an exponential decay recency-weighting algorithm to detect trends and output high-confidence, evidence-backed predictions.
7. **REST API**: Exposes these intelligence layers to the frontend without leaking database ORM implementations.

## Infrastructure
- **Database**: PostgreSQL 15.
- **Framework**: FastAPI (Python 3.14+).
- **ML Layer**: Local models via `sentence-transformers`, `numpy`.
