# -*- coding: utf-8 -*-
import re
with open('src/app/developers/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'const msg = dev\.name\.includes\("Aditya"\) \? "[^"]+" : "[^"]+";'
replacement = 'const msg = dev.name.includes("Aditya") ? "Listening to music \\U0001f3a7" : "Larping \\U0001f9d9\\u200d\\u2642\\ufe0f";'
code = re.sub(pattern, replacement, code)

with open('src/app/developers/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)