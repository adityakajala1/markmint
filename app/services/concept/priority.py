from app.schemas import ConceptEvidenceReport, StudyPriorityProfile, PriorityDimensions

class ConceptPriorityService:
    @staticmethod
    def calculate_priority(report: ConceptEvidenceReport, total_historical_papers: int) -> StudyPriorityProfile:
        """
        Calculates a transparent study priority ranking based on explicit underlying dimensions.
        Does NOT allow study-material frequency to alter historical exam frequency.
        """
        ex = report.exam_evidence
        st = report.study_evidence
        sy = report.syllabus_evidence

        # 1. Historical Importance Score (Max 1.0)
        # Based on paper coverage
        historical_importance = ex.number_of_papers / total_historical_papers if total_historical_papers > 0 else 0.0
        historical_importance = min(1.0, historical_importance)

        # 2. Recent Momentum (Max 1.0)
        # Did it appear in the last 2 available years?
        # A proper momentum calc would require total recent papers, but we'll use a scaled heuristic here.
        recent_momentum = 0.0
        if ex.years:
            max_year = max(ex.years)
            recent_appearances = sum(1 for y in ex.years if y >= max_year - 1)
            recent_momentum = min(1.0, recent_appearances / 2.0)

        # 3. Marks Importance (Max 1.0)
        # Average marks scaled against a typical 10-mark long answer
        avg_marks = (ex.total_marks / ex.number_of_questions) if ex.number_of_questions > 0 else 0.0
        marks_importance = min(1.0, avg_marks / 10.0)

        # 4. Recurrence Score (Max 1.0)
        recurrence = 0.0
        if ex.recurrence_interval > 0:
            # If interval is 1 year (appears every year) -> score 1.0
            # If interval is 4 years -> score 0.25
            recurrence = min(1.0, 1.0 / ex.recurrence_interval)

        # 5. Syllabus Relevance (Max 1.0)
        syllabus_relevance = 1.0 if sy.syllabus_references > 0 else 0.0

        # 6. Study Coverage Score (Max 1.0)
        coverage_map = {"STRONG": 1.0, "MODERATE": 0.6, "WEAK": 0.3, "NONE": 0.0}
        study_coverage = coverage_map.get(st.coverage_strength, 0.0)

        # 7. Evidence Strength (Max 1.0)
        evidence_strength = min(1.0, ex.number_of_questions / 10.0)

        # Transparent Weighting (Must sum to 1.0)
        # CRITICAL: Study coverage is NOT included in the final rank to avoid circular pollution.
        # Study coverage merely defines 'is_well_supported' or 'is_resource_gap'.
        weights = {
            "historical_importance": 0.35,
            "recent_momentum": 0.25,
            "marks_importance": 0.15,
            "recurrence": 0.15,
            "syllabus_relevance": 0.10,
            "study_coverage": 0.00, # Intentionally 0 so study freq doesn't boost exam freq
            "evidence_strength": 0.00 # Metadata only
        }

        final_score = (
            historical_importance * weights["historical_importance"] +
            recent_momentum * weights["recent_momentum"] +
            marks_importance * weights["marks_importance"] +
            recurrence * weights["recurrence"] +
            syllabus_relevance * weights["syllabus_relevance"]
        )

        # Gap Analysis
        # High exam importance but weak study coverage
        is_resource_gap = (final_score > 0.6) and (study_coverage < 0.5)
        
        # High exam importance and strong study coverage
        is_well_supported = (final_score > 0.6) and (study_coverage >= 0.8)

        dimensions = PriorityDimensions(
            historical_importance_score=round(historical_importance, 3),
            recent_momentum_score=round(recent_momentum, 3),
            marks_importance_score=round(marks_importance, 3),
            recurrence_score=round(recurrence, 3),
            syllabus_relevance_score=round(syllabus_relevance, 3),
            study_coverage_score=round(study_coverage, 3),
            evidence_strength_score=round(evidence_strength, 3)
        )

        return StudyPriorityProfile(
            concept_id=report.concept_id,
            dimensions=dimensions,
            final_priority_ranking=round(final_score, 3),
            is_resource_gap=is_resource_gap,
            is_well_supported=is_well_supported,
            weighting_documentation=weights
        )
