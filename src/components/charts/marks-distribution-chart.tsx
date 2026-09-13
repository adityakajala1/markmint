"use client";

import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { MarksDistribution } from "@/lib/types";

const PALETTE = ['#a78bfa', '#6366f1', '#22c55e', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899', '#8b5cf6', '#14b8a6', '#f97316', '#84cc16', '#e879f9'];

interface Props {
  data: MarksDistribution[];
}

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="rounded-lg border border-[#27272a] bg-[#18181b] p-3 shadow-md">
        <p className="font-medium text-zinc-300 mb-1">{data.name || data.marks}</p>
        <p className="text-sm" style={{ color: payload[0].color }}>
          Count: <span className="font-semibold">{payload[0].value}</span>
        </p>
      </div>
    );
  }
  return null;
};

export function MarksDistributionChart({ data }: Props) {
  if (!data || data.length === 0) {
    return <div className="flex h-[350px] items-center justify-center text-zinc-500">No data available</div>;
  }

  return (
    <div className="h-[350px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
              const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
              const x = cx + radius * Math.cos(-midAngle * Math.PI / 180);
              const y = cy + radius * Math.sin(-midAngle * Math.PI / 180);
              return percent > 0.05 ? (
                <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central" className="text-xs font-medium">
                  {`${(percent * 100).toFixed(0)}%`}
                </text>
              ) : null;
            }}
            outerRadius={120}
            innerRadius={0}
            fill="#8884d8"
            dataKey={data[0]?.count !== undefined ? "count" : "value"}
            nameKey={data[0]?.name !== undefined ? "name" : "marks"}
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
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
