# -*- coding: utf-8 -*-
code = r"""
"use client";

import { useState, useRef, useEffect } from "react";
import { Plus, Trash2, Copy, Check, AlertTriangle } from "lucide-react";
import { toast } from "sonner";

interface CourseGrade {
  id: string;
  name: string;
  credits: number;
  grade: string;
}

const GRADE_POINTS: Record<string, number> = {
  "O": 10,
  "A+": 9,
  "A": 8,
  "B+": 7,
  "B": 6,
  "C": 5,
  "W": 0,
  "F": 0,
  "Ab": 0,
};

const CURRICULUM: Record<string, Omit<CourseGrade, "grade">[]> = {
  "1": [
    { id: "1-1", name: "Calculus and Linear Algebra", credits: 4 },
    { id: "1-2", name: "Engineering Physics", credits: 3 },
    { id: "1-3", name: "Engineering Physics Lab", credits: 1 },
    { id: "1-4", name: "Communicative English", credits: 3 },
    { id: "1-5", name: "Programming in C", credits: 3 },
    { id: "1-6", name: "Programming in C Lab", credits: 1 },
  ],
  "2": [
    { id: "2-1", name: "Advanced Calculus and Complex Analysis", credits: 4 },
    { id: "2-2", name: "Engineering Chemistry", credits: 3 },
    { id: "2-3", name: "Engineering Chemistry Lab", credits: 1 },
    { id: "2-4", name: "Object Oriented Design and Programming", credits: 3 },
    { id: "2-5", name: "OODP Lab", credits: 1 },
    { id: "2-6", name: "Value Education", credits: 2 },
  ],
  "3": [
    { id: "3-1", name: "Transforms and Boundary Value Problems", credits: 4 },
    { id: "3-2", name: "Data Structures and Algorithms", credits: 3 },
    { id: "3-3", name: "Data Structures Lab", credits: 1 },
    { id: "3-4", name: "Computer Architecture", credits: 3 },
    { id: "3-5", name: "Software Engineering", credits: 3 },
  ]
};

export function ScopeCalculator() {
  const [selectedSemester, setSelectedSemester] = useState<string>("custom");
  const [showClearModal, setShowClearModal] = useState(false);
  const [copied, setCopied] = useState(false);
  
  const [courses, setCourses] = useState<CourseGrade[]>([
    { id: "1", name: "", credits: 3, grade: "" },
    { id: "2", name: "", credits: 4, grade: "" },
    { id: "3", name: "", credits: 3, grade: "" }
  ]);

  const hasShownGpaToast = useRef(false);

  const handleSemesterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setSelectedSemester(val);
    
    if (val !== "custom" && CURRICULUM[val]) {
      // Auto-populate courses for the semester
      const newCourses = CURRICULUM[val].map(c => ({
        ...c,
        grade: ""
      }));
      setCourses(newCourses);
    } else {
      // Reset to custom blank slate
      setCourses([
        { id: "1", name: "", credits: 3, grade: "" },
        { id: "2", name: "", credits: 4, grade: "" },
        { id: "3", name: "", credits: 3, grade: "" }
      ]);
    }
  };

  const validCourses = courses.filter(c => c.grade !== "");
  const totalCredits = validCourses.reduce((acc, curr) => acc + (curr.credits || 0), 0);
  const totalPoints = validCourses.reduce((acc, curr) => acc + (curr.credits || 0) * (GRADE_POINTS[curr.grade] || 0), 0);
  const gpa = totalCredits > 0 ? (totalPoints / totalCredits).toFixed(2) : "0.00";

  const copyResults = () => {
    navigator.clipboard.writeText(`MarkMint GPA Estimate: ${gpa} (${totalCredits} Credits)`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const addCourse = () => {
    setCourses([...courses, { id: Math.random().toString(), name: "", credits: 3, grade: "" }]);
    setSelectedSemester("custom");
  };

  const removeCourse = (id: string) => {
    setCourses(courses.filter((c) => c.id !== id));
    setSelectedSemester("custom");
  };

  const updateCourse = (id: string, field: keyof CourseGrade, value: string | number) => {
    setCourses(courses.map((c) => (c.id === id ? { ...c, [field]: value } : c)));
  };

  useEffect(() => {
    const allO = validCourses.length > 0 && validCourses.length === courses.length && courses.every((c) => c.grade === "O");
    if (allO) {
      if (!hasShownGpaToast.current) {
        toast("Academic Weapon Detected.", { duration: 3000 });
        hasShownGpaToast.current = true;
      }
    } else if (!allO) {
      hasShownGpaToast.current = false;
    }
  }, [courses]);

  return (
    <div className="w-full max-w-2xl mx-auto flex flex-col items-center">
      
      <div className="w-full bg-card border border-border rounded-md p-6 md:p-10 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
        
        <div className="space-y-8">
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-6">
            <h2 className="text-xl font-bold tracking-tight">Grade Calculator</h2>
            <div className="flex items-center gap-3">
              <label className="text-sm font-semibold text-muted-foreground whitespace-nowrap">Semester:</label>
              <select 
                value={selectedSemester}
                onChange={handleSemesterChange}
                className="bg-background border border-border rounded-md px-3 py-1.5 text-sm font-medium focus:outline-none focus:border-accent transition-colors"
              >
                <option value="custom" className="bg-background text-foreground">Custom</option>
                <option value="1" className="bg-background text-foreground">Semester 1 (CSE)</option>
                <option value="2" className="bg-background text-foreground">Semester 2 (CSE)</option>
                <option value="3" className="bg-background text-foreground">Semester 3 (CSE)</option>
              </select>
            </div>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-12 gap-2 px-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              <div className="col-span-6">Subject</div>
              <div className="col-span-3 text-center">Credits</div>
              <div className="col-span-2 text-center">Grade</div>
              <div className="col-span-1"></div>
            </div>

            {courses.map((course) => (
              <div key={course.id} className="grid grid-cols-12 gap-2 items-center">
                <div className="col-span-6">
                  <input 
                    type="text" 
                    placeholder="e.g. Data Structures"
                    value={course.name}
                    onChange={(e) => updateCourse(course.id, "name", e.target.value)}
                    className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-accent transition-colors"
                  />
                </div>
                <div className="col-span-3">
                  <input 
                    type="number" 
                    min="1" max="6"
                    value={course.credits}
                    onChange={(e) => updateCourse(course.id, "credits", Number(e.target.value))}
                    className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm text-center focus:outline-none focus:ring-2 focus:ring-accent transition-colors"
                  />
                </div>
                <div className="col-span-2">
                  <select
                    value={course.grade}
                    onChange={(e) => updateCourse(course.id, "grade", e.target.value)}
                    className="w-full bg-background border border-border rounded-md px-1 py-2 text-sm font-semibold text-center focus:outline-none focus:ring-2 focus:ring-accent appearance-none transition-colors"
                  >
                    <option value="" disabled className="bg-background text-foreground">--</option>
                    {Object.keys(GRADE_POINTS).map(g => (
                      <option key={g} value={g} className="bg-background text-foreground">{g}</option>
                    ))}
                  </select>
                </div>
                <div className="col-span-1 flex justify-center">
                  <button 
                    onClick={() => removeCourse(course.id)}
                    className="p-1.5 text-muted-foreground hover:text-red-500 hover:bg-red-500/10 rounded-md transition-colors"
                    title="Remove Subject"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="flex gap-3">
            <button 
              onClick={addCourse}
              className="flex-1 flex items-center justify-center gap-2 py-3 border-2 border-dashed border-border rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:border-foreground/30 transition-all"
            >
              <Plus size={16} /> Add Subject
            </button>
            <button 
              onClick={() => setShowClearModal(true)}
              className="px-4 py-3 border border-border bg-background rounded-md text-sm font-semibold text-muted-foreground hover:text-red-500 hover:border-red-500/50 transition-all flex items-center gap-2"
            >
              <Trash2 className="h-4 w-4" />
              Clear
            </button>
          </div>

          <div className="pt-8 border-t border-border flex items-end justify-between">
            <div>
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-sm font-semibold text-foreground/60 uppercase tracking-wide">
                  Estimated GPA
                </h3>
                <button onClick={copyResults} className="text-muted-foreground hover:text-foreground flex items-center gap-1 text-xs transition-colors ml-4" title="Copy Results">
                  {copied ? <Check className="w-3 h-3 text-accent" /> : <Copy className="w-3 h-3" />}
                  {copied ? "Copied" : "Copy"}
                </button>
              </div>
              <p className="text-[11px] text-muted-foreground max-w-[200px] leading-tight">Calculated based on {totalCredits} selected credits.</p>
            </div>
            <div className="text-[64px] leading-none font-bold text-accent tracking-tighter">
              {gpa}
            </div>
          </div>
          
        </div>

        {/* Confirmation Modal */}
        {showClearModal && (
          <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
            <div className="bg-card border border-border rounded-md max-w-sm w-full p-6 shadow-2xl relative flex flex-col items-center text-center">
              <AlertTriangle className="w-10 h-10 text-red-500 mb-4" />
              <h3 className="text-lg font-bold mb-2">Clear Calculator?</h3>
              <p className="text-sm text-muted-foreground mb-6">Are you sure you want to reset all your grades? This action cannot be undone.</p>
              <div className="flex w-full gap-3">
                <button onClick={() => setShowClearModal(false)} className="flex-1 px-4 py-2 bg-background border border-border rounded-md hover:bg-accent/10 transition-colors font-medium text-sm">Cancel</button>
                <button onClick={() => { 
                  setSelectedSemester("custom");
                  setCourses([{ id: "1", name: "", credits: 3, grade: "" }]); 
                  setShowClearModal(false); 
                }} className="flex-1 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors font-medium text-sm">Yes, Clear</button>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
"""
with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code[1:]) # Skip the first newline after r"""
