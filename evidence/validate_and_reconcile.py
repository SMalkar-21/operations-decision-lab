"""Demonstration of data quality gating for SYNTHETIC records.
Usage: python technical/validate_and_reconcile.py
Runs without external packages. No employer data is used.
"""
import csv
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
source=ROOT/'data'/'raw_contacts_WITH_PLANTED_ERRORS.csv'
valid=[];invalid=[];ids=set();why=Counter()
with source.open(newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        errors=[]
        if row['contact_id'] in ids: errors.append('duplicate_contact_id')
        else: ids.add(row['contact_id'])
        if not row['issue_type'].strip():errors.append('missing_issue_type')
        try:
            if float(row['workload_index'])<0:errors.append('negative_workload')
        except ValueError:errors.append('invalid_workload')
        try:
            if row['csat_score'] and not (1 <= float(row['csat_score']) <=5):errors.append('invalid_csat')
        except ValueError:errors.append('invalid_csat')
        if errors:
            invalid.append((row['contact_id'],','.join(errors)))
            why.update(errors)
        else: valid.append(row)
assert len(valid)==78000,(len(valid),len(invalid))
assert len(invalid)==72,(len(valid),len(invalid))
assert dict(why)=={'duplicate_contact_id':25,'negative_workload':20,'missing_issue_type':15,'invalid_csat':12},why
print(f'RAW {len(valid)+len(invalid):,} | ACCEPTED {len(valid):,} | QUARANTINED {len(invalid)}')
for k,v in why.items():print(f'  {k}: {v}')
print('PASS: all planted data-quality errors identified')
