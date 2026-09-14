# -*- coding: utf-8 -*-
with open('src/components/layout/footer.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re
replacement = '''<a href="/about" className="hover:text-foreground transition-colors">About</a>
          <a href="/privacy" className="hover:text-foreground transition-colors">Privacy</a>
          <a href="/terms" className="hover:text-foreground transition-colors">Terms</a>'''

code = code.replace('<a href="/about" className="hover:text-foreground transition-colors">About</a>', replacement)

with open('src/components/layout/footer.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
