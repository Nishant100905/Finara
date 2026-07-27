"""
Markdown report generator.
"""

from __future__ import annotations

from .models import FinancialReport


class MarkdownReportGenerator:
    """
    Converts FinancialReport into Markdown.
    """

    def generate(
        self,
        report: FinancialReport,
    ) -> str:

        lines: list[str] = []

        lines.append(
            f"# {report.title}"
        )

        lines.append("")

        lines.append(
            f"**Generated For:** {report.generated_for}"
        )

        lines.append(
            f"**Date:** {report.report_date}"
        )

        lines.append(
            f"**Version:** {report.metadata.version}"
        )

        lines.append("")

        lines.append("## Executive Summary")

        lines.append("")

        summary = report.executive_summary

        lines.append(summary.overview)

        lines.append("")

        if summary.strengths:

            lines.append("### Strengths")

            for item in summary.strengths:

                lines.append(f"- {item}")

            lines.append("")

        if summary.risks:

            lines.append("### Risks")

            for item in summary.risks:

                lines.append(f"- {item}")

            lines.append("")

        if summary.opportunities:

            lines.append("### Opportunities")

            for item in summary.opportunities:

                lines.append(f"- {item}")

            lines.append("")

        if summary.recommendations:

            lines.append("### Recommendations")

            for item in summary.recommendations:

                lines.append(f"- {item}")

            lines.append("")

        for section in sorted(
            report.sections,
            key=lambda x: x.order,
        ):

            lines.append(
                f"## {section.title}"
            )

            lines.append("")

            lines.append(
                section.content
            )

            lines.append("")

        return "\n".join(lines)


markdown_generator = MarkdownReportGenerator()