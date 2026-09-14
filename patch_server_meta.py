import os

def to_server_component(filepath, title, desc):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove "use client"
    content = content.replace('"use client";\n', '')
    content = content.replace('"use client"\n', '')
    
    # Add metadata
    meta_code = f"""
import type {{ Metadata }} from "next";

export const metadata: Metadata = {{
  title: "{title}",
  description: "{desc}",
}};
"""
    
    # Insert metadata after imports
    lines = content.split('\n')
    import_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('import '):
            import_idx = i
            
    lines.insert(import_idx + 1, meta_code)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

to_server_component('src/app/page.tsx', 'MarkMint | AI Exam Prediction for SRMIST', 'MintAi generates structured study plans, filters important PYQs, and predicts upcoming CT, FT, and End Sem question papers.')
to_server_component('src/app/calculator/page.tsx', 'Mint+ GPA Calculator | MarkMint', 'Calculate your exact GPA across 40+ engineering branches with automated course fetching.')
to_server_component('src/app/mintai/page.tsx', 'MintAi | Predict Your Next Exam', 'Chat with our custom AI to get instant, accurate answers about your syllabus, exams, and predict your paper.')
to_server_component('src/app/developers/page.tsx', 'The Duo | MarkMint Developers', 'Built, designed, engineered, and maintained by SRMIST students.')

