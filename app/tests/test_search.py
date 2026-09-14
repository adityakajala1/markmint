import pytest
from app.schemas import SearchQuery, SearchResultType, SearchFilters
from app.services.search.discovery import DiscoverySearchEngine

def test_intent_parsing_marks_and_type():
    engine = DiscoverySearchEngine(db=None) # DB not needed for parsing
    
    # 1. "5 mark questions on normalization"
    intent1 = engine._parse_intent("5 mark questions on normalization")
    assert intent1.target_type == SearchResultType.EXAM_QUESTION
    assert intent1.extracted_marks == 5.0
    assert "normalization" in intent1.clean_search_term
    assert "questions" not in intent1.clean_search_term

    # 2. "what keeps coming in DBMS"
    intent2 = engine._parse_intent("what keeps coming in DBMS")
    assert intent2.target_type == SearchResultType.QUESTION_FAMILY
    assert "dbms" in intent2.clean_search_term
    assert "what" not in intent2.clean_search_term

    # 3. "topics increasing recently"
    intent3 = engine._parse_intent("topics increasing recently")
    assert intent3.target_type == SearchResultType.ANALYSIS_FINDING
    assert "increasing" in intent3.clean_search_term # Actually we didn't strip increasing

from unittest.mock import patch

def test_search_routing():
    engine = DiscoverySearchEngine(db=None)
    
    # Mock the underlying DB search methods
    with patch.object(engine, '_hybrid_search_questions', return_value=[]) as mock_q, \
         patch.object(engine, '_hybrid_search_concepts', return_value=[]) as mock_c, \
         patch.object(engine, '_hybrid_search_study_material', return_value=[]) as mock_s:
        
        # Target Type: Concept
        query = SearchQuery(raw_query="concept of AVL tree")
        engine.search(query)
        mock_c.assert_called_once()
        mock_q.assert_not_called()
        
        # Reset mocks
        mock_q.reset_mock()
        mock_c.reset_mock()
        mock_s.reset_mock()

        # Broad query
        query2 = SearchQuery(raw_query="avl tree")
        engine.search(query2)
        # Should call all three
        mock_c.assert_called_once()
        mock_q.assert_called_once()
        mock_s.assert_called_once()
