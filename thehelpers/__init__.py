"""
The Helper - Academic Resource Scraper and Ingestor

Purpose:
    Scrape and ingest academic resources from The Helper platform.
    Integrates with ExamScope's 7-phase analysis pipeline for comprehensive
    resource classification and processing.

Features:
    - Idempotent, resumable ingestion with full state tracking
    - Intelligent resource classification and validation
    - Parallel downloading with retry logic
    - Deduplication and conflict resolution
    - Structured logging for audit trails

Usage:
    python -m thehelpers.ingest [command] [options]

    Commands:
        discover    - Crawl The Helper and discover resources
        classify    - Classify discovered resources
        download    - Download resources
        ingest      - Run full ingestion pipeline
        resume      - Resume interrupted ingestion

Integration:
    Part of the ExamScope platform's resource acquisition layer.
    Output feeds into 7-phase analysis pipeline for classification,
    processing, and storage.
"""

__version__ = "1.0.0"
__author__ = "ExamScope Team"

# Model exports
from .models import (
    DiscoveredResource,
    ClassifiedResource,
    DownloadedResource,
    IngestionRecord,
    ResourceType,
    ExamType,
    ProcessingStatus,
)

# Core component exports
from .classifier import ResourceClassifier
from .parser import parse_semester_page, parse_subject_page, normalize_url
from .crawler import TheHelperCrawler
from .downloader import ResourceDownloader
from .storage import IngestionRepository

# Ingest pipeline exports
from .ingest import main as ingest_main, IngestionReport

__all__ = [
    # Metadata
    "__version__",
    "__author__",
    # Models
    "DiscoveredResource",
    "ClassifiedResource",
    "DownloadedResource",
    "IngestionRecord",
    "ResourceType",
    "ExamType",
    "ProcessingStatus",
    # Core components
    "ResourceClassifier",
    "parse_semester_page",
    "parse_subject_page",
    "normalize_url",
    "TheHelperCrawler",
    "ResourceDownloader",
    "IngestionRepository",
    # Ingest pipeline
    "ingest_main",
    "IngestionReport",
]
