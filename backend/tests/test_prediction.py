import pytest
from types import SimpleNamespace

from backend.api.endpoints.predictions import _build_historical_exam_payloads
from backend.services.prediction.engine import ExamScopeCombinedModel
from backend.services.prediction.context import PredictionTarget
from backend.services.dna.analyzer import DNAAnalyzerService


def test_prediction_payload_uses_exam_assessment_type() -> None:
    question = SimpleNamespace(
        id=1,
        marks=1.0,
        is_alternative=False,
        topics=[SimpleNamespace(name="Topic")],
        memberships=[],
        family=None,
        difficulty=None,
        question_type=None,
    )
    exams = [
        SimpleNamespace(
            id=index,
            year=2025,
            assessment_type=assessment_type,
            sections=[SimpleNamespace(questions=[question])],
        )
        for index, assessment_type in enumerate(
            ("CT1", "CT2", "END_SEM", "UNKNOWN"), start=1
        )
    ]

    payloads = _build_historical_exam_payloads(exams)

    assert [payload["exam_type"] for payload in payloads] == [
        "CT1",
        "CT2",
        "END_SEM",
        "UNKNOWN",
    ]
    dna = DNAAnalyzerService.analyze(payloads)
    assert set(dna.sample_size.exam_types) == {"CT1", "CT2", "END_SEM", "UNKNOWN"}

def test_high_weight_topic_prediction() -> None:
    # 3 exams, Trees appear in all 3 and have high marks
    exams = [
        {
            "id": "e1", "year": 2021, "exam_type": "FINAL",
            "questions": [{"id": "q1", "topic": "Trees", "marks": 20.0, "is_alternative": False, "question_type": "LONG", "repetition_type": "singleton", "family_name": None, "difficulty": None}]
        },
        {
            "id": "e2", "year": 2022, "exam_type": "FINAL",
            "questions": [{"id": "q2", "topic": "Trees", "marks": 25.0, "is_alternative": False, "question_type": "LONG", "repetition_type": "singleton", "family_name": None, "difficulty": None}]
        },
        {
            "id": "e3", "year": 2023, "exam_type": "FINAL",
            "questions": [
                {"id": "q3", "topic": "Trees", "marks": 25.0, "is_alternative": False, "question_type": "LONG", "repetition_type": "singleton", "family_name": None, "difficulty": None},
                {"id": "q4", "topic": "Graphs", "marks": 5.0, "is_alternative": False, "question_type": "LONG", "repetition_type": "singleton", "family_name": None, "difficulty": None}
            ]
        }
    ]
    
    dna = DNAAnalyzerService.analyze(exams)
    
    engine = ExamScopeCombinedModel(dna)
    topic_preds = engine.predict(PredictionTarget.TOPIC)
    
    # Should predict Trees highly
    assert len(topic_preds) >= 1
    
    # Trees should be first
    trees_pred = topic_preds[0]
    assert trees_pred.name == "Trees"
    
    # Confidence should map to HIGH because score is very high (appears in all exams, heavy marks)
    assert trees_pred.confidence == "HIGH"
    
    # Trees freq should be 1.0 (3/3 papers)
    assert trees_pred.evidence["hist_freq"] > 0.5
    assert trees_pred.evidence["occurrences"] == 3
