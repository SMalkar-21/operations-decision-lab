-- ADVANCED OPERATIONS INTELLIGENCE PORTFOLIO
-- All data in this project are SYNTHETIC. Example SQLite queries.
-- Import clean_contacts_SYNTHETIC.csv as a SQLite table named contacts.
-- Do not use these hypothetical KPI definitions for a real employer without approval.

-- 01 / Quality gates: nulls, duplicates, invalid fields
SELECT COUNT(*) AS rows_total,
       COUNT(DISTINCT contact_id) AS distinct_contacts,
       SUM(CASE WHEN issue_type IS NULL OR TRIM(issue_type)='' THEN 1 ELSE 0 END) AS missing_issue_types,
       SUM(CASE WHEN workload_index < 0 THEN 1 ELSE 0 END) AS invalid_workload,
       SUM(CASE WHEN csat_score IS NOT NULL AND (csat_score<1 OR csat_score>5) THEN 1 ELSE 0 END) AS invalid_csat
FROM contacts;

-- 02 / Governed monthly KPIs: respondent denominator for CSAT
SELECT month,
       COUNT(*) AS contacts,
       ROUND(100.0*SUM(sla_met)/COUNT(*), 1) AS sla_pct,
       ROUND(100.0*SUM(first_contact_resolved)/COUNT(*),1) AS fcr_pct,
       ROUND(100.0*SUM(escalated)/COUNT(*),1) AS escalated_pct,
       ROUND(100.0*SUM(CASE WHEN csat_score>=4 THEN 1 ELSE 0 END)
             / NULLIF(SUM(CASE WHEN csat_score IS NOT NULL THEN 1 ELSE 0 END),0),1) AS csat_positive_pct
FROM contacts GROUP BY month ORDER BY month;

-- 03 / Breach Pareto: counts AND percentages for prioritisation
WITH segment AS (
  SELECT team,channel,COUNT(*) n,
         SUM(CASE WHEN sla_met=0 THEN 1 ELSE 0 END) breaches,
         ROUND(100.0*AVG(sla_met),1) sla_pct
  FROM contacts GROUP BY team,channel
)
SELECT team,channel,n,breaches,sla_pct,
       ROUND(100.0*breaches/SUM(breaches) OVER(),1) AS share_of_all_breaches_pct
FROM segment ORDER BY breaches DESC;

-- 04 / Requirement REQ-03: group-level SLA Jun-Aug 2025 vs Jan-Mar 2026
WITH grouped AS (
 SELECT team,channel,
        CASE WHEN month <= '2025-08' THEN 'EARLY'
             WHEN month BETWEEN '2026-01' AND '2026-03' THEN 'LATE' END period,
        COUNT(*) AS n,AVG(1.0*sla_met) AS sla_rate
 FROM contacts
 WHERE month<='2025-08' OR month BETWEEN '2026-01' AND '2026-03'
 GROUP BY team,channel,period
)
SELECT * FROM grouped ORDER BY team,channel,period;

-- 05 / What-if model: a planning assumption, not a causal prediction.
-- For Jan-Mar 2026 Billing/Email (the original diagnostic cohort), what if 25% of existing breaches were avoided?
WITH totals AS (
 SELECT COUNT(*) AS n, SUM(sla_met) AS successes FROM contacts
), target AS (
 SELECT SUM(CASE WHEN sla_met=0 THEN 1 ELSE 0 END) AS breaches
 FROM contacts WHERE team='Billing' AND channel='Email' AND month BETWEEN '2026-01' AND '2026-03'
)
SELECT ROUND(100.0*successes/n,2) AS baseline_sla_all_months_pct,
       breaches AS target_breaches,
       ROUND(0.25*breaches) AS hypothetical_avoided,
       ROUND(100.0*(successes+ROUND(0.25*breaches))/n,2) AS simulated_sla_all_months_pct
FROM totals CROSS JOIN target;

-- 06 / 2026 follow-up: show continuing simulated SLA pressure through Aug 2026
SELECT month, COUNT(*) AS contacts,
       ROUND(100.0*AVG(sla_met),1) AS sla_pct,
       SUM(CASE WHEN sla_met=0 THEN 1 ELSE 0 END) AS sla_breaches
FROM contacts WHERE month BETWEEN '2026-04' AND '2026-08'
GROUP BY month ORDER BY month;
