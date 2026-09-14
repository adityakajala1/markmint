import re
from typing import Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc

from backend.models.core import Question, Concept, StudyEvidence, Document, Exam
from backend.schemas import (
    SearchQuery, SearchResult, SearchResultType, ParsedIntent, SearchFilters
)

class DiscoverySearchEngine:
    def __init__(self, db: Session):
        self.db = db

    def _parse_intent(self, raw_query: str) -> ParsedIntent:
        """
        Parses natural language to extract implicit filters (e.g. '5 mark questions').
        """
        q = raw_query.lower()
        intent = ParsedIntent(clean_search_term=raw_query)
        
        # 1. Target Type
        if "trend" in q or "increasing" in q or "decreasing" in q:
            intent.target_type = SearchResultType.ANALYSIS_FINDING
        elif "family" in q or "repeat" in q or "coming" in q:
            intent.target_type = SearchResultType.QUESTION_FAMILY
        elif "question" in q:
            intent.target_type = SearchResultType.EXAM_QUESTION
        elif "concept" in q or "topic" in q:
            intent.target_type = SearchResultType.CONCEPT

        # 2. Extract Marks
        marks_match = re.search(r'(\d+)\s*mark', q)
        if marks_match:
            intent.extracted_marks = float(marks_match.group(1))
            
        # 3. Clean search term (remove boilerplate words)
        stopwords = ["about", "what", "keeps", "coming", "in", "questions", "on", "mark", "that", "repeat", "recently", "topics"]
        words = q.split()
        clean_words = [w for w in words if w not in stopwords and not w.isdigit()]
        intent.clean_search_term = " ".join(clean_words).strip()
        
        return intent

    def _hybrid_search_questions(self, intent: ParsedIntent, filters: SearchFilters, limit: int) -> list[SearchResult]:
        query = self.db.query(Question).join(Question.section).join(Section.exam).join(Exam.document)
        
        # Exact/Metadata filters
        if intent.extracted_marks:
            query = query.filter(Question.marks == intent.extracted_marks)
        if filters.marks:
            query = query.filter(Question.marks == filters.marks)
            
        if filters.year:
            query = query.filter(Exam.year == filters.year)
            
        # Text/Semantic filter (fallback to ILIKE for MVP, embedding logic goes here)
        if intent.clean_search_term:
            term = f"%{intent.clean_search_term}%"
            query = query.filter(
                or_(
                    Question.text.ilike(term),
                    Question.topic.ilike(term)
                )
            )
            
        results = query.limit(limit).all()
        
        out = []
        for q in results:
            out.append(SearchResult(
                id=q.id,
                result_type=SearchResultType.EXAM_QUESTION,
                title=f"Question on {q.topic or 'Unknown'}",
                text_snippet=q.text[:200] if q.text else "",
                year=q.section.exam.year,
                topic=q.topic,
                relevance_score=0.9, # Mock embedding distance
                provenance_url=q.section.exam.document.original_url if q.section.exam.document else None
            ))
        return out

    def _hybrid_search_concepts(self, intent: ParsedIntent, filters: SearchFilters, limit: int) -> list[SearchResult]:
        query = self.db.query(Concept)
        
        if filters.subject:
            query = query.filter(Concept.subject == filters.subject)
            
        if intent.clean_search_term:
            term = f"%{intent.clean_search_term}%"
            query = query.filter(Concept.canonical_name.ilike(term))
            
        results = query.limit(limit).all()
        
        return [SearchResult(
            id=c.id,
            result_type=SearchResultType.CONCEPT,
            title=c.canonical_name,
            text_snippet=c.description or "",
            subject=c.subject,
            relevance_score=0.95
        ) for c in results]
        
    def _hybrid_search_study_material(self, intent: ParsedIntent, filters: SearchFilters, limit: int) -> list[SearchResult]:
        query = self.db.query(StudyEvidence).join(StudyEvidence.document)
        
        if intent.clean_search_term:
            term = f"%{intent.clean_search_term}%"
            query = query.filter(StudyEvidence.content.ilike(term))
            
        results = query.limit(limit).all()
        
        return [SearchResult(
            id=s.id,
            result_type=SearchResultType.STUDY_MATERIAL,
            title=f"Study Extract: {s.document.title if s.document else 'Unknown'}",
            text_snippet=s.content[:200] if s.content else "",
            subject=s.document.subject if s.document else None,
            relevance_score=0.85,
            provenance_url=s.document.original_url if s.document else None,
            attribution=s.document.source if s.document else "Unknown Source"
        ) for s in results]

    def search(self, query: SearchQuery) -> list[SearchResult]:
        intent = self._parse_intent(query.raw_query)
        filters = query.filters or SearchFilters()
        
        results = []
        
        # Route to specific handlers if intent is strong
        if intent.target_type == SearchResultType.EXAM_QUESTION:
            # Need to fix Section import inside function to avoid circular/missing import
            from backend.models.core import Section
            results = self._hybrid_search_questions(intent, filters, query.limit)
        elif intent.target_type == SearchResultType.CONCEPT:
            results = self._hybrid_search_concepts(intent, filters, query.limit)
        elif intent.target_type == SearchResultType.STUDY_MATERIAL:
            results = self._hybrid_search_study_material(intent, filters, query.limit)
        else:
            # Broad search (scatter-gather)
            from backend.models.core import Section
            q_res = self._hybrid_search_questions(intent, filters, limit=max(3, query.limit // 3))
            c_res = self._hybrid_search_concepts(intent, filters, limit=max(3, query.limit // 3))
            s_res = self._hybrid_search_study_material(intent, filters, limit=max(3, query.limit // 3))
            results = q_res + c_res + s_res
            
        # Sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:query.limit]
