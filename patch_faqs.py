import os
import re

file_path = 'src/app/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The current FAQ section starts with {/* --- FAQ SECTION --- */}
# Let's replace the whole section.
old_faq_pattern = r'\{\/\* --- FAQ SECTION ---\*\/}.*?(?=</main>)'

new_faq = """{/* --- FAQ SECTION --- */}
        <section className="w-full max-w-3xl py-16 mb-16 border-t border-border mt-8">
          <h2 className="text-2xl font-bold mb-8">Frequently Asked Questions</h2>
          <div className="space-y-4">
            
            <details className="group border border-border bg-card p-4 rounded-md cursor-pointer">
              <summary className="font-semibold select-none flex justify-between items-center">
                How does MintAi predict exam papers?
                <span className="text-muted-foreground group-open:rotate-180 transition-transform">↓</span>
              </summary>
              <p className="text-muted-foreground mt-4 leading-relaxed text-sm">
                MintAi analyzes years of historical SRMIST question papers, syllabus trends, and academic patterns to identify the highest-probability questions for your upcoming Cycle Tests (CT), Final Tests (FT), and End Semester exams.
              </p>
            </details>

            <details className="group border border-border bg-card p-4 rounded-md cursor-pointer">
              <summary className="font-semibold select-none flex justify-between items-center">
                Are all engineering branches supported by the calculator?
                <span className="text-muted-foreground group-open:rotate-180 transition-transform">↓</span>
              </summary>
              <p className="text-muted-foreground mt-4 leading-relaxed text-sm">
                Yes! The Mint+ Calculator supports over 40 B.Tech and M.Tech engineering programs. When you select your branch and semester, it automatically loads your specific subjects and credit weights.
              </p>
            </details>

            <details className="group border border-border bg-card p-4 rounded-md cursor-pointer">
              <summary className="font-semibold select-none flex justify-between items-center">
                How do I get a customized study plan?
                <span className="text-muted-foreground group-open:rotate-180 transition-transform">↓</span>
              </summary>
              <p className="text-muted-foreground mt-4 leading-relaxed text-sm">
                Simply chat with MintAi. Tell it your branch, your current semester, and the exam you are preparing for. It will instantly generate a structured, day-by-day study plan focusing on the most important topics.
              </p>
            </details>

            <details className="group border border-border bg-card p-4 rounded-md cursor-pointer">
              <summary className="font-semibold select-none flex justify-between items-center">
                Is this an official SRMIST website?
                <span className="text-muted-foreground group-open:rotate-180 transition-transform">↓</span>
              </summary>
              <p className="text-muted-foreground mt-4 leading-relaxed text-sm">
                No, MarkMint is independently built, designed, engineered, and maintained by students. We are not officially affiliated with SRM Institute of Science and Technology.
              </p>
            </details>

            <details className="group border border-border bg-card p-4 rounded-md cursor-pointer">
              <summary className="font-semibold select-none flex justify-between items-center">
                How accurate is the GPA calculator?
                <span className="text-muted-foreground group-open:rotate-180 transition-transform">↓</span>
              </summary>
              <p className="text-muted-foreground mt-4 leading-relaxed text-sm">
                The Mint+ Calculator uses the exact 10-point scale formulas mandated by SRMIST. If you enter your expected grades accurately, the calculated GPA will be 100% precise.
              </p>
            </details>

          </div>
        </section>
      """

content = re.sub(old_faq_pattern, new_faq, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
