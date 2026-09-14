import os

file_path = 'src/app/developers/page.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_text = '<span className="text-accent">Built, designed, engineered, </span>and<span className="text-accent"> maintained</span> by :'
new_text = '<span className="text-accent">Built, designed, engineered </span>and<span className="text-accent"> maintained</span> by :'

content = content.replace(old_text, new_text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
