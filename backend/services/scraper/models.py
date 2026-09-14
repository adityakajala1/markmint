"""
Pydantic models for The Helper scraper module.

These models track resources through the discovery, classification, download,
and ingestion pipeline for ExamScope.
"""

from datetime import datetime
from enum import Enum
from hashlib import sha256
from typing import Optional
from urllib.parse import urlparse, parse_qs, urlencode

from pydantic import BaseModel, Field, field_validator, computed_field, ConfigDict


class ResourceType(str, Enum):
    """Classification of academic resource types."""

    PYQ = "pyq"
    CT_PAPER = "ct_paper"
    SEMESTER_PAPER = "semester_paper"
    SYLLABUS = "syllabus"
    QUESTION_BANK = "question_bank"
    NOTES = "notes"
    IMPORTANT_QUESTIONS = "important_questions"
    ANSWER_KEY = "answer_key"
    OTHER = "other"


class ExamType(str, Enum):
    """Type of examination or assessment."""

    SEMESTER = "semester"
    CT = "ct"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    OTHER = "other"


class ProcessingStatus(str, Enum):
    """Current state in the processing pipeline."""

    DISCOVERED = "discovered"
    CLASSIFIED = "classified"
    DOWNLOADED = "downloaded"
    EXTRACTED = "extracted"
    ANALYZED = "analyzed"
    FAILED = "failed"


class DiscoveredResource(BaseModel):
    """
    Metadata extracted during initial crawling phase.

    Represents a resource discovered from a university website before
    classification or download.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=False,
    )

    semester: Optional[str] = Field(
        None,
        description="Semester identifier (e.g., '1', '2', 'Summer')"
    )
    subject: Optional[str] = Field(
        None,
        description="Subject or course name"
    )
    title: str = Field(
        ...,
        min_length=1,
        description="Resource title as found on source page"
    )
    resource_type: Optional[ResourceType] = Field(
        None,
        description="Preliminary resource classification"
    )
    year: Optional[int] = Field(
        None,
        ge=2000,
        le=2100,
        description="Academic year"
    )
    exam_type: Optional[ExamType] = Field(
        None,
        description="Type of examination"
    )
    source_url: str = Field(
        ...,
        description="URL of the page where resource was discovered"
    )
    file_url: Optional[str] = Field(
        None,
        description="Direct URL to downloadable file (PDF, etc.)"
    )
    discovery_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this resource was discovered"
    )

    @field_validator("source_url", "file_url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        """Ensure URLs are properly formed."""
        if v is None:
            return v

        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")

        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Clean up title text."""
        return " ".join(v.split())

    @computed_field
    @property
    def resource_id(self) -> str:
        """
        Generate unique identifier for this resource.

        Combines source domain with normalized URL to create a stable ID
        that survives minor URL parameter changes.
        """
        url = self.file_url or self.source_url
        parsed = urlparse(url)

        # Normalize URL by sorting query parameters
        params = parse_qs(parsed.query)
        sorted_params = urlencode(sorted(params.items()), doseq=True)

        normalized = f"{parsed.netloc}{parsed.path}"
        if sorted_params:
            normalized += f"?{sorted_params}"

        return sha256(normalized.encode()).hexdigest()[:16]

    @computed_field
    @property
    def data_quality_score(self) -> float:
        """
        Assess completeness of discovered metadata.

        Returns a score from 0.0 to 1.0 based on how many fields are populated.
        """
        fields_present = sum([
            self.semester is not None,
            self.subject is not None,
            self.resource_type is not None,
            self.year is not None,
            self.exam_type is not None,
            self.file_url is not None,
        ])

        return fields_present / 6.0


class ClassifiedResource(DiscoveredResource):
    """
    Resource after classification with ML confidence scores.

    Extends DiscoveredResource with classification results and confidence metrics.
    """

    resource_type: ResourceType = Field(
        ...,
        description="Classified resource type (required after classification)"
    )
    classification_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for resource_type classification"
    )
    exam_type_confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence score for exam_type classification"
    )
    classification_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When classification was performed"
    )
    classifier_version: Optional[str] = Field(
        None,
        description="Version of classifier model used"
    )

    @computed_field
    @property
    def classification_score(self) -> float:
        """
        Overall classification quality score.

        Combines classification confidence with data completeness.
        """
        return (self.classification_confidence + self.data_quality_score) / 2.0


