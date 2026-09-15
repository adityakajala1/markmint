import Link from "next/link";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { AlertTriangle, Home, Activity } from "lucide-react";

export const metadata = {
  title: "404 - Detained | MarkMint",
  description: "This page has been detained due to insufficient attendance.",
};

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <Navbar />
      <main className="flex-1 flex flex-col items-center justify-center text-center px-4 pt-24 pb-32">
        
        {/* Detention Notice Card */}
        <div className="w-full max-w-md bg-card border border-border rounded-xl p-8 shadow-sm">
          
          {/* Top Badge */}
          <div className="inline-flex items-center gap-2 bg-accent/10 border border-accent/30 text-accent text-[10px] font-bold uppercase tracking-widest px-3 py-1.5 rounded mb-8">
            <AlertTriangle className="w-3 h-3" />
            Attendance Shortage
          </div>

          {/* Big 404 */}
          <h1 className="text-7xl font-black text-foreground tracking-tighter mb-2">404</h1>
          
          {/* The Line */}
          <h2 className="text-lg font-bold text-foreground mb-4">
            This page has less than 75% attendance.
          </h2>
          
          <p className="text-sm text-muted-foreground mb-8 leading-relaxed">
            It has been detained and cannot be displayed.<br />
            Please report to a valid route to continue.
          </p>

          {/* Fake Attendance Record */}
          <div className="bg-background border border-border rounded-lg p-4 mb-8 text-left">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-3">Attendance Record</p>
            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-muted-foreground">Classes Held</span>
                <span className="font-mono text-foreground">45</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-muted-foreground">Classes Attended</span>
                <span className="font-mono text-accent">0</span>
              </div>
              <div className="flex justify-between text-xs border-t border-border pt-2 mt-2">
                <span className="text-muted-foreground font-semibold">Attendance</span>
                <span className="font-mono font-bold text-accent">0.00%</span>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-3">
            <Link 
              href="/"
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-foreground text-background font-medium rounded-md hover:bg-foreground/90 transition-all duration-150 active:scale-[0.98] text-sm"
            >
              <Home className="w-4 h-4" />
              Go Home
            </Link>
            <Link 
              href="/mintai"
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-transparent border border-border text-foreground font-medium rounded-md hover:border-foreground/50 transition-all duration-150 active:scale-[0.98] text-sm"
            >
              <Activity className="w-4 h-4" />
              Try MintAI
            </Link>
          </div>
        </div>

      </main>
      <Footer />
    </div>
  );
}
