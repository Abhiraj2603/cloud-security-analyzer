from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class PDFService:
    @staticmethod
    def generate_report(data):
        """
        Generate PDF from run_scan() output.

        Expected input:

        {
            "summary": {...},
            "findings": [...]
        }
        """

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        story = []

        # ======================================================
        # Title
        # ======================================================

        story.append(
            Paragraph(
                "<b>Cloud Security Analyzer</b>",
                styles["Title"],
            )
        )

        story.append(
            Paragraph(
                "AWS Security Assessment Report",
                styles["Heading2"],
            )
        )

        story.append(Spacer(1, 20))

        # ======================================================
        # Summary
        # ======================================================

        summary = data.get("summary", {})

        table_data = [
            ["Metric", "Value"],
            ["Total Findings", str(summary.get("total_findings", 0))],
            ["Critical", str(summary.get("CRITICAL", 0))],
            ["High", str(summary.get("HIGH", 0))],
            ["Medium", str(summary.get("MEDIUM", 0))],
            ["Low", str(summary.get("LOW", 0))],
        ]

        table = Table(table_data)

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                    ("GRID", (0, 0), (-1, -1), 1, colors.black),

                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
            )
        )

        story.append(table)

        story.append(Spacer(1, 20))

        # ======================================================
        # Findings
        # ======================================================

        story.append(
            Paragraph(
                "Security Findings",
                styles["Heading2"],
            )
        )

        findings = data.get("findings", [])

        if not findings:

            story.append(
                Paragraph(
                    "No findings detected.",
                    styles["BodyText"],
                )
            )

        else:

            for finding in findings:

                severity = finding.get("severity", "UNKNOWN")
                title = finding.get("title", "")
                category = finding.get("category", "")
                resource = finding.get("resource", "")
                detail = finding.get("detail", "")
                remediation = finding.get("remediation", "")

                story.append(
                    Paragraph(
                        f"<b>{severity}</b> - {title}",
                        styles["Heading3"],
                    )
                )

                if category:
                    story.append(
                        Paragraph(
                            f"<b>Category:</b> {category}",
                            styles["BodyText"],
                        )
                    )

                if resource:
                    story.append(
                        Paragraph(
                            f"<b>Resource:</b> {resource}",
                            styles["BodyText"],
                        )
                    )

                if detail:
                    story.append(
                        Paragraph(
                            detail,
                            styles["BodyText"],
                        )
                    )

                if remediation:
                    story.append(
                        Paragraph(
                            f"<b>Recommendation:</b> {remediation}",
                            styles["BodyText"],
                        )
                    )

                story.append(Spacer(1, 12))

        doc.build(story)

        buffer.seek(0)

        return buffer
