from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


EXECUTIVE_SUMMARY_MD = Path("executive_summary.md")
FINAL_REPORT_MD = Path("final_report.md")

REPORTS_DIR = Path("outputs/reports")
EXECUTIVE_SUMMARY_PDF = REPORTS_DIR / "executive_summary.pdf"
FINAL_REPORT_PDF = REPORTS_DIR / "final_analysis_report.pdf"

CHARTS = {
    "1": Path("outputs/charts/01_revenue_net_income_trend.png"),
    "2": Path("outputs/charts/02_credit_card_loans_trend.png"),
    "3": Path("outputs/charts/03_provision_to_revenue_pressure.png"),
    "4": Path("outputs/charts/04_credit_risk_rates_trend.png"),
    "5": Path("outputs/charts/05_discover_cost_pressure.png"),
}


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontSize=20,
            leading=24,
            spaceAfter=14,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Heading1Custom",
            parent=styles["Heading1"],
            fontSize=15,
            leading=18,
            spaceBefore=14,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Heading2Custom",
            parent=styles["Heading2"],
            fontSize=12.5,
            leading=15,
            spaceBefore=10,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontSize=9.4,
            leading=13,
            spaceAfter=7,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BulletCustom",
            parent=styles["BodyText"],
            fontSize=9.4,
            leading=13,
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CodeCustom",
            parent=styles["Code"],
            fontSize=8,
            leading=10,
            backColor=colors.whitesmoke,
            borderColor=colors.lightgrey,
            borderWidth=0.5,
            borderPadding=5,
            spaceAfter=8,
        )
    )

    return styles


def clean_text(text: str) -> str:
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("**", "")
    return text


def add_chart(story, chart_number: str, styles):
    chart_path = CHARTS.get(chart_number)

    if chart_path is None:
        print(f"WARNING: No chart mapping found for Chart {chart_number}")
        return

    if not chart_path.exists():
        story.append(Paragraph(f"Chart image missing: {chart_path}", styles["BodyCustom"]))
        print(f"WARNING: Missing chart image: {chart_path}")
        return

    story.append(Spacer(1, 0.08 * inch))
    story.append(Image(str(chart_path), width=6.75 * inch, height=3.85 * inch))
    story.append(Spacer(1, 0.18 * inch))
    print(f"Embedded Chart {chart_number}: {chart_path}")


def is_chart_path_line(text: str) -> bool:
    return "outputs/charts/" in text and ".png" in text


def markdown_table_to_pdf_table(table_lines):
    rows = []

    for line in table_lines:
        stripped = line.strip()

        cleaned = stripped.replace("|", "").replace(":", "").replace("-", "").strip()
        if cleaned == "":
            continue

        cells = [clean_text(cell.strip()) for cell in stripped.strip("|").split("|")]
        rows.append(cells)

    if not rows:
        return None

    table = Table(rows, repeatRows=1)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 5.8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )

    return table


def markdown_to_pdf(md_path: Path, pdf_path: Path, include_charts: bool = False):
    styles = get_styles()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    story = []
    lines = md_path.read_text(encoding="utf-8").splitlines()

    in_code_block = False
    code_lines = []
    table_lines = []
    chart_count = 0

    for line in lines:
        stripped = line.strip()

        # Handle code block markers first
        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False

                # If a code block only contains chart path, skip printing it
                if code_lines and any(is_chart_path_line(x) for x in code_lines):
                    code_lines = []
                    continue

                if code_lines:
                    story.append(
                        Paragraph(
                            clean_text("<br/>".join(code_lines)),
                            styles["CodeCustom"],
                        )
                    )

                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Flush table if previous lines were table rows
        if table_lines and not (stripped.startswith("|") and stripped.endswith("|")):
            table = markdown_table_to_pdf_table(table_lines)
            if table:
                story.append(table)
                story.append(Spacer(1, 0.15 * inch))
            table_lines = []

        # Skip chart path lines and "File:" labels
        if include_charts and (stripped == "File:" or is_chart_path_line(stripped)):
            continue

        # Most important fix:
        # Detect chart headings BEFORE generic markdown heading logic.
        chart_match = re.match(r"^#{0,6}\s*Chart\s+(\d+):\s*(.*)$", stripped)
        if include_charts and chart_match:
            chart_number = chart_match.group(1)
            chart_title_rest = chart_match.group(2)
            chart_heading = f"Chart {chart_number}: {chart_title_rest}".strip()

            chart_count += 1

            if chart_count > 1:
                story.append(PageBreak())

            story.append(Paragraph(clean_text(chart_heading), styles["Heading2Custom"]))
            add_chart(story, chart_number, styles)
            continue

        # Markdown table rows
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines.append(line)
            continue

        # Empty line
        if stripped == "":
            story.append(Spacer(1, 0.05 * inch))
            continue

        # Markdown titles and headings
        if stripped.startswith("# "):
            story.append(Paragraph(clean_text(stripped.replace("# ", "", 1)), styles["ReportTitle"]))
            continue

        if stripped.startswith("## "):
            story.append(Paragraph(clean_text(stripped.replace("## ", "", 1)), styles["Heading1Custom"]))
            continue

        if stripped.startswith("### "):
            story.append(Paragraph(clean_text(stripped.replace("### ", "", 1)), styles["Heading2Custom"]))
            continue

        # Other headings
        if stripped.startswith("Question ") or stripped == "Interpretation":
            story.append(Paragraph(clean_text(stripped), styles["Heading2Custom"]))
            continue

        # Bullets
        if stripped.startswith("- "):
            story.append(Paragraph("• " + clean_text(stripped[2:]), styles["BulletCustom"]))
            continue

        # Numbered list items
        if re.match(r"^\d+\.\s+", stripped):
            story.append(Paragraph(clean_text(stripped), styles["BodyCustom"]))
            continue

        # Normal paragraph
        story.append(Paragraph(clean_text(stripped), styles["BodyCustom"]))

    # Flush final table
    if table_lines:
        table = markdown_table_to_pdf_table(table_lines)
        if table:
            story.append(table)

    doc.build(story)
    print(f"Created PDF: {pdf_path}")


def main():
    markdown_to_pdf(EXECUTIVE_SUMMARY_MD, EXECUTIVE_SUMMARY_PDF, include_charts=False)
    markdown_to_pdf(FINAL_REPORT_MD, FINAL_REPORT_PDF, include_charts=True)
    print("\nPDF export completed successfully.")


if __name__ == "__main__":
    main()
