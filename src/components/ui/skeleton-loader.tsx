import { cn } from "@/lib/utils";

export function SkeletonCard({ className }: { className?: string }) {
  return (
    <div className={cn("animate-pulse bg-muted rounded-2xl p-6", className)}>
      <div className="h-6 w-1/3 rounded bg-secondary mb-4" />
      <div className="space-y-2">
        <div className="h-4 w-full rounded bg-secondary" />
        <div className="h-4 w-5/6 rounded bg-secondary" />
        <div className="h-4 w-4/6 rounded bg-secondary" />
      </div>
    </div>
  );
}

export function SkeletonChart({ className }: { className?: string }) {
  return (
    <div className={cn("glass animate-pulse rounded-2xl p-6", className)}>
      <div className="h-6 w-1/4 rounded bg-muted mb-6" />
      <div className="flex h-[300px] items-end gap-2">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="flex-1 rounded-t-md bg-muted"
            style={{ height: `${Math.max(20, Math.random() * 100)}%` }}
          />
        ))}
      </div>
    </div>
  );
}

export function SkeletonText({ className }: { className?: string }) {
  return (
    <div className={cn("animate-pulse space-y-2", className)}>
      <div className="h-4 w-full rounded bg-muted" />
      <div className="h-4 w-5/6 rounded bg-muted" />
      <div className="h-4 w-4/6 rounded bg-muted" />
    </div>
  );
}

export function SkeletonStatCard({ className }: { className?: string }) {
  return (
    <div className={cn("glass animate-pulse rounded-2xl p-6", className)}>
      <div className="flex items-center justify-between mb-4">
        <div className="h-12 w-12 rounded-full bg-muted" />
        <div className="h-4 w-12 rounded bg-muted" />
      </div>
      <div className="h-4 w-20 rounded bg-muted mb-2" />
      <div className="h-8 w-24 rounded bg-muted" />
    </div>
  );
}
