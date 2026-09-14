# -*- coding: utf-8 -*-
with open('src/components/calculator/ScopeCalculator.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# Add imports for Copy/Trash and Check/X
if 'import { Copy' not in code:
    code = code.replace('import { Calculator, Plus, Trash2 }', 'import { Calculator, Plus, Trash2, Copy, Check, AlertTriangle, X } from "lucide-react";')

# Add state
if 'showClearModal' not in code:
    state_inject = '''
  const [showClearModal, setShowClearModal] = useState(false);
  const [copied, setCopied] = useState(false);
'''
    code = re.sub(r'(const \[regulation, setRegulation\].*?\n)', r'\1' + state_inject, code)

# Copy button logic
copy_logic = '''
  const copyResults = () => {
    navigator.clipboard.writeText(MarkMint GPA Estimate:  | Target End Sem: );
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
'''
code = re.sub(r'(const calculateRequired =.*?\n)', copy_logic + r'\1', code)

gpa_card_old = '''<h3 className="text-sm font-semibold text-foreground/60 mb-2 uppercase tracking-wide">
                    Estimated GPA
                  </h3>'''
gpa_card_new = '''<div className="flex justify-between items-center mb-2">
                  <h3 className="text-sm font-semibold text-foreground/60 uppercase tracking-wide">
                    Estimated GPA
                  </h3>
                  <button onClick={copyResults} className="text-muted-foreground hover:text-foreground flex items-center gap-1 text-xs transition-colors" title="Copy Results">
                    {copied ? <Check className="w-3 h-3 text-accent" /> : <Copy className="w-3 h-3" />}
                    {copied ? "Copied" : "Copy"}
                  </button>
                </div>'''
code = code.replace(gpa_card_old, gpa_card_new)

endsem_card_old = '''<h3 className="text-sm font-semibold text-foreground/60 mb-2 uppercase tracking-wide">
                    Target End Sem
                  </h3>'''
endsem_card_new = '''<div className="flex justify-between items-center mb-2">
                  <h3 className="text-sm font-semibold text-foreground/60 uppercase tracking-wide">
                    Target End Sem
                  </h3>
                  <button onClick={copyResults} className="text-muted-foreground hover:text-foreground flex items-center gap-1 text-xs transition-colors" title="Copy Results">
                    {copied ? <Check className="w-3 h-3 text-accent" /> : <Copy className="w-3 h-3" />}
                    {copied ? "Copied" : "Copy"}
                  </button>
                </div>'''
code = code.replace(endsem_card_old, endsem_card_new)


modal_ui = '''
      {/* Confirmation Modal (#17) */}
      {showClearModal && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-card border border-border rounded-md max-w-sm w-full p-6 shadow-2xl relative flex flex-col items-center text-center">
            <AlertTriangle className="w-10 h-10 text-red-500 mb-4" />
            <h3 className="text-lg font-bold mb-2">Clear Calculator?</h3>
            <p className="text-sm text-muted-foreground mb-6">Are you sure you want to reset all your grades? This action cannot be undone.</p>
            <div className="flex w-full gap-3">
              <button onClick={() => setShowClearModal(false)} className="flex-1 px-4 py-2 bg-background border border-border rounded-md hover:bg-accent/10 transition-colors font-medium text-sm">Cancel</button>
              <button onClick={() => { setCourses([{ id: "1", name: "", credits: 3, grade: "A+" }]); setShowClearModal(false); }} className="flex-1 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors font-medium text-sm">Yes, Clear</button>
            </div>
          </div>
        </div>
      )}
'''

add_btn_old = '''<button 
                    onClick={addCourse}
                    className="w-full flex items-center justify-center gap-2 py-3 border border-dashed border-border rounded-xl text-sm font-semibold text-muted-foreground hover:text-foreground hover:border-accent hover:bg-accent/5 transition-all"
                  >
                    <Plus className="h-4 w-4" />
                    Add Subject
                  </button>'''
add_btn_new = '''<div className="flex gap-3">
                  <button 
                    onClick={addCourse}
                    className="flex-1 flex items-center justify-center gap-2 py-3 border border-dashed border-border rounded-md text-sm font-semibold text-muted-foreground hover:text-foreground hover:border-accent hover:bg-accent/5 transition-all"
                  >
                    <Plus className="h-4 w-4" />
                    Add Subject
                  </button>
                  <button 
                    onClick={() => setShowClearModal(true)}
                    className="px-4 py-3 border border-border bg-background rounded-md text-sm font-semibold text-muted-foreground hover:text-red-500 hover:border-red-500/50 transition-all flex items-center gap-2"
                  >
                    <Trash2 className="h-4 w-4" />
                    Clear
                  </button>
                </div>'''
code = code.replace(add_btn_old, add_btn_new)
code = code.replace('</div>\n    </Card>', modal_ui + '\n</div>\n    </Card>')

with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
