# ExamScope System Architecture

## Component Overview

### 1. Ingestion Layer
- **Local Scraper Cache (`downloads.db`)**: Logs file system states.
- **Feeder Pipeline**: Loads PDFs, categorizes by heuristic, and orchestrates the extraction services.

### 2. Extraction & NLP Layer
- **PDFParser**: Converts PDF binary to layout-aware text.
- **KnowledgeExtractor / ExamExtractor**: Regex/heuristic parsing bridging raw text to domain models.
- **ConceptNormalizer**: Maps extracted topics to a canonical, cross-subject intelligence graph.

### 3. Core Database (PostgreSQL / SQLite)
- Isolated domains: `Exam`, `Question`, `StudyEvidence`, `Syllabus`, `Concept`.
- Uses SQLAlchemy ORM.

### 4. Intelligence Engines
- **Concept Intelligence Engine**: Aggregates separated evidence pools.
- **DNA Analyzer**: Converts historical exams into behavioral vectors (Exam DNA).
- **Exam Evolution**: Detects structural trends (RISING, DECLINING) and formatting change-points over time.
- **Backtest Engine**: Proves predictive accuracy against historical target years.
- **WHY (Evidence) Engine**: Translates DNA mathematics into human-readable deterministic provenance trails.

### 5. API Layer
- **FastAPI**: Serves the intelligence engines via `/api/analysis`, `/api/concepts`, and `/api/search`.
- **DiscoverySearchEngine**: Hybrid semantic router that applies metadata filters and routes broad requests across the entire relational graph.
- Includes a 5-minute in-memory TTL Cache to protect the DB from repeated heavy joins on dashboard load.
