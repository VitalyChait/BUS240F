# Final Project — Data Dictionary and Starter Guide

Use this guide while opening the starter and interpreting its fields. You do not need to memorize calculation syntax. AI can help write a formula when you specify the intended rule, population, and treatment of missing values; you remain responsible for checking the result.

---

## 1. Open the Starter

1. Download `BUS240F_Final_Project_Starter.twbx` and open it in Tableau Desktop.
2. Use **Save As** to create your team's working copy. Keep the file type as a **Tableau Packaged Workbook (`.twbx`)**.
3. You should see two blank worksheets: 
   * `01 Verify the Model`
   * `02 Build the Decision`
   
   *(Add or rename sheets as your analysis develops; these are starting points, not a required sheet count.)*

The CSVs are embedded in the package. You do not need to reconnect or upload them separately. A separate source-data ZIP is provided for inspection and recovery. The data source may appear as `Weekly_Activity+`.

---

## 2. Understand the Two Tables

| Table | What One Row Means | Expected Records |
| :--- | :--- | :--- |
| **`Candidate_Options.csv`** | One location and operating-window option. | 12 rows; 12 distinct option IDs. |
| **`Weekly_Activity.csv`** | One option during one scheduled historical week, including missing observations. | $192\text{ rows} = 12\text{ options} \times 16\text{ weeks}$.<br>184 Complete and 8 Missing. |

> **Tableau Relationship:**  
> The tables are already related on their option IDs (`option_id`). One candidate option corresponds to 16 weekly records. This is a Tableau relationship between two tables. Keep the supplied model; you do not need to replace it with a physical join.

---

## 3. Data Dictionary

### Candidate Options Fields (`Candidate_Options.csv`)

| CSV Field | Tableau Label | Type / Unit | Definition and Use |
| :--- | :--- | :--- | :--- |
| `option_id` | Option Id (Candidate Options.csv) | Text identifier | Unique location/window choice (e.g., `L01_A`). One row per option; relates to `option_id` in Weekly Activity. |
| `location_id` | Location Id | Text identifier | Fictional location (`L01`–`L06`). Each location has two options. |
| `location_name` | Location Name | Text category | Fictional descriptive name (e.g., *Cedar Walk*). Not a real geocoded address. |
| `window_id` | Window Id | Text category | `A` or `B`. Both windows have equal weekly scheduled hours. |
| `operating_window_label` | Operating Window Label | Text category | Days and hours: `Tue-Sat 10:00-14:00` or `Tue-Sat 14:00-18:00`, in common fictional local time. |
| `scheduled_hours_per_week` | Scheduled Hours Per Week | Whole number, hours/week | `20` for each option. A complete observation covers all these hours. |
| `pilot_weeks` | Pilot Weeks | Whole number, weeks | `4` for each option. Duration of the proposed trial, not the number of historical observations. |
| `total_pilot_cost_usd` | Total Pilot Cost Usd | Whole number, USD | All-inclusive commitment for one option for the whole four-week trial. Compare with **\$18,000**; do not sum across repeated weeks. |

---

### Weekly Activity Fields (`Weekly_Activity.csv`)

| CSV Field | Tableau Label | Type / Unit | Definition and Use |
| :--- | :--- | :--- | :--- |
| `option_id` | Option Id | Text identifier | The option observed that week. Repeats across weeks. Together with `week_start`, uniquely identifies a row. |
| `week_start` | Week Start | Date (`YYYY-MM-DD`) | Monday identifying the historical observation week. The count covers the specified Tuesday–Saturday window within that week. |
| `observation_status` | Observation Status | Text category | `Complete` = all 20 hours observed;<br>`Missing` = no usable weekly count.<br>*(No partial observations are supplied).* |
| `observed_passages` | Observed Passages | Whole number, passage events/week; may be blank | Crossings during the option's 20-hour weekly window, including repeats. Blank when status is `Missing`; **never silently replace with zero**. |

---

### Other Fields You Will See in Tableau

* **`Within Budget`:**  
  Supplied as a calculated True/False field. It tests whether the option's four-week cost is at most \$18,000:
  $$\text{[Total Pilot Cost Usd]} \le 18000$$
  *The rule includes an option costing exactly \$18,000. `True` means affordable under the case budget; it does not mean profitable or recommended.*
* **Row Count Helpers:**  
  `Candidate_Options.csv (Count)` and `Weekly_Activity.csv (Count)` represent Tableau's internal table row counts.  
  * Note the difference between:
    * `COUNT(Observed Passages)`: counts non-missing values.
    * `SUM(Observed Passages)`: sums passage events.
* **Tableau Helpers:**  
  `Measure Names` and `Measure Values` are system-generated helpers, not extra dataset columns.

---

## 4. First Checks in Tableau

Perform these baseline checks to verify your data model:

1. **Verify Total Weekly Records:** On a blank sheet with no filters, drag `Weekly_Activity.csv (Count)` to **Text** on the Marks card.  
   * **Expect:** `192` scheduled weekly records.
2. **Verify Observation Completeness:** Add `Observation Status` to **Rows**.  
   * **Expect:** `184 Complete` and `8 Missing` records.
3. **Verify Candidate Options Count:** On a separate blank sheet, drag `Candidate_Options.csv (Count)` to **Text**.  
   * **Expect:** `12` options.
4. **Inspect a Representative Source Row:**
   * Option `L01_A`, week starting `June 8`: has **1,175** observed passages and status `Complete`.
   * Option `L01_A`, week starting `June 29`: has a **blank** count and status `Missing`.

*(These are verification totals, not recommendations for the business decision. If totals differ, inspect applied filters).*

---

## 5. Reading Averages and Costs Correctly

* **Observed-Week Average:**  
  `AVG(Observed Passages)` only uses non-missing observations in the active view. Each option has 14–16 complete weeks. Always report or state the number of observed weeks used. *A mean over available weeks does not recover missing activity.*
* **Typical Activity:**  
  `MEDIAN(Observed Passages)` provides an alternative summary resistant to extreme weeks. Explain why your chosen metric fits the decision.
* **Fair Comparison:**  
  Totals summed over unequal numbers of complete weeks are **not directly comparable**. You may test a shared-week comparison (evaluating only weeks where all candidate options have complete data), but explicitly explain which weeks this removes. *(This serves as an optional approach for the required sensitivity test).*
* **Fixed Cost Handling:**  
  Show exactly one cost per option. For example, `L01_A` costs \$18,000 for the entire pilot; 16 historical records do **not** mean its cost is $\$18,000 \times 16 = \$288,000$.  
  * With one option per mark, `MIN(Total Pilot Cost Usd)` correctly displays its single fixed cost.  
  * Note: `MIN` across several options does not calculate their combined cost.

---

## 6. Boundaries and Version Control

* **Nature of Data:** Passages are raw crossings, not unique visitors, converted customers, or sales revenue.
* **Missing Data:** Missing counts are blank, not zero. The dataset provides no explanation for missing weeks or traffic spikes.
* **Predictive Limits:** Historical observations are neither future forecasts nor causal evidence.
* **Integrity:** This is a fixed synthetic snapshot. The two embedded CSVs match the standalone source ZIP. Keep original values intact and ensure every analytical decision/filter is explicitly documented in your workbook.