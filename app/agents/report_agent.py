"""
Financial Report Agent.

Responsible for generating financial reports
using the Report Generator module.
"""

from __future__ import annotations

import logging

from app.reports.models import ReportType
from app.reports.service import report_service

from .state import FinancialState

logger = logging.getLogger(__name__)


class ReportAgent:
    """
    Report Generation Agent.

    Responsibilities
    ----------------
    - Generate financial reports
    - Generate markdown reports
    - Export PDF
    - Export Excel
    - Store report metadata
    """

    def run(
        self,
        state: FinancialState,
    ) -> FinancialState:

        logger.info(
            "Report Agent started."
        )

        profile = state.get(
            "profile",
            {},
        )

        health = state.get(
            "financial_health",
            {},
        )

        goals = state.get(
            "goals",
            [],
        )

        planner = state.get(
            "planner",
            {},
        )

        recommendations = state.get(
            "recommendations",
            [],
        )

        forecast = state.get(
            "forecast",
            {},
        )

        coach = state.get(
            "coach",
            {},
        )

        market = state.get(
            "market",
            {},
        )

        portfolio = state.get(
            "portfolio",
            {},
        )

        metadata = state.setdefault(
            "metadata",
            {},
        )

        try:

            response = report_service.generate(

                profile=profile,

                health=health,

                goals=goals,

                planner=planner,

                recommendations=recommendations,

                forecast=forecast,

                coach=coach,

                market=market,

                portfolio=portfolio,

                report_type=ReportType.COMPLETE,

                export_pdf=False,

                export_excel=False,

            )

            if hasattr(
                response,
                "model_dump",
            ):

                report_data = response.model_dump()

            else:

                report_data = response

            state["report"] = report_data

            markdown = report_data.get(
                "markdown",
                "",
            )

            if markdown:

                state["response"] = markdown

            metadata[
                "report_status"
            ] = "completed"

            metadata[
                "report_type"
            ] = ReportType.COMPLETE.value

            logger.info(
                "Report Agent completed."
            )

        except Exception as exc:

            logger.exception(
                "Report Agent failed."
            )

            metadata[
                "report_status"
            ] = "failed"

            metadata[
                "error"
            ] = str(exc)

            state["report"] = {

                "error": str(exc)

            }

        return state


report_agent = ReportAgent()


def report_node(
    state: FinancialState,
) -> FinancialState:
    """
    LangGraph node.
    """

    return report_agent.run(
        state,
    )