import os

file_path = 'src/components/layout/navbar.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix header spacing: reduce height and remove max-w-7xl to make it span full width
old_header = """    <header className="sticky top-0 z-50 flex h-20 items-center justify-between bg-background/80 backdrop-blur-md pl-8 md:pl-16 pr-12 md:pr-16 transition-all duration-300 relative">
      <div className="flex items-center justify-between w-full max-w-7xl mx-auto">"""

new_header = """    <header className="sticky top-0 z-50 flex h-16 items-center justify-between bg-background/90 backdrop-blur-md px-6 md:px-10 transition-all duration-300 relative border-b border-border/40">
      <div className="flex items-center justify-between w-full">"""

content = content.replace(old_header, new_header)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
