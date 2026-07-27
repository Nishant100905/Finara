"""
Business rules for generating financial insights.

No AI is used here.
Only deterministic financial analysis.
"""

from __future__ import annotations

from typing import List

from .models import (
    FinancialProfile,
    Insight,
    InsightCategory,
    Severity,
)


def savings_rate(profile: FinancialProfile) -> List[Insight]:

    insights = []

    if profile.monthly_income <= 0:
        return insights

    rate = (
        profile.monthly_savings
        / profile.monthly_income
    ) * 100

    if rate < 20:

        insights.append(
            Insight(
                title="Low Savings Rate",
                description=f"You currently save {rate:.1f}% of your monthly income.",
                recommendation="Aim to save at least 20% of your monthly income.",
                category=InsightCategory.SAVINGS,
                severity=Severity.HIGH,
                score=90,
            )
        )

    return insights


def emergency_fund(profile: FinancialProfile) -> List[Insight]:

    insights = []

    if profile.monthly_expenses <= 0:
        return insights

    months = (
        profile.emergency_fund
        / profile.monthly_expenses
    )

    if months < 3:

        insights.append(
            Insight(
                title="Emergency Fund Too Small",
                description=f"You have only {months:.1f} months of emergency savings.",
                recommendation="Build an emergency fund covering at least 6 months of expenses.",
                category=InsightCategory.SAVINGS,
                severity=Severity.CRITICAL,
                score=100,
            )
        )

    return insights


def debt_ratio(profile: FinancialProfile) -> List[Insight]:

    insights = []

    if profile.monthly_income <= 0:
        return insights

    ratio = (
        profile.monthly_emi
        / profile.monthly_income
    ) * 100

    if ratio > 40:

        insights.append(
            Insight(
                title="High Debt Burden",
                description=f"Your EMI consumes {ratio:.1f}% of your income.",
                recommendation="Try reducing debt or increasing income.",
                category=InsightCategory.DEBT,
                severity=Severity.HIGH,
                score=95,
            )
        )

    return insights


def cash_flow(profile: FinancialProfile) -> List[Insight]:

    insights = []

    if profile.monthly_income < profile.monthly_expenses:

        insights.append(
            Insight(
                title="Negative Cash Flow",
                description="Your monthly expenses exceed your income.",
                recommendation="Reduce discretionary expenses immediately.",
                category=InsightCategory.CASHFLOW,
                severity=Severity.CRITICAL,
                score=100,
            )
        )

    return insights


def investment_ratio(profile: FinancialProfile) -> List[Insight]:

    insights = []

    if profile.monthly_income <= 0:
        return insights

    if (
        profile.investment_value == 0
        and profile.monthly_savings > 0
    ):

        insights.append(
            Insight(
                title="No Investments Found",
                description="You are saving money but not investing it.",
                recommendation="Consider SIPs, mutual funds, or index funds for long-term growth.",
                category=InsightCategory.INVESTMENT,
                severity=Severity.MEDIUM,
                score=70,
            )
        )

    return insights


RULES = [
    savings_rate,
    emergency_fund,
    debt_ratio,
    cash_flow,
    investment_ratio,
]