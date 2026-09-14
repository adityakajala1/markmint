import pytest
from app.services.similarity import SimilarityService, SimilarityThresholds
from app.services.question_classifier import BaseClassificationProvider
import numpy as np

class MockSimProvider(BaseClassificationProvider):
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        embs = []
        for t in texts:
            if "BFS" in t or "breadth-first" in t:
                embs.append([1.0, 0.0, 0.0])
            elif "binary" in t:
                embs.append([0.0, 1.0, 0.0])
            else:
                embs.append([0.0, 0.0, 1.0])
        return embs
        
    def get_semantic_classification(self, text: str, categories: list[str]) -> tuple[str, float]:
        return "", 0.0

def test_similarity_detection() -> None:
    provider = MockSimProvider()
    service = SimilarityService(provider)
    
    questions = [
        {"id": "q1", "text": "Explain BFS."},
        {"id": "q2", "text": "Describe breadth-first search."},
        {"id": "q3", "text": "Implement BFS traversal."},
        {"id": "q4", "text": "Explain binary search."}
    ]
    
    matches = service.find_matches(questions)
    
    # q1, q2, q3 should all match each other with high score
    # q4 should not match the others
    matched_ids = [(m.question_a_id, m.question_b_id) for m in matches]
    
    assert ("q1", "q2") in matched_ids
    assert ("q1", "q3") in matched_ids
    assert ("q2", "q3") in matched_ids
    
    # Q4 should not be in any match
    for m in matches:
        assert m.question_a_id != "q4" and m.question_b_id != "q4"

def test_false_positive_guardrail() -> None:
    provider = MockSimProvider()
    service = SimilarityService(provider)
    
    # Force them to have same embedding to simulate a confused model
    provider.get_embeddings = lambda texts: [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]] # type: ignore
    
    q1 = "Explain binary search."
    q2 = "Explain breadth-first search."
    
    matches = service.find_matches([
        {"id": "1", "text": q1},
        {"id": "2", "text": q2}
    ])
    
    # Should be rejected by the heuristic guardrail
    assert len(matches) == 0
