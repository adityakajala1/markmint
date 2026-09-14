import abc

class BaseClassificationProvider(abc.ABC):
    
    @abc.abstractmethod
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        pass
        
    @abc.abstractmethod
    def get_semantic_classification(self, text: str, categories: list[str]) -> tuple[str, float]:
        pass

import numpy as np
from typing import Any



class LocalTransformerProvider(BaseClassificationProvider):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts)
        if isinstance(embeddings, np.ndarray):
            return embeddings.tolist()  # type: ignore
        return [list(map(float, e)) for e in embeddings]

    def get_semantic_classification(self, text: str, categories: list[str]) -> tuple[str, float]:
        if not categories:
            return "", 0.0
            
        text_emb = np.array(self.get_embeddings([text]))
        cat_embs = np.array(self.get_embeddings(categories))
        
        # Compute cosine similarity manually using numpy
        dot = np.dot(text_emb, cat_embs.T)[0]
        norm_t = np.linalg.norm(text_emb, axis=1)[0]
        norm_c = np.linalg.norm(cat_embs, axis=1)
        similarities = dot / (norm_t * norm_c)
        
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])
        
        return categories[best_idx], best_score

from typing import Optional
from backend.schemas import ClassificationResult

class ClassificationService:
    def __init__(self, provider: BaseClassificationProvider):
        self.provider = provider
        
    def classify_question(
        self, 
        question_text: str, 
        available_topics: list[str],
        marks: Optional[float] = None
    ) -> ClassificationResult:
        
        q_type = self._determine_type(question_text)
        cog_level = self._determine_cognitive_level(question_text)
        difficulty = self._estimate_difficulty(marks, cog_level)
        
        # Semantic mapping to syllabus topics
        topic, conf = self.provider.get_semantic_classification(question_text, available_topics)
        
        return ClassificationResult(
            question_type=q_type,
            cognitive_level=cog_level,
            difficulty=difficulty,
            topics=[topic] if topic else [],
            confidence=conf
        )

    def _determine_type(self, text: str) -> str:
        text_lower = text.lower()
        if "compare" in text_lower or "difference" in text_lower:
            return "comparison"
        if "implement" in text_lower or "write a program" in text_lower:
            return "implementation"
        if "prove" in text_lower or "derivation" in text_lower:
            return "proof"
        return "explanation"

    def _determine_cognitive_level(self, text: str) -> str:
        text_lower = text.lower()
        if "evaluate" in text_lower or "critique" in text_lower:
            return "evaluate"
        if "design" in text_lower or "create" in text_lower:
            return "create"
        if "analyze" in text_lower:
            return "analyze"
        if "implement" in text_lower or "apply" in text_lower:
            return "apply"
        if "explain" in text_lower or "describe" in text_lower:
            return "understand"
        return "remember"

    def _estimate_difficulty(self, marks: Optional[float], cog_level: str) -> float:
        base = 0.5
        if cog_level in ["create", "evaluate"]:
            base += 0.3
        elif cog_level in ["apply", "analyze"]:
            base += 0.2
            
        if marks and marks > 10:
            base += 0.2
            
        return min(1.0, base)
