# Component 1 Verification & Audit Summary

## Dataset & Starter Snapshot Checks

| Validation Check | Status | Details |
| :--- | :---: | :--- |
| Check 1.1 (Options Count) | **PASS** | rows=12, distinct=12 |
| Check 1.2 (Uniform Trial Parameters) | **PASS** | hours_unique=[20], pilot_weeks_unique=[4] |
| Check 1.3 (Weekly Record Count) | **PASS** | rows=192, weeks=16 |
| Check 1.4 (Completeness Split) | **PASS** | Complete=184, Missing=8, missing_null=True |
| Check 1.5 (Representative Source Rows) | **PASS** | L01_A 2026-06-08=1175 Complete; L01_A 2026-06-29=Missing/null |
| Check 1.6 (Budget Rule) | **PASS** | within_budget=8, over_budget=4 |
| Check 1.7 (Starter Package Parity) | **PASS** | Embedded CSVs match Data/*.csv 100% |
| Check 1.8 (Baseline Reference Table Parity) | **PASS** | All 12 options, sensitivity subsets, pairwise 12-wk & rolling 4-wk benchmarks match 100% |

## Global Model Verification Totals

- **Candidate Options:** `12` (`8` Within Budget <= $18,000; `4` Over Budget)
- **Weekly Activity Rows:** `192` (`184 Complete` + `8 Missing`; `7` missing among affordable options, `1` over-budget)
- **Grand Total Observed Passages (`SUM(Observed Passages)`):** `256,773`
- **Representative Row Checks (`L01_A`):** `2026-06-08` = `Complete` (`1,175`), `2026-06-29` = `Missing` (null/blank)

## Verified Metrics Across All 12 Candidate Options

| Option | Location | Win | 4-Wk Cost | Budget | Obs (n) | Miss | Raw Sum | Mean | Median | SD | CV (%) | IQR | Min–Max | 10-Wk Mean | 9-Wk Mean | Late 4-Wk Mean |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `L01_A` | Cedar Walk | A | $18,000 | True | 14 | 2 | 21,140 | 1,510.00 | 1,535.00 | 302.58 | 20.04% | 477.50 | 920–1,970 | 1,407.00 | 1,423.33 | 1,370.00 |
| `L06_B` | Aspen Court | B | $16,000 | True | 15 | 1 | 21,439 | 1,429.27 | 1,327.00 | 470.64 | 32.93% | 554.50 | 840–2,422 | 1,619.10 | 1,649.44 | 1,420.00 |
| `L04_A` | Birch Arcade | A | $17,500 | True | 14 | 2 | 19,619 | 1,401.36 | 1,424.50 | 204.49 | 14.59% | 281.75 | 978–1,721 | 1,449.70 | 1,455.56 | 1,472.67 (n=3) |
| `L02_B` | Maple Court | B | $16,500 | True | 15 | 1 | 19,886 | 1,325.73 | 1,316.00 | 127.56 | 9.62% | 161.00 | 1,120–1,592 | 1,304.10 | 1,290.00 | 1,281.25 |
| `L02_A` | Maple Court | A | $15,000 | True | 16 | 0 | 20,009 | 1,250.56 | 1,249.00 | 92.62 | 7.41% | 112.50 | 1,110–1,457 | 1,239.40 | 1,229.33 | 1,228.75 |
| `L06_A` | Aspen Court | A | $14,500 | True | 16 | 0 | 18,719 | 1,169.94 | 1,170.00 | 156.76 | 13.40% | 267.50 | 915–1,390 | 1,240.60 | 1,247.00 | 1,222.50 |
| `L03_B` | Willow Square | B | $13,500 | True | 16 | 0 | 18,519 | 1,157.44 | 1,164.00 | 151.04 | 13.05% | 250.50 | 943–1,426 | 1,172.10 | 1,148.67 | 1,092.50 |
| `L03_A` | Willow Square | A | $12,000 | True | 15 | 1 | 16,211 | 1,080.73 | 1,102.00 | 111.94 | 10.36% | 182.50 | 934–1,263 | 1,089.20 | 1,070.11 | 1,032.25 |
| `L05_B` | Juniper Row | B | $21,000 | False | 15 | 1 | 25,971 | 1,731.40 | 1,757.00 | 173.19 | 10.00% | 220.00 | 1,490–2,053 | 1,744.11 (n=9) | 1,744.11 | 1,790.00 |
| `L01_B` | Cedar Walk | B | $19,500 | False | 16 | 0 | 26,094 | 1,630.88 | 1,679.00 | 347.68 | 21.32% | 509.25 | 1,035–2,237 | 1,536.10 | 1,551.00 | 1,490.00 |
| `L05_A` | Juniper Row | A | $19,000 | False | 16 | 0 | 25,651 | 1,603.19 | 1,590.00 | 153.50 | 9.57% | 217.00 | 1,365–1,878 | 1,605.90 | 1,620.78 | 1,670.00 |
| `L04_B` | Birch Arcade | B | $18,500 | False | 16 | 0 | 23,515 | 1,469.69 | 1,513.50 | 237.86 | 16.18% | 313.25 | 992–1,884 | 1,546.60 | 1,553.00 | 1,455.00 |

*Note: Means use standard half-up rounding (`ROUND_HALF_UP`) to match Tableau display formatting. IQR uses continuous linear interpolation (`PERCENTILE.INC`); Tableau default Tukey hinges give `485.00` for `L01_A` and `309.00` for `L04_A`. In `10-Wk Mean`, over-budget `L05_B` missed `2026-07-27` (`n=9`); in `Late 4-Wk Mean`, `L04_A` missed `2026-09-07` (`n=3`).*

## Key Sensitivity Benchmarks

- **L06_B Spike-Trimmed (`n=13`, excluding `2026-07-06`=2,422 and `2026-08-17`=2,343):** Mean = `1,282.62`, Median = `1,274.00`, SD = `288.83`
- **Shared 10-Week Affordable Subset (`n=10` complete weeks across all 8 affordable options):** `L04_A` Mean = `1,449.70` (Median `1,458.50`) vs. `L01_A` Mean = `1,407.00` (Median `1,390.00`)
- **Direct Pairwise Head-to-Head (`L01_A` vs. `L04_A`, `n=12` weeks where both have complete counts):** `L01_A` Mean = `1,482.08` (Median `1,512.50`) vs. `L04_A` Mean = `1,388.25` (Median `1,407.00`); weekly wins split `6–6` (mean diff `+93.83`, median diff `-1.50`, `SE = 132.17`, `t = 0.71`)
- **Shared 8-Week Non-Spike Subset (`n=8`, excluding 6 missing-overlap weeks + `07-06` & `08-17` spikes):** `L04_A` Mean = `1,497.13` (Median `1,500.50`) vs. `L06_B` Mean = `1,428.25` and `L01_A` Mean = `1,368.75`
- **September & Late-Season Shared-Week Checks (Strictly Matched Weeks):** Across `n=2` shared September weeks (`09-14`, `09-21`), `L01_A` Mean = `1,507.50` vs. `L04_A` = `1,459.00` (`1–1` wins; `L01_A` all `n=3` Sep = `1,520.00`). Across `n=3` shared Late 4-Wk dates (`08-31`, `09-14`, `09-21`), `L01_A` Mean = `1,311.67` (`n=4` = `1,370.00`) vs. `L04_A` = `1,472.67` (noting `L04` A/B correlate at `r = 0.9902` and `L04_B` dropped to `1,144` on `L04_A`'s missing `09-07` date).
- **Complete 4-Week Rolling Block Ranges (`n=4` complete weeks per block only):** `L01_A` = `1,370.00–1,657.50` (`5/13` blocks) vs. `L04_A` = `1,285.75–1,420.00` (`7/13` blocks); `L01_A` led `4/4` simultaneous complete 4-week blocks.
