import { cn } from "@/lib/utils";

export interface TopicChipProps {
  topic: string;
  variant?: "default" | "outline";
  onClick?: () => void;
  className?: string;
}

export function TopicChip({ topic, variant = "default", onClick, className }: TopicChipProps) {
  return (
    <span
      onClick={onClick}
      className={cn(
        "inline-flex items-center rounded-full px-3 py-1 text-sm font-medium transition-colors",
        variant === "default" ? "bg-primary/10 text-primary" : "border border-primary/30 text-foreground",
        onClick && "cursor-pointer hover:bg-primary/20",
        className
      )}
    >
      {topic}
    </span>
  );
}
