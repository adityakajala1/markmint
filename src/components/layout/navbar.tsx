"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Leaf, Menu, X } from "lucide-react";
import { HangingLamp } from "@/components/ambient/HangingLamp";
import { cn } from "@/lib/utils";

export function Navbar() {
  const pathname = usePathname();

  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    

  const links = [
    { href: "/", label: "Home" },
    { href: "/mintai", label: "MintAi" },
    { href: "/calculator", label: "Calculator" },
    { href: "/developers", label: "Developers" },
  ];

  return (
    <header className="sticky top-0 z-50 flex h-16 items-center justify-between bg-background/90 backdrop-blur-md px-6 md:px-10 transition-all duration-300 relative border-b border-border/40">
      <div className="flex items-center justify-between w-full">
        
        {/* Left: Logo & SRMIST Tag */}
        <div className="flex flex-col items-start justify-center">
          <Link href="/" className="flex items-center gap-2 group">
            <Leaf className="h-6 w-6 text-accent group-hover:rotate-12 transition-transform duration-300" />
            <span className="text-2xl font-bold tracking-tight text-foreground">
              MarkMint
            </span>
          </Link>
          <span className="text-[10px] uppercase tracking-widest text-muted-foreground mt-0.5 ml-8">
            For SRMIST Students
          </span>
        </div>

        {/* Center: Navigation */}
        
        <nav className="hidden md:flex items-center gap-8">
          {links.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "text-sm font-medium transition-colors hover:text-foreground",
                  isActive
                    ? "text-foreground border-b-2 border-accent pb-1"
                    : "text-muted-foreground"
                )}
              >
                {link.label}
              </Link>
            );
          })}
          

        </nav>

        {/* Mobile Menu Toggle */}
        <div className="md:hidden">
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-2 text-muted-foreground hover:text-foreground transition-colors">
            {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>


      </div>

      {/* The Hanging Lamp - Flush against the absolute right edge */}
      <div className="absolute right-0 top-1/2 -translate-y-1/2">
        <HangingLamp />
      </div>
    


      {/* Mobile Menu Dropdown (#5) */}
      {isMobileMenuOpen && (
        <div className="absolute top-20 left-0 w-full bg-background border-b border-border shadow-lg flex flex-col p-4 md:hidden no-print z-40">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setIsMobileMenuOpen(false)}
              className="py-3 px-4 text-sm font-medium border-b border-border/50 text-foreground hover:bg-accent/10 transition-colors"
            >
              {link.label}
            </Link>
          ))}

        </div>
      )}

    </header>
  );
}