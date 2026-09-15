"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { Leaf } from "lucide-react";

export function Footer() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Home" },
    { href: "/mintai", label: "MintAI" },
    { href: "/calculator", label: "Calculator" },
    { href: "/privacy", label: "Privacy" },
    { href: "/terms", label: "Terms" },
  ];

  return (
    <footer className="border-t border-border bg-background py-10 mt-auto">
      <div className="container mx-auto px-8 md:px-16 flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
        
        {/* Left: Logo + Meta */}
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2">
            <Leaf className="h-5 w-5 text-accent opacity-50" />
            <span className="text-xl font-bold tracking-tight text-foreground">
              MarkMint
            </span>
          </div>
          <div className="flex items-center gap-3 text-xs text-muted-foreground">
            <span>v1.0</span>
            <span className="w-1 h-1 rounded-full bg-border" />
            <span>Built for SRMIST students</span>
            <span className="w-1 h-1 rounded-full bg-border" />
            <span>Last updated Sep 2026</span>
          </div>
        </div>

        {/* Right: Navigation */}
        <nav className="flex items-center gap-5 text-sm text-muted-foreground">
          {links.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`hover:text-foreground transition-colors ${
                  isActive ? "text-foreground border-b border-accent pb-0.5" : ""
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

      </div>
    </footer>
  );
}