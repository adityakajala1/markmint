# -*- coding: utf-8 -*-
with open('src/components/layout/footer.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# Add Last Updated string
if 'Last Updated:' not in code:
    code = code.replace('<span>Built for SRMIST students</span>', '<span>Last Updated: Sep 2026</span>\n          <span className="w-1.5 h-1.5 rounded-full bg-accent"></span>\n          <span>Built for SRMIST students</span>')

with open('src/components/layout/footer.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
