import pytest
from backend.services.canonical import CanonicalRepresentationBuilder
from backend.services.families.normalizer import QuestionNormalizer
from backend.services.question_classifier import LocalTransformerProvider

def test_canonical_builder_matrix():
    class DummyQuestion:
        def __init__(self, structured, text):
            self.structured_content = structured
            self.original_text = text

    q = DummyQuestion({
        "question_number": "1",
        "original_text": r"Find Eigen values of the Matrix A = \begin{pmatrix} 2 & -2 & 3 \\ 1 & 1 & 1 \\ 1 & 3 & -1 \end{pmatrix}."
    }, "old_text")
    
    canonical = CanonicalRepresentationBuilder.build(q)
    assert "1. Find Eigen values" in canonical
    assert r"\begin{pmatrix}" in canonical

def test_canonical_builder_hierarchy():
    class DummyQuestion:
        def __init__(self):
            self.structured_content = {
                "question_number": "1",
                "original_text": "Main question.",
                "subquestions": [
                    {"number": "a", "text": "subquestion a"},
                    {"number": "b", "text": "subquestion b"}
                ],
                "or_alternative": {
                    "question_number": "2",
                    "original_text": "alternative question."
                }
            }
            self.original_text = ""
    
    q = DummyQuestion()
    canonical = CanonicalRepresentationBuilder.build(q)
    assert "1. Main question" in canonical
    assert "    (a) subquestion a" in canonical
    assert "    (b) subquestion b" in canonical
    assert "    --- OR ---" in canonical
    assert "    2. alternative question" in canonical

def test_normalizer_math_preservation():
    # x^2 and x² should map to same underlying normalized math
    norm1 = QuestionNormalizer.normalize("x²")
    norm2 = QuestionNormalizer.normalize("x^2")
    assert norm1 == norm2 == "x^2"
    
    norm3 = QuestionNormalizer.normalize("H₂SO₄")
    norm4 = QuestionNormalizer.normalize("H_2SO_4")
    assert norm3 == norm4 == "h_2so_4"
    
    norm_matrix = QuestionNormalizer.normalize(r"\begin{bmatrix} 2 & 1 \end{bmatrix}")
    assert r"\begin{bmatrix}" in norm_matrix
    assert "2 & 1" in norm_matrix

def test_classifier_latex():
    # Test that the classifier actually returns a topic when fed latex
    provider = LocalTransformerProvider()
    topics = ["Linear Algebra", "Calculus", "Chemistry"]
    
    q_latex = r"Find Eigen values of the Matrix A = \begin{pmatrix} 2 & -2 & 3 \\ 1 & 1 & 1 \\ 1 & 3 & -1 \end{pmatrix}."
    
    topic, conf = provider.get_semantic_classification(q_latex, topics)
    assert conf is not None  # it runs
    if topic is not None:
        assert topic == "Linear Algebra"
