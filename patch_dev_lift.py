import os

file_path = 'src/app/developers/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add subtle lift to the card
old_card_class = 'className="bg-card border border-border rounded-md p-8 flex flex-col items-center text-center gap-5 hover:border-accent/30 transition-colors"'
new_card_class = 'className="bg-card border border-border rounded-md p-8 flex flex-col items-center text-center gap-5 transition-all duration-300 hover:border-accent/50 hover:-translate-y-1 hover:shadow-[0_8px_30px_rgb(230,50,122,0.08)] cursor-pointer"'

content = content.replace(old_card_class, new_card_class)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
