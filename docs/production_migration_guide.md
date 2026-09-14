# Production PostgreSQL Migration Guide

This guide details the exact steps required to transfer the validated ExamScope corpus from the local structured SQLite database (`production_corpus.db`) to the live production PostgreSQL environment.

## 1. Prerequisites

Ensure your PostgreSQL instance is running and accessible. If you have just installed PostgreSQL, create the required database and user:

```bash
# Connect to PostgreSQL using your installation credentials
psql -U postgres

# Execute the following SQL to provision the environment:
CREATE USER exam_user WITH PASSWORD 'exam_password';
CREATE DATABASE exam_db;
GRANT ALL PRIVILEGES ON DATABASE exam_db TO exam_user;
ALTER DATABASE exam_db OWNER TO exam_user;
```

## 2. Update Configuration

Ensure the `.env` file points exactly to your PostgreSQL database. For example:
```env
ENVIRONMENT=production
DATABASE_URL=postgresql+psycopg2://exam_user:exam_password@localhost:5432/exam_db
```

## 3. Apply the Schema (Alembic)

The target PostgreSQL database must have the precise schema defined, including all tables, constraints, and indexes. We rely on Alembic to guarantee this.

Run the following command from the repository root:
```powershell
.\.venv\Scripts\Activate.ps1
alembic upgrade head
```
*This will establish the schema strictly based on your SQLAlchemy models without migrating any data yet.*

## 4. Run the Structural Data Transfer Script

Since SQLite and PostgreSQL have different syntaxes and data types (e.g., JSON vs JSONB), a raw dump/restore is insufficient. We utilize an explicit Python script that traverses the SQLAlchemy Metadata topology and bulk inserts records, preserving all Primary Keys and Foreign Key relationships perfectly.

I have generated `migrate_sqlite_to_pg.py` specifically for this task.

Run the script, passing the source SQLite path and the target PostgreSQL path:

```powershell
python <scratch_directory>\migrate_sqlite_to_pg.py "sqlite:///./production_corpus.db" "postgresql+psycopg2://exam_user:exam_password@localhost:5432/exam_db"
```

### What this script does:
1. Temporarily suppresses foreign-key constraints on the PostgreSQL side (`SET session_replication_role = 'replica'`) to prevent constraint violations during the batch load.
2. Iterates over `Base.metadata.sorted_tables`, reading from the SQLite file.
3. Bulk inserts dictionaries mapped from the rows into the Postgres tables.
4. Restores foreign-key enforcement (`SET session_replication_role = 'origin'`).

## 5. Verify the Production Database

Finally, confirm the counts match exactly between SQLite and PostgreSQL:
```bash
python -c "
from backend.core.database import SessionLocal
from backend.models.core import Exam, Question
db = SessionLocal()
print('Exams:', db.query(Exam).count())
print('Questions:', db.query(Question).count())
"
```
