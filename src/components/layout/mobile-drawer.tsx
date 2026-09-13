"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  FileQuestion,
  Dna,
  GitBranch,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface MobileDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export function MobileDrawer({ isOpen, onClose }: MobileDrawerProps) {
  const pathname = usePathname();

  const items = [
    { href: "/dashboard", label: "Overview", icon: LayoutDashboard },
    { href: "/dashboard/questions", label: "Questions", icon: FileQuestion },
    { href: "/dashboard/exam-dna", label: "Exam DNA", icon: Dna },
    { href: "/dashboard/question-family", label: "Question Family", icon: GitBranch },
    { href: "/predictions", label: "Predictions", icon: Dna },
    { href: "/study-plan", label: "Study Plan", icon: LayoutDashboard },
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm"
          />
          <motion.div
            initial={{ x: "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: "-100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed inset-y-0 left-0 z-50 w-3/4 max-w-sm border-r border-border bg-card shadow-lg"
          >
            <div className="flex items-center justify-between p-4 border-b border-border">
              <div className="flex items-center gap-2">
                <Dna className="h-6 w-6 text-primary" />
                <span className="text-xl font-bold tracking-tight text-foreground">
                  Exam<span className="text-primary">DNA</span>
                </span>
              </div>
              <button
                onClick={onClose}
                className="p-2 rounded-md text-muted-foreground hover:bg-accent/10 hover:text-foreground"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <nav className="p-4 flex flex-col gap-2">
              {items.map((item) => {
                const isActive = pathname === item.href;
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={onClose}
                    className={cn(
                      "flex items-center gap-3 px-3 py-3 rounded-md transition-colors",
                      isActive
                        ? "bg-primary/10 text-primary border-l-2 border-accent"
                        : "text-muted-foreground hover:bg-accent/10 hover:text-accent"
                    )}
                  >
                    <Icon className="h-5 w-5" />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
