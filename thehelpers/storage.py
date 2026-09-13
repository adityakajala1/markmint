"""Storage layer for The Helper scraper - integrates with ExamScope."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime, Index, ForeignKey
)
from sqlalchemy.orm import Session, relationship

from app.core.database import Base


# ------------------------------------------------------------------
# Enums
# ------------------------------------------------------------------
class ProcessingStatus(str, Enum):
    DISCOVERED = "discovered"
    DOWNLOADED = "downloaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ------------------------------------------------------------------
# Data classes (used by IngestionRepository)
# ------------------------------------------------------------------
class DiscoveredResource:
    def __init__(
        self,
        source_url: str,
        title: Optional[str] = None,
        file_type: Optional[str] = None,
        semester: Optional[str] = None,
        subject: Optional[str] = None,
        discovered_at: Optional[datetime] = None,
    ):
        self.source_url = source_url
        self.title = title
        self.file_type = file_type
        self.semester = semester
        self.subject = subject
        self.discovered_at = discovered_at or datetime.utcnow()


class DownloadedResource:
    def __init__(
        self,
        resource_id: int,
        source_url: str,
        local_path: str,
        sha256: str,
        file_size: int,
        status: str = ProcessingStatus.DOWNLOADED,
        downloaded_at: Optional[datetime] = None,
    ):
        self.resource_id = resource_id
        self.source_url = source_url
        self.local_path = local_path
        self.sha256 = sha256
        self.file_size = file_size
        self.status = status
        self.downloaded_at = downloaded_at or datetime.utcnow()


class IngestionRecord:
    def __init__(
        self,
        resource_id: int,
        source_url: str,
        sha256: Optional[str],
        status: str,
        semester: Optional[str] = None,
        subject: Optional[str] = None,
        exam_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.resource_id = resource_id
        self.source_url = source_url
        self.sha256 = sha256
        self.status = status
        self.semester = semester
        self.subject = subject
        self.exam_id = exam_id
        self.created_at = created_at or datetime.utcnow()


# ------------------------------------------------------------------
# SQLAlchemy Model
# ------------------------------------------------------------------
class TheHelperIngestion(Base):
    __tablename__ = "thehelper_ingestion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_url = Column(String(1024), nullable=False, index=True)
    title = Column(String(512), nullable=True)
    file_type = Column(String(64), nullable=True)
    semester = Column(String(64), nullable=True, index=True)
    subject = Column(String(128), nullable=True, index=True)
    sha256 = Column(String(64), nullable=True, index=True, unique=True)
    local_path = Column(String(1024), nullable=True)
    file_size = Column(Integer, nullable=True)
    status = Column(String(32), nullable=False, index=True, default=ProcessingStatus.DISCOVERED)
    error_message = Column(Text, nullable=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=True)
    question_count = Column(Integer, nullable=True)
    discovered_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    downloaded_at = Column(DateTime, nullable=True)
    processing_started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    failed_at = Column(DateTime, nullable=True)
    metadata_json = Column(Text, nullable=True)  # JSON string for extra provenance

    __table_args__ = (
        Index("ix_thehelper_ingestion_sha256", "sha256"),
        Index("ix_thehelper_ingestion_source_url", "source_url"),
        Index("ix_thehelper_ingestion_status", "status"),
        Index("ix_thehelper_ingestion_semester", "semester"),
        Index("ix_thehelper_ingestion_subject", "subject"),
        Index("ix_thehelper_ingestion_created_at", "discovered_at"),
        Index("ix_thehelper_ingestion_exam_id", "exam_id"),
    )

    exam = relationship("Exam", back_populates="thehelper_ingestions")


# Attach relationship to Exam model (lazy import to avoid circular issues)
from app.models.core import Exam
if hasattr(Exam, "__table__"):
    if not hasattr(Exam, "thehelper_ingestions"):
        from sqlalchemy.orm import relationship
        Exam.thehelper_ingestions = relationship(
            "TheHelperIngestion", back_populates="exam"
        )


# ------------------------------------------------------------------
# Repository
# ------------------------------------------------------------------
class IngestionRepository:
    """Repository managing The Helper ingestion pipeline."""

    def __init__(self, session: Session):
        self.session = session

    # 1 -- init handled above

    # 2
    def save_discovered_resource(self, resource: DiscoveredResource) -> int:
        record = TheHelperIngestion(
            source_url=resource.source_url,
            title=resource.title,
            file_type=resource.file_type,
            semester=resource.semester,
            subject=resource.subject,
            status=ProcessingStatus.DISCOVERED,
            discovered_at=resource.discovered_at,
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record.id  # resource_id for tracking

    # 3
    def update_resource_status(self, resource_id: int, status: ProcessingStatus, **metadata):
        record = self.session.query(TheHelperIngestion).filter(
            TheHelperIngestion.id == resource_id
        ).first()
        if record is None:
            raise ValueError(f"Resource {resource_id} not found")
        record.status = status.value if isinstance(status, ProcessingStatus) else str(status)
        if metadata:
            import json
            existing = {}
            try:
                if record.metadata_json:
                    existing = json.loads(record.metadata_json)
            except Exception:
                pass
            existing.update(metadata)
            record.metadata_json = json.dumps(existing)
        self.session.commit()
        self.session.refresh(record)

    # 4
    def mark_downloaded(self, resource_id: int, local_path: str, sha256: str, file_size: int):
        record = self.session.query(TheHelperIngestion).filter(
            TheHelperIngestion.id == resource_id
        ).first()
        if record is None:
            raise ValueError(f"Resource {resource_id} not found")
        record.local_path = local_path
        record.sha256 = sha256
        record.file_size = file_size
        record.status = ProcessingStatus.DOWNLOADED.value
        record.downloaded_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(record)

    # 5
    def mark_processing(self, resource_id: int, exam_id: Optional[int] = None):
        record = self.session.query(TheHelperIngestion).filter(
            TheHelperIngestion.id == resource_id
        ).first()
        if record is None:
            raise ValueError(f"Resource {resource_id} not found")
        record.status = ProcessingStatus.PROCESSING.value
        record.processing_started_at = datetime.utcnow()
        if exam_id is not None:
            record.exam_id = exam_id
        self.session.commit()
        self.session.refresh(record)

    # 6
    def mark_completed(self, resource_id: int, exam_id: int, question_count: int):
        record = self.session.query(TheHelperIngestion).filter(
            TheHelperIngestion.id == resource_id
        ).first()
        if record is None:
            raise ValueError(f"Resource {resource_id} not found")
        record.status = ProcessingStatus.COMPLETED.value
        record.exam_id = exam_id
        record.question_count = question_count
        record.completed_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(record)

    # 7
    def mark_failed(self, resource_id: int, error: str):
        record = self.session.query(TheHelperIngestion).filter(
            TheHelperIngestion.id == resource_id
        ).first()
        if record is None:
            raise ValueError(f"Resource {resource_id} not found")
        record.status = ProcessingStatus.FAILED.value
        record.error_message = error
        record.failed_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(record)

    # 8
    def get_unprocessed_resources(self) -> List[DownloadedResource]:
        query = self.session.query(TheHelperIngestion).filter(
            TheHelperIngestion.status == ProcessingStatus.DOWNLOADED.value
        )
        results = query.all()
        return [
            DownloadedResource(
                resource_id=r.id,
                source_url=r.source_url,
                local_path=r.local_path or "",
                sha256=r.sha256 or "",
                file_size=r.file_size or 0,
                status=r.status,
                downloaded_at=r.downloaded_at,
            )
            for r in results
        ]

    # 9
    def get_resources_by_status(self, status: ProcessingStatus) -> List[IngestionRecord]:
        query = self.session.query(TheHelperIngestion).filter(
            TheHelperIngestion.status == (status.value if isinstance(status, ProcessingStatus) else str(status))
        )
        results = query.all()
        return [
            IngestionRecord(
                resource_id=r.id,
                source_url=r.source_url,
                sha256=r.sha256,
                status=r.status,
                semester=r.semester,
                subject=r.subject,
                exam_id=r.exam_id,
                created_at=r.discovered_at,
            )
            for r in results
        ]

    # 10
    def check_sha256_exists(self, sha256: str) -> Optional[int]:
        record = self.session.query(TheHelperIngestion).filter(
            TheHelperIngestion.sha256 == sha256
        ).first()
        return record.id if record else None

    # 11
    def get_ingestion_stats(self) -> Dict[str, Any]:
        from sqlalchemy import func
        stats: Dict[str, Any] = {}
        total = self.session.query(TheHelperIngestion).count()
        stats["total"] = total

        # By status
        status_counts = (
            self.session.query(TheHelperIngestion.status, func.count(TheHelperIngestion.id))
            .group_by(TheHelperIngestion.status)
            .all()
        )
        stats["by_status"] = {s: c for s, c in status_counts}

        # By semester
        sem_counts = (
            self.session.query(TheHelperIngestion.semester, func.count(TheHelperIngestion.id))
            .filter(TheHelperIngestion.semester != None)
            .group_by(TheHelperIngestion.semester)
            .all()
        )
        stats["by_semester"] = {s: c for s, c in sem_counts if s}

        # By subject
        sub_counts = (
            self.session.query(TheHelperIngestion.subject, func.count(TheHelperIngestion.id))
            .filter(TheHelperIngestion.subject != None)
            .group_by(TheHelperIngestion.subject)
            .all()
        )
        stats["by_subject"] = {s: c for s, c in sub_counts if s}

        # By file type
        type_counts = (
            self.session.query(TheHelperIngestion.file_type, func.count(TheHelperIngestion.id))
            .filter(TheHelperIngestion.file_type != None)
            .group_by(TheHelperIngestion.file_type)
            .all()
        )
        stats["by_file_type"] = {t: c for t, c in type_counts if t}

        # Success / failure rates
        completed = stats["by_status"].get(ProcessingStatus.COMPLETED.value, 0)
        failed = stats["by_status"].get(ProcessingStatus.FAILED.value, 0)
        stats["success_rate"] = round(completed / total, 4) if total > 0 else 0.0
        stats["failure_rate"] = round(failed / total, 4) if total > 0 else 0.0

        # Exam linkage
        linked = (
            self.session.query(TheHelperIngestion)
            .filter(TheHelperIngestion.exam_id != None)
            .count()
        )
        stats["exam_linked"] = linked

        return stats

    # 12
    def get_subject_coverage(self) -> Dict[str, int]:
        from sqlalchemy import func
        results = (
            self.session.query(TheHelperIngestion.subject, func.count(TheHelperIngestion.id))
            .filter(TheHelperIngestion.subject != None)
            .group_by(TheHelperIngestion.subject)
            .all()
        )
        return {s: c for s, c in results if s}
