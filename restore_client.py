import os

# 1. Restore "use client" to the pages
def restore_client(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the metadata export
    import re
    content = re.sub(r'export const metadata: Metadata = \{.*?\}\n', '', content, flags=re.DOTALL)
    content = re.sub(r'import type \{ Metadata \} from "next";\n', '', content)
    
    # Add use client
    if not content.startswith('"use client";'):
        content = '"use client";\n\n' + content
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

restore_client('src/app/page.tsx')
restore_client('src/app/calculator/page.tsx')
restore_client('src/app/mintai/page.tsx')
restore_client('src/app/developers/page.tsx')

# 2. Create layouts for metadata
def create_meta_layout(folder, title, desc):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, 'layout.tsx')
    code = f"""import type {{ Metadata }} from "next";

export const metadata: Metadata = {{
  title: "{title}",
  description: "{desc}",
}};

export default function Layout({{ children }}: {{ children: React.ReactNode }}) {{
  return children;
}}
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)

create_meta_layout('src/app/calculator', 'Mint+ GPA Calculator | MarkMint', 'Calculate your exact GPA across 40+ engineering branches with automated course fetching.')
create_meta_layout('src/app/mintai', 'MintAi | Predict Your Next Exam', 'Chat with our custom AI to get instant, accurate answers about your syllabus, exams, and predict your paper.')
create_meta_layout('src/app/developers', 'The Duo | MarkMint Developers', 'Built, designed, engineered, and maintained by SRMIST students.')

