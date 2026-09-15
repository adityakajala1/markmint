import os

file_path = 'src/components/layout/navbar.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_lamp_section = """      {/* The Hanging Lamp and Mint Plant - Right edge */}
      <div className="absolute right-0 top-1/2 -translate-y-1/2 flex items-end">
        {/* Very small plant of mint */}
        <div className="mr-6 mb-1 relative flex flex-col items-center group cursor-default">
          <div className="relative w-4 h-4 mb-[2px] transition-transform duration-300 group-hover:-translate-y-1 group-hover:scale-110">
             <Leaf className="absolute -top-2 left-0 h-4 w-4 text-accent -rotate-12" strokeWidth={2.5} />
             <Leaf className="absolute -top-1 -right-1.5 h-3 w-3 text-accent/80 rotate-[45deg]" strokeWidth={2.5} />
             <Leaf className="absolute -top-1 -left-1.5 h-3 w-3 text-accent/80 -rotate-[30deg]" strokeWidth={2.5} />
          </div>
          <div className="h-2 w-3.5 bg-muted-foreground/80 rounded-b-[2px] border-t-2 border-muted-foreground" />
        </div>
        
        <HangingLamp />
      </div>"""

new_lamp_section = """      {/* The Hanging Lamp - Flush against the absolute right edge */}
      <div className="absolute right-0 top-1/2 -translate-y-1/2">
        <HangingLamp />
      </div>"""

content = content.replace(old_lamp_section, new_lamp_section)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
