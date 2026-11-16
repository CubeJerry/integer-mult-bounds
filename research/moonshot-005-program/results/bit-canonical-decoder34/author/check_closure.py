#!/usr/bin/env python3
"""Fresh current-stock and actual-history information envelopes for actual47."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
WORD='a910bb4504cf2a96303e8d560f076463268c4cb3ad4e6631d5f598c895db0567'
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 p=argparse.ArgumentParser()
 for n in ['repo','word','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();raw=a.word.read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];e=load(a.engine,'closure47_e');price=load(a.price_engine,'closure47_p');C,H,rep=e.replay(w,R)
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 for k,o in enumerate(w['operations']):
  op,n,*q=o
  if op=='CLEAR':cut=k;break
  if op=='INIT':v[n]=0;at[n]=q[0]
  elif op=='ADD':v[q[0]]^=v[n]
  elif op=='MOVE':at[n]=q[0]
 xm=(1<<111)-1;targets=set(w['targets']);initial={};local={};history={};own=[];qnonzero=[]
 for i in range(111):
  initial[i]=[z for n,z in v.items()if not z>>111 and e.sub(C[at[n]],C[f'F{i}'])]
  local[i]=[1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0]
  history[i]=[z&xm for _,_,c,z in H if e.sub(C[c],C[f'F{i}'])]
  if i not in targets:
   leaks=[{'step':st,'field':n,'chart':c,'row_hex':hex(z&xm)}for st,n,c,z in H if e.sub(C[c],C[f'F{i}'])and z>>i&1]
   if leaks:own.append({'receiver':i,'first':leaks[0],'count':len(leaks)})
   locmask=0
   for z in local[i]:locmask|=z
   keep=xm^(locmask|sum(1<<j for j in targets));qr=len(e.bb(z&keep for z in history[i]))
   if qr:qnonzero.append({'receiver':i,'rank':qr})
 def close(rows):
  known=targets.copy();waves=[]
  while True:
   new={i for i in range(111)if e.fits(rows[i]+[1<<j for j in known],1<<i)};assert known<=new
   if new==known:break
   waves.append(sorted(new-known));known=new
  return {'closure':sorted(known),'waves':waves,'remaining_duals':[{'receiver':i,'dual_hex':hex(price.outsider_dual(rows[i]+[1<<j for j in known],i))}for i in range(111)if i not in known]}
 models={'current_stock_and_completed_point_grants':close(initial),'current_stock_native_locals_completed_point_grants':close({i:initial[i]+local[i]for i in range(111)}),'all_actual_history_X_parts_and_raw_point_feedback':close(history)}
 assert all(len(z['closure'])==47 for z in models.values())
 result={'status':'PASS_FRESH_ACTUAL47_INFORMATION_CLOSURES','word_sha256':WORD,'source_sha256':w['source_sha256'],'replay':rep,'stock_cut_before_operation_index':cut,'models':models,'unfinished_receivers_with_visible_own_coordinate':own,'unfinished_receivers_with_nonzero_history_quotient_mod_locals_and47':qnonzero,'scope':'Exact fresh binary information envelopes for this changed47 word. Current stock and historical observations are separate grants; global completed-point feedback and arbitrary historical access are not physical decoder routes. Old65-own-zero theorem is not inherited.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'CLOSURE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'closures':{k:len(z['closure'])for k,z in models.items()},'unfinished_own_nonzero_count':len(own),'unfinished_nonzero_quotient_count':len(qnonzero)}))
if __name__=='__main__':main()
