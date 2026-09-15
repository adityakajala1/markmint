import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Text, Boolean, Enum as SQLEnum, DateTime, JSON
from sqlalchemy.orm import relationship

from backend.core.database import Base

class MappingConfidence(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNRESOLVED = "UNRESOLVED"

class ConceptStatus(str, enum.Enum):
    CANONICAL = "CANONICAL"
    PROVISIONAL = "PROVISIONAL"
    UNRESOLVED = "UNRESOLVED"

# Self-referential concept relationship
concept_relationship = Table(
    "concept_relationship",
    Base.metadata,
    Column("concept_a_id", Integer, ForeignKey("concepts.id"), primary_key=True),
    Column("concept_b_id", Integer, ForeignKey("concepts.id"), primary_key=True),
    Column("relationship_type", String, nullable=False, default="related")
)

# Syllabus <-> Concept explicit mapping
syllabus_concept = Table(
    "syllabus_concept",
    Base.metadata,
    Column("unit_id", Integer, ForeignKey("units.id"), primary_key=True),
    Column("concept_id", Integer, ForeignKey("concepts.id"), primary_key=True)
)

# Many-to-many for Question and Concept with confidence
class QuestionConcept(Base):
    __tablename__ = "question_concept"
    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), primary_key=True, index=True)
    confidence = Column(SQLEnum(MappingConfidence), default=MappingConfidence.UNRESOLVED)

    question = relationship("Question", back_populates="concept_associations")
    concept = relationship("Concept", back_populates="question_associations")

# Legacy Many-to-many for Question and Topic (Syllabus mapping)
question_topic = Table(
    "question_topic",
    Base.metadata,
    Column("question_id", Integer, ForeignKey("questions.id"), primary_key=True),
    Column("topic_id", Integer, ForeignKey("topics.id"), primary_key=True),
)


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    
    # Metadata
    source = Column(String, nullable=True)
    original_url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    semester = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    owner_id = Column(String, nullable=True, index=True)
    processing_status = Column(String, nullable=True)
    uploaded_at = Column(DateTime, nullable=True)
    
    # Classification
    resource_type = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    exam_type = Column(String, nullable=True)
    
    # Tracking
    document_hash = Column(String, unique=True, index=True, nullable=False)
    extraction_status = Column(String, nullable=False, default="pending")
    extraction_confidence = Column(Float, nullable=True)

    exams = relationship("Exam", back_populates="document")
    study_evidences = relationship("StudyEvidence", back_populates="document")


class Concept(Base):
    """Canonical representation of a topic/concept."""
    __tablename__ = "concepts"
    id = Column(Integer, primary_key=True, index=True)
    canonical_name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # New fields for intelligence engine
    subject = Column(String, nullable=True) # To prevent cross-subject ambiguity
    status = Column(SQLEnum(ConceptStatus), default=ConceptStatus.CANONICAL)
    parent_id = Column(Integer, ForeignKey("concepts.id"), nullable=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True, index=True)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id"), nullable=True, index=True)

    parent = relationship("Concept", remote_side=[id], back_populates="children")
    children = relationship("Concept", back_populates="parent")
    
    related_concepts = relationship(
        "Concept",
        secondary=concept_relationship,
        primaryjoin=id==concept_relationship.c.concept_a_id,
        secondaryjoin=id==concept_relationship.c.concept_b_id
    )

    aliases = relationship("ConceptAlias", back_populates="concept")
    study_evidences = relationship("StudyEvidence", back_populates="concept")
    question_associations = relationship("QuestionConcept", back_populates="concept")


class ConceptAlias(Base):
    """String matches mapped to a canonical concept."""
    __tablename__ = "concept_aliases"
    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True, index=True) # Nullable if UNRESOLVED
    alias = Column(String, unique=True, index=True, nullable=False)
    confidence = Column(SQLEnum(MappingConfidence), default=MappingConfidence.UNRESOLVED)

    concept = relationship("Concept", back_populates="aliases")


class StudyEvidence(Base):
    """Knowledge extracted from lecture notes or study material."""
    __tablename__ = "study_evidences"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True, index=True)
    
    knowledge_type = Column(String, nullable=False) # 'definition', 'formula', 'algorithm', 'context'
    content = Column(Text, nullable=False)
    original_text = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    confidence = Column(SQLEnum(MappingConfidence), default=MappingConfidence.UNRESOLVED)

    document = relationship("Document", back_populates="study_evidences")
    concept = relationship("Concept", back_populates="study_evidences")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)

    exams = relationship("Exam", back_populates="course")
    syllabuses = relationship("Syllabus", back_populates="course")


