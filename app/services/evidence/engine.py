from typing import Optional
from app.schemas import InsightExplanation, FactualMetrics, ProvenanceNode

class WhyEngineService:
    @staticmethod
    def generate_topic_importance(
        topic_name: str, 
        subject: str,
        metrics: FactualMetrics, 
        time_range: tuple[int, int],
        question_ids: list[int]
    ) -> InsightExplanation:
        
        # Guard against insufficient evidence exaggeration
        if metrics.total_papers < 3 or metrics.supported_questions < 5:
            return InsightExplanation(
                finding_type="topic_importance",
                subject=subject,
                time_range_years=time_range,
                insight_text="Insufficient historical data to determine a reliable pattern.",
                metrics=metrics,
                provenance_chain=[ProvenanceNode(record_type="question", record_id=qid) for qid in question_ids],
                confidence="INSUFFICIENT",
                limitations=f"Only {metrics.total_papers} historical papers available."
            )

        # Deterministic formatting
        insight_text = (
            f"'{topic_name}' has historically appeared in {metrics.supported_papers} of {metrics.total_papers} papers. "
            f"It represents {metrics.supported_questions} questions and {metrics.total_marks} total marks."
        )

        confidence = "HIGH" if (metrics.supported_papers / metrics.total_papers) >= 0.7 else "MEDIUM"
        
        limitations = None
        if metrics.recent_papers == 0:
            confidence = "LOW"
            limitations = "This topic has not appeared in any recent exams, reducing predictive confidence."

        return InsightExplanation(
            finding_type="topic_importance",
            subject=subject,
            time_range_years=time_range,
            insight_text=insight_text,
            metrics=metrics,
            provenance_chain=[ProvenanceNode(record_type="question", record_id=qid) for qid in question_ids],
            confidence=confidence,
            limitations=limitations
        )
