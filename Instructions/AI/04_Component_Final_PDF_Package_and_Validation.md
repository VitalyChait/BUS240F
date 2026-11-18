# Component 4: Milestone 3 — Final PDF Package (Two-Page Brief & Static View Backup) & Validation

> **Prerequisite:** Component 3 (`Vitaly_Chait_Project_Checkpoint.pdf`) must have passed Validation Gate 3.

## Objective
Produce the two final PDF submission files required by `Instructions/final_project_start_here_guide.md` and `Instructions/final_project_case_background.md`:
1. `Vitaly_Chait_Two_Page_Brief.pdf` (**strictly two pages total**, including verification notes).
2. `Vitaly_Chait_Static_View_Backup.pdf` (standalone multi-page backup of all decisive views, fully readable without Tableau).

---

## Deliverable 1: `Vitaly_Chait_Two_Page_Brief.pdf` (Strictly 2 Pages)
- **Page 1 — Executive Decision Brief & Primary Visual Evidence:**
  - **Recommendation & Priority Framework:** Recommend authorizing **`L01_A` (Cedar Walk, Window A: Tue–Sat 10:00–14:00, fixed cost $18,000)** for the 4-week trial (`Oct 12 – Nov 8, 2026`), prioritizing peak average and median exposure within the $18,000 budget cap.
  - **Comparison with Credible Affordable Alternatives:** Detailed contrast against **`L04_A` (Birch Arcade, Window A, $17,500)** (the high-stability, shared-week/late-season alternative) and **`L06_B` (Aspen Court, Window B, $16,000)** (the spike-driven raw-sum/mean alternative), plus **`L02_B` (Maple Court, Window B, $16,500)** (lowest variance benchmark).
  - **Primary Visual View & Summary Table:** Embedded vector chart and precision metrics table across all 12 candidate options.
- **Page 2 — Consequential Sensitivity Tests, Verification Notes, Boundaries & Decision Triggers:**
  - **Sensitivity Analysis (Chart + Quantitative Findings):**
    1. *Estimator & Outlier Sensitivity (Mean vs. Median & Spike-Trimming):* Switching from Mean (`1,429.27`) to Median (`1,327.00`) or trimming `L06_B`'s two unexplained spikes (`2,422` and `2,343` $\rightarrow$ trimmed mean `1,282.62`) proves `L06_B`'s apparent advantage over `L04_A` is an artifact of two outlier weeks.
    2. *Shared-Week Completeness Sensitivity (10 Shared Affordable Weeks / 9 Shared All-Option Weeks):* Restricting to the 10 weeks where all 8 affordable options have complete data removes four high-volume weeks for `L01_A` (`1,810`, `1,970`, `1,745`, `1,545`), shifting `L01_A`'s mean from `1,510.00` to `1,407.00` and elevating `L04_A` to `#1` stable affordable option (`1,449.70` mean, `1,458.50` median).
  - **Verification Notes & Stewardship:** Documents fixed dataset snapshot (`BUS240F_Final_Project_Starter.twbx`), record counts (`12` options; `192` weekly rows = `184 Complete` + `8 Missing`), source row checks (`L01_A` `2026-06-08` = `1,175`; `2026-06-29` = `Missing`), single fixed cost rule (`MIN(Total Pilot Cost Usd)`), and AI assistance disclosure.
  - **Data Boundaries & What Evidence Would Change Our Recommendation:** Quantitative thresholds for switching to `L04_A` (if CV $<15\%$ or late-season stability is prioritized) or waiting (if pre-trial October audit shows $<1,100$ passages/week or $>40\%$ repeat-crossing inflation).

---

## Deliverable 2: `Vitaly_Chait_Static_View_Backup.pdf` (4 Standalone Views)
- **Page 1 (View 1):** Model Verification, Completeness Heatmap (`184 Complete` vs. `8 Missing` across 12 options × 16 weeks), and Fixed Cost Audit Table.
- **Page 2 (View 2):** Primary Decision View — Mean vs. Median Weekly Passages, IQR & Min–Max Distribution, Fixed 4-Week Pilot Cost, and `$18,000` Budget Threshold across all 12 Options.
- **Page 3 (View 3):** Weekly Time-Series Trajectory (`2026-06-08` to `2026-09-21`) for Top Affordable Candidates (`L01_A`, `L04_A`, `L06_B`, `L02_B`), annotating `L06_B`'s two outlier spikes (`2,422` and `2,343`), `L01_A`'s Aug 31 dip (`920`), and missing-week gaps.
- **Page 4 (View 4):** Sensitivity Analysis View — Side-by-side Slope & Bar Comparison of Full Observed Sample ($n=14..16$) vs. Shared 10-Week Affordable Sample ($n=10$), Shared 9-Week Sample ($n=9$), and Late-Season 4-Week Sample (`Aug 31 – Sep 21`).

---

## Validation Gate 4 Checklist (`scripts/validate_step4_final_pdfs.py`)
- [ ] **Check 4.1 (Exact 2-Page Constraint):** `Vitaly_Chait_Two_Page_Brief.pdf` has **exactly `2` pages** (verified programmatically via PDF `/Type /Page` count and ReportLab canvas counter).
- [ ] **Check 4.2 (Backup View Completeness):** `Vitaly_Chait_Static_View_Backup.pdf` has **exactly `4` pages**, one per decisive view, with titles, units, population/time labels, and explicit filter/exclusion captions on every page.
- [ ] **Check 4.3 (Verification Notes Audit):** Confirms `Vitaly_Chait_Two_Page_Brief.pdf` includes all required verification figures (`192`, `184`, `8`, `12`, `1,175`, `2026-06-08`, `2026-06-29`, `$18,000`) and AI disclosure.
- [ ] **Check 4.4 (Metric Parity):** Confirms 100% agreement between all numbers in both PDFs and `Deliverables/golden_metrics.json`.
