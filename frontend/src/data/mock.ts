// All mock data lives here. Services import from this file. Swap with API later.

export const dashboardSummary = {
  netWorth: 1470000,
  netWorthChangePct: 4.8,
  portfolioValue: 843000,
  portfolioChangePct: 2.4,
  monthlyIncome: 120000,
  monthlyExpenses: 42000,
  savingsRate: 36,
  cashFlow: 78000,
  aiInsight:
    "Your savings rate is in the top 12% of users your age. Consider allocating ₹15,000 of your surplus to a diversified index fund to accelerate your Retirement goal by ~1.4 years.",
};

export const cashFlowSeries = [
  { month: "Jan", income: 118000, expenses: 46000, savings: 72000 },
  { month: "Feb", income: 120000, expenses: 44000, savings: 76000 },
  { month: "Mar", income: 121000, expenses: 48000, savings: 73000 },
  { month: "Apr", income: 122000, expenses: 41000, savings: 81000 },
  { month: "May", income: 120000, expenses: 43000, savings: 77000 },
  { month: "Jun", income: 124000, expenses: 40000, savings: 84000 },
  { month: "Jul", income: 120000, expenses: 42000, savings: 78000 },
];

export const portfolioPerformance = [
  { date: "Jan", value: 720000, benchmark: 700000 },
  { date: "Feb", value: 735000, benchmark: 712000 },
  { date: "Mar", value: 755000, benchmark: 722000 },
  { date: "Apr", value: 780000, benchmark: 738000 },
  { date: "May", value: 795000, benchmark: 748000 },
  { date: "Jun", value: 820000, benchmark: 761000 },
  { date: "Jul", value: 843000, benchmark: 775000 },
];

export const allocation = [
  { name: "Stocks", value: 385000, color: "var(--chart-1)" },
  { name: "Mutual Funds", value: 240000, color: "var(--chart-2)" },
  { name: "Crypto", value: 78000, color: "var(--chart-3)" },
  { name: "Gold", value: 62000, color: "var(--chart-4)" },
  { name: "Fixed Deposits", value: 58000, color: "var(--chart-5)" },
  { name: "Cash", value: 20000, color: "oklch(0.75 0.05 260)" },
];

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

export const holdings: Holding[] = [
  { id: "h1", symbol: "RELIANCE", name: "Reliance Industries", type: "Stocks", quantity: 40, avgPrice: 2450, currentPrice: 2812, changePct: 1.8, value: 112480 },
  { id: "h2", symbol: "TCS", name: "Tata Consultancy Services", type: "Stocks", quantity: 22, avgPrice: 3400, currentPrice: 3985, changePct: 0.9, value: 87670 },
  { id: "h3", symbol: "INFY", name: "Infosys", type: "Stocks", quantity: 60, avgPrice: 1420, currentPrice: 1568, changePct: -0.6, value: 94080 },
  { id: "h4", symbol: "HDFCBANK", name: "HDFC Bank", type: "Stocks", quantity: 55, avgPrice: 1520, currentPrice: 1642, changePct: 1.1, value: 90310 },
  { id: "h5", symbol: "PPFAS", name: "Parag Parikh Flexi Cap", type: "Mutual Funds", quantity: 1250, avgPrice: 62, currentPrice: 78, changePct: 0.7, value: 97500 },
  { id: "h6", symbol: "AXIS-BC", name: "Axis Bluechip Fund", type: "Mutual Funds", quantity: 2100, avgPrice: 42, currentPrice: 51, changePct: 0.3, value: 107100 },
  { id: "h7", symbol: "MIRAE-ELSS", name: "Mirae ELSS Tax Saver", type: "Mutual Funds", quantity: 800, avgPrice: 32, currentPrice: 44, changePct: -0.2, value: 35200 },
  { id: "h8", symbol: "BTC", name: "Bitcoin", type: "Crypto", quantity: 0.012, avgPrice: 3800000, currentPrice: 5200000, changePct: 3.4, value: 62400 },
  { id: "h9", symbol: "ETH", name: "Ethereum", type: "Crypto", quantity: 0.08, avgPrice: 180000, currentPrice: 195000, changePct: -1.2, value: 15600 },
  { id: "h10", symbol: "GOLDBEES", name: "Gold ETF", type: "Gold", quantity: 90, avgPrice: 58, currentPrice: 69, changePct: 0.4, value: 6210 },
  { id: "h11", symbol: "SGB-24", name: "Sovereign Gold Bond 2024", type: "Gold", quantity: 8, avgPrice: 5800, currentPrice: 6975, changePct: 0.5, value: 55800 },
  { id: "h12", symbol: "HDFC-FD", name: "HDFC 5Y Fixed Deposit", type: "Fixed Deposits", quantity: 1, avgPrice: 58000, currentPrice: 58000, changePct: 0, value: 58000 },
  { id: "h13", symbol: "CASH", name: "Savings Account", type: "Cash", quantity: 1, avgPrice: 20000, currentPrice: 20000, changePct: 0, value: 20000 },
];

