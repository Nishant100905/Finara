"""
Financial Report Service.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

from .analyzer import report_analyzer
from .excel import excel_generator
from .markdown import markdown_generator
from .models import (
    ExecutiveSummary,
    FinancialReport,
    ReportMetadata,
    ReportResponse,
    ReportType,
)
from .pdf import pdf_generator
from .prompts import build_report_prompt
from .templates import report_templates


class ReportService:
    """
    Main report generation service.
    """

    def generate(
        self,
        profile: dict[str, Any],
        health: dict | None = None,
        goals: list | None = None,
        planner: dict | None = None,
        recommendations: list | None = None,
        forecast: dict | None = None,
        coach: dict | None = None,
        market: dict | None = None,
        portfolio: dict | None = None,
        report_type: ReportType = ReportType.COMPLETE,
        export_pdf: bool = False,
        export_excel: bool = False,
        output_dir: str = "reports",
    ) -> ReportResponse:

        report_data = report_analyzer.analyze(
            profile=profile,
            health=health,
            goals=goals,
            planner=planner,
            recommendations=recommendations,
            forecast=forecast,
            coach=coach,
            market=market,
            portfolio=portfolio,
        )

        statistics = report_analyzer.build_statistics(
            report_data,
        )

        summary_data = report_analyzer.executive_summary(
            report_data,
        )

        sections = self._build_sections(
            report_data,
        )

        report = FinancialReport(

            title="Financial Advisor Report",

            generated_for=profile.get(
                "name",
                "User",
            ),

            report_date=date.today(),

            metadata=ReportMetadata(

                generated_at=datetime.utcnow(),

                report_type=report_type,

            ),

            executive_summary=ExecutiveSummary(
                **summary_data,
            ),

            sections=sections,

            raw_data=report_data,

        )

        markdown = markdown_generator.generate(
            report,
        )

        pdf_path = None

        excel_path = None

        output = Path(output_dir)

        output.mkdir(
            parents=True,
            exist_ok=True,
        )

        if export_pdf:

            pdf_path = pdf_generator.generate(

                report,

                str(
                    output
                    / "financial_report.pdf"
                ),

            )

        if export_excel:

            excel_path = excel_generator.generate(

                report,

                str(
                    output
                    / "financial_report.xlsx"
                ),

            )

        return ReportResponse(

            report=report,

            markdown=markdown,

            pdf_path=pdf_path,

            excel_path=excel_path,

        )

    def build_prompt(
        self,
        profile: dict,
        report_data: dict,
    ) -> str:
        """
        Build LLM prompt.
        """

        statistics = report_analyzer.build_statistics(
            report_data,
        )

        return build_report_prompt(

            profile,

            statistics,

            report_data,

        )

    def _build_sections(
        self,
        report_data: dict,
    ):
        """
        Build report sections.
        """

        sections = []

        sections.append(

            report_templates.profile(

                report_data.get(
                    "profile",
                    {},
                )

            )

        )

        sections.append(

            report_templates.financial_health(

                report_data.get(
                    "health",
                    {},
                )

            )

        )

        sections.append(

            report_templates.goals(

                report_data.get(
                    "goals",
                    [],
                )

            )

        )

        sections.append(

            report_templates.portfolio(

                report_data.get(
                    "portfolio",
                    {},
                )

            )

        )

        recommendations = report_data.get(
            "recommendations",
            [],
        )

        if recommendations:

            if (
                isinstance(
                    recommendations[0],
                    dict,
                )
                and "title" in recommendations[0]
            ):

                recommendation_list = [

                    item["title"]

                    for item in recommendations

                ]

            else:

                recommendation_list = [

                    str(item)

                    for item in recommendations

                ]

        else:

            recommendation_list = []

        sections.append(

            report_templates.recommendations(

                recommendation_list

            )

        )

        return sections


report_service = ReportService()