class Syllabus(Base):
    __tablename__ = "syllabuses"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    version = Column(String, nullable=False)

    course = relationship("Course", back_populates="syllabuses")
    units = relationship("Unit", back_populates="syllabus")


class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabuses.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    number = Column(Integer, nullable=False)

    syllabus = relationship("Syllabus", back_populates="units")
    topics = relationship("Topic", back_populates="unit")


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)
    name = Column(String, nullable=False)

    unit = relationship("Unit", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic")
    questions = relationship("Question", secondary=question_topic, back_populates="topics")


class Subtopic(Base):
    __tablename__ = "subtopics"
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)
    name = Column(String, nullable=False)

    topic = relationship("Topic", back_populates="subtopics")


class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), unique=True, nullable=True, index=True)
    year = Column(Integer, nullable=True) # Nullable to support exams missing year metadata
    term = Column(String, nullable=True)
    assessment_type = Column(String, nullable=True)

    course = relationship("Course", back_populates="exams")
    document = relationship("Document", back_populates="exams")
    sections = relationship("Section", back_populates="exam")


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    instructions = Column(Text, nullable=True)

    exam = relationship("Exam", back_populates="sections")
    questions = relationship("Question", back_populates="section")


class QuestionFamily(Base):
    __tablename__ = "question_families"
    id = Column(Integer, primary_key=True, index=True)
    canonical_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String, nullable=False, index=True)
    first_seen_year = Column(Integer, nullable=True)
    latest_seen_year = Column(Integer, nullable=True)
    repetition_type = Column(String, nullable=True)

    questions = relationship("Question", back_populates="family")
    memberships = relationship("QuestionFamilyMembership", back_populates="family")


class QuestionFamilyMembership(Base):
    __tablename__ = "question_family_memberships"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    family_id = Column(Integer, ForeignKey("question_families.id"), nullable=False, index=True)
    match_type = Column(String, nullable=False)
    similarity_score = Column(Float, nullable=True)
    decision_method = Column(String, nullable=False)
    algorithm_version = Column(String, nullable=False)

    question = relationship("Question", back_populates="memberships")
    family = relationship("QuestionFamily", back_populates="memberships")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False, index=True)
    family_id = Column(Integer, ForeignKey("question_families.id"), nullable=True, index=True)

    question_number = Column(String, nullable=False)
    original_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=True)
    marks = Column(Float, nullable=True)
    is_alternative = Column(Boolean, default=False, nullable=False)
    structured_content = Column(JSON, nullable=True)
    needs_review = Column(Boolean, default=False, nullable=False)
    extraction_method = Column(String, nullable=True)
    extraction_confidence = Column(Float, nullable=True)

    question_type = Column(String, nullable=True)
    cognitive_level = Column(String, nullable=True)
    difficulty = Column(Float, nullable=True)
    classification_confidence = Column(Float, nullable=True)
    classification_input = Column(Text, nullable=True)
    classification_metadata = Column(JSON, nullable=True)

    section = relationship("Section", back_populates="questions")
    topics = relationship("Topic", secondary=question_topic, back_populates="questions")
    concept_associations = relationship("QuestionConcept", back_populates="question")
    family = relationship("QuestionFamily", back_populates="questions")
    memberships = relationship("QuestionFamilyMembership", back_populates="question")
    evidences = relationship("Evidence", back_populates="question")


class Evidence(Base):
    __tablename__ = "evidences"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)

    question = relationship("Question", back_populates="evidences")

class StudentTopicProgress(Base):
    __tablename__ = 'student_topic_progress'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False, index=True)
    
    status = Column(String, nullable=False, default='NOT_STARTED')
    practice_attempted = Column(Integer, default=0)
    practice_correct = Column(Integer, default=0)
    last_studied_at = Column(DateTime, nullable=True)
    
    topic = relationship('Topic')

class StudentResourceProgress(Base):
    __tablename__ = 'student_resource_progress'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, nullable=False, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False, index=True)
    
    viewed = Column(Boolean, default=False)
    last_viewed_at = Column(DateTime, nullable=True)
    
    document = relationship('Document')
