"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { HeatmapCell } from "@/lib/types";
import { cn } from "@/lib/utils";

interface Props {
  data: HeatmapCell[];
}

export function TopicHeatmap({ data }: Props) {
  const [hoveredCell, setHoveredCell] = useState<HeatmapCell | null>(null);

  const { topics, years, grid, maxFreq } = useMemo(() => {
    if (!data || data.length === 0) {
        return { topics: [], years: [], grid: new Map(), maxFreq: 1 };
    }
    const topicSet = new Set<string>();
    const yearSet = new Set<string>();

    data.forEach((d) => {
      topicSet.add(d.topic);
      yearSet.add(d.year);
    });

    const topicsArray = Array.from(topicSet).sort();
    const yearsArray = Array.from(yearSet).sort();

    const maxFrequency = Math.max(...data.map(d => d.frequency), 1);

    const gridMap = new Map();
    data.forEach(d => {
      gridMap.set(`${d.topic}-${d.year}`, d);
    });

    return { topics: topicsArray, years: yearsArray, grid: gridMap, maxFreq: maxFrequency };
  }, [data]);

  if (!data || data.length === 0) {
    return <div className="flex h-[350px] items-center justify-center text-zinc-500">No data available</div>;
  }

  const getIntensityClass = (frequency: number, max: number) => {
    if (frequency === 0) return "bg-muted/30";
    const ratio = frequency / max;
    if (ratio <= 0.25) return "bg-primary/20";
    if (ratio <= 0.5) return "bg-primary/50";
    if (ratio <= 0.75) return "bg-primary/80";
    return "bg-primary";
  };

  return (
    <div className="w-full overflow-x-auto pb-4">
      <div className="min-w-max">
        {/* Years Header */}
        <div className="flex ml-40 gap-1">
          {years.map((year) => (
            <div key={year} className="w-12 text-center text-xs text-zinc-500 mb-2 truncate">
              {year}
            </div>
          ))}
        </div>

        {/* Grid Body */}
        <div className="flex flex-col gap-1">
          {topics.map((topic) => (
            <div key={topic} className="flex items-center">
              <div className="w-40 truncate pr-4 text-xs text-zinc-400 text-right" title={topic}>
                {topic}
              </div>
              <div className="flex gap-1">
                {years.map((year) => {
                  const cell = grid.get(`${topic}-${year}`) || { topic, year, frequency: 0 };
                  
                  return (
                    <motion.div
                      key={`${topic}-${year}`}
                      whileHover={{ scale: 1.1, zIndex: 10 }}
                      onMouseEnter={() => setHoveredCell(cell)}
                      onMouseLeave={() => setHoveredCell(null)}
                      className={cn(
                        "h-8 w-12 rounded relative cursor-pointer transition-colors duration-200",
                        getIntensityClass(cell.frequency, maxFreq)
                      )}
                    >
                      {hoveredCell === cell && (
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-max z-50 rounded-lg border border-[#27272a] bg-[#18181b] px-3 py-2 text-xs shadow-xl pointer-events-none">
                          <div className="font-medium text-zinc-300">{cell.topic}</div>
                          <div className="text-zinc-400 mt-1">Year: {cell.year}</div>
                          <div className="text-[#a78bfa]">Frequency: {cell.frequency}</div>
                        </div>
                      )}
                    </motion.div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
