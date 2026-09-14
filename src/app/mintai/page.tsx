"use client";

import { useState } from "react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Leaf, Search, AlertCircle, BarChart3, Database, FileText, Activity } from "lucide-react";

export default function MintAIPage() {
  const [course, setCourse] = useState("");
  const [examType, setExamType] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [hasData, setHasData] = useState(false);
  const [activeTab, setActiveTab] = useState<'dna' | 'forecast'>('forecast');

  const handleAnalyze = (e: React.FormEvent) => {
    e.preventDefault();
    if (!course || !examType) return;
    
    setIsAnalyzing(true);
    setHasData(false);
    
    // Simulate backend deterministic processing
    setTimeout(() => {
      setIsAnalyzing(false);
      setHasData(true);
      setActiveTab('forecast'); // Default to forecast on fresh run
    }, 1500);
  };

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground selection:bg-accent/20">
      <Navbar />
      
      <main className="flex-1 w-full max-w-7xl mx-auto px-6 md:px-10 pt-8 pb-32 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Panel: Configuration */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-bold mb-1 flex items-center gap-2">
              <Leaf className="w-4 h-4 text-accent" />
              Intelligence Engine
            </h2>
            <p className="text-xs text-muted-foreground mb-6">
              Extract historical ExamDNA and generate deterministic probability forecasts.
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
                className="w-full mt-4 bg-foreground text-background py-2.5 rounded-md text-sm font-medium hover:bg-foreground/90 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isAnalyzing ? (
                  <>
                    <div className="w-4 h-4 border-2 border-background border-t-transparent rounded-full animate-spin" />
                    Analyzing Evidence...
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    Run Analysis
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
              MintAI does not invent probabilities. If historical data volume is insufficient, the system returns a "Low Data Quality" status rather than guessing.
            </p>
          </div>
        </div>

        {/* Right Panel: Data Dashboard */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          {!hasData && !isAnalyzing ? (
            <div className="h-full min-h-[400px] border border-dashed border-border rounded-xl flex flex-col items-center justify-center text-center p-8 bg-card/30">
              <Database className="w-10 h-10 text-muted-foreground mb-4 opacity-50" />
              <h3 className="text-lg font-bold text-foreground mb-2">Awaiting Parameters</h3>
              <p className="text-sm text-muted-foreground max-w-sm">
                Select a course and target examination on the left to extract the historical ExamDNA and generate a probability forecast.
              </p>
            </div>
          ) : isAnalyzing ? (
             <div className="h-full min-h-[400px] border border-border rounded-xl p-8 flex flex-col gap-6">
                <div className="w-1/3 h-6 bg-muted rounded animate-pulse mb-8" />
                <div className="grid grid-cols-3 gap-4 mb-8">
                  <div className="h-24 bg-muted rounded-lg animate-pulse" />
                  <div className="h-24 bg-muted rounded-lg animate-pulse" />
                  <div className="h-24 bg-muted rounded-lg animate-pulse" />
                </div>
                <div className="space-y-4">
                  <div className="w-full h-12 bg-muted rounded animate-pulse" />
                  <div className="w-full h-12 bg-muted rounded animate-pulse" />
                  <div className="w-full h-12 bg-muted rounded animate-pulse" />
                </div>
             </div>
          ) : (
            <div className="flex flex-col animate-in fade-in duration-500">
              
              {/* Internal Tabs */}
              <div className="flex border-b border-border mb-6">
                <button
                  onClick={() => setActiveTab('forecast')}
                  className={`px-6 py-3 text-sm font-semibold border-b-2 transition-colors flex items-center gap-2 ${activeTab === 'forecast' ? 'border-accent text-foreground' : 'border-transparent text-muted-foreground hover:text-foreground'}`}
                >
                  <BarChart3 className="w-4 h-4" />
                  MintAI Forecast
                </button>
                <button
                  onClick={() => setActiveTab('dna')}
                  className={`px-6 py-3 text-sm font-semibold border-b-2 transition-colors flex items-center gap-2 ${activeTab === 'dna' ? 'border-accent text-foreground' : 'border-transparent text-muted-foreground hover:text-foreground'}`}
                >
                  <Activity className="w-4 h-4" />
                  ExamDNA Structure
                </button>
              </div>

              {activeTab === 'forecast' ? (
                <div className="flex flex-col gap-6">
                  {/* Top Stats */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-card border border-border rounded-xl p-5">
                      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Global Confidence</p>
                      <div className="flex items-end gap-2">
                        <span className="text-3xl font-bold text-foreground">High</span>
                        <span className="text-sm text-accent font-medium mb-1 border border-accent/30 bg-accent/10 px-2 py-0.5 rounded">Tier 1</span>
                      </div>
                    </div>
                    <div className="bg-card border border-border rounded-xl p-5">
                      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Evidence Pool</p>
                      <div className="flex items-end gap-2">
                        <span className="text-3xl font-bold text-foreground">12</span>
                        <span className="text-sm text-muted-foreground mb-1">papers analyzed</span>
                      </div>
                    </div>
                    <div className="bg-card border border-border rounded-xl p-5">
                      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Historical Volatility</p>
                      <div className="flex items-end gap-2">
                        <span className="text-3xl font-bold text-foreground">0.24</span>
                        <span className="text-sm text-muted-foreground mb-1">variance</span>
                      </div>
                    </div>
                  </div>

                  {/* Main Probability Table */}
                  <div className="bg-card border border-border rounded-xl overflow-hidden flex flex-col">
                    <div className="px-6 py-4 border-b border-border flex justify-between items-center bg-muted/20">
                      <h3 className="font-bold flex items-center gap-2">
                        <Leaf className="w-4 h-4 text-accent" />
                        Top Predicted Topics
                      </h3>
                      <span className="text-xs text-muted-foreground">Sorted by Likelihood Score</span>
                    </div>
                    
                    <div className="p-6 flex flex-col gap-6">
                      {/* Item 1 */}
                      <div className="flex flex-col gap-2">
                        <div className="flex justify-between items-center">
                          <span className="font-semibold text-sm">Organic Synthesis Mechanisms</span>
                          <span className="font-mono text-accent font-bold">0.85</span>
                        </div>
                        <div className="w-full bg-background rounded-full h-2.5 border border-border overflow-hidden">
                          <div className="bg-accent h-full rounded-full" style={{ width: '85%' }}></div>
                        </div>
                        <div className="flex justify-between text-[11px] text-muted-foreground mt-1">
                          <span>Occurrences: 9/12</span>
                          <span>Recent Freq: 0.90 | Hist Freq: 0.75</span>
                        </div>
                      </div>

                      {/* Item 2 */}
                      <div className="flex flex-col gap-2">
                        <div className="flex justify-between items-center">
                          <span className="font-semibold text-sm">Spectroscopy Fundamentals</span>
                          <span className="font-mono text-accent font-bold">0.68</span>
                        </div>
                        <div className="w-full bg-background rounded-full h-2.5 border border-border overflow-hidden">
                          <div className="bg-accent h-full rounded-full opacity-80" style={{ width: '68%' }}></div>
                        </div>
                        <div className="flex justify-between text-[11px] text-muted-foreground mt-1">
                          <span>Occurrences: 7/12</span>
                          <span>Recent Freq: 0.40 | Hist Freq: 0.65</span>
                        </div>
                      </div>

                      {/* Item 3 */}
                      <div className="flex flex-col gap-2 opacity-60">
                        <div className="flex justify-between items-center">
                          <span className="font-semibold text-sm">Reaction Kinetics</span>
                          <span className="font-mono text-muted-foreground font-bold">0.30</span>
                        </div>
                        <div className="w-full bg-background rounded-full h-2.5 border border-border overflow-hidden">
                          <div className="bg-muted-foreground h-full rounded-full" style={{ width: '30%' }}></div>
                        </div>
                        <div className="flex justify-between text-[11px] text-muted-foreground mt-1">
                          <span>Occurrences: 3/12</span>
                          <span>Recent Freq: 0.10 | Hist Freq: 0.35</span>
                        </div>
                      </div>

                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col gap-6">
                  {/* Structural Summary */}
                  <div className="bg-card border border-border rounded-xl p-6">
                    <h3 className="font-bold flex items-center gap-2 mb-6">
                      <FileText className="w-4 h-4 text-accent" />
                      Historical Paper Structure
                    </h3>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                      <div className="flex flex-col">
                        <span className="text-xs text-muted-foreground uppercase mb-1">Format</span>
                        <span className="font-semibold text-sm">Standard (3 Parts)</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-xs text-muted-foreground uppercase mb-1">Max Marks</span>
                        <span className="font-semibold text-sm">100</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-xs text-muted-foreground uppercase mb-1">Data Quality</span>
                        <span className="font-semibold text-sm text-green-500">Robust</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-xs text-muted-foreground uppercase mb-1">Years Mapped</span>
                        <span className="font-semibold text-sm">2019 - 2025</span>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <h4 className="text-sm font-semibold text-muted-foreground">Section Weightage Analysis</h4>
                      
                      <div className="flex items-center gap-4 text-sm">
                        <div className="w-24 font-medium">Part A</div>
                        <div className="flex-1 bg-background rounded-full h-2 border border-border overflow-hidden">
                          <div className="bg-muted-foreground h-full w-[20%]"></div>
                        </div>
                        <div className="w-16 text-right font-mono text-muted-foreground">20%</div>
                      </div>
                      
                      <div className="flex items-center gap-4 text-sm">
                        <div className="w-24 font-medium">Part B</div>
                        <div className="flex-1 bg-background rounded-full h-2 border border-border overflow-hidden">
                          <div className="bg-accent h-full w-[60%]"></div>
                        </div>
                        <div className="w-16 text-right font-mono text-muted-foreground">60%</div>
                      </div>
                      
                      <div className="flex items-center gap-4 text-sm">
                        <div className="w-24 font-medium">Part C</div>
                        <div className="flex-1 bg-background rounded-full h-2 border border-border overflow-hidden">
                          <div className="bg-muted-foreground h-full w-[20%]"></div>
                        </div>
                        <div className="w-16 text-right font-mono text-muted-foreground">20%</div>
                      </div>
                    </div>

                  </div>

                  {/* Question Families */}
                  <div className="bg-card border border-border rounded-xl p-6">
                    <h3 className="font-bold flex items-center gap-2 mb-6">
                      <Activity className="w-4 h-4 text-accent" />
                      Recurring Question Families
                    </h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="p-4 border border-border rounded-lg bg-background">
                        <p className="text-sm font-semibold mb-2">"Derive the equation for..."</p>
                        <p className="text-xs text-muted-foreground mb-3">Often appears in Part B. Historically targets Unit 2 and Unit 4.</p>
                        <span className="text-[10px] uppercase font-bold text-accent bg-accent/10 px-2 py-1 rounded">High Frequency Family</span>
                      </div>
                      
                      <div className="p-4 border border-border rounded-lg bg-background">
                        <p className="text-sm font-semibold mb-2">"Differentiate between..."</p>
                        <p className="text-xs text-muted-foreground mb-3">Almost exclusively appears in Part A short answers.</p>
                        <span className="text-[10px] uppercase font-bold text-muted-foreground border border-border px-2 py-1 rounded">Moderate Frequency Family</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

      </main>
      <Footer />
    </div>
  );
}
