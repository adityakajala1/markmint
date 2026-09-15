import os

# 1. Update navbar.tsx
nav_path = 'src/components/layout/navbar.tsx'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()
nav = nav.replace('"/markai"', '"/mintai"').replace('"MarkAi"', '"MintAi"').replace('>MarkAi<', '>MintAi<')
with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

# 2. Update footer.tsx
foot_path = 'src/components/layout/footer.tsx'
with open(foot_path, 'r', encoding='utf-8') as f:
    foot = f.read()
foot = foot.replace('"/markai"', '"/mintai"').replace('>MarkAi<', '>MintAi<')
with open(foot_path, 'w', encoding='utf-8') as f:
    f.write(foot)

# 3. Update mintai/page.tsx
page_path = 'src/app/mintai/page.tsx'
if os.path.exists(page_path):
    with open(page_path, 'r', encoding='utf-8') as f:
        page = f.read()
    page = page.replace('MarkAi', 'MintAi')
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(page)
