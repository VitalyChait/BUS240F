# BUS 240F Final Project — Presentation, Defense & Critique Playbook

**Author / Team:** Vitaly Chait (BUS 240F Team Deliverable — *Add Team # and 3 Teammates' Names Below Before Live Session*)  
**Session Schedule:** Practice Defense (December 2, 2026) | Final Presentation & Individual Defense (December 10, 2026, 1:30–4:30 p.m. Eastern)  
**Format:** 20-minute slot per team — **6 minutes** Presentation | **12 minutes** Questioning (**3 protected minutes per member across 4 teammates**) | **1 minute** Final Position | **1 minute** Transition  
**Source Snapshot:** `BUS240F_Final_Project_Starter.twbx` (Fixed synthetic snapshot; `12` candidate options, `192` scheduled weekly rows)

> **Suggested 4-Member Speaking & Defense Division (BUS 240F Team Structure):**  
> - **Member 1 (0:00–1:30 + Q1/Q3/Q8):** Decision framing, `$18,000` budget boundary, and primary `L01_A` recommendation.  
> - **Member 2 (1:30–2:45 + Q2/Q4/Q10):** Model audit (`192 = 184 + 8`), missingness vs. zero hygiene, `MIN()` cost rule, and passage boundaries.  
> - **Member 3 (2:45–4:30 + Q5/Q6/Q7):** Primary options comparison (`L01_A` vs. `L04_A`, `L06_B`, `L02_B`) and `10-Wk`/`8-Wk`/`12-Wk` sensitivity regimes.  
> - **Member 4 (4:30–6:00 + Final 1-Min Position + Q9/Q11/Q12):** Rolling 4-week risk, late-season/missingness limits, `Oct 6–10` switch/wait triggers, and verification/AI disclosure.

---

## 1. Six-Minute Timed Presentation Script

> **Visual Reference Map:** Use `Vitaly_Chait_Final_Project_Workbook.twbx` (or `Vitaly_Chait_Static_View_Backup.pdf` Views 1–4) as noted at each cue.

### Minute 0:00–1:00 — Decision Framing, Budget Constraint & Primary Recommendation
*(Cue: Static View 2 / Sheet `02 Build the Decision`)*

"Good afternoon. We are advising the pilot-program manager on a single authorization choice for a four-week pop-up retail trial selling reusable bottles, lunch containers, and everyday carry accessories from **October 12 to November 8, 2026**—**80 total operating hours** across 20 scheduled hours per week.

We evaluated **12 candidate options** across six fictional locations and two equal-duration operating windows: Window A (Tue–Sat 10:00–14:00) and Window B (Tue–Sat 14:00–18:00). The binding constraint is the **\$18,000 fixed four-week pilot budget**. That rule immediately disqualifies four over-budget options—`L05_B` (\$21,000), `L01_B` (\$19,500), `L05_A` (\$19,000), and `L04_B` (\$18,500)—leaving **8 affordable options**.

Our primary recommendation is to authorize **`L01_A` (Cedar Walk, Window A, fixed cost \$18,000)**. Across all available historical observations, `L01_A` maximizes both average and typical weekly passerby exposure within budget while clearly supporting the retailer's goal to learn about site engagement."

### Minute 1:00–2:15 — Data Model Verification & Measurement Boundaries
*(Cue: Static View 1 / Sheets `01 Verify the Model`, `01b Option Cost & Completeness Audit`, `01c Representative Source Check (L01_A)`)*

"Before comparing sites, we audited the fixed `BUS240F_Final_Project_Starter.twbx` relational model linking `Candidate_Options.csv` (12 rows) to `Weekly_Activity.csv` on `option_id`.

- **Record completeness:** The `192` scheduled weekly records (`12 options × 16 weekly periods`, Week Start Mondays **2026-06-08 to 2026-09-21**, covering **Jun 8 – Sep 27, 2026** Tue–Sat shifts) split into **`184` Complete** records totaling **`256,773` observed passage events** and **`8` Missing** records (`7` among affordable options, `1` over-budget).
- **Missing-data hygiene:** Missing observations are left blank/null and excluded from every Mean and Median denominator (`n = 14 to 16` complete weeks per option)—never replaced with zero. We verified our source benchmark rows directly: `L01_A` on **2026-06-08** is `Complete` with **`1,175`** passages, and `L01_A` on **2026-06-29** is `Missing` with a blank value.
- **Fixed cost stewardship:** Each option's cost is a single four-week planning commitment read via `MIN(Total Pilot Cost Usd)`—never summed across 16 historical weeks (which would falsely inflate `L01_A` from `\$18,000` to `\$288,000`).
- **Scope boundary:** Passage events count bidirectional line crossings, including repeat crossings. They measure *potential exposure*, not unique people, customer demand, transactions, or profit."

### Minute 2:15–3:45 — Primary Comparison: `L01_A` vs. Credible Affordable Alternatives
*(Cue: Static View 2 & View 3 / Sheets `02 Build the Decision`, `02b Dispersion & Cost Metrics Table` & `03 Weekly Trajectory & Outliers`)*

"Comparing the 8 affordable options on Observed-Week Mean (`AVG(Observed Passages)`) and Observed-Week Median (`MEDIAN(Observed Passages)`), alongside Standard Deviation (`SD`), Coefficient of Variation (`CV`), and Interquartile Range (`IQR`, continuous `PERCENTILE.INC`):

1. **Recommended Option — `L01_A` (Cedar Walk, Window A, \$18,000, `n = 14`):** Leads all 8 affordable options in both **Mean (`1,510.00` passages/wk)** and **Median (`1,535.00` passages/wk)**, with `SD = 302.58`, `CV = 20.04%`, `IQR = 477.50`, and a range of `920–1,970` (raw sum `21,140`). Notably, Window B outperforms Window A at every single location (`+68.33` to `+259.33`/wk) at a `\$1,000–\$2,000` fee premium that prices `L01_B`, `L04_B`, and `L05_B` over budget—making morning Cedar Walk (`L01_A`) the strongest affordable site.
2. **Primary Stability Alternative — `L04_A` (Birch Arcade, Window A, \$17,500, `n = 14`):** Saves `\$500` and posts a Mean of **`1,401.36`** and the second-highest affordable Median of **`1,424.50`**, with substantially tighter operational consistency (`SD = 204.49`, `CV = 14.59%`, `IQR = 281.75`, range `978–1,721`, raw sum `19,619`).
3. **Spike-Driven Alternative — `L06_B` (Aspen Court, Window B, \$16,000, `n = 15`):** Saves `\$2,000` and has the highest affordable raw sum (`21,439`) and #2 Mean (**`1,429.27`**), yet its Median drops to **`1,327.00`** and its dispersion surges (`SD = 470.64`, `CV = 32.93%`, `IQR = 554.50`, range `840–2,422`).
4. **Low-Variance Benchmark — `L02_B` (Maple Court, Window B, \$16,500, `n = 15`):** Offers tight consistency (`Mean = 1,325.73`, `Median = 1,316.00`, `SD = 127.56`, `CV = 9.62%`), while `L02_A` (`\$15,000`, `CV = 7.41%`, `Mean = 1,250.56`) and lower-cost sites (`L06_A`, `L03_B`, `L03_A`) sacrifice `259–429` weekly passages."

### Minute 3:45–5:00 — Consequential Analytical Sensitivity Tests
*(Cue: Static View 3 & View 4 / Sheets `04 Shared-Week Sensitivity Test`, `04b Pairwise L01_A vs L04_A (12 Wk)`, `04c Shared 8-Wk Non-Spike Audit`, `04d`–`04f`)*

"Because our `8` missing rows do not occur on the same dates and `L06_B` shows extreme spikes, we ran multi-regime sensitivity tests comparing listwise vs. pairwise missingness:

1. **Estimator & Outlier Trimming (`L06_B` — Sheet `04f`):** Switching from Mean (`1,429.27`) to Median (`1,327.00`) drops `L06_B` behind `L04_A` (`1,424.50`). As View 3 shows, `L06_B` has two isolated summer surges—**`2,422` on 2026-07-06** and **`2,343` on 2026-08-17`**. Trimming those two unexplained spikes leaves `n = 13` weeks with a Mean of **`1,282.62`**, Median **`1,274.00`**, and `SD = 288.83`—proving `L06_B`'s apparent advantage over `L04_A` is an outlier artifact.
2. **Listwise vs. Pairwise Shared-Week Completeness Tests (`10-Wk` / `9-Wk` / `8-Wk Non-Spike` vs. `12-Wk Pairwise` — Sheets `04`–`04d`):** Restricting to the **10 weeks where all 8 affordable options have complete data** (excluding `06-22`, `06-29`, `07-20`, `08-10`, `08-24`, `09-07`) drops four busy `L01_A` weeks (`1,810`, `1,970`, `1,745`, `1,545`). `L01_A`'s Mean falls from `1,510.00` to **`1,407.00`** (Median **`1,390.00`**), while **`L04_A` overtakes `L01_A` at `1,449.70` Mean and `1,458.50` Median**. Across the **9 shared weeks** for all 12 options (Sheet `04d`, also excluding `07-27`), `L04_A` leads `1,455.56` to `1,423.33`. Note that `L06_B` spikes to `1,619.10` in the 10-week chart only because the 6 excluded dates remove **5 of `L06_B`'s 7 slowest weeks (`840–1,274`; keeping `1,024` and `1,170`)** while retaining both spikes; removing both missing dates and spikes (**8 shared non-spike weeks**, Sheet `04c`) puts **`L04_A` first at `1,497.13`** (Median `1,500.50`) vs. `L06_B` (`1,428.25`) and `L01_A` (`1,368.75`). **Crucial pairwise check:** Because `07-20` and `08-10` were missing only at other sites (`L02_B`, `L03_A`), and `07-06` and `08-17` were `L06_B` spikes, dropping them removed the exact weeks where `L01_A` outpaced `L04_A` (`1,970` vs. `978`; `1,745` vs. `1,184`; `1,875` vs. `1,301`). Directly comparing all **`12` shared weeks where both `L01_A` and `L04_A` were observed** (Sheet `04b`) restores **`L01_A`'s mean lead (`1,482.08` Mean / `1,512.50` Median vs. `L04_A` `1,388.25` Mean / `1,407.00` Median)**—yet weekly wins split **`6–6`** (`median diff = -1.50`, `SE = 132.17`), confirming this is a genuine exposure-upside vs. stability tradeoff rather than a statistically certain gap.
3. **Late-Season Trend & Complete 4-Week Rolling Blocks (Sheet `04e`):** In the **Late 4-Week window (Aug 31 – Sep 21)**, `L04_A` averages **`1,472.67` (`n = 3`)** vs. `L01_A`'s **`1,370.00` (`n = 4`)** (`1,311.67` on shared `n = 3`), dragged by `L01_A`'s single Aug 31 dip (`920`) and helped by `L04_A` missing `09-07`—when same-site `L04_B` (`r = 0.9902` with `L04_A`) plunged to `1,144`. Across the **2 matched September weeks (`09-14`, `09-21`)**, `L01_A` leads **`1,507.50`** (all `3` Sep weeks `1,520.00`) vs. `L04_A` **`1,459.00`** (`1–1` wins). Across **complete 4-week rolling blocks (`n = 4` complete weeks per block only)** matching pilot duration, `L01_A` (`5/13` blocks: **`1,370.00–1,657.50`**) outperforms `L04_A` (`7/13` blocks: **`1,285.75–1,420.00`**) on **`4/4`** simultaneous complete 4-week blocks.

We retain `L01_A` as our primary recommendation because it leads across all `14` observed weeks, all `12` direct pairwise weeks, and all `4/4` simultaneous complete 4-week blocks—while acknowledging the `6–6` weekly split and keeping `L04_A` ready if stability is prioritized."

### Minute 5:00–6:00 — Uncertainties, Actionable Check & Decision-Switching Thresholds
*(Cue: Static View 4 / Decision Triggers)*

"Three uncertainties remain: missing-week causes, summer-to-October seasonality, and repeat-crossing rates vs. actual purchases. Rather than waiting indefinitely—since the trial itself is designed to test engagement—we recommend authorizing `L01_A` subject to two crisp decision rules:

- **Switch to `L04_A` (Birch Arcade, Window A, \$17,500)** if management prioritizes operational stability (`CV < 15%`) over average upside given the `6–6` paired tie, or if a pre-trial **Oct 6–10** spot check (the one full Tue–Sat week in October between the Sep 28 decision and Oct 12 launch) finds `L01_A < 1,350` passages/wk while `L04_A >= 1,400`.
- **Wait and defer authorization** if that Oct 6–10 pre-trial check falls below **`1,100` passages/wk** at both sites, observational sampling finds **`> 40%` repeat-crossing share**, or unresolved access outages explain `L01_A`'s missing dates (`06-29`, `08-24`). Thank you—we welcome your questions."

---

## 2. Twelve-Minute Question & Defense Playbook (12 High-Probability Questions)

### Q1. Why did you exclude the 8 `Missing` observations instead of setting them to zero or imputing the option's mean?
- **Answer:** Per the data dictionary, `Missing` indicates *no usable weekly count*, not zero foot traffic. Setting the 8 missing rows (`L01_A` x2, `L04_A` x2, `L06_B` x1, `L02_B` x1, `L03_A` x1, `L05_B` x1) to zero would falsely pull `L01_A`'s 16-week average down from `1,510.00` (`21,140 / 14`) to `1,321.25` (`21,140 / 16`), confounding site traffic with sensor/reporting completeness. Conversely, simple mean imputation leaves the point estimate unchanged while artificially shrinking variance (`SD` and `IQR`). Leaving missing rows blank (`n = 14..16`) and explicitly testing sensitivity via the **10-week shared complete subset** (`L04_A` `1,449.70` vs. `L01_A` `1,407.00`) is transparent and methodologically sound.

### Q2. Why didn't you rank options by total `SUM(Observed Passages)`? Look—`L06_B` has `21,439` total passages, higher than `L01_A`'s `21,140`!
- **Answer:** Comparing raw sums across unequal numbers of complete weeks is invalid (`L06_B` has `n = 15` observed weeks while `L01_A` has `n = 14`). Dividing by observed weeks shows `L01_A` averages **`1,510.00` passages/wk** (Median `1,535.00`) vs. `L06_B`'s **`1,429.27` passages/wk** (Median `1,327.00`). Moreover, `L06_B`'s raw sum includes two extreme outlier weeks (`2,422` and `2,343`).

### Q3. In Tableau, why does `MIN(Total Pilot Cost Usd)` return the true cost, and what happens if someone uses `SUM`?
- **Answer:** `Weekly_Activity.csv` has 16 rows per option, related to `Candidate_Options.csv` (1 row per option) on `option_id`. Because `total_pilot_cost_usd` is a **single fixed four-week commitment** (not a weekly expense), dragging `SUM(Total Pilot Cost Usd)` when weekly rows are in the view multiplies cost by 16—turning `L01_A`'s `\$18,000` into `\$288,000`. Using `MIN(Total Pilot Cost Usd)` (or `AVG` / `MAX` at the single-option mark level) returns exactly `\$18,000` for `L01_A`, `\$17,500` for `L04_A`, and `\$16,000` for `L06_B`, as verified in `01b Option Cost & Completeness Audit`. (Note: `MIN` across multiple options is not a combined cost, since only one option can be selected.)

### Q4. How did you verify that Tableau's relationship model didn't drop records or misalign `Candidate_Options.csv` and `Weekly_Activity.csv`?
- **Answer:** We performed a four-part model audit (documented in Workbook Sheets `01`, `01b`, `01c` and Static View 1):
  1. `12` distinct `option_id` values in `Candidate_Options.csv`, all with `20` hrs/wk and `4` pilot weeks.
  2. `192` scheduled rows in `Weekly_Activity.csv` (`184 Complete` totaling `256,773` passages + `8 Missing` with null `observed_passages`).
  3. Direct inspection of `L01_A` benchmark rows: `2026-06-08 = Complete (1,175)` and `2026-06-29 = Missing (blank)`.
  4. 100% byte-for-byte parity between standalone CSVs and embedded CSVs in `BUS240F_Final_Project_Starter.twbx`.

### Q5. In your own 10-week shared-week sensitivity test, `L04_A` (`1,449.70`)—and even `L06_B` (`1,619.10`)—beats `L01_A` (`1,407.00`), and `L04_A` costs \$500 less! Why didn't you change your recommendation to `L04_A`?
- **Answer:** First, why `L06_B` (`1,619.10`) looks tallest in the 10-week chart: the 6 excluded dates (`06-22`, `06-29`, `07-20`, `08-10`, `08-24`, `09-07`) happen to cut **5 of `L06_B`'s 7 slowest weeks (`840–1,274`; leaving `1,024` and `1,170` in)** while leaving both extreme spikes (`2,422` and `2,343`) in the subset! Controlling for both missing dates and those 2 spikes (**8 shared non-spike weeks**, Sheet `04c`), `L04_A` leads at `1,497.13` Mean (`1,500.50` Median) ahead of `L06_B` (`1,428.25`) and `L01_A` (`1,368.75`). Second, why listwise exclusion penalizes `L01_A`: dates `07-20` and `08-10` were excluded only because unrelated sites (`L02_B`, `L03_A`) were missing, and `07-06` and `08-17` only because `L06_B` spiked—yet `07-20`, `08-10`, and `07-06` were `L01_A`'s strongest head-to-head weeks over `L04_A` (`1,970` vs. `978`; `1,745` vs. `1,184`; `1,875` vs. `1,301`; while `08-17` was `1,245` vs. `1,219`). Comparing `L01_A` and `L04_A` directly across all **`12` pairwise shared weeks** (`Sheet 04b`), **`L01_A` leads `1,482.08` Mean (`1,512.50` Median) vs. `L04_A` `1,388.25` Mean (`1,407.00` Median)**, and leads `4/4` simultaneous complete 4-week rolling blocks (`1,370.00–1,657.50` vs. `1,285.75–1,420.00`). We do acknowledge openly that pairwise weekly wins tie `6–6` (`median diff = -1.50`, `SD_diff = 457.84`, `SE = 132.17`, `t(11) = 0.71`), so the choice boils down to prioritizing `L01_A`'s `+93.83`–`+108.64`/wk exposure upside (`~$1.15`/extra crossing over 4 weeks at `+108.64`) versus `L04_A`'s tighter stability (`CV = 14.59%` vs. `20.04%`) and `\$500` budget savings. *(Methodological note: reported IQRs use standard continuous linear interpolation `PERCENTILE.INC`, e.g., `L01_A = 477.50`, `L04_A = 281.75`; Tableau default box-plot Tukey hinges yield `485.00` and `309.00`, and both methods agree identically on odd-`n` options like `L06_B = 554.50` and `L02_B = 161.00`.)*

### Q6. `L06_B` saves \$2,000 compared to `L01_A` and has a Mean of `1,429.27`. Isn't `\$2,000` worth a tiny drop in mean exposure?
- **Answer:** Not once distribution shape and outliers are examined. `L06_B` has the widest dispersion of all 12 options (`SD = 470.64`, `CV = 32.93%`, `IQR = 554.50`, range `840–2,422`). Its Median is only **`1,327.00`**, `208` passages/wk below `L01_A` (`1,535.00`) and `97.50` below `L04_A` (`1,424.50`). When we trim its two unexplained spikes (`2,422` on `07-06` and `2,343` on `08-17`), its `n = 13` Mean collapses to **`1,282.62`** (Median `1,274.00`, `SD = 288.83`)—lower than `L02_B` (`1,325.73`). Choosing `L06_B` exposes a 4-week pilot to severe downside risk (`840–1,024` passages/wk in weak weeks).

### Q7. Why not choose `L02_A` (`CV = 7.41%`) or `L02_B` (`CV = 9.62%`) for maximum operational predictability?
- **Answer:** Stability alone is insufficient if baseline exposure is materially lower. `L02_A` (`\$15,000`, `n = 16`, `Mean = 1,250.56`, `Median = 1,249.00`) gives up `259.44` mean passages/wk (~`1,038` crossings over 4 weeks) relative to `L01_A`. `L02_B` (`\$16,500`, `n = 15`, `Mean = 1,325.73`, `Median = 1,316.00`) is a solid low-risk benchmark (`SD = 127.56`), but still trails `L01_A` by `184.27` mean passages/wk and `L04_A` by `108.50` median passages/wk while `L04_A` already delivers sub-15% `CV` (`14.59%`).

### Q8. The over-budget options—especially `L05_B` (`1,731.40` mean, `CV = 10.00%`, `\$21,000`) and `L01_B` (`1,630.88` mean, `\$19,500`)—look much stronger. Could we run `L05_B` for 3 weeks to stay under \$18,000 or split across two sites?
- **Answer:** No—per the case rules, the manager must choose *one existing candidate option* for the fixed four-week (`80`-hour) trial (`Oct 12 – Nov 8, 2026`), and the listed cost is an all-inclusive fixed commitment (`\$21,000` for `L05_B`, `\$19,500` for `L01_B`, `\$19,000` for `L05_A`, `\$18,500` for `L04_B`), not a pro-rated weekly rate. Any option above `\$18,000` violates the hard budget constraint. (Though if management were ever able to raise the budget cap by `\$3,000`, `L05_B` would dominate our top contenders on both volume `1,731.40` and stability `CV = 10.00%`, trailing only lower-volume `L02_A` `7.41%`, `L05_A` `9.57%`, and `L02_B` `9.62%` on pure `CV`.)

### Q9. The proposed trial runs October 12 – November 8, 2026, yet your historical data ends September 21. How serious is seasonality risk?
- **Answer:** Seasonality is an explicit boundary condition in the case (noting `2026-09-21` is the Monday `week_start` covering `Tue Sep 22 – Sat Sep 26`, ending Sunday `Sep 27, 2026`). Checking the **Late-Season 4-Week subset (`2026-08-31` to `2026-09-21`, Sheet `04e`)** closest to October shows `L01_A` averaging **`1,370.00` (`n = 4`)** while `L04_A` averages **`1,472.67` (`n = 3`: `1,500`, `1,501`, `1,417`)**. However, two critical diagnostics temper that gap: first, `L01_A`'s late 4-week average is dragged down by one dip (`920` on `2026-08-31`), and on the **2 matched September weeks where both were observed (`09-14`, `09-21`)**, `L01_A` leads **`1,507.50`** (all `3` Sep weeks `1,520.00`) vs. **`L04_A` `1,459.00`** (`1–1` split). Second, `L04_A` was missing `2026-09-07`—a week when same-site afternoon `L04_B` (which correlates with `L04_A` at `r = 0.9902`) dropped to `1,144` (its 2nd lowest week)—so `L04_A`'s `1,472.67` (`n = 3`) vs. `L01_A`'s `1,311.67` on those same 3 weeks omits a likely weak `L04_A` date. Still, because `L01_A` has a negative overall slope (`-12.90`/wk) and landed at `1,280` on `09-21`, our pre-trial **Oct 6–10** spot check (`L01_A < 1,350` vs. `L04_A >= 1,400`, the single full Tue–Sat week in October before Oct 12 launch) protects the decision.

### Q10. Does `1,510` weekly passages mean `1,510` prospective customers per week?
- **Answer:** Definitely not. A *passage event* is a bidirectional crossing of the counting line—one person walking past twice in a shift counts as two passages. Moreover, the retailer has never operated this pop-up at any of these sites, so historical counts carry zero conversion, basket-size, or product-interest data. That is precisely why the case frames the four-week pilot as a *learning trial* rather than a guaranteed-revenue rollout.

### Q11. Given missing weeks, unexplained spikes, and unmeasured conversion, why not recommend "Wait" instead of running the trial?
- **Answer:** Because the case states that *guaranteed sales are not a prerequisite for running a trial*—the pilot is specifically intended to learn about customer engagement. Waiting only makes sense if an unresolved operational barrier prevents a responsible test. All 8 affordable options have `14–16` complete weeks (`87.5%–100%` completeness) and clear historical traffic baselines (`1,080–1,510` passages/wk). Waiting is warranted only under our explicit stop-gate triggers: if a pre-trial **Oct 6–10** count shows `< 1,100` passages/wk or `> 40%` repeat-crossing share, or if site management cannot rule out recurring closures on `L01_A`'s missing dates (`06-29`, `08-24`).

### Q12. How did you use AI tools in this project, and how did you ensure accuracy?
- **Answer:** Before starting any AI conversation, Vitaly manually cleaned and converted all course instructions into structured `.md` files (`Instructions/`), then used a structured master plan (`00_Master_Implementation_Plan.md`), modular subtask routines (`01`–`06`), and independent multi-model checks across different platforms to challenge assumptions. An AI coding assistant (Antigravity / Gemini) helped build reproducible Python unit tests (`validate_step1_data.py`–`validate_step5_package.py`), XML-validated Tableau sheets (`Vitaly_Chait_Final_Project_Workbook.twbx`, 12 sheets with titles/captions/sorts), and vector PDFs. Vitaly manually verified every part against `Deliverables/golden_metrics.json` and raw CSVs, and inspected the `.twbx` in Tableau Desktop (`https://github.com/VitalyChait/BUS240F`).

---

## 3. One-Minute Final Position Statement

"To close: within the binding **\$18,000 four-week budget cap**, we recommend authorizing **`L01_A` (Cedar Walk, Window A: Tue–Sat 10:00–14:00, \$18,000)** for the **October 12 – November 8, 2026** learning trial. Across `14` verified complete weeks (`2026-06-08` to `2026-09-21`, leaving `2` missing weeks blank rather than zero), `L01_A` leads all `8` affordable options in both **Mean (`1,510.00` passages/wk)** and **Median (`1,535.00` passages/wk)**—outperforming spike-inflated `L06_B` (`1,429.27` mean / `1,327.00` median; `1,282.62` spike-trimmed) and maintaining a full-period, `12`-week pairwise (`1,482.08` vs. `1,388.25`), and `4/4` complete 4-week rolling lead (`1,370.00–1,657.50` vs. `1,285.75–1,420.00`) over steady `L04_A` (`1,401.36` mean / `1,424.50` median).

Our sensitivity tests showed that `L04_A` (`\$17,500`, `CV = 14.59%`) overtakes `L01_A` on the `10` shared complete weeks (`1,449.70` vs. `1,407.00`) and ties weekly wins `6–6` head-to-head. Accordingly, if management prioritizes downside stability (`CV < 15%`) or an **Oct 6–10** pre-trial check shows `L01_A < 1,350` while `L04_A >= 1,400`, we switch cleanly to **`L04_A`**; and if pre-trial checks show `< 1,100` passages/wk or `> 40%` repeat-crossing share, we wait. This disciplined rule lets the retailer launch a responsible, evidence-backed learning pilot."

---

## 4. Individual Decision-Critique Memo Template & Rubric Checklist (15% of Grade)

> **Instructions:** Due within **48 hours** of the critiqued team's presentation ending. Complete independently using evidence observed during that team's live presentation and submitted brief/backup.

### Memo Header
- **Reviewer Name:** Vitaly Chait  
- **Critiqued Team:** [Team Number / Names]  
- **Presentation Date & End Time:** [Date, HH:MM Eastern]  
- **Submission Timestamp:** [Within 48 Hours of End Time]  
- **Team's Recommended Option:** [Option ID, Location, Window, Fixed Cost — or "Wait"]

### Part A: Executive Summary of Critique (3–5 Sentences)
- State whether the team's recommendation is **well-supported**, **partially supported**, or **compromised by an analytical flaw**, naming the single strongest aspect and the single most consequential gap.

### Part B: Structured Audit Across 5 Core Criteria
1. **Decision Framing & Budget Stewardship:**
   - Did the team enforce the `<= $18,000` cap and treat `total_pilot_cost_usd` as a single fixed 4-week commitment (`MIN`, not `SUM` × 16)?
   - Did they respect the single-option, fixed `Oct 12 – Nov 8` (`80`-hour) case constraint?
2. **Data Hygiene & Verification Accuracy:**
   - Did they verify baseline counts (`12` options, `192` rows = `184 Complete` + `8 Missing`, `256,773` passages) and benchmark checks (`L01_A` `06-08 = 1,175`, `06-29 = Missing`)?
   - Were the `8` missing rows kept blank/excluded from denominators rather than zero-filled?
3. **Metric Choice, Variability & Outlier Interpretation:**
   - Did they compare both central tendency (Mean vs. Median) and dispersion (`SD`, `CV`, `IQR`, `Min–Max`) rather than ranking blindly on `Raw Sum` or spike-inflated means (e.g., `L06_B`'s `2,422` and `2,343` spikes)?
   - Did they clearly compare at least one credible affordable alternative?
4. **Consequential Sensitivity Test & Visual Clarity:**
   - Did their sensitivity test (e.g., shared 10-week listwise vs. 12-week pairwise subset, median/trimmed mean, or late-season window) meaningfully challenge their ranking, and did they explain what changed (`L04_A` vs. `L01_A`, or `L06_B` drop)?
   - Were charts readable without Tableau with explicit titles, units (`passage events / 20-hr week`), timeframes, and exclusion captions?
5. **Boundaries, Unresolved Risks & Decision-Reversal Triggers:**
   - Did they avoid equating passage crossings with unique visitors, sales, or profit?
   - Did they specify concrete, quantitative evidence that would change their recommendation?

### Part C: Actionable Recommendation for the Critiqued Team
- Provide **2 specific, constructive improvements** (one analytical/sensitivity improvement and one visual/communication improvement) grounded in observed evidence from their session.

### Submission Self-Check Before Uploading (48-Hour Deadline)
- [ ] Submitted independently within 48 hours of the critiqued team's presentation ending.
- [ ] Every numerical critique cites exact observed values (no fabricated or misremembered counts).
- [ ] Explicitly evaluates data hygiene (missing vs. zero, fixed cost via `MIN`), metric validity, sensitivity testing, and measurement boundaries (`passage events` $\ne$ unique customers/sales).
- [ ] Written in crisp, professional executive prose adhering to all formatting and word-limit guidelines.
