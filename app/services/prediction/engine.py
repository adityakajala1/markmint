from typing import Any
from collections import defaultdict
import math

from app.schemas import Prediction, ExamPredictions

class PredictionEngineService:
    def __init__(self, min_sample_size: int = 3, recency_weight_decay: float = 0.9):
        """
        min_sample_size: Minimum number of historical papers required to make High/Medium predictions.
        recency_weight_decay: How much older papers are discounted compared to newer ones. 
                              e.g., 0.9 means n-1 year is worth 0.9 of year n.
        """
        self.min_sample_size = min_sample_size
        self.recency_weight_decay = recency_weight_decay

    def generate_predictions(self, exams: list[dict[str, Any]]) -> ExamPredictions:
        total_exams = len(exams)
        
        if total_exams == 0:
            return ExamPredictions(
                predictions=[], 
                total_papers_analyzed=0, 
                insufficient_data=True
            )

        if total_exams < self.min_sample_size:
            limitation = f"Only {total_exams} historical paper{'s are' if total_exams > 1 else ' is'} available, which is insufficient for reliable predictions."
            return ExamPredictions(
                predictions=[
                    Prediction(
                        characteristic="Overall",
                        predicted_insight="Cannot generate reliable predictions.",
                        confidence="Insufficient Evidence",
                        supporting_evidence="Dataset size falls below the minimum threshold.",
                        sample_size=total_exams,
                        limitations=limitation
                    )
                ],
                total_papers_analyzed=total_exams,
                insufficient_data=True
            )
            
        # We have enough data.
        predictions = []
        predictions.extend(self._predict_high_weight_topics(exams))
        
        return ExamPredictions(
            predictions=predictions,
            total_papers_analyzed=total_exams,
            insufficient_data=False
        )
        
    def _predict_high_weight_topics(self, exams: list[dict[str, Any]]) -> list[Prediction]:
        """
        Analyzes topics based on recency-weighted appearance and marks.
        """
        total_exams = len(exams)
        sorted_exams = sorted(exams, key=lambda x: x.get("year", 0), reverse=True)
        
        topic_paper_appearances: dict[str, int] = defaultdict(int)
        topic_total_marks: dict[str, float] = defaultdict(float)
        topic_weighted_marks: dict[str, float] = defaultdict(float)
        
        total_historical_marks = 0.0
        
        # Calculate weights based on decay (0 index = newest exam = weight 1.0)
        for i, exam in enumerate(sorted_exams):
            weight = math.pow(self.recency_weight_decay, i)
            
            seen_topics_in_exam = set()
            exam_marks = sum(q.get("marks") or 0.0 for q in exam.get("questions", []))
            total_historical_marks += exam_marks
            
            for q in exam.get("questions", []):
                topic = q.get("topic")
                marks = q.get("marks") or 0.0
                
                if topic:
                    seen_topics_in_exam.add(topic)
                    topic_total_marks[topic] += marks
                    topic_weighted_marks[topic] += (marks * weight)
                    
            for t in seen_topics_in_exam:
                topic_paper_appearances[t] += 1
                
        # Generate predictions for top topics
        predictions = []
        
        # Sort by recency-weighted marks
        sorted_topics = sorted(topic_weighted_marks.items(), key=lambda x: x[1], reverse=True)
        
        for topic, w_marks in sorted_topics:
            appearances = topic_paper_appearances[topic]
            freq = appearances / total_exams
            raw_marks_pct = (topic_total_marks[topic] / total_historical_marks) * 100 if total_historical_marks > 0 else 0
            
            # Avoid false precision: round to 0 decimal places
            raw_marks_pct = round(raw_marks_pct)
            freq_rounded = round(freq, 2)
            
            if appearances >= (total_exams * 0.5) and raw_marks_pct > 15:
                predictions.append(
                    Prediction(
                        characteristic="High-Weight Topic",
                        predicted_insight=f"'{topic}' has consistently high historical importance for marks.",
                        confidence="High" if freq >= 0.8 else "Medium",
                        supporting_evidence=f"Appeared in {appearances} of {total_exams} papers and accounted for approximately {raw_marks_pct}% of total historical marks.",
                        sample_size=total_exams,
                        historical_frequency=freq_rounded,
                        limitations=f"Sample size of {total_exams} papers limits long-term certainty."
                    )
                )
                
        return predictions
