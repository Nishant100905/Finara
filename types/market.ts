export interface MarketIndex {
    id: string;
    name: string;
    symbol: string;
    price: number;
    change: number;
    changePercent: number;
}

export interface Stock {
    symbol: string;
    companyName: string;
    price: number;
    change: number;
    changePercent: number;
    volume: number;
}

export interface WatchlistStock extends Stock {
    sparkline: number[];
}

export interface SectorPerformance {
    sector: string;
    changePercent: number;
}

export interface MarketNews {
    id: string;
    title: string;
    summary: string;
    source: string;
    url: string;
    publishedAt: string;
    sentiment: "Bullish" | "Bearish" | "Neutral";
}

export interface MarketInsight {
    id: string;
    title: string;
    description: string;
    confidence: number;
}

export interface FearGreedIndex {
    value: number;
    label:
    | "Extreme Fear"
    | "Fear"
    | "Neutral"
    | "Greed"
    | "Extreme Greed";
}

export interface MarketOverview {
    indices: MarketIndex[];
    gainers: Stock[];
    losers: Stock[];
    active: Stock[];
    watchlist: WatchlistStock[];
    sectors: SectorPerformance[];
    news: MarketNews[];
    insights: MarketInsight[];
    fearGreed: FearGreedIndex;
}