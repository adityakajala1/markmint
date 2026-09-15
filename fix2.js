const fs = require('fs');
let code = fs.readFileSync('src/components/calculator/ScopeCalculator.tsx', 'utf8');
code = code.replace(/toast\("Calculated: You need a time machine[^"]+", \{ duration: 3000 \}\);/, 'toast("Calculated: You need a time machine. ⏳", { duration: 3000 });');
fs.writeFileSync('src/components/calculator/ScopeCalculator.tsx', code);
