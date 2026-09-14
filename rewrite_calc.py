# -*- coding: utf-8 -*-
code = '''"use client";

import { useState, useRef, useEffect } from "react";
import { Calculator, Plus, Trash2, Copy, Check, AlertTriangle, X } from "lucide-react";
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

export function ScopeCalculator() {
  const [activeTab, setActiveTab] = useState<"endsem" | "gpa">("gpa");
  
  // End Sem State
  const [regulation, setRegulation] = useState<"5050" | "6040">("5050");
  const [internalMarks, setInternalMarks] = useState<number>(82);
  const [targetMarks, setTargetMarks] = useState<number>(90);

  const [showClearModal, setShowClearModal] = useState(false);
  const [copied, setCopied] = useState(false);
  
  // GPA State
  const [courses, setCourses] = useState<CourseGrade[]>([
    { id: "1", name: "", credits: 3, grade: "A+" },
    { id: "2", name: "", credits: 4, grade: "O" },
    { id: "3", name: "", credits: 3, grade: "A" }
  ]);

  const hasShownTimeMachineToast = useRef(false);
  const hasShownGpaToast = useRef(false);

  const calculateRequired = () => {
    let maxInternal = 50;
    let weightInternal = 0.5;
    let weightExternal = 0.5;
    if (regulation === "6040") {
      maxInternal = 60;
      weightInternal = 0.6;
      weightExternal = 0.4;
    }
    const currentInternalPoints = (internalMarks / 100) * maxInternal;
    const currentTotal = currentInternalPoints;
    const requiredTotal = targetMarks;
    const requiredExternalPoints = requiredTotal - currentTotal;
    const requiredExternalPercentage = (requiredExternalPoints / (100 * weightExternal)) * 100;
    return Math.ceil(requiredExternalPercentage);
  };

  const requiredEndSem = calculateRequired();

  const totalCredits = courses.reduce((acc, curr) => acc + (curr.credits || 0), 0);
  const totalPoints = courses.reduce((acc, curr) => acc + (curr.credits || 0) * (GRADE_POINTS[curr.grade] || 0), 0);
  const gpa = totalCredits > 0 ? (totalPoints / totalCredits).toFixed(2) : "0.00";

  const copyResults = () => {
    navigator.clipboard.writeText(MarkMint GPA Estimate:  | Target End Sem: );
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const addCourse = () => {
    setCourses([...courses, { id: Math.random().toString(), name: "", credits: 3, grade: "A" }]);
  };

  const removeCourse = (id: string) => {
    setCourses(courses.filter((c) => c.id !== id));
  };

  const updateCourse = (id: string, field: keyof CourseGrade, value: string | number) => {
    setCourses(courses.map((c) => (c.id === id ? { ...c, [field]: value } : c)));
  };

  useEffect(() => {
    if (activeTab === "endsem") {
      if (internalMarks === 0 && targetMarks === 100) {
        if (!hasShownTimeMachineToast.current) {
          toast("You need a time machine.", { duration: 3000 });
          hasShownTimeMachineToast.current = true;
        }
      } else {
        hasShownTimeMachineToast.current = false;
      }
    } else if (activeTab === "gpa") {
      const allO = courses.length > 0 && courses.every((c) => c.grade === "O");
      if (allO) {
        if (!hasShownGpaToast.current) {
          toast("Academic Weapon Detected.", { duration: 3000 });
          hasShownGpaToast.current = true;
        }
      } else if (!allO) {
        hasShownGpaToast.current = false;
      }
    }
  }, [internalMarks, targetMarks, courses, activeTab]);

  return (
    <div className="w-full max-w-2xl mx-auto flex flex-col items-center">
      
      {/* Tabs */}
      <div className="flex bg-card border border-border p-1 rounded-md shadow-sm max-w-md mx-auto w-full mb-8">
        <button 
          onClick={() => setActiveTab("endsem")}
          className={lex-1 py-2 px-4 rounded-md text-sm font-semibold transition-all }
        >
          End Semester
        </button>
        <button 
          onClick={() => setActiveTab("gpa")}
          className={lex-1 py-2 px-4 rounded-md text-sm font-semibold transition-all }
        >
          Mint+ GPA
        </button>
      </div>

      <div className="w-full bg-card border border-border rounded-md p-8 md:p-10 space-y-10 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
        
        {activeTab === "endsem" ? (
          <>
            <div className="space-y-6">
              <div>
                <label className="text-sm font-semibold text-foreground/80 block mb-2">Regulation Framework</label>
                <select 
                  className="w-full bg-background border border-border rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-accent transition-all"
                  value={regulation}
                  onChange={(e) => setRegulation(e.target.value as "5050" | "6040")}
                >
                  <option value="5050" className="bg-background text-foreground">2026-till now</option>
                  <option value="6040" className="bg-background text-foreground">Other</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-semibold text-foreground/80 block mb-2">Internal Score (/100)</label>
                  <input 
                    type="number" 
                    value={internalMarks}
                    onChange={(e) => setInternalMarks(Number(e.target.value))}
                    className="w-full bg-background border border-border rounded-md px-4 py-3 text-lg font-medium text-foreground focus:outline-none focus:ring-2 focus:ring-accent transition-all"
                  />
                </div>
                <div>
                  <label className="text-sm font-semibold text-foreground/80 block mb-2">Target Grade (/100)</label>
                  <input 
                    type="number" 
                    value={targetMarks}
                    onChange={(e) => setTargetMarks(Number(e.target.value))}
                    className="w-full bg-background border border-border rounded-md px-4 py-3 text-lg font-medium text-foreground focus:outline-none focus:ring-2 focus:ring-accent transition-all"
                  />
                </div>
              </div>
            </div>

            <div className="pt-8 border-t border-border flex items-end justify-between">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <h3 className="text-sm font-semibold text-foreground/60 uppercase tracking-wide">
                    Target End Sem
                  </h3>
                  <button onClick={copyResults} className="text-muted-foreground hover:text-foreground flex items-center gap-1 text-xs transition-colors ml-4" title="Copy Results">
                    {copied ? <Check className="w-3 h-3 text-accent" /> : <Copy className="w-3 h-3" />}
                    {copied ? "Copied" : "Copy"}
                  </button>
                </div>
                <p className="text-[11px] text-muted-foreground max-w-[200px] leading-tight">Out of 100 marks. This is the minimum you need to score on the final paper.</p>
              </div>
              <div className="text-right">
                <div className="text-[64px] leading-none font-bold text-accent tracking-tighter">
                  {requiredEndSem > 100 ? (
                    <span className="text-red-500">N/A</span>
                  ) : requiredEndSem < 0 ? (
                    "0"
                  ) : (
                    requiredEndSem
                  )}
                </div>
                {requiredEndSem > 100 && (
                  <p className="text-xs text-red-500 mt-2 font-medium">Mathematically impossible</p>
                )}
              </div>
            </div>
          </>
        ) : (
          <div className="space-y-8">
            
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
                      className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-accent"
                    />
                  </div>
                  <div className="col-span-3">
                    <input 
                      type="number" 
                      min="1" max="6"
                      value={course.credits}
                      onChange={(e) => updateCourse(course.id, "credits", Number(e.target.value))}
                      className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm text-center focus:outline-none focus:ring-2 focus:ring-accent"
                    />
                  </div>
                  <div className="col-span-2">
                    <select
                      value={course.grade}
                      onChange={(e) => updateCourse(course.id, "grade", e.target.value)}
                      className="w-full bg-background border border-border rounded-md px-1 py-2 text-sm font-semibold text-center focus:outline-none focus:ring-2 focus:ring-accent appearance-none"
                    >
                      {Object.keys(GRADE_POINTS).map(g => (
                        <option key={g} value={g} className="bg-background text-foreground">{g}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-span-1 flex justify-center">
                    <button 
                      onClick={() => removeCourse(course.id)}
                      className="p-1.5 text-muted-foreground hover:text-red-500 hover:bg-red-500/10 rounded-md transition-colors"
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
                <p className="text-[11px] text-muted-foreground max-w-[200px] leading-tight">Calculated using standard 10-point scale based on {totalCredits} total credits.</p>
              </div>
              <div className="text-[64px] leading-none font-bold text-accent tracking-tighter">
                {gpa}
              </div>
            </div>
            
          </div>
        )}

      {/* Confirmation Modal (#17) */}
      {showClearModal && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-card border border-border rounded-md max-w-sm w-full p-6 shadow-2xl relative flex flex-col items-center text-center">
            <AlertTriangle className="w-10 h-10 text-red-500 mb-4" />
            <h3 className="text-lg font-bold mb-2">Clear Calculator?</h3>
            <p className="text-sm text-muted-foreground mb-6">Are you sure you want to reset all your grades? This action cannot be undone.</p>
            <div className="flex w-full gap-3">
              <button onClick={() => setShowClearModal(false)} className="flex-1 px-4 py-2 bg-background border border-border rounded-md hover:bg-accent/10 transition-colors font-medium text-sm">Cancel</button>
              <button onClick={() => { setCourses([{ id: "1", name: "", credits: 3, grade: "A+" }]); setShowClearModal(false); }} className="flex-1 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors font-medium text-sm">Yes, Clear</button>
            </div>
          </div>
        </div>
      )}

      </div>
    </div>
  );
}
'''

with open('src/components/calculator/ScopeCalculator.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
