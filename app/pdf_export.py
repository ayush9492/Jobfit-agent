"""Render the resume to a PDF (as bytes) for the Streamlit download button.

Produces a clean one-page resume. (The tailored_bullets highlights section is
optional and off by default — we keep the resume honest and one page.)
"""
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable, Table, TableStyle
from reportlab.lib import colors

from app.resume_data import RESUME


def _styles():
    s = getSampleStyleSheet()
    return {
        "name": ParagraphStyle("Name", parent=s["Title"], fontName="Helvetica-Bold",
                               fontSize=17, alignment=TA_CENTER, spaceAfter=1,
                               textColor=colors.HexColor("#1a1a1a")),
        "contact": ParagraphStyle("Contact", parent=s["Normal"], fontSize=8.8,
                                  alignment=TA_CENTER, spaceAfter=3,
                                  textColor=colors.HexColor("#333333")),
        "section": ParagraphStyle("Section", parent=s["Heading2"], fontName="Helvetica-Bold",
                                  fontSize=10.5, spaceBefore=4, spaceAfter=1,
                                  textColor=colors.HexColor("#1a1a1a")),
        "role": ParagraphStyle("Role", parent=s["Normal"], fontName="Helvetica-Bold",
                               fontSize=9.5, spaceBefore=3, spaceAfter=0),
        "sub": ParagraphStyle("Sub", parent=s["Normal"], fontName="Helvetica-Oblique",
                              fontSize=8.5, spaceAfter=1, textColor=colors.HexColor("#444444")),
        "body": ParagraphStyle("Body", parent=s["Normal"], fontSize=8.7, leading=10.4, spaceAfter=0.8),
        "bullet": ParagraphStyle("Bullet", parent=s["Normal"], fontSize=8.7, leading=10.4,
                                 leftIndent=12, bulletIndent=2, spaceAfter=1),
        "right": ParagraphStyle("Right", parent=s["Normal"], fontSize=9, alignment=2),
    }


def _esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_resume_pdf(resume=None, tailored_bullets=None, role_label=None):
    """Return PDF bytes. tailored_bullets is optional and OFF by default."""
    resume = resume or RESUME
    st = _styles()
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
                            leftMargin=0.55 * inch, rightMargin=0.55 * inch,
                            topMargin=0.4 * inch, bottomMargin=0.3 * inch)
    story = []

    def rule():
        story.append(HRFlowable(width="100%", thickness=0.6,
                                color=colors.HexColor("#888888"), spaceBefore=0.5, spaceAfter=2))

    def section(title):
        story.append(Paragraph(_esc(title).upper(), st["section"]))
        rule()

    def bullet(text):
        story.append(Paragraph(_esc(text), st["bullet"], bulletText="•"))

    def role_row(left_bold, right_plain):
        t = Table([[Paragraph(_esc(left_bold), st["role"]),
                    Paragraph(_esc(right_plain), st["right"])]],
                  colWidths=[4.7 * inch, 2.65 * inch])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 2),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
        story.append(t)

    # header
    story.append(Paragraph(_esc(resume["name"]), st["name"]))
    story.append(Paragraph(_esc(resume["contact"]), st["contact"]))

    # optional highlights (OFF by default — pass tailored_bullets to enable)
    if tailored_bullets:
        heading = "Highlights Tailored for This Role"
        if role_label:
            heading = f"Highlights Tailored for: {role_label}"
        section(heading)
        for b in tailored_bullets:
            bullet(b)

    section("Summary")
    story.append(Paragraph(_esc(resume["summary"]), st["body"]))

    section("Education")
    for e in resume["education"]:
        role_row(e["school"], e["loc"])
        story.append(Paragraph(_esc(e["detail"]), st["sub"]))

    section("Skills")
    for label, items in resume["skills"]:
        story.append(Paragraph(f"<b>{_esc(label)}:</b> {_esc(items)}", st["body"]))

    section("Work Experience")
    for job in resume["experience"]:
        role_row(job["org"], job["loc"])
        story.append(Paragraph(_esc(job["role"]), st["sub"]))
        for b in job["bullets"]:
            bullet(b)

    section("Projects")
    for p in resume["projects"]:
        story.append(Paragraph(_esc(p["name"]), st["role"]))
        story.append(Paragraph(_esc(p["stack"]), st["sub"]))
        for b in p["bullets"]:
            bullet(b)

    section("Leadership & Activities")
    lead = resume["leadership"]
    lead_cell = ParagraphStyle("LeadCell", parent=st["bullet"], leftIndent=8,
                               bulletIndent=0, fontSize=8.3, leading=9.8)
    if len(lead) >= 2:
        cells = [Paragraph("• " + _esc(x), lead_cell) for x in lead[:2]]
        lt = Table([cells], colWidths=[3.65 * inch, 3.65 * inch])
        lt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                ("RIGHTPADDING", (0, 0), (0, 0), 10),
                                ("TOPPADDING", (0, 0), (-1, -1), 0),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
        story.append(lt)
        for extra in lead[2:]:
            bullet(extra)
    else:
        for item in lead:
            bullet(item)

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()