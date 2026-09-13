import pytest
import sys, importlib.util, types
# Direct module load without package init to avoid playwright dependency
spec = importlib.util.spec_from_file_location("thehelpers.classifier", r"C:\Users\ASUS\Desktop\system\thehelpers\classifier.py")
class_mod = importlib.util.module_from_spec(spec)
sys.modules["thehelpers"] = types.ModuleType("thehelpers")
sys.modules["thehelpers.classifier"] = class_mod
spec.loader.exec_module(class_mod)
ResourceClassifier = class_mod.ResourceClassifier
ResourceType = class_mod.ResourceType
ExamType = class_mod.ExamType

@pytest.fixture
def classifier():
    return ResourceClassifier()

@pytest.mark.parametrize("title, expected_type, expected_year, expected_exam_type, min_confidence", [
    ("PYQ Nov 2024", ResourceType.PYQ, 2024, None, 0.8),
    ("CT Papers 2025", ResourceType.CT_PAPER, 2025, ExamType.CT, 0.8),
    ("Semester Exam May 2023", ResourceType.SEMESTER_PAPER, 2023, ExamType.SEMESTER, 0.7),
    ("Syllabus", ResourceType.SYLLABUS, None, None, 0.7),
    ("Question Bank", ResourceType.QUESTION_BANK, None, None, 0.7),
    ("Unit 1 Notes", ResourceType.NOTES, None, None, 0.6),
    ("Important Topics", ResourceType.IMPORTANT_QUESTIONS, None, None, 0.6),
    ("Answer Key 2024", ResourceType.ANSWER_KEY, 2024, None, 0.7),
    ("Best Books", ResourceType.OTHER, None, None, 0.0),
    ("PYQ Master PDF", ResourceType.PYQ, None, None, 0.7),
])
def test_resource_classification(classifier, title, expected_type, expected_year, expected_exam_type, min_confidence):
    """Test basic classification of different resource types."""
    rtype, year, exam, conf = classifier.classify(title)
    assert rtype == expected_type
    assert year == expected_year
    # Only assert exam type if it's expected; otherwise check if it's consistent with expectations
    if expected_exam_type:
        assert exam == expected_exam_type
    assert conf >= min_confidence

@pytest.mark.parametrize("title, expected_year", [
    ("PYQ 2025", 2025),
    ("Nov 2024", 2024),
    ("May 2023", 2023),
    ("Jul 2023", 2023),
    ("No year here", None),
    ("Year 2019", None), # Out of range (2020-2026)
    ("Future 2030", None), # Out of range
])
def test_year_extraction(classifier, title, expected_year):
    """Test year extraction and range validation."""
    _, year, _, _ = classifier.classify(title)
    assert year == expected_year

@pytest.mark.parametrize("title, expected_exam_type", [
    ("PYQ Semester Exam", ExamType.SEMESTER),
    ("CT 1 Paper", ExamType.CT),
    ("Quiz 2 MCQ", ExamType.QUIZ),
    ("General Notes", None),
])
def test_exam_type_inference(classifier, title, expected_exam_type):
    """Test inference of exam type from title keywords."""
    _, _, exam, _ = classifier.classify(title)
    assert exam == expected_exam_type

@pytest.mark.parametrize("title, expected_conf_range", [
    ("PYQ Nov 2024", (0.8, 1.0)), # Clear match + year
    ("Syllabus", (0.7, 1.0)),     # Single strong pattern
    ("Something Random", (0.0, 0.5)), # Ambiguous/Other
])
def test_confidence_scoring(classifier, title, expected_conf_range):
    """Test that confidence scores fall within expected ranges."""
    _, _, _, conf = classifier.classify(title)
    assert expected_conf_range[0] <= conf <= expected_conf_range[1]

@pytest.mark.parametrize("title, expected_type, expected_year, expected_exam_type", [
    ("pyq nov 2024", ResourceType.PYQ, 2024, None),
    ("PYQ NOV 2024", ResourceType.PYQ, 2024, None),
    ("PYQ Master PDF", ResourceType.PYQ, None, None),
    ("CT PAPERS 2025", ResourceType.CT_PAPER, 2025, ExamType.CT),
    ("  pyq 2023  ", ResourceType.PYQ, 2023, None),
])
def test_edge_cases(classifier, title, expected_type, expected_year, expected_exam_type):
    """Test case insensitivity, spacing, and formatting."""
    rtype, year, exam, _ = classifier.classify(title)
    assert rtype == expected_type
    assert year == expected_year
    assert exam == expected_exam_type

def test_empty_title(classifier):
    """Test behavior with empty or whitespace titles."""
    rtype, year, exam, conf = classifier.classify("")
    assert rtype == ResourceType.OTHER
    assert year is None
    assert exam is None
    assert conf < 0.2

    rtype, year, exam, conf = classifier.classify("   ")
    assert rtype == ResourceType.OTHER
    assert year is None
    assert exam is None
    assert conf < 0.2
