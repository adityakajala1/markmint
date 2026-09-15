with open('src/components/calculator/ScopeCalculator.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('<option value="6040" className="bg-background text-foreground">Other</option>', '<option value="6040" className="bg-background text-foreground">2013-2025</option>')

with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
