from typing import Generic, TypeVar, Optional, List
from typing import Optional
from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from enum import Enum

class ClassificationResult(BaseModel):
    question_type: Optional[str] = None
    cognitive_level: Optional[str] = None
    difficulty: Optional[float] = None
    topics: list[str] = []
    confidence: float

class ExamEvidenceStats(BaseModel):
    number_of_papers: int
    number_of_questions: int
    total_marks: float
    years: list[int]
    exam_types: list[str]
    question_ids: list[int] = []
    question_families: list[str] = []
    recurrence_interval: float = 0.0

class StudyEvidenceStats(BaseModel):
    number_of_documents: int
    number_of_evidence_chunks: int
    source_types: list[str]
    source_diversity: int # Number of distinct source types
    coverage_strength: str # 'STRONG', 'MODERATE', 'WEAK', 'NONE'
    evidence_chunk_ids: list[int] = []

class SyllabusEvidenceStats(BaseModel):
    units: list[str]
    syllabus_references: int

class ConceptEvidenceReport(BaseModel):
    concept_id: int
    canonical_name: str
    unit: Optional[str]
    subtopic: Optional[str]

    related_concept_ids: list[int] = []

    exam_evidence: ExamEvidenceStats
    study_evidence: StudyEvidenceStats
    syllabus_evidence: SyllabusEvidenceStats

class PriorityDimensions(BaseModel):
    historical_importance_score: float # based on paper coverage / marks
    recent_momentum_score: float # based on recent appearances
    marks_importance_score: float
    recurrence_score: float
    syllabus_relevance_score: float
    study_coverage_score: float
    evidence_strength_score: float

class StudyPriorityProfile(BaseModel):
    concept_id: int
    dimensions: PriorityDimensions
    final_priority_ranking: float
    is_resource_gap: bool # High exam importance but weak study coverage
    is_well_supported: bool # High exam importance AND strong study coverage
    weighting_documentation: dict[str, float] # To keep ranking transparent


# Course Schemas
class CourseBase(BaseModel):
    name: str
    code: str


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True


# Exam Schemas
class ExamBase(BaseModel):
    year: int
    term: str


class ExamCreate(ExamBase):
    course_id: int


