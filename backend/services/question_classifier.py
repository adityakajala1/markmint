import abc
import re
import unicodedata
from typing import Optional

from backend.schemas import ClassificationResult

class BaseClassificationProvider(abc.ABC):
    
    @abc.abstractmethod
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        pass
        
    @abc.abstractmethod
    def get_semantic_classification(self, text: str, categories: list[str]) -> tuple[str | None, float]:
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

    def get_semantic_classification(self, text: str, categories: list[str]) -> tuple[str | None, float]:
        if not categories:
            return None, 0.0
            
        text_emb = np.array(self.get_embeddings([text]))
        cat_embs = np.array(self.get_embeddings(categories))
        
        # Compute cosine similarity manually using numpy
        dot = np.dot(text_emb, cat_embs.T)[0]
        norm_t = np.linalg.norm(text_emb, axis=1)[0]
        norm_c = np.linalg.norm(cat_embs, axis=1)
        similarities = dot / (norm_t * norm_c)
        
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])
        
        # Threshold: if score is too low, it's not a confident match.
        if best_score < 0.45:
            return None, best_score

        return categories[best_idx], best_score

from typing import Optional
from backend.schemas import ClassificationResult

class ClassificationService:
    CLASSIFIER_VERSION = "course-scoped-semantic-v1"
    SIMILARITY_THRESHOLD = 0.45

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
        
        # Semantic mapping to syllabus topics. The canonical representation is
        # supplied by the caller and is intentionally not normalized here.
        topic, conf = self.provider.get_semantic_classification(question_text, available_topics)

        guardrail_reason = self._domain_guardrail_reason(question_text, topic)
        if guardrail_reason:
            topic = None

        return ClassificationResult(
            question_type=q_type,
            cognitive_level=cog_level,
            difficulty=difficulty,
            topics=[topic] if topic else [],
            confidence=conf,
            guardrail_reason=guardrail_reason,
        )

    @classmethod
    def _domain_guardrail_reason(
        cls, question_text: str, candidate_topic: Optional[str]
    ) -> Optional[str]:
        """Reject known cross-domain collisions while preserving unresolved results."""
        if not candidate_topic:
            return None

        question = cls._domain_text(question_text)
        topic = cls._domain_text(candidate_topic)

        if cls._topic_matches(topic, ("ionization energy", "ionisation energy")):
            if cls._contains_any(
                question,
                (
                    "polarizability",
                    "polarising power",
                    "polarizing power",
                    "fajan rule",
                    "fajan s rule",
                    "fajans rule",
                ),
            ):
                return "polarization-domain content is not ionization energy"
            if cls._contains_any(
                question,
                (
                    "photoelectron",
                    "photo electron",
                    "photoelectric",
                    "photo electric",
                    "photo emission",
                    "photoemission",
                    "photoelectron spectroscopy",
                    "xps",
                    "impinging photon",
                ),
            ):
                return "photoelectron/photoelectric content is not ionization energy"

        if cls._topic_matches(topic, ("photoelectron spectroscopy",)):
            if not cls._contains_any(question, ("photoelectron", "photo electron", "xps")):
                return "electronic/other spectroscopy content is not photoelectron spectroscopy"

        if cls._topic_matches(topic, ("hydrogen atomic orbitals",)):
            if cls._contains_any(
                question,
                (
                    "molecular orbital",
                    "lcao",
                    "linear combination of atomic orbitals",
                    "bond order",
                    "bonding and antibonding",
                    "overlap of",
                    "overlapping of",
                ),
            ):
                return "molecular-orbital content is not hydrogen atomic orbitals"

        if cls._topic_matches(topic, ("molecular orbital theory",)):
            if cls._contains_any(
                question,
                (
                    "crystal field",
                    "ligand field",
                    "cfse",
                    "high spin",
                    "low spin",
                    "d orbital splitting",
                    "spectrochemical series",
                    "uncertainty principle",
                    "de broglie",
                    "spin quantum number",
                ),
            ):
                return "quantum/coordination content is not molecular orbital theory"

        if cls._topic_matches(topic, ("spectroscopy fundamentals",)):
            if cls._contains_any(
                question,
                (
                    "spectrochemical series",
                    "crystal field",
                    "ligand field",
                    "nmr",
                    "nuclear magnetic resonance",
                    "chemical shift",
                    "spin spin",
                    "shielding",
                    "uv vis",
                    "uv visible",
                ),
            ):
                return "specific spectroscopy/coordination content is not spectroscopy fundamentals"

        if cls._topic_matches(topic, ("crystal field theory",)):
            if not cls._contains_any(
                question,
                (
                    "crystal field",
                    "ligand field",
                    "cfse",
                    "high spin",
                    "low spin",
                    "d orbital",
                    "spectrochemical series",
                ),
            ):
                return "non-coordination content is not crystal field theory"

        if cls._topic_matches(topic, ("coordination isomerism",)):
            if not cls._contains_any(
                question,
                ("coordination", "transition metal", "complex", "metal ion"),
            ):
                return "general organic isomerism is not coordination isomerism"

        if cls._topic_matches(topic, ("organic reagents and reaction types",)):
            if cls._contains_any(question, ("oxidation", "oxidized", "reduction", "reducing")):
                return "redox content is not general organic reagent types"

        if cls._topic_matches(topic, ("atomic radius", "atomic radii")) and cls._contains_any(
            question,
            (
                "radial wave function",
                "radial wavefunction",
                "wave function",
                "wavefunction",
                "schrodinger",
                "schrödinger",
            ),
        ):
            return "quantum wavefunction content is not atomic radius"

        return None

    @staticmethod
    def _domain_text(value: str) -> str:
        ascii_value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        return re.sub(r"[^a-z0-9]+", " ", ascii_value.lower()).strip()

    @staticmethod
    def _contains_any(value: str, phrases: tuple[str, ...]) -> bool:
        return any(phrase in value for phrase in phrases)

    @staticmethod
    def _topic_matches(topic: str, aliases: tuple[str, ...]) -> bool:
        return any(alias in topic for alias in aliases)

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
