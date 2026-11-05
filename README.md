# Operations Decision Lab | June 2025–August 2026 (synthetic period)

This portfolio simulates 15 months of customer operations. The **project was revised in November 2026**; the dates refer to fictional interactions, not the project completion date.

- Open `index.html` in a browser, or upload the contents of this folder to the root of a GitHub Pages repository.
- `portfolio.pdf` is the matching nine-page LinkedIn portfolio.
- `data/clean_contacts_SYNTHETIC.csv` has 78,000 fictional interactions.
- `data/raw_contacts_WITH_PLANTED_ERRORS.csv` has 78,072 records including 72 deliberate defects.
- `technical/dashboard_mart.json` is the 360-group summary embedded into the offline dashboard.
- Run `python evidence/validate_and_reconcile.py` and `python evidence/test_portfolio_evidence.py` to verify the generated data.
- The model AUC 0.66 is from the original Jun 2025–Mar 2026 synthetic historical subset, NOT a new model evaluation including Apr–Aug 2026.
- The dashboard uses HTML and JavaScript; it is not a native Power BI report. Example DAX measures are supplied.

No confidential business or real customer data. Nothing in the scenario represents a realised pilot, employer outcome, or a project completed in the 2025–2026 reporting interval.
