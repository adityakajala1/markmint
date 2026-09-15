import pytest
from backend.services.dna.analyzer import DNAAnalyzerService

def test_dna_analysis_with_controlled_dataset() -> None:
    # Controlled dataset: 2 exams, 4 questions total
    exams = [
        {
            "id": "e1",
            "year": 2021,
            "questions": [
                {
                    "id": "q1",
                    "marks": 5.0,
                    "topic": "Graphs",
                    "unit": "Unit 1",
                    "question_type": "explanation",
                    "cognitive_level": "understand",
                    "difficulty": 0.5,
                    "repetition_type": None,
                    "is_alternative": False,
                    "year": 2021
                },
                {
                    "id": "q2",
                    "marks": 15.0,
                    "topic": "Trees",
                    "unit": "Unit 2",
                    "question_type": "implementation",
                    "cognitive_level": "apply",
                    "difficulty": 0.8,
                    "repetition_type": None,
                    "is_alternative": False,
                    "year": 2021
                }
            ]
        },
        {
            "id": "e2",
            "year": 2022,
            "questions": [
                {
                    "id": "q3",
                    "marks": 5.0,
                    "topic": "Graphs",
                    "unit": "Unit 1",
                    "question_type": "explanation",
                    "cognitive_level": "understand",
                    "difficulty": 0.5,
                    "repetition_type": "exact",
                    "is_alternative": False,
                    "year": 2022
                },
                {
                    "id": "q4",
                    "marks": 10.0,
                    "topic": "Sorting",
                    "unit": "Unit 3",
                    "question_type": "comparison",
                    "cognitive_level": "analyze",
                    "difficulty": 0.7,
                    "repetition_type": "conceptual",
                    "is_alternative": False,
                    "year": 2022
                }
            ]
        }
    ]
    
    dna = DNAAnalyzerService.analyze(exams)
    
    assert dna.sample_size.papers == 2
    assert dna.sample_size.questions == 4
    
    # Check Topic Distribution (Graphs: 2, Trees: 1, Sorting: 1)
    graphs_dist = next(d for d in dna.topics if d.topic == "Graphs")
    assert graphs_dist.question_count == 2
    assert graphs_dist.total_marks == 10.0
    
    trees_dist = next(d for d in dna.topics if d.topic == "Trees")
    assert trees_dist.question_count == 1
    assert trees_dist.total_marks == 15.0
    
    # Repetition
    assert dna.repetition.exact_count == 1
    assert dna.repetition.conceptual_count == 1
