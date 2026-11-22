"""Materialize and price the actual changed t=26 source/D phases.

Only changed source phases are recompiled; unchanged H/source receipts are
source-bound dependencies, separately distinguished from fresh execution.
"""
from pathlib import Path
import argparse,importlib.util,json,gzip,hashlib
import numpy as np

def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def read(p):return json.loads(gzip.decompress(p.read_bytes()))if p.suffix=='.gz'else json.loads(p.read_text())
def save(p,v):
 raw=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode();p.write_bytes(gzip.compress(raw,mtime=0));return hashlib.sha256(raw).hexdigest()
def need(v,msg):
 if not v:raise ValueError(msg)

def eliminate(A,c):
 rows=c.binary_rows(A);n=len(rows);ops=[]
 def add(t,s):rows[t]^=rows[s];ops.append([t,s])
 for q in range(n):
  bit=1<<q
  if not rows[q]&bit:
   p=next(r for r in range(q+1,n)if rows[r]&bit);add(q,p);add(p,q);add(q,p)
  for r in range(n):
   if r!=q and rows[r]&bit:add(r,q)
 need(rows==[1<<q for q in range(n)],'elimination identity')
 state=[1<<q for q in range(n)]
 for t,s in reversed(ops):state[t]^=state[s]
 need(state==c.binary_rows(A),'all source/D original columns forward replay')
 for t,s in ops:state[t]^=state[s]
 need(state==[1<<q for q in range(n)],'pure inverse replay')
 return ops

def run(repo,candidate,out):
 base=repo/'research/moonshot-005-program/results';four=base/'bit-simultaneous-d1509-s032';b=mod(Path(__file__).parent/'check.py','sourcecheck');g,a,s,e,src,cc,changed=b.load(repo,candidate);c=mod(base/'bit-shared-h-s031-construction/native-d1509-all-native/compile_prefix.py','compiler');old=read(four/'output/PHASE-COMPILER-RECEIPTS.json.gz');prior=read(four/'output/COMPILER-RESULT.json');dw=read(four/'output/D-WORD.json.gz');oldsource=s['paired_maps'];newearly={};newparities={};opsrec={};delta=0;changed_donors=sorted({j for j,h in changed});out.mkdir(parents=True,exist_ok=True)
 for j in changed_donors:
  E=np.array(e[str(j)]['physical_matrix'],dtype=np.uint8);ordered=[];late={};P={h:a.mm(np.array(s['frames'][f'{j}/{h}'],dtype=np.uint8),F)for h,F in src[j].items()}
  for q,(h,owner) in enumerate(e[str(j)]['row_owners']):
   within=sum(t[0]==h for t in e[str(j)]['row_owners'][:q]);row=P[h][within];E[owner]=row;ordered.append(row)
  for h in src[j]:
   quota=sum(t[0]==h for t in e[str(j)]['row_owners']);late[h]=P[h][quota:]
  ops=eliminate(E,c);weight=int(c.WEIGHT[np.vstack(list(late.values()))].sum());oldrec=old['sources'][str(j)];oldadd=oldrec['early']['ADD_per_direction'];oldweight=oldrec['exact_parity_form_ADD'];difference=2*(len(ops)-oldadd)+weight-oldweight;delta+=difference
  opsrec[j]={'elimination_word_uint32le_sha256':hashlib.sha256(np.asarray(ops,dtype='<u4').tobytes()).hexdigest(),'actual_early_owners':e[str(j)]['row_owners'],'ADD_per_direction':len(ops),'old_ADD_per_direction':oldadd,'parity_form_ADD':weight,'old_parity_form_ADD':oldweight,'base_ADD_delta':difference,'binary_columns_replayed':2880,'stationary_parity_bits':6*sum(len(M)for M in late.values())}
  newearly[j]={'matrix':np.array(ordered,dtype=np.uint8).tolist(),'physical_matrix':E.tolist(),'row_owners':e[str(j)]['row_owners']};newparities[j]={h:M.tolist()for h,M in late.items()};print('SOURCE_COMPILED',j,len(ops),weight,difference,flush=True)
 T=np.array(cc['D_matrix'],dtype=np.uint8);Eops=eliminate(T[:19,:19],c);Bops=eliminate(T[19:,19:],c);X=[1<<q for q in range(114)];Y=[1<<(q+114)for q in range(96)];cache=X.copy();cross=[]
 for t,s0 in reversed(Eops):X[t]^=X[s0]
 for t,s0 in reversed(Bops):Y[t]^=Y[s0]
 for t,row in enumerate(c.binary_rows(T[19:,:19])):
  for s0 in range(114):
   if row>>s0&1:Y[t]^=cache[s0];cross.append([t,s0])
 need(X+Y==c.binary_rows(T),'210-column chronological D replay')
 dnew=2*(len(Eops)+len(Bops))+114+len(cross);dold=dw['compiler']['including_pure_inverse_ADDs'];delta+=dnew-dold;result={'status':'PASS_COUPLED_T26_SOURCE_D_CHRONOLOGICAL_COMPILERS'if cc.get('t')==26 else'PASS_COUPLED_GLOBAL_GAUGE_SOURCE_D_CHRONOLOGICAL_COMPILERS','changed_sources':changed_donors,'source_records':{j:{k:v for k,v in rec.items()if k not in['actual_early_owners']}for j,rec in opsrec.items()},'D_early_ADD_per_direction':len(Eops),'D_late_ADD_per_direction':len(Bops),'D_cross_ADD':len(cross),'D_cache_copy_ADD':114,'D_including_pure_inverse_ADD':dnew,'D_old_including_pure_inverse_ADD':dold,'source_and_D_base_ADD_delta':delta,'fullbank_ADD_delta':8*delta,'fullbank_source_H_D_ADD':prior['fullbank_ADD_including_phase_inverses']+8*delta,'fullbank_INIT':prior['fullbank_INIT'],'fullbank_dirty_CLEAR':prior['fullbank_dirty_CLEAR'],'fullbank_extra_field_exports':16,'extra_MOVE_gap':6,'new_MOVE_records':0,'replayed_changed_source_binary_columns':len(changed_donors)*2880,'replayed_D_binary_columns':210,'unchanged_H_and_source_receipts_reused':len(changed_donors)<11,'unchanged_H_receipts_reused':True,'unchanged_source_receipts_reused':11-len(changed_donors),'pure_inverse_global_placement':False,'full_global_supplier_invoice':False,'new_complete_kappa':False}
 save(out/'CHANGED-EARLY.json.gz',newearly);save(out/'CHANGED-LATE-PARITIES.json.gz',newparities);result['source_phase_receipts_sha256']=save(out/'PHASE-COMPILER-RECEIPTS.json.gz',opsrec);result['D_word_sha256']=save(out/'D-WORD.json.gz',{'owners':dw['owners'],'matrix':T.tolist(),'inverse':g.inverse(T,a).tolist(),'early_elimination_ADD':Eops,'late_elimination_ADD':Bops,'late_cross_from_original_early_cache_ADD':cross,'cache_labels':dw['compiler']['cache_labels']});(out/'COMPILER-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],result['fullbank_source_H_D_ADD'],result['fullbank_ADD_delta'],flush=True)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--candidate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args();run(q.repo.resolve(),q.candidate.resolve(),q.out.resolve())
