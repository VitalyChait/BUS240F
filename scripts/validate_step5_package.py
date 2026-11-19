#!/usr/bin/env python3
"""Component 5: End-to-End Package Validation & Cross-Deliverable Consistency Audit."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_PATH = REPO_ROOT / "Deliverables" / "golden_metrics.json"
DEFENSE_GUIDE = REPO_ROOT / "Deliverables" / "Presentation_and_Defense_Guide.md"

DELIVERABLES = {
    "checkpoint_pdf": REPO_ROOT / "Vitaly_Chait_Project_Checkpoint.pdf",
    "twbx": REPO_ROOT / "Vitaly_Chait_Final_Project_Workbook.twbx",
    "brief_pdf": REPO_ROOT / "Vitaly_Chait_Two_Page_Brief.pdf",
    "backup_pdf": REPO_ROOT / "Vitaly_Chait_Static_View_Backup.pdf",
    "defense_guide": DEFENSE_GUIDE,
}


def decode_pdf_text(pdf_path: Path) -> tuple[int, str]:
    pdf_bytes = pdf_path.read_bytes()
    pages = len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", pdf_bytes))
    raw = pdf_bytes.decode("latin1")
    chunks: list[str] = []
    for sm in re.finditer(r"stream\r?\n(.*?)\r?\nendstream", raw, flags=re.S):
        body = sm.group(1)
        i, n = 0, len(body)
        while i < n:
            if body[i] == "(":
                i += 1
                depth = 1
                buf: list[str] = []
                while i < n and depth > 0:
                    ch = body[i]
                    if ch == "\\" and i + 1 < n:
                        nxt = body[i + 1]
                        if nxt in ("(", ")", "\\"):
                            buf.append(nxt)
                            i += 2
                        elif nxt in ("n", "r", "t"):
                            buf.append(" ")
                            i += 2
                        elif nxt.isdigit():
                            oct_d = body[i + 1 : i + 4]
                            if len(oct_d) == 3 and all(d in "01234567" for d in oct_d):
                                buf.append(bytes([int(oct_d, 8)]).decode("cp1252", errors="replace"))
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
    return pages, re.sub(r"\s+", " ", " ".join(chunks)).strip()


def run_subvalidator(script_name: str) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / script_name)],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0, proc.stdout.strip()


def validate_package() -> int:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    opts = golden["options"]
    meta = golden["metadata"]

    checks: list[tuple[str, bool, str]] = []

    # Check 5.1: All 5 Final Deliverables Present, Non-Empty & Individually Validated
    missing_files = [
        k for k, p in DELIVERABLES.items() if not p.exists() or p.stat().st_size == 0
    ]

    v1_ok, _ = run_subvalidator("validate_step1_data.py")
    v2_ok, _ = run_subvalidator("validate_step2_twbx.py")
    v3_ok, _ = run_subvalidator("validate_step3_checkpoint.py")
    v4_ok, _ = run_subvalidator("validate_step4_final_pdfs.py")

    guide_text = DEFENSE_GUIDE.read_text(encoding="utf-8") if DEFENSE_GUIDE.exists() else ""
    req_guide_sections = [
        "## 1. Six-Minute Timed Presentation Script",
        "## 2. Twelve-Minute Question & Defense Playbook",
        "## 3. One-Minute Final Position Statement",
        "## 4. Individual Decision-Critique Memo Template",
    ]
    guide_sec_ok = all(s in guide_text for s in req_guide_sections) and len(re.findall(r"^### Q\d+\.", guide_text, flags=re.M)) == 12

    c51 = (
        len(missing_files) == 0
        and v1_ok
        and v2_ok
        and v3_ok
        and v4_ok
        and guide_sec_ok
    )
    checks.append(
        (
            "Check 5.1 (All Final Deliverables Present & Validated)",
            c51,
            f"missing={missing_files}, gates=[s1:{v1_ok}, s2:{v2_ok}, s3:{v3_ok}, s4:{v4_ok}], guide_sections={guide_sec_ok}",
        )
    )

    # Check 5.2: Cross-Deliverable Metric Consistency against golden_metrics.json
    _, cp_text = decode_pdf_text(DELIVERABLES["checkpoint_pdf"])
    _, br_text = decode_pdf_text(DELIVERABLES["brief_pdf"])
    _, bk_text = decode_pdf_text(DELIVERABLES["backup_pdf"])

    core_metrics = [
        f"{opts['L01_A']['mean']:,.2f}",          # 1,510.00
        f"{opts['L01_A']['median']:,.2f}",        # 1,535.00
        f"{opts['L04_A']['mean']:,.2f}",          # 1,401.36
        f"{opts['L04_A']['median']:,.2f}",        # 1,424.50
        f"{opts['L06_B']['mean']:,.2f}",          # 1,429.27
        f"{opts['L06_B']['median']:,.2f}",        # 1,327.00
        f"{opts['L04_A']['shared_10wk_mean']:,.2f}",  # 1,449.70
        f"{opts['L01_A']['shared_10wk_mean']:,.2f}",  # 1,407.00
        f"{opts['L06_B']['spike_trimmed']['mean']:,.2f}",  # 1,282.62
        f"{opts['L04_A']['late_4wk_mean']:,.2f}", # 1,472.67
        f"{opts['L01_A']['late_4wk_mean']:,.2f}", # 1,370.00
        f"${opts['L01_A']['total_pilot_cost_usd']:,}",     # $18,000
        f"${opts['L04_A']['total_pilot_cost_usd']:,}",     # $17,500
        f"${opts['L06_B']['total_pilot_cost_usd']:,}",     # $16,000
        str(meta["weekly_rows_total"]),           # 192
        str(meta["complete_rows_count"]),         # 184
        str(meta["missing_rows_count"]),          # 8
        "1,175",
        "256,773",
        "2,422",
        "2,343",
    ]

    inconsistencies: list[str] = []
    for label, txt in [
        ("Checkpoint_PDF", cp_text),
        ("Two_Page_Brief_PDF", br_text),
        ("Static_View_Backup_PDF", bk_text),
        ("Presentation_and_Defense_Guide.md", guide_text),
    ]:
        missing_here = [m for m in core_metrics if m not in txt]
        if missing_here:
            inconsistencies.append(f"{label} missing {missing_here}")

    # Also confirm 8-week non-spike, September 3-week, shared Sep/Late, and 12-week pairwise benchmarks across deliverables
    post_checkpoint_metrics = [
        f"{opts['L04_A']['shared_8wk_nonspike_mean']:,.2f}",  # 1,497.13
        f"{opts['L06_B']['shared_8wk_nonspike_mean']:,.2f}",  # 1,428.25
        f"{opts['L01_A']['shared_8wk_nonspike_mean']:,.2f}",  # 1,368.75
        f"{opts['L01_A']['sep_3wk_mean']:,.2f}",              # 1,520.00
        f"{opts['L04_A']['sep_3wk_mean']:,.2f}",              # 1,459.00
        f"{meta['pairwise_L01A_L04A']['L01_A_mean']:,.2f}",   # 1,482.08
        f"{meta['pairwise_L01A_L04A']['L04_A_mean']:,.2f}",   # 1,388.25
        f"{meta['pairwise_L01A_L04A']['shared_sep_L01_A_mean']:,.2f}",  # 1,507.50
        f"{meta['pairwise_L01A_L04A']['shared_late_L01_A_mean']:,.2f}", # 1,311.67
    ]
    bad_phrases = [
        "5 slowest weeks",
        "5 lowest summer weeks",
        "1,497.12",
        "1,236.67",
        "1,790.00",
        "1,516.67",
        "same 3 September weeks",
        "exact same September weeks",
        "2-week pre-trial",
    ]
    for label, txt in [
        ("Checkpoint_PDF", cp_text),
        ("Two_Page_Brief_PDF", br_text),
        ("Static_View_Backup_PDF", bk_text),
        ("Presentation_and_Defense_Guide.md", guide_text),
    ]:
        # Checkpoint intentionally stops at 10-wk, 12-wk pairwise & Sep/Late shared; Brief/Backup/Guide also cover 8-wk non-spike
        req_here = post_checkpoint_metrics[3:] if label == "Checkpoint_PDF" else post_checkpoint_metrics
        miss_pc = [m for m in req_here if m not in txt]
        if miss_pc:
            inconsistencies.append(f"{label} missing {miss_pc}")
        for bad in bad_phrases:
            if bad in txt:
                inconsistencies.append(f"{label} contains inaccurate phrase: {bad!r}")

    # Also confirm exact numbers in defense guide for Q&A benchmarks
    extra_guide = [
        f"{opts['L02_B']['mean']:,.2f}",
        f"{opts['L02_B']['median']:,.2f}",
        f"{opts['L02_A']['mean']:,.2f}",
        f"{opts['L05_B']['mean']:,.2f}",
        f"{opts['L04_A']['shared_10wk_median']:,.2f}",
        f"{opts['L01_A']['shared_10wk_median']:,.2f}",
        f"{opts['L04_A']['shared_9wk_mean']:,.2f}",
        f"{opts['L01_A']['shared_9wk_mean']:,.2f}",
        f"{opts['L04_A']['shared_8wk_nonspike_median']:,.2f}",
        f"{meta['pairwise_L01A_L04A']['L01_A_median']:,.2f}",
        f"{meta['pairwise_L01A_L04A']['L04_A_median']:,.2f}",
        f"{opts['L01_A']['rolling_4wk_min_mean']:,.2f}",
        f"{opts['L01_A']['rolling_4wk_max_mean']:,.2f}",
        f"{opts['L04_A']['rolling_4wk_min_mean']:,.2f}",
        f"{opts['L04_A']['rolling_4wk_max_mean']:,.2f}",
        "21,140",
        "21,439",
        "19,619",
    ]
    miss_extra = [m for m in extra_guide if m not in guide_text]
    if miss_extra:
        inconsistencies.append(f"Defense_Guide extra metrics missing {miss_extra}")

    c52 = len(inconsistencies) == 0
    checks.append(
        (
            "Check 5.2 (Cross-Deliverable Consistency)",
            c52,
            f"all {len(core_metrics)} core metrics, {len(post_checkpoint_metrics)} sensitivity benchmarks & {len(extra_guide)} defense benchmarks aligned 100% across deliverables"
            if c52
            else "; ".join(inconsistencies),
        )
    )

    all_ok = True
    for name, ok, msg in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")
        if not ok:
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(validate_package())
