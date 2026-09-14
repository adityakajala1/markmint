import { Leaf } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border bg-background py-12 mt-auto">
      <div className="container mx-auto px-8 md:px-16 flex flex-col md:flex-row items-center justify-between">
        <div className="flex items-center gap-2 mb-4 md:mb-0">
          <Leaf className="h-5 w-5 text-accent opacity-50" />
          <span className="text-xl font-bold tracking-tight text-foreground">
            MarkMint
          </span>
        </div>
        
        <nav className="flex items-center gap-6 text-sm text-muted-foreground mb-4 md:mb-0">
          <a href="/" className="hover:text-foreground transition-colors">Home</a>
          <a href="/mintai" className="hover:text-foreground transition-colors">MintAi</a>
          <a href="/calculator" className="hover:text-foreground transition-colors">Calculator</a>
          <a href="/privacy" className="hover:text-foreground transition-colors">Privacy</a>
          <a href="/terms" className="hover:text-foreground transition-colors">Terms</a>
          
        </nav>

        <div className="text-sm text-muted-foreground flex items-center gap-4">
          <span>Last Updated: Sep 2026</span>
          <span className="w-1.5 h-1.5 rounded-full bg-accent"></span>
          <span>Built for SRMIST students</span>
          <span className="w-1.5 h-1.5 rounded-full bg-accent"></span>
          <span>v1.0</span>
        </div>
      </div>
    </footer>
  );
}