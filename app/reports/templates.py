"""
Reusable report templates.
"""

from __future__ import annotations

from .models import ReportSection


class ReportTemplates:
    """
    Common report section templates.
    """

    @staticmethod
    def profile(profile: dict) -> ReportSection:

        content = f"""
Name: {profile.get("name", "N/A")}
Age: {profile.get("age", "N/A")}

Monthly Income: ₹{profile.get("monthly_income", 0):,.2f}
Monthly Expenses: ₹{profile.get("monthly_expenses", 0):,.2f}

Risk Profile: {profile.get("risk_profile", "Unknown")}
"""

        return ReportSection(
            title="Financial Profile",
            content=content.strip(),
            order=1,
        )

    @staticmethod
    def financial_health(health: dict) -> ReportSection:

        content = f"""
Health Score : {health.get("score", "N/A")}

Status : {health.get("status", "Unknown")}

Summary :

{health.get("summary", "No summary available.")}
"""

        return ReportSection(
            title="Financial Health",
            content=content.strip(),
            order=2,
        )

    @staticmethod
    def goals(goals: list[dict]) -> ReportSection:

        if not goals:
            body = "No financial goals available."

        else:

            lines = []

            for goal in goals:

                lines.append(
                    f"- {goal.get('name','Goal')} "
                    f"(₹{goal.get('current_amount',0):,.0f}"
                    f" / ₹{goal.get('target_amount',0):,.0f})"
                )

            body = "\n".join(lines)

        return ReportSection(
            title="Financial Goals",
            content=body,
            order=3,
        )

    @staticmethod
    def portfolio(portfolio: dict) -> ReportSection:

        value = portfolio.get(
            "total_value",
            0,
        )

        invested = portfolio.get(
            "invested_amount",
            0,
        )

        returns = value - invested

        body = f"""
Portfolio Value : ₹{value:,.2f}

Invested Amount : ₹{invested:,.2f}

Profit/Loss : ₹{returns:,.2f}
"""

        return ReportSection(
            title="Investment Portfolio",
            content=body.strip(),
            order=4,
        )

    @staticmethod
    def recommendations(items: list[str]) -> ReportSection:

        if not items:

            body = "No recommendations."

        else:

            body = "\n".join(
                f"• {item}"
                for item in items
            )

        return ReportSection(
            title="Recommendations",
            content=body,
            order=5,
        )


report_templates = ReportTemplates()