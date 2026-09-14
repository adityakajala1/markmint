# -*- coding: utf-8 -*-
with open('src/components/calculator/ScopeCalculator.tsx', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('You need a time machine. ⏳', 'You need a time machine.')
code = code.replace('Academic Weapon Detected 🎯', 'Academic Weapon Detected.')
with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

with open('src/app/developers/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('Listening to music \U0001f3a7', 'Listening to music')
code = code.replace('Larping \U0001f9d9\u200d\u2642\ufe0f', 'Larping')
code = code.replace('I\'m coding! 💻', 'I\'m coding!')
with open('src/app/developers/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

with open('src/components/ambient/EasterEggManager.tsx', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('%c🔍 ExamScope', '%c ExamScope')
code = code.replace('%cHello fellow dev! 👨‍💻', '%cHello fellow dev!')
code = code.replace('🌪️ Do a barrel roll!', 'Do a barrel roll!')
with open('src/components/ambient/EasterEggManager.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
