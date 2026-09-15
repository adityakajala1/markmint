# -*- coding: utf-8 -*-
with open('src/app/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re
code = code.replace('rounded-full', 'rounded-md')
code = code.replace('Study smarter, score higher.', 'SRMIST Previous Year Papers & Grade Calculator.')
code = code.replace('Don\'t leave your grades to chance. Analyze past papers and calculate exact requirements to hit your target GPA.', 'Access previous semester question papers and use the grading calculator to determine required marks for your target GPA.')

with open('src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
