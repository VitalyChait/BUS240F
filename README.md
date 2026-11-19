# BUS 240F Final Project

This repository contains the BUS 240F Final Project deliverables, reproducible build scripts, and verification suite, intended for course **BUS 240F** and inspected by **Prof. Yeabin Moon**.

---

## Project Goal

Advise a fictional retailer on authorizing **one affordable location and operating window** for a four-week pop-up engagement pilot:

- **Decision Scope & Constraints:**
  - Choose `1` option from `12` candidates (`6` locations × `2` Tue–Sat 20-hr/wk shifts)
  - Hard 4-week budget cap: `<= $18,000`
  - Pilot window: **Oct 12 – Nov 8, 2026** (`4` weeks, `80` total hours)
  - Historical data: **Jun 8 – Sep 27, 2026** (`16` weeks; `192` rows = `184 Complete` + `8 Missing`)
- **Primary Recommendation:**
  - Authorize **`L01_A`** (Cedar Walk, Window A, `$18,000`)
  - Ranks `#1` among all `8` affordable options in Mean (`1,510.00` passages/wk) and Median (`1,535.00`, `n = 14`)
- **Key Alternatives & Budget Counterfactual:**
  - **`L04_A`** (`$17,500`, `CV = 14.59%`): Steadiest affordable backup; leads shared `10-Wk` and `8-Wk non-spike` subsets
  - **`L06_B`** (`$16,000`, `CV = 32.93%`): Spike-driven runner-up; drops to `1,282.62` mean after trimming 2 outlier weeks
  - **`L05_B`** (`$21,000`, `1,731.40` Mean, `CV = 10.00%`): **Best Overall Statistical Winner**, excluded solely by the hard `$18,000` cap
- **Data Boundaries & Decision Triggers:**
  - Counts measure bidirectional `passage events` (including repeat crossings), not unique customers or sales
  - Pre-trial **Oct 6–10** spot checks set explicit quantitative thresholds to **Switch to `L04_A`** or **Wait**

---

## Deliverables

### Final Three-File Submission Package
- **`Vitaly_Chait_Final_Project_Workbook.twbx`** — Packaged Tableau workbook (`12` worksheets) covering model/completeness audits, cost & KPI tables, distribution/box plots, and sensitivity views.
- **`Vitaly_Chait_Two_Page_Brief.pdf`** — Strictly `2`-page executive decision brief covering the recommendation, multi-level priority ranking, 12-option baseline table, stress tests, verification notes, AI disclosure, and decision triggers.
- **`Vitaly_Chait_Static_View_Backup.pdf`** — Strictly `4`-page landscape standalone backup of all decisive views, readable without Tableau.

### Milestone, Defense & Reference Files
- **`Vitaly_Chait_Project_Checkpoint.pdf`** — `1`-page Milestone 1 checkpoint framing the decision, metric, preliminary view, and open questions.
- **`Deliverables/Presentation_and_Defense_Guide.md`** — 6-minute team presentation script, 12-question defense playbook, 1-minute final statement, and 48-hour individual critique memo template.
- **`Deliverables/golden_metrics.json` & `Deliverables/verification_audit_summary.md`** — Single-source-of-truth metric oracle and verification audit trail.

---

## Approaches & Engineering Methodology

1. **Upfront Human Context Engineering:** Manually cleaned and normalized all raw course instructions into structured Markdown specs (`Instructions/`) and modular component plans (`Instructions/AI/00`–`06`) prior to building deliverables.
2. **Data Hygiene & Analytical Stress-Testing:**
   - Kept the `8` missing observations blank (`NULL`) instead of zero-imputing, and read fixed 4-week cost via `MIN(Total Pilot Cost Usd)` to prevent `16x` inflation across weekly joins.
   - Stress-tested rankings across spike-trimming (`L06_B` without `2,422` & `2,343`), listwise (`10-Wk`, `9-Wk`, `8-Wk non-spike`) vs. `12-Wk` pairwise `L01_A`/`L04_A` comparisons, strictly complete (`n = 4`) rolling 4-week blocks, late-season/September checks, and paired week-to-week uncertainty.
3. **Multi-Model Challenge & Automated Verification (`37` Checks):**
   - Cross-checked statistical, Tableau XML, and clarity assumptions across multiple AI platforms alongside manual inspection in Tableau Desktop and rendered PDFs.
   - Automated build and validation pipeline in `scripts/` (`validate_step1_data.py` through `validate_step5_package.py`) enforcing `100%` CSV/starter-`.twbx` parity, Tableau 18.1 XML schema compliance, exact PDF page counts, and cross-deliverable metric consistency against `Deliverables/golden_metrics.json`.

---

## Reproducing Validation

```bash
python3 scripts/validate_step5_package.py
```
