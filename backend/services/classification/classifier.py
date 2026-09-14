from typing import Optional
from backend.schemas.classification import ClassificationResult
from backend.services.classification.providers.base import BaseClassificationProvider

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
