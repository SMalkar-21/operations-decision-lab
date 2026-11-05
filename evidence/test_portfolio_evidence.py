"""Reproducible quality checks for synthetic operations portfolio (no external dependencies)."""
from pathlib import Path
import csv, json, collections, math
R=Path(__file__).resolve().parent
# support being run next to data/ folder in GitHub Pages, or inside the work directory
if not (R/'data').exists():
    R=R.parent
raw=R/'data'/'raw_contacts_WITH_PLANTED_ERRORS.csv'
clean=R/'data'/'clean_contacts_SYNTHETIC.csv'
metrics=json.loads((R/'technical'/'metrics.json').read_text())
with raw.open(newline='',encoding='utf8') as f: rawrows=list(csv.DictReader(f))
with clean.open(newline='',encoding='utf8') as f: rows=list(csv.DictReader(f))
results=[]
def check(name, ok, detail):
    results.append((name,bool(ok),detail)); print(('PASS' if ok else 'FAIL')+' | '+name+' | '+detail)
check('Raw to clean row counts', len(rawrows)==78072 and len(rows)==78000,'78,072 source; 78,000 curated')
check('Quarantine exception count',len(rawrows)-len(rows)==72,'72 planted exceptions')
check('Unique curated contact IDs', len({r['contact_id'] for r in rows})==len(rows),'No duplicate IDs in curated data')
sla=sum(int(r['sla_met']) for r in rows)/len(rows)
check('Governed SLA denominator',math.isclose(sla,metrics['overall_sla'],abs_tol=1e-11),f'{sla*100:.2f}% across all valid contacts')
focus=[r for r in rows if r['team']=='Billing' and r['channel']=='Email' and '2026-01'<=r['month']<='2026-03']
breaches=sum(int(r['sla_met'])==0 for r in focus)
check('Billing/Email cohort SQL-equivalent',len(focus)==metrics['target_n'] and breaches==metrics['target_breach'],f'{len(focus):,} contacts; {breaches} breached')
avoided=round(breaches*.25)
check('25% what-if arithmetic',avoided==metrics['scenario_recover_25'] and math.isclose(100*avoided/len(rows),metrics['scenario_overall_pp_25'],abs_tol=1e-9),f'{avoided} hypothetical avoided; +{100*avoided/len(rows):.2f} pp over full period')
check('Extended data end-month', all(r['month']>='2025-06' and r['month']<='2026-08' for r in rows) and any(r['month']=='2026-08' for r in rows), 'June 2025 through August 2026')
check('Zero-recovery scenario control',round(breaches*0)==0 and (sum(int(r['sla_met']) for r in rows)+0)/len(rows)==sla,'0% recovery produces no uplift')
delta=(metrics['new_sla']-metrics['old_sla'])*100
check('Mix decomposition reconciliation', math.isclose(metrics['within_pp']+metrics['mix_pp'],delta,abs_tol=1e-9),f'{metrics["within_pp"]:+.3f} pp within + {metrics["mix_pp"]:+.3f} pp mix = {delta:+.3f} pp')
passed=sum(ok for _,ok,_ in results)
print(f'RESULT: {passed}/{len(results)} automated dataset checks passed')
assert passed==len(results), 'Verification failed'
