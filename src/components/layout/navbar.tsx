"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Dna, Menu } from "lucide-react";
import { cn } from "@/lib/utils";

export function Navbar() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Home" },
    { href: "/papers", label: "Papers" },
    { href: "/calculator", label: "Calculator" },
  ];

  return (
    <header className="sticky top-0 z-50 flex h-16 items-center justify-between border-b border-border bg-card/80 px-6 backdrop-blur-md">
      <div className="flex items-center gap-6 w-full max-w-6xl mx-auto">
        <Link href="/" className="flex items-center gap-2">
          <Dna className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold tracking-tight text-foreground">
            Exam<span className="text-primary">Scope</span>
          </span>
        </Link>
        <nav className="hidden md:flex items-center gap-2 ml-8">
          {links.map((link) => {
            const isActive = pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href));
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200",
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-foreground/70 hover:text-primary hover:bg-black/5"
                )}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
        <div className="md:hidden ml-auto">
          <button className="p-2 text-foreground/70 hover:text-primary transition-colors">
            <Menu className="h-6 w-6" />
          </button>
        </div>
      </div>
    </header>
  );
}
