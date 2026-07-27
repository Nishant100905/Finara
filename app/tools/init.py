"""
Financial tools package.
"""

from .budget import (
    analyze_budget,
    fifty_thirty_twenty_rule,
)

from .calculator import (
    compound_interest,
    future_value,
    percentage,
    profit_loss,
    simple_interest,
)

from .currency import (
    convert_currency,
    supported_currencies,
)

from .emi import (
    calculate_emi,
    loan_affordability,
)

from .expense import (
    analyze_expenses,
    detect_overspending,
)

from .mutual_funds import (
    evaluate_mutual_fund,
    lump_sum_projection,
)

from .portfolio import (
    analyze_portfolio,
    rebalance_suggestion,
)

from .savings import (
    savings_goal,
    time_to_goal,
)

from .sip import (
    required_sip,
    sip_maturity,
)

from .stocks import (
    evaluate_stock,
    expected_return,
)

from .tax import (
    compare_tax_regimes,
    income_tax_new_regime,
    income_tax_old_regime,
)

__all__ = [
    "percentage",
    "compound_interest",
    "simple_interest",
    "future_value",
    "profit_loss",
    "analyze_budget",
    "fifty_thirty_twenty_rule",
    "savings_goal",
    "time_to_goal",
    "sip_maturity",
    "required_sip",
    "calculate_emi",
    "loan_affordability",
    "analyze_expenses",
    "detect_overspending",
    "analyze_portfolio",
    "rebalance_suggestion",
    "evaluate_stock",
    "expected_return",
    "evaluate_mutual_fund",
    "lump_sum_projection",
    "income_tax_old_regime",
    "income_tax_new_regime",
    "compare_tax_regimes",
    "convert_currency",
    "supported_currencies",
]