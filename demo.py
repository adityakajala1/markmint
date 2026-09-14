import json
import os

# FORCE SQLITE FOR DEMO
os.environ['DATABASE_URL'] = 'sqlite:///./demo.db'

from app.core.database import SessionLocal, Base, engine
from app.models.core import Course, Topic, Unit
from app.services.exam import ExamService

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 1. Clean up old demo data if it exists
db.query(Course).filter(Course.code == 'CS301').delete()
db.commit()

# 2. Create Course
course = Course(name='Data Structures and Algorithms', code='CS301')
db.add(course)
db.commit()
db.refresh(course)

# 3. Simulate Extracted Data from 3 Historical Exams
historical_extractions = [
    {
        'year': 2021, 'term': 'Fall',
        'extraction': {
            'sections': [
                {'name': 'Section A', 'questions': [
                    {'question_number': '1', 'original_text': 'Explain AVL Trees', 'marks': 10.0},
                    {'question_number': '2', 'original_text': 'What is a Hash Table?', 'marks': 5.0}
                ]}
            ]
        }
    },
    {
        'year': 2022, 'term': 'Fall',
        'extraction': {
            'sections': [
                {'name': 'Section A', 'questions': [
                    {'question_number': '1', 'original_text': 'Implement AVL Tree insertion', 'marks': 15.0},
                    {'question_number': '2', 'original_text': 'Compare BFS and DFS', 'marks': 10.0}
                ]}
            ]
        }
    },
    {
        'year': 2023, 'term': 'Fall',
        'extraction': {
            'sections': [
                {'name': 'Section A', 'questions': [
                    {'question_number': '1', 'original_text': 'Write AVL Tree rotation logic', 'marks': 15.0},
                    {'question_number': '2', 'original_text': 'Explain Graph coloring', 'marks': 5.0},
                    {'question_number': '3', 'original_text': 'Hash collision resolution', 'marks': 10.0}
                ]}
            ]
        }
    }
]

# 4. Import the mock extractions using our real pipeline
svc = ExamService(db)
exam_ids = []
for ex in historical_extractions:
    exam = svc.import_extraction(course_id=course.id, year=ex['year'], term=ex['term'], extraction_data=ex['extraction'])
    exam_ids.append(exam.id)
    
    # Manually assign topics to simulate the Classification Engine (Phase 3)
    for sec in exam.sections:
        for q in sec.questions:
            if 'AVL' in q.original_text:
                topic = db.query(Topic).filter_by(name='AVL Trees').first()
                if not topic:
                    topic = Topic(name='AVL Trees', unit_id=1)
                    db.add(topic)
                q.topics.append(topic)
            elif 'Hash' in q.original_text:
                topic = db.query(Topic).filter_by(name='Hashing').first()
                if not topic:
                    topic = Topic(name='Hashing', unit_id=2)
                    db.add(topic)
                q.topics.append(topic)
    db.commit()

# 5. Generate Exam DNA & Predictions using the last exam as reference
print('=========================================')
print('?? EXAM DNA RESULTS (Historical Aggregation)')
print('=========================================')
dna = svc.get_exam_dna(exam_ids[-1])
print(json.dumps(dna.model_dump(), indent=2))

print('\n=========================================')
print('?? EXAM PREDICTIONS (Recency-Weighted)')
print('=========================================')
preds = svc.get_exam_predictions(exam_ids[-1])
print(json.dumps(preds.model_dump(), indent=2))

db.close()
