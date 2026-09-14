import re
from typing import Any, Optional

from backend.schemas import (
    DocumentExtractionResult,
    ExtractedQuestion,
    ExtractedSection,
)


class QuestionExtractor:
    """Deterministic regex-based question extractor."""

    # Matches "1.", "1)", "Q1", "Q. 1", "Question 1"
    Q_NUM_PATTERN = re.compile(
        r"^(?:Q(?:uestion)?\.?\s*)?(\d+[a-z]?)[.)\]]\s+", re.IGNORECASE
    )

    # Matches "[5]", "(5 marks)", "[5 marks]"
    MARKS_PATTERN = re.compile(
        r"[\[(]\s*(\d+(?:\.\d+)?)\s*(?:marks?)?\s*[\])]", re.IGNORECASE
    )

    # Matches "SECTION A", "PART 1"
    SECTION_PATTERN = re.compile(r"^(?:SECTION|PART)\s+([A-Z0-9]+)(.*)$", re.IGNORECASE)

    @classmethod
    def extract(
        cls, pages_data: list[dict[str, Any]]
    ) -> DocumentExtractionResult:
        sections: list[ExtractedSection] = []

        current_section = ExtractedSection(name="Default", questions=[])
        sections.append(current_section)

        current_question: Optional[dict[str, Any]] = None

        for page_info in pages_data:
            page_num = int(page_info["page_number"])
            text = str(page_info["text"])

            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Check for section boundary
                sec_match = cls.SECTION_PATTERN.match(line)
                if sec_match:
                    # Save pending question if exists
                    cls._finalize_question(current_question, current_section)
                    current_question = None

                    sec_name = f"Section {sec_match.group(1).strip()}"
                    sec_instructions = sec_match.group(2).strip() or None

                    current_section = ExtractedSection(
                        name=sec_name, instructions=sec_instructions, questions=[]
                    )
                    sections.append(current_section)
                    continue

                # Check for question boundary
                q_match = cls.Q_NUM_PATTERN.match(line)
                if q_match:
                    cls._finalize_question(current_question, current_section)

                    q_num = q_match.group(1)
                    q_text = line[q_match.end() :].strip()

                    marks_match = cls.MARKS_PATTERN.search(q_text)
                    marks = None
                    if marks_match:
                        marks = float(marks_match.group(1))
                        # Remove marks from the question text itself to clean it
                        q_text = (
                            q_text[: marks_match.start()] + q_text[marks_match.end() :]
                        )
                        q_text = q_text.strip()

                    current_question = {
                        "question_number": q_num,
                        "text": [q_text],
                        "marks": marks,
                        "page": page_num,
                    }
                elif current_question:
                    # Continuation of current question
                    marks_match = cls.MARKS_PATTERN.search(line)
                    if marks_match and current_question["marks"] is None:
                        current_question["marks"] = float(marks_match.group(1))
                        line = line[: marks_match.start()] + line[marks_match.end() :]
                        line = line.strip()
                    if line:
                        current_question["text"].append(line)

        # Finalize last question
        cls._finalize_question(current_question, current_section)

        # Remove empty default section if another section was found
        if len(sections) > 1 and not sections[0].questions:
            sections = sections[1:]

        return DocumentExtractionResult(
            sections=sections, total_pages=len(pages_data), successful=True
        )

    @staticmethod
    def _finalize_question(
        q_data: Optional[dict[str, Any]], section: ExtractedSection
    ) -> None:
        if not q_data:
            return

        text = " ".join(q_data["text"]).strip()
        if text:
            # Deterministic parsing implies high confidence if we matched the regex
            confidence = 0.95 if q_data["marks"] is not None else 0.85

            section.questions.append(
                ExtractedQuestion(
                    question_number=q_data["question_number"],
                    original_text=text,
                    marks=q_data["marks"],
                    page_number=q_data["page"],
                    confidence=confidence,
                )
            )
