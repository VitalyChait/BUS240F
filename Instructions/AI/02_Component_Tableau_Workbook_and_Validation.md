# Component 2: Packaged Tableau Workbook (`.twbx`) Engineering, Deep XML Validation & Mandatory User Approval Gate

## Objective
Create a rock-solid, fully populated Packaged Tableau Workbook (`Vitaly_Chait_Final_Project_Workbook.twbx`) built directly from `BUS240F_Final_Project_Starter.twbx`. The workbook must preserve the starter's relational object model (`Candidate_Options.csv` related to `Weekly_Activity.csv` on `option_id`), contain zero missing or malformed XML tags, pass an 18-point automated XML/schema validation suite, and **pass manual inspection and explicit approval by the user in Tableau Desktop before moving to Component 3**.

---

## Planned Worksheets in `Vitaly_Chait_Final_Project_Workbook.twbx` (12 Worksheets with Titles, Captions & Ranked Sorts)

1. **`01 Verify the Model`**
   - **Purpose:** Baseline model verification required by Section 4 of the Data Dictionary & Starter Guide.
   - **Structure:** `Observation Status` on Rows (`Complete` = 184, `Missing` = 8), showing `Scheduled Weekly Records` (`COUNT([week_start])` = `192` total), `COUNT(Observed Passages)` (`184`), and `SUM(Observed Passages)` (`256,773` total passages across all 12 options).
2. **`01b Option Cost & Completeness Audit`**
   - **Purpose:** Verify all 12 candidate options (`Within Budget` sorted `ASC` by `MIN(Total Pilot Cost Usd)` so `True` appears above `False`; options sorted descending by fixed cost), single fixed 4-week cost (`MIN(Total Pilot Cost Usd)`), observed weeks (`COUNT(Observed Passages)` = 14..16), and scheduled rows (`16`).
3. **`01c Representative Source Check (L01_A)`**
   - **Purpose:** Directly verify the starter guide's two benchmark rows for `L01_A`: week starting `2026-06-08` (`Complete`, `1,175` passages) and week starting `2026-06-29` (`Missing`, blank count).
4. **`02 Build the Decision`**
   - **Purpose:** Primary decision bar view comparing all 12 candidate options grouped by `Within Budget` (`True` sorted above `False`, ranked descending by performance), displaying `AVG(Observed Passages)`, `MEDIAN(Observed Passages)`, with `Weekly SD`, `Weekly CV`, `MIN(Total Pilot Cost Usd)`, and `COUNT(Observed Passages)` in tooltip/LOD.
5. **`02b Dispersion & Cost Metrics Table`**
   - **Purpose:** Exact numerical cross-tab showing `MIN(Total Pilot Cost Usd)`, `COUNT(Observed Passages)`, `Missing Weekly Records`, `SUM(Observed Passages)`, `AVG`, `MEDIAN`, `Weekly SD`, `Weekly CV`, `MIN(Observed Passages)`, and `MAX(Observed Passages)` in ranked order matching the Two-Page Brief Page 1 table (with caption documenting `PERCENTILE.INC` vs. Tukey hinge IQR).
6. **`03 Weekly Trajectory & Outliers`**
   - **Purpose:** Weekly time-series across the 16 historical weeks (`2026-06-08` to `2026-09-21`, covering `Jun 8 – Sep 27, 2026`) filtered to the 8 affordable options, visually revealing `L06_B`'s two extreme spikes (`2,422` and `2,343`), `L01_A`'s `08-31` dip (`920`), and missing-week breaks.
7. **`04 Shared-Week Sensitivity Test`**
   - **Purpose:** Tests the 10-week all-affordable subset (`Shared 10-Week Affordable Flag`), showing `L04_A` (`1,449.70`) overtaking `L01_A` (`1,407.00`) when all 6 missing-overlap dates are removed.
8. **`04b Pairwise L01_A vs L04_A (12 Wk)`**
   - **Purpose:** Direct head-to-head filter (`Pairwise L01_A vs L04_A Flag`) over all `12` weeks where BOTH `L01_A` and `L04_A` are complete, proving `L01_A` leads `1,482.08` to `1,388.25`.
