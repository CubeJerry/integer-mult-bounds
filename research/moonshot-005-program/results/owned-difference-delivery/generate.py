#!/usr/bin/env python3
"""Rebuild exact rows/versions/residuals for the ten fixed algebraic witnesses."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN="2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
SOURCE="research/shared-wire-split-composition/data/final.json.gz"
TERMS={28169: [[41, '5/4'], [42, '-1/8'], [106, '1/2'], [400, '2'], [730, '-1/4'], [1162, '-1'], [1373, '-1/2'], [1385, '-1/4'], [1392, '1/4']], 33272: [[749, '-1']], 33281: [[756, '-1']], 33558: [[1130, '-1'], [1492, '-1/16']], 34479: [[86, '-1/8'], [93, '-1/4'], [1098, '-1'], [1491, '1/8']], 37606: [[228, '-8'], [913, '2'], [992, '-4'], [1444, '-8']], 39217: [[173, '-17/2'], [752, '-2']], 40094: [[695, '-1'], [1336, '-2'], [1362, '2'], [1502, '-2']], 40096: [[133, '1/2'], [901, '2']], 41758: [[151, '-33'], [472, '4'], [917, '-2']]}
def add(a,b,c):
 for k,v in b.items():
  z=a.get(k,F(0))+c*v
  if z:a[k]=z
  else:a.pop(k,None)
def encoded(a):return [[k,str(v)] for k,v in sorted(a.items())]
def reverse(w,cut,row):
 row=dict(row)
 for e in reversed(w['program'][:cut]):
  op,r=e[:2]
  if op in ('INIT','CLEAR'):row.pop(r,None)
  elif op in ('ADD','COPY') and r in row:
   z=row.get(e[2],F(0))+F(e[3])*row[r]
   if z:row[e[2]]=z
   else:row.pop(e[2],None)
  elif op=='SCALE' and r in row:row[r]*=F(e[2])
 return row
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();raw=a.source.read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('source pin')
w=json.loads(gzip.decompress(raw));n=w['public'];M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);rows=[{r:F(1)} if r in M else {} for r in range(n+w['owned_fields'])];cur=w['initial']+[None]*w['owned_fields'];versions=[-1]*len(rows);records=[]
for i,e in enumerate(w['program']):
 op,r=e[:2]
 if i in TERMS:
  terms=TERMS[i];form={r:F(1)}
  for s,c in terms:form[s]=form.get(s,F(0))-F(c)
  rec={'before_event':i,'move':e,'rank':abs(len(w['frames'][e[2]])-len(w['frames'][e[3]])),'target_row':encoded(rows[r]),'source_last_value_event':versions[r],'witness':terms,'observer_current_frames':{str(s):cur[s] for s,c in terms},'observer_last_value_events':{str(s):versions[s] for s,c in terms},'observer_rows':{str(s):encoded(rows[s]) for s,c in terms},'available_cochart_owners':[s for s in range(len(rows)) if s!=r and cur[s]==e[3]],'common_value_residual_on_entering_helpers':encoded(reverse(w,i,form)),'observer_kinds':{str(s):'main' if s in M else 'helper' if s<n else 'owned' for s,c in terms}}
  records.append(rec)
 if op in ('INIT','CLEAR'):cur[r]=e[2] if op=='INIT' else None;rows[r]={};versions[r]=i
 elif op=='MOVE':cur[r]=e[3]
 elif op=='SCALE':rows[r]={j:F(e[2])*v for j,v in rows[r].items()};versions[r]=i
 else:add(rows[r],rows[e[2]],F(e[3]));versions[r]=i
out={'schema':'moonshot-owned-difference-delivery-v1','source_sha256':PIN,'source_path':SOURCE,'source_events':len(w['program']),'interpretation':'Delta=copy2-copy1, same arbitrary entering helpers; exact normalized current source rows on400maininputs. Observations are virtual; physical cochart availability remains a premise.','witnesses':records}
with a.output.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