export type Transaction = {
  id: string;
  title: string;
  category: "Food" | "Shopping" | "Transport" | "Salary" | "Investment" | "Bills" | "Entertainment" | "Health";
  amount: number;
  type: "credit" | "debit";
  date: string;
  merchant?: string;
};

export const transactions: Transaction[] = [
  { id: "t1", title: "Salary — July", category: "Salary", amount: 120000, type: "credit", date: "2026-07-01", merchant: "Acme Corp" },
  { id: "t2", title: "SIP — Parag Parikh Flexi Cap", category: "Investment", amount: 15000, type: "debit", date: "2026-07-02", merchant: "Zerodha Coin" },
  { id: "t3", title: "Zomato dinner", category: "Food", amount: 820, type: "debit", date: "2026-07-14", merchant: "Zomato" },
  { id: "t4", title: "Amazon — Kindle case", category: "Shopping", amount: 1499, type: "debit", date: "2026-07-13", merchant: "Amazon" },
  { id: "t5", title: "Uber ride", category: "Transport", amount: 320, type: "debit", date: "2026-07-12", merchant: "Uber" },
  { id: "t6", title: "Netflix", category: "Entertainment", amount: 649, type: "debit", date: "2026-07-10", merchant: "Netflix" },
  { id: "t7", title: "Electricity bill", category: "Bills", amount: 2180, type: "debit", date: "2026-07-08", merchant: "BESCOM" },
  { id: "t8", title: "Freelance project", category: "Salary", amount: 28000, type: "credit", date: "2026-07-05", merchant: "Upwork" },
];

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

export const goals: Goal[] = [
  { id: "g1", title: "Emergency Fund",      emoji: "🛟", target: 300000,  current: 210000, deadline: "2026-12-31", monthlyContribution: 15000, category: "Emergency" },
  { id: "g2", title: "Down payment — Home", emoji: "🏡", target: 2500000, current: 780000, deadline: "2029-06-30", monthlyContribution: 35000, category: "Home" },
  { id: "g3", title: "Japan trip",          emoji: "🗾", target: 350000,  current: 128000, deadline: "2027-03-15", monthlyContribution: 12000, category: "Travel" },
  { id: "g4", title: "Retirement corpus",   emoji: "🌴", target: 30000000, current: 4200000, deadline: "2045-01-01", monthlyContribution: 25000, category: "Retirement" },
  { id: "g5", title: "MBA fund",            emoji: "🎓", target: 1800000, current: 640000, deadline: "2028-08-01", monthlyContribution: 22000, category: "Education" },
];

export const financialHealth = {
  overall: 78,
  scores: [
    { key: "credit",     label: "Credit Health",     score: 82, trend: 3.2,  hint: "Your credit utilization is 18%. Keep it under 30%." },
    { key: "emergency",  label: "Emergency Fund",    score: 70, trend: 5.1,  hint: "You have 3.5 months of expenses saved. Target 6 months." },
    { key: "debt",       label: "Debt Ratio",        score: 88, trend: -1.2, hint: "Debt-to-income is 12%. Excellent." },
    { key: "investment", label: "Investment Score",  score: 75, trend: 2.6,  hint: "Diversify — 46% of your portfolio is in Indian equities." },
    { key: "insurance",  label: "Insurance",         score: 62, trend: 0,    hint: "Consider a 1 Cr term-life plan." },
    { key: "budget",     label: "Budget Discipline", score: 84, trend: 4.4,  hint: "You've stayed under budget for 5 months in a row." },
  ],
  trend: [
    { month: "Feb", score: 68 }, { month: "Mar", score: 71 },
    { month: "Apr", score: 72 }, { month: "May", score: 74 },
    { month: "Jun", score: 76 }, { month: "Jul", score: 78 },
  ],
  recommendations: [
    { id: "r1", title: "Boost your Emergency Fund", body: "Add ₹8,000 per month to reach 6 months of expenses by Nov 2026.", severity: "medium" as const },
    { id: "r2", title: "Buy a term-life insurance policy", body: "A 1 Cr policy costs ~₹9,800/year at your age.", severity: "high" as const },
    { id: "r3", title: "Rebalance towards international equity", body: "Add a global index fund — target 15% allocation.", severity: "low" as const },
  ],
};

