import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import {
  Cell, Pie, PieChart, ResponsiveContainer, Tooltip,
  Area, AreaChart, XAxis, YAxis, CartesianGrid,
} from "recharts";
import { Search, TrendingUp, TrendingDown, ArrowUpDown, ChevronLeft, ChevronRight } from "lucide-react";
import { api } from "@/services/api";
import type { Holding } from "@/data/mock";
import { GlassCard } from "@/components/common/GlassCard";
import { SectionHeader } from "@/components/common/SectionHeader";
import { ChangePill } from "@/components/common/ChangePill";
import { StatCard } from "@/components/common/StatCard";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Drawer, DrawerContent, DrawerDescription, DrawerHeader, DrawerTitle } from "@/components/ui/drawer";
import { Skeleton } from "@/components/ui/skeleton";
import { formatCurrency } from "@/lib/format";

export const Route = createFileRoute("/_app/portfolio")({
  component: PortfolioPage,
  head: () => ({ meta: [{ title: "Portfolio — Finara" }] }),
});

const TYPES = ["All", "Stocks", "Mutual Funds", "Crypto", "Gold", "Fixed Deposits", "Cash"] as const;
type SortKey = "name" | "value" | "changePct";

const chartTooltip = {
  contentStyle: { background: "oklch(0.18 0.02 265 / 0.95)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, color: "white", fontSize: 12 },
  labelStyle: { color: "rgb(180,190,210)" },
};

function PortfolioPage() {
  const { data: holdings, isLoading } = useQuery({ queryKey: ["holdings"], queryFn: api.getHoldings });
  const { data: allocation } = useQuery({ queryKey: ["allocation"], queryFn: api.getAllocation });
  const { data: performance } = useQuery({ queryKey: ["perf"], queryFn: api.getPortfolioPerformance });
  const { data: movers } = useQuery({ queryKey: ["movers"], queryFn: api.getTopMovers });

  const [query, setQuery] = useState("");
  const [type, setType] = useState<(typeof TYPES)[number]>("All");
  const [sort, setSort] = useState<{ key: SortKey; dir: "asc" | "desc" }>({ key: "value", dir: "desc" });
  const [page, setPage] = useState(1);
  const perPage = 8;
  const [selected, setSelected] = useState<Holding | null>(null);

  const total = holdings?.reduce((s, h) => s + h.value, 0) ?? 0;
  const invested = holdings?.reduce((s, h) => s + h.avgPrice * h.quantity, 0) ?? 0;
  const gain = total - invested;
  const gainPct = invested ? (gain / invested) * 100 : 0;

  const filtered = useMemo(() => {
    const list = (holdings ?? []).filter((h) => {
      const okType = type === "All" || h.type === type;
      const okQ = !query || h.name.toLowerCase().includes(query.toLowerCase()) || h.symbol.toLowerCase().includes(query.toLowerCase());
      return okType && okQ;
    });
    return list.sort((a, b) => {
      const av = a[sort.key], bv = b[sort.key];
      const cmp = typeof av === "number" && typeof bv === "number" ? av - bv : String(av).localeCompare(String(bv));
      return sort.dir === "asc" ? cmp : -cmp;
    });
  }, [holdings, query, type, sort]);

  const paged = filtered.slice((page - 1) * perPage, page * perPage);
  const pages = Math.max(1, Math.ceil(filtered.length / perPage));

  const toggleSort = (key: SortKey) => setSort((s) => ({ key, dir: s.key === key && s.dir === "desc" ? "asc" : "desc" }));

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Portfolio</h1>
          <p className="mt-1 text-sm text-muted-foreground">All your investments, one clean view.</p>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Total Value" value={formatCurrency(total)} hint="Current market value" accent="primary" />
        <StatCard label="Invested" value={formatCurrency(invested)} hint="Capital deployed" accent="accent" />
        <StatCard label="Overall Gain" value={formatCurrency(gain)} hint="Realized + unrealized" changePct={gainPct} accent={gain >= 0 ? "success" : "destructive"} />
        <StatCard label="Holdings" value={holdings?.length ?? 0} hint={`${new Set(holdings?.map((h) => h.type)).size} asset classes`} accent="warning" />
      </div>

      <div className="grid gap-4 xl:grid-cols-3">
        <GlassCard className="xl:col-span-2">
          <SectionHeader title="Performance" description="Portfolio value over time" />
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={performance ?? []}>
                <defs>
                  <linearGradient id="pfG" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--color-primary)" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="var(--color-primary)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="date" stroke="rgb(150,160,180)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgb(150,160,180)" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => formatCurrency(v, { compact: true })} />
                <Tooltip {...chartTooltip} formatter={(v: number) => formatCurrency(v)} />
                <Area type="monotone" dataKey="value" stroke="var(--color-primary)" strokeWidth={2.5} fill="url(#pfG)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <GlassCard>
          <SectionHeader title="Allocation" description="By asset class" />
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={allocation ?? []} dataKey="value" innerRadius={54} outerRadius={82} paddingAngle={3} stroke="none">
                  {(allocation ?? []).map((e) => <Cell key={e.name} fill={e.color} />)}
                </Pie>
                <Tooltip {...chartTooltip} formatter={(v: number, n) => [formatCurrency(v), n as string]} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-3 grid grid-cols-2 gap-2">
            {(allocation ?? []).map((a) => (
              <div key={a.name} className="flex items-center gap-2 text-xs">
                <span className="h-2.5 w-2.5 rounded-full" style={{ background: a.color }} />
                <span className="truncate text-muted-foreground">{a.name}</span>
                <span className="ml-auto font-medium">{Math.round((a.value / total) * 100)}%</span>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Top movers */}
      <div className="grid gap-4 sm:grid-cols-2">
        <GlassCard>
          <SectionHeader title="Top gainers" action={<TrendingUp className="h-4 w-4 text-success" />} />
          <ul className="space-y-2">
            {(movers?.gainers ?? []).map((h) => (
              <li key={h.id} className="flex items-center justify-between rounded-xl bg-white/[0.03] p-3">
                <div>
                  <div className="text-sm font-medium">{h.symbol}</div>
                  <div className="text-xs text-muted-foreground">{h.name}</div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium">{formatCurrency(h.currentPrice)}</div>
                  <ChangePill value={h.changePct} />
                </div>
              </li>
            ))}
          </ul>
        </GlassCard>
        <GlassCard>
          <SectionHeader title="Top losers" action={<TrendingDown className="h-4 w-4 text-destructive" />} />
          <ul className="space-y-2">
            {(movers?.losers ?? []).map((h) => (
              <li key={h.id} className="flex items-center justify-between rounded-xl bg-white/[0.03] p-3">
                <div>
                  <div className="text-sm font-medium">{h.symbol}</div>
                  <div className="text-xs text-muted-foreground">{h.name}</div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium">{formatCurrency(h.currentPrice)}</div>
                  <ChangePill value={h.changePct} />
                </div>
              </li>
            ))}
          </ul>
        </GlassCard>
      </div>

      {/* Holdings */}
      <GlassCard>
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-semibold">Holdings</h2>
            <p className="text-sm text-muted-foreground">{filtered.length} of {holdings?.length ?? 0}</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input placeholder="Search…" value={query} onChange={(e) => { setQuery(e.target.value); setPage(1); }} className="h-9 w-56 pl-9 border-white/10 bg-white/[0.03]" />
            </div>
            <Tabs value={type} onValueChange={(v) => { setType(v as typeof type); setPage(1); }}>
              <TabsList className="border border-white/10 bg-white/[0.03]">
                {TYPES.map((t) => <TabsTrigger key={t} value={t} className="text-xs">{t}</TabsTrigger>)}
              </TabsList>
            </Tabs>
          </div>
        </div>

        <div className="mt-4 overflow-x-auto rounded-xl border border-white/5">
          <Table>
            <TableHeader>
              <TableRow className="border-white/5 hover:bg-transparent">
                <TableHead>
                  <button className="inline-flex items-center gap-1" onClick={() => toggleSort("name")}>Name <ArrowUpDown className="h-3 w-3" /></button>
                </TableHead>
                <TableHead>Type</TableHead>
                <TableHead className="text-right">Qty</TableHead>
                <TableHead className="text-right">Avg</TableHead>
                <TableHead className="text-right">Price</TableHead>
                <TableHead className="text-right">
                  <button className="inline-flex items-center gap-1" onClick={() => toggleSort("changePct")}>Δ <ArrowUpDown className="h-3 w-3" /></button>
                </TableHead>
                <TableHead className="text-right">
                  <button className="inline-flex items-center gap-1" onClick={() => toggleSort("value")}>Value <ArrowUpDown className="h-3 w-3" /></button>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <TableRow key={i} className="border-white/5"><TableCell colSpan={7}><Skeleton className="h-8 w-full" /></TableCell></TableRow>
                ))
              ) : paged.length === 0 ? (
                <TableRow><TableCell colSpan={7} className="py-10 text-center text-muted-foreground">No holdings match your filters</TableCell></TableRow>
              ) : (
                paged.map((h) => (
                  <TableRow key={h.id} className="cursor-pointer border-white/5 hover:bg-white/[0.03]" onClick={() => setSelected(h)}>
                    <TableCell>
                      <div className="text-sm font-medium">{h.symbol}</div>
                      <div className="text-xs text-muted-foreground">{h.name}</div>
                    </TableCell>
                    <TableCell><Badge variant="secondary" className="border-white/10 bg-white/5 text-xs">{h.type}</Badge></TableCell>
                    <TableCell className="text-right text-sm">{h.quantity}</TableCell>
                    <TableCell className="text-right text-sm">{formatCurrency(h.avgPrice)}</TableCell>
                    <TableCell className="text-right text-sm">{formatCurrency(h.currentPrice)}</TableCell>
                    <TableCell className="text-right"><ChangePill value={h.changePct} /></TableCell>
                    <TableCell className="text-right text-sm font-medium">{formatCurrency(h.value)}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>

        <div className="mt-4 flex items-center justify-between text-sm text-muted-foreground">
          <div>Page {page} of {pages}</div>
          <div className="flex gap-2">
            <Button size="sm" variant="outline" className="border-white/10 bg-white/[0.03]" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button size="sm" variant="outline" className="border-white/10 bg-white/[0.03]" disabled={page >= pages} onClick={() => setPage((p) => p + 1)}>
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </GlassCard>

      <Drawer open={!!selected} onOpenChange={(v) => !v && setSelected(null)}>
        <DrawerContent className="bg-background/95 backdrop-blur-xl">
          {selected && (
            <div className="mx-auto w-full max-w-2xl p-6">
              <DrawerHeader className="px-0">
                <DrawerTitle className="flex items-center gap-3">
                  <span className="grid h-10 w-10 place-items-center rounded-xl gradient-brand text-primary-foreground text-sm font-semibold">{selected.symbol.slice(0,2)}</span>
                  {selected.name}
                  <ChangePill value={selected.changePct} className="ml-2" />
                </DrawerTitle>
                <DrawerDescription>{selected.type} · {selected.symbol}</DrawerDescription>
              </DrawerHeader>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                {[
                  { k: "Quantity", v: selected.quantity },
                  { k: "Avg price", v: formatCurrency(selected.avgPrice) },
                  { k: "Current", v: formatCurrency(selected.currentPrice) },
                  { k: "Value", v: formatCurrency(selected.value) },
                ].map((s) => (
                  <div key={s.k} className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
                    <div className="text-xs text-muted-foreground">{s.k}</div>
                    <div className="mt-1 text-sm font-medium">{s.v}</div>
                  </div>
                ))}
              </div>
              <div className="mt-4 flex gap-2">
                <Button className="gradient-brand text-primary-foreground">Buy more</Button>
                <Button variant="outline" className="border-white/10 bg-white/[0.03]">Sell</Button>
                <Button variant="ghost">Set alert</Button>
              </div>
            </div>
          )}
        </DrawerContent>
      </Drawer>
    </div>
  );
}
