import os

file_path = 'src/app/developers/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('rounded-md p-8', 'rounded-2xl p-8 cursor-pointer')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
