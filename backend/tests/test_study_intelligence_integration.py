import pytest
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.database import Base
from backend.models.core import Course, Topic, Document, StudyEvidence, Concept, Unit, Syllabus, StudentTopicProgress
from backend.services.study_intelligence import StudyIntelligenceService, PriorityResult, StudyPriority
from backend.services.student_uploads import StudentUploadService
from backend.services.prediction.engine import PredictionResult

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

def test_topic_resource_matching_and_course_isolation(db_session):
    # Setup test data
    c1 = Course(name="Calculus", code="CALC101")
    c2 = Course(name="Chemistry", code="CHEM101")
    db_session.add_all([c1, c2])
    db_session.commit()
    
    syl1 = Syllabus(course_id=c1.id, version="v1")
    db_session.add(syl1)
    db_session.commit()
    
    u1 = Unit(syllabus_id=syl1.id, name="Unit 1", number=1)
    db_session.add(u1)
    db_session.commit()
    
    t1 = Topic(unit_id=u1.id, name="Matrices")
    t2 = Topic(unit_id=u1.id, name="Integration")
    db_session.add_all([t1, t2])
    db_session.commit()
    
    from backend.models.core import MappingConfidence
    concept1 = Concept(canonical_name="Matrices", unit_id=u1.id)
    db_session.add(concept1)
    db_session.commit()
    
    # Create some documents
    doc_local = Document(document_hash="h1", title="Local Notes", source="local", resource_type="lecture notes", subject="Calculus")
    doc_studique = Document(document_hash="h2", title="Studique PYQ", source="studique", resource_type="examination papers / PYQs", subject="Calculus")
    doc_upload = Document(document_hash="h3", title="My Notes", source="student_upload", owner_id="user1", subject="Calculus")
    db_session.add_all([doc_local, doc_studique, doc_upload])
    db_session.commit()
    
    # Link them to concept via StudyEvidence
    ev1 = StudyEvidence(document_id=doc_local.id, concept_id=concept1.id, knowledge_type="definition", content="A", original_text="A", confidence=MappingConfidence.HIGH)
    ev2 = StudyEvidence(document_id=doc_studique.id, concept_id=concept1.id, knowledge_type="context", content="B", original_text="B", confidence=MappingConfidence.HIGH)
    ev3 = StudyEvidence(document_id=doc_upload.id, concept_id=concept1.id, knowledge_type="formula", content="C", original_text="C", confidence=MappingConfidence.HIGH)
    db_session.add_all([ev1, ev2, ev3])
    db_session.commit()

    svc = StudyIntelligenceService(db_session)
    
    # Test Resource Matching
    resources = svc.get_topic_resources("Matrices", c1.id)
    assert len(resources) == 3
    sources = [r["source"] for r in resources]
    assert "local" in sources
    assert "studique" in sources
    assert "student_upload" in sources
    
    # Test No Resource State
    resources_empty = svc.get_topic_resources("Integration", c1.id)
    assert len(resources_empty) == 0
    
    # Test Course Isolation
    resources_isolated = svc.get_topic_resources("Matrices", c2.id)
    # The topic does not belong to c2
    assert len(resources_isolated) == 0

def test_progress_foundation(db_session):
    c1 = Course(name="Calculus", code="CALC101")
    db_session.add(c1)
    db_session.commit()
    syl1 = Syllabus(course_id=c1.id, version="v1")
    db_session.add(syl1)
    db_session.commit()
    u1 = Unit(syllabus_id=syl1.id, name="Unit 1", number=1)
    db_session.add(u1)
    db_session.commit()
    t1 = Topic(unit_id=u1.id, name="Matrices")
    db_session.add(t1)
    db_session.commit()

    svc = StudyIntelligenceService(db_session)
    
    # Start studying
    p1 = svc.record_progress(user_id="user1", course_id=c1.id, topic_id=t1.id, status="STARTED")
    assert p1.status == "STARTED"
    assert p1.practice_attempted == 0
    
    # Complete and practice
    p3 = svc.record_progress(user_id="user1", course_id=c1.id, topic_id=t1.id, status="COMPLETED", practice_attempted=True, practice_accuracy=0.8)
    
    assert p3.status == "COMPLETED"
    assert p3.practice_attempted == 1
    assert p3.practice_correct == 1
    assert p3.last_studied_at is not None


def test_prediction_to_priority_is_explainable_and_deterministic(db_session):
    course = Course(name="Calculus", code="CALC102")
    db_session.add(course)
    db_session.commit()
    syllabus = Syllabus(course_id=course.id, version="v1")
    db_session.add(syllabus)
    db_session.commit()
    unit = Unit(syllabus_id=syllabus.id, name="Unit 1", number=1)
    db_session.add(unit)
    db_session.commit()
    topic = Topic(unit_id=unit.id, name="Eigenvalues")
    db_session.add(topic)
    db_session.commit()

    prediction = PredictionResult(
        target="topic",
        name="Eigenvalues",
        rank=1,
        score=0.82,
        confidence="HIGH",
        evidence={"occurrences": 4, "recent_freq": 0.4},
    )
    service = StudyIntelligenceService(db_session)

    first = service.generate_study_plan([prediction], course.id, "student-1")
    second = service.generate_study_plan([prediction], course.id, "student-1")

    assert first == second
    assert first[0]["priority"] == StudyPriority.VERY_HIGH
    assert "Very high predicted exam probability." in first[0]["reasons"]
    assert "Appears repeatedly in historical papers." in first[0]["reasons"]
    assert "No trusted topic-mapped study material is available." in first[0]["reasons"]


def test_student_upload_uses_existing_taxonomy_only(db_session, monkeypatch):
    course = Course(name="Calculus", code="CALC103")
    db_session.add(course)
    db_session.commit()
    syllabus = Syllabus(course_id=course.id, version="v1")
    db_session.add(syllabus)
    db_session.commit()
    unit = Unit(syllabus_id=syllabus.id, name="Unit 1", number=1)
    db_session.add(unit)
    db_session.commit()
    topic = Topic(unit_id=unit.id, name="Matrices")
    concept = Concept(canonical_name="Matrices", unit_id=unit.id)
    db_session.add_all([topic, concept])
    db_session.commit()

    from backend.services.extraction.pdf_parser import PDFParser

    monkeypatch.setattr(
        PDFParser,
        "extract_text_with_pages",
        lambda _stream: [{"page_number": 1, "text": "1. Matrices\nDefinition: A matrix."}],
    )
    path = Path("scratch") / "test_notes_upload.pdf"
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(b"test pdf bytes")

    document = StudentUploadService(db_session).process_student_upload(
        str(path), "notes.pdf", course.id, "student-1"
    )

    assert document.processing_status == "completed"
    evidence = db_session.query(StudyEvidence).filter_by(
        document_id=document.id, concept_id=concept.id
    ).one()
    assert evidence.concept_id == concept.id
    assert evidence.confidence.name == "HIGH"
    assert StudyIntelligenceService(db_session).get_topic_resources("Matrices", course.id)
    path.unlink(missing_ok=True)
