#!/usr/bin/env python3
"""Component 1: Data & Starter Model Audit and Validation.

Verifies Data/Candidate_Options.csv, Data/Weekly_Activity.csv, and embedded
CSVs inside BUS240F_Final_Project_Starter.twbx against all baseline checks,
cross-checks all metrics against the Master Implementation Plan reference
table, and outputs Deliverables/golden_metrics.json and
Deliverables/verification_audit_summary.md.
"""

from __future__ import annotations

import datetime
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "Data"
STARTER_TWBX = REPO_ROOT / "BUS240F_Final_Project_Starter.twbx"
DELIVERABLES_DIR = REPO_ROOT / "Deliverables"

BUDGET_CAP_USD = 18000
EXCLUDED_10WK_DATES = [
    "2026-06-22",
    "2026-06-29",
    "2026-07-20",
    "2026-08-10",
    "2026-08-24",
    "2026-09-07",
]
EXCLUDED_9WK_DATES = EXCLUDED_10WK_DATES + ["2026-07-27"]
LATE_4WK_DATES = [
    "2026-08-31",
    "2026-09-07",
    "2026-09-14",
    "2026-09-21",
]
L06_B_SPIKE_DATES = ["2026-07-06", "2026-08-17"]
EXCLUDED_8WK_NONSPIKE_DATES = sorted(set(EXCLUDED_10WK_DATES) | set(L06_B_SPIKE_DATES))
SEP_3WK_DATES = ["2026-09-07", "2026-09-14", "2026-09-21"]

