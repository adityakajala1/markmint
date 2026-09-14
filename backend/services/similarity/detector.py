import numpy as np
from pydantic import BaseModel
from typing import Optional
from backend.services.classification.providers.base import BaseClassificationProvider

class SimilarityThresholds(BaseModel):
    exact: float = 0.95
    conceptual: float = 0.80
    structural: float = 0.70

class SimilarityMatch(BaseModel):
    question_a_id: str
    question_b_id: str
    score: float
    repetition_type: str

class SimilarityService:
    def __init__(self, provider: BaseClassificationProvider, thresholds: Optional[SimilarityThresholds] = None):
        self.provider = provider
        self.thresholds = thresholds or SimilarityThresholds()

    def find_matches(self, questions: list[dict[str, str]]) -> list[SimilarityMatch]:
        """
        questions: list of dicts with 'id' and 'text'.
        Returns a list of SimilarityMatch indicating relationships.
        """
        if len(questions) < 2:
            return []

        texts = [q["text"] for q in questions]
        ids = [q["id"] for q in questions]
        
        embs = np.array(self.provider.get_embeddings(texts))
        
        # Compute pairwise cosine similarity
        dot = np.dot(embs, embs.T)
        norms = np.linalg.norm(embs, axis=1)
        sim_matrix = dot / np.outer(norms, norms)

        
        matches = []
        n = len(questions)
        for i in range(n):
            for j in range(i + 1, n):
                score = float(sim_matrix[i][j])
                rep_type = self._determine_repetition_type(score)
                
                # Check for negative strict conceptual checks
                # Example: "binary search" vs "breadth-first search"
                # If they share keyword "search" but conceptually different, score might be high
                # We can enforce negative keyword checks or rely on embeddings.
                # MiniLM handles semantic differences well, but let's implement a heuristic guardrail
                if rep_type:
                    # Guardrail: If they share the exact same root words but differ in key modifiers
                    if self._is_false_positive(texts[i], texts[j]):
                        continue
                        
                    matches.append(
                        SimilarityMatch(
                            question_a_id=ids[i],
                            question_b_id=ids[j],
                            score=score,
                            repetition_type=rep_type
                        )
                    )
        return matches

    def _determine_repetition_type(self, score: float) -> Optional[str]:
        if score >= self.thresholds.exact:
            return "exact"
        if score >= self.thresholds.conceptual:
            return "conceptual"
        if score >= self.thresholds.structural:
            return "structural"
        return None

    def _is_false_positive(self, text_a: str, text_b: str) -> bool:
        """
        Heuristic to catch false positives like 'Explain binary search' vs 'Explain breadth-first search'
        If 'binary' is in A and 'breadth-first' in B, and they are short, they are likely distinct concepts.
        """
        a_lower = text_a.lower()
        b_lower = text_b.lower()
        
        # Specific guard for known opposites or distinct algorithms
        distinct_pairs = [
            ("binary", "breadth-first"),
            ("binary", "depth-first"),
            ("bfs", "dfs"),
            ("stack", "queue")
        ]
        
        for p1, p2 in distinct_pairs:
            if (p1 in a_lower and p2 in b_lower) or (p2 in a_lower and p1 in b_lower):
                return True
                
        return False
