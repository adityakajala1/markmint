"use client";

import Link from "next/link";
import { ArrowRight, Calculator, FileText, Dna } from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground selection:bg-primary/20">
      <Navbar />
      
      <main className="flex-1 flex flex-col items-center justify-center p-6 text-center relative overflow-hidden">
        
        {/* Subtle organic abstract shapes in background */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl pointer-events-none mix-blend-multiply" />
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-primary/5 rounded-full blur-3xl pointer-events-none mix-blend-multiply" />

        <div className="max-w-2xl space-y-8 z-10">
          
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-foreground">
            Exam<span className="text-primary">Scope</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-foreground/80 font-medium tracking-wide">
            SRMIST Exam Intelligence & Grade Calculator
          </p>
          
          <p className="text-lg text-foreground/70 max-w-xl mx-auto leading-relaxed">
            Analyze previous year papers, understand exam patterns, and calculate exactly what you need in your End Semester.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-10">
            <Link 
              href="/papers"
              className="group flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-card border border-border text-primary rounded-full hover:bg-card/80 transition-all duration-200 shadow-sm active:scale-[0.98]"
            >
              <FileText className="h-5 w-5" />
              <span className="font-semibold">Explore Papers</span>
            </Link>
            <Link 
              href="/calculator"
              className="group flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-primary text-primary-foreground rounded-full hover:bg-primary/90 transition-all duration-200 shadow-sm active:scale-[0.98]"
            >
              <Calculator className="h-5 w-5" />
              <span className="font-semibold">Grade Calculator</span>
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
