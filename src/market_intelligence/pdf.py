"""A4 PDF renderer using reportlab; only accepts validated report objects."""
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

NAVY = colors.HexColor("#13243C")
TEAL = colors.HexColor("#136A79")
LIGHT = colors.HexColor("#EAF1F5")
MUTED = colors.HexColor("#586A79")
RED = colors.HexColor("#AC3640")


def render_pdf(report, output):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    st = getSampleStyleSheet()
    st.add(ParagraphStyle(name="MITitle", fontName="Helvetica-Bold", fontSize=19,
                          leading=24, textColor=NAVY, spaceAfter=12))
    st.add(ParagraphStyle(name="MIHead", fontName="Helvetica-Bold", fontSize=11,
                          leading=14, textColor=TEAL, spaceBefore=12, spaceAfter=7))
    st.add(ParagraphStyle(name="MIBody", fontName="Helvetica", fontSize=8,
                          leading=11.5, textColor=NAVY, spaceAfter=6))
    st.add(ParagraphStyle(name="MISmall", fontName="Helvetica", fontSize=6.8,
                          leading=9, textColor=MUTED))
    st.add(ParagraphStyle(name="MICell", fontName="Helvetica", fontSize=7,
                          leading=9, textColor=NAVY))
    doc = SimpleDocTemplate(str(path), pagesize=(210*mm,297*mm),
                            leftMargin=17*mm, rightMargin=17*mm,
                            topMargin=17*mm, bottomMargin=17*mm)
    story = []
    def p(value, style="MIBody"):
        return Paragraph(escape(str(value)), st[style])
    def section(number, text):
        story.append(Paragraph(str(number) + ". " + escape(text), st["MIHead"]))
    def table(rows, widths):
        data = [[p(c, "MICell") for c in row] for row in rows]
        t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, -1), (-1, -1), 0.4, LIGHT),
        ]))
        story.append(t)
    def sources(item):
        refs = item.get("source_ids", [])
        return " [" + ", ".join(refs) + "]" if refs else ""
    story.append(Paragraph("MARKET INTELLIGENCE", st["MITitle"]))
    story.append(p(report["edition"]["asof"] + " | Europe/Paris", "MISmall"))
    story.append(Spacer(1, 6))
    if report["synthetic"]:
        story.append(Paragraph("<font color='#AC3640'><b>DONNÉES FICTIVES - DÉMONSTRATION - NE PAS DIFFUSER COMME RAPPORT RÉEL</b></font>", st["MIBody"]))
    section(1, "Synthèse exécutive")
    for item in report["summary"]:
        story.append(p(item["kind"].upper() + " : " + item["text"] + sources(item)))
    section(2, "Principaux marchés")
    rows = [["Instrument", "Valeur", "Var.", "Statut / Heure / Source"]]
    for item in report["markets"]:
        val = "Non vérifié" if item["value"] is None else str(item["value"]) + " " + item.get("unit", "")
        rows.append([item["instrument"], val, item.get("change") or "-",
                     item["status"] + " | " + str(item.get("asof", "-")) + " | " + str(item.get("source_id", "-"))])
    table(rows, [36*mm, 32*mm, 23*mm, 85*mm])
    section(3, "Analyse macroéconomique et financière")
    for item in report["macro"]:
        story.append(p(item["kind"].upper() + " : " + item["text"] + sources(item)))
    section(4, "Trois risques et scénarios")
    table([["Risque", "Scénario favorable", "Scénario défavorable"]] + [
        [x["title"], x["upside"], x["downside"]] for x in report["risks"]
    ], [39*mm, 68*mm, 69*mm])
    section(5, "Trois événements prioritaires")
    table([["Événement", "Horodatage", "Importance / Source"]] + [
        [x["title"], x.get("asof") or "Non vérifié",
         x.get("impact", "") + " | " + (", ".join(x["source_ids"]) if x.get("verified") else "NON VÉRIFIÉ")]
        for x in report["events"]
    ], [49*mm, 55*mm, 72*mm])
    section(6, "Sources consultables")
    for item in report["sources"]:
        url = escape(item["url"], quote=True)
        name = escape(item.get("title", item["id"]))
        story.append(Paragraph("[" + escape(item["id"]) + "] <link href='" + url + "' color='#136A79'>" + name + "</link> - " + escape(item["url"]), st["MISmall"]))
        story.append(Spacer(1, 4))
    section(7, "Impact portefeuille IBKR")
    portfolio = report["portfolio"]
    if portfolio["status"] == "inaccessible":
        story.append(p(portfolio["message"]))
        story.append(p("Les anciennes positions ne sont pas utilisées. Aucun ordre n'est passé."))
    else:
        story.append(p("NAV : " + str(portfolio["nav"]) + " " + portfolio["base_currency"] +
                       " | Cash : " + str(portfolio["cash"]) + " | " + portfolio["asof"] +
                       " | Realtime : " + str(portfolio["realtime"])))
        table([["Ticker", "Qté", "Valeur", "Poids NAV", "P&L jour / latent"]] + [
            [x["ticker"], str(x["quantity"]), str(x["market_value"]) + " " + x["currency"],
             str(x["weight_pct"]) + " %", str(x.get("daily_pnl", "N/D")) + " / " + str(x.get("unrealized_pnl", "N/D"))]
            for x in portfolio["positions"]
        ], [29*mm, 19*mm, 45*mm, 29*mm, 54*mm])
        story.append(p("Ecart de rapprochement : " + str(portfolio["reconciliation_difference"])))
        story.append(p("Secteurs directs : " + str(portfolio["sector_weights_pct"])))
        story.append(p("Devises des titres : " + str(portfolio["currency_weights_pct"])))
    if report["quality_warnings"]:
        story.append(Paragraph("Points de vigilance", st["MIHead"]))
        for item in report["quality_warnings"]:
            story.append(p("- " + item))
    story.append(p("Document de recherche, pas un conseil en investissement. Sources et horaires hétérogènes.", "MISmall"))
    def foot(canvas, document):
        canvas.saveState()
        width, height = document.pagesize
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(17*mm, 10*mm, "Market Intelligence | research only | no orders")
        canvas.drawRightString(width-17*mm, 10*mm, "Page " + str(document.page))
        canvas.restoreState()
    doc.build(story, onFirstPage=foot, onLaterPages=foot)
