"""
Portfolio analysis engine.
"""

from __future__ import annotations

from collections import defaultdict

from .models import (
    PortfolioAnalysis,
    PortfolioHolding,
)


class PortfolioAnalyzer:
    """
    Portfolio analysis engine.
    """

    def analyze(
        self,
        holdings: list[dict],
    ) -> PortfolioAnalysis:
        """
        Analyze a portfolio.
        """

        portfolio: list[PortfolioHolding] = []

        total_value = 0.0
        total_cost = 0.0

        sector_weights: dict[str, float] = defaultdict(float)

        for item in holdings:

            quantity = float(item.get("quantity", 0))

            average_buy_price = float(
                item.get("average_buy_price", 0)
            )

            current_price = float(
                item.get("current_price", 0)
            )

            sector = item.get(
                "sector",
                "Unknown",
            )

            market_value = quantity * current_price

            invested = quantity * average_buy_price

            gain_loss = market_value - invested

            gain_loss_percent = (
                (gain_loss / invested) * 100
                if invested > 0
                else 0
            )

            portfolio.append(
                PortfolioHolding(
                    symbol=item["symbol"],
                    quantity=quantity,
                    average_buy_price=average_buy_price,
                    current_price=current_price,
                    market_value=market_value,
                    gain_loss=gain_loss,
                    gain_loss_percent=round(
                        gain_loss_percent,
                        2,
                    ),
                )
            )

            total_value += market_value

            total_cost += invested

            sector_weights[sector] += market_value

        total_gain = total_value - total_cost

        total_gain_percent = (
            (total_gain / total_cost) * 100
            if total_cost > 0
            else 0
        )

        diversification = self.diversification_score(
            sector_weights,
            total_value,
        )

        risk = self.risk_score(
            diversification,
        )

        return PortfolioAnalysis(

            holdings=portfolio,

            total_value=round(
                total_value,
                2,
            ),

            total_gain_loss=round(
                total_gain,
                2,
            ),

            total_gain_loss_percent=round(
                total_gain_percent,
                2,
            ),

            diversification_score=diversification,

            risk_score=risk,
        )

    def diversification_score(
        self,
        sectors: dict[str, float],
        total_value: float,
    ) -> float:
        """
        Calculate diversification score.
        """

        if total_value == 0:
            return 0

        largest = max(sectors.values())

        concentration = largest / total_value

        score = 100 - concentration * 100

        return round(score, 2)

    def risk_score(
        self,
        diversification_score: float,
    ) -> float:
        """
        Estimate portfolio risk.
        """

        return round(
            100 - diversification_score,
            2,
        )

    def rebalance(
        self,
        holdings: list[dict],
        max_allocation: float = 30,
    ) -> list[str]:
        """
        Suggest portfolio rebalancing.
        """

        total = sum(
            h["quantity"] * h["current_price"]
            for h in holdings
        )

        suggestions = []

        if total == 0:
            return suggestions

        for holding in holdings:

            allocation = (
                holding["quantity"]
                * holding["current_price"]
            ) / total * 100

            if allocation > max_allocation:

                suggestions.append(
                    f"Reduce {holding['symbol']} "
                    f"({allocation:.1f}% allocation)"
                )

        if not suggestions:

            suggestions.append(
                "Portfolio allocation looks balanced."
            )

        return suggestions

    def summary(
        self,
        holdings: list[dict],
    ) -> str:
        """
        Human-readable portfolio summary.
        """

        report = self.analyze(
            holdings,
        )

        return (
            f"Portfolio Value: ₹{report.total_value:,.2f}\n"
            f"Gain/Loss: ₹{report.total_gain_loss:,.2f} "
            f"({report.total_gain_loss_percent:.2f}%)\n"
            f"Diversification Score: "
            f"{report.diversification_score:.1f}/100\n"
            f"Risk Score: "
            f"{report.risk_score:.1f}/100\n"
            f"Holdings: {len(report.holdings)}"
        )

# Singleton instance
portfolio_analyzer = PortfolioAnalyzer()