from collections import defaultdict
from typing import Any
import math

from backend.schemas import (
    ExamDNA,
    DataSufficiency,
    DNASampleSize,
    TopicDNA,
    UnitDNA,
    QuestionTypeDNA,
    RepetitionDNA,
    FamilyDNA,
    TemporalTrend
)

class DNAAnalyzerService:
    @classmethod
    def determine_sufficiency(cls, papers: int, questions: int) -> DataSufficiency:
        if papers <= 1 or questions < 10:
            return DataSufficiency.INSUFFICIENT
        if papers <= 3 or questions <= 30:
            return DataSufficiency.LIMITED
        if papers <= 6 or questions <= 100:
            return DataSufficiency.MODERATE
        return DataSufficiency.STRONG

    @classmethod
    def analyze(cls, exams: list[dict[str, Any]]) -> ExamDNA:
        """
        Analyzes historical exams mathematically. 
        Expects a list of exam dicts mapped from the database.
        """
        sorted_exams = sorted(exams, key=lambda x: x.get("year") or 0)
        total_exams = len(sorted_exams)
        
        all_questions = []
        for exam in sorted_exams:
            all_questions.extend(exam.get("questions", []))
            
        total_questions = len(all_questions)
        
        if total_questions == 0 or total_exams == 0:
            return cls._empty_dna()
            
        years = [e.get("year") for e in sorted_exams if e.get("year")]
        min_year = min(years) if years else 0
        max_year = max(years) if years else 0
        
        # 'Recent' is the last 2 available chronological years in THIS dataset
        recent_years_set = {y for y in years if y >= max_year - 1}

        exam_types = list({e.get("exam_type") for e in sorted_exams if e.get("exam_type")})
        
        sufficiency = cls.determine_sufficiency(total_exams, total_questions)
        
        sample_size = DNASampleSize(
            papers=total_exams,
            questions=total_questions,
            time_range_years=(min_year, max_year),
            exam_types=exam_types,
            sufficiency=sufficiency
        )
        
        if sufficiency == DataSufficiency.INSUFFICIENT:
            # We still return aggregations, but frontend should hide percentages
            pass

        # 1. Base Aggregators
        total_marks = sum(q.get("marks", 0.0) or 0.0 for q in all_questions if not q.get("is_alternative"))
        recent_total_marks = sum(
            q.get("marks", 0.0) or 0.0 
            for e in sorted_exams if e.get("year") in recent_years_set 
            for q in e.get("questions", []) if not q.get("is_alternative")
        )
        
        topics_data: dict[str, Any] = defaultdict(lambda: {
            "q_count": 0, "marks": 0.0, "papers": set(), 
            "long_ans": 0, "short_ans": 0, "recent_q_count": 0,
            "diffs": []
        })
        units_data: dict[str, Any] = defaultdict(lambda: {
            "q_count": 0, "marks": 0.0, "papers": set(), "recent_marks": 0.0
        })
        qtypes_data: dict[str, Any] = defaultdict(lambda: {"count": 0, "marks": 0.0})
        
        rep_exact = rep_near = rep_concept = rep_struct = 0
        
        families_data: dict[str, Any] = defaultdict(lambda: {
            "occurrences": 0, "years": set(), "exam_types": set(), 
            "marks": [], "recent_count": 0
        })

        # 2. Populate Aggregators
        for exam in sorted_exams:
            exam_year = exam.get("year")
            exam_id = exam.get("id")
            exam_type = exam.get("exam_type")
            is_recent = exam_year in recent_years_set
            
            for q in exam.get("questions", []):
                m = q.get("marks") or 0.0
                
                # Topics
                topic = q.get("topic")
                if topic:
                    td = topics_data[topic]
                    td["q_count"] += 1
                    td["marks"] += m
                    td["papers"].add(exam_id)
                    if m >= 5.0: td["long_ans"] += 1
                    if m <= 3.0: td["short_ans"] += 1
                    if is_recent: td["recent_q_count"] += 1
                    if q.get("difficulty") is not None:
                        td["diffs"].append(q["difficulty"])
                
                # Units
                unit = q.get("unit")
                if unit:
                    ud = units_data[unit]
                    ud["q_count"] += 1
                    ud["marks"] += m
                    ud["papers"].add(exam_id)
                    if is_recent: ud["recent_marks"] += m
                    
                # Question Types
                qtype = q.get("question_type")
                if qtype:
                    qtypes_data[qtype]["count"] += 1
                    qtypes_data[qtype]["marks"] += m
                    
                # Repetition Types
                rep = q.get("repetition_type")
                if rep == "exact": rep_exact += 1
                elif rep == "near": rep_near += 1
                elif rep == "conceptual": rep_concept += 1
                elif rep == "structural": rep_struct += 1
                
                # Question Families
                fam = q.get("family_name")
                if fam:
                    fd = families_data[fam]
                    fd["occurrences"] += 1
                    if exam_year: fd["years"].add(exam_year)
                    if exam_type: fd["exam_types"].add(exam_type)
                    fd["marks"].append(m)
                    if is_recent: fd["recent_count"] += 1

        # 3. Compile DTOs
        topics_dna = []
        for t_name, td in topics_data.items():
            # Difficulty distribution binning
            diff_dist = {"0.0-0.3": 0, "0.3-0.7": 0, "0.7-1.0": 0}
            for d in td["diffs"]:
                if d < 0.3: diff_dist["0.0-0.3"] += 1
                elif d < 0.7: diff_dist["0.3-0.7"] += 1
                else: diff_dist["0.7-1.0"] += 1
                
            recent_freq = td["recent_q_count"] / total_questions if total_questions > 0 else 0
            hist_freq = td["q_count"] / total_questions if total_questions > 0 else 0
            
            topics_dna.append(TopicDNA(
                topic=t_name,
                question_count=td["q_count"],
                paper_coverage=len(td["papers"]) / total_exams,
                total_marks=td["marks"],
                average_marks=td["marks"] / td["q_count"],
                long_answer_frequency=td["long_ans"] / td["q_count"],
                short_answer_frequency=td["short_ans"] / td["q_count"],
                recent_frequency=recent_freq,
                historical_frequency=hist_freq,
                difficulty_distribution=diff_dist
            ))
            
        units_dna = []
        for u_name, ud in units_data.items():
            units_dna.append(UnitDNA(
                unit=u_name,
                question_count=ud["q_count"],
                marks=ud["marks"],
                paper_coverage=len(ud["papers"]) / total_exams,
                recent_weighting=ud["recent_marks"] / recent_total_marks if recent_total_marks > 0 else 0,
                historical_weighting=ud["marks"] / total_marks if total_marks > 0 else 0
            ))
            
        qtypes_dna = []
        for qt, qtd in qtypes_data.items():
            qtypes_dna.append(QuestionTypeDNA(
                question_type=qt,
                count=qtd["count"],
                percentage=qtd["count"] / total_questions,
                marks_weighting=qtd["marks"] / total_marks if total_marks > 0 else 0
            ))
            
        families_dna = []
        for f_name, fd in families_data.items():
            sorted_years = sorted(list(fd["years"]))
            interval = 0.0
            if len(sorted_years) > 1:
                diffs = [sorted_years[i] - sorted_years[i-1] for i in range(1, len(sorted_years))]
                interval = sum(diffs) / len(diffs)
                
            families_dna.append(FamilyDNA(
                family_name=f_name,
                occurrences=fd["occurrences"],
                years=sorted_years,
                exam_types=list(fd["exam_types"]),
                average_marks=sum(fd["marks"]) / len(fd["marks"]) if fd["marks"] else 0,
                recurrence_interval_years=interval,
                recent_recurrence_count=fd["recent_count"],
                trend="stable" # Basic default, temporal engine can override
            ))

        return ExamDNA(
            sample_size=sample_size,
            topics=topics_dna,
            units=units_dna,
            question_types=qtypes_dna,
            repetition=RepetitionDNA(
                exact_count=rep_exact,
                near_count=rep_near,
                conceptual_count=rep_concept,
                structural_count=rep_struct
            ),
            families=families_dna,
            temporal_trends=[]
        )

    @classmethod
    def _empty_dna(cls) -> ExamDNA:
        return ExamDNA(
            sample_size=DNASampleSize(
                papers=0, questions=0, time_range_years=(0,0), 
                exam_types=[], sufficiency=DataSufficiency.INSUFFICIENT
            ),
            topics=[], units=[], question_types=[],
            repetition=RepetitionDNA(exact_count=0, near_count=0, conceptual_count=0, structural_count=0),
            families=[], temporal_trends=[]
        )
