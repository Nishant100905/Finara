import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { AlertTriangle, CheckCircle2, Info, Sparkles } from "lucide-react";
import {
  Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";
import { api } from "@/services/api";
import { GlassCard } from "@/components/common/GlassCard";
import { SectionHeader } from "@/components/common/SectionHeader";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/_app/financial-health")({
  component: HealthPage,
  head: () => ({ meta: [{ title: "Financial Health — Finara" }] }),
});

const chartTooltip = { contentStyle: { background: "oklch(0.18 0.02 265 / 0.95)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, color: "white", fontSize: 12 }, labelStyle: { color: "rgb(180,190,210)" } };

function HealthPage() {
  const { data, isLoading } = useQuery({ queryKey: ["health"], queryFn: api.getFinancialHealth });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Financial health</h1>
        <p className="mt-1 text-sm text-muted-foreground">A holistic look at your money, scored across six dimensions.</p>
      </div>

      {/* Overall score */}
      <div className="grid gap-4 xl:grid-cols-3">
        <GlassCard className="xl:col-span-1">
          {isLoading || !data ? <Skeleton className="h-72" /> : <Gauge value={data.overall} />}
        </GlassCard>
        <GlassCard className="xl:col-span-2">
          <SectionHeader title="6-month trend" description="Your composite score over time" />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data?.trend ?? []}>
                <defs>
                  <linearGradient id="trG" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--color-primary)" stopOpacity={0.5} />
                    <stop offset="100%" stopColor="var(--color-primary)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="month" stroke="rgb(150,160,180)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis domain={[40, 100]} stroke="rgb(150,160,180)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip {...chartTooltip} />
                <Area type="monotone" dataKey="score" stroke="var(--color-primary)" strokeWidth={2.5} fill="url(#trG)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>

      {/* Sub-scores */}
      <SectionHeader title="Score breakdown" description="Tap any card to see recommendations." />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {isLoading || !data
          ? Array.from({ length: 6 }).map((_, i) => <Skeleton key={i} className="h-40 rounded-2xl" />)
          : data.scores.map((s, i) => (
              <motion.div key={s.key} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}>
                <ScoreCard label={s.label} score={s.score} trend={s.trend} hint={s.hint} />
              </motion.div>
            ))}
      </div>

      {/* Recommendations */}
      <SectionHeader title="AI recommendations" description="Prioritized by potential impact." />
      <div className="grid gap-3">
        {(data?.recommendations ?? []).map((r) => <RecCard key={r.id} rec={r} />)}
      </div>
    </div>
  );
}

function Gauge({ value }: { value: number }) {
  const r = 90;
  const c = Math.PI * r;
  const off = c - (value / 100) * c;
  const grade =
    value >= 85 ? { label: "Excellent", color: "text-success" }
    : value >= 70 ? { label: "Good", color: "text-primary" }
    : value >= 55 ? { label: "Fair", color: "text-warning" }
    : { label: "Needs work", color: "text-destructive" };
  return (
    <div className="flex flex-col items-center">
      <div className="text-xs uppercase tracking-wider text-muted-foreground">Composite score</div>
      <svg width={240} height={140} viewBox="0 0 240 140">
        <path d={`M 30 130 A ${r} ${r} 0 0 1 210 130`} stroke="rgba(255,255,255,0.08)" strokeWidth={14} fill="none" strokeLinecap="round" />
        <motion.path
          d={`M 30 130 A ${r} ${r} 0 0 1 210 130`}
          stroke="url(#gg)" strokeWidth={14} fill="none" strokeLinecap="round"
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          animate={{ strokeDashoffset: off }}
          transition={{ duration: 1.1, ease: [0.2, 0.7, 0.2, 1] }}
        />
        <defs>
          <linearGradient id="gg" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="var(--color-primary)" />
            <stop offset="100%" stopColor="var(--color-accent)" />
          </linearGradient>
        </defs>
      </svg>
      <div className="-mt-6 text-center">
        <div className="text-5xl font-semibold tracking-tight">{value}</div>
        <div className={cn("mt-1 text-sm font-medium", grade.color)}>{grade.label}</div>
      </div>
      <p className="mt-4 max-w-xs text-center text-xs text-muted-foreground">
        Your composite score is based on 6 dimensions. Improving your weakest area yields the fastest gains.
      </p>
    </div>
  );
}

function ScoreCard({ label, score, trend, hint }: { label: string; score: number; trend: number; hint: string }) {
  const color = score >= 80 ? "var(--color-success)" : score >= 65 ? "var(--color-primary)" : score >= 50 ? "var(--color-warning)" : "var(--color-destructive)";
  return (
    <div className="glass hover-lift rounded-2xl p-5">
      <div className="flex items-center justify-between">
        <div className="text-sm font-medium text-muted-foreground">{label}</div>
        <span className={cn("rounded-full px-2 py-0.5 text-[10px] font-medium", trend >= 0 ? "bg-success/15 text-success" : "bg-destructive/15 text-destructive")}>
          {trend >= 0 ? "+" : ""}{trend.toFixed(1)}
        </span>
      </div>
      <div className="mt-2 flex items-end gap-2">
        <div className="text-4xl font-semibold" style={{ color }}>{score}</div>
        <div className="pb-1 text-xs text-muted-foreground">/ 100</div>
      </div>
      <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/5">
        <motion.div className="h-full rounded-full" style={{ background: color }}
          initial={{ width: 0 }} animate={{ width: `${score}%` }} transition={{ duration: 1, ease: [0.2, 0.7, 0.2, 1] }} />
      </div>
      <p className="mt-3 text-xs text-muted-foreground">{hint}</p>
    </div>
  );
}

function RecCard({ rec }: { rec: { id: string; title: string; body: string; severity: "low" | "medium" | "high" } }) {
  const cfg = {
    high:   { icon: AlertTriangle,  color: "text-destructive", bg: "bg-destructive/10", ring: "border-destructive/30", label: "High priority" },
    medium: { icon: Info,           color: "text-warning",     bg: "bg-warning/10",     ring: "border-warning/30",     label: "Medium" },
    low:    { icon: CheckCircle2,   color: "text-success",     bg: "bg-success/10",     ring: "border-success/30",     label: "Low" },
  }[rec.severity];
  const Icon = cfg.icon;
  return (
    <div className={cn("flex items-start gap-4 rounded-2xl border p-4", cfg.ring, cfg.bg)}>
      <div className={cn("grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-white/5", cfg.color)}>
        <Icon className="h-5 w-5" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <div className="font-medium">{rec.title}</div>
          <Badge variant="secondary" className="border-white/10 bg-white/5 text-[10px]">{cfg.label}</Badge>
        </div>
        <p className="mt-1 text-sm text-muted-foreground">{rec.body}</p>
      </div>
      <Button size="sm" variant="outline" className="border-white/10 bg-white/[0.03]"><Sparkles className="mr-1.5 h-3.5 w-3.5" />Fix with AI</Button>
    </div>
  );
}
