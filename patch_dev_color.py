import os

file_path = 'src/app/developers/page.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Built, designed, engineered, and maintained by :', '<span className="text-accent">Built, designed, engineered, and maintained</span> by :')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
