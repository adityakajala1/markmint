"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { UnitDistribution } from "@/lib/types";

const ACCENT_COLOR = "#6366f1";
const MUTED_FG = "#a1a1aa";
const BORDER = "#27272a";

interface Props {
  data: UnitDistribution[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-lg border border-[#27272a] bg-[#18181b] p-3 shadow-md">
        <p className="mb-2 font-medium text-zinc-300">{label}</p>
        <p className="text-sm" style={{ color: ACCENT_COLOR }}>
          Weight: <span className="font-semibold">{payload[0].value}</span>
        </p>
      </div>
    );
  }
  return null;
};

export function UnitDistributionChart({ data }: Props) {
  if (!data || data.length === 0) {
    return <div className="flex h-[300px] items-center justify-center text-zinc-500">No data available</div>;
  }

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 20, right: 30, left: 60, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke={BORDER} horizontal={false} />
          <XAxis 
            type="number" 
            tick={{ fill: MUTED_FG, fontSize: 12 }} 
            tickLine={false}
            axisLine={{ stroke: BORDER }}
          />
          <YAxis 
            dataKey="unit" 
            type="category" 
            tick={{ fill: MUTED_FG, fontSize: 12 }} 
            tickLine={false}
            axisLine={{ stroke: BORDER }}
            width={80}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: '#27272a', opacity: 0.4 }} />
          <Bar 
            dataKey="weight" 
            fill={ACCENT_COLOR} 
            radius={[0, 4, 4, 0]} 
            barSize={24}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
