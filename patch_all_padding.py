import os

def fix_padding(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('px-8 md:px-16 pt-12 pb-32', 'px-6 md:px-10 pt-8 pb-32')
    content = content.replace('px-8 md:px-16 pt-24 pb-32', 'px-6 md:px-10 pt-8 pb-32')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_padding('src/app/terms/page.tsx')
fix_padding('src/app/privacy/page.tsx')
fix_padding('src/app/calculator/page.tsx')
fix_padding('src/app/mintai/page.tsx')
fix_padding('src/app/developers/page.tsx')
