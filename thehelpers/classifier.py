"""
Resource classifier for The Helper scraper.
Classifies resources by type, year, and exam type with confidence scoring.
"""

import re
from typing import Optional, Tuple
from enum import Enum


class ResourceType(Enum):
    """Types of academic resources."""
    PYQ = "pyq"
    CT_PAPER = "ct_paper"
    SEMESTER_PAPER = "semester_paper"
    SYLLABUS = "syllabus"
    QUESTION_BANK = "question_bank"
    NOTES = "notes"
    IMPORTANT_QUESTIONS = "important_questions"
    ANSWER_KEY = "answer_key"
    OTHER = "other"


class ExamType(Enum):
    """Types of exams."""
    SEMESTER = "semester"
    CT = "ct"
    QUIZ = "quiz"


class ResourceClassifier:
    """
    Classifies academic resources based on title patterns.

    Examples:
        >>> classifier = ResourceClassifier()
        >>> rtype, year, exam, conf = classifier.classify("PYQ Nov 2024")
        >>> rtype == ResourceType.PYQ
        True
        >>> year
        2024
        >>> exam is None  # PYQ alone doesn't imply exam type
        True
        >>> conf > 0.8
        True

        >>> rtype, year, exam, conf = classifier.classify("CT Papers 2025")
        >>> rtype == ResourceType.CT_PAPER
        True
        >>> year
        2025
        >>> exam == ExamType.CT
        True

        >>> rtype, year, exam, conf = classifier.classify("Question Bank")
        >>> rtype == ResourceType.QUESTION_BANK
        True
        >>> year is None
        True
        >>> exam is None
        True

        >>> rtype, year, exam, conf = classifier.classify("Unit 1 Notes")
        >>> rtype == ResourceType.NOTES
        True

        >>> rtype, year, exam, conf = classifier.classify("Syllabus 2024")
        >>> rtype == ResourceType.SYLLABUS
        True
        >>> year
        2024

        >>> rtype, year, exam, conf = classifier.classify("Important Questions")
        >>> rtype == ResourceType.IMPORTANT_QUESTIONS
        True

        >>> rtype, year, exam, conf = classifier.classify("Answer Key May 2023")
        >>> rtype == ResourceType.ANSWER_KEY
        True
        >>> year
        2023

        >>> rtype, year, exam, conf = classifier.classify("Best Books")
        >>> rtype == ResourceType.OTHER
        True

        >>> rtype, year, exam, conf = classifier.classify("PYQ Master PDF")
        >>> rtype == ResourceType.PYQ
        True
        >>> conf > 0.7
        True
    """

    def __init__(self):
        """Initialize classifier with pattern definitions."""
        # Resource type patterns (pattern, resource_type, weight)
        self.resource_patterns = [
            # PYQ patterns
            (r'\bpyq\b', ResourceType.PYQ, 1.0),
            (r'\bprevious\s+year\b', ResourceType.PYQ, 0.9),
            (r'\bprev\s+year\b', ResourceType.PYQ, 0.9),
            (r'\bpast\s+year\b', ResourceType.PYQ, 0.9),
            (r'\bold\s+question\b', ResourceType.PYQ, 0.8),

            # CT Paper patterns
            (r'\bct\b', ResourceType.CT_PAPER, 1.0),
            (r'\bclass\s+test\b', ResourceType.CT_PAPER, 1.0),
            (r'\bclasstest\b', ResourceType.CT_PAPER, 1.0),
            (r'\bct\s*\d+\b', ResourceType.CT_PAPER, 1.0),

            # Semester paper patterns
            (r'\bsemester\b', ResourceType.SEMESTER_PAPER, 0.9),
            (r'\bend\s+sem\b', ResourceType.SEMESTER_PAPER, 1.0),
            (r'\bendsem\b', ResourceType.SEMESTER_PAPER, 1.0),
            (r'\bsem\s+exam\b', ResourceType.SEMESTER_PAPER, 0.9),
            (r'\bmidsem\b', ResourceType.SEMESTER_PAPER, 0.9),
            (r'\bmid\s+sem\b', ResourceType.SEMESTER_PAPER, 0.9),

            # Syllabus patterns
            (r'\bsyllabus\b', ResourceType.SYLLABUS, 1.0),
            (r'\bcurriculum\b', ResourceType.SYLLABUS, 0.8),
            (r'\bcourse\s+outline\b', ResourceType.SYLLABUS, 0.8),

            # Question bank patterns
            (r'\bquestion\s+bank\b', ResourceType.QUESTION_BANK, 1.0),
            (r'\bqb\b', ResourceType.QUESTION_BANK, 0.9),
            (r'\bq\.?\s*bank\b', ResourceType.QUESTION_BANK, 1.0),

            # Notes patterns
            (r'\bnotes?\b', ResourceType.NOTES, 0.9),
            (r'\bunit\s+\d+', ResourceType.NOTES, 0.8),
            (r'\bchapter\s+\d+', ResourceType.NOTES, 0.8),
            (r'\blecture\b', ResourceType.NOTES, 0.8),
            (r'\bhandout\b', ResourceType.NOTES, 0.8),

            # Important questions patterns
            (r'\bimportant\s+questions?\b', ResourceType.IMPORTANT_QUESTIONS, 1.0),
            (r'\bimp\s+questions?\b', ResourceType.IMPORTANT_QUESTIONS, 1.0),
            (r'\bimportant\s+que\b', ResourceType.IMPORTANT_QUESTIONS, 0.9),
            (r'\bimp\b.*\bque\b', ResourceType.IMPORTANT_QUESTIONS, 0.8),

            # Answer key patterns
            (r'\banswer\s+key\b', ResourceType.ANSWER_KEY, 1.0),
            (r'\bsolutions?\b', ResourceType.ANSWER_KEY, 0.8),
            (r'\banswers?\b', ResourceType.ANSWER_KEY, 0.7),
            (r'\bkey\b', ResourceType.ANSWER_KEY, 0.6),
        ]

        # Exam type patterns
        self.exam_patterns = [
            (r'\bsemester\b|\bend\s+sem\b|\bendsem\b|\bmidsem\b|\bmid\s+sem\b', ExamType.SEMESTER),
            (r'\bct\b|\bclass\s+test\b|\bclasstest\b', ExamType.CT),
            (r'\bquiz\b', ExamType.QUIZ),
        ]

        # Year patterns
        self.year_patterns = [
            r'\b(20[2-9][0-9])\b',  # 2020-2099
            r'\b(nov|may|jul|june|december|jan)\s+(20[2-9][0-9])\b',
            r'\b(20[2-9][0-9])\s+(nov|may|jul|june|december|jan)\b',
        ]

    def _extract_year(self, title: str) -> Optional[int]:
        """
        Extract year from title.

        Args:
            title: Resource title

        Returns:
            Year if found (2020-2026), None otherwise

        Examples:
            >>> classifier = ResourceClassifier()
            >>> classifier._extract_year("PYQ Nov 2024")
            2024
            >>> classifier._extract_year("CT Papers 2025")
            2025
            >>> classifier._extract_year("Question Bank")
            >>> classifier._extract_year("May 2023 Exam")
            2023
            >>> classifier._extract_year("2022 Syllabus")
            2022
        """
        title_lower = title.lower()

        for pattern in self.year_patterns:
            match = re.search(pattern, title_lower)
            if match:
                # Extract year from groups
                year_str = None
                for group in match.groups():
                    if group and group.isdigit():
                        year_str = group
                        break

                if year_str:
                    year = int(year_str)
                    # Validate year range
                    if 2020 <= year <= 2026:
                        return year

        return None

    def _infer_exam_type(self, title: str) -> Optional[ExamType]:
        """
        Infer exam type from title.

        Args:
            title: Resource title

        Returns:
            ExamType if identified, None otherwise

        Examples:
            >>> classifier = ResourceClassifier()
            >>> classifier._infer_exam_type("PYQ Semester")
            <ExamType.SEMESTER: 'semester'>
            >>> classifier._infer_exam_type("CT Papers")
            <ExamType.CT: 'ct'>
            >>> classifier._infer_exam_type("Quiz 1")
            <ExamType.QUIZ: 'quiz'>
            >>> classifier._infer_exam_type("Notes")
        """
        title_lower = title.lower()

        for pattern, exam_type in self.exam_patterns:
            if re.search(pattern, title_lower):
                return exam_type

        return None

    def _classify_type(self, title: str) -> Tuple[ResourceType, float]:
        """
        Classify resource type with confidence score.

        Args:
            title: Resource title

        Returns:
            Tuple of (ResourceType, confidence_score)

        Examples:
            >>> classifier = ResourceClassifier()
            >>> rtype, conf = classifier._classify_type("PYQ Nov 2024")
            >>> rtype == ResourceType.PYQ
            True
            >>> conf > 0.8
            True

            >>> rtype, conf = classifier._classify_type("Best Books")
            >>> rtype == ResourceType.OTHER
            True
            >>> conf < 0.5
            True
        """
        title_lower = title.lower()

        # Track matches: {ResourceType: [weights]}
        matches = {}

        for pattern, resource_type, weight in self.resource_patterns:
            if re.search(pattern, title_lower):
                if resource_type not in matches:
                    matches[resource_type] = []
                matches[resource_type].append(weight)

        # No matches - classify as OTHER with low confidence
        if not matches:
            return ResourceType.OTHER, 0.3

        # Calculate scores for each resource type
        scores = {}
        for resource_type, weights in matches.items():
            # Score = max weight + bonus for multiple matches
            max_weight = max(weights)
            match_bonus = min(0.1 * (len(weights) - 1), 0.2)
            scores[resource_type] = min(max_weight + match_bonus, 1.0)

        # Return type with highest score
        best_type = max(scores.items(), key=lambda x: x[1])
        return best_type[0], best_type[1]

    def classify(self, title: str) -> Tuple[ResourceType, Optional[int], Optional[ExamType], float]:
        """
        Classify a resource by its title.

        Args:
            title: Resource title to classify

        Returns:
            Tuple of (resource_type, year, exam_type, confidence)
            - resource_type: Classified ResourceType
            - year: Extracted year (2020-2026) or None
            - exam_type: Inferred ExamType or None
            - confidence: Confidence score (0.0-1.0)

        Examples:
            >>> classifier = ResourceClassifier()
            >>> rtype, year, exam, conf = classifier.classify("PYQ Nov 2024")
            >>> rtype == ResourceType.PYQ and year == 2024
            True

            >>> rtype, year, exam, conf = classifier.classify("CT Papers 2025")
            >>> rtype == ResourceType.CT_PAPER and year == 2025 and exam == ExamType.CT
            True

            >>> rtype, year, exam, conf = classifier.classify("Syllabus")
            >>> rtype == ResourceType.SYLLABUS and year is None
            True

            >>> rtype, year, exam, conf = classifier.classify("Unit 3 Notes 2023")
            >>> rtype == ResourceType.NOTES and year == 2023
            True
        """
        if not title or not title.strip():
            return ResourceType.OTHER, None, None, 0.1

        # Extract components
        resource_type, base_confidence = self._classify_type(title)
        year = self._extract_year(title)
        exam_type = self._infer_exam_type(title)

        # Adjust confidence based on information richness
        confidence = base_confidence

        # Boost confidence if year found for relevant types
        if year and resource_type in [ResourceType.PYQ, ResourceType.CT_PAPER, ResourceType.SEMESTER_PAPER]:
            confidence = min(confidence + 0.1, 1.0)

        # Boost confidence if exam type matches resource type
        if exam_type:
            if (exam_type == ExamType.SEMESTER and resource_type == ResourceType.SEMESTER_PAPER) or \
               (exam_type == ExamType.CT and resource_type == ResourceType.CT_PAPER):
                confidence = min(confidence + 0.1, 1.0)

        # Title clarity bonus - shorter, clearer titles get higher confidence
        words = title.strip().split()
        if len(words) <= 3 and resource_type != ResourceType.OTHER:
            confidence = min(confidence + 0.05, 1.0)

        return resource_type, year, exam_type, confidence


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Additional manual tests
    classifier = ResourceClassifier()

    test_cases = [
        "PYQ Nov 2024",
        "CT Papers 2025",
        "Question Bank",
        "Unit 1 Notes",
        "Syllabus 2024",
        "Important Questions",
        "Answer Key May 2023",
        "Best Books",
        "PYQ Master PDF",
        "End Sem Paper 2022",
        "Quiz 1 Solutions",
        "Lecture Notes Unit 5",
        "IMP Questions for Finals",
        "Previous Year Question Papers",
    ]

    print("\n=== Manual Test Results ===\n")
    for title in test_cases:
        rtype, year, exam, conf = classifier.classify(title)
        print(f"Title: {title}")
        print(f"  Type: {rtype.value}")
        print(f"  Year: {year}")
        print(f"  Exam: {exam.value if exam else None}")
        print(f"  Confidence: {conf:.2f}")
        print()
