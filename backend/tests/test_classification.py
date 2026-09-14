import pytest
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