# Reference values from Instructions/AI/00_Master_Implementation_Plan.md
EXPECTED_BASELINE: dict[str, dict[str, Any]] = {
    "L01_A": {
        "location_name": "Cedar Walk",
        "window_id": "A",
        "cost": 18000,
        "within_budget": True,
        "obs_weeks": 14,
        "missing_weeks": 2,
        "raw_sum": 21140,
        "mean": 1510.00,
        "median": 1535.00,
        "sd": 302.58,
        "cv_pct": 20.04,
        "iqr": 477.50,
        "min": 920,
        "max": 1970,
        "shared_10wk_mean": 1407.00,
        "shared_9wk_mean": 1423.33,
        "late_4wk_mean": 1370.00,
    },
    "L06_B": {
        "location_name": "Aspen Court",
        "window_id": "B",
        "cost": 16000,
        "within_budget": True,
        "obs_weeks": 15,
        "missing_weeks": 1,
        "raw_sum": 21439,
        "mean": 1429.27,
        "median": 1327.00,
        "sd": 470.64,
        "cv_pct": 32.93,
        "iqr": 554.50,
        "min": 840,
        "max": 2422,
        "shared_10wk_mean": 1619.10,
        "shared_9wk_mean": 1649.44,
        "late_4wk_mean": 1420.00,
    },
    "L04_A": {
        "location_name": "Birch Arcade",
        "window_id": "A",
        "cost": 17500,
        "within_budget": True,
        "obs_weeks": 14,
        "missing_weeks": 2,
        "raw_sum": 19619,
        "mean": 1401.36,
        "median": 1424.50,
        "sd": 204.49,
        "cv_pct": 14.59,
        "iqr": 281.75,
        "min": 978,
        "max": 1721,
        "shared_10wk_mean": 1449.70,
        "shared_9wk_mean": 1455.56,
        "late_4wk_mean": 1472.67,
    },
    "L02_B": {
        "location_name": "Maple Court",
        "window_id": "B",
        "cost": 16500,
        "within_budget": True,
        "obs_weeks": 15,
        "missing_weeks": 1,
        "raw_sum": 19886,
        "mean": 1325.73,
        "median": 1316.00,
        "sd": 127.56,
        "cv_pct": 9.62,
        "iqr": 161.00,
        "min": 1120,
        "max": 1592,
        "shared_10wk_mean": 1304.10,
        "shared_9wk_mean": 1290.00,
        "late_4wk_mean": 1281.25,
    },
    "L02_A": {
        "location_name": "Maple Court",
        "window_id": "A",
        "cost": 15000,
        "within_budget": True,
        "obs_weeks": 16,
        "missing_weeks": 0,
        "raw_sum": 20009,
        "mean": 1250.56,
        "median": 1249.00,
        "sd": 92.62,
        "cv_pct": 7.41,
        "iqr": 112.50,
        "min": 1110,
        "max": 1457,
        "shared_10wk_mean": 1239.40,
        "shared_9wk_mean": 1229.33,
        "late_4wk_mean": 1228.75,
    },
    "L06_A": {
        "location_name": "Aspen Court",
        "window_id": "A",
        "cost": 14500,
        "within_budget": True,
        "obs_weeks": 16,
        "missing_weeks": 0,
        "raw_sum": 18719,
        "mean": 1169.94,
        "median": 1170.00,
        "sd": 156.76,
        "cv_pct": 13.40,
        "iqr": 267.50,
        "min": 915,
        "max": 1390,
        "shared_10wk_mean": 1240.60,
        "shared_9wk_mean": 1247.00,
        "late_4wk_mean": 1222.50,
    },
    "L03_B": {
        "location_name": "Willow Square",
        "window_id": "B",
        "cost": 13500,
        "within_budget": True,
        "obs_weeks": 16,
        "missing_weeks": 0,
        "raw_sum": 18519,
        "mean": 1157.44,
        "median": 1164.00,
        "sd": 151.04,
        "cv_pct": 13.05,
        "iqr": 250.50,
        "min": 943,
        "max": 1426,
        "shared_10wk_mean": 1172.10,
        "shared_9wk_mean": 1148.67,
        "late_4wk_mean": 1092.50,
    },
    "L03_A": {
        "location_name": "Willow Square",
        "window_id": "A",
        "cost": 12000,
        "within_budget": True,
        "obs_weeks": 15,
        "missing_weeks": 1,
        "raw_sum": 16211,
        "mean": 1080.73,
        "median": 1102.00,
        "sd": 111.94,
        "cv_pct": 10.36,
        "iqr": 182.50,
        "min": 934,
        "max": 1263,
        "shared_10wk_mean": 1089.20,
        "shared_9wk_mean": 1070.11,
        "late_4wk_mean": 1032.25,
    },
    "L05_B": {
        "location_name": "Juniper Row",
        "window_id": "B",
        "cost": 21000,
        "within_budget": False,
        "obs_weeks": 15,
        "missing_weeks": 1,
        "raw_sum": 25971,
        "mean": 1731.40,
        "median": 1757.00,
        "sd": 173.19,
        "cv_pct": 10.00,
        "iqr": 220.00,
        "min": 1490,
        "max": 2053,
        "shared_10wk_mean": 1744.11,
        "shared_9wk_mean": 1744.11,
        "late_4wk_mean": 1790.00,
    },
    "L01_B": {
        "location_name": "Cedar Walk",
        "window_id": "B",
        "cost": 19500,
        "within_budget": False,
        "obs_weeks": 16,
        "missing_weeks": 0,
        "raw_sum": 26094,
        "mean": 1630.88,
        "median": 1679.00,
        "sd": 347.68,
        "cv_pct": 21.32,
        "iqr": 509.25,
        "min": 1035,
        "max": 2237,
        "shared_10wk_mean": 1536.10,
        "shared_9wk_mean": 1551.00,
        "late_4wk_mean": 1490.00,
    },
    "L05_A": {
        "location_name": "Juniper Row",
        "window_id": "A",
        "cost": 19000,
        "within_budget": False,
        "obs_weeks": 16,
        "missing_weeks": 0,
        "raw_sum": 25651,
        "mean": 1603.19,
        "median": 1590.00,
        "sd": 153.50,
        "cv_pct": 9.57,
        "iqr": 217.00,
        "min": 1365,
        "max": 1878,
        "shared_10wk_mean": 1605.90,
        "shared_9wk_mean": 1620.78,
        "late_4wk_mean": 1670.00,
    },
    "L04_B": {
        "location_name": "Birch Arcade",
        "window_id": "B",
        "cost": 18500,
        "within_budget": False,
        "obs_weeks": 16,
        "missing_weeks": 0,
        "raw_sum": 23515,
        "mean": 1469.69,
        "median": 1513.50,
        "sd": 237.86,
        "cv_pct": 16.18,
        "iqr": 313.25,
        "min": 992,
        "max": 1884,
        "shared_10wk_mean": 1546.60,
        "shared_9wk_mean": 1553.00,
        "late_4wk_mean": 1455.00,
    },
}


