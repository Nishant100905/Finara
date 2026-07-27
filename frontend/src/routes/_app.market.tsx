import { createFileRoute } from "@tanstack/react-router";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";
import {
  Search, Plus, TrendingUp, TrendingDown, Star, Loader2,
  ExternalLink, Calendar,
} from "lucide-react";
import { api } from "@/services/api";
import type { MarketQuote, MarketNews } from "@/data/mock";
import type { MarketSearchResult } from "@/lib/types";
import { GlassCard } from "@/components/common/GlassCard";
import { SectionHeader } from "@/components/common/SectionHeader";
import { ChangePill } from "@/components/common/ChangePill";
import { Sparkline } from "@/components/common/Sparkline";
import { StatCard } from "@/components/common/StatCard";
import { Input } from "@/components/ui/input";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription,
} from "@/components/ui/dialog";
import { formatCurrency } from "@/lib/format";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/_app/market")({
  component: MarketPage,
  head: () => ({ meta: [{ title: "Market — Finara" }] }),
});

function MarketPage() {
  const { data, isLoading } = useQuery({ queryKey: ["market"], queryFn: api.getMarket });
  const [q, setQ] = useState("");
  const [readingNews, setReadingNews] = useState<MarketNews | null>(null);

  const gainers = [...(data?.trending ?? [])].sort((a, b) => b.changePct - a.changePct).slice(0, 4);
  const losers  = [...(data?.trending ?? [])].sort((a, b) => a.changePct - b.changePct).slice(0, 4);

  // The input filter on the existing trending/crypto lists.
  const normalizedQuery = q.trim().toLowerCase();
  const localStocks = (data?.trending ?? []).filter(
    (f) =>
      !normalizedQuery ||
      f.name.toLowerCase().includes(normalizedQuery) ||
      f.symbol.toLowerCase().includes(normalizedQuery)
  );
  const localCrypto = (data?.crypto ?? []).filter(
    (f) =>
      !normalizedQuery ||
      f.name.toLowerCase().includes(normalizedQuery) ||
      f.symbol.toLowerCase().includes(normalizedQuery)
  );

  // Debounce the server-side search so we don't fire on every keystroke
  // when the local lists don't match. Only kick in once the user has
  // typed at least 2 chars and there are zero local matches.
  const [debouncedQ, setDebouncedQ] = useState("");
  useEffect(() => {
    const handle = window.setTimeout(() => setDebouncedQ(q.trim()), 350);
    return () => window.clearTimeout(handle);
  }, [q]);

  const shouldRunRemoteSearch =
    debouncedQ.length >= 2 && localStocks.length === 0 && localCrypto.length === 0;

  const {
    data: searchResults,
    isFetching: isSearching,
    isError: searchErrored,
  } = useQuery({
    queryKey: ["market-search", debouncedQ],
    queryFn: () => api.searchSymbols(debouncedQ, 10),
    enabled: shouldRunRemoteSearch,
    staleTime: 60_000,
    placeholderData: keepPreviousData,
  });

  const searchView = useMemo<{
    results: MarketSearchResult[];
    quotes: Map<string, MarketQuote | undefined>;
    loadingQuotes: boolean;
  }>(() => {
    const results = searchResults ?? [];
    return {
      results,
      quotes: new Map(results.map((r) => [r.symbol, undefined])),
      loadingQuotes: isSearching,
    };
  }, [searchResults, isSearching]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Market</h1>
          <p className="mt-1 text-sm text-muted-foreground">Real-time pulse of the markets, filtered by what matters to you.</p>
        </div>
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          {isSearching && (
            <Loader2 className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 animate-spin text-muted-foreground" />
          )}
          <Input
            placeholder="Search stocks, crypto… (try Apple, Tesla, RELIANCE)"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="h-10 w-full pl-9 sm:w-72 border-white/10 bg-white/[0.03]"
          />
        </div>
      </div>

      {/* Indices */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {isLoading || !data
          ? Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-32 rounded-2xl" />)
          : data.indices.map((idx) => (
              <StatCard
                key={idx.symbol}
                label={idx.name}
                value={idx.price.toLocaleString("en-IN", { maximumFractionDigits: 2 })}
                changePct={idx.changePct}
                accent={idx.changePct >= 0 ? "success" : "destructive"}
              />
            ))}
      </div>

      <div className="grid gap-4 xl:grid-cols-3">
        {/* Sentiment */}
        <GlassCard>
          <SectionHeader title="Market sentiment" description="Fear & greed index" />
          {data && <SentimentGauge score={data.sentiment.score} label={data.sentiment.label} />}
        </GlassCard>

        {/* Sectors */}
        <GlassCard className="xl:col-span-2">
          <SectionHeader title="Sector performance" description="Today" />
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            {(data?.sectors ?? []).map((s) => (
              <div
                key={s.name}
                className={cn(
                  "rounded-xl border p-3",
                  s.changePct >= 0 ? "border-success/20 bg-success/5" : "border-destructive/20 bg-destructive/5"
                )}
              >
                <div className="text-xs text-muted-foreground">{s.name}</div>
                <div
                  className={cn(
                    "mt-1 text-lg font-semibold",
                    s.changePct >= 0 ? "text-success" : "text-destructive"
                  )}
                >
                  {s.changePct >= 0 ? "+" : ""}
                  {s.changePct.toFixed(2)}%
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Movers */}
      <div className="grid gap-4 sm:grid-cols-2">
        <GlassCard>
          <SectionHeader title="Top gainers" action={<TrendingUp className="h-4 w-4 text-success" />} />
          <QuoteList list={gainers} />
        </GlassCard>
        <GlassCard>
          <SectionHeader title="Top losers" action={<TrendingDown className="h-4 w-4 text-destructive" />} />
          <QuoteList list={losers} />
        </GlassCard>
      </div>

      {/* Trending + crypto + live lookup */}
      <GlassCard>
        <Tabs defaultValue="stocks">
          <div className="flex items-center justify-between">
            <SectionHeader
              title={normalizedQuery ? `Results for "${q}"` : "Explore"}
              description=""
              className="mb-0"
            />
            <TabsList className="border border-white/10 bg-white/[0.03]">
              <TabsTrigger value="stocks">Stocks</TabsTrigger>
              <TabsTrigger value="crypto">Crypto</TabsTrigger>
              {shouldRunRemoteSearch && (
                <TabsTrigger value="search">Lookups</TabsTrigger>
              )}
            </TabsList>
          </div>
          <TabsContent value="stocks" className="mt-4">
            <QuoteGrid list={localStocks} emptyText="No trending stocks match." />
          </TabsContent>
          <TabsContent value="crypto" className="mt-4">
            <QuoteGrid list={localCrypto} emptyText="No crypto assets match." />
          </TabsContent>
          {shouldRunRemoteSearch && (
            <TabsContent value="search" className="mt-4">
              <SearchPanel
                results={searchView.results}
                loading={searchView.loadingQuotes}
                errored={searchErrored}
                onPick={(s) => setQ(s)}
              />
            </TabsContent>
          )}
        </Tabs>
      </GlassCard>

      {/* News */}
      <GlassCard>
        <SectionHeader title="Latest news" />
        <ul className="divide-y divide-white/5">
          {(data?.news ?? []).map((n) => (
            <li key={n.id} className="flex items-start gap-3 py-3">
              <Badge variant="secondary" className="mt-0.5 border-white/10 bg-white/5 text-[10px]">
                {n.tag}
              </Badge>
              <div className="min-w-0 flex-1">
                <div className="text-sm font-medium text-foreground/95">{n.title}</div>
                <div className="mt-0.5 text-xs text-muted-foreground">
                  {n.source} · {n.time}
                </div>
              </div>
              <Button
                size="sm"
                variant="ghost"
                className="shrink-0"
                onClick={() => setReadingNews(n)}
              >
                Read
              </Button>
            </li>
          ))}
        </ul>
      </GlassCard>

      <NewsReaderDialog
        news={readingNews}
        onOpenChange={(open) => {
          if (!open) setReadingNews(null);
        }}
      />
    </div>
  );
}

function SearchPanel({
  results,
  loading,
  errored,
  onPick,
}: {
  results: MarketSearchResult[];
  loading: boolean;
  errored: boolean;
  onPick: (symbol: string) => void;
}) {
  if (loading) {
    return (
      <div className="space-y-2">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-12 w-full rounded-xl" />
        ))}
      </div>
    );
  }
  if (errored) {
    return (
      <div className="rounded-xl border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive">
        Couldn't reach Yahoo Finance. Try again in a moment.
      </div>
    );
  }
  if (!results.length) {
    return <div className="py-10 text-center text-sm text-muted-foreground">No matching symbols found.</div>;
  }
  return (
    <ul className="space-y-2">
      {results.map((r) => (
        <li
          key={`${r.symbol}-${r.exchange ?? ""}`}
          className="flex items-center justify-between rounded-xl border border-white/5 bg-white/[0.03] p-3"
        >
          <div className="min-w-0">
            <div className="truncate text-sm font-medium">{r.symbol}</div>
            <div className="truncate text-xs text-muted-foreground">
              {r.name}
              {r.exchange ? ` · ${r.exchange}` : ""}
              {r.type ? ` · ${r.type}` : ""}
            </div>
          </div>
          <Button
            size="sm"
            variant="outline"
            className="border-white/10 bg-white/[0.03]"
            onClick={() => onPick(r.symbol)}
          >
            View
          </Button>
        </li>
      ))}
    </ul>
  );
}

