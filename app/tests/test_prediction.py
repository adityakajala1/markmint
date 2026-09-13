import pytest
from app.services.prediction.engine import PredictionEngineService

def test_insufficient_data() -> None:
    engine = PredictionEngineService(min_sample_size=3)
    
    # Provide only 2 exams
    exams = [{"year": 2021}, {"year": 2022}]
    result = engine.generate_predictions(exams)
    
    assert result.insufficient_data is True
    assert len(result.predictions) == 1
    assert result.predictions[0].confidence == "Insufficient Evidence"

def test_high_weight_topic_prediction() -> None:
    engine = PredictionEngineService(min_sample_size=3, recency_weight_decay=0.9)
    
    # 3 exams, Trees appear in all 3 and have high marks
    exams = [
        {
            "id": "e1", "year": 2021,
            "questions": [{"id": "q1", "topic": "Trees", "marks": 20.0}]
        },
        {
            "id": "e2", "year": 2022,
            "questions": [{"id": "q2", "topic": "Trees", "marks": 25.0}]
        },
        {
            "id": "e3", "year": 2023,
            "questions": [
                {"id": "q3", "topic": "Trees", "marks": 25.0},
                {"id": "q4", "topic": "Graphs", "marks": 5.0}
            ]
        }
    ]
    
    result = engine.generate_predictions(exams)
    assert result.insufficient_data is False
    
    # Should predict Trees as High-Weight
    assert len(result.predictions) >= 1
    trees_pred = next(p for p in result.predictions if "Trees" in p.predicted_insight)
    
    assert trees_pred.confidence == "High"
    assert trees_pred.historical_frequency == 1.0 # 3 out of 3 papers
    assert trees_pred.sample_size == 3
    
    # Total marks = 20 + 25 + 30 = 75
    # Trees marks = 70. 70/75 = 93.3%
    # We round to avoid false precision, so "93%"
    assert "93%" in trees_pred.supporting_evidence
    assert "3 of 3 papers" in trees_pred.supporting_evidence
