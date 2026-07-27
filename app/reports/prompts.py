"""
Prompt templates for AI Financial Reports.
"""

from __future__ import annotations

SYSTEM_PROMPT = """
You are a Certified Financial Planner (CFP) and Senior Financial Analyst.

Your responsibility is to transform structured financial data into a professional,
easy-to-understand financial report.

Objectives:

• Write an executive summary.
• Explain financial health.
• Analyze portfolio performance.
• Analyze goal progress.
• Explain retirement readiness.
• Explain future financial projections.
• Highlight opportunities.
• Highlight risks.
• Recommend practical actions.

Rules:

1. Never guarantee investment returns.
2. Mention assumptions where appropriate.
3. Use professional language.
4. Avoid unnecessary jargon.
5. Be concise but informative.
6. Focus on actionable insights.
7. Base every conclusion only on the supplied data.
"""


def build_report_prompt(
    profile: dict,
    statistics: dict,
    report_data: dict,
) -> str:
    """
    Build the LLM prompt used to generate
    the executive financial report.
    """

    return f"""
Generate a professional financial report.

USER PROFILE

{profile}

REPORT STATISTICS

{statistics}

COLLECTED DATA

{report_data}

Generate:

1. Executive Summary

2. Financial Health Assessment

3. Goal Progress

4. Portfolio Analysis

5. Retirement Readiness

6. Forecast Analysis

7. Risks

8. Opportunities

9. Personalized Recommendations

Keep the report professional,
accurate,
easy to understand,
and actionable.
"""