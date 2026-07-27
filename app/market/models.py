"""
Pydantic models for market data.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AssetType(str, Enum):
    STOCK = "STOCK"
    ETF = "ETF"
    INDEX = "INDEX"
    MUTUAL_FUND = "MUTUAL_FUND"
    CRYPTO = "CRYPTO"


class StockInfo(BaseModel):
    """
    Live stock information.
    """

    symbol: str

    company_name: Optional[str] = None

    asset_type: AssetType = AssetType.STOCK

    exchange: Optional[str] = None

    sector: Optional[str] = None

    industry: Optional[str] = None

    currency: str = "INR"

    current_price: Optional[float] = None

    previous_close: Optional[float] = None

    open_price: Optional[float] = None

    day_high: Optional[float] = None

    day_low: Optional[float] = None

    fifty_two_week_high: Optional[float] = None

    fifty_two_week_low: Optional[float] = None

    volume: Optional[float] = None

    average_volume: Optional[float] = None

    market_cap: Optional[float] = None

    enterprise_value: Optional[float] = None

    pe_ratio: Optional[float] = None

    forward_pe: Optional[float] = None

    peg_ratio: Optional[float] = None

    price_to_book: Optional[float] = None

    eps: Optional[float] = None

    dividend_yield: Optional[float] = None

    beta: Optional[float] = None

    roe: Optional[float] = None

    profit_margin: Optional[float] = None

    revenue_growth: Optional[float] = None

    debt_to_equity: Optional[float] = None

    website: Optional[str] = None

    summary: Optional[str] = None

    last_updated: datetime = Field(default_factory=datetime.utcnow)


class HistoricalPrice(BaseModel):
    """
    Historical candle.
    """

    date: datetime

    open: float

    high: float

    low: float

    close: float

    volume: float


class MarketNews(BaseModel):
    """
    News article.
    """

    title: str

    publisher: Optional[str] = None

    url: Optional[str] = None

    published_at: Optional[datetime] = None

    summary: Optional[str] = None


class MarketAnalysis(BaseModel):
    """
    AI analysis of a stock.
    """

    stock: StockInfo

    recommendation: str

    risk_level: str

    trend: str

    confidence: float

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)


class PortfolioHolding(BaseModel):
    """
    Portfolio holding.
    """

    symbol: str

    quantity: float

    average_buy_price: float

    current_price: float

    market_value: float

    gain_loss: float

    gain_loss_percent: float


class PortfolioAnalysis(BaseModel):
    """
    Portfolio analysis.
    """

    holdings: list[PortfolioHolding] = Field(default_factory=list)

    total_value: float

    total_gain_loss: float

    total_gain_loss_percent: float

    diversification_score: float

    risk_score: float


class QuoteResponse(BaseModel):
    """
    Standard quote response.
    """

    data: StockInfo

    source: str

    cached: bool = False


class SearchResponse(BaseModel):
    """
    Result of a free-text ticker / company search.
    """

    query: str

    results: list[dict] = Field(default_factory=list)