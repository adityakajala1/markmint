from pydantic import BaseModel
from typing import Optional


# Course Schemas
class CourseBase(BaseModel):
    name: str
    code: str


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True


# Exam Schemas
class ExamBase(BaseModel):
    year: int
    term: str


class ExamCreate(ExamBase):
    course_id: int


class Exam(ExamBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True


# Section Schemas
class SectionBase(BaseModel):
    name: str
    instructions: Optional[str] = None


class SectionCreate(SectionBase):
    exam_id: int


class Section(SectionBase):
    id: int
    exam_id: int

    class Config:
        from_attributes = True


# Topic Schemas
class TopicBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class TopicCreate(TopicBase):
    pass


class Topic(TopicBase):
    id: int

    class Config:
        from_attributes = True


# Question Schemas
class QuestionBase(BaseModel):
    question_number: str
    original_text: str
    normalized_text: Optional[str] = None
    marks: Optional[float] = None
    question_type: Optional[str] = None
    cognitive_level: Optional[str] = None
    difficulty: Optional[float] = None


class QuestionCreate(QuestionBase):
    section_id: int


class Question(QuestionBase):
    id: int
    section_id: int

    class Config:
        from_attributes = True
