import { cn } from "@/lib/utils";

export interface ConfidenceBadgeProps {
  confidence: number;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function ConfidenceBadge({ confidence, size = "md", className }: ConfidenceBadgeProps) {
  let colorClass = "bg-destructive/10 text-destructive";
  if (confidence >= 75) {
    colorClass = "bg-success/10 text-success";
  } else if (confidence >= 50) {
    colorClass = "bg-warning/10 text-warning";
  }

  const sizeClass = {
    sm: "px-2 py-0.5 text-xs",
    md: "px-2.5 py-1 text-sm",
    lg: "px-3 py-1.5 text-base",
  }[size];

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full font-medium",
        colorClass,
        sizeClass,
        className
      )}
    >
      {confidence}%
    </span>
  );
}
