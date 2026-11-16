#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib
import sympy as sp
from check import rank

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();w=json.loads((a.out/'WORD.json').read_text());raw=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['source_sha256'];R=json.loads(raw)['native_roots'];dot=lambda x,y:sum(a*b for a,b in zip(x,y));C={};ann={};local={}
 for ch,c in w['charts'].items():
  M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);B=M.rowspace()if c['kind']=='span'else M.nullspace();C[ch]=[list(v)for v in B];N=sp.Matrix(C[ch]).nullspace()if C[ch]else sp.eye(8).columnspace();ann[ch]=[list(v)for v in N];local[ch]=sum(1<<j for j in range(111)if all(dot(v,R[j])==0 for v in ann[ch]))
 val={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};owners=set();snap=[];cut=None
 isp=lambda n:n.startswith('P')and n[1:].isdigit()
 def save(n,k,phase):snap.append({'index':len(snap),'step':k,'packet':n,'chart':loc[n],'phase':phase,'row_hex':hex(val[n])})
 for k,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='INIT':val[n]=0;loc[n]=q[0];owners.add(n)
  elif op=='ADD':
   d=q[0]
   if isp(d)and loc[d]!='Hub':save(d,k,'before')
   val[d]^=val[n]
   if isp(d)and loc[d]!='Hub':save(d,k,'after')
  elif op=='MOVE':
   loc[n]=q[0]
   if isp(n)and loc[n]!='Hub':save(n,k,'arrival')
  elif op=='CLEAR':owners.remove(n);del val[n],loc[n]
  if k==w['milestones']['seed8_before_Y']:cut={'values':val.copy(),'charts':loc.copy(),'owners':sorted(owners)}
 assert cut;v=cut['values'];at=cut['charts'];xmask=(1<<111)-1;pure={n:r for n,r in v.items()if r&~xmask==0};ground=[r for n,r in pure.items()if not C[at[n]]];nonlocal_rows=[{'field':n,'chart':at[n],'dimension':len(C[at[n]]),'row_hex':hex(r),'outside_local_support':[j for j in range(111)if r>>j&1 and not(local[at[n]]>>j&1)]}for n,r in pure.items()if C[at[n]]and r&~local[at[n]]];access=[];actual=[];optimistic=[];history_optimistic=[]
 for i in range(111):
  vis=[r for n,r in pure.items()if all(dot(x,R[i])==0 for x in C[at[n]])];rawlocal=[1<<j for j in range(111)if dot(R[i],R[j])==0];ss=[int(s['row_hex'],16)for s in snap if all(dot(x,R[i])==0 for x in C[s['chart']])];a0=rank(vis+[1<<i])==rank(vis);a1=rank(vis+rawlocal+[1<<i])==rank(vis+rawlocal);a2=rank(vis+rawlocal+ss+[1<<i])==rank(vis+rawlocal+ss)
  if a0:actual.append(i)
  if a1:optimistic.append(i)
  if a2:history_optimistic.append(i)
  access.append({'receiver':i,'actual_visible_span_has_target':a0,'all_raw_proper_locals_have_target':a1,'all_actual_history_snapshots_plus_raw_locals_have_target':a2})
 H=[int(s['row_hex'],16)for s in snap];K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];W=[k&sum(1<<j for j in range(111)if w['singular_h'][i]==w['singular_h'][j])for i,k in enumerate(K)];assert rank(H+K+W)==rank(H);assert all(i in actual for i in w['targets']);out={'status':'PASS_COMPLETE_LITERAL_NONLOCAL_LEDGER','word_sha256':hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest(),'principal_snapshot_count':len(snap),'principal_history_rank':rank(H),'contains_full_C9_and_W15':True,'ground_rank':rank(ground),'actual_nonlocal_positive_inventory':nonlocal_rows,'actual_visible_targets_ignoring_order':actual,'raw_local_fitting_targets':optimistic,'history_plus_raw_local_fitting_targets':history_optimistic,'access':access,'original_Y_cut_values':{n:{'chart':at[n],'row_hex':hex(r)}for n,r in v.items()if n.startswith('Y')},'scope':'All actual positive nonlocal fields included, especially Q1/Q3/Q4 descended toM1. Original Y nuisance columns retained separately, never silently granted as pureX. Raw-local and extra stationary-history access are explicitly optimistic and do not assert a physical path.','new_complete_kappa':False};(a.out/'HISTORY-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(snap,indent=2)+'\n');print(out['status'],'snapshots',len(snap),'rank',rank(H),'nonlocal',[z['field']for z in nonlocal_rows],'actual',len(actual),'rawfit',len(optimistic),'historyfit',len(history_optimistic))
if __name__=='__main__':main()