class Exam(ExamBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True


# Section Schemas
class SectionBase(BaseModel):
    name: str
    instructions: Optional[str] = None


class SectionCreate(SectionBase):
    exam_id: int


class Section(SectionBase):
    id: int
    exam_id: int

    class Config:
        from_attributes = True


# Topic Schemas
class TopicBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class TopicCreate(TopicBase):
    pass


class Topic(TopicBase):
    id: int

    class Config:
        from_attributes = True


# Question Schemas
class QuestionBase(BaseModel):
    question_number: str
    original_text: str
    normalized_text: Optional[str] = None
    marks: Optional[float] = None
    is_alternative: bool = False
    question_type: Optional[str] = None
    cognitive_level: Optional[str] = None
    difficulty: Optional[float] = None


class QuestionCreate(QuestionBase):
    section_id: int


class Question(QuestionBase):
    id: int
    section_id: int

    class Config:
        from_attributes = True

class DataSufficiency(str, Enum):
    INSUFFICIENT = "insufficient"
    LIMITED = "limited"
    MODERATE = "moderate"
    STRONG = "strong"

class DNASampleSize(BaseModel):
    papers: int
    questions: int
    time_range_years: tuple[int, int]
    exam_types: list[str]
    sufficiency: DataSufficiency

class MetricWithEvidence(BaseModel):
    value: float | str | int
    sample_size: int
    denominator: Optional[int] = None
    supporting_question_ids: list[int] = []

class TopicDNA(BaseModel):
    topic: str
    question_count: int
    paper_coverage: float
    total_marks: float
    average_marks: float
    long_answer_frequency: float
    short_answer_frequency: float
    recent_frequency: float
    historical_frequency: float
    difficulty_distribution: dict[str, int] # e.g. "0.0-0.3": 5

class UnitDNA(BaseModel):
    unit: str
    question_count: int
    marks: float
    paper_coverage: float
    recent_weighting: float
    historical_weighting: float

class QuestionTypeDNA(BaseModel):
    question_type: str
    count: int
    percentage: float
    marks_weighting: float

class RepetitionDNA(BaseModel):
    exact_count: int
    near_count: int
    conceptual_count: int
    structural_count: int

class FamilyDNA(BaseModel):
    family_name: str
    occurrences: int
    years: list[int]
    exam_types: list[str]
    average_marks: float
    recurrence_interval_years: float
    recent_recurrence_count: int
    trend: str # 'growing', 'declining', 'stable'

class TemporalTrend(BaseModel):
    metric_name: str
    trend_type: str # 'rising', 'declining', 'stable'
    historical_avg: float
    recent_avg: float
    description: str

class ExamDNA(BaseModel):
    sample_size: DNASampleSize

    topics: list[TopicDNA]
    units: list[UnitDNA]
    question_types: list[QuestionTypeDNA]

    repetition: RepetitionDNA
    families: list[FamilyDNA]

    temporal_trends: list[TemporalTrend]

class ProvenanceNode(BaseModel):
    record_type: str # 'question', 'exam', 'document', 'study_evidence'
    record_id: int
    context_text: Optional[str] = None

class FactualMetrics(BaseModel):
    supported_papers: int
    total_papers: int
    supported_questions: int
    total_marks: float
    long_answer_count: int
    recent_papers: int
    recurring_families: int

class InsightExplanation(BaseModel):
    finding_type: str # 'topic_importance', 'trend', 'repetition'
    subject: str
    time_range_years: tuple[int, int]
    insight_text: str # Deterministic, factual string

    metrics: FactualMetrics
    provenance_chain: list[ProvenanceNode]

    confidence: str # 'HIGH', 'MEDIUM', 'LOW', 'INSUFFICIENT'
    limitations: Optional[str] = None

class TrendClassification(str, Enum):
    RISING = "rising"
    DECLINING = "declining"
    STABLE = "stable"
    VOLATILE = "volatile"
    INSUFFICIENT = "insufficient"

class EvolutionEvidence(BaseModel):
    before_value: float
    after_value: float
    magnitude: float
    sample_size_before_papers: int
    sample_size_after_papers: int
    sample_size_before_questions: int
    sample_size_after_questions: int
    supporting_exam_ids: list[int]

class ChangePoint(BaseModel):
    dimension: str
    change_year: int
    time_range_before: tuple[int, int]
    time_range_after: tuple[int, int]
    description: str
    evidence: EvolutionEvidence
    confidence: str # 'HIGH', 'MEDIUM', 'LOW', 'INSUFFICIENT'

class ComponentTrend(BaseModel):
    name: str # e.g. "Graphs" or "Unit 1"
    classification: TrendClassification
    evidence: EvolutionEvidence

class EvolutionReport(BaseModel):
    course_id: int
    total_papers_analyzed: int
    excluded_papers_missing_year: int = 0
    time_range: tuple[int, int]

    topic_trends: list[ComponentTrend]
    unit_trends: list[ComponentTrend]

    format_change_points: list[ChangePoint]
    difficulty_change_points: list[ChangePoint]
    repetition_change_points: list[ChangePoint]


class ExtractedQuestion(BaseModel):
    question_number: str
    original_text: str
    marks: Optional[float] = None
    is_alternative: bool = False
    page_number: int
    confidence: float


class ExtractedSection(BaseModel):
    name: str
    instructions: Optional[str] = None
    questions: list[ExtractedQuestion]


class DocumentExtractionResult(BaseModel):
    sections: list[ExtractedSection]
    total_pages: int
    successful: bool
    error_message: Optional[str] = None


class ExtractedConcept(BaseModel):
    concept_name: str
    knowledge_type: str # 'definition', 'formula', 'algorithm', 'context'
    content: str
    original_text: str
    page_number: Optional[int] = None
    confidence: float


class KnowledgeExtractionResult(BaseModel):
    concepts: list[ExtractedConcept]
    total_pages: int
    successful: bool
    error_message: Optional[str] = None

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

class Prediction(BaseModel):
    characteristic: str
    predicted_insight: str
    confidence: str # "High", "Medium", "Low", "Insufficient Evidence"
    supporting_evidence: str
    sample_size: int
    historical_frequency: Optional[float] = None
    limitations: str

class ExamPredictions(BaseModel):
    predictions: list[Prediction]
    total_papers_analyzed: int
    insufficient_data: bool

class SearchResultType(str, Enum):
    EXAM_QUESTION = "exam_question"
    STUDY_MATERIAL = "study_material"
    CONCEPT = "concept"
    QUESTION_FAMILY = "question_family"
    ANALYSIS_FINDING = "analysis_finding"

class SearchFilters(BaseModel):
    subject: Optional[str] = None
    semester: Optional[int] = None
    year: Optional[int] = None
    exam_type: Optional[str] = None
    unit: Optional[str] = None
    topic: Optional[str] = None
    marks: Optional[float] = None
    resource_type: Optional[str] = None

class SearchResult(BaseModel):
    id: int
    result_type: SearchResultType
    title: str
    text_snippet: str

    subject: Optional[str] = None
    unit: Optional[str] = None
    topic: Optional[str] = None
    year: Optional[int] = None
    exam_type: Optional[str] = None

    relevance_score: float
    provenance_url: Optional[str] = None
    attribution: Optional[str] = None

class SearchQuery(BaseModel):
    raw_query: str
    filters: Optional[SearchFilters] = None
    limit: int = 10

class ParsedIntent(BaseModel):
    target_type: Optional[SearchResultType] = None
    extracted_marks: Optional[float] = None
    extracted_subject: Optional[str] = None
    extracted_trend: Optional[str] = None
    clean_search_term: str