class DownloadedResource(ClassifiedResource):
    """
    Resource after successful download with file metadata.

    Extends ClassifiedResource with download information and file integrity data.
    """

    file_hash: str = Field(
        ...,
        min_length=64,
        max_length=64,
        description="SHA-256 hash of downloaded file for integrity verification"
    )
    local_path: str = Field(
        ...,
        description="Absolute path to downloaded file on local filesystem"
    )
    file_size: int = Field(
        ...,
        gt=0,
        description="File size in bytes"
    )
    download_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When file was downloaded"
    )
    mime_type: Optional[str] = Field(
        None,
        description="MIME type of downloaded file"
    )

    @field_validator("file_hash")
    @classmethod
    def validate_hash(cls, v: str) -> str:
        """Ensure hash is valid hexadecimal."""
        try:
            int(v, 16)
        except ValueError:
            raise ValueError("file_hash must be valid hexadecimal")
        return v.lower()


class IngestionRecord(DownloadedResource):
    """
    Complete record tracking resource through ExamScope pipeline.

    Extends DownloadedResource with processing status and error tracking
    for the full ingestion workflow.
    """

    status: ProcessingStatus = Field(
        default=ProcessingStatus.DISCOVERED,
        description="Current processing state"
    )
    extraction_timestamp: Optional[datetime] = Field(
        None,
        description="When text/content extraction was completed"
    )
    analysis_timestamp: Optional[datetime] = Field(
        None,
        description="When analysis/indexing was completed"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error details if processing failed"
    )
    retry_count: int = Field(
        default=0,
        ge=0,
        description="Number of retry attempts for failed processing"
    )
    examscope_id: Optional[str] = Field(
        None,
        description="ID assigned by ExamScope system after ingestion"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Additional metadata extracted during processing"
    )

    @field_validator("status")
    @classmethod
    def validate_status_progression(cls, v: ProcessingStatus) -> ProcessingStatus:
        """Ensure status transitions are valid."""
        return v

    @computed_field
    @property
    def processing_duration(self) -> Optional[float]:
        """
        Total processing time in seconds from discovery to completion.

        Returns None if processing is not yet complete.
        """
        if self.analysis_timestamp is None:
            return None

        return (self.analysis_timestamp - self.discovery_timestamp).total_seconds()

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Check if resource has completed the full pipeline."""
        return self.status == ProcessingStatus.ANALYZED

    @computed_field
    @property
    def is_failed(self) -> bool:
        """Check if resource processing has failed."""
        return self.status == ProcessingStatus.FAILED


# Example usage and validation
if __name__ == "__main__":
    # Example discovered resource
    discovered = DiscoveredResource(
        title="Computer Networks Semester Exam 2024",
        source_url="https://university.edu/exams/cn-sem.pdf",
        file_url="https://university.edu/files/cn-2024.pdf",
        semester="5",
        subject="Computer Networks",
        year=2024,
    )

    print(f"Resource ID: {discovered.resource_id}")
    print(f"Quality Score: {discovered.data_quality_score:.2f}")

    # Example classified resource
    classified = ClassifiedResource(
        **discovered.model_dump(),
        resource_type=ResourceType.SEMESTER_PAPER,
        classification_confidence=0.95,
        exam_type_confidence=0.88,
        classifier_version="v1.2.0",
    )

    print(f"Classification Score: {classified.classification_score:.2f}")

    # Example downloaded resource
    downloaded = DownloadedResource(
        **classified.model_dump(),
        file_hash="a" * 64,
        local_path="/data/downloads/cn-2024.pdf",
        file_size=2048576,
        mime_type="application/pdf",
    )

    print(f"Downloaded to: {downloaded.local_path}")

    # Example ingestion record
    ingestion = IngestionRecord(
        **downloaded.model_dump(),
        status=ProcessingStatus.ANALYZED,
        examscope_id="ES-2024-001234",
        analysis_timestamp=datetime.utcnow(),
    )

    print(f"Complete: {ingestion.is_complete}")
    print(f"Duration: {ingestion.processing_duration:.2f}s")
