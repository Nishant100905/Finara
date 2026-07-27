"""
Market analysis service.
"""

from __future__ import annotations

from statistics import mean

from .models import (
    HistoricalPrice,
    MarketAnalysis,
    StockInfo,
)


class MarketAnalyzer:
    """
    Market intelligence engine.
    """

    @staticmethod
    def moving_average(
        prices: list[HistoricalPrice],
        days: int = 20,
    ) -> float:

        closes = [p.close for p in prices[-days:]]

        if not closes:
            return 0.0

        return round(mean(closes), 2)

    @staticmethod
    def trend(
        prices: list[HistoricalPrice],
    ) -> str:

        if len(prices) < 30:
            return "Insufficient Data"

        short = mean(
            p.close for p in prices[-10:]
        )

        long = mean(
            p.close for p in prices[-30:]
        )

        if short > long:
            return "Bullish"

        if short < long:
            return "Bearish"

        return "Sideways"

    @staticmethod
    def volatility(
        prices: list[HistoricalPrice],
    ) -> float:

        if len(prices) < 2:
            return 0.0

        returns = []

        for previous, current in zip(
            prices,
            prices[1:],
        ):

            if previous.close == 0:
                continue

            returns.append(
                abs(
                    (
                        current.close
                        - previous.close
                    )
                    / previous.close
                )
            )

        if not returns:
            return 0.0

        return round(
            mean(returns) * 100,
            2,
        )

    @staticmethod
    def valuation(
        stock: StockInfo,
    ) -> str:

        pe = stock.pe_ratio

        if pe is None:
            return "Unknown"

        if pe < 15:
            return "Undervalued"

        if pe < 30:
            return "Fairly Valued"

        return "Overvalued"

    @staticmethod
    def risk(
        stock: StockInfo,
    ) -> str:

        beta = stock.beta

        if beta is None:
            return "Unknown"

        if beta < 0.8:
            return "Low"

        if beta <= 1.2:
            return "Moderate"

        return "High"

    @classmethod
    def analyze(
        cls,
        stock: StockInfo,
        prices: list[HistoricalPrice],
    ) -> MarketAnalysis:

        trend = cls.trend(prices)

        valuation = cls.valuation(stock)

        risk = cls.risk(stock)

        strengths: list[str] = []

        weaknesses: list[str] = []

        if trend == "Bullish":
            strengths.append(
                "Positive price trend"
            )
        elif trend == "Bearish":
            weaknesses.append(
                "Negative price trend"
            )

        if valuation == "Undervalued":
            strengths.append(
                "Potentially undervalued"
            )

        if valuation == "Overvalued":
            weaknesses.append(
                "High valuation"
            )

        if risk == "Low":
            recommendation = "BUY"
            confidence = 0.90

        elif risk == "Moderate":
            recommendation = "HOLD"
            confidence = 0.75

        else:
            recommendation = "CAUTION"
            confidence = 0.60

        return MarketAnalysis(

            stock=stock,

            recommendation=recommendation,

            risk_level=risk,

            trend=trend,

            confidence=confidence,

            strengths=strengths,

            weaknesses=weaknesses,
        )

    @classmethod
    def generate_summary(
        cls,
        stock: StockInfo,
        prices: list[HistoricalPrice],
    ) -> str:
        analysis = cls.analyze(stock, prices)
        price_str = f"{stock.current_price} {stock.currency}" if stock.current_price is not None else "N/A"
        return (
            f"{stock.company_name or stock.symbol} ({stock.symbol}) is currently trading at {price_str} "
            f"with a {analysis.trend.lower()} trend and {analysis.risk_level.lower()} risk level. "
            f"Valuation: {analysis.valuation.lower()}. Recommendation: {analysis.recommendation}."
        )