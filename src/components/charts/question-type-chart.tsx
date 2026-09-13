"use client";

import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { QuestionTypeBreakdown } from "@/lib/types";

const PALETTE = ['#a78bfa', '#6366f1', '#22c55e', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899', '#8b5cf6', '#14b8a6', '#f97316', '#84cc16', '#e879f9'];

interface Props {
  data: QuestionTypeBreakdown[];
}

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="rounded-lg border border-[#27272a] bg-[#18181b] p-3 shadow-md">
        <p className="font-medium text-zinc-300 mb-1">{data.type || data.name}</p>
        <p className="text-sm" style={{ color: payload[0].color }}>
          Count: <span className="font-semibold">{payload[0].value}</span>
        </p>
      </div>
    );
  }
  return null;
};

export function QuestionTypeChart({ data }: Props) {
  if (!data || data.length === 0) {
    return <div className="flex h-[350px] items-center justify-center text-zinc-500">No data available</div>;
  }

  const total = data.reduce((sum, item) => sum + (item.count || item.value || 0), 0);
  const dataKey = data[0]?.count !== undefined ? "count" : "value";
  const nameKey = data[0]?.type !== undefined ? "type" : "name";

  return (
    <div className="h-[350px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            fill="#8884d8"
            dataKey={dataKey}
            nameKey={nameKey}
            isAnimationActive={true}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={PALETTE[index % PALETTE.length]} stroke="#18181b" strokeWidth={2} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ fontSize: '12px', color: '#a1a1aa' }} 
            iconType="circle"
          />
          <text
            x="50%"
            y="50%"
            textAnchor="middle"
            dominantBaseline="middle"
            className="fill-zinc-300 text-xl font-bold"
          >
            {total}
          </text>
          <text
            x="50%"
            y="58%"
            textAnchor="middle"
            dominantBaseline="middle"
            className="fill-zinc-500 text-xs"
          >
            Total
          </text>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
