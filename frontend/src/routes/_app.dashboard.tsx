import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import {
  Wallet, TrendingUp, PiggyBank, Receipt, ArrowUpRight, ArrowDownRight,
  Sparkles, Plus, Target, MessageSquareText, ArrowRight,
} from "lucide-react";
import {
  Area, AreaChart, CartesianGrid, Legend, Line, LineChart,
  Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis, Cell,
} from "recharts";
import { api } from "@/services/api";
import { useAuth } from "@/context/AuthContext";
import { StatCard } from "@/components/common/StatCard";
import { GlassCard } from "@/components/common/GlassCard";
import { SectionHeader } from "@/components/common/SectionHeader";
import { ChangePill } from "@/components/common/ChangePill";
import { Sparkline } from "@/components/common/Sparkline";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { formatCurrency, formatPercent, formatDate } from "@/lib/format";

export const Route = createFileRoute("/_app/dashboard")({
  component: DashboardPage,
  head: () => ({ meta: [{ title: "Dashboard — Finara" }] }),
});

const chartTooltip = {
  contentStyle: {
    background: "oklch(0.18 0.02 265 / 0.95)",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: 12,
    color: "white",
    fontSize: 12,
  },
  labelStyle: { color: "rgb(180,190,210)" },
};

function DashboardPage() {
  const { user } = useAuth();
  const { data, isLoading } = useQuery({ queryKey: ["dashboard"], queryFn: api.getDashboard });

  const greeting = (() => {
    const h = new Date().getHours();
    if (h < 12) return "Good morning";
    if (h < 18) return "Good afternoon";
    return "Good evening";
  })();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="text-sm text-muted-foreground">{greeting},</div>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
            {user?.name?.split(" ")[0] ?? "there"} <span className="gradient-text">👋</span>
          </h1>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button asChild variant="outline" className="border-white/10 bg-white/[0.03]">
            <Link to="/goals"><Target className="mr-2 h-4 w-4" />New goal</Link>
          </Button>
          <Button asChild className="gradient-brand text-primary-foreground">
            <Link to="/assistant"><MessageSquareText className="mr-2 h-4 w-4" />Ask AI</Link>
          </Button>
        </div>
      </div>

      {/* AI Insight */}
      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <div className="relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-primary/15 via-accent/10 to-transparent p-5 shadow-elegant sm:p-6">
          <div className="pointer-events-none absolute -right-16 -top-16 h-64 w-64 rounded-full bg-primary/30 blur-3xl" />
          <div className="relative flex items-start gap-4">
            <div className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl gradient-brand text-primary-foreground shadow-glow">
              <Sparkles className="h-5 w-5" />
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2">
                <div className="text-xs font-medium uppercase tracking-wider text-primary">AI insight of the day</div>
                <Badge variant="secondary" className="border-white/10 bg-white/5">Personalized</Badge>
              </div>
              <div className="mt-2 text-base leading-relaxed text-foreground/90 sm:text-lg">
                {isLoading ? <Skeleton className="h-6 w-3/4" /> : data?.summary.aiInsight}
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                <Button size="sm" asChild className="gradient-brand text-primary-foreground">
                  <Link to="/assistant">Explore in chat <ArrowRight className="ml-1.5 h-3.5 w-3.5" /></Link>
                </Button>
                <Button size="sm" variant="outline" className="border-white/10 bg-white/[0.03]">Dismiss</Button>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Stat grid */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {isLoading || !data ? (
          Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-32 rounded-2xl" />)
        ) : (
          <>
            <StatCard
              label="Net Worth" value={formatCurrency(data.summary.netWorth)}
              hint="Across all accounts" icon={<Wallet className="h-5 w-5" />}
              changePct={data.summary.netWorthChangePct} accent="primary"
            />
            <StatCard
              label="Portfolio Value" value={formatCurrency(data.summary.portfolioValue)}
              hint="Invested capital + returns" icon={<TrendingUp className="h-5 w-5" />}
              changePct={data.summary.portfolioChangePct} accent="accent"
            />
            <StatCard
              label="Monthly Savings" value={`${data.summary.savingsRate}%`}
              hint={`${formatCurrency(data.summary.cashFlow, { compact: true })} cash flow`}
              icon={<PiggyBank className="h-5 w-5" />} accent="success"
            />
            <StatCard
              label="Expenses" value={formatCurrency(data.summary.monthlyExpenses)}
              hint="This month" icon={<Receipt className="h-5 w-5" />}
              changePct={-3.4} accent="warning"
            />
          </>
        )}
      </div>

      {/* Charts row */}
      <div className="grid gap-4 xl:grid-cols-3">
        <GlassCard className="xl:col-span-2">
          <SectionHeader
            title="Portfolio performance"
            description="Last 7 months vs benchmark"
            action={
              <div className="hidden sm:flex gap-1 rounded-full border border-white/10 bg-white/5 p-1 text-xs">
                {["1M","3M","6M","1Y","All"].map((r,i) => (
                  <button key={r} className={`rounded-full px-3 py-1 ${i===3?"gradient-brand text-primary-foreground":"text-muted-foreground hover:text-foreground"}`}>{r}</button>
                ))}
              </div>
            }
          />
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data?.performance ?? []} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="valG" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--color-primary)" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="var(--color-primary)" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="bmG" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--color-accent)" stopOpacity={0.2} />
                    <stop offset="100%" stopColor="var(--color-accent)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="date" stroke="rgb(150,160,180)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgb(150,160,180)" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => formatCurrency(v, { compact: true })} />
                <Tooltip {...chartTooltip} formatter={(v: number) => formatCurrency(v)} />
                <Area type="monotone" dataKey="benchmark" stroke="var(--color-accent)" strokeWidth={2} fill="url(#bmG)" strokeDasharray="4 3" />
                <Area type="monotone" dataKey="value" stroke="var(--color-primary)" strokeWidth={2.5} fill="url(#valG)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <GlassCard>
          <SectionHeader title="Investment allocation" description="By asset class" />
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={data?.allocation ?? []} dataKey="value" innerRadius={54} outerRadius={82} paddingAngle={3} stroke="none">
                  {(data?.allocation ?? []).map((entry) => <Cell key={entry.name} fill={entry.color} />)}
                </Pie>
                <Tooltip {...chartTooltip} formatter={(v: number, n) => [formatCurrency(v), n as string]} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-3 space-y-1.5">
            {(data?.allocation ?? []).slice(0, 4).map((a) => (
              <div key={a.name} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 rounded-full" style={{ background: a.color }} />
                  <span className="text-muted-foreground">{a.name}</span>
                </div>
                <span className="font-medium">{formatCurrency(a.value, { compact: true })}</span>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Cash flow + transactions */}
      <div className="grid gap-4 xl:grid-cols-3">
        <GlassCard className="xl:col-span-2">
          <SectionHeader title="Cash flow" description="Income vs expenses" />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data?.cashFlow ?? []}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="month" stroke="rgb(150,160,180)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgb(150,160,180)" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => formatCurrency(v, { compact: true })} />
                <Tooltip {...chartTooltip} formatter={(v: number) => formatCurrency(v)} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Line type="monotone" dataKey="income" stroke="var(--color-success)" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="expenses" stroke="var(--color-destructive)" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="savings" stroke="var(--color-primary)" strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <GlassCard>
          <SectionHeader
            title="Recent transactions"
            action={<Link to="/portfolio" className="text-xs text-primary hover:underline">View all</Link>}
          />
          <ul className="divide-y divide-white/5">
            {(data?.transactions ?? []).map((t) => (
              <li key={t.id} className="flex items-center gap-3 py-3">
                <Avatar className="h-9 w-9">
                  <AvatarFallback className="bg-white/5 text-xs">{t.merchant?.slice(0, 2).toUpperCase() ?? "TX"}</AvatarFallback>
                </Avatar>
                <div className="min-w-0 flex-1">
                  <div className="truncate text-sm font-medium">{t.title}</div>
                  <div className="text-xs text-muted-foreground">{t.category} · {formatDate(t.date)}</div>
                </div>
                <div className={`text-sm font-medium ${t.type === "credit" ? "text-success" : "text-foreground/90"}`}>
                  {t.type === "credit" ? "+" : "−"}{formatCurrency(t.amount, { compact: true })}
                </div>
              </li>
            ))}
          </ul>
        </GlassCard>
      </div>

      {/* Goals + market + watchlist */}
      <div className="grid gap-4 xl:grid-cols-3">
        <GlassCard>
          <SectionHeader
            title="Goals"
            action={<Link to="/goals" className="text-xs text-primary hover:underline">Manage</Link>}
          />
          <div className="space-y-4">
            {(data?.goals ?? []).map((g) => {
              const pct = Math.min(100, Math.round((g.current / g.target) * 100));
              return (
                <div key={g.id}>
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{g.emoji}</span>
                      <span className="font-medium">{g.title}</span>
                    </div>
                    <span className="text-muted-foreground">{pct}%</span>
                  </div>
                  <Progress value={pct} className="mt-2 h-2 bg-white/5" />
                  <div className="mt-1 flex items-center justify-between text-xs text-muted-foreground">
                    <span>{formatCurrency(g.current, { compact: true })} / {formatCurrency(g.target, { compact: true })}</span>
                    <span>{formatCurrency(g.monthlyContribution, { compact: true })}/mo</span>
                  </div>
                </div>
              );
            })}
          </div>
        </GlassCard>

        <GlassCard>
          <SectionHeader title="Market summary" action={<Link to="/market" className="text-xs text-primary hover:underline">Open</Link>} />
          <ul className="space-y-3">
            {(data?.market.indices ?? []).map((m) => (
              <li key={m.symbol} className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium">{m.name}</div>
                  <div className="text-xs text-muted-foreground">{m.symbol}</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-20"><Sparkline data={m.spark} positive={m.changePct >= 0} height={28} /></div>
                  <div className="text-right">
                    <div className="text-sm font-medium">{m.price.toLocaleString("en-IN", { maximumFractionDigits: 2 })}</div>
                    <ChangePill value={m.changePct} />
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </GlassCard>

        <GlassCard>
          <SectionHeader title="Watchlist" action={<Button size="sm" variant="outline" className="h-7 border-white/10 bg-white/5"><Plus className="mr-1 h-3 w-3" />Add</Button>} />
          <ul className="space-y-3">
            {(data?.market.watchlist ?? []).map((w) => (
              <li key={w.symbol} className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium">{w.symbol}</div>
                  <div className="text-xs text-muted-foreground">{w.name}</div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium">{formatCurrency(w.price, { compact: true })}</div>
                  <ChangePill value={w.changePct} />
                </div>
              </li>
            ))}
          </ul>
          <div className="mt-4 rounded-xl border border-white/5 bg-white/[0.03] p-3">
            <div className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Top news</div>
            <ul className="mt-2 space-y-2 text-sm">
              {(data?.market.news ?? []).slice(0, 3).map((n) => (
                <li key={n.id} className="flex items-start gap-2">
                  <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                  <span className="text-foreground/90 line-clamp-2">{n.title}</span>
                </li>
              ))}
            </ul>
          </div>
        </GlassCard>
      </div>

      {/* Quick actions */}
      <GlassCard>
        <SectionHeader title="Quick actions" />
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { icon: Plus,           label: "Add transaction", to: "/portfolio",        color: "from-primary/25" },
            { icon: Target,         label: "New goal",         to: "/goals",            color: "from-accent/25" },
            { icon: MessageSquareText, label: "Ask AI",        to: "/assistant",        color: "from-chart-3/25" },
            { icon: TrendingUp,     label: "Explore market",   to: "/market",           color: "from-warning/25" },
          ].map((a) => {
            const Icon = a.icon;
            return (
              <Link key={a.label} to={a.to} className="group relative overflow-hidden rounded-2xl border border-white/10 bg-white/[0.03] p-4 transition hover:bg-white/[0.06]">
                <div className={`absolute -right-8 -top-8 h-24 w-24 rounded-full bg-gradient-to-br ${a.color} to-transparent blur-2xl`} />
                <div className="relative flex items-center gap-3">
                  <div className="grid h-9 w-9 place-items-center rounded-xl bg-white/5">
                    <Icon className="h-4.5 w-4.5 h-[18px] w-[18px]" />
                  </div>
                  <div className="text-sm font-medium">{a.label}</div>
                  <ArrowUpRight className="ml-auto h-4 w-4 text-muted-foreground transition group-hover:text-primary" />
                </div>
              </Link>
            );
          })}
        </div>
      </GlassCard>
    </div>
  );
}
