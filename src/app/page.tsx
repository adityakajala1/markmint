"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Leaf, Activity, ChevronRight, Calculator, BookOpen, Clock } from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";

export default function Home() {
  const [recentStudy, setRecentStudy] = useState<{ course: string; type: string } | null>(null);

  useEffect(() => {
    // Read from localStorage (simulate remembered state)
    const stored = localStorage.getItem("markmint_recent");
    if (stored) {
      try {
        setRecentStudy(JSON.parse(stored));
      } catch (e) {}
    }
  }, []);

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground selection:bg-accent/20 font-sans">
      <Navbar />
      
      <main id="main-content" className="flex-1 flex flex-col items-start justify-start w-full px-6 md:px-10 pt-4 pb-16">
        
        {/* --- HERO SECTION --- */}
        <section className="relative z-10 w-full pt-8 pb-12 flex flex-col md:flex-row items-center justify-between gap-12">
          
          {/* Left: Text Content */}
          <div className="w-full md:w-3/5 flex flex-col items-start">
            <p className="text-xs font-semibold tracking-[0.2em] uppercase text-muted-foreground mb-6 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-accent animate-pulse"></span>
              MintAI Intelligence Engine
            </p>
            
            <h1 className="text-5xl md:text-[64px] font-bold tracking-tight text-foreground leading-[1.1] mb-8">
              Predict your exams with <br/>
              <span className="text-accent italic font-serif">historical evidence.</span>
            </h1>
            
            <p className="text-lg text-muted-foreground max-w-xl leading-relaxed mb-10">
              MintAI analyzes previous year papers, recurring question families, section weightage, and historical volatility to forecast the most important topics for your SRMIST exams.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto">
              <Link 
                href="/mintai"
                className="group flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-foreground text-background rounded-md hover:bg-foreground/90 transition-all duration-150 active:scale-[0.98] font-medium"
              >
                <Activity className="w-4 h-4 text-accent" strokeWidth={2.5} />
                Try MintAI
              </Link>
              
              <Link 
                href="/calculator"
                className="flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-transparent border border-border text-foreground rounded-md hover:border-foreground/50 transition-all duration-150 active:scale-[0.98] font-medium"
              >
                <Calculator className="w-4 h-4" />
                Mint+ Calculator
              </Link>
            </div>
          </div>

          {/* Right: Botanical Mint Graphic */}
          <div className="w-full md:w-2/5 flex justify-center md:justify-end items-center relative hidden sm:flex pointer-events-none">
            <div className="relative flex items-center justify-center w-full max-w-[360px] aspect-square">
              <div className="absolute inset-0 bg-accent/5 rounded-full blur-3xl opacity-50" />
              <Leaf 
                className="w-40 h-40 md:w-56 md:h-56 text-accent/60 -rotate-12 transition-transform duration-700" 
                strokeWidth={0.5} 
              />
              <Leaf 
                className="absolute top-[25%] right-[20%] w-20 h-20 md:w-28 md:h-28 text-accent/30 rotate-[45deg]" 
                strokeWidth={1} 
              />
            </div>
          </div>
        </section>

        {/* --- CONTINUE STUDYING --- */}
        {recentStudy && (
          <section className="w-full max-w-xl mt-4">
            <h2 className="text-xs font-semibold tracking-wider text-muted-foreground mb-4">Continue Studying</h2>
            
            <Link href="/mintai" className="group block bg-card border border-border hover:border-accent/40 rounded-xl p-5 transition-all duration-150 hover:-translate-y-[2px]">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center text-accent">
                    <Clock className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-foreground text-sm group-hover:text-accent transition-colors">
                      {recentStudy.course}
                    </h4>
                    <p className="text-xs text-muted-foreground mt-0.5 flex items-center gap-2">
                      <BookOpen className="w-3 h-3" />
                      {recentStudy.type} &bull; Last opened today
                    </p>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
              </div>
            </Link>
          </section>
        )}

      </main>

      <Footer />
    </div>
  );
}
