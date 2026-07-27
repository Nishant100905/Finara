"use client";

import { useState } from "react";

import {
    useMarket,
    useRefreshMarket,
} from "@/hooks/useMarket";

import MarketHeader from "./MarketHeader";
import MarketOverview from "./MarketOverview";
import MarketIndices from "./MarketIndices";
import FearGreedCard from "./FearGreedCard";
import TrendingStocks from "./TrendingStocks";
import TopMovers from "./TopMovers";
import Watchlist from "./Watchlist";
import SectorPerformance from "./SectorPerformance";
import MarketNews from "./MarketNews";
import MarketInsights from "./MarketInsights";
import StockSearch from "./StockSearch";

export default function MarketClient() {
    const [search, setSearch] =
        useState("");

    const { data } = useMarket();

    const refresh =
        useRefreshMarket();

    if (!data) return null;

    return (
        <div className="space-y-8">

            <MarketHeader
                refreshing={
                    refresh.isPending
                }
                onRefresh={() =>
                    refresh.mutate()
                }
            />

            <StockSearch
                value={search}
                onChange={setSearch}
            />

            <MarketOverview
                indices={data.indices}
            />

            <div className="grid gap-6 xl:grid-cols-2">

                <MarketIndices
                    indices={data.indices}
                />

                <FearGreedCard
                    data={data.fearGreed}
                />

            </div>

            <div className="grid gap-6 xl:grid-cols-2">

                <TrendingStocks
                    stocks={data.active}
                />

                <TopMovers
                    gainers={data.gainers}
                    losers={data.losers}
                />

            </div>

            <div className="grid gap-6 xl:grid-cols-2">

                <Watchlist
                    stocks={data.watchlist}
                />

                <SectorPerformance
                    sectors={data.sectors}
                />

            </div>

            <div className="grid gap-6 xl:grid-cols-2">

                <MarketNews
                    news={data.news}
                />

                <MarketInsights
                    insights={data.insights}
                />

            </div>

        </div>
    );
}

