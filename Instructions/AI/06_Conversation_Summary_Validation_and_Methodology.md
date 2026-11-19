# BUS 240F Final Project — Conversation Summary, Validations, Pushback & Engineering Methodology

**Repository:** `https://github.com/VitalyChait/BUS240F`  
**Scope:** End-to-end record of the human-driven context engineering, cross-platform multi-model stress testing, verifiable unit-testing architecture, manual audits, user pushback, and iterative refinements across Components 1–5.

---

## 1. Pre-LLM Preparation & Context Engineering (Manual `.md` Transformation)

Before initiating any conversation with the coding LLM, **I (Vitaly Chait) manually cleaned, normalized, and converted all raw project files into clean Markdown (`.md`) files** inside `Instructions/`:

- `Instructions/final_project_case_background.md`
- `Instructions/final_project_data_dictionary_and_starter_guide.md`
- `Instructions/final_project_start_here_guide.md`
- `Instructions/project_checkpoint_template.md`

### Why This Upfront Context Engineering Mattered
- **Human & Machine Readability:** Converting cluttered source handouts/documents into structured `.md` files stripped layout noise, normalized tables and constraints, and made every rule unambiguously parseable by both humans and LLMs.
- **Zero Premature Ambiguity:** Having clean `.md` specifications before the first LLM prompt enabled deterministic decomposition into a master implementation plan (`00_Master_Implementation_Plan.md`) and five modular component subtask routines (`01` through `05`) rather than ad-hoc prompting.
- **Grounding Against Source Data:** Alongside the cleaned `.md` specs, raw CSV extracts (`Data/Candidate_Options.csv` and `Data/Weekly_Activity.csv`) were verified directly against the starter workbook (`BUS240F_Final_Project_Starter.twbx`).

---

## 2. Cross-Platform & Multi-Model Assumption Testing

Rather than relying on a single LLM session or accepting first-pass outputs at face value, **Vitaly frequently used additional frontier AI models across separate platforms to independently test, challenge, and validate core assumptions** before and during execution:

- **Statistical & Modeling Assumptions:** Cross-checked how missing weeks (`8` blank rows out of `192`) must be treated (`NULL` excluded from `AVG`/`MEDIAN` denominators rather than zero-imputed), how `Total Pilot Cost Usd` behaves across a one-to-many join (`MIN(Total Pilot Cost Usd)` to avoid 16x inflation), and when sensitivity subsets introduce survivor/exclusion bias.
- **Tableau Packaging & XSD Constraints:** Independently validated Tableau `.twb`/`.twbx` XML schema rules, `<datasource-dependencies>` ordering, `<filter>`/`<slices>` parity, and `MIN(...)` vs. `SUM(...)` grain safety prior to automated XML generation.
- **Adversarial & Non-Technical Critique:** Used separate model passes and human inspection to surface edge cases (such as the shared-10-week outlier paradox) and to audit whether executive summaries remained understandable to a non-technical reader.

---

## 3. Verifiable Architecture: Master Plan, Subtask Routines & Unit Testing

Every deliverable was built under a **verifiable, unit-tested engineering workflow** with mandatory manual verification by Vitaly at every stage:

### Modular Plan & Subtask Routines (`Instructions/AI/`)
1. `00_Master_Implementation_Plan.md` — Master execution table, baseline metric oracle, and gating rules.
2. `01_Component_Data_Audit_and_Validation.md` — Raw CSV & starter `.twbx` parity audit (`Deliverables/golden_metrics.json`, `Deliverables/verification_audit_summary.md`).
3. `02_Component_Tableau_Workbook_and_Validation.md` — Programmatic Tableau workbook synthesis (`Vitaly_Chait_Final_Project_Workbook.twbx`).
4. `03_Component_Checkpoint_PDF_and_Validation.md` — 1-page Milestone 1 Checkpoint (`Vitaly_Chait_Project_Checkpoint.pdf`).
5. `04_Component_Final_PDF_Package_and_Validation.md` — 2-page Executive Decision Brief (`Vitaly_Chait_Two_Page_Brief.pdf`) and 4-page Landscape Backup (`Vitaly_Chait_Static_View_Backup.pdf`).
6. `05_Component_Presentation_Defense_and_Validation.md` — Presentation script, Q&A defense playbook, and critique template (`Deliverables/Presentation_and_Defense_Guide.md`).

