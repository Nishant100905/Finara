// Service layer. Market data fetches hit the FastAPI backend
// (Yahoo Finance-backed) — no more hardcoded stock market mocks.

import {
  dashboardSummary,
  cashFlowSeries,
  portfolioPerformance,
  allocation,
  holdings,
  transactions,
  goals,
  financialHealth,
  seedChats,
  suggestedPrompts,
  watchlist,
  type Goal,
  type Holding,
  type Transaction,
  type ChatSession,
  type ChatMessage,
  type MarketData,
  type MarketQuote,
} from "@/data/mock";
import type { MarketSearchResult } from "@/lib/types";
import apiClient from "@/lib/api";
const delay = <T>(data: T, ms = 300): Promise<T> =>
  new Promise((resolve) => setTimeout(() => resolve(data), ms));

// Watchlist symbols the dashboard should surface — feeds into the
// market section of getDashboard() alongside the live indices/news.
const WATCHLIST_SYMBOLS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "TATAMOTORS.NS"];

export const api = {
  // =========================
  // Dashboard
  // =========================
  getDashboard: async () => {
    // Pull live market data in parallel with the mock-backed personal
    // finance payloads. The dashboard already has indices/news widgets;
    // those now reflect real Yahoo Finance values rather than the
    // hardcoded spark series from mock.ts.
    const market = await api.getMarket().catch(() => null);

    const watchlistQuotes: MarketQuote[] = market
      ? (market.trending ?? []).filter((q) =>
          WATCHLIST_SYMBOLS.some((sym) => q.symbol === sym || q.symbol.startsWith(sym))
        )
      : [];

    return delay({
      summary: dashboardSummary,
      cashFlow: cashFlowSeries,
      performance: portfolioPerformance,
      allocation,
      transactions: transactions.slice(0, 6),
      goals: goals.slice(0, 3),
      market: market
        ? {
            indices: market.indices,
            news: market.news.slice(0, 4),
            watchlist: watchlistQuotes,
          }
        : {
            indices: [],
            news: [],
            watchlist: [],
          },
    });
  },

  // =========================
  // Portfolio
  // =========================
  getHoldings: (): Promise<Holding[]> => delay([...holdings]),

  getAllocation: () => delay(allocation),

  getPortfolioPerformance: () => delay(portfolioPerformance),

  getTopMovers: () =>
    delay({
      gainers: [...holdings]
        .sort((a, b) => b.changePct - a.changePct)
        .slice(0, 3),
      losers: [...holdings]
        .sort((a, b) => a.changePct - b.changePct)
        .slice(0, 3),
    }),

  createHolding: async (holding: Holding): Promise<Holding> => {
    holdings.push(holding);
    return delay(holding);
  },

  updateHolding: async (
    id: string,
    updated: Partial<Holding>
  ): Promise<Holding> => {
    const index = holdings.findIndex((h) => h.id === id);

    if (index === -1) {
      throw new Error("Holding not found");
    }

    holdings[index] = {
      ...holdings[index],
      ...updated,
    };

    return delay(holdings[index]);
  },

  deleteHolding: async (id: string): Promise<boolean> => {
    const index = holdings.findIndex((h) => h.id === id);

    if (index !== -1) {
      holdings.splice(index, 1);
    }

    return delay(true);
  },

  // =========================
  // Transactions
  // =========================
  getTransactions: (): Promise<Transaction[]> =>
    delay(transactions),

  // =========================
  // Goals
  // =========================
  getGoals: (): Promise<Goal[]> =>
    delay(goals),

  // =========================
  // Financial Health
  // =========================
  getFinancialHealth: () =>
    delay(financialHealth),

  // =========================
  // Market
  // =========================
  getMarket: async (): Promise<MarketData> => {
    const res = await apiClient.get<MarketData>("/api/market/");
    return res.data;
  },

  getWatchlist: async (): Promise<MarketQuote[]> => {
    const market = await api.getMarket();
    return (market.trending ?? []).filter((q) =>
      watchlist.includes(q.symbol)
    );
  },

  searchSymbols: async (
    q: string,
    limit = 10
  ): Promise<MarketSearchResult[]> => {
    const trimmed = q.trim();
    if (!trimmed) return [];
    const res = await apiClient.get<{ query: string; results: MarketSearchResult[] }>(
      "/api/market/search",
      { params: { q: trimmed, limit } }
    );
    return res.data.results ?? [];
  },

  getQuote: async (symbol: string): Promise<MarketQuote> => {
    const res = await apiClient.get<MarketQuote>("/api/market/quote", {
      params: { symbol },
    });
    return res.data;
  },

  // =========================
  // AI Assistant
  // =========================
  getChats: (): Promise<ChatSession[]> =>
    delay(seedChats),

  getSuggestedPrompts: () =>
    delay(suggestedPrompts),

  async streamAssistantReply(
    userMessage: string,
    onToken: (chunk: string) => void,
    signal?: AbortSignal,
    documentIds?: string[]
  ): Promise<ChatMessage> {
    // The backend SSE endpoint can run for many minutes (LangGraph
    // pipeline). Use the native fetch + ReadableStream so the response
    // body is consumed incrementally without an axios timeout capping it.
    const token =
      typeof window !== "undefined"
        ? window.localStorage.getItem("access_token")
        : null;

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    };
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
    const API_BASE =
      (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_URL) ||
      "http://127.0.0.1:8000";

    const res = await fetch(`${API_BASE}/api/chat/stream`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        message: userMessage,
        thread_id: crypto.randomUUID(),
        ...(documentIds?.length ? { document_ids: documentIds } : {}),
      }),
      signal,
    });

    if (!res.ok || !res.body) {
      // Surface the failure to the caller as a synthetic assistant message
      return {
        id: crypto.randomUUID(),
        role: "assistant",
        content: `⚠️ The assistant request failed (HTTP ${res.status}). Please try again.`,
        createdAt: new Date().toISOString(),
      };
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let buffer = "";
    let accumulated = "";
    let aborted = false;

    // Parse the SSE stream as a sequence of `data: ...\n\n` events.
    // Chunks can split events across reads, so we buffer until we see
    // a blank line that delimits an event.
    try {
      while (true) {
        if (signal?.aborted) {
          aborted = true;
          try {
            await reader.cancel();
          } catch {
            /* noop */
          }
          break;
        }

        const { value, done } = await reader.read();

        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Process complete events. A blank line ends an event.
        let boundary: number;
        // eslint-disable-next-line no-cond-assign
        while ((boundary = buffer.indexOf("\n\n")) !== -1) {
          const rawEvent = buffer.slice(0, boundary);
          buffer = buffer.slice(boundary + 2);

          // An event may contain multiple `data:` lines; we only emit one
          // per line for simplicity since the backend sends one per event.
          const lines = rawEvent.split("\n");
          for (const line of lines) {
            if (!line.startsWith("data:")) continue;
            const payload = line.slice(5).trim();
            if (!payload) continue;
            if (payload === "[DONE]") {
              // Stream complete.
              return {
                id: crypto.randomUUID(),
                role: "assistant",
                content: accumulated,
                createdAt: new Date().toISOString(),
              };
            }

            // Try to parse as JSON. The metadata event is a JSON object
            // with `source`/`cache_hit`; token events are JSON strings.
            try {
              const parsed = JSON.parse(payload);
              if (
                parsed &&
                typeof parsed === "object" &&
                "error" in parsed
              ) {
                throw new Error(String(parsed.error));
              }
              if (
                parsed &&
                typeof parsed === "object" &&
                ("source" in parsed || "cache_hit" in parsed)
              ) {
                // Metadata event — skip from stream content but continue.
                continue;
              }
              const text =
                typeof parsed === "string"
                  ? parsed
                  : typeof parsed?.text === "string"
                    ? parsed.text
                    : null;
              if (text === null) continue;
              accumulated += text;
              onToken(text);
            } catch (err) {
              if (err instanceof SyntaxError) {
                // Plain text payload — treat the raw value as a token.
                accumulated += payload;
                onToken(payload);
              } else {
                throw err;
              }
            }
          }
        }
      }
    } catch (err) {
      if ((err as { name?: string })?.name === "AbortError") {
        aborted = true;
      } else {
        throw err;
      }
    }

    if (aborted) {
      return {
        id: crypto.randomUUID(),
        role: "assistant",
        content: accumulated || "⏹️ Generation stopped.",
        createdAt: new Date().toISOString(),
      };
    }

    if (!accumulated) {
      return {
        id: crypto.randomUUID(),
        role: "assistant",
        content: "⚠️ The assistant returned an empty response. Please try again.",
        createdAt: new Date().toISOString(),
      };
    }

    return {
      id: crypto.randomUUID(),
      role: "assistant",
      content: accumulated,
      createdAt: new Date().toISOString(),
    };
  },
};

