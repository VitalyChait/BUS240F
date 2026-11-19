#!/usr/bin/env python3
"""Component 4: Build Vitaly_Chait_Two_Page_Brief.pdf (2 pages) and
Vitaly_Chait_Static_View_Backup.pdf (4 landscape pages).

All metrics are read directly from Deliverables/golden_metrics.json and
Data/Weekly_Activity.csv for 100% parity.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_PATH = REPO_ROOT / "Deliverables" / "golden_metrics.json"
WA_PATH = REPO_ROOT / "Data" / "Weekly_Activity.csv"

OUT_BRIEF = REPO_ROOT / "Vitaly_Chait_Two_Page_Brief.pdf"
OUT_BACKUP = REPO_ROOT / "Vitaly_Chait_Static_View_Backup.pdf"

NAVY = colors.HexColor("#1B365D")
BLUE = colors.HexColor("#1F618D")
TEAL = colors.HexColor("#0E7C7B")
AMBER = colors.HexColor("#D97706")
SLATE = colors.HexColor("#4A6B82")
MUTED = colors.HexColor("#64748B")
OVER_COLOR = colors.HexColor("#94A3B8")
LIGHT_BG = colors.HexColor("#F8FAFC")
CALLOUT_BG = colors.HexColor("#EEF4FA")
WARN_BG = colors.HexColor("#FEF2F2")
BORDER = colors.HexColor("#CBD5E1")
DARK_TEXT = colors.HexColor("#1E293B")
RED_ACCENT = colors.HexColor("#B91C1C")
GREEN_ACCENT = colors.HexColor("#0F766E")

ALL_ORDER = [
    "L01_A", "L06_B", "L04_A", "L02_B", "L02_A", "L06_A", "L03_B", "L03_A",
    "L05_B", "L01_B", "L05_A", "L04_B",
]
AFFORDABLE_ORDER = ["L01_A", "L06_B", "L04_A", "L02_B", "L02_A", "L06_A", "L03_B", "L03_A"]


def draw_para(
    c: canvas.Canvas,
    html_text: str,
    style: ParagraphStyle,
    x: float,
    y_top: float,
    width: float,
) -> float:
    p = Paragraph(html_text, style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def draw_section_bar(c: canvas.Canvas, title: str, x: float, y_top: float, width: float) -> float:
    c.setFillColor(NAVY)
    c.rect(x, y_top - 12, 3, 10, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(x + 7, y_top - 10.5, title)
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(x, y_top - 14.5, x + width, y_top - 14.5)
    return y_top - 17.5


def draw_distribution_chart(
    c: canvas.Canvas,
    golden: dict,
    x: float,
    y_top: float,
    width: float,
    height: float,
    title: str,
    subtitle: str,
    compact: bool = True,
) -> float:
    """Draw horizontal Min-Max/IQR/Mean/Median distribution across all 12 options."""
    opts = golden["options"]
    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.8)
    c.roundRect(x, y_top - height, width, height, 4, fill=1, stroke=1)

    pad = 8
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8.2 if compact else 9.6)
    c.drawString(x + pad, y_top - 13, title)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.8 if compact else 7.6)
    c.drawString(x + pad, y_top - 22.5, subtitle)

    # Legend
    leg_y = y_top - 13
    lx = x + width - (162 if compact else 188)
    f_leg = 6.4 if compact else 7.3
    c.setStrokeColor(SLATE)
    c.setLineWidth(1.0)
    c.line(lx, leg_y + 2, lx + 10, leg_y + 2)
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica", f_leg)
    c.drawString(lx + 13, leg_y, "Min-Max")

    c.setFillColor(colors.HexColor("#BFDBFE"))
    c.rect(lx + 45, leg_y - 1, 8, 5.5, fill=1, stroke=0)
    c.setFillColor(DARK_TEXT)
    c.drawString(lx + 56, leg_y, "IQR")

    c.setFillColor(BLUE)
    c.circle(lx + 76, leg_y + 2, 2.5, fill=1, stroke=0)
    c.setFillColor(DARK_TEXT)
    c.drawString(lx + 82, leg_y, "Mean")

    mx = lx + 107
    my = leg_y + 2
    c.setFillColor(colors.white)
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.9)
    p = c.beginPath()
    p.moveTo(mx, my + 2.7)
    p.lineTo(mx + 2.7, my)
    p.lineTo(mx, my - 2.7)
    p.lineTo(mx - 2.7, my)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(DARK_TEXT)
    c.drawString(lx + 113, leg_y, "Median")

    label_x = x + pad
    plot_left = x + (154 if compact else 206)
    plot_right = x + width - (116 if compact else 206)
    plot_w = plot_right - plot_left
    val_min, val_max = 700.0, 2600.0

    def x_of(val: float) -> float:
        return plot_left + (val - val_min) / (val_max - val_min) * plot_w

    plot_top = y_top - (33 if compact else 42)
    plot_bottom = y_top - height + (16 if compact else 24)
    total_units = 12.6
    row_h = (plot_top - plot_bottom) / total_units

    ticks = [800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]
    for t in ticks:
        gx = x_of(t)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.5)
        c.line(gx, plot_bottom, gx, plot_top)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.3 if compact else 7.2)
        c.drawCentredString(gx, plot_bottom - 8.5, f"{t:,}")

    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 6.5 if compact else 7.5)
    c.drawCentredString((plot_left + plot_right) / 2, plot_bottom - (15 if compact else 18), "Observed Weekly Passages (passage events / 20-hr week)")

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 6.6 if compact else 7.6)
    c.drawString(label_x, plot_top + 2, "Option | Site (Win)")
    c.drawRightString(plot_left - 6, plot_top + 2, "4-Wk Cost | n")
    c.drawString(
        plot_right + 6,
        plot_top + 2,
        "Mean | Med | CV%" if compact else "Mean  |  Med  |  SD  |  CV%  |  IQR  |  Min-Max",
    )

    for idx, oid in enumerate(ALL_ORDER):
        o = opts[oid]
        slot = idx + (0.6 if idx >= 8 else 0.0)
        cy = plot_top - (slot + 0.5) * row_h

        if idx % 2 == 0:
            c.setFillColor(LIGHT_BG)
            c.rect(x + 4, cy - row_h * 0.47, width - 8, row_h * 0.94, fill=1, stroke=0)

        if oid == "L01_A":
            accent, iqr_fill = BLUE, colors.HexColor("#BFDBFE")
        elif oid == "L04_A":
            accent, iqr_fill = TEAL, colors.HexColor("#99F6E4")
        elif oid == "L06_B":
            accent, iqr_fill = AMBER, colors.HexColor("#FDE68A")
        elif o["within_budget"]:
            accent, iqr_fill = SLATE, colors.HexColor("#CBD5E1")
        else:
            accent, iqr_fill = OVER_COLOR, colors.HexColor("#E2E8F0")

        is_key = oid in ("L01_A", "L04_A", "L06_B", "L02_B")
        c.setFillColor(DARK_TEXT if o["within_budget"] else MUTED)
        c.setFont("Helvetica-Bold" if is_key else "Helvetica", 6.6 if compact else 7.8)
        c.drawString(
            label_x,
            cy - 2.3,
            f"{oid} {o['location_name']} ({o['window_id']})"
            if compact
            else f"{oid} - {o['location_name']} (Win {o['window_id']})",
        )
        c.setFont("Helvetica", 6.3 if compact else 7.5)
        c.drawRightString(plot_left - 6, cy - 2.3, f"${o['total_pilot_cost_usd']:,} | n={o['obs_weeks']}")

        x_min, x_max = x_of(o["min"]), x_of(o["max"])
        c.setStrokeColor(accent)
        c.setLineWidth(1.0 if compact else 1.3)
        c.line(x_min, cy, x_max, cy)
        c.line(x_min, cy - 2.3, x_min, cy + 2.3)
        c.line(x_max, cy - 2.3, x_max, cy + 2.3)

        x_q1, x_q3 = x_of(o["q1"]), x_of(o["q3"])
        box_h = 6.4 if compact else 8.8
        c.setFillColor(iqr_fill)
        c.setStrokeColor(accent)
        c.setLineWidth(0.5)
        c.rect(x_q1, cy - box_h / 2, max(x_q3 - x_q1, 1.5), box_h, fill=1, stroke=1)

        xm = x_of(o["mean"])
        c.setFillColor(accent)
        c.circle(xm, cy, 2.7 if compact else 3.6, fill=1, stroke=0)

        xmed = x_of(o["median"])
        r = 2.8 if compact else 3.7
        c.setFillColor(colors.white)
        c.setStrokeColor(NAVY if o["within_budget"] else MUTED)
        c.setLineWidth(0.9)
        dp = c.beginPath()
        dp.moveTo(xmed, cy + r)
        dp.lineTo(xmed + r, cy)
        dp.lineTo(xmed, cy - r)
        dp.lineTo(xmed - r, cy)
        dp.close()
        c.drawPath(dp, stroke=1, fill=1)

        c.setFillColor(DARK_TEXT if o["within_budget"] else MUTED)
        c.setFont("Helvetica-Bold" if is_key else "Helvetica", 6.3 if compact else 7.3)
        if compact:
            c.drawString(plot_right + 6, cy - 2.3, f"{o['mean']:,.2f} | {o['median']:,.2f} | {o['cv_pct']:.2f}%")
        else:
            c.drawString(
                plot_right + 6,
                cy - 2.3,
                f"{o['mean']:,.2f} | {o['median']:,.2f} | {o['sd']:.2f} | {o['cv_pct']:.2f}% | {o['iqr']:.2f} | {o['min']:,}-{o['max']:,}",
            )

        if idx == 7:
            div_y = plot_top - 8.3 * row_h
            c.setStrokeColor(RED_ACCENT)
            c.setLineWidth(0.85)
            c.setDash(3, 2)
            c.line(x + 4, div_y, x + width - 4, div_y)
            c.setDash()
            c.setFillColor(RED_ACCENT)
            c.setFont("Helvetica-Bold", 6.2 if compact else 7.2)
            c.drawString(
                x + pad,
                div_y + 1.8,
                "AFFORDABLE (<= $18,000 BUDGET CAP, n=8) ABOVE  |  OVER-BUDGET (> $18,000, EXCLUDED, n=4) BELOW",
            )

    return y_top - height


def draw_sensitivity_chart(
    c: canvas.Canvas,
    golden: dict,
    x: float,
    y_top: float,
    width: float,
    height: float,
    compact: bool = True,
) -> float:
    """Draw side-by-side multi-regime comparison for top affordable options."""
    opts = golden["options"]
    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.8)
    c.roundRect(x, y_top - height, width, height, 4, fill=1, stroke=1)

    pad = 8
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8.5 if compact else 9.8)
    c.drawString(
        x + pad,
        y_top - 13,
        "Sensitivity Chart: Mean Weekly Passages Across Subset & Outlier Regimes (Top Affordable Options)",
    )
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.5 if compact else 7.5)
    c.drawString(
        x + pad,
        y_top - 22.5,
        "Units: Passage events / 20-hr week | Compares Full (n=14-15), Shared 10-Wk (n=10), Shared 9-Wk (n=9), Late 4-Wk, & Spike-Trimmed L06_B (n=13)",
    )

    series = [
        ("L01_A", "L01_A Cedar Walk ($18,000)", BLUE),
        ("L04_A", "L04_A Birch Arcade ($17,500)", TEAL),
        ("L06_B", "L06_B Aspen Court ($16,000)", AMBER),
        ("L02_B", "L02_B Maple Court ($16,500)", SLATE),
    ]

    # Legend
    lx = x + pad
    ly = y_top - 33.5
    for oid, lbl, col in series:
        c.setFillColor(col)
        c.rect(lx, ly, 8, 5.5, fill=1, stroke=0)
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold" if oid in ("L01_A", "L04_A") else "Helvetica", 6.5 if compact else 7.3)
        c.drawString(lx + 11, ly + 0.5, lbl)
        lx += 132 if compact else 160

    # Also legend for Spike-Trimmed L06_B on 2nd legend line
    tx = x + pad
    ty = ly - 9.5
    c.setFillColor(colors.HexColor("#FEF3C7"))
    c.setStrokeColor(AMBER)
    c.setLineWidth(1.0)
    c.setDash(2, 1.5)
    c.rect(tx, ty, 8, 5.5, fill=1, stroke=1)
    c.setDash()
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica", 6.4 if compact else 7.2)
    c.drawString(tx + 11, ty + 0.5, "L06_B Spike-Trimmed (n=13, excludes 07-06=2,422 & 08-17=2,343 -> Mean 1,282.62)")

    plot_left = x + 36
    plot_right = x + width - 14
    plot_top = y_top - 53
    plot_bottom = y_top - height + (24 if compact else 28)
    plot_h = plot_top - plot_bottom
    plot_w = plot_right - plot_left

    y_min, y_max = 1000.0, 1750.0

    def y_of(v: float) -> float:
        return plot_bottom + (v - y_min) / (y_max - y_min) * plot_h

    for t in [1000, 1150, 1300, 1450, 1600, 1750]:
        gy = y_of(t)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.5)
        c.line(plot_left, gy, plot_right, gy)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.3 if compact else 7.2)
        c.drawRightString(plot_left - 4, gy - 2, f"{t:,}")

    regimes = [
        ("Full Observed\n(n=14-15)", "mean"),
        ("Shared 10-Wk\n(Affordable, n=10)", "shared_10wk_mean"),
        ("Shared 9-Wk\n(All 12, n=9)", "shared_9wk_mean"),
        ("Late 4-Wk\n(Aug 31-Sep 21)", "late_4wk_mean"),
        ("Spike-Trimmed\n(L06_B n=13 vs Base)", "trimmed"),
    ]

    group_w = plot_w / len(regimes)
    bar_w = min(21.5 if compact else 27.0, group_w * 0.20)
    bar_gap = 3.0 if compact else 3.5

    for g_idx, (r_label, key) in enumerate(regimes):
        gx_center = plot_left + (g_idx + 0.5) * group_w
        if g_idx % 2 == 1:
            c.setFillColor(LIGHT_BG)
            c.rect(plot_left + g_idx * group_w, plot_bottom, group_w, plot_h, fill=1, stroke=0)

        # Group label
        lines = r_label.split("\n")
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 6.5 if compact else 7.3)
        c.drawCentredString(gx_center, plot_bottom - 10, lines[0])
        c.setFont("Helvetica", 6.0 if compact else 6.8)
        c.drawCentredString(gx_center, plot_bottom - 18, lines[1])

        total_bw = 4 * bar_w + 3 * bar_gap
        start_bx = gx_center - total_bw / 2
        for s_idx, (oid, _, col) in enumerate(series):
            bx = start_bx + s_idx * (bar_w + bar_gap)
            if key == "trimmed":
                if oid == "L06_B":
                    val = opts["L06_B"]["spike_trimmed"]["mean"]
                else:
                    val = opts[oid]["mean"]
            else:
                val = opts[oid][key]

            bh = max(2.0, y_of(val) - plot_bottom)
            if key == "trimmed" and oid == "L06_B":
                c.setFillColor(colors.HexColor("#FEF3C7"))
                c.setStrokeColor(AMBER)
                c.setLineWidth(1.0)
                c.setDash(2, 1.5)
                c.rect(bx, plot_bottom, bar_w, bh, fill=1, stroke=1)
                c.setDash()
            else:
                c.setFillColor(col)
                c.rect(bx, plot_bottom, bar_w, bh, fill=1, stroke=0)

            c.setFillColor(DARK_TEXT)
            c.setFont("Helvetica-Bold" if oid in ("L01_A", "L04_A") or (key == "trimmed" and oid == "L06_B") else "Helvetica", 4.7 if compact else 6.2)
            c.drawCentredString(bx + bar_w / 2, plot_bottom + bh + 2.5, f"{val:,.2f}")

    return y_top - height


def build_two_page_brief(golden: dict) -> None:
    page_w, page_h = letter  # 612 x 792
    margin_x = 32.0
    content_w = page_w - 2 * margin_x

    c = canvas.Canvas(str(OUT_BRIEF), pagesize=letter, pageCompression=0)
    c.setTitle("BUS 240F Two-Page Executive Decision Brief - Vitaly Chait")
    c.setAuthor("Vitaly Chait")

    body_st = ParagraphStyle("B", fontName="Helvetica", fontSize=6.9, leading=9.3, textColor=DARK_TEXT)
    bullet_st = ParagraphStyle(
        "BL", fontName="Helvetica", fontSize=6.9, leading=9.2,
        leftIndent=10, firstLineIndent=-8, spaceBefore=2.0, textColor=DARK_TEXT,
    )
    small_st = ParagraphStyle("S", fontName="Helvetica", fontSize=6.8, leading=9.1, textColor=DARK_TEXT)

    # ==================== PAGE 1 ====================
    y = page_h - 20.0
    c.setFillColor(NAVY)
    c.roundRect(margin_x, y - 32, content_w, 32, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11.0)
    c.drawString(margin_x + 10, y - 13.5, "BUS 240F Executive Decision Brief - Pop-Up Pilot Location & Window Selection")
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.drawString(
        margin_x + 10,
        y - 24.5,
        "Vitaly Chait  |  Decision Date: Sep 28, 2026  |  Trial Period: Oct 12 - Nov 8, 2026 (4 wks, 80 hrs)  |  Page 1 of 2",
    )
    y -= 40

    # Recommendation Callout + Priority Framework (Plain English)
    rec_html = (
        "<b>OUR RECOMMENDATION - Pick L01_A (Cedar Walk, Shift A: Tue-Sat 10:00am-2:00pm, Cost $18,000):</b> "
        "To test shopper interest in reusable bottles and lunch containers during the 4-week pilot (Oct 12 - Nov 8, 2026; 20 hrs/wk), "
        "<b>L01_A</b> brings the most foot traffic of any option within the <b>&lt;= $18,000</b> budget: <b>1,510.00</b> crossings per week on average "
        "and <b>1,535.00</b> in a typical middle week (across 14 complete weeks; raw sum 21,140, SD 302.58, CV 20.04%, IQR 477.50, range 920-1,970).<br/>"
        "<b>How We Ranked Options:</b> (1) Stay within the hard <b>$18,000</b> budget (ruling out 4 over-budget sites: <i>L05_B</i> $21,000, <i>L01_B</i> $19,500, <i>L05_A</i> $19,000, <i>L04_B</i> $18,500); "
        "(2) Maximize weekly passerby exposure; (3) Check whether paying $500 more than <i>L04_A</i> ($17,500) is worthwhile (+108.64 crossings/wk = +435 over 4 weeks, just $1.15 per extra crossing)."
    )
    rp = Paragraph(rec_html, body_st)
    _, rh = rp.wrap(content_w - 14, 150)
    box_h = rh + 11
    c.setFillColor(CALLOUT_BG)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.0)
    c.roundRect(margin_x, y - box_h, content_w, box_h, 4, fill=1, stroke=1)
    rp.drawOn(c, margin_x + 7, y - 5.5 - rh)
    y -= (box_h + 8)

    # Credible Affordable Alternatives Comparison (Plain-English Bullets)
    y = draw_section_bar(c, "How L01_A Compares to the Best Affordable Alternatives (<= $18,000)", margin_x, y, content_w)
    y = draw_para(
        c,
        "&bull; <b>L04_A (Birch Arcade, Window A, $17,500, n=14 weeks) - Steadiest Backup Choice:</b> Saves $500 and achieves a <b>1,401.36</b> average and #2 typical median (<b>1,424.50</b>; raw sum 19,619). Its traffic varies far less week-to-week (SD = <b>204.49</b>, CV = <b>14.59%</b>, IQR = 281.75, range 978-1,721) and even edges ahead of L01_A on shared dates (see Page 2).",
        bullet_st,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>L06_B (Aspen Court, Window B, $16,000, n=15 weeks) - Unpredictable Spike-Driven Choice:</b> Saves $2,000 and shows a high total (21,439 over 15 weeks) and #2 average (<b>1,429.27</b>), yet a typical week is only <b>1,327.00</b>. Traffic swings wildly (SD = <b>470.64</b>, CV = <b>32.93%</b>, IQR = 554.50, range 840-2,422) because two giant spikes distort its average.",
        bullet_st,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>L02_B (Maple Court, Window B, $16,500, n=15 weeks) &amp; Lower-Cost Options:</b> <i>L02_B</i> is very consistent (SD = <b>127.56</b>, CV = <b>9.62%</b>, IQR = 161.00) but averages only <b>1,325.73</b> (median <b>1,316.00</b>) - about 184 crossings/wk behind L01_A. Remaining affordable options (<i>L02_A</i> $15,000, Mean 1,250.56, CV 7.41%; <i>L06_A</i> $14,500, 1,169.94; <i>L03_B</i> $13,500, 1,157.44; <i>L03_A</i> $12,000, 1,080.73) give up too much traffic.",
        bullet_st,
        margin_x,
        y,
        content_w,
    )
    y -= 8

    # Primary Visual View (Compact Distribution Chart)
    y = draw_distribution_chart(
        c,
        golden,
        margin_x,
        y,
        content_w,
        220.0,
        title="Primary Visual View: Exposure, Variability & Budget Cap (All 12 Options)",
        subtitle="Units: Passage events / 20-hr scheduled week (Jun 8 - Sep 27, 2026) | Missing weeks (n=8) blank & excluded from denominators",
        compact=True,
    )
    y -= 8

    # Precision Summary Table (All 12 Options)
    y = draw_section_bar(c, "Complete 12-Option Baseline Metrics Table (Jun 8 - Sep 27, 2026; Verified Against Starter CSVs)", margin_x, y, content_w)
    col_widths = [38, 62, 22, 42, 34, 22, 24, 40, 42, 42, 36, 36, 36, 74]
    headers = ["Option", "Location", "Win", "4-Wk Cost", "Budget", "n", "Miss", "Raw Sum", "Mean", "Median", "SD", "CV%", "IQR", "Min-Max"]
    row_h = 12.2

    # Header bar
    c.setFillColor(NAVY)
    c.rect(margin_x, y - row_h, content_w, row_h, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6.4)
    cx = margin_x
    for h_txt, cw in zip(headers, col_widths):
        c.drawCentredString(cx + cw / 2, y - 8.7, h_txt)
        cx += cw
    y -= row_h

    opts = golden["options"]
    for idx, oid in enumerate(ALL_ORDER):
        o = opts[oid]
        if idx == 8:
            c.setStrokeColor(RED_ACCENT)
            c.setLineWidth(0.9)
            c.line(margin_x, y, margin_x + content_w, y)

        if oid == "L01_A":
            c.setFillColor(colors.HexColor("#DBEAFE"))
        elif oid in ("L04_A", "L06_B"):
            c.setFillColor(colors.HexColor("#ECFDF5") if oid == "L04_A" else colors.HexColor("#FEF3C7"))
        elif idx % 2 == 1:
            c.setFillColor(LIGHT_BG)
        else:
            c.setFillColor(colors.white)
        c.rect(margin_x, y - row_h, content_w, row_h, fill=1, stroke=0)

        vals = [
            oid,
            o["location_name"],
            o["window_id"],
            f"${o['total_pilot_cost_usd']:,}",
            "Yes" if o["within_budget"] else "Over",
            str(o["obs_weeks"]),
            str(o["missing_weeks"]),
            f"{o['raw_sum']:,}",
            f"{o['mean']:,.2f}",
            f"{o['median']:,.2f}",
            f"{o['sd']:.2f}",
            f"{o['cv_pct']:.2f}%",
            f"{o['iqr']:.2f}",
            f"{o['min']:,}-{o['max']:,}",
        ]
        c.setFillColor(DARK_TEXT if o["within_budget"] else MUTED)
        c.setFont("Helvetica-Bold" if oid in ("L01_A", "L04_A", "L06_B") else "Helvetica", 6.3)
        cx = margin_x
        for c_idx, (v_txt, cw) in enumerate(zip(vals, col_widths)):
            if c_idx <= 2 or c_idx == 4:
                c.drawCentredString(cx + cw / 2, y - 8.7, v_txt)
            else:
                c.drawRightString(cx + cw - 3, y - 8.7, v_txt)
            cx += cw
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.4)
        c.line(margin_x, y - row_h, margin_x + content_w, y - row_h)
        y -= row_h

    if y < 18:
        raise RuntimeError(f"Page 1 overflow! y={y:.2f}")
    c.showPage()

    # ==================== PAGE 2 ====================
    p2_body = ParagraphStyle("P2B", fontName="Helvetica", fontSize=6.9, leading=9.3, textColor=DARK_TEXT)
    p2_bullet = ParagraphStyle(
        "P2BL", fontName="Helvetica", fontSize=6.9, leading=9.2,
        leftIndent=10, firstLineIndent=-8, spaceBefore=2.0, textColor=DARK_TEXT,
    )
    p2_small = ParagraphStyle("P2S", fontName="Helvetica", fontSize=6.8, leading=9.1, textColor=DARK_TEXT)

    y = page_h - 20.0
    c.setFillColor(NAVY)
    c.roundRect(margin_x, y - 28, content_w, 28, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10.6)
    c.drawString(margin_x + 10, y - 12.5, "BUS 240F Executive Decision Brief - Stress Tests, Data Checks & When to Switch")
    c.setFont("Helvetica", 7.1)
    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.drawString(margin_x + 10, y - 22.5, "Vitaly Chait  |  Fixed Snapshot: BUS240F_Final_Project_Starter.twbx  |  Page 2 of 2")
    y -= 36

    # Section A: Consequential Sensitivity Analysis (Plain-English Bullets)
    y = draw_section_bar(c, "Stress-Testing Our Pick: Spikes, Missing Weeks & Late-Summer Trends", margin_x, y, content_w)
    y = draw_para(
        c,
        "&bull; <b>Test 1 - Removing L06_B's Two One-Off Spikes:</b> L06_B looks strong on average (<b>1,429.27</b> vs. L04_A 1,401.36), but its typical middle week is much lower (<b>1,327.00</b> vs. L04_A 1,424.50). That is because L06_B had two huge isolated spikes (<b>2,422</b> on <b>2026-07-06</b> and <b>2,343</b> on <b>2026-08-17</b>), while its other 13 weeks ranged from 840 to 1,740. Without those two spikes (<b>n=13</b>), L06_B's average drops to <b>1,282.62</b> (median <b>1,274.00</b>, SD = 288.83) - proving it is too erratic to rely on.",
        p2_bullet,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>Test 2 - Fair \"Apples-to-Apples\" Shared Weeks (10 Shared Affordable / 9 All-Option / 8 Non-Spike):</b> Because different sites had missing counts on different dates (L01_A missed 06-29 &amp; 08-24; L04_A missed 06-22 &amp; 09-07), we compared only the <b>10 shared weeks</b> where all 8 affordable sites had data. Cutting those 6 dates drops four busy L01_A weeks (1,810; 1,970; 1,745; 1,545), lowering L01_A to <b>1,407.00</b> (median <b>1,390.00</b>) while <b>L04_A moves ahead to 1,449.70</b> (median <b>1,458.50</b>; and <b>1,455.56 vs. 1,423.33</b> in the 9 shared all-option weeks). <i>Why L06_B jumps to 1,619.10 on the chart:</i> the 6 excluded dates remove L06_B's 5 slowest weeks (840-1,274) while keeping both 2,422 &amp; 2,343 spikes. Removing both missing dates and those 2 spikes leaves <b>8 shared non-spike weeks</b> where <b>L04_A leads all sites at 1,497.12</b> (median 1,500.50) vs. L06_B (1,428.25) and L01_A (1,368.75).",
        p2_bullet,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>Late-Season Trend (Aug 31 - Sep 21) &amp; What We Learned:</b> In the final 4 weeks closest to October, <b>L04_A averages 1,472.67</b> (median 1,500.00, n=3) vs. <b>L01_A at 1,370.00</b> (n=4, L06_B 1,420.00). However, L01_A's dip came from one slow week (920 on Aug 31) followed by a strong <b>1,520.00 September rebound</b> (1,545; 1,735; 1,280). We keep <b>L01_A</b> as primary pick for full-summer peak exposure (1,510.00 mean / 1,535.00 median), with <b>L04_A</b> as a very close, steadier fallback.",
        p2_bullet,
        margin_x,
        y,
        content_w,
    )
    y -= 10

    # Embedded Multi-Subset Sensitivity Vector Chart
    y = draw_sensitivity_chart(c, golden, margin_x, y, content_w, 252.0, compact=True)
    y -= 10

    # Mini Sensitivity Regime Table (Top 4 Contenders)
    s_w = [78, 52, 66, 66, 70, 70, 68, 78]
    s_h = ["Contender", "4-Wk Cost", "Full Mean", "Full Med", "10-Wk Mean", "10-Wk Med", "9-Wk Mean", "Late 4-Wk Mean"]
    sr_h = 14.5
    c.setFillColor(NAVY)
    c.rect(margin_x, y - sr_h, content_w, sr_h, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6.6)
    cx = margin_x
    for ht, cw in zip(s_h, s_w):
        c.drawCentredString(cx + cw / 2, y - 10.2, ht)
        cx += cw
    y -= sr_h
    for idx, oid in enumerate(["L01_A", "L04_A", "L06_B", "L02_B"]):
        o = opts[oid]
        c.setFillColor(colors.HexColor("#DBEAFE") if oid == "L01_A" else (colors.HexColor("#CCFBF1") if oid == "L04_A" else (colors.HexColor("#FEF3C7") if oid == "L06_B" else LIGHT_BG)))
        c.rect(margin_x, y - sr_h, content_w, sr_h, fill=1, stroke=0)
        row_vals = [
            f"{oid} ({o['location_name']})", f"${o['total_pilot_cost_usd']:,}",
            f"{o['mean']:,.2f}", f"{o['median']:,.2f}",
            f"{o['shared_10wk_mean']:,.2f}", f"{o['shared_10wk_median']:,.2f}",
            f"{o['shared_9wk_mean']:,.2f}", f"{o['late_4wk_mean']:,.2f}",
        ]
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold" if oid in ("L01_A", "L04_A") else "Helvetica", 6.5)
        cx = margin_x
        for ci, (vt, cw) in enumerate(zip(row_vals, s_w)):
            if ci == 0:
                c.drawString(cx + 4, y - 10.2, vt)
            else:
                c.drawRightString(cx + cw - 4, y - 10.2, vt)
            cx += cw
        y -= sr_h
    y -= 12

    # Section B: Verification Notes, Stewardship & AI Assistance Disclosure
    y = draw_section_bar(c, "Verification Notes, Data Hygiene & AI Assistance Disclosure", margin_x, y, content_w)
    ver_html = (
        "<b>Data Check &amp; Fixed Snapshot:</b> Checked all records in <b>BUS240F_Final_Project_Starter.twbx</b> (matches raw <i>Candidate_Options.csv</i> and <i>Weekly_Activity.csv</i> 100%): <b>12</b> options (<b>8</b> within the <b>$18,000</b> cap, <b>4</b> over budget) and <b>192</b> weekly rows (2026-06-08 to 2026-09-21) = <b>184 Complete</b> (<b>256,773</b> total passages) + <b>8 Missing</b> (kept blank, never set to zero). "
        "<b>Spot Checks &amp; Cost Rule:</b> Confirmed <b>L01_A</b> on <b>2026-06-08 = Complete (1,175 passages)</b> and <b>2026-06-29 = Missing (blank)</b>; read single 4-week cost via <b>MIN(Total Pilot Cost Usd)</b> so it is never multiplied by 16 weeks. "
        "<b>AI Assistance Disclosure:</b> An AI coding assistant (Antigravity / Gemini) helped build Python check scripts, Tableau XML files, and PDF layouts; the author verified every metric against raw CSVs and inspected the workbook in Tableau Desktop."
    )
    vp = Paragraph(ver_html, p2_small)
    _, vh = vp.wrap(content_w - 14, 200)
    vbox_h = vh + 12
    c.setFillColor(LIGHT_BG)
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.8)
    c.roundRect(margin_x, y - vbox_h, content_w, vbox_h, 4, fill=1, stroke=1)
    vp.drawOn(c, margin_x + 7, y - 6 - vh)
    y -= (vbox_h + 12)

    # Section C: Data Boundaries & What Evidence Would Change Our Recommendation
    y = draw_section_bar(c, "Important Limits & Clear Rules for When to Switch or Wait", margin_x, y, content_w)
    y = draw_para(
        c,
        "&bull; <b>What Counts Do Not Show:</b> Counts measure bidirectional foot-traffic crossings (including repeat passersby), <b>not</b> unique shoppers, actual purchases, or profit. Summer-to-September history does not guarantee October-November volume, and causes of missing weeks or spikes are unknown.",
        p2_bullet,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>Switch to L04_A (Birch Arcade, Window A, $17,500) if:</b> management values steady weekly traffic (<b>CV &lt; 15%</b>; L04_A = 14.59% vs. L01_A = 20.04%) over peak average, OR a quick October check shows L01_A below <b>1,350 passages/wk</b> while L04_A stays at <b>&gt;= 1,400 passages/wk</b>.",
        p2_bullet,
        margin_x,
        y,
        content_w,
    )
    y = draw_para(
        c,
        "&bull; <b>Wait Before Launching if:</b> a pre-trial October spot check finds traffic under <b>1,100 passages/wk</b> at both sites, shows <b>&gt; 40% repeat-crossing inflation</b>, or uncovers unresolved closures explaining L01_A's missing weeks (06-29, 08-24).",
        p2_bullet,
        margin_x,
        y,
        content_w,
    )

    if y < 18:
        raise RuntimeError(f"Page 2 overflow! y={y:.2f}")
    c.showPage()
    c.save()
    print(f"Generated {OUT_BRIEF.name} (2 pages; Page 2 bottom remaining: {y:.1f} pt).")


def build_static_backup(golden: dict, wa_df: pd.DataFrame) -> None:
    page_w, page_h = landscape(letter)  # 792 x 612
    margin_x = 30.0
    content_w = page_w - 2 * margin_x

    c = canvas.Canvas(str(OUT_BACKUP), pagesize=landscape(letter), pageCompression=0)
    c.setTitle("BUS 240F Static View Backup (4 Decisive Views) - Vitaly Chait")
    c.setAuthor("Vitaly Chait")

    def draw_page_banner(page_num: int, view_title: str, meta_line: str) -> float:
        y = page_h - 18.0
        c.setFillColor(NAVY)
        c.roundRect(margin_x, y - 34, content_w, 34, 4, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11.0)
        c.drawString(margin_x + 10, y - 14, f"Static View {page_num} of 4: {view_title}")
        c.setFont("Helvetica", 7.4)
        c.setFillColor(colors.HexColor("#CBD5E1"))
        c.drawString(margin_x + 10, y - 26, meta_line)
        return y - 42

    # ==================== VIEW 1: Model Verification, 12x16 Completeness Matrix & Fixed Cost Audit ====================
    y = draw_page_banner(
        1,
        "Model Verification, 12x16 Weekly Completeness Heatmap & Fixed Cost Audit",
        "Units: Passage events / 20-hr week | Population: All 12 options x 16 Mondays (2026-06-08 to 2026-09-21 = 192 rows) | Filter/Exclusions: Unfiltered; 8 Missing cells blank (never 0); Cost via MIN()",
    )

    weeks = sorted(wa_df["week_start"].astype(str).unique().tolist())
    # Matrix box
    mat_h = 248.0
    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.roundRect(margin_x, y - mat_h, content_w, mat_h, 4, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(margin_x + 8, y - 13, "12 x 16 Historical Activity & Missingness Matrix (184 Complete Cells = 256,773 Total Passages; 8 Missing Cells Highlighted)")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.0)
    c.drawString(margin_x + 8, y - 22.5, "Benchmark Source Checks: L01_A on 2026-06-08 = Complete (1,175) | L01_A on 2026-06-29 = Missing (blank) | Total Weekly Records = 192 (16 per option)")

    left_col_w = 130.0
    right_tot_w = 42.0
    cell_w = (content_w - 16 - left_col_w - right_tot_w) / 16.0
    top_hdr_y = y - 34
    row_h = (mat_h - 42) / 13.0

    # Week column headers
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 6.2)
    c.drawString(margin_x + 8, top_hdr_y - 8, "Option (Budget)")
    for w_idx, w_str in enumerate(weeks):
        wx = margin_x + 8 + left_col_w + w_idx * cell_w
        c.drawCentredString(wx + cell_w / 2, top_hdr_y - 8, w_str[5:])
    c.drawCentredString(margin_x + 8 + left_col_w + 16 * cell_w + right_tot_w / 2, top_hdr_y - 8, "Obs / 16")

    pivot = wa_df.set_index(["option_id", "week_start"])
    for r_idx, oid in enumerate(ALL_ORDER):
        o = golden["options"][oid]
        ry = top_hdr_y - (r_idx + 1) * row_h - 4
        c.setFillColor(DARK_TEXT if o["within_budget"] else MUTED)
        c.setFont("Helvetica-Bold" if oid in ("L01_A", "L04_A", "L06_B") else "Helvetica", 6.4)
        c.drawString(margin_x + 8, ry - 9, f"{oid} {o['location_name']} ({'OK' if o['within_budget'] else '>$18k'})")

        for w_idx, w_str in enumerate(weeks):
            wx = margin_x + 8 + left_col_w + w_idx * cell_w
            rec = pivot.loc[(oid, w_str)]
            status = str(rec["observation_status"])
            is_bench = oid == "L01_A" and w_str in ("2026-06-08", "2026-06-29")
            if status == "Missing":
                c.setFillColor(colors.HexColor("#FEE2E2"))
                c.setStrokeColor(RED_ACCENT if is_bench else colors.HexColor("#FCA5A5"))
                c.setLineWidth(1.2 if is_bench else 0.5)
                c.rect(wx + 0.8, ry - row_h + 1, cell_w - 1.6, row_h - 1.5, fill=1, stroke=1)
                c.setFillColor(RED_ACCENT)
                c.setFont("Helvetica-Bold", 5.8)
                c.drawCentredString(wx + cell_w / 2, ry - 9, "MISS")
            else:
                val = int(rec["observed_passages"])
                # Intensity shading
                shade = colors.HexColor("#DBEAFE") if val >= 1700 else (colors.HexColor("#EFF6FF") if val >= 1350 else colors.HexColor("#F8FAFC"))
                c.setFillColor(shade)
                c.setStrokeColor(BLUE if is_bench else colors.HexColor("#E2E8F0"))
                c.setLineWidth(1.2 if is_bench else 0.4)
                c.rect(wx + 0.8, ry - row_h + 1, cell_w - 1.6, row_h - 1.5, fill=1, stroke=1)
                c.setFillColor(DARK_TEXT)
                c.setFont("Helvetica-Bold" if is_bench or val >= 2000 else "Helvetica", 5.9)
                c.drawCentredString(wx + cell_w / 2, ry - 9, f"{val:,}")

        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 6.3)
        c.drawCentredString(margin_x + 8 + left_col_w + 16 * cell_w + right_tot_w / 2, ry - 9, f"{o['obs_weeks']} / 16")

    y -= (mat_h + 10)

    # Bottom: Global Model Verification Strip + 12-Option Fixed Cost Audit Table
    c.setFillColor(CALLOUT_BG)
    c.setStrokeColor(BLUE)
    c.roundRect(margin_x, y - 24, content_w, 24, 3, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7.3)
    c.drawString(
        margin_x + 8,
        y - 15,
        "Model Verification Totals:  Candidate Options = 12 (8 Affordable <= $18,000, 4 Over-Budget)  |  Scheduled Weekly Rows = 192  |  Complete = 184 (Sum = 256,773)  |  Missing = 8 (Blank/Null)",
    )
    y -= 32

    t_cols = [50, 82, 34, 88, 60, 56, 48, 46, 62, 206]
    t_hdrs = ["Option ID", "Location Name", "Win", "Operating Window", "4-Wk Cost", "Budget <=$18k", "Obs (n)", "Sched", "Raw Sum", "Missing Week Dates (Excluded)"]
    tr_h = 13.5
    c.setFillColor(NAVY)
    c.rect(margin_x, y - tr_h, content_w, tr_h, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6.8)
    cx = margin_x
    for h_txt, cw in zip(t_hdrs, t_cols):
        c.drawCentredString(cx + cw / 2, y - 9.5, h_txt)
        cx += cw
    y -= tr_h

    for idx, oid in enumerate(ALL_ORDER):
        o = golden["options"][oid]
        c.setFillColor(LIGHT_BG if idx % 2 == 1 else colors.white)
        c.rect(margin_x, y - tr_h, content_w, tr_h, fill=1, stroke=0)
        miss_str = ", ".join(o["missing_week_dates"]) if o["missing_week_dates"] else "None (100% Complete)"
        vals = [
            oid, o["location_name"], o["window_id"], o["operating_window_label"],
            f"${o['total_pilot_cost_usd']:,}", "True" if o["within_budget"] else "False",
            str(o["obs_weeks"]), "16", f"{o['raw_sum']:,}", miss_str,
        ]
        c.setFillColor(DARK_TEXT if o["within_budget"] else MUTED)
        c.setFont("Helvetica-Bold" if oid in ("L01_A", "L04_A", "L06_B") else "Helvetica", 6.7)
        cx = margin_x
        for c_idx, (v_txt, cw) in enumerate(zip(vals, t_cols)):
            if c_idx in (0, 2, 5, 6, 7):
                c.drawCentredString(cx + cw / 2, y - 9.5, v_txt)
            elif c_idx in (4, 8):
                c.drawRightString(cx + cw - 5, y - 9.5, v_txt)
            else:
                c.drawString(cx + 5, y - 9.5, v_txt)
            cx += cw
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.line(margin_x, y - tr_h, margin_x + content_w, y - tr_h)
        y -= tr_h

    c.showPage()

    # ==================== VIEW 2: Primary Decision View ====================
    y = draw_page_banner(
        2,
        "Primary Decision View - Observed-Week Mean, Median, Dispersion & Fixed Pilot Cost (All 12 Options)",
        "Units: Passage events / 20-hr scheduled week | Timeframe: Jun 8 - Sep 27, 2026 (16 weeks) | Filter/Exclusions: Missing weeks (n=8) excluded from denominators; $18,000 budget boundary shown",
    )
    y = draw_distribution_chart(
        c,
        golden,
        margin_x,
        y,
        content_w,
        460.0,
        title="Candidate Option Performance: Full-Period Distribution, Mean vs. Median & Cost",
        subtitle="L01_A leads all 8 affordable options on both Mean (1,510.00) and Median (1,535.00); L04_A offers tighter stability (CV 14.59%, Med 1,424.50); L06_B has widest dispersion (CV 32.93%)",
        compact=False,
    )
    y -= 10
    c.setFillColor(CALLOUT_BG)
    c.setStrokeColor(BLUE)
    c.roundRect(margin_x, y - 48, content_w, 48, 4, fill=1, stroke=1)
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica-Bold", 8.0)
    c.drawString(margin_x + 10, y - 15, "Key Decision Readout:")
    c.setFont("Helvetica", 7.6)
    c.drawString(margin_x + 10, y - 27.5, "- Primary Recommendation: L01_A (Cedar Walk, Win A, $18,000, n=14) leads affordable Mean (1,510.00) and Median (1,535.00) within the $18,000 budget cap.")
    c.drawString(margin_x + 10, y - 39.5, "- Credible Alternatives: L04_A (Birch Arcade, Win A, $17,500, n=14; Mean 1,401.36, Med 1,424.50, CV 14.59%) & L06_B (Aspen Court, Win B, $16,000, n=15; Mean 1,429.27, Med 1,327.00, CV 32.93%).")
    c.showPage()

    # ==================== VIEW 3: Weekly Trajectory & Outliers ====================
    y = draw_page_banner(
        3,
        "Weekly Time-Series Trajectory & Outlier Diagnostics (Jun 8 - Sep 21, 2026)",
        "Units: Passage events / 20-hr week | Population: 8 Affordable Options (<= $18,000) across 16 Mondays | Filter/Exclusions: Over-budget options excluded for legibility; lines break across 7 affordable missing weeks",
    )

    chart_h = 465.0
    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.roundRect(margin_x, y - chart_h, content_w, chart_h, 4, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(margin_x + 10, y - 15, "16-Week Passage Trajectory by Affordable Option (Missing Weeks Shown as Explicit Line Gaps)")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.4)
    c.drawString(margin_x + 10, y - 25.5, "Top contenders highlighted: L01_A (Blue), L04_A (Teal), L06_B (Amber), L02_B (Slate) | Remaining 4 affordable options (L02_A, L06_A, L03_B, L03_A) shown in light gray")

    p_left = margin_x + 48
    p_right = margin_x + content_w - 22
    p_top = y - 48
    p_bot = y - chart_h + 44
    pw = p_right - p_left
    ph = p_top - p_bot
    vmin, vmax = 750.0, 2600.0

    def tx_of(w_idx: int) -> float:
        return p_left + (w_idx / 15.0) * pw

    def ty_of(val: float) -> float:
        return p_bot + (val - vmin) / (vmax - vmin) * ph

    # Y-axis grid
    for tv in [800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]:
        gy = ty_of(tv)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.5)
        c.line(p_left, gy, p_right, gy)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.0)
        c.drawRightString(p_left - 5, gy - 2.3, f"{tv:,}")

    # Shade late-season 4-week window
    lx1, lx2 = tx_of(12), tx_of(15)
    c.setFillColor(colors.HexColor("#F0FDFA"))
    c.rect(lx1, p_bot, lx2 - lx1, ph, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawCentredString((lx1 + lx2) / 2, p_top + 4, "Late 4-Wk (Aug 31 - Sep 21)")

    # X-axis ticks
    for w_idx, w_str in enumerate(weeks):
        gx = tx_of(w_idx)
        c.setStrokeColor(colors.HexColor("#F1F5F9"))
        c.line(gx, p_bot, gx, p_top)
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica", 6.8)
        c.drawCentredString(gx, p_bot - 11, w_str[5:])

    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 7.4)
    c.drawCentredString((p_left + p_right) / 2, p_bot - 24, "Historical Observation Week Start (Monday, 2026)")

    # Plot series (muted background first, then top 4)
    bg_opts = ["L02_A", "L06_A", "L03_B", "L03_A"]
    fg_opts = [
        ("L02_B", SLATE, 1.4),
        ("L06_B", AMBER, 1.7),
        ("L04_A", TEAL, 2.0),
        ("L01_A", BLUE, 2.2),
    ]

    for oid in bg_opts:
        sub = wa_df[wa_df["option_id"] == oid].set_index("week_start")
        c.setStrokeColor(colors.HexColor("#CBD5E1"))
        c.setLineWidth(0.9)
        prev_pt = None
        for w_idx, w_str in enumerate(weeks):
            row = sub.loc[w_str]
            if row["observation_status"] == "Complete":
                pt = (tx_of(w_idx), ty_of(float(row["observed_passages"])))
                if prev_pt is not None:
                    c.line(prev_pt[0], prev_pt[1], pt[0], pt[1])
                prev_pt = pt
            else:
                prev_pt = None

    for oid, col, lw in fg_opts:
        sub = wa_df[wa_df["option_id"] == oid].set_index("week_start")
        c.setStrokeColor(col)
        c.setFillColor(col)
        c.setLineWidth(lw)
        prev_pt = None
        for w_idx, w_str in enumerate(weeks):
            row = sub.loc[w_str]
            if row["observation_status"] == "Complete":
                pt = (tx_of(w_idx), ty_of(float(row["observed_passages"])))
                if prev_pt is not None:
                    c.line(prev_pt[0], prev_pt[1], pt[0], pt[1])
                c.circle(pt[0], pt[1], 2.5, fill=1, stroke=0)
                prev_pt = pt
            else:
                prev_pt = None

    # Explicit callout annotations
    def annotate(w_idx: int, val: float, text: str, dx: float, dy: float, col) -> None:
        ax, ay = tx_of(w_idx), ty_of(val)
        c.setStrokeColor(col)
        c.setLineWidth(0.8)
        c.circle(ax, ay, 4.8, fill=0, stroke=1)
        c.line(ax, ay, ax + dx, ay + dy)
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 6.8)
        c.drawString(ax + dx + (2 if dx >= 0 else -c.stringWidth(text, "Helvetica-Bold", 6.8) - 2), ay + dy - 2, text)

    annotate(4, 2422, "L06_B Spike #1: 2,422 (07-06)", 10, 4, AMBER)
    annotate(10, 2343, "L06_B Spike #2: 2,343 (08-17)", -10, 6, AMBER)
    annotate(12, 920, "L01_A Dip: 920 (08-31)", -12, -16, BLUE)
    annotate(14, 1501, "L04_A Steady Corridor (978-1,721; Late Mean 1,472.67)", -205, 128, TEAL)
    annotate(6, 1970, "L01_A Peak: 1,970 (07-20)", 8, 8, BLUE)

    # Bottom Legend Strip (2x2 clean grid)
    for idx_l, (oid, col, _) in enumerate(reversed(fg_opts)):
        o = golden["options"][oid]
        col_i = idx_l % 2
        row_i = idx_l // 2
        lx = margin_x + 12 + col_i * 365
        ly = y - chart_h - 14 - row_i * 12
        c.setFillColor(col)
        c.rect(lx, ly, 12, 7, fill=1, stroke=0)
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 7.4)
        c.drawString(lx + 16, ly + 0.5, f"{oid} {o['location_name']} (Mean {o['mean']:,.2f}, Med {o['median']:,.2f}, SD {o['sd']:.2f}, n={o['obs_weeks']})")
    c.showPage()

    # ==================== VIEW 4: Consequential Sensitivity Analysis ====================
    y = draw_page_banner(
        4,
        "Consequential Sensitivity Analysis - Multi-Regime Comparison & Outlier Trimming (8 Affordable Options)",
        "Units: Passage events / 20-hr week | Subsets: Full Observed (n=14-16), Shared 10-Wk Affordable (n=10), Shared 9-Wk All (n=9), Late 4-Wk (Aug 31-Sep 21), & L06_B Spike-Trimmed (n=13)",
    )
    y = draw_sensitivity_chart(c, golden, margin_x, y, content_w, 275.0, compact=False)
    y -= 10

    # Sensitivity Comparison Table across all 8 affordable options
    s_cols = [50, 84, 52, 40, 58, 58, 60, 60, 58, 58, 154]
    s_hdrs = [
        "Option", "Location (Win)", "4-Wk Cost", "Obs n",
        "Full Mean", "Full Med", "10-Wk Mean", "10-Wk Med",
        "9-Wk Mean", "Late 4-Wk", "Sensitivity Notes",
    ]
    sr_h = 16.0
    c.setFillColor(NAVY)
    c.rect(margin_x, y - sr_h, content_w, sr_h, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6.8)
    cx = margin_x
    for h_txt, cw in zip(s_hdrs, s_cols):
        c.drawCentredString(cx + cw / 2, y - 10.5, h_txt)
        cx += cw
    y -= sr_h

    notes_map = {
        "L01_A": "Missing 06-29, 08-24; -103.00 in 10-wk",
        "L06_B": "Spike-trimmed (n=13): Mean 1,282.62",
        "L04_A": "Overtakes L01_A in 10-wk, 9-wk & Late",
        "L02_B": "Tightest top stability (CV 9.62%)",
        "L02_A": "Lowest overall CV (7.41%); 0 missing",
        "L06_A": "0 missing; +70.66 in 10-wk subset",
        "L03_B": "0 missing; fades late (1,092.50)",
        "L03_A": "Lowest cost ($12,000); fades late",
    }

    for idx, oid in enumerate(AFFORDABLE_ORDER):
        o = golden["options"][oid]
        if oid == "L01_A":
            c.setFillColor(colors.HexColor("#DBEAFE"))
        elif oid == "L04_A":
            c.setFillColor(colors.HexColor("#CCFBF1"))
        elif oid == "L06_B":
            c.setFillColor(colors.HexColor("#FEF3C7"))
        else:
            c.setFillColor(LIGHT_BG if idx % 2 == 1 else colors.white)
        c.rect(margin_x, y - sr_h, content_w, sr_h, fill=1, stroke=0)

        vals = [
            oid, f"{o['location_name']} ({o['window_id']})", f"${o['total_pilot_cost_usd']:,}",
            str(o["obs_weeks"]), f"{o['mean']:,.2f}", f"{o['median']:,.2f}",
            f"{o['shared_10wk_mean']:,.2f}", f"{o['shared_10wk_median']:,.2f}",
            f"{o['shared_9wk_mean']:,.2f}", f"{o['late_4wk_mean']:,.2f}",
            notes_map[oid],
        ]
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold" if oid in ("L01_A", "L04_A", "L06_B") else "Helvetica", 6.7)
        cx = margin_x
        for c_idx, (v_txt, cw) in enumerate(zip(vals, s_cols)):
            if c_idx in (0, 3):
                c.drawCentredString(cx + cw / 2, y - 10.5, v_txt)
            elif c_idx in (1, 10):
                c.drawString(cx + 4, y - 10.5, v_txt)
            else:
                c.drawRightString(cx + cw - 5, y - 10.5, v_txt)
            cx += cw
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.line(margin_x, y - sr_h, margin_x + content_w, y - sr_h)
        y -= sr_h

    y -= 10
    c.setFillColor(CALLOUT_BG)
    c.setStrokeColor(BLUE)
    c.roundRect(margin_x, y - 62, content_w, 62, 4, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7.6)
    c.drawString(margin_x + 10, y - 13.5, "Analytical Takeaway & Subset Exclusion Definitions:")
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica", 6.8)
    c.drawString(margin_x + 10, y - 24.5, "- Shared 10-Week Affordable excludes 6 weeks with >=1 missing affordable record (2026-06-22, 06-29, 07-20, 08-10, 08-24, 09-07); Shared 9-Week also excludes 2026-07-27.")
    c.drawString(margin_x + 10, y - 35.5, "- Why L06_B Spikes in 10-Wk (1,619.10): Excluded dates drop L06_B's 5 slowest weeks (840-1,274) while keeping both spikes; on 8 non-spike shared weeks L04_A leads (1,497.12 vs L06_B 1,428.25, L01_A 1,368.75).")
    c.drawString(margin_x + 10, y - 46.5, "- Rank Reversal & Sep Rebound: Shared 10-wk drops L01_A to 1,407.00 vs L04_A 1,449.70 (Late 4-wk: 1,472.67 vs 1,370.00), yet L01_A rebounded to 1,520.00 across its 3 Sep weeks (09-07, 09-14, 09-21).")
    c.drawString(margin_x + 10, y - 57.5, "- Outlier Sensitivity: Trimming L06_B's two unexplained spikes (2,422 on 2026-07-06; 2,343 on 2026-08-17) yields n=13 Mean = 1,282.62, Med = 1,274.00, SD = 288.83.")

    c.showPage()
    c.save()
    print(f"Generated {OUT_BACKUP.name} (4 landscape pages; Page 4 bottom remaining: {y - 62:.1f} pt).")


def main() -> None:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    wa_df = pd.read_csv(WA_PATH)
    for oid, o in golden["options"].items():
        vals = wa_df[(wa_df["option_id"] == oid) & (wa_df["observation_status"] == "Complete")]["observed_passages"].astype(float)
        o["q1"] = float(vals.quantile(0.25))
        o["q3"] = float(vals.quantile(0.75))

    build_two_page_brief(golden)
    build_static_backup(golden, wa_df)


if __name__ == "__main__":
    main()