### Single Source of Truth + Automated Unit Tests (`37` Checks Total)
- **Single Metric Oracle:** `Deliverables/golden_metrics.json` stores exact pre-verified integers, floats, subset counts, and representative spot-checks (`L01_A` on `2026-06-08 = 1,175`, `2026-06-29 = Missing`), preventing numerical drift across files.
- **Uncompressed PDF Stream Inspection (`pageCompression=0`):** ReportLab PDFs are written with uncompressed text streams so automated Python unit tests can directly extract and verify every page count, section heading, metric string, and missing-placeholder rule without fragile OCR approximations.
- **37 Unit Checks Across 5 Validators:**
  - `scripts/validate_step1_data.py` (**8 checks:** `Check 1.1`–`Check 1.8`) — CSV counts, uniform parameters, `192 = 184 + 8` split, starter `.twbx` byte/content parity, full 12-option metric table.
  - `scripts/validate_step2_twbx.py` (**18 checks:** `Check 2.1`–`Check 2.18`) — ZIP integrity, embedded CSV byte-for-byte parity, XML root/XSD tag order, `<object-graph>` join, calculated fields, `<column>`/`<column-instance>` declarations, `<filter>`/`<slices>` parity, `<pane>` structure, unique uppercase UUIDs.
  - `scripts/validate_step3_checkpoint.py` (**5 checks:** `Check 3.1`–`Check 3.5`) — PDF validity, strict `1`-page limit, all required sections + completed narrative template, zero unfilled `[...]` placeholders, 100% metric parity.
  - `scripts/validate_step4_final_pdfs.py` (**4 checks:** `Check 4.1`–`Check 4.4`) — Strict `2`-page Brief limit, `4`-page annotated Backup completeness, verification/stewardship & AI disclosure tokens, cross-PDF metric parity.
  - `scripts/validate_step5_package.py` (**2 checks:** `Check 5.1`–`Check 5.2`) — Re-runs Validators 1–4 end-to-end and cross-checks `21` core metrics, `9` sensitivity benchmarks, and `18` defense benchmarks across all deliverables.
- **Manual Verification on Every Part:** Vitaly personally reviewed generated artifacts at each stage—including inspecting `Vitaly_Chait_Final_Project_Workbook.twbx` inside **Tableau Desktop** at Gate 2B and visually checking rendered PDF pages.

---

## 4. Chronological Summary of Conversations, Pushback & Iterative Validations

### Stage 1 — Plan Execution, Initial Bug Fixes & Gate 2B Tableau Inspection
- **Execution:** Implemented and validated Components 1 through 5 sequentially using `scripts/build_step*.py` and `scripts/validate_step*.py`.
- **Technical Fixes Caught During Unit Testing & Layout:**
  - Resolved initial vertical page overflow in `scripts/build_step3_checkpoint.py` by tightening typography (`7.0 pt` body / `6.9 pt` callout) and sizing `chart_h = 282.0` (maintaining positive bottom margin on Page 1).
  - Fixed regex double-bracketing (`[[field]]`) in `Check 2.14` of `scripts/validate_step2_twbx.py` when parsing calculated-field references.
- **Human Gate 2B Validation:** Paused after Component 2 for Vitaly to open `Vitaly_Chait_Final_Project_Workbook.twbx` in Tableau Desktop and confirm all worksheets, numbers, and layouts matched expectations (`"I validated the file and it looks good"`).

### Stage 2 — Adversarial Audit #1 & Vitaly's Pushback on Readability
Following completion of Components 1–5, Vitaly requested a strict re-validation to uncover data edge cases, visual defects, and areas of improvement ranked by priority. That audit surfaced several real issues, combined with explicit pushback from Vitaly on writing style:

