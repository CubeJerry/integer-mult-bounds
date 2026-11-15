#!/usr/bin/env python3
"""Exact post-handoff static gate; all donor masks are optimistically global."""
import sys,json,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p));from shared_facet_source import source_geometry,dot,rank_f2,rank_q,mask
r,h,_=source_geometry(next(q for q in p.parents if(q/'AGENTS.md').exists()));w=json.loads((p/'two-receiver-output/COUPLED-WORD.json').read_text());owned=w['expected_owned_at_handoff'];T=[int(owned[f'P{i}']['value_hex'],16)for i in range(8)];masks=[(n,int(v['value_hex'],16))for n,v in owned.items()if n.startswith(('DM','SM'))];G=T+[v for n,v in masks]
fit=[];nofit=[]
def dual(rows,i):
 basis={}
 for row,b in[(v,0)for v in rows]+[(1<<i,1)]:
  while row:
   j=(row&-row).bit_length()-1
   if j not in basis:basis[j]=(row,b);break
   x,c=basis[j];row^=x;b^=c
  else:
   if b:raise ValueError('No separating dual')
 z=0
 for j,(row,b)in sorted(basis.items(),reverse=True):
  if b^((row&z).bit_count()%2):z|=1<<j
 return z
for i,v in enumerate(r):
 nm=mask(j for j in range(111)if dot(v,r[j])!=0);rows=[x&nm for x in G]
 if rank_f2(rows+[1<<i])==rank_f2(rows):fit.append(i)
 else:
  z=dual(rows,i)
  if z&~nm or not(z>>i&1)or any((g&z).bit_count()%2 for g in G):raise ValueError('Bad dual')
  nofit.append({'role':i,'dual_hex':hex(z)})
print('G',rank_f2(G),'feasible',len(fit),fit,'infeasible',len(nofit))
local=[];nonlocal_records=[]
for name,v in owned.items():
 chart=w['charts'][v['chart']];val=int(v['value_hex'],16)
 if val>>111 or name.startswith('P'):continue
 if chart['kind']=='ann': bad=[j for j in range(111)if val>>j&1 and any(dot(r[j],n)for n in chart['rows'])]
 else:bad=[j for j in range(111)if val>>j&1 and rank_q(chart['rows']+[r[j]])!=rank_q(chart['rows'])]
 if bad:nonlocal_records.append((name,bad))
 else:local.append(name)
print('nonlocal owners',nonlocal_records)
if {n for n,bad in nonlocal_records}!={n for n,v in masks}:raise ValueError('Unaccounted nonlocal proper owner')
(p/'TWO-RECEIVER-STATIC-GATE.json').write_text(json.dumps({'word_sha256':hashlib.sha256((p/'two-receiver-output/COUPLED-WORD.json').read_bytes()).hexdigest(),'global_rows_hex':[hex(v)for v in G],'global_rank':rank_f2(G),'donor_mask_rows':[{ 'record':n,'value_hex':hex(v)}for n,v in masks],'feasible_receivers':fit,'infeasible_duals':nofit,'nonlocal_proper_owners':nonlocal_records,'scope':'Frozen handoff, no further owned descents or new nonlocal inputs; all seven donor masks granted globally. Ascending Y mixing allowed. Existing completed target34 is not retrospectively subjected to this post-handoff gate. No complete kappa.'},indent=2)+'\n')
