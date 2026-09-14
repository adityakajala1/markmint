import re
import sys
import glob

def resolve_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find conflict blocks
    def replacer(match):
        # match.group(1) is HEAD part, match.group(2) is main part
        main_part = match.group(2)
        # We prefer main's architecture (schemas, flattened structure) 
        # but it uses 'app.', so we replace 'app.' with 'backend.'
        resolved = main_part.replace('from app.', 'from backend.').replace('import app.', 'import backend.')
        return resolved

    new_content = re.sub(
        r'<<<<<<< HEAD.*?\n(.*?)=======\n(.*?)>>>>>>> main.*?\n',
        replacer,
        content,
        flags=re.DOTALL
    )
    
    # We also want to replace any other stray `app.` imports in the rest of the file that might have come from main
    new_content = re.sub(r'^from app\.', 'from backend.', new_content, flags=re.MULTILINE)
    new_content = re.sub(r'^import app\.', 'import backend.', new_content, flags=re.MULTILINE)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Resolved {filepath}")

# Find all conflicted files
conflicted_files = [
    'backend/api/endpoints/courses.py',
    'backend/api/endpoints/exams.py',
    'backend/api/endpoints/papers.py',
    'backend/services/course.py',
    'backend/services/dna/analyzer.py',
    'backend/services/exam.py',
    'backend/services/extraction/question_extractor.py',
    'backend/services/prediction/engine.py',
    'backend/services/question_classifier.py',
    'backend/services/similarity.py',
    'backend/tests/test_classification.py',
    'backend/tests/test_similarity.py'
]

for file in conflicted_files:
    resolve_file(file)
