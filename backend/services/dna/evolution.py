from typing import Any
from collections import defaultdict
import statistics

from backend.schemas import (
    EvolutionReport, ChangePoint, ComponentTrend, EvolutionEvidence, TrendClassification
)

class ExamEvolutionService:
    @classmethod
    def _calculate_trend(
        cls, 
        h1_values: list[float], 
        h2_values: list[float], 
        h1_papers: int, 
        h2_papers: int,
        exam_ids: list[int]
    ) -> tuple[TrendClassification, EvolutionEvidence]:
        
        q_before = len(h1_values)
        q_after = len(h2_values)
        
        # We need sufficient evidence to declare a trend
        if h1_papers < 2 or h2_papers < 2 or (q_before + q_after < 5):
            ev = EvolutionEvidence(
                before_value=0.0, after_value=0.0, magnitude=0.0,
                sample_size_before_papers=h1_papers, sample_size_after_papers=h2_papers,
                sample_size_before_questions=q_before, sample_size_after_questions=q_after,
                supporting_exam_ids=exam_ids
            )
            return TrendClassification.INSUFFICIENT, ev

        val_before = sum(h1_values) / h1_papers if h1_papers else 0.0
        val_after = sum(h2_values) / h2_papers if h2_papers else 0.0
        
        magnitude = val_after - val_before
        
        # Volatility check: if standard deviation of year-over-year counts is very high relative to mean
        # (Simplified heuristic for the sake of the engine)
        
        classification = TrendClassification.STABLE
        # Threshold: > 15% change in average appearances per paper OR average marks per paper
        if magnitude > 0.15 * max(val_before, 1.0):
            classification = TrendClassification.RISING
        elif magnitude < -0.15 * max(val_before, 1.0):
            classification = TrendClassification.DECLINING

        ev = EvolutionEvidence(
            before_value=round(val_before, 3), 
            after_value=round(val_after, 3), 
            magnitude=round(magnitude, 3),
            sample_size_before_papers=h1_papers, 
            sample_size_after_papers=h2_papers,
            sample_size_before_questions=q_before, 
            sample_size_after_questions=q_after,
            supporting_exam_ids=exam_ids
        )
        return classification, ev

    @classmethod
    def analyze_evolution(cls, course_id: int, exams: list[dict[str, Any]]) -> EvolutionReport:
        # Filter valid chronological exams
        valid_exams = [e for e in exams if e.get("year") is not None]
        excluded_count = len(exams) - len(valid_exams)
        
        sorted_exams = sorted(valid_exams, key=lambda x: x["year"])
        total_papers = len(sorted_exams)
        
        if total_papers < 4:
            # Insufficient papers for a before/after split
            return EvolutionReport(
                course_id=course_id, total_papers_analyzed=total_papers, 
                excluded_papers_missing_year=excluded_count, time_range=(0,0),
                topic_trends=[], unit_trends=[], format_change_points=[], 
                difficulty_change_points=[], repetition_change_points=[]
            )
            
        years = [e["year"] for e in sorted_exams]
        min_year = min(years)
        max_year = max(years)
        
        # Split chronologically at the median index
        mid_idx = total_papers // 2
        h1_exams = sorted_exams[:mid_idx]
        h2_exams = sorted_exams[mid_idx:]
        
        split_year = h2_exams[0].get("year", 0)
        
        tr_before = (min_year, split_year - 1 if split_year > min_year else split_year)
        tr_after = (split_year, max_year)
        
        h1_ids = [e.get("id") for e in h1_exams]
        h2_ids = [e.get("id") for e in h2_exams]
        all_ids = h1_ids + h2_ids
        
        # Data aggregation
        topics_h1 = defaultdict(list) # topic -> list of marks
        topics_h2 = defaultdict(list)
        
        format_h1 = defaultdict(list) # format_type -> list of marks
        format_h2 = defaultdict(list)
        
        diff_h1 = []
        diff_h2 = []

        def process_half(exam_list, topic_dict, format_dict, diff_list):
            for ex in exam_list:
                for q in ex.get("questions", []):
                    m = q.get("marks", 0.0) or 0.0
                    
                    if q.get("topic"):
                        topic_dict[q["topic"]].append(m)
                    
                    qtype = q.get("question_type")
                    if qtype in ["implementation", "application", "numerical"]:
                        format_dict["practical"].append(m)
                    elif qtype in ["definition", "explanation", "comparison", "derivation"]:
                        format_dict["theoretical"].append(m)
                        
                    if m >= 5.0:
                        format_dict["long_answer"].append(m)
                        
                    if q.get("difficulty") is not None:
                        diff_list.append(q["difficulty"])

        process_half(h1_exams, topics_h1, format_h1, diff_h1)
        process_half(h2_exams, topics_h2, format_h2, diff_h2)
        
        topic_trends = []
        all_topics = set(topics_h1.keys()).union(set(topics_h2.keys()))
        for t in all_topics:
            cls_trend, ev = cls._calculate_trend(
                topics_h1.get(t, []), topics_h2.get(t, []), 
                len(h1_exams), len(h2_exams), all_ids
            )
            topic_trends.append(ComponentTrend(name=t, classification=cls_trend, evidence=ev))

        # Format Change Points
        format_cps = []
        prac_cls, prac_ev = cls._calculate_trend(
            format_h1.get("practical", []), format_h2.get("practical", []),
            len(h1_exams), len(h2_exams), all_ids
        )
        if prac_cls == TrendClassification.RISING:
            format_cps.append(ChangePoint(
                dimension="format.practical_focus",
                change_year=split_year,
                time_range_before=tr_before,
                time_range_after=tr_after,
                description=f"The exam became increasingly implementation and application-heavy after {split_year}.",
                evidence=prac_ev,
                confidence="HIGH" if prac_ev.sample_size_after_papers >= 3 else "MEDIUM"
            ))
            
        long_cls, long_ev = cls._calculate_trend(
            format_h1.get("long_answer", []), format_h2.get("long_answer", []),
            len(h1_exams), len(h2_exams), all_ids
        )
        if long_cls == TrendClassification.DECLINING:
            format_cps.append(ChangePoint(
                dimension="format.length",
                change_year=split_year,
                time_range_before=tr_before,
                time_range_after=tr_after,
                description=f"The exam shifted away from long-answer questions (>= 5 marks) after {split_year}.",
                evidence=long_ev,
                confidence="HIGH" if long_ev.sample_size_after_papers >= 3 else "MEDIUM"
            ))

        # Difficulty Change Points
        diff_cps = []
        if diff_h1 and diff_h2:
            avg_d1 = sum(diff_h1) / len(diff_h1)
            avg_d2 = sum(diff_h2) / len(diff_h2)
            if avg_d2 - avg_d1 > 0.15:
                diff_cps.append(ChangePoint(
                    dimension="difficulty.average",
                    change_year=split_year,
                    time_range_before=tr_before,
                    time_range_after=tr_after,
                    description=f"The average difficulty of questions noticeably increased after {split_year}.",
                    evidence=EvolutionEvidence(
                        before_value=round(avg_d1, 3), after_value=round(avg_d2, 3), magnitude=round(avg_d2 - avg_d1, 3),
                        sample_size_before_papers=len(h1_exams), sample_size_after_papers=len(h2_exams),
                        sample_size_before_questions=len(diff_h1), sample_size_after_questions=len(diff_h2),
                        supporting_exam_ids=all_ids
                    ),
                    confidence="HIGH"
                ))

        return EvolutionReport(
            course_id=course_id,
            total_papers_analyzed=total_papers,
            excluded_papers_missing_year=excluded_count,
            time_range=(min_year, max_year),
            topic_trends=topic_trends,
            unit_trends=[], # Extensible for units
            format_change_points=format_cps,
            difficulty_change_points=diff_cps,
            repetition_change_points=[] # Extensible for repetition
        )
