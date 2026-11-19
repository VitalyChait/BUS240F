#!/usr/bin/env python3
"""Component 3: Build Vitaly_Chait_Project_Checkpoint.pdf (Strictly 1 Page).

Generates a high-resolution, single-page executive Milestone 1 Checkpoint PDF
adhering strictly to Instructions/project_checkpoint_template.md and
Deliverables/golden_metrics.json.
"""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_PATH = REPO_ROOT / "Deliverables" / "golden_metrics.json"
OUT_PDF = REPO_ROOT / "Vitaly_Chait_Project_Checkpoint.pdf"

NAVY = colors.HexColor("#1B365D")
BLUE = colors.HexColor("#1F618D")
TEAL = colors.HexColor("#0E7C7B")
AMBER = colors.HexColor("#D97706")
SLATE = colors.HexColor("#4A6B82")
MUTED = colors.HexColor("#64748B")
OVER_COLOR = colors.HexColor("#94A3B8")
LIGHT_BG = colors.HexColor("#F1F5F9")
CALLOUT_BG = colors.HexColor("#EEF4FA")
BORDER = colors.HexColor("#CBD5E1")
DARK_TEXT = colors.HexColor("#1E293B")
RED_ACCENT = colors.HexColor("#B91C1C")


def draw_para(
    c: canvas.Canvas,
    html_text: str,
    style: ParagraphStyle,
    x: float,
    y_top: float,
    width: float,
) -> float:
    """Wrap and draw a ReportLab Paragraph from top-left (x, y_top); return new y below."""
    p = Paragraph(html_text, style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def draw_section_header(c: canvas.Canvas, num: str, title: str, x: float, y_top: float, width: float) -> float:
    c.setFillColor(NAVY)
    c.rect(x, y_top - 13, 3, 11, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(x + 7, y_top - 11, f"{num}. {title}")
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.6)
    c.line(x, y_top - 15.5, x + width, y_top - 15.5)
    return y_top - 19


def draw_static_chart(
    c: canvas.Canvas,
    golden: dict,
    x: float,
    y_top: float,
    width: float,
    height: float,
) -> float:
    """Draw vector distribution & mean/median chart across all 12 candidate options."""
    opts = golden["options"]
    ordered_ids = [
        "L01_A", "L06_B", "L04_A", "L02_B", "L02_A", "L06_A", "L03_B", "L03_A",
        "L05_B", "L01_B", "L05_A", "L04_B",
    ]

    # Chart card container
    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.8)
    c.roundRect(x, y_top - height, width, height, 4, fill=1, stroke=1)

    # Title & metadata subtitle inside chart box
    pad = 8
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8.6)
    c.drawString(
        x + pad,
        y_top - 13,
        "4. Static View: Weekly Observed Passages (Jun 8 - Sep 27, 2026)",
    )
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.0)
    c.drawString(
        x + pad,
        y_top - 22.5,
        "Units: Passage events / 20-hr scheduled week (Tue-Sat) | 8 Missing weeks excluded (n=14..16) | Budget Cap <= $18,000",
    )

    # Legend (top-right)
    leg_y = y_top - 13
    lx = x + width - 178
    c.setStrokeColor(SLATE)
    c.setLineWidth(1.0)
    c.line(lx, leg_y + 2, lx + 11, leg_y + 2)
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica", 6.7)
    c.drawString(lx + 14, leg_y, "Min-Max")

    c.setFillColor(colors.HexColor("#BFDBFE"))
    c.rect(lx + 47, leg_y - 1, 9, 5.5, fill=1, stroke=0)
    c.setFillColor(DARK_TEXT)
    c.drawString(lx + 59, leg_y, "IQR")

    c.setFillColor(BLUE)
    c.circle(lx + 81, leg_y + 2, 2.6, fill=1, stroke=0)
    c.setFillColor(DARK_TEXT)
    c.drawString(lx + 87, leg_y, "Mean")

    c.setFillColor(colors.white)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.0)
    mx = lx + 114
    my = leg_y + 2
    p = c.beginPath()
    p.moveTo(mx, my + 2.8)
    p.lineTo(mx + 2.8, my)
    p.lineTo(mx, my - 2.8)
    p.lineTo(mx - 2.8, my)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(DARK_TEXT)
    c.drawString(lx + 120, leg_y, "Median")

    # Plot coordinate system
    label_x = x + pad
    plot_left = x + 154
    plot_right = x + width - 132
    plot_w = plot_right - plot_left
    val_min, val_max = 700.0, 2600.0

    def x_of(val: float) -> float:
        return plot_left + (val - val_min) / (val_max - val_min) * plot_w

    plot_top = y_top - 32
    plot_bottom = y_top - height + 18
    # 12 rows + 1 divider gap between affordable (8) and over-budget (4)
    total_units = 12.6
    row_h = (plot_top - plot_bottom) / total_units

    # Vertical gridlines
    ticks = [800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]
    for t in ticks:
        gx = x_of(t)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.5)
        c.line(gx, plot_bottom, gx, plot_top)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.6)
        c.drawCentredString(gx, plot_bottom - 9, f"{t:,}")

    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawCentredString((plot_left + plot_right) / 2, plot_bottom - 16, "Observed Weekly Passages (passage events / 20-hr week)")

    # Column headers
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawString(label_x, plot_top + 1.5, "Option | Location (Win)")
    c.drawRightString(plot_left - 6, plot_top + 1.5, "Cost | n")
    c.drawString(plot_right + 6, plot_top + 1.5, "Mean | Med | CV% | Range")

    for idx, oid in enumerate(ordered_ids):
        o = opts[oid]
        # Shift down by 0.6 row after index 7 for budget boundary divider
        slot = idx + (0.6 if idx >= 8 else 0.0)
        cy = plot_top - (slot + 0.5) * row_h

        # Alternating subtle row tint
        if idx % 2 == 0:
            c.setFillColor(colors.HexColor("#F8FAFC"))
            c.rect(x + 4, cy - row_h * 0.48, width - 8, row_h * 0.96, fill=1, stroke=0)

        # Highlight color by role
        if oid == "L01_A":
            accent = BLUE
            iqr_fill = colors.HexColor("#BFDBFE")
        elif oid == "L04_A":
            accent = TEAL
            iqr_fill = colors.HexColor("#99F6E4")
        elif oid == "L06_B":
            accent = AMBER
            iqr_fill = colors.HexColor("#FDE68A")
        elif o["within_budget"]:
            accent = SLATE
            iqr_fill = colors.HexColor("#CBD5E1")
        else:
            accent = OVER_COLOR
            iqr_fill = colors.HexColor("#E2E8F0")

        # Left label
        is_key = oid in ("L01_A", "L04_A", "L06_B")
        c.setFillColor(DARK_TEXT if o["within_budget"] else MUTED)
        c.setFont("Helvetica-Bold" if is_key else "Helvetica", 7.0)
        c.drawString(label_x, cy - 2.3, f"{oid} {o['location_name']} ({o['window_id']})")

        c.setFont("Helvetica", 6.7)
        c.drawRightString(plot_left - 6, cy - 2.3, f"${o['total_pilot_cost_usd']:,} | n={o['obs_weeks']}")

        # Min-Max whisker
        x_min = x_of(o["min"])
        x_max = x_of(o["max"])
        c.setStrokeColor(accent)
        c.setLineWidth(1.0)
        c.line(x_min, cy, x_max, cy)
        c.line(x_min, cy - 2.5, x_min, cy + 2.5)
        c.line(x_max, cy - 2.5, x_max, cy + 2.5)

        # Approximate IQR box centered around median/mean span (exact width = o['iqr'])
        # Compute exact Q1/Q3 from CSV? Wait: we know min/max/median/iqr; let's compute exact Q1/Q3 from Weekly_Activity.csv!
        q1, q3 = o["q1"], o["q3"]
        x_q1 = x_of(q1)
        x_q3 = x_of(q3)
        c.setFillColor(iqr_fill)
        c.setStrokeColor(accent)
        c.setLineWidth(0.5)
        c.rect(x_q1, cy - 3.6, max(x_q3 - x_q1, 1.5), 7.2, fill=1, stroke=1)

        # Mean dot
        xm = x_of(o["mean"])
        c.setFillColor(accent)
        c.circle(xm, cy, 3.0, fill=1, stroke=0)

        # Median diamond
        xmed = x_of(o["median"])
        c.setFillColor(colors.white)
        c.setStrokeColor(NAVY if o["within_budget"] else MUTED)
        c.setLineWidth(0.9)
        dp = c.beginPath()
        dp.moveTo(xmed, cy + 3.1)
        dp.lineTo(xmed + 3.1, cy)
        dp.lineTo(xmed, cy - 3.1)
        dp.lineTo(xmed - 3.1, cy)
        dp.close()
        c.drawPath(dp, stroke=1, fill=1)

        # Right metrics readout
        c.setFillColor(DARK_TEXT if o["within_budget"] else MUTED)
        c.setFont("Helvetica-Bold" if is_key else "Helvetica", 6.6)
        c.drawString(
            plot_right + 6,
            cy - 2.3,
            f"{o['mean']:,.2f} | {o['median']:,.2f} | {o['cv_pct']:.2f}% | {o['min']:,}-{o['max']:,}",
        )

        # Budget boundary divider after row index 7
        if idx == 7:
            div_y = plot_top - 8.3 * row_h
            c.setStrokeColor(RED_ACCENT)
            c.setLineWidth(0.9)
            c.setDash(3, 2)
            c.line(x + 4, div_y, x + width - 4, div_y)
            c.setDash()
            c.setFillColor(RED_ACCENT)
            c.setFont("Helvetica-Bold", 6.6)
            c.drawString(x + pad, div_y + 2.0, "AFFORDABLE (<= $18,000 BUDGET CAP) ABOVE  |  OVER-BUDGET (> $18,000, EXCLUDED) BELOW")

    return y_top - height


