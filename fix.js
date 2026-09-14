const fs = require('fs');
let code = fs.readFileSync('src/components/calculator/ScopeCalculator.tsx', 'utf8');
code = code.replace('dYZ_', '🎯');
code = code.replace('You need a time machine. ⏳', 'You need a time machine. ⏳');
fs.writeFileSync('src/components/calculator/ScopeCalculator.tsx', code);
