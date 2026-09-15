"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Search, Calculator, Activity, Code, BookOpen } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const COMMANDS = [
  { id: "mintai", title: "MintAI Intelligence Engine", icon: Activity, href: "/mintai", category: "App" },
  { id: "calc", title: "Mint+ GPA Calculator", icon: Calculator, href: "/calculator", category: "App" },
  { id: "dev", title: "The Duo (Developers)", icon: Code, href: "/developers", category: "App" },
  { id: "sub1", title: "Data Structures (18CSC201J)", icon: BookOpen, href: "/mintai?course=18CSC201J", category: "Subjects" },
  { id: "sub2", title: "Operating Systems (18CSC301J)", icon: BookOpen, href: "/mintai?course=18CSC301J", category: "Subjects" },
];

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const filtered = COMMANDS.filter((cmd) =>
    cmd.title.toLowerCase().includes(query.toLowerCase())
  );

  useEffect(() => {
    setActiveIndex(0);
  }, [query]);

  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [open]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIndex((prev) => (prev + 1) % filtered.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((prev) => (prev - 1 + filtered.length) % filtered.length);
    } else if (e.key === "Enter" && filtered.length > 0) {
      e.preventDefault();
      router.push(filtered[activeIndex].href);
      setOpen(false);
    }
  };

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="fixed inset-0 bg-background/80 backdrop-blur-sm z-[100]"
            onClick={() => setOpen(false)}
          />
          <div className="fixed inset-0 z-[101] flex items-start justify-center pt-[15vh] pointer-events-none">
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: -10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: -10 }}
              transition={{ duration: 0.15 }}
              className="w-full max-w-xl bg-card border border-border rounded-xl shadow-2xl overflow-hidden pointer-events-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center px-4 border-b border-border">
                <Search className="w-5 h-5 text-muted-foreground mr-3" />
                <input
                  ref={inputRef}
                  type="text"
                  placeholder="Search MintAI, Calculator, Subjects..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={handleKeyDown}
                  className="w-full bg-transparent border-none py-4 text-sm focus:outline-none text-foreground placeholder:text-muted-foreground"
                />
                <div className="text-[10px] text-muted-foreground font-mono bg-accent/10 px-2 py-1 rounded">ESC</div>
              </div>

              <div className="max-h-[60vh] overflow-y-auto py-2">
                {filtered.length === 0 ? (
                  <div className="px-6 py-12 text-center text-sm text-muted-foreground">
                    No results found for "{query}"
                  </div>
                ) : (
                  filtered.map((cmd, idx) => {
                    const active = idx === activeIndex;
                    const Icon = cmd.icon;
                    return (
                      <div
                        key={cmd.id}
                        onMouseEnter={() => setActiveIndex(idx)}
                        onClick={() => {
                          router.push(cmd.href);
                          setOpen(false);
                        }}
                        className={`flex items-center gap-3 px-4 py-3 mx-2 rounded-lg cursor-pointer transition-colors ${active ? 'bg-accent/10 text-accent' : 'text-muted-foreground hover:bg-muted/50'}`}
                      >
                        <Icon className="w-4 h-4" />
                        <span className="text-sm font-medium">
                          {cmd.title}
                        </span>
                        <span className="ml-auto text-xs">
                          {cmd.category}
                        </span>
                      </div>
                    );
                  })
                )}
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}
