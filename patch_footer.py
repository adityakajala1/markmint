# -*- coding: utf-8 -*-
with open('src/components/layout/footer.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# We will just replace the entire <nav> block
nav_pattern = r'<nav className="flex items-center gap-6 text-sm text-muted-foreground mb-4 md:mb-0">.*?</nav>'

new_nav = '''<nav className="flex items-center gap-6 text-sm text-muted-foreground mb-4 md:mb-0">
          <a href="/" className="hover:text-foreground transition-colors">Home</a>
          <a href="/markai" className="hover:text-foreground transition-colors">MarkAi</a>
          <a href="/calculator" className="hover:text-foreground transition-colors">Calculator</a>
          <a href="/privacy" className="hover:text-foreground transition-colors">Privacy</a>
          <a href="/terms" className="hover:text-foreground transition-colors">Terms</a>
        </nav>'''

code = re.sub(nav_pattern, new_nav, code, flags=re.DOTALL)

with open('src/components/layout/footer.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
