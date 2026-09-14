# -*- coding: utf-8 -*-
with open('src/components/calculator/ScopeCalculator.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update CURRICULUM keys to use the full names
code = code.replace('"CSE": {', '"Computer Science and Engineering": {')
code = code.replace('"ECE": {', '"Electronics and Communication Engineering": {')
code = code.replace('"MECH": {', '"Mechanical Engineering": {')

# 2. Update the default state
code = code.replace('useState<string>("CSE");', 'useState<string>("Computer Science and Engineering");')

# 3. Remove the hardcoded top 3 courses and the optgroup wrapper
old_select = """              <select 
                value={selectedBranch}
                onChange={(e) => handleCurriculumChange(e.target.value, selectedSemester)}
                className="bg-background border border-border rounded-md px-3 py-1.5 text-sm font-medium focus:outline-none focus:border-accent transition-colors w-full sm:max-w-[300px] truncate"
              >
                <option value="CSE" className="bg-background text-foreground">B.Tech CSE</option>
                <option value="ECE" className="bg-background text-foreground">B.Tech ECE</option>
                <option value="MECH" className="bg-background text-foreground">B.Tech MECH</option>
                <optgroup label="All Programs">
                  {BRANCHES.map(branch => (
                    <option key={branch} value={branch} className="bg-background text-foreground">
                      {branch}
                    </option>
                  ))}
                </optgroup>
              </select>"""

new_select = """              <select 
                value={selectedBranch}
                onChange={(e) => handleCurriculumChange(e.target.value, selectedSemester)}
                className="bg-background border border-border rounded-md px-3 py-1.5 text-sm font-medium focus:outline-none focus:border-accent transition-colors w-full sm:max-w-[300px] truncate"
              >
                {BRANCHES.map(branch => (
                  <option key={branch} value={branch} className="bg-background text-foreground">
                    {branch}
                  </option>
                ))}
              </select>"""

code = code.replace(old_select, new_select)

with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
