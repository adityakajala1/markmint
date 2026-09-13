import pytest
from app.services.dna.analyzer import DNAAnalyzerService

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
                    "year": 2022
                }
            ]
        }
    ]
    
    dna = DNAAnalyzerService.analyze(exams)
    
    assert dna.total_exams_analyzed == 2
    assert dna.total_questions_analyzed == 4
    assert dna.total_marks_analyzed == 35.0
    
    # Check Topic Distribution (Graphs: 2, Trees: 1, Sorting: 1)
    graphs_dist = next(d for d in dna.topic_distribution if d.key == "Graphs")
    assert graphs_dist.count == 2
    assert graphs_dist.percentage_of_total == 0.5  # 2/4
    assert graphs_dist.marks_weighting == 10.0 / 35.0
    
    # Check Difficulty
    # Average difficulty = (0.5 + 0.8 + 0.5 + 0.7) / 4 = 2.5 / 4 = 0.625
    assert dna.average_difficulty.value == 0.625
    assert dna.average_difficulty.sample_size == 4
    assert dna.average_difficulty.denominator == 4
    
    # Check Repetition Rates
    assert dna.exact_repetition_rate.value == 0.25 # 1/4 (q3)
    assert dna.exact_repetition_rate.sample_size == 1
    assert dna.exact_repetition_rate.supporting_question_ids == ["q3"]
    
    assert dna.conceptual_repetition_rate.value == 0.25 # 1/4 (q4)
    
    # Check Temporal Trends
    trends = dna.temporal_trends
    assert "topic_Graphs_frequency" in trends
    # In 2021, Graphs was 1 out of 2 questions (0.5)
    # In 2022, Graphs was 1 out of 2 questions (0.5)
    graph_trend = trends["topic_Graphs_frequency"]
    assert len(graph_trend) == 2
    assert graph_trend[0]["year"] == 2021
    assert graph_trend[0]["frequency"] == 0.5
    assert graph_trend[1]["year"] == 2022
    assert graph_trend[1]["frequency"] == 0.5