def run_validation() -> int:
    DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)

    co_path = DATA_DIR / "Candidate_Options.csv"
    wa_path = DATA_DIR / "Weekly_Activity.csv"

    co_df = pd.read_csv(co_path)
    wa_df = pd.read_csv(wa_path, keep_default_na=True)

    checks: list[tuple[str, bool, str]] = []

    # Check 1.1: Options Count
    expected_ids = {f"L0{i}_{w}" for i in range(1, 7) for w in ("A", "B")}
    actual_ids = set(co_df["option_id"].astype(str))
    c11 = len(co_df) == 12 and co_df["option_id"].nunique() == 12 and actual_ids == expected_ids
    checks.append(("Check 1.1 (Options Count)", c11, f"rows={len(co_df)}, distinct={co_df['option_id'].nunique()}"))

    # Check 1.2: Uniform Trial Parameters
    c12 = bool(
        (co_df["scheduled_hours_per_week"] == 20).all()
        and (co_df["pilot_weeks"] == 4).all()
    )
    checks.append(
        (
            "Check 1.2 (Uniform Trial Parameters)",
            c12,
            f"hours_unique={co_df['scheduled_hours_per_week'].unique().tolist()}, pilot_weeks_unique={co_df['pilot_weeks'].unique().tolist()}",
        )
    )

    # Check 1.3: Weekly Record Count (192 rows, 12 options x 16 Mondays 2026-06-08..2026-09-21)
    expected_mondays = [
        (datetime.date(2026, 6, 8) + datetime.timedelta(days=7 * i)).isoformat()
        for i in range(16)
    ]
    actual_weeks = sorted(wa_df["week_start"].astype(str).unique().tolist())
    c13 = (
        len(wa_df) == 192
        and actual_weeks == expected_mondays
        and wa_df.groupby("option_id").size().eq(16).all()
    )
    checks.append(("Check 1.3 (Weekly Record Count)", c13, f"rows={len(wa_df)}, weeks={len(actual_weeks)}"))

    # Check 1.4: Completeness Split (184 Complete positive int, 8 Missing blank/null)
    comp_df = wa_df[wa_df["observation_status"] == "Complete"]
    miss_df = wa_df[wa_df["observation_status"] == "Missing"]
    c14 = (
        len(comp_df) == 184
        and len(miss_df) == 8
        and len(comp_df) + len(miss_df) == len(wa_df)
        and comp_df["observed_passages"].notna().all()
        and (comp_df["observed_passages"] > 0).all()
        and (comp_df["observed_passages"] % 1 == 0).all()
        and miss_df["observed_passages"].isna().all()
    )
    checks.append(
        (
            "Check 1.4 (Completeness Split)",
            c14,
            f"Complete={len(comp_df)}, Missing={len(miss_df)}, missing_null={bool(miss_df['observed_passages'].isna().all())}",
        )
    )

    # Check 1.5: Representative Source Rows
    r1 = wa_df[(wa_df["option_id"] == "L01_A") & (wa_df["week_start"] == "2026-06-08")]
    r2 = wa_df[(wa_df["option_id"] == "L01_A") & (wa_df["week_start"] == "2026-06-29")]
    c15 = (
        len(r1) == 1
        and r1.iloc[0]["observation_status"] == "Complete"
        and int(r1.iloc[0]["observed_passages"]) == 1175
        and len(r2) == 1
        and r2.iloc[0]["observation_status"] == "Missing"
        and pd.isna(r2.iloc[0]["observed_passages"])
    )
    checks.append(
        (
            "Check 1.5 (Representative Source Rows)",
            c15,
            "L01_A 2026-06-08=1175 Complete; L01_A 2026-06-29=Missing/null",
        )
    )

    # Check 1.6: Budget Rule
    affordable = set(co_df[co_df["total_pilot_cost_usd"] <= BUDGET_CAP_USD]["option_id"])
    over_budget = set(co_df[co_df["total_pilot_cost_usd"] > BUDGET_CAP_USD]["option_id"])
    exp_aff = {"L01_A", "L02_A", "L02_B", "L03_A", "L03_B", "L04_A", "L06_A", "L06_B"}
    exp_over = {"L04_B", "L05_A", "L01_B", "L05_B"}
    c16 = affordable == exp_aff and over_budget == exp_over and len(affordable) == 8 and len(over_budget) == 4
    checks.append(("Check 1.6 (Budget Rule)", c16, f"within_budget={len(affordable)}, over_budget={len(over_budget)}"))

    # Check 1.7: Starter Package Parity (normalizing CRLF/LF)
    with zipfile.ZipFile(STARTER_TWBX, "r") as zf:
        emb_co = zf.read("Data/Prototype/Candidate_Options.csv").replace(b"\r\n", b"\n")
        emb_wa = zf.read("Data/Prototype/Weekly_Activity.csv").replace(b"\r\n", b"\n")
    disk_co = co_path.read_bytes().replace(b"\r\n", b"\n")
    disk_wa = wa_path.read_bytes().replace(b"\r\n", b"\n")
    c17 = emb_co == disk_co and emb_wa == disk_wa
    checks.append(("Check 1.7 (Starter Package Parity)", c17, "Embedded CSVs match Data/*.csv 100%"))

    # Compute metrics for all 12 options
    options_out: dict[str, dict[str, Any]] = {}
    baseline_mismatches: list[str] = []

    ordered_ids = [
        "L01_A", "L06_B", "L04_A", "L02_B", "L02_A", "L06_A", "L03_B", "L03_A",
        "L05_B", "L01_B", "L05_A", "L04_B",
    ]

    # Rolling 4-calendar-week block statistics (for pilot-duration risk bounds)
    all_weeks_sorted = sorted(wa_df["week_start"].astype(str).unique().tolist())

    for opt_id in ordered_ids:
        meta = co_df[co_df["option_id"] == opt_id].iloc[0]
        opt_rows = wa_df[wa_df["option_id"] == opt_id].sort_values("week_start")
        comp_rows = opt_rows[opt_rows["observation_status"] == "Complete"]
        miss_rows = opt_rows[opt_rows["observation_status"] == "Missing"]

        vals = comp_rows["observed_passages"].astype(float).to_numpy()
        obs_weeks = int(len(vals))
        missing_weeks = int(len(miss_rows))
        missing_dates = miss_rows["week_start"].astype(str).tolist()
        raw_sum = int(vals.sum())
        mean = round(float(np.mean(vals)), 2)
        median = round(float(np.median(vals)), 2)
        sd = round(float(np.std(vals, ddof=1)), 2)
        cv_pct = round(float(np.std(vals, ddof=1) / np.mean(vals) * 100.0), 2)
        iqr = round(float(np.percentile(vals, 75) - np.percentile(vals, 25)), 2)
        vmin = int(np.min(vals))
        vmax = int(np.max(vals))

        week_map = {
            str(r["week_start"]): float(r["observed_passages"])
            for _, r in comp_rows.iterrows()
        }
        roll_means: list[float] = []
        for idx in range(len(all_weeks_sorted) - 3):
            block_vals = [
                week_map[w] for w in all_weeks_sorted[idx : idx + 4] if w in week_map
            ]
            if block_vals:
                roll_means.append(round(sum(block_vals) / len(block_vals), 2))

        s10 = comp_rows[~comp_rows["week_start"].isin(EXCLUDED_10WK_DATES)]["observed_passages"].astype(float)
        s9 = comp_rows[~comp_rows["week_start"].isin(EXCLUDED_9WK_DATES)]["observed_passages"].astype(float)
        s8_ns = comp_rows[~comp_rows["week_start"].isin(EXCLUDED_8WK_NONSPIKE_DATES)]["observed_passages"].astype(float)
        late4 = comp_rows[comp_rows["week_start"].isin(LATE_4WK_DATES)]["observed_passages"].astype(float)
        sep3 = comp_rows[comp_rows["week_start"].isin(SEP_3WK_DATES)]["observed_passages"].astype(float)

        cost = int(meta["total_pilot_cost_usd"])
        within_budget = bool(cost <= BUDGET_CAP_USD)

        opt_entry: dict[str, Any] = {
            "option_id": opt_id,
            "location_id": str(meta["location_id"]),
            "location_name": str(meta["location_name"]),
            "window_id": str(meta["window_id"]),
            "operating_window_label": str(meta["operating_window_label"]),
            "scheduled_hours_per_week": int(meta["scheduled_hours_per_week"]),
            "pilot_weeks": int(meta["pilot_weeks"]),
            "total_pilot_cost_usd": cost,
            "within_budget": within_budget,
            "obs_weeks": obs_weeks,
            "missing_weeks": missing_weeks,
            "missing_week_dates": missing_dates,
            "raw_sum": raw_sum,
            "mean": mean,
            "median": median,
            "sd": sd,
            "cv_pct": cv_pct,
            "iqr": iqr,
            "min": vmin,
            "max": vmax,
            "rolling_4wk_min_mean": min(roll_means),
            "rolling_4wk_max_mean": max(roll_means),
            "shared_10wk_obs": int(len(s10)),
            "shared_10wk_mean": round(float(s10.mean()), 2),
            "shared_10wk_median": round(float(s10.median()), 2),
            "shared_9wk_obs": int(len(s9)),
            "shared_9wk_mean": round(float(s9.mean()), 2),
            "shared_9wk_median": round(float(s9.median()), 2),
            "shared_8wk_nonspike_obs": int(len(s8_ns)),
            "shared_8wk_nonspike_mean": round(float(s8_ns.mean()), 2),
            "shared_8wk_nonspike_median": round(float(s8_ns.median()), 2),
            "late_4wk_obs": int(len(late4)),
            "late_4wk_mean": round(float(late4.mean()), 2),
            "late_4wk_median": round(float(late4.median()), 2),
            "sep_3wk_obs": int(len(sep3)),
            "sep_3wk_mean": round(float(sep3.mean()), 2),
            "sep_3wk_median": round(float(sep3.median()), 2),
        }

        if opt_id == "L06_B":
            trimmed = comp_rows[~comp_rows["week_start"].isin(L06_B_SPIKE_DATES)]["observed_passages"].astype(float)
            opt_entry["spike_trimmed"] = {
                "excluded_dates": L06_B_SPIKE_DATES,
                "excluded_values": [2422, 2343],
                "obs_weeks": int(len(trimmed)),
                "mean": round(float(trimmed.mean()), 2),
                "median": round(float(trimmed.median()), 2),
                "sd": round(float(trimmed.std(ddof=1)), 2),
            }

        # Verify against Master Implementation Plan baseline table
        ref = EXPECTED_BASELINE[opt_id]
        for field in [
            "location_name", "window_id", "within_budget", "obs_weeks", "missing_weeks",
            "raw_sum", "mean", "median", "sd", "cv_pct", "iqr", "min", "max",
            "shared_10wk_mean", "shared_9wk_mean", "late_4wk_mean",
        ]:
            if opt_entry[field] != ref[field]:
                baseline_mismatches.append(f"{opt_id}.{field}: got {opt_entry[field]} != expected {ref[field]}")
        if opt_entry["total_pilot_cost_usd"] != ref["cost"]:
            baseline_mismatches.append(f"{opt_id}.total_pilot_cost_usd: got {opt_entry['total_pilot_cost_usd']} != expected {ref['cost']}")

        options_out[opt_id] = opt_entry

    # Verify L06_B spike-trimmed target (n=13, mean=1282.62) & extended sensitivity regimes
    l06b_trim = options_out["L06_B"]["spike_trimmed"]
    if l06b_trim["obs_weeks"] != 13 or l06b_trim["mean"] != 1282.62:
        baseline_mismatches.append(f"L06_B.spike_trimmed mismatch: {l06b_trim}")

    # Direct pairwise complete-case check: L01_A vs. L04_A across all shared complete weeks (n=12)
    pw_df = wa_df[wa_df["option_id"].isin(["L01_A", "L04_A"])].pivot(
        index="week_start", columns="option_id", values="observed_passages"
    ).dropna()
    pw_dates = sorted([str(idx) for idx in pw_df.index])
    l01a_pw_vals = pw_df["L01_A"].astype(float).to_numpy()
    l04a_pw_vals = pw_df["L04_A"].astype(float).to_numpy()
    pairwise_12wk = {
        "obs_weeks": int(len(pw_dates)),
        "dates": pw_dates,
        "L01_A_mean": round(float(np.mean(l01a_pw_vals)), 2),
        "L01_A_median": round(float(np.median(l01a_pw_vals)), 2),
        "L04_A_mean": round(float(np.mean(l04a_pw_vals)), 2),
        "L04_A_median": round(float(np.median(l04a_pw_vals)), 2),
        "L01_A_weekly_wins": int((l01a_pw_vals > l04a_pw_vals).sum()),
        "L04_A_weekly_wins": int((l04a_pw_vals > l01a_pw_vals).sum()),
        "listwise_excluded_pairwise_dates": [
            d for d in pw_dates if d in EXCLUDED_8WK_NONSPIKE_DATES
        ],
    }

    # Window B vs. Window A premium across all 6 locations
    win_b_vs_a: dict[str, dict[str, Any]] = {}
    for loc_num in range(1, 7):
        oa = options_out[f"L0{loc_num}_A"]
        ob = options_out[f"L0{loc_num}_B"]
        win_b_vs_a[f"L0{loc_num}"] = {
            "location_name": oa["location_name"],
            "win_a_mean": oa["mean"],
            "win_b_mean": ob["mean"],
            "mean_diff_b_minus_a": round(ob["mean"] - oa["mean"], 2),
            "cost_diff_b_minus_a": ob["total_pilot_cost_usd"] - oa["total_pilot_cost_usd"],
        }

    ext_checks = [
        ("L04_A.shared_8wk_nonspike_mean", options_out["L04_A"]["shared_8wk_nonspike_mean"], 1497.12),
        ("L06_B.shared_8wk_nonspike_mean", options_out["L06_B"]["shared_8wk_nonspike_mean"], 1428.25),
        ("L01_A.shared_8wk_nonspike_mean", options_out["L01_A"]["shared_8wk_nonspike_mean"], 1368.75),
        ("L01_A.sep_3wk_mean", options_out["L01_A"]["sep_3wk_mean"], 1520.00),
        ("L04_A.sep_3wk_mean", options_out["L04_A"]["sep_3wk_mean"], 1459.00),
        ("pairwise_12wk.obs_weeks", pairwise_12wk["obs_weeks"], 12),
        ("pairwise_12wk.L01_A_mean", pairwise_12wk["L01_A_mean"], 1482.08),
        ("pairwise_12wk.L04_A_mean", pairwise_12wk["L04_A_mean"], 1388.25),
        ("L01_A.rolling_4wk_min_mean", options_out["L01_A"]["rolling_4wk_min_mean"], 1236.67),
        ("L01_A.rolling_4wk_max_mean", options_out["L01_A"]["rolling_4wk_max_mean"], 1790.00),
        ("L04_A.rolling_4wk_min_mean", options_out["L04_A"]["rolling_4wk_min_mean"], 1285.75),
        ("L04_A.rolling_4wk_max_mean", options_out["L04_A"]["rolling_4wk_max_mean"], 1516.67),
    ]
    for label, got, exp in ext_checks:
        if got != exp:
            baseline_mismatches.append(f"{label}: got {got} != expected {exp}")

    checks.append(
        (
            "Check 1.8 (Baseline Reference Table Parity)",
            len(baseline_mismatches) == 0,
            "All 12 options, sensitivity subsets, pairwise 12-wk & rolling 4-wk benchmarks match 100%"
            if not baseline_mismatches
            else "; ".join(baseline_mismatches),
        )
    )

    total_passages = int(comp_df["observed_passages"].sum())

    golden = {
        "metadata": {
            "source_starter_twbx": "BUS240F_Final_Project_Starter.twbx",
            "historical_window_start": "2026-06-08",
            "historical_window_end": "2026-09-21",
            "historical_window_display": "Jun 8 – Sep 27, 2026 (16 scheduled weeks)",
            "decision_date": "2026-09-28",
            "proposed_pilot_period": "2026-10-12 to 2026-11-08",
            "scheduled_hours_per_week": 20,
            "pilot_weeks": 4,
            "total_pilot_hours": 80,
            "budget_cap_usd": BUDGET_CAP_USD,
            "options_count": int(len(co_df)),
            "affordable_options_count": int(len(affordable)),
            "over_budget_options_count": int(len(over_budget)),
            "weekly_rows_total": int(len(wa_df)),
            "complete_rows_count": int(len(comp_df)),
            "missing_rows_count": int(len(miss_df)),
            "missing_rows_affordable_count": int(
                miss_df[miss_df["option_id"].isin(affordable)].shape[0]
            ),
            "total_observed_passages_sum": total_passages,
            "representative_checks": {
                "L01_A_2026_06_08": {"status": "Complete", "observed_passages": 1175},
                "L01_A_2026_06_29": {"status": "Missing", "observed_passages": None},
            },
            "subsets": {
                "shared_10wk_excluded_dates": EXCLUDED_10WK_DATES,
                "shared_9wk_excluded_dates": EXCLUDED_9WK_DATES,
                "shared_8wk_nonspike_excluded_dates": EXCLUDED_8WK_NONSPIKE_DATES,
                "pairwise_12wk_dates": pw_dates,
                "late_4wk_dates": LATE_4WK_DATES,
                "sep_3wk_dates": SEP_3WK_DATES,
            },
            "pairwise_L01A_L04A": pairwise_12wk,
            "window_b_vs_a_by_location": win_b_vs_a,
        },
        "options": options_out,
    }

    golden_path = DELIVERABLES_DIR / "golden_metrics.json"
    golden_path.write_text(json.dumps(golden, indent=2) + "\n", encoding="utf-8")

    # Write human-readable audit log
    lines = [
        "# Component 1 Verification & Audit Summary",
        "",
        "## Dataset & Starter Snapshot Checks",
        "",
        "| Validation Check | Status | Details |",
        "| :--- | :---: | :--- |",
    ]
    all_passed = True
    for name, passed, details in checks:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        lines.append(f"| {name} | **{status}** | {details} |")

    lines.extend(
        [
            "",
            "## Global Model Verification Totals",
            "",
            f"- **Candidate Options:** `12` (`8` Within Budget <= $18,000; `4` Over Budget)",
            f"- **Weekly Activity Rows:** `192` (`184 Complete` + `8 Missing`; `7` missing among affordable options, `1` over-budget)",
            f"- **Grand Total Observed Passages (`SUM(Observed Passages)`):** `{total_passages:,}`",
            "- **Representative Row Checks (`L01_A`):** `2026-06-08` = `Complete` (`1,175`), `2026-06-29` = `Missing` (null/blank)",
            "",
            "## Verified Metrics Across All 12 Candidate Options",
            "",
            "| Option | Location | Win | 4-Wk Cost | Budget | Obs (n) | Miss | Raw Sum | Mean | Median | SD | CV (%) | IQR | Min–Max | 10-Wk Mean | 9-Wk Mean | Late 4-Wk Mean |",
            "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]
    )

    for opt_id in ordered_ids:
        o = options_out[opt_id]
        s10_cell = f"{o['shared_10wk_mean']:,.2f}"
        if o["shared_10wk_obs"] != 10:
            s10_cell += f" (n={o['shared_10wk_obs']})"
        lines.append(
            f"| `{opt_id}` | {o['location_name']} | {o['window_id']} | ${o['total_pilot_cost_usd']:,} | "
            f"{o['within_budget']} | {o['obs_weeks']} | {o['missing_weeks']} | {o['raw_sum']:,} | "
            f"{o['mean']:,.2f} | {o['median']:,.2f} | {o['sd']:.2f} | {o['cv_pct']:.2f}% | "
            f"{o['iqr']:.2f} | {o['min']:,}–{o['max']:,} | {s10_cell} | "
            f"{o['shared_9wk_mean']:,.2f} | {o['late_4wk_mean']:,.2f} |"
        )

    lines.extend(
        [
            "",
            "*Note: IQR uses continuous linear interpolation (`PERCENTILE.INC`); Tableau default Tukey hinges give `485.00` for `L01_A` and `309.00` for `L04_A`. In the `10-Wk Mean` column, over-budget `L05_B` missed `2026-07-27`, so its mean over the 10-week affordable window covers `n=9` observed weeks.*",
            "",
            "## Key Sensitivity Benchmarks",
            "",
            f"- **L06_B Spike-Trimmed (`n=13`, excluding `2026-07-06`=2,422 and `2026-08-17`=2,343):** "
            f"Mean = `{l06b_trim['mean']:,.2f}`, Median = `{l06b_trim['median']:,.2f}`, SD = `{l06b_trim['sd']:.2f}`",
            f"- **Shared 10-Week Affordable Subset (`n=10` complete weeks across all 8 affordable options):** "
            f"`L04_A` Mean = `{options_out['L04_A']['shared_10wk_mean']:,.2f}` (Median `{options_out['L04_A']['shared_10wk_median']:,.2f}`) "
            f"vs. `L01_A` Mean = `{options_out['L01_A']['shared_10wk_mean']:,.2f}` (Median `{options_out['L01_A']['shared_10wk_median']:,.2f}`)",
            f"- **Direct Pairwise Head-to-Head (`L01_A` vs. `L04_A`, `n=12` weeks where both have complete counts):** "
            f"`L01_A` Mean = `{pairwise_12wk['L01_A_mean']:,.2f}` (Median `{pairwise_12wk['L01_A_median']:,.2f}`) "
            f"vs. `L04_A` Mean = `{pairwise_12wk['L04_A_mean']:,.2f}` (Median `{pairwise_12wk['L04_A_median']:,.2f}`); weekly wins split `{pairwise_12wk['L01_A_weekly_wins']}–{pairwise_12wk['L04_A_weekly_wins']}`",
            f"- **Shared 8-Week Non-Spike Subset (`n=8`, excluding 6 missing-overlap weeks + `07-06` & `08-17` spikes):** "
            f"`L04_A` Mean = `{options_out['L04_A']['shared_8wk_nonspike_mean']:,.2f}` (Median `{options_out['L04_A']['shared_8wk_nonspike_median']:,.2f}`) "
            f"vs. `L06_B` Mean = `{options_out['L06_B']['shared_8wk_nonspike_mean']:,.2f}` and `L01_A` Mean = `{options_out['L01_A']['shared_8wk_nonspike_mean']:,.2f}`",
            f"- **September 3-Week Rebound (`2026-09-07` to `2026-09-21`, apples-to-apples):** "
            f"`L01_A` Mean = `{options_out['L01_A']['sep_3wk_mean']:,.2f}` (`n=3`) vs. `L04_A` Sep 3-Wk Mean = `{options_out['L04_A']['sep_3wk_mean']:,.2f}` (`n=2`; `L04_A` Late 4-Wk Mean incl. `08-31` = `{options_out['L04_A']['late_4wk_mean']:,.2f}`)",
            f"- **4-Week Rolling Block Ranges (`13` overlapping 4-week windows):** "
            f"`L01_A` = `{options_out['L01_A']['rolling_4wk_min_mean']:,.2f}–{options_out['L01_A']['rolling_4wk_max_mean']:,.2f}` vs. "
            f"`L04_A` = `{options_out['L04_A']['rolling_4wk_min_mean']:,.2f}–{options_out['L04_A']['rolling_4wk_max_mean']:,.2f}`",
            "",
        ]
    )

    summary_path = DELIVERABLES_DIR / "verification_audit_summary.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    for name, passed, details in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}: {details}")

    if not all_passed:
        return 1
    print(f"\nAll checks passed! Generated {golden_path.relative_to(REPO_ROOT)} and {summary_path.relative_to(REPO_ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(run_validation())