function QuoteList({ list }: { list: MarketQuote[] }) {
  return (
    <ul className="space-y-2">
      {list.map((q) => (
        <li key={q.symbol} className="flex items-center justify-between rounded-xl bg-white/[0.03] p-3">
          <div>
            <div className="text-sm font-medium">{q.symbol}</div>
            <div className="text-xs text-muted-foreground">{q.name}</div>
          </div>
          <div className="w-16">
            <Sparkline data={q.spark} positive={q.changePct >= 0} height={28} />
          </div>
          <div className="text-right">
            <div className="text-sm font-medium">
              {formatCurrency(q.price, { compact: true })}
            </div>
            <ChangePill value={q.changePct} />
          </div>
        </li>
      ))}
    </ul>
  );
}

function QuoteGrid({ list, emptyText }: { list: MarketQuote[]; emptyText?: string }) {
  if (list.length === 0)
    return (
      <div className="py-10 text-center text-sm text-muted-foreground">
        {emptyText ?? "No results"}
      </div>
    );
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {list.map((q) => (
        <div key={q.symbol} className="glass hover-lift rounded-2xl p-4">
          <div className="flex items-start justify-between">
            <div>
              <div className="text-sm font-semibold">{q.symbol}</div>
              <div className="text-xs text-muted-foreground">{q.name}</div>
            </div>
            <button
              aria-label="Add to watchlist"
              className="rounded-md p-1 text-muted-foreground hover:bg-white/5 hover:text-warning"
            >
              <Star className="h-4 w-4" />
            </button>
          </div>
          <div className="mt-3">
            <Sparkline data={q.spark} positive={q.changePct >= 0} height={44} />
          </div>
          <div className="mt-2 flex items-end justify-between">
            <div className="text-lg font-semibold">
              {formatCurrency(q.price, { compact: true })}
            </div>
            <ChangePill value={q.changePct} />
          </div>
        </div>
      ))}
    </div>
  );
}

