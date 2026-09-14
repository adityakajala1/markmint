import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.core import Base, Concept, ConceptAlias, MappingConfidence, ConceptStatus
from app.services.concept.engine import ConceptIntelligenceEngine
from app.services.concept.normalizer import ConceptNormalizer

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_concept_normalizer_exact_alias(db_session):
    normalizer = ConceptNormalizer(db_session)
    
    # Create existing concept
    concept = Concept(canonical_name="AVL Tree", subject="Computer Science", status=ConceptStatus.CANONICAL)
    db_session.add(concept)
    db_session.commit()
    
    alias = ConceptAlias(concept_id=concept.id, alias="avl tree", confidence=MappingConfidence.HIGH)
    db_session.add(alias)
    db_session.commit()
    
    # Test resolution
    resolved_concept, confidence = normalizer.resolve_concept("AVL tree", subject="Computer Science")
    
    assert resolved_concept.id == concept.id
    assert confidence == MappingConfidence.HIGH

def test_concept_normalizer_cross_subject_ambiguity(db_session):
    normalizer = ConceptNormalizer(db_session)
    
    # Create CS concept
    concept_cs = Concept(canonical_name="Bank", subject="Computer Science", status=ConceptStatus.CANONICAL)
    db_session.add(concept_cs)
    db_session.commit()
    
    # Try resolving 'Bank' for Finance. Should NOT merge with CS 'Bank'.
    resolved_concept, confidence = normalizer.resolve_concept("Bank", subject="Finance")
    
    assert resolved_concept.id != concept_cs.id
    assert resolved_concept.subject == "Finance"
    assert resolved_concept.status == ConceptStatus.UNRESOLVED
    assert confidence == MappingConfidence.UNRESOLVED

def test_concept_normalizer_creates_unresolved(db_session):
    normalizer = ConceptNormalizer(db_session)
    
    resolved_concept, confidence = normalizer.resolve_concept("Totally New Concept")
    
    assert resolved_concept.canonical_name == "Totally New Concept"
    assert resolved_concept.status == ConceptStatus.UNRESOLVED
    assert confidence == MappingConfidence.UNRESOLVED

    # Check that alias was registered to this unresolved concept
    alias = db_session.query(ConceptAlias).filter(ConceptAlias.alias == "Totally New Concept").first()
    assert alias.concept_id == resolved_concept.id
    assert alias.confidence == MappingConfidence.UNRESOLVED

def test_evidence_segregation(db_session):
    from app.models.core import Document, StudyEvidence
    
    engine = ConceptIntelligenceEngine(db_session)
    
    # Create a Concept
    concept = Concept(canonical_name="Deadlock", subject="Computer Science", status=ConceptStatus.CANONICAL)
    db_session.add(concept)
    
    # Create a Study Document
    doc = Document(document_hash="abc", resource_type="lecture notes")
    db_session.add(doc)
    db_session.commit()
    
    # Add 10 StudyEvidences for this Concept
    for i in range(10):
        ev = StudyEvidence(document_id=doc.id, concept_id=concept.id, knowledge_type="definition", content=f"def {i}", original_text=f"txt {i}")
        db_session.add(ev)
    db_session.commit()
    
    # Retrieve evidence report
    report = engine.get_concept_evidence(concept.id)
    
    assert report is not None
    assert report.study_evidence.number_of_evidence_chunks == 10
    
    # CRITICAL: Exam evidence must remain completely untouched
    assert report.exam_evidence.number_of_papers == 0
    assert report.exam_evidence.number_of_questions == 0
    assert report.exam_evidence.total_marks == 0.0

