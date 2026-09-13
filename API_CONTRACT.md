# API Usage Guide

This document provides frontend developers with the information needed to integrate with the Exam Reverse Engineer Backend.

## Base URL
Local Development: `http://localhost:8000/api`

## Authentication
*(Phase 7 does not currently implement auth locks, endpoints are open for local dev).*

---

## 1. Courses

### Create a Course
`POST /courses/`
```json
// Request Body
{
  "name": "Introduction to Computer Science",
  "code": "CS101"
}

// Response (200 OK)
{
  "id": 1,
  "name": "Introduction to Computer Science",
  "code": "CS101"
}
```

### Get a Course
`GET /courses/{id}`
Returns the course object.

---

## 2. Exams

### Create an Exam
`POST /exams/`
```json
// Request Body
{
  "course_id": 1,
  "year": 2023,
  "term": "Fall"
}
```

### Get Exam Questions (Paginated & Filtered)
`GET /exams/{id}/questions?page=1&size=50&topic=Graphs&question_type=explanation`

**Query Parameters:**
- `page` (int): Defaults to 1.
- `size` (int): Items per page, max 100.
- `topic` (str, optional): Filter by topic name.
- `question_type` (str, optional): Filter by type (e.g. "explanation", "implementation").

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "section_id": 1,
      "question_number": "1a",
      "original_text": "Explain BFS.",
      "marks": 5.0,
      "question_type": "explanation",
      "cognitive_level": "understand",
      "difficulty": 0.5
    }
  ],
  "total": 1,
  "page": 1,
  "size": 50,
  "pages": 1
}
```

---

## 3. Analytics & Predictions

### Get Exam DNA
`GET /exams/{id}/dna`
Returns the deterministic historical distributions and repetition rates.

**Response Snippet:**
```json
{
  "total_exams_analyzed": 5,
  "topic_distribution": [
    {
      "key": "Graphs",
      "count": 12,
      "percentage_of_total": 0.15,
      "marks_weighting": 0.22
    }
  ],
  "average_difficulty": {
    "value": 0.65,
    "sample_size": 120,
    "denominator": 150,
    "supporting_question_ids": ["q1", "q2"]
  }
}
```

### Get Exam Predictions
`GET /exams/{id}/predictions`
Returns evidence-backed predictive insights. If data is insufficient, `insufficient_data` will be `true`.

**Response:**
```json
{
  "predictions": [
    {
      "characteristic": "High-Weight Topic",
      "predicted_insight": "'Trees' has consistently high historical importance for marks.",
      "confidence": "High",
      "supporting_evidence": "Appeared in 3 of 3 papers and accounted for approximately 93% of total historical marks.",
      "sample_size": 3,
      "historical_frequency": 1.0,
      "limitations": "Sample size of 3 papers limits long-term certainty."
    }
  ],
  "total_papers_analyzed": 3,
  "insufficient_data": false
}
```

---

## 4. Document Ingestion

### Upload Paper (PDF Extraction)
`POST /papers/upload`
Uploads a raw PDF and extracts structured questions before they are committed to the database.

**Request:** `multipart/form-data` containing a `file` field with the PDF.

**Response:**
Returns a `DocumentExtractionResult` containing sections, extracted questions, marks, and extraction confidence.
