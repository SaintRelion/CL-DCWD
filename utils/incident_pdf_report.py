from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from database.db_locations import location_dict

# Palette
BLUE = colors.HexColor("#2C5F8A")
LIGHT_BLUE = colors.HexColor("#EBF3FA")
GRAY = colors.HexColor("#5F5E5A")
LIGHT_GRAY = colors.HexColor("#F5F5F3")
BORDER = colors.HexColor("#D3D1C7")
GREEN = colors.HexColor("#1D9E75")
RED = colors.HexColor("#D85A30")


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontSize=20,
            textColor=BLUE,
            spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=base["Normal"],
            fontSize=10,
            textColor=GRAY,
            spaceAfter=2,
            fontName="Helvetica",
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontSize=12,
            textColor=BLUE,
            spaceBefore=14,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#2C2C2A"),
            fontName="Helvetica",
            leading=14,
        ),
        "meta_label": ParagraphStyle(
            "MetaLabel",
            parent=base["Normal"],
            fontSize=8,
            textColor=GRAY,
            fontName="Helvetica-Bold",
        ),
        "meta_val": ParagraphStyle(
            "MetaVal",
            parent=base["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#2C2C2A"),
            fontName="Helvetica",
        ),
    }


def export_incidents_pdf(
    incidents: list,
    output_path: str = "incident_report.pdf",
    title: str = "Water Incident Report",
):
    """
    Generates a readable PDF report from a list of incident rows.

    Each row: (id, timestamp, category_name, location_id, street_name, plumber_name, status)
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    s = _styles()
    story = []
    now_str = datetime.now().strftime("%B %d, %Y  %I:%M %p")

    # Header
    story.append(Paragraph(title, s["title"]))
    story.append(Paragraph(f"Generated on {now_str}", s["subtitle"]))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceAfter=10))

    # Summary strip
    total = len(incidents)
    handled = sum(1 for r in incidents if r[6] == "Handled")
    active = sum(1 for r in incidents if r[6] == "Active")
    no_plumber = sum(1 for r in incidents if not r[5])

    summary_data = [
        [
            Paragraph("TOTAL INCIDENTS", s["meta_label"]),
            Paragraph("HANDLED", s["meta_label"]),
            Paragraph("ACTIVE", s["meta_label"]),
            Paragraph("NO PLUMBER ASSIGNED", s["meta_label"]),
        ],
        [
            Paragraph(
                str(total),
                ParagraphStyle(
                    "Big", fontSize=18, fontName="Helvetica-Bold", textColor=BLUE
                ),
            ),
            Paragraph(
                str(handled),
                ParagraphStyle(
                    "Big", fontSize=18, fontName="Helvetica-Bold", textColor=GREEN
                ),
            ),
            Paragraph(
                str(active),
                ParagraphStyle(
                    "Big", fontSize=18, fontName="Helvetica-Bold", textColor=RED
                ),
            ),
            Paragraph(
                str(no_plumber),
                ParagraphStyle(
                    "Big", fontSize=18, fontName="Helvetica-Bold", textColor=GRAY
                ),
            ),
        ],
    ]
    summary_table = Table(summary_data, colWidths=["25%", "25%", "25%", "25%"])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 16))

    # Incident detail section
    story.append(Paragraph("Incident Details", s["section"]))
    story.append(Spacer(1, 4))

    # Table header
    col_widths = [
        0.55 * inch,
        1.3 * inch,
        1.1 * inch,
        1.2 * inch,
        1.1 * inch,
        1.2 * inch,
        0.75 * inch,
    ]
    header_style = ParagraphStyle(
        "TH", fontSize=8, fontName="Helvetica-Bold", textColor=colors.white, leading=10
    )
    cell_style = ParagraphStyle(
        "TD",
        fontSize=8,
        fontName="Helvetica",
        textColor=colors.HexColor("#2C2C2A"),
        leading=11,
    )

    rows = [
        [
            Paragraph("ID", header_style),
            Paragraph("Date", header_style),
            Paragraph("Category", header_style),
            Paragraph("Barangay", header_style),
            Paragraph("Street", header_style),
            Paragraph("Plumber", header_style),
            Paragraph("Status", header_style),
        ]
    ]

    for row in incidents:
        inc_id, ts, category, loc_id, street, plumber, status, remarks = row

        # Readable date
        date_str = ts.strftime("%b %d, %Y\n%I:%M %p") if ts else "—"

        # Barangay from location_dict
        loc_data = location_dict.get(loc_id, {})
        barangay = loc_data.get("barangay", "Unknown")

        street_str = street or "—"
        plumber_str = plumber or "Unassigned"
        cat_str = (category or "Unknown").title()

        # Status colour
        stat_color = (
            GREEN if status == "Handled" else (RED if status == "Active" else GRAY)
        )
        stat_style = ParagraphStyle(
            "Stat",
            fontSize=8,
            fontName="Helvetica-Bold",
            textColor=stat_color,
            leading=10,
        )

        rows.append(
            [
                Paragraph(str(inc_id), cell_style),
                Paragraph(date_str, cell_style),
                Paragraph(cat_str, cell_style),
                Paragraph(barangay, cell_style),
                Paragraph(street_str, cell_style),
                Paragraph(plumber_str, cell_style),
                Paragraph(status or "—", stat_style),
            ]
        )

    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                # Header row
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                # Alternating rows
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
                # Grid
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
                # Padding
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(table)

    # Footer note
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))
    story.append(
        Paragraph(
            "This report was generated automatically by the Water Incident Management System.",
            ParagraphStyle(
                "Footer", fontSize=7, textColor=GRAY, fontName="Helvetica-Oblique"
            ),
        )
    )

    doc.build(story)
    print(f"[PDF] Report saved → {output_path}")
    return output_path
