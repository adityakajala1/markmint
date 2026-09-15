# -*- coding: utf-8 -*-
with open('src/components/ambient/HangingLamp.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# Add custom styling for smaller toast
small_style = ', style: { fontSize: "13px", padding: "8px 14px", minHeight: "36px", width: "fit-content", marginLeft: "auto" }'
code = re.sub(r'toast\("Switched to Aditya", \{ duration: 1000 \}\);', f'toast("Switched to Aditya", {{ duration: 1000{small_style} }});', code)
code = re.sub(r'toast\("Switched to Naman", \{ duration: 1000 \}\);', f'toast("Switched to Naman", {{ duration: 1000{small_style} }});', code)

with open('src/components/ambient/HangingLamp.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
