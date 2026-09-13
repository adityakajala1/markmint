# ExamScope TODO List

## Completed (Backend Intelligence Phase 1-7)
- [x] Base FastAPI & PostgreSQL setup
- [x] Document Ingestion Pipeline
- [x] Semantic Classification Engine
- [x] Similarity & Question-Family Clustering
- [x] Exam DNA Engine
- [x] Evidence-backed Prediction Engine
- [x] REST API for Frontend Developer
- [x] Claude integration: `thehelpers` crawler and downloader

## Next Steps
- [ ] Connect `thehelpers` downloader outputs to the `POST /api/papers/upload` ingestion pipeline.
- [ ] Expand Database schemas to separate "Student Uploaded Context" (Assignments, Syllabus, Notes) from "Historical Exams" as mandated by project rules.
- [ ] Expand prediction and DNA engines to support isolated queries by `exam_type` (e.g. Midterm vs End-semester).
- [ ] Add explicit syllabus version tracking.
