import os
import re

def strip_metadata(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'export const metadata: Metadata = \{.*?\};\n', '', content, flags=re.DOTALL)
    content = re.sub(r'import type \{ Metadata \} from "next";\n', '', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

strip_metadata('src/app/page.tsx')
strip_metadata('src/app/calculator/page.tsx')
strip_metadata('src/app/mintai/page.tsx')
strip_metadata('src/app/developers/page.tsx')
