import os
import re

file_path = 'src/app/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the Horizontal Padding (match Navbar's px-6 md:px-10) and Vertical Padding (reduce pt/py)
old_main = '<main id="main-content" className="flex-1 flex flex-col items-start justify-center w-full px-8 md:px-16 pt-8 pb-16">'
new_main = '<main id="main-content" className="flex-1 flex flex-col items-start justify-start w-full px-6 md:px-10 pt-4 pb-16">'

old_section = '<section className="relative z-10 max-w-3xl py-16">'
new_section = '<section className="relative z-10 max-w-4xl pt-8 pb-16">'

content = content.replace(old_main, new_main)
content = content.replace(old_section, new_section)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
