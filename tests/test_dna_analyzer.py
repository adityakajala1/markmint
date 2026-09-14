import pytest
from backend.services.dna.analyzer import DNAAnalyzerService

def test_recent_frequency_denominator():
    synthetic_exams = [
        {
            "id": 1,
            "year": 2021,
            "exam_type": "midterm",
            "questions": [
                {"id": 1, "marks": 10.0, "is_alternative": False, "topic": "Calculus", "unit": "Unit 1", "question_type": "theoretical"},
                {"id": 2, "marks": 10.0, "is_alternative": False, "topic": "Calculus", "unit": "Unit 1", "question_type": "numerical"},
                {"id": 3, "marks": 10.0, "is_alternative": False, "topic": "Calculus", "unit": "Unit 1", "question_type": "theoretical"},
                {"id": 4, "marks": 10.0, "is_alternative": False, "topic": "Calculus", "unit": "Unit 1", "question_type": "numerical"},
            ]
        },
        {
            "id": 2,
            "year": 2023, # Recent is 2022, 2023 (max_year - 1)
            "exam_type": "final",
            "questions": [
                {"id": 5, "marks": 10.0, "is_alternative": False, "topic": "Calculus", "unit": "Unit 1", "question_type": "theoretical"},
                {"id": 6, "marks": 10.0, "is_alternative": False, "topic": "Algebra", "unit": "Unit 2", "question_type": "numerical"},
            ]
        }
    ]

    # Total questions = 6
    # Recent total questions = 2
    # Recent calculus questions = 1
    # Expected recent frequency = 1 / 2 = 0.5 (NOT 1 / 6 = 0.166)

    dna = DNAAnalyzerService.analyze(synthetic_exams)

    calculus_dna = next(t for t in dna.topics if t.topic == "Calculus")
    
    # Check that recent frequency relies on recent total questions
    assert calculus_dna.recent_frequency == 0.5, f"Expected 0.5, got {calculus_dna.recent_frequency}"

def test_alternative_marks_weighting():
    synthetic_exams = [
        {
            "id": 1,
            "year": 2023,
            "exam_type": "final",
            "questions": [
                # Normal question
                {"id": 1, "marks": 10.0, "is_alternative": False, "topic": "Algebra", "unit": "Unit 1", "question_type": "numerical"},
                # OR Alternative (same marks, different topic/unit but same exam block conceptually)
                # To maximize unit weighting distortion, we assign it to the same unit
                {"id": 2, "marks": 10.0, "is_alternative": True, "topic": "Algebra", "unit": "Unit 1", "question_type": "theoretical"},
                
                # Another question in a different unit
                {"id": 3, "marks": 10.0, "is_alternative": False, "topic": "Calculus", "unit": "Unit 2", "question_type": "numerical"},
            ]
        }
    ]

    # Total marks (excluding alternative) = 10 (id1) + 10 (id3) = 20
    # Unit 1 total marks (excluding alternative) = 10
    # Expected Unit 1 Weighting = 10 / 20 = 0.5 (50%)
    
    # If the bug were active, Unit 1 marks would be 20, making Unit 1 Weighting 20 / 20 = 1.0 (100%),
    # but Calculus is also 10 / 20 = 0.5, meaning total weighting across units = 150%!

    dna = DNAAnalyzerService.analyze(synthetic_exams)

    unit1_dna = next(u for u in dna.units if u.unit == "Unit 1")
    unit2_dna = next(u for u in dna.units if u.unit == "Unit 2")
    
    assert unit1_dna.historical_weighting == 0.5, f"Expected 0.5, got {unit1_dna.historical_weighting}"
    assert unit2_dna.historical_weighting == 0.5, f"Expected 0.5, got {unit2_dna.historical_weighting}"
    
    # Total historical weightings should sum to 1.0 (100%)
    total_weighting = sum(u.historical_weighting for u in dna.units)
    assert total_weighting == 1.0, f"Total weightings exceed 100%: {total_weighting * 100}%"