1. **Discovery of the Shared-10-Week Spike Paradox & September Rebound:**
   - Auditing why `L06_B` jumped to `1,619.10` in the `10-week` shared-affordable subset (`1,649.44` in `9-week` shared-all) showed that excluding the 6 missing-overlap dates removed **5 of `L06_B`'s slowest weeks (`840–1,274`)** while retaining **both isolated spikes (`2,422` on `07-06` and `2,343` on `08-17`)**. Adding an `8-week non-spike` test showed `L04_A` leading all affordable options (`1,497.12` mean vs. `L06_B` `1,428.25` and `L01_A` `1,368.75`).
   - Auditing `L01_A`'s `late_4wk_mean` (`1,370.00` vs. `L04_A` `1,472.67`) isolated that the drop came from a single low week (`920` on `2026-08-31`), followed by a `1,520.00` mean across the 3 September weeks (`1,545; 1,735; 1,280`).
2. **Visual & Layout Defects Fixed via Rendered PDF Inspection:**
   - Shortened chart titles and adjusted legend offsets where top-right chart legends collided with titles.
   - Widened the left column (`130.0 pt`) on Page 1 of `Vitaly_Chait_Static_View_Backup.pdf` so location names rendered in full rather than truncated (`[:10]`).
   - Adjusted bar value precision to 2 decimals (`1,510.00`) on Brief Page 2 to match all tables and avoid rounding ambiguity (`1,510` vs. `1,510.00`), and shrank Backup Page 4 callout text (`6.8 pt`) to eliminate clipping.
3. **Vitaly's Pushback — Simplicity, Non-Technical Clarity & Font Size:**
   - Vitaly pushed back that the initial executive summaries were **too dense/compact and too technical** for a general non-technical audience.
   - **Action Taken:** Lowered body font sizes (`~6.8–7.1 pt`) to give paragraphs breathing room on fixed 1-page / 2-page PDFs, and rewrote `Vitaly_Chait_Two_Page_Brief.pdf` and `Vitaly_Chait_Project_Checkpoint.pdf` into straightforward, plain-English prose explaining *why* metrics matter (e.g., `"typical middle week"` alongside `"average"`, `"apples-to-apples shared weeks"`, `"passage events / crossings"`) without jargon.

### Stage 3 — Adversarial Audit #2 & Targeted High-Priority Fixes
After the simplification rewrite, Vitaly ran a second validation pass and selected three prioritized fixes for implementation:

- **Priority 2 (High — Tableau `01 Verify the Model` Ambiguity):** Added calculated field `Scheduled Weekly Records` (`COUNT([week_start])`, `CALC_SCHED_RECS`) to `scripts/build_step2_twbx.py` and displayed it alongside `CNT(Observed Passages)` and `SUM(Observed Passages)` so readers immediately see why the `Missing` row reflects `8` scheduled records with `0` observed counts (`184 + 8 = 192`).
- **Priority 4 (Medium — Leader Line Crossing on Backup Page 3):** Attempted updating the `L04_A Steady Corridor` annotation offset (`dx=-205, dy=128`) in `scripts/build_step4_final_pdfs.py`, which reduced clutter but still crossed `L01_A`'s blue trajectory between `09-07` and `09-14` until fully resolved in Stage 6 (`w_idx=11`, `08-24`, `dx=4, dy=152`).
- **Priority 5 (Medium-Low — Data Governance Parity):** Promoted the `shared_8wk_nonspike` (`obs`, `mean`, `median`) and `sep_3wk` (`obs`, `mean`, `median`) metrics into `Deliverables/golden_metrics.json` (and `scripts/validate_step1_data.py`) so secondary sensitivity findings were governed by the same single source of truth as primary metrics.

### Stage 4 — Final Editorial Polish & Attribution
In the refinement passes, Vitaly tightened presentation language and attribution:

