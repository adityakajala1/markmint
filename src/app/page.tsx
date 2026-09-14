"use client";

import Link from "next/link";
import { Leaf, Activity, BarChart2, ShieldCheck } from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground selection:bg-accent/20 font-sans">
      <Navbar />
      
      <main id="main-content" className="flex-1 flex flex-col items-start justify-start w-full px-6 md:px-10 pt-4 pb-16">
        
        {/* --- HERO SECTION --- */}
        <section className="relative z-10 w-full pt-8 pb-20 flex flex-col md:flex-row items-center justify-between gap-12">
          
          {/* Left: Text Content */}
          <div className="w-full md:w-3/5 flex flex-col items-start">
            <p className="text-[11px] font-semibold tracking-[0.2em] uppercase text-muted-foreground mb-6">
              Evidence-Backed Exam Intelligence
            </p>
            
            <h1 className="text-5xl md:text-[64px] font-bold tracking-tight text-foreground leading-[1.1] mb-8">
              Study smarter with<br/>
              <span className="text-accent italic font-serif">Historical Data.</span>
            </h1>
            
            <p className="text-lg text-muted-foreground max-w-xl leading-relaxed mb-12">
              MarkMint analyzes years of historical exam papers to extract structural patterns. We turn raw academic data into <strong>ExamDNA</strong>, and use <strong>MintAI</strong> to generate highly probable forecasts of what you should focus on next. No guessing. Just evidence.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <Link 
                href="/mintai"
                className="group flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-foreground text-background rounded-md hover:bg-foreground/90 transition-all duration-200 active:scale-[0.98] font-medium"
              >
                <Activity className="w-5 h-5 text-accent group-hover:scale-110 transition-transform" strokeWidth={2.5} />
                Analyze ExamDNA
              </Link>
              
              <Link 
                href="/mintai"
                className="flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-transparent border border-border text-foreground rounded-md hover:border-foreground/30 transition-all duration-200 active:scale-[0.98] font-medium"
              >
                View Forecasts
              </Link>
            </div>
          </div>

          {/* Right: Botanical Mint Graphic */}
          <div className="w-full md:w-2/5 flex justify-center md:justify-end items-center relative hidden sm:flex">
            <div className="relative flex items-center justify-center w-full max-w-[400px] aspect-square">
              <div className="absolute inset-0 bg-accent/5 rounded-full blur-3xl" />
              <Leaf 
                className="w-48 h-48 md:w-64 md:h-64 text-accent/80 -rotate-12 transition-transform duration-700 hover:rotate-0" 
                strokeWidth={0.5} 
              />
              <Leaf 
                className="absolute top-[20%] right-[15%] w-24 h-24 md:w-32 md:h-32 text-accent/40 rotate-[45deg]" 
                strokeWidth={1} 
              />
              <Leaf 
                className="absolute bottom-[20%] left-[15%] w-16 h-16 md:w-20 md:h-20 text-accent/30 -rotate-[30deg]" 
                strokeWidth={1} 
              />
            </div>
          </div>

        </section>

        {/* --- NARRATIVE SECTION --- */}
        <section className="w-full max-w-5xl py-16 mb-16 border-t border-border mt-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            
            <div className="flex flex-col items-start">
              <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-6">
                <BarChart2 className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-xl font-bold mb-3">1. Historical Structure</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We ingest years of past CT, FT, and End Semester papers. We map out exactly which units and topics historically carry the most weight.
              </p>
            </div>

            <div className="flex flex-col items-start">
              <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-6">
                <Activity className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-xl font-bold mb-3">2. ExamDNA Extraction</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                The platform identifies the structural 'DNA' of a course—detecting recurring question families, temporal shifts, and the reliability of past data.
              </p>
            </div>

            <div className="flex flex-col items-start">
              <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-6">
                <ShieldCheck className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-xl font-bold mb-3">3. MintAI Forecast</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                MintAI calculates a deterministic likelihood score for upcoming exam topics. You get a clear, probability-based forecast of what to study, completely backed by evidence.
              </p>
            </div>

          </div>
        </section>

      </main>

      <Footer />
    </div>
  );
}
