import os

file_path = 'src/components/layout/navbar.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove search imports and states
content = content.replace(', Search, X', ', X')
content = content.replace('const [isSearchOpen, setIsSearchOpen] = useState(false);\n', '')
content = content.replace('const [searchQuery, setSearchQuery] = useState("");\n', '')

# 2. Remove desktop search button
search_btn_str = """          <button onClick={() => setIsSearchOpen(!isSearchOpen)} className="text-muted-foreground hover:text-foreground transition-colors ml-2" aria-label="Search">
            <Search className="h-4 w-4" />
          </button>"""
content = content.replace(search_btn_str, '')

# 3. Replace the Hanging Lamp section with the Lamp + Small Plant
old_lamp = """      {/* The Hanging Lamp - Flush against the absolute right edge */}
      <div className="absolute right-0 top-1/2 -translate-y-1/2">
        <HangingLamp />
      </div>"""

new_lamp = """      {/* The Hanging Lamp and Mint Plant - Right edge */}
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

content = content.replace(old_lamp, new_lamp)

# 4. Remove Search Modal
search_modal = """      {/* Search Modal (#3) */}
      {isSearchOpen && (
        <div className="absolute top-20 left-0 w-full bg-background border-b border-border p-4 shadow-lg flex justify-center no-print z-40">
          <div className="relative w-full max-w-md">
            <input 
              type="text" 
              placeholder="Search MarkMint..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-card border border-border rounded-md pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-accent"
              autoFocus
            />
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <button onClick={() => setIsSearchOpen(false)} className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
              <X className="h-3 w-3" />
            </button>
          </div>
        </div>
      )}"""
content = content.replace(search_modal, '')

# 5. Remove Mobile search input
mobile_search = """          <div className="py-3 px-4 relative">
             <input 
              type="text" 
              placeholder="Search..."
              className="w-full bg-card border border-border rounded-md pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-accent"
            />
            <Search className="absolute left-7 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          </div>"""
content = content.replace(mobile_search, '')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
