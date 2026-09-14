import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Download } from "lucide-react";

// Mock Data
const sem1Papers = [
  { id: 1, subject: "Calculus and Linear Algebra", year: "2024 - 2025" },
  { id: 2, subject: "Engineering Physics", year: "2024 - 2025" },
  { id: 3, subject: "Basic Electrical Engineering", year: "2024 - 2025" },
];

const sem2Papers = [
  { id: 4, subject: "Advanced Calculus and Complex Analysis", year: "2024 - 2025" },
  { id: 5, subject: "Engineering Chemistry", year: "2024 - 2025" },
  { id: 6, subject: "Programming for Problem Solving", year: "2024 - 2025" },
];

export default function PapersPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <Navbar />
      
      <main className="flex-1 max-w-6xl w-full mx-auto p-6 md:p-12">
        <div className="space-y-4 mb-16">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-primary">Papers</h1>
          <p className="text-lg text-foreground/70 max-w-2xl">Download past question papers to analyze patterns and practice efficiently.</p>
        </div>

        <div className="space-y-16">
          {/* Semester 1 */}
          <section>
            <h2 className="text-2xl font-bold mb-8 flex items-center gap-4 text-foreground">
              <span className="flex items-center justify-center bg-primary/10 text-primary w-10 h-10 rounded-full text-lg">1</span>
              Semester 1
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {sem1Papers.map((paper) => (
                <div key={paper.id} className="bg-card border border-border rounded-[20px] p-8 hover:shadow-[0_8px_30px_rgb(0,0,0,0.06)] hover:-translate-y-1 transition-all duration-300 flex flex-col h-full">
                  
                  <div className="flex-1">
                    <div className="inline-block px-3 py-1 bg-border/50 text-foreground/70 text-xs font-semibold rounded-full mb-6 uppercase tracking-wider">
                      {paper.year}
                    </div>
                    <h3 className="text-xl font-bold text-primary mb-4 leading-snug">{paper.subject}</h3>
                  </div>
                  
                  <button className="mt-8 w-full py-4 px-4 flex items-center justify-center gap-3 bg-transparent border border-primary/20 hover:border-accent hover:bg-accent/5 text-primary hover:text-accent rounded-xl text-sm font-semibold transition-colors duration-200 group active:scale-[0.98]">
                    <Download className="h-4 w-4 text-accent group-hover:scale-110 transition-transform duration-200" />
                    Download PDF
                  </button>
                </div>
              ))}
            </div>
          </section>

          {/* Semester 2 */}
          <section>
            <h2 className="text-2xl font-bold mb-8 flex items-center gap-4 text-foreground">
              <span className="flex items-center justify-center bg-primary/10 text-primary w-10 h-10 rounded-full text-lg">2</span>
              Semester 2
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {sem2Papers.map((paper) => (
                <div key={paper.id} className="bg-card border border-border rounded-[20px] p-8 hover:shadow-[0_8px_30px_rgb(0,0,0,0.06)] hover:-translate-y-1 transition-all duration-300 flex flex-col h-full">
                  
                  <div className="flex-1">
                    <div className="inline-block px-3 py-1 bg-border/50 text-foreground/70 text-xs font-semibold rounded-full mb-6 uppercase tracking-wider">
                      {paper.year}
                    </div>
                    <h3 className="text-xl font-bold text-primary mb-4 leading-snug">{paper.subject}</h3>
                  </div>
                  
                  <button className="mt-8 w-full py-4 px-4 flex items-center justify-center gap-3 bg-transparent border border-primary/20 hover:border-accent hover:bg-accent/5 text-primary hover:text-accent rounded-xl text-sm font-semibold transition-colors duration-200 group active:scale-[0.98]">
                    <Download className="h-4 w-4 text-accent group-hover:scale-110 transition-transform duration-200" />
                    Download PDF
                  </button>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
}
