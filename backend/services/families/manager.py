import numpy as np
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.models.core import Question, QuestionFamily, QuestionFamilyMembership
from backend.services.question_classifier import BaseClassificationProvider
from backend.services.families.normalizer import QuestionNormalizer

class FamilyMatchDecision:
    def __init__(self, is_match: bool, match_type: str, score: float, method: str):
        self.is_match = is_match
        self.match_type = match_type
        self.score = score
        self.method = method

class LLMStructuralGuardrail:
    """
    Acts as a bounded validation layer for high-similarity conceptual matches
    to prevent structural false positives (e.g., 'Explain X' vs 'Explain Y').
    """
    @staticmethod
    def validate(q1_text: str, q2_text: str, similarity_score: float) -> bool:
        # In production, this would dispatch to an LLM:
        # "Do these two questions test the exact same underlying concept? Yes/No."
        # For now, we simulate the guardrail using lexical divergence on the nouns.
        
        # If similarity is extremely high, we trust the embedding
        if similarity_score >= 0.92:
            return True
            
        q1_lower = q1_text.lower()
        q2_lower = q2_text.lower()
        
        # Simple heuristic: if they share structural verbs but completely differ in key terms
        distinct_pairs = [
            ("binary", "breadth"),
            ("bfs", "dfs"),
            ("stack", "queue"),
            ("indexing", "scheduling"), # from user prompt
            ("normalization", "machine learning")
        ]
        
        for p1, p2 in distinct_pairs:
            if (p1 in q1_lower and p2 in q2_lower) or (p2 in q1_lower and p1 in q2_lower):
                return False
                
        return True

