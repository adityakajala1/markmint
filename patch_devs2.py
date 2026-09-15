import re

file_path = 'src/app/developers/page.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix The Duo
content = re.sub(r'The Team', 'The Duo', content)

# Fix subtitle
content = re.sub(r'Built, designed, engineered, and maintained by.*?students\.</.*?>', 'Built, designed, engineered, and maintained by :', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
