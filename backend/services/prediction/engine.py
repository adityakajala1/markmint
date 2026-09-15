from typing import List, Dict, Any, Tuple
from backend.services.dna.analyzer import ExamDNA
from backend.services.prediction.context import PredictionTarget

class PredictionResult:
    def __init__(self, target: str, name: str, rank: int, score: float, confidence: str, evidence: dict):
        self.target = target  # 'topic', 'unit', 'family', 'concept'
        self.name = name
        self.rank = rank
        self.score = score
        self.confidence = confidence
        self.evidence = evidence

class BaseModel:
    def __init__(self, dna: ExamDNA):
        self.dna = dna

    def predict_topics(self) -> List[PredictionResult]:
        return []
        
    def predict_units(self) -> List[PredictionResult]:
        return []
        
    def predict_families(self) -> List[PredictionResult]:
        return []
        
    def predict(self, target_type: str) -> List[PredictionResult]:
        if target_type == PredictionTarget.TOPIC:
            return self.predict_topics()
        elif target_type == PredictionTarget.UNIT:
            return self.predict_units()
        elif target_type == PredictionTarget.FAMILY:
            return self.predict_families()
        return []
        
    def _rank_and_format(self, scored_items: List[Tuple[str, float, dict]], target: str) -> List[PredictionResult]:
        # Sort by score descending
        scored_items.sort(key=lambda x: x[1], reverse=True)
        results = []
        for rank, (name, score, evidence) in enumerate(scored_items, start=1):
            conf = "HIGH" if score > 0.7 else "MEDIUM" if score > 0.4 else "LOW"
            if evidence.get("sample_size", 0) < 3 and target == PredictionTarget.FAMILY:
                conf = "INSUFFICIENT"
            
            results.append(PredictionResult(
                target=target,
                name=name,
                rank=rank,
                score=score,
                confidence=conf,
                evidence=evidence
            ))
        return results

class AllTimeFrequencyBaseline(BaseModel):
    def predict_topics(self):
        scores = [(t.topic, t.historical_frequency, {"freq": t.historical_frequency}) for t in self.dna.topics]
        return self._rank_and_format(scores, PredictionTarget.TOPIC)
        
    def predict_units(self):
        # We use question count percentage for unit frequency if we want count frequency
        # But we only have historical_weighting which is marks. 
        # Wait, the unit DNA has question_count. We can divide by dna.sample_size.questions.
        total_q = self.dna.sample_size.questions
        scores = []
        for u in self.dna.units:
            freq = (u.question_count / total_q) if total_q else 0
            scores.append((u.unit, freq, {"freq": freq}))
        return self._rank_and_format(scores, PredictionTarget.UNIT)

class RecentFrequencyBaseline(BaseModel):
    def predict_topics(self):
        scores = [(t.topic, t.recent_frequency, {"recent_freq": t.recent_frequency}) for t in self.dna.topics]
        return self._rank_and_format(scores, PredictionTarget.TOPIC)
        
    def predict_units(self):
        scores = [(u.unit, u.recent_weighting, {"recent_weight": u.recent_weighting}) for u in self.dna.units]
        return self._rank_and_format(scores, PredictionTarget.UNIT)

class RecencyWeightedBaseline(BaseModel):
    def predict_topics(self):
        scores = []
        for t in self.dna.topics:
            score = (0.7 * t.recent_frequency) + (0.3 * t.historical_frequency)
            scores.append((t.topic, score, {"recent_freq": t.recent_frequency, "hist_freq": t.historical_frequency}))
        return self._rank_and_format(scores, PredictionTarget.TOPIC)

class MarksWeightedBaseline(BaseModel):
    def predict_topics(self):
        total_marks = sum(t.total_marks for t in self.dna.topics)
        scores = []
        for t in self.dna.topics:
            weight = (t.total_marks / total_marks) if total_marks else 0
            scores.append((t.topic, weight, {"marks_weight": weight}))
        return self._rank_and_format(scores, PredictionTarget.TOPIC)
        
    def predict_units(self):
        scores = [(u.unit, u.historical_weighting, {"marks_weight": u.historical_weighting}) for u in self.dna.units]
        return self._rank_and_format(scores, PredictionTarget.UNIT)

class FamilyRecurrenceBaseline(BaseModel):
    def predict_families(self):
        scores = []
        for f in self.dna.families:
            # Score heavily based on recurrence interval and historical consistency
            # For a naive baseline, we just use occurrences or recent count
            score = f.occurrences * 0.5 + f.recent_recurrence_count * 0.5
            scores.append((f.family_name, score, {"occurrences": f.occurrences, "sample_size": f.occurrences}))
        return self._rank_and_format(scores, PredictionTarget.FAMILY)

class ExamScopeCombinedModel(BaseModel):
    def predict_topics(self):
        total_marks = sum(t.total_marks for t in self.dna.topics)
        scores = []
        for t in self.dna.topics:
            marks_w = (t.total_marks / total_marks) if total_marks else 0
            score = (0.4 * t.recent_frequency) + (0.3 * marks_w) + (0.3 * t.historical_frequency)
            scores.append((t.topic, score, {
                "combo": True, 
                "recent_freq": t.recent_frequency,
                "hist_freq": t.historical_frequency,
                "occurrences": t.question_count
            }))
        return self._rank_and_format(scores, PredictionTarget.TOPIC)
        
    def predict_units(self):
        scores = []
        for u in self.dna.units:
            score = (0.6 * u.recent_weighting) + (0.4 * u.historical_weighting)
            scores.append((u.unit, score, {
                "combo": True,
                "occurrences": u.question_count
            }))
        return self._rank_and_format(scores, PredictionTarget.UNIT)
        
    def predict_families(self):
        scores = []
        for f in self.dna.families:
            score = (f.occurrences * 0.4) + (f.recent_recurrence_count * 0.6)
            last_seen = str(max(f.years)) if f.years else "Unknown"
            scores.append((f.family_name, score, {
                "occurrences": f.occurrences, 
                "sample_size": f.occurrences, 
                "interval": f.recurrence_interval_years,
                "last_seen": last_seen
            }))
        return self._rank_and_format(scores, PredictionTarget.FAMILY)
