import re

# 1. layout.tsx
layout_path = 'src/app/layout.tsx'
with open(layout_path, 'r', encoding='utf-8') as f:
    layout = f.read()

old_meta = r'export const metadata: Metadata = \{.*?\}'
new_meta = """export const metadata: Metadata = {
  title: "MarkMint | Predict exams & track GPA for SRMIST",
  description: "MintAi predicts your CT, FT, and End Sem question papers. Calculate your GPA instantly for 40+ engineering branches.",
  openGraph: {
    title: "MarkMint | SRMIST AI Assistant",
    description: "Generate structured study plans, filter PYQs, and predict exams with MintAi.",
    url: "https://markmint.com",
    siteName: "MarkMint",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "MarkMint | SRMIST AI Assistant",
    description: "MintAi predicts your CT, FT, and End Sem question papers.",
  }
}"""
layout = re.sub(old_meta, new_meta, layout, flags=re.DOTALL)
with open(layout_path, 'w', encoding='utf-8') as f:
    f.write(layout)

def add_metadata(filepath, title, desc):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if metadata already exists (usually not in client components, wait - client components CANNOT export metadata)
    # If the page is "use client", we have to remove it or make a wrapper.
    # Actually, in Next.js app router, "use client" pages CANNOT export metadata.
    # We must check if it's a client component.
    return content

# Wait, `src/app/page.tsx`, `calculator/page.tsx`, `mintai/page.tsx`, `developers/page.tsx` are ALL "use client"!
# To add metadata per page in Next.js for client components, we usually either:
# 1. Make the page a Server Component that imports a Client Component.
# 2. Add <title> in a next/head (Pages router) - not App router.
# Let's inspect `src/app/page.tsx`