9. **`04c Shared 8-Wk Non-Spike Audit`**
   - **Purpose:** Top-4 contenders across the `8` non-spike shared weeks (`Shared 8-Week Non-Spike Flag`), matching Tableau half-up precision (`L04_A 1,497.13`, `L06_B 1,428.25`, `L01_A 1,368.75`).
10. **`04d Shared 9-Wk All-Options Audit`**
    - **Purpose:** Tests the `9`-week all-12-complete subset (`Shared 9-Week All-Options Flag`), verifying Brief Page 2 & Backup View 4 (`L06_B 1,649.44`, `L04_A 1,455.56`, `L01_A 1,423.33`).
11. **`04e Late 4-Wk Seasonality Check`**
    - **Purpose:** Evaluates `Aug 31 – Sep 21` (`Late 4-Week Flag`) across the 8 affordable options (`L04_A 1,472.67` at `n=3`, `L06_B 1,420.00`, `L01_A 1,370.00`).
12. **`04f L06_B Spike-Trimmed Check`**
    - **Purpose:** Excludes `L06_B`'s two summer spikes (`07-06=2,422`, `08-17=2,343`) via `L06_B Non-Spike Flag`, proving `L06_B` falls to `1,282.62` (`n=13`) behind `L04_A` (`1,401.36`) and `L02_B` (`1,325.73`).

---

## Strict Tableau 18.1 / 2025.2 XML Engineering Rules (Zero Missing Tags)

To guarantee that Tableau Desktop loads the `.twbx` without any schema errors or missing-tag warnings:

1. **Exact Root & Manifest Preservation:**
   - Keep `<?xml version='1.0' encoding='utf-8' ?>` and root attributes `original-version='18.1' source-build='2025.2.1 (20252.25.0710.1712)' source-platform='mac' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'`.
   - Keep all 7 flags in `<document-format-change-manifest>` (`AnimationOnByDefault`, `MarkAnimation`, `ObjectModelEncapsulateLegacy`, `ObjectModelTableType`, `SchemaViewerObjectModel`, `SheetIdentifierTracking`, `WindowsPersistSimpleIdentifiers`).
2. **Strict `<datasource>` Child Ordering:**
   - Inside `<datasource caption='Weekly_Activity+' inline='true' name='federated.1uzq3s41802ykr10f4fc80617xzf' version='18.1'>`:
     1. `<connection class='federated'>` (unchanged from starter)
     2. `<aliases enabled='yes' />`
     3. `<column ...>` declarations (all starter columns + new calculated fields)
     4. `<column-instance ...>` declarations
     5. `<layout dim-ordering='alphabetic' measure-ordering='alphabetic' show-structure='true' />`
     6. `<style>`
     7. `<semantic-values>`
     8. `<object-graph>` (unchanged from starter, preserving relationship `[option_id (Candidate_Options.csv)] = [option_id]`)
3. **Strict `<worksheet>` Child Ordering & Dependency Completeness:**
   - Every `<worksheet name='...'>` must contain:
     - `<layout-options>` containing `<title>` and `<caption>` (`<formatted-text><run ...>...</run></formatted-text>`)
     - `<table>`
       - `<view>`
         - `<datasources><datasource caption='Weekly_Activity+' name='federated.1uzq3s41802ykr10f4fc80617xzf' /></datasources>`
         - `<datasource-dependencies datasource='federated.1uzq3s41802ykr10f4fc80617xzf'>` containing:
           - Every `<column>` referenced anywhere in the worksheet (ordered before `<column-instance>`)
           - Every `<column-instance>` referenced in `<rows>`, `<cols>`, `<encodings>`, `<filter>`, or `<sort>`
         - Optional `<filter class='categorical' column='[federated...].[...]' ...>`
         - Optional `<sort class='computed' column='[federated...].[...]' direction='DESC' using='[federated...].[...]' />`
         - Mandatory `<slices><column>[federated...].[...]</column></slices>` whenever one or more `<filter>` tags exist in `<view>`
         - `<aggregation value='true' />` (always last inside `<view>`)
       - `<style />`
       - `<panes><pane selection-relaxation-option='selection-relaxation-allow'><view><breakdown value='auto' /></view><mark class='...' />...</pane></panes>`
       - `<rows>...</rows>`
       - `<cols>...</cols>`
     - `<simple-id uuid='{...}' />`