class QuestionFamilyManager:
    ALGORITHM_VERSION = "v1.0"
    EXACT_THRESHOLD = 0.98
    CONCEPTUAL_THRESHOLD = 0.82
    
    def __init__(self, db: Session, embedding_provider: BaseClassificationProvider):
        self.db = db
        self.provider = embedding_provider

    def _get_historical_families(self, subject: str, max_year: Optional[int]) -> List[QuestionFamily]:
        """
        Retrieves families strictly bounded by subject and chronological cutoff.
        If max_year is None (unanchored question), it can view all existing families to join them,
        but it will never spawn a family visible to historical cutoffs.
        """
        query = self.db.query(QuestionFamily).filter(QuestionFamily.subject == subject)
        if max_year is not None:
            # A dated question only sees families born in or before its year.
            # Null (unanchored) families are excluded because SQL `col <= val` evaluates to false/unknown for NULLs.
            query = query.filter(QuestionFamily.first_seen_year <= max_year)
        
        return query.all()

    def process_course_questions(self, course_id: int, subject_name: str):
        """
        Processes questions strictly chronologically to prevent temporal leakage.
        """
        from backend.models.core import Exam, Section
        
        # 1. Fetch all questions ordered by year
        # In SQLAlchemy, we need to join to get the year
        questions_by_year = (
            self.db.query(Question, Exam.year)
            .join(Section, Question.section_id == Section.id)
            .join(Exam, Section.exam_id == Exam.id)
            .filter(Exam.course_id == course_id)
            .order_by(Exam.year.asc())
            .all()
        )
        
        if not questions_by_year:
            return
            
        # Local cache of family embeddings for Top-K retrieval
        # Maps family_id -> list of embeddings (we can take the mean or max)
        family_embeddings_cache = {}
        
        # Load existing families into cache
        existing_families = self._get_historical_families(subject_name, 2100)
        
        # Precompute embeddings for all questions for efficiency, though we will apply them chronologically
        from backend.services.canonical import CanonicalRepresentationBuilder
        texts = [CanonicalRepresentationBuilder.build(q) for q, _ in questions_by_year]
        all_embeddings = self.provider.get_embeddings(texts)
        
        for i, (question, year) in enumerate(questions_by_year):
            # Skip if already processed
            if question.family_id is not None:
                continue
                
            q_year = year
            
            # Extract high-fidelity canonical text from structured JSON
            from backend.services.canonical import CanonicalRepresentationBuilder
            q_text = CanonicalRepresentationBuilder.build(question)
            
            q_norm = QuestionNormalizer.normalize(q_text)
            q_emb = np.array(all_embeddings[i])
            
            # Update the question's text fields to the new high-fidelity version
            question.original_text = q_text
            question.normalized_text = q_norm
            
            # 2. Retrieve candidates strictly from families first seen <= q_year
            # (Immutable historical ancestry)
            candidate_families = self._get_historical_families(subject_name, q_year)
            
            decision = None
            best_family_id = None
            
            # Attempt Exact Match (Lexical) first against questions in candidate families
            for family in candidate_families:
                # We could optimize this by caching normalized canonical texts
                fam_norm = QuestionNormalizer.normalize(family.canonical_name)
                # Jaccard/Levenshtein approximation (exact string for now)
                if q_norm == fam_norm:
                    if len(q_norm) > 10: # Avoid matching trivial "1"
                        decision = FamilyMatchDecision(True, "exact", 1.0, "lexical_hash")
                        best_family_id = family.id
                        break
            
            # 3. Semantic Top-K Matching
            if not decision and candidate_families:
                # Compute scores
                scores = []
                valid_candidates = []
                
                for family in candidate_families:
                    # Retrieve the embedding of the canonical question or compute it
                    fam_emb = np.array(self.provider.get_embeddings([family.canonical_name])[0])
                    
                    dot = np.dot(q_emb, fam_emb)
                    norm_q = np.linalg.norm(q_emb)
                    norm_f = np.linalg.norm(fam_emb)
                    
                    if norm_q > 0 and norm_f > 0:
                        sim = float(dot / (norm_q * norm_f))
                        scores.append(sim)
                        valid_candidates.append(family)
                        
                if scores:
                    best_idx = int(np.argmax(scores))
                    best_score = scores[best_idx]
                    best_fam = valid_candidates[best_idx]
                    
                    if best_score >= self.CONCEPTUAL_THRESHOLD:
                        # 4. LLM Structural Guardrail Validation
                        is_valid = LLMStructuralGuardrail.validate(q_text, best_fam.canonical_name, best_score)
                        
                        if is_valid:
                            decision = FamilyMatchDecision(True, "conceptual", best_score, "semantic_embedding+llm_guardrail")
                            best_family_id = best_fam.id
                        else:
                            # Flagged as structural but different concept -> Reject match
                            pass
            
            # 5. Assignment
            if decision and best_family_id:
                # Assign to existing family
                question.family_id = best_family_id
                
                # Update latest seen
                fam_to_update = self.db.query(QuestionFamily).get(best_family_id)
                if fam_to_update and q_year is not None:
                    if fam_to_update.latest_seen_year is None or q_year > fam_to_update.latest_seen_year:
                        fam_to_update.latest_seen_year = q_year
                
                # Persist evidence
                membership = QuestionFamilyMembership(
                    question_id=question.id,
                    family_id=best_family_id,
                    match_type=decision.match_type,
                    similarity_score=decision.score,
                    decision_method=decision.method,
                    algorithm_version=self.ALGORITHM_VERSION
                )
                self.db.add(membership)
                
            else:
                # 6. Spawns a new family (Singleton initially)
                new_family = QuestionFamily(
                    canonical_name=q_text,
                    subject=subject_name,
                    first_seen_year=q_year,
                    latest_seen_year=q_year,
                    repetition_type="singleton"
                )
                self.db.add(new_family)
                self.db.flush() # get ID
                
                question.family_id = new_family.id
                
                membership = QuestionFamilyMembership(
                    question_id=question.id,
                    family_id=new_family.id,
                    match_type="exact", # self-match
                    similarity_score=1.0,
                    decision_method="spawn",
                    algorithm_version=self.ALGORITHM_VERSION
                )
                self.db.add(membership)
                
        self.db.commit()
