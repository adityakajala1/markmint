"use client";

import { useState } from "react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Calculator } from "lucide-react";

export default function CalculatorPage() {
  const [regulation, setRegulation] = useState<"5050" | "6040">("5050");
  const [internalMarks, setInternalMarks] = useState<number>(82);
  const [targetMarks, setTargetMarks] = useState<number>(90);

  // Math
  let requiredEndSem = 0;
  if (regulation === "5050") {
    requiredEndSem = (targetMarks - internalMarks * 0.5) / 0.5;
  } else {
    requiredEndSem = (targetMarks - internalMarks * 0.6) / 0.4;
  }
  
  requiredEndSem = Math.ceil(requiredEndSem);

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <Navbar />
      
      <main className="flex-1 flex flex-col items-center p-6 md:p-12">
        <div className="w-full max-w-xl space-y-10">
          
          <div className="text-center space-y-3 mb-10">
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-primary">Scope+</h1>
            <p className="text-foreground/70 font-medium">Calculate exactly what you need in the End Semester.</p>
          </div>

          <div className="bg-card border border-border rounded-[20px] p-8 md:p-10 space-y-10 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
            
            {/* Regulation Selection */}
            <div className="space-y-4">
              <label className="text-sm font-semibold text-foreground/80 tracking-wide uppercase">Regulation Weightage</label>
              <div className="grid grid-cols-2 gap-4">
                <button 
                  onClick={() => setRegulation("5050")}
                  className={`py-4 px-4 rounded-xl font-medium text-sm border transition-all duration-200 active:scale-[0.98] ${regulation === "5050" ? "bg-primary border-primary text-primary-foreground shadow-md" : "bg-card border-border text-foreground/70 hover:border-primary/40 hover:text-primary"}`}
                >
                  2026-till now<br/>
                  <span className={`text-xs mt-1 block ${regulation === "5050" ? "opacity-90" : "opacity-60"}`}>(50% Internal / 50% EndSem)</span>
                </button>
                <button 
                  onClick={() => setRegulation("6040")}
                  className={`py-4 px-4 rounded-xl font-medium text-sm border transition-all duration-200 active:scale-[0.98] ${regulation === "6040" ? "bg-primary border-primary text-primary-foreground shadow-md" : "bg-card border-border text-foreground/70 hover:border-primary/40 hover:text-primary"}`}
                >
                  2013-2025<br/>
                  <span className={`text-xs mt-1 block ${regulation === "6040" ? "opacity-90" : "opacity-60"}`}>(60% Internal / 40% EndSem)</span>
                </button>
              </div>
            </div>

            {/* Internal Marks Slider */}
            <div className="space-y-5">
              <div className="flex justify-between items-center">
                <label className="text-sm font-semibold text-foreground/80 tracking-wide uppercase">Current Internal Marks</label>
                <span className="text-2xl font-bold text-primary">{internalMarks}</span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="100" 
                value={internalMarks}
                onChange={(e) => setInternalMarks(Number(e.target.value))}
                className="w-full h-2 bg-border rounded-lg appearance-none cursor-pointer accent-primary"
              />
            </div>

            {/* Target Marks Slider */}
            <div className="space-y-5">
              <div className="flex justify-between items-center">
                <label className="text-sm font-semibold text-foreground/80 tracking-wide uppercase">Target Overall Marks</label>
                <span className="text-2xl font-bold text-primary">{targetMarks}</span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="100" 
                value={targetMarks}
                onChange={(e) => setTargetMarks(Number(e.target.value))}
                className="w-full h-2 bg-border rounded-lg appearance-none cursor-pointer accent-primary"
              />
            </div>

            {/* Results Card */}
            <div className={`mt-10 p-8 rounded-[16px] text-center transition-colors duration-300 ${requiredEndSem > 100 ? 'bg-accent/10 border border-accent/20' : 'bg-primary/5 border border-primary/10'}`}>
              <h3 className="text-sm font-semibold text-foreground/60 mb-2 uppercase tracking-wide">
                Required End Sem
              </h3>
              
              {requiredEndSem > 100 ? (
                <div className="mt-4">
                  <p className="text-5xl font-black text-accent mb-2">Impossible</p>
                  <p className="text-sm text-accent/80 font-medium mt-3">
                    Target is not achievable with current internal marks.
                  </p>
                </div>
              ) : requiredEndSem <= 0 ? (
                <div className="mt-4">
                  <p className="text-5xl font-black text-primary mb-2">Secured</p>
                  <p className="text-sm text-primary/80 font-medium mt-3">
                    You have already achieved your target grade!
                  </p>
                </div>
              ) : (
                <div className="mt-4">
                  <p className="text-6xl md:text-7xl font-black text-primary tracking-tighter">
                    {requiredEndSem} <span className="text-2xl md:text-3xl text-primary/60 font-bold">/ 100</span>
                  </p>
                </div>
              )}
            </div>

          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
