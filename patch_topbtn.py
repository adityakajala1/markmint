# -*- coding: utf-8 -*-
with open('src/components/ui/GlobalFeatures.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# Find the empty/broken classname for top button and replace it
# It probably looks like className="p-3 bg-card..." because the backticks were stripped, AND the  might have been evaluated to empty!
code = re.sub(r'className="p-3 bg-card.*?"', 'className={p-3 bg-card border border-border rounded-md shadow-lg text-foreground hover:bg-accent hover:text-accent-foreground transition-all }', code)

with open('src/components/ui/GlobalFeatures.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
