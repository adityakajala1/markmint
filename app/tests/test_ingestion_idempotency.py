import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.core import Base, Course, Document, Exam, Section, Question
from app.services.document import DocumentService

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Setup base course
    course = Course(name="Test Course", code="TC101")
    session.add(course)
    session.commit()
    
    yield session
    
    session.close()

def test_ingest_same_document_twice(db_session):
    svc = DocumentService(db_session)
    course = db_session.query(Course).first()
    
    doc = svc.get_or_create_document(document_hash="hash123")
    extraction = {
        "sections": [
            {"name": "A", "questions": [{"marks": 5}]}
        ]
    }
    
    # First ingest
    svc.import_exam_extraction(doc.id, course.id, 2023, "Fall", extraction)
    assert db_session.query(Exam).count() == 1
    assert db_session.query(Section).count() == 1
    assert db_session.query(Question).count() == 1
    
    # Second ingest (simulate rerunning feeder script)
    svc.import_exam_extraction(doc.id, course.id, 2023, "Fall", extraction)
    
    # Verify exactly one exam and no duplicate questions
    assert db_session.query(Exam).count() == 1
    assert db_session.query(Section).count() == 1
    assert db_session.query(Question).count() == 1

def test_ingest_duplicate_url(db_session):
    svc = DocumentService(db_session)
    course = db_session.query(Course).first()
    
    # First doc
    doc1 = svc.get_or_create_document(document_hash="hash_a", original_url="http://test.com/exam.pdf")
    svc.import_exam_extraction(doc1.id, course.id, 2023, "Fall", {})
    
    # Second doc with different hash (e.g. timestamp changed) but same URL
    doc2 = svc.get_or_create_document(document_hash="hash_b", original_url="http://test.com/exam.pdf")
    
    assert doc1.id == doc2.id # Should resolve to the same logical document
    
    # Re-ingest
    svc.import_exam_extraction(doc2.id, course.id, 2023, "Fall", {})
    assert db_session.query(Exam).count() == 1

def test_simulate_partial_failure_and_rerun(db_session):
    svc = DocumentService(db_session)
    course = db_session.query(Course).first()
    
    doc = svc.get_or_create_document(document_hash="hash_fail")
    
    # Simulate a partial failure (e.g., crashed during section insertion)
    partial_exam = Exam(course_id=course.id, document_id=doc.id, year=2023, term="Fall")
    db_session.add(partial_exam)
    db_session.commit()
    
    assert db_session.query(Exam).count() == 1
    assert db_session.query(Section).count() == 0
    
    # Rerun ingestion properly
    extraction = {
        "sections": [
            {"name": "A", "questions": [{"marks": 10}]}
        ]
    }
    svc.import_exam_extraction(doc.id, course.id, 2023, "Fall", extraction)
    
    # Should clean up the partial exam and insert fully
    assert db_session.query(Exam).count() == 1
    assert db_session.query(Section).count() == 1
    assert db_session.query(Question).count() == 1
