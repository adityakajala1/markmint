"use client";

import Link from "next/link";
import { Leaf } from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground selection:bg-accent/20 font-sans">
      <Navbar />
      
      <main id="main-content" className="flex-1 flex flex-col items-start justify-start w-full px-6 md:px-10 pt-4 pb-16">
        
        {/* --- HERO SECTION --- */}
        <section className="relative z-10 w-full pt-8 pb-16 flex flex-col md:flex-row items-center justify-between gap-12">
          
          {/* Left: Text Content */}
          <div className="w-full md:w-3/5 flex flex-col items-start">
            <p className="text-[11px] font-semibold tracking-[0.2em] uppercase text-muted-foreground mb-6">
              Built for SRMIST Students
            </p>
            
            <h1 className="text-5xl md:text-[64px] font-bold tracking-tight text-foreground leading-[1.1] mb-8">
              Predict your exams with<br/>
              <span className="text-accent italic font-serif">MintAi.</span>
            </h1>
            
            <p className="text-lg text-muted-foreground max-w-xl leading-relaxed mb-12">
              MintAi generates structured study plans, filters important PYQs, and predicts upcoming CT, FT, and End Sem question papers. Get probable questions, answers, and predicted papers instantly. Includes the Mint+ GPA Calculator.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <Link 
                href="/mintai"
                className="group flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-foreground text-background rounded-md hover:bg-foreground/90 transition-all duration-200 active:scale-[0.98] font-medium"
              >
                <Leaf className="w-5 h-5 text-accent group-hover:-rotate-12 transition-transform" strokeWidth={2.5} />
                Get Started
              </Link>
              
              <Link 
                href="/calculator"
                className="flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-transparent border border-border text-foreground rounded-md hover:border-foreground/30 transition-all duration-200 active:scale-[0.98] font-medium"
              >
                Mint+ Calculator
              </Link>
            </div>
          </div>

          {/* Right: Botanical Mint Graphic */}
          <div className="w-full md:w-2/5 flex justify-center md:justify-end items-center relative hidden sm:flex">
            <div className="relative flex items-center justify-center w-full max-w-[400px] aspect-square">
              {/* Subtle natural glow, avoiding neon/AI vibes */}
              <div className="absolute inset-0 bg-accent/5 rounded-full blur-3xl" />
              
              {/* Minimalist, wireframe botanical leaves (Not AI/Techy) */}
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

      </main>

      <Footer />
    </div>
  );
}
