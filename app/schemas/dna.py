from pydantic import BaseModel
from typing import Optional, Any

class MetricWithEvidence(BaseModel):
    value: float | str
    sample_size: int
    denominator: Optional[int] = None
    supporting_question_ids: list[str] = []

class DistributionMetric(BaseModel):
    key: str
    count: int
    percentage_of_total: float
    marks_weighting: float

class ExamDNA(BaseModel):
    total_exams_analyzed: int
    total_questions_analyzed: int
    total_marks_analyzed: float

    # Distributions
    topic_distribution: list[DistributionMetric]
    unit_distribution: list[DistributionMetric]
    question_type_distribution: list[DistributionMetric]
    cognitive_level_distribution: list[DistributionMetric]
    
    # Aggregates
    average_difficulty: MetricWithEvidence
    
    # Repetition
    exact_repetition_rate: MetricWithEvidence
    conceptual_repetition_rate: MetricWithEvidence
    structural_repetition_rate: MetricWithEvidence
    
    # Trends
    temporal_trends: dict[str, Any] = {} # e.g., {"topic_X_frequency": [{"year": 2021, "freq": 0.2}]}
