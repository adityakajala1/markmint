import pytest
from backend.schemas import (
    ConceptEvidenceReport, ExamEvidenceStats, StudyEvidenceStats, SyllabusEvidenceStats
)
from backend.services.concept.priority import ConceptPriorityService

def test_priority_no_study_pollution():
    # Base concept with high exam evidence
    base_report = ConceptEvidenceReport(
        concept_id=1,
        canonical_name="Trees",
        unit=None, subtopic=None, related_concept_ids=[],
        exam_evidence=ExamEvidenceStats(
            number_of_papers=8, number_of_questions=15, total_marks=75,
            years=[2020, 2021, 2022, 2023], exam_types=[], recurrence_interval=1.0
        ),
        study_evidence=StudyEvidenceStats(
            number_of_documents=0, number_of_evidence_chunks=0, source_types=[],
            source_diversity=0, coverage_strength="NONE"
        ),
        syllabus_evidence=SyllabusEvidenceStats(units=[], syllabus_references=1)
    )

    profile_no_study = ConceptPriorityService.calculate_priority(base_report, total_historical_papers=10)
    
    # Same concept but now with massive study evidence
    base_report.study_evidence.number_of_documents = 100
    base_report.study_evidence.coverage_strength = "STRONG"
    
    profile_with_study = ConceptPriorityService.calculate_priority(base_report, total_historical_papers=10)
    
    # CRITICAL ASSERTION: Study frequency must NOT alter the final exam priority score
    assert profile_no_study.final_priority_ranking == profile_with_study.final_priority_ranking
    
    # But it SHOULD alter the gap analysis tags
    assert profile_no_study.is_resource_gap is True
    assert profile_no_study.is_well_supported is False
    
    assert profile_with_study.is_resource_gap is False
    assert profile_with_study.is_well_supported is True

def test_priority_dimensions():
    report = ConceptEvidenceReport(
        concept_id=2, canonical_name="Hashing", unit=None, subtopic=None,
        exam_evidence=ExamEvidenceStats(
            number_of_papers=10, number_of_questions=10, total_marks=100,
            years=[2022, 2023], exam_types=[], recurrence_interval=1.0
        ),
        study_evidence=StudyEvidenceStats(
            number_of_documents=0, number_of_evidence_chunks=0, source_types=[],
            source_diversity=0, coverage_strength="NONE"
        ),
        syllabus_evidence=SyllabusEvidenceStats(units=[], syllabus_references=1)
    )
    
    profile = ConceptPriorityService.calculate_priority(report, total_historical_papers=10)
    
    # 10/10 papers = 1.0
    assert profile.dimensions.historical_importance_score == 1.0
    # 100 marks / 10 q = 10 avg -> 1.0
    assert profile.dimensions.marks_importance_score == 1.0
    # 1.0 recurrence -> 1.0
    assert profile.dimensions.recurrence_score == 1.0
    # 1 ref -> 1.0
    assert profile.dimensions.syllabus_relevance_score == 1.0
