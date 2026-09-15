import os

file_path = 'src/app/developers/page.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace The Team with The Duo
content = content.replace('>The Team<', '>The Duo<')
content = content.replace('"The Team"', '"The Duo"')
content = content.replace('> The Team <', '> The Duo <')

# Replace subtitle text
content = content.replace('Built, designed, engineered, and maintained by students.', 'Built, designed, engineered, and maintained by :')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
