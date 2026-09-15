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
        r"^(Definition|Algorithm|Formula|Concept|Equation|Nota(?:tion|te))\s*:?\s*(.+)$", re.IGNORECASE
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

                concept_name = None
                k_type = "context"
                content = line
                
                # Check for headings directly
                heading_match = re.match(r"^(?:\d+\.)+\d*\s+([A-Z][A-Za-z0-9\s\-\_]{2,40})$", line)
                unit_match = re.match(r"^(?:Unit|Chapter|Module|Section)\s+\d+[\:\-\s]+([A-Z][A-Za-z0-9\s\-\_]{2,40})$", line, re.IGNORECASE)
                
                if heading_match:
                    concept_name = heading_match.group(1).strip()
                    k_type = "topic"
                elif unit_match:
                    concept_name = unit_match.group(1).strip()
                    k_type = "topic"
                else:
                    # Check definition pattern
                    match = cls.KNOWLEDGE_PATTERN.match(line)
                    if match:
                        k_type = match.group(1).lower()
                        content = match.group(2).strip()
                        
                        def_match = re.match(r"^(?:Definition|Concept|Algorithm)\s+of\s+([A-Za-z0-9\s\-\_]{2,40})\s*\:?", content, re.IGNORECASE)
                        g_match = re.match(r"^([A-Z][a-zA-Z0-9\s\-\_]{2,40})\s*\:\s*[A-Z]", content)
                        
                        if def_match:
                            concept_name = def_match.group(1).strip()
                        elif g_match and not g_match.group(1).lower().startswith(('definition', 'example', 'note', 'solution', 'fig', 'table')):
                            concept_name = g_match.group(1).strip()
                
                if not concept_name and k_type == "context":
                    # Neither a heading nor a definition, skip entirely to avoid spamming StudyEvidence
                    continue
                    
                if not concept_name:
                    concept_name = "Unknown Concept"
                    
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