4. **Strict `<windows>` Parity:**
   - Every `<worksheet name='...'>` in `<worksheets>` must have a matching `<window class='worksheet' name='...'>` in `<windows source-height='30'>` with complete `<cards>` (`left` edge: `pages`, `filters`, `marks`; `top` edge: `columns`, `rows`, `title`; `bottom` edge: `caption`) and a unique `<simple-id uuid='{...}' />`.

---

## Validation Gate 2A: Automated 18-Point `.twbx` XML Validator (`scripts/validate_step2_twbx.py`)
- [ ] **Check 2.1:** `.twbx` is a valid ZIP archive containing `.twb`, `Data/Prototype/Candidate_Options.csv`, and `Data/Prototype/Weekly_Activity.csv`.
- [ ] **Check 2.2:** Embedded CSVs match `Data/Candidate_Options.csv` and `Data/Weekly_Activity.csv` byte-for-byte.
- [ ] **Check 2.3:** `.twb` parses without error in `xml.etree.ElementTree` and retains `xmlns:user='http://www.tableausoftware.com/xml/user'`.
- [ ] **Check 2.4:** Root `<workbook>` children appear in exact order: `document-format-change-manifest`, `preferences`, `datasources`, `worksheets`, `windows`, `thumbnails`.
- [ ] **Check 2.5:** `<document-format-change-manifest>` contains all 7 starter capability tags.
- [ ] **Check 2.6:** `<datasource>` children appear in exact XSD order: `connection`, `aliases`, `column`(s), `column-instance`(s), `layout`, `style`, `semantic-values`, `object-graph`.
- [ ] **Check 2.7:** `<object-graph>` contains both table objects and the exact `<relationship>` on `option_id`.
- [ ] **Check 2.8:** All calculated `<column>` definitions have valid `<calculation class='tableau' formula='...' />` attributes and unique `[Calculation_...]` names.
- [ ] **Check 2.9:** Every `<worksheet>` has exact child sequence `<layout-options>` (with non-empty `<title>` and `<caption>`), `<table>`, `<simple-id>`.
- [ ] **Check 2.10:** Every `<table>` inside a worksheet has exact child sequence `<view>`, `<style>`, `<panes>`, `<rows>`, `<cols>`.
- [ ] **Check 2.11:** Every `<view>` inside `<table>` has exact child sequence `<datasources>`, `<datasource-dependencies>` (if non-empty), `(<filter> | <sort>)*`, `<slices>` (mandatory iff filters > 0), `<aggregation value='true' />`.
- [ ] **Check 2.12:** Every `<filter column='X'>` has a matching `<column>X</column>` inside `<slices>`, and vice versa.
- [ ] **Check 2.13:** Every `[federated...].[instance]` token used in `<rows>`, `<cols>`, `<encodings>`, `<filter>`, `<sort>`, or `<slices>` is declared as a `<column-instance>` in that worksheet's `<datasource-dependencies>`.
- [ ] **Check 2.14:** Every `<column-instance column='[base_col]'>` in `<datasource-dependencies>` has its corresponding `<column name='[base_col]'>` declared in `<datasource-dependencies>` AND in the main `<datasource>`.
- [ ] **Check 2.15:** Inside `<datasource-dependencies>`, all `<column>` elements appear before all `<column-instance>` elements.
- [ ] **Check 2.16:** Every `<pane>` has `<view><breakdown value='auto' /></view>` and `<mark class='...' />` in the proper order before `<encodings>`.
- [ ] **Check 2.17:** `<worksheets>` and `<windows>` have an exact 1-to-1 match of all 12 worksheet names, `[Within Budget]` sorts `ASC` so `True` appears above `False`, and exactly one `<window>` has `maximized='true'`.
- [ ] **Check 2.18:** All `24` `<simple-id uuid='{...}' />` attributes across the entire workbook are valid uppercase UUIDs in braces with zero duplicates.

---

## Validation Gate 2B: MANDATORY USER APPROVAL GATE
- **STOP CONDITION:** Once Gate 2A passes all 18 automated checks, the AI **must stop** and advise the user to open `Vitaly_Chait_Final_Project_Workbook.twbx` in Tableau Desktop.
- **No work on Component 3, Component 4, or Component 5 may proceed until the user confirms that `Vitaly_Chait_Final_Project_Workbook.twbx` opens cleanly and meets their expectations.**
