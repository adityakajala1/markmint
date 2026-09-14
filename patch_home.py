# -*- coding: utf-8 -*-
with open('src/app/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# We will replace the entire hero section block
old_hero = """        {/* --- HERO SECTION --- */}
        <section className="relative z-10 max-w-3xl py-16">
          <p className="text-[11px] font-semibold tracking-[0.2em] uppercase text-muted-foreground mb-6">
            Built for SRMIST Students
          </p>
          
          <h1 className="text-5xl md:text-[64px] font-bold tracking-tight text-foreground leading-[1.1] mb-8">SRMIST Previous Year Papers &<br/><span className="text-accent italic font-serif">Grade Calculator.</span></h1>
          
          <p className="text-lg text-muted-foreground max-w-xl leading-relaxed mb-12">Access previous semester question papers and use the grading calculator to determine required marks for your target GPA.</p>
          
          <div className="flex flex-col sm:flex-row items-center gap-6">
            
            <Link 
              href="/calculator"
              className="flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-transparent border border-border text-foreground rounded-md hover:border-foreground/30 transition-all duration-200 active:scale-[0.98] font-medium"
            >
              Grade Calculator
            </Link>
          </div>
        </section>"""

new_hero = """        {/* --- HERO SECTION --- */}
        <section className="relative z-10 max-w-3xl py-16">
          <p className="text-[11px] font-semibold tracking-[0.2em] uppercase text-muted-foreground mb-6">
            Built for SRMIST Students
          </p>
          
          <h1 className="text-5xl md:text-[64px] font-bold tracking-tight text-foreground leading-[1.1] mb-8">Smart GPA tracking &<br/><span className="text-accent italic font-serif">MintAi Assistant.</span></h1>
          
          <p className="text-lg text-muted-foreground max-w-xl leading-relaxed mb-12">Instantly calculate your GPA across 40+ engineering branches, and chat with MintAi—our custom AI designed exclusively to answer your SRMIST academic queries.</p>
          
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <Link 
              href="/mintai"
              className="flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-foreground text-background rounded-md hover:bg-foreground/90 transition-all duration-200 active:scale-[0.98] font-medium"
            >
              Try MintAi
            </Link>
            
            <Link 
              href="/calculator"
              className="flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-transparent border border-border text-foreground rounded-md hover:border-foreground/30 transition-all duration-200 active:scale-[0.98] font-medium"
            >
              Mint+ Calculator
            </Link>
          </div>
        </section>"""

code = code.replace(old_hero, new_hero)

with open('src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
