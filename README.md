# Exam Reverse Engineer (ExamScope)

Evidence-based examination analysis system.

## Local Setup

1. **Prerequisites**: Python 3.10+, Docker, Docker Compose
2. **Environment Setup**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   cp .env.example .env
   ```
3. **Database Setup**:
   ```bash
   docker-compose up -d
   ```
4. **Run Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Run Tests**:
   ```bash
   pytest
   ```
