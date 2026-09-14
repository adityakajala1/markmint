import os

file_path = 'src/app/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_p = 'Chat with our custom AI to get instant, accurate answers about your syllabus, exams, and academic policies. Includes the Mint+ GPA Calculator for tracking your grades.'
new_p = 'MintAi generates structured study plans, filters important PYQs, and predicts upcoming CT, FT, and End Sem question papers. Get probable questions, answers, and predicted papers instantly. Includes the Mint+ GPA Calculator.'

content = content.replace(old_p, new_p)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
