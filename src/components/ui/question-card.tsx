"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Question } from "@/lib/types";
import { TopicChip } from "./topic-chip";
import { DifficultyBadge } from "./difficulty-badge";
import { ConfidenceBadge } from "./confidence-badge";

export interface QuestionCardProps {
  question: Question;
  onClick?: () => void;
  className?: string;
}

export function QuestionCard({ question, onClick, className }: QuestionCardProps) {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      onClick={onClick}
      className={cn(
        "glass glass-hover rounded-2xl p-5 flex flex-col gap-4",
        onClick && "cursor-pointer",
        className
      )}
    >
      <div className="flex flex-wrap items-center justify-between gap-2">
        <TopicChip topic={question.topic} />
        <div className="flex items-center gap-3">
          <DifficultyBadge difficulty={question.difficulty} />
          {question.confidence !== undefined && (
            <ConfidenceBadge confidence={question.confidence} size="sm" />
          )}
        </div>
      </div>
      <p className="line-clamp-3 text-sm text-foreground">
        {question.text}
      </p>
      <div className="mt-auto flex flex-wrap items-center gap-2 pt-2 text-xs font-medium">
        <span className="rounded-full bg-accent/10 px-2 py-1 text-accent-foreground">
          {question.marks} Marks
        </span>
        <span className="rounded-full bg-secondary px-2 py-1 text-secondary-foreground">
          Unit {question.unit}
        </span>
        <span className="rounded-full bg-muted px-2 py-1 text-muted-foreground">
          {question.year}
        </span>
      </div>
    </motion.div>
  );
}
