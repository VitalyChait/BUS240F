# Component 3: Milestone 1 — November 20 Checkpoint PDF & Validation

> **Prerequisite:** Component 2 (`Vitaly_Chait_Final_Project_Workbook.twbx`) must have passed both Automated Validation Gate 2A and **Mandatory User Approval Gate 2B**.

## Objective
Generate `Vitaly_Chait_Project_Checkpoint.pdf` adhering strictly to `Instructions/project_checkpoint_template.md` and `Instructions/final_project_start_here_guide.md`.

---

## Required Content Elements
1. **Decision Question:**
   - Identifies the decision-maker (pilot-program manager), the 12 total candidate options (narrowed to the 8 affordable options meeting `Total Pilot Cost <= $18,000`), the 4-week trial window (`Oct 12 – Nov 8, 2026`, 20 hrs/wk, 80 hrs total), and the comparison between primary candidate **`L01_A` (Cedar Walk, Window A, $18,000)** and credible affordable alternatives **`L04_A` (Birch Arcade, Window A, $17,500)** and **`L06_B` (Aspen Court, Window B, $16,000)**.
2. **Defined Metric:**
   - **Average Observed Passages and the Typical (Median) Middle Week Observed Passages**, in **passage events per 20-hour Tue–Sat week** across 16 weekly periods (Week Start Mondays `2026-06-08` to `2026-09-21`, covering `Jun 8 – Sep 27, 2026`). Fixed 4-week cost is read via **The minimum of Total Pilot Cost Usd**.
   - Explicit treatment of missing observations: 8 missing rows (7 among affordable options) are left blank and excluded from the mean/median denominator ($n_i \in \{14, 15, 16\}$), never replaced with zero.
3. **Preliminary Claim:**
   - Bounded, quantitative statement: Across all available complete weeks (`2026-06-08` to `2026-09-21`), `L01_A` ($n=14$, $18,000) leads all 8 affordable options in both Mean (`1,510.00` passages/wk) and Median (`1,535.00` passages/wk), ahead of `L04_A` ($n=14$, $17,500; Mean `1,401.36`, Median `1,424.50`) and `L06_B` ($n=15$, $16,000; Mean `1,429.27`, Median `1,327.00`).
4. **Static View (Visualization):**
   - Standalone high-resolution vector graphic comparing all 12 options with clear title, units (`passage events / 20-hr week`), time window (`Jun 8 – Sep 27, 2026`), budget boundary (`$18,000`), sample sizes ($n_i$), Mean vs. Median markers, and IQR/range bars.
5. **Unresolved Question & Completed Narrative Template:**
   - Evaluates how missing-week overlap (`L01_A` missing `Jun 29` and `Aug 24`), `L06_B`'s two unexplained spikes (`2,422` and `2,343`), and early-autumn seasonality affect the ranking.
   - Includes the filled-in Narrative Template from `Instructions/project_checkpoint_template.md` with zero leftover bracket placeholders.

---

## Validation Gate 3 Checklist (`scripts/validate_step3_checkpoint.py`)
- [ ] **Check 3.1 (File & PDF Integrity):** `Vitaly_Chait_Project_Checkpoint.pdf` exists, is non-empty, starts with `%PDF-`, and ends with `%%EOF`.
- [ ] **Check 3.2 (Exact Page Count):** PDF contains exactly `1` page (clean, zero-overflow layout).
- [ ] **Check 3.3 (All 5 Required Sections Present):** Verifies presence of Decision Question, Defined Metric, Preliminary Claim, Static View, Unresolved Question, and Suggested Narrative Template.
- [ ] **Check 3.4 (No Unfilled Placeholders):** Verifies zero leftover template placeholders (`[option A]`, `[option B]`, `[constraint]`, etc.).
- [ ] **Check 3.5 (Metric Parity):** All numerical figures in the PDF text and chart labels match `Deliverables/golden_metrics.json` 100%.