export type MarketQuote = {
  symbol: string;
  name: string;
  price: number;
  changePct: number;
  spark: number[];
};

export type MarketSector = { name: string; changePct: number };
export type MarketNews = {
  id: string;
  title: string;
  source: string;
  time: string;
  tag: string;
  summary?: string;
  url?: string;
  published_at?: string;
};
export type MarketData = {
  indices: MarketQuote[];
  trending: MarketQuote[];
  crypto: MarketQuote[];
  sectors: MarketSector[];
  news: MarketNews[];
  sentiment: { score: number; label: string };
};

const spark = (base: number, n = 24, vol = 0.02) =>
  Array.from({ length: n }, (_, i) => base * (1 + Math.sin(i / 3) * vol + (Math.random() - 0.5) * vol));

export const market = {
  indices: [
    { symbol: "NIFTY 50",   name: "NIFTY 50",     price: 24870.4, changePct:  0.62, spark: spark(24800) },
    { symbol: "SENSEX",     name: "BSE Sensex",   price: 81420.1, changePct:  0.48, spark: spark(81000) },
    { symbol: "BANKNIFTY",  name: "Bank Nifty",   price: 52180.9, changePct: -0.21, spark: spark(52000) },
    { symbol: "NASDAQ",     name: "NASDAQ",       price: 20450.6, changePct:  1.12, spark: spark(20300) },
  ] as MarketQuote[],
  trending: [
    { symbol: "TATAMOTORS", name: "Tata Motors",     price: 1082.4, changePct:  4.2, spark: spark(1050) },
    { symbol: "ADANIGREEN", name: "Adani Green",     price: 1734.0, changePct: -2.8, spark: spark(1780) },
    { symbol: "BAJFINANCE", name: "Bajaj Finance",   price: 7420.5, changePct:  1.9, spark: spark(7300) },
    { symbol: "LT",         name: "Larsen & Toubro", price: 3612.1, changePct:  0.8, spark: spark(3580) },
    { symbol: "ITC",        name: "ITC Ltd",         price: 468.7,  changePct: -0.4, spark: spark(470) },
    { symbol: "MARUTI",     name: "Maruti Suzuki",   price: 12480,  changePct:  2.1, spark: spark(12300) },
  ] as MarketQuote[],
  crypto: [
    { symbol: "BTC", name: "Bitcoin",  price: 5210000, changePct:  2.8, spark: spark(5100000) },
    { symbol: "ETH", name: "Ethereum", price:  198000, changePct: -1.1, spark: spark(200000) },
    { symbol: "SOL", name: "Solana",   price:   18900, changePct:  4.6, spark: spark(18000) },
    { symbol: "ADA", name: "Cardano",  price:      82, changePct:  0.9, spark: spark(80) },
  ] as MarketQuote[],
  sectors: [
    { name: "Technology", changePct:  2.1 },
    { name: "Financials", changePct:  0.8 },
    { name: "Energy",     changePct: -1.2 },
    { name: "Healthcare", changePct:  1.4 },
    { name: "Consumer",   changePct:  0.4 },
    { name: "Metals",     changePct: -0.7 },
    { name: "Auto",       changePct:  2.6 },
    { name: "Realty",     changePct:  1.1 },
  ],
  news: [
    {
      id: "n1",
      title: "RBI holds repo rate at 6.5%, signals cautious optimism",
      source: "Mint",
      time: "2h ago",
      tag: "Policy",
      summary:
        "The Reserve Bank of India's Monetary Policy Committee voted 5-1 to keep the repo rate unchanged at 6.5%, citing persistent core inflation and uneven monsoon progress. Governor emphasized a data-dependent path forward and reiterated that any future cuts will be calibrated to growth-inflation balance.",
      url: "https://www.livemint.com/news/india/rbi-mpc-decision-repo-rate-august-2026",
      published_at: new Date(Date.now() - 2 * 3600_000).toISOString(),
    },
    {
      id: "n2",
      title: "Tata Motors surges 4% on strong Q1 EV deliveries",
      source: "Bloomberg",
      time: "3h ago",
      tag: "Stocks",
      summary:
        "Tata Motors reported a 38% YoY jump in EV deliveries, with the Nexon EV and Punch EV leading volume. Management raised its full-year EV guidance and confirmed two new model launches in Q3.",
      url: "https://www.bloomberg.com/news/articles/tata-motors-q1-ev-deliveries",
      published_at: new Date(Date.now() - 3 * 3600_000).toISOString(),
    },
    {
      id: "n3",
      title: "Bitcoin breaks $62K amid ETF inflow rally",
      source: "CoinDesk",
      time: "5h ago",
      tag: "Crypto",
      summary:
        "Spot Bitcoin ETFs in the US recorded $487M of net inflows over the past five sessions, the strongest stretch since launch. Analysts attribute the rally to softer US macro prints and renewed institutional demand.",
      url: "https://www.coindesk.com/markets/bitcoin-62k-etf-inflows",
      published_at: new Date(Date.now() - 5 * 3600_000).toISOString(),
    },
    {
      id: "n4",
      title: "Nifty IT jumps 2.4% as tech earnings beat estimates",
      source: "Economic Times",
      time: "6h ago",
      tag: "Sector",
      summary:
        "TCS and Infosys posted Q1 revenue ahead of consensus, with management commentary pointing to a steady demand environment in BFSI and healthcare verticals. Deal pipelines for FY26 are tracking 14% higher YoY.",
      url: "https://economictimes.indiatimes.com/tech/it-q1-earnings-nifty-it",
      published_at: new Date(Date.now() - 6 * 3600_000).toISOString(),
    },
    {
      id: "n5",
      title: "Gold hits new all-time high on safe-haven demand",
      source: "Reuters",
      time: "8h ago",
      tag: "Commodities",
      summary:
        "Spot gold topped $2,460/oz as softer US dollar and geopolitical tensions fueled safe-haven buying. Central banks, led by India and China, continue to accumulate at multi-year highs.",
      url: "https://www.reuters.com/markets/commodities/gold-record-high",
      published_at: new Date(Date.now() - 8 * 3600_000).toISOString(),
    },
  ],
  sentiment: { score: 62, label: "Greed" },
};

