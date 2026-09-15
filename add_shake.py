# -*- coding: utf-8 -*-
with open('src/app/globals.css', 'r', encoding='utf-8') as f:
    code = f.read()

shake_css = '''
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px) rotate(-5deg); }
  50% { transform: translateX(5px) rotate(5deg); }
  75% { transform: translateX(-5px) rotate(-5deg); }
}
.animate-shake {
  animation: shake 0.4s ease-in-out;
}
'''

if 'animate-shake' not in code:
    code += '\n' + shake_css

with open('src/app/globals.css', 'w', encoding='utf-8') as f:
    f.write(code)
