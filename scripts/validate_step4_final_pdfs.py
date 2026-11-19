#!/usr/bin/env python3
"""Component 4: Automated Validation for Two-Page Brief and Static View Backup PDFs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BRIEF_PDF = REPO_ROOT / "Vitaly_Chait_Two_Page_Brief.pdf"
BACKUP_PDF = REPO_ROOT / "Vitaly_Chait_Static_View_Backup.pdf"
GOLDEN_PATH = REPO_ROOT / "Deliverables" / "golden_metrics.json"


def decode_stream_text(stream_body: str) -> str:
    chunks: list[str] = []
    i = 0
    n = len(stream_body)
    while i < n:
        if stream_body[i] == "(":
            i += 1
            depth = 1
            buf: list[str] = []
            while i < n and depth > 0:
                ch = stream_body[i]
                if ch == "\\" and i + 1 < n:
                    nxt = stream_body[i + 1]
                    if nxt in ("(", ")", "\\"):
                        buf.append(nxt)
                        i += 2
                    elif nxt in ("n", "r", "t"):
                        buf.append(" ")
                        i += 2
                    elif nxt.isdigit():
                        oct_digits = stream_body[i + 1 : i + 4]
                        if len(oct_digits) == 3 and all(d in "01234567" for d in oct_digits):
                            code = int(oct_digits, 8)
                            buf.append(bytes([code]).decode("cp1252", errors="replace"))
                            i += 4
                        else:
                            i += 2
                    else:
                        i += 2
                elif ch == "(":
                    depth += 1
                    buf.append(ch)
                    i += 1
                elif ch == ")":
                    depth -= 1
                    if depth > 0:
                        buf.append(ch)
                    i += 1
                else:
                    buf.append(ch)
                    i += 1
            chunks.append("".join(buf))
        else:
            i += 1
    return re.sub(r"\s+", " ", " ".join(chunks)).strip()


def extract_pages_text(pdf_path: Path) -> tuple[bool, int, list[str]]:
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        return False, 0, []
    pdf_bytes = pdf_path.read_bytes()
    valid_pdf = pdf_bytes.startswith(b"%PDF-") and pdf_bytes.rstrip().endswith(b"%%EOF")
    page_count = len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", pdf_bytes))
    raw = pdf_bytes.decode("latin1")
    stream_texts = [
        decode_stream_text(m.group(1))
        for m in re.finditer(r"stream\r?\n(.*?)\r?\nendstream", raw, flags=re.S)
    ]
    return valid_pdf, page_count, stream_texts


def validate_final_pdfs() -> int:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    opts = golden["options"]
    meta = golden["metadata"]
    checks: list[tuple[str, bool, str]] = []

    # Check 4.1: Exact 2-Page Constraint on Brief
    b_valid, b_pages, b_streams = extract_pages_text(BRIEF_PDF)
    brief_text = " ".join(b_streams)
    c41 = b_valid and b_pages == 2
    checks.append(("Check 4.1 (Exact 2-Page Constraint)", c41, f"valid_pdf={b_valid}, pages={b_pages}"))

    # Check 4.2: Backup View Completeness (4 pages + required view headers/units/captions per page)
    v_valid, v_pages, v_streams = extract_pages_text(BACKUP_PDF)
    backup_text = " ".join(v_streams)
    per_page_ok = len(v_streams) == 4
    page_diag: list[str] = []
    if per_page_ok:
        for p_idx, p_txt in enumerate(v_streams, start=1):
            has_title = f"Static View {p_idx} of 4" in p_txt
            has_units = "Units:" in p_txt and "20-hr" in p_txt
            has_scope = ("2026" in p_txt) and ("Missing" in p_txt or "missing" in p_txt or "Excludes" in p_txt or "excludes" in p_txt)
            if not (has_title and has_units and has_scope):
                per_page_ok = False
                page_diag.append(f"p{p_idx}(title={has_title}, units={has_units}, scope={has_scope})")
    c42 = v_valid and v_pages == 4 and per_page_ok
    checks.append(
        (
            "Check 4.2 (Backup View Completeness)",
            c42,
            f"valid_pdf={v_valid}, pages={v_pages}, all_4_views_annotated={per_page_ok} {page_diag}".strip(),
        )
    )

    # Check 4.3: Verification Notes Audit in Two-Page Brief
    required_ver_tokens = [
        str(meta["weekly_rows_total"]),          # 192
        str(meta["complete_rows_count"]),        # 184
        str(meta["missing_rows_count"]),         # 8
        str(meta["options_count"]),              # 12
        "1,175",
        "2026-06-08",
        "2026-06-29",
        "$18,000",
        "256,773",
        "BUS240F_Final_Project_Starter.twbx",
        "AI Assistance Disclosure",
    ]
    missing_ver = [t for t in required_ver_tokens if t not in brief_text]
    c43 = len(missing_ver) == 0
    checks.append(
        (
            "Check 4.3 (Verification Notes Audit)",
            c43,
            "all required verification figures & AI disclosure present" if c43 else f"missing={missing_ver}",
        )
    )

    # Check 4.4: Metric Parity across both PDFs against golden_metrics.json
    brief_reqs: list[str] = []
    for oid, o in opts.items():
        brief_reqs.extend(
            [
                oid,
                f"${o['total_pilot_cost_usd']:,}",
                f"{o['raw_sum']:,}",
                f"{o['mean']:,.2f}",
                f"{o['median']:,.2f}",
                f"{o['sd']:.2f}",
                f"{o['cv_pct']:.2f}%",
                f"{o['iqr']:.2f}",
                f"{o['min']:,}-{o['max']:,}",
            ]
        )
    for oid in ("L01_A", "L04_A", "L06_B", "L02_B"):
        o = opts[oid]
        brief_reqs.extend(
            [
                f"{o['shared_10wk_mean']:,.2f}",
                f"{o['shared_10wk_median']:,.2f}",
                f"{o['shared_9wk_mean']:,.2f}",
                f"{o['late_4wk_mean']:,.2f}",
            ]
        )
    brief_reqs.extend(
        [
            f"{opts['L06_B']['spike_trimmed']['mean']:,.2f}",
            f"{opts['L06_B']['spike_trimmed']['median']:,.2f}",
            f"{opts['L06_B']['spike_trimmed']['sd']:.2f}",
            f"{opts['L04_A']['shared_8wk_nonspike_mean']:,.2f}",
            f"{opts['L06_B']['shared_8wk_nonspike_mean']:,.2f}",
            f"{opts['L01_A']['shared_8wk_nonspike_mean']:,.2f}",
            f"{opts['L01_A']['sep_3wk_mean']:,.2f}",
            f"{opts['L04_A']['sep_3wk_mean']:,.2f}",
            f"{meta['pairwise_L01A_L04A']['L01_A_mean']:,.2f}",
            f"{meta['pairwise_L01A_L04A']['L04_A_mean']:,.2f}",
        ]
    )

    backup_reqs: list[str] = []
    for oid, o in opts.items():
        backup_reqs.extend(
            [
                oid,
                f"${o['total_pilot_cost_usd']:,}",
                f"{o['raw_sum']:,}",
                f"{o['mean']:,.2f}",
                f"{o['median']:,.2f}",
                f"{o['sd']:.2f}",
                f"{o['cv_pct']:.2f}%",
                f"{o['iqr']:.2f}",
                f"{o['min']:,}-{o['max']:,}",
            ]
        )
    for oid in ("L01_A", "L06_B", "L04_A", "L02_B", "L02_A", "L06_A", "L03_B", "L03_A"):
        o = opts[oid]
        backup_reqs.extend(
            [
                f"{o['shared_10wk_mean']:,.2f}",
                f"{o['shared_10wk_median']:,.2f}",
                f"{o['shared_9wk_mean']:,.2f}",
                f"{o['late_4wk_mean']:,.2f}",
            ]
        )
    backup_reqs.extend(
        [
            "2,422", "2,343", "1,282.62", "1,274.00", "288.83",
            f"{opts['L04_A']['shared_8wk_nonspike_mean']:,.2f}",
            f"{opts['L06_B']['shared_8wk_nonspike_mean']:,.2f}",
            f"{opts['L01_A']['shared_8wk_nonspike_mean']:,.2f}",
            f"{opts['L01_A']['sep_3wk_mean']:,.2f}",
            f"{opts['L04_A']['sep_3wk_mean']:,.2f}",
            f"{meta['pairwise_L01A_L04A']['L01_A_mean']:,.2f}",
            f"{meta['pairwise_L01A_L04A']['L04_A_mean']:,.2f}",
        ]
    )

    miss_brief = [t for t in dict.fromkeys(brief_reqs) if t not in brief_text]
    miss_backup = [t for t in dict.fromkeys(backup_reqs) if t not in backup_text]
    bad_claims = [c for c in ["L06_B's 5 slowest weeks", "L06_B's 5 lowest"] if c in brief_text or c in backup_text]
    c44 = len(miss_brief) == 0 and len(miss_backup) == 0 and len(bad_claims) == 0
    checks.append(
        (
            "Check 4.4 (Metric Parity)",
            c44,
            "100% metric & claim parity across Two-Page Brief & 4-View Backup"
            if c44
            else f"miss_brief={miss_brief[:8]}, miss_backup={miss_backup[:8]}, bad_claims={bad_claims}",
        )
    )

    all_ok = True
    for name, ok, msg in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")
        if not ok:
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(validate_final_pdfs())