def attach_exact_quartiles(golden: dict) -> None:
    import pandas as pd

    wa = pd.read_csv(REPO_ROOT / "Data" / "Weekly_Activity.csv")
    for oid, o in golden["options"].items():
        vals = wa[(wa["option_id"] == oid) & (wa["observation_status"] == "Complete")]["observed_passages"].astype(float)
        o["q1"] = float(vals.quantile(0.25))
        o["q3"] = float(vals.quantile(0.75))


def build_checkpoint_pdf() -> None:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    attach_exact_quartiles(golden)

    page_w, page_h = letter  # 612 x 792
    margin_x = 34.0
    content_w = page_w - 2 * margin_x

    c = canvas.Canvas(str(OUT_PDF), pagesize=letter, pageCompression=0)
    c.setTitle("BUS 240F Project Checkpoint - Vitaly Chait")
    c.setAuthor("Vitaly Chait")

    body_style = ParagraphStyle(
        "Body",
        fontName="Helvetica",
        fontSize=7.7,
        leading=9.7,
        textColor=DARK_TEXT,
    )
    callout_style = ParagraphStyle(
        "Callout",
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.4,
        textColor=DARK_TEXT,
    )

    # Top Header Banner
    y = page_h - 22.0
    c.setFillColor(NAVY)
    c.roundRect(margin_x, y - 32, content_w, 32, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(margin_x + 10, y - 14, "BUS 240F Final Project - Milestone 1 Checkpoint (Due November 20, 2026)")
    c.setFont("Helvetica", 7.6)
    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.drawString(
        margin_x + 10,
        y - 25.0,
        "Author: Vitaly Chait  |  Snapshot: BUS240F_Final_Project_Starter.twbx  |  Historical Window: Jun 8 - Sep 27, 2026 (16 Weeks)  |  Trial: Oct 12 - Nov 8, 2026",
    )
    y -= 37

    # 1. Decision Question
    y = draw_section_header(c, "1", "Decision Question", margin_x, y, content_w)
    y = draw_para(
        c,
        "<b>Decision Maker &amp; Objective:</b> Advise the <b>pilot-program manager</b> on which single location-and-operating-window option (out of <b>12 candidate options</b>: 6 fictional sites x Windows A [Tue-Sat 10:00-14:00] and B [Tue-Sat 14:00-18:00], 20 scheduled hrs/wk each) to authorize for a 4-week pop-up retail trial (<b>Oct 12 - Nov 8, 2026</b>; 80 total hours) evaluating passerby engagement with reusable bottles, lunch containers, and carry accessories. "
        "<b>Binding Constraint:</b> Fixed 4-week pilot cost must satisfy <b>Total Pilot Cost &lt;= $18,000</b>, eliminating 4 over-budget options (<i>L05_B</i> $21,000; <i>L01_B</i> $19,500; <i>L05_A</i> $19,000; <i>L04_B</i> $18,500) and focusing comparison on the <b>8 affordable options</b> - specifically primary candidate <b>L01_A (Cedar Walk, Window A, $18,000)</b> vs. credible alternatives <b>L04_A (Birch Arcade, Window A, $17,500)</b>, <b>L06_B (Aspen Court, Window B, $16,000)</b>, and low-variance benchmark <b>L02_B (Maple Court, Window B, $16,500)</b>.",
        body_style,
        margin_x,
        y,
        content_w,
    )
    y -= 4

    # 2. Defined Metric
    y = draw_section_header(c, "2", "Defined Metric & Data Hygiene", margin_x, y, content_w)
    y = draw_para(
        c,
        "<b>Measure &amp; Units:</b> <b>Observed-Week Mean (AVG(Observed Passages))</b> and <b>Observed-Week Median (MEDIAN(Observed Passages))</b> measured in <b>passage events per 20-hour scheduled week</b> across 16 historical Monday weeks (<b>2026-06-08 to 2026-09-21</b>). Passage events count bidirectional line crossings (including repeat crossings) and measure <i>potential exposure</i>, not unique visitors, conversions, or revenue. "
        "<b>Scope &amp; Fixed Cost Rule:</b> All 12 options x 16 weeks = <b>192 scheduled rows</b> (<b>184 Complete</b> totaling <b>256,773</b> passages; <b>8 Missing</b>). Single fixed 4-week cost is read via <b>MIN(Total Pilot Cost Usd)</b> (never summed across 16 weeks). "
        "<b>Missing-Data Treatment:</b> The 8 missing rows (7 affordable: <i>L01_A</i> x2, <i>L04_A</i> x2, <i>L06_B</i> x1, <i>L02_B</i> x1, <i>L03_A</i> x1; plus <i>L05_B</i> x1) are left blank/null and excluded from Mean/Median denominators (<b>n = 14 to 16</b> complete weeks), never zero-filled. Verified starter check rows: <b>L01_A on 2026-06-08 = Complete (1,175 passages)</b>; <b>L01_A on 2026-06-29 = Missing (blank)</b>.",
        body_style,
        margin_x,
        y,
        content_w,
    )
    y -= 4

    # 3. Preliminary Claim
    y = draw_section_header(c, "3", "Preliminary Claim (Bounded Quantitative Evidence)", margin_x, y, content_w)
    y = draw_para(
        c,
        "Across all available complete weeks (<b>2026-06-08 to 2026-09-21</b>), <b>L01_A (Cedar Walk, Window A, $18,000, n=14)</b> leads all 8 affordable options in both <b>Observed-Week Mean (1,510.00 passages/wk)</b> and <b>Observed-Week Median (1,535.00 passages/wk)</b>, with SD = 302.58, CV = 20.04%, IQR = 477.50, and range 920-1,970 (raw sum = 21,140). "
        "<b>L06_B (Aspen Court, Window B, $16,000, n=15)</b> ranks 2nd in Mean (<b>1,429.27</b>, raw sum = 21,439) but drops to 3rd in Median (<b>1,327.00</b>) due to extreme volatility (SD = 470.64, CV = 32.93%, IQR = 554.50, range 840-2,422). "
        "<b>L04_A (Birch Arcade, Window A, $17,500, n=14)</b> delivers 2nd-highest affordable Median (<b>1,424.50</b>) and Mean <b>1,401.36</b> with substantially tighter consistency (SD = 204.49, CV = 14.59%, IQR = 281.75, range 978-1,721), while <b>L02_B ($16,500, n=15)</b> offers the tightest stability among top contenders (Mean 1,325.73, Median 1,316.00, CV = 9.62%).",
        body_style,
        margin_x,
        y,
        content_w,
    )
    y -= 5

    # 4. Static View (Visualization)
    chart_h = 280.0
    y = draw_static_chart(c, golden, margin_x, y, content_w, chart_h)
    y -= 5

    # 5. Unresolved Question
    y = draw_section_header(c, "5", "Unresolved Question & Diagnostic Sensitivity Preview", margin_x, y, content_w)
    y = draw_para(
        c,
        "Three structural uncertainties could alter the preliminary ranking between <b>L01_A</b>, <b>L04_A</b>, and <b>L06_B</b>: "
        "(1) <b>Non-Overlapping Missing Weeks:</b> Restricting to the <b>10 shared complete weeks</b> across all 8 affordable options (excluding 06-22, 06-29, 07-20, 08-10, 08-24, 09-07) drops four strong <i>L01_A</i> weeks and reduces <i>L01_A</i>'s mean from 1,510.00 to <b>1,407.00</b> (median 1,390.00), allowing <b>L04_A (1,449.70 mean / 1,458.50 median)</b> to overtake <i>L01_A</i>. "
        "(2) <b>Unexplained Outlier Spikes:</b> Trimming <i>L06_B</i>'s two extreme summer spikes (<b>2,422</b> on 2026-07-06; <b>2,343</b> on 2026-08-17) lowers its <i>n=13</i> mean from 1,429.27 to <b>1,282.62</b>. "
        "(3) <b>Early-Autumn Seasonality:</b> In the late 4 weeks (Aug 31 - Sep 21), <i>L04_A</i> averages <b>1,472.67</b> vs. <i>L01_A</i> at <b>1,370.00</b> (with an Aug 31 dip to 920).",
        body_style,
        margin_x,
        y,
        content_w,
    )
    y -= 5

    # Suggested Narrative Template Callout Box
    tmpl_html = (
        "<b>Suggested Narrative Template (Completed):</b> &ldquo;I am deciding between "
        "<b>L01_A (Cedar Walk, Window A, $18,000)</b> and <b>L04_A (Birch Arcade, Window A, $17,500) / L06_B (Aspen Court, Window B, $16,000)</b> "
        "for <b>evaluating passerby engagement in a 4-week reusable-goods pop-up trial (Oct 12 - Nov 8, 2026; 80 scheduled hours)</b>, "
        "within <b>the $18,000 total pilot budget constraint</b>. Our measure is "
        "<b>Observed-Week Mean and Median passage events per 20-hour scheduled week across Jun 8 - Sep 27, 2026 (16 historical weeks; 8 missing rows left blank and excluded from denominators, n = 14 to 16)</b>. "
        "The view suggests <b>L01_A leads all 8 affordable options in both Mean (1,510.00) and Median (1,535.00), outperforming L06_B (1,429.27 mean / 1,327.00 median) and L04_A (1,401.36 mean / 1,424.50 median)</b>. "
        "I still need to check <b>how shared-week missingness (10 shared weeks: L04_A 1,449.70 vs. L01_A 1,407.00), L06_B's two outlier spikes (2,422 and 2,343; trimmed mean 1,282.62), and October-November seasonality affect site stability and selection</b>.&rdquo;"
    )
    tp = Paragraph(tmpl_html, callout_style)
    _, th = tp.wrap(content_w - 14, 200)
    box_h = th + 10
    c.setFillColor(CALLOUT_BG)
    c.setStrokeColor(BLUE)
    c.setLineWidth(0.9)
    c.roundRect(margin_x, y - box_h, content_w, box_h, 4, fill=1, stroke=1)
    tp.drawOn(c, margin_x + 7, y - 5 - th)
    y_end = y - box_h

    if y_end < 20:
        raise RuntimeError(f"Page overflow detected! y_end={y_end:.2f}")

    c.showPage()
    c.save()
    print(f"Generated {OUT_PDF.name} cleanly (bottom margin remaining: {y_end:.1f} pt).")


if __name__ == "__main__":
    build_checkpoint_pdf()
