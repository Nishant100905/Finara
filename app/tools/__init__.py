"""
Financial tools package.
"""

# Calculator
from .calculator import (
    percentage,
    compound_interest,
    simple_interest,
    profit_loss,
    future_value,
)

# Budget
from .budget import (
    analyze_budget,
    fifty_thirty_twenty_rule,
)

# Savings
from .savings import (
    savings_goal,
    time_to_goal,
)

# SIP
from .sip import (
    sip_maturity,
    required_sip,
)

# EMI
from .emi import (
    calculate_emi,
    loan_affordability,
)

# Expense Analysis
from .expense import (
    analyze_expenses,
    detect_overspending,
)

# Portfolio
from .portfolio import (
    analyze_portfolio,
    rebalance_portfolio,
    portfolio_summary,
)

# Stocks
from .stocks import (
    analyze_stock,
    compare_stocks,
    stock_price,
    search_stock,
    suggest_stocks,
)

# Mutual Funds
from .mutual_funds import (
    evaluate_mutual_fund,
    lump_sum_projection,
)

# Tax
from .tax import (
    income_tax_old_regime,
    income_tax_new_regime,
    compare_tax_regimes,
)

# Currency
from .currency import (
    convert_currency,
    supported_currencies,
)

__all__ = [
    # Calculator
    "percentage",
    "compound_interest",
    "simple_interest",
    "profit_loss",
    "future_value",

    # Budget
    "analyze_budget",
    "fifty_thirty_twenty_rule",

    # Savings
    "savings_goal",
    "time_to_goal",

    # SIP
    "sip_maturity",
    "required_sip",

    # EMI
    "calculate_emi",
    "loan_affordability",

    # Expense
    "analyze_expenses",
    "detect_overspending",

    # Portfolio
    "analyze_portfolio",
    "rebalance_portfolio",
    "portfolio_summary",

    # Stocks
    "analyze_stock",
    "compare_stocks",
    "stock_price",
    "search_stock",
    "suggest_stocks",

    # Mutual Funds
    "evaluate_mutual_fund",
    "lump_sum_projection",

    # Tax
    "income_tax_old_regime",
    "income_tax_new_regime",
    "compare_tax_regimes",

    # Currency
    "convert_currency",
    "supported_currencies",
]