import pytest
from backend.services.dna.analyzer import DNAAnalyzerService
from backend.schemas import DataSufficiency

def test_data_sufficiency_insufficient():
    # 1 paper, 11 questions -> INSUFFICIENT (needs >1 paper)
    exams = [{"year": 2023, "questions": [{"marks": 5} for _ in range(11)]}]
    dna = DNAAnalyzerService.analyze(exams)
    assert dna.sample_size.sufficiency == DataSufficiency.INSUFFICIENT
    
    # 2 papers, 9 questions -> INSUFFICIENT (needs >=10 questions)
    exams = [
        {"year": 2022, "questions": [{"marks": 5} for _ in range(5)]},
        {"year": 2023, "questions": [{"marks": 5} for _ in range(4)]}
    ]
    dna = DNAAnalyzerService.analyze(exams)
    assert dna.sample_size.sufficiency == DataSufficiency.INSUFFICIENT

def test_data_sufficiency_moderate():
    # 5 papers, 50 questions -> MODERATE
    exams = [
        {"year": 2020 + i, "questions": [{"marks": 5} for _ in range(10)]}
        for i in range(5)
    ]
    dna = DNAAnalyzerService.analyze(exams)
    assert dna.sample_size.sufficiency == DataSufficiency.MODERATE

def test_topic_paper_coverage():
    # 5 papers total. "Graphs" appears in 3 of them.
    exams = [
        {"id": 1, "year": 2018, "questions": [{"topic": "Graphs", "marks": 5}]},
        {"id": 2, "year": 2019, "questions": [{"topic": "Trees", "marks": 5}]},
        {"id": 3, "year": 2020, "questions": [{"topic": "Graphs", "marks": 5}]},
        {"id": 4, "year": 2021, "questions": [{"topic": "Graphs", "marks": 5}]},
        {"id": 5, "year": 2022, "questions": [{"topic": "Hashing", "marks": 5}]},
    ]
    
    dna = DNAAnalyzerService.analyze(exams)
    graph_dna = next(t for t in dna.topics if t.topic == "Graphs")
    
    assert graph_dna.paper_coverage == 0.6 # 3 / 5

def test_recurrence_interval():
    # Family appears in 2018, 2020, 2022. Intervals: 2020-2018=2, 2022-2020=2. Avg=2.0
    exams = [
        {"id": 1, "year": 2018, "questions": [{"family_name": "DFS_Traversal", "marks": 5}]},
        {"id": 2, "year": 2020, "questions": [{"family_name": "DFS_Traversal", "marks": 5}]},
        {"id": 3, "year": 2022, "questions": [{"family_name": "DFS_Traversal", "marks": 5}]},
    ]
    
    dna = DNAAnalyzerService.analyze(exams)
    fam_dna = next(f for f in dna.families if f.family_name == "DFS_Traversal")
    
    assert fam_dna.recurrence_interval_years == 2.0

def test_repetition_distinction():
    exams = [{"id": 1, "year": 2023, "questions": [
        {"repetition_type": "exact"},
        {"repetition_type": "near"},
        {"repetition_type": "near"},
        {"repetition_type": "conceptual"},
        {"repetition_type": "structural"},
        {"repetition_type": "structural"},
        {"repetition_type": "structural"}
    ]}]
    
    dna = DNAAnalyzerService.analyze(exams)
    assert dna.repetition.exact_count == 1
    assert dna.repetition.near_count == 2
    assert dna.repetition.conceptual_count == 1
    assert dna.repetition.structural_count == 3
