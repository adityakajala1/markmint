from collections import defaultdict
from typing import Any

from app.schemas.dna import (
    ExamDNA,
    DistributionMetric,
    MetricWithEvidence,
)

class DNAAnalyzerService:
    @classmethod
    def analyze(cls, exams: list[dict[str, Any]]) -> ExamDNA:
        """
        Expects a list of historical exams, each containing questions.
        Question dict format expected:
        {
            "id": "q1",
            "marks": 5.0,
            "topic": "Graphs",
            "unit": "Unit 3",
            "question_type": "explanation",
            "cognitive_level": "understand",
            "difficulty": 0.6,
            "repetition_type": "exact", # exact, conceptual, structural, or None
            "year": 2023
        }
        """
        total_exams = len(exams)
        all_questions = []
        for exam in exams:
            all_questions.extend(exam.get("questions", []))
            
        total_questions = len(all_questions)
        total_marks = sum(q.get("marks") or 0.0 for q in all_questions)

        if total_questions == 0:
            return cls._empty_dna()
            
        # Initialize aggregators
        topics: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0.0, "marks": 0.0})
        units: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0.0, "marks": 0.0})
        q_types: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0.0, "marks": 0.0})
        cog_levels: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0.0, "marks": 0.0})
        
        rep_exact_ids = []
        rep_conceptual_ids = []
        rep_structural_ids = []
        
        total_diff = 0.0
        diff_count = 0
        diff_ids = []

        for q in all_questions:
            m = q.get("marks") or 0.0
            
            # Topics
            if q.get("topic"):
                topics[q["topic"]]["count"] += 1
                topics[q["topic"]]["marks"] += m
                
            # Units
            if q.get("unit"):
                units[q["unit"]]["count"] += 1
                units[q["unit"]]["marks"] += m
                
            # Question Types
            if q.get("question_type"):
                q_types[q["question_type"]]["count"] += 1
                q_types[q["question_type"]]["marks"] += m
                
            # Cognitive Levels
            if q.get("cognitive_level"):
                cog_levels[q["cognitive_level"]]["count"] += 1
                cog_levels[q["cognitive_level"]]["marks"] += m
                
            # Difficulty
            if q.get("difficulty") is not None:
                total_diff += q["difficulty"]
                diff_count += 1
                diff_ids.append(q["id"])
                
            # Repetition
            rt = q.get("repetition_type")
            if rt == "exact":
                rep_exact_ids.append(q["id"])
            elif rt == "conceptual":
                rep_conceptual_ids.append(q["id"])
            elif rt == "structural":
                rep_structural_ids.append(q["id"])

        # Compile Distributions
        def _build_dist(agg_dict: dict[str, dict[str, float]]) -> list[DistributionMetric]:
            return [
                DistributionMetric(
                    key=k,
                    count=int(v["count"]),
                    percentage_of_total=v["count"] / total_questions,
                    marks_weighting=v["marks"] / total_marks if total_marks > 0 else 0.0
                ) for k, v in agg_dict.items()
            ]

        # Calculate Temporal Trends
        trends = cls._calculate_temporal_trends(exams)

        return ExamDNA(
            total_exams_analyzed=total_exams,
            total_questions_analyzed=total_questions,
            total_marks_analyzed=total_marks,
            topic_distribution=_build_dist(topics),
            unit_distribution=_build_dist(units),
            question_type_distribution=_build_dist(q_types),
            cognitive_level_distribution=_build_dist(cog_levels),
            average_difficulty=MetricWithEvidence(
                value=total_diff / diff_count if diff_count > 0 else 0.0,
                sample_size=diff_count,
                denominator=total_questions,
                supporting_question_ids=diff_ids
            ),
            exact_repetition_rate=MetricWithEvidence(
                value=len(rep_exact_ids) / total_questions,
                sample_size=len(rep_exact_ids),
                denominator=total_questions,
                supporting_question_ids=rep_exact_ids
            ),
            conceptual_repetition_rate=MetricWithEvidence(
                value=len(rep_conceptual_ids) / total_questions,
                sample_size=len(rep_conceptual_ids),
                denominator=total_questions,
                supporting_question_ids=rep_conceptual_ids
            ),
            structural_repetition_rate=MetricWithEvidence(
                value=len(rep_structural_ids) / total_questions,
                sample_size=len(rep_structural_ids),
                denominator=total_questions,
                supporting_question_ids=rep_structural_ids
            ),
            temporal_trends=trends
        )

    @classmethod
    def _calculate_temporal_trends(cls, exams: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Calculates how specific properties (e.g., topic frequencies) change over time.
        """
        trends: dict[str, list[dict[str, float | int]]] = defaultdict(list)
        
        # Sort exams by year
        sorted_exams = sorted(exams, key=lambda x: x.get("year", 0))
        
        for exam in sorted_exams:
            year = exam.get("year")
            if not year:
                continue
                
            questions = exam.get("questions", [])
            total_q = len(questions)
            if total_q == 0:
                continue
                
            # Topic trend
            topic_counts: dict[str, int] = defaultdict(int)
            for q in questions:
                if q.get("topic"):
                    topic_counts[q["topic"]] += 1
            
            for topic, count in topic_counts.items():
                trends[f"topic_{topic}_frequency"].append({
                    "year": year,
                    "frequency": count / total_q
                })
                
        return dict(trends)

    @classmethod
    def _empty_dna(cls) -> ExamDNA:
        return ExamDNA(
            total_exams_analyzed=0,
            total_questions_analyzed=0,
            total_marks_analyzed=0.0,
            topic_distribution=[],
            unit_distribution=[],
            question_type_distribution=[],
            cognitive_level_distribution=[],
            average_difficulty=MetricWithEvidence(value=0.0, sample_size=0),
            exact_repetition_rate=MetricWithEvidence(value=0.0, sample_size=0),
            conceptual_repetition_rate=MetricWithEvidence(value=0.0, sample_size=0),
            structural_repetition_rate=MetricWithEvidence(value=0.0, sample_size=0)
        )
