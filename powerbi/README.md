# Power BI Desktop Report — build package

This is a **build kit**, not a finished `.pbix` report. The separate interactive site is implemented using HTML/JavaScript.

## To make the native report
1. Download `PowerBI_Build_Kit.zip` and extract it locally.
2. Install Power BI Desktop (Windows).
3. Home > Get data > Text/CSV > import `Contacts_SYNTHETIC_Jun2025_Aug2026.csv`.
4. Use `PowerBI_DAX_Measures_And_WhatIf.txt` to add measures; apply `PowerBI_Theme.json` and create visuals following the build guide.
5. Verify reconciled counts with `KPI_Reconciliation_By_Month_SYNTHETIC.csv`, then save your actual `.pbix`.
6. When your genuine `.pbix` is ready, upload it separately to the GitHub repository or publish it to Power BI Service when your account permits.

The model contains **synthetic** data only, covering a fictional reporting period June 2025–August 2026. The design mockups are **not** screenshots from Power BI Desktop.
