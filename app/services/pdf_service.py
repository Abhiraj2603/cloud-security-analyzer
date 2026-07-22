from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(scan_data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Cloud Security Analyzer Report</b>", styles["Title"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    summary = scan_data.get("summary", {})

    story.append(
        Paragraph(
            f"<b>Total Findings:</b> {summary.get('total_findings',0)}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Security Groups:</b> {summary.get('total_sgs',0)}",
            styles["Normal"],
        )
    )

    story.append(Paragraph("<br/><b>Findings</b>", styles["Heading2"]))

    for finding in scan_data.get("findings", []):

        story.append(
            Paragraph(
                f"""
<b>Severity:</b> {finding.get('severity')}<br/>
<b>Category:</b> {finding.get('category')}<br/>
<b>Title:</b> {finding.get('title')}<br/>
<b>Region:</b> {finding.get('region')}<br/>
<b>Recommendation:</b> {finding.get('remediation')}
""",
                styles["BodyText"],
            )
        )

        story.append(Paragraph("<br/>", styles["Normal"]))

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf
