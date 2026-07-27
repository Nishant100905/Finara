// ==========================================================
// Shared TypeScript types for the Finara frontend.
// Extracted from mock data — used by all route pages and services.
// ==========================================================

// ========================
// Auth
// ========================

export type User = {
  id: string;
  email: string;
  name: string;
  avatarUrl?: string;
  createdAt?: string;
};

// ========================
// Portfolio
// ========================

export type Holding = {
  id: string;
  symbol: string;
  name: string;
  type: "Stocks" | "Crypto" | "Mutual Funds" | "Gold" | "Fixed Deposits" | "Cash";
  quantity: number;
  avgPrice: number;
  currentPrice: number;
  changePct: number;
  value: number;
};

export type AllocationItem = {
  name: string;
  value: number;
  color: string;
};

export type PerformancePoint = {
  date: string;
  value: number;
  benchmark?: number;
};

// ========================
// Transactions
// ========================

export type Transaction = {
  id: string;
  title: string;
  category: "Food" | "Shopping" | "Transport" | "Salary" | "Investment" | "Bills" | "Entertainment" | "Health";
  amount: number;
  type: "credit" | "debit";
  date: string;
  merchant?: string;
};

// ========================
// Goals
// ========================

export type Goal = {
  id: string;
  title: string;
  emoji: string;
  target: number;
  current: number;
  deadline: string;
  monthlyContribution: number;
  category: "Retirement" | "Home" | "Travel" | "Education" | "Emergency" | "Vehicle";
};

// ========================
// Financial Health
// ========================

export type HealthScore = {
  key: string;
  label: string;
  score: number;
  trend: number;
  hint: string;
};

export type HealthRecommendation = {
  id: string;
  title: string;
  body: string;
  severity: "low" | "medium" | "high";
};

export type FinancialHealth = {
  overall: number;
  scores: HealthScore[];
  trend: { month: string; score: number }[];
  recommendations: HealthRecommendation[];
};

// ========================
// Market
// ========================

export type MarketQuote = {
  symbol: string;
  name: string;
  price: number;
  changePct: number;
  spark: number[];
};

export type MarketSector = {
  name: string;
  changePct: number;
};

export type MarketNews = {
  id: string;
  title: string;
  source: string;
  time: string;
  tag: string;
};

export type MarketData = {
  indices: MarketQuote[];
  trending: MarketQuote[];
  crypto: MarketQuote[];
  sectors: MarketSector[];
  news: MarketNews[];
  sentiment: { score: number; label: string };
};

// Result returned by /api/market/search. Unlike a MarketQuote, these
// rows haven't had prices fetched — the UI calls them out as
// "lookup results" before fetching the user's pick.
export type MarketSearchResult = {
  symbol: string;
  name: string;
  exchange?: string;
  type?: string;
  score?: number;
};

// ========================
// Dashboard
// ========================

export type DashboardSummary = {
  netWorth: number;
  netWorthChangePct: number;
  portfolioValue: number;
  portfolioChangePct: number;
  monthlyIncome: number;
  monthlyExpenses: number;
  savingsRate: number;
  cashFlow: number;
  aiInsight: string;
};

export type CashFlowPoint = {
  month: string;
  income: number;
  expenses: number;
  savings: number;
};

export type DashboardData = {
  summary: DashboardSummary;
  cashFlow: CashFlowPoint[];
  performance: PerformancePoint[];
  allocation: AllocationItem[];
  transactions: Transaction[];
  goals: Goal[];
  market: {
    indices: MarketQuote[];
    news: MarketNews[];
    watchlist: MarketQuote[];
  };
};

// ========================
// Chat / AI Assistant
// ========================

export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
};

export type ChatSession = {
  id: string;
  title: string;
  updatedAt: string;
  pinned?: boolean;
  messages: ChatMessage[];
};
