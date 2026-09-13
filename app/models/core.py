from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Text
from sqlalchemy.orm import relationship

from app.core.database import Base

question_topic = Table(
    "question_topic",
    Base.metadata,
    Column("question_id", Integer, ForeignKey("questions.id"), primary_key=True),
    Column("topic_id", Integer, ForeignKey("topics.id"), primary_key=True),
)


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
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    version = Column(String, nullable=False)

    course = relationship("Course", back_populates="syllabuses")
    units = relationship("Unit", back_populates="syllabus")


class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabuses.id"), nullable=False)
    name = Column(String, nullable=False)
    number = Column(Integer, nullable=False)

    syllabus = relationship("Syllabus", back_populates="units")
    topics = relationship("Topic", back_populates="unit")


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    name = Column(String, nullable=False)

    unit = relationship("Unit", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic")
    questions = relationship("Question", secondary=question_topic, back_populates="topics")


class Subtopic(Base):
    __tablename__ = "subtopics"
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    name = Column(String, nullable=False)

    topic = relationship("Topic", back_populates="subtopics")


class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    year = Column(Integer, nullable=False)
    term = Column(String, nullable=False)

    course = relationship("Course", back_populates="exams")
    sections = relationship("Section", back_populates="exam")


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    name = Column(String, nullable=False)
    instructions = Column(Text, nullable=True)

    exam = relationship("Exam", back_populates="sections")
    questions = relationship("Question", back_populates="section")


class QuestionFamily(Base):
    __tablename__ = "question_families"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    repetition_type = Column(String, nullable=False)

    questions = relationship("Question", back_populates="family")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    family_id = Column(Integer, ForeignKey("question_families.id"), nullable=True)

    question_number = Column(String, nullable=False)
    original_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=True)
    marks = Column(Float, nullable=True)

    question_type = Column(String, nullable=True)
    cognitive_level = Column(String, nullable=True)
    difficulty = Column(Float, nullable=True)
    classification_confidence = Column(Float, nullable=True)

    section = relationship("Section", back_populates="questions")
    topics = relationship("Topic", secondary=question_topic, back_populates="questions")
    family = relationship("QuestionFamily", back_populates="questions")
    evidences = relationship("Evidence", back_populates="question")


class Evidence(Base):
    __tablename__ = "evidences"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    description = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)

    question = relationship("Question", back_populates="evidences")
