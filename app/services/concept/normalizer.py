from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.core import Concept, ConceptAlias, MappingConfidence, ConceptStatus


class ConceptNormalizer:
    def __init__(self, db: Session):
        self.db = db

    def _normalize_string(self, text: str) -> str:
        return text.lower().strip()

    def resolve_concept(
        self, 
        alias_text: str, 
        context: str = "", 
        subject: Optional[str] = None
    ) -> tuple[Concept, MappingConfidence]:
        """
        Resolves a string alias to a canonical Concept.
        If a definitive match is found, returns the Concept and HIGH/MEDIUM confidence.
        If uncertain, creates an UNRESOLVED provisional concept.
        """
        normalized_alias = self._normalize_string(alias_text)

        # 1. Exact Alias Match
        alias_match = (
            self.db.query(ConceptAlias)
            .filter(func.lower(ConceptAlias.alias) == normalized_alias)
            .first()
        )

        if alias_match and alias_match.concept_id:
            concept = self.db.query(Concept).filter(Concept.id == alias_match.concept_id).first()
            if concept and (subject is None or concept.subject == subject):
                return concept, MappingConfidence.HIGH

        # 2. Heuristic Contextual Search (Stub for Semantic/LLM Engine)
        # Prevent blind substring matching (e.g., "Bank" in CS vs Finance).
        # We only match canonical name if subject aligns and word is significant.
        canonical_match = (
            self.db.query(Concept)
            .filter(func.lower(Concept.canonical_name) == normalized_alias)
            .first()
        )
        
        if canonical_match:
            if subject and canonical_match.subject and canonical_match.subject != subject:
                # Same word, different subject. DO NOT MERGE.
                pass
            else:
                # Good match, register the exact alias
                new_alias = ConceptAlias(
                    concept_id=canonical_match.id,
                    alias=alias_text, # Keep original casing
                    confidence=MappingConfidence.HIGH
                )
                self.db.add(new_alias)
                self.db.commit()
                return canonical_match, MappingConfidence.HIGH

        # 3. Fallback: Provisional Concept (UNRESOLVED)
        # If the string is totally new, we create an unresolved concept.
        # This prevents polluting the graph while allowing evidence to accumulate.
        provisional = Concept(
            canonical_name=alias_text,
            subject=subject,
            description=f"Auto-extracted from context: {context[:100]}...",
            status=ConceptStatus.UNRESOLVED
        )
        self.db.add(provisional)
        self.db.commit()
        self.db.refresh(provisional)

        new_alias = ConceptAlias(
            concept_id=provisional.id,
            alias=alias_text,
            confidence=MappingConfidence.UNRESOLVED
        )
        self.db.add(new_alias)
        self.db.commit()

        return provisional, MappingConfidence.UNRESOLVED

