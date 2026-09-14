# -*- coding: utf-8 -*-
with open('src/components/layout/footer.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('<a href="/login" className="hover:text-foreground transition-colors">Login</a>', '')

with open('src/components/layout/footer.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
