# -*- coding: utf-8 -*-
with open('src/app/calculator/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('<option value="1">1 Cr</option>', '<option value="1" className="bg-background text-foreground">1 Cr</option>')
code = code.replace('<option value="2">2 Cr</option>', '<option value="2" className="bg-background text-foreground">2 Cr</option>')
code = code.replace('<option value="3">3 Cr</option>', '<option value="3" className="bg-background text-foreground">3 Cr</option>')
code = code.replace('<option value="4">4 Cr</option>', '<option value="4" className="bg-background text-foreground">4 Cr</option>')
code = code.replace('<option value="5">5 Cr</option>', '<option value="5" className="bg-background text-foreground">5 Cr</option>')
code = code.replace('<option key={g} value={g}>', '<option key={g} value={g} className="bg-background text-foreground">')

with open('src/app/calculator/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
