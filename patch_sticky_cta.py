import os

file_path = 'src/components/ui/GlobalFeatures.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

sticky_cta = """
      {/* Sticky Mobile CTA */}
      <div className="sm:hidden fixed bottom-6 left-0 right-0 px-4 z-[90] flex justify-center pointer-events-none">
        <a 
          href="/mintai" 
          className="pointer-events-auto bg-foreground text-background shadow-2xl px-6 py-3 rounded-full font-bold text-sm flex items-center gap-2 hover:scale-105 transition-transform"
        >
          Try MintAi
        </a>
      </div>
"""

# Insert right before the Contact Form modal
content = content.replace('{/* Contact Form Modal */}', sticky_cta + '\n      {/* Contact Form Modal */}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
