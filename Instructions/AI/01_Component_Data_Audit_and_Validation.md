# Component 1: Data & Starter Model Audit and Validation

## Objective
Verify the raw source CSV files (`Data/Candidate_Options.csv` and `Data/Weekly_Activity.csv`) and the embedded CSVs inside `BUS240F_Final_Project_Starter.twbx` against all baseline requirements in `Instructions/final_project_data_dictionary_and_starter_guide.md`, and generate the immutable `Deliverables/golden_metrics.json` reference file used by all subsequent validation gates.

---

## Implementation Steps
1. Create `scripts/validate_step1_data.py`.
2. Load `Data/Candidate_Options.csv` and `Data/Weekly_Activity.csv`.
3. Inspect the ZIP contents of `BUS240F_Final_Project_Starter.twbx` and compare `Data/Prototype/Candidate_Options.csv` and `Data/Prototype/Weekly_Activity.csv` byte-for-byte (normalizing CRLF/LF line endings) against `Data/Candidate_Options.csv` and `Data/Weekly_Activity.csv`.
4. Compute all option-level metrics across:
   - **Full observed period** (`2026-06-08` through `2026-09-21`, $n \in \{14, 15, 16\}$)
   - **Shared 10-week affordable subset** (excluding `2026-06-22`, `2026-06-29`, `2026-07-20`, `2026-08-10`, `2026-08-24`, `2026-09-07`)
   - **Shared 9-week all-options subset** (additionally excluding `2026-07-27`)
   - **Late-season 4-week subset** (`2026-08-31`, `2026-09-07`, `2026-09-14`, `2026-09-21`)
   - **Spike-trimmed subset for `L06_B`** (removing `2026-07-06` = `2,422` and `2026-08-17` = `2,343`, leaving $n=13$ weeks with mean `1,282.62`).
5. Save the verified metrics to `Deliverables/golden_metrics.json` and a human-readable audit log to `Deliverables/verification_audit_summary.md`.

---

## Validation Gate 1 Checklist (Must Pass 100% Before Component 2)
- [ ] **Check 1.1 (Options Count):** `Candidate_Options.csv` has exactly `12` rows and `12` distinct `option_id` values (`L01_A`..`L06_B`).
- [ ] **Check 1.2 (Uniform Trial Parameters):** Every option has `scheduled_hours_per_week == 20` and `pilot_weeks == 4`.
- [ ] **Check 1.3 (Weekly Record Count):** `Weekly_Activity.csv` has exactly `192` rows (`12 options × 16 weeks`, Mondays from `2026-06-08` to `2026-09-21`).
- [ ] **Check 1.4 (Completeness Split):** Exactly `184` rows have `observation_status == 'Complete'` (with positive integer `observed_passages`) and `8` rows have `observation_status == 'Missing'` (with blank/null `observed_passages`, never zero).
- [ ] **Check 1.5 (Representative Source Rows):**
  - `L01_A` on `2026-06-08` has `observation_status == 'Complete'` and `observed_passages == 1175`.
  - `L01_A` on `2026-06-29` has `observation_status == 'Missing'` and `observed_passages` is null/blank.
- [ ] **Check 1.6 (Budget Rule):** `total_pilot_cost_usd <= 18000` classifies exactly `8` options as `Within Budget = True` (`L01_A`, `L02_A`, `L02_B`, `L03_A`, `L03_B`, `L04_A`, `L06_A`, `L06_B`) and `4` options as `False` (`L04_B`, `L05_A`, `L01_B`, `L05_B`).
- [ ] **Check 1.7 (Starter Package Parity):** Embedded CSVs inside `BUS240F_Final_Project_Starter.twbx` match standalone CSVs 100%.
- [ ] **Check 1.8 (Baseline Reference Table Parity):** All 12 option metrics (`ROUND_HALF_UP`), sensitivity subsets (`10-Wk`, `9-Wk`, `8-Wk Non-Spike`, `Late 4-Wk`, `Sep 3-Wk`, `Spike-Trimmed`), `12-Wk` pairwise uncertainty stats, Window A/B correlations, and complete `n=4` rolling 4-week blocks match 100%.
