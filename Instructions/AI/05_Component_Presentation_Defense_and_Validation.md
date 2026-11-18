# Component 5: Milestone 4 — Presentation, Defense & Critique Playbook and Final Package Validation

> **Prerequisite:** Component 4 (`Vitaly_Chait_Two_Page_Brief.pdf` and `Vitaly_Chait_Static_View_Backup.pdf`) must have passed Validation Gate 4.

## Objective
Prepare `Deliverables/Presentation_and_Defense_Guide.md` for the December 2 practice and December 10 final presentation/defense session (6-minute presentation + 12-minute questioning + 1-minute final position), plus a structured evaluation template for the Individual Decision-Critique Memo (15% of course grade), followed by an end-to-end validation of the entire submission package.

---

## Required Sections in `Deliverables/Presentation_and_Defense_Guide.md`
1. **6-Minute Timed Presentation Script:**
   - **Minute 0:00–1:00:** Decision framing, $18,000 budget constraint (8 affordable vs. 4 over-budget options), and primary recommendation (`L01_A`, Cedar Walk Window A, $18,000).
   - **Minute 1:00–2:15:** Data model verification (`192` rows = `184 Complete` + `8 Missing`, `MIN(Total Pilot Cost Usd)` rule, `L01_A` check rows, and passage events vs. unique visitors boundary).
   - **Minute 2:15–3:45:** Visual comparison of `L01_A` (`1,510.00` mean, `1,535.00` median) vs. credible alternatives `L04_A` ($17,500; `1,401.36` mean, `1,424.50` median, CV `14.59%`) and `L06_B` ($16,000; `1,429.27` mean, `1,327.00` median, CV `32.93%`).
   - **Minute 3:45–5:00:** Consequential analytical sensitivity tests (Mean vs. Median / spike trimming on `L06_B`, and the 10-week shared-week test showing `L04_A` overtaking `L01_A` at `1,449.70` vs. `1,407.00`).
   - **Minute 5:00–6:00:** Unresolved uncertainties (missingness, seasonality, repeat crossings), actionable next check, and explicit quantitative thresholds that would change the recommendation.
2. **12-Minute Question & Defense Playbook:**
   - Ready-to-use, quantitative responses to 12 high-probability examiner questions covering data hygiene, missing values, unequal week counts, fixed-cost aggregation in Tableau, outlier handling, seasonality, and decision reversals.
3. **1-Minute Final Position Statement:**
   - Crisp closing summary synthesizing the recommendation, boundary conditions, and decision rule.
4. **Individual Decision-Critique Memo Template & Rubric Checklist (15% of Grade):**
   - Structured analytical framework for evaluating another team's presentation within the 48-hour deadline.

---

## Validation Gate 5 Checklist (`scripts/validate_step5_package.py`)
- [ ] **Check 5.1 (All Final Deliverables Present & Non-Empty):**
  - `Vitaly_Chait_Project_Checkpoint.pdf` (1 page)
  - `Vitaly_Chait_Final_Project_Workbook.twbx` (18/18 XML & archive checks)
  - `Vitaly_Chait_Two_Page_Brief.pdf` (2 pages)
  - `Vitaly_Chait_Static_View_Backup.pdf` (4 pages)
  - `Deliverables/Presentation_and_Defense_Guide.md`
- [ ] **Check 5.2 (Cross-Deliverable Consistency):** All 5 deliverables cite identical numbers from `Deliverables/golden_metrics.json`.
