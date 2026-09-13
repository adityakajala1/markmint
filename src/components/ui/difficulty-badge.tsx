import { cn } from "@/lib/utils";

export interface DifficultyBadgeProps {
  difficulty: number; // 1-5
  showLabel?: boolean;
  className?: string;
}

export function DifficultyBadge({ difficulty, showLabel, className }: DifficultyBadgeProps) {
  const getLabel = (d: number) => {
    switch (d) {
      case 1: return "Easy";
      case 2: return "Medium";
      case 3: return "Hard";
      case 4: return "Very Hard";
      case 5: return "Expert";
      default: return "Unknown";
    }
  };

  const getColor = (d: number) => {
    if (d <= 2) return "bg-success";
    if (d === 3) return "bg-warning";
    return "bg-destructive";
  };

  const colorClass = getColor(difficulty);

  return (
    <div className={cn("flex items-center gap-2", className)}>
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((level) => (
          <div
            key={level}
            className={cn(
              "h-2 w-2 rounded-full",
              level <= difficulty ? colorClass : "bg-muted"
            )}
          />
        ))}
      </div>
      {showLabel && (
        <span className="text-xs font-medium text-muted-foreground">
          {getLabel(difficulty)}
        </span>
      )}
    </div>
  );
}
