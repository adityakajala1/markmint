import pytest
from datetime import datetime
from backend.services.study_intelligence import StudyIntelligenceService, PriorityResult, StudyPriority
from backend.services.prediction.engine import PredictionResult
from backend.models.core import Document, StudyEvidence, Concept, Topic, Course, Unit

def test_calculate_study_priority():
    svc = StudyIntelligenceService(db=None)
    
    # Exceptionally high
    p1 = PredictionResult(target="topic", name="Eigenvalues", rank=1, score=0.85, confidence="high", evidence={"freq": 0.4})
    r1 = svc.calculate_study_priority(p1)
    assert r1.priority == StudyPriority.VERY_HIGH
    assert "Exceptionally high" in "".join(r1.reasons)
    
    # High
    p2 = PredictionResult(target="topic", name="Matrices", rank=2, score=0.65, confidence="high", evidence={})
    r2 = svc.calculate_study_priority(p2)
    assert r2.priority == StudyPriority.HIGH
    
    # Medium
    p3 = PredictionResult(target="topic", name="Integration", rank=3, score=0.45, confidence="medium", evidence={"recent_freq": 0.25})
    r3 = svc.calculate_study_priority(p3)
    assert r3.priority == StudyPriority.MEDIUM
    assert "Appeared recently" in "".join(r3.reasons)

def test_priority_ordering():
    svc = StudyIntelligenceService(db=None)
    
    predictions = [
        PredictionResult("topic", "T1", 3, 0.45, "medium", {}), # MEDIUM
        PredictionResult("topic", "T2", 1, 0.85, "high", {}), # VERY_HIGH
        PredictionResult("topic", "T3", 2, 0.70, "high", {}), # HIGH
        PredictionResult("topic", "T4", 4, 0.10, "low", {}), # LOW
    ]
    
    # generate_study_plan expects a mock DB to get resources, we can patch `get_topic_resources`
    svc.get_topic_resources = lambda t, c: []
    
    plan = svc.generate_study_plan(predictions, course_id=1)
    
    # Order should be VERY_HIGH, HIGH, MEDIUM, LOW
    assert plan[0]["topic"] == "T2"
    assert plan[1]["topic"] == "T3"
    assert plan[2]["topic"] == "T1"
    assert plan[3]["topic"] == "T4"
