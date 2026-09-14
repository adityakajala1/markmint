# -*- coding: utf-8 -*-
with open('src/components/layout/navbar.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# Add state import
if 'useState' not in code:
    code = code.replace('import Link', 'import { useState } from "react";\nimport Link')
    
# Add search icon to imports
code = code.replace('import { Leaf, Menu }', 'import { Leaf, Menu, Search, X }')

# Add state to component
state_code = '''
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
'''
code = re.sub(r'(const pathname = usePathname\(\);)', r'\1' + '\n' + state_code, code)

# Mobile Menu trigger & Search Icon
nav_replace = '''
        <nav className="hidden md:flex items-center gap-8">
          {links.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "text-sm font-medium transition-colors hover:text-foreground",
                  isActive
                    ? "text-foreground border-b-2 border-accent pb-1"
                    : "text-muted-foreground"
                )}
              >
                {link.label}
              </Link>
            );
          })}
          
          <button onClick={() => setIsSearchOpen(!isSearchOpen)} className="text-muted-foreground hover:text-foreground transition-colors ml-2" aria-label="Search">
            <Search className="h-4 w-4" />
          </button>
        </nav>

        {/* Mobile Menu Toggle */}
        <div className="md:hidden">
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-2 text-muted-foreground hover:text-foreground transition-colors">
            {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
'''
code = re.sub(r'<nav className="hidden md:flex items-center gap-8">.*?</nav>\s*<!-- Mobile Menu -->\s*<div className="md:hidden">.*?</div>', nav_replace, code, flags=re.DOTALL|re.IGNORECASE)
code = re.sub(r'<nav className="hidden md:flex items-center gap-8">.*?</nav>\s*\{/\* Mobile Menu \*/\}\s*<div className="md:hidden">.*?</div>', nav_replace, code, flags=re.DOTALL)


# Add Mobile dropdown and Search Modal
modals = '''
      {/* Search Modal (#3) */}
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
      )}

      {/* Mobile Menu Dropdown (#5) */}
      {isMobileMenuOpen && (
        <div className="absolute top-20 left-0 w-full bg-background border-b border-border shadow-lg flex flex-col p-4 md:hidden no-print z-40">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setIsMobileMenuOpen(false)}
              className="py-3 px-4 text-sm font-medium border-b border-border/50 text-foreground hover:bg-accent/10 transition-colors"
            >
              {link.label}
            </Link>
          ))}
          <div className="py-3 px-4 relative">
             <input 
              type="text" 
              placeholder="Search..."
              className="w-full bg-card border border-border rounded-md pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-accent"
            />
            <Search className="absolute left-7 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          </div>
        </div>
      )}
'''

code = code.replace('</header>', modals + '\n    </header>')

with open('src/components/layout/navbar.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
