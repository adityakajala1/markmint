# -*- coding: utf-8 -*-
import re
with open('src/app/developers/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = re.sub(r"I'm coding! [^\"']+", "I'm coding! 💻", code)

with open('src/app/developers/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
