"""
PDF report generator using ReportLab.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from .models import FinancialReport


class PDFReportGenerator:
    """
    Generates PDF reports.
    """

    def __init__(self) -> None:

        styles = getSampleStyleSheet()

        self.title_style = styles["Heading1"]
        self.title_style.alignment = TA_CENTER

        self.heading_style = styles["Heading2"]

        self.body_style = styles["BodyText"]

    def generate(
        self,
        report: FinancialReport,
        output_path: str,
    ) -> str:
        """
        Generate a PDF report.

        Returns:
            Path to generated PDF.
        """

        output = Path(output_path)
        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        document = SimpleDocTemplate(
            str(output),
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        elements = []

        self._build_title(
            elements,
            report,
        )

        self._build_summary(
            elements,
            report,
        )

        self._build_sections(
            elements,
            report,
        )

        document.build(elements)

        return str(output)

    def _build_title(
        self,
        elements: list,
        report: FinancialReport,
    ) -> None:

        elements.append(
            Paragraph(
                report.title,
                self.title_style,
            )
        )

        elements.append(
            Spacer(
                1,
                0.3 * inch,
            )
        )

        elements.append(
            Paragraph(
                f"<b>Generated For:</b> "
                f"{report.generated_for}",
                self.body_style,
            )
        )

        elements.append(
            Paragraph(
                f"<b>Date:</b> "
                f"{report.report_date}",
                self.body_style,
            )
        )

        elements.append(
            Paragraph(
                f"<b>Version:</b> "
                f"{report.metadata.version}",
                self.body_style,
            )
        )

        elements.append(
            Spacer(
                1,
                0.35 * inch,
            )
        )

    def _build_summary(
        self,
        elements: list,
        report: FinancialReport,
    ) -> None:

        summary = report.executive_summary

        elements.append(
            Paragraph(
                "Executive Summary",
                self.heading_style,
            )
        )

        elements.append(
            Paragraph(
                summary.overview,
                self.body_style,
            )
        )

        elements.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

        self._bullet_section(
            elements,
            "Strengths",
            summary.strengths,
        )

        self._bullet_section(
            elements,
            "Risks",
            summary.risks,
        )

        self._bullet_section(
            elements,
            "Opportunities",
            summary.opportunities,
        )

        self._bullet_section(
            elements,
            "Recommendations",
            summary.recommendations,
        )

    def _build_sections(
        self,
        elements: list,
        report: FinancialReport,
    ) -> None:

        sections = sorted(
            report.sections,
            key=lambda s: s.order,
        )

        for section in sections:

            elements.append(
                Spacer(
                    1,
                    0.20 * inch,
                )
            )

            elements.append(
                Paragraph(
                    section.title,
                    self.heading_style,
                )
            )

            elements.append(
                Paragraph(
                    section.content.replace(
                        "\n",
                        "<br/>",
                    ),
                    self.body_style,
                )
            )

    def _bullet_section(
        self,
        elements: list,
        title: str,
        items: list[str],
    ) -> None:

        if not items:
            return

        elements.append(
            Paragraph(
                title,
                self.heading_style,
            )
        )

        for item in items:

            elements.append(
                Paragraph(
                    f"• {item}",
                    self.body_style,
                )
            )

        elements.append(
            Spacer(
                1,
                0.15 * inch,
            )
        )


pdf_generator = PDFReportGenerator()