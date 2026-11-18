# BUS 240F Final Project — Master Implementation & Validation Plan

## Execution Architecture & Gated Workflow

This project is split into **five sequential components**, each guarded by an automated validation script. **No component may begin until the preceding component passes all validation checks.** In addition, **Component 2 (Packaged Tableau Workbook `.twbx`) has a mandatory User Approval Gate**: once the `.twbx` passes all automated XML/tag/schema validations, the AI must pause and ask the user to inspect and approve the workbook in Tableau Desktop before moving to Component 3.

| Step / Component | Specification File | Key Deliverable(s) | Validation Gate | Gate Type |
| :---: | :--- | :--- | :--- | :--- |
| **Component 1** | `01_Component_Data_Audit_and_Validation.md` | `Deliverables/golden_metrics.json`<br>`Deliverables/verification_audit_summary.md` | `scripts/validate_step1_data.py` | Automated (100% Data & CSV parity) |
| **Component 2** | `02_Component_Tableau_Workbook_and_Validation.md` | `Vitaly_Chait_Final_Project_Workbook.twbx` | `scripts/validate_step2_twbx.py` + **User Review in Tableau Desktop** | **Automated (18 XML/Tag/Schema checks) + MANDATORY USER APPROVAL GATE** |
| **Component 3** | `03_Component_Checkpoint_PDF_and_Validation.md` | `Vitaly_Chait_Project_Checkpoint.pdf` | `scripts/validate_step3_checkpoint.py` | Automated (1-page PDF, template & metric audit) |
| **Component 4** | `04_Component_Final_PDF_Package_and_Validation.md` | `Vitaly_Chait_Two_Page_Brief.pdf`<br>`Vitaly_Chait_Static_View_Backup.pdf` | `scripts/validate_step4_final_pdfs.py` | Automated (Strict 2-page check + 4-view backup audit) |
| **Component 5** | `05_Component_Presentation_Defense_and_Validation.md` | `Deliverables/Presentation_and_Defense_Guide.md` | `scripts/validate_step5_package.py` | Automated (End-to-end 3-file final package & defense audit) |

---

## Baseline Verifiable Reference Metrics (All 12 Options)

Every number across all five components must strictly match this verified table computed from `Data/Candidate_Options.csv` and `Data/Weekly_Activity.csv`:

| Option ID | Location Name | Window | 4-Wk Cost (USD) | Within Budget (<= $18k) | Obs. Weeks (n) | Missing Weeks | Raw Sum | Mean (All Obs.) | Median (All Obs.) | SD | CV (%) | IQR | Min-Max | Shared 10-Wk Mean (Affordable) | Shared 9-Wk Mean (All 12) | Late 4-Wk Mean (Aug 31-Sep 21) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`L01_A`** | **Cedar Walk** | **A** | **$18,000** | **True** | **14** | **2** (`06-29`, `08-24`) | **21,140** | **1,510.00** | **1,535.00** | **302.58** | **20.04%** | **477.50** | **920-1,970** | **1,407.00** | **1,423.33** | **1,370.00** |
| **`L06_B`** | **Aspen Court** | **B** | **$16,000** | **True** | **15** | **1** (`08-24`) | **21,439** | **1,429.27** | **1,327.00** | **470.64** | **32.93%** | **554.50** | **840-2,422** | **1,619.10** | **1,649.44** | **1,420.00** |
| **`L04_A`** | **Birch Arcade** | **A** | **$17,500** | **True** | **14** | **2** (`06-22`, `09-07`) | **19,619** | **1,401.36** | **1,424.50** | **204.49** | **14.59%** | **281.75** | **978-1,721** | **1,449.70** | **1,455.56** | **1,472.67** |
| **`L02_B`** | **Maple Court** | **B** | **$16,500** | **True** | **15** | **1** (`07-20`) | **19,886** | **1,325.73** | **1,316.00** | **127.56** | **9.62%** | **161.00** | **1,120-1,592** | **1,304.10** | **1,290.00** | **1,281.25** |
| **`L02_A`** | **Maple Court** | **A** | **$15,000** | **True** | **16** | **0** | **20,009** | **1,250.56** | **1,249.00** | **92.62** | **7.41%** | **112.50** | **1,110-1,457** | **1,239.40** | **1,229.33** | **1,228.75** |
| **`L06_A`** | **Aspen Court** | **A** | **$14,500** | **True** | **16** | **0** | **18,719** | **1,169.94** | **1,170.00** | **156.76** | **13.40%** | **267.50** | **915-1,390** | **1,240.60** | **1,247.00** | **1,222.50** |
| **`L03_B`** | **Willow Square** | **B** | **$13,500** | **True** | **16** | **0** | **18,519** | **1,157.44** | **1,164.00** | **151.04** | **13.05%** | **250.50** | **943-1,426** | **1,172.10** | **1,148.67** | **1,092.50** |
| **`L03_A`** | **Willow Square** | **A** | **$12,000** | **True** | **15** | **1** (`08-10`) | **16,211** | **1,080.73** | **1,102.00** | **111.94** | **10.36%** | **182.50** | **934-1,263** | **1,089.20** | **1,070.11** | **1,032.25** |
| `L05_B` | Juniper Row | B | $21,000 | False | 15 | 1 (`07-27`) | 25,971 | 1,731.40 | 1,757.00 | 173.19 | 10.00% | 220.00 | 1,490-2,053 | 1,744.11 | 1,744.11 | 1,790.00 |
| `L01_B` | Cedar Walk | B | $19,500 | False | 16 | 0 | 26,094 | 1,630.88 | 1,679.00 | 347.68 | 21.32% | 509.25 | 1,035-2,237 | 1,536.10 | 1,551.00 | 1,490.00 |
| `L05_A` | Juniper Row | A | $19,000 | False | 16 | 0 | 25,651 | 1,603.19 | 1,590.00 | 153.50 | 9.57% | 217.00 | 1,365-1,878 | 1,605.90 | 1,620.78 | 1,670.00 |
| `L04_B` | Birch Arcade | B | $18,500 | False | 16 | 0 | 23,515 | 1,469.69 | 1,513.50 | 237.86 | 16.18% | 313.25 | 992-1,884 | 1,546.60 | 1,553.00 | 1,455.00 |