- **Checkpoint PDF (`scripts/build_step3_checkpoint.py`):**
  1. Replaced raw formula labels (`Average (AVG(Observed Passages))` / `Typical Middle Week (MEDIAN(Observed Passages))`) with plain English: **`Average Observed Passages and the Typical (Median) Middle Week Observed Passages`**.
  2. Replaced `MIN(Total Pilot Cost Usd)` in prose with **`The minimum of Total Pilot Cost Usd`**.
  3. Reformatted **`Suggested Narrative Template (Completed)`** into 4 scannable bullets: **`Decision`**, **`Measurement`**, **`View`**, and **`TODO`**.
- **Two-Page Brief (`scripts/build_step4_final_pdfs.py`):**
  - Converted **`Verification Notes, Data Hygiene & AI Assistance Disclosure`** on Page 2 into 3 structured bullets (**Data Check & Fixed Snapshot**, **Spot Checks, Cost Rule & IQR Note**, **AI Assistance Disclosure**).
  - Updated the AI disclosure to replace `"the author"` with **`I (Vitaly)`**, explicitly document the upfront **`.md` file conversion**, the **master plan + modular subtask routines + verifiable unit-testing architecture**, **manual verification on every part**, and the public GitHub repository (`https://github.com/VitalyChait/BUS240F`).

### Stage 5 — Comprehensive End-to-End Content, Tableau & Statistical Validation
A full-project adversarial validation prioritizing content and analytical accuracy surfaced 10 further improvements, all implemented and re-verified:

1. **Direct Pairwise Test (`12` Shared `L01_A` / `L04_A` Weeks):** Added the direct `n=12` pairwise comparison (`L01_A = 1,482.08` mean / `1,512.50` median vs. `L04_A = 1,388.25` mean / `1,407.00` median; `6–6` weekly wins), exposing how listwise deletion in the 10-week and 8-week subsets removed `07-20`, `08-10`, `07-06`, and `08-17`—the exact 4 weeks where `L01_A` outpaced `L04_A` by its widest margins.
2. **Corrected `L06_B` Slowest-Weeks Claim:** Fixed `"5 slowest weeks"` / `"5 lowest summer weeks"` to **`"5 of L06_B's 7 slowest weeks (840–1,274; keeping 1,024 and 1,170 in)"`**.
3. **Apples-to-Apples September Rebound:** Fixed Q9/summaries to compare `L01_A` (`1,520.00`, `n=3`) directly against **`L04_A`'s exact same September 3-week mean (`1,459.00`, `n=2`)** alongside `L04_A`'s Late 4-Week average (`1,472.67`).
4. **Window B Premium, 4-Week Rolling Risk & Non-Technical Glossary:** Added Window B > Window A at all 6 locations (`+$68` to `+$259`/wk at `+$1k–$2k`), 4-week rolling risk (`L01_A` `1,236.67–1,790.00` vs. `L04_A` `1,285.75–1,516.67`), plain-English expansions of `SD`/`CV`/`IQR` + `PERCENTILE.INC` vs. Tableau Tukey hinges, `Week Start` Monday clarifications (`Jun 8 – Sep 27, 2026`), and `L05_B` `(n=9)` annotation in `10-Wk Mean` tables.
5. **Tableau Workbook (`.twbx`) Parity, 18.1 DTD Titles/Captions & Sorts:** Added `<layout-options>` (`<title>` and `<caption>`) + bottom caption cards, `<sort class='computed'>` rankings (switching from `2026_1` XSD `<manual-sort>` after Tableau Desktop DTD error `D2E8DA72` confirmed `version='18.1'` expects `<sort>`), `Weekly SD`/`Weekly CV`/`Pairwise`/`8-Wk Non-Spike` calculated fields, and 3 new worksheets (`02b`, `04b`, `04c`, bringing the workbook to `9` verified sheets), alongside expanded automated assertions in `validate_step1_data.py`–`validate_step5_package.py` and typo fixes in `README.md`.

