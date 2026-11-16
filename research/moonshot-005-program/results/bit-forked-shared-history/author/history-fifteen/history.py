#!/usr/bin/env python3
"""All-column chronological packet witnesses and optimistic stationary visibility."""
from pathlib import Path
import argparse,json,hashlib
import sympy as sp
from build import rank,solve,combination

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();w=json.loads((a.out/'WORD.json').read_text());raw=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['source_sha256'];R=json.loads(raw)['native_roots'];dot=lambda x,y:sum(a*b for a,b in zip(x,y));h=w['singular_h'];A=[sum(1<<j for j in range(111)if h[i]==h[j]and(i==j or dot(R[i],R[j])==0))for i in range(111)];S=[int(v,16)for v in w['seed_rows_hex']];X=[f'X{j}'for j in range(111)];Y=[f'Y{j}'for j in range(111)];val={n:1<<i for i,n in enumerate(X+Y)};loc={n:f'L{j}'for j,n in enumerate(X)}|{n:'zero'for n in Y};snap=[];read_pairs=[];cut={};cache_expected={c['name']:int(c['row_hex'],16)for c in w['history_cache_metadata']}
 def observe(n,step,phase):
  assert n.startswith('P')and loc[n]!='Hub';snap.append({'index':len(snap),'step':step,'phase':phase,'packet':n,'chart':loc[n],'row_hex':hex(val[n])});return len(snap)-1
 for step,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='INIT':val[n]=0;loc[n]=q[0]
  elif op=='ADD':
   d=q[0];before=observe(d,step,'before')if d.startswith('P')and loc[d]!='Hub'else None;val[d]^=val[n]
   if before is not None:
    after=observe(d,step,'after')
    if n in cache_expected:assert int(snap[before]['row_hex'],16)^int(snap[after]['row_hex'],16)==cache_expected[n];read_pairs.append({'cache':n,'before_snapshot':before,'after_snapshot':after,'step':step,'chart':loc[d]})
  elif op=='MOVE':
   loc[n]=q[0]
   if n.startswith('P')and loc[n]!='Hub':observe(n,step,'arrival')
  elif op=='CLEAR':
   if n in cache_expected:assert val[n]==cache_expected[n]
   del val[n],loc[n]
  if step==w['milestones']['source_cut']:
   for n,v in cache_expected.items():assert val[n]==v
  if step==w['milestones']['seed8_before_Y']:
   for p,s in enumerate(S):assert val[f'P{p}']==s and loc[f'P{p}']=='zero'
   cut={n:{'chart':loc[n],'row':v}for n,v in val.items()if not n.startswith('Y')}
 assert len(read_pairs)==len(cache_expected)==44
 H=[int(s['row_hex'],16)for s in snap];assert all(v.bit_length()<=111 for v in H);assert rank(H+A)==rank(H);fitting=[]
 for i,row in enumerate(A):
  c=solve(H,row);assert combination(H,c)==row;fitting.append({'receiver':i,'snapshot_indices':[j for j in range(len(H))if c>>j&1]})
 reps=[]
 for r in w['history_quotient_representatives_hex']:
  v=int(r,16);c=solve(H,v);reps.append({'row_hex':r,'snapshot_indices':[j for j in range(len(H))if c>>j&1],'single_actual_snapshot_matches':[j for j,s in enumerate(H)if s==v],'classification':'Formal combination of actual chronological snapshots; no single co-located materialized field is granted.'})
 charts={}
 for name,c in w['charts'].items():
  M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);charts[name]=[list(v)for v in(M.rowspace()if c['kind']=='span'else M.nullspace())]
 def visible(chart,i):return all(dot(v,R[i])==0 for v in charts[chart])
 access=[];completed=[];ground=S+[1<<j for j in w['point_targets']];fitting_compatible=[]
 for i in range(111):
  fields=[n for n,v in cut.items()if visible(v['chart'],i)];snaps=[s['index']for s in snap if visible(s['chart'],i)];rows=[cut[n]['row']for n in fields]+[H[j]for j in snaps];ok=rank(rows+[1<<i])==rank(rows)
  if ok:completed.append(i)
  forbidden=sum(1<<j for j in range(111)if dot(R[i],R[j])!=0);r0=[r&forbidden for r in ground];fits=rank(r0+[1<<i])==rank(r0)
  if fits:fitting_compatible.append(i)
  access.append({'receiver':i,'visible_actual_fields':fields,'visible_snapshot_indices':snaps,'optimistic_visible_rank':rank(rows),'target_in_optimistic_visible_span':ok,'ground_code_has_compatible_fitting':fits})
 assert completed==w['targets'];assert fitting_compatible==[1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80]
 result={'status':'PASS_ACTUAL_HISTORY_W15_AND_STATIONARY_ACCESS_SCREEN','word_sha256':hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest(),'all_input_columns':222,'snapshots':len(snap),'history_rank':rank(H),'W_rank':rank(A),'W_contained_in_actual_principal_history':True,'history_cache_difference_witnesses':read_pairs,'seven_W_mod_S_representatives':reps,'all111_fitting_witnesses':fitting,'stationary_capture_scope':'Optimistically grant a separate stationary owner copied from each actual non-Hub snapshot at its real chart/time; INIT, ADD, dirty CLEAR would be additional and MOVE zero. No capture/combine transport is granted. Ignore incompatible multi-chart visit ordering only to obtain an upper bound.','optimistically_completable_receivers':completed,'new_receivers_from_any_stationary_captures':[],'ground_fitting_compatible':fitting_compatible,'actual_correction_missing_receivers':[i for i in fitting_compatible if i not in completed],'access_rows':access,'new_complete_kappa':False};(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(snap,indent=2)+'\n');(a.out/'HISTORY-RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS_ACTUAL_HISTORY_W15_AND_STATIONARY_ACCESS_SCREEN','snapshots',len(snap),'historyrank',rank(H),'optimisticoutputs',completed)
if __name__=='__main__':main()
