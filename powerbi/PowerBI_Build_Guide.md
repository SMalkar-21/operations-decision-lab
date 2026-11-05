# Power BI Desktop: full report build guide

## 1. Import and model
- Start **Power BI Desktop**. Choose **Home > Get data > Text/CSV** and browse to `Contacts_SYNTHETIC_Jun2025_Aug2026.csv`.
- Click **Transform Data**. In Power Query, verify `contact_date` is **Date**; `csat_score`, `handle_minutes` and `workload_index` are **Decimal Number**; `sla_met`, `first_contact_resolved`, `escalated`, `reopened`, and `new_agent_flag` are **Whole Number**; `month` is Text. Keep missing CSAT cells as blanks. Click **Close & Apply**.
- Rename the resulting table **Contacts**. Each row represents one synthetic contact, and 78,000 is the expected count.
- In **Modeling > New column** create `Queue = 'Contacts'[team] & " / " & 'Contacts'[channel]`.
- Optionally create `Calendar = CALENDAR(DATE(2025,6,1), DATE(2026,8,31))` and relate Calendar[Date] (one) to Contacts[contact_date] (many). A simple report can instead use Contacts[month] directly; ISO `YYYY-MM` sorts chronologically as text.

## 2. Measures
- In **Modeling > New measure**, add each definition in `PowerBI_DAX_Measures_And_WhatIf.txt` separately. Don't paste the entire file into a single New Measure box.
- Format `SLA %`, `FCR %`, `CSAT Positive %`, `Escalation %`, `Reopened %`, `Scenario SLA %`, `Early Period SLA %`, and `Diagnostic Period SLA %` as **Percentage** (one decimal place).
- Format `AHT (Minutes)` with one decimal and `Potential Avoided Breaches`, `Breaches`, and `Total Contacts` as whole numbers.
- Create `Recovery Rate = GENERATESERIES(0, 1, 0.05)` under **Modeling > New table**. Do **not** relate it to Contacts. Format Value as percentage.

## 3. Report page 1: Executive overview (16:9)
- Title: **Customer Operations Intelligence**; subtitle: **Simulated reporting period | Jun 2025–Aug 2026**.
- Add 5 **Card** visuals: Total Contacts, SLA %, FCR %, CSAT Positive %, AHT (Minutes).
- Add slicers: Contacts[month], Contacts[team], Contacts[channel], Contacts[priority].
- **Line chart**: X=Contacts[month]; Y=SLA %; include a constant/reference line at SLA Target % (90%). Sort months ascending.
- **Clustered bar chart**: Y=Contacts[Queue], X=Breaches; sort descending; show top 10 queues.
- **Matrix**: rows=Contacts[team], columns=Contacts[channel], values=SLA % and Total Contacts (conditional formatting for SLA).
- Recommendation note: the **Billing / Email** queue contributes materially to the simulated SLA decline.

## 4. Report page 2: Diagnosis and data quality
- **Line chart**: month vs SLA %, add team as legend. Create small multiples by channel if helpful.
- **Stacked columns**: Contacts[month] vs Total Contacts with legend Contacts[channel].
- **Matrix**: rows=team and channel, values=Breaches, SLA %, FCR %, CSAT Positive %, AHT (Minutes).
- **Bar chart**: team vs Escalation %.
- Optional: import `Data_Quality_Exceptions_SYNTHETIC.csv` as a **separate** table named Quality, with no relationship. Bar chart=issue vs count; title `72 deliberately planted invalid source records`.
- Add a text note distinguishing the synthetic data quality demonstration from measured employer data.

## 5. Report page 3: What-if and BA delivery
- Slicer: Recovery Rate[Value] (single-select recommended). Default measure is 25% if no selection.
- Cards: Targeted Breaches Q1 2026, Potential Avoided Breaches, SLA %, Scenario SLA %, Scenario Uplift (pp).
- Column or KPI comparison: baseline SLA % vs Scenario SLA %; duplicate into a small two-bar chart if desired.
- Business problem and decision rule: investigate Billing/Email Q1 2026; propose a controlled six-week pilot with comparison group, an **illustrative** +5pp adjusted SLA threshold, and no deterioration in FCR or CSAT.
- If you place a month/team/channel slicer on this page, remember the scenario is filter-aware and can show zero if the selected range excludes the target cohort.
- Do **not** label `Scenario SLA %` a forecast: it assumes a chosen fraction of breaches is avoided and does not measure causal impact.

## 6. Sanity tests before sharing
- All months, teams, channels: total contacts = 78,000; SLA=85.37%, FCR=78.41%, CSAT Positive=81.54%, AHT=8.45.
- With **month Jan–Mar 2026, team Billing and channel Email**: Contacts=1,827; Breaches=662; SLA=63.77%.
- With no filters, recovery 0%: Scenario SLA % exactly equals SLA %.
- With no filters, recovery 25%: Potential Avoided Breaches=166; Scenario Uplift≈0.21pp.
- Use *File > Save As* to create your real `.pbix` in Power BI Desktop. We cannot create or verify this binary file in the current environment.

## 7. LinkedIn integration
- If you create and verify the native Power BI report, **export it to PDF** or capture 1–2 page screenshots and add them to Featured, labelling it a **Power BI portfolio project built with synthetic data**.
- Keep the interactive HTML site as a separate link and label it accurately as an HTML/JavaScript implementation.
- Don't publish a report to the open web if it contains confidential data; this supplied dataset is synthetic.
