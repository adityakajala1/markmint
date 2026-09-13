"use client";

import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { HistoricalTrend } from "@/lib/types";
import { useState } from "react";

const PALETTE = ['#a78bfa', '#6366f1', '#22c55e', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899', '#8b5cf6', '#14b8a6', '#f97316', '#84cc16', '#e879f9'];
const MUTED_FG = "#a1a1aa";
const BORDER = "#27272a";

interface Props {
  data: HistoricalTrend[];
  topics: string[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-lg border border-[#27272a] bg-[#18181b] p-3 shadow-md max-w-xs">
        <p className="mb-2 font-medium text-zinc-300">Year {label}</p>
        <div className="flex flex-col gap-1">
          {payload.map((entry: any, index: number) => (
            <div key={index} className="flex items-center justify-between gap-4 text-sm">
              <span style={{ color: entry.color }} className="truncate max-w-[200px]">{entry.name}</span>
              <span className="font-semibold text-zinc-200">{entry.value}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return null;
};

export function HistoricalTrendsChart({ data, topics }: Props) {
  const [hiddenTopics, setHiddenTopics] = useState<Set<string>>(new Set());

  if (!data || data.length === 0 || !topics || topics.length === 0) {
    return <div className="flex h-[400px] items-center justify-center text-zinc-500">No data available</div>;
  }

  const toggleLine = (dataKey: string) => {
    setHiddenTopics(prev => {
      const next = new Set(prev);
      if (next.has(dataKey)) {
        next.delete(dataKey);
      } else {
        next.add(dataKey);
      }
      return next;
    });
  };

  return (
    <div className="h-[400px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={BORDER} vertical={false} />
          <XAxis 
            dataKey="year" 
            tick={{ fill: MUTED_FG, fontSize: 12 }} 
            tickLine={false}
            axisLine={{ stroke: BORDER }}
          />
          <YAxis 
            tick={{ fill: MUTED_FG, fontSize: 12 }} 
            tickLine={false}
            axisLine={{ stroke: BORDER }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#27272a', strokeWidth: 1 }} />
          <Legend 
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px', color: '#a1a1aa' }}
            onClick={(e) => toggleLine(e.dataKey as string)}
            formatter={(value, entry: any) => (
              <span className={hiddenTopics.has(entry.dataKey) ? "text-zinc-600 line-through" : "text-zinc-400 cursor-pointer hover:text-zinc-200 transition-colors"}>
                {value}
              </span>
            )}
          />
          {topics.map((topic, i) => (
            <Line
              key={topic}
              type="monotone"
              dataKey={topic}
              stroke={PALETTE[i % PALETTE.length]}
              strokeWidth={2}
              dot={{ r: 4, fill: '#18181b', strokeWidth: 2 }}
              activeDot={{ r: 6, strokeWidth: 0 }}
              hide={hiddenTopics.has(topic)}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
