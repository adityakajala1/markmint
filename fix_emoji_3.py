# -*- coding: utf-8 -*-
import re
with open('src/app/developers/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# I will use Python's raw string literal to match the corrupted text, but honestly it's safer to just replace the whole ternary line
pattern = r'const msg = dev\.name\.includes\("Aditya"\) \? "[^"]+" : "[^"]+";'
replacement = 'const msg = dev.name.includes("Aditya") ? "Listening to music 🎧" : "Larping 🧙‍♂️";'
code = re.sub(pattern, replacement, code)

with open('src/app/developers/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
