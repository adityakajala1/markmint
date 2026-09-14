# -*- coding: utf-8 -*-
with open('src/components/calculator/ScopeCalculator.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Add classes to the option tags
code = code.replace('<option value="5050">', '<option value="5050" className="bg-background text-foreground">')
code = code.replace('<option value="6040">', '<option value="6040" className="bg-background text-foreground">')
code = code.replace('<option key={g} value={g}>', '<option key={g} value={g} className="bg-background text-foreground">')

with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
