import pytest
from app.services.dna.evolution import ExamEvolutionService
from app.schemas import TrendClassification

def test_evolution_insufficient_data():
    exams = [
        {"id": 1, "year": 2021, "questions": [{"topic": "A", "marks": 5}]},
        {"id": 2, "year": 2022, "questions": [{"topic": "A", "marks": 5}]},
        {"id": 3, "year": 2023, "questions": [{"topic": "A", "marks": 5}]}
    ]
    # Need 4 exams minimum to split into 2 halves for meaningful comparison
    report = ExamEvolutionService.analyze_evolution(1, exams)
    assert report.total_papers_analyzed == 3
    assert len(report.topic_trends) == 0

def test_evolution_rising_trend():
    exams = [
        {"id": 1, "year": 2018, "questions": [{"topic": "A", "marks": 1}]},
        {"id": 2, "year": 2019, "questions": [{"topic": "A", "marks": 1}]},
        {"id": 3, "year": 2020, "questions": [{"topic": "A", "marks": 5}, {"topic": "A", "marks": 5}]},
        {"id": 4, "year": 2021, "questions": [{"topic": "A", "marks": 5}, {"topic": "A", "marks": 5}]}
    ]
    
    report = ExamEvolutionService.analyze_evolution(1, exams)
    
    trend_A = next((t for t in report.topic_trends if t.name == "A"), None)
    assert trend_A is not None
    assert trend_A.classification == TrendClassification.RISING
    assert trend_A.evidence.before_value == 1.0 # 2 marks / 2 papers
    assert trend_A.evidence.after_value == 10.0 # 20 marks / 2 papers
    assert trend_A.evidence.magnitude == 9.0

def test_evolution_change_point():
    exams = [
        {"id": 1, "year": 2018, "questions": [{"question_type": "definition", "marks": 2}, {"question_type": "numerical", "marks": 1}]},
        {"id": 2, "year": 2019, "questions": [{"question_type": "explanation", "marks": 2}, {"question_type": "application", "marks": 1}]},
        {"id": 3, "year": 2020, "questions": [{"question_type": "implementation", "marks": 5}, {"question_type": "numerical", "marks": 5}]},
        {"id": 4, "year": 2021, "questions": [{"question_type": "application", "marks": 15}]}
    ]
    
    report = ExamEvolutionService.analyze_evolution(1, exams)
    
    assert len(report.format_change_points) == 1
    cp = report.format_change_points[0]
    
    assert cp.dimension == "format.practical_focus"
    assert "increasingly implementation and application-heavy" in cp.description
    assert cp.change_year == 2020
    assert cp.evidence.before_value == 1.0 # 2 practical marks / 2 papers in H1
    assert cp.evidence.after_value == 12.5 # 25 marks / 2 papers in H2

def test_evolution_missing_years():
    exams = [
        {"id": 1, "year": 2018, "questions": [{"topic": "A", "marks": 1}, {"topic": "A", "marks": 1}]},
        {"id": 2, "year": None, "questions": [{"topic": "A", "marks": 100}]}, # Should be ignored chronologically
        {"id": 3, "year": 2019, "questions": [{"topic": "A", "marks": 1}]},
        {"id": 4, "year": 2020, "questions": [{"topic": "A", "marks": 5}, {"topic": "A", "marks": 5}]},
        {"id": 5, "year": 2021, "questions": [{"topic": "A", "marks": 5}]}
    ]
    
    report = ExamEvolutionService.analyze_evolution(1, exams)
    assert report.excluded_papers_missing_year == 1
    assert report.total_papers_analyzed == 4
    
    trend_A = next((t for t in report.topic_trends if t.name == "A"), None)
    assert trend_A is not None
    assert trend_A.evidence.before_value == 1.5  # (2+1)/2, not including the 100
    assert trend_A.evidence.after_value == 7.5   # (10+5)/2

def test_evolution_all_missing_years():
    exams = [
        {"id": 1, "year": None, "questions": [{"topic": "A", "marks": 1}]},
        {"id": 2, "year": None, "questions": [{"topic": "A", "marks": 1}]}
    ]
    report = ExamEvolutionService.analyze_evolution(1, exams)
    assert report.excluded_papers_missing_year == 2
    assert report.total_papers_analyzed == 0
    assert len(report.topic_trends) == 0

def test_evolution_duplicate_years():
    exams = [
        {"id": 1, "year": 2020, "questions": [{"topic": "A", "marks": 2}, {"topic": "A", "marks": 2}]},
        {"id": 2, "year": 2020, "questions": [{"topic": "A", "marks": 2}]},
        {"id": 3, "year": 2021, "questions": [{"topic": "A", "marks": 10}, {"topic": "A", "marks": 10}]},
        {"id": 4, "year": 2021, "questions": [{"topic": "A", "marks": 10}]}
    ]
    report = ExamEvolutionService.analyze_evolution(1, exams)
    assert report.excluded_papers_missing_year == 0
    assert report.total_papers_analyzed == 4
    
    trend_A = next((t for t in report.topic_trends if t.name == "A"), None)
    assert trend_A is not None
    assert trend_A.classification == TrendClassification.RISING
    assert trend_A.evidence.before_value == 3.0 # (4 + 2) / 2
    assert trend_A.evidence.after_value == 15.0 # (20 + 10) / 2

def test_evolution_sparse_years():
    exams = [
        {"id": 1, "year": 2005, "questions": [{"topic": "A", "marks": 1}, {"topic": "A", "marks": 1}]},
        {"id": 2, "year": 2012, "questions": [{"topic": "A", "marks": 1}]},
        {"id": 3, "year": 2020, "questions": [{"topic": "A", "marks": 1}, {"topic": "A", "marks": 1}]},
        {"id": 4, "year": 2024, "questions": [{"topic": "A", "marks": 1}]}
    ]
    report = ExamEvolutionService.analyze_evolution(1, exams)
    assert report.total_papers_analyzed == 4
    trend_A = next((t for t in report.topic_trends if t.name == "A"), None)
    assert trend_A.classification == TrendClassification.STABLE
