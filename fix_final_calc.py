# -*- coding: utf-8 -*-
with open('src/components/calculator/ScopeCalculator.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# Fix writeText
code = code.replace('writeText(MarkMint GPA Estimate:  | Target End Sem: );', 'writeText(MarkMint GPA Estimate:  | Target End Sem: );')

# Fix End Sem tab button class
code = re.sub(r'className=\{flex-1 py-2 px-4 rounded-full text-sm font-semibold transition-all \$\{activeTab === "endsem" \? "bg-accent text-accent-foreground shadow-md" : "text-foreground/60 hover:text-accent"\}\}', 'className={lex-1 py-2 px-4 rounded-full text-sm font-semibold transition-all }', code)

# Fix Mint+ GPA tab button class
code = re.sub(r'className=\{flex-1 py-2 px-4 rounded-full text-sm font-semibold transition-all \$\{activeTab === "gpa" \? "bg-accent text-accent-foreground shadow-md" : "text-foreground/60 hover:text-accent"\}\}', 'className={lex-1 py-2 px-4 rounded-full text-sm font-semibold transition-all }', code)

with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
