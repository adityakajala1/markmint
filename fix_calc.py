# -*- coding: utf-8 -*-
import re

with open('src/components/calculator/ScopeCalculator.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = re.sub(r'toast\("Calculated: You need a time machine[^"]+", \{ duration: 3000 \}\);', 'toast("Calculated: You need a time machine. ⏳", { duration: 3000 });', code)
code = re.sub(r'toast\("Academic Weapon Detected[^"]+", \{ duration: 3000 \}\);', 'toast("Academic Weapon Detected 🎯", { duration: 3000 });', code)

with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
