#!/usr/bin/env python3
"""Component 3: Automated Validation for Vitaly_Chait_Project_Checkpoint.pdf."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = REPO_ROOT / "Vitaly_Chait_Project_Checkpoint.pdf"
GOLDEN_PATH = REPO_ROOT / "Deliverables" / "golden_metrics.json"


def extract_pdf_text_and_pages(pdf_bytes: bytes) -> tuple[int, str]:
    """Count exact /Type /Page objects and decode uncompressed PDF text literals."""
    page_count = len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", pdf_bytes))
    raw = pdf_bytes.decode("latin1")
    # Extract all PDF string literals inside content streams (between stream..endstream)
    chunks: list[str] = []
    for sm in re.finditer(r"stream\r?\n(.*?)\r?\nendstream", raw, flags=re.S):
        stream_body = sm.group(1)
        # Parse literal strings (...) honoring backslash escapes
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
    text = re.sub(r"\s+", " ", " ".join(chunks)).strip()
    return page_count, text


def validate_checkpoint() -> int:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    checks: list[tuple[str, bool, str]] = []

    # Check 3.1: File & PDF Integrity
    exists = PDF_PATH.exists() and PDF_PATH.stat().st_size > 0
    pdf_bytes = PDF_PATH.read_bytes() if exists else b""
    c31 = exists and pdf_bytes.startswith(b"%PDF-") and pdf_bytes.rstrip().endswith(b"%%EOF")
    checks.append(("Check 3.1 (File & PDF Integrity)", c31, f"size={len(pdf_bytes)} bytes"))

    if not c31:
        for name, ok, msg in checks:
            print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")
        return 1

    page_count, text = extract_pdf_text_and_pages(pdf_bytes)

    # Check 3.2: Exact Page Count == 1
    c32 = page_count == 1
    checks.append(("Check 3.2 (Exact Page Count)", c32, f"pages={page_count}"))

    # Check 3.3: All 5 Required Sections + Suggested Narrative Template Present
    required_sections = [
        "Decision Question",
        "Defined Metric",
        "Preliminary Claim",
        "Static View",
        "Unresolved Question",
        "Suggested Narrative Template",
    ]
    missing_sections = [s for s in required_sections if s not in text]
    c33 = len(missing_sections) == 0
    checks.append(
        (
            "Check 3.3 (All Required Sections Present)",
            c33,
            "all 6 headers found" if c33 else f"missing={missing_sections}",
        )
    )

    # Check 3.4: Zero Unfilled Template Placeholders
    placeholders = [
        "[option A]",
        "[option B]",
        "[learning objective]",
        "[constraint]",
        "[definition",
        "[bounded claim]",
        "[uncertainty]",
    ]
    found_ph = [p for p in placeholders if p.lower() in text.lower()]
    c34 = len(found_ph) == 0
    checks.append(
        (
            "Check 3.4 (No Unfilled Placeholders)",
            c34,
            "zero leftover bracket placeholders" if c34 else f"found={found_ph}",
        )
    )

    # Check 3.5: Metric Parity with golden_metrics.json
    opts = golden["options"]
    meta = golden["metadata"]
    expected_tokens = [
        f"{opts['L01_A']['mean']:,.2f}",
        f"{opts['L01_A']['median']:,.2f}",
        f"{opts['L04_A']['mean']:,.2f}",
        f"{opts['L04_A']['median']:,.2f}",
        f"{opts['L06_B']['mean']:,.2f}",
        f"{opts['L06_B']['median']:,.2f}",
        f"{opts['L04_A']['shared_10wk_mean']:,.2f}",
        f"{opts['L01_A']['shared_10wk_mean']:,.2f}",
        f"{meta['pairwise_L01A_L04A']['L01_A_mean']:,.2f}",
        f"{meta['pairwise_L01A_L04A']['L04_A_mean']:,.2f}",
        f"{opts['L01_A']['sep_3wk_mean']:,.2f}",
        f"{opts['L04_A']['sep_3wk_mean']:,.2f}",
        f"{opts['L06_B']['spike_trimmed']['mean']:,.2f}",
        f"${opts['L01_A']['total_pilot_cost_usd']:,}",
        f"${opts['L04_A']['total_pilot_cost_usd']:,}",
        f"${opts['L06_B']['total_pilot_cost_usd']:,}",
        str(meta["weekly_rows_total"]),
        str(meta["complete_rows_count"]),
        str(meta["missing_rows_count"]),
        "1,175",
        "256,773",
    ]
    # Also ensure every one of the 12 options' exact mean and median appears in the chart/text
    for oid, o in opts.items():
        expected_tokens.append(oid)
        expected_tokens.append(f"{o['mean']:,.2f}")
        expected_tokens.append(f"{o['median']:,.2f}")

    missing_metrics = [tok for tok in dict.fromkeys(expected_tokens) if tok not in text]
    c35 = len(missing_metrics) == 0
    checks.append(
        (
            "Check 3.5 (Metric Parity)",
            c35,
            f"all {len(dict.fromkeys(expected_tokens))} baseline metrics verified"
            if c35
            else f"missing={missing_metrics}",
        )
    )

    all_ok = True
    for name, ok, msg in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")
        if not ok:
            all_ok = False

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(validate_checkpoint())
