"use client";

import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { MarksPattern } from "@/lib/types";

const PALETTE = ['#a78bfa', '#6366f1', '#22c55e', '#f59e0b', '#ef4444', '#06b6d4'];
const MUTED_FG = "#a1a1aa";
const BORDER = "#27272a";

interface Props {
  data: MarksPattern[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    let total = 0;
    return (
      <div className="rounded-lg border border-[#27272a] bg-[#18181b] p-3 shadow-md min-w-[150px]">
        <p className="mb-2 font-medium text-zinc-300">Year {label}</p>
        <div className="flex flex-col gap-1">
          {payload.map((entry: any, index: number) => {
            total += entry.value;
            return (
              <div key={index} className="flex items-center justify-between gap-4 text-sm">
                <span style={{ color: entry.color }}>{entry.name} Marks</span>
                <span className="font-semibold text-zinc-200">{entry.value}</span>
              </div>
            );
          })}
          <div className="mt-2 pt-2 border-t border-zinc-800 flex items-center justify-between gap-4 text-sm">
            <span className="text-zinc-400">Total Count</span>
            <span className="font-bold text-zinc-100">{total}</span>
          </div>
        </div>
      </div>
    );
  }
  return null;
};

export function MarksPatternChart({ data }: Props) {
  if (!data || data.length === 0) {
    return <div className="flex h-[400px] items-center justify-center text-zinc-500">No data available</div>;
  }

  // Extract keys dynamically and prioritize '2marks', '5marks', '10marks', '15marks' if they exist
  const firstItem = data[0] || {};
  let categories = Object.keys(firstItem).filter(key => key !== 'year');
  const preferred = ['2marks', '5marks', '10marks', '15marks'];
  
  if (preferred.every(p => categories.includes(p))) {
    categories = preferred;
  }

  return (
    <div className="h-[400px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
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
          <Tooltip content={<CustomTooltip />} cursor={{ fill: '#27272a', opacity: 0.4 }} />
          <Legend 
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px', color: '#a1a1aa' }}
            formatter={(value) => <span className="text-zinc-400">{value}</span>}
          />
          {categories.map((category, i) => (
            <Bar 
              key={category}
              dataKey={category} 
              stackId="a" 
              fill={PALETTE[i % PALETTE.length]} 
              radius={i === categories.length - 1 ? [4, 4, 0, 0] : [0, 0, 0, 0]}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
