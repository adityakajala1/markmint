import json
import os
from typing import List, Dict, Any
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from backend.core.database import SessionLocal
from backend.models.core import Course
from backend.services.prediction.context import HistoricalContext, PredictionTarget
from backend.services.prediction.repository import HistoricalRepository
from backend.services.dna.analyzer import DNAAnalyzerService
from backend.services.prediction.engine import (
    AllTimeFrequencyBaseline,
    RecentFrequencyBaseline,
    RecencyWeightedBaseline,
    MarksWeightedBaseline,
    FamilyRecurrenceBaseline,
    ExamScopeCombinedModel
)

class BacktestEvaluator:
    @staticmethod
    def evaluate(predictions: list, target_items: list, k_values: list = [5, 10, 20]) -> dict:
        """
        predictions: list of PredictionResult
        target_items: list of dicts with 'name', 'marks', 'count' for the target exam
        """
        results = {}
        target_names = {t['name'] for t in target_items}
        total_target_unique = len(target_names)
        total_target_questions = sum(t['count'] for t in target_items)
        total_target_marks = sum(t['marks'] for t in target_items)
        
        for k in k_values:
            top_k = predictions[:k]
            top_k_names = {p.name for p in top_k}
            
            # Intersection (True Positives)
            hits = top_k_names.intersection(target_names)
            
            # Metrics
            precision = len(hits) / k if k > 0 else 0
            recall = len(hits) / total_target_unique if total_target_unique > 0 else 0
            
            # Coverage
            covered_questions = sum(t['count'] for t in target_items if t['name'] in top_k_names)
            covered_marks = sum(t['marks'] for t in target_items if t['name'] in top_k_names)
            
            q_coverage = covered_questions / total_target_questions if total_target_questions > 0 else 0
            m_coverage = covered_marks / total_target_marks if total_target_marks > 0 else 0
            
            results[f"P@{k}"] = precision
            results[f"R@{k}"] = recall
            results[f"Q_Cov@{k}"] = q_coverage
            results[f"M_Cov@{k}"] = m_coverage
            
        return results

class BacktestHarness:
    def __init__(self):
        self.db = SessionLocal()
        
    def get_usable_years(self, course_id: int) -> List[int]:
        from backend.models.core import Exam
        # Get all distinct years for the course that are anchored (not null)
        years = self.db.query(Exam.year).filter(
            Exam.course_id == course_id,
            Exam.year != None
        ).distinct().order_by(Exam.year.asc()).all()
        years = [y[0] for y in years]
        
        # We need at least 1 year of history to predict the next year
        if len(years) < 2:
            return []
        return years[1:] # Skip the very first year since it has no history

    def extract_target_data(self, target_exams: list) -> dict:
        topics = {}
        units = {}
        families = {}
        
        for exam in target_exams:
            for section in exam.sections:
                for q in section.questions:
                    m = q.marks or 0.0
                    
                    if q.topic:
                        t = topics.setdefault(q.topic.name, {'name': q.topic.name, 'count': 0, 'marks': 0.0})
                        t['count'] += 1
                        if not q.is_alternative: t['marks'] += m
                        
                    if q.unit:
                        u = units.setdefault(q.unit.name, {'name': q.unit.name, 'count': 0, 'marks': 0.0})
                        u['count'] += 1
                        if not q.is_alternative: u['marks'] += m
                        
                    if q.family_id:
                        fam_name = q.family.canonical_name if q.family else str(q.family_id)
                        f = families.setdefault(fam_name, {'name': fam_name, 'count': 0, 'marks': 0.0})
                        f['count'] += 1
                        if not q.is_alternative: f['marks'] += m
                        
        return {
            PredictionTarget.TOPIC: list(topics.values()),
            PredictionTarget.UNIT: list(units.values()),
            PredictionTarget.FAMILY: list(families.values())
        }

    def run(self):
        courses = self.db.query(Course).all()
        report = []
        
        for course in courses:
            usable_years = self.get_usable_years(course.id)
            if not usable_years:
                continue
                
            for target_year in usable_years:
                context = HistoricalContext(course_id=course.id, cutoff_year=target_year)
                repo = HistoricalRepository(self.db, context)
                
                # 1. Freeze Historical State
                hist_exams_orm = repo.get_historical_exams()
                # Convert ORM to dicts for ExamDNAAnalyzer
                hist_exams_dicts = [
                    {
                        "id": e.id,
                        "year": e.year,
                        "exam_type": e.exam_type,
                        "questions": [
                            {
                                "id": q.id,
                                "marks": q.marks,
                                "is_alternative": q.is_alternative,
                                "topic": q.topic.name if q.topic else None,
                                "unit": q.unit.name if q.unit else None,
                                "question_type": q.question_type,
                                "repetition_type": q.memberships[0].match_type if q.memberships else "singleton",
                                "family_name": q.family.canonical_name if q.family else None,
                                "difficulty": q.difficulty
                            }
                            for sec in e.sections for q in sec.questions
                        ]
                    }
                    for e in hist_exams_orm
                ]
                
                analyzer = DNAAnalyzerService()
                dna = analyzer.analyze(hist_exams_dicts, course.name)
                
                # 2. Generate Predictions (Models A-F)
                models = {
                    "A_AllTimeFreq": AllTimeFrequencyBaseline(dna),
                    "B_RecentFreq": RecentFrequencyBaseline(dna),
                    "C_RecencyWeighted": RecencyWeightedBaseline(dna),
                    "E_MarksWeighted": MarksWeightedBaseline(dna),
                    "F_ExamScopeCombined": ExamScopeCombinedModel(dna)
                }
                
                fam_models = {
                    "D_FamilyRecurrence": FamilyRecurrenceBaseline(dna),
                    "F_ExamScopeCombined": ExamScopeCombinedModel(dna)
                }
                
                # 3. Reveal Target Exam
                targ_exams_orm = repo.get_target_exams()
                target_data = self.extract_target_data(targ_exams_orm)
                
                # 4. Evaluate
                for m_name, model in models.items():
                    for target_type in [PredictionTarget.TOPIC, PredictionTarget.UNIT]:
                        preds = model.predict(target_type)
                        targ_items = target_data[target_type]
                        if targ_items:
                            evals = BacktestEvaluator.evaluate(preds, targ_items)
                            report.append({
                                "course": course.name,
                                "target_year": target_year,
                                "model": m_name,
                                "target_type": target_type,
                                "eval": evals
                            })
                            
                for m_name, model in fam_models.items():
                    preds = model.predict(PredictionTarget.FAMILY)
                    targ_items = target_data[PredictionTarget.FAMILY]
                    if targ_items:
                        evals = BacktestEvaluator.evaluate(preds, targ_items)
                        report.append({
                            "course": course.name,
                            "target_year": target_year,
                            "model": m_name,
                            "target_type": PredictionTarget.FAMILY,
                            "eval": evals
                        })

        os.makedirs('data/reports', exist_ok=True)
        with open('data/reports/backtest_results.json', 'w') as f:
            json.dump(report, f, indent=2)
            
        print("Backtest complete. Results written to data/reports/backtest_results.json")

if __name__ == '__main__':
    harness = BacktestHarness()
    harness.run()
