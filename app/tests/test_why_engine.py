import pytest
from app.schemas import FactualMetrics
from app.services.evidence.engine import WhyEngineService

def test_why_engine_deterministic_formatting():
    metrics = FactualMetrics(
        supported_papers=14,
        total_papers=18,
        supported_questions=31,
        total_marks=94.0,
        long_answer_count=9,
        recent_papers=5,
        recurring_families=3
    )
    
    explanation = WhyEngineService.generate_topic_importance(
        topic_name="Trees",
        subject="Computer Science",
        metrics=metrics,
        time_range=(2018, 2023),
        question_ids=[1, 2, 3]
    )
    
    # Assert deterministic text (no exaggeration)
    assert "14 of 18" in explanation.insight_text
    assert "31 questions" in explanation.insight_text
    assert "probability" not in explanation.insight_text.lower()
    
    # Assert provenance
    assert len(explanation.provenance_chain) == 3
    assert explanation.provenance_chain[0].record_type == "question"
    assert explanation.confidence == "HIGH"

def test_why_engine_insufficient_evidence():
    metrics = FactualMetrics(
        supported_papers=2,
        total_papers=2,
        supported_questions=4,
        total_marks=20.0,
        long_answer_count=2,
        recent_papers=2,
        recurring_families=0
    )
    
    explanation = WhyEngineService.generate_topic_importance(
        topic_name="Advanced Graphs",
        subject="Computer Science",
        metrics=metrics,
        time_range=(2022, 2023),
        question_ids=[4, 5]
    )
    
    # Assert downgrade
    assert explanation.confidence == "INSUFFICIENT"
    assert "Insufficient historical data" in explanation.insight_text