### Stage 6 — Rigorous Fallacy, Visual Collision & Workbook Parity Audit Fixes
A full forensic re-audit from `Instructions/final_project_start_here_guide.md` through every deliverable, script, `.twbx` XML node, and rendered PDF image uncovered and resolved the following concrete errors:

1. **Strict Complete `n=4` Rolling 4-Week Blocks:** Fixed `scripts/validate_step1_data.py` (`len(block_vals) == 4`) so rolling 4-week metrics no longer average partial `n=3` missing-week blocks (`1,236.67`, `1,790.00`, `1,516.67`, `1,720.00`, `1,432.33`); true complete 4-week blocks show `L01_A` (`1,370.00–1,657.50`, `5/13`) leading `L04_A` (`1,285.75–1,420.00`, `7/13`) on all `4/4` simultaneous blocks.
2. **Strictly Matched September / Late-Season Diagnostics & Missingness Bias:** Replaced unequal `"same 3 September weeks (n=3 vs n=2)"` prose with matched `n=2` September (`09-14`, `09-21`: `L01_A 1,507.50` vs. `L04_A 1,459.00`) and matched `n=3` Late (`1,311.67` vs. `1,472.67`), annotated `L04_A` `(n=3)` in `Late 4-Wk` tables, documented Window A/B correlation (`L04 r = 0.9902`, `L04_B = 1,144` on `L04_A`'s missing `09-07`), and documented `12-Wk` paired uncertainty (`6–6` wins, median diff `-1.50`, `SE = 132.17`, `t(11) = 0.71`).
3. **Half-Up Rounding Parity (`1,497.13`) & Realistic Pre-Trial Timing (`Oct 6–10`):** Switched mean rounding in `validate_step1_data.py` to `ROUND_HALF_UP` so `L04_A`'s 8-week non-spike mean (`1,497.13`) matches Tableau Desktop exactly, clarified Q8 stability rank (`CV = 10.00%` is 4th overall), and aligned pre-trial checks to `Oct 6–10` (the single full Tue–Sat week between `Sep 28` and `Oct 12`).
4. **Tableau `.twbx` Fixes (`12` Sheets):** Added `<sort class='computed' direction='ASC' using='MIN(Total Pilot Cost Usd)'>` on `[Within Budget]` in `01b`, `02`, `02b` (putting `True` above `False`), fixed Sheet `04c`'s false `"two peak L01_A weeks (07-06=1,875, 08-17=1,245)"` caption, expanded `02b` to all `10` Tableau-aggregated metrics, and added `04d` (`Shared 9-Wk`), `04e` (`Late 4-Wk`), and `04f` (`L06_B Spike-Trimmed`) matching PDF sensitivity views.
5. **Visual PDF Collision Fixes & Homework Alignment:** Fixed the `AFFORDABLE...` red divider overlap on `L03_A` (Two-Page Brief Page 1 and Checkpoint Page 1), eliminated the `L04_A Steady` leader-line crossing on Static Backup Page 3 (`w_idx=11, dx=4, dy=152`), fixed Checkpoint Section 5 vs. `TODO` contradiction, and added a 4-member team presentation/defense speaking allocation in `Deliverables/Presentation_and_Defense_Guide.md`.

---

## 5. Summary of Key Lessons Applied

1. **Human Context Engineering First:** Cleaning and translating messy project specs into structured `.md` files *before* prompting dramatically improves downstream accuracy and modularity.
2. **Independent Triangulation Beats Single-Pass Generation:** Testing assumptions across multiple models/platforms alongside deterministic CSV scripts catches subtle traps (`MIN` vs. `SUM` cost, missing-date exclusion bias, outlier skew) early.
3. **Verifiable Contracts Prevent Regression:** Combining a single JSON oracle (`golden_metrics.json`), uncompressed PDF stream assertions, XML schema validators, and mandatory human visual gates guarantees that late copy edits never break numeric parity or page-count constraints.
