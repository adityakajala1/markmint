import re
from typing import Any

from backend.schemas import (
    KnowledgeExtractionResult,
    ExtractedConcept,
)

class KnowledgeExtractor:
    """Simple regex/heuristic based knowledge extractor for study materials."""

    # Matches "Definition: <text>", "Algorithm: <text>", etc.
    KNOWLEDGE_PATTERN = re.compile(
        r"^(Definition|Algorithm|Formula|Concept)\s*:\s*(.+)$", re.IGNORECASE
    )

    @classmethod
    def extract(cls, pages_data: list[dict[str, Any]]) -> KnowledgeExtractionResult:
        concepts = []

        for page_info in pages_data:
            page_num = int(page_info["page_number"])
            text = str(page_info["text"])

            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                match = cls.KNOWLEDGE_PATTERN.match(line)
                if match:
                    k_type = match.group(1).lower()
                    content = match.group(2).strip()
                    
                    # Try to infer concept name from content
                    words = content.split()
                    concept_name = " ".join(words[:3]) if words else "Unknown Concept"
                    
                    concepts.append(
                        ExtractedConcept(
                            concept_name=concept_name,
                            knowledge_type=k_type,
                            content=content,
                            original_text=line,
                            page_number=page_num,
                            confidence=0.8
                        )
                    )

        return KnowledgeExtractionResult(
            concepts=concepts,
            total_pages=len(pages_data),
            successful=True
        )
