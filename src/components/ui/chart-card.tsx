"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import React from "react";

export interface ChartCardProps {
  title: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
  isLoading?: boolean;
}

export function ChartCard({ title, description, children, className, isLoading }: ChartCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={cn("glass rounded-2xl p-6 flex flex-col", className)}
    >
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-foreground">{title}</h3>
        {description && <p className="text-sm text-muted-foreground">{description}</p>}
      </div>
      <div className="flex-1 min-h-[300px]">
        {isLoading ? (
          <div className="w-full h-full flex items-end gap-2 animate-pulse">
            {[...Array(6)].map((_, i) => (
              <div
                key={i}
                className="bg-muted rounded-t-md flex-1"
                style={{ height: `${Math.max(20, Math.random() * 100)}%` }}
              />
            ))}
          </div>
        ) : (
          children
        )}
      </div>
    </motion.div>
  );
}