function SentimentGauge({ score, label }: { score: number; label: string }) {
  const color =
    score >= 70 ? "var(--color-success)" : score >= 45 ? "var(--color-warning)" : "var(--color-destructive)";
  return (
    <div className="flex flex-col items-center gap-3 pt-2">
      <div className="relative h-40 w-40">
        <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
          <circle cx="50" cy="50" r="42" stroke="rgba(255,255,255,0.08)" strokeWidth="10" fill="none" />
          <circle
            cx="50"
            cy="50"
            r="42"
            stroke={color}
            strokeWidth="10"
            fill="none"
            strokeDasharray={`${(score / 100) * 264} 264`}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 grid place-items-center">
          <div className="text-center">
            <div className="text-3xl font-semibold">{score}</div>
            <div className="text-xs uppercase tracking-wider" style={{ color }}>
              {label}
            </div>
          </div>
        </div>
      </div>
      <div className="text-center text-xs text-muted-foreground">
        Markets are showing signs of {label.toLowerCase()}. Diversify entries.
      </div>
    </div>
  );
}

function formatAbsoluteDate(iso?: string): string | null {
  if (!iso) return null;
  try {
    return new Date(iso).toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return null;
  }
}

function NewsReaderDialog({
  news,
  onOpenChange,
}: {
  news: MarketNews | null;
  onOpenChange: (open: boolean) => void;
}) {
  const open = news !== null;
  const absoluteDate = formatAbsoluteDate(news?.published_at);
  const hasUrl = !!news?.url;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="border-white/10 bg-background/95 backdrop-blur-xl sm:max-w-xl">
        {news && (
          <>
            <DialogHeader>
              <div className="flex items-center gap-2">
                {news.tag && (
                  <Badge
                    variant="secondary"
                    className="border-white/10 bg-white/5 text-[10px]"
                  >
                    {news.tag}
                  </Badge>
                )}
                <span className="text-xs text-muted-foreground">
                  {news.source}
                  {news.time ? ` · ${news.time}` : ""}
                </span>
              </div>
              <DialogTitle className="mt-2 text-xl leading-snug">
                {news.title}
              </DialogTitle>
              {absoluteDate && (
                <div className="mt-1 flex items-center gap-1.5 text-xs text-muted-foreground">
                  <Calendar className="h-3 w-3" />
                  <span>{absoluteDate}</span>
                </div>
              )}
            </DialogHeader>

            <div className="max-h-[55vh] overflow-y-auto pr-1">
              <DialogDescription className="text-sm leading-relaxed text-foreground/85">
                {news.summary ?? "No preview available for this article."}
              </DialogDescription>
            </div>

            <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onOpenChange(false)}
              >
                Close
              </Button>
              {hasUrl ? (
                <Button
                  asChild
                  size="sm"
                  className="gradient-brand text-primary-foreground"
                >
                  <a
                    href={news.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Open original article
                    <ExternalLink className="ml-1.5 h-3.5 w-3.5" />
                  </a>
                </Button>
              ) : (
                <Button size="sm" variant="outline" disabled>
                  Original link unavailable
                </Button>
              )}
            </div>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}