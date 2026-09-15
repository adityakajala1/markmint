"use client";

import { useState, useEffect } from "react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Leaf, Search, AlertCircle, BarChart3, Database, FileText, Activity, Clock, ShieldCheck, CheckCircle2 } from "lucide-react";
import { getCourses, getPredictions, getExamDNA } from "@/lib/api";
import { BackendCourse, PredictionResponse, ExamDNAAnalysis, BackendPrediction } from "@/lib/types";

export default function MintAIPage() {
  const [courses, setCourses] = useState<BackendCourse[]>([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [hasData, setHasData] = useState(false);
  const [error, setError] = useState("");

  const [predictions, setPredictions] = useState<PredictionResponse | null>(null);
  const [dna, setDna] = useState<ExamDNAAnalysis | null>(null);

  useEffect(() => {
    getCourses().then((data) => {
      // Data might be an array or an object with an array
      const courseList = Array.isArray(data) ? data : (data.items || data.courses || []);
      setCourses(courseList);
    }).catch(err => {
      console.error("Failed to load courses", err);
    });
  }, []);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCourse) return;
    
    setIsAnalyzing(true);
    setHasData(false);
    setError("");
    
    try {
      // Find the course to get its name if subject is needed
      const courseObj = courses.find(c => c.course_id === selectedCourse || (c as any).id === selectedCourse);
      const subject = courseObj ? courseObj.course_name || courseObj.course_id || selectedCourse : selectedCourse;
      
      const [predData, dnaData] = await Promise.all([
        getPredictions(subject).catch(e => {
            if(e.status === 404) return null;
            throw e;
        }),
        getExamDNA(selectedCourse).catch(e => null)
      ]);
      
      if (!predData) {
        setError("No prediction data found for this course. Try another one.");
      } else {
        setPredictions(predData);
        setDna(dnaData);
        setHasData(true);
        localStorage.setItem("markmint_recent", JSON.stringify({ course: subject, type: "Forecast" }));
      }
    } catch (err: any) {
      setError(err.message || "Failed to fetch predictions. Ensure the backend is running.");
    } finally {
      setIsAnalyzing(false);
    }
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
                  Select Course
                </label>
                <select 
                  value={selectedCourse}
                  onChange={(e) => setSelectedCourse(e.target.value)}
                  className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:border-accent transition-colors appearance-none"
                >
                  <option value="" disabled>Select a course</option>
                  {courses.map((c: any) => (
                    <option key={c.course_id || c.id} value={c.course_id || c.id}>
                      {c.course_code || c.code} - {c.course_name || c.name}
                    </option>
                  ))}
                </select>
              </div>

              <button 
                type="submit"
                disabled={!selectedCourse || isAnalyzing}
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
              MintAI relies strictly on deterministic historical extraction. It does not hallucinate probabilities. The unresolved questions are intentional.
            </p>
          </div>
        </div>

        {/* Right Panel: Data Dashboard */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          {error ? (
            <div className="h-full min-h-[400px] border border-red-500/20 bg-red-500/5 rounded-xl flex flex-col items-center justify-center text-center p-8">
              <AlertCircle className="w-10 h-10 text-red-500 mb-4 opacity-80" />
              <h3 className="text-lg font-bold text-red-500 mb-2">Analysis Failed</h3>
              <p className="text-sm text-red-400 max-w-sm">{error}</p>
            </div>
          ) : !hasData && !isAnalyzing ? (
            <div className="h-full min-h-[400px] border border-dashed border-border rounded-xl flex flex-col items-center justify-center text-center p-8 bg-card/30">
              <Database className="w-10 h-10 text-muted-foreground mb-4 opacity-30" />
              <h3 className="text-lg font-bold text-foreground mb-2">Awaiting Parameters</h3>
              <p className="text-sm text-muted-foreground max-w-sm">
                No historical papers available yet. Select a course on the left to extract the evidence pool.
              </p>
            </div>
          ) : isAnalyzing ? (
             <div className="h-full min-h-[400px] border border-border rounded-xl p-8 flex flex-col justify-center">
                <div className="max-w-md mx-auto w-full flex flex-col items-center justify-center text-center">
                  <Activity className="w-10 h-10 text-accent animate-pulse mb-4" />
                  <h3 className="text-lg font-bold text-foreground mb-2">Analyzing Evidence Pool</h3>
                  <p className="text-sm text-muted-foreground max-w-sm">
                    Connecting to intelligence layer...
                  </p>
                </div>
             </div>
          ) : predictions ? (
            <div className="flex flex-col gap-8 animate-in fade-in duration-500">
              
              {/* STATE 2: DASHBOARD */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                  <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Data Quality</p>
                  <div className="flex items-end gap-2">
                    <span className="text-2xl font-bold text-foreground capitalize">{predictions.data_quality || "Unknown"}</span>
                  </div>
                </div>
                <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                  <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Target Year</p>
                  <div className="flex items-end gap-2">
                    <span className="text-2xl font-bold text-foreground">{predictions.target_year || "Latest"}</span>
                  </div>
                </div>
                <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                  <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Evidence Pool</p>
                  <div className="flex flex-col gap-0.5">
                    <span className="text-sm font-medium text-foreground">{predictions.evidence?.total_papers || 0} Papers</span>
                    <span className="text-sm text-muted-foreground">{predictions.evidence?.total_questions || 0} Questions</span>
                  </div>
                </div>
              </div>

              {/* DNA SUMMARY */}
              {dna && dna.analysis_summary && (
                <div className="bg-card border border-border rounded-xl p-6">
                  <h3 className="font-bold text-lg flex items-center gap-2 mb-3">
                    <Database className="w-5 h-5 text-accent" />
                    ExamDNA Insights
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                    {dna.analysis_summary}
                  </p>
                </div>
              )}

              {/* PREDICTION CARDS */}
              <div className="flex flex-col gap-4">
                <h3 className="font-bold text-lg flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-accent" />
                  Forecasted Topics
                </h3>
                
                {predictions.predictions && predictions.predictions.length > 0 ? (
                  predictions.predictions.map((p: BackendPrediction, i: number) => (
                    <div key={i} className="bg-card border border-border rounded-xl p-5 hover:-translate-y-[1px] transition-transform duration-150">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h4 className="text-lg font-bold text-foreground mb-1">{p.name || "Unknown Topic"}</h4>
                          <div className="flex items-center gap-3 text-xs text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <CheckCircle2 className="w-3 h-3 text-accent" /> 
                              Rank #{p.rank}
                            </span>
                            <span className="flex items-center gap-1">
                              <Clock className="w-3 h-3" /> 
                              Last: {p.lastSeen || "Unknown"}
                            </span>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-mono font-bold text-accent">{Math.round(p.confidence * 100)}%</div>
                          <div className="text-[10px] uppercase tracking-wider text-muted-foreground">Confidence</div>
                        </div>
                      </div>
                      
                      <div className="w-full bg-background rounded-full h-1.5 mb-4 overflow-hidden">
                        <div className="bg-accent h-full" style={{ width: `${Math.round(p.confidence * 100)}%` }}></div>
                      </div>
                      
                      <div className="flex flex-col gap-2 text-xs text-muted-foreground bg-background rounded-lg px-4 py-3 border border-border/50">
                        <div className="flex items-center justify-between">
                          <span>Appeared <strong>{p.historyCount}</strong> times historically</span>
                          <span className="capitalize text-foreground font-medium">{p.category} Category</span>
                        </div>
                        {p.evidence_details && (
                          <div className="mt-1 pt-2 border-t border-border/50 italic opacity-80">
                            "{p.evidence_details}"
                          </div>
                        )}
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground border border-dashed border-border rounded-xl">
                    No predictions could be generated from the evidence pool. (Unresolved state)
                  </div>
                )}
                
              </div>
            </div>
          ) : null}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
