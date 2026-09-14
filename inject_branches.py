# -*- coding: utf-8 -*-
with open('src/components/calculator/ScopeCalculator.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Define the exhaustive list of branches
branches_list = """
const BRANCHES = [
  "Aerospace Engineering",
  "Artificial Intelligence",
  "Automobile Engineering",
  "Automobile Engineering with Specialization in Automotive Electronics",
  "Automobile Engineering with Specialization in Vehicles Testing GARC",
  "Automotive Engineering ARAI",
  "Biomedical Engineering",
  "Biomedical Engineering with specialisation in Machine Intelligence",
  "Biotechnology",
  "Biotechnology Computational Biology",
  "Biotechnology with specialization in Food Technology",
  "Biotechnology with specialization in Regenerative Medicine",
  "Chemical Engineering",
  "Civil Engineering",
  "Civil Engineering with Computer Applications",
  "Computer Science and Engineering",
  "Computer Science And Engineering Data Science",
  "Computer Science And Engineering with Specialization in Artificial Intelligence and Machine Learning",
  "Computer Science And Engineering with Specialization in Big Data Analytics",
  "Computer Science And Engineering with Specialization in Blockchain Technology",
  "Computer Science And Engineering with Specialization in Cloud Computing",
  "Computer Science And Engineering with Specialization in Cyber Security",
  "Electronics and Communication Engineering",
  "Integrated MTech Computer Science And Engineering with Specialization in Data Science",
  "Integrated MTech Electronics And Communication Engineering",
  "Integrated MTech in Artificial Intelligence",
  "Integrated MTech in Computer Science And Engineering with Specialization in Cognitive Computing",
  "Integrated MTech in Computer Science And Engineering",
  "Integrated MTech in Material Science and Engineering",
  "Integrated MTech in Mechanical Engineering",
  "Mechanical Engineering",
  "Mechanical Engineering with specialization in Artificial Intelligence and Machine Learning",
  "Mechanical Engineering with specialization in Automation and Robotics",
  "Mechatronics Engineering",
  "Mechatronics Engineering with Specialization in Robotics",
  "Mechatronics Engineering with specialization in Autonomous Driving Technology",
  "Mechatronics Engineering with specialization in Immersive Technologies",
  "Mechatronics Engineering with specialization in Industrial IoT and Systems Engineering",
  "Nanotechnology"
];
"""

# Insert branches list right after CURRICULUM definition
code = code.replace('export function ScopeCalculator() {', branches_list + '\nexport function ScopeCalculator() {')

# Replace the hardcoded select options with map
old_select = """              <select 
                value={selectedBranch}
                onChange={(e) => handleCurriculumChange(e.target.value, selectedSemester)}
                className="bg-background border border-border rounded-md px-3 py-1.5 text-sm font-medium focus:outline-none focus:border-accent transition-colors w-full sm:w-auto"
              >
                <option value="CSE" className="bg-background text-foreground">B.Tech CSE</option>
                <option value="ECE" className="bg-background text-foreground">B.Tech ECE</option>
                <option value="MECH" className="bg-background text-foreground">B.Tech MECH</option>
              </select>"""

new_select = """              <select 
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

code = code.replace(old_select, new_select)

with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
