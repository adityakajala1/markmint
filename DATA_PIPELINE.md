# ExamScope Data Pipeline

The ExamScope architecture strictly decouples data discovery and ingestion from the public web application. This ensures that the production FastAPI application remains fast and secure, merely serving statically extracted and validated relationships from the PostgreSQL database, rather than dynamically parsing PDFs or interacting with scraper endpoints.

## Architecture

```mermaid
flowchart TD
    A[TheHelper / Source] -->|Scrape| B[scripts/scrape.py]
    B -->|Downloads| C[data/.download_cache/]
    C -->|Ingest & Extract| D[scripts/ingest.py]
    D -->|Write| E[(PostgreSQL Database)]
    E -->|Read| F[FastAPI Web Server]
    F -->|Serve| G[Next.js Frontend]
```

## CLI Commands

The pipeline requires explicit execution by the administrator in isolated worker environments.

### 1. Scrape

The scraper discovers and downloads raw PDFs to the local cache. It prevents duplicates and handles network failures gracefully.

```bash
python scripts/scrape.py
```

### 2. Ingest

The ingestion worker parses local PDFs, extracts structural evidence (questions, concepts, sections), and persists them idempotently into the database schema. Running it multiple times on the same cache produces the exact same database state.

```bash
python scripts/ingest.py
```

### 3. Analyze

The analysis engine precomputes DNA structures, calculates temporal distributions, identifies families, and aggregates marks patterns.

```bash
python scripts/analyze.py
```

### 4. Backtest

The backtester validates predictive accuracy by holding out historical years (e.g., hiding 2023 data) and testing whether the DNA correctly projected the 2023 topic distribution.

```bash
python scripts/backtest.py
```

### 5. Automated Sync (Cron/Scheduler)

The `sync_pipeline.py` script orchestrates the full lifecycle for periodic automated updates. It bounds execution scope (e.g., max 50 downloads, 100 ingestions) to ensure safety and avoid infinite retries on failed resources. It also maintains idempotency, preventing duplicates.

```bash
python scripts/sync_pipeline.py
```

It records detailed logs including `start_time`, `end_time`, `discovered`, `downloaded`, `processed`, `failures`, and `db_changes` to `data/logs/sync_history.jsonl`.

## Production Guidelines

- **NEVER** run scraping logic in a web request handler.
- **NEVER** download PDFs in the public API.
- **NEVER** run LLM extraction (Knowledge/Question) synchronously during a user API call.
- The pipeline commands should be run as cron jobs or manual operations in a secured backend environment.
