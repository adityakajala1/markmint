"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { TopicFrequency } from "@/lib/types";
import { cn } from "@/lib/utils";

const PRIMARY_COLOR = "#a78bfa";
const MUTED_FG = "#a1a1aa";
const BORDER = "#27272a";

interface Props {
  data: TopicFrequency[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-lg border border-[#27272a] bg-[#18181b] p-3 shadow-md">
        <p className="mb-2 font-medium text-zinc-300">{label}</p>
        <p className="text-sm" style={{ color: PRIMARY_COLOR }}>
          Frequency: <span className="font-semibold">{payload[0].value}</span>
        </p>
      </div>
    );
  }
  return null;
};

export function TopicFrequencyChart({ data }: Props) {
  if (!data || data.length === 0) {
    return <div className="flex h-[350px] items-center justify-center text-zinc-500">No data available</div>;
  }

  return (
    <div className="h-[350px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={BORDER} vertical={false} />
          <XAxis 
            dataKey="topic" 
            tick={{ fill: MUTED_FG, fontSize: 12 }} 
            tickLine={false}
            axisLine={{ stroke: BORDER }}
            angle={-45}
            textAnchor="end"
            height={60}
          />
          <YAxis 
            tick={{ fill: MUTED_FG, fontSize: 12 }} 
            tickLine={false}
            axisLine={{ stroke: BORDER }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: '#27272a', opacity: 0.4 }} />
          <Bar 
            dataKey="frequency" 
            fill={PRIMARY_COLOR} 
            radius={[4, 4, 0, 0]} 
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