function generateMockReply(q: string): string {
  const lower = q.toLowerCase();

  if (lower.includes("retirement")) {
    return `Based on your current savings of **₹42L** and monthly contribution of **₹25,000**, you are **on track** to reach your ₹3 Cr retirement corpus by 2045 assuming 11% CAGR.

**Sensitivity**
- +₹5,000/mo → retire 1.6 years earlier
- -1% return → shortfall of ~₹38L

Want me to model a few scenarios?`;
  }

  if (lower.includes("portfolio") || lower.includes("risk")) {
    return `Your portfolio has a **moderate-high** risk profile:

- **Equity concentration:** 74% (target: 65%)
- **Single-stock max:** RELIANCE at 13.3%
- **International exposure:** 0% — consider a global index fund
- **Volatility (12m):** 14.2% vs 11.8% benchmark

Suggested action: trim RELIANCE by 3%, allocate to a NASDAQ 100 index fund.`;
  }

  return `Here's what I found:

- Your **savings rate** is 36%, top 12% for your age
- **Cash flow** is positive at ₹78,000/month
- **Emergency fund** covers 3.5 months (target: 6)

\`\`\`text
Suggested next step: increase Emergency Fund SIP by ₹8,000/mo.
\`\`\`

Ask me anything else about your money.`;
}
