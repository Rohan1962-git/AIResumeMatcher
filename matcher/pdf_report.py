
from io import BytesIO

from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from xml.sax.saxutils import escape

from .models import ResumeAnalysis


@login_required(login_url="login")
def download_pdf_report(request, analysis_id):
    analysis = get_object_or_404(
        ResumeAnalysis,
        id=analysis_id,
        user=request.user,
    )

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1d4ed8"),
        spaceAfter=18,
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#1d4ed8"),
        spaceBefore=12,
        spaceAfter=8,
    )

    story = []

    story.append(Paragraph("AI Resume Matcher", title_style))
    story.append(Paragraph("Resume Analysis Report", styles["Heading2"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        f"<b>Resume:</b> {escape(analysis.resume_name)}",
        styles["BodyText"],
    ))
    story.append(Paragraph(
        f"<b>Analysis Date:</b> "
        f"{analysis.created_at.strftime('%d %B %Y, %I:%M %p')}",
        styles["BodyText"],
    ))
    story.append(Spacer(1, 12))

    score_data = [
        ["Overall Match Score", f"{analysis.match_score}%"]
    ]

    score_table = Table(score_data, colWidths=[110 * mm, 45 * mm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1e3a8a")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 13),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#bfdbfe")),
        ("PADDING", (0, 0), (-1, -1), 12),
    ]))

    story.append(score_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Matching Skills", section_style))

    matched = [
        skill.strip()
        for skill in analysis.matched_skills.split(",")
        if skill.strip()
    ]

    if matched:
        for skill in matched:
            story.append(Paragraph(
                f"&bull; {escape(skill)}",
                styles["BodyText"],
            ))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph(
            "No matching skills found.",
            styles["BodyText"],
        ))

    story.append(Paragraph("Skills to Develop", section_style))

    missing = [
        skill.strip()
        for skill in analysis.missing_skills.split(",")
        if skill.strip()
    ]

    if missing:
        for skill in missing:
            story.append(Paragraph(
                f"&bull; {escape(skill)}",
                styles["BodyText"],
            ))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph(
            "No missing skills recorded.",
            styles["BodyText"],
        ))

    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Note: This score is based on the skills recognized by the "
        "application. It is not a guarantee of job suitability.",
        styles["Italic"],
    ))

    document.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="resume_analysis_report.pdf"'
    )

    return response