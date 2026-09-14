"use client";

import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { ScopeCalculator } from "@/components/calculator/ScopeCalculator";

export default function CalculatorPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground relative overflow-hidden">
      <Navbar />
      <main className="flex-1 w-full mx-auto px-4 sm:px-6 md:px-10 pt-8 pb-32 relative z-10 flex flex-col justify-center items-center">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4 text-center">Mint+ GPA</h1>
        <p className="text-muted-foreground text-center mb-12 max-w-lg">
          Select your semester or enter custom subjects to calculate your precise Grade Point Average.
        </p>
        
        <ScopeCalculator />
      </main>
      <Footer />
    </div>
  );
}
