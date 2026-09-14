# ExamScope Data Pipeline

## Overview
The ExamScope data pipeline is responsible for ingesting raw academic documents, categorizing them, extracting structured knowledge, and feeding the intelligence engine.

## Stages

### 1. Source & Ingestion
- **Scraper**: A separate process that pulls academic materials (PYQs, CT papers, Syllabi, Notes) and logs them in a local SQLite cache (`downloads.db`).
- **Feeder (`feed_pipeline.py`)**: Reads unprocessed PDFs. Categorizes them based on filename heuristics into Exam Evidence (PYQs/CTs) or Study Evidence (Notes/Materials).

### 2. Normalization & Extraction
- **Exams**: Processed by `ExamQuestionExtractor`. Identifies sections, question text, marks, and base topics.
- **Study Material**: Processed by `KnowledgeExtractor`. Extracts definitions, formulas, and context.

### 3. Classification (Concept Engine)
- The `ConceptNormalizer` maps extracted topics to a canonical knowledge graph.
- Prevents cross-subject ambiguity.
- Uses an `UNRESOLVED` fallback to prevent false merges when confidence is low.

### 4. Storage
- Data is strictly segregated into `Exam`, `StudyEvidence`, and `Syllabus` tables.
- Study material frequency strictly cannot alter exam frequency metrics.

## Known Idempotency Risks
- The current pipeline relies on the local scraper cache. Restarting the pipeline without UPSERT locks in the main database will result in duplicated exams.
