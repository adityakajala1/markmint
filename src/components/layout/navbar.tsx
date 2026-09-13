"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Dna, Menu } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface NavbarProps {
  onMenuClick?: () => void;
}

export function Navbar({ onMenuClick }: NavbarProps) {
  const pathname = usePathname();

  const links = [
    { href: "/dashboard", label: "Dashboard" },
    { href: "/predictions", label: "Predictions" },
    { href: "/study-plan", label: "Study Plan" },
  ];

  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
      className="sticky top-0 z-50 flex h-16 items-center justify-between border-b border-border bg-background/80 px-6 backdrop-blur-md glass"
    >
      <div className="flex items-center gap-6">
        <Link href="/" className="flex items-center gap-2">
          <Dna className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold tracking-tight text-foreground">
            Exam<span className="text-primary">DNA</span>
          </span>
        </Link>
        <nav className="hidden md:flex items-center gap-1">
          {links.map((link) => {
            const isActive = pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "px-3 py-2 rounded-md text-sm font-medium transition-colors hover:bg-accent/10 hover:text-accent",
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground"
                )}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
      <div className="flex items-center">
        <button
          className="md:hidden p-2 text-muted-foreground hover:text-foreground"
          onClick={onMenuClick}
          aria-label="Toggle Menu"
        >
          <Menu className="h-6 w-6" />
        </button>
      </div>
    </motion.header>
  );
}
