"use client";

import { motion } from "framer-motion";
import { Clock } from "lucide-react";
import { cn } from "@/lib/utils";
import { StudyDay } from "@/lib/types";

export interface TimelineCardProps {
  day: StudyDay;
  className?: string;
}

export function TimelineCard({ day, className }: TimelineCardProps) {
  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -10 },
    show: { opacity: 1, x: 0 }
  };

  return (
    <div className={cn("glass rounded-2xl p-6", className)}>
      <h3 className="mb-4 text-xl font-bold text-foreground">Day {day.dayNumber}</h3>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="space-y-4"
      >
        {day.tasks.map((task) => (
          <motion.div
            key={task.id}
            variants={itemVariants}
            className="flex items-center justify-between rounded-xl bg-secondary/30 p-3"
          >
            <div className="flex items-center gap-3">
              <div
                className={cn("h-3 w-3 rounded-full", {
                  "bg-destructive": task.priority === "high",
                  "bg-warning": task.priority === "medium",
                  "bg-success": task.priority === "low",
                })}
              />
              <div className="flex flex-col">
                <span className="text-sm font-medium text-foreground">{task.topic}</span>
                <span
                  className={cn("text-xs w-max rounded px-1.5 py-0.5 font-medium mt-1", {
                    "bg-primary/20 text-primary": task.type === "study",
                    "bg-warning/20 text-warning": task.type === "practice",
                    "bg-destructive/20 text-destructive": task.type === "mock-test",
                    "bg-success/20 text-success": task.type === "revision",
                  })}
                >
                  {task.type}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
              <Clock className="h-4 w-4" />
              <span>{task.hours}h</span>
            </div>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
