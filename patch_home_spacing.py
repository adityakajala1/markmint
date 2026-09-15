import os
import re

file_path = 'src/app/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Change main layout from centered to left-aligned
old_main = '<main id="main-content" className="flex-1 flex flex-col items-center justify-center w-full max-w-7xl mx-auto px-8 md:px-16 pt-16">'
new_main = '<main id="main-content" className="flex-1 flex flex-col items-start justify-center w-full px-8 md:px-16 pt-8 pb-16">'

content = content.replace(old_main, new_main)

# Also ensure FAQ section matches the left alignment
old_faq = '<section className="w-full max-w-3xl py-16 mb-16 border-t border-border mt-8">'
new_faq = '<section className="w-full max-w-4xl py-16 mb-16 border-t border-border mt-16">'

content = content.replace(old_faq, new_faq)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
