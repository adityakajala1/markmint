"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Prediction } from "@/lib/types";
import { ConfidenceBadge } from "./confidence-badge";

export interface PredictionCardProps {
  prediction: Prediction;
  className?: string;
}

export function PredictionCard({ prediction, className }: PredictionCardProps) {
  let progressColor = "bg-destructive";
  if (prediction.probability >= 75) progressColor = "bg-success";
  else if (prediction.probability >= 50) progressColor = "bg-warning";

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={cn("glass rounded-2xl p-6 flex flex-col gap-4", className)}
    >
      <div className="flex items-start justify-between gap-4">
        <h3 className="text-lg font-semibold text-foreground">{prediction.topic}</h3>
        <ConfidenceBadge confidence={prediction.probability} />
      </div>

      <div className="space-y-1">
        <div className="flex justify-between text-sm text-muted-foreground">
          <span>Likelihood</span>
          <span>{prediction.probability}%</span>
        </div>
        <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${prediction.probability}%` }}
            className={cn("h-full rounded-full", progressColor)}
          />
        </div>
        <p className="text-xs text-muted-foreground mt-2 italic">
          * This is a probabilistic estimate based on historical data, not a certainty.
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 rounded-xl bg-secondary/50 p-3">
        <div className="flex flex-col">
          <span className="text-xs text-muted-foreground">Appearance</span>
          <span className="text-sm font-medium text-foreground">
            {prediction.evidence.appeared} of {prediction.evidence.total} papers
          </span>
        </div>
        <div className="flex flex-col">
          <span className="text-xs text-muted-foreground">Long Answers</span>
          <span className="text-sm font-medium text-foreground">
            {prediction.evidence.longAnswerCount}
          </span>
        </div>
      </div>

      {prediction.evidence.historicalYears && prediction.evidence.historicalYears.length > 0 && (
        <div className="space-y-2">
          <span className="text-xs text-muted-foreground">Historical Appearances</span>
          <div className="flex flex-wrap gap-2">
            {prediction.evidence.historicalYears.map((year) => (
              <span key={year} className="rounded-md bg-muted px-2 py-1 text-xs text-muted-foreground">
                {year}
              </span>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}
