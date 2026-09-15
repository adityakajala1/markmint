import os

file_path = 'src/app/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix em dash and weird encoding
content = content.replace('MintAi—our', 'MintAi, our')
# If it encoded weirdly, fallback replace:
import re
content = re.sub(r'MintAi.*?our', 'MintAi, our', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
