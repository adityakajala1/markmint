# -*- coding: utf-8 -*-
with open('src/app/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# Add main-content id
code = code.replace('<main className="flex-1 flex items-center w-full max-w-7xl mx-auto px-8 md:px-16">', '<main id="main-content" className="flex-1 flex flex-col items-center justify-center w-full max-w-7xl mx-auto px-8 md:px-16 pt-16">')

# Add FAQ section
faq_section = '''
        {/* --- FAQ SECTION --- */}
        <section className="w-full max-w-3xl py-16 mb-16 border-t border-border mt-8">
          <h2 className="text-2xl font-bold mb-8">Frequently Asked Questions</h2>
          <div className="flex flex-col gap-4">
            <details className="group border border-border bg-card p-4 rounded-md cursor-pointer">
              <summary className="font-semibold select-none flex justify-between items-center">
                How accurate is the grade calculator?
                <span className="text-muted-foreground group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <p className="text-muted-foreground mt-4 leading-relaxed text-sm">
                The grade calculator uses exact formulas mandated by SRMIST. If you enter your internals accurately, the required external score will be 100% accurate.
              </p>
            </details>
            <details className="group border border-border bg-card p-4 rounded-md cursor-pointer">
              <summary className="font-semibold select-none flex justify-between items-center">
                How often are previous papers updated?
                <span className="text-muted-foreground group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <p className="text-muted-foreground mt-4 leading-relaxed text-sm">
                Papers are sourced and verified at the end of every semester. Check the "Last Updated" date in our footer for the most recent batch.
              </p>
            </details>
          </div>
        </section>
'''

# insert faq before closing main tag
code = re.sub(r'(</main>)', faq_section + r'\1', code)

with open('src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
