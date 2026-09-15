"use client";

import { useState, useEffect } from "react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Leaf, Search, AlertCircle, BarChart3, Database, FileText, Activity, Clock, ShieldCheck, CheckCircle2 } from "lucide-react";

export default function MintAIPage() {
  const [course, setCourse] = useState("");
  const [examType, setExamType] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [hasData, setHasData] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);

  const LOADING_STEPS = [
    "Analyzing historical papers...",
    "Extracting section weightage...",
    "Detecting recurring question families...",
    "Calculating historical volatility...",
    "Finalizing deterministic forecast..."
  ];

  const handleAnalyze = (e: React.FormEvent) => {
    e.preventDefault();
    if (!course || !examType) return;
    
    setIsAnalyzing(true);
    setHasData(false);
    setLoadingStep(0);
    
    // Simulate backend deterministic processing sequence
    let step = 0;
    const interval = setInterval(() => {
      step++;
      if (step >= LOADING_STEPS.length) {
        clearInterval(interval);
        setIsAnalyzing(false);
        setHasData(true);
        // Save to localStorage
        localStorage.setItem("markmint_recent", JSON.stringify({ course, type: `${examType} Forecast` }));
      } else {
        setLoadingStep(step);
      }
    }, 600); // 600ms per step
  };

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground selection:bg-accent/20">
      <Navbar />
      
      <main className="flex-1 w-full max-w-7xl mx-auto px-6 md:px-10 pt-8 pb-32 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Panel: Configuration */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="bg-card border border-border rounded-xl p-6 shadow-sm transition-all duration-150">
            <h2 className="text-lg font-bold mb-1 flex items-center gap-2">
              <Leaf className="w-4 h-4 text-accent" />
              Intelligence Engine
            </h2>
            <p className="text-xs text-muted-foreground mb-6">
              Generate deterministic probability forecasts based on historical evidence.
            </p>
            
            <form onSubmit={handleAnalyze} className="space-y-4">
              <div>
                <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2 block">
                  Course Code / Name
                </label>
                <input 
                  type="text" 
                  value={course}
                  onChange={(e) => setCourse(e.target.value)}
                  placeholder="e.g. 18CSC301J"
                  className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:border-accent transition-colors"
                />
              </div>

              <div>
                <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2 block">
                  Target Examination
                </label>
                <select 
                  value={examType}
                  onChange={(e) => setExamType(e.target.value)}
                  className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:border-accent transition-colors appearance-none"
                >
                  <option value="" disabled>Select Exam Type</option>
                  <option value="CT1">Cycle Test 1</option>
                  <option value="CT2">Cycle Test 2</option>
                  <option value="CT3">Cycle Test 3</option>
                  <option value="ENDSEM">End Semester</option>
                </select>
              </div>

              <button 
                type="submit"
                disabled={!course || !examType || isAnalyzing}
                className="w-full mt-4 bg-foreground text-background py-2.5 rounded-md text-sm font-medium hover:bg-foreground/90 transition-all duration-150 active:scale-[0.98] disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isAnalyzing ? (
                  <>
                    <div className="w-4 h-4 border-2 border-background border-t-transparent rounded-full animate-spin" />
                    Analyzing Evidence...
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    Run Forecast
                  </>
                )}
              </button>
            </form>
          </div>

          <div className="bg-accent/5 border border-accent/20 rounded-xl p-5">
            <h3 className="text-xs font-bold uppercase tracking-wider text-accent mb-2 flex items-center gap-2">
              <AlertCircle className="w-4 h-4" />
              Evidence Rule
            </h3>
            <p className="text-xs text-muted-foreground leading-relaxed">
              MintAI relies strictly on deterministic historical extraction. It does not hallucinate probabilities.
            </p>
          </div>
        </div>

        {/* Right Panel: Data Dashboard */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          {!hasData && !isAnalyzing ? (
            <div className="h-full min-h-[400px] border border-dashed border-border rounded-xl flex flex-col items-center justify-center text-center p-8 bg-card/30">
              <Database className="w-10 h-10 text-muted-foreground mb-4 opacity-30" />
              <h3 className="text-lg font-bold text-foreground mb-2">Awaiting Parameters</h3>
              <p className="text-sm text-muted-foreground max-w-sm">
                No historical papers available yet. Select a course and target examination on the left to extract the evidence pool.
              </p>
            </div>
          ) : isAnalyzing ? (
             <div className="h-full min-h-[400px] border border-border rounded-xl p-8 flex flex-col justify-center">
                <div className="max-w-md mx-auto w-full">
                  <div className="flex items-center gap-3 mb-6 text-accent">
                    <Activity className="w-5 h-5 animate-pulse" />
                    <span className="font-semibold text-sm tracking-widest uppercase">Analyzing Evidence Pool</span>
                  </div>
                  
                  <div className="space-y-4">
                    {LOADING_STEPS.map((step, idx) => {
                      const isComplete = idx < loadingStep;
                      const isActive = idx === loadingStep;
                      const isPending = idx > loadingStep;

                      return (
                        <div key={idx} className={`flex items-center gap-3 text-sm transition-opacity duration-300 ${isPending ? 'opacity-30' : 'opacity-100'}`}>
                          {isComplete ? (
                            <CheckCircle2 className="w-4 h-4 text-accent" />
                          ) : isActive ? (
                            <div className="w-4 h-4 border-2 border-accent border-t-transparent rounded-full animate-spin" />
                          ) : (
                            <div className="w-4 h-4 rounded-full border-2 border-border" />
                          )}
                          <span className={`${isActive ? 'text-foreground font-medium' : 'text-muted-foreground'}`}>
                            {step}
                          </span>
                        </div>
                      )
                    })}
                  </div>
                  
                  {/* Subtle skeleton shimmer */}
                  <div className="mt-8 pt-8 border-t border-border/50">
                    <div className="h-4 bg-muted/40 rounded w-1/3 animate-pulse mb-3" />
                    <div className="h-16 bg-muted/20 rounded w-full animate-pulse" />
                  </div>
                </div>
             </div>
          ) : (
            <div className="flex flex-col gap-8 animate-in fade-in duration-500">
              
              {/* STATE 2: DASHBOARD */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                  <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Global Confidence</p>
                  <div className="flex items-end gap-2">
                    <span className="text-2xl font-bold text-foreground">High</span>
                  </div>
                </div>
                <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                  <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Historical Volatility</p>
                  <div className="flex items-end gap-2">
                    <span className="text-2xl font-bold text-foreground">Stable</span>
                  </div>
                </div>
                <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                  <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Evidence Pool</p>
                  <div className="flex flex-col gap-0.5">
                    <span className="text-sm font-medium text-foreground">7 Years</span>
                    <span className="text-sm text-muted-foreground">14 Papers (186 Qs)</span>
                  </div>
                </div>
              </div>

              {/* PREDICTION CARDS */}
              <div className="flex flex-col gap-4">
                <h3 className="font-bold text-lg flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-accent" />
                  Forecasted Topics
                </h3>
                
                {/* Topic 1 */}
                <div className="bg-card border border-border rounded-xl p-5 hover:-translate-y-[1px] transition-transform duration-150">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h4 className="text-lg font-bold text-foreground mb-1">Process Scheduling Algorithms</h4>
                      <div className="flex items-center gap-3 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-accent" /> High Confidence</span>
                        <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> Last: 2023</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-mono font-bold text-accent">89%</div>
                      <div className="text-[10px] uppercase tracking-wider text-muted-foreground">Likelihood</div>
                    </div>
                  </div>
                  
                  <div className="w-full bg-background rounded-full h-1.5 mb-4 overflow-hidden">
                    <div className="bg-accent h-full" style={{ width: '89%' }}></div>
                  </div>
                  
                  <div className="flex items-center justify-between text-xs text-muted-foreground bg-background rounded-lg px-3 py-2 border border-border/50">
                    <span>Appeared in <strong>12 of 14</strong> historical papers</span>
                    <span>Usually appears in <strong>Section C</strong></span>
                  </div>
                </div>

                {/* Topic 2 */}
                <div className="bg-card border border-border rounded-xl p-5 hover:-translate-y-[1px] transition-transform duration-150">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h4 className="text-lg font-bold text-foreground mb-1">Deadlock Avoidance (Banker's Algorithm)</h4>
                      <div className="flex items-center gap-3 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-accent" /> High Confidence</span>
                        <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> Last: 2023</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-mono font-bold text-foreground">76%</div>
                      <div className="text-[10px] uppercase tracking-wider text-muted-foreground">Likelihood</div>
                    </div>
                  </div>
                  
                  <div className="w-full bg-background rounded-full h-1.5 mb-4 overflow-hidden">
                    <div className="bg-foreground/50 h-full" style={{ width: '76%' }}></div>
                  </div>
                  
                  <div className="flex items-center justify-between text-xs text-muted-foreground bg-background rounded-lg px-3 py-2 border border-border/50">
                    <span>Appeared in <strong>9 of 14</strong> historical papers</span>
                    <span>Usually appears in <strong>Section B</strong></span>
                  </div>
                </div>
              </div>

              {/* EXAM DNA EVIDENCE */}
              <div className="mt-4 pt-8 border-t border-border">
                <h3 className="font-bold text-lg flex items-center gap-2 mb-6">
                  <ShieldCheck className="w-5 h-5 text-muted-foreground" />
                  Why MintAI believes this
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-background border border-border rounded-xl p-5">
                    <h4 className="text-sm font-bold mb-2 flex items-center gap-2">
                      <FileText className="w-4 h-4 text-accent" />
                      Section Weightage
                    </h4>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Historically, Process Scheduling dominates Section C (15 marks), while Deadlock concepts appear reliably in Section B short-form questions.
                    </p>
                  </div>
                  
                  <div className="bg-background border border-border rounded-xl p-5">
                    <h4 className="text-sm font-bold mb-2 flex items-center gap-2">
                      <Activity className="w-4 h-4 text-accent" />
                      Recurring Question Families
                    </h4>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      "Calculate average waiting time using Round Robin" is a highly recurring pattern detected in 7 of the last 14 papers.
                    </p>
                  </div>
                  
                  <div className="bg-background border border-border rounded-xl p-5">
                    <h4 className="text-sm font-bold mb-2 flex items-center gap-2">
                      <Database className="w-4 h-4 text-accent" />
                      Historical Frequency
                    </h4>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Topics from Unit 2 account for 35% of total exam marks across the entire evidence pool since 2019.
                    </p>
                  </div>
                  
                  <div className="bg-background border border-border rounded-xl p-5">
                    <h4 className="text-sm font-bold mb-2 flex items-center gap-2">
                      <BarChart3 className="w-4 h-4 text-accent" />
                      Trend Since 2022
                    </h4>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Banker's Algorithm shows a stable year-over-year occurrence rate, with zero indication of being phased out of the curriculum.
                    </p>
                  </div>
                </div>
              </div>

            </div>
          )}
        </div>

      </main>
      <Footer />
    </div>
  );
}
