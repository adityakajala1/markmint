import { Dna } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border bg-background py-8 mt-auto">
      <div className="container mx-auto px-6 text-center">
        <p className="text-sm text-foreground/60 flex items-center justify-center gap-2 font-medium">
          Built for SRMIST students &bull; Exam<span className="text-primary">Scope</span> <Dna className="h-4 w-4 text-primary" />
        </p>
      </div>
    </footer>
  );
}