export const watchlist = ["TATAMOTORS", "BAJFINANCE", "MARUTI", "BTC", "ETH"];

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

export const seedChats: ChatSession[] = [
  {
    id: "c1",
    title: "How should I invest ₹1L?",
    updatedAt: new Date().toISOString(),
    pinned: true,
    messages: [
      { id: "m1", role: "user", content: "I have ₹1,00,000 to invest. What do you recommend?", createdAt: new Date().toISOString() },
      {
        id: "m2",
        role: "assistant",
        createdAt: new Date().toISOString(),
        content:
`Great question! Based on your profile (moderate risk, 8-year horizon), here's a suggested split:

- **60% Equity Mutual Funds** — ₹60,000 across a Flexi-Cap and a Nifty 50 index fund
- **20% Debt** — ₹20,000 in a short-duration debt fund
- **10% Gold** — ₹10,000 in a Gold ETF
- **10% International equity** — ₹10,000 in a NASDAQ index fund

\`\`\`text
Expected 8y CAGR: 11–13%
Projected value: ₹2.4L – ₹2.7L
\`\`\`

Would you like me to pick specific funds?`,
      },
    ],
  },
  {
    id: "c2",
    title: "Analyze my portfolio risk",
    updatedAt: new Date(Date.now() - 86400000).toISOString(),
    messages: [],
  },
  {
    id: "c3",
    title: "Should I prepay my home loan?",
    updatedAt: new Date(Date.now() - 3 * 86400000).toISOString(),
    messages: [],
  },
];

export const suggestedPrompts = [
  "Analyze my portfolio and find risks",
  "Am I on track for retirement?",
  "How much can I safely spend this month?",
  "Compare NIFTY 50 vs S&P 500 for a 10y horizon",
];
