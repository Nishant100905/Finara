"""
Financial strategy engine.
"""

from __future__ import annotations

from .models import (
    ActionItem,
    FinancialPlan,
    PlanPriority,
    StrategyType,
)


class StrategyEngine:
    """
    Builds action items based on the selected strategy.
    """

    def generate_actions(
        self,
        plan: FinancialPlan,
    ) -> list[ActionItem]:

        strategy = plan.strategy

        if strategy == StrategyType.EMERGENCY_FUND:
            return self._emergency_fund_actions(plan)

        if strategy == StrategyType.DEBT_REDUCTION:
            return self._debt_actions(plan)

        if strategy == StrategyType.AGGRESSIVE_INVESTING:
            return self._investment_actions(plan)

        if strategy == StrategyType.WEALTH_PRESERVATION:
            return self._wealth_preservation_actions(plan)

        return self._balanced_growth_actions(plan)

    def _emergency_fund_actions(
        self,
        plan: FinancialPlan,
    ) -> list[ActionItem]:

        return [

            ActionItem(
                title="Build Emergency Fund",
                description="Save consistently until your emergency fund reaches six months of expenses.",
                priority=PlanPriority.CRITICAL,
                category="Savings",
                estimated_amount=plan.monthly_savings_target,
            ),

            ActionItem(
                title="Reduce Non-essential Spending",
                description="Identify subscriptions and discretionary expenses that can be reduced.",
                priority=PlanPriority.HIGH,
                category="Budget",
            ),

            ActionItem(
                title="Automate Savings",
                description="Create an automatic monthly transfer to your emergency fund.",
                priority=PlanPriority.HIGH,
                category="Automation",
            ),
        ]

    def _debt_actions(
        self,
        plan: FinancialPlan,
    ) -> list[ActionItem]:

        return [

            ActionItem(
                title="Pay High Interest Debt",
                description="Prioritize paying loans with the highest interest rates.",
                priority=PlanPriority.CRITICAL,
                category="Debt",
                estimated_amount=plan.debt_payment_target,
            ),

            ActionItem(
                title="Avoid New Debt",
                description="Pause unnecessary borrowing until current debt decreases.",
                priority=PlanPriority.HIGH,
                category="Debt",
            ),

            ActionItem(
                title="Create Debt Snowball",
                description="List debts and create a structured repayment plan.",
                priority=PlanPriority.MEDIUM,
                category="Debt",
            ),
        ]

    def _investment_actions(
        self,
        plan: FinancialPlan,
    ) -> list[ActionItem]:

        return [

            ActionItem(
                title="Increase Monthly Investments",
                description="Invest consistently through SIPs or diversified ETFs.",
                priority=PlanPriority.HIGH,
                category="Investment",
                estimated_amount=plan.monthly_investment_target,
            ),

            ActionItem(
                title="Portfolio Review",
                description="Review asset allocation and rebalance quarterly.",
                priority=PlanPriority.MEDIUM,
                category="Investment",
            ),

            ActionItem(
                title="Increase Equity Allocation",
                description="Increase long-term growth exposure if suitable.",
                priority=PlanPriority.LOW,
                category="Investment",
            ),
        ]

    def _balanced_growth_actions(
        self,
        plan: FinancialPlan,
    ) -> list[ActionItem]:

        return [

            ActionItem(
                title="Save Monthly",
                description="Maintain consistent monthly savings.",
                priority=PlanPriority.HIGH,
                category="Savings",
                estimated_amount=plan.monthly_savings_target,
            ),

            ActionItem(
                title="Invest Monthly",
                description="Continue investing through SIPs.",
                priority=PlanPriority.MEDIUM,
                category="Investment",
                estimated_amount=plan.monthly_investment_target,
            ),

            ActionItem(
                title="Review Budget",
                description="Track expenses every month.",
                priority=PlanPriority.LOW,
                category="Budget",
            ),
        ]

    def _wealth_preservation_actions(
        self,
        plan: FinancialPlan,
    ) -> list[ActionItem]:

        return [

            ActionItem(
                title="Protect Existing Wealth",
                description="Maintain emergency reserves and diversified investments.",
                priority=PlanPriority.HIGH,
                category="Investment",
            ),

            ActionItem(
                title="Review Insurance",
                description="Ensure adequate health and life insurance coverage.",
                priority=PlanPriority.MEDIUM,
                category="Insurance",
            ),

            ActionItem(
                title="Quarterly Portfolio Review",
                description="Review portfolio every quarter.",
                priority=PlanPriority.LOW,
                category="Investment",
            ),
        ]


strategy_engine = StrategyEngine()