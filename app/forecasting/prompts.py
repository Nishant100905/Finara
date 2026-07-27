"""
Prompt templates for Financial Forecasting.
"""

SYSTEM_PROMPT = """
You are an expert Financial Forecasting AI.

Responsibilities:

- Forecast future financial position
- Explain assumptions
- Compare financial scenarios
- Estimate goal completion
- Analyze retirement readiness
- Explain investment growth

Rules:

- Never guarantee returns.
- Clearly state assumptions.
- Mention risks.
- Be realistic.
- Encourage disciplined investing.

Output format:

1. Summary
2. Forecast
3. Opportunities
4. Risks
5. Recommendations
"""


def build_forecast_prompt(
    profile: dict,
    analysis: dict,
    forecast,
    retirement,
    goals,
    scenarios,
) -> str:
    """
    Build forecasting prompt.
    """

    return f"""
User Profile

{profile}

Financial Analysis

{analysis}

Forecast

{forecast}

Retirement

{retirement}

Goals

{goals}

Scenarios

{scenarios}

Generate an easy-to-understand financial forecast.

Include:

• Future outlook
• Opportunities
• Risks
• Recommended actions
"""