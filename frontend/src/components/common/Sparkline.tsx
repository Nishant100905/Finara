import { Area, AreaChart, ResponsiveContainer } from "recharts";

export function Sparkline({
  data,
  positive = true,
  height = 40,
}: {
  data: number[];
  positive?: boolean;
  height?: number;
}) {
  const rows = data.map((v, i) => ({ i, v }));
  const color = positive ? "var(--color-success)" : "var(--color-destructive)";
  const id = `sp-${Math.random().toString(36).slice(2, 8)}`;
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={rows} margin={{ top: 2, right: 2, left: 2, bottom: 2 }}>
          <defs>
            <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={color} stopOpacity={0.4} />
              <stop offset="100%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <Area type="monotone" dataKey="v" stroke={color} strokeWidth={1.75} fill={`url(#${id})`} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
