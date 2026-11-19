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
        "Units: Passage events / 20-hr Tue-Sat week | All 12 options (8 Affordable <= $18k, 4 Over-Budget) | 8 Missing weeks excluded (n=14-16)",
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
    # 12 rows + 1 full-row divider gap between affordable (8) and over-budget (4)
    total_units = 13.0
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
        # Shift down by 1.0 row after index 7 for clean budget boundary divider clearance
        slot = idx + (1.0 if idx >= 8 else 0.0)
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
            div_y = plot_top - 8.65 * row_h
            c.setStrokeColor(RED_ACCENT)
            c.setLineWidth(0.9)
            c.setDash(3, 2)
            c.line(x + 4, div_y, x + width - 4, div_y)
            c.setDash()
            c.setFillColor(RED_ACCENT)
            c.setFont("Helvetica-Bold", 6.3)
            c.drawString(x + pad, div_y + 3.0, "AFFORDABLE (<= $18,000 BUDGET CAP) ABOVE  |  OVER-BUDGET (> $18,000, EXCLUDED) BELOW")

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
        fontSize=7.0,
        leading=9.5,
        textColor=DARK_TEXT,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        fontName="Helvetica",
        fontSize=7.0,
        leading=9.4,
        leftIndent=10,
        firstLineIndent=-8,
        spaceBefore=1.5,
        textColor=DARK_TEXT,
    )
    callout_style = ParagraphStyle(
        "Callout",
        fontName="Helvetica",
        fontSize=6.9,
        leading=9.2,
        textColor=DARK_TEXT,
    )

    # Top Header Banner
    y = page_h - 22.0
    c.setFillColor(NAVY)
    c.roundRect(margin_x, y - 32, content_w, 32, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11.2)
    c.drawString(margin_x + 10, y - 14, "BUS 240F Final Project - Milestone 1 Checkpoint (Due November 20, 2026)")
    c.setFont("Helvetica", 7.4)
    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.drawString(
        margin_x + 10,
        y - 25.0,
        "Author: Vitaly Chait (Team Deliverable)  |  Snapshot: BUS240F_Final_Project_Starter.twbx  |  Jun 8 - Sep 27, 2026 (16 Wks)  |  Trial: Oct 12 - Nov 8, 2026",
    )
    y -= 40

    # 1. Decision Question
    y = draw_section_header(c, "1", "Decision Question", margin_x, y, content_w)
    y = draw_para(
        c,
        "The <b>pilot-program manager</b> needs to pick <b>one store site and one 4-hour daily shift</b> for a 4-week pop-up shop (<b>Oct 12 - Nov 8, 2026</b>; 20 hours/week, 80 total hours) to test whether shoppers stop to engage with reusable bottles, lunch containers, and carry accessories.",
        body_style,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>12 Options Narrowed to 8 by Budget:</b> There are 6 locations, each with Shift A (Tue-Sat 10am-2pm) or Shift B (Tue-Sat 2pm-6pm). The hard <b>$18,000 total budget cap</b> rules out 4 expensive options (<i>L05_B</i> $21,000; <i>L01_B</i> $19,500; <i>L05_A</i> $19,000; <i>L04_B</i> $18,500) and leaves <b>8 affordable options</b>.",
        bullet_style,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>Top Affordable Choices Compared:</b> Front-runner <b>L01_A (Cedar Walk, Window A, $18,000)</b> vs. steady runner-up <b>L04_A (Birch Arcade, Window A, $17,500)</b>, spike-heavy <b>L06_B (Aspen Court, Window B, $16,000)</b>, and low-variance <b>L02_B (Maple Court, Window B, $16,500)</b>.",
        bullet_style,
        margin_x,
        y,
        content_w,
    )
    y -= 6

    # 2. Defined Metric
    y = draw_section_header(c, "2", "Defined Metric & Data Hygiene", margin_x, y, content_w)
    y = draw_para(
        c,
        "&bull; <b>What We Measure &amp; Units:</b> Weekly foot-traffic crossings (<b>passage events per 20-hour Tue-Sat week</b>) across 16 weekly periods (Week Start Mondays <b>2026-06-08 to 2026-09-21</b>, covering Jun 8 - Sep 27, 2026), summarized by both the <b>Average Observed Passages</b> and the <b>Typical (Median) Middle Week Observed Passages</b>. One person walking past twice counts twice, so these measure <i>foot-traffic exposure</i>, not unique shoppers or sales.",
        bullet_style,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>Baseline Audit &amp; Missing Weeks:</b> All 12 options x 16 weeks = <b>192 scheduled weekly rows</b>: <b>184 Complete</b> (<b>256,773</b> total passages) and <b>8 Missing</b> (7 affordable, 1 over-budget). Missing weeks mean no usable count was recorded, not zero traffic, so they are left blank and excluded from averages (<b>n = 14 to 16</b> complete weeks). Verified source checks: <b>L01_A on 2026-06-08 = Complete (1,175 passages)</b>; <b>L01_A on 2026-06-29 = Missing (blank)</b>. Fixed 4-week cost is read once per option: <b>The minimum of Total Pilot Cost Usd</b>.",
        bullet_style,
        margin_x,
        y,
        content_w,
    )
    y -= 6

    # 3. Preliminary Claim
    y = draw_section_header(c, "3", "Preliminary Claim (What Current Data Shows)", margin_x, y, content_w)
    y = draw_para(
        c,
        "&bull; <b>L01_A Leads Full-Period Traffic ($18,000, n=14 complete weeks):</b> Ranks #1 among affordable sites in both <b>Average (1,510.00 passages/wk)</b> and <b>Typical Median (1,535.00 passages/wk)</b>, with raw sum = 21,140, Standard Deviation (SD) = 302.58, Coefficient of Variation (CV) = 20.04%, Interquartile Range (IQR, continuous) = 477.50, and range 920-1,970.",
        bullet_style,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>L04_A Is the Steadiest Top Contender ($17,500, n=14):</b> Saves $500 and earns the #2 affordable Median (<b>1,424.50</b>) and a <b>1,401.36</b> Average, with smaller weekly swings (SD = 204.49, CV = 14.59%, IQR = 281.75, range 978-1,721).",
        bullet_style,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>L06_B Is Pulled Up by Outliers ($16,000, n=15):</b> Saves $2,000 and posts raw sum 21,439 and a <b>1,429.27</b> Average, but its Typical Median drops to <b>1,327.00</b> with wide swings (SD = 470.64, CV = 32.93%, IQR = 554.50, range 840-2,422). Benchmark <b>L02_B ($16,500, n=15)</b> is very steady (CV = 9.62%) at Mean 1,325.73 / Median 1,316.00.",
        bullet_style,
        margin_x,
        y,
        content_w,
    )
    y -= 7

    # 4. Static View (Visualization)
    chart_h = 256.0
    y = draw_static_chart(c, golden, margin_x, y, content_w, chart_h)
    y -= 6

    # 5. Unresolved Question
    y = draw_section_header(c, "5", "Unresolved Question & Key Checks Before Final Decision", margin_x, y, content_w)
    y = draw_para(
        c,
        "&bull; <b>Shared-Week Overlap (10-Wk All-Affordable vs. 12-Wk Pairwise):</b> Excluding all 6 missing-overlap dates across the 8 affordable sites drops L01_A's average to <b>1,407.00</b> (median 1,390.00), letting <b>L04_A lead at 1,449.70</b> (median 1,458.50). Yet 2 excluded dates (07-20, 08-10) came from other sites while L01_A &amp; L04_A share <b>12 pairwise weeks</b> where L01_A leads <b>1,482.08 vs. 1,388.25</b> (6-6 wins; median diff -1.50).",
        bullet_style,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>Spikes, Missingness &amp; Seasonality:</b> Dropping <i>L06_B</i>'s spikes (<b>2,422</b> on 07-06; <b>2,343</b> on 08-17) pulls its <i>n=13</i> mean to <b>1,282.62</b>. Over Aug 31-Sep 21, <i>L04_A</i> averages <b>1,472.67</b> (<i>n=3</i>; missing 09-07 when <i>L04_B</i> hit 1,144) vs. <i>L01_A</i> <b>1,370.00</b> (<i>n=4</i>; <b>1,311.67</b> shared <i>n=3</i>). On 2 shared Sep weeks (09-14, 09-21), <i>L01_A</i> leads <b>1,507.50</b> (3 Sep wks <b>1,520.00</b>) vs. <i>L04_A</i> <b>1,459.00</b>.",
        bullet_style,
        margin_x,
        y,
        content_w,
    )
    y -= 6

    # Suggested Narrative Template Callout Box
    tmpl_html = (
        "<b>Suggested Narrative Template (Completed):</b><br/>"
        "&bull; <b>Decision:</b> We are deciding between <b>L01_A (Cedar Walk, Window A, $18,000)</b> and <b>L04_A (Birch Arcade, Window A, $17,500) / L06_B (Aspen Court, Window B, $16,000)</b> for <b>testing shopper engagement in a 4-week reusable-goods pop-up trial (Oct 12 - Nov 8, 2026; 80 scheduled hours)</b>, within <b>the $18,000 total pilot budget constraint</b>.<br/>"
        "&bull; <b>Measurement:</b> Our measure is <b>Average and Typical Median passage events per 20-hour Tue-Sat week across Jun 8 - Sep 27, 2026 (16 weeks total; 8 missing rows left blank and excluded from denominators, n = 14 to 16)</b>.<br/>"
        "&bull; <b>View:</b> The view suggests <b>L01_A leads all 8 affordable options in both Mean (1,510.00) and Median (1,535.00), ahead of L06_B (1,429.27 mean / 1,327.00 median) and L04_A (1,401.36 mean / 1,424.50 median)</b>.<br/>"
        "&bull; <b>TODO:</b> We still need to check <b>the operational causes of L01_A's missing weeks (06-29, 08-24) and L04_A's missing 09-07 week, whether Oct-Nov autumn seasonality erodes L01_A's narrow 6-6 paired edge over L04_A, and what fraction of crossings are repeat passersby</b>."
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
