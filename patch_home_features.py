import re

file_path = 'src/app/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_h1 = r'<h1 className="text-5xl md:text-\[64px\] font-bold tracking-tight text-foreground leading-\[1.1\] mb-8">Intelligent answers for SRMIST students.<br/><span className="text-accent italic font-serif">Meet MintAi.</span></h1>'
new_h1 = '<h1 className="text-5xl md:text-[64px] font-bold tracking-tight text-foreground leading-[1.1] mb-8">Predict your exams with<br/><span className="text-accent italic font-serif">MintAi.</span></h1>'

old_p = r'<p className="text-lg text-muted-foreground max-w-xl leading-relaxed mb-12">Chat with our custom AI to get instant, accurate answers about your syllabus, exams, and academic policies. Includes the Mint+ GPA Calculator for tracking your grades.</p>'
new_p = '<p className="text-lg text-muted-foreground max-w-xl leading-relaxed mb-12">MintAi generates structured study plans, filters important PYQs, and predicts upcoming CT, FT, and End Sem question papers. Get probable questions, answers, and predicted papers instantly. Includes the Mint+ GPA Calculator.</p>'

content = re.sub(old_h1, new_h1, content)
content = re.sub(old_p, new_p, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
