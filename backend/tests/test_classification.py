import pytest
from backend.services.canonical import CanonicalRepresentationBuilder
from backend.services.question_classifier import ClassificationService
from backend.schemas import ClassificationResult
from backend.services.question_classifier import BaseClassificationProvider

class MockProvider(BaseClassificationProvider):
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        # Mock embeddings
        return [[0.1] * 384 for _ in texts]
        
    def get_semantic_classification(self, text: str, categories: list[str]) -> tuple[str, float]:
        if "BFS" in text:
            return "Graphs", 0.95
        return categories[0], 0.8


class FixedProvider(BaseClassificationProvider):
    def __init__(self, topic: str, score: float = 0.8) -> None:
        self.topic = topic
        self.score = score
        self.inputs: list[str] = []

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        return [[0.1] * 384 for _ in texts]

    def get_semantic_classification(
        self, text: str, categories: list[str]
    ) -> tuple[str, float]:
        self.inputs.append(text)
        return self.topic, self.score

def test_classification_service() -> None:
    provider = MockProvider()
    service = ClassificationService(provider)
    
    # Test 1: Implementation
    res1 = service.classify_question("Implement a linked list.", ["Lists", "Graphs"])
    assert res1.question_type == "implementation"
    assert res1.cognitive_level == "apply"
    
    # Test 2: Semantic mapping
    res2 = service.classify_question("Explain BFS traversal.", ["Trees", "Graphs"])
    assert res2.topics == ["Graphs"]
    assert res2.question_type == "explanation"


@pytest.mark.parametrize(
    ("question", "candidate_topic"),
    [
        (
            "Explain polarizability and polarizing power using Fajan's rule.",
            "Ionization Energy",
        ),
        (
            "The kinetic energy of the ejected photoelectron depends on the impinging photon.",
            "Ionization Energy",
        ),
        (
            "Discuss the radial wave functions of the hydrogen atom.",
            "Atomic Radius",
        ),
    ],
)
def test_domain_guardrails_leave_known_false_positives_unresolved(
    question: str, candidate_topic: str
) -> None:
    service = ClassificationService(FixedProvider(candidate_topic))

    result = service.classify_question(question, [candidate_topic])

    assert result.topics == []
    assert result.confidence == 0.8
    assert result.guardrail_reason


@pytest.mark.parametrize(
    ("question", "candidate_topic"),
    [
        (
            "Draw the molecular orbital energy level diagram for H2 and calculate bond order.",
            "Hydrogen Atomic Orbitals",
        ),
        (
            "Write the selection rule for H atom in electronic spectroscopy.",
            "Photoelectron Spectroscopy",
        ),
        (
            "What is the spectrochemical series and its importance?",
            "Spectroscopy Fundamentals",
        ),
        (
            "Explain the principle of UV-Vis spectroscopy.",
            "Spectroscopy Fundamentals",
        ),
        (
            "Write notes on structural isomerism with examples.",
            "Coordination Isomerism",
        ),
        (
            "Write a note on van der Waals interactions and Bragg's law.",
            "Crystal Field Theory",
        ),
    ],
)
def test_expanded_taxonomy_guardrails_reject_cross_domain_collisions(
    question: str, candidate_topic: str
) -> None:
    service = ClassificationService(FixedProvider(candidate_topic))

    result = service.classify_question(question, [candidate_topic])

    assert result.topics == []
    assert result.guardrail_reason


def test_canonical_stem_structure_is_passed_to_classifier() -> None:
    class DummyQuestion:
        structured_content = {
            "number": "1",
            "text": (
                r"Find the matrix A = \begin{pmatrix} x^2_1 & H_2SO_4 \\ "
                r"y_1 & z^2 \end{pmatrix} and solve E = mc^2."
            ),
        }
        original_text = "fallback"

    provider = FixedProvider("Chemistry")
    service = ClassificationService(provider)
    canonical = CanonicalRepresentationBuilder.build(DummyQuestion())

    service.classify_question(canonical, ["Chemistry"])

    classifier_input = provider.inputs[0]
    assert r"\begin{pmatrix}" in classifier_input
    assert "x^2_1" in classifier_input
    assert "E = mc^2" in classifier_input
    assert "H_2SO_4" in classifier_input
